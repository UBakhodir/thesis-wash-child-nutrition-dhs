"""
07_descriptives.py
====================
Country-specific descriptive statistics (Ethiopia, Ghana, Kenya, Nigeria)
built from the Step 06 geolinked dataset. No pooled/four-country combined
statistic is computed anywhere in this script, and no
weight_pooled_rescaled column is created.

Survey design: svy.Design(stratum="strata", psu="psu", wgt="weight_original"),
built per country (and per outcome-specific subset for Table 2/2b) from a
Polars conversion of the relevant pandas subset - svy.Sample requires a
Polars DataFrame; pandas DataFrames are not accepted directly (confirmed
during API verification).

Reads ONLY data/processed/pooled_kr_four_country_geolinked.parquet.
Never writes to that file or to any Step 00-06 script/output.
No figures, maps, regressions, weight changes, or WASH/anthropometric
recoding are performed.
"""

import hashlib
import importlib.util
import math
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import polars as pl
from svy import Design, Sample

SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

INPUT_PATH = config.POOLED_GEOLINKED_OUTPUT
OUTPUT_DIR = config.PROJECT_ROOT / "outputs" / "tables"

TABLE1_PATH = OUTPUT_DIR / "table1_sample_characteristics.csv"
TABLE2_PATH = OUTPUT_DIR / "table2_anthropometric_outcomes.csv"
TABLE2B_PATH = OUTPUT_DIR / "table2b_severe_anthropometric_outcomes_secondary.csv"
TABLE3_PATH = OUTPUT_DIR / "table3_wash_characteristics.csv"
TABLE4_PATH = OUTPUT_DIR / "table4_missingness_summary.csv"

APPROVED_COUNTRIES = ["ethiopia", "ghana", "kenya", "nigeria"]

# Audit guard: exact row counts confirmed at Step 05/06 execution. If the
# Step 06 parquet ever changes, this catches it immediately.
EXPECTED_ROW_COUNTS = {
    "ethiopia": 13565, "ghana": 9353, "kenya": 19530, "nigeria": 27783,
}

# Audit guard: Nigeria underweight denominator/outcome counts, locked per
# the approved specification.
NIGERIA_UNDERWEIGHT_LOCK = {
    "valid": 9513, "missing": 18270, "underweight": 2398, "not_underweight": 7115,
}

CORE_OUTCOMES = [("stunted", "haz", "Stunting"),
                  ("wasted", "whz", "Wasting"),
                  ("underweight", "waz", "Underweight")]
SEVERE_OUTCOMES = [("severe_stunted", "haz", "Severe stunting"),
                     ("severe_wasted", "whz", "Severe wasting"),
                     ("severe_underweight", "waz", "Severe underweight")]

CONTROL_VARS = ["child_sex", "maternal_education", "literacy", "wealth_quintile", "residence"]
CONTROL_LABELS = {
    "child_sex": "Child sex", "maternal_education": "Maternal education",
    "literacy": "Literacy", "wealth_quintile": "Wealth quintile", "residence": "Residence",
}

WASH_STRUCTURAL_CATEGORIES = {"StructuralNotApplicable", "Unknown", "UnclassifiedBioDigester"}
WASH_CATEGORY_LABELS = {
    "Improved": "Improved", "Unimproved": "Unimproved", "SurfaceWater": "Surface water",
    "Basic": "Basic sanitation", "Limited": "Limited sanitation",
    "OpenDefecation": "Open defecation", "NonImproved": "Non-improved",
    "StructuralNotApplicable": "Structural / not applicable",
    "Unknown": "Unknown", "UnclassifiedBioDigester": "Unclassified bio-digester (Ghana)",
}

COUNTRY_LABELS = {"ethiopia": "Ethiopia", "ghana": "Ghana", "kenya": "Kenya", "nigeria": "Nigeria"}

WEIGHT_COL = "weight_original"
PSU_COL = "psu"
STRATA_COL = "strata"

