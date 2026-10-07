"""
21_validate_all_primary_cells.py
=================================
Independent verification of all 24 primary established-date historical models
(2 products x 3 outcomes x {GH2014, KE2014, NG2018, POOLED_ESTABLISHED}),
generalising 20_validate_pooled_estimate.py (which covered one cell: water,
HAZ, pooled). Same method: sample rebuilt from analysis_candidates_RESTRICTED
.parquet (not the stored model dataset), estimated with linearmodels.PanelOLS
(a different library/code path from 16_estimate_preliminary.py's hand-written
weighted-demeaning estimator), country-local-reference birth-year dummies,
child age-in-months included, equal-country-total PERWEIGHT.

Audit context (2026-10-07): the prior independent-validation coverage was
3 cells (17_validate_estimates.py, country-specific) + 1 cell (20, pooled
water-HAZ) = 4 of 24 primary cells. This script extends coverage to all 24,
closing the largest single verification gap named in
docs/provenance/independent_audit_v1_2026-10-07/03_issue_register.md (B-05).

PRELIMINARY - measurement-weight documentation and final design review still
pending for the extension as a whole; this script validates implementation
correctness, not that pending documentation.
"""
import json
import os
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

warnings.filterwarnings("ignore", category=UserWarning)

SRC = "data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet"
STORED_CSV = "data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join("data/processed/estimation", f"all_primary_independent_validation_{STAMP}")
os.makedirs(OUT, exist_ok=False)
PRELIM = ("PRELIMINARY - independent verification of all 24 primary established-date "
          "historical models. Validates implementation; does not resolve the "
          "extension's pending measurement-weight and product-definition issues.")

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
record(f"=== {STAMP} independent verification: all 24 primary established-date cells ===")
raw = pd.read_parquet(SRC)
record(f"analysis candidates loaded: {len(raw)} rows, {raw.shape[1]} columns")

stored = pd.read_csv(STORED_CSV)
stored = stored[(stored.family == "primary") & (stored.window == "post_12m") & (stored.weighted == True)]  # noqa: E712
record(f"stored primary post_12m weighted rows: {len(stored)} (expect 24)")

SAMPLE_GROUPS = {
    "GH2014": [28806.0], "KE2014": [40406.0], "NG2018": [56606.0],
    "POOLED_ESTABLISHED": [28806.0, 40406.0, 56606.0],
}

results_rows = []

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
                record(f"{product} {outcome} {group_name}: empty sample, skipped")
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

            try:
                mod = PanelOLS(y, X, weights=w, entity_effects=True, drop_absorbed=True)
                res = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True)
                beta = float(res.params["E10"]); se = float(res.std_errors["E10"])
                ci = res.conf_int().loc["E10"]; p = float(res.pvalues["E10"])
            except Exception as e:
                record(f"{product} {outcome} {group_name}: ESTIMATION FAILED: {e}")
                continue

            srow = stored[(stored["product"] == product) & (stored.outcome == outcome)
                           & (stored.sample_group == group_name)]
            if len(srow) == 1:
                sr = srow.iloc[0]
                beta_diff = abs(beta - sr.beta_per_10)
                se_diff = abs(se - sr.se_per_10)
                n_match = N == int(sr.N)
                g_match = G == int(sr.G_clusters)
                status = "estimated"
            else:
                beta_diff = se_diff = None
                n_match = g_match = False
                status = f"no_unique_stored_row(found {len(srow)})"

            row = {
                "product": product, "outcome": outcome, "sample_group": group_name,
                "N": N, "G_clusters": G, "beta_per_10_independent": round(beta, 6),
                "se_per_10_independent": round(se, 6),
                "ci95_low_per_10_independent": round(float(ci.iloc[0]), 6),
                "ci95_high_per_10_independent": round(float(ci.iloc[1]), 6),
                "p_value_independent": p,
                "beta_per_10_stored": float(srow.beta_per_10.iloc[0]) if len(srow) == 1 else None,
                "se_per_10_stored": float(srow.se_per_10.iloc[0]) if len(srow) == 1 else None,
                "N_stored": int(srow.N.iloc[0]) if len(srow) == 1 else None,
                "G_clusters_stored": int(srow.G_clusters.iloc[0]) if len(srow) == 1 else None,
                "beta_abs_diff": beta_diff, "se_abs_diff": se_diff,
                "N_match": n_match, "G_match": g_match, "status": status,
            }
            results_rows.append(row)
            record(f"{product} {outcome} {group_name}: beta_per_10={beta:.6f} (stored "
                   f"{row['beta_per_10_stored']}), diff={beta_diff}, N={N}(stored {row['N_stored']}), "
                   f"G={G}(stored {row['G_clusters_stored']}) N_match={n_match} G_match={g_match}")

results_df = pd.DataFrame(results_rows)
results_df.to_csv(os.path.join(OUT, "all_primary_cells_independent_AGGREGATE.csv"), index=False)
with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))

summary = {
    "label": PRELIM,
    "cells_attempted": len(results_df),
    "cells_with_matched_stored_row": int((results_df.status == "estimated").sum()),
    "all_N_match": bool(results_df.N_match.all()),
    "all_G_match": bool(results_df.G_match.all()),
    "max_beta_abs_diff": float(results_df.beta_abs_diff.max()) if results_df.beta_abs_diff.notna().any() else None,
    "max_se_abs_diff": float(results_df.se_abs_diff.max()) if results_df.se_abs_diff.notna().any() else None,
    "mean_beta_abs_diff": float(results_df.beta_abs_diff.mean()) if results_df.beta_abs_diff.notna().any() else None,
}
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1, default=str)
record("\n=== SUMMARY ===")
record(json.dumps(summary, indent=1, default=str))
print(f"\nOutput written to {OUT}")
