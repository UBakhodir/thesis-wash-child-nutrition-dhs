"""
14_household_community_wash_models.py
=======================================
DEVELOPMENT STAGE (post-audit). NOT part of the frozen Steps 00-13
pipeline. Additive only: reads the same Step-10 analytical dataset Step 11
reads, and reuses Step 11/12's own design-matrix, weighting, dummy-encoding
and rank-check machinery (imported, never copied/modified) to estimate an
extended set of household- and community-WASH specifications:

  A. Household WASH + country_admin_region FE
  B. Household WASH + country_psu (cluster) FE, via a weighted within
     (demeaning) transformation, validated against explicit-dummy WLS
  C. Household + community WASH jointly (+ region FE)
  D. The existing community Model 4, re-estimated on a COMMON comparison
     sample shared with A-C, for a fair side-by-side comparison
  E. Flexible (age-in-month FE) vs linear age, for A/B/D
  F. Household WASH x age-band interactions (region FE and cluster FE)
  G. A structured block diagnostic of the Nigeria sanitation->HAZ sign
     reversal (M1-M4 reproduction + sequential/leave-one-out SES blocks)
  H. Anthropometric-availability (selection) descriptive diagnostic
  I. Country-specific household+region-FE and household+cluster-FE models

This script:
  - never imports/executes any script's __main__ block
  - never writes to data/, outputs/final_tables/, outputs/final_figures/,
    outputs/regressions/, outputs/final_appendix/, or any Steps 00-13 file
  - writes ONLY under outputs/household_community_wash/
  - does not choose any specification based on significance
"""

import hashlib
import importlib.util
import io
import itertools
import os
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

SCRIPT_DIR = Path(__file__).resolve().parent


def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Reuse Step 11 / Step 12's own machinery - never re-implemented, never
# executed via __main__ (both files guard their heavy work behind
# `if __name__ == "__main__":`, so importing only defines functions/consts).
reg = _load_module("11_main_regressions.py", "dhs_main_regressions")
rob = _load_module("12_robustness.py", "dhs_robustness")
config = reg.config

# Canonical output directory, unless overridden for validation-only scratch
# runs via THESIS_STEP14_OUT_DIR (e.g. a temp directory outside the repo).
# When the environment variable is unset, behavior is byte-identical to the
# original hard-coded path - this override exists solely so a corrected
# version of this script can be validated against a scratch location before
# any canonical output is replaced.
_out_dir_override = os.environ.get("THESIS_STEP14_OUT_DIR")
OUT_DIR = Path(_out_dir_override) if _out_dir_override else (config.PROJECT_ROOT / "outputs" / "household_community_wash")
OUT_DIR.mkdir(parents=True, exist_ok=False)  # hard-fail if it already exists - never silently reuse/overwrite

LOG_PATH = OUT_DIR / "run_log.txt"
_log_f = io.open(LOG_PATH, "w", encoding="utf-8")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    _log_f.write(s + "\n")


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================
# BASELINE FILE HASHES (recorded BEFORE any development estimation runs)
# ============================================================================
BASELINE_FILES = {
    "step11_main_regressions_script": SCRIPT_DIR / "11_main_regressions.py",
    "step12_robustness_script": SCRIPT_DIR / "12_robustness.py",
    "main_continuous_models_output": config.PROJECT_ROOT / "outputs" / "regressions" / "main_continuous_models.csv",
    "robustness_household_wash_output": config.PROJECT_ROOT / "outputs" / "regressions" / "robustness_household_wash.csv",
}
baseline_hashes_before = {k: sha256_of_file(p) for k, p in BASELINE_FILES.items()}
log("=" * 90)
log("BASELINE FILE SHA-256 HASHES (recorded before development estimation)")
log("=" * 90)
for k, v in baseline_hashes_before.items():
    log(f"  {k}: {v}  ({BASELINE_FILES[k]})")

# ============================================================================
# PART 0: LOAD + PRE-RUN VALIDATION
# ============================================================================
log("\n" + "=" * 90 + "\nPART 0: LOAD + PRE-RUN VALIDATION\n" + "=" * 90)

INPUT_PATH = reg.INPUT_PATH  # identical file Step 11 reads - data/processed/pooled_kr_four_country_birth_order.parquet
df = pd.read_parquet(INPUT_PATH)
log(f"Loaded: {INPUT_PATH}  shape={df.shape}")
if df.shape != (reg.EXPECTED_TOTAL_ROWS, reg.EXPECTED_STEP10_COLS):
    raise RuntimeError(f"Unexpected input shape {df.shape}. STOP.")
for country, n in reg.EXPECTED_ROW_COUNTS.items():
    if (df["country"] == country).sum() != n:
        raise RuntimeError(f"[{country}] row count mismatch vs frozen baseline. STOP.")
log("Shape and per-country row counts match the frozen Step-10 baseline exactly.")

# 1. Reconstruct current Model-4 sample logic via Step 11's OWN function
haz_mask_m4 = reg.build_estimation_sample(df, "haz")
waz_mask_m4 = reg.build_estimation_sample(df, "waz")
whz_mask_m4 = reg.build_estimation_sample(df, "whz")
log(f"Reconstructed Model-4 masks via reg.build_estimation_sample(): "
    f"haz N={haz_mask_m4.sum()}, waz N={waz_mask_m4.sum()}, whz N={whz_mask_m4.sum()}")
if int(haz_mask_m4.sum()) != 36985 or int(waz_mask_m4.sum()) != 37260 or int(whz_mask_m4.sum()) != 37088:
    raise RuntimeError(
        f"DISCREPANCY vs prior audit: reconstructed N's "
        f"(haz={int(haz_mask_m4.sum())}, waz={int(waz_mask_m4.sum())}, whz={int(whz_mask_m4.sum())}) "
        "do not match the audit's reported 36985/37260/37088. STOPPING per instructions rather than "
        "forcing the implementation."
    )
log("Model-4 N's match the prior audit exactly (haz=36985, waz=37260, whz=37088). No discrepancy.")

# 2. country_child_id uniqueness
if df["country_child_id"].duplicated().any() or df["country_child_id"].isna().any():
    raise RuntimeError("Duplicate/null country_child_id found. STOP.")
log("country_child_id: unique and non-null across all 70,231 rows.")

# 3. Outcome direction sanity (not re-deriving the mapping, just sanity-checking sign convention)
for oc in ["haz", "waz", "whz"]:
    s = df[oc].dropna()
    log(f"  {oc}: mean={s.mean():.4f} median={s.median():.4f} min={s.min():.2f} max={s.max():.2f} "
        f"(negative mean consistent with SSA stunting/underweight burden; direction not reversed)")

# 4. Household WASH coding - build binary indicators via Step 12's OWN function (never re-implemented)
water_hh, sani_hh = rob.build_household_wash_indicators(df)
df["_water_hh_binary"] = water_hh
df["_sani_hh_binary"] = sani_hh
log(f"Household water binary: {df['_water_hh_binary'].value_counts(dropna=False).to_dict()}")
log(f"Household sanitation binary: {df['_sani_hh_binary'].value_counts(dropna=False).to_dict()}")
if not set(df["_water_hh_binary"].dropna().unique()) <= {0.0, 1.0}:
    raise RuntimeError("Household water binary contains a value outside {0,1,NaN}. STOP.")
if not set(df["_sani_hh_binary"].dropna().unique()) <= {0.0, 1.0}:
    raise RuntimeError("Household sanitation binary contains a value outside {0,1,NaN}. STOP.")
log("Household WASH binary coding: passed (values restricted to {0.0, 1.0, NaN}).")

# 5. Community LOO coding - range check
for col in ["water_rate_loo", "sanitation_rate_loo_core"]:
    valid = df[col].dropna()
    if ((valid < 0) | (valid > 1)).any():
        raise RuntimeError(f"{col}: value(s) outside [0,1]. STOP.")
log("Community LOO exposures: all non-missing values in [0,1]. Confirmed, not assumed.")

# 6. country_psu nested within country_admin_region (hard requirement for Part 3's "drop region FE" claim)
nested_check = df.groupby("country_psu")["country_admin_region"].nunique()
if (nested_check > 1).any():
    bad = nested_check[nested_check > 1]
    raise RuntimeError(f"country_psu is NOT nested within country_admin_region for {len(bad)} PSU(s). STOP - "
                        "Part 3's justification for dropping region FE under cluster FE would be invalid.")
log(f"Nesting check: every one of {nested_check.shape[0]} country_psu values maps to exactly ONE "
    "country_admin_region. Confirmed by direct computation, not assumed.")

# 7. Age range 0-59
if df["b19_raw"].min() < 0 or df["b19_raw"].max() > 59:
    raise RuntimeError(f"b19_raw out of expected [0,59] range: min={df['b19_raw'].min()} max={df['b19_raw'].max()}. STOP.")
log(f"b19_raw range: [{df['b19_raw'].min()}, {df['b19_raw'].max()}] - confirmed within [0,59].")

# 8. No impossible exposure values already covered in (5); repeat for household as sanity
log("Impossible-value checks: passed for all four WASH exposure variables.")

log("\nPART 0: ALL PRE-RUN VALIDATION CHECKS PASSED. Proceeding to estimation.")

# ============================================================================
# SHARED CONSTANTS (aliases into Step 11's approved objects - never redefined)
# ============================================================================
PRIMARY_OUTCOMES = reg.PRIMARY_OUTCOMES  # ["haz","waz","whz"]
CHILD_CONTROLS_CONTINUOUS = reg.CHILD_CONTROLS_CONTINUOUS       # ["b19_raw","birth_order_raw"]
CHILD_CONTROLS_CATEGORICAL = reg.CHILD_CONTROLS_CATEGORICAL     # {"child_sex":"Male"}
SES_CONTROLS_CONTINUOUS = reg.SES_CONTROLS_CONTINUOUS
SES_CONTROLS_CATEGORICAL = reg.SES_CONTROLS_CATEGORICAL
FE_VAR = reg.FE_VAR  # "country_admin_region"
MODEL4_CONTINUOUS = reg.MODEL4_CONTINUOUS
MODEL4_CATEGORICAL = reg.MODEL4_CATEGORICAL
EXPOSURES = reg.EXPOSURES  # ["water_rate_loo","sanitation_rate_loo_core"]
HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS = rob.HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS  # child+ses continuous only

HOUSEHOLD_EXPOSURES = ["_water_hh_binary", "_sani_hh_binary"]