PREVALENCE_TOLERANCE = 1e-6
PCT_SUM_TOLERANCE = 1e-6         # for "percentages sum to 100%" checks (percentage points)
WEIGHT_SUM_REL_TOLERANCE = 1e-9  # relative tolerance for weight-sum reconciliation checks


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================
# SURVEY-DESIGN HELPERS (svy, verified API)
# ============================================================
def check_no_singleton_psu(df_subset, context_label):
    """
    Manual pre-check (independent of svy's own singleton detection) so we
    can hard-fail with a clear message before ever calling svy.
    """
    psu_per_stratum = df_subset.groupby(STRATA_COL)[PSU_COL].nunique()
    singletons = psu_per_stratum[psu_per_stratum == 1]
    if len(singletons) > 0:
        raise RuntimeError(
            f"[{context_label}] {len(singletons)} stratum/strata contain only one PSU: "
            f"{sorted(singletons.index.tolist())}. Aborting rather than proceeding "
            "with an unexpected singleton-PSU design."
        )


def build_sample(df_subset):
    """Pandas -> Polars conversion (required; svy.Sample does not accept
    pandas directly) + svy.Design/Sample construction."""
    pl_df = pl.from_pandas(df_subset)
    design = Design(stratum=STRATA_COL, psu=PSU_COL, wgt=WEIGHT_COL)
    return Sample(pl_df, design=design)


def design_based_proportion(df_subset, y_col, context_label):
    """
    df_subset: pandas subset already restricted to the non-missing outcome
    rows for one country. y_col must be a float64 0/1 column.
    Returns the dict for y_level == 1 (the "outcome=1" prevalence row).
    """
    check_no_singleton_psu(df_subset, context_label)
    sample = build_sample(df_subset)
    est = sample.estimation.prop(y=y_col, alpha=0.05, ci_method="logit")
    dicts = est.to_dicts()
    row1 = next(d for d in dicts if d["y_level"] == 1)
    return row1


def design_based_mean(df_subset, y_col, context_label):
    check_no_singleton_psu(df_subset, context_label)
    sample = build_sample(df_subset)
    est = sample.estimation.mean(y=y_col, alpha=0.05)
    dicts = est.to_dicts()
    return dicts[0]


