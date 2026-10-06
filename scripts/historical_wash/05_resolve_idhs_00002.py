"""
05_resolve_idhs_00002.py
========================
Methodological resolution checks following the idhs_00002 validation.

Reads the FINAL validated run (run_20261006T140022Z) read-only and writes a new
resolution directory. Nothing in the source run is modified.

Covers:
  A. Ethiopian -> Gregorian conversion of interview dates (new derived fields),
     with independent validation anchors.
  B. Consistency of converted dates with IPUMS-converted Gregorian birth CMC and
     with reported age (KIDCURAGEMO).
  C. Investigation of negative and out-of-range age differences.
  D. Under-five and window boundary sensitivity.
  E. Anthropometric flag structure (cross-outcome).
  F. Non-measurement (NIU) diagnostics by available local variables.
  G. GPS zero-pair handling and cluster coverage (no coordinates printed).
  H. Analysis-relevant readiness counts by sample, outcome and window.
  I. Nigeria prenatal vs birth-year boundary reconciliation.

Conversion formula (documented here, validated below):
  Ethiopian (Y, M, D) -> Julian Day Number:
      JDN = 365*(Y-1) + floor(Y/4) + 30*(M-1) + D + 1724220
  Gregorian date = proleptic Gregorian date with JDN (ordinal = JDN - 1721425).
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
RUN = os.path.join(BASE, "run_20261006T140022Z")
RUN_ID = "20261006T140022Z"
EPOCH = 1724220
GREG_ORD_OFFSET = 1721425  # ordinal = JDN - 1721425 (proleptic Gregorian)
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
ET_FIELDWORK = (np.datetime64("2016-01-18"), np.datetime64("2016-06-27"))  # DHS/World Bank catalogue
RASTER = (1201, 1416)  # Jan 2000 .. Dec 2017

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
    y = np.asarray(y, dtype=np.int64)
    m = np.asarray(m, dtype=np.int64)
    d = np.asarray(d, dtype=np.int64)
    return 365 * (y - 1) + y // 4 + 30 * (m - 1) + d + EPOCH


def jdn_to_greg(jdn):
    """Return numpy datetime64[D] for JDN array."""
    ordinal = np.asarray(jdn, dtype=np.int64) - GREG_ORD_OFFSET
    return np.datetime64("0001-01-01") + (ordinal - 1).astype("timedelta64[D]")


def ymd(dt):
    dt = np.asarray(dt, dtype="datetime64[D]")
    y = dt.astype("datetime64[Y]").astype(int) + 1970
    m = dt.astype("datetime64[M]").astype(int) % 12 + 1
    d = (dt - dt.astype("datetime64[M]")).astype(int) + 1
    return y, m, d


def is_leap(y):
    return (y % 4 == 0) & ((y % 100 != 0) | (y % 400 == 0))


def cmc_from_ymd(y, m):
    return (y - 1900) * 12 + m


def elig_status(b, t, key_ok, greg_ok, et_unres, window):
    """Hierarchy identical to script 03 (mutually exclusive)."""
    bb = np.where(greg_ok, b, 0.0)
    tt = np.where(greg_ok, t, 0.0)
    if window == "birth_year":
        yb = np.floor((bb - 1) / 12) * 12 + 1
        st, en, need = yb, yb + 11, None
    elif window == "prenatal_9m":
        st, en, need = bb - 9, bb - 1, None
    elif window == "post_12m":
        st, en, need = bb, bb + 11, bb + 12
    else:
        st, en, need = bb, bb + 23, bb + 24
    conds = [~key_ok, et_unres, ~greg_ok & ~et_unres, greg_ok & (bb > tt),
             greg_ok & (st < RASTER[0]), greg_ok & (en > RASTER[1]),
             (greg_ok & (tt < need)) if need is not None else np.zeros(len(b), bool)]
    labels = ["key_invalid", "calendar_unresolved", "dates_missing", "birth_after_interview",
              "window_before_2000", "window_after_2017", "postnatal_incomplete"]
    return np.select(conds, labels, default="eligible")


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    OUT = os.path.join(BASE, f"resolution_{RUN_ID}_{stamp}")
    os.makedirs(OUT, exist_ok=False)
    R = lambda f: os.path.join(OUT, f)
    log(f"resolution run -> {OUT}")
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha256_file(__file__)}")
    src_hash_before = {f: sha256_file(os.path.join(RUN, f)) for f in
                       [f"idhs_00002_typed_{RUN_ID}.parquet", f"idhs_00002_derived_{RUN_ID}.parquet"]}

    T = pd.read_parquet(os.path.join(RUN, f"idhs_00002_typed_{RUN_ID}.parquet"))
    D = pd.read_parquet(os.path.join(RUN, f"idhs_00002_derived_{RUN_ID}.parquet"))
    T["sample"] = T["SAMPLE"].map(lambda v: SAMPLES.get(int(v), "UNEXPECTED")).values
    et = (T["SAMPLE"] == 23104).values
    log(f"loaded final run typed rows={len(T)} derived rows={len(D)}")

    # ------------------------------------------------------------------
    # A. Conversion validation (independent anchors)
    # ------------------------------------------------------------------
    anchors = {}
    yrs = np.arange(1900, 2031)
    ms = jdn_to_greg(et_jdn(yrs, np.ones_like(yrs), np.ones_like(yrs)))
    gy, gm, gd = ymd(ms)
    expected_day12 = is_leap(gy + 1)
    rule_ok = ((gd == 12) == expected_day12) & np.isin(gd, [11, 12]) & (gm == 9)
    anchors["meskerem1_is_sep11_or_sep12"] = bool(np.all(np.isin(gd, [11, 12]) & (gm == 9)))
    anchors["meskerem1_sep12_iff_next_gregorian_year_leap"] = {
        "years_tested": int(len(yrs)), "mismatches": int((~rule_ok).sum())}
    # Known anchor: Meskerem 1, 2008 E.C. = 12 Sep 2015; Meskerem 1, 2009 E.C. = 11 Sep 2016
    a2008 = jdn_to_greg(et_jdn(2008, 1, 1))
    a2009 = jdn_to_greg(et_jdn(2009, 1, 1))
    anchors["meskerem1_2008_is_2015_09_12"] = str(a2008) == "2015-09-12"
    anchors["meskerem1_2009_is_2016_09_11"] = str(a2009) == "2016-09-11"
    # Ethiopian leap rule: year length 366 iff Y % 4 == 3
    yy = np.arange(1900, 2030)
    ylen = et_jdn(yy + 1, 1, 1) - et_jdn(yy, 1, 1)
    anchors["ethiopian_leap_rule_mismatches"] = int(((ylen == 366) != (yy % 4 == 3)).sum())
    # Century-day origin: CDC day 0 = Meskerem 1, 1900 E.C.; IPUMS states an anchor of 12 Sep 1907
    origin_greg = jdn_to_greg(et_jdn(1900, 1, 1))
    anchors["cdc_origin_gregorian_date"] = str(origin_greg)
    anchors["cdc_origin_matches_ipums_stated_1907_09_12"] = str(origin_greg) == "1907-09-12"
    log("A. anchors: " + json.dumps(anchors, default=str))

    # Century-day structure: INTDATECDC_ET should equal idx(Y,M,D) - idx(1900,1,1)
    def idx(y, m, d):
        return 365 * (y - 1) + y // 4 + 30 * (m - 1) + d

    ey = T.loc[et, "INTYEAR_ET"].values.astype(int)
    em = T.loc[et, "MONTHINT_ET"].values.astype(int)
    ed = T.loc[et, "INTDAY_ET"].values.astype(int)
    cdc = T.loc[et, "INTDATECDC_ET"].values.astype(int)
    pred_cdc = idx(ey, em, ed) - idx(1900, 1, 1)
    cdc_diff = cdc - pred_cdc
    cdc_struct = {"rows": int(et.sum()), "exact_match": int((cdc_diff == 0).sum()),
                  "diff_values": {str(int(k)): int(v) for k, v in
                                  pd.Series(cdc_diff).value_counts().items()}}
    log("A. CDC structure: " + json.dumps(cdc_struct))

    # Converted exact interview date from delivered Ethiopian fields
    jd_int = et_jdn(ey, em, ed)
    int_date = jdn_to_greg(jd_int)
    # Cross-check: converting CDC directly (must equal the triple conversion when the triple is exact)
    cdc_date = jdn_to_greg(cdc + idx(1900, 1, 1) + EPOCH)
    same_day = int((int_date == cdc_date).sum())
    in_window = int(((int_date >= ET_FIELDWORK[0]) & (int_date <= ET_FIELDWORK[1])).sum())
    months_et = pd.Series(em).value_counts().sort_index().to_dict()
    year_et = pd.Series(ey).value_counts().to_dict()
    # Primary ET interview date = century-day route (approximate, see report). The delivered
    # triple is retained only as a comparison because it contains impossible Ethiopian days.
    gy_i, gm_i, gd_i = ymd(cdc_date)
    month_end = (cdc_date.astype("datetime64[M]") + 1).astype("datetime64[D]") - 1
    dim = (month_end - cdc_date.astype("datetime64[M]").astype("datetime64[D]")).astype(int) + 1
    near_edge = (gd_i <= 5) | (gd_i >= dim - 4)
    anchors["invalid_ethiopian_days_triple"] = {
        "rows_INTDAY_ET_gt_30": int((ed > 30).sum()),
        "by_MONTHINT_ET": {str(int(k)): int(v) for k, v in pd.Series(ed[ed > 30]).value_counts().items()}
        if (ed > 30).any() else {},
        "candidate_month_disagreement_triple_vs_cdc": int((cmc_from_ymd(*ymd(int_date)[:2]) != cmc_from_ymd(gy_i, gm_i)).sum()),
    }
    anchors["cdc_route_fieldwork_inside"] = int(((cdc_date >= ET_FIELDWORK[0]) & (cdc_date <= ET_FIELDWORK[1])).sum())
    anchors["cdc_route_within_5_days_of_month_edge"] = int(near_edge.sum())
    anchors["cdc_route_converted_min_max"] = [str(cdc_date.min()), str(cdc_date.max())]
    log("A. invalid-day and CDC-route checks: " + json.dumps({k: anchors[k] for k in [
        "invalid_ethiopian_days_triple", "cdc_route_fieldwork_inside", "cdc_route_within_5_days_of_month_edge"]}, default=str))
    month_span = (pd.Series(int_date).min(), pd.Series(int_date).max())
    anchors["fieldwork_check"] = {
        "converted_interviews": int(len(int_date)),
        "inside_2016_01_18_to_2016_06_27": in_window,
        "triple_vs_cdc_same_day": same_day,
        "ethiopian_months_present": {str(int(k)): int(v) for k, v in months_et.items()},
        "min_converted": str(month_span[0]), "max_converted": str(month_span[1]),
        "ethiopian_years": {str(int(k)): int(v) for k, v in year_et.items()},
    }
    log("A. fieldwork check: " + json.dumps(anchors["fieldwork_check"]))

    # Save restricted, respondent-level converted dates (outside tracked repo)
    conv = pd.DataFrame({
        "record_number": T.loc[et, "record_number"].values,
        "ET_interview_gregorian_date": pd.to_datetime(int_date).strftime("%Y-%m-%d"),
        "ET_interview_gregorian_CMC": cmc_from_ymd(gy_i, gm_i),
        "ET_interview_date_source": "INTDATECDC_ET via Ethiopian-origin JDN (APPROXIMATE, +/-5 days)",
        "ET_interview_near_month_edge": near_edge,
        "ET_triple_vs_CDC_agree": (int_date == cdc_date),
    })
    conv.to_parquet(R("ET_converted_interview_dates_RESTRICTED.parquet"), index=False)

    # ------------------------------------------------------------------
    # B. Consistency with IPUMS-converted Gregorian birth CMC and with age
    # ------------------------------------------------------------------
    kd = T.loc[et, "KIDDOBCMC"].values
    kd_et = T.loc[et, "KIDDOBCMC_ET"].values
    # IPUMS KIDDOBCMC for ET is documented as a Gregorian conversion (Beyene-Kudlek).
    # Test: the Gregorian month of each Ethiopian birth month, over all days 1..30,
    # should contain the IPUMS-converted birth CMC.
    ye = (kd_et - 1) // 12 + 1900
    me = kd_et - (ye - 1900) * 12
    in_set = np.zeros(len(kd), bool)
    d1_match = np.zeros(len(kd), bool)
    for dday in range(1, 31):
        jd_b = et_jdn(ye.astype(int), me.astype(int), np.full(len(kd), dday))
        g = jdn_to_greg(jd_b)
        gyb, gmb, _ = ymd(g)
        c = cmc_from_ymd(gyb, gmb)
        in_set |= (c == kd)
        if dday == 1:
            d1_match = (c == kd)
    birth_test = {"ET_births_tested": int(len(kd)), "IPUMS_birth_CMC_in_possible_month_set": int(in_set.sum()),
                  "matches_day1_mapping": int(d1_match.sum()),
                  "not_in_set": int((~in_set).sum())}
    log("B. ET birth CMC test: " + json.dumps(birth_test))

    t_g = cmc_from_ymd(gy_i, gm_i)
    diff_g = t_g - kd
    k_et = T.loc[et, "KIDCURAGEMO"].values
    kvalid = ~np.isnan(k_et)
    rel = diff_g[kvalid] - k_et[kvalid]
    age_conv = {"rows_with_KIDCURAGEMO": int(kvalid.sum()),
                "diff_calendar_minus_KIDCURAGEMO": {str(int(k)): int(v) for k, v in
                                                   pd.Series(rel).value_counts().sort_index().items()}}
    log("B. converted calendar age vs KIDCURAGEMO: " + json.dumps(age_conv))
    # Converted Gregorian CMC minus IPUMS Gregorian birth CMC; compare with ET-calendar difference
    et_cal = T.loc[et, "INTDATECMC_ET"].values - kd_et
    ratio = pd.Series(diff_g - et_cal).value_counts().sort_index()
    log("B. Gregorian minus ET-calendar CMC offset distribution: " + json.dumps({str(int(k)): int(v) for k, v in ratio.items()}))

    # ------------------------------------------------------------------
    # C. Negative / out-of-range age differences (all samples)
    # ------------------------------------------------------------------
    rows = []
    prec = D["birth_date_precision"].values
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        if lab == "ET2016":
            cal = (T["INTDATECMC_ET"].values - T["KIDDOBCMC_ET"].values)
        else:
            cal = (T["INTDATECMC"].values - T["KIDDOBCMC"].values)
        kc = T["KIDCURAGEMO"].values
        ok = sel & ~np.isnan(kc) & ~np.isnan(cal)
        dd = (cal - kc)
        out = ok & ((dd < 0) | (dd > 1))
        for label, mask in [("all_outside_0_1", out), ("negative", ok & (dd < 0)),
                            ("equal_2_or_more", ok & (dd >= 2))]:
            r = {"sample": lab, "category": label, "rows": int(mask.sum())}
            if mask.sum():
                r["difference_values"] = json.dumps({str(int(k)): int(v) for k, v in
                                                     pd.Series(dd[mask]).value_counts().sort_index().items()})
                r["birth_precision_classes"] = json.dumps({str(k): int(v) for k, v in
                                                           pd.Series(prec[mask]).value_counts().items()})
                r["birth_month_imputed_component"] = int((prec[mask] == "imputed_component").sum())
            rows.append(r)
    neg_df = pd.DataFrame(rows)
    neg_df.to_csv(R("age_discrepancy_investigation_v2.csv"), index=False)
    log("C. discrepancy investigation:\n" + neg_df.to_string(index=False))

    # Are ET negatives also negative on the converted Gregorian calendar? (interview side check)
    et_kc = T.loc[et, "KIDCURAGEMO"].values
    et_cal_all = T.loc[et, "INTDATECMC_ET"].values - T.loc[et, "KIDDOBCMC_ET"].values
    et_neg_mask = (~np.isnan(et_kc)) & ((et_cal_all - et_kc) < 0)
    et_neg_greg = diff_g[et_neg_mask] - et_kc[et_neg_mask]
    log(f"C. ET negative ET-calendar rows={int(et_neg_mask.sum())}; Gregorian-converted difference on those rows: "
        + json.dumps({str(int(k)): int(v) for k, v in pd.Series(et_neg_greg).value_counts().items()}))

    # ------------------------------------------------------------------
    # D. Under-five and window boundary sensitivity
    # ------------------------------------------------------------------
    sens_rows = []
    # Build full-length interview CMC (ET from conversion; others from INTDATECMC)
    tc_full = T["INTDATECMC"].values.astype(float).copy()
    tc_full[et] = np.nan
    tc_full[et] = t_g
    bc_full = T["KIDDOBCMC"].values.astype(float)
    key_ok = D["child_key_valid"].values.astype(bool)
    greg_ok = ~np.isnan(bc_full) & ~np.isnan(tc_full)
    et_unres = np.zeros(len(T), bool)
    base_status = {}
    for w in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        base_status[w] = elig_status(bc_full, tc_full, key_ok, greg_ok, et_unres, w)
        # sensitivity A: birth one month later (birth day unknown -> later birth is conservative for completion)
        alt_b = elig_status(bc_full + 1, tc_full, key_ok, greg_ok, et_unres, w)
        # sensitivity B: interview one month earlier
        alt_t = elig_status(bc_full, tc_full - 1, key_ok, greg_ok, et_unres, w)
        alt_tp = elig_status(bc_full, tc_full + 1, key_ok, greg_ok, et_unres, w)
        for lab_s, arr in [("birth_plus_1_month", alt_b), ("interview_minus_1_month", alt_t),
                           ("interview_plus_1_month", alt_tp)]:
            for sid, lab in SAMPLES.items():
                sel = (T["SAMPLE"] == sid).values
                base_e = base_status[w][sel] == "eligible"
                alt_e = arr[sel] == "eligible"
                sens_rows.append({"sample": lab, "window": w, "shift": lab_s,
                                  "eligible_base": int(base_e.sum()), "eligible_shifted": int(alt_e.sum()),
                                  "gained": int((~base_e & alt_e).sum()), "lost": int((base_e & ~alt_e).sum())})
    sens_df = pd.DataFrame(sens_rows)
    sens_df.to_csv(R("timing_boundary_sensitivity_v2.csv"), index=False)
    log("D. timing sensitivity:\n" + sens_df.to_string(index=False))

    # Under-5 boundary: calendar difference exactly 60 (completed age could be 59)
    u5 = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        cal = np.where(sel, tc_full - bc_full, np.nan)
        kc = T["KIDCURAGEMO"].values
        u5.append({"sample": lab, "rows": int(sel.sum()),
                   "calendar_age_60": int((cal == 60).sum()),
                   "calendar_age_59": int((cal == 59).sum()),
                   "KIDCURAGEMO_available": int((~np.isnan(kc) & sel).sum()),
                   "KIDCURAGEMO_equals_60": int(((kc == 60) & sel).sum()),
                   "KIDCURAGEMO_equals_59": int(((kc == 59) & sel).sum()),
                   "measurement_age_available": False})
    pd.DataFrame(u5).to_csv(R("under5_boundary_v2.csv"), index=False)
    log("D. under-5 boundary:\n" + pd.DataFrame(u5).to_string(index=False))

    # ------------------------------------------------------------------
    # E. Anthropometric flag structure across outcomes
    # ------------------------------------------------------------------
    flag_rows = []
    codes = {"HAZ": T["HWHAZWHO"].values, "WAZ": T["HWWAZWHO"].values, "WHZ": T["HWWHZWHO"].values}
    flagset = {9995.0, 9996.0, 9997.0, 9998.0}
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        fl = {k: np.isin(v[sel], list(flagset)) for k, v in codes.items()}
        niu = {k: v[sel] == 9999.0 for k, v in codes.items()}
        any_fl = fl["HAZ"] | fl["WAZ"] | fl["WHZ"]
        flag_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "HAZ_flagged": int(fl["HAZ"].sum()), "WAZ_flagged": int(fl["WAZ"].sum()),
            "WHZ_flagged": int(fl["WHZ"].sum()),
            "any_flagged": int(any_fl.sum()),
            "all_three_flagged": int((fl["HAZ"] & fl["WAZ"] & fl["WHZ"]).sum()),
            "flagged_in_exactly_one": int(((fl["HAZ"].astype(int) + fl["WAZ"] + fl["WHZ"]) == 1).sum()),
            "HAZ_9995": int((codes["HAZ"][sel] == 9995).sum()),
            "WHZ_9995": int((codes["WHZ"][sel] == 9995).sum()),
            "9995_in_HAZ_and_WHZ": int(((codes["HAZ"][sel] == 9995) & (codes["WHZ"][sel] == 9995)).sum()),
            "HAZ_NIU_and_WHZ_flagged": int((niu["HAZ"] & fl["WHZ"]).sum()),
            "HAZ_valid_and_WHZ_NIU": int((~fl["HAZ"] & ~niu["HAZ"] & niu["WHZ"]).sum()),
        })
    flag_df = pd.DataFrame(flag_rows)
    flag_df.to_csv(R("anthropometry_flag_structure_v2.csv"), index=False)
    log("E. flag structure:\n" + flag_df.to_string(index=False))

    # valid z within 0.05 of threshold (evidence of truncation/replacement)
    thr = {"HAZ": (-6.0, 6.0), "WAZ": (-6.0, 5.0), "WHZ": (-5.0, 5.0)}
    near = []
    for z, (lo, hi) in thr.items():
        v = codes[z] / 100.0
        valid = ~np.isin(codes[z], list(flagset | {9999.0})) & ~np.isnan(codes[z])
        near.append({"outcome": z, "valid": int(valid.sum()),
                     "valid_within_0.05_of_lower": int((valid & (np.abs(v - lo) <= 0.05)).sum()),
                     "valid_within_0.05_of_upper": int((valid & (np.abs(v - hi) <= 0.05)).sum()),
                     "valid_beyond_lower": int((valid & (v < lo)).sum()),
                     "valid_beyond_upper": int((valid & (v > hi)).sum())})
    pd.DataFrame(near).to_csv(R("anthropometry_threshold_proximity_v2.csv"), index=False)
    log("E. threshold proximity: " + json.dumps(near))

    # ------------------------------------------------------------------
    # F. Non-measurement diagnostics (NIU share by local variables)
    # ------------------------------------------------------------------
    niu_rows = []
    best_age = np.where(~np.isnan(T["KIDCURAGEMO"].values), T["KIDCURAGEMO"].values,
                        np.where(~np.isnan(bc_full) & ~np.isnan(tc_full), tc_full - bc_full, np.nan))
    bins = [-1, 11, 23, 35, 47, 59, 999]
    labels_age = ["0-11", "12-23", "24-35", "36-47", "48-59", "60+"]
    age_bin = pd.cut(best_age, bins=bins, labels=labels_age)
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        niu = (T["HWHAZWHO"].values == 9999.0)
        base = {"sample": lab, "rows": int(sel.sum()), "HAZ_NIU": int((niu & sel).sum())}
        base["NIU_share"] = round(float(base["HAZ_NIU"] / max(sel.sum(), 1)), 4)
        niu_rows.append({**base, "group": "all", "level": "all", "rows_in_group": int(sel.sum()),
                         "NIU_in_group": base["HAZ_NIU"]})
        for var, grp in [("LINENOKID_not_listed", T["LINENOKID"].values == 0),
                         ("URBAN", None), ("WEALTHQ", None), ("age_band", None)]:
            if var == "LINENOKID_not_listed":
                for flag, msk in [("not listed in household", grp), ("listed in household", ~grp & ~np.isnan(T["LINENOKID"].values))]:
                    m = sel & msk
                    niu_rows.append({"sample": lab, "rows": int(sel.sum()), "HAZ_NIU": base["HAZ_NIU"],
                                     "NIU_share": base["NIU_share"], "group": var, "level": flag,
                                     "rows_in_group": int(m.sum()), "NIU_in_group": int((m & niu).sum())})
            else:
                col = {"URBAN": T["URBAN"].values, "WEALTHQ": T["WEALTHQ"].values,
                       "age_band": np.asarray(age_bin.astype(str))}[var]
                for level in pd.unique(col[sel]):
                    m = sel & (col == level)
                    niu_rows.append({"sample": lab, "rows": int(sel.sum()), "HAZ_NIU": base["HAZ_NIU"],
                                     "NIU_share": base["NIU_share"], "group": var, "level": str(level),
                                     "rows_in_group": int(m.sum()), "NIU_in_group": int((m & niu).sum())})
    niu_df = pd.DataFrame(niu_rows)
    niu_df["NIU_group_share"] = (niu_df["NIU_in_group"] / niu_df["rows_in_group"].replace(0, np.nan)).round(4)
    niu_df.to_csv(R("nonmeasurement_diagnostics_v2.csv"), index=False)
    log("F. NIU diagnostics written")

    # ------------------------------------------------------------------
    # G. GPS: documented zero = missing; cluster coverage (no coordinates printed)
    # ------------------------------------------------------------------
    la = T["GPSLAT"].values
    lo = T["GPSLONG"].values
    zero_both = (la == 0) & (lo == 0)
    zero_one = ((la == 0) ^ (lo == 0))
    in_range = (np.abs(la) <= 90) & (np.abs(lo) <= 180)
    usable = ~np.isnan(la) & ~np.isnan(lo) & ~zero_both & ~zero_one & in_range
    g_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        psu = T["IDHSPSU"].values
        all_psu = np.unique(psu[sel])
        usable_psu = np.unique(psu[sel & usable])
        zero_psu = np.unique(psu[sel & zero_both])
        g_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "zero_both_pairs_rows (documented missing)": int((sel & zero_both).sum()),
            "one_zero_only_rows (provisional invalid flag)": int((sel & zero_one).sum()),
            "out_of_range_rows": int((sel & ~in_range & ~np.isnan(la)).sum()),
            "usable_rows": int((sel & usable).sum()),
            "clusters_total": int(len(all_psu)),
            "clusters_with_usable_coordinates": int(len(usable_psu)),
            "clusters_lost_under_zero_rule": int(len(all_psu) - len(usable_psu)),
            "clusters_with_any_zero_pair": int(len(zero_psu)),
            "rows_lost_to_zero_rule_pct": round(100 * float((sel & zero_both).sum()) / max(sel.sum(), 1), 2),
        })
    g_df = pd.DataFrame(g_rows)
    g_df.to_csv(R("gps_coverage_v2.csv"), index=False)
    log("G. GPS coverage:\n" + g_df.to_string(index=False))

    # ------------------------------------------------------------------
    # H. Readiness counts by sample, outcome and window (sequential, then intersection)
    # ------------------------------------------------------------------
    ready_rows = []
    age_info = (~np.isnan(T["KIDCURAGEMO"].values)) | (~np.isnan(tc_full - bc_full))
    valid_dates = greg_ok & key_ok
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        for oc in ["HAZ", "WAZ", "WHZ"]:
            c = codes[oc]
            in_univ = sel & ~np.isnan(c) & (c != 9999.0)
            valid_out = in_univ & ~np.isin(c, list(flagset))
            step_age = valid_out & age_info
            step_dates = step_age & valid_dates
            for w in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
                win_ok = sel & (base_status[w] == "eligible")
                s_w = step_dates & (base_status[w] == "eligible")
                coord_ok = sel & usable
                inter = s_w & usable
                ready_rows.append({
                    "sample": lab, "outcome": oc, "window": w,
                    "1_birth_history_records": int(sel.sum()),
                    "2_in_outcome_universe (not NIU)": int(in_univ.sum()),
                    "3_valid_outcome (universe minus flags/missing)": int(valid_out.sum()),
                    "4_valid_analysis_age": int(step_age.sum()),
                    "5_valid_timing_dates_(birth_and_interview)": int(step_dates.sum()),
                    "6_complete_window_2000_2017": int(s_w.sum()),
                    "7_technically_usable_coordinates (all rows of sample)": int(coord_ok.sum()),
                    "8_intersection_6_and_7": int(inter.sum()),
                    "window_eligible_all_outcome_rows": int(win_ok.sum()),
                })
    ready_df = pd.DataFrame(ready_rows)
    ready_df.to_csv(R("analysis_readiness_counts_v2.csv"), index=False)
    log("H. readiness counts written (rows=" + str(len(ready_df)) + ")")

    # ------------------------------------------------------------------
    # I. Nigeria prenatal vs birth-year boundary reconciliation
    # ------------------------------------------------------------------
    ng = (T["SAMPLE"] == 56606).values
    bng = bc_full[ng]
    tng = tc_full[ng]
    ng_bi = {}
    for w in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        st = base_status[w][ng]
        ng_bi[w] = int((st == "eligible").sum())
    births2018 = ng & (bc_full >= 1417) & (bc_full <= 1428)
    # Prenatal window of birth month b is b-9..b-1; it lies wholly in 2017 only if b-1 <= 1416, i.e. b = Jan 2018 (1417)
    jan_sep_2018 = ng & (bc_full == 1417)
    prenatal_extra = ng_bi["prenatal_9m"] - ng_bi["birth_year"]
    recon = {
        "birth_year_eligible": ng_bi["birth_year"],
        "prenatal_eligible": ng_bi["prenatal_9m"],
        "prenatal_minus_birth_year": prenatal_extra,
        "births_in_January_2018_only (prenatal fully in 2017)": int(jan_sep_2018.sum()),
        "births_in_2018_total": int(births2018.sum()),
        "births_before_2000": int((ng & (bc_full < 1201)).sum()),
        "birth_year_excluded_as_2018": int((ng & (base_status["birth_year"] == "window_after_2017")).sum()),
        "prenatal_superset_of_birth_year_in_NG": bool(np.all(
            ~(ng & (base_status["birth_year"] == "eligible")) | (base_status["prenatal_9m"] == "eligible"))),
    }
    recon["explained"] = bool(prenatal_extra == recon["births_in_January_2018_only (prenatal fully in 2017)"])
    log("I. NG boundary reconciliation: " + json.dumps(recon))
    with open(R("nigeria_window_boundary_reconciliation_v2.json"), "w", encoding="utf-8") as f:
        json.dump(recon, f, indent=1)

    # ------------------------------------------------------------------
    # Save anchors / conversion summaries and close
    # ------------------------------------------------------------------
    with open(R("et_conversion_validation_v2.json"), "w", encoding="utf-8") as f:
        json.dump({"anchors": anchors, "cdc_structure": cdc_struct, "birth_cmc_test": birth_test,
                   "calendar_age_vs_KIDCURAGEMO": age_conv,
                   "gregorian_minus_ET_offset": {str(int(k)): int(v) for k, v in ratio.items()}},
                  f, indent=1, default=str)

    src_hash_after = {f: sha256_file(os.path.join(RUN, f)) for f in src_hash_before}
    manifest = {
        "run_id": os.path.basename(OUT),
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "script": "scripts/historical_wash/05_resolve_idhs_00002.py",
        "script_sha256": sha256_file(__file__),
        "command": "python scripts\\historical_wash\\05_resolve_idhs_00002.py",
        "interpreter": sys.executable,
        "python": platform.python_version(),
        "packages": {"pandas": pd.__version__, "numpy": np.__version__, "pyarrow": pa.__version__},
        "source_run": RUN,
        "source_hashes_before": src_hash_before,
        "source_hashes_after": src_hash_after,
        "source_unchanged": src_hash_before == src_hash_after,
        "outputs": sorted(os.listdir(OUT)),
    }
    with open(R("manifest_resolution_v2.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, default=str)
    log(f"source unchanged: {manifest['source_unchanged']}")
    with open(R("execution_log_resolution_v2.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
