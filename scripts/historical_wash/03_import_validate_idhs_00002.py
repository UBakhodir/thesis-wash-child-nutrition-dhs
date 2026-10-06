"""
03_import_validate_idhs_00002.py
================================
Read-only import and validation of the revised IPUMS DHS extract idhs_00002.

Scope (per the validation brief): structural validation, raw-string and typed
datasets, child-key and date validation, anthropometry scaling (documented
x100 Z-scores), weights and design, geography readiness (no coordinates printed),
and preliminary historical timing eligibility. NO outcome regressions, NO IHME
extraction, NO specification choice.

Metadata authority:
  - idhs_00002.xml : DDI codebook (variable positions, value labels, notes).
  - idhs_00002.do  : Stata infix dictionary (cross-checked against the XML).
  - Documentation text in the XML (HWHAZWHO etc. x100 scaling; CMC formulas;
    Ethiopian-calendar variables) is used for conversions.

Outputs go to a NEW run directory (never overwritten) outside the tracked
repository:
  <MASTER>\\data\\processed\\ipums_import\\v2\\run_<UTC run id>\\

Failure policy: any structural failure stops the dependent import; the failure
and its diagnostics are written to the run log before exit.
"""
import glob
import gzip
import hashlib
import json
import os
import platform
import re
import sys
import traceback
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa

DOWNLOADS = r"C:\Users\user\Downloads"
MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
BASE = os.path.join(MASTER, "data", "processed", "ipums_import", "v2")
V1_RAW = os.path.join(MASTER, "data", "processed", "ipums_import", "v1",
                      "idhs_00001_raw_strings_v1.parquet")
SRC = {
    "dat": os.path.join(DOWNLOADS, "idhs_00002.dat.gz"),
    "xml": os.path.join(DOWNLOADS, "idhs_00002.xml"),
    "do": os.path.join(DOWNLOADS, "idhs_00002.do"),
}
NS = "{ddi:codebook:2_5}"
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
CMC_PLAUSIBLE = (1000, 1800)   # proposed plausibility window for CMC values (1983-2050)
CMC_RASTER = (1201, 1416)      # Jan 2000 .. Dec 2017 (IHME raster span)
HAZ_WHO = (-6.0, 6.0)          # WHO flag limits (secondary sources; see report)
WAZ_WHO = (-6.0, 5.0)
WHZ_WHO = (-5.0, 5.0)

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


def classify_code(label):
    lab = label.lower()
    if "not in universe" in lab or "niu" in lab:
        return "NIU"
    if "missing" in lab:
        return "MISSING"
    if "plausible" in lab or "flagged" in lab:
        return "FLAG"
    return None


def parse_xml(path):
    root = ET.parse(path).getroot()
    out = {}
    for v in root.iter(NS + "var"):
        name = v.get("name")
        loc = v.find(NS + "location")
        vf = v.find(NS + "varFormat")
        cats = []
        for c in v.findall(NS + "catgry"):
            code = (c.findtext(NS + "catValu") or "").strip()
            lab = " ".join((c.findtext(NS + "labl") or "").split())
            cats.append((code, lab))
        out[name] = {
            "start": int(loc.get("StartPos")),
            "end": int(loc.get("EndPos")),
            "xml_type": vf.get("type") if vf is not None else None,
            "dcml": vf.get("DCML") if vf is not None else None,
            "label": " ".join((v.findtext(NS + "labl") or "").split()),
            "concept": " ".join((v.findtext(NS + "concept") or "").split()),
            "cats": cats,
        }
    notes = [" ".join("".join(n.itertext()).split()) for n in root.iter(NS + "notes")]
    return out, [n for n in notes if n]


def parse_do(path):
    text = open(path, encoding="latin-1").read()
    block = text.split("infix", 1)[1].split("using", 1)[0]
    fields = re.findall(r"(byte|int|long|float|double|str\d*)\s+(\w+)\s+(\d+)-(\d+)", block)
    do_fields = {n.lower(): {"stata_type": t, "start": int(s), "end": int(e)}
                 for t, n, s, e in fields}
    labels = {}
    for m in re.finditer(r"label define (\w+)_lbl\s+(\d+)\s", text):
        labels.setdefault(m.group(1).lower(), set()).add(int(m.group(2)))
    return do_fields, labels


def q_stats(x):
    if len(x) == 0:
        return [np.nan] * 7
    return list(np.percentile(x, [0, 1, 5, 50, 95, 99, 100]))