# ----------------------------------------------------------------------
# CLUSTER-FE-SPECIFIC CONTROL SET: `residence` (urban/rural) must be
# EXCLUDED from every country_psu-cluster-FE specification. Verified
# empirically (not assumed) below in Part 3, first run: every one of the
# 4,481 DHS PSUs in this dataset is 100% urban OR 100% rural with ZERO
# exceptions (df.groupby('country_psu')['residence'].nunique().max() == 1).
# This is DHS's own cluster/EA sampling-frame design, not a data error.
# Consequently `residence` has exactly zero within-cluster variation
# everywhere, and a weighted-demeaned design matrix that still includes it
# is exactly rank-deficient (confirmed via SVD: the sole near-zero
# singular value's null vector loads at 1.0 on residence_Urban and 0.0 on
# every other column). It is therefore dropped ONLY from cluster-FE
# models; it remains in every region-FE model (Model A, Model C, the
# common-sample community model), where it is fully identified because
# clusters within the same admin region do vary in urban/rural status.
# ----------------------------------------------------------------------
CLUSTER_FE_SES_CATEGORICAL = {k: v for k, v in SES_CONTROLS_CATEGORICAL.items() if k != "residence"}
CLUSTER_FE_CATEGORICAL = {**CHILD_CONTROLS_CATEGORICAL, **CLUSTER_FE_SES_CATEGORICAL}
log(f"\nCLUSTER-FE CONTROL-SET ADJUSTMENT: 'residence' excluded from all country_psu-cluster-FE "
    f"models. Verified: every one of 4,481 DHS PSUs is 100% urban or 100% rural (0 exceptions) - "
    f"'residence' has zero within-cluster variation by DHS's own sampling design and is exactly "
    f"absorbed by cluster FE. All other controls unchanged. Cluster-FE categorical set: "
    f"{list(CLUSTER_FE_CATEGORICAL.keys())} (region-FE models keep the full set: "
    f"{list(MODEL4_CATEGORICAL.keys())}).")

RESULT_COLUMNS = [
    "development_family", "model_label", "outcome", "sample_variant", "term",
    "coefficient", "standard_error", "ci_lower", "ci_upper", "p_value",
    "estimation_n", "psu_count", "fe_region_count", "weight_method",
    "clustering_method", "se_note",
]


# ============================================================================
# GENERIC HELPERS (built ONLY from Step 11's exported primitives)
# ============================================================================

def build_raw_design(sample_df, continuous_vars, categorical_vars_with_ref):
    """Design matrix WITHOUT a constant and WITHOUT any FE block - reuses
    reg.build_categorical_dummies() for every categorical term."""
    parts = []
    if continuous_vars:
        parts.append(sample_df[continuous_vars].astype(float))
    ref_metadata = {}
    for cat_var, ref_level in categorical_vars_with_ref.items():
        dummies, ref_col = reg.build_categorical_dummies(sample_df[cat_var], ref_level, cat_var)
        parts.append(dummies)
        ref_metadata[cat_var] = {"reference": ref_level, "reference_column": ref_col}
    X = pd.concat(parts, axis=1) if parts else pd.DataFrame(index=sample_df.index)
    return X, ref_metadata


def build_design_explicit_fe(sample_df, continuous_vars, categorical_vars_with_ref, fe_col, fe_ref=None):
    """Explicit-dummy design matrix (constant + covariates + FE dummies) for
    an ARBITRARY fe_col (e.g. country_psu) - generalizes reg.build_design_matrix,
    which is hardcoded to FE_VAR=country_admin_region, to any grouping column."""
    X_raw, ref_metadata = build_raw_design(sample_df, continuous_vars, categorical_vars_with_ref)
    if fe_ref is None:
        fe_ref = sorted(sample_df[fe_col].unique())[0]
    fe_dummies, fe_ref_col = reg.build_categorical_dummies(sample_df[fe_col], fe_ref, fe_col)
    X = pd.concat([X_raw, fe_dummies], axis=1)
    X = sm.add_constant(X, has_constant="add")
    ref_metadata[fe_col] = {"reference": fe_ref, "reference_column": fe_ref_col}
    return X, ref_metadata


def rows_from_fit(res, outcome, family, model_label, sample_variant, weight_method,
                   clustering_method, psu_count, fe_region_count, se_note="baseline cluster-robust SE (statsmodels default)"):
    ci = res.conf_int()
    rows = []
    for term in res.params.index:
        rows.append({
            "development_family": family, "model_label": model_label, "outcome": outcome,
            "sample_variant": sample_variant, "term": term,
            "coefficient": res.params[term], "standard_error": res.bse[term],
            "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res.pvalues[term],
            "estimation_n": int(res.nobs), "psu_count": psu_count, "fe_region_count": fe_region_count,
            "weight_method": weight_method, "clustering_method": clustering_method, "se_note": se_note,
        })
    return rows


def run_explicit_wls(label, sample_df, outcome, continuous_vars, categorical_vars_with_ref,
                      weight_series, cluster_series, include_fe=False, fe_col=None, fe_ref=None):
    """Standard explicit-dummy WLS (region FE or no FE) - statsmodels' native
    cov_type='cluster' df-correction is CORRECT here because every FE dummy
    is an explicit column in X, so k_params is accurate."""
    if include_fe:
        X, ref_metadata = build_design_explicit_fe(sample_df, continuous_vars, categorical_vars_with_ref, fe_col, fe_ref)
    else:
        X_raw, ref_metadata = build_raw_design(sample_df, continuous_vars, categorical_vars_with_ref)
        X = sm.add_constant(X_raw, has_constant="add")

    rank = np.linalg.matrix_rank(X.values)
    if rank != X.shape[1]:
        raise RuntimeError(f"[{label}] Design matrix RANK-DEFICIENT: rank={rank} cols={X.shape[1]}. STOP.")

    y = sample_df[outcome].astype(float)
    w = weight_series.astype(float)
    if not (w > 0).all() or not np.all(np.isfinite(w.values)):
        raise RuntimeError(f"[{label}] Weight vector invalid (non-positive/non-finite). STOP.")

    model = sm.WLS(y, X, weights=w)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": cluster_series})
    if not np.all(np.isfinite(res.params.values)) or not np.all(np.isfinite(res.bse.values)):
        raise RuntimeError(f"[{label}] Non-finite coefficient/SE. STOP.")
    return res, ref_metadata


def weighted_demean(sample_df, cluster_col, weight_col, value_cols):
    """Weighted within-cluster demeaning: v_tilde_i = v_i - [sum(w*v)/sum(w)]
    over cluster(i). Mathematically equivalent (Frisch-Waugh-Lovell, weighted
    case) to including full explicit cluster dummies in a WLS regression -
    validated empirically below (Part 3B), not merely asserted."""
    work = sample_df[[cluster_col, weight_col] + value_cols].copy()
    wsum = work.groupby(cluster_col)[weight_col].transform("sum")
    out = {}
    for c in value_cols:
        wv = work[c].astype(float) * work[weight_col].astype(float)
        gsum = wv.groupby(work[cluster_col]).transform("sum")
        out[c] = work[c].astype(float) - (gsum / wsum)
    return out


def run_cluster_fe_demeaned(label, sample_df, outcome, continuous_vars, categorical_vars_with_ref,
                             weight_series, cluster_col):
    """Cluster-FE model via weighted demeaning. Returns (res, ref_metadata,
    k_reported, n_clusters).

    PRIMARY INFERENCE CONVENTION (adjudicated - see
    docs/provenance/cluster_fe_inference_adjudication.md): the fixed-effect
    grouping absorbed by the demeaning transform and the clustering
    grouping used for the cluster-robust covariance are the SAME PSU
    variable here. For that same-effect/same-cluster case, `res.bse`,
    `res.pvalues`, and `res.conf_int()` (statsmodels' native
    `cov_type="cluster"` output, `use_correction=True`) are the primary,
    reported inference - with NO additional penalty for the PSU effects
    absorbed by demeaning. This was cross-validated against
    `linearmodels.PanelOLS(entity_effects=True).fit(cov_type="clustered",
    cluster_entity=True, auto_df=True)` on this project's own data, which
    agrees with the native statsmodels values to 4-5 decimal places and
    explicitly documents (in its own `auto_df` docstring) that clustered
    SEs sharing their grouping variable with an absorbed effect do not
    require an extra degrees-of-freedom correction. A full-dummy-style
    sensitivity scale (treating every absorbed PSU dummy as an explicitly
    estimated parameter) remains available via
    `full_dummy_df_sensitivity_scale()` / `apply_full_dummy_df_sensitivity()`
    below, retained only as a labelled secondary sensitivity, not as the
    thesis's primary convention."""
    X_raw, ref_metadata = build_raw_design(sample_df, continuous_vars, categorical_vars_with_ref)
    work = sample_df.copy()
    work["_w"] = weight_series.values
    work["_y"] = sample_df[outcome].astype(float).values
    for c in X_raw.columns:
        work[c] = X_raw[c].values

    demeaned = weighted_demean(work, cluster_col, "_w", ["_y"] + list(X_raw.columns))
    y_t = demeaned["_y"]
    X_t = pd.DataFrame({c: demeaned[c] for c in X_raw.columns}, index=sample_df.index)
    # NO constant is added: after weighted within-cluster demeaning the intercept is not
    # identified (standard practice for a within/FE transformation - an added constant here
    # is collinear with the demeaned regressors, confirmed empirically: including one produced
    # a rank-deficient design matrix, rank = n_cols-1). Omitting it is mathematically correct,
    # not a workaround: the FE-cell-specific intercepts are exactly what demeaning absorbs.

    rank = np.linalg.matrix_rank(X_t.values)
    if rank != X_t.shape[1]:
        raise RuntimeError(f"[{label}] Demeaned design matrix RANK-DEFICIENT: rank={rank} cols={X_t.shape[1]}. STOP.")

    w = weight_series.astype(float)
    model = sm.WLS(y_t, X_t, weights=w)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": sample_df[cluster_col]})
    if not np.all(np.isfinite(res.params.values)) or not np.all(np.isfinite(res.bse.values)):
        raise RuntimeError(f"[{label}] Non-finite coefficient/SE (demeaned fit). STOP.")

    n_clusters = int(sample_df[cluster_col].nunique())
    k_reported = X_t.shape[1]  # design columns statsmodels actually sees (covariates only, no constant)

    return res, ref_metadata, k_reported, n_clusters


def full_dummy_df_sensitivity_scale(k_reported, n_clusters, N):
    """SENSITIVITY ONLY - not the thesis's primary inference convention.

    Computes the SE-scale factor that would result from treating every
    absorbed PSU dummy as an explicitly estimated parameter
    (k_full_dummy = k_reported + n_clusters), i.e. the finite-sample
    correction a full-explicit-dummy WLS fit's naive parameter count would
    imply. This double-counts degrees of freedom already accounted for by
    clustering on the same PSU variable that defines the fixed effect (see
    docs/provenance/cluster_fe_inference_adjudication.md) and is retained
    here only as a transparency/sensitivity check, never as the reported
    headline inference."""
    k_full_dummy = k_reported + n_clusters
    factor_reported = (n_clusters / (n_clusters - 1)) * ((N - 1) / (N - k_reported))
    factor_full_dummy = (n_clusters / (n_clusters - 1)) * ((N - 1) / (N - k_full_dummy))
    scale = float(np.sqrt(factor_full_dummy / factor_reported))
    return scale, k_full_dummy


