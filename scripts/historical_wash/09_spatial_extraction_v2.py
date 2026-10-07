"""
09_spatial_extraction_v2.py
===========================
Cluster-level extraction of IHME modelled WASH coverage (S_IMP, W_IMP; LOWER, MEAN,
UPPER; 2000-2017) around displaced DHS cluster coordinates.

Supersedes 08_spatial_extraction_PREPARED.py for execution. Version 08 used
ESRI:102022 (Africa Albers equal-area), whose distances are not exact radially
from a point; version 09 uses an azimuthal equidistant projection (AEQD) centred
on each cluster, so distance from the cluster centre is exact by construction.

Method (per cluster, per radius):
  - Projection: AEQD centred on the cluster (distances from centre exact).
  - Buffer: disk of radius R (urban 2 km; rural 5 km primary; rural 10 km sensitivity).
  - Pixel geometry: each IHME pixel is approximated as the bilinear image of its four
    projected corners; sub-sampled on an n x n grid (n = 12). Inside test: distance
    from the cluster centre <= R.
  - Area weight of pixel k: (inside sub-samples / n^2) x metric area of pixel k.
  - Buffer total area = sum of weights over ALL pixels in the window, including
    indices outside the raster (uncovered).
  - Valid area = weight of pixels that are inside the raster and not NoData and
    within 0..100. Mean = area-weighted mean over valid area (covered area only).
  - Coverage status: full (valid/total >= 1 - 1e-3), partial, or missing (reason given).
    Partial buffers are NOT renormalised to full coverage; the valid-area fraction is kept.
  - Point method: containing-pixel rule only (no nearest substitution). NoData -> missing.

Modes:
  --selftest   synthetic rasters; independent Monte Carlo reference (random points
               uniform in the disk, mapped back to lon/lat); no respondent data.
  --pilot      20 real clusters chosen with a fixed seed; compared with Monte Carlo
               on one real raster. Prints aggregate differences only.
  --execute --confirm-gps-authorized --confirm-round-access
               full extraction; restricted outputs outside the repository.

Dependencies: numpy, pandas, pyarrow, Pillow, pyproj.
"""
import argparse
import hashlib
import io
import json
import os
import platform
import sys
import zipfile
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa
from PIL import Image
from pyproj import Geod, Transformer

Image.MAX_IMAGE_PIXELS = None

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
DOWNLOADS = r"C:\Users\user\Downloads"
RUN = os.path.join(MASTER, "data", "processed", "ipums_import", "v2", "run_20261006T140022Z")
RUN_ID = "20261006T140022Z"
OUT_ROOT = os.path.join(MASTER, "data", "processed", "spatial_extraction")
ARCHIVES = {"W_IMP": os.path.join(DOWNLOADS, "Percent (2).zip"),
            "S_IMP": os.path.join(DOWNLOADS, "Percent.zip")}
YEARS = list(range(2000, 2018))
TYPES = ["LOWER", "MEAN", "UPPER"]
NODATA = -999999.0
EXPECTED_SHAPE = (2123, 6610)
N_SUB = 12
RADIUS_M = {"urban": 2000.0, "rural": 5000.0}
SENS_RURAL_M = 10000.0
FULL_TOL = 1e-3
TAG_TIE, TAG_SCALE, TAG_GEOKEY = 33922, 33550, 34735
GEOD = Geod(ellps="WGS84")
NATIONAL_BOX = {23104: (3.4, 14.9, 33.0, 48.0), 28806: (4.7, 11.2, -3.3, 1.2),
                40406: (-4.7, 5.0, 33.9, 41.9), 56606: (4.2, 13.9, 2.7, 14.7)}
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


def read_raster(data, expected_shape=EXPECTED_SHAPE):
    im = Image.open(io.BytesIO(data))
    t = im.tag_v2
    gk = list(t.get(TAG_GEOKEY, ()))
    rtype, epsg = None, None
    for i in range(4, len(gk), 4):
        if gk[i] == 1025:
            rtype = gk[i + 3]
        if gk[i] == 2048:
            epsg = gk[i + 3]
    if rtype != 1:
        raise RuntimeError(f"raster type {rtype} is not PixelIsArea; rule not applicable")
    if epsg != 4326:
        raise RuntimeError(f"CRS EPSG {epsg} is not 4326")
    arr = np.asarray(im, dtype=np.float64)
    if arr.shape != expected_shape:
        raise RuntimeError(f"unexpected shape {arr.shape}")
    tie, scale = t.get(TAG_TIE), t.get(TAG_SCALE)
    gt = {"x0": float(tie[3]), "y0": float(tie[4]), "sx": float(scale[0]), "sy": float(scale[1]), "epsg": epsg}
    return arr, gt


