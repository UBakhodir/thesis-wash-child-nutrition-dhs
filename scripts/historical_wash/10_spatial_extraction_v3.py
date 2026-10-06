"""
10_spatial_extraction_v3.py
===========================
Cluster-level extraction of IHME modelled WASH coverage (S_IMP, W_IMP; LOWER, MEAN,
UPPER; 2000-2017) around displaced DHS cluster coordinates.

Version history:
  08  first preparation (ESRI:102022; not executed).
  09  AEQD per cluster with sub-sampled pixel overlap. Self-test FAILED: sub-sampling
      error at 1-2 km buffers (up to ~12% at n=12; not monotone in n up to n=48).
      Preserved as a failed version; not used for any output.
  10  (this file) AEQD per cluster with EXACT polygon-disk overlap. Each IHME pixel is
      the quadrilateral of its four projected corners (AEQD centred on the cluster);
      its overlap with the disk of radius R is computed exactly by summing signed
      circle-triangle intersection areas (standard decomposition). No sampling error.

Method (per cluster, per radius):
  - Projection: AEQD centred on the cluster: distance from the centre is exact.
  - Buffer: disk radius R (urban 2 km; rural 5 km primary; rural 10 km sensitivity).
  - Area weight of pixel k: exact area of (pixel quadrilateral intersect disk).
  - Buffer total area = sum over ALL window pixels, including indices outside the raster
    (uncovered). Compared with pi R^2 in the tests.
  - Valid area = weight of pixels inside the raster, not NoData, and within 0..100.
  - Mean = area-weighted mean over valid area (covered area only). Not renormalised to
    full coverage: the valid-area fraction is reported with the status.
  - Status: full (valid/total >= 1 - 1e-3, the numerical tolerance), partial, or missing;
    reasons report outside-raster and NoData area fractions.
  - Point method: containing-pixel rule only (no nearest substitution). NoData -> missing.

Modes:
  --selftest   synthetic rasters checked against analytic values and independent Monte
               Carlo references (random points uniform in the disk, mapped back to lon/lat).
  --pilot      20 real clusters (fixed seed) compared with Monte Carlo on one real raster.
               Aggregate differences only.
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
from pyproj import Geod, Proj, Transformer

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
    if expected_shape is not None and arr.shape != expected_shape:
        raise RuntimeError(f"unexpected shape {arr.shape}")
    tie, scale = t.get(TAG_TIE), t.get(TAG_SCALE)
    gt = {"x0": float(tie[3]), "y0": float(tie[4]), "sx": float(scale[0]), "sy": float(scale[1]), "epsg": epsg}
    return arr, gt


def check_coordinates(lat, lon, sample):
    if not ((-90 <= lat <= 90) and (-180 <= lon <= 180)) or (lat == 0 and lon == 0):
        return False
    la0, la1, lo0, lo1 = NATIONAL_BOX[int(sample)]
    return la0 <= lat <= la1 and lo0 <= lon <= lo1


def aeqd(lat0, lon0):
    return Transformer.from_crs("EPSG:4326",
                                f"+proj=aeqd +lat_0={lat0} +lon_0={lon0} +datum=WGS84 +units=m",
                                always_xy=True)


def window_pixels(gt, lat0, lon0, radius_m):
    """Rows/cols covering the disk; indices may fall outside the raster (uncovered)."""
    dlat = radius_m / 110_000.0 + 2 * abs(gt["sy"])
    dlon = radius_m / (110_000.0 * max(np.cos(np.radians(lat0)), 1e-6)) + 2 * abs(gt["sx"])
    r0 = int(np.floor((gt["y0"] - (lat0 + dlat)) / gt["sy"]))
    r1 = int(np.floor((gt["y0"] - (lat0 - dlat)) / gt["sy"]))
    c0 = int(np.floor(((lon0 - dlon) - gt["x0"]) / gt["sx"]))
    c1 = int(np.floor(((lon0 + dlon) - gt["x0"]) / gt["sx"]))
    rr, cc = np.meshgrid(np.arange(r0, r1 + 1), np.arange(c0, c1 + 1), indexing="ij")
    return rr.ravel(), cc.ravel()


def pixel_corners_ll(gt, rows, cols):
    lon_l = gt["x0"] + cols * gt["sx"]
    lon_r = lon_l + gt["sx"]
    lat_t = gt["y0"] - rows * gt["sy"]
    lat_b = lat_t - gt["sy"]
    return np.stack([np.stack([lon_l, lat_t], -1), np.stack([lon_r, lat_t], -1),
                     np.stack([lon_r, lat_b], -1), np.stack([lon_l, lat_b], -1)], axis=1)


def _seg_circle_area(p, q, r):
    """Signed area of disk(0, r) intersect triangle (0, p, q), vectorised over rows."""
    d = q - p
    A = np.sum(d * d, axis=1)
    B = 2 * np.sum(p * d, axis=1)
    C = np.sum(p * p, axis=1) - r * r
    disc = B * B - 4 * A * C
    area = np.zeros(len(p))
    # breakpoints along the segment: 0, roots in (0,1), 1
    with np.errstate(invalid="ignore", divide="ignore"):
        sq = np.sqrt(np.where(disc >= 0, disc, 0.0))
        t1 = np.where(A > 0, (-B - sq) / (2 * A), 0.0)
        t2 = np.where(A > 0, (-B + sq) / (2 * A), 0.0)
    ts = np.stack([np.zeros(len(p)), np.clip(np.where(disc >= 0, t1, 0.0), 0, 1),
                   np.clip(np.where(disc >= 0, t2, 0.0), 0, 1), np.ones(len(p))], axis=1)
    ts = np.sort(ts, axis=1)
    for i in range(3):
        t_a, t_b = ts[:, i], ts[:, i + 1]
        P = p + t_a[:, None] * d
        Q = p + t_b[:, None] * d
        M = p + 0.5 * (t_a + t_b)[:, None] * d
        seg_len = (t_b - t_a)
        inside_mid = np.sum(M * M, axis=1) <= r * r
        cross = P[:, 0] * Q[:, 1] - P[:, 1] * Q[:, 0]
        dot = np.sum(P * Q, axis=1)
        tri = 0.5 * cross
        sector = 0.5 * r * r * np.arctan2(cross, dot)
        area += np.where(seg_len > 0, np.where(inside_mid, tri, sector), 0.0)
    return area


def polygon_disk_area(poly, r):
    """Exact area of (polygon ∩ disk(0,r)). poly: (P,4,2) in metres, origin at the centre."""
    total = np.zeros(len(poly))
    for i in range(poly.shape[1]):
        total += _seg_circle_area(poly[:, i], poly[:, (i + 1) % poly.shape[1]], r)
    return np.abs(total)


def precompute(gt, lat0, lon0, radius_m):
    """Per-cluster pixel weights (exact area overlap). Independent of product, type and year."""
    rows, cols = window_pixels(gt, lat0, lon0, radius_m)
    corners = pixel_corners_ll(gt, rows, cols)
    tr = aeqd(lat0, lon0)
    x, y = tr.transform(corners[..., 0].ravel(), corners[..., 1].ravel())
    XY = np.stack([x, y], -1).reshape(len(rows), 4, 2)
    w = polygon_disk_area(XY, radius_m)
    pix_area = 0.5 * np.abs(
        (XY[:, 0, 0] * XY[:, 1, 1] - XY[:, 1, 0] * XY[:, 0, 1]) +
        (XY[:, 1, 0] * XY[:, 2, 1] - XY[:, 2, 0] * XY[:, 1, 1]) +
        (XY[:, 2, 0] * XY[:, 3, 1] - XY[:, 3, 0] * XY[:, 2, 1]) +
        (XY[:, 3, 0] * XY[:, 0, 1] - XY[:, 0, 0] * XY[:, 3, 1]))
    # floating-point slivers from pixels that do not overlap the disk are set to zero
    w = np.where(w < 1e-9 * pix_area, 0.0, w)
    return {"rows": rows, "cols": cols, "w": w, "pix_area": pix_area,
            "total_area_m2": float(w.sum())}


def aggregate(arr, pre):
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
    base = {"total_area_m2": total, "valid_area_m2": valid_area, "n_cells": int((w > 0).sum()),
            "n_cells_valid": int((ok & (w > 0)).sum())}
    if valid_area <= 0:
        reason = "outside_raster" if not inr.any() else "nodata"
        return {**base, "value": np.nan, "status": "missing", "reason": reason, "valid_fraction": 0.0}
    mean = float((w[ok] * vals[ok]).sum() / valid_area)
    status = "full" if frac >= 1 - FULL_TOL else "partial"
    reason = "" if status == "full" else f"outside_fraction={out_frac:.4f};nodata_fraction={nodata_frac:.4f}"
    return {**base, "value": mean, "status": status, "reason": reason, "valid_fraction": frac}


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
    a = aggregate(np.full((400, 400), 7.0), precompute(gt, lat0, lon0, 2000.0))
    res["T1_constant_mean_exact"] = bool(abs(a["value"] - 7.0) < 1e-9 and a["status"] == "full")
    # T2/T5 total area vs analytic pi R^2 (exact overlap; tolerance 0.01%) for 1, 2, 5, 10 km
    for R in (1000.0, 2000.0, 5000.0, 10000.0):
        p = precompute(gt, lat0, lon0, R)
        res[f"T2_area_rel_err_R{int(R)}_below_0.01pct"] = bool(abs(p["total_area_m2"] / (np.pi * R * R) - 1) < 1e-4)
    res["T5_small_buffer_few_cells"] = bool((precompute(gt, lat0, lon0, 1000.0)["w"] > 0).sum() <= 9)
    # T3 fractional overlap: mean and valid fraction vs Monte Carlo (two-valued raster)
    pre = precompute(gt, lat0, lon0, 5000.0)
    arr2 = np.arange(400 * 400, dtype=float).reshape(400, 400) % 100
    a2 = aggregate(arr2, pre)
    mc = mc_reference(arr2, gt, lat0, lon0, 5000.0)
    res["T3_mean_vs_MC_within_0.5"] = bool(abs(a2["value"] - mc["mean"]) < 0.5)
    res["T3_valid_fraction_vs_MC_within_0.5pct"] = bool(abs(a2["valid_fraction"] - mc["valid_fraction"]) < 0.005)
    # T4 NoData boundary passes through the buffer centre (NoData on columns left of the centre)
    centre_col = int(np.floor((lon0 - gt["x0"]) / gt["sx"]))
    arr3 = np.full((400, 400), 40.0)
    arr3[:, :centre_col] = NODATA
    a3 = aggregate(arr3, pre)
    mc3 = mc_reference(arr3, gt, lat0, lon0, 5000.0)
    res["T4_nodata_mean_is_valid_value"] = bool(abs(a3["value"] - 40.0) < 1e-9)
    res["T4_nodata_fraction_vs_MC_within_0.5pct"] = bool(abs(a3["valid_fraction"] - mc3["valid_fraction"]) < 0.005)
    res["T4_nodata_status_partial"] = bool(a3["status"] == "partial" and 0 < a3["valid_fraction"] < 1)
    res["T4_all_nodata_is_missing_not_zero"] = bool(np.isnan(aggregate(np.full((400, 400), NODATA), pre)["value"]))
    # T6 buffer crossing cell boundaries with two values split at the centre column
    arr6 = np.tile(np.where(np.arange(400) < centre_col, 10.0, 30.0)[None, :], (400, 1))
    a6 = aggregate(arr6, pre)
    mc6 = mc_reference(arr6, gt, lat0, lon0, 5000.0)
    res["T6_split_raster_mean_vs_MC_within_0.5"] = bool(abs(a6["value"] - mc6["mean"]) < 0.5)
    # T7 raster edge: centre at the top-left corner of the grid
    gt7 = dict(gt)
    pre7 = precompute(gt7, 10.0, 38.0, 5000.0)
    a7 = aggregate(np.full((400, 400), 50.0), pre7)
    mc7 = mc_reference(np.full((400, 400), 50.0), gt7, 10.0, 38.0, 5000.0)
    res["T7_edge_valid_fraction_vs_MC_within_1pct"] = bool(abs(a7["valid_fraction"] - mc7["valid_fraction"]) < 0.01)
    res["T7_edge_status_partial"] = bool(a7["status"] == "partial" and a7["valid_fraction"] < 0.5)
    # T8 AEQD radial distance vs geodesic distance (200 random pairs within 0.05 degrees)
    errs = []
    rng = np.random.default_rng(7)
    for _ in range(200):
        la, lo = rng.uniform(3.5, 14.0), rng.uniform(33.5, 47.0)
        dlat, dlon = rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05)
        x, y = aeqd(la, lo).transform(lo + dlon, la + dlat)
        _, _, d_geod = GEOD.inv(lo, la, lo + dlon, la + dlat)
        errs.append(abs(np.hypot(x, y) / d_geod - 1))
    res["T8_aeqd_radial_below_0.01pct"] = bool(max(errs) < 1e-4)
    res["_T8_max_rel_err"] = float(max(errs))
    # T9 documented anisotropy of ESRI:102022 (the reason it is not used for buffers)
    alb = Proj("ESRI:102022")
    aniso = [abs(alb.get_factors(lo, la).meridional_scale / alb.get_factors(lo, la).parallel_scale - 1)
             for la, lo in [(3.4, 33.9), (14.9, 47.9), (-4.7, 33.9), (4.7, -3.3), (13.9, 14.7), (4.2, 2.7)]]
    res["_T9_esri102022_max_anisotropy_pct"] = round(float(max(aniso)) * 100, 3)
    passes = {k: v for k, v in res.items() if not k.startswith("_") and isinstance(v, bool)}
    res["ALL_PASS"] = bool(all(passes.values()))
    log("SELFTEST " + json.dumps(res, default=float))
    return res["ALL_PASS"]


def pilot(out_dir):
    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                        columns=["SAMPLE", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    usable = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    cl = T[usable & T["URBAN"].isin([1, 2])].groupby("IDHSPSU").agg(
        URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"), LON=("GPSLONG", "first")).reset_index()
    pick = cl.sample(n=20, random_state=42)
    with zipfile.ZipFile(ARCHIVES["W_IMP"]) as z:
        arr, gt = read_raster(z.read(member_name("W_IMP", "MEAN", 2016)))
    dm, dv = [], []
    for r in pick.itertuples(index=False):
        R = RADIUS_M["urban" if r.URBAN == 1 else "rural"]
        a = aggregate(arr, precompute(gt, r.LAT, r.LON, R))
        m = mc_reference(arr, gt, r.LAT, r.LON, R, m=200_000, seed=int(r.IDHSPSU) % 100000)
        if not np.isnan(a["value"]) and not np.isnan(m["mean"]):
            dm.append(abs(a["value"] - m["mean"]))
        dv.append(abs(a["valid_fraction"] - m["valid_fraction"]))
    summary = {"clusters": int(len(pick)),
               "max_abs_mean_diff_vs_MC": float(max(dm)) if dm else None,
               "median_abs_mean_diff_vs_MC": float(np.median(dm)) if dm else None,
               "max_abs_valid_fraction_diff_vs_MC": float(max(dv)),
               "note": "aggregate only; cluster coordinates not printed"}
    log("PILOT " + json.dumps(summary))
    with open(os.path.join(out_dir, "pilot_summary_AGGREGATE.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    return summary


def execute(out_dir):
    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"),
                        columns=["SAMPLE", "DHSID", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    usable = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    U = T[usable].groupby("IDHSPSU").agg(nU=("URBAN", "nunique"), nLA=("GPSLAT", "nunique"),
                                         nLO=("GPSLONG", "nunique"), nS=("SAMPLE", "nunique"))
    conflicts = U[(U["nU"] > 1) | (U["nLA"] > 1) | (U["nLO"] > 1) | (U["nS"] > 1)]
    cl = T[usable].groupby("IDHSPSU").agg(SAMPLE=("SAMPLE", "first"), DHSID=("DHSID", "first"),
                                          URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"),
                                          LON=("GPSLONG", "first")).reset_index()
    cl = cl[~cl["IDHSPSU"].isin(conflicts.index)]
    cl = cl[cl["URBAN"].isin([1, 2])].copy()
    cl["stratum"] = np.where(cl["URBAN"] == 1, "urban", "rural")
    bad = [not check_coordinates(a, b, s) for a, b, s in zip(cl["LAT"], cl["LON"], cl["SAMPLE"])]
    if any(bad):
        raise RuntimeError(f"{sum(bad)} clusters fail coordinate/box checks; execution stopped")
    log(f"clusters usable={len(cl)}; conflicting PSUs excluded={int(len(conflicts))}")
    with zipfile.ZipFile(ARCHIVES["W_IMP"]) as z:
        _, gt = read_raster(z.read(member_name("W_IMP", "MEAN", 2016)))
    pre_primary, pre_sens = {}, {}
    for r in cl.itertuples(index=False):
        pre_primary[r.IDHSPSU] = precompute(gt, r.LAT, r.LON, RADIUS_M[r.stratum])
        if r.stratum == "rural":
            pre_sens[r.IDHSPSU] = precompute(gt, r.LAT, r.LON, SENS_RURAL_M)
    log("precomputed exact overlap weights for all clusters")
    rows, lineage = [], {}
    for label, path in ARCHIVES.items():
        lineage[label] = {"path": path, "sha256": sha256_file(path)}
        with zipfile.ZipFile(path) as z:
            for typ in TYPES:
                for y in YEARS:
                    arr, gt_y = read_raster(z.read(member_name(label, typ, y)))
                    if any(abs(gt_y[k] - gt[k]) > 1e-12 for k in ("x0", "y0", "sx", "sy")):
                        raise RuntimeError(f"geotransform differs for {label} {typ} {y}; stopped")
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
    with open(os.path.join(out_dir, "lineage_v3.json"), "w", encoding="utf-8") as f:
        json.dump({"lineage": lineage, "rows": int(len(res)), "clusters": int(len(cl)),
                   "conflicting_psus_excluded": int(len(conflicts))}, f, indent=1)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--execute", action="store_true")
    ap.add_argument("--confirm-gps-authorized", action="store_true")
    ap.add_argument("--confirm-round-access", action="store_true")
    args = ap.parse_args()
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__} "
        f"script_sha256={sha256_file(__file__)}")
    if args.selftest:
        sys.exit(0 if selftest() else 1)
    if not (args.pilot or args.execute):
        sys.exit("choose --selftest, --pilot or --execute")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(OUT_ROOT, f"run_v3_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    log(f"output -> {out_dir}")
    if args.pilot:
        pilot(out_dir)
    else:
        if not (args.confirm_gps_authorized and args.confirm_round_access):
            sys.exit("refused: --execute requires --confirm-gps-authorized and --confirm-round-access")
        src_before = sha256_file(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
        execute(out_dir)
        src_after = sha256_file(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
        with open(os.path.join(out_dir, "manifest_v3.json"), "w", encoding="utf-8") as f:
            json.dump({"script": "scripts/historical_wash/10_spatial_extraction_v3.py",
                       "script_sha256": sha256_file(__file__), "interpreter": sys.executable,
                       "python": platform.python_version(),
                       "packages": {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pa.__version__},
                       "config": {"RADIUS_M": RADIUS_M, "SENS_RURAL_M": SENS_RURAL_M, "FULL_TOL": FULL_TOL,
                                  "projection": "AEQD per cluster, exact polygon-disk overlap",
                                  "products": list(ARCHIVES), "types": TYPES, "years": [YEARS[0], YEARS[-1]]},
                       "source_hash_before": src_before, "source_hash_after": src_after,
                       "source_unchanged": src_before == src_after, "status": "completed_execution"}, f, indent=1)
    with open(os.path.join(out_dir, "execution_log_v3.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
