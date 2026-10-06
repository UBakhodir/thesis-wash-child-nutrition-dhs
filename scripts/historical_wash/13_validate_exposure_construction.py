"""
13_validate_exposure_construction.py
====================================
Validation, readiness and variation diagnostics for a construction run from
12_construct_exposure_windows.py. Reads restricted outputs read-only; writes aggregate
tables to a new folder inside the construction run. Outcome associations are NOT estimated:
the only regressions-like step is exposure-on-fixed-effects residual variance (diagnostic).

Usage: python 13_validate_exposure_construction.py <construction_run_folder>
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    sys.exit("usage: 13_validate_exposure_construction.py <construction_run_folder>")
RUN = sys.argv[1]
RUN_ID = "20261006T140022Z"
TYPED = os.path.join(r"C:\Users\user\Documents\Graduation_Thesis", "data", "processed", "ipums_import", "v2",
                     f"run_{RUN_ID}", f"idhs_00002_typed_{RUN_ID}.parquet")
EXTRACT = os.path.join(r"C:\Users\user\Documents\Graduation_Thesis", "data", "processed", "spatial_extraction",
                       "run_v3_20261006T183003Z", "cluster_year_extraction_RESTRICTED.parquet")
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join(RUN, f"validation_aggregates_{STAMP}")
os.makedirs(OUT, exist_ok=False)
log = []


def say(msg):
    print(f"{datetime.now(timezone.utc).isoformat()} {msg}", flush=True)
    log.append(msg)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


hash_before = {"typed": sha(TYPED), "extract": sha(EXTRACT)}
child = pd.read_parquet(os.path.join(RUN, "child_exposure_candidates_RESTRICTED.parquet"))
typed = pd.read_parquet(TYPED, columns=["record_number", "SAMPLE", "IDHSPSU", "URBAN", "GPSLAT", "GPSLONG",
                                        "HWHAZWHO", "HWWAZWHO", "HWWHZWHO", "LINENOKID"])
ex = pd.read_parquet(EXTRACT, columns=["IDHSPSU", "product", "estimate", "year", "method", "status",
                                       "valid_fraction", "value"])
child["sample"] = child["SAMPLE"].map(SAMPLES)
res = {}

# ---------------------------------------------------------------- A. merge and key checks
res["child_records_typed"] = int(len(typed))
res["typed_record_number_unique"] = bool(typed["record_number"].is_unique)
cand_n = child.groupby("candidate").size().to_dict()
res["candidate_rows_by_candidate"] = {k: int(v) for k, v in cand_n.items()}
res["child_candidate_pairs_unique"] = bool(child.duplicated(["record_number", "candidate"]).sum() == 0)
res["rows_before_merge_equals_after"] = bool(len(child) == 60772 + 3 * 10641)
mean = ex[ex["estimate"] == "MEAN"]
key_dup = int(mean.duplicated(["IDHSPSU", "product", "year", "method"]).sum())
res["annual_extraction_key_duplicates_MEAN"] = key_dup
res["annual_rows_MEAN"] = int(len(mean))
# cardinality of child -> cluster-year: count of cluster-year rows per child is at most one per year
clusters_with_extract = set(mean.loc[mean["method"] == "primary_area_buffer", "IDHSPSU"].unique())
typed["usable"] = typed["GPSLAT"].notna() & typed["GPSLONG"].notna() & ~((typed["GPSLAT"] == 0) & (typed["GPSLONG"] == 0))
typed["in_extract"] = typed["IDHSPSU"].isin(clusters_with_extract)
um = typed[~typed["in_extract"]]
reasons = pd.DataFrame({
    "sample": um["SAMPLE"].map(SAMPLES).values,
    "reason": np.where(~um["usable"].values, "no_usable_coordinates",
                       np.where(~um["URBAN"].isin([1, 2]).values, "urban_code_not_1_or_2", "other")),
})
reasons_tab = reasons.groupby(["sample", "reason"]).size().rename("child_records").reset_index()
reasons_tab.to_csv(os.path.join(OUT, "unmatched_children_reasons.csv"), index=False)
res["unmatched_child_records_typed_level"] = int(len(um))
res["unmatched_reason_counts"] = {f"{a}|{b}": int(c) for a, b, c in
                                  reasons_tab[["sample", "reason", "child_records"]].values}
say("A. merge: " + json.dumps({k: res[k] for k in ["child_records_typed", "child_candidate_pairs_unique",
                                                   "rows_before_merge_equals_after",
                                                   "annual_extraction_key_duplicates_MEAN",
                                                   "unmatched_child_records_typed_level"]}))

# ---------------------------------------------------------------- B. coverage reconciliation
cov = ex.groupby(["product", "estimate", "method", "status"]).size().unstack(fill_value=0)
cov["rows"] = cov.sum(axis=1)
cov.to_csv(os.path.join(OUT, "coverage_reconciliation_all_estimates.csv"))
expected = ex.groupby(["product", "estimate", "method"]).agg(clusters=("IDHSPSU", "nunique"), rows=("year", "size"))
expected["expected_rows_clusters_x18"] = expected["clusters"] * 18
expected.to_csv(os.path.join(OUT, "coverage_row_denominators.csv"))
res["coverage_rows_equal_clusters_x18"] = bool((expected["rows"] == expected["expected_rows_clusters_x18"]).all())
say("B. coverage denominators ok: " + str(res["coverage_rows_equal_clusters_x18"]))

# ---------------------------------------------------------------- C. outcome validity and readiness
child = child.merge(typed[["record_number", "HWHAZWHO", "HWWAZWHO", "HWWHZWHO"]], on="record_number", how="left")
OUTC = {"HAZ": "HWHAZWHO", "WAZ": "HWWAZWHO", "WHZ": "HWWHZWHO"}
FLAGS = {9995.0, 9996.0, 9997.0, 9998.0}
rows = []
exclusion_rows = []
for oc, col in OUTC.items():
    code = child[col].values
    universe = ~np.isnan(code) & (code != 9999.0)
    valid_out = universe & ~np.isin(code, list(FLAGS))
    child[f"{oc}_valid_outcome"] = valid_out
    child[f"{oc}_in_universe"] = universe
for product in ["W_IMP", "S_IMP"]:
    for window in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        for method in ["complete_primary", "partial_diagnostic_primary", "containing_pixel", "rural_10km"]:
            sc = f"{product}_{window}_" + {"complete_primary": "complete_status",
                                           "partial_diagnostic_primary": "partial_diag_status",
                                           "containing_pixel": "containing_status",
                                           "rural_10km": "rural10_status"}[method]
            for (cand, smp), sub in child.groupby(["candidate", "sample"]):
                s = sub[sc].values
                date_ok = sub["date_ok"].values.astype(bool)
                timing_ok = np.isin(s, ["spatial_missing_year", "spatial_partial_year", "eligible_complete",
                                        "eligible_diagnostic"])
                if method == "rural_10km":
                    rural = sub["URBAN"].values == 2
                else:
                    rural = np.ones(len(sub), bool)
                n = len(sub)
                for oc, col in OUTC.items():
                    vo = sub[f"{oc}_valid_outcome"].values
                    spatial_final = (s == "eligible_diagnostic") if method == "partial_diagnostic_primary" else (s == "eligible_complete")
                    final = vo & spatial_final & rural
                    rows.append({"product": product, "window": window, "method": method, "candidate": cand,
                                 "sample": smp, "outcome": oc, "records": int(n), "applicable_records": int(rural.sum()),
                                 "valid_outcome": int((vo & rural).sum()), "valid_dates": int((date_ok & rural).sum()),
                                 "complete_timing": int((timing_ok & rural).sum()),
                                 "complete_spatial": int(((s == "eligible_complete") & rural).sum()),
                                 "final_intersection": int(final.sum())})
                    # mutually exclusive, ordered exclusion categories
                    cats = [s == "unmatched_cluster", ~rural, ~vo, ~date_ok, s == "birth_after_interview",
                            s == "window_outside_2000_2017", s == "postnatal_incomplete",
                            s == "spatial_missing_year", s == "spatial_partial_year"]
                    labs = ["unmatched_cluster", "not_applicable_method", "outcome_invalid_or_absent", "dates_invalid",
                            "birth_after_interview", "window_outside_2000_2017", "postnatal_incomplete",
                            "spatial_missing_year", "spatial_partial_year"]
                    # default = passes every earlier exclusion (for the diagnostic method this includes
                    # partial buffers, because s == eligible_diagnostic is not excluded above)
                    cat = np.select(cats, labs, default="final_intersection")
                    for lab, c in pd.Series(cat).value_counts().items():
                        exclusion_rows.append({"product": product, "window": window, "method": method,
                                               "candidate": cand, "sample": smp, "outcome": oc,
                                               "category": lab, "records": int(c)})
rd = pd.DataFrame(rows)
rd.to_csv(os.path.join(OUT, "readiness_by_sample_outcome_window_method.csv"), index=False)
exd = pd.DataFrame(exclusion_rows)
exd.to_csv(os.path.join(OUT, "exclusion_categories_mutually_exclusive.csv"), index=False)
# reconciliation: categories sum to applicable records
ck = exd.groupby(["product", "window", "method", "candidate", "sample", "outcome"])["records"].sum().reset_index()
ck = ck.merge(rd[["product", "window", "method", "candidate", "sample", "outcome", "records", "final_intersection"]],
              on=["product", "window", "method", "candidate", "sample", "outcome"], suffixes=("_cat", ""))
res["exclusion_categories_sum_to_records"] = bool((ck["records_cat"] == ck["records"]).all())
fin = exd[exd["category"] == "final_intersection"].groupby(["product", "window", "method", "candidate", "sample", "outcome"])["records"].sum().reset_index()
fin = fin.merge(rd[["product", "window", "method", "candidate", "sample", "outcome", "final_intersection"]],
                on=["product", "window", "method", "candidate", "sample", "outcome"], how="outer").fillna(0)
res["final_category_equals_final_intersection"] = bool((fin["records"] == fin["final_intersection"]).all())
res["exclusion_categories_sum_to_applicable"] = res["exclusion_categories_sum_to_records"]
res["readiness_rows"] = int(len(rd))
say("C. readiness written; exclusions reconcile: " + str(res["exclusion_categories_sum_to_applicable"]))

# ---------------------------------------------------------------- D. exposure descriptives (eligible complete)
desc = []
for product in ["W_IMP", "S_IMP"]:
    for window in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        for method, col, stc in [("complete_primary", f"{product}_{window}_complete_exposure", f"{product}_{window}_complete_status"),
                                 ("containing_pixel", f"{product}_{window}_containing_exposure", f"{product}_{window}_containing_status"),
                                 ("rural_10km", f"{product}_{window}_rural10_exposure", f"{product}_{window}_rural10_status"),
                                 ("partial_diagnostic_primary", f"{product}_{window}_partial_diag_exposure", f"{product}_{window}_partial_diag_status")]:
            for (cand, smp), sub in child.groupby(["candidate", "sample"]):
                x = sub[col].dropna().values
                if len(x) == 0:
                    continue
                desc.append({"product": product, "window": window, "method": method, "candidate": cand,
                             "sample": smp, "n": int(len(x)), "mean": float(np.mean(x)), "sd": float(np.std(x, ddof=1)) if len(x) > 1 else np.nan,
                             "p5": float(np.percentile(x, 5)), "p50": float(np.percentile(x, 50)),
                             "p95": float(np.percentile(x, 95)),
                             "post_interview_year_flagged": int(sub.loc[sub[col].notna(), f"{product}_{window}_post_interview_year_used"].sum())})
dd = pd.DataFrame(desc)
dd.to_csv(os.path.join(OUT, "exposure_descriptives_eligible_only.csv"), index=False)
say("D. descriptives rows=" + str(len(dd)))

# ---------------------------------------------------------------- E. Ethiopia candidate agreement
et = child[child["sample"] == "ET2016"]
piv = et.pivot_table(index="record_number", columns="candidate", values="date_ok", aggfunc="first")
agree_rows = []
for product in ["W_IMP", "S_IMP"]:
    for window in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        col_s = {c: f"{product}_{window}_complete_status" for c in et["candidate"].unique()}
        pv = et.pivot_table(index="record_number", columns="candidate", values=f"{product}_{window}_complete_status", aggfunc="first")
        pe = et.pivot_table(index="record_number", columns="candidate", values=f"{product}_{window}_complete_exposure", aggfunc="first")
        cands = ["ET_C1_triple_provisional", "ET_C2_century_1907_provisional", "ET_C3_century_2015_provisional"]
        elig = pv[cands].eq("eligible_complete")
        n_all = int(elig.all(axis=1).sum())
        n_none = int((~elig).all(axis=1).sum())
        n_some = int(len(elig) - n_all - n_none)
        both = elig["ET_C2_century_1907_provisional"] & elig["ET_C3_century_2015_provisional"]
        diff_exp = np.nanmax(np.abs(pe.loc[both, "ET_C2_century_1907_provisional"].values -
                                    pe.loc[both, "ET_C3_century_2015_provisional"].values)) if both.any() else np.nan
        agree_rows.append({"product": product, "window": window, "records": int(len(pv)),
                           "eligible_under_all_three_candidates": n_all,
                           "eligible_under_none": n_none,
                           "eligible_under_some_candidates_dependent": n_some,
                           "C1_dates_unavailable": int(pv["ET_C1_triple_provisional"].eq("dates_missing").sum()),
                           "max_abs_exposure_diff_C2_vs_C3_where_both_eligible": float(diff_exp) if not np.isnan(diff_exp) else None})
agree = pd.DataFrame(agree_rows)
agree.to_csv(os.path.join(OUT, "ethiopia_candidate_agreement_PROVISIONAL.csv"), index=False)
say("E. Ethiopia agreement:\n" + agree.to_string(index=False))

# ---------------------------------------------------------------- F. exposure variation and collinearity (exposure only)
var_rows = []
for product in ["W_IMP", "S_IMP"]:
    for window in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        col = f"{product}_{window}_complete_exposure"
        for cand in ["GREGORIAN_ESTABLISHED", "ET_C2_century_1907_provisional", "ET_C3_century_2015_provisional"]:
            for smp in ["GH2014", "KE2014", "NG2018", "ET2016"]:
                if (cand == "GREGORIAN_ESTABLISHED") != (smp != "ET2016"):
                    continue
                sub = child[(child["candidate"] == cand) & (child["sample"] == smp)].copy()
                sub = sub[sub[col].notna()]
                if len(sub) < 10:
                    continue
                sub["birth_year"] = np.floor((sub["birth_cmc"] - 1) / 12) + 1900
                sub["e"] = sub[col]
                sub["age"] = sub["age_months_cal"]
                g = sub.groupby("IDHSPSU")["e"]
                sub["e_w"] = sub["e"] - g.transform("mean")
                multi = g.transform("size") >= 2
                within_sd = float(sub.loc[multi, "e_w"].std(ddof=1)) if multi.sum() > 2 else np.nan
                total_sd = float(sub["e"].std(ddof=1))
                # residual after cluster FE and birth-year FE (alternating projections, 25 passes)
                r = sub["e"].values.copy()
                cl = sub["IDHSPSU"].values
                by = sub["birth_year"].values
                for _ in range(25):
                    r = r - pd.Series(r).groupby(cl).transform("mean").values
                    r = r - pd.Series(r).groupby(by).transform("mean").values
                resid_sd = float(np.std(r, ddof=1))
                # collinearity: within-cluster design of birth-year dummies + age (months)
                dums = pd.get_dummies(sub["birth_year"].astype(int), drop_first=True).astype(float)
                X = pd.concat([dums, sub[["age"]].astype(float)], axis=1)
                Xw = X - X.groupby(cl).transform("mean")
                Xw_mat = Xw.values
                rank = int(np.linalg.matrix_rank(Xw_mat))
                s_ = np.linalg.svd(Xw_mat, compute_uv=False)
                cond = float(s_[0] / s_[-1]) if s_[-1] > 0 else np.inf
                corr_age_by = float(np.corrcoef(sub["age"], sub["birth_year"])[0, 1])
                var_rows.append({"product": product, "window": window, "candidate": cand, "sample": smp,
                                 "n": int(len(sub)), "clusters": int(sub["IDHSPSU"].nunique()),
                                 "clusters_with_2plus": int(sub.groupby("IDHSPSU").size().ge(2).sum()),
                                 "exposure_sd_total": total_sd, "within_cluster_sd": within_sd,
                                 "residual_sd_after_cluster_and_birthyear_FE": resid_sd,
                                 "design_columns_within": int(X.shape[1]), "design_rank_within": rank,
                                 "design_condition_number_within": cond,
                                 "corr_age_birthyear": corr_age_by})
var = pd.DataFrame(var_rows)
var.to_csv(os.path.join(OUT, "exposure_variation_and_collinearity_diagnostics.csv"), index=False)
say("F. variation rows=" + str(len(var)))

# ---------------------------------------------------------------- G. independent cross-check of stored exposures
# Month enumeration below is calendar-by-calendar (independent of the array arithmetic) and
# annual values come from the pandas table, not from the array lookup used in construction.
ann = mean[mean["method"] == "primary_area_buffer"].set_index(["IDHSPSU", "product", "year"])["value"]
checks = []
for product in ["W_IMP", "S_IMP"]:
    for window, L in [("birth_year", 12), ("prenatal_9m", 9), ("post_12m", 12), ("post_24m", 24)]:
        col = f"{product}_{window}_complete_exposure"
        pool = child[child[col].notna()]
        if pool.empty:
            continue
        pick = pool.sample(n=min(300, len(pool)), random_state=7)
        for r in pick.itertuples(index=False):
            b = int(r.birth_cmc)
            if window == "birth_year":
                by = (b - 1) // 12 + 1900
                y, m = by, 1
                L_ = 12
            elif window == "prenatal_9m":
                start = b - 9
                y, m = (start - 1) // 12 + 1900, (start - 1) % 12 + 1
                L_ = 9
            else:
                y, m = (b - 1) // 12 + 1900, (b - 1) % 12 + 1
                L_ = L
            wsum = {}
            for _ in range(L_):
                wsum[y] = wsum.get(y, 0) + 1
                m += 1
                if m > 12:
                    y, m = y + 1, 1
            vals = []
            for yy, cnt in wsum.items():
                vals.append((cnt / L_) * float(ann.loc[(r.IDHSPSU, product, yy)]))
            expected_val = sum(vals)
            stored = float(r._asdict()[col])
            checks.append({"product": product, "window": window,
                           "abs_diff": abs(expected_val - stored),
                           "weights_sum_to_one": abs(sum(wsum.values()) / L_ - 1) < 1e-12})
chk = pd.DataFrame(checks)
chk.to_csv(os.path.join(OUT, "independent_cross_check_sample.csv"), index=False)
res["cross_check_rows"] = int(len(chk))
res["cross_check_max_abs_diff"] = float(chk["abs_diff"].max()) if len(chk) else None
res["cross_check_weights_sum_to_one_all"] = bool(chk["weights_sum_to_one"].all()) if len(chk) else None
say(f"G. cross-check rows={len(chk)} max abs diff={res['cross_check_max_abs_diff']}")

# ---------------------------------------------------------------- hashes and manifest
hash_after = {"typed": sha(TYPED), "extract": sha(EXTRACT)}
res["sources_unchanged"] = bool(hash_before == hash_after)
with open(os.path.join(OUT, "validation_summary.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, default=str)
with open(os.path.join(OUT, "validation_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
say(f"sources unchanged: {res['sources_unchanged']}")