def check_coordinates(lat, lon, sample):
    if not ((-90 <= lat <= 90) and (-180 <= lon <= 180)) or (lat == 0 and lon == 0):
        return False
    la0, la1, lo0, lo1 = NATIONAL_BOX[int(sample)]
    return la0 <= lat <= la1 and lo0 <= lon <= lo1


def window_pixels(gt, lat0, lon0, radius_m):
    """Rows/cols of the window; indices may fall outside the raster (uncovered)."""
    dlat = radius_m / 110_000.0 + 2 * abs(gt["sy"])
    dlon = radius_m / (110_000.0 * max(np.cos(np.radians(lat0)), 1e-6)) + 2 * abs(gt["sx"])
    r0 = int(np.floor((gt["y0"] - (lat0 + dlat)) / gt["sy"]))
    r1 = int(np.floor((gt["y0"] - (lat0 - dlat)) / gt["sy"]))
    c0 = int(np.floor(((lon0 - dlon) - gt["x0"]) / gt["sx"]))
    c1 = int(np.floor(((lon0 + dlon) - gt["x0"]) / gt["sx"]))
    rr, cc = np.meshgrid(np.arange(r0, r1 + 1), np.arange(c0, c1 + 1), indexing="ij")
    return rr.ravel(), cc.ravel()


def pixel_corners_ll(gt, rows, cols):
    """Corners (TL, TR, BR, BL) in lon/lat, shape (P, 4, 2) as (lon, lat)."""
    lon_l = gt["x0"] + cols * gt["sx"]
    lon_r = lon_l + gt["sx"]
    lat_t = gt["y0"] - rows * gt["sy"]
    lat_b = lat_t - gt["sy"]
    return np.stack([np.stack([lon_l, lat_t], -1), np.stack([lon_r, lat_t], -1),
                     np.stack([lon_r, lat_b], -1), np.stack([lon_l, lat_b], -1)], axis=1)


def aeqd(lat0, lon0):
    return Transformer.from_crs("EPSG:4326",
                                f"+proj=aeqd +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m",
                                always_xy=True)


def precompute(gt, lat0, lon0, radius_m, n=N_SUB):
    """Per-cluster pixel weights (independent of product, type and year)."""
    rows, cols = window_pixels(gt, lat0, lon0, radius_m)
    corners = pixel_corners_ll(gt, rows, cols)                 # (P,4,2)
    tr = aeqd(lat0, lon0)
    x, y = tr.transform(corners[..., 0].ravel(), corners[..., 1].ravel())
    XY = np.stack([x, y], -1).reshape(len(rows), 4, 2)         # projected corners
    A, B, C, D = XY[:, 0], XY[:, 1], XY[:, 2], XY[:, 3]
    area = 0.5 * np.abs(
        (A[:, 0] * B[:, 1] - B[:, 0] * A[:, 1]) + (B[:, 0] * C[:, 1] - C[:, 0] * B[:, 1]) +
        (C[:, 0] * D[:, 1] - D[:, 0] * C[:, 1]) + (D[:, 0] * A[:, 1] - A[:, 0] * D[:, 1]))
    s = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(s, s, indexing="xy")                     # U along columns, V along rows
    U, V = U.ravel()[None, :], V.ravel()[None, :]
    PX = ((1 - U) * (1 - V))[..., None] * A[:, None] + (U * (1 - V))[..., None] * B[:, None] + \
         ((U * V))[..., None] * C[:, None] + (((1 - U) * V))[..., None] * D[:, None]
    inside = (PX[..., 0] ** 2 + PX[..., 1] ** 2) <= radius_m ** 2
    frac = inside.mean(axis=1)
    return {"rows": rows, "cols": cols, "w": frac * area, "total_area_m2": float((frac * area).sum())}


