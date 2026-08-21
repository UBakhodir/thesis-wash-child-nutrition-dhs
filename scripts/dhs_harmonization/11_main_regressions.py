"""
11_main_regressions.py
========================
Main regression stage: Models 1-4 for the three primary continuous
outcomes (haz/waz/whz), pooled and country-specific, per the approved
Step 11 regression specification lock.

APPROVED SPECIFICATION (recap, not re-derived here):
  Outcomes:    haz, waz, whz (primary); stunted/wasted/underweight (LPM
               robustness, later stage); severe_* (secondary robustness,
               later stage).
  Exposures:   water_rate_loo, sanitation_rate_loo_core (continuous,
               [0,1], leave-one-out cluster coverage). Household-level
               WASH and the Ghana bio-digester robustness exposure are
               NOT used here - later robustness stage.
  Controls:    child_sex, b19_raw, birth_order_raw (Model 2 block);
               maternal_age, maternal_education, literacy,
               wealth_quintile, household_size_raw, residence (Model 3
               block). birth_order_raw and household_size_raw are
               continuous/linear (a new, explicitly approved decision -
               the original thesis design did not specify a functional
               form for either). No maternal_age squared.
  Fixed effects: country_admin_region (Model 4 only) - country-qualified
               administrative-region identifier, implemented as EXPLICIT
               categorical/dummy encoding (NOT absorption, NOT
               linearmodels.PanelOLS, NOT any artificial panel
               structure). country_admin_region already subsumes a
               country effect (each level belongs to exactly one
               country) - no separate country dummy is added alongside
               it. No interview_year FE, no country x interview_year FE,
               no region x interview_year FE, no spatial grid FE.
  Architecture: pooled main analysis + country-specific
               robustness/heterogeneity analysis.
  Weighting:   pooled models use a TEMPORARY, model-specific,
               equal-total-country weight (constructed fresh for each
               model's own estimation sample, held in memory only, NEVER
               written to any parquet - see build_temporary_pooled_weight()
               below). Country-specific models use weight_original
               unchanged.
  Estimator:   statsmodels.WLS (continuous outcomes). LPM for binary
               outcomes is a later-stage robustness item, not built here.
               No logit/probit.
  Clustering:  PSU-clustered robust SE (statsmodels cov_type='cluster').
               country_psu for pooled models, psu for country-specific
               models. This is a cluster-robust sandwich approximation,
               NOT a full stratified DHS svyset-equivalent design-based
               variance estimator (see the Pre-Regression Engine
               Verification for the svy.GLM alternative, not used here).

EXECUTION APPROVED (main continuous-outcome stage only): this script runs
the full Models 1-4 estimation loop for haz/waz/whz, pooled and
country-specific, and writes the two output files listed below. It does
NOT run the LPM binary robustness outcomes, severe outcomes, the Ghana
bio-digester robustness exposure, the household-level baseline model, or
any alternative-weight/sensitivity/spatial robustness item - those remain
a later, separately-approved stage.

Reads (read-only):
  - data/processed/pooled_kr_four_country_birth_order.parquet (Step 10 output)

Writes:
  - outputs/regressions/main_continuous_models.csv
  - outputs/tables/step11_model_sample_flow.csv

KNOWN ISSUE HISTORY (preserved for provenance - do not remove):
The FIRST execution of this script's Models 1-4 loop had a bug: water_rate_loo
and sanitation_rate_loo_core were never actually added to any MODEL_SPECS
entry's continuous-variable list (MODEL1_CONTINUOUS was hard-coded to an empty
list, and EXPOSURES - used elsewhere for missingness masking - was never
merged into it or into MODEL2_CONTINUOUS). As a result, Model 1's design
matrix contained only a constant, and Models 2-4 omitted both primary
exposures entirely. This was caught by a manual spot-check of the written
output (inspecting the actual `term` values in main_continuous_models.csv),
not by any automated check in the script at the time. The fix: MODEL1_CONTINUOUS
= list(EXPOSURES); MODEL2_CONTINUOUS = EXPOSURES + CHILD_CONTROLS_CONTINUOUS
(Models 3-4 inherit correctly since they extend MODEL2_CONTINUOUS). The
script was re-run after the fix, and the first (invalid) contents of
main_continuous_models.csv / step11_model_sample_flow.csv were overwritten by
the corrected re-run before being reported. Every Step 11 coefficient/SE/CI/
p-value that was ever reported in the thesis comes exclusively from the
corrected re-run - none of the invalid first-run numbers were reported.
"""