def apply_full_dummy_df_sensitivity(res, scale):
    """SENSITIVITY ONLY - see full_dummy_df_sensitivity_scale(). Returns a
    (coef, se_sensitivity, ci_lo, ci_hi, p_sensitivity) tuple per term,
    rescaling SE/CI by `scale` and recomputing p from a normal
    approximation (consistent with statsmodels' own cluster-robust
    p-values, which already use a normal/t reference distribution here).
    Not the thesis's primary reported inference."""
    from scipy import stats as _stats
    out = {}
    for term in res.params.index:
        b = res.params[term]
        se0 = res.bse[term]
        se1 = se0 * scale
        z = b / se1 if se1 > 0 else np.nan
        p1 = 2 * (1 - _stats.norm.cdf(abs(z))) if np.isfinite(z) else np.nan
        ci_lo = b - 1.959963984540054 * se1
        ci_hi = b + 1.959963984540054 * se1
        out[term] = (b, se1, ci_lo, ci_hi, p1)
    return out


log("\nGeneric estimation helpers defined (explicit-dummy WLS; weighted-demeaning cluster-FE; "
    "manual finite-cluster SE correction). Proceeding to Part 1.")

# ============================================================================
# PART 1: COMMON COMPARISON SAMPLE
# ============================================================================
log("\n" + "=" * 90 + "\nPART 1: COMMON COMPARISON SAMPLE\n" + "=" * 90)

COMMON_REQUIRED_VARS = (
    HOUSEHOLD_EXPOSURES + EXPOSURES + CHILD_CONTROLS_CONTINUOUS + list(CHILD_CONTROLS_CATEGORICAL)
    + SES_CONTROLS_CONTINUOUS + list(SES_CONTROLS_CATEGORICAL) + [FE_VAR, "country_psu", "weight_original"]
)

common_masks = {}
common_samples = {}
sample_flow_rows = []
for outcome in PRIMARY_OUTCOMES:
    mask = df[outcome].notna()
    for v in COMMON_REQUIRED_VARS:
        mask &= df[v].notna()
    mask &= (df["weight_original"] > 0)
    common_masks[outcome] = mask
    samp = df[mask].copy()
    common_samples[outcome] = samp
    orig_m4_n = int(reg.build_estimation_sample(df, outcome).sum())
    by_country = samp["country"].value_counts().to_dict()
    sample_flow_rows.append({
        "outcome": outcome,
        "common_sample_n": len(samp),
        "unique_households": samp["country_household_id"].nunique(),
        "unique_psu": samp["country_psu"].nunique(),
        "unique_admin_region": samp[FE_VAR].nunique(),
        "n_ethiopia": by_country.get("ethiopia", 0),
        "n_ghana": by_country.get("ghana", 0),
        "n_kenya": by_country.get("kenya", 0),
        "n_nigeria": by_country.get("nigeria", 0),
        "original_model4_n": orig_m4_n,
        "difference_from_model4_n": len(samp) - orig_m4_n,
        "pct_of_model4_n_retained": round(100 * len(samp) / orig_m4_n, 3),
    })
    log(f"  [{outcome}] common sample N={len(samp)} (Model-4 N={orig_m4_n}, "
        f"diff={len(samp) - orig_m4_n}) unique_hh={samp['country_household_id'].nunique()} "
        f"unique_psu={samp['country_psu'].nunique()} unique_admin={samp[FE_VAR].nunique()}")

sample_flow_df = pd.DataFrame(sample_flow_rows)
sample_flow_df.to_csv(OUT_DIR / "01_development_sample_flow.csv", index=False)
log("Written: 01_development_sample_flow.csv")

# ============================================================================
# PART 2: MODEL A - HOUSEHOLD WASH + REGION FE
# ============================================================================
log("\n" + "=" * 90 + "\nPART 2: MODEL A - HOUSEHOLD WASH + REGION FE\n" + "=" * 90)

A_CONTINUOUS = HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
A_CATEGORICAL = MODEL4_CATEGORICAL

model_a_rows = []
for outcome in PRIMARY_OUTCOMES:
    mask_a1 = df[outcome].notna()
    for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(A_CATEGORICAL) + [FE_VAR, "country_psu", "weight_original"]:
        mask_a1 &= df[v].notna()
    sample_a1 = df[mask_a1].copy()
    weight_a1, _ = reg.build_temporary_pooled_weight(sample_a1)
    res_a1, ref_a1 = run_explicit_wls(f"A1-{outcome}", sample_a1, outcome, A_CONTINUOUS, A_CATEGORICAL,
                                       weight_a1, sample_a1["country_psu"], include_fe=True, fe_col=FE_VAR)
    model_a_rows += rows_from_fit(res_a1, outcome, "model_A_household_region_fe", "A1_household_natural_sample",
                                   "A1_natural_sample", "model_specific_equal_total_country_weight",
                                   "cluster_robust_country_psu", int(sample_a1["country_psu"].nunique()),
                                   int(sample_a1[FE_VAR].nunique()))
    log(f"  A1 [{outcome}] N={len(sample_a1)} PSUs={sample_a1['country_psu'].nunique()} OK")

    sample_a2 = common_samples[outcome]
    weight_a2, _ = reg.build_temporary_pooled_weight(sample_a2)
    res_a2, ref_a2 = run_explicit_wls(f"A2-{outcome}", sample_a2, outcome, A_CONTINUOUS, A_CATEGORICAL,
                                       weight_a2, sample_a2["country_psu"], include_fe=True, fe_col=FE_VAR)
    model_a_rows += rows_from_fit(res_a2, outcome, "model_A_household_region_fe", "A2_common_comparison_sample",
                                   "A2_common_sample", "model_specific_equal_total_country_weight",
                                   "cluster_robust_country_psu", int(sample_a2["country_psu"].nunique()),
                                   int(sample_a2[FE_VAR].nunique()))
    log(f"  A2 [{outcome}] N={len(sample_a2)} PSUs={sample_a2['country_psu'].nunique()} OK")

model_a_df = pd.DataFrame(model_a_rows, columns=RESULT_COLUMNS)
model_a_df.to_csv(OUT_DIR / "02_household_region_fe.csv", index=False)
log("Written: 02_household_region_fe.csv")

# ============================================================================
# PART 3: MODEL B - HOUSEHOLD WASH + CLUSTER (PSU) FE
# ============================================================================
log("\n" + "=" * 90 + "\nPART 3: MODEL B - HOUSEHOLD WASH + CLUSTER (PSU) FE\n" + "=" * 90)

B_CONTINUOUS = HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
B_CATEGORICAL = CLUSTER_FE_CATEGORICAL  # 'residence' excluded - see adjustment note above

support_rows = []
model_b_rows = []
model_b_samples = {}
for outcome in PRIMARY_OUTCOMES:
    mask_b = df[outcome].notna()
    for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(B_CATEGORICAL) + ["country_psu", "weight_original"]:
        mask_b &= df[v].notna()
    sample_b = df[mask_b].copy()
    model_b_samples[outcome] = sample_b

    hh_lvl = sample_b.drop_duplicates(subset="country_household_id")[
        ["country_household_id", "country_psu", "_water_hh_binary", "_sani_hh_binary"]
    ]
    grp = hh_lvl.groupby("country_psu")
    n_psu_total = grp.ngroups
    water_var = grp["_water_hh_binary"].nunique() > 1
    sani_var = grp["_sani_hh_binary"].nunique() > 1
    both_var = water_var & sani_var
    n_water_var = int(water_var.sum())
    n_sani_var = int(sani_var.sum())
    n_both_var = int(both_var.sum())
    children_in_water_informative = int(sample_b[sample_b["country_psu"].isin(water_var[water_var].index)].shape[0])
    children_in_sani_informative = int(sample_b[sample_b["country_psu"].isin(sani_var[sani_var].index)].shape[0])
    hh_in_water_informative = int(hh_lvl[hh_lvl["country_psu"].isin(water_var[water_var].index)].shape[0])
    hh_in_sani_informative = int(hh_lvl[hh_lvl["country_psu"].isin(sani_var[sani_var].index)].shape[0])

    support_rows.append({
        "outcome": outcome, "n_psu_total": n_psu_total,
        "n_psu_with_water_variation": n_water_var, "pct_psu_water_variation": round(100 * n_water_var / n_psu_total, 2),
        "n_psu_with_sanitation_variation": n_sani_var, "pct_psu_sanitation_variation": round(100 * n_sani_var / n_psu_total, 2),
        "n_psu_with_both_variation": n_both_var, "pct_psu_both_variation": round(100 * n_both_var / n_psu_total, 2),
        "children_in_water_informative_clusters": children_in_water_informative,
        "children_in_sanitation_informative_clusters": children_in_sani_informative,
        "households_in_water_informative_clusters": hh_in_water_informative,
        "households_in_sanitation_informative_clusters": hh_in_sani_informative,
        "total_children_in_sample": len(sample_b), "total_households_in_sample": len(hh_lvl),
    })
    log(f"  [{outcome}] support: {n_psu_total} PSUs total; water-informative {n_water_var} "
        f"({100 * n_water_var / n_psu_total:.1f}%); sanitation-informative {n_sani_var} "
        f"({100 * n_sani_var / n_psu_total:.1f}%); both {n_both_var}")

    weight_b, _ = reg.build_temporary_pooled_weight(sample_b)
    res_b, ref_b, k_rep, n_clusters = run_cluster_fe_demeaned(
        f"B-{outcome}", sample_b, outcome, B_CONTINUOUS, B_CATEGORICAL, weight_b, "country_psu"
    )
    log(f"    statsmodels res.cov_kwds for [{outcome}] Model B fit: {res_b.cov_kwds}")
    N_b = int(res_b.nobs)
    fd_scale, k_full_dummy = full_dummy_df_sensitivity_scale(k_rep, n_clusters, N_b)
    fd_scaled = apply_full_dummy_df_sensitivity(res_b, fd_scale)

    # PRIMARY: native statsmodels cluster-robust inference (cov_type="cluster",
    # use_correction=True) on the demeaned fit. The absorbed PSU fixed effect
    # and the clustering variable are the same PSU grouping, so no additional
    # degrees-of-freedom penalty is applied - see the adjudication note in
    # run_cluster_fe_demeaned()'s docstring and
    # docs/provenance/cluster_fe_inference_adjudication.md.
    model_b_rows += rows_from_fit(
        res_b, outcome, "model_B_household_cluster_fe", "natural_sample_PRIMARY_SAME_CLUSTER_CRV1",
        "natural_sample", "model_specific_equal_total_country_weight",
        "cluster_robust_country_psu_demeaned", n_clusters, 0,
        se_note=(f"PRIMARY: statsmodels native cluster-robust SE on demeaned data, use_correction=True "
                 f"(confirmed default; see res.cov_kwds in run log). k_reported={k_rep}. No additional "
                 f"absorbed-PSU-FE degrees-of-freedom penalty is applied, because the fixed-effect grouping "
                 f"and the clustering grouping are the same PSU variable (adjudicated convention; "
                 f"cross-validated against linearmodels.PanelOLS(auto_df=True) - see "
                 f"docs/provenance/cluster_fe_inference_adjudication.md). See the "
                 f"FULL_DUMMY_DF_SENSITIVITY row-set below for a labelled sensitivity check only.")
    )
    for term, (b, se1, lo, hi, p1) in fd_scaled.items():
        model_b_rows.append({
            "development_family": "model_B_household_cluster_fe", "model_label": "natural_sample_FULL_DUMMY_DF_SENSITIVITY",
            "outcome": outcome, "sample_variant": "natural_sample", "term": term,
            "coefficient": b, "standard_error": se1, "ci_lower": lo, "ci_upper": hi, "p_value": p1,
            "estimation_n": N_b, "psu_count": n_clusters, "fe_region_count": 0,
            "weight_method": "model_specific_equal_total_country_weight",
            "clustering_method": "cluster_robust_country_psu_demeaned",
            "se_note": (f"SENSITIVITY ONLY, NOT THE PRIMARY CONVENTION: scale={fd_scale:.4f} applied as if "
                        f"every one of the {n_clusters} absorbed PSU dummies were an explicitly estimated "
                        f"parameter (k_full_dummy={k_full_dummy} vs k_reported={k_rep}); p/CI recomputed from "
                        f"a normal reference distribution. Retained only for transparency - see "
                        f"docs/provenance/cluster_fe_inference_adjudication.md for why this is not used as "
                        f"the primary inference convention when FE and clustering share the same grouping."),
        })
    log(f"  B [{outcome}] N={N_b} clusters={n_clusters} k_reported={k_rep} "
        f"(full_dummy_sensitivity_scale={fd_scale:.4f}, sensitivity only) OK")

