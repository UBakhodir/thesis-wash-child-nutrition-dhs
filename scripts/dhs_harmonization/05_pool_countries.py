"""
05_pool_countries.py
======================
Pools the four approved Step 04 country-level analytical KR datasets into
a single row-concatenated pooled dataset. Adds country-qualified identifier
columns (country_child_id, country_psu, country_strata) required because
raw child/PSU/strata identifiers collide numerically across countries
(confirmed empirically during Step 05 design review - e.g. Ethiopia and
Kenya share 796 numeric PSU codes; Kenya and Nigeria share 861 caseid
values). No joins, aggregation, recoding, imputation, standardization,
modeling, fixed effects, interactions, age-squared, geospatial operations,
or weight rescaling are performed anywhere in this script.

weight_original is carried through completely unchanged; pooled/rescaled
weights are explicitly deferred to a later regression-preparation step.

Reads ONLY the four data/processed/<country>_kr_clean.parquet files.
Never touches data/raw/, data/interim/, or any Step 00-04 script/output.
"""

import hashlib
import importlib.util
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

INPUT_PATHS = {c: info["processed_file"] for c, info in config.COUNTRIES.items()}
OUTPUT_PATH = config.POOLED_OUTPUT

WASH_CATEGORY_COLS = [
    "water_category", "sanitation_category_core",
    "sanitation_category_robustness_biodigester",
    "sanitation_service_core", "sanitation_service_robustness_biodigester",
    "sanitation_collapsed_core", "sanitation_collapsed_robustness_biodigester",
]

