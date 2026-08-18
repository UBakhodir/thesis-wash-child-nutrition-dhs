"""
02_load_flag_anthro.py
========================
Reads each country's KR .dta file (identifiers + anthropometric z-score
variables only), applies DHS-documented special-code handling and 1/100
scaling to hw70/hw71/hw72, and writes one flagged/scaled staging file per
country. Reads ONLY from data/interim/DHS/; never writes to data/raw/ or
data/interim/. Hard-fails (raises, does not write output) if any
validation check fails.

Three distinct conceptual layers, kept separate throughout this script:
  1. DHS STORED SPECIAL CODES - documented in the bundled .map/.DO files
     for every country (verified against ETKR8AFL.map, GHKR8CFL.map,
     KEKR8CFL.map, NGKR8BFL.map):
       9996 = "Height out of plausible limits"
       9997 = "Age in days out of plausible limits"
       9998 = "Flagged cases"
       9999 = "Missing" (DHS's own designated missing-value code;
               empirically observed as UNUSED in all four real datasets -
               see point 2 below)
  2. SYSTEM-MISSING - a raw value that is blank/NaN in the source .dta.
     Empirically, this is how "missing" is actually represented in all
     four countries' real data, not the documented code 9999. System-
     missing rows are NOT given a sentinel flagcode - they are a
     genuinely distinct state from the four documented DHS codes above.
  3. OUR ANALYTICAL TREATMENT - the decision to collapse all five non-
     substantive states (9996, 9997, 9998, 9999, system-missing) into a
     single NaN in the scaled z-score column. This is a choice we are
     making for this analysis, informed by DHS's documentation but not
     dictated verbatim by it.

Approved per Final Analysis Specification SS2/SS3 and the anthropometric
documentation verification.
"""

import importlib.util
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyreadstat

# ----------------------------------------------------------------------
# Load 00_config.py by file path (digit-prefixed filename, not import-able
# with a normal `import` statement)
# ----------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

# ----------------------------------------------------------------------
# Columns to read from each KR file
# ----------------------------------------------------------------------
IDENTIFIER_VARS = ["caseid", "v001", "v002", "v003", "bidx"]
COMPANION_VARS = ["hw1"]                      # child's age in months at measurement
ANTHRO_RAW_VARS = ["hw70", "hw71", "hw72"]    # HAZ, WAZ, WHZ raw (x100, special-coded)

REQUIRED_COLUMNS = IDENTIFIER_VARS + COMPANION_VARS + ANTHRO_RAW_VARS

# ----------------------------------------------------------------------
# DHS-documented special codes for hw70/hw71/hw72 (identical across all
# four countries' bundled .map files - verified this session). Existing
# 00_config.py only defines the two most commonly used (9998/9999); the
# other two (9996/9997) are added here since they are confirmed to occur
# in real hw72 data for Ethiopia/Kenya/Nigeria. A future revision of
# 00_config.py could consolidate all four into one place.
# ----------------------------------------------------------------------
FLAG_HEIGHT_IMPLAUSIBLE = 9996   # "Height out of plausible limits"
FLAG_AGE_IMPLAUSIBLE = 9997      # "Age in days out of plausible limits"
FLAG_FLAGGED_CASES = config.ANTHRO_FLAG_IMPLAUSIBLE   # 9998, "Flagged cases"
FLAG_DOCUMENTED_MISSING = config.ANTHRO_FLAG_MISSING  # 9999, "Missing" (documented; unused in practice)

SPECIAL_CODES = [FLAG_HEIGHT_IMPLAUSIBLE, FLAG_AGE_IMPLAUSIBLE,
                 FLAG_FLAGGED_CASES, FLAG_DOCUMENTED_MISSING]

SCALE = config.ANTHRO_SCALE_DIVISOR   # 100.0

