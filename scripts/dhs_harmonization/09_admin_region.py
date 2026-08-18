"""
09_admin_region.py
====================
Constructs a country-qualified subnational ADMINISTRATIVE-region fixed-
effect identifier, per the approved cross-sectional identification
strategy (multi-round θ_kt/α_c identification is not feasible with one
DHS round per country - see the approved Step 09 methodological
reconciliation and pre-execution design audit).

Source variable is the appropriate DHS sampling-frame administrative
geography for each country - NOT a single raw variable name forced
uniformly across countries, and NOT DHSREGNA (Kenya's DHSREGNA is a
malaria-endemicity ecological zone, not administrative geography - see
audit):

  Ethiopia: v024  (14 regions)
  Ghana:    v024  (16 regions)
  Kenya:    v024  (47 counties - preserved in full, NOT harmonized/
            collapsed to DHSREGNA's 5 malaria-endemicity zones)
  Nigeria:  sstate1 (37 states/FCT - preserved in full, NOT replaced by
            the coarser 6-zone v024 variable)

Builds exactly three new substantive columns plus one provenance
timestamp:
  admin_region_code   - raw numeric source code, unchanged
  admin_region_name   - label decoded directly from that source
                         variable's own DHS value-label dictionary, no
                         manual recoding
  country_admin_region - country + "::" + zero-padded 2-digit
                         admin_region_code (collision-proof across
                         countries by construction; uses the CODE, not
                         the name, so it does not depend on label-text
                         formatting)
  generated_at_utc_step09

KNOWN LABEL-TEXT VARIANT (documented, not corrected): Nigeria's v023
(strata) value-label dictionary spells the Federal Capital Territory
"fct", while sstate1's own value-label dictionary spells it "fct-abuja".
Same place, two DHS-supplied label strings. admin_region_name uses
sstate1's own label ("fct-abuja") unchanged, per the approved design -
this is not normalized or corrected here.

REGRESSION INTERPRETATION LOCK (approved, stated here for the record):
country_admin_region is a CROSS-SECTIONAL geographic fixed-effect
identifier. It is NOT a longitudinal panel identifier, NOT a survey-year
FE, NOT a substitute for country x survey-year in a multi-round design,
and is NOT evidence of temporal identification. The original multi-round
identification strategy (grid alpha_c / country x survey-year theta_kt)
is not feasible with the currently assembled data (one DHS round per
country) and is not reconstructed here. interview_year is NOT used
anywhere in this script. No spatial grid, coordinate transformation,
distance measure, or map is built here - LATNUM/LONGNUM/ALT_DEM remain
untouched in the Step 06/08 columns for possible future robustness work.

Reads (read-only):
  - data/processed/pooled_kr_four_country_wash_exposure.parquet (Step 08 output)
  - the four countries' raw KR .dta files under data/interim/DHS/.../KR/

Writes:
  - data/processed/pooled_kr_four_country_admin_region.parquet
  - outputs/tables/step09_admin_region_report.csv
  - outputs/tables/step09_admin_region_validation_summary.csv

Never opens Steps 00-08 scripts or outputs in write mode.
"""

import hashlib
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

POOLED_INPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_wash_exposure.parquet"
OUTPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_admin_region.parquet"
REPORT_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "step09_admin_region_report.csv"
VALIDATION_SUMMARY_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "step09_admin_region_validation_summary.csv"

KR_PATHS = {c: info["kr_path"] for c, info in config.COUNTRIES.items()}
ID_COLS = ["v001", "v002", "v003", "bidx"]