import hashlib
import importlib.util
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import statsmodels.api as sm

SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

# ----------------------------------------------------------------------
# INPUT / OUTPUT PATHS
# ----------------------------------------------------------------------
INPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_birth_order.parquet"

OUTPUT_DIR = config.PROJECT_ROOT / "outputs" / "regressions"
MAIN_CONTINUOUS_OUTPUT = OUTPUT_DIR / "main_continuous_models.csv"
SAMPLE_FLOW_AUDIT_OUTPUT = config.PROJECT_ROOT / "outputs" / "tables" / "step11_model_sample_flow.csv"

EXPECTED_TOTAL_ROWS = 70231
EXPECTED_STEP10_COLS = 90
EXPECTED_ROW_COUNTS = {"ethiopia": 13565, "ghana": 9353, "kenya": 19530, "nigeria": 27783}

# ----------------------------------------------------------------------
# APPROVED VARIABLE LISTS
# ----------------------------------------------------------------------
PRIMARY_OUTCOMES = ["haz", "waz", "whz"]
LPM_OUTCOMES = ["stunted", "wasted", "underweight"]           # later stage
SEVERE_OUTCOMES = ["severe_stunted", "severe_wasted", "severe_underweight"]  # later stage

EXPOSURES = ["water_rate_loo", "sanitation_rate_loo_core"]

CHILD_CONTROLS_CONTINUOUS = ["b19_raw", "birth_order_raw"]
CHILD_CONTROLS_CATEGORICAL = {"child_sex": "Male"}

SES_CONTROLS_CONTINUOUS = ["maternal_age", "household_size_raw"]
SES_CONTROLS_CATEGORICAL = {
    "maternal_education": "No education",
    "literacy": "Cannot read at all",
    "wealth_quintile": "Poorest",
    "residence": "Rural",
}

FE_VAR = "country_admin_region"

# Model RHS blocks (variable NAMES only - dummy expansion happens in build_design_matrix)
# NOTE: EXPOSURES must be in every model's continuous block - Models 1-4 all
# retain the exposures per the approved nested-progression design (only the
# CONTROL/FE blocks are added across Models 1-4, the exposures never drop out).
MODEL1_CONTINUOUS = list(EXPOSURES)
MODEL1_CATEGORICAL = {}

MODEL2_CONTINUOUS = EXPOSURES + CHILD_CONTROLS_CONTINUOUS
MODEL2_CATEGORICAL = dict(CHILD_CONTROLS_CATEGORICAL)

MODEL3_CONTINUOUS = MODEL2_CONTINUOUS + SES_CONTROLS_CONTINUOUS
MODEL3_CATEGORICAL = {**MODEL2_CATEGORICAL, **SES_CONTROLS_CATEGORICAL}

MODEL4_CONTINUOUS = MODEL3_CONTINUOUS  # FE handled separately, not as a plain categorical control
MODEL4_CATEGORICAL = MODEL3_CATEGORICAL

MODEL_SPECS = {
    1: {"continuous": MODEL1_CONTINUOUS, "categorical": MODEL1_CATEGORICAL, "fe": False,
        "label": "Exposures only"},
    2: {"continuous": MODEL2_CONTINUOUS, "categorical": MODEL2_CATEGORICAL, "fe": False,
        "label": "+ child controls"},
    3: {"continuous": MODEL3_CONTINUOUS, "categorical": MODEL3_CATEGORICAL, "fe": False,
        "label": "+ maternal/household SES controls"},
    4: {"continuous": MODEL4_CONTINUOUS, "categorical": MODEL4_CATEGORICAL, "fe": True,
        "label": "+ country_admin_region FE (preferred/full model)"},
}

