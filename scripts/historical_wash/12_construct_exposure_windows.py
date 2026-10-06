"""
12_construct_exposure_windows.py
================================
Child-level historical exposure windows from the validated annual cluster extraction.

Reads read-only:
  - idhs_00002 typed run (validated final run, run_20261006T140022Z)
  - cluster-year extraction (run_v3_20261006T183003Z; MEAN estimate used)
  - Ethiopia provisional candidate dates (audit folder)
Writes a new run directory (restricted, outside the repository).

Definitions (calendar months; CMC = (year - 1900) * 12 + month; b = birth CMC, t = interview CMC):
  birth_year   : the 12 calendar months of the birth year; weight 1 on that year.
  prenatal_9m  : the nine months b-9 .. b-1 (birth month excluded).
  post_12m     : the 12 months b .. b+11 (birth month included).
  post_24m     : the 24 months b .. b+23 (birth month included).
  Annual weight for year y = (months of the window falling in y) / (window months).
  Completion (postnatal windows, month-precision dates): complete iff t >= b + L
    (every window month has ended before the interview month). Sensitivity: t >= b + L + 1,
    because the birth day is unknown and the true birth may be later in the month.
  Raster span: years 2000-2017. A window needing any other year is out of range.
  Post-interview flag: a used annual value for the interview's own calendar year covers
    months after the interview; such exposures are flagged (not altered).

Spatial rules (per annual value; MEAN estimate):
  complete_primary            : every needed annual value has status 'full' (valid-area
                                fraction >= 1 - 1e-3). Primary buffers (urban 2 km, rural 5 km).
  partial_diagnostic_primary  : valid-area means accepted when partial; min valid fraction
                                retained. Diagnostic/sensitivity only; never merged with complete.
  containing_pixel            : containing-pixel value (never nearest-cell substitution).
  rural_10km                  : rural children only (sensitivity buffer).

Ethiopia: three candidate interview-date constructions (C1 triple where valid; C2 century-day
route with 1907 origin; C3 century-day route anchored to 2008 new year). Kept separate and
labelled PROVISIONAL. Non-Ethiopian samples use the Gregorian interview CMC (INTDATECMC).
Birth CMC for all samples: KIDDOBCMC (Gregorian, IPUMS-converted for Ethiopia; month precision).

Modes: default constructs; --selftest runs the temporal tests and the geometry/denominator checks.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import platform
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
RUN_ID = "20261006T140022Z"
TYPED = os.path.join(MASTER, "data", "processed", "ipums_import", "v2", f"run_{RUN_ID}", f"idhs_00002_typed_{RUN_ID}.parquet")
EXTRACT = os.path.join(MASTER, "data", "processed", "spatial_extraction", "run_v3_20261006T183003Z", "cluster_year_extraction_RESTRICTED.parquet")
ET_CAND = os.path.join(MASTER, "data", "processed", "ipums_import", "v2", "ethiopia_calendar_audit_PROVISIONAL_20261006T180523Z", "ET_provisional_dates_RESTRICTED.parquet")
E10 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "10_spatial_extraction_v3.py")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "child_exposure")
YEARS = list(range(2000, 2018))
NY = len(YEARS)
CMC_LO, CMC_HI = 1201, 1416
PRODUCTS = ["W_IMP", "S_IMP"]
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
WINDOWS = {"birth_year": ("birth", 12), "prenatal_9m": ("pre", 9),
           "post_12m": ("post", 12), "post_24m": ("post", 24)}
METHODS = ["complete_primary", "partial_diagnostic_primary", "containing_pixel", "rural_10km"]
EXTRACT_METHOD = {"complete_primary": "primary_area_buffer", "partial_diagnostic_primary": "primary_area_buffer",
                  "containing_pixel": "sensitivity_containing_pixel", "rural_10km": "sensitivity_rural_10km_buffer"}
STATUS_CODE = {"missing": 0, "partial": 1, "full": 2}

log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    log_lines.append(line)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def load_e10():
    spec = importlib.util.spec_from_file_location("e10", E10)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ---------------------------------------------------------------------------
# Annual value arrays
# ---------------------------------------------------------------------------
def build_annual(ex, cluster_ids, product, method):
    pos = {cid: i for i, cid in enumerate(cluster_ids)}
    V = np.full((len(cluster_ids), NY), np.nan)
    VF = np.zeros((len(cluster_ids), NY))
    ST = np.zeros((len(cluster_ids), NY), dtype=np.int8)
    sub = ex[(ex["product"] == product) & (ex["method"] == EXTRACT_METHOD[method])]
    ii = sub["IDHSPSU"].map(pos).values
    yy = sub["year"].values - 2000
    V[ii, yy] = sub["value"].values
    VF[ii, yy] = sub["valid_fraction"].values
    ST[ii, yy] = sub["status"].map(STATUS_CODE).values
    return V, VF, ST


# ---------------------------------------------------------------------------
# Window calculation (vectorised over child-candidate rows)
# ---------------------------------------------------------------------------
def window_calc(b, t, cl, window, V, VF, ST, method):
    kind, L = WINDOWS[window]
    n = len(b)
    ok_b = ~np.isnan(b)
    bb = np.where(ok_b, b, 1300.0)
    if kind == "birth":
        Y = (bb - 1) // 12 + 1900
        s = (Y - 1900) * 12 + 1
    elif kind == "pre":
        s = bb - 9
    else:
        s = bb
    s = s.astype(np.int64)
    y0 = (s - 1) // 12 + 1900
    counts = np.zeros((n, 3), dtype=np.int64)
    for k in range(L):
        j = ((s + k - 1) // 12 + 1900) - y0
        counts[np.arange(n), np.clip(j, 0, 2)] += 1
    expo = np.zeros(n)
    out_range = np.zeros(n, bool)
    any_missing = np.zeros(n, bool)
    complete_all = np.ones(n, bool)
    minfv = np.full(n, np.inf)
    t_year = np.where(np.isnan(t), -1, (np.nan_to_num(t, nan=0) - 1) // 12 + 1900).astype(int)
    post_flag = np.zeros(n, bool)
    clc = np.where(cl >= 0, cl, 0)
    for j in range(3):
        used = counts[:, j] > 0
        yr = y0 + j
        yi = yr - 2000
        inr = (yi >= 0) & (yi < NY)
        out_range |= used & ~inr
        yic = np.clip(yi, 0, NY - 1)
        bad = (cl < 0) | ~inr
        val = np.where(bad, np.nan, V[clc, yic])
        fv = np.where(bad, 0.0, VF[clc, yic])
        st = np.where(bad, 0, ST[clc, yic])
        w = counts[:, j] / L
        expo = np.where(used, expo + w * val, expo)
        any_missing |= used & (np.isnan(val) | (st == 0))
        complete_all &= ~used | (st == 2)
        minfv = np.where(used, np.minimum(minfv, fv), minfv)
        post_flag |= used & (yr == t_year)
    minfv = np.where(np.isfinite(minfv), minfv, np.nan)
    return {"exposure": expo, "out_range": out_range, "any_missing": any_missing,
            "complete_all": complete_all, "min_valid_fraction": minfv, "post_interview_year_used": post_flag,
            "n_years": (counts > 0).sum(axis=1), "s": s, "L": L, "kind": kind}


def eligibility(df, b, t, cl, urban, window, res, method):
    kind, L = WINDOWS[window]
    date_ok = (~np.isnan(b)) & (~np.isnan(t)) & (b >= 1000) & (b <= 1800) & (t >= 1000) & (t <= 1800)
    bnum = np.where(date_ok, b, 0.0)
    tnum = np.where(date_ok, t, 1e9)
    if kind == "post":
        need = bnum + L + 0.0  # completion requires t >= b + L
        incomplete = date_ok & (tnum < need)
    else:
        incomplete = np.zeros(len(b), bool)
    urban_na = (method == "rural_10km") & (urban != 2)
    if method == "partial_diagnostic_primary":
        spatial_missing = res["any_missing"]
        cats = [cl < 0, urban_na, ~date_ok, date_ok & (bnum > tnum), res["out_range"], incomplete, spatial_missing]
        labels = ["unmatched_cluster", "not_applicable_urban", "dates_missing", "birth_after_interview",
                  "window_outside_2000_2017", "postnatal_incomplete", "spatial_missing_year"]
        return np.select(cats, labels, default="eligible_diagnostic")
    cats = [cl < 0, urban_na, ~date_ok, date_ok & (bnum > tnum), res["out_range"], incomplete,
            res["any_missing"], ~res["complete_all"]]
    labels = ["unmatched_cluster", "not_applicable_urban", "dates_missing", "birth_after_interview",
              "window_outside_2000_2017", "postnatal_incomplete", "spatial_missing_year", "spatial_partial_year"]
    return np.select(cats, labels, default="eligible_complete")


# ---------------------------------------------------------------------------
# Child-candidate table
# ---------------------------------------------------------------------------
def build_candidates(typed, et):
    base = typed[["record_number", "SAMPLE", "IDHSPSU", "URBAN", "KIDDOBCMC", "INTDATECMC"]].copy()
    base["b"] = base["KIDDOBCMC"].astype(float)
    nonet = base[base["SAMPLE"] != 23104].copy()
    nonet["candidate"] = "GREGORIAN_ESTABLISHED"
    nonet["t"] = nonet["INTDATECMC"].astype(float)
    et_base = base[base["SAMPLE"] == 23104].merge(et, on="record_number", how="left")
    rows = []
    for cand, col in [("ET_C1_triple_provisional", "C1_CMC"), ("ET_C2_century_1907_provisional", "C2_CMC"),
                      ("ET_C3_century_2015_provisional", "C3_CMC")]:
        x = et_base.copy()
        x["candidate"] = cand
        x["t"] = x[col].astype(float)
        rows.append(x)
    out = pd.concat([nonet] + rows, ignore_index=True)
    out = out[["record_number", "SAMPLE", "IDHSPSU", "URBAN", "b", "t", "candidate"]]
    return out


def load_et_candidates():
    e = pd.read_parquet(ET_CAND)
    def to_cmc(s):
        d = pd.to_datetime(s, errors="coerce")
        return np.where(d.isna(), np.nan, (d.dt.year - 1900) * 12 + d.dt.month)
    out = pd.DataFrame({"record_number": e["record_number"].values,
                        "C1_CMC": to_cmc(e["C1_triple_date_if_valid"]),
                        "C2_CMC": to_cmc(e["C2_origin_1907_date"]),
                        "C3_CMC": e["C3_provisional_CMC"].astype(float).values})
    return out


# ---------------------------------------------------------------------------
# Self tests (temporal, merge-independent) on synthetic inputs
# ---------------------------------------------------------------------------
def cmc(y, m):
    return (y - 1900) * 12 + m


def expected_weights_dt(start_y, start_m, L):
    """Independent: enumerate calendar months with datetime-style arithmetic."""
    counts = {}
    y, m = start_y, start_m
    for _ in range(L):
        counts[y] = counts.get(y, 0) + 1
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return {k: v / L for k, v in counts.items()}


def run_temporal_tests(e10):
    res = {}
    tests = []
    # synthetic annual values: value = calendar year; one cluster; all full
    V = np.tile(np.array([float(y) for y in YEARS]), (1, 1))
    VF = np.ones((1, NY))
    ST = np.full((1, NY), 2, dtype=np.int8)
    def calc(b_cmc, t_cmc, window, V=V, ST=ST):
        r = window_calc(np.array([float(b_cmc)]), np.array([float(t_cmc)]), np.array([0]),
                        window, V, VF, ST, "complete_primary")
        return r
    cases = [
        ("within_one_year_birth_year_Jun2010", cmc(2010, 6), cmc(2014, 1), "birth_year", 2010, 2010.0),
        ("prenatal_within_one_year_Dec2010", cmc(2010, 12), cmc(2014, 1), "prenatal_9m", (2010, 3), None),
        ("span_post12_Jul2010", cmc(2010, 7), cmc(2014, 1), "post_12m", (2010, 7), None),
        ("january_birth_post12_Jan2010", cmc(2010, 1), cmc(2014, 1), "post_12m", (2010, 1), None),
        ("prenatal_span_Feb2010", cmc(2010, 2), cmc(2014, 1), "prenatal_9m", (2009, 5), None),
        ("post24_span_three_years_Mar2010", cmc(2010, 3), cmc(2014, 1), "post_24m", (2010, 3), None),
    ]
    for name, b, t, window, start, _ in cases:
        r = calc(b, t, window)
        kind, L = WINDOWS[window]
        if window == "birth_year":
            wts = {2010: 1.0} if b == cmc(2010, 6) else None
            wts = expected_weights_dt(2010, 1, 12)
        else:
            sy, sm = start if isinstance(start, tuple) else (start, 1)
            wts = expected_weights_dt(sy, sm, L)
        exp_val = sum(w * y for y, w in wts.items())
        got = float(r["exposure"][0])
        ok = abs(got - exp_val) < 1e-9 and abs(sum(wts.values()) - 1.0) < 1e-12
        tests.append({"test": name, "expected": exp_val, "got": got, "pass": bool(ok)})
    # birth near raster end: Dec 2017, post_12m needs 2018 -> out of range
    r = calc(cmc(2017, 12), cmc(2018, 6), "post_12m")
    tests.append({"test": "birth_near_end_post12_Dec2017_out_of_range", "pass": bool(r["out_range"][0])})
    # incomplete postnatal: interview 6 months after birth
    b_arr, t_arr = np.array([float(cmc(2014, 3))]), np.array([float(cmc(2014, 9))])
    st = eligibility(None, b_arr, t_arr, np.array([0]), np.array([1]), "post_12m",
                     window_calc(b_arr, t_arr, np.array([0]), "post_12m", V, VF, ST, "complete_primary"), "complete_primary")
    tests.append({"test": "incomplete_postnatal_flagged", "pass": bool(st[0] == "postnatal_incomplete")})
    # missing annual value in a needed year -> NaN and spatial_missing_year
    Vm = V.copy()
    Vm[0, 2011 - 2000] = np.nan
    STm = ST.copy()
    STm[0, 2011 - 2000] = 0
    r = window_calc(np.array([float(cmc(2010, 7))]), np.array([float(cmc(2014, 1))]), np.array([0]),
                    "post_12m", Vm, VF, STm, "complete_primary")
    st = eligibility(None, np.array([float(cmc(2010, 7))]), np.array([float(cmc(2014, 1))]), np.array([0]),
                     np.array([1]), "post_12m", r, "complete_primary")
    tests.append({"test": "missing_annual_value_no_fill", "pass": bool(np.isnan(r["exposure"][0]) and st[0] == "spatial_missing_year")})
    res["temporal_tests"] = tests
    res["temporal_all_pass"] = bool(all(t["pass"] for t in tests))
    return res


def run_geometry_checks(e10):
    """Geometry and denominator checks on a real raster (aggregate outputs only)."""
    import zipfile
    out = {}
    zipp = os.path.join(r"C:\Users\user\Downloads", "Percent (2).zip")
    with zipfile.ZipFile(zipp) as z:
        arr, gt = e10.read_raster(z.read(e10.member_name("W_IMP", "MEAN", 2016)))
    T = pd.read_parquet(TYPED, columns=["SAMPLE", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG"])
    usable = T["GPSLAT"].notna() & T["GPSLONG"].notna() & ~((T["GPSLAT"] == 0) & (T["GPSLONG"] == 0))
    cl = T[usable & T["URBAN"].isin([1, 2])].groupby("IDHSPSU").agg(URBAN=("URBAN", "first"), LAT=("GPSLAT", "first"), LON=("GPSLONG", "first")).reset_index()
    pick = cl.sample(n=min(150, len(cl)), random_state=11)
    dense_err_area, dense_err_mean, valid_frac_diff, pix_area_err = [], [], [], []
    alt_total_diff = []
    partial_count = 0
    for r in pick.itertuples(index=False):
        R = e10.RADIUS_M["urban" if r.URBAN == 1 else "rural"]
        pre = e10.precompute(gt, r.LAT, r.LON, R)
        a = e10.aggregate(arr, pre)
        if a["status"] == "partial":
            partial_count += 1
            # alternative (wrong) denominator: total buffer area, NoData treated as zero
            r_, c_ = pre["rows"], pre["cols"]
            H, W = arr.shape
            inr = (r_ >= 0) & (r_ < H) & (c_ >= 0) & (c_ < W)
            vals = np.full(len(r_), np.nan)
            vals[inr] = arr[r_[inr], c_[inr]]
            ok = inr & (vals != e10.NODATA) & np.isfinite(vals) & (vals >= 0) & (vals <= 100)
            wrong = float((pre["w"][ok] * vals[ok]).sum() / pre["total_area_m2"])
            if a["value"] is not None and not np.isnan(a["value"]):
                alt_total_diff.append(abs(wrong - a["value"]))
        # densified pixel boundaries (16 points per edge, straight in lon/lat before projection)
        dense = dense_precompute(gt, r.LAT, r.LON, R, K=16, e10=e10)
        b_ = e10.aggregate(arr, dense)
        if not np.isnan(a["value"]) and not np.isnan(b_["value"]):
            dense_err_mean.append(abs(a["value"] - b_["value"]))
        dense_err_area.append(abs(dense["total_area_m2"] / (np.pi * R * R) - 1))
        # per-pixel geometric error: straight corner-to-corner edges vs densified edges (same pixels)
        pa_s = pre["pix_area"]
        pa_d = dense["pix_area"]
        mask = pa_s > 0
        if mask.any():
            pix_area_err.extend(np.abs(pa_d[mask] / pa_s[mask] - 1).tolist())
        valid_frac_diff.append(abs(a["valid_fraction"] - b_["valid_fraction"]))
    out["geometry_clusters_tested"] = int(len(pick))
    out["note_total_area_is_tautological"] = "adjacent pixels share corners, so totals tile the disk for either edge model"
    out["straight_vs_densified_pixel_area_rel_err_median"] = float(np.median(pix_area_err))
    out["straight_vs_densified_pixel_area_rel_err_p99"] = float(np.percentile(pix_area_err, 99))
    out["straight_vs_densified_pixel_area_rel_err_max"] = float(np.max(pix_area_err))
    out["straight_vs_densified_total_area_rel_err_max"] = float(max(dense_err_area))
    out["straight_vs_densified_mean_abs_diff_max"] = float(max(dense_err_mean)) if dense_err_mean else None
    out["straight_vs_densified_mean_abs_diff_median"] = float(np.median(dense_err_mean)) if dense_err_mean else None
    out["straight_vs_densified_valid_fraction_diff_max"] = float(max(valid_frac_diff))
    out["partial_buffers_in_test"] = int(partial_count)
    out["mean_formula_vs_total_area_denominator_diff_max"] = float(max(alt_total_diff)) if alt_total_diff else None
    out["mean_formula_vs_total_area_denominator_diff_median"] = float(np.median(alt_total_diff)) if alt_total_diff else None
    return out


def dense_precompute(gt, lat0, lon0, radius_m, K, e10):
    rows, cols = e10.window_pixels(gt, lat0, lon0, radius_m)
    corners = e10.pixel_corners_ll(gt, rows, cols)  # (P,4,2) lon,lat
    seg = []
    for i in range(4):
        p, q = corners[:, i], corners[:, (i + 1) % 4]
        for k in range(K):
            t = k / K
            seg.append(p * (1 - t) + q * t)
    ll = np.stack(seg, axis=1)  # (P, 4K, 2)
    tr = e10.aeqd(lat0, lon0)
    x, y = tr.transform(ll[..., 0].ravel(), ll[..., 1].ravel())
    XY = np.stack([x, y], -1).reshape(len(rows), 4 * K, 2)
    w = e10.polygon_disk_area(XY, radius_m)
    # shoelace area of densified polygon
    xs, ys = XY[..., 0], XY[..., 1]
    area = 0.5 * np.abs(np.sum(xs * np.roll(ys, -1, axis=1) - np.roll(xs, -1, axis=1) * ys, axis=1))
    w = np.where(w < 1e-9 * np.maximum(area, 1e-9), 0.0, w)
    return {"rows": rows, "cols": cols, "w": w, "pix_area": area, "total_area_m2": float(w.sum())}


# ---------------------------------------------------------------------------
# Main construction
# ---------------------------------------------------------------------------
def construct(out_dir):
    typed = pd.read_parquet(TYPED, columns=["record_number", "SAMPLE", "IDHSPSU", "URBAN", "KIDDOBCMC", "INTDATECMC",
                                            "INTYEAR", "HWHAZWHO", "HWWAZWHO", "HWWHZWHO", "LINENOKID", "KIDCURAGEMO",
                                            "PERWEIGHT", "KIDWT"])
    log(f"typed child records={len(typed)}; unique record_number={typed['record_number'].is_unique}")
    ex = pd.read_parquet(EXTRACT, columns=["IDHSPSU", "SAMPLE", "stratum", "product", "estimate", "year", "method",
                                           "value", "status", "valid_fraction"])
    ex = ex[ex["estimate"] == "MEAN"]
    cluster_ids = sorted(ex.loc[ex["method"] == "primary_area_buffer", "IDHSPSU"].unique())
    log(f"extraction MEAN rows={len(ex)}; primary clusters={len(cluster_ids)}")
    et = load_et_candidates()
    cand = build_candidates(typed, et)
    log(f"child-candidate rows={len(cand)} (non-ET {int((cand.candidate=='GREGORIAN_ESTABLISHED').sum())})")
    cpos = {cid: i for i, cid in enumerate(cluster_ids)}
    cl_all = cand["IDHSPSU"].map(cpos).fillna(-1).astype(int).values
    b = cand["b"].values
    t = cand["t"].values
    urban = cand["URBAN"].values
    cand_name = cand["candidate"].values
    result = cand[["record_number", "SAMPLE", "IDHSPSU", "URBAN", "candidate", "b", "t"]].copy()
    result["cluster_index"] = cl_all
    result["birth_cmc"] = b
    result["interview_cmc"] = t
    result["age_months_cal"] = t - b
    result["date_ok"] = (~np.isnan(b)) & (~np.isnan(t))
    summaries = []
    cov_rows = []
    for product in PRODUCTS:
        for method in METHODS:
            pass
    for product in PRODUCTS:
        V, VF, ST = build_annual(ex, cluster_ids, product, "complete_primary")
        Vpt, VFpt, STpt = build_annual(ex, cluster_ids, product, "containing_pixel")
        Vr, VFr, STr = build_annual(ex, cluster_ids, product, "rural_10km")
        for window in WINDOWS:
            # complete primary
            res_c = window_calc(b, t, cl_all, window, V, VF, ST, "complete_primary")
            st_c = eligibility(None, b, t, cl_all, urban, window, res_c, "complete_primary")
            res_d = window_calc(b, t, cl_all, window, V, VF, ST, "partial_diagnostic_primary")
            st_d = eligibility(None, b, t, cl_all, urban, window, res_d, "partial_diagnostic_primary")
            res_p = window_calc(b, t, cl_all, window, Vpt, VFpt, STpt, "containing_pixel")
            st_p = eligibility(None, b, t, cl_all, urban, window, res_p, "containing_pixel")
            res_r = window_calc(b, t, cl_all, window, Vr, VFr, STr, "rural_10km")
            st_r = eligibility(None, b, t, cl_all, urban, window, res_r, "rural_10km")
            p = f"{product}_{window}"
            result[f"{p}_complete_exposure"] = np.where(st_c == "eligible_complete", res_c["exposure"], np.nan)
            result[f"{p}_complete_status"] = st_c
            result[f"{p}_partial_diag_exposure"] = np.where(st_d == "eligible_diagnostic", res_d["exposure"], np.nan)
            result[f"{p}_partial_diag_status"] = st_d
            result[f"{p}_partial_diag_min_valid_fraction"] = res_d["min_valid_fraction"]
            result[f"{p}_containing_exposure"] = np.where(st_p == "eligible_complete", res_p["exposure"], np.nan)
            result[f"{p}_containing_status"] = st_p
            result[f"{p}_rural10_exposure"] = np.where(st_r == "eligible_complete", res_r["exposure"], np.nan)
            result[f"{p}_rural10_status"] = st_r
            result[f"{p}_post_interview_year_used"] = res_c["post_interview_year_used"]
            result[f"{p}_min_valid_fraction_complete"] = res_c["min_valid_fraction"]
            result[f"{p}_n_years"] = res_c["n_years"]
            log(f"constructed {product} {window}")
    # Complete-timing (window within raster and completion) flags, independent of spatial rule
    result.to_parquet(os.path.join(out_dir, "child_exposure_candidates_RESTRICTED.parquet"), index=False)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha256_file(__file__)}")
    e10 = load_e10()
    if args.selftest:
        t = run_temporal_tests(e10)
        for x in t["temporal_tests"]:
            log(f"TEST {json.dumps(x, default=float)}")
        log(f"temporal_all_pass={t['temporal_all_pass']}")
        g = run_geometry_checks(e10)
        log("GEOMETRY " + json.dumps(g, default=float))
        out_dir = os.path.join(OUT_ROOT, f"selftest_{stamp}")
        os.makedirs(out_dir, exist_ok=False)
        with open(os.path.join(out_dir, "validation_AGGREGATE.json"), "w", encoding="utf-8") as f:
            json.dump({"temporal": t, "geometry": g}, f, indent=1, default=float)
        with open(os.path.join(out_dir, "validation_log.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(log_lines) + "\n")
        sys.exit(0 if t["temporal_all_pass"] else 1)
    out_dir = os.path.join(OUT_ROOT, f"run_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    src_before = {"typed": sha256_file(TYPED), "extract": sha256_file(EXTRACT), "et": sha256_file(ET_CAND)}
    result = construct(out_dir)
    src_after = {"typed": sha256_file(TYPED), "extract": sha256_file(EXTRACT), "et": sha256_file(ET_CAND)}
    with open(os.path.join(out_dir, "execution_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"script": "scripts/historical_wash/12_construct_exposure_windows.py",
                   "script_sha256": sha256_file(__file__), "interpreter": sys.executable,
                   "python": platform.python_version(),
                   "packages": {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pa.__version__},
                   "inputs_before": src_before, "inputs_after": src_after,
                   "inputs_unchanged": src_before == src_after,
                   "rows": int(len(result)), "status": "completed_construction"}, f, indent=1)


if __name__ == "__main__":
    main()
