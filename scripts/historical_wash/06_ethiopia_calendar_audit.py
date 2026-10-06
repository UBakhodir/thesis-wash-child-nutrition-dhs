"""
06_ethiopia_calendar_audit.py
=============================
Audit of Ethiopia 2016 interview-date reconstruction (PROVISIONAL), and an
aggregate household-level check of the anthropometry subsample design.

Reads the validated final run read-only. Writes a new versioned output directory
outside the tracked repository. Respondent-level outputs are restricted and are
never printed; only aggregate tables and counts are logged.

Tests:
  A. Within-month constancy of INTDATECDC_ET minus a 30-day Ethiopian day count.
  B. Fit of a month-length model (Gregorian cumulative lengths) to the same residual.
  C. Three provisional reconstructions of the Gregorian interview CMC:
       C1 triple (30-day Ethiopian arithmetic), valid-day rows only
       C2 century-day route, origin 1 Meskerem 1900 = 12 Sep 1907 (as earlier)
       C3 century-day route anchored to 1 Meskerem 2008 = 12 Sep 2015 with
          recode month lengths (Gregorian cumulative), no origin constant
     Each is compared with KIDCURAGEMO (completed months) and with the fieldwork window.
  D. Household-level measured share for Nigeria and Ghana (listed children).

Nothing here is a validated Gregorian interview date. All outputs are labelled
PROVISIONAL.
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
EPOCH = 1724220
GREG_ORD = 1721425
GREG_LEN = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
ET_FIELDWORK = (np.datetime64("2016-01-18"), np.datetime64("2016-06-27"))
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


def et_jdn(y, m, d):
    return 365 * (np.asarray(y, np.int64) - 1) + np.asarray(y, np.int64) // 4 + \
        30 * (np.asarray(m, np.int64) - 1) + np.asarray(d, np.int64) + EPOCH


def jdn_to_greg(j):
    o = np.asarray(j, np.int64) - GREG_ORD
    return np.datetime64("0001-01-01") + (o - 1).astype("timedelta64[D]")


def cmc_of(dt):
    dt = np.asarray(dt, "datetime64[D]")
    y = dt.astype("datetime64[Y]").astype(int) + 1970
    m = dt.astype("datetime64[M]").astype(int) % 12 + 1
    return (y - 1900) * 12 + m


def idx30(y, m, d):
    return 365 * (y - 1) + y // 4 + 30 * (m - 1) + d


def cumG(m):
    """Cumulative Gregorian-length days before recode month m (1-based)."""
    cum = np.concatenate([[0], np.cumsum(GREG_LEN)])
    return cum[np.asarray(m) - 1]


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUT = os.path.join(BASE, f"ethiopia_calendar_audit_PROVISIONAL_{stamp}")
    os.makedirs(OUT, exist_ok=False)
    R = lambda f: os.path.join(OUT, f)
    log(f"output -> {OUT}")
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha256_file(__file__)}")
    src = [f"idhs_00002_typed_{RUN_ID}.parquet", f"idhs_00002_derived_{RUN_ID}.parquet"]
    before = {f: sha256_file(os.path.join(RUN, f)) for f in src}

    T = pd.read_parquet(os.path.join(RUN, src[0]), columns=[
        "SAMPLE", "record_number", "INTYEAR_ET", "MONTHINT_ET", "INTDAY_ET", "INTDATECDC_ET",
        "KIDDOBCMC", "KIDDOBCMC_ET", "KIDCURAGEMO", "LINENOKID", "IDHSHID", "HWHAZWHO"])
    et = T[T["SAMPLE"] == 23104].copy()
    ey = et["INTYEAR_ET"].astype(int).values
    em = et["MONTHINT_ET"].astype(int).values
    ed = et["INTDAY_ET"].astype(int).values
    cdc = et["INTDATECDC_ET"].astype(int).values
    log(f"ET rows={len(et)}; Ethiopian year values={np.unique(ey).tolist()}")

    # ---- A. within-month constancy of residual to 30-day count (origin 1900 Meskerem 1)
    resid = cdc - (idx30(ey, em, ed) - idx30(1900, 1, 1))
    per_month = pd.DataFrame({"month": em, "resid": resid}).groupby("month")["resid"].agg(
        ["min", "median", "max", "size"]).reset_index()
    per_month["constant_within_month"] = per_month["min"] == per_month["max"]
    per_month.to_csv(R("A_residual_by_month_PROVISIONAL.csv"), index=False)
    log("A. residual by month:\n" + per_month.to_string(index=False))

    # ---- B. month-length model: CDC = idxG(2008,M,D) + k, idxG uses cumulative Gregorian lengths
    idxG = 365 * (ey - 1) + ey // 4 + cumG(em) + ed
    resid_g = cdc - idxG
    vc = pd.Series(resid_g).value_counts().sort_index()
    fit = {"k_values": {str(int(k)): int(v) for k, v in vc.items()},
           "rows_exact_under_best_single_k": int(vc.max()),
           "best_k": int(vc.idxmax()),
           "unexplained_rows": int(len(resid_g) - vc.max())}
    # month transitions implied by the residual (5..10) vs Gregorian lengths
    m_res = per_month.set_index("month")["median"]
    implied = {}
    for m in range(5, 10):
        implied[f"length_month_{m}_implied_minus_Gregorian"] = float(
            (m_res[m + 1] - m_res[m]) - (GREG_LEN[m - 1] - 30))
    fit["transition_check"] = implied
    with open(R("B_month_length_model_fit_PROVISIONAL.json"), "w", encoding="utf-8") as f:
        json.dump(fit, f, indent=1)
    log("B. month-length model fit: " + json.dumps(fit))

    # ---- C. three provisional reconstructions of the Gregorian interview CMC
    anchor_2008 = np.datetime64("2015-09-12")  # 1 Meskerem 2008 E.C. (Ethiopian new year)
    tripleok = ed <= 30
    dC1 = np.full(len(et), np.datetime64("NaT"), dtype="datetime64[D]")
    dC1[tripleok] = jdn_to_greg(et_jdn(ey[tripleok], em[tripleok], ed[tripleok]))
    dC2 = jdn_to_greg(cdc + idx30(1900, 1, 1) + EPOCH)
    dC3 = anchor_2008 + (cumG(em) + ed - 1).astype("timedelta64[D]")

    kc = et["KIDCURAGEMO"].values
    rows = []
    cmc_c = {}
    for name, d in [("C1_triple_30day_valid_rows", dC1), ("C2_cdc_origin_1907", dC2),
                    ("C3_cdc_anchored_2015_recode_lengths", dC3)]:
        ok = ~np.isnat(d)
        cm = cmc_of(d[ok])
        cmc_c[name] = (ok, d)
        # Ethiopian CMC of birth is 30-day arithmetic; compare calendar age with KIDCURAGEMO
        # via the Gregorian birth CMC (IPUMS-converted) for the same rows.
        kd_g = et["KIDDOBCMC"].values[ok]
        diff = cm - kd_g
        k_ok = ~np.isnan(kc[ok].astype(float))
        dd = diff[k_ok] - kc[ok][k_ok]
        in_win = int(((d[ok] >= ET_FIELDWORK[0]) & (d[ok] <= ET_FIELDWORK[1])).sum())
        rows.append({
            "candidate": name, "rows_dated": int(ok.sum()), "inside_fieldwork": in_win,
            "age_diff_lt0": int((dd < 0).sum()), "age_diff_0": int((dd == 0).sum()),
            "age_diff_1": int((dd == 1).sum()), "age_diff_ge2": int((dd >= 2).sum()),
        })
    cmp_df = pd.DataFrame(rows)
    cmp_df.to_csv(R("C_candidate_comparison_PROVISIONAL.csv"), index=False)
    log("C. candidates:\n" + cmp_df.to_string(index=False))

    # month disagreement between candidates (CMC level), on rows where both exist
    ok12 = ~np.isnat(dC1) & ~np.isnat(dC2) & ~np.isnat(dC3)
    dis = {
        "C1_vs_C2_month_differs": int((cmc_of(dC1[ok12]) != cmc_of(dC2[ok12])).sum()),
        "C1_vs_C3_month_differs": int((cmc_of(dC1[ok12]) != cmc_of(dC3[ok12])).sum()),
        "C2_vs_C3_month_differs": int((cmc_of(dC2[ok12]) != cmc_of(dC3[ok12])).sum()),
        "rows_compared": int(ok12.sum()),
    }
    with open(R("C_disagreement_PROVISIONAL.json"), "w", encoding="utf-8") as f:
        json.dump(dis, f, indent=1)
    log("C. disagreement: " + json.dumps(dis))

    # per-row provisional C3 CMC for downstream use (restricted, respondent-level)
    restricted = pd.DataFrame({
        "record_number": et["record_number"].values,
        "C3_provisional_gregorian_date": pd.to_datetime(dC3).strftime("%Y-%m-%d"),
        "C3_provisional_CMC": cmc_of(dC3),
        "C2_origin_1907_date": pd.to_datetime(dC2).strftime("%Y-%m-%d"),
        "C1_triple_date_if_valid": pd.Series(pd.to_datetime(dC1)).dt.strftime("%Y-%m-%d").values,
    })
    restricted.to_parquet(R("ET_provisional_dates_RESTRICTED.parquet"), index=False)

    # ---- D. household-level measured share (Nigeria, Ghana; listed children)
    D = []
    for sid, lab in [(56606, "NG2018"), (28806, "GH2014"), (23104, "ET2016"), (40406, "KE2014")]:
        g = T[(T["SAMPLE"] == sid) & (T["LINENOKID"] > 0)].copy()
        g["measured"] = g["HWHAZWHO"].notna() & (g["HWHAZWHO"] < 9995)
        hh = g.groupby("IDHSHID")["measured"].agg(["size", "sum"])
        hh2 = hh[hh["size"] >= 1]
        D.append({
            "sample": lab, "listed_children": int(len(g)),
            "listed_children_measured_share": round(float(g["measured"].mean()), 4),
            "households_with_listed_children": int(len(hh2)),
            "households_with_any_measured": int((hh2["sum"] > 0).sum()),
            "households_any_measured_share": round(float((hh2["sum"] > 0).mean()), 4),
        })
    d_df = pd.DataFrame(D)
    d_df.to_csv(R("D_household_measured_share_v2.csv"), index=False)
    log("D. household measured share:\n" + d_df.to_string(index=False))

    after = {f: sha256_file(os.path.join(RUN, f)) for f in src}
    manifest = {
        "run_id": os.path.basename(OUT), "completed_utc": datetime.now(timezone.utc).isoformat(),
        "script": "scripts/historical_wash/06_ethiopia_calendar_audit.py",
        "script_sha256": sha256_file(__file__), "interpreter": sys.executable,
        "source_run": RUN, "source_unchanged": before == after,
        "label": "PROVISIONAL - not a validated Gregorian interview date",
    }
    with open(R("manifest_PROVISIONAL.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    with open(R("execution_log_PROVISIONAL.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"source unchanged: {manifest['source_unchanged']}")


if __name__ == "__main__":
    main()