SOURCE_VAR = {"ethiopia": "v024", "ghana": "v024", "kenya": "v024", "nigeria": "sstate1"}
EXPECTED_REGION_COUNTS = {"ethiopia": 14, "ghana": 16, "kenya": 47, "nigeria": 37}
EXPECTED_ROW_COUNTS = {"ethiopia": 13565, "ghana": 9353, "kenya": 19530, "nigeria": 27783}
EXPECTED_TOTAL_ROWS = 70231
EXPECTED_STEP08_COLS = 84
MIN_CELL_CHILDREN = 30


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("="*90)
    print("STEP 09 - COUNTRY-QUALIFIED ADMINISTRATIVE-REGION FE CONSTRUCTION")
    print("="*90)

    # ---- Verify inputs exist ----
    if not POOLED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 08 pooled input not found: {POOLED_INPUT_PATH}")
    for country, path in KR_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(f"[{country}] KR file not found: {path}")

    checksum_pooled_before = md5_of_file(POOLED_INPUT_PATH)
    checksums_kr_before = {c: md5_of_file(p) for c, p in KR_PATHS.items()}

    # ====================================================================
    # LOAD STEP 08 POOLED DATASET
    # ====================================================================
    pooled = pd.read_parquet(POOLED_INPUT_PATH)
    n_pooled_before = len(pooled)
    pooled_cols_before = list(pooled.columns)
    step08_snapshot = pooled[pooled_cols_before].copy()
    print(f"\nLoaded Step 08 pooled dataset: {n_pooled_before} rows, {pooled.shape[1]} columns")

    if n_pooled_before != EXPECTED_TOTAL_ROWS:
        raise RuntimeError(f"Step 08 row count ({n_pooled_before}) != expected ({EXPECTED_TOTAL_ROWS}). Aborting.")
    if pooled.shape[1] != EXPECTED_STEP08_COLS:
        raise RuntimeError(f"Step 08 column count ({pooled.shape[1]}) != expected ({EXPECTED_STEP08_COLS}). Aborting.")

    n_per_country_before = pooled["country"].value_counts().to_dict()
    for country, expected_n in EXPECTED_ROW_COUNTS.items():
        if n_per_country_before.get(country) != expected_n:
            raise RuntimeError(
                f"[{country}] Step 08 row count ({n_per_country_before.get(country)}) != "
                f"expected ({expected_n}). Aborting."
            )
    print("Per-country row counts confirmed: Ethiopia 13,565 / Ghana 9,353 / Kenya 19,530 / Nigeria 27,783")

    if pooled["country_child_id"].duplicated().any() or pooled["country_child_id"].isna().any():
        raise RuntimeError("country_child_id not unique/non-null in Step 08 input. Aborting.")

    # ====================================================================
    # PER-COUNTRY: read fresh KR admin-region source variable + link
    # ====================================================================
    merged_frames = []
    report_rows = []

    for country_key, kr_path in KR_PATHS.items():
        source_var = SOURCE_VAR[country_key]
        print(f"\n{'-'*90}\n[{country_key}] source variable: {source_var}\n{'-'*90}")

        usecols = ID_COLS + [source_var]
        extra_nesting_col = None
        if country_key == "nigeria":
            usecols = usecols + ["v024"]
            extra_nesting_col = "v024"

        kr_df, meta = pyreadstat.read_dta(str(kr_path), usecols=usecols)

        # ---- Duplicate identifier guard (defense in depth) ----
        dup_mask = kr_df.duplicated(subset=ID_COLS, keep=False)
        if dup_mask.any():
            raise RuntimeError(f"[{country_key}] Duplicate identifier keys in fresh KR extraction. Aborting.")

        # ---- Decode admin_region_code / admin_region_name from the source variable's OWN dictionary ----
        value_labels = meta.variable_value_labels.get(source_var, {})
        if not value_labels:
            raise RuntimeError(f"[{country_key}] No value-label dictionary found for {source_var}. Aborting.")

        if kr_df[source_var].isna().any():
            n_na = int(kr_df[source_var].isna().sum())
            raise RuntimeError(f"[{country_key}] {source_var}: {n_na} row(s) missing - unexpected. Aborting.")

        kr_df["admin_region_code"] = kr_df[source_var].astype("int64")
        kr_df["admin_region_name"] = kr_df["admin_region_code"].map(value_labels)
        if kr_df["admin_region_name"].isna().any():
            unmapped = sorted(kr_df.loc[kr_df["admin_region_name"].isna(), "admin_region_code"].unique())
            raise RuntimeError(
                f"[{country_key}] {source_var} code(s) {unmapped} have no entry in the value-label "
                "dictionary. Aborting rather than guessing a label."
            )

        n_regions_observed = kr_df["admin_region_name"].nunique()
        expected_n = EXPECTED_REGION_COUNTS[country_key]
        if n_regions_observed != expected_n:
            raise RuntimeError(
                f"[{country_key}] Observed {n_regions_observed} administrative region(s), "
                f"expected {expected_n}. Aborting."
            )
        print(f"  {source_var}: {n_regions_observed} regions observed (== expected {expected_n}), "
              f"0 missing, dictionary-decoded")

        # ---- Constant-within-PSU check on the SOURCE variable (pre-merge) ----
        per_psu_nunique = kr_df.groupby("v001")["admin_region_name"].nunique(dropna=False)
        n_bad_psu = int((per_psu_nunique > 1).sum())
        if n_bad_psu > 0:
            raise RuntimeError(
                f"[{country_key}] {source_var} is not constant within {n_bad_psu} PSU(s). Aborting."
            )
        print(f"  {source_var} constant within every PSU: confirmed (0/{kr_df['v001'].nunique()} violations)")

        # ---- Nigeria-only: sstate1 must nest perfectly within v024 (1 zone per state) ----
        if extra_nesting_col:
            kr_df["_nesting_label"] = kr_df[extra_nesting_col].map(meta.variable_value_labels.get(extra_nesting_col, {}))
            nest = kr_df.groupby("admin_region_name")["_nesting_label"].nunique(dropna=False)
            n_bad_nest = int((nest > 1).sum())
            if n_bad_nest > 0:
                raise RuntimeError(
                    f"[{country_key}] {source_var} fails to nest within {extra_nesting_col}: "
                    f"{n_bad_nest} state(s) span more than one zone. Aborting."
                )
            print(f"  {source_var} nests perfectly within {extra_nesting_col}: confirmed (0 violations)")
            kr_df = kr_df.drop(columns=["_nesting_label", extra_nesting_col])

        # ---- country_admin_region ----
        kr_df["country_admin_region"] = country_key + "::" + kr_df["admin_region_code"].astype(str).str.zfill(2)

        admin_frame = kr_df[ID_COLS + ["admin_region_code", "admin_region_name", "country_admin_region"]]

        # ---- Link to this country's Step 08 subset ----
        step08_country = pooled[pooled["country"] == country_key].copy()
        before_ids = step08_country[ID_COLS].reset_index(drop=True)

        merged_country = step08_country.merge(
            admin_frame, on=ID_COLS, how="left", validate="one_to_one", indicator=True
        )
        if len(merged_country) != len(step08_country):
            raise RuntimeError(f"[{country_key}] Merge changed row count. Aborting.")
        n_unmatched = int((merged_country["_merge"] != "both").sum())
        if n_unmatched > 0:
            raise RuntimeError(f"[{country_key}] {n_unmatched} Step 08 child row(s) unmatched to {source_var}. Aborting.")
        merged_country = merged_country.drop(columns="_merge")

        after_ids = merged_country[ID_COLS].reset_index(drop=True)
        if not before_ids.equals(after_ids):
            raise RuntimeError(f"[{country_key}] Identifier values/order changed after merge. Aborting.")
        print(f"  Linkage to Step 08 children: 100% match, 0 unmatched ({len(merged_country)} rows)")

        merged_frames.append(merged_country)

        region_summary = merged_country.groupby(
            ["admin_region_code", "admin_region_name", "country_admin_region"]
        ).agg(child_n=("country_child_id", "count"), unique_psu_n=("psu", "nunique")).reset_index()
        region_summary.insert(0, "country", country_key)
        region_summary["percent_of_country_children"] = round(
            100 * region_summary["child_n"] / len(merged_country), 4
        )
        report_rows.append(region_summary)

    merged = pd.concat(merged_frames, ignore_index=True)
    print(f"\nCombined all four countries: {len(merged)} rows")

    # ====================================================================
    # VALIDATION
    # ====================================================================
    print(f"\n{'='*90}\nVALIDATION\n{'='*90}")

    if len(merged) != n_pooled_before:
        raise RuntimeError(f"Row count changed: {n_pooled_before} -> {len(merged)}. Aborting.")
    print(f"Row count check: {len(merged)} == Step 08 input ({n_pooled_before})")

    for country_key, n_before in n_per_country_before.items():
        n_after = int((merged["country"] == country_key).sum())
        if n_after != n_before:
            raise RuntimeError(f"[{country_key}] Row count changed: {n_before} -> {n_after}.")
    print("Per-country row count check: unchanged for all four")

    if merged["country_child_id"].duplicated().any() or merged["country_child_id"].isna().any():
        raise RuntimeError("country_child_id not unique/non-null after Step 09 linkage. Aborting.")
    print("country_child_id: unique and non-null after Step 09 linkage")

    # All Step 08 columns row-for-row identical (never overwritten)
    for col in pooled_cols_before:
        both_na = merged[col].isna() & step08_snapshot[col].isna()
        mismatch = (merged[col] != step08_snapshot[col]) & ~both_na
        if mismatch.any():
            raise RuntimeError(f"Step 08 column '{col}' changed after Step 09 linkage ({int(mismatch.sum())} row(s)). Aborting.")
    print(f"All {len(pooled_cols_before)} Step 08 columns: unchanged (row-for-row identity confirmed, "
          f"including DHSREGNA, DHSREGCO, strata, country_strata, psu, country_psu)")

    # admin_region_code / name / country_admin_region non-missing everywhere
    for col in ["admin_region_code", "admin_region_name", "country_admin_region"]:
        if merged[col].isna().any():
            raise RuntimeError(f"{col} missing for {int(merged[col].isna().sum())} row(s). Aborting.")
    print("admin_region_code / admin_region_name / country_admin_region: non-missing for all rows")

    # country_admin_region constant within country_psu; each country_psu -> exactly 1 country_admin_region
    psu_region_nunique = merged.groupby("country_psu")["country_admin_region"].nunique()
    if (psu_region_nunique > 1).any():
        bad = psu_region_nunique[psu_region_nunique > 1].index.tolist()
        raise RuntimeError(f"{len(bad)} country_psu value(s) map to more than one country_admin_region: {bad[:10]}. Aborting.")
    print("country_admin_region constant within every country_psu: confirmed (each country_psu -> exactly 1 region)")

    # each country_admin_region belongs to exactly 1 country
    region_country_nunique = merged.groupby("country_admin_region")["country"].nunique()
    if (region_country_nunique > 1).any():
        bad = region_country_nunique[region_country_nunique > 1].index.tolist()
        raise RuntimeError(f"{len(bad)} country_admin_region value(s) span more than one country: {bad[:10]}. Aborting.")
    print("Each country_admin_region belongs to exactly one country: confirmed")

    # region counts, singleton-PSU, small-cell checks, per country
    validation_summary_rows = []
    for country_key in config.COUNTRIES:
        sub = merged[merged["country"] == country_key]
        cell_stats = sub.groupby("country_admin_region").agg(
            n_children=("country_child_id", "count"), n_psu=("psu", "nunique")
        )
        n_observed = len(cell_stats)
        expected_n = EXPECTED_REGION_COUNTS[country_key]
        if n_observed != expected_n:
            raise RuntimeError(f"[{country_key}] Final observed region count ({n_observed}) != expected ({expected_n}). Aborting.")

        n_singleton_psu = int((cell_stats["n_psu"] == 1).sum())
        if n_singleton_psu > 0:
            raise RuntimeError(f"[{country_key}] {n_singleton_psu} region(s) have only 1 PSU. Aborting.")

        n_small = int((cell_stats["n_children"] < MIN_CELL_CHILDREN).sum())
        if n_small > 0:
            raise RuntimeError(f"[{country_key}] {n_small} region(s) have fewer than {MIN_CELL_CHILDREN} children. Aborting.")

        n_missing_region = int(sub["country_admin_region"].isna().sum())

        psu_span = sub.groupby("psu")["country_admin_region"].nunique()
        n_psu_spanning = int((psu_span > 1).sum())

        print(f"[{country_key}] regions: {n_observed} (== expected {expected_n}); "
              f"singleton-PSU regions: {n_singleton_psu}; regions <{MIN_CELL_CHILDREN} children: {n_small}; "
              f"PSUs spanning >1 region: {n_psu_spanning}")

        validation_summary_rows.append({
            "country": country_key,
            "expected_regions": expected_n,
            "observed_regions": n_observed,
            "missing_admin_region_rows": n_missing_region,
            "unique_psus": int(sub["psu"].nunique()),
            "psus_spanning_gt1_admin_region": n_psu_spanning,
            "singleton_psu_regions": n_singleton_psu,
            "regions_lt30_children": n_small,
        })

    # Kenya / Nigeria explicit preservation checks
    kenya_regions = merged.loc[merged["country"] == "kenya", "admin_region_name"].nunique()
    if kenya_regions != 47:
        raise RuntimeError(f"Kenya: {kenya_regions} counties in final output != 47. Aborting.")
    print("Kenya: all 47 counties preserved in final output")

    nigeria_regions = merged.loc[merged["country"] == "nigeria", "admin_region_name"].nunique()
    if nigeria_regions != 37:
        raise RuntimeError(f"Nigeria: {nigeria_regions} states in final output != 37. Aborting.")
    print("Nigeria: all 37 states/FCT preserved in final output")

    # ---- Add provenance timestamp AFTER all substantive validation ----
    merged["generated_at_utc_step09"] = datetime.now(timezone.utc).isoformat()

    new_cols = [c for c in merged.columns if c not in pooled_cols_before]
    print(f"\nNew columns added in Step 09 ({len(new_cols)}): {new_cols}")

    n_cols = merged.shape[1]
    expected_cols = EXPECTED_STEP08_COLS + 4  # admin_region_code, admin_region_name, country_admin_region, timestamp
    if n_cols != expected_cols:
        raise RuntimeError(f"Final column count ({n_cols}) != expected ({expected_cols}). Aborting.")
    print(f"Final schema check: {n_cols} columns (== {EXPECTED_STEP08_COLS} Step08 + 4 new)")

    # ====================================================================
    # WRITE OUTPUTS
    # ====================================================================
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nWritten: {OUTPUT_PATH}  ({len(merged)} rows, {merged.shape[1]} columns)")

    region_report = pd.concat(report_rows, ignore_index=True).sort_values(
        ["country", "admin_region_code"]
    ).reset_index(drop=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    region_report.to_csv(REPORT_PATH, index=False)
    print(f"Written: {REPORT_PATH}  ({len(region_report)} region rows)")

    validation_summary = pd.DataFrame(validation_summary_rows)
    validation_summary.to_csv(VALIDATION_SUMMARY_PATH, index=False)
    print(f"Written: {VALIDATION_SUMMARY_PATH}  ({len(validation_summary)} country rows)")

    # ---- Final source-integrity re-verification ----
    checksum_pooled_after = md5_of_file(POOLED_INPUT_PATH)
    if checksum_pooled_after != checksum_pooled_before:
        raise RuntimeError("Step 08 input file changed during Step 09 execution!")
    checksums_kr_after = {c: md5_of_file(p) for c, p in KR_PATHS.items()}
    if checksums_kr_before != checksums_kr_after:
        raise RuntimeError("A raw KR source file changed during Step 09 execution!")
    print("\nSource integrity check: Step 08 input and all four raw KR source files unchanged (checksum match)")


if __name__ == "__main__":
    main()