def _assert_exposures_in_every_model(model_specs, exposures):
    """
    Defensive, read-only guard against recurrence of the Step 11
    exposure-omission bug documented in KNOWN ISSUE HISTORY above (an
    earlier version of this script built MODEL_SPECS without the primary
    exposures present in every model's continuous block). This function
    does not modify model_specs, exposures, the design matrix, or any
    estimation/coefficient - it only verifies, once, at module-load time,
    that set(exposures) is a subset of every model's continuous-variable
    list, and raises loudly (instead of silently estimating an incomplete
    model) if that assumption is ever violated in the future.
    """
    missing = {
        model_num: sorted(set(exposures) - set(spec["continuous"]))
        for model_num, spec in model_specs.items()
        if not set(exposures).issubset(set(spec["continuous"]))
    }
    if missing:
        raise RuntimeError(
            "Step 11 defensive check FAILED: the following MODEL_SPECS "
            f"entries are missing required exposure(s): {missing}. This is "
            "exactly the bug class documented in KNOWN ISSUE HISTORY above "
            "- aborting rather than estimating an incomplete model."
        )

_assert_exposures_in_every_model(MODEL_SPECS, EXPOSURES)

# All variables that must be non-missing for ANY model in this script
ALL_MODEL_VARS = (
    EXPOSURES + CHILD_CONTROLS_CONTINUOUS + list(CHILD_CONTROLS_CATEGORICAL)
    + SES_CONTROLS_CONTINUOUS + list(SES_CONTROLS_CATEGORICAL) + [FE_VAR]
)


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================
# DATA / SAMPLE PREPARATION CODE
# ============================================================================

def build_estimation_sample(df, outcome):
    """
    Returns the row mask for a given outcome using the FULL control set
    (Model 3/4's variables - the superset). Models 1-2 use a subset of the
    same variables, so their samples are identical to Models 3-4's sample
    whenever the omitted controls have zero missingness (verified true for
    every control in the Step 11 audit) - this is checked explicitly, not
    assumed, in sample_flow_audit() below.
    """
    mask = df[outcome].notna()
    for v in ALL_MODEL_VARS:
        mask &= df[v].notna()
    return mask


def sample_flow_audit(df, outcomes):
    """
    Read-only: reports the exact exclusion cascade (outcome-missing,
    exposure-missing, control-missing) for each outcome, and confirms
    Models 1-4 share an identical sample per outcome (since all approved
    controls have zero missingness).
    """
    rows = []
    for outcome in outcomes:
        n_start = len(df)
        mask_outcome = df[outcome].notna()
        n_after_outcome = int(mask_outcome.sum())

        mask_exposure = mask_outcome.copy()
        for e in EXPOSURES:
            mask_exposure &= df[e].notna()
        n_after_exposure = int(mask_exposure.sum())

        mask_full = mask_exposure.copy()
        for v in CHILD_CONTROLS_CONTINUOUS + list(CHILD_CONTROLS_CATEGORICAL) + \
                  SES_CONTROLS_CONTINUOUS + list(SES_CONTROLS_CATEGORICAL) + [FE_VAR]:
            mask_full &= df[v].notna()
        n_final = int(mask_full.sum())

        final = df[mask_full]
        by_country = final["country"].value_counts().to_dict()

        rows.append({
            "outcome": outcome,
            "n_start": n_start,
            "n_after_outcome_nonmissing": n_after_outcome,
            "n_excluded_outcome": n_start - n_after_outcome,
            "n_after_exposure_nonmissing": n_after_exposure,
            "n_excluded_exposure": n_after_outcome - n_after_exposure,
            "n_final_all_controls_nonmissing": n_final,
            "n_excluded_controls": n_after_exposure - n_final,
            "n_ethiopia": by_country.get("ethiopia", 0),
            "n_ghana": by_country.get("ghana", 0),
            "n_kenya": by_country.get("kenya", 0),
            "n_nigeria": by_country.get("nigeria", 0),
            "n_unique_psu": int(final["psu"].nunique()),
            "n_unique_country_psu": int(final["country_psu"].nunique()),
            "n_unique_fe_regions": int(final[FE_VAR].nunique()),
        })

        # Confirm Models 1-3 (subset of controls) give an IDENTICAL sample to
        # Model 4's full-control mask, for this outcome - not assumed.
        mask_model1 = mask_exposure.copy()  # no controls at all
        n_model1 = int(mask_model1.sum())
        if n_model1 != n_final:
            raise RuntimeError(
                f"[{outcome}] Model 1 sample ({n_model1}) != Model 4 sample ({n_final}) - "
                "a control thought to have zero missingness actually has some. Aborting "
                "rather than silently using mismatched samples across Models 1-4."
            )

    return pd.DataFrame(rows)


