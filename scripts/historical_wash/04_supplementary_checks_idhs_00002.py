"""
04_supplementary_checks_idhs_00002.py
=====================================
Aggregate-only supplementary checks on the derived idhs_00002 dataset produced by
03_import_validate_idhs_00002.py. Writes new CSV tables to a separate directory
(never inside an existing run directory). No respondent-level rows, identifiers
or coordinates are printed.

Usage: python 04_supplementary_checks_idhs_00002.py <run_dir>
"""
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    sys.exit("usage: 04_supplementary_checks_idhs_00002.py <run_dir>")
RUN = sys.argv[1]
RUN_ID = os.path.basename(RUN).replace("run_", "")
OUT = os.path.join(os.path.dirname(RUN), f"supplementary_{RUN_ID}")
os.makedirs(OUT, exist_ok=False)
SAMPLE_OF = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}

typed = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
derived = pd.read_parquet(os.path.join(RUN, f"idhs_00002_derived_{RUN_ID}.parquet"))
typed["sample"] = typed["SAMPLE"].map(lambda v: SAMPLE_OF.get(int(v), "UNEXPECTED"))
derived["sample"] = typed["sample"].values
log = []


def note(msg):
    print(f"{datetime.now(timezone.utc).isoformat()} {msg}", flush=True)
    log.append(msg)


# A. Non-measurement (NIU for HAZ) against LINENOKID (not listed in household = 00)
rows = []
for s, g in typed.groupby("sample"):
    niu = g["HWHAZWHO"] == 9999
    not_listed = g["LINENOKID"] == 0
    rows.append({
        "sample": s, "rows": len(g),
        "HAZ_NIU": int(niu.sum()),
        "HAZ_NIU_and_not_listed_in_household": int((niu & not_listed).sum()),
        "HAZ_NIU_and_listed_in_household": int((niu & g["LINENOKID"].notna() & ~not_listed).sum()),
        "not_listed_in_household_total": int(not_listed.sum()),
        "HAZ_measured_and_listed": int(((g["HWHAZWHO"].notna() & (g["HWHAZWHO"] < 9995)) &
                                        ~not_listed).sum()),
        "HAZ_measured_and_not_listed": int(((g["HWHAZWHO"].notna() & (g["HWHAZWHO"] < 9995)) &
                                            not_listed).sum()),
    })
pd.DataFrame(rows).to_csv(os.path.join(OUT, "niu_vs_linenokid_v2.csv"), index=False)
note("A. NIU vs LINENOKID written")

# B. GPSLATLONG relation to GPSLAT and GPSLONG (no coordinate values printed)
rows = []
for s, g in typed.groupby("sample"):
    la, lo, ll = g["GPSLAT"], g["GPSLONG"], g["GPSLATLONG"]
    both = la.notna() & lo.notna()
    rows.append({
        "sample": s, "rows": len(g),
        "GPSLATLONG_equals_GPSLAT": int((np.isclose(ll, la) & ll.notna()).sum()),
        "GPSLATLONG_equals_GPSLONG": int((np.isclose(ll, lo) & ll.notna()).sum()),
        "GPSLATLONG_equals_GPSLAT_and_zero_pair": int((np.isclose(ll, la) & (la == 0) & (lo == 0)).sum()),
        "GPSLATLONG_nonzero_rows": int((ll != 0).sum()),
        "GPSLATLONG_abs_gt_90": int((ll.abs() > 90).sum()),
        "GPSLATLONG_abs_gt_180": int((ll.abs() > 180).sum()),
        "GPSLATLONG_is_integer_valued": int((ll.dropna() % 1 == 0).sum()),
        "GPSLATLONG_abs_gt_GPSLONG_abs_rows": int((ll.abs() > lo.abs()).sum()) if both.any() else None,
    })
pd.DataFrame(rows).to_csv(os.path.join(OUT, "gpslatlong_relation_v2.csv"), index=False)
note("B. GPSLATLONG relation written")

# C. ET calendar age difference outliers: direction only
et = derived[derived["sample"] == "ET2016"].copy()
et_k = typed.loc[typed["sample"] == "ET2016"]
diff_et = (typed.loc[typed["sample"] == "ET2016", "INTDATECMC_ET"] -
           typed.loc[typed["sample"] == "ET2016", "KIDDOBCMC_ET"]) - \
          typed.loc[typed["sample"] == "ET2016", "KIDCURAGEMO"]
rows = [{"sample": "ET2016", "rows_with_both": int(diff_et.notna().sum()),
         "diff_eq0": int((diff_et == 0).sum()), "diff_eq1": int((diff_et == 1).sum()),
         "diff_lt0": int((diff_et < 0).sum()), "diff_gt1": int((diff_et > 1).sum()),
         "diff_gt1_values_only_counts": int((diff_et > 1).sum())}]
pd.DataFrame(rows).to_csv(os.path.join(OUT, "et_calendar_age_outliers_v2.csv"), index=False)
note("C. ET outlier direction written")

# D. Key variable availability per sample (valid = non-blank and not documented special)
# Missing codes verified against the XML value labels (KIDSEX 9, KIDAGEINFO 15,
# EDUCLVL 8, WEALTHQ 8). Other variables: non-blank counts only.
spec_vars = {
    "KIDSEX": {9.0}, "KIDAGEINFO": {15.0}, "URBAN": set(), "AGE": set(), "EDUCLVL": {8.0},
    "WEALTHQ": {8.0}, "MARSTAT": set(), "LINENOKID": set(), "BIDX": set(),
}
rows = []
for s, g in typed.groupby("sample"):
    row = {"sample": s, "rows": len(g)}
    for v, miss in spec_vars.items():
        x = g[v]
        row[f"{v}_valid"] = int((x.notna() & ~x.isin(list(miss))).sum())
    rows.append(row)
pd.DataFrame(rows).T.to_csv(os.path.join(OUT, "key_control_availability_v2.csv"), header=False)
note("D. control availability written")

with open(os.path.join(OUT, "supplementary_log_v2.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
note(f"done -> {OUT}")
