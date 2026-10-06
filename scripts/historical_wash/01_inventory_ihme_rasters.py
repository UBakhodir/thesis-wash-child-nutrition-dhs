"""
01_inventory_ihme_rasters.py
============================
Read-only inventory of the IHME LMIC WASH annual GeoTIFF archives used for the
historical-WASH extension. Reads zip members in memory; never extracts into the
repository. Writes a manifest and log to a versioned directory OUTSIDE the
tracked repository.

Inputs (read-only, must exist, script fails loudly otherwise):
  Downloads/Percent.zip      S_IMP PERCENT (LOWER/MEAN/UPPER, 2000-2017)
  Downloads/Percent (2).zip  W_IMP PERCENT (LOWER/MEAN/UPPER, 2000-2017)

Outputs (new, versioned, not canonical):
  <MASTER>/data/processed/historical_wash/v1/ihme_raster_inventory_v1.csv
  <MASTER>/data/processed/historical_wash/v1/ihme_raster_inventory_v1.log
"""
import csv
import hashlib
import io
import os
import platform
import sys
import zipfile
from datetime import datetime, timezone

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

DOWNLOADS = r"C:\Users\user\Downloads"
MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
OUT_DIR = os.path.join(MASTER, "data", "processed", "historical_wash", "v1")

ARCHIVES = [
    ("S_IMP", os.path.join(DOWNLOADS, "Percent.zip")),
    ("W_IMP", os.path.join(DOWNLOADS, "Percent (2).zip")),
]
YEARS = list(range(2000, 2018))
TYPES = ["LOWER", "MEAN", "UPPER"]
GEOKEY_GEOGRAPHIC = 2048
GEOKEY_TYPE = 1024
EXPECTED_SHAPE = (2123, 6610)  # (height, width)
EXPECTED_NODATA = -999999.0

log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line)
    log_lines.append(line)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def member_name(product, typ, year):
    return (f"IHME_LMIC_WASH_2000_2017_{product}_PERCENT_{typ}_{year}_"
            f"Y2020M06D02.TIF")


def tiff_meta(im):
    t = im.tag_v2
    gk = list(t.get(34735, ()))
    epsg = None
    for i in range(0, len(gk), 4):
        if gk[i] == GEOKEY_GEOGRAPHIC:
            epsg = gk[i + 3]
    tie = t.get(33922)
    scale = t.get(33550)
    nodata = t.get(42113)
    nodata = float(nodata) if nodata is not None else None
    stats = {}
    meta_xml = t.get(42112, "")
    for key in ("STATISTICS_MINIMUM", "STATISTICS_MAXIMUM", "STATISTICS_MEAN"):
        tag = f'name="{key}"'
        if tag in meta_xml:
            seg = meta_xml.split(tag, 1)[1]
            stats[key] = float(seg.split(">", 1)[1].split("<", 1)[0])
    return {
        "epsg": epsg,
        "pixel_x_deg": scale[0] if scale else None,
        "pixel_y_deg": scale[1] if scale else None,
        "tiepoint_lon": tie[3] if tie else None,
        "tiepoint_lat": tie[4] if tie else None,
        "nodata": nodata,
        "sample_format_tag": t.get(339),
        "bits_per_sample": t.get(258),
        "stats_gdal": stats,
    }


def main():
    for label, path in ARCHIVES:
        if not os.path.isfile(path):
            log(f"FATAL missing input archive for {label}: {path}")
            sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_csv = os.path.join(OUT_DIR, "ihme_raster_inventory_v1.csv")
    if os.path.exists(out_csv):
        log(f"FATAL output already exists, refusing to overwrite: {out_csv}")
        sys.exit(1)

    log(f"python={platform.python_version()} numpy={np.__version__} "
        f"pillow={Image.__version__}")
    rows = []
    for product, path in ARCHIVES:
        digest = sha256_file(path)
        log(f"archive {product}: {os.path.basename(path)} "
            f"bytes={os.path.getsize(path)} sha256={digest}")
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            for typ in TYPES:
                for year in YEARS:
                    mn = member_name(product, typ, year)
                    if mn not in names:
                        log(f"FATAL missing member {mn} in {os.path.basename(path)}")
                        sys.exit(1)
                    data = z.read(mn)
                    im = Image.open(io.BytesIO(data))
                    meta = tiff_meta(im)
                    arr = np.asarray(im, dtype=np.float64)
                    shape_ok = arr.shape == EXPECTED_SHAPE
                    nd = meta["nodata"] if meta["nodata"] is not None else EXPECTED_NODATA
                    valid = arr[arr != nd]
                    valid = valid[np.isfinite(valid)]
                    rows.append({
                        "product": product,
                        "estimate": typ,
                        "year": year,
                        "member": mn,
                        "archive": os.path.basename(path),
                        "archive_sha256": digest,
                        "height": arr.shape[0],
                        "width": arr.shape[1],
                        "shape_matches_reference": shape_ok,
                        "epsg": meta["epsg"],
                        "pixel_x_deg": meta["pixel_x_deg"],
                        "pixel_y_deg": meta["pixel_y_deg"],
                        "tiepoint_lon": meta["tiepoint_lon"],
                        "tiepoint_lat": meta["tiepoint_lat"],
                        "nodata_value": nd,
                        "nodata_is_expected": nd == EXPECTED_NODATA,
                        "n_pixels": arr.size,
                        "n_valid": int(valid.size),
                        "valid_fraction": round(valid.size / arr.size, 6),
                        "value_min_valid": float(valid.min()) if valid.size else None,
                        "value_max_valid": float(valid.max()) if valid.size else None,
                        "value_mean_valid": float(valid.mean()) if valid.size else None,
                        "outside_0_100_count": int(((valid < 0) | (valid > 100)).sum()),
                        "gdal_stats_present": bool(meta["stats_gdal"]),
                    })
                    im.close()
                    log(f"{product} {typ} {year}: shape_ok={shape_ok} "
                        f"epsg={meta['epsg']} valid_frac={rows[-1]['valid_fraction']} "
                        f"outside_0_100={rows[-1]['outside_0_100_count']}")

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    log(f"wrote {len(rows)} rows -> {out_csv}")

    grids = {(r["height"], r["width"], r["pixel_x_deg"], r["pixel_y_deg"],
              r["tiepoint_lon"], r["tiepoint_lat"], r["epsg"]) for r in rows}
    log(f"distinct grid signatures across all {len(rows)} rasters: {len(grids)} "
        f"(1 = fully aligned)")
    log(f"all shapes match reference: {all(r['shape_matches_reference'] for r in rows)}")
    log(f"all nodata expected: {all(r['nodata_is_expected'] for r in rows)}")
    log(f"total outside_0_100 values: {sum(r['outside_0_100_count'] for r in rows)}")

    with open(os.path.join(OUT_DIR, "ihme_raster_inventory_v1.log"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