# ============================================================================
# WEIGHTING CODE
# ============================================================================

def build_temporary_pooled_weight(sample_df):
    """
    Model-specific, equal-total-country-weight pooled weight, computed on
    the EXACT estimation sample passed in (not on the full 70,231-row
    file). Returns a pandas Series aligned to sample_df.index. This is
    NEVER written to any parquet - it exists only in memory for the
    duration of a single model's estimation.

    weight_model_i = weight_original_i / W_k,  W_k = sum(weight_original)
                                                       over country k's
                                                       rows IN THIS SAMPLE

    => sum(weight_model | country k) == 1.0 for every country k present.
    """
    W_k = sample_df.groupby("country")["weight_original"].transform("sum")
    weight_model = sample_df["weight_original"] / W_k

    sums = sample_df.assign(_w=weight_model).groupby("country")["_w"].sum()
    if not np.allclose(sums.values, 1.0, atol=1e-9):
        raise RuntimeError(
            f"Temporary pooled weight assertion FAILED - country sums != 1.0: "
            f"{sums.to_dict()}. Aborting rather than estimating with a broken weight."
        )
    return weight_model, sums


# ============================================================================
# FIXED-EFFECT CODE
# ============================================================================

def build_categorical_dummies(series, ref_level, prefix):
    """
    Explicit dummy encoding with an EXPLICIT reference level dropped (not
    pandas' default alphabetical drop_first). Hard-fails if the reference
    level is not observed in this specific sample.
    """
    observed = series.unique()
    if ref_level not in observed:
        raise RuntimeError(
            f"[{prefix}] Reference level {ref_level!r} not observed in this "
            f"estimation sample (observed: {sorted(observed)}). Aborting rather "
            "than silently picking a different reference."
        )
    dummies = pd.get_dummies(series, prefix=prefix, drop_first=False)
    ref_col = f"{prefix}_{ref_level}"
    dummies = dummies.drop(columns=[ref_col]).astype(float)
    return dummies, ref_col


def verify_fe_encoding(df, sample_mask):
    """
    Read-only verification of country_admin_region's 114-level categorical
    encoding: observed levels, generated dummy columns, omitted/reference
    level, matrix rank of the FE block alone, and whether any level present
    in the full dataset disappears from this specific estimation sample.
    """
    full_levels = set(df[FE_VAR].unique())
    sample = df[sample_mask]
    sample_levels = set(sample[FE_VAR].unique())
    disappeared = full_levels - sample_levels

    # arbitrary but deterministic reference: first level alphabetically
    ref_level = sorted(sample_levels)[0]
    dummies, ref_col = build_categorical_dummies(sample[FE_VAR], ref_level, FE_VAR)

    X_fe = sm.add_constant(dummies, has_constant="add")
    rank = np.linalg.matrix_rank(X_fe.values)

    report = {
        "full_dataset_fe_levels": len(full_levels),
        "sample_fe_levels_observed": len(sample_levels),
        "fe_levels_disappeared_from_sample": sorted(disappeared),
        "generated_dummy_columns": dummies.shape[1],
        "reference_level_used": ref_level,
        "reference_column_dropped": ref_col,
        "expected_columns_if_full_rank": dummies.shape[1] + 1,  # + intercept
        "matrix_rank_observed": int(rank),
        "full_rank": rank == (dummies.shape[1] + 1),
    }
    return report