# ============================================================
# LOAD + PRE-FLIGHT VALIDATION
# ============================================================
def load_and_validate():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 06 input not found: {INPUT_PATH}")

    checksum_before = md5_of_file(INPUT_PATH)
    df = pd.read_parquet(INPUT_PATH)
    print(f"Loaded Step 06 output: {INPUT_PATH.name} ({len(df)} rows, {df.shape[1]} columns)")

    # Country set matches exactly the four approved countries
    actual_countries = sorted(df["country"].unique().tolist())
    if actual_countries != sorted(APPROVED_COUNTRIES):
        raise RuntimeError(
            f"Country set {actual_countries} does not match approved set "
            f"{sorted(APPROVED_COUNTRIES)}. Aborting."
        )

    # Per-country row counts match the audit-guard constants
    for country, expected_n in EXPECTED_ROW_COUNTS.items():
        actual_n = int((df["country"] == country).sum())
        if actual_n != expected_n:
            raise RuntimeError(
                f"[{country}] Row count {actual_n} != expected {expected_n}. Aborting."
            )
    print("Row-count audit guard: all four countries match expected counts")

    # country_child_id unique/non-null
    if df["country_child_id"].duplicated().any():
        raise RuntimeError("Duplicate country_child_id in Step 06 input. Aborting.")
    if df["country_child_id"].isna().any():
        raise RuntimeError("Null country_child_id in Step 06 input. Aborting.")
    print("country_child_id: unique and non-null")

    # weight_original: no missing, no zero/negative, all finite
    w = df[WEIGHT_COL]
    if w.isna().any():
        raise RuntimeError("weight_original has missing value(s). Aborting.")
    if (w <= 0).any():
        raise RuntimeError("weight_original has zero/negative value(s). Aborting.")
    if not np.isfinite(w.to_numpy()).all():
        raise RuntimeError("weight_original has non-finite value(s). Aborting.")
    print("weight_original: no missing, all positive, all finite")

    # psu / strata: no missing
    if df[PSU_COL].isna().any() or df[STRATA_COL].isna().any():
        raise RuntimeError("psu or strata has missing value(s). Aborting.")
    print("psu / strata: no missing values")

    # Required variables present
    required_vars = (
        ["country", "survey_round", "country_child_id", PSU_COL, STRATA_COL, WEIGHT_COL,
         "haz", "waz", "whz"]
        + [o for o, _, _ in CORE_OUTCOMES] + [o for o, _, _ in SEVERE_OUTCOMES]
        + CONTROL_VARS + ["maternal_age"]
        + ["water_category", "sanitation_category_core",
           "sanitation_service_core", "sanitation_collapsed_core"]
    )
    missing_vars = [v for v in required_vars if v not in df.columns]
    if missing_vars:
        raise RuntimeError(f"Required variable(s) missing from Step 06 input: {missing_vars}")
    print("All required variables present")

    # Categorical control variables: validate zero missingness at runtime (not assumed)
    for col in CONTROL_VARS:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            raise RuntimeError(
                f"Control variable '{col}' has {n_missing} unexpected missing value(s). Aborting."
            )
    print("Control variables: confirmed zero missingness at runtime")

    # Outcome domain: non-missing values must be 0 or 1
    for col, _, _ in CORE_OUTCOMES + SEVERE_OUTCOMES:
        vals = df[col].dropna()
        if not vals.isin([0, 1]).all():
            raise RuntimeError(f"'{col}' contains a non-missing value other than 0/1. Aborting.")
    print("Outcome domain check: all core/severe outcomes are 0/1/missing only")

    # severe == 1 implies standard == 1
    pairs = [("severe_stunted", "stunted"), ("severe_wasted", "wasted"),
             ("severe_underweight", "underweight")]
    for severe_col, std_col in pairs:
        violation = (df[severe_col] == 1) & (df[std_col] != 1)
        if violation.any():
            raise RuntimeError(
                f"{int(violation.sum())} row(s) have {severe_col}=1 but {std_col}!=1. Aborting."
            )
    print("Severe-implies-standard check: passed")

    # Outcome missingness matches underlying z-score missingness
    zmap = {"stunted": "haz", "wasted": "whz", "underweight": "waz",
            "severe_stunted": "haz", "severe_wasted": "whz", "severe_underweight": "waz"}
    for ind_col, z_col in zmap.items():
        mismatch = df[z_col].isna() != df[ind_col].isna()
        if mismatch.any():
            raise RuntimeError(
                f"'{ind_col}' missingness does not match '{z_col}' missingness "
                f"({int(mismatch.sum())} mismatched row(s)). Aborting."
            )
    print("Outcome-missingness-matches-zscore check: passed")

    # Nigeria underweight audit guard
    nga = df[df["country"] == "nigeria"]
    valid = nga["underweight"].notna().sum()
    missing = nga["underweight"].isna().sum()
    n1 = int((nga["underweight"] == 1).sum())
    n0 = int((nga["underweight"] == 0).sum())
    locked = NIGERIA_UNDERWEIGHT_LOCK
    if (valid, missing, n1, n0) != (locked["valid"], locked["missing"],
                                       locked["underweight"], locked["not_underweight"]):
        raise RuntimeError(
            f"Nigeria underweight audit guard FAILED: got "
            f"(valid={valid}, missing={missing}, =1:{n1}, =0:{n0}), "
            f"expected {locked}. Aborting."
        )
    print("Nigeria underweight audit guard: locked values confirmed exactly")

    return df, checksum_before


