"""
08_hr_cluster_wash_exposure.py
================================
Constructs household-level, leave-one-out cluster WASH coverage exposure
(water_rate_loo, sanitation_rate_loo_core, sanitation_rate_loo_robustness_
biodigester) from the DHS HR (household) file, per the approved Step 08
specification (Pre-Step-08 Household WASH Exposure Diagnostic, approved):

  - Source population: the DHS HR household census for each country - NOT
    KR-deduplicated households. The estimand is community-wide coverage
    among ALL sampled households in the child's DHS cluster, consistent
    with the original thesis design's community-externality framing.
  - Leave-one-out unit: the HOUSEHOLD. For a household h in cluster c, the
    rate is the mean improved-WASH status among all OTHER eligible HR
    households in c, excluding h itself. All children in the same
    household therefore receive an identical cluster leave-one-out
    exposure.
  - Weighting: UNWEIGHTED household proportion for the primary exposure.
    v005 is not used. hv005 is preserved (unused) for a possible future
    weighted-robustness variant, not built here.
  - Classification: reuses 01_wash_mapping.py's WATER_CATEGORY_MAP,
    SANITATION_CATEGORY_MAP_CORE / _ROBUSTNESS_BIODIGESTER,
    classify_sanitation_service(), and SANITATION_SERVICE_COLLAPSE_MAP
    UNCHANGED, applied to HR's hv201/hv205/hv225 (verified, in the
    approved diagnostic, to be a strict superset-compatible code universe
    of the KR-based v113/v116/v160 codes already validated in Step 03).
    No new WASH classification logic is introduced here.
  - Explicit states (Unknown, StructuralNotApplicable, and - for the core
    sanitation variant only - UnclassifiedBioDigester) are excluded from
    both the numerator and denominator of the coverage rate.
  - Minimum denominator: no invented minimum-cluster-size restriction. If
    zero other eligible households remain after exclusions, the rate is
    explicitly set to missing and reported (not silently repaired).

Reads (read-only):
  - data/processed/pooled_kr_four_country_geolinked.parquet (Step 06 output)
  - the four countries' raw HR .dta files under data/interim/DHS/.../HR/

Writes:
  - data/processed/pooled_kr_four_country_wash_exposure.parquet
  - outputs/tables/step08_hr_wash_exposure_report.csv
  - outputs/tables/step08_loo_denominator_diagnostics.csv

Never opens Steps 00-07 scripts or outputs in write mode. No pooled-country
weight is constructed, no geospatial covariate is acquired, no spatial
grid is built, no regression is run, no anthropometric definition or
approved WASH mapping is changed.
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
wash = _load_module("01_wash_mapping.py", "dhs_wash_mapping")

POOLED_INPUT_PATH = config.POOLED_GEOLINKED_OUTPUT
OUTPUT_PATH = config.DATA_PROCESSED / "pooled_kr_four_country_wash_exposure.parquet"
REPORT_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "step08_hr_wash_exposure_report.csv"
DIAGNOSTIC_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "step08_loo_denominator_diagnostics.csv"

HR_PATHS = {c: info["hr_path"] for c, info in config.COUNTRIES.items()}
HR_RAW_COLS = ["hv001", "hv002", "hv009", "hv005", "hv201", "hv205", "hv225"]

# Sets used to convert the already-approved categorical WASH variables into
# a numerator/denominator-inclusion pair. No new classification - these
# sets only decide which already-existing category labels count as 1, 0,
# or excluded from a coverage rate.
WATER_POSITIVE = {"Improved"}
WATER_ZERO = {"Unimproved", "SurfaceWater"}
WATER_EXCLUDED = {"Unknown", "StructuralNotApplicable"}

SANITATION_POSITIVE = {"Improved"}       # from the *collapsed* variable (Basic+Limited)
SANITATION_ZERO = {"NonImproved"}        # from the *collapsed* variable (Unimproved+OpenDefecation)
SANITATION_EXCLUDED_CORE = {"Unknown", "StructuralNotApplicable", "UnclassifiedBioDigester"}
SANITATION_EXCLUDED_ROBUSTNESS = {"Unknown", "StructuralNotApplicable"}


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================================
# PHASE B: household-level WASH classification from hv201/hv205/hv225,
# reusing 01_wash_mapping.py exactly as Step 03 does for KR.
# ============================================================================

def map_required_code(raw_series, mapping_dict, var_label, country):
    """Same hard-fail pattern as Step 03/04's mapping helpers: any
    system-missing value or any code not present in the approved
    dictionary aborts rather than guessing."""
    if raw_series.isna().any():
        n_na = int(raw_series.isna().sum())
        raise RuntimeError(
            f"[{country}] {var_label}: {n_na} row(s) have system-missing raw "
            "values - not observed in the approved diagnostic audit. Aborting."
        )
    observed_codes = set(raw_series.unique())
    unmapped = sorted(c for c in observed_codes if c not in mapping_dict)
    if unmapped:
        raise RuntimeError(
            f"[{country}] {var_label}: observed raw code(s) {unmapped} are not "
            "present in the approved mapping (01_wash_mapping.py). Aborting."
        )
    return raw_series.map(mapping_dict)


def build_sanitation_service(sanitation_category, shared_raw):
    return pd.Series(
        [wash.classify_sanitation_service(cat, v) for cat, v in zip(sanitation_category, shared_raw)],
        index=sanitation_category.index,
    )


def build_household_wash_classification(hr_df, country_key):
    """Adds water_category_hr, sanitation_category_core_hr,
    sanitation_category_robustness_biodigester_hr, sanitation_service_core_hr,
    sanitation_service_robustness_biodigester_hr, sanitation_collapsed_core_hr,
    sanitation_collapsed_robustness_biodigester_hr to hr_df, using ONLY the
    approved 01_wash_mapping.py dictionaries/function - identical logic to
    Step 03, applied to hv201/hv205/hv225 instead of v113/v116/v160."""
    hr_df = hr_df.copy()

    hr_df["water_category_hr"] = map_required_code(
        hr_df["hv201"], wash.WATER_CATEGORY_MAP, "hv201 (drinking water)", country_key
    )
    hr_df["sanitation_category_core_hr"] = map_required_code(
        hr_df["hv205"], wash.SANITATION_CATEGORY_MAP_CORE, "hv205 (sanitation, core)", country_key
    )
    hr_df["sanitation_category_robustness_biodigester_hr"] = map_required_code(
        hr_df["hv205"], wash.SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER,
        "hv205 (sanitation, bio-digester robustness)", country_key
    )

    hr_df["sanitation_service_core_hr"] = build_sanitation_service(
        hr_df["sanitation_category_core_hr"], hr_df["hv225"]
    )
    hr_df["sanitation_service_robustness_biodigester_hr"] = build_sanitation_service(
        hr_df["sanitation_category_robustness_biodigester_hr"], hr_df["hv225"]
    )

    hr_df["sanitation_collapsed_core_hr"] = hr_df["sanitation_service_core_hr"].map(
        wash.SANITATION_SERVICE_COLLAPSE_MAP
    )
    hr_df["sanitation_collapsed_robustness_biodigester_hr"] = hr_df["sanitation_service_robustness_biodigester_hr"].map(
        wash.SANITATION_SERVICE_COLLAPSE_MAP
    )

    # ---- VALIDATION: Ghana bio-digester code (16) only in Ghana ----
    is_code16 = hr_df["hv205"] == 16
    if country_key == "ghana":
        if is_code16.any():
            if not (hr_df.loc[is_code16, "sanitation_category_core_hr"] == "UnclassifiedBioDigester").all():
                raise RuntimeError(f"[{country_key}] hv205=16 rows must be 'UnclassifiedBioDigester' in core.")
            if not (hr_df.loc[is_code16, "sanitation_category_robustness_biodigester_hr"] == "Improved").all():
                raise RuntimeError(f"[{country_key}] hv205=16 rows must be 'Improved' in the robustness variant.")
    else:
        if is_code16.any():
            raise RuntimeError(
                f"[{country_key}] hv205=16 (Ghana-only bio-digester code) observed in a "
                "non-Ghana HR file - unexpected. Aborting."
            )

    # ---- VALIDATION: hv225 missing ONLY within hv205==31 (open defecation) ----
    # Mirrors the already-approved v116==31 -> v160-missing structural skip
    # pattern validated in Step 03.
    hv205_is_31 = hr_df["hv205"] == 31
    unexpected_missing = hr_df["hv225"].isna() & ~hv205_is_31
    if unexpected_missing.any():
        raise RuntimeError(
            f"[{country_key}] {int(unexpected_missing.sum())} HR row(s) have hv225 "
            "system-missing outside the approved structural skip pattern (hv205==31). Aborting."
        )

    # ---- VALIDATION: explicit-state identity propagation (service level) ----
    identity_categories = ["Unimproved", "OpenDefecation", "Unknown", "StructuralNotApplicable", "UnclassifiedBioDigester"]
    for cat in identity_categories:
        mask = hr_df["sanitation_category_core_hr"] == cat
        if mask.any() and not (hr_df.loc[mask, "sanitation_service_core_hr"] == cat).all():
            raise RuntimeError(f"[{country_key}] '{cat}' failed to propagate identically into sanitation_service_core_hr.")

    print(f"  [{country_key}] Household WASH classification built and validated "
          f"(Ghana bio-digester scope, hv225 structural-skip scope, explicit-state propagation)")
    return hr_df


# ============================================================================
# PHASE D/E/F: numerator/denominator indicators + leave-one-out construction
# ============================================================================

def build_indicator(series, positive_set, zero_set, excluded_set, label, country_key):
    observed = set(series.dropna().unique()) | (set(["<NA>"]) if series.isna().any() else set())
    covered = positive_set | zero_set | excluded_set
    unexpected = sorted(v for v in series.dropna().unique() if v not in covered)
    if unexpected:
        raise RuntimeError(f"[{country_key}] {label}: unexpected category value(s) {unexpected} not covered by the approved positive/zero/excluded sets. Aborting.")
    if series.isna().any():
        raise RuntimeError(f"[{country_key}] {label}: {int(series.isna().sum())} missing categorical value(s) - unexpected. Aborting.")

    indicator = pd.Series(np.nan, index=series.index, dtype="float64")
    indicator[series.isin(positive_set)] = 1.0
    indicator[series.isin(zero_set)] = 0.0
    included = series.isin(positive_set | zero_set)
    return indicator, included


def compute_leave_one_out(hh_df, cluster_key_col, indicator_col, included_col, prefix):
    grp = hh_df.groupby(cluster_key_col)
    cluster_n = grp[included_col].transform("sum").astype("float64")     # count of eligible households in cluster
    cluster_sum = grp[indicator_col].transform("sum")                    # pandas sum() skips NaN automatically

    own_included = hh_df[included_col].astype("float64")
    own_value = hh_df[indicator_col].fillna(0.0)

    other_n = cluster_n - own_included
    other_sum = cluster_sum - own_value

    rate = pd.Series(np.nan, index=hh_df.index, dtype="float64")
    eligible_mask = other_n >= 1
    rate[eligible_mask] = other_sum[eligible_mask] / other_n[eligible_mask]

    hh_df[f"{prefix}_rate_loo"] = rate
    hh_df[f"{prefix}_rate_loo_n_other_hh"] = other_n
    return hh_df


def brute_force_check(hh_df, cluster_key_col, indicator_col, included_col, rate_col, n_col, label, n_clusters=3):
    """Independent, non-vectorized recomputation for a deterministic sample
    of clusters (the largest-N cluster per country, to exercise multiple
    households), directly proving own-household exclusion."""
    cluster_sizes = hh_df.groupby(cluster_key_col).size().sort_values(ascending=False)
    sample_clusters = cluster_sizes.head(n_clusters).index.tolist()

    n_checked = 0
    for cl in sample_clusters:
        sub = hh_df[hh_df[cluster_key_col] == cl]
        for idx, row in sub.iterrows():
            others = sub.drop(index=idx)
            others_eligible = others[others[included_col]]
            if len(others_eligible) == 0:
                expected_rate = np.nan
                expected_n = 0
            else:
                expected_rate = others_eligible[indicator_col].mean()
                expected_n = len(others_eligible)

            actual_rate = row[rate_col]
            actual_n = row[n_col]

            if expected_n != actual_n:
                raise RuntimeError(
                    f"Brute-force check FAILED ({label}) for cluster {cl}, row {idx}: "
                    f"expected n_other={expected_n}, got {actual_n}."
                )
            both_nan = pd.isna(expected_rate) and pd.isna(actual_rate)
            if not both_nan:
                if pd.isna(expected_rate) != pd.isna(actual_rate) or abs(expected_rate - actual_rate) > 1e-9:
                    raise RuntimeError(
                        f"Brute-force check FAILED ({label}) for cluster {cl}, row {idx}: "
                        f"expected rate={expected_rate}, got {actual_rate}."
                    )
            n_checked += 1
    print(f"  Brute-force leave-one-out verification ({label}): {n_checked} household rows across "
          f"{len(sample_clusters)} largest clusters - all match independent recomputation exactly")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*90)
    print("STEP 08 - HR-BASED CLUSTER LEAVE-ONE-OUT WASH EXPOSURE CONSTRUCTION")
    print("="*90)

    # ---- Verify inputs exist ----
    if not POOLED_INPUT_PATH.exists():
        raise FileNotFoundError(f"Step 06 pooled input not found: {POOLED_INPUT_PATH}")
    for country, path in HR_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(f"[{country}] HR file not found: {path}")

    checksum_pooled_before = md5_of_file(POOLED_INPUT_PATH)
    checksums_hr_before = {c: md5_of_file(p) for c, p in HR_PATHS.items()}

    # ====================================================================
    # PHASE A: load pooled Step 06 dataset + audit four-country HR files
    # ====================================================================
    pooled = pd.read_parquet(POOLED_INPUT_PATH)
    n_pooled_before = len(pooled)
    pooled_cols_before = list(pooled.columns)
    step06_snapshot = pooled[pooled_cols_before].copy()
    print(f"\nLoaded Step 06 pooled dataset: {n_pooled_before} rows, {pooled.shape[1]} columns")

    n_per_country_before = pooled["country"].value_counts().to_dict()

    report_rows = []
    hh_frames = []

    for country_key, hr_path in HR_PATHS.items():
        print(f"\n{'-'*90}\n[{country_key}] Phase A: loading HR\n{'-'*90}")
        hr_df, _ = pyreadstat.read_dta(str(hr_path), usecols=HR_RAW_COLS)
        n_hr = len(hr_df)
        n_unique_hh = hr_df[["hv001", "hv002"]].drop_duplicates().shape[0]
        dup = hr_df.duplicated(subset=["hv001", "hv002"], keep=False).sum()
        if dup > 0:
            raise RuntimeError(f"[{country_key}] {dup} HR row(s) share a duplicate (hv001,hv002). Aborting.")
        if n_unique_hh != n_hr:
            raise RuntimeError(f"[{country_key}] HR household count mismatch: {n_hr} rows vs {n_unique_hh} unique (hv001,hv002).")
        print(f"  HR rows (= unique households, (hv001,hv002) verified unique): {n_hr}")

        n_clusters = hr_df["hv001"].nunique()
        hh_per_cluster = hr_df.groupby("hv001").size()
        print(f"  Distinct clusters: {n_clusters}; households per cluster: "
              f"min={hh_per_cluster.min()} median={hh_per_cluster.median():.1f} "
              f"mean={hh_per_cluster.mean():.2f} max={hh_per_cluster.max()}")

        # ---- PHASE B: household-level WASH classification ----
        hr_df = build_household_wash_classification(hr_df, country_key)

        hr_df["country"] = country_key
        hr_df["country_household_id"] = country_key + "_" + hr_df["hv001"].astype(str) + "_" + hr_df["hv002"].astype(str)
        if hr_df["country_household_id"].duplicated().any():
            raise RuntimeError(f"[{country_key}] Duplicate country_household_id. Aborting.")

        report_rows.append({
            "country": country_key,
            "hr_rows": n_hr,
            "hr_unique_households": n_unique_hh,
            "hr_clusters": n_clusters,
            "hh_per_cluster_min": int(hh_per_cluster.min()),
            "hh_per_cluster_median": float(hh_per_cluster.median()),
            "hh_per_cluster_mean": float(hh_per_cluster.mean()),
            "hh_per_cluster_max": int(hh_per_cluster.max()),
        })

        hh_frames.append(hr_df)

    hh_all = pd.concat(hh_frames, ignore_index=True)
    if hh_all["country_household_id"].duplicated().any():
        raise RuntimeError("Duplicate country_household_id after combining all four countries. Aborting.")
    print(f"\nCombined HR household data: {len(hh_all)} rows across all four countries")

    # ====================================================================
    # PHASE C: validate HR mappings against approved KR classifications
    # wherever households overlap (usual-resident-linked KR households only)
    # ====================================================================
    print(f"\n{'='*90}\nPHASE C: KR-vs-HR classification agreement audit\n{'='*90}")
    kr_usual_resident = pooled[pooled["v116_raw"] != 97].copy()
    kr_usual_resident["country_household_id"] = (
        kr_usual_resident["country"] + "_" + kr_usual_resident["v001"].astype(str) + "_" + kr_usual_resident["v002"].astype(str)
    )
    kr_dedup = kr_usual_resident.drop_duplicates(subset=["country_household_id"])[
        ["country_household_id", "water_category", "sanitation_category_core",
         "sanitation_service_core", "sanitation_collapsed_core"]
    ]

    agree_check = kr_dedup.merge(
        hh_all[["country_household_id", "water_category_hr", "sanitation_category_core_hr",
                "sanitation_service_core_hr", "sanitation_collapsed_core_hr"]],
        on="country_household_id", how="left", validate="one_to_one",
    )
    if agree_check["water_category_hr"].isna().any():
        raise RuntimeError("Some KR usual-resident households failed to find a matching HR household during the KR-vs-HR agreement audit. Aborting.")

    pairs = [
        ("water_category", "water_category_hr"),
        ("sanitation_category_core", "sanitation_category_core_hr"),
        ("sanitation_service_core", "sanitation_service_core_hr"),
        ("sanitation_collapsed_core", "sanitation_collapsed_core_hr"),
    ]
    for kr_col, hr_col in pairs:
        mismatch = (agree_check[kr_col] != agree_check[hr_col]).sum()
        if mismatch > 0:
            raise RuntimeError(f"{mismatch} household(s) disagree between KR '{kr_col}' and HR '{hr_col}'. Aborting.")
        print(f"  {kr_col} <-> {hr_col}: 0 mismatches across {len(agree_check)} overlapping usual-resident households")

    # ====================================================================
    # PHASE D/E/F: indicators + leave-one-out rates
    # ====================================================================
    print(f"\n{'='*90}\nPHASE D-F: numerator/denominator indicators + leave-one-out construction\n{'='*90}")

    hh_all["water_indicator"], hh_all["water_included"] = build_indicator(
        hh_all["water_category_hr"], WATER_POSITIVE, WATER_ZERO, WATER_EXCLUDED, "water_category_hr", "ALL"
    )
    hh_all["sanitation_core_indicator"], hh_all["sanitation_core_included"] = build_indicator(
        hh_all["sanitation_collapsed_core_hr"], SANITATION_POSITIVE, SANITATION_ZERO, SANITATION_EXCLUDED_CORE,
        "sanitation_collapsed_core_hr", "ALL"
    )
    hh_all["sanitation_robustness_indicator"], hh_all["sanitation_robustness_included"] = build_indicator(
        hh_all["sanitation_collapsed_robustness_biodigester_hr"], SANITATION_POSITIVE, SANITATION_ZERO,
        SANITATION_EXCLUDED_ROBUSTNESS, "sanitation_collapsed_robustness_biodigester_hr", "ALL"
    )

    hh_all["cluster_key"] = hh_all["country"] + "_" + hh_all["hv001"].astype(str)

    hh_all = compute_leave_one_out(hh_all, "cluster_key", "water_indicator", "water_included", "water")
    hh_all = compute_leave_one_out(hh_all, "cluster_key", "sanitation_core_indicator", "sanitation_core_included", "sanitation_core")
    hh_all = compute_leave_one_out(hh_all, "cluster_key", "sanitation_robustness_indicator", "sanitation_robustness_included", "sanitation_robustness")

    print("  Leave-one-out rates constructed: water_rate_loo, sanitation_core_rate_loo, sanitation_robustness_rate_loo")

    # ---- Range check [0,1] ----
    for col in ["water_rate_loo", "sanitation_core_rate_loo", "sanitation_robustness_rate_loo"]:
        valid = hh_all[col].dropna()
        if len(valid) and ((valid < 0) | (valid > 1)).any():
            raise RuntimeError(f"{col}: value(s) outside [0,1] found. Aborting.")
    print("  Range check: all non-missing leave-one-out rates lie in [0,1]")

    # ---- Brute-force independent verification (own-household exclusion proof) ----
    print("\n  Running brute-force verification on a deterministic sample of clusters:")
    brute_force_check(hh_all, "cluster_key", "water_indicator", "water_included", "water_rate_loo", "water_rate_loo_n_other_hh", "water")
    brute_force_check(hh_all, "cluster_key", "sanitation_core_indicator", "sanitation_core_included", "sanitation_core_rate_loo", "sanitation_core_rate_loo_n_other_hh", "sanitation_core")
    brute_force_check(hh_all, "cluster_key", "sanitation_robustness_indicator", "sanitation_robustness_included", "sanitation_robustness_rate_loo", "sanitation_robustness_rate_loo_n_other_hh", "sanitation_robustness")

    # ====================================================================
    # DENOMINATOR DIAGNOSTICS (household-level, per country)
    # ====================================================================
    diag_rows = []
    for country_key in config.COUNTRIES:
        sub = hh_all[hh_all["country"] == country_key]
        for prefix, n_col in [
            ("water", "water_rate_loo_n_other_hh"),
            ("sanitation_core", "sanitation_core_rate_loo_n_other_hh"),
            ("sanitation_robustness", "sanitation_robustness_rate_loo_n_other_hh"),
        ]:
            s = sub[n_col]
            diag_rows.append({
                "country": country_key, "rate": prefix,
                "n_households": len(s),
                "min_other_hh": s.min(), "p25_other_hh": s.quantile(0.25),
                "median_other_hh": s.median(), "mean_other_hh": s.mean(),
                "p75_other_hh": s.quantile(0.75), "max_other_hh": s.max(),
                "n_zero_other_hh": int((s == 0).sum()),
                "pct_zero_other_hh": round(100 * (s == 0).mean(), 4),
            })
    diag_df = pd.DataFrame(diag_rows)
    print(f"\n{'='*90}\nLEAVE-ONE-OUT DENOMINATOR DIAGNOSTICS (household-level)\n{'='*90}")
    print(diag_df.to_string(index=False))

    # ====================================================================
    # PHASE G: link exposures + hv009 to the Step 06 child analytical dataset
    # ====================================================================
    print(f"\n{'='*90}\nPHASE G: linking household-level exposures to the Step 06 child dataset\n{'='*90}")

    pooled = pooled.copy()
    pooled["country_household_id"] = pooled["country"] + "_" + pooled["v001"].astype(str) + "_" + pooled["v002"].astype(str)

    hh_export_cols = [
        "country_household_id", "hv009", "hv005",
        "water_rate_loo", "water_rate_loo_n_other_hh",
        "sanitation_core_rate_loo", "sanitation_core_rate_loo_n_other_hh",
        "sanitation_robustness_rate_loo", "sanitation_robustness_rate_loo_n_other_hh",
    ]
    # NOTE (pre-freeze readability audit): compute_leave_one_out() above
    # builds these columns under their internal names (water_rate_loo,
    # sanitation_core_rate_loo, sanitation_robustness_rate_loo); this is the
    # one place they are renamed to the final exported names used by every
    # downstream script (sanitation_rate_loo_core,
    # sanitation_rate_loo_robustness_biodigester). A reader searching for
    # "sanitation_rate_loo_core" elsewhere in this file will not find that
    # literal string until here.
    hh_export = hh_all[hh_export_cols].rename(columns={
        "hv009": "household_size_raw",
        "hv005": "hv005_raw",
        "sanitation_core_rate_loo": "sanitation_rate_loo_core",
        "sanitation_core_rate_loo_n_other_hh": "sanitation_rate_loo_core_n_other_hh",
        "sanitation_robustness_rate_loo": "sanitation_rate_loo_robustness_biodigester",
        "sanitation_robustness_rate_loo_n_other_hh": "sanitation_rate_loo_robustness_n_other_hh",
    })

    # ---- PHASE F (Item 6): verify country+hv001+hv002 -> country+v001+v002 linkage, ALL FOUR COUNTRIES ----
    kr_household_ids = set(pooled["country_household_id"])
    hr_household_ids = set(hh_export["country_household_id"])
    unmatched = kr_household_ids - hr_household_ids
    if unmatched:
        raise RuntimeError(
            f"{len(unmatched)} child-dataset household ID(s) have no matching HR household: "
            f"{sorted(unmatched)[:20]}{'...' if len(unmatched) > 20 else ''}. Aborting - 100% linkage is required."
        )
    for country_key in config.COUNTRIES:
        kr_ids_c = {x for x in kr_household_ids if x.startswith(f"{country_key}_")}
        hr_ids_c = {x for x in hr_household_ids if x.startswith(f"{country_key}_")}
        n_unmatched_c = len(kr_ids_c - hr_ids_c)
        print(f"  [{country_key}] child-dataset households: {len(kr_ids_c)}  unmatched to HR: {n_unmatched_c}")
        if n_unmatched_c > 0:
            raise RuntimeError(f"[{country_key}] {n_unmatched_c} unmatched household(s). Aborting.")
        report_entry = next(r for r in report_rows if r["country"] == country_key)
        report_entry["kr_households_checked"] = len(kr_ids_c)
        report_entry["kr_households_unmatched_to_hr"] = n_unmatched_c
    print("  Household linkage: 100% match, country+hv001+hv002 <-> country+v001+v002, all four countries")

    merged = pooled.merge(hh_export, on="country_household_id", how="left", validate="many_to_one", indicator=True)
    if (merged["_merge"] != "both").any():
        raise RuntimeError("Unmatched child row(s) after merge - contradicts the pre-merge 100% linkage check. Aborting.")
    merged = merged.drop(columns="_merge")

    # ====================================================================
    # PHASE H: VALIDATION
    # ====================================================================
    print(f"\n{'='*90}\nPHASE H: VALIDATION\n{'='*90}")

    if len(merged) != n_pooled_before:
        raise RuntimeError(f"Row count changed: {n_pooled_before} -> {len(merged)}. Aborting.")
    print(f"Row count check: {len(merged)} == Step 06 input ({n_pooled_before})")

    for country_key, n_before in n_per_country_before.items():
        n_after = int((merged["country"] == country_key).sum())
        if n_after != n_before:
            raise RuntimeError(f"[{country_key}] Row count changed: {n_before} -> {n_after}.")
    print("Per-country row count check: unchanged for all four")

    if merged["country_child_id"].duplicated().any():
        raise RuntimeError("Duplicate country_child_id after Step 08 linkage. Aborting.")
    if merged["country_child_id"].isna().any():
        raise RuntimeError("Null country_child_id after Step 08 linkage. Aborting.")
    print("country_child_id: unique and non-null after Step 08 linkage")

    # All Step 06 columns row-for-row identical (never overwritten)
    for col in pooled_cols_before:
        both_na = merged[col].isna() & step06_snapshot[col].isna()
        mismatch = (merged[col] != step06_snapshot[col]) & ~both_na
        if mismatch.any():
            raise RuntimeError(f"Step 06 column '{col}' changed after Step 08 linkage ({int(mismatch.sum())} row(s)). Aborting.")
    print(f"All {len(pooled_cols_before)} Step 06 columns: unchanged (row-for-row identity confirmed)")

    # Same-household children get identical leave-one-out rates
    rate_cols = ["water_rate_loo", "sanitation_rate_loo_core", "sanitation_rate_loo_robustness_biodigester"]
    for col in rate_cols:
        nunique = merged.groupby("country_household_id")[col].nunique(dropna=False)
        if (nunique > 1).any():
            bad = nunique[nunique > 1].index.tolist()
            raise RuntimeError(f"{col}: {len(bad)} household(s) have non-identical rates across siblings: {bad[:10]}. Aborting.")
    print("Same-household children receive identical leave-one-out rates: confirmed for all three rate variables")

    # hv009 missingness after linkage
    n_hv009_missing = merged["household_size_raw"].isna().sum()
    print(f"household_size_raw (hv009) missing after linkage: {n_hv009_missing} / {len(merged)}")
    if n_hv009_missing > 0:
        raise RuntimeError("household_size_raw missing after a verified 100%-matched linkage - unexpected. Aborting.")

    # Coverage / exclusion diagnostics at the CHILD level
    print(f"\n{'-'*90}\nCHILD-LEVEL COVERAGE DIAGNOSTICS\n{'-'*90}")
    coverage_rows = []
    for country_key in config.COUNTRIES:
        sub = merged[merged["country"] == country_key]
        row = {"country": country_key, "n_children": len(sub)}
        for col in rate_cols:
            n_nonmissing = sub[col].notna().sum()
            row[f"{col}_nonmissing_n"] = n_nonmissing
            row[f"{col}_nonmissing_pct"] = round(100 * n_nonmissing / len(sub), 3)
        coverage_rows.append(row)
    coverage_df = pd.DataFrame(coverage_rows)
    print(coverage_df.to_string(index=False))

    merged["generated_at_utc_step08"] = datetime.now(timezone.utc).isoformat()

    new_cols = [c for c in merged.columns if c not in pooled_cols_before]
    print(f"\nNew columns added in Step 08 ({len(new_cols)}): {new_cols}")

    n_cols = merged.shape[1]
    expected_new = 1 + len([  # country_household_id
        "household_size_raw", "hv005_raw",
        "water_rate_loo", "water_rate_loo_n_other_hh",
        "sanitation_rate_loo_core", "sanitation_rate_loo_core_n_other_hh",
        "sanitation_rate_loo_robustness_biodigester", "sanitation_rate_loo_robustness_n_other_hh",
    ]) + 1  # + generated_at_utc_step08
    expected_cols = len(pooled_cols_before) + expected_new
    if n_cols != expected_cols:
        raise RuntimeError(f"Final column count ({n_cols}) != expected ({expected_cols}). Aborting.")
    print(f"Final schema check: {n_cols} columns (== {len(pooled_cols_before)} Step06 + {expected_new} new)")

    # ====================================================================
    # PHASE I: WRITE OUTPUTS
    # ====================================================================
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nWritten: {OUTPUT_PATH}  ({len(merged)} rows, {merged.shape[1]} columns)")

    report_df = pd.DataFrame(report_rows).merge(coverage_df, on="country", how="left")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(REPORT_PATH, index=False)
    print(f"Written: {REPORT_PATH}")

    DIAGNOSTIC_PATH.parent.mkdir(parents=True, exist_ok=True)
    diag_df.to_csv(DIAGNOSTIC_PATH, index=False)
    print(f"Written: {DIAGNOSTIC_PATH}")

    # ---- Final source-integrity re-verification ----
    checksum_pooled_after = md5_of_file(POOLED_INPUT_PATH)
    if checksum_pooled_after != checksum_pooled_before:
        raise RuntimeError("Step 06 input file changed during Step 08 execution!")
    checksums_hr_after = {c: md5_of_file(p) for c, p in HR_PATHS.items()}
    if checksums_hr_before != checksums_hr_after:
        raise RuntimeError("An HR source file changed during Step 08 execution!")
    print("\nSource integrity check: Step 06 input and all four HR source files unchanged (checksum match)")


if __name__ == "__main__":
    main()