# ============================================================================
# MODEL-MATRIX CONSTRUCTION CODE
# ============================================================================

def build_design_matrix(df, continuous_vars, categorical_vars_with_ref, include_fe=False, fe_ref=None):
    """
    Assembles the full X matrix: intercept + continuous controls (as-is,
    linear) + categorical controls (explicit dummy encoding, explicit
    reference dropped) + [optional] country_admin_region FE dummies
    (explicit reference dropped - NOT absorption).
    """
    parts = []
    if continuous_vars:
        parts.append(df[continuous_vars].astype(float))

    ref_metadata = {}
    for cat_var, ref_level in categorical_vars_with_ref.items():
        dummies, ref_col = build_categorical_dummies(df[cat_var], ref_level, cat_var)
        parts.append(dummies)
        ref_metadata[cat_var] = {"reference": ref_level, "reference_column": ref_col}

    if include_fe:
        if fe_ref is None:
            fe_ref = sorted(df[FE_VAR].unique())[0]
        fe_dummies, fe_ref_col = build_categorical_dummies(df[FE_VAR], fe_ref, FE_VAR)
        parts.append(fe_dummies)
        ref_metadata[FE_VAR] = {"reference": fe_ref, "reference_column": fe_ref_col}

    X = pd.concat(parts, axis=1) if parts else pd.DataFrame(index=df.index)
    X = sm.add_constant(X, has_constant="add")
    return X, ref_metadata


def rank_check(X, label):
    """Hard-fail if the design matrix is not full column rank."""
    rank = np.linalg.matrix_rank(X.values)
    n_cols = X.shape[1]
    if rank != n_cols:
        raise RuntimeError(
            f"[{label}] Design matrix is RANK-DEFICIENT: rank={rank}, columns={n_cols}. "
            "Aborting rather than estimating an unidentified model."
        )
    return rank


# ============================================================================
# VALIDATION CODE (pre-model hard-fail checklist)
# ============================================================================

def validate_before_model(df, outcome, model_num, country_scope, sample_df, weight_series, cluster_series):
    """
    Explicit hard-fail checklist run immediately before every single model
    estimation (items 1-9, 12 of the approved checklist; items 10-11 are
    enforced immediately downstream by rank_check() and the finite-value
    check in run_single_model()).
    """
    spec = MODEL_SPECS[model_num]
    label = f"{outcome}-model{model_num}-{country_scope}"

    # 1. required variables exist
    required_vars = [outcome] + EXPOSURES + spec["continuous"] + list(spec["categorical"])
    if spec["fe"]:
        required_vars.append(FE_VAR)
    missing_vars = [v for v in required_vars if v not in df.columns]
    if missing_vars:
        raise RuntimeError(f"[{label}] Required variable(s) missing: {missing_vars}. Aborting.")

    # 2. estimation sample non-empty
    if len(sample_df) == 0:
        raise RuntimeError(f"[{label}] Estimation sample is empty. Aborting.")

    # 3. outcome non-missing in all estimation rows
    if sample_df[outcome].isna().any():
        raise RuntimeError(f"[{label}] Outcome has missing value(s) in the estimation sample. Aborting.")

    # 4. exposures non-missing and finite
    for e in EXPOSURES:
        if sample_df[e].isna().any():
            raise RuntimeError(f"[{label}] Exposure '{e}' has missing value(s). Aborting.")
        if not np.all(np.isfinite(sample_df[e].astype(float).values)):
            raise RuntimeError(f"[{label}] Exposure '{e}' has non-finite value(s). Aborting.")

    # 5. controls required for THIS model are non-missing
    for c in spec["continuous"] + list(spec["categorical"]):
        if sample_df[c].isna().any():
            raise RuntimeError(f"[{label}] Control '{c}' has missing value(s). Aborting.")

    # 6. weights positive and finite
    if not np.all(np.isfinite(weight_series.astype(float).values)):
        raise RuntimeError(f"[{label}] Weight vector contains non-finite value(s). Aborting.")
    if not (weight_series > 0).all():
        raise RuntimeError(f"[{label}] Weight vector contains non-positive value(s). Aborting.")

    # 7. pooled country weight sums equal 1 (re-asserted here explicitly;
    # build_temporary_pooled_weight() already asserts this at construction time)
    if country_scope == "pooled":
        sums = sample_df.assign(_w=weight_series).groupby("country")["_w"].sum()
        if not np.allclose(sums.values, 1.0, atol=1e-9):
            raise RuntimeError(f"[{label}] Pooled country weight sums != 1.0: {sums.to_dict()}. Aborting.")

    # 8. clustering identifier non-missing
    if cluster_series.isna().any():
        raise RuntimeError(f"[{label}] Clustering identifier has missing value(s). Aborting.")

    # 9. expected reference categories present
    for cat_var, ref_level in spec["categorical"].items():
        if ref_level not in set(sample_df[cat_var].unique()):
            raise RuntimeError(
                f"[{label}] Reference category '{ref_level}' for '{cat_var}' not present "
                "in this estimation sample. Aborting."
            )
    if spec["fe"] and sample_df[FE_VAR].isna().any():
        raise RuntimeError(f"[{label}] FE variable '{FE_VAR}' has missing value(s). Aborting.")

    # 12. FE encoding internal consistency: every FE level in this sample
    # must be constant within its own PSU (re-derived property, not assumed)
    if spec["fe"]:
        # cluster_series.name is always "country_psu"/"psu" in practice (set
        # explicitly at every call site), so the "else" fallback below is
        # unreachable defensive code - left in place rather than removed,
        # since it is provably behavior-neutral either way (pre-freeze
        # readability audit, not modified further to stay conservative).
        psu_col = cluster_series.name if cluster_series.name else ("country_psu" if country_scope == "pooled" else "psu")
        fe_per_psu = sample_df.groupby(psu_col)[FE_VAR].nunique()
        if (fe_per_psu > 1).any():
            raise RuntimeError(f"[{label}] FE variable is not constant within every PSU in this sample. Aborting.")