# ============================================================
# TABLE 1 - SAMPLE CHARACTERISTICS
# ============================================================
def build_table1(df):
    rows = []
    for country in APPROVED_COUNTRIES:
        sub = df[df["country"] == country]

        for col in CONTROL_VARS:
            # Explicit variable-specific non-missing subset and denominator -
            # NOT a country-wide total, and not relying on the separately
            # -asserted zero-missingness property.
            var_valid = sub[sub[col].notna()]
            n_non_missing = len(var_valid)
            denominator_weight = var_valid[WEIGHT_COL].sum()

            sum_n = 0
            sum_pct = 0.0
            for category, grp in var_valid.groupby(col, dropna=False):
                n = len(grp)
                weighted_pct = 100 * grp[WEIGHT_COL].sum() / denominator_weight
                sum_n += n
                sum_pct += weighted_pct
                rows.append({
                    "Country": COUNTRY_LABELS[country],
                    "Variable": CONTROL_LABELS[col],
                    "Category": category,
                    "Unweighted N": n,
                    "Weighted %": weighted_pct,
                    "Weighted Mean": None,
                    "Weighted SD": None,
                })

            # Reconciliation assertions
            if sum_n != n_non_missing:
                raise RuntimeError(
                    f"[{country}] '{col}': category unweighted counts sum to {sum_n}, "
                    f"expected variable non-missing N {n_non_missing}. Aborting."
                )
            if abs(sum_pct - 100.0) > PCT_SUM_TOLERANCE:
                raise RuntimeError(
                    f"[{country}] '{col}': weighted percentages sum to {sum_pct}, "
                    "not 100% within tolerance. Aborting."
                )

        # Maternal age: svy design-based mean, cross-checked against direct calc,
        # plus separately-computed descriptive weighted SD
        n_valid_age = int(sub["maternal_age"].notna().sum())
        age_valid = sub[sub["maternal_age"].notna()]
        direct_mean = np.average(age_valid["maternal_age"], weights=age_valid[WEIGHT_COL])

        svy_mean_result = design_based_mean(age_valid, "maternal_age", f"{country} maternal_age")
        svy_mean = svy_mean_result["est"]

        if abs(svy_mean - direct_mean) > PREVALENCE_TOLERANCE:
            raise RuntimeError(
                f"[{country}] svy weighted mean ({svy_mean}) does not match direct "
                f"weighted mean ({direct_mean}) within tolerance. Aborting."
            )

        w_var = np.average((age_valid["maternal_age"] - direct_mean) ** 2, weights=age_valid[WEIGHT_COL])
        descriptive_sd = math.sqrt(w_var)

        rows.append({
            "Country": COUNTRY_LABELS[country],
            "Variable": "Maternal age",
            "Category": None,
            "Unweighted N": n_valid_age,
            "Weighted %": None,
            "Weighted Mean": svy_mean,
            "Weighted SD": descriptive_sd,
        })

    return pd.DataFrame(rows)


# ============================================================
# TABLE 2 / 2B - ANTHROPOMETRIC OUTCOMES
# ============================================================
def build_anthro_table(df, outcome_specs, secondary):
    rows = []
    for country in APPROVED_COUNTRIES:
        full = df[df["country"] == country]
        total_n = len(full)

        for outcome_col, zscore_col, label in outcome_specs:
            valid = full[full[outcome_col].notna()].copy()
            n_valid = len(valid)
            n_missing = total_n - n_valid
            n1 = int((valid[outcome_col] == 1).sum())
            n0 = int((valid[outcome_col] == 0).sum())

            valid["_y"] = valid[outcome_col].astype("float64")
            direct_prev = (valid[WEIGHT_COL] * valid["_y"]).sum() / valid[WEIGHT_COL].sum()

            result = design_based_proportion(valid, "_y", f"{country} {outcome_col}")
            svy_prev = result["est"]

            if abs(svy_prev - direct_prev) > PREVALENCE_TOLERANCE:
                raise RuntimeError(
                    f"[{country}] {outcome_col}: svy point estimate ({svy_prev}) does not "
                    f"match direct weighted prevalence ({direct_prev}) within tolerance. "
                    "Aborting rather than writing results."
                )

            rows.append({
                "Country": COUNTRY_LABELS[country],
                "Outcome": label,
                "Outcome Type": "Secondary / robustness" if secondary else "Core",
                "Total KR N": total_n,
                "Valid Unweighted N": n_valid,
                "Missing Unweighted N": n_missing,
                "Outcome=1 Unweighted n": n1,
                "Outcome=0 Unweighted n": n0,
                "Weighted Prevalence (%)": 100 * svy_prev,
                "SE (%)": 100 * result["se"],
                "95% CI Lower (%)": 100 * result["lci"],
                "95% CI Upper (%)": 100 * result["uci"],
                "Design df": result.get("df"),
            })

    return pd.DataFrame(rows)