# Bounds verified directly against the bundled DHS recode dictionaries
# (.map files) for all four surveys this session:
#   HW70 (HAZ): documented valid range -600:600  ->  -6.00 to  6.00
#   HW71 (WAZ): documented valid range -600:500  ->  -6.00 to  5.00
#   HW72 (WHZ): documented valid range -600:500  ->  -6.00 to  5.00
# (WHZ shares WAZ's documented range in DHS's own dictionary; this is
# not a typo - confirmed identical across Ethiopia, Ghana, Kenya, Nigeria.)
APPROVED_VALIDATION_BOUNDS = {
    "hw70": (-6.0, 6.0),   # HAZ
    "hw71": (-6.0, 5.0),   # WAZ
    "hw72": (-6.0, 5.0),   # WHZ (corrected from -5.0 to -6.0 this revision)
}

SCALED_NAMES = {"hw70": "haz", "hw71": "waz", "hw72": "whz"}


def validate_source_columns(meta, country, kr_path):
    """Hard-fail if any required column is missing from the source file."""
    available = {c.lower() for c in meta.column_names}
    missing = [c for c in REQUIRED_COLUMNS if c.lower() not in available]
    if missing:
        raise RuntimeError(
            f"[{country}] Required column(s) missing from {kr_path.name}: {missing}. "
            "Aborting before any read of observation data."
        )


def check_duplicate_identifiers(df, country):
    """
    Checks for duplicate child identifiers on (v001, v002, v003, bidx).
    Does NOT deduplicate. Raises if duplicates are found so a human
    reviews them before this script is allowed to write any output.
    """
    key_cols = ["v001", "v002", "v003", "bidx"]
    dup_mask = df.duplicated(subset=key_cols, keep=False)
    n_dup_rows = int(dup_mask.sum())
    if n_dup_rows > 0:
        dup_keys = df.loc[dup_mask, key_cols].drop_duplicates().to_dict("records")
        raise RuntimeError(
            f"[{country}] Found {n_dup_rows} rows sharing a duplicate "
            f"(v001, v002, v003, bidx) key. Duplicate keys: {dup_keys}. "
            "This script does not deduplicate automatically - review "
            "required before proceeding."
        )
    return n_dup_rows


def flag_and_scale(df, raw_var):
    """
    Given the raw DHS column (e.g. 'hw70'), explicitly distinguishes SIX
    mutually exclusive row categories - system-missing, each of the four
    documented DHS special codes (9996/9997/9998/9999), and valid - and
    returns:
      - raw       : untouched copy of the original column
      - flagcode  : the exact DHS code (9996/9997/9998/9999), or <NA> for
                    system-missing and valid rows alike
      - scaled    : raw / 100.0 for valid rows only; NaN for system-
                    missing and all four special codes (our analytical
                    treatment - see module docstring, layer 3)
      - counts    : dict with n_system_missing, n_flag_9996, n_flag_9997,
                    n_flag_9998, n_flag_9999, n_valid
      - masks     : dict of the six boolean masks, for validation
    """
    raw = df[raw_var].copy()

    mask_sys_missing = raw.isna()
    mask_9996 = raw == FLAG_HEIGHT_IMPLAUSIBLE
    mask_9997 = raw == FLAG_AGE_IMPLAUSIBLE
    mask_9998 = raw == FLAG_FLAGGED_CASES
    mask_9999 = raw == FLAG_DOCUMENTED_MISSING
    mask_valid = ~(mask_sys_missing | mask_9996 | mask_9997 | mask_9998 | mask_9999)

    flagcode = pd.Series(pd.NA, index=df.index, dtype="Int64")
    flagcode[mask_9996] = FLAG_HEIGHT_IMPLAUSIBLE
    flagcode[mask_9997] = FLAG_AGE_IMPLAUSIBLE
    flagcode[mask_9998] = FLAG_FLAGGED_CASES
    flagcode[mask_9999] = FLAG_DOCUMENTED_MISSING
    # mask_sys_missing and mask_valid rows keep flagcode = <NA>, by construction

    scaled = pd.Series(np.nan, index=df.index, dtype="float64")
    scaled.loc[mask_valid] = raw.loc[mask_valid].astype("float64") / SCALE
    # system-missing and all four special-code rows keep scaled = NaN

    masks = {
        "sys_missing": mask_sys_missing,
        9996: mask_9996,
        9997: mask_9997,
        9998: mask_9998,
        9999: mask_9999,
        "valid": mask_valid,
    }
    counts = {
        "n_system_missing": int(mask_sys_missing.sum()),
        "n_flag_9996": int(mask_9996.sum()),
        "n_flag_9997": int(mask_9997.sum()),
        "n_flag_9998": int(mask_9998.sum()),
        "n_flag_9999": int(mask_9999.sum()),
        "n_valid": int(mask_valid.sum()),
    }

    return raw, flagcode, scaled, counts, masks


