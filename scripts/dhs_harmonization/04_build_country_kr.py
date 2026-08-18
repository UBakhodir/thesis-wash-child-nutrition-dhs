"""
04_build_country_kr.py
========================
Builds the final per-country analytical KR dataset by adding approved
child/maternal/household controls and survey-design/period variables to
Step 03's kr_indicators.parquet. Reads the additional raw variables
fresh (read-only) from the same source KR .dta files used in Steps 02-03.

Strata variable: v023 is used uniformly across all four countries as the
analytical strata variable, per the approved decision. v022 and v023 are
verified (not assumed) to be numerically identical in every row of all
four surveys - this script re-asserts that identity as a hard runtime
check rather than relying on the earlier one-time audit. v023 was chosen
over v022 primarily because Ethiopia's bundled metadata attaches value
labels only to v023, giving it stronger documentation support; for
Ghana/Kenya/Nigeria the two variables are documentation-symmetric, so
using v023 uniformly is a consistency choice, not a correction of
different content.

No regression is run, no pooling occurs, no wealth index is rescaled
across countries, no age-squared term is created, and s114 is not used.
"""

import importlib.util
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyreadstat

SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

ID_COLS = ["v001", "v002", "v003", "bidx"]
NEW_RAW_VARS = ["b4", "hw1", "b19", "v012", "v106", "v155", "v190", "v025",
                 "v005", "v021", "v022", "v023", "v007"]
# hw1 is already in Step 03's output; re-read here only for the explicit
# verification-against-source check, not to overwrite the existing column.

SEX_LABELS = {1: "Male", 2: "Female"}
EDUCATION_LABELS = {0: "No education", 1: "Primary", 2: "Secondary", 3: "Higher"}
LITERACY_LABELS = {
    0: "Cannot read at all", 1: "Able to read only parts of sentence",
    2: "Able to read whole sentence", 3: "No card with required language",
    4: "Blind/visually impaired",
}
WEALTH_LABELS = {1: "Poorest", 2: "Poorer", 3: "Middle", 4: "Richer", 5: "Richest"}
RESIDENCE_LABELS = {1: "Urban", 2: "Rural"}

WEIGHT_DIVISOR = config.WEIGHT_DIVISOR  # 1_000_000


def map_known_code(raw_series, mapping_dict, var_label, country):
    """Same pattern as Step 03's map_wash_code: hard-fail on any code or
    missingness not covered by the audited mapping. No guessing."""
    if raw_series.isna().any():
        n_na = int(raw_series.isna().sum())
        raise RuntimeError(
            f"[{country}] {var_label}: {n_na} row(s) system-missing - not "
            "observed in the pre-design audit (0 missing confirmed for all "
            "four countries). Aborting rather than silently handling this."
        )
    unmapped = sorted(c for c in set(raw_series.unique()) if c not in mapping_dict)
    if unmapped:
        raise RuntimeError(
            f"[{country}] {var_label}: unmapped code(s) {unmapped} not seen "
            "in the pre-design audit. Aborting rather than guessing a label."
        )
    return raw_series.map(mapping_dict)


