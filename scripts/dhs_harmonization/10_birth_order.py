"""
10_birth_order.py
===================
Extracts and links `bord` (DHS "birth order number") from each country's
raw KR file onto the Step 09 pooled dataset, per the approved Step 10
design audit.

birth_order_raw = bord, preserved exactly as the original integer count -
no categorization, capping, collapsing, recoding, standardization,
transformation, dummy-encoding, or imputation.

This is a data-linkage step only. No regression sample, weight, fixed
effect, dummy matrix, table, figure, map, or thesis prose is created
here, and country_admin_region / interview_year are not touched.

Reads (read-only):
  - data/processed/pooled_kr_four_country_admin_region.parquet (Step 09 output)
  - the four countries' raw KR .dta files under data/interim/DHS/.../KR/

Writes:
  - data/processed/pooled_kr_four_country_birth_order.parquet
  - outputs/tables/step10_birth_order_report.csv

Never opens Steps 00-09 scripts or outputs in write mode.
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

POOLED_INPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_admin_region.parquet"
OUTPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_birth_order.parquet"
REPORT_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "step10_birth_order_report.csv"

KR_PATHS = {c: info["kr_path"] for c, info in config.COUNTRIES.items()}
ID_COLS = ["v001", "v002", "v003", "bidx"]

EXPECTED_ROW_COUNTS = {"ethiopia": 13565, "ghana": 9353, "kenya": 19530, "nigeria": 27783}
EXPECTED_TOTAL_ROWS = 70231
EXPECTED_STEP09_COLS = 88


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    print("="*90)
    print("STEP 10 - BIRTH ORDER (bord) EXTRACTION AND LINKAGE")
    print("="*90)

    # ---- Verify inputs exist ----
    if not POOLED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 09 pooled input not found: {POOLED_INPUT_PATH}")
    for country, path in KR_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(f"[{country}] KR file not found: {path}")

    checksum_pooled_before = md5_of_file(POOLED_INPUT_PATH)
    checksums_kr_before = {c: md5_of_file(p) for c, p in KR_PATHS.items()}

    # ====================================================================
    # LOAD STEP 09 POOLED DATASET
    # ====================================================================
    pooled = pd.read_parquet(POOLED_INPUT_PATH)
    n_pooled_before = len(pooled)
    pooled_cols_before = list(pooled.columns)
    step09_snapshot = pooled[pooled_cols_before].copy()
    print(f"\nLoaded Step 09 pooled dataset: {n_pooled_before} rows, {pooled.shape[1]} columns")

    if n_pooled_before != EXPECTED_TOTAL_ROWS:
        raise RuntimeError(f"Step 09 row count ({n_pooled_before}) != expected ({EXPECTED_TOTAL_ROWS}). Aborting.")
    if pooled.shape[1] != EXPECTED_STEP09_COLS:
        raise RuntimeError(f"Step 09 column count ({pooled.shape[1]}) != expected ({EXPECTED_STEP09_COLS}). Aborting.")

    n_per_country_before = pooled["country"].value_counts().to_dict()
    for country, expected_n in EXPECTED_ROW_COUNTS.items():
        if n_per_country_before.get(country) != expected_n:
            raise RuntimeError(
                f"[{country}] Step 09 row count ({n_per_country_before.get(country)}) != "
                f"expected ({expected_n}). Aborting."
            )
    print("Per-country row counts confirmed: Ethiopia 13,565 / Ghana 9,353 / Kenya 19,530 / Nigeria 27,783")

    if pooled["country_child_id"].duplicated().any() or pooled["country_child_id"].isna().any():
        raise RuntimeError("country_child_id not unique/non-null in Step 09 input. Aborting.")
    print("country_child_id: unique and non-null")

    # ====================================================================
    # PER-COUNTRY: read fresh KR bord + link
    # ====================================================================
    merged_frames = []
    report_rows = []

    for country_key, kr_path in KR_PATHS.items():
        print(f"\n{'-'*90}\n[{country_key}] source variable: bord\n{'-'*90}")

        kr_df, meta = pyreadstat.read_dta(str(kr_path), usecols=ID_COLS + ["bord"])

        if "bord" not in kr_df.columns:
            raise RuntimeError(f"[{country_key}] bord not found in KR file. Aborting.")

        # ---- Duplicate identifier guard ----
        dup_mask = kr_df.duplicated(subset=ID_COLS, keep=False)
        if dup_mask.any():
            raise RuntimeError(f"[{country_key}] Duplicate identifier keys in fresh KR extraction. Aborting.")
        print(f"  Fresh KR read: {len(kr_df)} rows, 0 duplicate (v001,v002,v003,bidx) keys")

        # ---- bord missingness / positivity ----
        if kr_df["bord"].isna().any():
            n_na = int(kr_df["bord"].isna().sum())
            raise RuntimeError(f"[{country_key}] bord has {n_na} missing value(s). Aborting.")
        if (kr_df["bord"] <= 0).any():
            n_bad = int((kr_df["bord"] <= 0).sum())
            raise RuntimeError(f"[{country_key}] bord has {n_bad} non-positive value(s). Aborting.")
        if not np.issubdtype(kr_df["bord"].dtype, np.integer) and not (kr_df["bord"] == kr_df["bord"].round()).all():
            raise RuntimeError(f"[{country_key}] bord contains non-integer value(s). Aborting.")
        print(f"  bord: 0 missing, all positive integers, range {kr_df['bord'].min()}-{kr_df['bord'].max()}")

        kr_df = kr_df.rename(columns={"bord": "birth_order_raw"})
        bord_frame = kr_df[ID_COLS + ["birth_order_raw"]]

        # ---- Link to this country's Step 09 subset ----
        step09_country = pooled[pooled["country"] == country_key].copy()
        n_step09_country = len(step09_country)
        before_ids = step09_country[ID_COLS].reset_index(drop=True)

        merged_country = step09_country.merge(
            bord_frame, on=ID_COLS, how="left", validate="one_to_one", indicator=True
        )
        if len(merged_country) != n_step09_country:
            raise RuntimeError(f"[{country_key}] Merge changed row count. Aborting.")
        n_unmatched = int((merged_country["_merge"] != "both").sum())
        if n_unmatched > 0:
            raise RuntimeError(f"[{country_key}] {n_unmatched} Step 09 child row(s) unmatched to bord. Aborting.")
        merged_country = merged_country.drop(columns="_merge")

        after_ids = merged_country[ID_COLS].reset_index(drop=True)
        if not before_ids.equals(after_ids):
            raise RuntimeError(f"[{country_key}] Identifier values/order changed after merge. Aborting.")
        print(f"  Linkage to Step 09 children: 100% match, 0 unmatched ({len(merged_country)} rows)")

        if merged_country["birth_order_raw"].isna().any():
            raise RuntimeError(f"[{country_key}] birth_order_raw missing after merge - unexpected. Aborting.")

        # ---- Exact-equality re-verification against a fresh independent read ----
        recheck_df, _ = pyreadstat.read_dta(str(kr_path), usecols=ID_COLS + ["bord"])
        recheck = merged_country[ID_COLS].merge(
            recheck_df, on=ID_COLS, how="left", validate="one_to_one"
        )
        mismatch = (merged_country["birth_order_raw"].values != recheck["bord"].values).sum()
        if mismatch > 0:
            raise RuntimeError(f"[{country_key}] birth_order_raw does not exactly equal freshly-read bord for {mismatch} row(s). Aborting.")
        print(f"  birth_order_raw == freshly-read bord: confirmed exact match for all {len(merged_country)} rows")

        merged_frames.append(merged_country)

        report_rows.append({
            "country": country_key,
            "total_child_rows": n_step09_country,
            "linked_rows": int((merged_country["birth_order_raw"].notna()).sum()),
            "unmatched_rows": n_unmatched,
            "missing_birth_order_raw": int(merged_country["birth_order_raw"].isna().sum()),
            "min_birth_order": int(merged_country["birth_order_raw"].min()),
            "median_birth_order": float(merged_country["birth_order_raw"].median()),
            "mean_birth_order": float(merged_country["birth_order_raw"].mean()),
            "max_birth_order": int(merged_country["birth_order_raw"].max()),
            "n_unique_birth_order_values": int(merged_country["birth_order_raw"].nunique()),
        })

    merged = pd.concat(merged_frames, ignore_index=True)
    print(f"\nCombined all four countries: {len(merged)} rows")

    # ====================================================================
    # VALIDATION
    # ====================================================================
    print(f"\n{'='*90}\nVALIDATION\n{'='*90}")

    if len(merged) != n_pooled_before:
        raise RuntimeError(f"Row count changed: {n_pooled_before} -> {len(merged)}. Aborting.")
    print(f"Row count check: {len(merged)} == Step 09 input ({n_pooled_before})")

    for country_key, n_before in n_per_country_before.items():
        n_after = int((merged["country"] == country_key).sum())
        if n_after != n_before:
            raise RuntimeError(f"[{country_key}] Row count changed: {n_before} -> {n_after}.")
    print("Per-country row count check: unchanged for all four")

    if merged["country_child_id"].duplicated().any() or merged["country_child_id"].isna().any():
        raise RuntimeError("country_child_id not unique/non-null after Step 10 linkage. Aborting.")
    print("country_child_id: unique and non-null after Step 10 linkage")

    # All Step 09 columns row-for-row identical (never overwritten)
    for col in pooled_cols_before:
        both_na = merged[col].isna() & step09_snapshot[col].isna()
        mismatch = (merged[col] != step09_snapshot[col]) & ~both_na
        if mismatch.any():
            raise RuntimeError(f"Step 09 column '{col}' changed after Step 10 linkage ({int(mismatch.sum())} row(s)). Aborting.")
    print(f"All {len(pooled_cols_before)} Step 09 columns: unchanged (row-for-row identity confirmed, "
          f"including country_admin_region, interview_year, admin_region_code, admin_region_name)")

    if merged["birth_order_raw"].isna().any():
        raise RuntimeError(f"birth_order_raw missing for {int(merged['birth_order_raw'].isna().sum())} row(s). Aborting.")
    print("birth_order_raw: non-missing for all rows")

    print("\nObserved birth-order ranges by country:")
    for country_key in config.COUNTRIES:
        sub = merged[merged["country"] == country_key]["birth_order_raw"]
        print(f"  {country_key:10s} min={sub.min()} median={sub.median()} mean={sub.mean():.3f} "
              f"max={sub.max()} n_unique={sub.nunique()}")

    # ---- Add provenance timestamp AFTER all substantive validation ----
    merged["generated_at_utc_step10"] = datetime.now(timezone.utc).isoformat()

    new_cols = [c for c in merged.columns if c not in pooled_cols_before]
    print(f"\nNew columns added in Step 10 ({len(new_cols)}): {new_cols}")

    n_cols = merged.shape[1]
    expected_cols = EXPECTED_STEP09_COLS + 2  # birth_order_raw, generated_at_utc_step10
    if n_cols != expected_cols:
        raise RuntimeError(f"Final column count ({n_cols}) != expected ({expected_cols}). Aborting.")
    print(f"Final schema check: {n_cols} columns (== {EXPECTED_STEP09_COLS} Step09 + 2 new)")

    # ====================================================================
    # WRITE OUTPUTS
    # ====================================================================
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nWritten: {OUTPUT_PATH}  ({len(merged)} rows, {merged.shape[1]} columns)")

    report_df = pd.DataFrame(report_rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(REPORT_PATH, index=False)
    print(f"Written: {REPORT_PATH}  ({len(report_df)} country rows)")

    # ---- Final source-integrity re-verification ----
    checksum_pooled_after = md5_of_file(POOLED_INPUT_PATH)
    if checksum_pooled_after != checksum_pooled_before:
        raise RuntimeError("Step 09 input file changed during Step 10 execution!")
    checksums_kr_after = {c: md5_of_file(p) for c, p in KR_PATHS.items()}
    if checksums_kr_before != checksums_kr_after:
        raise RuntimeError("A raw KR source file changed during Step 10 execution!")
    print("\nSource integrity check: Step 09 input and all four raw KR source files unchanged (checksum match)")


if __name__ == "__main__":
    main()
