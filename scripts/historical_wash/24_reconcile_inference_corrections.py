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
copied verbatim for this exact purpose) three ways:
  (a) cov_type="clustered", cluster_entity=True, auto_df=True            [script 21's original config, reproduced here for a same-run comparison]
  (b) + group_debias=True                                               [the corrected config: declared formula now identical to 16's]
  (c) raw/uncorrected: debiased=False, group_debias=False, extra_df=0    [isolates the covariance FORMULA from the correction scalars entirely]
for every one of the 24 cells, against the stored authoritative SE/CI/p.

ADDENDUM (2026-10-07, second pass): extends the comparison from SE alone to
CI and p-value, computed EXPLICITLY from the corrected (config-b) SE using a
Student's t distribution on G-1 degrees of freedom -- 16_estimate_preliminary
.py's own declared reference distribution (lines 212, 225) -- rather than
trusting linearmodels' own `res.conf_int()`/`res.pvalues`. This distinction
matters: reading `linearmodels/panel/results.py` directly shows its CI/p
machinery uses `self.df_resid` (`nobs - df_model`, where `df_model` counts
the *full* absorbed-entity-effect count regardless of the same-group
covariance exemption), not G-1. For a small-G cell (e.g. Ghana, G=353) these
differ enough to matter: t.ppf(0.975, 352) = 1.96673 vs. t.ppf(0.975, 1572)
(an illustrative df_resid magnitude) = 1.96147, a ~0.27% difference in the
critical value alone -- large enough to reopen a small CI/p discrepancy even
after the SE itself is fully reconciled, if the wrong reference distribution
were used. This script reports both: the manually-matched t(G-1) CI/p (which
should now reconcile closely) and linearmodels' own native CI/p (which may
not), so the two are not conflated.

Full-precision absolute AND relative differences are saved (not rounded
before computing the difference); explicit numerical tolerances are stated
in the output, distinguishing "exact" (floating-point-level, ~1e-9 or
smaller -- consistent with two implementations solving literally the same
algebra) from "rounded agreement" (matches only at the thesis's own reported
display precision, e.g. 2-3 significant figures) from a genuine, unexplained
residual discrepancy (neither).

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

            # manual check: does se_c_raw * sqrt((G/(G-1))*((N-1)/(N-K))) == se_a (debiased=True, group_debias=False)?
            # se_a's correction is only the debiased scale N/(N-K); se_b's is the full (G/(G-1))*(N-1)/(N-K).
            k_eff = X.shape[1]  # columns actually fit (post drop_absorbed); matches K_regressors/rank already confirmed equal
            manual_scale_a = np.sqrt(N / (N - k_eff))
            manual_scale_b = np.sqrt((G / (G - 1)) * ((N - 1) / (N - k_eff)))
            se_c_scaled_to_a = se_c_raw * manual_scale_a
            se_c_scaled_to_b = se_c_raw * manual_scale_b

            # --- CI/p-value, computed EXPLICITLY with Student's t on G-1 df ---
            # (16_estimate_preliminary.py's own declared reference distribution;
            # NOT linearmodels' res_b.conf_int()/pvalues, which use df_resid =
            # nobs - df_model, a different and generally much larger df -- see
            # the module docstring addendum for why this distinction matters.)
            tcrit_g1 = float(stats.t.ppf(0.975, G - 1))
            ci_low_manual = beta - tcrit_g1 * se_b
            ci_high_manual = beta + tcrit_g1 * se_b
            p_manual = float(2 * stats.t.sf(abs(beta / se_b), G - 1)) if se_b > 0 else float("nan")

            # linearmodels' own native CI/p from the corrected (config-b) fit,
            # for explicit comparison -- NOT assumed equal to the manual ones.
            ci_native = res_b.conf_int().loc["E10"]
            ci_low_native = float(ci_native.iloc[0])
            ci_high_native = float(ci_native.iloc[1])
            p_native = float(res_b.pvalues["E10"])
            df_resid_native = float(res_b.df_resid)

            se_stored = float(sr.se_per_10)
            ci_low_stored = float(sr.ci95_low_per_10)
            ci_high_stored = float(sr.ci95_high_per_10)
            p_stored = float(sr.p_value)

            def abs_rel(a, b):
                d = abs(a - b)
                rel = d / abs(b) if b != 0 else float("nan")
                return d, rel

            se_a_abs, se_a_rel = abs_rel(se_a, se_stored)
            se_b_abs, se_b_rel = abs_rel(se_b, se_stored)
            ci_low_manual_abs, ci_low_manual_rel = abs_rel(ci_low_manual, ci_low_stored)
            ci_high_manual_abs, ci_high_manual_rel = abs_rel(ci_high_manual, ci_high_stored)
            p_manual_abs, p_manual_rel = abs_rel(p_manual, p_stored)
            ci_low_native_abs, _ = abs_rel(ci_low_native, ci_low_stored)
            ci_high_native_abs, _ = abs_rel(ci_high_native, ci_high_stored)
            p_native_abs, _ = abs_rel(p_native, p_stored)

            row = {
                "product": product, "outcome": outcome, "sample_group": group_name,
                "N": N, "G": G, "k_eff": k_eff, "tcrit_g1": tcrit_g1,
                "df_resid_native_linearmodels": df_resid_native,
                "beta": beta,
                "se_stored": se_stored, "se_a_auto_df_only": se_a, "se_b_group_debias": se_b,
                "se_c_raw_uncorrected": se_c_raw,
                "se_a_abs_diff": se_a_abs, "se_a_rel_diff": se_a_rel,
                "se_b_abs_diff": se_b_abs, "se_b_rel_diff": se_b_rel,
                "se_c_scaled_to_a_check": se_c_scaled_to_a, "se_c_scaled_to_b_check": se_c_scaled_to_b,
                "algebra_check_a_resid": abs(se_c_scaled_to_a - se_a),
                "algebra_check_b_resid": abs(se_c_scaled_to_b - se_b),
                "ci_low_stored": ci_low_stored, "ci_high_stored": ci_high_stored, "p_stored": p_stored,
                "ci_low_manual_tG1": ci_low_manual, "ci_high_manual_tG1": ci_high_manual, "p_manual_tG1": p_manual,
                "ci_low_manual_abs_diff": ci_low_manual_abs, "ci_low_manual_rel_diff": ci_low_manual_rel,
                "ci_high_manual_abs_diff": ci_high_manual_abs, "ci_high_manual_rel_diff": ci_high_manual_rel,
                "p_manual_abs_diff": p_manual_abs, "p_manual_rel_diff": p_manual_rel,
                "ci_low_native_linearmodels": ci_low_native, "ci_high_native_linearmodels": ci_high_native,
                "p_native_linearmodels": p_native,
                "ci_low_native_abs_diff": ci_low_native_abs, "ci_high_native_abs_diff": ci_high_native_abs,
                "p_native_abs_diff": p_native_abs,
            }
            rows.append(row)
            record(f"{product} {outcome} {group_name}: G={G} stored_se={se_stored:.6f} "
                   f"auto_df_only={se_a:.6f} (abs_diff {se_a_abs:.6f}) "
                   f"+group_debias={se_b:.6f} (abs_diff {se_b_abs:.3e}, rel_diff {se_b_rel:.3e}) | "
                   f"p_manual_tG1={p_manual:.6f} (abs_diff {p_manual_abs:.3e}) vs "
                   f"p_native_lm={p_native:.6f} (abs_diff {p_native_abs:.3e}, df_resid_native={df_resid_native:.0f})")

results_df = pd.DataFrame(rows)
results_df.to_csv(os.path.join(OUT, "inference_reconciliation_AGGREGATE.csv"), index=False)

# --- Explicit numerical-tolerance classification ---
# "exact": floating-point-level agreement (<=1e-9 absolute), consistent with
#   two independent implementations solving literally the same algebra up to
#   accumulation-order/numerical-method noise.
# "rounded_agreement": not floating-point-exact, but agrees at the precision
#   this thesis actually reports its numbers to (2 decimal places for beta/CI,
#   3 decimal places for p, i.e. <=0.005 absolute on beta/CI, <=0.0005 on p).
# "discrepant": neither -- a genuine, unexplained residual difference.
EXACT_TOL = 1e-9
ROUNDED_TOL_COEF = 0.005   # beta, CI bounds reported to 2 dp in the manuscript
ROUNDED_TOL_P = 0.0005     # p reported to 3 dp in the manuscript

def classify(diffs, tol_round):
    out = []
    for d in diffs:
        if d <= EXACT_TOL:
            out.append("exact")
        elif d <= tol_round:
            out.append("rounded_agreement")
        else:
            out.append("discrepant")
    return out

results_df["se_b_class"] = classify(results_df.se_b_abs_diff, ROUNDED_TOL_COEF)
results_df["ci_low_manual_class"] = classify(results_df.ci_low_manual_abs_diff, ROUNDED_TOL_COEF)
results_df["ci_high_manual_class"] = classify(results_df.ci_high_manual_abs_diff, ROUNDED_TOL_COEF)
results_df["p_manual_class"] = classify(results_df.p_manual_abs_diff, ROUNDED_TOL_P)
results_df["ci_low_native_class"] = classify(results_df.ci_low_native_abs_diff, ROUNDED_TOL_COEF)
results_df["ci_high_native_class"] = classify(results_df.ci_high_native_abs_diff, ROUNDED_TOL_COEF)
results_df["p_native_class"] = classify(results_df.p_native_abs_diff, ROUNDED_TOL_P)
results_df.to_csv(os.path.join(OUT, "inference_reconciliation_AGGREGATE.csv"), index=False)

summary = {
    "tolerances": {
        "exact_abs_tol": EXACT_TOL,
        "rounded_agreement_abs_tol_coef_and_ci": ROUNDED_TOL_COEF,
        "rounded_agreement_abs_tol_p": ROUNDED_TOL_P,
    },
    "se_a_auto_df_only": {
        "max_abs_diff_vs_stored": float(results_df.se_a_abs_diff.max()),
        "mean_abs_diff_vs_stored": float(results_df.se_a_abs_diff.mean()),
        "max_rel_diff_vs_stored": float(results_df.se_a_rel_diff.max()),
    },
    "se_b_group_debias_corrected": {
        "max_abs_diff_vs_stored": float(results_df.se_b_abs_diff.max()),
        "mean_abs_diff_vs_stored": float(results_df.se_b_abs_diff.mean()),
        "max_rel_diff_vs_stored": float(results_df.se_b_rel_diff.max()),
        "class_counts": results_df.se_b_class.value_counts().to_dict(),
    },
    "ci_p_manual_tG1_vs_stored": {
        "max_abs_diff_ci_low": float(results_df.ci_low_manual_abs_diff.max()),
        "max_abs_diff_ci_high": float(results_df.ci_high_manual_abs_diff.max()),
        "max_abs_diff_p": float(results_df.p_manual_abs_diff.max()),
        "max_rel_diff_ci_low": float(results_df.ci_low_manual_rel_diff.max()),
        "max_rel_diff_ci_high": float(results_df.ci_high_manual_rel_diff.max()),
        "max_rel_diff_p": float(results_df.p_manual_rel_diff.max()),
        "ci_low_class_counts": results_df.ci_low_manual_class.value_counts().to_dict(),
        "ci_high_class_counts": results_df.ci_high_manual_class.value_counts().to_dict(),
        "p_class_counts": results_df.p_manual_class.value_counts().to_dict(),
    },
    "ci_p_native_linearmodels_vs_stored_FOR_COMPARISON_ONLY": {
        "note": "Uses linearmodels' own df_resid (nobs - df_model), NOT G-1. "
                "Shown to demonstrate why the manual t(G-1) recomputation above "
                "is necessary rather than trusting res.conf_int()/res.pvalues.",
        "max_abs_diff_ci_low": float(results_df.ci_low_native_abs_diff.max()),
        "max_abs_diff_ci_high": float(results_df.ci_high_native_abs_diff.max()),
        "max_abs_diff_p": float(results_df.p_native_abs_diff.max()),
        "ci_low_class_counts": results_df.ci_low_native_class.value_counts().to_dict(),
        "ci_high_class_counts": results_df.ci_high_native_class.value_counts().to_dict(),
        "p_class_counts": results_df.p_native_class.value_counts().to_dict(),
        "df_resid_native_range": [float(results_df.df_resid_native_linearmodels.min()),
                                   float(results_df.df_resid_native_linearmodels.max())],
        "tcrit_g1_range": [float(results_df.tcrit_g1.min()), float(results_df.tcrit_g1.max())],
    },
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