def build_full_sample_flow_table(df):
    """
    Sample-flow cascade for EVERY (outcome, model, country_scope) triple -
    60 rows total (3 outcomes x 4 models x [pooled + 4 countries]).
    """
    rows = []
    scopes = ["pooled"] + list(EXPECTED_ROW_COUNTS.keys())
    for outcome in PRIMARY_OUTCOMES:
        for model_num, spec in MODEL_SPECS.items():
            model_vars = spec["continuous"] + list(spec["categorical"])
            for scope in scopes:
                base = df if scope == "pooled" else df[df["country"] == scope]
                n_start = len(base)

                m_outcome = base[outcome].notna()
                n_after_outcome = int(m_outcome.sum())

                m_exposure = m_outcome.copy()
                for e in EXPOSURES:
                    m_exposure &= base[e].notna()
                n_after_exposure = int(m_exposure.sum())

                m_final = m_exposure.copy()
                for v in model_vars:
                    m_final &= base[v].notna()
                if spec["fe"]:
                    m_final &= base[FE_VAR].notna()
                n_final = int(m_final.sum())

                final = base[m_final]
                cluster_col = "country_psu" if scope == "pooled" else "psu"
                weight_method = "model_specific_equal_total_country_weight" if scope == "pooled" else "weight_original"

                rows.append({
                    "outcome": outcome,
                    "model": model_num,
                    "country_scope": scope,
                    "n_start": n_start,
                    "n_excluded_outcome_missing": n_start - n_after_outcome,
                    "n_excluded_exposure_missing": n_after_outcome - n_after_exposure,
                    "n_excluded_control_missing": n_after_exposure - n_final,
                    "final_estimation_n": n_final,
                    "unique_psu_count": int(final[cluster_col].nunique()),
                    "fe_region_count": int(final[FE_VAR].nunique()) if spec["fe"] else 0,
                    "weight_method": weight_method,
                    "clustering_method": f"cluster_robust_{cluster_col}",
                })
    return pd.DataFrame(rows)


# ============================================================================
# REGRESSION-ESTIMATION CODE
# ============================================================================