support_df = pd.DataFrame(support_rows)
support_df.to_csv(OUT_DIR / "04_household_cluster_fe_support.csv", index=False)
log("Written: 04_household_cluster_fe_support.csv")

# ============================================================================
# PART 3B: CLUSTER-FE ESTIMATOR VALIDATION
# ============================================================================
log("\n" + "=" * 90 + "\nPART 3B: CLUSTER-FE ESTIMATOR VALIDATION\n" + "=" * 90)
log("Estimator choice: weighted within-cluster demeaning (Frisch-Waugh-Lovell, weighted case), NOT "
    "explicit PSU dummies for the full pooled sample (~4,434-4,481 clusters would require a dense "
    "design matrix of order 37,000 x ~4,450 columns - computationally unsafe/slow for this task) and "
    "NOT linearmodels.PanelOLS (linearmodels IS installed - v7.0 - but avoided here for consistency "
    "with this project's own established convention, documented verbatim in 11_main_regressions.py: "
    "'NOT linearmodels.PanelOLS, NOT any artificial panel structure'). Validated below against an "
    "explicit-dummy WLS fit on a computationally tractable subset (Ghana, ~618 PSUs).")

validation_country = "ghana"
val_outcome = "haz"
mask_val = df[val_outcome].notna()
for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(B_CATEGORICAL) + ["psu"]:
    mask_val &= df[v].notna()
mask_val &= (df["country"] == validation_country)
sample_val = df[mask_val].copy()
weight_val = sample_val["weight_original"]

res_explicit, ref_explicit = run_explicit_wls(
    "VALIDATION-explicit-dummy", sample_val, val_outcome, B_CONTINUOUS, B_CATEGORICAL,
    weight_val, sample_val["psu"], include_fe=True, fe_col="psu"
)
res_demeaned, ref_demeaned, k_rep_v, n_clusters_v = run_cluster_fe_demeaned(
    "VALIDATION-demeaned", sample_val, val_outcome, B_CONTINUOUS, B_CATEGORICAL, weight_val, "psu"
)

compare_terms = HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
validation_rows = []
max_abs_diff = 0.0
for term in compare_terms:
    b_explicit = res_explicit.params[term]
    b_demeaned = res_demeaned.params[term]
    diff = abs(b_explicit - b_demeaned)
    max_abs_diff = max(max_abs_diff, diff)
    validation_rows.append({"term": term, "coef_explicit_dummy_wls": b_explicit,
                             "coef_weighted_demeaning": b_demeaned, "abs_diff": diff})
    log(f"    {term:24s} explicit={b_explicit:+.10f}  demeaned={b_demeaned:+.10f}  |diff|={diff:.2e}")

TOLERANCE = 1e-6
if max_abs_diff > TOLERANCE:
    raise RuntimeError(
        f"CLUSTER-FE ESTIMATOR VALIDATION FAILED: max |coefficient difference| = {max_abs_diff:.2e} "
        f"exceeds tolerance {TOLERANCE:.0e}. STOPPING to diagnose rather than proceeding with an "
        "unvalidated estimator, per instructions."
    )
log(f"VALIDATION PASSED: max |coefficient difference| across {len(compare_terms)} terms = "
    f"{max_abs_diff:.2e} (tolerance {TOLERANCE:.0e}). Weighted demeaning confirmed mathematically "
    f"equivalent to explicit PSU-dummy WLS on the Ghana/{val_outcome} subset "
    f"(N={int(res_explicit.nobs)}, {n_clusters_v} PSUs).")
validation_df = pd.DataFrame(validation_rows)

# append validation block into the Model-B output file so it is self-contained
for _, r in validation_df.iterrows():
    model_b_rows.append({
        "development_family": "estimator_validation", "model_label": "explicit_dummy_vs_weighted_demeaning",
        "outcome": val_outcome, "sample_variant": f"validation_subset_{validation_country}", "term": r["term"],
        "coefficient": r["coef_explicit_dummy_wls"], "standard_error": np.nan, "ci_lower": np.nan, "ci_upper": np.nan,
        "p_value": np.nan, "estimation_n": int(res_explicit.nobs), "psu_count": n_clusters_v, "fe_region_count": 0,
        "weight_method": "weight_original", "clustering_method": "cluster_robust_psu_explicit_dummy",
        "se_note": f"coefficient_from='explicit_dummy_wls'; compare to demeaned coefficient below; abs_diff={r['abs_diff']:.2e}",
    })
    model_b_rows.append({
        "development_family": "estimator_validation", "model_label": "explicit_dummy_vs_weighted_demeaning",
        "outcome": val_outcome, "sample_variant": f"validation_subset_{validation_country}", "term": r["term"],
        "coefficient": r["coef_weighted_demeaning"], "standard_error": np.nan, "ci_lower": np.nan, "ci_upper": np.nan,
        "p_value": np.nan, "estimation_n": int(res_demeaned.nobs), "psu_count": n_clusters_v, "fe_region_count": 0,
        "weight_method": "weight_original", "clustering_method": "cluster_robust_psu_weighted_demeaning",
        "se_note": f"coefficient_from='weighted_demeaning'; compare to explicit-dummy coefficient above; abs_diff={r['abs_diff']:.2e}",
    })

model_b_df = pd.DataFrame(model_b_rows, columns=RESULT_COLUMNS)
model_b_df.to_csv(OUT_DIR / "03_household_cluster_fe.csv", index=False)
log("Written: 03_household_cluster_fe.csv (includes the estimator-validation block)")

# ============================================================================
# PART 4: MODEL C - HOUSEHOLD + COMMUNITY WASH JOINT MODEL
# ============================================================================
log("\n" + "=" * 90 + "\nPART 4: MODEL C - HOUSEHOLD + COMMUNITY WASH JOINT MODEL\n" + "=" * 90)

C_CONTINUOUS = HOUSEHOLD_EXPOSURES + EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
C_CATEGORICAL = MODEL4_CATEGORICAL

model_c_rows = []
model_c_res = {}
for outcome in PRIMARY_OUTCOMES:
    sample_c = common_samples[outcome]
    weight_c, _ = reg.build_temporary_pooled_weight(sample_c)
    res_c, ref_c = run_explicit_wls(f"C-{outcome}", sample_c, outcome, C_CONTINUOUS, C_CATEGORICAL,
                                     weight_c, sample_c["country_psu"], include_fe=True, fe_col=FE_VAR)
    model_c_res[outcome] = (res_c, sample_c, weight_c)
    model_c_rows += rows_from_fit(res_c, outcome, "model_C_joint_household_community", "joint_common_sample",
                                   "common_sample", "model_specific_equal_total_country_weight",
                                   "cluster_robust_country_psu", int(sample_c["country_psu"].nunique()),
                                   int(sample_c[FE_VAR].nunique()))
    log(f"  C [{outcome}] N={len(sample_c)} PSUs={sample_c['country_psu'].nunique()} OK")

model_c_df = pd.DataFrame(model_c_rows, columns=RESULT_COLUMNS)
model_c_df.to_csv(OUT_DIR / "05_joint_household_community.csv", index=False)
log("Written: 05_joint_household_community.csv")

# ============================================================================
# PART 4B: MULTICOLLINEARITY DIAGNOSTICS
# ============================================================================
log("\n" + "=" * 90 + "\nPART 4B: MULTICOLLINEARITY DIAGNOSTICS (Model C)\n" + "=" * 90)

