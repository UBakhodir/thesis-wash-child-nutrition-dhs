"""
08_spatial_extraction_PREPARED.py
=================================
Implementation of cluster-level spatial extraction of IHME modelled WASH coverage
(W_IMP, S_IMP; MEAN, LOWER, UPPER; 2000-2017) around displaced DHS cluster
coordinates. PREPARED: the module is complete and self-tested on synthetic
points, but it is NOT run on respondent clusters in this milestone.

Modes:
  --selftest              synthetic points only (public capital-city coordinates,
                          not respondent data); checks the implementation rules.
  --dry-run (default)     validates inputs; prints aggregate counts only.
  --execute --confirm-gps-authorized
                          full extraction on restricted cluster coordinates.
                          Writes restricted outputs outside the repository.

Requirements (not installed here; this script does not install packages):
  numpy, pandas, pyarrow, Pillow, pyproj

Rules (sources in the milestone and resolution reports):
  - Displacement (IPUMS GPSLAT page): urban up to 2 km; 99% of rural up to 5 km;
    1% of rural up to 10 km. Primary: urban 2 km, rural 5 km. 10 km rural = sensitivity.
  - Refugee clusters (URBAN = 3): no documented displacement rule; excluded from
    the primary specification and reported separately.
  - Buffers are metric (equal-area CRS, proposed ESRI:102022; to confirm for the
    study extent). Never in degrees.
  - Raster pixel centres are tested for membership in the metric buffer.
  - NoData (-999999) is never zero. Valid = finite, not NoData, 0 <= v <= 100.
    A buffer with no valid pixel is missing (value NaN, valid_fraction 0).
  - Coordinate order: GPSLAT = latitude, GPSLONG = longitude (WGS84).
  - Zero-zero pairs are documented missing and are never extracted.
  - Point (nearest-pixel) extraction is a sensitivity alternative.
  - Raster geotransform: tie point and scale from the GeoTIFF tags. The
    raster-type GeoKey (1025) is checked: PixelIsArea (1) is assumed for the tie
    point; any other value stops execution.
"""
import argparse
import hashlib
import importlib
import io
import json
import os
import platform
import struct
import sys
import zipfile
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
DOWNLOADS = r"C:\Users\user\Downloads"
RUN = os.path.join(MASTER, "data", "processed", "ipums_import", "v2", "run_20261006T140022Z")
RUN_ID = "20261006T140022Z"
RESTRICTED_OUT = os.path.join(MASTER, "data", "processed", "spatial_extraction_PREPARED")
ARCHIVES = {"W_IMP": os.path.join(DOWNLOADS, "Percent (2).zip"),
            "S_IMP": os.path.join(DOWNLOADS, "Percent.zip")}
YEARS = list(range(2000, 2018))
TYPES = ["LOWER", "MEAN", "UPPER"]
NODATA = -999999.0
EXPECTED_SHAPE = (2123, 6610)
RADIUS_M = {"urban": 2000.0, "rural": 5000.0}
SENS_RURAL_M = 10000.0
PROPOSED_CRS = "ESRI:102022"
REQUIRED = ["numpy", "pandas", "pyarrow", "PIL", "pyproj"]
TAG_TIE, TAG_SCALE, TAG_GEOKEY = 33922, 33550, 34735

log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    log_lines.append(line)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def member_name(product, typ, year):
    return f"IHME_LMIC_WASH_2000_2017_{product}_PERCENT_{typ}_{year}_Y2020M06D02.TIF"


def read_raster(data):
    """Return (array float64, geotransform dict). Stops if the raster-type key is unexpected."""
    im = Image.open(io.BytesIO(data))
    t = im.tag_v2
    gk = list(t.get(TAG_GEOKEY, ()))
    raster_type = None
    for i in range(4, len(gk), 4):
        if gk[i] == 1025:
            raster_type = gk[i + 3]
    if raster_type != 1:
        raise RuntimeError(f"raster type {raster_type} not PixelIsArea; geotransform rule not applicable")
    tie = t.get(TAG_TIE)
    scale = t.get(TAG_SCALE)
    arr = np.asarray(im, dtype=np.float64)
    if arr.shape != EXPECTED_SHAPE:
        raise RuntimeError(f"unexpected raster shape {arr.shape}")
    gt = {"x0": float(tie[3]), "y0": float(tie[4]), "sx": float(scale[0]), "sy": float(scale[1])}
    return arr, gt


def pixel_centres(gt, rows, cols):
    lon = gt["x0"] + (cols + 0.5) * gt["sx"]
    lat = gt["y0"] - (rows + 0.5) * gt["sy"]
    return lon, lat


# Coarse national boxes (lat_min, lat_max, lon_min, lon_max), used to detect swapped
# or gross errors. Approximate; a point just outside a border can be correct.
NATIONAL_BOX = {23104: (3.4, 14.9, 33.0, 48.0), 28806: (4.7, 11.2, -3.3, 1.2),
                40406: (-4.7, 5.0, 33.9, 41.9), 56606: (4.2, 13.9, 2.7, 14.7)}