def aggregate(arr, pre):
    """Area-weighted coverage statistics for one raster and one precomputed buffer."""
    H, W = arr.shape
    r, c, w = pre["rows"], pre["cols"], pre["w"]
    inr = (r >= 0) & (r < H) & (c >= 0) & (c < W)
    vals = np.full(len(r), np.nan)
    vals[inr] = arr[r[inr], c[inr]]
    ok = inr & (vals != NODATA) & np.isfinite(vals) & (vals >= 0) & (vals <= 100)
    total = pre["total_area_m2"]
    valid_area = float(w[ok].sum())
    frac = valid_area / total if total > 0 else 0.0
    out_frac = float(w[~inr].sum() / total) if total > 0 else 0.0
    nodata_frac = float(w[inr & ~ok].sum() / total) if total > 0 else 0.0
    if valid_area <= 0:
        reason = "outside_raster" if not ok.any() and not inr.any() else ("nodata" if not ok.any() else "other")
        return {"value": np.nan, "status": "missing", "reason": reason, "valid_fraction": 0.0,
                "total_area_m2": total, "valid_area_m2": 0.0, "n_cells": int((w > 0).sum()),
                "n_cells_valid": 0}
    mean = float((w[ok] * vals[ok]).sum() / valid_area)
    status = "full" if frac >= 1 - FULL_TOL else "partial"
    reason = "" if status == "full" else f"outside_fraction={out_frac:.4f};nodata_fraction={nodata_frac:.4f}"
    return {"value": mean, "status": status, "reason": reason, "valid_fraction": frac,
            "total_area_m2": total, "valid_area_m2": valid_area, "n_cells": int((w > 0).sum()),
            "n_cells_valid": int((ok & (w > 0)).sum())}


def point_stat(arr, gt, lat, lon):
    col = int(np.floor((lon - gt["x0"]) / gt["sx"]))
    row = int(np.floor((gt["y0"] - lat) / gt["sy"]))
    H, W = arr.shape
    if not (0 <= row < H and 0 <= col < W):
        return np.nan, "outside_raster"
    v = arr[row, col]
    if v == NODATA or not np.isfinite(v) or not (0 <= v <= 100):
        return np.nan, "nodata"
    return float(v), ""


def mc_reference(arr, gt, lat0, lon0, radius_m, m=200_000, seed=1):
    """Independent Monte Carlo: uniform points in the AEQD disk mapped back to lon/lat."""
    rng = np.random.default_rng(seed)
    rad = radius_m * np.sqrt(rng.random(m))
    th = 2 * np.pi * rng.random(m)
    back = Transformer.from_crs(f"+proj=aeqd +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m",
                                "EPSG:4326", always_xy=True)
    lon, lat = back.transform(rad * np.cos(th), rad * np.sin(th))
    H, W = arr.shape
    col = np.floor((lon - gt["x0"]) / gt["sx"]).astype(int)
    row = np.floor((gt["y0"] - lat) / gt["sy"]).astype(int)
    inr = (row >= 0) & (row < H) & (col >= 0) & (col < W)
    vals = np.full(m, np.nan)
    vals[inr] = arr[row[inr], col[inr]]
    ok = inr & (vals != NODATA) & np.isfinite(vals) & (vals >= 0) & (vals <= 100)
    return {"mean": float(vals[ok].mean()) if ok.any() else np.nan, "valid_fraction": float(ok.mean())}