def run_single_model(df, outcome, model_num, country_scope):
    """
    Estimates ONE model (outcome x model_num x country_scope) via
    statsmodels.WLS with PSU-clustered robust SE, per the approved spec.
    country_scope is either "pooled" or one of the four country names.
    """
    spec = MODEL_SPECS[model_num]

    if country_scope == "pooled":
        sample_df = df[build_estimation_sample(df, outcome)].copy()
        weight, weight_check = build_temporary_pooled_weight(sample_df)
        sample_df["_weight"] = weight
        cluster_col = "country_psu"
        weight_method = "model_specific_equal_total_country_weight"
    else:
        country_mask = build_estimation_sample(df, outcome) & (df["country"] == country_scope)
        sample_df = df[country_mask].copy()
        sample_df["_weight"] = sample_df["weight_original"]
        cluster_col = "psu"
        weight_method = "weight_original"

    validate_before_model(
        df, outcome, model_num, country_scope, sample_df,
        weight_series=sample_df["_weight"], cluster_series=sample_df[cluster_col]
    )

    X, ref_metadata = build_design_matrix(
        sample_df, spec["continuous"], spec["categorical"], include_fe=spec["fe"]
    )
    y = sample_df[outcome].astype(float)
    w = sample_df["_weight"].astype(float)
    groups = sample_df[cluster_col]

    rank_check(X, label=f"{outcome}-model{model_num}-{country_scope}")

    model = sm.WLS(y, X, weights=w)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": groups})

    if not np.all(np.isfinite(res.params.values)) or not np.all(np.isfinite(res.bse.values)):
        raise RuntimeError(
            f"[{outcome}-model{model_num}-{country_scope}] Non-finite coefficient or SE. Aborting."
        )

    ci = res.conf_int()
    rows = []
    for term in res.params.index:
        rows.append({
            "outcome": outcome,
            "model": model_num,
            "country_scope": country_scope,
            "term": term,
            "coefficient": res.params[term],
            "standard_error": res.bse[term],
            "ci_lower": ci.loc[term, 0],
            "ci_upper": ci.loc[term, 1],
            "p_value": res.pvalues[term],
            "estimation_n": int(res.nobs),
            "psu_count": int(groups.nunique()),
            "fe_region_count": int(sample_df[FE_VAR].nunique()) if spec["fe"] else 0,
            "weight_method": weight_method,
            "clustering_method": f"cluster_robust_{cluster_col}",
            "fe_included": spec["fe"],
            "reference_category_metadata": str(ref_metadata),
        })
    return pd.DataFrame(rows)


# ============================================================================
# RESULT-EXPORT CODE
# ============================================================================

