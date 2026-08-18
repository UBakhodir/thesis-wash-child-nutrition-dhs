"""
06_ge_linkage.py
==================
Attaches cluster-level geographic information from each country's DHS GE
shapefile to the pooled Step 05 KR dataset, joined on a country-qualified
cluster key (country_psu <-> country_ge_cluster) so that raw DHSCLUST
codes - which are small per-survey integers and collide numerically
across countries, exactly like v001/psu (see Step 05 design review) -
can never be matched across the wrong country.

IMPORTANT: The retained LATNUM/LONGNUM coordinates are DHS's official
RANDOMLY DISPLACED cluster coordinates, NOT exact household locations.
This script does not reverse displacement, reconstruct true locations,
interpolate, or reproject anything - coordinates are carried through
exactly as DHS provides them. This must be described as such in any
later methodology text discussing precision or distance-based analysis.

Reads ONLY:
  - data/processed/pooled_kr_four_country.parquet (Step 05 output)
  - the four countries' GE shapefiles under data/interim/DHS/.../GE/

Never touches data/raw/, data/interim/, or any Step 00-05 script/output.
No distances, buffers, external covariates, maps, regressions, or
descriptive statistics are computed. No weight/WASH/anthropometric
variable is altered.
"""

import hashlib
import importlib.util
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import geopandas as gpd

SCRIPT_DIR = Path(__file__).resolve().parent