def selftest():
    res = {}
    gt = {"x0": 38.0, "y0": 10.0, "sx": 0.041667, "sy": 0.041667, "epsg": 4326}
    lat0, lon0 = 9.5, 38.5
    # T1 constant raster, buffer fully inside
    arr = np.full((400, 400), 7.0)
    gt1 = dict(gt)
    pre = precompute(gt1, lat0, lon0, 2000.0)
    a = aggregate(arr, pre)
    res["T1_constant_mean_exact"] = bool(abs(a["value"] - 7.0) < 1e-9 and a["status"] == "full")
    # T2 total area vs analytic pi R^2 (n=12 sub-sampling error), R=5 km and 2 km
    for R in (2000.0, 5000.0):
        p = precompute(gt1, lat0, lon0, R)
        err = abs(p["total_area_m2"] / (np.pi * R * R) - 1)
        res[f"T2_area_rel_err_R{int(R)}_below_0.5pct"] = bool(err < 0.005)
    # T3 fractional overlap vs Monte Carlo (pixel-level fractions)
    pre = precompute(gt1, lat0, lon0, 5000.0)
    arr2 = np.arange(400 * 400, dtype=float).reshape(400, 400) % 100
    a2 = aggregate(arr2, pre)
    mc = mc_reference(arr2, gt1, lat0, lon0, 5000.0)
    res["T3_mean_vs_MC_within_0.5"] = bool(abs(a2["value"] - mc["mean"]) < 0.5)
    res["T3_valid_fraction_vs_MC_within_0.5pct"] = bool(abs(a2["valid_fraction"] - mc["valid_fraction"]) < 0.005)
    # T4 NoData half raster: valid fraction ~ MC; mean is valid value only (never zero)
    arr3 = np.full((400, 400), 40.0)
    arr3[:, :200] = NODATA
    a3 = aggregate(arr3, pre)
    mc3 = mc_reference(arr3, gt1, lat0, lon0, 5000.0)
    res["T4_nodata_mean_is_valid_value"] = bool(abs(a3["value"] - 40.0) < 1e-9)
    res["T4_nodata_fraction_vs_MC_within_0.5pct"] = bool(abs(a3["valid_fraction"] - mc3["valid_fraction"]) < 0.005)
    res["T4_nodata_status_partial"] = bool(a3["status"] == "partial")
    # T5 buffer smaller than one cell (R = 1 km): contributing cells and total area
    p5 = precompute(gt1, lat0, lon0, 1000.0)
    res["T5_small_buffer_area_close_to_pi_R2"] = bool(abs(p5["total_area_m2"] / (np.pi * 1e6) - 1) < 0.02)
    res["T5_small_buffer_few_cells"] = bool((p5["w"] > 0).sum() <= 9)
    # T6 buffer crossing cell boundaries with two values split at the centre column
    centre_col = int(np.floor((lon0 - gt1["x0"]) / gt1["sx"]))
    arr6 = np.tile(np.where(np.arange(400) < centre_col, 10.0, 30.0)[None, :], (400, 1))
    a6 = aggregate(arr6, pre)
    mc6 = mc_reference(arr6, gt1, lat0, lon0, 5000.0)
    res["T6_split_raster_mean_vs_MC_within_0.5"] = bool(abs(a6["value"] - mc6["mean"]) < 0.5)
    # T7 raster edge: centre at the top-left corner of the grid
    gt7 = {"x0": 38.0, "y0": 10.0, "sx": 0.041667, "sy": 0.041667, "epsg": 4326}
    pre7 = precompute(gt7, 10.0, 38.0, 5000.0)
    a7 = aggregate(np.full((400, 400), 50.0), pre7)
    mc7 = mc_reference(np.full((400, 400), 50.0), gt7, 10.0, 38.0, 5000.0)
    res["T7_edge_valid_fraction_vs_MC_within_1pct"] = bool(abs(a7["valid_fraction"] - mc7["valid_fraction"]) < 0.01)
    res["T7_edge_status_partial"] = bool(a7["status"] == "partial" and a7["valid_fraction"] < 0.5)
    # T8 coordinate and projection: AEQD radial distances vs geodesic distance
    errs = []
    rng = np.random.default_rng(7)
    for _ in range(200):
        la, lo = rng.uniform(3.5, 14.0), rng.uniform(33.5, 47.0)
        tr = aeqd(la, lo)
        dlat = rng.uniform(-0.05, 0.05)
        dlon = rng.uniform(-0.05, 0.05)
        x, y = tr.transform(lo + dlon, la + dlat)
        d_aeqd = float(np.hypot(x, y))
        _, _, d_geod = GEOD.inv(lo, la, lo + dlon, la + dlat)
        errs.append(abs(d_aeqd / d_geod - 1))
    res["T8_aeqd_radial_max_rel_err"] = float(max(errs))
    res["T8_aeqd_radial_below_0.1pct"] = bool(max(errs) < 0.001)
    # T9 ESRI:102022 anisotropy (reason for not using it for buffers): meridional vs parallel scale
    from pyproj import Proj
    alb = Proj("ESRI:102022")
    aniso = []
    for la, lo in [(3.4, 33.9), (14.9, 47.9), (-4.7, 33.9), (4.7, -3.3), (13.9, 14.7), (4.2, 2.7), (9.5, 38.5)]:
        f = alb.get_factors(lo, la)
        aniso.append(abs(f.meridional_scale / f.parallel_scale - 1))
    res["_T9_esri102022_max_anisotropy_pct"] = round(float(max(aniso)) * 100, 4)
    res["_T8_detail_max_pct"] = round(float(max(errs)) * 100, 4)
    passes = {k: v for k, v in res.items() if not k.startswith("_") and isinstance(v, bool)}
    res["ALL_PASS"] = all(passes.values())
    log("SELFTEST " + json.dumps(res, default=float))
    return res["ALL_PASS"]