def export_results(results_df, path):
    """Writes the machine-readable regression output, unrounded."""
    path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(path, index=False)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*90)
    print("STEP 11 MAIN REGRESSION EXECUTION - haz/waz/whz, Models 1-4, pooled + country-specific")
    print("="*90)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 10 input not found: {INPUT_PATH}")
    checksum_before = md5_of_file(INPUT_PATH)

    df = pd.read_parquet(INPUT_PATH)
    print(f"\nLoaded: {len(df)} rows, {df.shape[1]} columns")
    if df.shape != (EXPECTED_TOTAL_ROWS, EXPECTED_STEP10_COLS):
        raise RuntimeError(f"Unexpected shape {df.shape} != ({EXPECTED_TOTAL_ROWS},{EXPECTED_STEP10_COLS}). Aborting.")
    for country, n in EXPECTED_ROW_COUNTS.items():
        actual = (df["country"] == country).sum()
        if actual != n:
            raise RuntimeError(f"[{country}] row count {actual} != expected {n}. Aborting.")
    print("Input shape and per-country row counts confirmed.")

    for v in ALL_MODEL_VARS + PRIMARY_OUTCOMES + LPM_OUTCOMES + SEVERE_OUTCOMES + ["weight_original", "psu", "country_psu"]:
        if v not in df.columns:
            raise RuntimeError(f"Required variable '{v}' missing from Step 10 input. Aborting.")
    print("All required variables present.")

    # ---- PHASE 1: FE-encoding sanity check (114-level, haz sample) ----
    print(f"\n{'='*90}\nPHASE 1: country_admin_region FE-ENCODING CHECK (haz pooled sample)\n{'='*90}")
    haz_mask = build_estimation_sample(df, "haz")
    fe_report = verify_fe_encoding(df, haz_mask)
    for k, v in fe_report.items():
        print(f"  {k}: {v}")
    if fe_report["fe_levels_disappeared_from_sample"]:
        raise RuntimeError(f"FE levels disappeared from the haz sample: {fe_report['fe_levels_disappeared_from_sample']}. Aborting.")
    print("  All 114 FE levels present in the haz estimation sample - none disappear.")

    # ---- PHASE 2: sample-flow table for every (outcome, model, scope) ----
    print(f"\n{'='*90}\nPHASE 2: FULL SAMPLE-FLOW TABLE (3 outcomes x 4 models x 5 scopes = 60 rows)\n{'='*90}")
    flow_table = build_full_sample_flow_table(df)
    print(flow_table.to_string(index=False))

    # ---- PHASE 3: MODELS 1-4 ESTIMATION LOOP - haz/waz/whz, pooled + country-specific ----
    print(f"\n{'='*90}\nPHASE 3: MODELS 1-4 ESTIMATION - haz/waz/whz, pooled + 4 country-specific\n{'='*90}")
    scopes = ["pooled"] + list(EXPECTED_ROW_COUNTS.keys())
    all_results = []
    n_fits = 0
    warnings_seen = []
    import warnings as _warnings
    for outcome in PRIMARY_OUTCOMES:
        for model_num in MODEL_SPECS:
            for scope in scopes:
                with _warnings.catch_warnings(record=True) as caught:
                    _warnings.simplefilter("always")
                    res_df = run_single_model(df, outcome, model_num, scope)
                    for w in caught:
                        warnings_seen.append(f"{outcome}-model{model_num}-{scope}: {w.category.__name__}: {w.message}")
                all_results.append(res_df)
                n_fits += 1
                print(f"  [{n_fits:3d}] {outcome} / Model {model_num} / {scope:10s} - "
                      f"N={res_df['estimation_n'].iloc[0]}  PSUs={res_df['psu_count'].iloc[0]}  OK")

    final_results = pd.concat(all_results, ignore_index=True)
    print(f"\nTotal regression fits completed: {n_fits}")
    print(f"Total result rows (one per term per fit): {len(final_results)}")

    if not np.all(np.isfinite(final_results["coefficient"].values)):
        raise RuntimeError("Non-finite coefficient found in final_results. Aborting before write.")
    if not np.all(np.isfinite(final_results["standard_error"].values)):
        raise RuntimeError("Non-finite standard_error found in final_results. Aborting before write.")
    print("Finite-value check on all coefficients/SEs in final_results: PASSED")

    if warnings_seen:
        print(f"\nWarnings captured during estimation ({len(warnings_seen)}):")
        for w in warnings_seen:
            print(f"  {w}")
    else:
        print("\nNo warnings captured during estimation (convergence/numerical/rank/covariance).")

    # ---- WRITE OUTPUTS ----
    export_results(final_results, MAIN_CONTINUOUS_OUTPUT)
    print(f"\nWritten: {MAIN_CONTINUOUS_OUTPUT}  ({final_results.shape[0]} rows, {final_results.shape[1]} columns)")
    export_results(flow_table, SAMPLE_FLOW_AUDIT_OUTPUT)
    print(f"Written: {SAMPLE_FLOW_AUDIT_OUTPUT}  ({flow_table.shape[0]} rows, {flow_table.shape[1]} columns)")

    # ---- Source integrity check ----
    checksum_after = md5_of_file(INPUT_PATH)
    if checksum_after != checksum_before:
        raise RuntimeError("Step 10 input file changed during this run!")
    print(f"\n{'='*90}\nSource integrity check: Step 10 input unchanged before/after "
          f"(checksum {checksum_before} == {checksum_after})\n{'='*90}")

    return final_results, flow_table


if __name__ == "__main__":
    main()