OUTCOME_WASH_COLS = [
    "haz", "waz", "whz", "stunted", "wasted", "underweight",
    "severe_stunted", "severe_wasted", "severe_underweight",
] + WASH_CATEGORY_COLS


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    """
    Row-concatenates the four countries' Step 04 outputs into one pooled
    dataset - no joins, aggregation, or recoding (see module docstring for
    why: this step exists purely to combine, not transform). Adds the
    country-qualified identifiers (country_child_id/country_psu/
    country_strata) needed because raw v001/v021/v023 values collide
    numerically across countries once pooled.
    """
    # ---- Checksum inputs BEFORE reading (defense in depth) ----
    for c, p in INPUT_PATHS.items():
        if not p.exists():
            raise FileNotFoundError(f"Missing Step 04 input for {c}: {p}")
    checksums_before = {c: md5_of_file(p) for c, p in INPUT_PATHS.items()}

    # ---- Load all four ----
    dfs = {}
    for country, path in INPUT_PATHS.items():
        df = pd.read_parquet(path)
        dfs[country] = df
        print(f"Loaded {country}: {path.name}  ({len(df)} rows, {df.shape[1]} columns)")

    # ---- SCHEMA VALIDATION: identical columns and dtypes, before concatenation ----
    reference_country = "ethiopia"
    reference_cols = list(dfs[reference_country].columns)
    reference_dtypes = dfs[reference_country].dtypes

    for country, df in dfs.items():
        if list(df.columns) != reference_cols:
            missing = set(reference_cols) - set(df.columns)
            extra = set(df.columns) - set(reference_cols)
            raise RuntimeError(
                f"[{country}] Column mismatch vs {reference_country}. "
                f"Missing: {missing}  Extra: {extra}. Aborting."
            )
        for col in reference_cols:
            if str(df[col].dtype) != str(reference_dtypes[col]):
                raise RuntimeError(
                    f"[{country}] dtype mismatch for '{col}': "
                    f"{df[col].dtype} vs {reference_country}'s {reference_dtypes[col]}. Aborting."
                )
    print("Schema validation: identical columns (name, order) and dtypes across all four inputs")

    n_expected_total = sum(len(df) for df in dfs.values())
    n_per_country_before = {c: len(df) for c, df in dfs.items()}

    # ---- Pre-concat snapshots for later identity checks ----
    missing_before = {c: df[reference_cols].isna().sum() for c, df in dfs.items()}
    weight_before = {c: df["weight_original"].copy() for c, df in dfs.items()}
    outcome_wash_before = {c: df[OUTCOME_WASH_COLS].copy() for c, df in dfs.items()}
    category_counts_before = {
        col: {c: df[col].value_counts(dropna=False) for c, df in dfs.items()}
        for col in WASH_CATEGORY_COLS
    }
    psu_nunique_before = {c: df["psu"].nunique() for c, df in dfs.items()}
    strata_nunique_before = {c: df["strata"].nunique() for c, df in dfs.items()}

    # ====================================================================
    # POOL: row concatenation only - no joins, aggregation, or recoding
    # ====================================================================
    pooled = pd.concat(list(dfs.values()), ignore_index=True)

    # ---- Add country-qualified identifiers (string concatenation only) ----
    pooled["country_child_id"] = (
        pooled["country"].astype(str) + "_" +
        pooled["v001"].astype(str) + "_" +
        pooled["v002"].astype(str) + "_" +
        pooled["v003"].astype(str) + "_" +
        pooled["bidx"].astype(str)
    )
    pooled["country_psu"] = pooled["country"].astype(str) + "_" + pooled["psu"].astype(str)
    pooled["country_strata"] = pooled["country"].astype(str) + "_" + pooled["strata"].astype(str)

    # ====================================================================
    # VALIDATION (all checks run BEFORE writing anything)
    # ====================================================================

    # 1. Row count vs dynamically computed sum of the four inputs
    if len(pooled) != n_expected_total:
        raise RuntimeError(
            f"Pooled row count ({len(pooled)}) != sum of input row counts "
            f"({n_expected_total}). Aborting."
        )
    print(f"Row count check: {len(pooled)} == sum of inputs ({n_expected_total})")

    # 2. Per-country row count preserved within pooled data
    for country, n_before in n_per_country_before.items():
        n_after = int((pooled["country"] == country).sum())
        if n_after != n_before:
            raise RuntimeError(f"[{country}] Row count changed after pooling: {n_before} -> {n_after}.")
    print("Per-country row count check: unchanged for all four")

    # 3. country_child_id uniqueness and non-null
    if pooled["country_child_id"].duplicated().any():
        n_dup = int(pooled["country_child_id"].duplicated().sum())
        raise RuntimeError(f"{n_dup} duplicate country_child_id value(s) found. Aborting.")
    if pooled["country_child_id"].isna().any():
        raise RuntimeError("country_child_id contains null value(s). Aborting.")
    print("country_child_id: unique and non-null for all rows")

    # 4. country / survey_round unchanged vs source
    for country, df in dfs.items():
        subset = pooled[pooled["country"] == country]
        expected_round = df["survey_round"].iloc[0]
        if not (subset["survey_round"] == expected_round).all():
            raise RuntimeError(f"[{country}] survey_round label corrupted after pooling.")
    print("country/survey_round labels: unchanged for all four")

    # 5. weight_original unchanged vs source (row-for-row, order preserved by concat)
    for country, df in dfs.items():
        subset_weight = pooled.loc[pooled["country"] == country, "weight_original"].reset_index(drop=True)
        source_weight = weight_before[country].reset_index(drop=True)
        if not np.allclose(subset_weight.to_numpy(), source_weight.to_numpy(), atol=1e-12, equal_nan=True):
            raise RuntimeError(f"[{country}] weight_original changed after pooling. Aborting.")
    print("weight_original: identical to source for all four countries")

    # 6. Outcome/WASH columns unchanged vs source
    for country, df in dfs.items():
        subset = pooled.loc[pooled["country"] == country, OUTCOME_WASH_COLS].reset_index(drop=True)
        source = outcome_wash_before[country].reset_index(drop=True)
        for col in OUTCOME_WASH_COLS:
            both_na = subset[col].isna() & source[col].isna()
            mismatch = (subset[col] != source[col]) & ~both_na
            if mismatch.any():
                raise RuntimeError(
                    f"[{country}] Column '{col}' changed after pooling "
                    f"({int(mismatch.sum())} mismatched row(s)). Aborting."
                )
    print("Outcome/WASH columns (incl. Ghana core+robustness): identical to source for all four countries")

    # 7. country_psu / country_strata uniquely country-qualified
    expected_psu_unique = sum(psu_nunique_before.values())
    actual_psu_unique = pooled["country_psu"].nunique()
    if actual_psu_unique != expected_psu_unique:
        raise RuntimeError(
            f"country_psu unique count ({actual_psu_unique}) != sum of per-country "
            f"counts ({expected_psu_unique}) - possible cross-country collision. Aborting."
        )
    expected_strata_unique = sum(strata_nunique_before.values())
    actual_strata_unique = pooled["country_strata"].nunique()
    if actual_strata_unique != expected_strata_unique:
        raise RuntimeError(
            f"country_strata unique count ({actual_strata_unique}) != sum of per-country "
            f"counts ({expected_strata_unique}) - possible cross-country collision. Aborting."
        )
    print(f"country_psu: {actual_psu_unique} unique (== sum of per-country counts)")
    print(f"country_strata: {actual_strata_unique} unique (== sum of per-country counts)")

    # 8. Explicit WASH-state category counts reconcile exactly (per column, per category)
    for col in WASH_CATEGORY_COLS:
        summed_counts = None
        for c in dfs:
            counts = category_counts_before[col][c]
            summed_counts = counts if summed_counts is None else summed_counts.add(counts, fill_value=0)
        pooled_counts = pooled[col].value_counts(dropna=False)

        all_categories = set(summed_counts.index) | set(pooled_counts.index)
        mismatches = {}
        for cat in all_categories:
            expected = int(summed_counts.get(cat, 0))
            actual = int(pooled_counts.get(cat, 0))
            if expected != actual:
                mismatches[cat] = (expected, actual)
        if mismatches:
            raise RuntimeError(
                f"Category counts for '{col}' do not reconcile after pooling. "
                f"Mismatches (category: (expected, actual)): {mismatches}. Aborting."
            )
    print("WASH explicit-state category counts: reconcile exactly for all columns "
          "(Unknown/StructuralNotApplicable/UnclassifiedBioDigester preserved)")

    # ---- Additional approved checks a-d ----

    # (a) Missing-value counts per column reconcile exactly (all 59 original columns)
    missing_after = pooled[reference_cols].isna().sum()
    summed_missing_before = sum(missing_before.values())
    if not missing_after.equals(summed_missing_before):
        mismatched = missing_after[missing_after != summed_missing_before]
        raise RuntimeError(
            f"Check (a) FAILED: missing-value counts do not reconcile for "
            f"column(s): {list(mismatched.index)}. Aborting."
        )
    print("Check (a): missing-value counts reconcile exactly for every original column")

    # (b) dtypes preserved exactly post-concat for all 59 original columns
    for col in reference_cols:
        if str(pooled[col].dtype) != str(reference_dtypes[col]):
            raise RuntimeError(
                f"Check (b) FAILED: dtype for '{col}' changed after pooling: "
                f"{reference_dtypes[col]} -> {pooled[col].dtype}. Aborting."
            )
    print("Check (b): dtypes unchanged for all 59 original columns after concatenation")

    # (c) country_child_id non-null for 100% of rows (explicit restatement of check 3)
    if pooled["country_child_id"].isna().sum() != 0:
        raise RuntimeError("Check (c) FAILED: country_child_id has null value(s).")
    print("Check (c): country_child_id 100% non-null")

    # (d) v022_raw == v023_raw holds for every row in the pooled data
    if not (pooled["v022_raw"] == pooled["v023_raw"]).all():
        n_diff = int((pooled["v022_raw"] != pooled["v023_raw"]).sum())
        raise RuntimeError(f"Check (d) FAILED: v022_raw != v023_raw for {n_diff} pooled row(s).")
    print("Check (d): v022_raw == v023_raw holds for all pooled rows")

    # ---- Add provenance timestamp AFTER all checks, BEFORE final column count ----
    pooled["generated_at_utc_step05"] = datetime.now(timezone.utc).isoformat()

    n_cols = pooled.shape[1]
    expected_cols = len(reference_cols) + 4  # country_child_id, country_psu, country_strata, generated_at_utc_step05
    if n_cols != expected_cols:
        raise RuntimeError(
            f"Final column count ({n_cols}) != expected ({expected_cols} = "
            f"{len(reference_cols)} original + 4 new). Aborting."
        )
    print(f"Final schema check: {n_cols} columns (== {len(reference_cols)} original + 4 new)")

    # ====================================================================
    # WRITE
    # ====================================================================
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pooled.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nWritten: {OUTPUT_PATH}  ({len(pooled)} rows, {pooled.shape[1]} columns)")

    # ---- Final re-verification: the four Step 04 inputs are still unchanged ----
    checksums_after = {c: md5_of_file(p) for c, p in INPUT_PATHS.items()}
    for c in INPUT_PATHS:
        if checksums_before[c] != checksums_after[c]:
            raise RuntimeError(
                f"[{c}] Step 04 input file checksum changed during Step 05 execution! "
                "This should be impossible - Step 05 never opens these files for writing."
            )
    print("Input file integrity check: all four Step 04 parquet files unchanged (checksum match)")


if __name__ == "__main__":
    main()
