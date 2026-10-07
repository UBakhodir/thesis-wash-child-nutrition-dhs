"""
20_validate_pooled_estimate.py
===============================
Independent verification of the headline pooled historical-WASH estimate: established-
date sample (Ghana 2014, Kenya 2014, Nigeria 2018), weighted, water (W_IMP), HAZ,
post_12m window. The prior independent check (17_validate_estimates.py) covered four
representative COUNTRY-specific models; it did not cover the pooled model. This script:

  (a) rebuilds the estimation sample itself, directly from the analysis-sample stage
      output (analysis_candidates_RESTRICTED.parquet), not from the estimation run's
      stored primary_model_datasets_RESTRICTED.parquet, applying every filtering step
      explicitly and logging the row counts at each step;
  (b) estimates with linearmodels.PanelOLS (entity effects = cluster, clustered CRV1),
      a different library and code path from 16_estimate_preliminary.py's hand-written
      weighted group-demeaning estimator;
  (c) reports both the auto_df (PRIMARY, same-group convention) and non-auto_df
      (FULL_DUMMY-style sensitivity) clustered standard errors, labelled accordingly;
  (d) estimates the unweighted counterpart on exactly the same final observations;
  (e) reports the coefficient per 1 residual-exposure-SD alongside the per-10-point
      coefficient, and states the ratio between them.

Development note (kept for honesty, not pride): the first version of this script omitted
the child's own age-in-months (age_m) as a linear control and coded the country-by-
birth-year terms with a single pooled reference cell instead of a separate reference
year per country. That version gave beta_per_10 = 1.385 against the stored 1.026, a
~35% gap, despite N, G, and the exposure mean/SD matching exactly -- which is what
pointed at a specification difference rather than a sample-construction error. Matching
16_estimate_preliminary.py's design_matrix() exactly (age_m included; one birth-year
dummy set per country, each with its own local reference year) closed the gap to
6.7e-08 on the coefficient and 3.6e-05 on the standard error. This is recorded here,
not to inflate the result, but because an independent check that can silently acquire
its own bugs is not independent verification -- the discrepancy and its resolution are
part of what this script verifies.

PRELIMINARY - measurement-weight documentation and final design review still pending
for the extension as a whole; this script validates implementation, not that pending
documentation.

ADDENDUM (2026-10-07, pass 4): the 3.6e-05 SE gap noted above is now fully explained,
not residual noise -- this script's .fit() call omits linearmodels' separate, opt-in
`group_debias=True` flag, which supplies part of the small-sample cluster correction
16_estimate_preliminary.py's hand-written formula applies. Adding that flag closes the
gap to 0.0 at 8 decimal places for this cell (and all 23 others). See
scripts/historical_wash/24_reconcile_inference_corrections.py and
docs/provenance/independent_audit_v1_2026-10-07/09_update_2026-10-07_pass4.md.
"""
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

SRC = "data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join("data/processed/estimation", f"pooled_independent_validation_{STAMP}")
os.makedirs(OUT, exist_ok=False)
PRELIM = ("PRELIMINARY - independent verification of the pooled headline water-HAZ "
          "estimate. Validates implementation; does not resolve the extension's "
          "pending measurement-weight and product-definition issues.")

SAMPLE_COUNTRY = {28806.0: "GH2014", 40406.0: "KE2014", 56606.0: "NG2018"}

STORED = {  # from data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv, row id m0004
    "beta_per_10": 1.025553, "se_per_10": 0.260730, "ci95_low_per_10": 0.514332,
    "ci95_high_per_10": 1.536774, "p_value": 0.000086, "N": 23018, "G_clusters": 3114,
    "K_regressors": 24, "rank": 24, "E_residual_sd_after_controls": 0.428348,
}

log = []
def record(msg):
    log.append(str(msg))
    print(msg)

record(f"=== {STAMP} independent pooled-model verification ===")
record(f"source: {SRC}")

cols = ["SAMPLE", "candidate", "W_IMP_post_12m_complete_status", "W_IMP_post_12m_complete_exposure",
        "HAZ_valid", "HAZ_universe", "HAZ_z", "PERWEIGHT", "cluster_key", "record_number",
        "KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_reported", "age_cal_candidate"]
d = pd.read_parquet(SRC, columns=cols)
record(f"step 0 (raw candidates loaded): {len(d)} rows")

d = d[d["SAMPLE"].isin(SAMPLE_COUNTRY)].copy()
d["country"] = d["SAMPLE"].map(SAMPLE_COUNTRY)
record(f"step 1 (established-country SAMPLE restriction): {len(d)} rows; countries = {sorted(d.country.unique())}")
assert set(d.country.unique()) == {"GH2014", "KE2014", "NG2018"}, "country set mismatch after SAMPLE restriction"

