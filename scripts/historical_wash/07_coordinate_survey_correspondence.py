"""
07_coordinate_survey_correspondence.py
======================================
Aggregate-only checks linking the GPS cluster coordinates in the validated
idhs_00002 extract to their survey, and a household-level measurement-design
diagnostic. Reads the final validated run read-only; writes a new output folder
outside the tracked repository. No coordinate values or identifiers are printed.

Checks:
  A. DHSID structure: the DHS documentation defines DHSID as a 2-character
     country code, a 4-digit survey year and an 8-digit cluster number. The
     country code and year must match the sample; the cluster number must be
     consistent with IDHSPSU (one DHSID per PSU).
  B. Approximate national bounding-box sanity check on usable coordinates.
     Boxes are coarse, hand-set and used only to flag gross errors; a point
     just outside a box can be correct near a border.
  C. Household measured share by PSU (listed children): spread across clusters,
     for the one-third household design check.
"""
import hashlib
import json
import os
import platform
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
BASE = os.path.join(MASTER, "data", "processed", "ipums_import", "v2")
RUN_ID = "20261006T140022Z"
RUN = os.path.join(BASE, f"run_{RUN_ID}")
SAMPLES = {
    23104: ("ET2016", "ET", 2016, (3.4, 14.9, 33.0, 48.0)),   # lat_min, lat_max, lon_min, lon_max (approx)
    28806: ("GH2014", "GH", 2014, (4.7, 11.2, -3.3, 1.2)),
    40406: ("KE2014", "KE", 2014, (-4.7, 5.0, 33.9, 41.9)),
    56606: ("NG2018", "NG", 2018, (4.2, 13.9, 2.7, 14.7)),
}
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


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUT = os.path.join(BASE, f"coordinate_correspondence_{stamp}")
    os.makedirs(OUT, exist_ok=False)
    R = lambda f: os.path.join(OUT, f)
    src_name = f"idhs_00002_typed_{RUN_ID}.parquet"
    before = sha256_file(os.path.join(RUN, src_name))
    log(f"output -> {OUT}; python={platform.python_version()} pandas={pd.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha256_file(__file__)}")

    T = pd.read_parquet(os.path.join(RUN, src_name), columns=[
        "SAMPLE", "DHSID", "IDHSPSU", "GPSLAT", "GPSLONG", "LINENOKID", "HWHAZWHO", "IDHSHID"])
    T["DHSID"] = T["DHSID"].astype(str).str.strip()

    # ---- A. DHSID structure
    a_rows = []
    for sid, (lab, cc, yr, _) in SAMPLES.items():
        g = T[T["SAMPLE"] == sid]
        d = g["DHSID"]
        ok_len = d.str.len() == 14
        ok_cc = d.str[:2] == cc
        ok_yr = d.str[2:6] == str(yr)
        ok_num = d.str[6:].str.fullmatch(r"\d{8}")
        ok_all = ok_len & ok_cc & ok_yr & ok_num.fillna(False)
        psu_map = g.groupby("IDHSPSU")["DHSID"].nunique()
        dhs_map = g.groupby("DHSID")["IDHSPSU"].nunique()
        a_rows.append({
            "sample": lab, "rows": int(len(g)),
            "DHSID_length_14": int(ok_len.sum()),
            "country_code_matches": int(ok_cc.sum()),
            "survey_year_matches": int(ok_yr.sum()),
            "cluster_number_8_digits": int(ok_num.fillna(False).sum()),
            "all_components_match": int(ok_all.sum()),
            "rows_failing": int((~ok_all).sum()),
            "PSUs_with_multiple_DHSID": int((psu_map > 1).sum()),
            "DHSIDs_with_multiple_PSU": int((dhs_map > 1).sum()),
            "distinct_DHSID": int(d.nunique()),
            "distinct_PSU": int(g["IDHSPSU"].nunique()),
        })
    a_df = pd.DataFrame(a_rows)
    a_df.to_csv(R("A_dhsid_structure_v2.csv"), index=False)
    log("A. DHSID structure:\n" + a_df.to_string(index=False))

    # ---- B. approximate bounding-box sanity on usable coordinates (counts only)
    b_rows = []
    for sid, (lab, cc, yr, (la0, la1, lo0, lo1)) in SAMPLES.items():
        g = T[T["SAMPLE"] == sid]
        la, lo = g["GPSLAT"], g["GPSLONG"]
        usable = la.notna() & lo.notna() & ~((la == 0) & (lo == 0))
        inside = usable & la.between(la0, la1) & lo.between(lo0, lo1)
        psu_u = g.loc[usable, "IDHSPSU"].nunique()
        psu_out = g.loc[usable & ~inside, "IDHSPSU"].nunique()
        b_rows.append({
            "sample": lab, "usable_rows": int(usable.sum()), "usable_rows_inside_box": int(inside.sum()),
            "usable_rows_outside_box": int((usable & ~inside).sum()),
            "share_inside_box": round(float(inside.sum() / max(usable.sum(), 1)), 4),
            "PSUs_with_usable_coordinates": int(psu_u), "PSUs_with_any_point_outside_box": int(psu_out),
            "box_lat_lon": f"{la0}..{la1} / {lo0}..{lo1} (approximate; sanity only)",
        })
    b_df = pd.DataFrame(b_rows)
    b_df.to_csv(R("B_bounding_box_sanity_v2.csv"), index=False)
    log("B. bounding-box sanity:\n" + b_df.to_string(index=False))

    # ---- C. PSU-level measured share among listed children (design diagnostic)
    c_rows = []
    for sid, (lab, _, _, _) in SAMPLES.items():
        g = T[(T["SAMPLE"] == sid) & (T["LINENOKID"] > 0)].copy()
        g["measured"] = g["HWHAZWHO"].notna() & (g["HWHAZWHO"] < 9995)
        hh = g.groupby(["IDHSPSU", "IDHSHID"])["measured"].any()
        psu_share = hh.groupby("IDHSPSU").mean()
        c_rows.append({
            "sample": lab, "households_with_listed_children": int(len(hh)),
            "household_measured_share": round(float(hh.mean()), 4),
            "PSUs": int(len(psu_share)),
            "PSU_share_mean": round(float(psu_share.mean()), 4),
            "PSU_share_sd": round(float(psu_share.std()), 4),
            "PSUs_with_zero_measured_households": int((psu_share == 0).sum()),
            "PSUs_with_all_households_measured": int((psu_share == 1).sum()),
        })
    c_df = pd.DataFrame(c_rows)
    c_df.to_csv(R("C_psu_household_measurement_v2.csv"), index=False)
    log("C. PSU-level measurement:\n" + c_df.to_string(index=False))

    after = sha256_file(os.path.join(RUN, src_name))
    manifest = {
        "run_id": os.path.basename(OUT), "completed_utc": datetime.now(timezone.utc).isoformat(),
        "script": "scripts/historical_wash/07_coordinate_survey_correspondence.py",
        "script_sha256": sha256_file(__file__), "interpreter": sys.executable,
        "source": src_name, "source_unchanged": before == after,
        "authorization_source": "DHS Program dataset account screenshot (restricted local copy); see authorization note",
    }
    with open(R("manifest_v2.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    with open(R("execution_log_v2.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"source unchanged: {manifest['source_unchanged']}")


if __name__ == "__main__":
    main()