collin_rows = []
for outcome in PRIMARY_OUTCOMES:
    sample_c = common_samples[outcome]
    exposures4 = HOUSEHOLD_EXPOSURES + EXPOSURES
    corr = sample_c[exposures4].corr()
    for a, b in itertools.combinations(exposures4, 2):
        collin_rows.append({"outcome": outcome, "diagnostic": "pairwise_correlation", "term_a": a, "term_b": b,
                             "value": corr.loc[a, b], "note": ""})

    X_sub = sm.add_constant(sample_c[exposures4].astype(float), has_constant="add")
    for i, term in enumerate(exposures4):
        vif = variance_inflation_factor(X_sub.values, i + 1)
        collin_rows.append({"outcome": outcome, "diagnostic": "VIF_exposures_only", "term_a": term, "term_b": "",
                             "value": vif, "note": "VIF among the 4 WASH exposures + constant only (isolates WASH-specific collinearity)"})

    full_conts = exposures4 + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
    X_raw, _ = build_raw_design(sample_c, full_conts, MODEL4_CATEGORICAL)
    X_full = sm.add_constant(X_raw, has_constant="add")
    cond_no_full = np.linalg.cond(X_full.values)
    for term in exposures4:
        col_idx = list(X_full.columns).index(term)
        vif = variance_inflation_factor(X_full.values, col_idx)
        collin_rows.append({"outcome": outcome, "diagnostic": "VIF_exposures_plus_controls", "term_a": term, "term_b": "",
                             "value": vif, "note": "VIF among the 4 exposures + full child/SES controls (excl. FE dummies)"})
    collin_rows.append({"outcome": outcome, "diagnostic": "condition_number_exposures_plus_controls", "term_a": "", "term_b": "",
                         "value": cond_no_full, "note": "np.linalg.cond(), unweighted design matrix, exposures+controls+constant, excl. FE dummies"})

    res_c, _, _ = model_c_res[outcome]
    for term in exposures4:
        collin_rows.append({"outcome": outcome, "diagnostic": "joint_model_coefficient", "term_a": term, "term_b": "",
                             "value": res_c.params[term],
                             "note": f"se={res_c.bse[term]:.5f} p={res_c.pvalues[term]:.4f} (Model C, common sample)"})

collin_df = pd.DataFrame(collin_rows)
collin_df.to_csv(OUT_DIR / "06_joint_model_collinearity.csv", index=False)
log("Written: 06_joint_model_collinearity.csv")

# ============================================================================
# PART 5: FAIR COMMUNITY MODEL ON COMMON SAMPLE + COMPARISON TABLE
# ============================================================================
log("\n" + "=" * 90 + "\nPART 5: FAIR COMMUNITY MODEL ON COMMON SAMPLE + COMPARISON TABLE\n" + "=" * 90)

D_CONTINUOUS = EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
D_CATEGORICAL = MODEL4_CATEGORICAL

comparison_rows = []
model_d_res = {}
model_a2_res = {}
for outcome in PRIMARY_OUTCOMES:
    sample_d = common_samples[outcome]
    weight_d, _ = reg.build_temporary_pooled_weight(sample_d)
    res_d, ref_d = run_explicit_wls(f"D-{outcome}", sample_d, outcome, D_CONTINUOUS, D_CATEGORICAL,
                                     weight_d, sample_d["country_psu"], include_fe=True, fe_col=FE_VAR)
    model_d_res[outcome] = res_d
    log(f"  D(community-only, common sample) [{outcome}] N={len(sample_d)} OK")

    sample_a2 = common_samples[outcome]
    weight_a2, _ = reg.build_temporary_pooled_weight(sample_a2)
    res_a2, _ = run_explicit_wls(f"A2redo-{outcome}", sample_a2, outcome, A_CONTINUOUS, A_CATEGORICAL,
                                  weight_a2, sample_a2["country_psu"], include_fe=True, fe_col=FE_VAR)
    model_a2_res[outcome] = res_a2

    res_c, sample_c, weight_c = model_c_res[outcome]

    def pull(res, term, n_psu):
        ci = res.conf_int()
        return {"beta": res.params[term], "se": res.bse[term], "ci_lower": ci.loc[term, 0],
                "ci_upper": ci.loc[term, 1], "p_value": res.pvalues[term], "N": int(res.nobs), "psu_count": n_psu}

    n_psu_common = int(sample_d["country_psu"].nunique())
    specs = [
        ("community_only", res_d, "water_rate_loo"), ("community_only", res_d, "sanitation_rate_loo_core"),
        ("household_only", res_a2, "_water_hh_binary"), ("household_only", res_a2, "_sani_hh_binary"),
        ("joint_household_term", res_c, "_water_hh_binary"), ("joint_household_term", res_c, "_sani_hh_binary"),
        ("joint_community_term", res_c, "water_rate_loo"), ("joint_community_term", res_c, "sanitation_rate_loo_core"),
    ]
    for spec_label, res_obj, term in specs:
        d = pull(res_obj, term, n_psu_common)
        comparison_rows.append({"outcome": outcome, "spec": spec_label, "term": term, **d})

comparison_df = pd.DataFrame(comparison_rows)
comparison_df.to_csv(OUT_DIR / "07_common_sample_community_vs_household.csv", index=False)
log("Written: 07_common_sample_community_vs_household.csv")

# ============================================================================
# PART 6: FLEXIBLE CHILD-AGE CONTROL
# ============================================================================
log("\n" + "=" * 90 + "\nPART 6: FLEXIBLE CHILD-AGE CONTROL (age-month FE vs linear)\n" + "=" * 90)


def with_age_month(sample_df):
    s = sample_df.copy()
    s["_age_month_cat"] = s["b19_raw"].astype(int).astype(str)
    return s


AGE_REF = "0"  # youngest observed month - fixed before seeing any result, not tuned

age_flex_rows = []

for outcome in PRIMARY_OUTCOMES:
    sample = with_age_month(common_samples[outcome])
    cont = HOUSEHOLD_EXPOSURES + [v for v in HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS if v != "b19_raw"]
    cat = {**MODEL4_CATEGORICAL, "_age_month_cat": AGE_REF}
    weight, _ = reg.build_temporary_pooled_weight(sample)
    res_lin, _ = run_explicit_wls(f"E-A-linear-{outcome}", sample, outcome, A_CONTINUOUS, A_CATEGORICAL,
                                   weight, sample["country_psu"], include_fe=True, fe_col=FE_VAR)
    res_flex, _ = run_explicit_wls(f"E-A-flex-{outcome}", sample, outcome, cont, cat,
                                    weight, sample["country_psu"], include_fe=True, fe_col=FE_VAR)
    for term in ["_water_hh_binary", "_sani_hh_binary"]:
        age_flex_rows.append({
            "specification": "A_household_region_fe", "outcome": outcome, "term": term,
            "beta_linear_age": res_lin.params[term], "se_linear_age": res_lin.bse[term], "p_linear_age": res_lin.pvalues[term],
            "beta_age_month_fe": res_flex.params[term], "se_age_month_fe": res_flex.bse[term], "p_age_month_fe": res_flex.pvalues[term],
            "sign_change": bool(np.sign(res_lin.params[term]) != np.sign(res_flex.params[term])),
            "significance_change_at_5pct": bool((res_lin.pvalues[term] < 0.05) != (res_flex.pvalues[term] < 0.05)),
            "N": int(res_flex.nobs), "se_caveat": "",
        })
    log(f"  A [{outcome}] linear-age vs age-month-FE: OK (N={int(res_flex.nobs)})")

for outcome in PRIMARY_OUTCOMES:
    sample = with_age_month(common_samples[outcome])
    cont = EXPOSURES + [v for v in HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS if v != "b19_raw"]
    cat = {**MODEL4_CATEGORICAL, "_age_month_cat": AGE_REF}
    weight, _ = reg.build_temporary_pooled_weight(sample)
    res_lin, _ = run_explicit_wls(f"E-D-linear-{outcome}", sample, outcome, D_CONTINUOUS, D_CATEGORICAL,
                                   weight, sample["country_psu"], include_fe=True, fe_col=FE_VAR)
    res_flex, _ = run_explicit_wls(f"E-D-flex-{outcome}", sample, outcome, cont, cat,
                                    weight, sample["country_psu"], include_fe=True, fe_col=FE_VAR)
    for term in ["water_rate_loo", "sanitation_rate_loo_core"]:
        age_flex_rows.append({
            "specification": "D_community_region_fe_common_sample", "outcome": outcome, "term": term,
            "beta_linear_age": res_lin.params[term], "se_linear_age": res_lin.bse[term], "p_linear_age": res_lin.pvalues[term],
            "beta_age_month_fe": res_flex.params[term], "se_age_month_fe": res_flex.bse[term], "p_age_month_fe": res_flex.pvalues[term],
            "sign_change": bool(np.sign(res_lin.params[term]) != np.sign(res_flex.params[term])),
            "significance_change_at_5pct": bool((res_lin.pvalues[term] < 0.05) != (res_flex.pvalues[term] < 0.05)),
            "N": int(res_flex.nobs), "se_caveat": "",
        })
    log(f"  D [{outcome}] linear-age vs age-month-FE: OK (N={int(res_flex.nobs)})")

for outcome in PRIMARY_OUTCOMES:
    sample = with_age_month(model_b_samples[outcome])
    cont_lin = HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS
    cont_flex = HOUSEHOLD_EXPOSURES + [v for v in HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS if v != "b19_raw"]
    cat_flex = {**CLUSTER_FE_CATEGORICAL, "_age_month_cat": AGE_REF}
    weight, _ = reg.build_temporary_pooled_weight(sample)
    res_lin, *_ = run_cluster_fe_demeaned(f"E-B-linear-{outcome}", sample, outcome, cont_lin, B_CATEGORICAL, weight, "country_psu")
    res_flex, *_ = run_cluster_fe_demeaned(f"E-B-flex-{outcome}", sample, outcome, cont_flex, cat_flex, weight, "country_psu")
    for term in ["_water_hh_binary", "_sani_hh_binary"]:
        age_flex_rows.append({
            "specification": "B_household_cluster_fe", "outcome": outcome, "term": term,
            "beta_linear_age": res_lin.params[term], "se_linear_age": res_lin.bse[term], "p_linear_age": res_lin.pvalues[term],
            "beta_age_month_fe": res_flex.params[term], "se_age_month_fe": res_flex.bse[term], "p_age_month_fe": res_flex.pvalues[term],
            "sign_change": bool(np.sign(res_lin.params[term]) != np.sign(res_flex.params[term])),
            "significance_change_at_5pct": bool((res_lin.pvalues[term] < 0.05) != (res_flex.pvalues[term] < 0.05)),
            "N": int(res_flex.nobs),
            "se_caveat": "SE/p shown are statsmodels' native cluster-robust values on the demeaned fit "
                         "(cov_type='cluster', use_correction=True) - the thesis's primary same-PSU-FE/"
                         "same-PSU-cluster inference convention (see docs/provenance/"
                         "cluster_fe_inference_adjudication.md); no additional absorbed-FE degrees-of-freedom "
                         "penalty is applied.",
        })
    log(f"  B [{outcome}] linear-age vs age-month-FE (demeaned): OK (N={int(res_flex.nobs)})")

age_flex_df = pd.DataFrame(age_flex_rows)
age_flex_df.to_csv(OUT_DIR / "08_flexible_age_sensitivity.csv", index=False)
log("Written: 08_flexible_age_sensitivity.csv")

# ============================================================================
# PART 7: AGE HETEROGENEITY (household WASH x age-band)
# ============================================================================
log("\n" + "=" * 90 + "\nPART 7: AGE HETEROGENEITY (household WASH x age-band)\n" + "=" * 90)