def _load_module(filename, modname):
    spec = importlib.util.spec_from_file_location(modname, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

config = _load_module("00_config.py", "dhs_config")

POOLED_PATH = config.POOLED_OUTPUT
OUTPUT_PATH = config.POOLED_GEOLINKED_OUTPUT
REPORT_PATH = config.PROJECT_ROOT / "outputs" / "tables" / "ge_linkage_report.csv"

GE_PATHS = {c: info["ge_path"] for c, info in config.COUNTRIES.items()}

# Approved final set of GE columns to retain in the geolinked output.
GE_RETAINED_COLS = [
    "DHSCLUST", "DHSID", "DHSYEAR", "DHSREGNA", "DHSREGCO",
    "URBAN_RURA", "LATNUM", "LONGNUM", "ALT_DEM", "SOURCE",
]

SHAPEFILE_COMPONENT_EXTENSIONS = [
    ".shp", ".shx", ".dbf", ".prj", ".cpg", ".sbn", ".sbx", ".shp.xml",
]


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def shapefile_component_paths(shp_path):
    """All existing sidecar files sharing the shapefile's base name."""
    base = shp_path.with_suffix("")
    paths = []
    for ext in SHAPEFILE_COMPONENT_EXTENSIONS:
        p = Path(str(base) + ext)
        if p.exists():
            paths.append(p)
    return paths


def checksum_ge_inputs(ge_paths):
    """Checksums every sidecar file of every country's GE shapefile (not
    just the .shp itself - a shapefile is a multi-file format, and .dbf/
    .shx changes would corrupt the read without changing .shp). Called
    once before and once after main() to prove the raw GE sources were
    never modified by this script."""
    checksums = {}
    for country, shp_path in ge_paths.items():
        for p in shapefile_component_paths(shp_path):
            checksums[str(p)] = md5_of_file(p)
    return checksums


def main():
    """
    Attaches cluster-level GE geographic columns to the pooled Step 05
    dataset via the country-qualified country_psu <-> country_ge_cluster
    key (see module docstring for why raw DHSCLUST alone isn't safe to
    join on across pooled countries). Retains only the approved GE column
    subset and validates a 100% match with no coordinate/region drift.
    """
    # ---- Verify inputs exist ----
    if not POOLED_PATH.exists():
        raise FileNotFoundError(f"Step 05 pooled input not found: {POOLED_PATH}")
    for country, path in GE_PATHS.items():
        if not path.exists():
            raise FileNotFoundError(f"[{country}] GE shapefile not found: {path}")

    # ---- Checksum GE inputs BEFORE reading (defense in depth) ----
    checksums_before = checksum_ge_inputs(GE_PATHS)

    # ---- Load pooled Step 05 dataset ----
    pooled = pd.read_parquet(POOLED_PATH)
    n_pooled_before = len(pooled)
    pooled_cols_before = list(pooled.columns)
    print(f"Loaded pooled Step 05 dataset: {n_pooled_before} rows, {pooled.shape[1]} columns")

    # Snapshot of every Step 05 column, for the row-for-row identity check later
    step05_snapshot = pooled[pooled_cols_before].copy()

    n_per_country_before = pooled["country"].value_counts().to_dict()
    psu_nunique_before = pooled.groupby("country")["psu"].nunique().to_dict()

    # ====================================================================
    # LOAD + VALIDATE EACH COUNTRY'S GE SHAPEFILE (before any merge)
    # ====================================================================
    ge_frames = []
    report_rows = []

    for country, shp_path in GE_PATHS.items():
        gdf = gpd.read_file(shp_path)
        print(f"\n[{country}] Loaded GE: {shp_path.name} ({len(gdf)} rows)")

        missing_cols = [c for c in GE_RETAINED_COLS if c not in gdf.columns]
        if missing_cols:
            raise RuntimeError(f"[{country}] GE shapefile missing expected column(s): {missing_cols}")

        # ---- No duplicate / missing DHSCLUST ----
        if gdf["DHSCLUST"].isna().any():
            raise RuntimeError(f"[{country}] GE has missing DHSCLUST value(s). Aborting.")
        if gdf["DHSCLUST"].duplicated().any():
            dups = sorted(gdf.loc[gdf["DHSCLUST"].duplicated(keep=False), "DHSCLUST"].unique())
            raise RuntimeError(f"[{country}] Duplicate DHSCLUST value(s) in GE: {dups}. Aborting.")

        # ---- LATNUM/LONGNUM non-missing and coordinate pair is not (0,0) ----
        if gdf["LATNUM"].isna().any() or gdf["LONGNUM"].isna().any():
            raise RuntimeError(f"[{country}] GE has missing LATNUM/LONGNUM. Aborting.")
        if ((gdf["LATNUM"] == 0) & (gdf["LONGNUM"] == 0)).any():
            n_zero = int(((gdf["LATNUM"] == 0) & (gdf["LONGNUM"] == 0)).sum())
            raise RuntimeError(f"[{country}] {n_zero} GE cluster(s) have (0,0) sentinel coordinates. Aborting.")

        # ---- Build country-qualified join key ----
        # DHSCLUST is a whole-number cluster id (may be stored as float in
        # the shapefile's DBF); cast to int before string-building so it
        # matches country_psu's integer-based format from Step 05.
        ge_sub = gdf[GE_RETAINED_COLS].copy()
        ge_sub["DHSCLUST"] = ge_sub["DHSCLUST"].astype("int64")
        ge_sub["country_ge_cluster"] = country + "_" + ge_sub["DHSCLUST"].astype(str)

        n_dup_key = ge_sub["country_ge_cluster"].duplicated().sum()
        if n_dup_key > 0:
            raise RuntimeError(f"[{country}] Duplicate country_ge_cluster after prefixing. Aborting.")

        ge_frames.append(ge_sub)

        report_rows.append({
            "country": country,
            "ge_rows": len(gdf),
            "ge_unique_dhsclust": gdf["DHSCLUST"].nunique(),
        })

    ge_combined = pd.concat(ge_frames, ignore_index=True)
    if ge_combined["country_ge_cluster"].duplicated().any():
        raise RuntimeError("Duplicate country_ge_cluster found across combined GE data. Aborting.")
    print(f"\nCombined GE data: {len(ge_combined)} rows across all four countries")

    # ====================================================================
    # KR CLUSTER -> GE MATCH CHECK (before merging, so unmatched IDs can
    # be reported exactly rather than only inferred from merge indicator)
    # ====================================================================
    for country in GE_PATHS:
        kr_clusters = set(pooled.loc[pooled["country"] == country, "country_psu"])
        ge_clusters = set(ge_combined.loc[
            ge_combined["country_ge_cluster"].str.startswith(f"{country}_"), "country_ge_cluster"
        ])
        unmatched = kr_clusters - ge_clusters
        if unmatched:
            raise RuntimeError(
                f"[{country}] {len(unmatched)} KR cluster(s) have no match in GE: "
                f"{sorted(unmatched)}. Aborting - 100% match is required."
            )
        report_entry = next(r for r in report_rows if r["country"] == country)
        report_entry["kr_unique_psu"] = len(kr_clusters)
        report_entry["kr_clusters_matched_in_ge"] = len(kr_clusters)
        report_entry["kr_clusters_unmatched"] = 0
    print("Pre-merge cluster match check: 100% of KR clusters found in GE for all four countries")

    # ====================================================================
    # MERGE: country-safe, many (KR children) -> one (GE cluster)
    # ====================================================================
    merged = pooled.merge(
        ge_combined,
        left_on="country_psu", right_on="country_ge_cluster",
        how="left", validate="many_to_one", indicator=True,
    )

    n_unmatched_rows = int((merged["_merge"] != "both").sum())
    if n_unmatched_rows > 0:
        unmatched_ids = sorted(merged.loc[merged["_merge"] != "both", "country_psu"].unique())
        raise RuntimeError(
            f"{n_unmatched_rows} pooled child row(s) failed to match GE. "
            f"Unmatched country_psu values: {unmatched_ids}. Aborting."
        )
    print("Merge check: 0 unmatched child rows (100% match) across all four countries")

    # ---- Explicit country-qualified merge relationship validation
    # (performed BEFORE dropping country_ge_cluster, since these checks
    # need that column) ----
    if not (merged["country_psu"] == merged["country_ge_cluster"]).all():
        n_bad = int((merged["country_psu"] != merged["country_ge_cluster"]).sum())
        raise RuntimeError(
            f"{n_bad} row(s) have country_psu != country_ge_cluster after the "
            "merge - the join key must match exactly on every row. Aborting."
        )
    print("country_psu == country_ge_cluster: confirmed for every merged row")

    psu_to_cluster = merged.groupby("country_psu")["country_ge_cluster"].nunique()
    if (psu_to_cluster != 1).any():
        bad_psu = sorted(psu_to_cluster[psu_to_cluster != 1].index.tolist())
        raise RuntimeError(
            f"{len(bad_psu)} country_psu value(s) map to more than one "
            f"country_ge_cluster: {bad_psu}. Aborting."
        )
    print("Each country_psu maps to exactly one country_ge_cluster")

    cluster_to_psu = merged.groupby("country_ge_cluster")["country_psu"].nunique()
    if (cluster_to_psu != 1).any():
        bad_cluster = sorted(cluster_to_psu[cluster_to_psu != 1].index.tolist())
        raise RuntimeError(
            f"{len(bad_cluster)} country_ge_cluster value(s) map to more than "
            f"one country_psu among linked KR clusters: {bad_cluster}. Aborting."
        )
    print("Each country_ge_cluster maps to exactly one country_psu among linked KR clusters")

    # country_ge_cluster may now be dropped: country_psu + retained DHSCLUST
    # provide the necessary audit trail for the join going forward.
    merged = merged.drop(columns=["_merge", "country_ge_cluster"])

    # ====================================================================
    # VALIDATION (all checks run BEFORE writing anything)
    # ====================================================================

    # Row count unchanged
    if len(merged) != n_pooled_before:
        raise RuntimeError(f"Row count changed: {n_pooled_before} -> {len(merged)}. Aborting.")
    print(f"Row count check: {len(merged)} == pooled input ({n_pooled_before})")

    # Per-country row counts unchanged
    for country, n_before in n_per_country_before.items():
        n_after = int((merged["country"] == country).sum())
        if n_after != n_before:
            raise RuntimeError(f"[{country}] Row count changed after GE linkage: {n_before} -> {n_after}.")
    print("Per-country row count check: unchanged for all four")

    # country_child_id unique/non-null
    if merged["country_child_id"].duplicated().any():
        raise RuntimeError("Duplicate country_child_id after GE linkage. Aborting.")
    if merged["country_child_id"].isna().any():
        raise RuntimeError("Null country_child_id after GE linkage. Aborting.")
    print("country_child_id: unique and non-null after GE linkage")

    # All Step 05 columns row-for-row identical (never overwritten)
    for col in pooled_cols_before:
        both_na = merged[col].isna() & step05_snapshot[col].isna()
        mismatch = (merged[col] != step05_snapshot[col]) & ~both_na
        if mismatch.any():
            raise RuntimeError(
                f"Step 05 column '{col}' changed after GE linkage "
                f"({int(mismatch.sum())} mismatched row(s)). Aborting."
            )
    print("All Step 05 columns (incl. residence, psu, strata, country_psu, country, "
          "survey_round, anthropometric, WASH, control variables): unchanged")

    # Unique merged cluster count == unique KR PSU count, per country
    # (additional check, kept alongside the explicit relationship checks above)
    for country in GE_PATHS:
        sub = merged[merged["country"] == country]
        n_unique_merged_clusters = sub["DHSCLUST"].nunique()
        n_unique_kr_psu = psu_nunique_before[country]
        if n_unique_merged_clusters != n_unique_kr_psu:
            raise RuntimeError(
                f"[{country}] Unique merged GE clusters ({n_unique_merged_clusters}) != "
                f"unique KR PSUs ({n_unique_kr_psu}). Aborting."
            )
        one_to_one = sub.groupby("psu")["DHSCLUST"].nunique().eq(1).all()
        if not one_to_one:
            raise RuntimeError(f"[{country}] Some psu values map to more than one DHSCLUST. Aborting.")
        report_entry = next(r for r in report_rows if r["country"] == country)
        report_entry["unique_merged_clusters"] = n_unique_merged_clusters
        report_entry["unique_kr_psu"] = n_unique_kr_psu
    print("Unique merged DHSCLUST count equals unique KR PSU count, for all four countries")

    # LATNUM/LONGNUM non-missing and coordinate pair is not (0,0)
    if merged["LATNUM"].isna().any() or merged["LONGNUM"].isna().any():
        raise RuntimeError("Missing LATNUM/LONGNUM after merge. Aborting.")
    if ((merged["LATNUM"] == 0) & (merged["LONGNUM"] == 0)).any():
        raise RuntimeError("(0,0) sentinel coordinate row(s) found after merge. Aborting.")
    print("LATNUM/LONGNUM: non-missing and coordinate pair is not (0,0) for all rows after merge")

    # Geographic values constant within cluster
    geo_cols_to_check = ["DHSID", "DHSYEAR", "DHSREGNA", "DHSREGCO",
                          "URBAN_RURA", "LATNUM", "LONGNUM", "ALT_DEM", "SOURCE"]
    for col in geo_cols_to_check:
        n_multi = merged.groupby(["country", "DHSCLUST"])[col].nunique().gt(1).sum()
        if n_multi > 0:
            raise RuntimeError(
                f"Geographic column '{col}' is not constant within {n_multi} "
                f"(country, DHSCLUST) cluster(s). Aborting."
            )
    print("Geographic values constant within every (country, DHSCLUST) cluster")

    # KR residence vs GE URBAN_RURA: 100% consistency required
    urban_rural_map = {"U": "Urban", "R": "Rural"}
    merged["_ge_residence_check"] = merged["URBAN_RURA"].map(urban_rural_map)
    disagree = merged["residence"] != merged["_ge_residence_check"]
    if disagree.any():
        n_dis = int(disagree.sum())
        raise RuntimeError(
            f"{n_dis} row(s) disagree between KR residence and GE URBAN_RURA. "
            "100% consistency is required. Aborting."
        )
    merged = merged.drop(columns=["_ge_residence_check"])
    print("KR residence <-> GE URBAN_RURA: 100% consistent for all rows")

    # ---- Add provenance timestamp AFTER all checks, BEFORE final column count ----
    merged["generated_at_utc_step06"] = datetime.now(timezone.utc).isoformat()

    n_cols = merged.shape[1]
    expected_cols = len(pooled_cols_before) + len(GE_RETAINED_COLS) + 1  # +1 for generated_at_utc_step06
    if n_cols != expected_cols:
        raise RuntimeError(
            f"Final column count ({n_cols}) != expected ({expected_cols} = "
            f"{len(pooled_cols_before)} Step05 + {len(GE_RETAINED_COLS)} GE + 1 provenance). Aborting."
        )
    print(f"Final schema check: {n_cols} columns "
          f"(== {len(pooled_cols_before)} Step05 + {len(GE_RETAINED_COLS)} GE + 1 provenance)")

    # ====================================================================
    # WRITE MAIN OUTPUT
    # ====================================================================
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(OUTPUT_PATH, index=False)
    print(f"\nWritten: {OUTPUT_PATH}  ({len(merged)} rows, {merged.shape[1]} columns)")

    # ====================================================================
    # WRITE VALIDATION REPORT
    # ====================================================================
    report_df = pd.DataFrame(report_rows)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(REPORT_PATH, index=False)
    print(f"Written: {REPORT_PATH}")

    # ---- Final re-verification: GE source files unchanged ----
    checksums_after = checksum_ge_inputs(GE_PATHS)
    if checksums_before != checksums_after:
        changed = [p for p in checksums_before if checksums_before[p] != checksums_after.get(p)]
        raise RuntimeError(f"GE source file(s) changed during Step 06 execution: {changed}")
    print("GE source file integrity check: all shapefile components unchanged (checksum match)")


if __name__ == "__main__":
    main()