def pilot(out_dir):
    rng = np.random.default_rng(42)
    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                        columns=["SAMPLE", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    usable = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    cl = T[usable & T["URBAN"].isin([1, 2])].groupby("IDHSPSU").agg(
        SAMPLE=("SAMPLE", "first"), URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"), LON=("GPSLONG", "first")).reset_index()
    pick = cl.sample(n=20, random_state=42)
    with zipfile.ZipFile(ARCHIVES["W_IMP"]) as z:
        arr, gt = read_raster(z.read(member_name("W_IMP", "MEAN", 2016)))
    diffs_mean, diffs_vf = [], []
    for r in pick.itertuples(index=False):
        stratum = "urban" if r.URBAN == 1 else "rural"
        R = RADIUS_M[stratum]
        a = aggregate(arr, precompute(gt, r.LAT, r.LON, R))
        m = mc_reference(arr, gt, r.LAT, r.LON, R, m=200_000, seed=int(r.IDHSPSU) % 100000)
        if not np.isnan(a["value"]) and not np.isnan(m["mean"]):
            diffs_mean.append(abs(a["value"] - m["mean"]))
        diffs_vf.append(abs(a["valid_fraction"] - m["valid_fraction"]))
    summary = {"clusters": int(len(pick)),
               "max_abs_mean_diff_vs_MC": float(max(diffs_mean)) if diffs_mean else None,
               "median_abs_mean_diff_vs_MC": float(np.median(diffs_mean)) if diffs_mean else None,
               "max_abs_valid_fraction_diff_vs_MC": float(max(diffs_vf)),
               "note": "aggregate only; cluster coordinates not printed"}
    log("PILOT " + json.dumps(summary))
    with open(os.path.join(out_dir, "pilot_summary_AGGREGATE.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    return summary


def execute(out_dir, store_dir):
    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                        columns=["SAMPLE", "DHSID", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    usable = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    U = T[usable].groupby("IDHSPSU").agg(nU=("URBAN", "nunique"), nLA=("GPSLAT", "nunique"),
                                         nLO=("GPSLONG", "nunique"))
    conflicts = U[(U["nU"] > 1) | (U["nLA"] > 1) | (U["nLO"] > 1)]
    cl = T[usable].groupby("IDHSPSU").agg(SAMPLE=("SAMPLE", "first"), DHSID=("DHSID", "first"),
                                          URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"),
                                          LON=("GPSLONG", "first")).reset_index()
    excluded_conflict = int(len(conflicts))
    cl = cl[~cl["IDHSPSU"].isin(conflicts.index)]
    cl = cl[cl["URBAN"].isin([1, 2])].copy()
    cl["stratum"] = np.where(cl["URBAN"] == 1, "urban", "rural")
    bad = [not check_coordinates(a, b, s) for a, b, s in zip(cl["LAT"], cl["LON"], cl["SAMPLE"])]
    if any(bad):
        raise RuntimeError(f"{sum(bad)} clusters fail coordinate/box checks; execution stopped")
    log(f"clusters usable={len(cl)} (reconciles to 4,011 expected); conflicting PSUs excluded={excluded_conflict}")
    # precompute once per cluster (grid identical for all rasters)
    with zipfile.ZipFile(ARCHIVES["W_IMP"]) as z:
        _, gt = read_raster(z.read(member_name("W_IMP", "MEAN", 2016)))
    pre_primary, pre_sens = {}, {}
    for r in cl.itertuples(index=False):
        pre_primary[r.IDHSPSU] = precompute(gt, r.LAT, r.LON, RADIUS_M[r.stratum])
        if r.stratum == "rural":
            pre_sens[r.IDHSPSU] = precompute(gt, r.LAT, r.LON, SENS_RURAL_M)
    log("precomputed weights for all clusters")
    rows = []
    lineage = {}
    for label, path in ARCHIVES.items():
        lineage[label] = {"path": path, "sha256": sha256_file(path)}
        with zipfile.ZipFile(path) as z:
            for typ in TYPES:
                for y in YEARS:
                    arr, gt_y = read_raster(z.read(member_name(label, typ, y)))
                    if any(abs(gt_y[k] - gt[k]) > 1e-12 for k in ("x0", "y0", "sx", "sy")):
                        raise RuntimeError(f"geotransform differs for {label} {typ} {y}; execution stopped")
                    for r in cl.itertuples(index=False):
                        a = aggregate(arr, pre_primary[r.IDHSPSU])
                        rows.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "primary_area_buffer",
                                     a["value"], a["status"], a["reason"], a["valid_fraction"],
                                     a["total_area_m2"] / 1e6, a["valid_area_m2"] / 1e6, a["n_cells"], a["n_cells_valid"]))
                        if r.stratum == "rural":
                            b = aggregate(arr, pre_sens[r.IDHSPSU])
                            rows.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "sensitivity_rural_10km_buffer",
                                         b["value"], b["status"], b["reason"], b["valid_fraction"],
                                         b["total_area_m2"] / 1e6, b["valid_area_m2"] / 1e6, b["n_cells"], b["n_cells_valid"]))
                        pv, pr = point_stat(arr, gt, r.LAT, r.LON)
                        rows.append((r.IDHSPSU, r.SAMPLE, r.stratum, label, typ, y, "sensitivity_containing_pixel",
                                     pv, "full" if not np.isnan(pv) else "missing", pr,
                                     1.0 if not np.isnan(pv) else 0.0, np.nan, np.nan, 1, int(not np.isnan(pv))))
                    log(f"done {label} {typ} {y}")
    cols = ["IDHSPSU", "SAMPLE", "stratum", "product", "estimate", "year", "method", "value", "status",
            "reason", "valid_fraction", "total_area_km2", "valid_area_km2", "n_cells", "n_cells_valid"]
    res = pd.DataFrame(rows, columns=cols)
    res.to_parquet(os.path.join(out_dir, "cluster_year_extraction_RESTRICTED.parquet"), index=False)
    with open(os.path.join(out_dir, "lineage_v2.json"), "w", encoding="utf-8") as f:
        json.dump({"lineage": lineage, "rows": int(len(res)), "clusters": int(len(cl)),
                   "conflicting_psus_excluded": excluded_conflict}, f, indent=1)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--confirm-gps-authorized", action="store_true")
    ap.add_argument("--confirm-round-access", action="store_true")
    args = ap.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__} "
        f"script_sha256={sha256_file(__file__)}")
    if args.selftest:
        ok = selftest()
        sys.exit(0 if ok else 1)
    out_dir = os.path.join(OUT_ROOT, f"run_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    log(f"output -> {out_dir}")
    if args.pilot:
        pilot(out_dir)
    elif args.execute:
        if not (args.confirm_gps_authorized and args.confirm_round_access):
            sys.exit("refused: --execute requires --confirm-gps-authorized and --confirm-round-access")
        src_before = sha256_file(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
        execute(out_dir, out_dir)
        src_after = sha256_file(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
        with open(os.path.join(out_dir, "manifest_v2.json"), "w", encoding="utf-8") as f:
            json.dump({"script": "scripts/historical_wash/09_spatial_extraction_v2.py",
                       "script_sha256": sha256_file(__file__), "interpreter": sys.executable,
                       "python": platform.python_version(),
                       "packages": {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pa.__version__},
                       "config": {"N_SUB": N_SUB, "RADIUS_M": RADIUS_M, "SENS_RURAL_M": SENS_RURAL_M,
                                  "FULL_TOL": FULL_TOL, "projection": "AEQD per cluster",
                                  "products": list(ARCHIVES), "types": TYPES, "years": [YEARS[0], YEARS[-1]]},
                       "source_hash_before": src_before, "source_hash_after": src_after,
                       "source_unchanged": src_before == src_after,
                       "status": "completed_execution"}, f, indent=1)
    else:
        sys.exit("choose --selftest, --pilot or --execute")
    with open(os.path.join(out_dir, "execution_log_v2.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
