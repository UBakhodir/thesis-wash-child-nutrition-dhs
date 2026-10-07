"""
16_validate_region_fe_and_joint_models_independent.py
=======================================================
INDEPENDENT AUDIT SCRIPT - not part of the frozen Steps 00-13 pipeline, and
not part of the development Step 14 script. Written to cross-check two
specific cells that a prior, separate audit left unreproduced:

  (1) Model A - household WASH + country_admin_region FE
      (outputs/household_community_wash/02_household_region_fe.csv,
      sample_variant == "A1_natural_sample")
  (2) Model C - household + community WASH jointly, region FE, common
      sample (outputs/household_community_wash/05_joint_household_community.csv)

Both of these are built in
scripts/dhs_harmonization/14_household_community_wash_models.py via
`run_explicit_wls()`, i.e. statsmodels.WLS with an EXPLICIT dummy-encoded
country_admin_region fixed effect block, cov_type="cluster" clustered on
country_psu (CRV1, use_correction=True, the statsmodels default finite-
sample correction).

This script independently reproduces the headline water-HAZ and
sanitation-HAZ cells for BOTH models using a DIFFERENT estimator:
`linearmodels.PanelOLS` with entity_effects=True (region FE absorbed by
within-transformation, NOT explicit dummy columns) and
cov_type="clustered", cluster_entity=False, clusters=country_psu (i.e.
clustering by an arbitrary variable that is NOT the absorbed effect, so
linearmodels' standard CRV1 covariance applies with no auto_df ambiguity -
region FE and PSU clustering are two distinct groupings here, unlike the
Model-B same-cluster case already adjudicated elsewhere).

Sample, weights, and exposure/control construction are REBUILT HERE from
the raw Step-10 parquet, independently (not by importing Step 11/12/14's
sample-construction functions), following the documented logic in Step 14's
own comments/docstrings and in docs/empirical_strategy.md:
  - weight: "model-specific, equal-total-country-weight" pooled weight,
    weight_model_i = weight_original_i / sum(weight_original over the
    SAME country within the estimation sample).
  - household water/sanitation binary: water_category/sanitation_collapsed_core
    mapped {"Improved":1, "Unimproved"/"NonImproved":0, "SurfaceWater":0},
    with "Unknown"/"StructuralNotApplicable"/"UnclassifiedBioDigester" -> NaN.
  - FE: country_admin_region (country-specific admin region codes).
  - cluster: country_psu.
  - controls: b19_raw, birth_order_raw, maternal_age, household_size_raw
    (continuous); child_sex, maternal_education, literacy, wealth_quintile,
    residence (categorical, reference levels as in Step 11).

Writes ONLY to data/processed/_audit_scratch/ (gitignored/local-only - this
output contains no new microdata, just coefficient tables, but is kept out
of outputs/ to avoid any appearance of being an authoritative pipeline
output) and prints a comparison table to stdout. Never writes under
outputs/, never imports or executes any pipeline script's __main__ block,
never modifies any existing file.
"""

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

pd.set_option("display.width", 200)

PROJECT_ROOT = r"C:\Users\user\Documents\Graduation_Thesis"
INPUT_PATH = PROJECT_ROOT + r"\data\processed\pooled_kr_four_country_birth_order.parquet"
STORED_A_PATH = r"C:\Users\user\Documents\Graduation_Thesis\thesis-wash-child-nutrition-dhs\outputs\household_community_wash\02_household_region_fe.csv"
STORED_C_PATH = r"C:\Users\user\Documents\Graduation_Thesis\thesis-wash-child-nutrition-dhs\outputs\household_community_wash\05_joint_household_community.csv"

OUT_DIR = PROJECT_ROOT + r"\data\processed\_audit_scratch"
import os
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 90)
print("Loading Step-10 analytical parquet (same file Step 11/14 read)")
print("=" * 90)
df = pd.read_parquet(INPUT_PATH)
print("shape:", df.shape)
assert df.shape == (70231, 90), f"Unexpected shape {df.shape}"

# ----------------------------------------------------------------------
# Household WASH binary indicators (rebuilt independently; same mapping
# documented in scripts/dhs_harmonization/12_robustness.py
# build_household_wash_indicators(), verified by reading that function's
# source rather than importing/executing it)
# ----------------------------------------------------------------------
water_map = {"Improved": 1.0, "Unimproved": 0.0, "SurfaceWater": 0.0}
sanitation_map = {"Improved": 1.0, "NonImproved": 0.0}
df["_water_hh_binary"] = df["water_category"].map(water_map)
df["_sani_hh_binary"] = df["sanitation_collapsed_core"].map(sanitation_map)

