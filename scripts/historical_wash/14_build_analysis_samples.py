"""
14_build_analysis_samples.py
============================
Analysis-sample construction for the historical WASH extension (preparation only; no outcome
model is estimated here).

Inputs (read-only):
  - validated idhs_00002 typed run (child records, outcomes, controls, weights)
  - child exposure candidates (construction run 20261006T183803Z)
Outputs (new run directory, restricted, outside the repository):
  - analysis_candidates_RESTRICTED.parquet   one row per child x timing candidate
  - sample_flow_AGGREGATE.csv                mutually exclusive, ordered exclusion counts
  - ethiopia_birthyear_candidate_rules.csv   which rule explains candidate differences
  - age_rule_reconciliation.csv              reported vs derived age (aggregate)
  - manifest.json, execution_log.txt

Under-five rule (documented; see specification):
  age_reported  = KIDCURAGEMO (completed months) where delivered (Ethiopia 2016, Nigeria 2018)
  age_derived   = interview CMC - birth CMC (calendar-month difference). Ethiopia uses its own
                  Ethiopian-calendar pair (INTDATECMC_ET - KIDDOBCMC_ET), which needs no conversion.
  under5 = age_reported in 0..59 if delivered; otherwise age_derived in 0..59.
  Negative derived age (interview before birth) -> birth_after_interview; never silently repaired.
  Calendar difference 60 with reported completed age <= 59 is resolved by the reported value.
  Disagreement flag: derived - reported not in {0, 1}; preserved, not corrected.
Outcome validity: HAZ/WAZ/WHZ value not NaN, not 9995-9998 (flag/missing), not 9999 (not in universe).
Spatial rules and windows: taken from the construction run (complete primary construction).
"""
import argparse
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
RUN_ID = "20261006T140022Z"
TYPED = os.path.join(MASTER, "data", "processed", "ipums_import", "v2", f"run_{RUN_ID}", f"idhs_00002_typed_{RUN_ID}.parquet")
CONS = os.path.join(MASTER, "data", "processed", "child_exposure", "run_20261006T183803Z", "child_exposure_candidates_RESTRICTED.parquet")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "analysis_samples")
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
OUTCOMES = {"HAZ": "HWHAZWHO", "WAZ": "HWWAZWHO", "WHZ": "HWWHZWHO"}
FLAG_CODES = [9995.0, 9996.0, 9997.0, 9998.0]
NIU = 9999.0
WINDOWS = ["birth_year", "prenatal_9m", "post_12m", "post_24m"]
PRODUCTS = ["W_IMP", "S_IMP"]
log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    log_lines.append(line)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def age_rules(typed):
    """Per-record age rules (candidate-independent parts)."""
    a = pd.DataFrame({"record_number": typed["record_number"].values, "SAMPLE": typed["SAMPLE"].values})
    rep = typed["KIDCURAGEMO"].astype(float).values
    a["age_reported"] = rep
    a["has_reported"] = ~np.isnan(rep)
    b_g = typed["KIDDOBCMC"].astype(float).values
    t_g = typed["INTDATECMC"].astype(float).values
    b_e = typed["KIDDOBCMC_ET"].astype(float).values
    t_e = typed["INTDATECMC_ET"].astype(float).values
    et = typed["SAMPLE"].values == 23104
    der = np.where(et, t_e - b_e, t_g - b_g)
    a["age_derived"] = der
    a["age_derived_basis"] = np.where(et, "ET_calendar_pair", "gregorian_CMC_pair")
    diff = der - rep
    a["derived_minus_reported"] = diff
    a["age_disagreement_outside_0_1"] = a["has_reported"] & ~np.isin(diff, [0.0, 1.0]) & ~np.isnan(diff)
    a["derived_negative"] = (der < 0)
    a["calendar_60"] = (der == 60)
    under5_rep = a["has_reported"] & (rep >= 0) & (rep <= 59)
    under5_der = (~a["has_reported"]) & (der >= 0) & (der <= 59)
    a["under5"] = under5_rep | under5_der
    a["under5_basis"] = np.select([a["has_reported"], ~a["has_reported"]], ["reported_KIDCURAGEMO", "derived_CMC"], "none")
    return a