def validate_flagging(raw, flagcode, scaled, masks, raw_var, country):
    """
    Explicit checks, one per documented special code, plus system-missing,
    plus valid-value arithmetic, plus a total-missingness reconciliation,
    plus the approved post-scaling plausible-range check.
    """
    # 1-4: for each of the four documented special codes, its rows must
    # carry that exact flagcode AND be NaN in the scaled column.
    for code in SPECIAL_CODES:
        mask_code = masks[code]
        if not (flagcode[mask_code] == code).all():
            raise RuntimeError(f"[{country}] {raw_var}: not all raw=={code} rows have flagcode {code}.")
        if not scaled[mask_code].isna().all():
            raise RuntimeError(f"[{country}] {raw_var}: not all raw=={code} rows have scaled NaN.")

    # 5. system-missing rows -> scaled NaN, flagcode NOT a sentinel
    mask_sys_missing = masks["sys_missing"]
    if not scaled[mask_sys_missing].isna().all():
        raise RuntimeError(f"[{country}] {raw_var}: not all system-missing rows have scaled NaN.")
    if flagcode[mask_sys_missing].notna().any():
        raise RuntimeError(
            f"[{country}] {raw_var}: system-missing rows must not carry a sentinel flagcode."
        )

    # 6. valid rows -> scaled == raw / 100 exactly (within float tolerance)
    mask_valid = masks["valid"]
    expected = raw[mask_valid].astype("float64") / SCALE
    actual = scaled[mask_valid]
    if actual.isna().any():
        raise RuntimeError(f"[{country}] {raw_var}: valid rows must not be NaN in scaled column.")
    if not np.allclose(actual.to_numpy(), expected.to_numpy(), atol=1e-9):
        raise RuntimeError(f"[{country}] {raw_var}: scaled values for valid rows do not equal raw/100.")

    # 7. no unexplained missingness beyond the five known causes
    expected_missing = int(
        mask_sys_missing.sum()
        + masks[9996].sum() + masks[9997].sum() + masks[9998].sum() + masks[9999].sum()
    )
    actual_missing = int(scaled.isna().sum())
    if expected_missing != actual_missing:
        raise RuntimeError(
            f"[{country}] {raw_var}: unexplained missingness detected - expected "
            f"{expected_missing} missing scaled values (system-missing + 9996 + 9997 "
            f"+ 9998 + 9999), found {actual_missing}."
        )

    # 8. approved plausible-range check on valid, non-missing values only.
    # This is a hard check that raises on violation - it never silently
    # alters or re-flags any additional observation.
    lo, hi = APPROVED_VALIDATION_BOUNDS[raw_var]
    out_of_range = actual[(actual < lo) | (actual > hi)]
    if len(out_of_range) > 0:
        raise RuntimeError(
            f"[{country}] {raw_var}: {len(out_of_range)} valid value(s) fall outside "
            f"the approved validation bounds [{lo}, {hi}] after scaling. This indicates "
            f"an unexpected raw code not covered by system-missing/9996/9997/9998/9999. "
            "Aborting rather than silently accepting."
        )


def validate_identifier_preservation(df_before, out_after, id_cols, country):
    """
    Exact check: identifier column VALUES and ROW ORDER must be identical
    between the just-read input and the constructed output.
    """
    before = df_before[id_cols].reset_index(drop=True)
    after = out_after[id_cols].reset_index(drop=True)
    if not before.equals(after):
        raise RuntimeError(
            f"[{country}] Identifier columns changed (values and/or row order) "
            "between the input read and the constructed output. Aborting."
        )


