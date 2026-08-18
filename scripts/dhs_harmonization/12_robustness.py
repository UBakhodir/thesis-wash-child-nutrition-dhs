"""
12_robustness.py
==================
Step 12 robustness battery for the Step 11 preferred Model 4 specification,
per the approved Step 12 robustness design audit and execution approval.

WHAT THIS SCRIPT RUNS (six independent robustness families, each with its
own machine-readable output file - never mixed into one undifferentiated
table, so a reader can tell at a glance which robustness question a given
row answers):

  1. BINARY LPM ROBUSTNESS - stunted/wasted/underweight, preferred Model 4
     RHS (exposures + full control set + country_admin_region FE), pooled
     + all four country-specific scopes. Estimator is still statsmodels.WLS
     (a weighted Linear Probability Model IS just WLS on a 0/1 outcome -
     no new estimator is introduced). WHY Model 4 only, not Models 1-3:
     the approved robustness plan treats binary outcomes purely as an
     alternative *outcome coding* check on the preferred specification,
     not as a fresh nested-build-up exercise already done once for the
     continuous outcomes in Step 11.

  2. SEVERE OUTCOMES (secondary/appendix) - severe_stunted/wasted/
     underweight, preferred Model 4, POOLED ONLY. WHY pooled only: the
     Step 12 audit found severe_wasted has 24/114 zero-event FE regions
     (18 of them in Kenya alone) - a country-specific severe_wasted model
     would have many region dummies perfectly predicting zero, which is
     not something to present as a headline or even an appendix
     coefficient. The sparsity diagnostics themselves (event count,
     prevalence, zero-event region count) are written into the output so
     a reader sees the sparsity, not just a coefficient. The "18 in Kenya
     alone" figure was independently re-verified read-only (pre-freeze
     remediation stage) by replicating this exact sample/groupby logic
     against the current data: 24/114 zero-event regions overall, split
     kenya=18, nigeria=3, ghana=2, ethiopia=1 - see
     outputs/final_audit/kenya_zero_event_region_verification.txt.

  3. GHANA BIO-DIGESTER SANITATION ROBUSTNESS - swaps ONLY
     sanitation_rate_loo_core for sanitation_rate_loo_robustness_
     biodigester in the preferred Model 4 RHS; water_rate_loo and every
     control/FE/weight/clustering choice is unchanged. Run pooled AND
     Ghana-specific. WHY pooled is safe here (unlike other robustness
     families, which stay pooled-only or country-specific-only by
     design): the two sanitation-rate columns are proven (Step 08, and
     re-asserted below as a hard-fail, not just cited) to be identical
     for every non-Ghana row, so the pooled comparison isolates exactly
     the Ghana-specific reclassification with no contamination from the
     other three countries.

  4. HOUSEHOLD-LEVEL WASH BASELINE - follows thesis_design.md Section 9.1
     LITERALLY: household-level binary WASH variables, full control set,
     but explicitly NO country_admin_region FE (Section 9.1's own words:
     "Household-level treatment variables, no fixed effects... expected
     to suffer from omitted variable bias"). Pooled only, haz/waz/whz.
     Explicit WASH states (Unknown, StructuralNotApplicable,
     UnclassifiedBioDigester) are excluded from the binary indicator
     (mapped to NaN, never silently coded 0) - checked with a hard-fail
     assertion in build_household_wash_indicators(), not merely assumed
     from the mapping dictionary.

  5. ALTERNATIVE POOLED WEIGHTING - haz/waz/whz, preferred Model 4
     structure (same exposures/controls/FE/clustering), comparing three
     weighting choices: (A) the approved model-specific equal-total-
     country weight (Step 11's method, recomputed here fresh for a clean
     side-by-side comparison); (B) raw weight_original with no rescaling;
     (C) unweighted (every row weight 1.0, equivalent to OLS). Only (A)
     is asserted to sum to 1.0 per country - (B) and (C) have no such
     property by construction and are not checked against it.

  6. LOO DENOMINATOR SENSITIVITY - haz/waz/whz, preferred Model 4
     structure, POOLED ONLY, comparing the unrestricted approved sample
     against two BOTH-exposures-simultaneously minimum-denominator
     restrictions (>=5/>=5 and >=10/>=10 "other household" counts,
     illustrative thresholds only - not a new preferred sample
     definition, reported strictly as sensitivity).

WHAT THIS SCRIPT DOES NOT RUN (explicitly out of scope this stage): Nigeria
five-cluster exclusion, country-specific severe outcomes, Kenya-specific
severe_wasted, any spatial/grid model, any new raster-based model, raw
uncentered maternal_age squared, Models 1-3 repeated for anything, any new
permanent/persisted weight column, any new analytical parquet, any causal
interpretation.

REUSE, NOT DUPLICATION: this script imports scripts/dhs_harmonization/
11_main_regressions.py and reuses its build_design_matrix(),
build_categorical_dummies(), build_temporary_pooled_weight(), rank_check(),
build_estimation_sample(), md5_of_file(), and the approved MODEL4_CONTINUOUS/
MODEL4_CATEGORICAL/FE_VAR constants directly - the model-matrix construction,
weighting, and rank-checking machinery is never reimplemented here. Only the
per-family SAMPLE DEFINITION and WHICH VARIABLES enter the RHS differ across
the six families, which is genuinely new specification logic each time (not
duplicated regression logic).

Reads (read-only):
  - data/processed/pooled_kr_four_country_birth_order.parquet (Step 10 output)
  - outputs/regressions/main_continuous_models.csv (Step 11 output, read-only,
    checksummed before/after - never opened in write mode)
  - outputs/tables/step11_model_sample_flow.csv (Step 11 output, same)

Writes:
  - outputs/regressions/robustness_binary_lpm.csv
  - outputs/regressions/robustness_biodigester.csv
  - outputs/regressions/robustness_household_wash.csv
  - outputs/regressions/robustness_alternative_weights.csv
  - outputs/regressions/robustness_loo_denominator.csv
  - outputs/regressions/appendix/severe_outcomes.csv
  - outputs/tables/step12_robustness_sample_flow.csv

All coefficients below and in the console/report output are associations,
not causal effects - no causal language is used anywhere in this script's
comments, prints, or column names.
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

# Step 11's script is imported (never modified) so its verified model-matrix,
# weighting, and rank-check machinery is reused rather than re-implemented.
reg = _load_module("11_main_regressions.py", "dhs_main_regressions")
config = reg.config

# ----------------------------------------------------------------------
# INPUT / OUTPUT PATHS
# ----------------------------------------------------------------------
INPUT_PATH = reg.INPUT_PATH  # Step 10 output - same file Step 11 reads
STEP11_OUTPUTS_TO_PRESERVE = [reg.MAIN_CONTINUOUS_OUTPUT, reg.SAMPLE_FLOW_AUDIT_OUTPUT]

OUTPUT_DIR = config.PROJECT_ROOT / "outputs" / "regressions"
APPENDIX_DIR = OUTPUT_DIR / "appendix"

BINARY_LPM_OUTPUT = OUTPUT_DIR / "robustness_binary_lpm.csv"
BIODIGESTER_OUTPUT = OUTPUT_DIR / "robustness_biodigester.csv"
HOUSEHOLD_WASH_OUTPUT = OUTPUT_DIR / "robustness_household_wash.csv"
ALT_WEIGHTS_OUTPUT = OUTPUT_DIR / "robustness_alternative_weights.csv"
LOO_DENOMINATOR_OUTPUT = OUTPUT_DIR / "robustness_loo_denominator.csv"
SEVERE_OUTPUT = APPENDIX_DIR / "severe_outcomes.csv"
SAMPLE_FLOW_OUTPUT = config.PROJECT_ROOT / "outputs" / "tables" / "step12_robustness_sample_flow.csv"

EXPECTED_TOTAL_ROWS = reg.EXPECTED_TOTAL_ROWS
EXPECTED_STEP10_COLS = reg.EXPECTED_STEP10_COLS
EXPECTED_ROW_COUNTS = reg.EXPECTED_ROW_COUNTS
COUNTRIES = list(EXPECTED_ROW_COUNTS.keys())

# ----------------------------------------------------------------------
# SPECIFICATION CONSTANTS (explicit, not magic numbers)
# ----------------------------------------------------------------------
PRIMARY_OUTCOMES = reg.PRIMARY_OUTCOMES                 # ["haz","waz","whz"]
BINARY_OUTCOMES = reg.LPM_OUTCOMES                      # ["stunted","wasted","underweight"]
SEVERE_OUTCOMES = reg.SEVERE_OUTCOMES                    # severe_*

# Pairing used to re-assert that each binary outcome's non-missing count
# matches its corresponding continuous z-score's non-missing count exactly
# (both are governed by the same underlying DHS anthropometry-completion
# flag - this is a hard-fail check, not an assumption).
BINARY_TO_ZSCORE_PAIR = {"stunted": "haz", "wasted": "whz", "underweight": "waz"}

FE_VAR = reg.FE_VAR
MODEL4_CONTINUOUS = reg.MODEL4_CONTINUOUS                # [exposures + all continuous controls]
MODEL4_CATEGORICAL = reg.MODEL4_CATEGORICAL              # {categorical control: reference level}

GHANA_BIODIGESTER_CONTINUOUS = [
    "sanitation_rate_loo_robustness_biodigester" if v == "sanitation_rate_loo_core" else v
    for v in MODEL4_CONTINUOUS
]

# Household-level baseline (thesis_design.md Section 9.1, literal): no FE,
# same control set, but the exposures are the two new household-binary
# columns built by build_household_wash_indicators() below, not the
# cluster leave-one-out rates.
HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS = [
    v for v in MODEL4_CONTINUOUS if v not in ("water_rate_loo", "sanitation_rate_loo_core")
]

LOO_DENOMINATOR_THRESHOLDS = {"unrestricted": None, "min5": 5, "min10": 10}


def md5_of_file(path):
    return reg.md5_of_file(path)


# ============================================================================
# DATA / SAMPLE PREPARATION CODE
# ============================================================================

def build_household_wash_indicators(df):
    """
    Household-level binary WASH exposures for the Section 9.1 baseline.
    Explicit non-substantive DHS states (Unknown, StructuralNotApplicable,
    and - for sanitation - UnclassifiedBioDigester) map to NaN (excluded),
    never to 0. This is verified with a hard-fail assertion immediately
    below, not merely assumed from the mapping dictionaries.
    """
    water_map = {"Improved": 1.0, "Unimproved": 0.0, "SurfaceWater": 0.0}
    sanitation_map = {"Improved": 1.0, "NonImproved": 0.0}

    water_bin = df["water_category"].map(water_map)
    sanitation_bin = df["sanitation_collapsed_core"].map(sanitation_map)

    excluded_water = df["water_category"].isin(["Unknown", "StructuralNotApplicable"])
    if not water_bin[excluded_water].isna().all():
        raise RuntimeError(
            "Household water baseline: an excluded state (Unknown/StructuralNotApplicable) "
            "resolved to a non-missing binary value instead of NaN. Aborting."
        )
    excluded_sanitation = df["sanitation_collapsed_core"].isin(
        ["Unknown", "StructuralNotApplicable", "UnclassifiedBioDigester"]
    )
    if not sanitation_bin[excluded_sanitation].isna().all():
        raise RuntimeError(
            "Household sanitation baseline: an excluded state (Unknown/StructuralNotApplicable/"
            "UnclassifiedBioDigester) resolved to a non-missing binary value instead of NaN. Aborting."
        )
    return water_bin, sanitation_bin


def assert_ghana_biodigester_isolated(df):
    """
    Hard-fail re-assertion (not just a cited audit finding) that the
    bio-digester robustness sanitation rate is identical to the core rate
    for every non-Ghana row - the pooled Ghana-robustness comparison is
    only valid because of this property.
    """
    non_ghana = df["country"] != "ghana"
    differs = df.loc[non_ghana, "sanitation_rate_loo_core"] != df.loc[non_ghana, "sanitation_rate_loo_robustness_biodigester"]
    if differs.any():
        raise RuntimeError(
            f"{int(differs.sum())} non-Ghana row(s) differ between sanitation_rate_loo_core and "
            "sanitation_rate_loo_robustness_biodigester - the pooled Ghana-robustness comparison "
            "is invalid under this condition. Aborting."
        )


def assert_binary_matches_zscore_denominator(df):
    """
    Hard-fail re-assertion that each binary outcome's non-missing count
    exactly matches its paired continuous z-score's non-missing count -
    both are governed by the same DHS anthropometry-completion flag.
    """
    for binary_outcome, zscore_outcome in BINARY_TO_ZSCORE_PAIR.items():
        n_binary = int(df[binary_outcome].notna().sum())
        n_zscore = int(df[zscore_outcome].notna().sum())
        if n_binary != n_zscore:
            raise RuntimeError(
                f"{binary_outcome} non-missing N ({n_binary}) != paired z-score {zscore_outcome} "
                f"non-missing N ({n_zscore}). Aborting - denominators must match exactly."
            )


# ============================================================================
# VALIDATION CODE (generic pre-fit hard-fail checklist, reused across all
# six robustness families rather than re-implemented per family)
# ============================================================================

def validate_before_fit(label, sample_df, outcome, continuous_vars, categorical_vars_with_ref,
                         fe_required, weight_series, cluster_series,
                         weight_must_sum_to_one_per_country=False, binary_outcome=False):
    if len(sample_df) == 0:
        raise RuntimeError(f"[{label}] Empty estimation sample. Aborting.")
    if sample_df[outcome].isna().any():
        raise RuntimeError(f"[{label}] Outcome has missing value(s). Aborting.")
    if binary_outcome:
        vals = set(sample_df[outcome].dropna().unique())
        if not vals <= {0, 1}:
            raise RuntimeError(f"[{label}] Binary outcome has value(s) outside {{0,1}}: {vals}. Aborting.")
    for v in continuous_vars:
        if sample_df[v].isna().any():
            raise RuntimeError(f"[{label}] Continuous variable '{v}' has missing value(s). Aborting.")
        if not np.all(np.isfinite(sample_df[v].astype(float).values)):
            raise RuntimeError(f"[{label}] Continuous variable '{v}' has non-finite value(s). Aborting.")
    for cat_var, ref_level in categorical_vars_with_ref.items():
        if sample_df[cat_var].isna().any():
            raise RuntimeError(f"[{label}] Categorical variable '{cat_var}' has missing value(s). Aborting.")
        if ref_level not in set(sample_df[cat_var].unique()):
            raise RuntimeError(
                f"[{label}] Reference category '{ref_level}' for '{cat_var}' is absent from this "
                "estimation sample. Aborting."
            )
    if fe_required and sample_df[FE_VAR].isna().any():
        raise RuntimeError(f"[{label}] FE variable has missing value(s). Aborting.")
    if not np.all(np.isfinite(weight_series.astype(float).values)):
        raise RuntimeError(f"[{label}] Weight vector has non-finite value(s). Aborting.")
    if not (weight_series > 0).all():
        raise RuntimeError(f"[{label}] Weight vector has non-positive value(s). Aborting.")
    if cluster_series.isna().any():
        raise RuntimeError(f"[{label}] Clustering identifier has missing value(s). Aborting.")
    if weight_must_sum_to_one_per_country:
        sums = sample_df.assign(_w=weight_series).groupby("country")["_w"].sum()
        if not np.allclose(sums.values, 1.0, atol=1e-9):
            raise RuntimeError(f"[{label}] Pooled country weight sums != 1.0: {sums.to_dict()}. Aborting.")


# ============================================================================
# REGRESSION-ESTIMATION CODE (generic fit + term-row extraction, reused by
# every robustness family below - only the sample/RHS/weight differ)
# ============================================================================

def run_wls_generic(label, sample_df, outcome, continuous_vars, categorical_vars_with_ref, include_fe,
                     weight_series, cluster_series, weight_method, clustering_method,
                     robustness_family, model_label, country_scope, extra_cols=None):
    """
    Fits ONE weighted OLS/LPM model via statsmodels.WLS with cluster-robust
    SE, reusing Step 11's build_design_matrix()/rank_check() so the
    model-matrix and inference machinery is never duplicated.
    """
    X, ref_metadata = reg.build_design_matrix(sample_df, continuous_vars, categorical_vars_with_ref, include_fe=include_fe)
    y = sample_df[outcome].astype(float)
    w = weight_series.astype(float)

    reg.rank_check(X, label=label)

    model = sm.WLS(y, X, weights=w)
    res = model.fit(cov_type="cluster", cov_kwds={"groups": cluster_series})

    if not np.all(np.isfinite(res.params.values)) or not np.all(np.isfinite(res.bse.values)):
        raise RuntimeError(f"[{label}] Non-finite coefficient or SE. Aborting.")

    ci = res.conf_int()
    rows = []
    for term in res.params.index:
        row = {
            "robustness_family": robustness_family,
            "model_label": model_label,
            "outcome": outcome,
            "country_scope": country_scope,
            "term": term,
            "coefficient": res.params[term],
            "standard_error": res.bse[term],
            "ci_lower": ci.loc[term, 0],
            "ci_upper": ci.loc[term, 1],
            "p_value": res.pvalues[term],
            "estimation_n": int(res.nobs),
            "psu_count": int(cluster_series.nunique()),
            "fe_region_count": int(sample_df[FE_VAR].nunique()) if include_fe else 0,
            "weight_method": weight_method,
            "clustering_method": clustering_method,
            "fe_included": include_fe,
            "reference_category_metadata": str(ref_metadata),
        }
        if extra_cols:
            row.update(extra_cols)
        rows.append(row)
    return pd.DataFrame(rows)


def scoped_sample(df, base_mask, country_scope):
    if country_scope == "pooled":
        return df[base_mask].copy()
    return df[base_mask & (df["country"] == country_scope)].copy()


def pooled_weight_and_cluster(sample_df):
    weight, _ = reg.build_temporary_pooled_weight(sample_df)
    return weight, sample_df["country_psu"], "model_specific_equal_total_country_weight", "cluster_robust_country_psu"


def country_weight_and_cluster(sample_df):
    return sample_df["weight_original"], sample_df["psu"], "weight_original", "cluster_robust_psu"


# ============================================================================
# FAMILY 1: BINARY LPM ROBUSTNESS
# ============================================================================

def run_binary_lpm_family(df):
    print(f"\n{'='*90}\nFAMILY 1: BINARY LPM ROBUSTNESS (stunted/wasted/underweight, preferred Model 4)\n{'='*90}")
    results, flow_rows = [], []
    for outcome in BINARY_OUTCOMES:
        base_mask = reg.build_estimation_sample(df, outcome)
        for scope in ["pooled"] + COUNTRIES:
            sample = scoped_sample(df, base_mask, scope)
            if scope == "pooled":
                weight, cluster, wmethod, cmethod = pooled_weight_and_cluster(sample)
            else:
                weight, cluster, wmethod, cmethod = country_weight_and_cluster(sample)

            label = f"binary_lpm-{outcome}-{scope}"
            validate_before_fit(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL,
                fe_required=True, weight_series=weight, cluster_series=cluster,
                weight_must_sum_to_one_per_country=(scope == "pooled"), binary_outcome=True,
            )
            res_df = run_wls_generic(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL, True,
                weight, cluster, wmethod, cmethod, "binary_lpm", "model4_preferred_lpm", scope,
            )
            results.append(res_df)
            flow_rows.append({
                "robustness_family": "binary_lpm", "outcome": outcome, "country_scope": scope,
                "final_estimation_n": len(sample), "psu_count": int(cluster.nunique()),
                "fe_region_count": int(sample[FE_VAR].nunique()), "outcome_prevalence": float(sample[outcome].mean()),
                "weight_method": wmethod, "clustering_method": cmethod,
            })
            print(f"  {outcome:12s} {scope:10s} N={len(sample):6d} PSUs={cluster.nunique():5d} "
                  f"prevalence={sample[outcome].mean():.4f}  OK")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# FAMILY 2: SEVERE OUTCOMES (pooled only, secondary/appendix)
# ============================================================================

def run_severe_outcomes_family(df):
    print(f"\n{'='*90}\nFAMILY 2: SEVERE OUTCOMES - POOLED ONLY (secondary/appendix)\n{'='*90}")
    results, flow_rows = [], []
    for outcome in SEVERE_OUTCOMES:
        base_mask = reg.build_estimation_sample(df, outcome)
        sample = scoped_sample(df, base_mask, "pooled")
        weight, cluster, wmethod, cmethod = pooled_weight_and_cluster(sample)

        # Sparsity diagnostics computed BEFORE fitting, and attached to every
        # output row so a reader sees the sparsity alongside the coefficient
        # rather than having to cross-reference a separate audit.
        region_events = sample.groupby(FE_VAR)[outcome].sum()
        n_zero_event_regions = int((region_events == 0).sum())
        event_count = int(sample[outcome].sum())
        event_prevalence = float(sample[outcome].mean())

        label = f"severe-{outcome}-pooled"
        validate_before_fit(
            label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL,
            fe_required=True, weight_series=weight, cluster_series=cluster,
            weight_must_sum_to_one_per_country=True, binary_outcome=True,
        )
        res_df = run_wls_generic(
            label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL, True,
            weight, cluster, wmethod, cmethod, "severe_outcomes_secondary", "model4_preferred_lpm", "pooled",
            extra_cols={
                "event_count": event_count, "event_prevalence": event_prevalence,
                "n_zero_event_regions": n_zero_event_regions, "n_total_regions": int(sample[FE_VAR].nunique()),
                "is_secondary_appendix_result": True,
            },
        )
        results.append(res_df)
        flow_rows.append({
            "robustness_family": "severe_outcomes_secondary", "outcome": outcome, "country_scope": "pooled",
            "final_estimation_n": len(sample), "psu_count": int(cluster.nunique()),
            "fe_region_count": int(sample[FE_VAR].nunique()), "outcome_prevalence": event_prevalence,
            "weight_method": wmethod, "clustering_method": cmethod,
        })
        print(f"  {outcome:20s} N={len(sample):6d} events={event_count:5d} prevalence={event_prevalence:.4%} "
              f"zero_event_regions={n_zero_event_regions}/{sample[FE_VAR].nunique()}  OK "
              f"(secondary/appendix - not a headline result)")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# FAMILY 3: GHANA BIO-DIGESTER SANITATION ROBUSTNESS
# ============================================================================

def run_ghana_biodigester_family(df):
    print(f"\n{'='*90}\nFAMILY 3: GHANA BIO-DIGESTER SANITATION ROBUSTNESS\n{'='*90}")
    assert_ghana_biodigester_isolated(df)
    print("  Hard-fail re-assertion passed: robustness sanitation rate == core sanitation rate for every non-Ghana row.")

    results, flow_rows = [], []
    for outcome in PRIMARY_OUTCOMES:
        base_mask = reg.build_estimation_sample(df, outcome)
        for scope in ["pooled", "ghana"]:
            sample = scoped_sample(df, base_mask, scope)
            if scope == "pooled":
                weight, cluster, wmethod, cmethod = pooled_weight_and_cluster(sample)
            else:
                weight, cluster, wmethod, cmethod = country_weight_and_cluster(sample)

            label = f"biodigester-{outcome}-{scope}"
            validate_before_fit(
                label, sample, outcome, GHANA_BIODIGESTER_CONTINUOUS, MODEL4_CATEGORICAL,
                fe_required=True, weight_series=weight, cluster_series=cluster,
                weight_must_sum_to_one_per_country=(scope == "pooled"),
            )
            res_df = run_wls_generic(
                label, sample, outcome, GHANA_BIODIGESTER_CONTINUOUS, MODEL4_CATEGORICAL, True,
                weight, cluster, wmethod, cmethod, "ghana_biodigester", "model4_biodigester_swap", scope,
            )
            results.append(res_df)
            flow_rows.append({
                "robustness_family": "ghana_biodigester", "outcome": outcome, "country_scope": scope,
                "final_estimation_n": len(sample), "psu_count": int(cluster.nunique()),
                "fe_region_count": int(sample[FE_VAR].nunique()), "outcome_prevalence": None,
                "weight_method": wmethod, "clustering_method": cmethod,
            })
            print(f"  {outcome:5s} {scope:8s} N={len(sample):6d} PSUs={cluster.nunique():5d}  OK")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# FAMILY 4: HOUSEHOLD-LEVEL WASH BASELINE (thesis_design.md Section 9.1, no FE)
# ============================================================================

def run_household_baseline_family(df):
    print(f"\n{'='*90}\nFAMILY 4: HOUSEHOLD-LEVEL WASH BASELINE (Section 9.1 literal - NO FE)\n{'='*90}")
    water_bin, sanitation_bin = build_household_wash_indicators(df)
    df = df.copy()
    df["_water_hh_binary"] = water_bin
    df["_sanitation_hh_binary"] = sanitation_bin
    continuous_vars = ["_water_hh_binary", "_sanitation_hh_binary"] + HOUSEHOLD_BASELINE_CONTROLS_CONTINUOUS

    results, flow_rows = [], []
    for outcome in PRIMARY_OUTCOMES:
        preferred_mask = reg.build_estimation_sample(df, outcome)
        n_preferred = int(preferred_mask.sum())

        baseline_mask = preferred_mask & df["_water_hh_binary"].notna() & df["_sanitation_hh_binary"].notna()
        sample = df[baseline_mask].copy()
        n_baseline = len(sample)

        weight, cluster, wmethod, cmethod = pooled_weight_and_cluster(sample)

        label = f"household_baseline-{outcome}-pooled"
        validate_before_fit(
            label, sample, outcome, continuous_vars, MODEL4_CATEGORICAL,
            fe_required=False, weight_series=weight, cluster_series=cluster,
            weight_must_sum_to_one_per_country=True,
        )
        res_df = run_wls_generic(
            label, sample, outcome, continuous_vars, MODEL4_CATEGORICAL, False,
            weight, cluster, wmethod, cmethod, "household_wash_baseline",
            "section_9_1_transparent_baseline_no_fe", "pooled",
            extra_cols={
                "preferred_model_n": n_preferred, "baseline_n": n_baseline,
                "n_excluded_by_household_wash_states": n_preferred - n_baseline,
            },
        )
        results.append(res_df)
        flow_rows.append({
            "robustness_family": "household_wash_baseline", "outcome": outcome, "country_scope": "pooled",
            "final_estimation_n": n_baseline, "psu_count": int(cluster.nunique()),
            "fe_region_count": 0, "outcome_prevalence": None,
            "weight_method": wmethod, "clustering_method": cmethod,
        })
        print(f"  {outcome:5s} preferred_N={n_preferred:6d}  baseline_N={n_baseline:6d}  "
              f"excluded={n_preferred - n_baseline:5d} ({100*(n_preferred-n_baseline)/n_preferred:.2f}%)  "
              f"PSUs={cluster.nunique():5d}  no FE  OK")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# FAMILY 5: ALTERNATIVE POOLED WEIGHTING
# ============================================================================

def run_alternative_weights_family(df):
    print(f"\n{'='*90}\nFAMILY 5: ALTERNATIVE POOLED WEIGHTING (haz/waz/whz, preferred Model 4)\n{'='*90}")
    results, flow_rows = [], []
    for outcome in PRIMARY_OUTCOMES:
        base_mask = reg.build_estimation_sample(df, outcome)
        sample = scoped_sample(df, base_mask, "pooled")
        cluster = sample["country_psu"]

        weight_specs = {
            "A_equal_total_country": (reg.build_temporary_pooled_weight(sample)[0], True),
            "B_raw_weight_original": (sample["weight_original"], False),
            "C_unweighted": (pd.Series(1.0, index=sample.index), False),
        }
        for weight_label, (weight, must_sum_to_one) in weight_specs.items():
            label = f"alt_weight-{outcome}-{weight_label}"
            validate_before_fit(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL,
                fe_required=True, weight_series=weight, cluster_series=cluster,
                weight_must_sum_to_one_per_country=must_sum_to_one,
            )
            res_df = run_wls_generic(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL, True,
                weight, cluster, weight_label, "cluster_robust_country_psu",
                "alternative_pooled_weighting", f"model4_weight_{weight_label}", "pooled",
            )
            results.append(res_df)
            flow_rows.append({
                "robustness_family": "alternative_pooled_weighting", "outcome": outcome,
                "country_scope": f"pooled_{weight_label}", "final_estimation_n": len(sample),
                "psu_count": int(cluster.nunique()), "fe_region_count": int(sample[FE_VAR].nunique()),
                "outcome_prevalence": None, "weight_method": weight_label,
                "clustering_method": "cluster_robust_country_psu",
            })
            print(f"  {outcome:5s} {weight_label:24s} N={len(sample):6d}  OK")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# FAMILY 6: LOO DENOMINATOR SENSITIVITY
# ============================================================================

def run_loo_denominator_family(df):
    print(f"\n{'='*90}\nFAMILY 6: LOO DENOMINATOR SENSITIVITY (haz/waz/whz, preferred Model 4, pooled only)\n{'='*90}")
    results, flow_rows = [], []
    for outcome in PRIMARY_OUTCOMES:
        base_mask = reg.build_estimation_sample(df, outcome)
        unrestricted = scoped_sample(df, base_mask, "pooled")
        n_unrestricted = len(unrestricted)

        for threshold_label, threshold in LOO_DENOMINATOR_THRESHOLDS.items():
            if threshold is None:
                sample = unrestricted
            else:
                keep = (
                    (unrestricted["water_rate_loo_n_other_hh"] >= threshold)
                    & (unrestricted["sanitation_rate_loo_core_n_other_hh"] >= threshold)
                )
                sample = unrestricted[keep].copy()

            weight, _ = reg.build_temporary_pooled_weight(sample)
            cluster = sample["country_psu"]

            label = f"loo_denom-{outcome}-{threshold_label}"
            validate_before_fit(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL,
                fe_required=True, weight_series=weight, cluster_series=cluster,
                weight_must_sum_to_one_per_country=True,
            )
            res_df = run_wls_generic(
                label, sample, outcome, MODEL4_CONTINUOUS, MODEL4_CATEGORICAL, True,
                weight, cluster, "model_specific_equal_total_country_weight", "cluster_robust_country_psu",
                "loo_denominator_sensitivity", f"model4_{threshold_label}", "pooled",
                extra_cols={
                    "unrestricted_n": n_unrestricted, "retained_n": len(sample),
                    "pct_retained": round(100 * len(sample) / n_unrestricted, 4),
                    "min_other_hh_threshold": threshold if threshold else 0,
                },
            )
            results.append(res_df)
            flow_rows.append({
                "robustness_family": "loo_denominator_sensitivity", "outcome": outcome,
                "country_scope": f"pooled_{threshold_label}", "final_estimation_n": len(sample),
                "psu_count": int(cluster.nunique()), "fe_region_count": int(sample[FE_VAR].nunique()),
                "outcome_prevalence": None, "weight_method": "model_specific_equal_total_country_weight",
                "clustering_method": "cluster_robust_country_psu",
            })
            print(f"  {outcome:5s} {threshold_label:14s} N={len(sample):6d} "
                  f"({100*len(sample)/n_unrestricted:.2f}% of unrestricted)  OK")
    return pd.concat(results, ignore_index=True), pd.DataFrame(flow_rows)


# ============================================================================
# RESULT-EXPORT CODE
# ============================================================================

def export_results(results_df, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(path, index=False)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*90)
    print("STEP 12 ROBUSTNESS EXECUTION - binary LPM, severe (pooled), Ghana bio-digester,")
    print("household-level baseline, alternative pooled weighting, LOO denominator sensitivity")
    print("="*90)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 10 input not found: {INPUT_PATH}")
    for p in STEP11_OUTPUTS_TO_PRESERVE:
        if not p.exists():
            raise FileNotFoundError(f"Expected Step 11 output not found: {p}")

    checksum_input_before = md5_of_file(INPUT_PATH)
    checksums_step11_before = {p: md5_of_file(p) for p in STEP11_OUTPUTS_TO_PRESERVE}

    df = pd.read_parquet(INPUT_PATH)
    print(f"\nLoaded: {len(df)} rows, {df.shape[1]} columns")
    if df.shape != (EXPECTED_TOTAL_ROWS, EXPECTED_STEP10_COLS):
        raise RuntimeError(f"Unexpected input shape {df.shape}. Aborting.")
    for country, n in EXPECTED_ROW_COUNTS.items():
        if (df["country"] == country).sum() != n:
            raise RuntimeError(f"[{country}] row count mismatch. Aborting.")
    print("Input shape and per-country row counts confirmed.")

    # ---- Pre-flight hard-fail re-assertions (not merely cited from the audit) ----
    assert_binary_matches_zscore_denominator(df)
    print("Binary-outcome-vs-paired-zscore denominator check: passed "
          "(stunted<->haz, wasted<->whz, underweight<->waz all match exactly).")

    all_results = {}
    all_flow = []

    binary_results, binary_flow = run_binary_lpm_family(df)
    all_results["binary_lpm"] = binary_results
    all_flow.append(binary_flow)

    severe_results, severe_flow = run_severe_outcomes_family(df)
    all_results["severe"] = severe_results
    all_flow.append(severe_flow)

    biodigester_results, biodigester_flow = run_ghana_biodigester_family(df)
    all_results["biodigester"] = biodigester_results
    all_flow.append(biodigester_flow)

    household_results, household_flow = run_household_baseline_family(df)
    all_results["household"] = household_results
    all_flow.append(household_flow)

    altweight_results, altweight_flow = run_alternative_weights_family(df)
    all_results["altweight"] = altweight_results
    all_flow.append(altweight_flow)

    loo_results, loo_flow = run_loo_denominator_family(df)
    all_results["loo"] = loo_results
    all_flow.append(loo_flow)

    # ---- Aggregate finite-value check across every family before writing ----
    print(f"\n{'='*90}\nFINAL VALIDATION\n{'='*90}")
    total_fits = 0
    for name, res in all_results.items():
        if not np.all(np.isfinite(res["coefficient"].values)):
            raise RuntimeError(f"[{name}] Non-finite coefficient in results. Aborting before write.")
        if not np.all(np.isfinite(res["standard_error"].values)):
            raise RuntimeError(f"[{name}] Non-finite standard_error in results. Aborting before write.")
        n_fits = res.drop_duplicates(subset=["outcome", "model_label", "country_scope"]).shape[0]
        total_fits += n_fits
        print(f"  {name:12s}: {n_fits:3d} fits, {len(res):5d} term-rows, finite-value check PASSED")
    print(f"\nTotal robustness regression fits completed: {total_fits}")

    # ---- WRITE OUTPUTS ----
    export_results(all_results["binary_lpm"], BINARY_LPM_OUTPUT)
    export_results(all_results["severe"], SEVERE_OUTPUT)
    export_results(all_results["biodigester"], BIODIGESTER_OUTPUT)
    export_results(all_results["household"], HOUSEHOLD_WASH_OUTPUT)
    export_results(all_results["altweight"], ALT_WEIGHTS_OUTPUT)
    export_results(all_results["loo"], LOO_DENOMINATOR_OUTPUT)
    sample_flow_df = pd.concat(all_flow, ignore_index=True)
    export_results(sample_flow_df, SAMPLE_FLOW_OUTPUT)

    for name, path in [
        ("binary_lpm", BINARY_LPM_OUTPUT), ("severe", SEVERE_OUTPUT), ("biodigester", BIODIGESTER_OUTPUT),
        ("household", HOUSEHOLD_WASH_OUTPUT), ("altweight", ALT_WEIGHTS_OUTPUT), ("loo", LOO_DENOMINATOR_OUTPUT),
        ("sample_flow", SAMPLE_FLOW_OUTPUT),
    ]:
        shape = all_results[name].shape if name in all_results else sample_flow_df.shape
        print(f"Written: {path}  ({shape[0]} rows, {shape[1]} columns)")

    # ---- Source / upstream integrity re-verification ----
    checksum_input_after = md5_of_file(INPUT_PATH)
    if checksum_input_after != checksum_input_before:
        raise RuntimeError("Step 10 input file changed during Step 12 execution!")
    for p in STEP11_OUTPUTS_TO_PRESERVE:
        if md5_of_file(p) != checksums_step11_before[p]:
            raise RuntimeError(f"Step 11 output changed during Step 12 execution: {p}")
    print(f"\n{'='*90}")
    print(f"Source integrity check: Step 10 input unchanged (checksum {checksum_input_before})")
    print("Step 11 outputs (main_continuous_models.csv, step11_model_sample_flow.csv) unchanged (checksum match)")
    print("="*90)

    return all_results, sample_flow_df


if __name__ == "__main__":
    main()