# ============================================================
# TABLE 3 - WASH CHARACTERISTICS
# ============================================================
def build_table3(df):
    rows = []
    domains = [
        ("water_category", "Drinking water source"),
        ("sanitation_service_core", "Sanitation service level"),
        ("sanitation_collapsed_core", "Sanitation (collapsed)"),
    ]

    for country in APPROVED_COUNTRIES:
        sub = df[df["country"] == country]
        country_n = len(sub)
        country_total_w = sub[WEIGHT_COL].sum()

        for col, domain_label in domains:
            # ---- RAW baseline captured BEFORE any presentation-label mapping ----
            raw_counts = sub[col].value_counts(dropna=False)
            raw_categories = set(raw_counts.index)

            block_rows = []
            sum_n = 0
            sum_w = 0.0
            sum_pct = 0.0
            seen_categories = set()

            for category, grp in sub.groupby(col, dropna=False):
                n = len(grp)
                w_sum = grp[WEIGHT_COL].sum()
                weighted_pct = 100 * w_sum / country_total_w

                sum_n += n
                sum_w += w_sum
                sum_pct += weighted_pct
                seen_categories.add(category)

                block_rows.append({
                    "Country": COUNTRY_LABELS[country],
                    "WASH Domain": domain_label,
                    "Category": WASH_CATEGORY_LABELS.get(category, str(category)),
                    "Unweighted N": n,
                    "Weighted %": weighted_pct,
                })

            # ---- Reconciliation assertions, using RAW categories/counts only ----
            if seen_categories != raw_categories:
                missing = raw_categories - seen_categories
                extra = seen_categories - raw_categories
                raise RuntimeError(
                    f"[{country}] '{col}': raw category mismatch. "
                    f"Missing from table: {missing}  Unexpected extra: {extra}. Aborting."
                )
            if sum_n != country_n:
                raise RuntimeError(
                    f"[{country}] '{col}': category unweighted counts sum to {sum_n}, "
                    f"expected country row count {country_n}. Aborting."
                )
            if not math.isclose(sum_w, country_total_w, rel_tol=WEIGHT_SUM_REL_TOLERANCE):
                raise RuntimeError(
                    f"[{country}] '{col}': summed category weights ({sum_w}) do not match "
                    f"country total weight ({country_total_w}) within tolerance. Aborting."
                )
            if abs(sum_pct - 100.0) > PCT_SUM_TOLERANCE:
                raise RuntimeError(
                    f"[{country}] '{col}': weighted percentages sum to {sum_pct}, "
                    "not 100% within tolerance. Aborting."
                )

            # ---- Explicit-state presence: if it occurs in raw data, it must
            # remain its own visible row - never merged/converted to missing ----
            for explicit_state in WASH_STRUCTURAL_CATEGORIES:
                if explicit_state in raw_categories and explicit_state not in seen_categories:
                    raise RuntimeError(
                        f"[{country}] '{col}': explicit state '{explicit_state}' present in "
                        "Step 06 raw data but missing from Table 3. Aborting."
                    )

            rows.extend(block_rows)

    return pd.DataFrame(rows)