# sanity: excluded states must map to NaN, never to a real binary value
excluded_water = df["water_category"].isin(["Unknown", "StructuralNotApplicable"])
assert df.loc[excluded_water, "_water_hh_binary"].isna().all()
excluded_san = df["sanitation_collapsed_core"].isin(
    ["Unknown", "StructuralNotApplicable", "UnclassifiedBioDigester"]
)
assert df.loc[excluded_san, "_sani_hh_binary"].isna().all()
print("Household WASH binary indicators rebuilt and sanity-checked (independent of Step 12).")

HOUSEHOLD_EXPOSURES = ["_water_hh_binary", "_sani_hh_binary"]
COMMUNITY_EXPOSURES = ["water_rate_loo", "sanitation_rate_loo_core"]

CHILD_CONT = ["b19_raw", "birth_order_raw"]
CHILD_CAT = {"child_sex": "Male"}
SES_CONT = ["maternal_age", "household_size_raw"]
SES_CAT = {
    "maternal_education": "No education",
    "literacy": "Cannot read at all",
    "wealth_quintile": "Poorest",
    "residence": "Rural",
}
FE_VAR = "country_admin_region"
CLUSTER_VAR = "country_psu"
OUTCOME = "haz"  # headline outcome for this spot-check; see note at bottom for waz/whz

ALL_CAT = {**CHILD_CAT, **SES_CAT}
BASELINE_CONT = CHILD_CONT + SES_CONT


def build_sample_mask(frame, exposures):
    required = (
        exposures + BASELINE_CONT + list(ALL_CAT) + [FE_VAR, CLUSTER_VAR, "weight_original", "country"]
    )
    mask = frame[OUTCOME].notna()
    for v in required:
        mask &= frame[v].notna()
    mask &= frame["weight_original"] > 0
    return mask


def build_pooled_weight(sample_df):
    """Model-specific, equal-total-country-weight pooled weight, rebuilt
    independently from the documented formula in Step 14's
    build_temporary_pooled_weight() docstring:
        weight_model_i = weight_original_i / W_k, W_k = sum(weight_original)
        over country k's rows IN THIS SAMPLE.
    """
    w_k = sample_df.groupby("country")["weight_original"].transform("sum")
    w = sample_df["weight_original"] / w_k
    sums = sample_df.assign(_w=w).groupby("country")["_w"].sum()
    assert np.allclose(sums.values, 1.0, atol=1e-9), sums.to_dict()
    return w


def build_dummies(series, ref_level, prefix):
    observed = series.unique()
    assert ref_level in observed, f"{prefix}: ref {ref_level!r} not observed"
    dummies = pd.get_dummies(series, prefix=prefix, drop_first=False)
    ref_col = f"{prefix}_{ref_level}"
    return dummies.drop(columns=[ref_col]).astype(float)


def run_panelols(sample_df, exposures, label):
    """Region-FE model via linearmodels.PanelOLS entity_effects=True
    (absorption via within-transform, NOT explicit dummy columns - the
    deliberately DIFFERENT estimator from Step 14's run_explicit_wls()).
    Clustering on country_psu, a variable DISTINCT from the absorbed
    region effect, so PanelOLS's standard clustered-CRV1 covariance
    applies cleanly (no same-grouping auto_df ambiguity as in the
    Model-B cluster-FE case)."""
    work = sample_df.copy()
    w = build_pooled_weight(work)
    work["_w"] = w.values

    cat_blocks = []
    for cat_var, ref in ALL_CAT.items():
        cat_blocks.append(build_dummies(work[cat_var], ref, cat_var))
    X = pd.concat([work[exposures + BASELINE_CONT].astype(float)] + cat_blocks, axis=1)
    X = X.set_index(pd.MultiIndex.from_arrays(
        [work[FE_VAR].values, work.index.values], names=["entity", "time"]
    ))
    y = work[OUTCOME].astype(float)
    y.index = X.index
    w_panel = work["_w"]
    w_panel.index = X.index
    clusters = work[CLUSTER_VAR]
    clusters.index = X.index

    mod = PanelOLS(y, X, weights=w_panel, entity_effects=True, drop_absorbed=True)
    res = mod.fit(cov_type="clustered", clusters=clusters)

    n_clusters = int(work[CLUSTER_VAR].nunique())
    n_regions = int(work[FE_VAR].nunique())
    print(f"\n[{label}] PanelOLS N={int(res.nobs)} entities(regions)={n_regions} "
          f"clusters(country_psu)={n_clusters} rank={res.df_model}")
    return res, work


# ============================================================================
# MODEL A: household WASH + region FE, natural sample (A1)
# ============================================================================
print("\n" + "=" * 90 + "\nMODEL A - household WASH + region FE (PanelOLS, entity_effects=region)\n" + "=" * 90)
mask_a = build_sample_mask(df, HOUSEHOLD_EXPOSURES)
sample_a = df[mask_a].copy()
res_a, work_a = run_panelols(sample_a, HOUSEHOLD_EXPOSURES, "Model A / haz / A1 natural sample")

stored_a = pd.read_csv(STORED_A_PATH)
stored_a_sub = stored_a[(stored_a["sample_variant"] == "A1_natural_sample") & (stored_a["outcome"] == OUTCOME)]

