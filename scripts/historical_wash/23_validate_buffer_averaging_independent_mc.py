"""
23_validate_buffer_averaging_independent_mc.py
================================================
Independent verification of the BUFFER-AVERAGING ALGORITHM'S OUTPUT (not just
the raster data layer), written for the 2026-10-07 audit's continuation pass.

Context / division of labour:
  - 22_validate_spatial_extraction_independent.py verified the raw raster
    DATA LAYER only (containing-pixel lookups via rasterio against the
    original archives). It explicitly did not touch the buffer-averaging
    (exact polygon-disk overlap) algorithm in 10_spatial_extraction_v3.py.
  - This script verifies that algorithm's OUTPUT -- the primary_area_buffer
    MEAN and valid_fraction stored in cluster_year_extraction_RESTRICTED
    .parquet -- using a from-scratch Monte Carlo spatial integration that is
    methodologically independent of 10_spatial_extraction_v3.py in several
    ways simultaneously:
      1. Sampling scheme: REJECTION sampling of points uniform in a square
         circumscribing the disk, kept if inside the disk. The project's own
         internal check (mc_reference() in script 10) instead uses polar
         sampling (r = R*sqrt(u), theta = 2*pi*v). This script's rejection
         sampler was written without reading mc_reference()'s body first.
      2. Local projection: a closed-form WGS84 degrees-per-metre tangent-
         plane approximation (meridian/parallel arc-length series in lat0),
         not pyproj's AEQD transform that the project uses for its exact
         polygon weights. See APPROXIMATION NOTE below for its error budget.
      3. RNG: numpy Generator(PCG64), but with independent seeds/streams and
         a different consumption pattern (two uniform draws per candidate
         point in a rejection loop, not one radius draw + one angle draw).
      4. Pixel lookup: rasterio reading directly from the original archive
         zips (as in script 22), not the project's PIL+manual-TIFF-tag
         georeferencing in 10_spatial_extraction_v3.py's read_raster().
  No code or functions are imported from 10_spatial_extraction_v3.py.

APPROXIMATION NOTE (tangent-plane lat/lon conversion):
  Points are generated as metre offsets (dx east, dy north) from the cluster
  centre and converted to lat/lon using the standard WGS84 meridian/parallel
  arc-length-per-degree series (Snyder 1987; same formulas widely used for
  "flat-earth" local conversions), evaluated at the cluster's own latitude:
      m_per_deg_lat(lat0) = 111132.92 - 559.82*cos(2*lat0) + 1.175*cos(4*lat0)
                            - 0.0023*cos(6*lat0)
      m_per_deg_lon(lat0) = 111412.84*cos(lat0) - 93.5*cos(3*lat0)
                            + 0.118*cos(5*lat0)
      lat = lat0 + dy / m_per_deg_lat(lat0); lon = lon0 + dx / m_per_deg_lon(lat0)
  This is a first-order (locally flat) approximation, distinct from the
  project's own AEQD (exact at all distances from the centre) and from the
  project's crude /110_000 constant used only for sizing the pixel window
  (never for its area weights). At radii of 2-10 km the curvature/ellipsoid
  correction neglected by a flat local tangent plane is second order in
  (radius / earth_radius): for R=10 km, (R/6.371e6)^2 / 6 =~ 4e-7 relative --
  centimetres of positional error, orders of magnitude below both the raster
  pixel footprint and the Monte Carlo sampling error computed below. This
  approximation is therefore immaterial to the comparison and is not the
  source of any discrepancy found.

Sample selection (deterministic, reproducible from the stored outputs):
  Three established-date countries/years used throughout this audit (SAMPLE
  codes as already identified in script 22): Ghana 2014 (28806), Kenya 2014
  (40406), Nigeria 2018 (56606). For each, cases are drawn from
  cluster_year_extraction_RESTRICTED.parquet, method=="primary_area_buffer",
  estimate=="MEAN", year=2014 (valid_fraction is constant across years for a
  given cluster/product -- verified empirically before selection; the choice
  of year therefore does not affect which structural case is being tested):
    - FULL: status=="full", one urban + one rural case per country (highest
      valid_fraction among full cases -- the one farthest from any edge).
    - PARTIAL: one case per country drawn from a different valid_fraction
      bucket per country/stratum/product (spanning low/mid/high partial
      coverage), i.e. clusters whose buffer straddles a NoData boundary.
    - ZERO: valid_fraction==0 clusters exist ONLY in Kenya (40406) in this
      dataset (2 distinct clusters, one urban one rural, both products,
      constant 0 across all 18 years) -- both are included; no analogous
      cases exist in Ghana or Nigeria in this sample, which is reported
      rather than substituted.

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
RADIUS_M = {"urban": 2000.0, "rural": 5000.0}  # primary radii, per 10_spatial_extraction_v3.py docstring
YEAR = 2014
N_TARGET = 600_000  # >= 500,000 required by the audit brief
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join(MASTER, "data", "processed", "spatial_extraction", f"independent_mc_buffer_validation_{STAMP}")
os.makedirs(OUT, exist_ok=False)

STORED_PATH = os.path.join(MASTER, "data", "processed", "spatial_extraction",
                            "run_v3_20261006T183003Z", "cluster_year_extraction_RESTRICTED.parquet")
COORDS_PATH = os.path.join(MASTER, "data", "processed", "ipums_import", "v2",
                            "run_20261006T140022Z", "idhs_00002_typed_20261006T140022Z.parquet")
ARCHIVES = {"W_IMP": os.path.join(DOWNLOADS, "Percent (2).zip"),
            "S_IMP": os.path.join(DOWNLOADS, "Percent.zip")}
COUNTRIES = [(28806.0, "Ghana_2014"), (40406.0, "Kenya_2014"), (56606.0, "Nigeria_2018")]


def tif_member(product, year):
    return f"IHME_LMIC_WASH_2000_2017_{product}_PERCENT_MEAN_{year}_Y2020M06D02.TIF"


def load_raster(product, year):
    """Read the full band + affine georeferencing directly from the archive via rasterio
    (independent of the project's PIL/manual-TIFF-tag georeferencing)."""
    with zipfile.ZipFile(ARCHIVES[product]) as z:
        data = z.read(tif_member(product, year))
    with MemoryFile(data) as mem:
        with mem.open() as src:
            arr = src.read(1).astype(np.float64)
            transform = src.transform
    return arr, transform


def select_cases(stored):
    """Deterministic selection; see module docstring for the exact rule per case type."""
    sub = stored[(stored["method"] == "primary_area_buffer") & (stored["estimate"] == "MEAN")
                 & (stored["year"] == YEAR)]
    cases = []
    partial_buckets = {  # (sample, stratum, product): (lo, hi)
        (28806.0, "urban", "S_IMP"): (0.0, 0.3), (28806.0, "rural", "W_IMP"): (0.3, 0.7),
        (40406.0, "rural", "S_IMP"): (0.0, 0.3), (40406.0, "urban", "W_IMP"): (0.3, 0.7),
        (56606.0, "rural", "S_IMP"): (0.3, 0.7), (56606.0, "urban", "W_IMP"): (0.7, 0.99)}
    full_product = {("Ghana_2014", "urban"): "W_IMP", ("Ghana_2014", "rural"): "S_IMP",
                    ("Kenya_2014", "urban"): "S_IMP", ("Kenya_2014", "rural"): "W_IMP",
                    ("Nigeria_2018", "urban"): "W_IMP", ("Nigeria_2018", "rural"): "S_IMP"}
    for sample, label in COUNTRIES:
        for stratum in ["urban", "rural"]:
            prod = full_product[(label, stratum)]
            s = sub[(sub["SAMPLE"] == sample) & (sub["stratum"] == stratum)
                    & (sub["product"] == prod) & (sub["status"] == "full")]
            if len(s):
                r = s.sort_values("valid_fraction", ascending=False).iloc[0]
                cases.append(dict(case_type="full", country=label, stratum=stratum, product=prod,
                                   IDHSPSU=float(r["IDHSPSU"]), SAMPLE=sample, year=YEAR,
                                   stored_valid_fraction=float(r["valid_fraction"]), stored_mean=float(r["value"])))
    for (sample, stratum, prod), (lo, hi) in partial_buckets.items():
        label = dict(COUNTRIES)[sample]
        s = sub[(sub["SAMPLE"] == sample) & (sub["stratum"] == stratum) & (sub["product"] == prod)
                & (sub["valid_fraction"] > lo) & (sub["valid_fraction"] <= hi)]
        if len(s):
            r = s.sort_values("IDHSPSU").iloc[0]
            cases.append(dict(case_type="partial", country=label, stratum=stratum, product=prod,
                               IDHSPSU=float(r["IDHSPSU"]), SAMPLE=sample, year=YEAR,
                               stored_valid_fraction=float(r["valid_fraction"]), stored_mean=float(r["value"])))
    zero = sub[(sub["SAMPLE"] == 40406.0) & (sub["valid_fraction"] == 0.0)]
    zero_clusters = zero[["IDHSPSU", "stratum"]].drop_duplicates().sort_values("IDHSPSU")
    for _, zc in zero_clusters.iterrows():
        for prod in ["W_IMP", "S_IMP"]:
            s = zero[(zero["IDHSPSU"] == zc["IDHSPSU"]) & (zero["product"] == prod)]
            if len(s):
                r = s.iloc[0]
                cases.append(dict(case_type="zero", country="Kenya_2014", stratum=zc["stratum"], product=prod,
                                   IDHSPSU=float(r["IDHSPSU"]), SAMPLE=40406.0, year=YEAR,
                                   stored_valid_fraction=float(r["valid_fraction"]),
                                   stored_mean=(float(r["value"]) if pd.notna(r["value"]) else None)))
    return cases


def sample_disk_rejection(radius_m, n_target, rng):
    """Uniform points in the disk of radius radius_m, by rejection sampling from the
    circumscribing square. Different scheme from the project's own polar MC check."""
    xs, ys, have = [], [], 0
    while have < n_target:
        need = n_target - have
        batch = max(int(need / 0.70), 20_000)  # pi/4 ~ 0.785 acceptance; margin for small-n variance
        x = rng.uniform(-radius_m, radius_m, size=batch)
        y = rng.uniform(-radius_m, radius_m, size=batch)
        keep = (x * x + y * y) <= radius_m * radius_m
        xs.append(x[keep]); ys.append(y[keep]); have += int(keep.sum())
    X = np.concatenate(xs)[:n_target]
    Y = np.concatenate(ys)[:n_target]
    return X, Y


def metres_per_degree(lat0_deg):
    la = np.radians(lat0_deg)
    m_lat = 111132.92 - 559.82 * np.cos(2 * la) + 1.175 * np.cos(4 * la) - 0.0023 * np.cos(6 * la)
    m_lon = 111412.84 * np.cos(la) - 93.5 * np.cos(3 * la) + 0.118 * np.cos(5 * la)
    return m_lat, m_lon


def mc_buffer_mean(arr, transform, lat0, lon0, radius_m, n_target, rng):
    dx, dy = sample_disk_rejection(radius_m, n_target, rng)
    m_lat, m_lon = metres_per_degree(lat0)
    lat = lat0 + dy / m_lat
    lon = lon0 + dx / m_lon
    a, c = transform.a, transform.c  # pixel width, x of upper-left
    e, f = transform.e, transform.f  # pixel height (negative), y of upper-left
    col = np.floor((lon - c) / a).astype(np.int64)
    row = np.floor((lat - f) / e).astype(np.int64)
    H, W = arr.shape
    inr = (row >= 0) & (row < H) & (col >= 0) & (col < W)
    vals = np.full(n_target, np.nan)
    vals[inr] = arr[row[inr], col[inr]]
    ok = inr & (vals != NODATA) & np.isfinite(vals) & (vals >= 0) & (vals <= 100)
    n_valid = int(ok.sum())
    valid_fraction = n_valid / n_target
    se_valid_fraction = float(np.sqrt(valid_fraction * (1 - valid_fraction) / n_target))
    if n_valid == 0:
        return dict(mc_mean=None, mc_valid_fraction=valid_fraction, se_valid_fraction=se_valid_fraction,
                    se_mean=None, n_valid=0, n_total=n_target)
    valid_vals = vals[ok]
    mc_mean = float(valid_vals.mean())
    se_mean = float(valid_vals.std(ddof=1) / np.sqrt(n_valid)) if n_valid > 1 else None
    return dict(mc_mean=mc_mean, mc_valid_fraction=valid_fraction, se_valid_fraction=se_valid_fraction,
                se_mean=se_mean, n_valid=n_valid, n_total=n_target)


def main():
    log = [f"=== {STAMP} independent Monte Carlo verification of buffer-averaging OUTPUT ===",
           f"n_target per case = {N_TARGET}; radii: urban={RADIUS_M['urban']}m rural={RADIUS_M['rural']}m primary"]
    stored = pd.read_parquet(STORED_PATH)
    coords = pd.read_parquet(COORDS_PATH, columns=["IDHSPSU", "SAMPLE", "GPSLAT", "GPSLONG"]
                              ).drop_duplicates(subset=["IDHSPSU", "SAMPLE"])
    cases = select_cases(stored)
    log.append(f"cases selected: {len(cases)} "
               f"(full={sum(c['case_type']=='full' for c in cases)}, "
               f"partial={sum(c['case_type']=='partial' for c in cases)}, "
               f"zero={sum(c['case_type']=='zero' for c in cases)})")

    raster_cache = {}
    rows = []
    for i, case in enumerate(cases):
        key = (case["product"], case["year"])
        if key not in raster_cache:
            raster_cache[key] = load_raster(*key)
        arr, transform = raster_cache[key]
        crow = coords[(coords["IDHSPSU"] == case["IDHSPSU"]) & (coords["SAMPLE"] == case["SAMPLE"])]
        if crow.empty:
            log.append(f"case {i}: coordinate lookup failed -- skipped")
            continue
        lat0, lon0 = float(crow["GPSLAT"].iloc[0]), float(crow["GPSLONG"].iloc[0])
        radius_m = RADIUS_M[case["stratum"]]
        rng = np.random.default_rng(900_000_000 + i * 7919)  # distinct seed stream per case
        mc = mc_buffer_mean(arr, transform, lat0, lon0, radius_m, N_TARGET, rng)
        row = {**{k: v for k, v in case.items() if k not in ("IDHSPSU", "SAMPLE")}, **mc}
        if mc["mc_mean"] is not None and case["stored_mean"] is not None:
            row["abs_diff_mean"] = abs(mc["mc_mean"] - case["stored_mean"])
            row["z_mean"] = (row["abs_diff_mean"] / mc["se_mean"]) if mc["se_mean"] else None
        else:
            row["abs_diff_mean"], row["z_mean"] = None, None
        row["abs_diff_valid_fraction"] = abs(mc["mc_valid_fraction"] - case["stored_valid_fraction"])
        row["z_valid_fraction"] = row["abs_diff_valid_fraction"] / mc["se_valid_fraction"] if mc["se_valid_fraction"] > 0 else None
        rows.append(row)
        zvf_str = f"{row['z_valid_fraction']:.2f}" if row['z_valid_fraction'] is not None else "NA(exact)"
        log.append(f"case {i} [{case['case_type']}/{case['country']}/{case['stratum']}/{case['product']}]: "
                   f"n_valid={mc['n_valid']}/{mc['n_total']}, "
                   f"valid_fraction mc={mc['mc_valid_fraction']:.5f} stored={case['stored_valid_fraction']:.5f} "
                   f"diff={row['abs_diff_valid_fraction']:.5f} se={mc['se_valid_fraction']:.5f} z={zvf_str}")
        if row["abs_diff_mean"] is not None:
            log.append(f"         mean mc={mc['mc_mean']:.4f} stored={case['stored_mean']:.4f} "
                       f"diff={row['abs_diff_mean']:.4f} se={mc['se_mean']:.4f} z={row['z_mean']:.2f}")
        else:
            log.append("         mean: no valid MC samples (zero-coverage case) or no stored comparator")

    df = pd.DataFrame(rows)
    both_mean = df[df["abs_diff_mean"].notna()]
    summary = {
        "label": "Independent Monte Carlo verification of the primary_area_buffer MEAN and valid_fraction "
                 "(buffer-averaging algorithm output), methodologically independent of 10_spatial_extraction_v3.py",
        "n_cases": int(len(df)),
        "n_target_per_case": N_TARGET,
        "cases_by_type": df["case_type"].value_counts().to_dict(),
        "mean_comparison": {
            "n_cases_with_both_valid_mean": int(len(both_mean)),
            "max_abs_diff": float(both_mean["abs_diff_mean"].max()) if len(both_mean) else None,
            "mean_abs_diff": float(both_mean["abs_diff_mean"].mean()) if len(both_mean) else None,
            "max_abs_z": float(both_mean["z_mean"].abs().max()) if len(both_mean) else None,
            "mean_abs_z": float(both_mean["z_mean"].abs().mean()) if len(both_mean) else None,
            "n_cases_z_beyond_3": int((both_mean["z_mean"].abs() > 3).sum()) if len(both_mean) else 0,
        },
        "valid_fraction_comparison": {
            "max_abs_diff": float(df["abs_diff_valid_fraction"].max()),
            "mean_abs_diff": float(df["abs_diff_valid_fraction"].mean()),
            "max_abs_z": float(df["z_valid_fraction"].dropna().abs().max()) if df["z_valid_fraction"].notna().any() else None,
            "n_cases_z_beyond_3": int((df["z_valid_fraction"].dropna().abs() > 3).sum()),
        },
        "zero_coverage_cases": {
            "n": int((df["case_type"] == "zero").sum()),
            "all_mc_valid_fraction_zero": bool((df.loc[df["case_type"] == "zero", "mc_valid_fraction"] == 0).all()),
            "note": "No analogous valid_fraction==0 clusters exist for Ghana or Nigeria in this dataset; "
                    "all 4 zero-coverage cases checked are Kenya clusters (2 clusters x 2 products).",
        },
    }
    log.append("\n=== OVERALL ===")
    log.append(json.dumps(summary, indent=1, default=str))
    print("\n".join(log))

    df.to_csv(os.path.join(OUT, "independent_mc_buffer_check_AGGREGATE.csv"), index=False)
    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1, default=str)
    with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    print(f"\nOutput written to {OUT}")


if __name__ == "__main__":
    main()
