"""
24_reconcile_inference_corrections.py
=======================================
Reconciles the small, previously unexplained SE/CI/p-value differences
between 16_estimate_preliminary.py (the authoritative pipeline) and
21_validate_all_primary_cells.py (the independent re-estimation), for all
24 primary established-date historical cells. Written in response to a
direct instruction not to label these differences "numerical noise" without
demonstrating what explains them.

16_estimate_preliminary.py's CRV1 implementation (read directly, lines
157-237): weighted within-cluster (IDHSPSU) demeaning: the cluster IS the
fixed effect, absorbed by demeaning and not counted in K (the project's own
"same-group, no-double-penalty" convention). Its small-sample scalar
correction, applied to the raw sandwich B @ meat @ B:

    corr = (G / (G - 1)) * ((N - 1) / (N - K))

with CIs/p-values from a Student's t distribution on G-1 degrees of freedom.

21_validate_all_primary_cells.py calls:

    mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True)

Reading the installed linearmodels 7.0 source directly
(.venv/Lib/site-packages/linearmodels/panel/{model,covariance}.py;
.venv/Lib/site-packages/linearmodels/shared/covariance.py):

- `auto_df=True` with entity effects nested inside the cluster variable
  (same-group case, confirmed via `_determine_df_adjustment` /
  `_is_effect_nested`) sets `extra_df=0` -- i.e. it correctly implements the
  SAME same-group, no-double-penalty convention as the hand-written
  estimator for the *degrees-of-freedom* side. This much was already
  verified in the prior pass.
- BUT `ClusteredCovariance`'s small-sample correction has TWO independent
  pieces: (1) a `debiased` scale, `nobs / (nobs - extra_df - nvar)` =
  N / (N - K) with extra_df=0, applied automatically whenever `debiased=True`
  (PanelOLS.fit's own default); and (2) a *separate*, opt-in
  `group_debias=True` flag applying `group_debias_coefficient(clusters)` =
  (G / (G - 1)) * ((N - 1) / N) (linearmodels/shared/covariance.py lines
  16-42) -- NOT enabled by default, and NOT passed by
  21_validate_all_primary_cells.py's `.fit()` call.

Multiplying both pieces together: [N/(N-K)] * [(G/(G-1))*(N-1)/N]
  = (G/(G-1)) * (N-1)/(N-K)
-- algebraically IDENTICAL to 16's declared `corr` formula. So the SE
discrepancy observed in the prior pass is explained, precisely: script 21
was missing `group_debias=True`, applying only the N/(N-K) debiased-residual
scale and NOT the (G/(G-1))*((N-1)/N) cluster-count small-sample adjustment.
This is a real, identified, fixable omission in the *validation* script's
covariance configuration -- not a property of the authoritative pipeline,
and not "numerical noise."

This script re-fits all 24 cells (same sample-construction code as script 21,
copied verbatim for this exact purpose) three ways and reports the result:
  (a) cov_type="clustered", cluster_entity=True, auto_df=True            [script 21's original config, reproduced here for a same-run comparison]
  (b) + group_debias=True                                               [the corrected config: declared formula now identical to 16's]
  (c) raw/uncorrected: debiased=False, group_debias=False, extra_df=0    [isolates the covariance FORMULA from the correction scalars entirely]
for every one of the 24 cells, against the stored authoritative SE/CI/p.

No authoritative result is touched. Output is a new, separate validation run.
"""
import json
import os
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS
from scipy import stats

warnings.filterwarnings("ignore", category=UserWarning)

SRC = "data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet"
STORED_CSV = "data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join("data/processed/estimation", f"inference_reconciliation_{STAMP}")
os.makedirs(OUT, exist_ok=False)

SAMPLE_COUNTRY = {28806.0: "GH2014", 40406.0: "KE2014", 56606.0: "NG2018"}
OUTCOME_Z = {"HAZ": "HAZ_z", "WAZ": "WAZ_z", "WHZ": "WHZ_z"}
OUTCOME_VALID = {"HAZ": "HAZ_valid", "WAZ": "WAZ_valid", "WHZ": "WHZ_valid"}
OUTCOME_UNIV = {"HAZ": "HAZ_universe", "WAZ": "WAZ_universe", "WHZ": "WHZ_universe"}