rows_out = []
for term in HOUSEHOLD_EXPOSURES:
    b_new = res_a.params[term]
    se_new = res_a.std_errors[term]
    ci = res_a.conf_int().loc[term]
    p_new = res_a.pvalues[term]
    stored_row = stored_a_sub[stored_a_sub["term"] == term].iloc[0]
    print(f"\n  TERM = {term}")
    print(f"    stored (explicit-dummy WLS, statsmodels):  "
          f"coef={stored_row['coefficient']:.6f} se={stored_row['standard_error']:.6f} "
          f"ci=[{stored_row['ci_lower']:.6f},{stored_row['ci_upper']:.6f}] p={stored_row['p_value']:.6f} "
          f"N={int(stored_row['estimation_n'])} psu={int(stored_row['psu_count'])}")
    print(f"    independent (PanelOLS, entity-FE):          "
          f"coef={b_new:.6f} se={se_new:.6f} ci=[{ci['lower']:.6f},{ci['upper']:.6f}] p={p_new:.6f} "
          f"N={int(res_a.nobs)} psu={int(work_a[CLUSTER_VAR].nunique())}")
    print(f"    |diff| coef={abs(b_new - stored_row['coefficient']):.2e} se={abs(se_new - stored_row['standard_error']):.2e}")
    rows_out.append({
        "model": "A_household_region_fe", "term": term,
        "stored_coef": stored_row["coefficient"], "new_coef": b_new, "diff_coef": b_new - stored_row["coefficient"],
        "stored_se": stored_row["standard_error"], "new_se": se_new, "diff_se": se_new - stored_row["standard_error"],
        "stored_p": stored_row["p_value"], "new_p": p_new,
        "stored_N": int(stored_row["estimation_n"]), "new_N": int(res_a.nobs),
        "stored_psu": int(stored_row["psu_count"]), "new_psu": int(work_a[CLUSTER_VAR].nunique()),
    })

# ============================================================================
# MODEL C: household + community WASH joint, region FE, common sample
# ============================================================================
print("\n" + "=" * 90 + "\nMODEL C - joint household+community WASH + region FE (PanelOLS)\n" + "=" * 90)
JOINT_EXPOSURES = HOUSEHOLD_EXPOSURES + COMMUNITY_EXPOSURES
mask_c = build_sample_mask(df, JOINT_EXPOSURES)
sample_c = df[mask_c].copy()
res_c, work_c = run_panelols(sample_c, JOINT_EXPOSURES, "Model C / haz / common sample")

stored_c = pd.read_csv(STORED_C_PATH)
stored_c_sub = stored_c[stored_c["outcome"] == OUTCOME]

for term in JOINT_EXPOSURES:
    b_new = res_c.params[term]
    se_new = res_c.std_errors[term]
    ci = res_c.conf_int().loc[term]
    p_new = res_c.pvalues[term]
    stored_row = stored_c_sub[stored_c_sub["term"] == term].iloc[0]
    print(f"\n  TERM = {term}")
    print(f"    stored (explicit-dummy WLS, statsmodels):  "
          f"coef={stored_row['coefficient']:.6f} se={stored_row['standard_error']:.6f} "
          f"ci=[{stored_row['ci_lower']:.6f},{stored_row['ci_upper']:.6f}] p={stored_row['p_value']:.6f} "
          f"N={int(stored_row['estimation_n'])} psu={int(stored_row['psu_count'])}")
    print(f"    independent (PanelOLS, entity-FE):          "
          f"coef={b_new:.6f} se={se_new:.6f} ci=[{ci['lower']:.6f},{ci['upper']:.6f}] p={p_new:.6f} "
          f"N={int(res_c.nobs)} psu={int(work_c[CLUSTER_VAR].nunique())}")
    print(f"    |diff| coef={abs(b_new - stored_row['coefficient']):.2e} se={abs(se_new - stored_row['standard_error']):.2e}")
    rows_out.append({
        "model": "C_joint_household_community", "term": term,
        "stored_coef": stored_row["coefficient"], "new_coef": b_new, "diff_coef": b_new - stored_row["coefficient"],
        "stored_se": stored_row["standard_error"], "new_se": se_new, "diff_se": se_new - stored_row["standard_error"],
        "stored_p": stored_row["p_value"], "new_p": p_new,
        "stored_N": int(stored_row["estimation_n"]), "new_N": int(res_c.nobs),
        "stored_psu": int(stored_row["psu_count"]), "new_psu": int(work_c[CLUSTER_VAR].nunique()),
    })

out_df = pd.DataFrame(rows_out)
out_path = os.path.join(OUT_DIR, "16_region_fe_joint_model_independent_validation.csv")
out_df.to_csv(out_path, index=False)
print("\n" + "=" * 90)
print(f"Wrote comparison table: {out_path}")
print(out_df.to_string())