def check_coordinates(lat, lon, sample=None):
    """Range check; with a sample code, also the national box (detects swapped order)."""
    if not ((-90.0 <= lat <= 90.0) and (-180.0 <= lon <= 180.0)) or (lat == 0 and lon == 0):
        return False
    if sample is None:
        return True
    la0, la1, lo0, lo1 = NATIONAL_BOX[int(sample)]
    return la0 <= lat <= la1 and lo0 <= lon <= lo1


def buffer_stat(arr, gt, lat, lon, radius_m, transformer):
    """Mean of valid pixels whose centres fall in a metric buffer. Never zero-fills."""
    x0, y0 = transformer.transform(lon, lat)
    span_deg = radius_m / 111000.0 + 2 * max(abs(gt["sx"]), abs(gt["sy"]))
    c_lo = int(np.floor((lon - span_deg - gt["x0"]) / gt["sx"]))
    c_hi = int(np.ceil((lon + span_deg - gt["x0"]) / gt["sx"]))
    r_lo = int(np.floor((gt["y0"] - (lat + span_deg)) / gt["sy"]))
    r_hi = int(np.ceil((gt["y0"] - (lat - span_deg)) / gt["sy"]))
    rows_ = np.clip(np.arange(r_lo, r_hi + 1), 0, arr.shape[0] - 1)
    cols_ = np.clip(np.arange(c_lo, c_hi + 1), 0, arr.shape[1] - 1)
    R, C = np.meshgrid(rows_, cols_, indexing="ij")
    lo, la = pixel_centres(gt, R.ravel(), C.ravel())
    px, py = transformer.transform(lo, la)
    inside = (px - x0) ** 2 + (py - y0) ** 2 <= radius_m ** 2
    vals = arr[R.ravel()[inside], C.ravel()[inside]]
    n = int(inside.sum())
    valid = vals[(vals != NODATA) & np.isfinite(vals) & (vals >= 0) & (vals <= 100)]
    vf = float(len(valid) / n) if n else 0.0
    return (float(valid.mean()) if len(valid) else np.nan), vf, n


def point_stat(arr, gt, lat, lon):
    col = int(np.floor((lon - gt["x0"]) / gt["sx"]))
    row = int(np.floor((gt["y0"] - lat) / gt["sy"]))
    if not (0 <= row < arr.shape[0] and 0 <= col < arr.shape[1]):
        return np.nan
    v = arr[row, col]
    return float(v) if (v != NODATA and np.isfinite(v) and 0 <= v <= 100) else np.nan


def selftest():
    """Synthetic public capital-city points; checks the implementation rules."""
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", PROPOSED_CRS, always_xy=True)
    results = {}
    # 1. coordinate-order check rejects swapped pairs and accepts correct order
    results["accepts_addis_lat_lon_in_box"] = check_coordinates(9.03, 38.74, 23104)
    results["rejects_swapped_pair_by_box"] = not check_coordinates(38.74, 9.03, 23104)
    results["rejects_zero_pair"] = not check_coordinates(0.0, 0.0, 23104)
    results["accepts_range_only_pair_without_box"] = check_coordinates(38.74, 9.03)  # documents the limit
    # 2. synthetic raster: constant 50 with a NoData strip, geotransform like the IHME grid
    arr = np.full(EXPECTED_SHAPE, 50.0)
    arr[:, :300] = NODATA
    gt = {"x0": -180.0, "y0": 90.0, "sx": 0.041667, "sy": 0.041667}
    v, vf, n = buffer_stat(arr, gt, 9.03, 38.74, 2000.0, tr)
    results["buffer_inside_valid_value_recovered"] = bool(v == 50.0 and vf == 1.0)
    v2, vf2, _ = buffer_stat(arr, gt, 0.0, -170.0, 5000.0, tr)   # NoData strip
    results["nodata_region_is_nan_not_zero"] = bool(np.isnan(v2) and vf2 == 0.0)
    results["nodata_region_valid_fraction_zero"] = bool(vf2 == 0.0)
    # 3. buffer radius is metric: a 5 km buffer contains more pixels than a 2 km one at equator-scale grid
    _, _, n2 = buffer_stat(np.zeros(EXPECTED_SHAPE), gt, 9.03, 38.74, 2000.0, tr)
    _, _, n5 = buffer_stat(np.zeros(EXPECTED_SHAPE), gt, 9.03, 38.74, 5000.0, tr)
    results["larger_radius_more_pixels"] = bool(n5 > n2)
    # 4. NoData never zero: a point in NoData returns NaN from point extraction
    results["point_nodata_nan"] = bool(np.isnan(point_stat(arr, gt, 0.0, -170.0)))
    # the range-only acceptance is a documented limit, not a pass criterion
    results.pop("accepts_range_only_pair_without_box")
    ok = all(v for v in results.values())
    log("SELFTEST " + json.dumps(results) + f" ALL_PASS={ok}")
    return ok


