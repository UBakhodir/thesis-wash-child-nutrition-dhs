"""
03_build_indicators.py
========================
Builds:
  (a) anthropometric outcome indicators (stunted/wasted/underweight, plus
      severe forms as secondary/robustness outcomes) from Step 02's
      flagged/scaled haz/waz/whz columns, and
  (b) harmonized WASH exposure variables (water category, sanitation
      category, Basic/Limited/Unimproved/OpenDefecation service level,
      collapsed Improved/NonImproved robustness variable, and the Ghana
      bio-digester robustness alternative) using ONLY the mappings
      already defined and approved in 01_wash_mapping.py.

Reads Step 02's kr_anthro_flagged.parquet (data/processed/staging/) plus
v113/v116/v160 read fresh (read-only) from the same source KR .dta files
used in Step 02. Never writes to data/raw/ or data/interim/.

No new WASH classification logic is invented here - every category and
every service-level propagation rule comes directly from
01_wash_mapping.py. Known WASH states (v113/v116=96/97, Ghana v116=16)
are represented with explicit descriptive labels rather than generic
None/NaN, and those labels propagate unchanged through the sanitation
service and collapsed variables per the approved specification.

No regression controls, weights, pooling, or geographic variables are
added in this script - that begins in 04_build_country_kr.py onward.
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
wash = _load_module("01_wash_mapping.py", "dhs_wash_mapping")

ID_COLS = ["v001", "v002", "v003", "bidx"]
WASH_RAW_VARS = ["v113", "v116", "v160"]

STUNTING_CUTOFF = config.STUNTING_CUTOFF        # -2.0
WASTING_CUTOFF = config.WASTING_CUTOFF          # -2.0
UNDERWEIGHT_CUTOFF = config.UNDERWEIGHT_CUTOFF  # -2.0
SEVERE_CUTOFF = config.SEVERE_CUTOFF            # -3.0

ANTHRO_INDICATOR_SPECS = [
    ("stunted", "haz", STUNTING_CUTOFF),
    ("wasted", "whz", WASTING_CUTOFF),
    ("underweight", "waz", UNDERWEIGHT_CUTOFF),
    ("severe_stunted", "haz", SEVERE_CUTOFF),
    ("severe_wasted", "whz", SEVERE_CUTOFF),
    ("severe_underweight", "waz", SEVERE_CUTOFF),
]


def build_binary_indicator(zscore, cutoff):
    """
    1 if zscore < cutoff, 0 if zscore >= cutoff, <NA> if zscore is NaN.
    No indicator is ever created for a missing z-score.
    """
    out = pd.Series(pd.NA, index=zscore.index, dtype="Int64")
    valid = zscore.notna()
    out[valid & (zscore < cutoff)] = 1
    out[valid & (zscore >= cutoff)] = 0
    return out


def map_wash_code(raw_series, mapping_dict, var_label, country):
    """
    Maps raw DHS codes to harmonized categories using ONLY the approved
    dictionary from 01_wash_mapping.py. Hard-fails if:
      - any raw value is system-missing (NaN) - not covered by any
        approved mapping entry for v113/v116 (confirmed 0 occurrences in
        all four countries by the read-only audit performed before this
        script was designed; retained as a safety net for future data), or
      - any raw value is a numeric code not present as a key in the
        approved mapping dictionary at all.
    Every code that IS in the dictionary - including 96, 97, and Ghana's
    16 - maps to an explicit descriptive label (see 01_wash_mapping.py),
    not a generic None. That is the approved, correct outcome, not an error.
    """
    if raw_series.isna().any():
        n_na = int(raw_series.isna().sum())
        raise RuntimeError(
            f"[{country}] {var_label}: {n_na} row(s) have system-missing raw "
            "values. This state is not covered by the approved WASH mapping "
            "and was not observed in the pre-design audit. Aborting rather "
            "than silently classifying them."
        )
    observed_codes = set(raw_series.unique())
    unmapped = sorted(c for c in observed_codes if c not in mapping_dict)
    if unmapped:
        raise RuntimeError(
            f"[{country}] {var_label}: observed raw code(s) {unmapped} are not "
            "present in the approved mapping (01_wash_mapping.py). Aborting "
            "rather than guessing a classification."
        )
    return raw_series.map(mapping_dict)


def build_sanitation_service(sanitation_category, v160_raw):
    """
    Applies wash.classify_sanitation_service() row-wise - the single
    approved source of truth for Basic/Limited/Unimproved/OpenDefecation
    and the explicit-state propagation rules. No reimplementation of that
    logic here.
    """
    return pd.Series(
        [wash.classify_sanitation_service(cat, v160)
         for cat, v160 in zip(sanitation_category, v160_raw)],
        index=sanitation_category.index,
    )


def print_value_counts(series, label, n_total):
    """Console-only reporting helper: prints one column's value counts
    (including missing) with percentages, for the post-construction audit
    tables below. Purely diagnostic output - writes nothing to disk and
    does not affect any validation decision."""
    print(f"\n  {label}:")
    vc = series.value_counts(dropna=False).sort_index(key=lambda x: x.astype(str))
    for val, freq in vc.items():
        display_val = "<missing>" if pd.isna(val) else val
        pct = 100 * freq / n_total
        print(f"    {str(display_val):<28} {freq:>8}  ({pct:5.2f}%)")


def print_audit_tables(merged, country_key):
    """Prints the post-construction distribution of every anthropometric
    indicator and WASH category, plus the WASH edge-case counts (Unknown,
    StructuralNotApplicable, Ghana bio-digester, the v116==31 structural
    skip pattern) called out explicitly so a reviewer can see at a glance
    that the explicit-state counts look as expected for this country,
    without having to reopen the output parquet."""
    n_total = len(merged)
    print(f"\n{'-'*70}\nPOST-CONSTRUCTION AUDIT TABLES - {country_key}\n{'-'*70}")

    for ind_col, _, _ in ANTHRO_INDICATOR_SPECS:
        print_value_counts(merged[ind_col], ind_col, n_total)

    for col in ["water_category", "sanitation_category_core",
                "sanitation_service_core", "sanitation_collapsed_core"]:
        print_value_counts(merged[col], col, n_total)

    print("\n  Separate WASH edge-case counts:")
    print(f"    v113==96 (Unknown):                        {(merged['v113_raw']==96).sum()}")
    print(f"    v113==97 (StructuralNotApplicable):         {(merged['v113_raw']==97).sum()}")
    print(f"    v116==96 (Unknown):                        {(merged['v116_raw']==96).sum()}")
    print(f"    v116==97 (StructuralNotApplicable):         {(merged['v116_raw']==97).sum()}")
    print(f"    v116==16 (Ghana bio-digester):               {(merged['v116_raw']==16).sum()}")
    v116_31 = merged["v116_raw"] == 31
    print(f"    v116==31 with v160 system-missing:          {(v116_31 & merged['v160_raw'].isna()).sum()}")
    unexpected_v160 = merged["v160_raw"].isna() & ~v116_31
    print(f"    v160 missing OUTSIDE v116==31 (unexpected):  {unexpected_v160.sum()}")


def run_country(country_key, info):
    """
    End-to-end Step 03 processing for one country: load Step 02's flagged
    anthropometry, build the binary stunting/wasting/underweight (and
    severe) indicators, re-read v113/v116/v160 fresh from the source KR
    file and build the WASH categories using ONLY the approved
    01_wash_mapping.py dictionaries, run the full explicit-state and
    propagation-rule validation, then write the indicators parquet.
    """
    print(f"\n{'='*90}\n{info['survey_label']}\n{'='*90}")

    # ---- Load Step 02 output (identifiers + anthro) ----
    step02_path = info["staging_dir"] / "kr_anthro_flagged.parquet"
    if not step02_path.exists():
        raise FileNotFoundError(f"[{country_key}] Step 02 output not found: {step02_path}")
    anthro_df = pd.read_parquet(step02_path)
    n_step02 = len(anthro_df)
    print(f"Loaded Step 02 output: {step02_path.name} ({n_step02} rows)")

    # ---- Read WASH raw columns fresh from the source KR .dta (read-only) ----
    kr_path = info["kr_path"]
    wash_df, meta = pyreadstat.read_dta(str(kr_path), usecols=ID_COLS + WASH_RAW_VARS)

    # ---- PRE-MERGE VALIDATION: duplicate-key guarantee (defense in depth) ----
    dup_mask = wash_df.duplicated(subset=ID_COLS, keep=False)
    if dup_mask.any():
        raise RuntimeError(
            f"[{country_key}] Duplicate identifier keys found while re-reading "
            "WASH columns - should be impossible given Step 02 already "
            "validated uniqueness on the same source file. Aborting."
        )

    # ---- MERGE anthro (Step 02) with WASH raw columns on identifier keys ----
    merged = anthro_df.merge(
        wash_df, on=ID_COLS, how="left", validate="one_to_one", indicator=True
    )
    if len(merged) != n_step02:
        raise RuntimeError(
            f"[{country_key}] Merge with WASH columns changed row count: "
            f"{n_step02} -> {len(merged)}. Aborting."
        )
    if not (merged["_merge"] == "both").all():
        n_unmatched = int((merged["_merge"] != "both").sum())
        raise RuntimeError(
            f"[{country_key}] {n_unmatched} Step 02 row(s) had no matching WASH "
            "row when re-reading the source KR file - should be impossible "
            "since both reads come from the same file. Aborting."
        )
    merged = merged.drop(columns="_merge")

    # ---- IDENTIFIER PRESERVATION CHECK vs Step 02 ----
    before = anthro_df[ID_COLS].reset_index(drop=True)
    after = merged[ID_COLS].reset_index(drop=True)
    if not before.equals(after):
        raise RuntimeError(
            f"[{country_key}] Identifier values/order changed relative to "
            "Step 02 output after merging WASH columns. Aborting."
        )
    print("Identifier preservation check (vs Step 02): values and row order identical")

    merged = merged.rename(columns={"v113": "v113_raw", "v116": "v116_raw", "v160": "v160_raw"})

    # ====================================================================
    # ANTHROPOMETRIC INDICATORS
    # ====================================================================
    for ind_col, z_col, cutoff in ANTHRO_INDICATOR_SPECS:
        merged[ind_col] = build_binary_indicator(merged[z_col], cutoff)

    # ---- VALIDATION: binary indicators only 0/1/<NA> ----
    for ind_col, _, _ in ANTHRO_INDICATOR_SPECS:
        vals = merged[ind_col].dropna()
        if not vals.isin([0, 1]).all():
            raise RuntimeError(f"[{country_key}] {ind_col} contains a value other than 0/1/missing.")

    # ---- VALIDATION: severe==1 implies standard==1 ----
    pairs = [("severe_stunted", "stunted"), ("severe_wasted", "wasted"), ("severe_underweight", "underweight")]
    for severe_col, std_col in pairs:
        violation = (merged[severe_col] == 1) & (merged[std_col] != 1)
        if violation.any():
            raise RuntimeError(
                f"[{country_key}] {int(violation.sum())} row(s) have {severe_col}=1 "
                f"but {std_col}!=1 - severe outcome must imply the standard outcome."
            )

    # ---- VALIDATION: no indicator created for a missing z-score ----
    for ind_col, z_col, _ in ANTHRO_INDICATOR_SPECS:
        mismatch = merged[z_col].isna() != merged[ind_col].isna()
        if mismatch.any():
            raise RuntimeError(
                f"[{country_key}] {ind_col} missingness does not exactly match "
                f"{z_col} missingness ({int(mismatch.sum())} mismatched row(s))."
            )

    # ---- VALIDATION: indicators mathematically identical to direct
    # recomputation from the preserved z-score columns ----
    for ind_col, z_col, cutoff in ANTHRO_INDICATOR_SPECS:
        recomputed = build_binary_indicator(merged[z_col], cutoff)
        both_na = merged[ind_col].isna() & recomputed.isna()
        mismatch = (merged[ind_col] != recomputed) & ~both_na
        if mismatch.any():
            raise RuntimeError(
                f"[{country_key}] {ind_col} does not match direct recomputation "
                f"from {z_col} using cutoff {cutoff} ({int(mismatch.sum())} "
                "mismatched row(s))."
            )

    print("Anthropometric indicator validation: passed "
          "(binary domain, severe<=standard, missingness alignment, "
          "recomputation-from-zscore identity)")

    # ====================================================================
    # WASH INDICATORS - built ONLY from 01_wash_mapping.py's approved dicts
    # ====================================================================
    merged["water_category"] = map_wash_code(
        merged["v113_raw"], wash.WATER_CATEGORY_MAP, "v113 (drinking water)", country_key
    )
    merged["sanitation_category_core"] = map_wash_code(
        merged["v116_raw"], wash.SANITATION_CATEGORY_MAP_CORE, "v116 (sanitation, core)", country_key
    )
    merged["sanitation_category_robustness_biodigester"] = map_wash_code(
        merged["v116_raw"], wash.SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER,
        "v116 (sanitation, bio-digester robustness)", country_key
    )

    merged["sanitation_service_core"] = build_sanitation_service(
        merged["sanitation_category_core"], merged["v160_raw"]
    )
    merged["sanitation_service_robustness_biodigester"] = build_sanitation_service(
        merged["sanitation_category_robustness_biodigester"], merged["v160_raw"]
    )

    merged["sanitation_collapsed_core"] = merged["sanitation_service_core"].map(
        wash.SANITATION_SERVICE_COLLAPSE_MAP
    )
    merged["sanitation_collapsed_robustness_biodigester"] = merged["sanitation_service_robustness_biodigester"].map(
        wash.SANITATION_SERVICE_COLLAPSE_MAP
    )

    # ---- VALIDATION: Ghana bio-digester treatment exactly as approved ----
    is_code16 = merged["v116_raw"] == 16
    if country_key == "ghana":
        if is_code16.any():
            if not (merged.loc[is_code16, "sanitation_category_core"] == "UnclassifiedBioDigester").all():
                raise RuntimeError(
                    f"[{country_key}] v116=16 rows must be 'UnclassifiedBioDigester' "
                    "in the core sanitation category."
                )
            if not (merged.loc[is_code16, "sanitation_category_robustness_biodigester"] == "Improved").all():
                raise RuntimeError(
                    f"[{country_key}] v116=16 rows must be 'Improved' in the "
                    "bio-digester robustness sanitation category."
                )
    else:
        if is_code16.any():
            raise RuntimeError(
                f"[{country_key}] v116=16 (Ghana-only bio-digester code) "
                "observed in a non-Ghana country - unexpected. Aborting."
            )

    # Core and robustness categories must be identical everywhere except code-16 rows
    diff_mask = merged["sanitation_category_core"] != merged["sanitation_category_robustness_biodigester"]
    if not diff_mask.equals(is_code16):
        raise RuntimeError(
            f"[{country_key}] Core and robustness sanitation categories differ "
            "on rows other than v116=16 - the robustness mapping must only "
            "override code 16, per the approved specification."
        )

    # ---- VALIDATION: exact service-level propagation rules ----
    identity_categories = ["Unimproved", "OpenDefecation", "Unknown",
                            "StructuralNotApplicable", "UnclassifiedBioDigester"]
    for cat in identity_categories:
        mask = merged["sanitation_category_core"] == cat
        if mask.any() and not (merged.loc[mask, "sanitation_service_core"] == cat).all():
            raise RuntimeError(
                f"[{country_key}] Rows with sanitation_category_core=='{cat}' must "
                f"propagate to sanitation_service_core=='{cat}' unchanged, regardless "
                "of v160. Aborting."
            )

    mask_improved_shared0 = (merged["sanitation_category_core"] == "Improved") & (merged["v160_raw"] == 0)
    if mask_improved_shared0.any() and not (merged.loc[mask_improved_shared0, "sanitation_service_core"] == "Basic").all():
        raise RuntimeError(f"[{country_key}] Improved + v160=0 rows must resolve to 'Basic'.")

    mask_improved_shared1 = (merged["sanitation_category_core"] == "Improved") & (merged["v160_raw"] == 1)
    if mask_improved_shared1.any() and not (merged.loc[mask_improved_shared1, "sanitation_service_core"] == "Limited").all():
        raise RuntimeError(f"[{country_key}] Improved + v160=1 rows must resolve to 'Limited'.")

    # ---- VALIDATION: collapsed mapping matches the approved table exactly ----
    expected_collapse = {
        "Basic": "Improved", "Limited": "Improved",
        "Unimproved": "NonImproved", "OpenDefecation": "NonImproved",
        "Unknown": "Unknown", "StructuralNotApplicable": "StructuralNotApplicable",
        "UnclassifiedBioDigester": "UnclassifiedBioDigester",
    }
    for service_val, expected_collapsed_val in expected_collapse.items():
        mask = merged["sanitation_service_core"] == service_val
        if mask.any() and not (merged.loc[mask, "sanitation_collapsed_core"] == expected_collapsed_val).all():
            raise RuntimeError(
                f"[{country_key}] sanitation_service_core=='{service_val}' must collapse "
                f"to '{expected_collapsed_val}' in sanitation_collapsed_core."
            )

    # ---- VALIDATION: Ghana bio-digester robustness rows use NORMAL
    # Improved-branch v160 logic, not the UnclassifiedBioDigester identity path ----
    if is_code16.any():
        bad = merged.loc[is_code16, "sanitation_service_robustness_biodigester"] == "UnclassifiedBioDigester"
        if bad.any():
            raise RuntimeError(
                f"[{country_key}] v116=16 rows in the robustness variant must be "
                "resolved via the normal Improved/v160 logic (Basic/Limited/"
                "StructuralNotApplicable), not the UnclassifiedBioDigester identity path."
            )

    # ---- VALIDATION: no v160 missingness outside the approved structural
    # skip pattern (v116==31) ----
    v116_is_31 = merged["v116_raw"] == 31
    unexpected_v160_missing = merged["v160_raw"].isna() & ~v116_is_31
    if unexpected_v160_missing.any():
        raise RuntimeError(
            f"[{country_key}] {int(unexpected_v160_missing.sum())} row(s) have "
            "v160 system-missing outside the approved structural skip pattern "
            "(v116==31). Aborting rather than silently treating this as "
            "ordinary missingness."
        )

    print("WASH indicator validation: passed "
          "(unmapped-code hard-fail, Ghana bio-digester, explicit-state "
          "propagation, collapsed-mapping correctness, v160 structural-"
          "missingness scope)")

    # ====================================================================
    # FINAL VALIDATION: row count vs Step 02
    # ====================================================================
    if len(merged) != n_step02:
        raise RuntimeError(
            f"[{country_key}] Final row count ({len(merged)}) does not match "
            f"Step 02 row count ({n_step02})."
        )

    # ====================================================================
    # POST-CONSTRUCTION AUDIT TABLES
    # ====================================================================
    print_audit_tables(merged, country_key)

    merged["generated_at_utc_step03"] = datetime.now(timezone.utc).isoformat()

    print(f"\nAll validation checks passed for {country_key}. "
          f"({len(merged)} rows, {merged.shape[1]} columns)")

    # ---- WRITE ----
    out_path = info["staging_dir"] / "kr_indicators.parquet"
    merged.to_parquet(out_path, index=False)
    print(f"Written: {out_path}")

    return merged


if __name__ == "__main__":
    for country_key, info in config.COUNTRIES.items():
        run_country(country_key, info)