bad_candidate = int((d.candidate != "GREGORIAN_ESTABLISHED").sum())
record(f"step 2 check: rows with non-GREGORIAN_ESTABLISHED candidate label despite established SAMPLE: {bad_candidate}")
d = d[d.candidate == "GREGORIAN_ESTABLISHED"].copy()
record(f"step 2 (candidate == GREGORIAN_ESTABLISHED): {len(d)} rows")

dupe = int(d.duplicated("record_number").sum())
record(f"step 3 check: duplicate record_number count: {dupe}")
assert dupe == 0, "record_number is not a unique key within the established sample"

d = d[d["W_IMP_post_12m_complete_status"] == "eligible_complete"].copy()
record(f"step 4 (complete postnatal window + complete spatial coverage): {len(d)} rows")

d = d[(d.HAZ_valid == True) & (d.HAZ_universe == True)].copy()  # noqa: E712
record(f"step 5 (HAZ valid and within measured universe): {len(d)} rows")

# Child's own age in completed months: reported where delivered, else the documented
# calendar-month difference (matches 16_estimate_preliminary.py's age_mode="reported_first").
d["age_m"] = np.where(d["age_reported"].notna(), d["age_reported"], d["age_cal_candidate"]).astype(float)

covs = ["KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_m"]
before = len(d)
d = d.dropna(subset=covs + ["W_IMP_post_12m_complete_exposure", "PERWEIGHT", "cluster_key"])
record(f"step 6 (complete-case on covariates incl. child age_m, exposure, weight, cluster key): {before} -> {len(d)}")

sizes = d.groupby("cluster_key").size()
singleton_clusters = sizes[sizes < 2].index
before_n, before_g = len(d), d.cluster_key.nunique()
d = d[~d.cluster_key.isin(singleton_clusters)].copy()
record(f"step 7 (drop singleton clusters): clusters dropped = {len(singleton_clusters)}, "
       f"obs dropped = {before_n - len(d)}, clusters {before_g} -> {d.cluster_key.nunique()}")

N = len(d)
G = d.cluster_key.nunique()
record(f"final estimation sample: N={N}, G={G}")

multi_country_clusters = int((d.groupby("cluster_key").country.nunique() > 1).sum())
record(f"check: cluster_key maps to more than one country for {multi_country_clusters} clusters (expect 0)")
assert multi_country_clusters == 0

K_countries = d.country.nunique()
country_perweight_sum = d.groupby("country").PERWEIGHT.sum()
target_total = N / K_countries
d["w"] = d["PERWEIGHT"] * target_total / d["country"].map(country_perweight_sum)
wt_check = d.groupby("country").w.sum()
record(f"equal-country weight totals in THIS estimation sample (target {target_total:.6f} each): "
       f"{wt_check.round(6).to_dict()}")
assert np.allclose(wt_check.values, target_total, rtol=1e-8), "weight totals do not equal N/K in this sample"

d["E10"] = d["W_IMP_post_12m_complete_exposure"] / 10.0
record(f"exposure E (0-100 scale): mean={d['W_IMP_post_12m_complete_exposure'].mean():.4f}, "
       f"sd={d['W_IMP_post_12m_complete_exposure'].std():.4f}, "
       f"min={d['W_IMP_post_12m_complete_exposure'].min():.4f}, max={d['W_IMP_post_12m_complete_exposure'].max():.4f}")

record(f"b_year range {int(d.b_year.min())}-{int(d.b_year.max())}")

d["KIDSEX"] = d["KIDSEX"].astype(int).astype(str)
d["EDUCLVL"] = d["EDUCLVL"].astype(int).astype(str)
d["MARSTAT"] = d["MARSTAT"].astype(int).astype(str)

d = d.sort_values(["cluster_key", "record_number"]).reset_index(drop=True)
d["t_idx"] = d.groupby("cluster_key").cumcount()
panel = d.set_index(["cluster_key", "t_idx"])

dummies = pd.get_dummies(panel[["KIDSEX", "EDUCLVL", "MARSTAT"]], drop_first=True)

# Survey-qualified country-by-birth-year terms: each country gets its OWN set of
# birth-year dummies relative to that country's own (lowest) birth year, matching
# 16_estimate_preliminary.py's design_matrix(). This is NOT the same as one combined
# "country_byear" categorical with a single global reference cell: since cluster FE
# already fully absorbs anything constant within a cluster (and every cluster belongs
# to exactly one country), a single-global-reference coding leaves two extra columns
# that are collinear with the cluster FE (confirmed by PanelOLS's own
# AbsorbingEffectWarning in the first run of this script) and changes which comparisons
# are attributed to the birth-year terms versus left for the cluster FE to absorb.
byear_dummies = []
byear_names = []
for smp in sorted(panel["country"].unique()):
    yrs = sorted(panel.loc[panel["country"] == smp, "b_year"].unique())
    for yv in yrs[1:]:
        col = ((panel["country"] == smp) & (panel["b_year"] == yv)).astype(float)
        byear_dummies.append(col)
        byear_names.append(f"by_{smp}_{int(yv)}")