def dry_run():
    report = {"mode": "dry-run", "packages": {}, "inputs": {}, "counts": {}}
    for m in REQUIRED:
        try:
            importlib.import_module(m)
            report["packages"][m] = "available"
        except Exception:
            report["packages"][m] = "MISSING"
    for label, path in ARCHIVES.items():
        entry = {"path_exists": os.path.isfile(path)}
        if entry["path_exists"]:
            with zipfile.ZipFile(path) as z:
                names = set(z.namelist())
            expected = [member_name(label, t, y) for t in TYPES for y in YEARS]
            entry["members_expected"] = len(expected)
            entry["members_present"] = int(sum(1 for n in expected if n in names))
        report["inputs"][label] = entry
    report["inputs"]["validated_run_present"] = os.path.isdir(RUN)
    if os.path.isdir(RUN):
        T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                            columns=["SAMPLE", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
        pair_ok = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
        cl = T[pair_ok].groupby("IDHSPSU").agg(URBAN=("URBAN", "first"))
        report["counts"]["clusters_with_usable_coordinates"] = int(len(cl))
        report["counts"]["by_urban_code"] = {str(int(k)): int(v) for k, v in cl["URBAN"].value_counts().items()}
        report["counts"]["primary_eligible_urban_or_rural"] = int(cl["URBAN"].isin([1, 2]).sum())
        report["counts"]["refugee_excluded_from_primary"] = int((cl["URBAN"] == 3).sum())
    report["status"] = "dry-run complete: no raster values extracted; no coordinates printed"
    log("DRY-RUN " + json.dumps(report, default=str))
    return report


def execute():
    from pyproj import Transformer
    tr = Transformer.from_crs("EPSG:4326", PROPOSED_CRS, always_xy=True)
    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                        columns=["SAMPLE", "DHSID", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    pair_ok = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    cl = T[pair_ok].groupby("IDHSPSU").agg(SAMPLE=("SAMPLE", "first"), DHSID=("DHSID", "first"),
                                           URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"),
                                           LON=("GPSLONG", "first")).reset_index()
    cl = cl[cl["URBAN"].isin([1, 2])].copy()   # refugee (3) excluded from primary
    cl["stratum"] = np.where(cl["URBAN"] == 1, "urban", "rural")
    bad = [not check_coordinates(a, b, s) for a, b, s in zip(cl["LAT"], cl["LON"], cl["SAMPLE"])]
    if any(bad):
        raise RuntimeError(f"coordinate check failed for {sum(bad)} clusters; execution stopped (counts only)")
    os.makedirs(RESTRICTED_OUT, exist_ok=False)
    out = []
    lineage = {}
    for label, path in ARCHIVES.items():
        lineage[label] = {"path": path, "sha256": sha256_file(path)}
        with zipfile.ZipFile(path) as z:
            for typ in TYPES:
                for y in YEARS:
                    arr, gt = read_raster(z.read(member_name(label, typ, y)))
                    for r in cl.itertuples(index=False):
                        radius = RADIUS_M[r.stratum]
                        m, vf, n = buffer_stat(arr, gt, r.LAT, r.LON, radius, tr)
                        out.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "primary_buffer",
                                    m, vf, n))
                        if r.stratum == "rural":
                            m10, vf10, n10 = buffer_stat(arr, gt, r.LAT, r.LON, SENS_RURAL_M, tr)
                            out.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "sensitivity_rural_10km",
                                        m10, vf10, n10))
                        out.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "sensitivity_point",
                                    point_stat(arr, gt, r.LAT, r.LON), np.nan, 1))
    res = pd.DataFrame(out, columns=["IDHSPSU", "SAMPLE", "stratum", "product", "estimate", "year",
                                     "method", "value", "valid_fraction", "n_pixels"])
    res.to_parquet(os.path.join(RESTRICTED_OUT, "spatial_extraction_RESTRICTED.parquet"), index=False)
    with open(os.path.join(RESTRICTED_OUT, "lineage_PREPARED.json"), "w", encoding="utf-8") as f:
        json.dump({"lineage": lineage, "crs": PROPOSED_CRS, "status": "PROVISIONAL - CRS to confirm",
                    "completed_utc": datetime.now(timezone.utc).isoformat()}, f, indent=1)
    log(f"execute: rows={len(res)} clusters={len(cl)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--confirm-gps-authorized", action="store_true")
    args = ap.parse_args()
    log(f"python={platform.python_version()} script={os.path.basename(__file__)} "
        f"script_sha256={sha256_file(__file__)}")
    if args.selftest:
        ok = selftest()
        sys.exit(0 if ok else 1)
    if args.execute:
        if not args.confirm_gps_authorized:
            sys.exit("refused: --execute requires --confirm-gps-authorized (GPS approval verified first)")
        execute()
    else:
        dry_run()