# ============================================================
# TABLE 4 - MISSINGNESS / ANALYTICAL AVAILABILITY
# ============================================================
def build_table4(df):
    rows = []

    for country in APPROVED_COUNTRIES:
        sub = df[df["country"] == country]
        total_n = len(sub)

        for outcome_col, _, label in CORE_OUTCOMES + SEVERE_OUTCOMES:
            n_valid = int(sub[outcome_col].notna().sum())
            n_missing = total_n - n_valid
            for status, n in [("Valid", n_valid), ("Ordinary / system missing", n_missing)]:
                rows.append({
                    "Country": COUNTRY_LABELS[country],
                    "Variable": label,
                    "Status": status,
                    "Unweighted n": n,
                    "Unweighted %": 100 * n / total_n,
                })

        for col, domain_label in [("water_category", "Drinking water source"),
                                    ("sanitation_service_core", "Sanitation service level")]:
            n_sysmiss = int(sub[col].isna().sum())
            classified_mask = ~sub[col].isin(WASH_STRUCTURAL_CATEGORIES) & sub[col].notna()
            n_classified = int(classified_mask.sum())
            status_counts = {"Classified / substantive response": n_classified}
            for special_cat in WASH_STRUCTURAL_CATEGORIES:
                status_counts[WASH_CATEGORY_LABELS.get(special_cat, special_cat)] = int(
                    (sub[col] == special_cat).sum()
                )
            status_counts["Ordinary / system missing"] = n_sysmiss

            for status, n in status_counts.items():
                rows.append({
                    "Country": COUNTRY_LABELS[country],
                    "Variable": domain_label,
                    "Status": status,
                    "Unweighted n": n,
                    "Unweighted %": 100 * n / total_n,
                })

    return pd.DataFrame(rows)


# ============================================================
# ROUNDING FOR CSV PRESENTATION (applied only at write time)
# ============================================================
def round_for_output(df, pct_cols=(), mean_sd_cols=(), ci_cols=()):
    df = df.copy()
    for c in pct_cols:
        if c in df.columns:
            df[c] = df[c].astype("float64").round(1)
    for c in mean_sd_cols:
        if c in df.columns:
            df[c] = df[c].astype("float64").round(2)
    for c in ci_cols:
        if c in df.columns:
            df[c] = df[c].astype("float64").round(1)
    return df


def main():
    df, checksum_before = load_and_validate()

    print("\nBuilding Table 1 (sample characteristics)...")
    table1 = build_table1(df)

    print("Building Table 2 (core anthropometric outcomes)...")
    table2 = build_anthro_table(df, CORE_OUTCOMES, secondary=False)

    print("Building Table 2b (severe anthropometric outcomes, secondary)...")
    table2b = build_anthro_table(df, SEVERE_OUTCOMES, secondary=True)

    print("Building Table 3 (WASH characteristics)...")
    table3 = build_table3(df)

    print("Building Table 4 (missingness summary)...")
    table4 = build_table4(df)

    # ---- Final check: writing must not modify the Step 06 input ----
    checksum_before_write = md5_of_file(INPUT_PATH)
    if checksum_before_write != checksum_before:
        raise RuntimeError("Step 06 input changed between load and write. Aborting.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    round_for_output(table1, pct_cols=["Weighted %"], mean_sd_cols=["Weighted Mean", "Weighted SD"]) \
        .to_csv(TABLE1_PATH, index=False)
    round_for_output(table2, pct_cols=["Weighted Prevalence (%)", "SE (%)"],
                      ci_cols=["95% CI Lower (%)", "95% CI Upper (%)"]) \
        .to_csv(TABLE2_PATH, index=False)
    round_for_output(table2b, pct_cols=["Weighted Prevalence (%)", "SE (%)"],
                      ci_cols=["95% CI Lower (%)", "95% CI Upper (%)"]) \
        .to_csv(TABLE2B_PATH, index=False)
    round_for_output(table3, pct_cols=["Weighted %"]).to_csv(TABLE3_PATH, index=False)
    round_for_output(table4, pct_cols=["Unweighted %"]).to_csv(TABLE4_PATH, index=False)

    print(f"\nWritten: {TABLE1_PATH}")
    print(f"Written: {TABLE2_PATH}")
    print(f"Written: {TABLE2B_PATH}")
    print(f"Written: {TABLE3_PATH}")
    print(f"Written: {TABLE4_PATH}")

    # ---- Final re-verification: Step 06 input unchanged ----
    checksum_after = md5_of_file(INPUT_PATH)
    if checksum_after != checksum_before:
        raise RuntimeError("Step 06 input was modified during Step 07 execution!")
    print("\nStep 06 input integrity check: unchanged (checksum match) before/after execution")


if __name__ == "__main__":
    main()