def outcome_status(typed):
    out = {}
    for oc, col in OUTCOMES.items():
        x = typed[col].astype(float).values
        univ = ~np.isnan(x) & (x != NIU)
        flagged = np.isin(x, FLAG_CODES)
        valid = univ & ~flagged
        out[oc] = {"universe": univ, "valid": valid, "z": np.where(valid, x / 100.0, np.nan)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(OUT_ROOT, f"run_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    log(f"python={platform.python_version()} pandas={pd.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha(__file__)}")
    before = {"typed": sha(TYPED), "cons": sha(CONS)}

    typed = pd.read_parquet(TYPED, columns=[
        "record_number", "SAMPLE", "IDHSPSU", "IDHSHID", "URBAN", "KIDSEX", "AGE", "EDUCLVL", "MARSTAT",
        "WEALTHQ", "KIDDOBCMC", "INTDATECMC", "INTDATECMC_ET", "KIDDOBCMC_ET", "INTYEAR", "KIDCURAGEMO",
        "LINENOKID", "HWHAZWHO", "HWWAZWHO", "HWWHZWHO", "PERWEIGHT", "KIDWT"])
    cons = pd.read_parquet(CONS)
    log(f"typed records={len(typed)}; construction candidate rows={len(cons)}")

    rules = age_rules(typed)
    rec = typed.merge(rules, on=["record_number", "SAMPLE"], how="left")
    oc = outcome_status(typed)

    # ---- age agreement table (aggregate)
    agree = []
    for sid, lab in SAMPLES.items():
        m = (rec["SAMPLE"] == sid).values
        sub = rec[m]
        has = sub["has_reported"].values
        d = sub.loc[has, "derived_minus_reported"].values
        agree.append({"sample": lab, "records": int(m.sum()), "reported_available": int(has.sum()),
                      "reported_absent": int((~has).sum()),
                      "derived_minus_reported_0": int((d == 0).sum()), "derived_minus_reported_1": int((d == 1).sum()),
                      "outside_0_1_negative": int((d < 0).sum()), "outside_0_1_ge2": int((d >= 2).sum()),
                      "derived_negative": int(sub["derived_negative"].sum()),
                      "derived_calendar_60": int(sub["calendar_60"].sum()),
                      "under5_by_reported": int((sub["under5_basis"] == "reported_KIDCURAGEMO").sum()),
                      "under5_by_derived": int((sub["under5_basis"] == "derived_CMC").sum()),
                      "under5_total": int(sub["under5"].sum())})
    agree_df = pd.DataFrame(agree)
    agree_df.to_csv(os.path.join(out_dir, "age_rule_reconciliation_AGGREGATE.csv"), index=False)
    log("age reconciliation:\n" + agree_df.to_string(index=False))

    # ---- candidate analysis table
    # construction table already carries candidate, birth/interview CMC, date flag, cluster index,
    # the complete-spatial statuses and exposures; add the child-level variables from the typed run.
    # the construction table already holds the birth and interview CMC as 'b' and 't'
    cand = cons.drop(columns=[c_ for c_ in ["birth_cmc", "interview_cmc", "age_months_cal"] if c_ in cons.columns]).copy()
    rec_extra = rec.drop(columns=[c_ for c_ in rec.columns if c_ in cand.columns and c_ != "record_number"])
    cand = cand.merge(rec_extra, on="record_number", how="left")
    cand["t_year"] = np.where(np.isnan(cand["t"]), np.nan, (cand["t"] - 1) // 12 + 1900)
    cand["b_year"] = np.where(np.isnan(cand["b"]), np.nan, (cand["b"] - 1) // 12 + 1900)
    # candidate-specific derived age: Ethiopia's candidate t with Gregorian birth CMC is NOT used for the
    # under-5 rule (it uses the Ethiopian-calendar pair); the candidate t only enters timing rules.
    cand["age_cal_candidate"] = cand["t"] - cand["b"]

    # outcome values (align by record_number)
    idx = typed.reset_index(drop=True)
    pos = pd.Series(np.arange(len(idx)), index=idx["record_number"].values)
    ii = cand["record_number"].map(pos).values
    for k, v in oc.items():
        cand[f"{k}_valid"] = v["valid"][ii]
        cand[f"{k}_universe"] = v["universe"][ii]
        cand[f"{k}_z"] = v["z"][ii]

    # ---- exclusion flow per outcome x window x product (sequential, mutually exclusive)
    flows = []
    for product in PRODUCTS:
        for window in WINDOWS:
            st = cand[f"{product}_{window}_complete_status"].values
            for k in OUTCOMES:
                for (cname, sid), sub_idx in cand.groupby(["candidate", "SAMPLE"]).groups.items():
                    s = cand.loc[sub_idx]
                    sst = s[f"{product}_{window}_complete_status"].values
                    u5 = s["under5"].values.astype(bool)
                    univ = s[f"{k}_universe"].values.astype(bool)
                    val = s[f"{k}_valid"].values.astype(bool)
                    dok = s["date_ok"].values.astype(bool)
                    cats = [
                        sst == "unmatched_cluster",
                        ~u5,
                        ~univ,
                        ~val,
                        ~dok,
                        sst == "birth_after_interview",
                        sst == "window_outside_2000_2017",
                        sst == "postnatal_incomplete",
                        sst == "spatial_missing_year",
                        sst == "spatial_partial_year",
                    ]
                    labs = ["unmatched_cluster", "not_under5", "not_in_universe", "outcome_flagged_or_missing",
                            "dates_invalid", "birth_after_interview", "window_outside_2000_2017",
                            "postnatal_incomplete", "spatial_missing_year", "spatial_partial_year"]
                    cat = np.select(cats, labs, default="final_analysis_sample")
                    for lab, n in pd.Series(cat).value_counts().items():
                        flows.append({"candidate": cname, "sample": SAMPLES[int(sid)], "product": product,
                                      "window": window, "outcome": k, "category": lab, "records": int(n)})
    flow = pd.DataFrame(flows)
    flow.to_csv(os.path.join(out_dir, "sample_flow_AGGREGATE.csv"), index=False)
    tot = flow.groupby(["candidate", "sample", "product", "window", "outcome"])["records"].sum().reset_index()
    recs = cand.groupby(["candidate", "SAMPLE"]).size().rename("n").reset_index()
    recs["sample"] = recs["SAMPLE"].map(SAMPLES)
    chk = tot.merge(recs[["candidate", "sample", "n"]], on=["candidate", "sample"])
    flow_ok = bool((chk["records"] == chk["n"]).all())
    log(f"flow categories sum to records in every row: {flow_ok}")

    # ---- Ethiopia birth-year candidate rule attribution
    # Which status (rule) differs across the three Ethiopian candidates, birth-year window, W_IMP.
    et = cand[cand["SAMPLE"] == 23104].copy()
    cands = ["ET_C1_triple_provisional", "ET_C2_century_1907_provisional", "ET_C3_century_2015_provisional"]
    stat = et.pivot_table(index="record_number", columns="candidate", values="W_IMP_birth_year_complete_status",
                          aggfunc="first")[cands]
    differ = stat.nunique(axis=1, dropna=False) > 1
    pattern = stat[differ].reset_index(drop=True)
    ct = pattern.value_counts().reset_index(name="records")
    ct.columns = ["C1_status", "C2_status", "C3_status", "records"]
    ct.to_csv(os.path.join(out_dir, "ethiopia_birthyear_candidate_rules_AGGREGATE.csv"), index=False)
    log("Ethiopia birth-year candidate status patterns (records whose status differs):\n" + ct.to_string(index=False))
    # Attribution: birth-after-interview depends on the candidate interview month; test directly.
    b_et = et.pivot_table(index="record_number", columns="candidate", values="b", aggfunc="first")[cands]
    t_et = et.pivot_table(index="record_number", columns="candidate", values="t", aggfunc="first")[cands]
    after = pd.DataFrame({c_: (b_et[c_] > t_et[c_]) for c_ in cands})
    attr = {"records_differing": int(differ.sum()),
            "birth_after_interview_by_candidate": {c_: int(after[c_].sum()) for c_ in cands},
            "dates_missing_C1_only": int((stat["ET_C1_triple_provisional"] == "dates_missing").sum())}
    with open(os.path.join(out_dir, "ethiopia_birthyear_attribution_AGGREGATE.json"), "w", encoding="utf-8") as f:
        json.dump(attr, f, indent=1)
    log("Ethiopia birth-year attribution: " + json.dumps(attr))

    # ---- analysis-ready dataset (restricted)
    keep_cols = ["record_number", "candidate", "SAMPLE", "IDHSPSU", "IDHSHID", "URBAN", "KIDSEX", "AGE", "EDUCLVL",
                 "MARSTAT", "WEALTHQ", "b", "t", "date_ok", "b_year", "t_year", "age_cal_candidate",
                 "age_reported", "age_derived", "age_derived_basis", "derived_minus_reported",
                 "age_disagreement_outside_0_1", "derived_negative", "calendar_60", "under5", "under5_basis",
                 "PERWEIGHT", "KIDWT", "HAZ_valid", "WAZ_valid", "WHZ_valid", "HAZ_z", "WAZ_z", "WHZ_z",
                 "HAZ_universe", "WAZ_universe", "WHZ_universe"]
    ex_cols = [c for c in cand.columns if c.endswith("_complete_exposure") or c.endswith("_complete_status")
               or c.endswith("_post_interview_year_used") or c.endswith("_min_valid_fraction_complete")]
    out = cand[keep_cols + ex_cols].copy()
    out["cluster_key"] = out["IDHSPSU"]          # IDHSPSU is unique across samples (documented)
    out.to_parquet(os.path.join(out_dir, "analysis_candidates_RESTRICTED.parquet"), index=False)
    log(f"analysis-ready rows={len(out)} columns={out.shape[1]}")

    after = {"typed": sha(TYPED), "cons": sha(CONS)}
    manifest = {"script": "scripts/historical_wash/14_build_analysis_samples.py",
                "script_sha256": sha(__file__), "interpreter": sys.executable,
                "python": platform.python_version(),
                "packages": {"pandas": pd.__version__, "numpy": np.__version__, "pyarrow": pa.__version__},
                "inputs_before": before, "inputs_after": after, "inputs_unchanged": before == after,
                "flow_categories_reconcile": flow_ok, "analysis_rows": int(len(out)),
                "status": "completed_sample_construction"}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    with open(os.path.join(out_dir, "execution_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"done -> {out_dir}")


if __name__ == "__main__":
    main()
