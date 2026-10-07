"""
22_validate_spatial_extraction_independent.py
===============================================
Independent verification of the historical spatial extraction's raw data
layer, written for the 2026-10-07 audit's material-verification pass
(docs/provenance/independent_audit_v1_2026-10-07/07_update_2026-10-07_pass2.md
section 2).

Uses rasterio (a different library from the project's own PIL-based
10_spatial_extraction_v3.py) to read the raw IHME GeoTIFFs directly from the
original downloaded archives and compare against the project's stored
containing-pixel extraction values, for a justified, non-arbitrary sample:
full-coverage, boundary/low-valid-fraction, and NoData/missing cases, drawn
from all three established-date countries and both products.

Scope, stated precisely: this verifies the raster-reading/coordinate/year-
mapping/NoData data layer that the project's primary buffer-averaging method
also depends on. It does NOT independently re-implement the exact-polygon-
overlap buffer-averaging algorithm itself, which remains verified only by
the project's own internal Monte Carlo self-check (10_spatial_extraction_v3
.py's mc_reference(), same codebase). These are two different claims and
this script only supports the first.

No coordinates, cluster identifiers, or individual record values are printed
anywhere in this script's output -- aggregate match statistics only.
"""
import json
import os
import zipfile
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import rasterio
from rasterio.io import MemoryFile

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
DOWNLOADS = r"C:\Users\user\Downloads"
NODATA = -999999.0
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join(MASTER, "data", "processed", "spatial_extraction",
                    f"independent_validation_{STAMP}")
os.makedirs(OUT, exist_ok=False)

STORED_PATH = os.path.join(MASTER, "data", "processed", "spatial_extraction",
                            "run_v3_20261006T183003Z", "cluster_year_extraction_RESTRICTED.parquet")
COORDS_PATH = os.path.join(MASTER, "data", "processed", "ipums_import", "v2",
                            "run_20261006T140022Z", "idhs_00002_typed_20261006T140022Z.parquet")
ARCHIVES = {"W_IMP": os.path.join(DOWNLOADS, "Percent (2).zip"),
            "S_IMP": os.path.join(DOWNLOADS, "Percent.zip")}

STORED = pd.read_parquet(STORED_PATH)
COORDS = pd.read_parquet(COORDS_PATH, columns=["IDHSPSU", "SAMPLE", "GPSLAT", "GPSLONG", "URBAN"]
                          ).drop_duplicates(subset=["IDHSPSU", "SAMPLE"])


def tif_member(product, year):
    return f"IHME_LMIC_WASH_2000_2017_{product}_PERCENT_MEAN_{year}_Y2020M06D02.TIF"


def read_pixel(product, year, lat, lon):
    with zipfile.ZipFile(ARCHIVES[product]) as z:
        with z.open(tif_member(product, year)) as fh:
            data = fh.read()
    with MemoryFile(data) as mem:
        with mem.open() as src:
            row, col = src.index(lon, lat)  # rasterio convention: index(x=lon, y=lat)
            if row < 0 or col < 0 or row >= src.height or col >= src.width:
                return None, "outside_raster"
            val = float(src.read(1, window=((row, row + 1), (col, col + 1)))[0, 0])
    if val == NODATA or not np.isfinite(val) or not (0 <= val <= 100):
        return np.nan, "nodata"
    return val, "full"


def pick_cases(sample_code, product, n_full=4, n_partial=2, n_missing=2):
    """Justified, non-arbitrary sample selection: full-coverage cases (random
    draw among status=='full' containing-pixel rows), NoData/missing cases
    (random draw among status=='missing'), and boundary cases (the lowest
    valid_fraction clusters under the primary buffer method, checked here at
    their own containing-pixel value) -- covering the three failure modes
    most likely to reveal a coordinate, CRS, year-mapping, or NoData bug."""
    sub = STORED[(STORED.SAMPLE == sample_code) & (STORED["product"] == product)
                 & (STORED.method == "sensitivity_containing_pixel") & (STORED.estimate == "MEAN")]
    full = sub[sub.status == "full"]
    missing = sub[sub.status == "missing"]
    buf = STORED[(STORED.SAMPLE == sample_code) & (STORED["product"] == product)
                 & (STORED.method == "primary_area_buffer") & (STORED.estimate == "MEAN")]
    boundary_psus = buf.sort_values("valid_fraction").head(20)[["IDHSPSU", "year"]].drop_duplicates()
    cases = [("full", full.sample(n=min(n_full, len(full)), random_state=1)),
             ("missing", missing.sample(n=min(n_missing, len(missing)), random_state=1))]
    bsub = sub.merge(boundary_psus, on=["IDHSPSU", "year"]).head(n_partial)
    cases.append(("boundary_low_valid_fraction", bsub))
    return cases


def run(sample_code, product, label, log):
    log.append(f"\n=== {label}: product={product} ===")
    results = []
    for case_type, rows in pick_cases(sample_code, product):
        for _, r in rows.iterrows():
            crow = COORDS[(COORDS.IDHSPSU == r.IDHSPSU) & (COORDS.SAMPLE == r.SAMPLE)]
            if crow.empty:
                continue
            lat, lon = float(crow.GPSLAT.iloc[0]), float(crow.GPSLONG.iloc[0])
            indep_val, indep_status = read_pixel(product, int(r.year), lat, lon)
            match_status = (indep_status == "full") == (r.status == "full")
            diff = abs(indep_val - r.value) if (indep_status == "full" and r.status == "full") else None
            results.append({"country": label, "product": product, "case_type": case_type,
                             "status_match": match_status,
                             "both_full": indep_status == "full" and r.status == "full",
                             "abs_diff": diff})
    df = pd.DataFrame(results)
    log.append(f"n_checked={len(df)}, status_match={df.status_match.sum()}/{len(df)}")
    both_full = df[df.both_full]
    if len(both_full):
        log.append(f"both-full: n={len(both_full)}, max_abs_diff={both_full.abs_diff.max():.6f}, "
                    f"mean_abs_diff={both_full.abs_diff.mean():.6f}")
    return df


if __name__ == "__main__":
    log = [f"=== {STAMP} independent spatial-extraction verification (data layer only) ==="]
    all_results = []
    for sample_code, label in [(56606.0, "Nigeria 2018"), (28806.0, "Ghana 2014"), (40406.0, "Kenya 2014")]:
        for product in ["W_IMP", "S_IMP"]:
            all_results.append(run(sample_code, product, label, log))
    full_df = pd.concat(all_results, ignore_index=True)
    bf = full_df[full_df.both_full]
    summary = {
        "label": "Spatial data-layer verification only -- does not verify the buffer-overlap algorithm itself",
        "total_n_checked": int(len(full_df)),
        "status_agreement": f"{int(full_df.status_match.sum())}/{len(full_df)}",
        "status_agreement_rate": float(full_df.status_match.mean()),
        "both_full_n": int(len(bf)),
        "max_abs_diff": float(bf.abs_diff.max()) if len(bf) else None,
        "mean_abs_diff": float(bf.abs_diff.mean()) if len(bf) else None,
    }
    log.append("\n=== OVERALL ===")
    log.append(json.dumps(summary, indent=1))
    print("\n".join(log))
    full_df.to_csv(os.path.join(OUT, "independent_spatial_check_AGGREGATE.csv"), index=False)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print(f"\nOutput written to {OUT}")