log = []
def record(msg):
    log.append(str(msg))
    print(msg)


BASE_COLS = ["SAMPLE", "candidate", "PERWEIGHT", "cluster_key", "record_number",
             "KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_reported", "age_cal_candidate"]
record(f"=== {STAMP} inference-correction reconciliation: all 24 primary established-date cells ===")
raw = pd.read_parquet(SRC)

stored = pd.read_csv(STORED_CSV)
stored = stored[(stored.family == "primary") & (stored.window == "post_12m") & (stored.weighted == True)]  # noqa: E712
record(f"stored primary post_12m weighted rows: {len(stored)} (expect 24)")

SAMPLE_GROUPS = {
    "GH2014": [28806.0], "KE2014": [40406.0], "NG2018": [56606.0],
    "POOLED_ESTABLISHED": [28806.0, 40406.0, 56606.0],
}

rows = []

for product in ["W_IMP", "S_IMP"]:
    exp_col = f"{product}_post_12m_complete_exposure"
    status_col = f"{product}_post_12m_complete_status"
    for outcome in ["HAZ", "WAZ", "WHZ"]:
        zcol, validcol, univcol = OUTCOME_Z[outcome], OUTCOME_VALID[outcome], OUTCOME_UNIV[outcome]
        for group_name, sample_codes in SAMPLE_GROUPS.items():
            cols = BASE_COLS + [exp_col, status_col, zcol, validcol, univcol]
            d = raw[cols].copy()
            d = d[d["SAMPLE"].isin(sample_codes)].copy()
            d["country"] = d["SAMPLE"].map(SAMPLE_COUNTRY)
            d = d[d.candidate == "GREGORIAN_ESTABLISHED"].copy()
            d = d[d[status_col] == "eligible_complete"].copy()
            d = d[(d[validcol] == True) & (d[univcol] == True)].copy()  # noqa: E712
            d["age_m"] = np.where(d["age_reported"].notna(), d["age_reported"], d["age_cal_candidate"]).astype(float)
            covs = ["KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_m"]
            d = d.dropna(subset=covs + [exp_col, "PERWEIGHT", "cluster_key"])
            sizes = d.groupby("cluster_key").size()
            d = d[~d.cluster_key.isin(sizes[sizes < 2].index)].copy()

            N, G = len(d), d.cluster_key.nunique()
            K_countries = d.country.nunique()
            if N == 0 or G == 0:
                continue
            country_sum = d.groupby("country").PERWEIGHT.sum()
            target = N / K_countries
            d["w"] = d["PERWEIGHT"] * target / d["country"].map(country_sum)
            d["E10"] = d[exp_col] / 10.0

            d["KIDSEX"] = d["KIDSEX"].astype(int).astype(str)
            d["EDUCLVL"] = d["EDUCLVL"].astype(int).astype(str)
            d["MARSTAT"] = d["MARSTAT"].astype(int).astype(str)
            d = d.sort_values(["cluster_key", "record_number"]).reset_index(drop=True)
            d["t_idx"] = d.groupby("cluster_key").cumcount()
            panel = d.set_index(["cluster_key", "t_idx"])

            dummies = pd.get_dummies(panel[["KIDSEX", "EDUCLVL", "MARSTAT"]], drop_first=True)
            byear_cols, byear_names = [], []
            for smp in sorted(panel["country"].unique()):
                yrs = sorted(panel.loc[panel["country"] == smp, "b_year"].unique())
                for yv in yrs[1:]:
                    byear_cols.append(((panel["country"] == smp) & (panel["b_year"] == yv)).astype(float))
                    byear_names.append(f"by_{smp}_{int(yv)}")
            byear_df = pd.concat(byear_cols, axis=1) if byear_cols else pd.DataFrame(index=panel.index)
            if len(byear_names):
                byear_df.columns = byear_names

            X = pd.concat([panel[["E10", "age_m", "AGE"]], dummies, byear_df], axis=1).astype(float)
            y = panel[zcol].astype(float)
            w = panel["w"].astype(float)

            srow = stored[(stored["product"] == product) & (stored.outcome == outcome)
                           & (stored.sample_group == group_name)]
            if len(srow) != 1:
                continue
            sr = srow.iloc[0]

            mod = PanelOLS(y, X, weights=w, entity_effects=True, drop_absorbed=True)

            res_a = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True)
            res_b = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True, group_debias=True)
            res_c = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True,
                             debiased=False, group_debias=False)

            se_a = float(res_a.std_errors["E10"])
            se_b = float(res_b.std_errors["E10"])
            se_c_raw = float(res_c.std_errors["E10"])  # uncorrected sandwich SE

            beta = float(res_a.params["E10"])  # identical across all three configs (point estimate unaffected)
            K = int(res_a.df_model) if hasattr(res_a, "df_model") else None

            # manual check: does se_c_raw * sqrt((G/(G-1))*((N-1)/(N-K))) == se_a (debiased=True, group_debias=False)?
            # se_a's correction is only the debiased scale N/(N-K); se_b's is the full (G/(G-1))*(N-1)/(N-K).
            k_eff = X.shape[1]  # columns actually fit (post drop_absorbed); matches K_regressors/rank already confirmed equal
            manual_scale_a = np.sqrt(N / (N - k_eff))
            manual_scale_b = np.sqrt((G / (G - 1)) * ((N - 1) / (N - k_eff)))
            se_c_scaled_to_a = se_c_raw * manual_scale_a
            se_c_scaled_to_b = se_c_raw * manual_scale_b

            row = {
                "product": product, "outcome": outcome, "sample_group": group_name,
                "N": N, "G": G, "k_eff": k_eff,
                "se_stored_handrolled": float(sr.se_per_10),
                "se_a_auto_df_only": round(se_a, 8),
                "se_b_auto_df_plus_group_debias": round(se_b, 8),
                "se_c_raw_uncorrected": round(se_c_raw, 8),
                "diff_a_vs_stored": round(abs(se_a - sr.se_per_10), 8),
                "diff_b_vs_stored": round(abs(se_b - sr.se_per_10), 8),
                "se_c_scaled_to_a_check": round(se_c_scaled_to_a, 8),  # should equal se_a
                "se_c_scaled_to_b_check": round(se_c_scaled_to_b, 8),  # should equal se_b
                "algebra_check_a_resid": round(abs(se_c_scaled_to_a - se_a), 10),
                "algebra_check_b_resid": round(abs(se_c_scaled_to_b - se_b), 10),
            }
            rows.append(row)
            record(f"{product} {outcome} {group_name}: stored={row['se_stored_handrolled']:.6f} "
                   f"auto_df_only={se_a:.6f} (diff {row['diff_a_vs_stored']:.6f}) "
                   f"+group_debias={se_b:.6f} (diff {row['diff_b_vs_stored']:.8f})")

results_df = pd.DataFrame(rows)
results_df.to_csv(os.path.join(OUT, "inference_reconciliation_AGGREGATE.csv"), index=False)

summary = {
    "max_diff_a_auto_df_only_vs_stored": float(results_df.diff_a_vs_stored.max()),
    "max_diff_b_auto_df_plus_group_debias_vs_stored": float(results_df.diff_b_vs_stored.max()),
    "mean_diff_a": float(results_df.diff_a_vs_stored.mean()),
    "mean_diff_b": float(results_df.diff_b_vs_stored.mean()),
    "max_algebra_check_a_residual": float(results_df.algebra_check_a_resid.max()),
    "max_algebra_check_b_residual": float(results_df.algebra_check_b_resid.max()),
}
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
record("\n=== SUMMARY ===")
record(json.dumps(summary, indent=1))
print(f"\nOutput written to {OUT}")