def run_country(country_key, info):
    """
    End-to-end Step 02 processing for one country: read the source KR file
    (selective columns only), validate identifiers, flag/scale the three
    anthropometric variables via flag_and_scale()/validate_flagging(), and
    write the staging parquet. Every validation step raises rather than
    silently repairing, so a failed run never produces a partial or
    silently-adjusted output file.
    """
    print(f"\n{'='*90}\n{info['survey_label']}\n{'='*90}")

    kr_path = info["kr_path"]
    if not kr_path.exists():
        raise FileNotFoundError(f"[{country_key}] KR source file not found: {kr_path}")

    # ---- PRE-READ VALIDATION: confirm required columns exist ----
    _, meta = pyreadstat.read_dta(str(kr_path), metadataonly=True)
    validate_source_columns(meta, country_key, kr_path)
    n_source_rows = meta.number_rows
    print(f"Source file confirmed: {kr_path.name}  (source row count per metadata: {n_source_rows})")

    # ---- READ (selective columns only, source file opened read-only) ----
    df, meta = pyreadstat.read_dta(str(kr_path), usecols=REQUIRED_COLUMNS)
    n_raw = len(df)

    if n_raw != n_source_rows:
        raise RuntimeError(
            f"[{country_key}] Row count mismatch: metadata reported "
            f"{n_source_rows}, selective read returned {n_raw}."
        )

    # ---- PRE-TRANSFORM VALIDATION: identifiers non-null ----
    for col in IDENTIFIER_VARS:
        n_null = df[col].isna().sum()
        if n_null > 0:
            raise RuntimeError(
                f"[{country_key}] Identifier column '{col}' has {n_null} "
                "null value(s) before any transformation. Aborting."
            )

    # ---- PRE-TRANSFORM VALIDATION: duplicate identifiers (hard fail, no dedup) ----
    check_duplicate_identifiers(df, country_key)
    print("Duplicate-identifier check: 0 duplicates found on (v001, v002, v003, bidx)")

    # ---- TRANSFORM: flag + scale each anthro variable ----
    out = df[IDENTIFIER_VARS + COMPANION_VARS].copy()
    out.insert(0, "country", country_key)
    out.insert(1, "survey_round", info["country_round"])

    header = f"{'Variable':<8}{'SysMiss':>10}{'9996':>8}{'9997':>8}{'9998':>8}{'9999':>8}{'Valid':>10}"
    print(f"\n{header}")
    for raw_var in ANTHRO_RAW_VARS:
        raw, flagcode, scaled, counts, masks = flag_and_scale(df, raw_var)

        validate_flagging(raw, flagcode, scaled, masks, raw_var, country_key)

        out[f"{raw_var}_raw"] = raw
        out[f"{raw_var}_flagcode"] = flagcode
        out[SCALED_NAMES[raw_var]] = scaled

        print(f"{raw_var:<8}{counts['n_system_missing']:>10}{counts['n_flag_9996']:>8}"
              f"{counts['n_flag_9997']:>8}{counts['n_flag_9998']:>8}{counts['n_flag_9999']:>8}"
              f"{counts['n_valid']:>10}")

    out["source_file"] = kr_path.name
    out["generated_at_utc"] = datetime.now(timezone.utc).isoformat()

    # ---- FINAL VALIDATION: row count ----
    if len(out) != n_raw:
        raise RuntimeError(
            f"[{country_key}] Output row count ({len(out)}) does not match "
            f"input row count ({n_raw})."
        )

    # ---- FINAL VALIDATION: exact identifier preservation (values + row order) ----
    validate_identifier_preservation(df, out, IDENTIFIER_VARS, country_key)
    print("Identifier preservation check: values and row order identical to source read")

    print(f"\nAll validation checks passed for {country_key}. "
          f"({len(out)} rows, {out.shape[1]} columns)")

    # ---- WRITE ----
    out_dir = info["staging_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "kr_anthro_flagged.parquet"
    out.to_parquet(out_path, index=False)
    print(f"Written: {out_path}")

    return out


if __name__ == "__main__":
    for country_key, info in config.COUNTRIES.items():
        run_country(country_key, info)