def run_country(country_key, info):
    """
    End-to-end Step 04 processing for one country: load Step 03's
    indicators, re-read the additional control/weight/design variables
    fresh from the source KR file, verify v022==v023 (the basis for the
    uniform-v023-as-strata decision - see module docstring), decode the
    categorical controls via the approved label dictionaries, construct
    weight_original/psu/strata/interview_year, and write the per-country
    clean parquet.
    """
    print(f"\n{'='*90}\n{info['survey_label']}\n{'='*90}")

    step03_path = info["staging_dir"] / "kr_indicators.parquet"
    if not step03_path.exists():
        raise FileNotFoundError(f"[{country_key}] Step 03 output not found: {step03_path}")
    base_df = pd.read_parquet(step03_path)
    n_step03 = len(base_df)
    print(f"Loaded Step 03 output: {step03_path.name} ({n_step03} rows)")

    kr_path = info["kr_path"]
    new_df, meta = pyreadstat.read_dta(str(kr_path), usecols=ID_COLS + NEW_RAW_VARS)

    dup_mask = new_df.duplicated(subset=ID_COLS, keep=False)
    if dup_mask.any():
        raise RuntimeError(f"[{country_key}] Duplicate identifier keys re-reading controls. Aborting.")

    merged = base_df.merge(
        new_df, on=ID_COLS, how="left", validate="one_to_one",
        suffixes=("", "_fresh"), indicator=True
    )
    if len(merged) != n_step03:
        raise RuntimeError(f"[{country_key}] Merge changed row count: {n_step03} -> {len(merged)}.")
    if not (merged["_merge"] == "both").all():
        raise RuntimeError(f"[{country_key}] Unmatched rows in control-variable merge.")
    merged = merged.drop(columns="_merge")

    # ---- Explicit verification: hw1 already in Step 03 output matches source ----
    both_na = merged["hw1"].isna() & merged["hw1_fresh"].isna()
    mismatch = (merged["hw1"] != merged["hw1_fresh"]) & ~both_na
    if mismatch.any():
        raise RuntimeError(
            f"[{country_key}] hw1 in Step 03 output does not match a fresh "
            f"source read ({int(mismatch.sum())} mismatched row(s)). Aborting."
        )
    merged = merged.drop(columns="hw1_fresh")
    print("hw1 verification against source: identical")

    # ---- Identifier preservation vs Step 03 ----
    before = base_df[ID_COLS].reset_index(drop=True)
    after = merged[ID_COLS].reset_index(drop=True)
    if not before.equals(after):
        raise RuntimeError(f"[{country_key}] Identifier values/order changed vs Step 03.")
    print("Identifier preservation check (vs Step 03): identical")

    # ---- Rename raw columns for auditability ----
    merged = merged.rename(columns={
        "b4": "b4_raw", "b19": "b19_raw", "v012": "v012_raw", "v106": "v106_raw",
        "v155": "v155_raw", "v190": "v190_raw", "v025": "v025_raw",
        "v005": "v005_raw", "v021": "v021_raw", "v022": "v022_raw",
        "v023": "v023_raw", "v007": "v007_raw",
    })

    # ---- HARD VALIDATION: v022_raw == v023_raw for every row, every country ----
    # Re-asserted here at runtime rather than relying solely on the earlier
    # one-time audit, since the uniform-v023 decision depends on this identity.
    if not (merged["v022_raw"] == merged["v023_raw"]).all():
        n_diff = int((merged["v022_raw"] != merged["v023_raw"]).sum())
        raise RuntimeError(
            f"[{country_key}] v022_raw != v023_raw for {n_diff} row(s). The "
            "uniform-v023 strata decision assumes these are always identical "
            "in every country. Aborting rather than silently continuing."
        )
    print("v022_raw == v023_raw check: identical for all rows")

    # ---- Harmonized categorical labels ----
    merged["child_sex"] = map_known_code(merged["b4_raw"], SEX_LABELS, "b4", country_key)
    merged["maternal_education"] = map_known_code(merged["v106_raw"], EDUCATION_LABELS, "v106", country_key)
    merged["literacy"] = map_known_code(merged["v155_raw"], LITERACY_LABELS, "v155", country_key)
    merged["wealth_quintile"] = map_known_code(merged["v190_raw"], WEALTH_LABELS, "v190", country_key)
    merged["residence"] = map_known_code(merged["v025_raw"], RESIDENCE_LABELS, "v025", country_key)

    # ---- Continuous controls (linear, unchanged) ----
    merged["maternal_age"] = merged["v012_raw"].astype("float64")

    # ---- Survey weight: only the 1,000,000 scaling, nothing else ----
    if (merged["v005_raw"] < 0).any():
        raise RuntimeError(f"[{country_key}] Negative v005 values found - aborting.")
    merged["weight_original"] = merged["v005_raw"].astype("float64") / WEIGHT_DIVISOR

    # ---- Survey design identifiers ----
    merged["psu"] = merged["v021_raw"]
    merged["strata"] = merged["v023_raw"]   # uniform v023 decision

    # ---- Survey period ----
    merged["interview_year"] = merged["v007_raw"]
    # country / survey_round already present from Step 02/03, untouched

    # ====================================================================
    # VALIDATION
    # ====================================================================
    if len(merged) != n_step03:
        raise RuntimeError(f"[{country_key}] Final row count changed from Step 03.")

    if (merged["country"] != country_key).any():
        raise RuntimeError(f"[{country_key}] country column altered.")
    if (merged["survey_round"] != info["country_round"]).any():
        raise RuntimeError(f"[{country_key}] survey_round column altered.")

    if not (merged["psu"] == merged["v021_raw"]).all():
        raise RuntimeError(f"[{country_key}] psu does not exactly equal v021_raw.")
    if not (merged["strata"] == merged["v023_raw"]).all():
        raise RuntimeError(f"[{country_key}] strata does not exactly equal v023_raw.")

    expected_weight = merged["v005_raw"].astype("float64") / WEIGHT_DIVISOR
    if not np.allclose(merged["weight_original"], expected_weight, atol=1e-12):
        raise RuntimeError(f"[{country_key}] weight_original does not equal v005_raw/1,000,000 exactly.")

    # ---- Add provenance timestamp BEFORE computing/printing final column
    # count, so the reported count exactly matches the written parquet ----
    merged["generated_at_utc_step04"] = datetime.now(timezone.utc).isoformat()

    n_cols = merged.shape[1]  # computed live, after all columns exist
    print(f"All validation checks passed for {country_key}. "
          f"({len(merged)} rows, {n_cols} columns)")

    out_path = info["processed_file"]
    merged.to_parquet(out_path, index=False)
    print(f"Written: {out_path}  ({merged.shape[1]} columns)")

    return merged


if __name__ == "__main__":
    for country_key, info in config.COUNTRIES.items():
        run_country(country_key, info)