AGE_BANDS = [(-1, 5, "0-5"), (5, 11, "6-11"), (11, 23, "12-23"), (23, 35, "24-35"), (35, 47, "36-47"), (47, 59, "48-59")]
AGE_BAND_REF = "12-23"  # largest/most central band - fixed before any heterogeneity result was seen


def add_age_band(sample_df):
    s = sample_df.copy()
    bins = [b[0] for b in AGE_BANDS] + [AGE_BANDS[-1][1]]
    labels = [b[2] for b in AGE_BANDS]
    s["_age_band"] = pd.cut(s["b19_raw"], bins=bins, labels=labels).astype(str)
    return s


def add_interactions(sample_df, exposure_cols, band_col="_age_band", ref=AGE_BAND_REF):
    s = sample_df.copy()
    bands = [b[2] for b in AGE_BANDS if b[2] != ref]
    inter_cols = []
    for exp in exposure_cols:
        for band in bands:
            col = f"{exp}_x_{band.replace('-', '_')}"
            s[col] = s[exp] * (s[band_col] == band).astype(float)
            inter_cols.append(col)
    return s, inter_cols, bands


age_het_rows = []
joint_test_rows = []
desc_rows = []
for outcome in PRIMARY_OUTCOMES:
    sample = add_age_band(model_b_samples[outcome])
    vc = sample["_age_band"].value_counts()
    for band, n in vc.items():
        desc_rows.append({"outcome": outcome, "age_band": band, "n": int(n)})

for outcome in PRIMARY_OUTCOMES:
    sample = add_age_band(common_samples[outcome])
    sample, inter_cols, bands = add_interactions(sample, HOUSEHOLD_EXPOSURES)
    cont = HOUSEHOLD_EXPOSURES + [v for v in HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS if v != "b19_raw"] + inter_cols
    cat = {**MODEL4_CATEGORICAL, "_age_band": AGE_BAND_REF}
    weight, _ = reg.build_temporary_pooled_weight(sample)
    res_h1, ref_h1 = run_explicit_wls(f"H1-{outcome}", sample, outcome, cont, cat, weight,
                                       sample["country_psu"], include_fe=True, fe_col=FE_VAR)
    ci = res_h1.conf_int()
    for term in HOUSEHOLD_EXPOSURES + inter_cols:
        age_het_rows.append({
            "spec": "H1_household_region_fe", "outcome": outcome, "term": term,
            "coefficient": res_h1.params[term], "se": res_h1.bse[term],
            "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_h1.pvalues[term],
            "N": int(res_h1.nobs), "reference_age_band": AGE_BAND_REF,
        })
    cov = res_h1.cov_params()
    for exp in HOUSEHOLD_EXPOSURES:
        for band in [b[2] for b in AGE_BANDS]:
            if band == AGE_BAND_REF:
                implied, implied_se = res_h1.params[exp], res_h1.bse[exp]
            else:
                inter_term = f"{exp}_x_{band.replace('-', '_')}"
                implied = res_h1.params[exp] + res_h1.params[inter_term]
                var_sum = cov.loc[exp, exp] + cov.loc[inter_term, inter_term] + 2 * cov.loc[exp, inter_term]
                implied_se = np.sqrt(var_sum)
            age_het_rows.append({
                "spec": "H1_implied_total_by_band", "outcome": outcome, "term": f"{exp}__band_{band}",
                "coefficient": implied, "se": implied_se, "ci_lower": implied - 1.959963984540054 * implied_se,
                "ci_upper": implied + 1.959963984540054 * implied_se, "p_value": np.nan, "N": int(res_h1.nobs),
                "reference_age_band": AGE_BAND_REF,
            })
    param_names = list(res_h1.params.index)

    def wald_joint(res, terms, pnames):
        R = np.zeros((len(terms), len(pnames)))
        for i, t in enumerate(terms):
            R[i, pnames.index(t)] = 1.0
        wt = res.wald_test(R, use_f=False, scalar=True)
        return float(wt.statistic), float(wt.pvalue), len(terms)

    water_inter = [f"_water_hh_binary_x_{b.replace('-', '_')}" for b in bands]
    sani_inter = [f"_sani_hh_binary_x_{b.replace('-', '_')}" for b in bands]
    for label, terms in [("water_interactions_jointly_zero", water_inter),
                          ("sanitation_interactions_jointly_zero", sani_inter),
                          ("all_interactions_jointly_zero", water_inter + sani_inter)]:
        stat, pval, dfree = wald_joint(res_h1, terms, param_names)
        joint_test_rows.append({"spec": "H1_household_region_fe", "outcome": outcome, "hypothesis": label,
                                 "chi2_or_wald_stat": stat, "p_value": pval, "df": dfree})
    log(f"  H1 [{outcome}] N={int(res_h1.nobs)} OK")

for outcome in PRIMARY_OUTCOMES:
    sample = add_age_band(model_b_samples[outcome])
    sample, inter_cols, bands = add_interactions(sample, HOUSEHOLD_EXPOSURES)
    cont = HOUSEHOLD_EXPOSURES + [v for v in HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS if v != "b19_raw"] + inter_cols
    cat = {**CLUSTER_FE_CATEGORICAL, "_age_band": AGE_BAND_REF}
    weight, _ = reg.build_temporary_pooled_weight(sample)
    # PRIMARY inference: native statsmodels cluster-robust covariance on the
    # demeaned fit, directly from res_h2 - no additional absorbed-PSU-FE
    # degrees-of-freedom scaling. Same adjudicated same-effect/same-cluster
    # convention as Model B; see docs/provenance/cluster_fe_inference_adjudication.md.
    res_h2, ref_h2, k_rep2, nclu2 = run_cluster_fe_demeaned(
        f"H2-{outcome}", sample, outcome, cont, cat, weight, "country_psu"
    )
    ci_h2 = res_h2.conf_int()
    for term in HOUSEHOLD_EXPOSURES + inter_cols:
        age_het_rows.append({
            "spec": "H2_household_cluster_fe", "outcome": outcome, "term": term,
            "coefficient": res_h2.params[term], "se": res_h2.bse[term],
            "ci_lower": ci_h2.loc[term, 0], "ci_upper": ci_h2.loc[term, 1], "p_value": res_h2.pvalues[term],
            "N": int(res_h2.nobs), "reference_age_band": AGE_BAND_REF,
        })
    cov2 = res_h2.cov_params()
    for exp in HOUSEHOLD_EXPOSURES:
        for band in [b[2] for b in AGE_BANDS]:
            if band == AGE_BAND_REF:
                implied, implied_se = res_h2.params[exp], float(np.sqrt(cov2.loc[exp, exp]))
            else:
                inter_term = f"{exp}_x_{band.replace('-', '_')}"
                implied = res_h2.params[exp] + res_h2.params[inter_term]
                var_sum = cov2.loc[exp, exp] + cov2.loc[inter_term, inter_term] + 2 * cov2.loc[exp, inter_term]
                implied_se = float(np.sqrt(var_sum))
            age_het_rows.append({
                "spec": "H2_implied_total_by_band", "outcome": outcome, "term": f"{exp}__band_{band}",
                "coefficient": implied, "se": implied_se, "ci_lower": implied - 1.959963984540054 * implied_se,
                "ci_upper": implied + 1.959963984540054 * implied_se, "p_value": np.nan, "N": int(res_h2.nobs),
                "reference_age_band": AGE_BAND_REF,
            })
    param_names2 = list(res_h2.params.index)

    def wald_joint2(res, terms, pnames, covmat):
        from scipy import stats as _stats
        R = np.zeros((len(terms), len(pnames)))
        for i, t in enumerate(terms):
            R[i, pnames.index(t)] = 1.0
        Rb = R @ res.params.values
        RcovR = R @ covmat.values @ R.T
        stat = float(Rb @ np.linalg.inv(RcovR) @ Rb)
        pval = float(1 - _stats.chi2.cdf(stat, df=len(terms)))
        return stat, pval, len(terms)

    water_inter = [f"_water_hh_binary_x_{b.replace('-', '_')}" for b in bands]
    sani_inter = [f"_sani_hh_binary_x_{b.replace('-', '_')}" for b in bands]
    for label, terms in [("water_interactions_jointly_zero", water_inter),
                          ("sanitation_interactions_jointly_zero", sani_inter),
                          ("all_interactions_jointly_zero", water_inter + sani_inter)]:
        stat, pval, dfree = wald_joint2(res_h2, terms, param_names2, cov2)
        joint_test_rows.append({"spec": "H2_household_cluster_fe", "outcome": outcome, "hypothesis": label,
                                 "chi2_or_wald_stat": stat, "p_value": pval, "df": dfree})
    log(f"  H2 [{outcome}] N={int(res_h2.nobs)} clusters={nclu2} k_reported={k_rep2} OK (native same-cluster CRV1)")

age_het_df = pd.DataFrame(age_het_rows)
age_het_df.to_csv(OUT_DIR / "09_age_heterogeneity.csv", index=False)
desc_df = pd.DataFrame(desc_rows)
desc_df.to_csv(OUT_DIR / "09b_age_heterogeneity_descriptive_bands.csv", index=False)
log("Written: 09_age_heterogeneity.csv, 09b_age_heterogeneity_descriptive_bands.csv (supplementary)")

joint_test_df = pd.DataFrame(joint_test_rows)
joint_test_df.to_csv(OUT_DIR / "10_age_heterogeneity_joint_tests.csv", index=False)
log("Written: 10_age_heterogeneity_joint_tests.csv")

# ============================================================================
# PART 8: NIGERIA SANITATION -> HAZ SIGN-REVERSAL DIAGNOSTIC
# ============================================================================
log("\n" + "=" * 90 + "\nPART 8: NIGERIA SANITATION -> HAZ SIGN-REVERSAL DIAGNOSTIC\n" + "=" * 90)

nigeria_reproduction_rows = []
for model_num in [1, 2, 3, 4]:
    res_df_nig = reg.run_single_model(df, "haz", model_num, "nigeria")
    for term_name in ["sanitation_rate_loo_core", "water_rate_loo"]:
        row = res_df_nig[res_df_nig["term"] == term_name].iloc[0]
        nigeria_reproduction_rows.append({
            "model": model_num, "term": term_name, "coefficient": row["coefficient"],
            "se": row["standard_error"], "ci_lower": row["ci_lower"], "ci_upper": row["ci_upper"],
            "p_value": row["p_value"], "N": row["estimation_n"], "psu_count": row["psu_count"],
        })
    r = [x for x in nigeria_reproduction_rows if x["model"] == model_num and x["term"] == "sanitation_rate_loo_core"][0]
    log(f"  M{model_num} Nigeria sanitation_rate_loo_core: beta={r['coefficient']:+.4f} p={r['p_value']:.4f}")