def main():
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = os.path.join(BASE, f"run_{run_id}")
    os.makedirs(run_dir, exist_ok=False)
    R = lambda f: os.path.join(run_dir, f)
    log(f"run_id={run_id} run_dir={run_dir}")
    log(f"python={platform.python_version()} pandas={pd.__version__} "
        f"numpy={np.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha256_file(__file__)}")

    # ---- 1. Sources ----------------------------------------------------
    for p in SRC.values():
        if not os.path.isfile(p):
            raise FileNotFoundError(p)
    src_info = {}
    for k, p in SRC.items():
        src_info[k] = {"path": p, "bytes": os.path.getsize(p), "sha256_before": sha256_file(p)}
        log(f"source {k}: bytes={src_info[k]['bytes']} sha256={src_info[k]['sha256_before']}")
    candidates = sorted(glob.glob(os.path.join(DOWNLOADS, "idhs_00002*")))
    log(f"idhs_00002* candidates in Downloads: {[os.path.basename(c) for c in candidates]}")

    xml, notes = parse_xml(SRC["xml"])
    do_fields, do_labels = parse_do(SRC["do"])
    log(f"XML variables={len(xml)} do fields={len(do_fields)}")
    for n in notes:
        log(f"XML note: {n[:160]}")
    sample_notes = [n for n in notes if "Children" in n]
    log(f"XML sample notes listing 'Children': {len(sample_notes)}")

    # ---- 2. Layout reconciliation -------------------------------------
    recon = []
    for name, x in xml.items():
        d = do_fields.get(name.lower())
        dl = do_labels.get(name.lower())
        xml_codes = {int(c) for c, _ in x["cats"] if c.lstrip("-").isdigit()}
        recon.append({
            "variable": name,
            "xml_start": x["start"], "xml_end": x["end"], "xml_width": x["end"] - x["start"] + 1,
            "xml_type": x["xml_type"], "xml_dcml": x["dcml"],
            "do_present": d is not None,
            "do_stata_type": d["stata_type"] if d else None,
            "do_start": d["start"] if d else None, "do_end": d["end"] if d else None,
            "positions_match": bool(d and d["start"] == x["start"] and d["end"] == x["end"]),
            "type_consistent": bool(d and (
                (x["xml_type"] == "character") == d["stata_type"].startswith("str"))),
            "n_xml_categories": len(x["cats"]),
            "do_label_codes_present": dl is not None,
            "label_codes_match": bool(dl is not None and xml_codes and
                                       {c for c in xml_codes} == dl) if dl else None,
        })
    recon_df = pd.DataFrame(recon)
    recon_df.to_csv(R("layout_reconciliation_v2.csv"), index=False)
    n_pos_mis = int((~recon_df.positions_match).sum())
    n_type_mis = int((~recon_df.type_consistent).sum())
    log(f"layout: positions mismatched={n_pos_mis} type inconsistent={n_type_mis} "
        f"do-only fields={len(set(do_fields) - {n.lower() for n in xml})}")
    if n_pos_mis or n_type_mis:
        raise RuntimeError("XML/Stata layout disagreement; see layout_reconciliation_v2.csv")

    spans = sorted((x["start"], x["end"], n) for n, x in xml.items())
    gaps, overlaps = [], []
    for (s1, e1, n1), (s2, e2, n2) in zip(spans, spans[1:]):
        if s2 > e1 + 1:
            gaps.append((n1, n2, e1 + 1, s2 - 1))
        if s2 <= e1:
            overlaps.append((n1, n2))
    W = spans[-1][1]
    log(f"layout span: start={spans[0][0]} max_end={W} gaps={len(gaps)} overlaps={len(overlaps)}")
    if spans[0][0] != 1 or overlaps:
        raise RuntimeError("layout does not start at column 1 or has overlaps")
    if gaps:
        log(f"gaps (undelivered columns, documented in report): {gaps}")

    names = [n for _, _, n in spans]

    # ---- 3. Physical structure ----------------------------------------
    len_counter = Counter()
    crlf = lf = nonascii = empty = 0
    lines = []
    with gzip.open(SRC["dat"], "rb") as f:
        for raw in f:
            if raw.endswith(b"\r\n"):
                crlf += 1
                line = raw[:-2]
            elif raw.endswith(b"\n"):
                lf += 1
                line = raw[:-1]
            else:
                line = raw
            ln = len(line)
            len_counter[ln] += 1
            if ln == 0:
                empty += 1
            if any(b > 127 for b in line):
                nonascii += 1
            lines.append(line)
    n_records = len(lines)
    bad = {ln: c for ln, c in len_counter.items() if ln != W}
    diag = pd.DataFrame([{"record_length": k, "records": v, "expected": W,
                          "matches_expected": k == W} for k, v in sorted(len_counter.items())])
    diag.to_csv(R("record_length_diagnostics_v2.csv"), index=False)
    log(f"records={n_records} CRLF={crlf} LF={lf} empty={empty} "
        f"records_with_nonascii_bytes={nonascii} length_distribution={dict(len_counter)}")
    if bad:
        raise RuntimeError(f"malformed records (length != {W}): {bad}; dependent import stopped")

    mat = np.frombuffer(b"".join(lines), dtype=np.uint8).reshape(n_records, W)
    del lines

    # ---- 4. Raw-string dataset (untrimmed, latin-1) ---------------------
    raw_cols = {}
    for name, x in xml.items():
        a, b = x["start"] - 1, x["end"]
        raw_cols[name] = pd.Series([row.tobytes().decode("latin-1") for row in mat[:, a:b]],
                                   dtype="string")
    raw = pd.DataFrame(raw_cols)[names]
    raw.insert(0, "record_number", np.arange(1, n_records + 1, dtype=np.int64))
    raw.to_parquet(R(f"idhs_00002_raw_strings_{run_id}.parquet"), index=False)
    log(f"raw-string dataset rows={len(raw)} cols={raw.shape[1]}")

    # ---- 5. Typed (raw codes, no special-code recode) -------------------
    typed = pd.DataFrame({"record_number": raw["record_number"].values})
    nonnumeric_fail = {}
    for name in names:
        s = raw[name].str.strip()
        if xml[name]["xml_type"] == "numeric":
            num = pd.to_numeric(s.replace("", np.nan), errors="coerce").astype(float)
            fails = int(((s != "") & num.isna()).sum())
            if fails:
                nonnumeric_fail[name] = fails
            typed[name] = num.values
        else:
            typed[name] = s.values
    log(f"typed dataset built; non-numeric content in numeric fields: {nonnumeric_fail or 'none'}")
    typed.to_parquet(R(f"idhs_00002_typed_{run_id}.parquet"), index=False)

    T = typed  # alias
    sample_num = T["SAMPLE"]
    present_samples = {int(s): int(c) for s, c in sample_num.value_counts().items()}
    log(f"SAMPLE values observed: {present_samples}")
    if set(present_samples) != set(SAMPLES):
        raise RuntimeError(f"observed samples {present_samples} != expected {SAMPLES}")
    T["sample_label"] = sample_num.map(lambda v: SAMPLES.get(int(v), "UNEXPECTED")).values
    is_et = (T["SAMPLE"] == 23104).values

    # ---- 6. Special codes and availability ----------------------------
    spec = {}
    for name, x in xml.items():
        codes = {}
        for c, lab in x["cats"]:
            cls = classify_code(lab)
            if cls and c.lstrip("-").isdigit():
                codes[float(int(c))] = cls
        spec[name] = codes

    def valid_mask(name):
        s = T[name]
        m = s.notna().values.copy()
        for code in spec[name]:
            m &= (s.values != code)
        return m

    avail = []
    for name in names:
        x = xml[name]
        for sid, lab in SAMPLES.items():
            sel = (T["SAMPLE"] == sid).values
            if x["xml_type"] == "numeric":
                v = T.loc[sel, name].values
                vm = valid_mask(name)[sel]
                cls_counts = Counter()
                for code, cl in spec[name].items():
                    cls_counts[cl] += int((v == code).sum())
                documented = {float(int(c)) for c, _ in x["cats"] if c.lstrip("-").isdigit()}
                undoc = int((~np.isin(v, list(documented)) & ~np.isnan(v)).sum()) if documented else None
                valid_v = v[vm]
                avail.append({
                    "variable": name, "sample": lab, "rows": int(sel.sum()),
                    "blank_or_nonnumeric": int(np.isnan(v).sum()),
                    "valid": int(vm.sum()),
                    "missing_code": cls_counts.get("MISSING", 0),
                    "niu_code": cls_counts.get("NIU", 0),
                    "flag_code": cls_counts.get("FLAG", 0),
                    "documented_codes": len(documented),
                    "undocumented_nonmissing": undoc,
                    "valid_min": float(valid_v.min()) if len(valid_v) else np.nan,
                    "valid_max": float(valid_v.max()) if len(valid_v) else np.nan,
                    "valid_zero": int((valid_v == 0).sum()),
                    "valid_negative": int((valid_v < 0).sum()),
                })
            else:
                v = T.loc[sel, name].values
                nb = int(np.sum(np.array([s != "" for s in v], dtype=bool)))
                avail.append({"variable": name, "sample": lab, "rows": int(sel.sum()),
                              "blank_or_nonnumeric": int(sel.sum()) - nb, "valid": nb,
                              "missing_code": None, "niu_code": None, "flag_code": None,
                              "documented_codes": None, "undocumented_nonmissing": None,
                              "valid_min": None, "valid_max": None,
                              "valid_zero": None, "valid_negative": None})
    avail_df = pd.DataFrame(avail)
    avail_df.to_csv(R("variable_availability_by_sample_v2.csv"), index=False)
    log(f"availability table rows={len(avail_df)}")

    inv = pd.DataFrame([{
        "variable": n, "start": xml[n]["start"], "end": xml[n]["end"],
        "xml_type": xml[n]["xml_type"], "concept": xml[n]["concept"], "label": xml[n]["label"],
        "n_documented_codes": len(xml[n]["cats"]),
        "documented_special_codes": ";".join(f"{int(k)}={v}" for k, v in sorted(spec[n].items())),
        "dcml_in_xml": xml[n]["dcml"],
    } for n in names])
    inv.to_csv(R("variable_inventory_v2.csv"), index=False)

    # ---- 7. Observation unit and keys ---------------------------------
    bidx_ok = valid_mask("BIDX")
    caseid_ok = np.asarray((raw["CASEID"].str.strip() != "").to_numpy(dtype=bool))
    T["child_key_valid"] = np.asarray(bidx_ok & caseid_ok, dtype=bool)
    T["child_key"] = np.where(T["child_key_valid"],
                              [f"{int(s)}|{c.strip()}|{int(b)}" if ok else ""
                               for s, c, b, ok in zip(T["SAMPLE"].fillna(0), raw["CASEID"],
                                                      T["BIDX"].fillna(0), T["child_key_valid"])],
                              "")
    T["woman_key"] = [f"{int(s)}|{c.strip()}" if c.strip() else "" for s, c in
                      zip(T["SAMPLE"].fillna(0), raw["CASEID"])]
    T["household_key"] = [h.strip() for h in raw["IDHSHID"]]

    key_rows = []
    rowhash = pd.util.hash_pandas_object(raw[names].astype(object), index=False).values
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        keys = T.loc[sel & T["child_key_valid"].values, "child_key"]
        h = pd.Series(rowhash[sel & T["child_key_valid"].values],
                      index=keys.index)
        grp = pd.DataFrame({"k": keys.values, "h": h.values}).groupby("k")
        sizes = grp.size()
        dup_keys = sizes[sizes > 1]
        identical_groups = int((grp["h"].nunique() == 1)[dup_keys.index].sum()) if len(dup_keys) else 0
        key_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "child_key_invalid_rows": int((sel & ~T["child_key_valid"].values).sum()),
            "unique_child_keys": int(sizes.shape[0]),
            "duplicate_child_key_groups": int(len(dup_keys)),
            "rows_in_duplicate_groups": int(dup_keys.sum()) if len(dup_keys) else 0,
            "duplicate_groups_identical_content": identical_groups,
            "duplicate_groups_conflicting": int(len(dup_keys) - identical_groups),
            "unique_woman_keys": int(pd.Series(T.loc[sel, "woman_key"]).replace("", np.nan).nunique()),
            "unique_household_ids": int(pd.Series(T.loc[sel, "household_key"]).replace("", np.nan).nunique()),
            "unique_IDHSPSU": int(T.loc[sel, "IDHSPSU"].nunique()),
            "unique_DHSID": int(pd.Series(raw.loc[sel, "DHSID"].str.strip()).nunique()),
            "children_per_woman_median": float(np.median(
                pd.Series(T.loc[sel & T["child_key_valid"].values, "woman_key"]).value_counts().values))
            if (sel & T["child_key_valid"].values).any() else np.nan,
            "children_per_woman_max": int(pd.Series(T.loc[sel & T["child_key_valid"].values,
                                                           "woman_key"]).value_counts().max())
            if (sel & T["child_key_valid"].values).any() else np.nan,
        })
    key_df = pd.DataFrame(key_rows)
    key_df.to_csv(R("key_structure_v2.csv"), index=False)
    log("key structure:\n" + key_df.to_string(index=False))

    # ---- 8. Dates -----------------------------------------------------
    def plaus(name):
        s = T[name].values
        return valid_mask(name) & (s >= CMC_PLAUSIBLE[0]) & (s <= CMC_PLAUSIBLE[1])

    ok_kd = plaus("KIDDOBCMC")
    ok_ki = plaus("INTDATECMC")
    ok_kd_et = plaus("KIDDOBCMC_ET")
    ok_ki_et = plaus("INTDATECMC_ET")
    T["ok_kd"], T["ok_ki"], T["ok_kd_et"], T["ok_ki_et"] = ok_kd, ok_ki, ok_kd_et, ok_ki_et

    yr_ok = valid_mask("INTYEAR") & valid_mask("MONTHINT")
    ymd_g = (T["INTYEAR"] - 1900) * 12 + T["MONTHINT"]
    ymd_agree_g = (yr_ok & ok_ki & (ymd_g.values == T["INTDATECMC"].values))
    yr_et_ok = valid_mask("INTYEAR_ET") & valid_mask("MONTHINT_ET")
    ymd_et = (T["INTYEAR_ET"] - 1900) * 12 + T["MONTHINT_ET"]
    ymd_agree_et = (yr_et_ok & ok_ki_et & (ymd_et.values == T["INTDATECMC_ET"].values))
    T["ymd_agree_g"] = ymd_agree_g
    T["ymd_agree_et"] = ymd_agree_et

    age_g = T["INTDATECMC"].values - T["KIDDOBCMC"].values
    age_et = T["INTDATECMC_ET"].values - T["KIDDOBCMC_ET"].values
    both_g = ok_kd & ok_ki & (T["KIDDOBCMC"].values <= T["INTDATECMC"].values)
    both_et = ok_kd_et & ok_ki_et & (T["KIDDOBCMC_ET"].values <= T["INTDATECMC_ET"].values)
    kcm = T["KIDCURAGEMO"].values
    kcm_ok = valid_mask("KIDCURAGEMO")
    T["age_cal_greg"] = np.where(both_g, age_g, np.nan)
    T["age_cal_et"] = np.where(both_et, age_et, np.nan)
    T["kidcuragemo_valid"] = kcm_ok
    # Under-five rule: reported KIDCURAGEMO where delivered (ET, NG); otherwise the
    # Gregorian calendar-month difference (GH, KE, where KIDCURAGEMO is blank).
    # Calendar difference can exceed completed months by 1, so the rule is
    # conservative at the 59/60-month boundary; recorded in the source column.
    age_cal_g = T["age_cal_greg"].values
    T["under5_source"] = np.where(kcm_ok, "KIDCURAGEMO",
                                  np.where(both_g, "gregorian_CMC_difference", "none"))
    T["under5"] = np.where(kcm_ok, (kcm >= 0) & (kcm <= 59),
                           np.where(both_g, (age_cal_g >= 0) & (age_cal_g <= 59), False)).astype(bool)
    # Birth-date precision from KIDAGEINFO (IPUMS category codes, from the DDI)
    KA = T["KIDAGEINFO"].values
    T["birth_date_precision"] = np.select(
        [np.isin(KA, [1, 2]), KA == 3, np.isin(KA, list(range(4, 14))), KA == 14, KA == 15],
        ["complete_day_or_month_year", "year_season_only", "imputed_component",
         "inconsistent", "missing"], default="unclassified_or_blank")

    date_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        diff = np.where(both_g & kcm_ok, age_g - kcm, np.nan)[sel]
        diff = diff[~np.isnan(diff)]
        diff_et = np.where(both_et & kcm_ok, age_et - kcm, np.nan)[sel]
        diff_et = diff_et[~np.isnan(diff_et)]
        date_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "INTYEAR_valid": int((valid_mask("INTYEAR") & sel).sum()),
            "INTYEAR_matches_survey_year": int(((T["INTYEAR"] == T["YEAR"]) & sel).sum()),
            "INTDATECMC_valid_plausible": int((ok_ki & sel).sum()),
            "INTDATECMC_matches_INTYEAR_MONTHINT": int((ymd_agree_g & sel).sum()),
            "KIDDOBCMC_valid_plausible": int((ok_kd & sel).sum()),
            "INTDATECMC_ET_valid_plausible": int((ok_ki_et & sel).sum()),
            "INTDATECMC_ET_matches_ymd": int((ymd_agree_et & sel).sum()),
            "KIDDOBCMC_ET_valid_plausible": int((ok_kd_et & sel).sum()),
            "gregorian_birth_and_interview_both_valid": int((both_g & sel).sum()),
            "birth_after_interview_gregorian": int(((ok_kd & ok_ki) &
                                                    (T["KIDDOBCMC"].values > T["INTDATECMC"].values) & sel).sum()),
            "ET_birth_and_interview_both_valid": int((both_et & sel).sum()),
            "ET_birth_after_interview": int(((ok_kd_et & ok_ki_et) &
                                             (T["KIDDOBCMC_ET"].values > T["INTDATECMC_ET"].values) & sel).sum()),
            "KIDCURAGEMO_valid": int((kcm_ok & sel).sum()),
            "age_check_n_gregorian": int(len(diff)),
            "age_diff_gregorian_eq0": int((diff == 0).sum()),
            "age_diff_gregorian_eq1": int((diff == 1).sum()),
            "age_diff_gregorian_eq2": int((diff == 2).sum()),
            "age_diff_gregorian_lt0": int((diff < 0).sum()),
            "age_diff_gregorian_gt2": int((diff > 2).sum()),
            "KIDCURAGEMO_blank_or_nonnumeric": int((~kcm_ok & sel).sum()),
            "INTYEAR_distinct_values": int(T.loc[sel, "INTYEAR"].nunique()),
            "INTYEAR_ET_valid": int((valid_mask("INTYEAR_ET") & sel).sum()),
            "INTYEAR_ET_distinct_values": int(T.loc[sel, "INTYEAR_ET"].nunique()),
            "KIDDOBCMC_ET_minus_KIDDOBCMC_min": (float(np.min(T["KIDDOBCMC_ET"].values[sel & ok_kd_et & ok_kd] -
                                                              T["KIDDOBCMC"].values[sel & ok_kd_et & ok_kd]))
                                                 if (sel & ok_kd_et & ok_kd).any() else None),
            "KIDDOBCMC_ET_minus_KIDDOBCMC_max": (float(np.max(T["KIDDOBCMC_ET"].values[sel & ok_kd_et & ok_kd] -
                                                              T["KIDDOBCMC"].values[sel & ok_kd_et & ok_kd]))
                                                 if (sel & ok_kd_et & ok_kd).any() else None),
            "birth_precision_counts": json.dumps(dict(Counter(
                T.loc[sel, "birth_date_precision"].values))),
            "under5_source_counts": json.dumps(dict(Counter(T.loc[sel, "under5_source"].values))),
            "under5_n": int((T["under5"].values & sel).sum()),
            "age_check_n_ET_calendar": int(len(diff_et)),
            "age_diff_ET_eq0": int((diff_et == 0).sum()),
            "age_diff_ET_eq1": int((diff_et == 1).sum()),
            "age_diff_ET_eq2": int((diff_et == 2).sum()),
            "age_diff_ET_other": int(((diff_et < 0) | (diff_et > 2)).sum()),
            "KIDAGEINFO_counts": json.dumps({str(int(k)): int(v) for k, v in
                                            pd.Series(T.loc[sel & valid_mask("KIDAGEINFO"), "KIDAGEINFO"]).value_counts().items()}),
        })
    date_df = pd.DataFrame(date_rows)
    date_df.to_csv(R("date_validation_v2.csv"), index=False)
    log("date validation:\n" + date_df.T.to_string())

    # ---- 9. Anthropometry (documented x100 Z-scores) ------------------
    anth_rows = []
    z_cols = {"HAZ": ("HWHAZWHO", HAZ_WHO), "WAZ": ("HWWAZWHO", WAZ_WHO), "WHZ": ("HWWHZWHO", WHZ_WHO)}
    for zname, (src, lim) in z_cols.items():
        vm = valid_mask(src)
        T[f"{zname}_valid"] = vm
        T[f"{zname}"] = np.where(vm, T[src].values / 100.0, np.nan)
        T[f"{zname}_who_flag"] = vm & ((T[f"{zname}"].values < lim[0]) | (T[f"{zname}"].values > lim[1]))
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        for zname, (src, lim) in z_cols.items():
            v = T[src].values[sel]
            vm = T[f"{zname}_valid"].values[sel]
            zv = T[zname].values[sel][vm]
            codes = {c: int((v == c).sum()) for c in (9995.0, 9996.0, 9997.0, 9998.0, 9999.0)}
            q = q_stats(zv)
            anth_rows.append({
                "sample": lab, "outcome": zname, "rows": int(sel.sum()),
                "raw_valid_nonflag": int(vm.sum()),
                "code_9995_height_implausible": codes[9995.0],
                "code_9996_age_days_implausible": codes[9996.0],
                "code_9997_flagged": codes[9997.0],
                "code_9998_missing": codes[9998.0],
                "code_9999_NIU": codes[9999.0],
                "blank_or_nonnumeric": int(np.isnan(v).sum()),
                "z_min": q[0], "z_p1": q[1], "z_p5": q[2], "z_p50": q[3],
                "z_p95": q[4], "z_p99": q[5], "z_max": q[6],
                "outside_WHO_flag_limits": int(T[f"{zname}_who_flag"].values[sel].sum()),
                "WHO_limits_used": f"{lim[0]} to {lim[1]}",
            })
    anth_df = pd.DataFrame(anth_rows)
    anth_df.to_csv(R("anthropometry_summary_v2.csv"), index=False)
    log("anthropometry:\n" + anth_df[["sample", "outcome", "raw_valid_nonflag", "z_min", "z_p50",
                                       "z_max", "outside_WHO_flag_limits"]].to_string(index=False))

    joint = {}
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        joint[lab] = {
            "HAZ_valid": int((T["HAZ_valid"].values & sel).sum()),
            "WAZ_valid": int((T["WAZ_valid"].values & sel).sum()),
            "WHZ_valid": int((T["WHZ_valid"].values & sel).sum()),
            "all_three_valid": int((T["HAZ_valid"].values & T["WAZ_valid"].values &
                                    T["WHZ_valid"].values & sel).sum()),
        }
    log(f"joint outcome availability: {joint}")

    # ---- 10. Weights and design ---------------------------------------
    w_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        for wname in ["PERWEIGHT", "KIDWT"]:
            v = T[wname].values[sel]
            fin = v[~np.isnan(v)]
            w_rows.append({
                "sample": lab, "weight": wname, "rows": int(sel.sum()),
                "missing_or_blank": int(np.isnan(v).sum()),
                "positive": int((fin > 0).sum()), "zero": int((fin == 0).sum()),
                "negative": int((fin < 0).sum()),
                "sum_raw": float(fin.sum()), "mean_raw": float(fin.mean()) if len(fin) else np.nan,
                "min_raw": float(fin.min()) if len(fin) else np.nan,
                "max_raw": float(fin.max()) if len(fin) else np.nan,
                "rows_with_valid_HAZ": int((T["HAZ_valid"].values[sel] & ~np.isnan(v)).sum()),
            })
    w_df = pd.DataFrame(w_rows)
    w_df.to_csv(R("weights_summary_v2.csv"), index=False)
    log("weights:\n" + w_df.to_string(index=False))

    d_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        psu = T.loc[sel, "PSU"]
        idpsu = T.loc[sel, "IDHSPSU"]
        pair = pd.DataFrame({"PSU": psu.values, "IDHSPSU": idpsu.values})
        d_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "IDHSPSU_missing": int(idpsu.isna().sum()),
            "PSU_missing": int(psu.isna().sum()),
            "IDHSSTRATA_missing": int(T.loc[sel, "IDHSSTRATA"].isna().sum()),
            "STRATA_missing": int(T.loc[sel, "STRATA"].isna().sum()),
            "DOMAIN_distinct": int(T.loc[sel, "DOMAIN"].nunique()),
            "PSU_distinct_sample_specific": int(psu.nunique()),
            "IDHSPSU_distinct": int(idpsu.nunique()),
            "IDHSPSU_maps_to_multiple_PSU": int((pair.groupby("IDHSPSU")["PSU"].nunique() > 1).sum()),
            "PSU_maps_to_multiple_IDHSPSU": int((pair.groupby("PSU")["IDHSPSU"].nunique() > 1).sum()),
        })
    d_df = pd.DataFrame(d_rows)
    d_df.to_csv(R("design_summary_v2.csv"), index=False)
    log("design:\n" + d_df.to_string(index=False))

    # ---- 11. Geography (no coordinates printed) -----------------------
    g_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        la = T.loc[sel, "GPSLAT"].values
        lo = T.loc[sel, "GPSLONG"].values
        ll = T.loc[sel, "GPSLATLONG"].values
        pair_ok = ~np.isnan(la) & ~np.isnan(lo)
        zero_pair = pair_ok & (la == 0) & (lo == 0)
        in_range = pair_ok & (np.abs(la) <= 90) & (np.abs(lo) <= 180)
        g = pd.DataFrame({"psu": T.loc[sel, "IDHSPSU"].values,
                          "la": np.round(la, 6), "lo": np.round(lo, 6)})
        gv = g[pair_ok & in_range & ~zero_pair]
        multi = int((gv.groupby("psu")[["la", "lo"]].nunique().max(axis=1) > 1).sum())
        g_rows.append({
            "sample": lab, "rows": int(sel.sum()),
            "GPSLAT_nonmissing": int((~np.isnan(la)).sum()),
            "GPSLONG_nonmissing": int((~np.isnan(lo)).sum()),
            "GPSLATLONG_nonmissing": int((~np.isnan(ll)).sum()),
            "pair_both_present": int(pair_ok.sum()),
            "zero_pairs": int(zero_pair.sum()),
            "out_of_range_pairs": int((pair_ok & ~in_range).sum()),
            "abs_gt_90_lat_values": int((np.abs(la[~np.isnan(la)]) > 90).sum()),
            "non_integer_lat_values": int((np.mod(la[~np.isnan(la)], 1) != 0).sum()),
            "usable_pairs_nonzero_in_range": int(len(gv)),
            "PSUs_with_coordinates": int(gv["psu"].nunique()),
            "PSUs_with_more_than_one_coordinate_pair": multi,
            "GPSLAT_equals_GPSLATLONG_rows": int(np.sum(np.isclose(la, ll, equal_nan=False))),
        })
    g_df = pd.DataFrame(g_rows)
    g_df.to_csv(R("geography_summary_v2.csv"), index=False)
    log("geography (counts only):\n" + g_df.to_string(index=False))

    # ---- 12. Historical timing eligibility (CMC arithmetic) -----------
    key_ok = T["child_key_valid"].values
    greg_ok = ok_kd & ok_ki
    et_ok = ok_kd_et & ok_ki_et
    b = np.where(greg_ok, T["KIDDOBCMC"].values, 0.0)
    t = np.where(greg_ok, T["INTDATECMC"].values, 0.0)
    is_et_row = is_et
    cal_unres = is_et_row & ~greg_ok & et_ok
    windows = {
        "birth_year": (np.floor((b - 1) / 12) * 12 + 1, np.floor((b - 1) / 12) * 12 + 12, None),
        "prenatal_9m": (b - 9, b - 1, None),
        "post_12m": (b, b + 11, b + 12),
        "post_24m": (b, b + 23, b + 24),
    }
    elig_cols = {}
    for wname, (st, en, need) in windows.items():
        c_key = ~key_ok
        c_cal = cal_unres
        c_miss = ~greg_ok & ~cal_unres
        c_after = greg_ok & (b > t)
        c_before = greg_ok & (st < CMC_RASTER[0])
        c_after17 = greg_ok & (en > CMC_RASTER[1])
        c_inc = (greg_ok & (t < need)) if need is not None else np.zeros(len(T), bool)
        labels = ["key_invalid", "calendar_unresolved_ET", "dates_missing_or_implausible",
                  "birth_after_interview", "window_before_2000", "window_after_2017",
                  "postnatal_incomplete_at_interview"]
        conds = [c_key, c_cal, c_miss, c_after, c_before, c_after17, c_inc]
        status = np.select(conds, labels, default="eligible_timing")
        status = np.where(key_ok, status, "key_invalid")
        elig_cols[f"elig_{wname}"] = status
        end_year = np.floor((np.where(greg_ok, en, 0) - 1) / 12) + 1900
        int_year = np.floor((t - 1) / 12) + 1900
        elig_cols[f"flag_{wname}_annual_includes_interview_year"] = (
            (status == "eligible_timing") & (end_year >= int_year))
    for k, v in elig_cols.items():
        T[k] = v

    e_rows = []
    for sid, lab in SAMPLES.items():
        sel = (T["SAMPLE"] == sid).values
        for wname in windows:
            s = pd.Series(T.loc[sel, f"elig_{wname}"].values).value_counts()
            row = {"sample": lab, "window": wname, "rows": int(sel.sum())}
            for lbl in ["eligible_timing", "key_invalid", "calendar_unresolved_ET",
                        "dates_missing_or_implausible", "birth_after_interview",
                        "window_before_2000", "window_after_2017",
                        "postnatal_incomplete_at_interview"]:
                row[lbl] = int(s.get(lbl, 0))
            row["eligible_and_under5"] = int(((T[f"elig_{wname}"] == "eligible_timing") &
                                              T["under5"].values & sel).sum())
            row["eligible_and_under5_precision_complete"] = int(
                ((T[f"elig_{wname}"] == "eligible_timing") & T["under5"].values &
                 (T["birth_date_precision"].values == "complete_day_or_month_year") & sel).sum())
            row["eligible_flag_annual_includes_interview_year"] = int(
                (T[f"flag_{wname}_annual_includes_interview_year"] & sel).sum())
            for oc in ["HAZ", "WAZ", "WHZ"]:
                row[f"eligible_and_{oc}_valid"] = int(((T[f"elig_{wname}"] == "eligible_timing") &
                                                       T[f"{oc}_valid"] & sel).sum())
            e_rows.append(row)
    e_df = pd.DataFrame(e_rows)
    e_df.to_csv(R("eligibility_timing_v2.csv"), index=False)
    log("timing eligibility:\n" + e_df.to_string(index=False))

    # ---- 13. Persist derived dataset ----------------------------------
    derived_cols = ["record_number", "sample_label", "child_key", "child_key_valid", "woman_key",
                    "household_key", "ok_kd", "ok_ki", "ok_kd_et", "ok_ki_et", "ymd_agree_g",
                    "ymd_agree_et", "age_cal_greg", "age_cal_et", "kidcuragemo_valid",
                    "under5", "under5_source", "birth_date_precision", "HAZ", "WAZ", "WHZ",
                    "HAZ_valid", "WAZ_valid",
                    "WHZ_valid", "HAZ_who_flag", "WAZ_who_flag", "WHZ_who_flag"] + \
                   list(elig_cols.keys())
    deriv = T[derived_cols].copy()
    for c in ["SAMPLE", "COUNTRY", "YEAR", "INTYEAR", "KIDDOBCMC", "INTDATECMC",
              "KIDDOBCMC_ET", "INTDATECMC_ET", "KIDCURAGEMO", "HWHAZWHO", "HWWAZWHO", "HWWHZWHO",
              "PERWEIGHT", "KIDWT", "IDHSPSU", "PSU", "IDHSSTRATA", "STRATA", "DOMAIN",
              "GPSLAT", "GPSLONG", "GPSLATLONG", "BIDX", "AGE", "URBAN", "EDUCLVL", "WEALTHQ",
              "MARSTAT", "KIDSEX", "KIDAGEINFO"]:
        deriv[c] = T[c].values
    deriv.to_parquet(R(f"idhs_00002_derived_{run_id}.parquet"), index=False)
    log(f"derived dataset rows={len(deriv)} cols={deriv.shape[1]}")

    # ---- 14. Comparison with idhs_00001 -------------------------------
    comp_rows = []
    if os.path.isfile(V1_RAW):
        v1 = pd.read_parquet(V1_RAW)
        v1_bidx_ok = v1["BIDX"].str.strip().str.fullmatch(r"\d+").fillna(False)
        v1["ckey"] = [f"{int(s)}|{c.strip()}|{int(b)}" if ok else "" for s, c, b, ok in
                      zip(v1["SAMPLE"].astype(int), v1["CASEID"], v1["BIDX"], v1_bidx_ok)]
        v1_unique = v1.loc[v1["ckey"] != "", "ckey"].is_unique
        v2_unique = deriv.loc[deriv["child_key_valid"], "child_key"].is_unique
        v1_keys = set(v1.loc[v1["ckey"] != "", "ckey"])
        v2_keys = set(deriv.loc[deriv["child_key_valid"], "child_key"])
        v1_pers = v1.groupby(v1["SAMPLE"].str.strip().astype(int))["CASEID"].nunique()
        for sid, lab in SAMPLES.items():
            n1 = int((v1["SAMPLE"].str.strip().astype(int) == sid).sum())
            n2 = int((T["SAMPLE"] == sid).sum())
            comp_rows.append({
                "sample": lab, "rows_v1": n1, "rows_v2": n2,
                "unique_women_v1": int(v1_pers.get(sid, 0)),
                "unique_women_v2": int(T.loc[T["SAMPLE"] == sid, "woman_key"].replace("", np.nan).nunique()),
            })
        comp_rows.append({"sample": "ALL", "rows_v1": len(v1), "rows_v2": len(T),
                          "unique_women_v1": None, "unique_women_v2": None,
                          "child_key_unique_v1": bool(v1_unique), "child_key_unique_v2": bool(v2_unique),
                          "keys_in_both": len(v1_keys & v2_keys),
                          "keys_only_v1": len(v1_keys - v2_keys),
                          "keys_only_v2": len(v2_keys - v1_keys)})
        if v1_unique and v2_unique:
            m = v1[["ckey", "PERWEIGHT", "AGE", "EDUCLVL", "URBAN", "WEALTHQ", "MARSTAT",
                    "LINENOKID", "IDHSPID", "IDHSHID"]].merge(
                pd.DataFrame({"ckey": deriv.loc[deriv["child_key_valid"], "child_key"].values,
                              "PERWEIGHT_v2": T.loc[T["child_key_valid"].values, "PERWEIGHT"].values,
                              "AGE_v2": T.loc[T["child_key_valid"].values, "AGE"].values,
                              "EDUCLVL_v2": T.loc[T["child_key_valid"].values, "EDUCLVL"].values,
                              "URBAN_v2": T.loc[T["child_key_valid"].values, "URBAN"].values,
                              "WEALTHQ_v2": T.loc[T["child_key_valid"].values, "WEALTHQ"].values,
                              "MARSTAT_v2": T.loc[T["child_key_valid"].values, "MARSTAT"].values,
                              }), on="ckey", how="inner", validate="one_to_one")
            eq = {}
            for a, bcol in [("PERWEIGHT", "PERWEIGHT_v2"), ("AGE", "AGE_v2"), ("EDUCLVL", "EDUCLVL_v2"),
                            ("URBAN", "URBAN_v2"), ("WEALTHQ", "WEALTHQ_v2"), ("MARSTAT", "MARSTAT_v2")]:
                v1num = pd.to_numeric(m[a].str.strip(), errors="coerce")
                eq[a] = int((np.isclose(v1num.values, m[bcol].values.astype(float), equal_nan=False)).sum())
            comp_rows.append({"sample": "MATCHED_KEYS", "rows_v1": len(m), "rows_v2": len(m),
                              **{f"equal_{k}": v for k, v in eq.items()}})
    comp_df = pd.DataFrame(comp_rows)
    comp_df.to_csv(R("v1_v2_comparison_v2.csv"), index=False)
    log("v1 vs v2:\n" + comp_df.to_string(index=False))

    # ---- 15. Source preservation and manifest -------------------------
    for k, p in SRC.items():
        src_info[k]["sha256_after"] = sha256_file(p)
        src_info[k]["unchanged"] = src_info[k]["sha256_before"] == src_info[k]["sha256_after"]
    log(f"sources unchanged: {all(v['unchanged'] for v in src_info.values())}")
    manifest = {
        "run_id": run_id,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "script": "scripts/historical_wash/03_import_validate_idhs_00002.py",
        "script_sha256": sha256_file(__file__),
        "command": "python scripts\\historical_wash\\03_import_validate_idhs_00002.py",
        "interpreter": sys.executable,
        "python": platform.python_version(),
        "packages": {"pandas": pd.__version__, "numpy": np.__version__, "pyarrow": pa.__version__},
        "sources": src_info,
        "download_candidates": [os.path.basename(c) for c in candidates],
        "records": n_records,
        "record_width": W,
        "layout_gaps": gaps,
        "outputs": sorted(os.listdir(run_dir)),
        "status": "completed_import_and_validation",
        "unresolved_issues": [
            "KIDDOBCMC/INTDATECMC Gregorian status for Ethiopia 2016 (see date_validation_v2.csv)",
            "HWHAZWHO ages: measurement date not delivered; interview date used as proxy",
            "GPSLATLONG use requires DHS permission confirmation (not verified here)",
            "KIDWT scale and use not documented in the extract files",
            "WHO flag limits taken from secondary sources; confirm against WHO Anthro documentation",
        ],
    }
    with open(R("manifest_v2.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, default=str)
    log("manifest written")
    with open(R("execution_log_v2.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("FAILED:\n" + traceback.format_exc())
        raise