byear_df = pd.concat(byear_dummies, axis=1)
byear_df.columns = byear_names
record(f"country-local-reference birth-year dummies: {len(byear_names)} "
       f"(one reference year withheld per country, matching 16_estimate_preliminary.py)")

X = pd.concat([panel[["E10", "age_m", "AGE"]], dummies, byear_df], axis=1).astype(float)
y = panel["HAZ_z"].astype(float)
w = panel["w"].astype(float)

rank = int(np.linalg.matrix_rank(X.to_numpy()))
record(f"design matrix: {X.shape[1]} regressors (excluding absorbed cluster FE), rank={rank}")

def fit_and_report(weights, label, auto_df):
    mod = PanelOLS(y, X, weights=weights, entity_effects=True, drop_absorbed=True)
    res = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=auto_df)
    beta = float(res.params["E10"])
    se = float(res.std_errors["E10"])
    ci = res.conf_int().loc["E10"]
    p = float(res.pvalues["E10"])
    record(f"-- {label} (auto_df={auto_df}) -- beta_per_10={beta:.6f} se={se:.6f} "
           f"CI=[{float(ci.iloc[0]):.6f}, {float(ci.iloc[1]):.6f}] p={p:.6f} "
           f"N={int(res.nobs)} df_resid={res.df_resid}")
    return {"label": label, "auto_df": auto_df, "beta_per_10": beta, "se_per_10": se,
            "ci95_low_per_10": float(ci.iloc[0]), "ci95_high_per_10": float(ci.iloc[1]),
            "p_value": p, "N": int(res.nobs), "G_clusters": G}

results = []
results.append(fit_and_report(w, "weighted_PRIMARY_same_cluster_CRV1", auto_df=True))
results.append(fit_and_report(w, "weighted_FULL_DUMMY_DF_SENSITIVITY", auto_df=False))
results.append(fit_and_report(pd.Series(1.0, index=panel.index), "unweighted_same_observations_PRIMARY", auto_df=True))

# Residual exposure SD after controls: residualize E10 on the other regressors + cluster FE (weighted), independent of the main fit
other_X = X.drop(columns=["E10"])
mod_e = PanelOLS(X["E10"], other_X, weights=w, entity_effects=True, drop_absorbed=True)
res_e = mod_e.fit(cov_type="clustered", cluster_entity=True, auto_df=True)
# res_e.resids are the within-cluster residuals of E10 (E/10) after partialling out
# the other controls; convert back to percentage-point units.
e_resid_sd_points = float(res_e.resids.std()) * 10.0
record(f"independent residual exposure SD after controls (percentage points): {e_resid_sd_points:.6f} "
       f"(stored value: {STORED['E_residual_sd_after_controls']})")

primary = results[0]
effect_per_residual_sd = primary["beta_per_10"] / 10.0 * e_resid_sd_points
ten_point_vs_residual_sd_ratio = 10.0 / e_resid_sd_points
record(f"effect per 1 residual-exposure-SD (HAZ units): {effect_per_residual_sd:.6f}")
record(f"a 10-percentage-point contrast is {ten_point_vs_residual_sd_ratio:.2f}x the residual within-cluster exposure SD "
       f"({e_resid_sd_points:.4f} points) -- the reported beta_per_10 is a scaling convention, not an observed "
       f"typical within-cluster contrast.")

comparison = {
    "stored": STORED,
    "independent_primary": results[0],
    "independent_full_dummy_df_sensitivity": results[1],
    "independent_unweighted_same_observations": results[2],
    "beta_match_abs_diff": abs(results[0]["beta_per_10"] - STORED["beta_per_10"]),
    "se_match_abs_diff": abs(results[0]["se_per_10"] - STORED["se_per_10"]),
    "N_match": results[0]["N"] == STORED["N"],
    "G_match": results[0]["G_clusters"] == STORED["G_clusters"],
    "rank_match": rank == STORED["rank"],
    "independent_residual_exposure_sd_points": e_resid_sd_points,
    "stored_residual_exposure_sd_points": STORED["E_residual_sd_after_controls"],
    "effect_per_1_residual_sd_haz_units": effect_per_residual_sd,
    "ten_point_contrast_vs_residual_sd_ratio": ten_point_vs_residual_sd_ratio,
}
record(json.dumps(comparison, indent=1, default=str))

with open(os.path.join(OUT, "comparison_summary.json"), "w", encoding="utf-8") as f:
    json.dump({"label": PRELIM, **comparison}, f, indent=1, default=str)
with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
pd.DataFrame(results).to_csv(os.path.join(OUT, "independent_estimates_AGGREGATE.csv"), index=False)
print(f"\nOutput written to {OUT}")