existing = pd.read_csv(config.PROJECT_ROOT / "outputs" / "regressions" / "main_continuous_models.csv")
existing_nigeria = existing[(existing["outcome"] == "haz") & (existing["country_scope"] == "nigeria") &
                             (existing["term"] == "sanitation_rate_loo_core")]
recon = pd.DataFrame(nigeria_reproduction_rows)
recon_sani = recon[recon["term"] == "sanitation_rate_loo_core"].set_index("model")["coefficient"]
mismatch = False
for _, r in existing_nigeria.iterrows():
    if abs(recon_sani.loc[r["model"]] - r["coefficient"]) > 1e-9:
        mismatch = True
        log(f"  DISCREPANCY: model {r['model']} existing={r['coefficient']} vs reproduced={recon_sani.loc[r['model']]}")
if mismatch:
    raise RuntimeError("Nigeria M1-M4 reproduction does not match frozen main_continuous_models.csv. STOP.")
log("Nigeria M1-M4 sanitation_rate_loo_core reproduction: EXACT match to the frozen baseline output.")

nigeria_mask_full = reg.build_estimation_sample(df, "haz") & (df["country"] == "nigeria")
nigeria_sample = df[nigeria_mask_full].copy()
nig_weight = nigeria_sample["weight_original"]
nig_cluster = nigeria_sample["psu"]

BLOCKS = {
    "A_maternal_age": ("cont", "maternal_age"),
    "B_maternal_education": ("cat", "maternal_education", "No education"),
    "C_literacy": ("cat", "literacy", "Cannot read at all"),
    "D_wealth_quintile": ("cat", "wealth_quintile", "Poorest"),
    "E_household_size": ("cont", "household_size_raw"),
    "F_residence": ("cat", "residence", "Rural"),
}
BLOCK_ORDER = ["A_maternal_age", "B_maternal_education", "C_literacy", "D_wealth_quintile", "E_household_size", "F_residence"]

seq_rows = []
cur_cont = list(EXPOSURES) + list(CHILD_CONTROLS_CONTINUOUS)
cur_cat = dict(CHILD_CONTROLS_CATEGORICAL)
label = "M2_base(exposures+child_controls)"
res_cur, _ = run_explicit_wls(f"NIG-seq-{label}", nigeria_sample, "haz", cur_cont, cur_cat, nig_weight, nig_cluster, include_fe=False)
for term in ["water_rate_loo", "sanitation_rate_loo_core"]:
    ci = res_cur.conf_int()
    seq_rows.append({"step": label, "term": term, "coefficient": res_cur.params[term], "se": res_cur.bse[term],
                      "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_cur.pvalues[term], "N": int(res_cur.nobs)})

for block_name in BLOCK_ORDER:
    spec = BLOCKS[block_name]
    if spec[0] == "cont":
        cur_cont = cur_cont + [spec[1]]
    else:
        cur_cat = {**cur_cat, spec[1]: spec[2]}
    label = f"+{block_name}"
    res_cur, _ = run_explicit_wls(f"NIG-seq-{label}", nigeria_sample, "haz", cur_cont, cur_cat, nig_weight, nig_cluster, include_fe=False)
    for term in ["water_rate_loo", "sanitation_rate_loo_core"]:
        ci = res_cur.conf_int()
        seq_rows.append({"step": label, "term": term, "coefficient": res_cur.params[term], "se": res_cur.bse[term],
                          "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_cur.pvalues[term], "N": int(res_cur.nobs)})
    log(f"  sequential {label}: sanitation beta={res_cur.params['sanitation_rate_loo_core']:+.4f}")

FULL_M3_CONT = list(EXPOSURES) + list(CHILD_CONTROLS_CONTINUOUS) + SES_CONTROLS_CONTINUOUS
FULL_M3_CAT = {**CHILD_CONTROLS_CATEGORICAL, **SES_CONTROLS_CATEGORICAL}

loo_rows = []
res_full, _ = run_explicit_wls("NIG-M3-full", nigeria_sample, "haz", FULL_M3_CONT, FULL_M3_CAT, nig_weight, nig_cluster, include_fe=False)
for term in ["water_rate_loo", "sanitation_rate_loo_core"]:
    ci = res_full.conf_int()
    loo_rows.append({"variant": "full_M3", "term": term, "coefficient": res_full.params[term], "se": res_full.bse[term],
                      "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_full.pvalues[term], "N": int(res_full.nobs)})

for block_name in BLOCK_ORDER:
    spec = BLOCKS[block_name]
    if spec[0] == "cont":
        cont_i = [v for v in FULL_M3_CONT if v != spec[1]]
        cat_i = dict(FULL_M3_CAT)
    else:
        cont_i = list(FULL_M3_CONT)
        cat_i = {k: v for k, v in FULL_M3_CAT.items() if k != spec[1]}
    res_i, _ = run_explicit_wls(f"NIG-M3-minus-{block_name}", nigeria_sample, "haz", cont_i, cat_i, nig_weight, nig_cluster, include_fe=False)
    for term in ["water_rate_loo", "sanitation_rate_loo_core"]:
        ci = res_i.conf_int()
        loo_rows.append({"variant": f"M3_minus_{block_name}", "term": term, "coefficient": res_i.params[term], "se": res_i.bse[term],
                          "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_i.pvalues[term], "N": int(res_i.nobs)})
    log(f"  M3 minus {block_name}: sanitation beta={res_i.params['sanitation_rate_loo_core']:+.4f}")

nigeria_sign_df = pd.concat([
    pd.DataFrame(nigeria_reproduction_rows).assign(section="M1_M4_reproduction"),
    pd.DataFrame(seq_rows).assign(section="sequential_block_addition"),
    pd.DataFrame(loo_rows).assign(section="leave_one_block_out"),
], ignore_index=True)
nigeria_sign_df.to_csv(OUT_DIR / "11_nigeria_sign_reversal.csv", index=False)
log("Written: 11_nigeria_sign_reversal.csv")

covar_rows = []
for cat_var in ["wealth_quintile", "residence", "maternal_education", "literacy"]:
    g = nigeria_sample.groupby(cat_var, observed=True)["sanitation_rate_loo_core"].agg(["mean", "std", "count"])
    for level, row in g.iterrows():
        covar_rows.append({"covariate": cat_var, "level": level, "mean_sanitation_rate_loo_core": row["mean"],
                            "sd": row["std"], "n": int(row["count"])})
covar_df = pd.DataFrame(covar_rows)

nig_compare_rows = []
res_m4 = reg.run_single_model(df, "haz", 4, "nigeria")
r = res_m4[res_m4["term"] == "sanitation_rate_loo_core"].iloc[0]
nig_compare_rows.append({"spec": "1_community_region_fe", "term": "sanitation_rate_loo_core", "coefficient": r["coefficient"],
                          "se": r["standard_error"], "p_value": r["p_value"], "N": r["estimation_n"]})

nig_hh_mask = df["haz"].notna()
for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(MODEL4_CATEGORICAL) + [FE_VAR]:
    nig_hh_mask &= df[v].notna()
nig_hh_mask &= (df["country"] == "nigeria")
nig_hh_sample = df[nig_hh_mask].copy()
res_nig_a, _ = run_explicit_wls("NIG-A", nig_hh_sample, "haz", A_CONTINUOUS, MODEL4_CATEGORICAL,
                                 nig_hh_sample["weight_original"], nig_hh_sample["psu"], include_fe=True, fe_col=FE_VAR)
nig_compare_rows.append({"spec": "2_household_region_fe", "term": "_sani_hh_binary", "coefficient": res_nig_a.params["_sani_hh_binary"],
                          "se": res_nig_a.bse["_sani_hh_binary"], "p_value": res_nig_a.pvalues["_sani_hh_binary"], "N": int(res_nig_a.nobs)})

nig_b_mask = df["haz"].notna()
for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(CLUSTER_FE_CATEGORICAL) + ["psu"]:
    nig_b_mask &= df[v].notna()
nig_b_mask &= (df["country"] == "nigeria")
nig_b_sample = df[nig_b_mask].copy()
res_nig_b, *_ = run_cluster_fe_demeaned("NIG-B", nig_b_sample, "haz", B_CONTINUOUS, CLUSTER_FE_CATEGORICAL,
                                         nig_b_sample["weight_original"], "psu")
nig_compare_rows.append({"spec": "3_household_cluster_fe", "term": "_sani_hh_binary", "coefficient": res_nig_b.params["_sani_hh_binary"],
                          "se": res_nig_b.bse["_sani_hh_binary"], "p_value": res_nig_b.pvalues["_sani_hh_binary"], "N": int(res_nig_b.nobs)})

nig_c_mask = df["haz"].notna()
for v in HOUSEHOLD_EXPOSURES + EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(MODEL4_CATEGORICAL) + [FE_VAR]:
    nig_c_mask &= df[v].notna()
nig_c_mask &= (df["country"] == "nigeria")
nig_c_sample = df[nig_c_mask].copy()
res_nig_c, _ = run_explicit_wls("NIG-C", nig_c_sample, "haz", C_CONTINUOUS, MODEL4_CATEGORICAL,
                                 nig_c_sample["weight_original"], nig_c_sample["psu"], include_fe=True, fe_col=FE_VAR)
nig_compare_rows.append({"spec": "4_joint_household_community_region_fe", "term": "_sani_hh_binary(joint)",
                          "coefficient": res_nig_c.params["_sani_hh_binary"], "se": res_nig_c.bse["_sani_hh_binary"],
                          "p_value": res_nig_c.pvalues["_sani_hh_binary"], "N": int(res_nig_c.nobs)})
nig_compare_rows.append({"spec": "4_joint_household_community_region_fe", "term": "sanitation_rate_loo_core(joint)",
                          "coefficient": res_nig_c.params["sanitation_rate_loo_core"], "se": res_nig_c.bse["sanitation_rate_loo_core"],
                          "p_value": res_nig_c.pvalues["sanitation_rate_loo_core"], "N": int(res_nig_c.nobs)})

nig_compare_df = pd.DataFrame(nig_compare_rows)
nig_diag_out = pd.concat([covar_df.assign(section="covariate_group_means"),
                           nig_compare_df.assign(section="four_way_comparison")], ignore_index=True)
nig_diag_out.to_csv(OUT_DIR / "12_nigeria_sign_reversal_covariate_diagnostics.csv", index=False)
log("Written: 12_nigeria_sign_reversal_covariate_diagnostics.csv")

# ============================================================================
# PART 9: ANTHROPOMETRIC AVAILABILITY / SELECTION DIAGNOSTIC
# ============================================================================
log("\n" + "=" * 90 + "\nPART 9: ANTHROPOMETRIC AVAILABILITY / SELECTION DIAGNOSTIC\n" + "=" * 90)

avail_rows = []
_bins = [-1, 5, 11, 23, 35, 47, 59]
_labels = ["0-5", "6-11", "12-23", "24-35", "36-47", "48-59"]
df["_age_band_avail"] = pd.cut(df["b19_raw"], bins=_bins, labels=_labels)


def avail_block(sub, groupvar, groupname, country):
    rows = []
    for level, g in sub.groupby(groupvar, observed=True):
        if len(g) == 0:
            continue
        rows.append({
            "country": country, "breakdown": groupname, "level": str(level), "n_total": len(g),
            "haz_available_n": int(g["haz"].notna().sum()), "haz_available_pct": round(100 * g["haz"].notna().mean(), 2),
            "waz_available_n": int(g["waz"].notna().sum()), "waz_available_pct": round(100 * g["waz"].notna().mean(), 2),
            "whz_available_n": int(g["whz"].notna().sum()), "whz_available_pct": round(100 * g["whz"].notna().mean(), 2),
        })
    return rows


for country in ["ethiopia", "ghana", "kenya", "nigeria", "ALL"]:
    sub_c = df if country == "ALL" else df[df["country"] == country]
    avail_rows.append({
        "country": country, "breakdown": "OVERALL", "level": "ALL", "n_total": len(sub_c),
        "haz_available_n": int(sub_c["haz"].notna().sum()), "haz_available_pct": round(100 * sub_c["haz"].notna().mean(), 2),
        "waz_available_n": int(sub_c["waz"].notna().sum()), "waz_available_pct": round(100 * sub_c["waz"].notna().mean(), 2),
        "whz_available_n": int(sub_c["whz"].notna().sum()), "whz_available_pct": round(100 * sub_c["whz"].notna().mean(), 2),
    })
    avail_rows += avail_block(sub_c, "_age_band_avail", "age_band", country)
    avail_rows += avail_block(sub_c.dropna(subset=["water_category"]), "water_category", "household_water_status", country)
    avail_rows += avail_block(sub_c.dropna(subset=["sanitation_collapsed_core"]), "sanitation_collapsed_core", "household_sanitation_status", country)
    sub_c2 = sub_c.dropna(subset=["water_rate_loo"]).copy()
    sub_c2["_wq"] = pd.qcut(sub_c2["water_rate_loo"], 4, duplicates="drop")
    avail_rows += avail_block(sub_c2, "_wq", "community_water_loo_quartile", country)
    sub_c3 = sub_c.dropna(subset=["sanitation_rate_loo_core"]).copy()
    sub_c3["_sq"] = pd.qcut(sub_c3["sanitation_rate_loo_core"], 4, duplicates="drop")
    avail_rows += avail_block(sub_c3, "_sq", "community_sanitation_loo_quartile", country)
    avail_rows += avail_block(sub_c, "wealth_quintile", "wealth_quintile", country)
    avail_rows += avail_block(sub_c, "residence", "residence", country)

avail_df = pd.DataFrame(avail_rows)
avail_df.to_csv(OUT_DIR / "13_anthro_availability_diagnostic.csv", index=False)
log("Written: 13_anthro_availability_diagnostic.csv")

import pyreadstat as _pyreadstat
_, meta_check = _pyreadstat.read_dta(str(config.COUNTRIES["ethiopia"]["kr_path"]), metadataonly=True)
b5_present = "b5" in {c.lower() for c in meta_check.column_names}
log(f"Raw KR metadata check (Ethiopia, read-only, COLUMN NAMES ONLY - no observation data read): "
    f"'b5' (child survival status) present = {b5_present}. NOT extracted into any processed file by "
    "this development script. Exact reasons for anthropometry non-completion (death vs non-residence "
    "vs absence vs refusal) CANNOT be established from currently-processed data and are not inferred here.")

# ============================================================================
# PART 10: COUNTRY-SPECIFIC HOUSEHOLD MODELS
# ============================================================================
log("\n" + "=" * 90 + "\nPART 10: COUNTRY-SPECIFIC HOUSEHOLD MODELS\n" + "=" * 90)

country_rows = []
country_support_rows = []
for outcome in PRIMARY_OUTCOMES:
    for country in ["ethiopia", "ghana", "kenya", "nigeria"]:
        mask = df[outcome].notna()
        for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(MODEL4_CATEGORICAL) + [FE_VAR, "psu"]:
            mask &= df[v].notna()
        mask &= (df["country"] == country)
        samp = df[mask].copy()
        res_reg_c, _ = run_explicit_wls(f"CTRY-A-{country}-{outcome}", samp, outcome, A_CONTINUOUS, MODEL4_CATEGORICAL,
                                         samp["weight_original"], samp["psu"], include_fe=True, fe_col=FE_VAR)
        for term in HOUSEHOLD_EXPOSURES:
            ci = res_reg_c.conf_int()
            country_rows.append({"model": "household_region_fe", "country": country, "outcome": outcome, "term": term,
                                  "coefficient": res_reg_c.params[term], "se": res_reg_c.bse[term],
                                  "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_reg_c.pvalues[term],
                                  "N": int(res_reg_c.nobs), "psu_count": int(samp["psu"].nunique()), "fe_count": int(samp[FE_VAR].nunique())})

        maskB = df[outcome].notna()
        for v in HOUSEHOLD_EXPOSURES + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS + list(CLUSTER_FE_CATEGORICAL) + ["psu"]:
            maskB &= df[v].notna()
        maskB &= (df["country"] == country)
        sampB = df[maskB].copy()
        res_clu_c, *_ = run_cluster_fe_demeaned(f"CTRY-B-{country}-{outcome}", sampB, outcome, B_CONTINUOUS, CLUSTER_FE_CATEGORICAL,
                                                 sampB["weight_original"], "psu")
        for term in HOUSEHOLD_EXPOSURES:
            ci = res_clu_c.conf_int()
            country_rows.append({"model": "household_cluster_fe", "country": country, "outcome": outcome, "term": term,
                                  "coefficient": res_clu_c.params[term], "se": res_clu_c.bse[term],
                                  "ci_lower": ci.loc[term, 0], "ci_upper": ci.loc[term, 1], "p_value": res_clu_c.pvalues[term],
                                  "N": int(res_clu_c.nobs), "psu_count": int(sampB["psu"].nunique()), "fe_count": 0})

        hh_lvl = sampB.drop_duplicates(subset="country_household_id")[["country_household_id", "psu", "_water_hh_binary", "_sani_hh_binary"]]
        grp = hh_lvl.groupby("psu")
        n_psu_total = grp.ngroups
        water_var = int((grp["_water_hh_binary"].nunique() > 1).sum())
        sani_var = int((grp["_sani_hh_binary"].nunique() > 1).sum())
        country_support_rows.append({"country": country, "outcome": outcome, "n_psu_total": n_psu_total,
                                      "n_psu_water_variation": water_var, "pct_water_variation": round(100 * water_var / n_psu_total, 2),
                                      "n_psu_sanitation_variation": sani_var, "pct_sanitation_variation": round(100 * sani_var / n_psu_total, 2)})
        log(f"  [{country}/{outcome}] region-FE N={int(res_reg_c.nobs)}; cluster-FE N={int(res_clu_c.nobs)} "
            f"({n_psu_total} PSUs, water-var {water_var}, sani-var {sani_var}) OK")

country_hh_region_df = pd.DataFrame([r for r in country_rows if r["model"] == "household_region_fe"])
country_hh_region_df.to_csv(OUT_DIR / "14_country_household_region_fe.csv", index=False)
country_hh_cluster_df = pd.DataFrame([r for r in country_rows if r["model"] == "household_cluster_fe"])
country_hh_cluster_df.to_csv(OUT_DIR / "15_country_household_cluster_fe.csv", index=False)
pd.DataFrame(country_support_rows).to_csv(OUT_DIR / "15b_country_cluster_fe_support.csv", index=False)
log("Written: 14_country_household_region_fe.csv, 15_country_household_cluster_fe.csv, 15b_country_cluster_fe_support.csv")

# ============================================================================
# PART 12: FINAL VALIDATION + SUMMARY
# ============================================================================
log("\n" + "=" * 90 + "\nPART 12: FINAL VALIDATION\n" + "=" * 90)

baseline_hashes_after = {k: sha256_of_file(p) for k, p in BASELINE_FILES.items()}
hash_ok = True
for k in BASELINE_FILES:
    if baseline_hashes_before[k] != baseline_hashes_after[k]:
        hash_ok = False
        log(f"  MISMATCH: {k} hash changed!")
if not hash_ok:
    raise RuntimeError("BASELINE FILE HASH MISMATCH DETECTED AFTER DEVELOPMENT RUN. STOP - investigate immediately.")
log("Baseline file hashes RE-VERIFIED IDENTICAL before and after the full development run (all 4 files).")

hash_rows = []
for k in BASELINE_FILES:
    hash_rows.append({"file_key": k, "path": str(BASELINE_FILES[k]), "sha256_before": baseline_hashes_before[k],
                       "sha256_after": baseline_hashes_after[k], "match": baseline_hashes_before[k] == baseline_hashes_after[k]})
pd.DataFrame(hash_rows).to_csv(OUT_DIR / "baseline_file_hashes.csv", index=False)
log("Written: baseline_file_hashes.csv")

summary_rows = []
for _, r in model_a_df[(model_a_df["sample_variant"] == "A2_common_sample") & (model_a_df["term"].isin(HOUSEHOLD_EXPOSURES))].iterrows():
    summary_rows.append({"family": "A_household_region_fe", "outcome": r["outcome"], "term": r["term"],
                          "coefficient": r["coefficient"], "se": r["standard_error"], "p_value": r["p_value"], "N": r["estimation_n"]})
for _, r in model_b_df[(model_b_df["model_label"] == "natural_sample_PRIMARY_SAME_CLUSTER_CRV1") & (model_b_df["term"].isin(HOUSEHOLD_EXPOSURES))].iterrows():
    summary_rows.append({"family": "B_household_cluster_fe", "outcome": r["outcome"], "term": r["term"],
                          "coefficient": r["coefficient"], "se": r["standard_error"], "p_value": r["p_value"], "N": r["estimation_n"]})
for _, r in model_c_df[model_c_df["term"].isin(HOUSEHOLD_EXPOSURES + EXPOSURES)].iterrows():
    summary_rows.append({"family": "C_joint_household_community", "outcome": r["outcome"], "term": r["term"],
                          "coefficient": r["coefficient"], "se": r["standard_error"], "p_value": r["p_value"], "N": r["estimation_n"]})
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(OUT_DIR / "16_development_model_summary.csv", index=False)
log("Written: 16_development_model_summary.csv")

log("\n" + "=" * 90 + "\nDEVELOPMENT RUN COMPLETE - ALL PARTS 0-10 AND 12 EXECUTED SUCCESSFULLY\n" + "=" * 90)
_log_f.close()
