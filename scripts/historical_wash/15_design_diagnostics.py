"""
15_design_diagnostics.py
========================
Design diagnostics for the proposed historical-WASH specification, computed on the
candidate analysis samples. No outcome model is estimated. Only exposure is projected on
the controls, to measure residual exposure variation and collinearity (identification
diagnostics, not effect estimates).

Within-cluster transformation absorbs the cluster fixed effects (IDHSPSU). Survey (country)
terms are absorbed by cluster fixed effects because clusters nest within surveys; they are
checked explicitly and reported as absorbed.

Usage: python 15_design_diagnostics.py <analysis_sample_run_folder>
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    sys.exit("usage: 15_design_diagnostics.py <analysis_sample_run_folder>")
RUN = sys.argv[1]
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join(RUN, f"design_diagnostics_AGGREGATE_{STAMP}")
os.makedirs(OUT, exist_ok=False)
log = []
SAMPLE_NAME = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}


def say(m):
    print(f"{datetime.now(timezone.utc).isoformat()} {m}", flush=True)
    log.append(m)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


src = os.path.join(RUN, "analysis_candidates_RESTRICTED.parquet")
src_hash = sha(src)
A = pd.read_parquet(src)
A["sample"] = A["SAMPLE"].map(SAMPLE_NAME)


def design(sub, exp_col, outcome_flag, add_interview_month=False):
    """Build the within-cluster design for one sample subset. Returns dict of diagnostics.
    add_interview_month: adds within-sample interview-CMC dummies (variant for collinearity check)."""
    d = sub.copy()
    d = d[d[exp_col].notna() & d[outcome_flag].astype(bool)]
    d = d[d["under5"].astype(bool)]
    if len(d) == 0:
        return None
    cl = d["IDHSPSU"].values
    # candidate-independent age: reported completed months where delivered, else calendar CMC difference
    age = np.where(d["age_reported"].notna(), d["age_reported"], d["age_cal_candidate"]).astype(float)
    d["age_m"] = age
    d["birth_year"] = d["b_year"].astype(int)
    cols = {}
    # birth-year dummies within sample (reference = earliest year in the sample)
    for y in sorted(d["birth_year"].unique())[1:]:
        cols[f"by_{int(y)}"] = (d["birth_year"] == y).astype(float).values
    cols["age_months"] = d["age_m"].values
    cols["child_female"] = (d["KIDSEX"] == 2).astype(float).values
    cols["mother_age"] = d["AGE"].astype(float).values
    for lev in sorted(d["EDUCLVL"].dropna().unique())[1:]:
        cols[f"educ_{int(lev)}"] = (d["EDUCLVL"] == lev).astype(float).values
    for lev in sorted(d["MARSTAT"].dropna().unique())[1:]:
        cols[f"marstat_{int(lev)}"] = (d["MARSTAT"] == lev).astype(float).values
    cols["urban_hh"] = (d["URBAN"] == 1).astype(float).values
    if add_interview_month:
        tm = d["t"].astype(float).values
        for v in sorted(np.unique(tm))[1:]:
            cols[f"int_cmc_{int(v)}"] = (tm == v).astype(float)
    X = pd.DataFrame(cols, index=d.index)
    e = d[exp_col].astype(float).values
    # within-cluster transform
    dfw = pd.DataFrame(np.column_stack([X.values, e]), index=d.index, columns=list(X.columns) + ["_e"])
    dfw["_cl"] = cl
    Wm = dfw.groupby("_cl").transform("mean")
    Z = dfw[list(X.columns) + ["_e"]].values - Wm.values
    Xw = Z[:, :-1]
    ew = Z[:, -1]
    # absorbed columns (zero within-variation)
    norms = np.linalg.norm(Xw, axis=0)
    absorbed = [c for c, n in zip(X.columns, norms) if n < 1e-10]
    keep = [i for i, n in enumerate(norms) if n >= 1e-10]
    Xk = Xw[:, keep]
    names = [X.columns[i] for i in keep]
    # scale columns for conditioning
    scale = np.linalg.norm(Xk, axis=0)
    Xs = Xk / scale
    rank = int(np.linalg.matrix_rank(Xs))
    sv = np.linalg.svd(Xs, compute_uv=False)
    cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
    # exact dependence: regress each column on the others (within-cluster)
    dep = []
    for j, nm in enumerate(names):
        others = np.delete(Xs, j, axis=1)
        if others.shape[1] == 0:
            continue
        beta, *_ = np.linalg.lstsq(others, Xs[:, j], rcond=None)
        r2 = 1 - np.sum((Xs[:, j] - others @ beta) ** 2) / np.sum(Xs[:, j] ** 2)
        if r2 > 0.999999:
            dep.append({"column": nm, "R2_on_others": float(r2)})
    # residual exposure variation after the controls
    beta_e, *_ = np.linalg.lstsq(Xs, ew, rcond=None)
    resid = ew - Xs @ beta_e
    sizes = pd.Series(cl).value_counts()
    n_cl = int(len(sizes))
    singletons = int((sizes == 1).sum())
    multi = sizes[sizes >= 2].index
    varying = d.assign(_e=e).groupby("IDHSPSU")["_e"].agg(lambda s: s.nunique() > 1)
    contributing = int(varying.reindex(multi).fillna(False).sum())
    nonvarying_multi = int(len(multi) - contributing)
    within_sd = float(np.std(ew[np.isin(cl, multi)], ddof=1)) if np.isin(cl, multi).sum() > 2 else np.nan
    return {"n": int(len(d)), "clusters": n_cl, "singleton_clusters": singletons,
            "clusters_2plus": int(len(multi)), "clusters_2plus_exposure_varies": contributing,
            "clusters_2plus_exposure_constant": nonvarying_multi,
            "columns_proposed": int(X.shape[1]), "absorbed_columns": absorbed,
            "rank_within": rank, "columns_used_within": int(len(names)),
            "condition_number_scaled": cond, "exact_dependence": dep,
            "exposure_within_sd": within_sd,
            "exposure_residual_sd_after_controls": float(np.std(resid, ddof=1)),
            "exposure_residual_share_of_within": float(np.var(resid, ddof=1) / np.var(ew, ddof=1)) if np.var(ew) > 0 else np.nan,
            "age_birthyear_corr": float(np.corrcoef(d["age_m"], d["birth_year"])[0, 1]) if len(d) > 2 else np.nan,
            "age_t_b_identity_check": float(np.max(np.abs((d["t"] - d["b"]) - d["age_cal_candidate"]))) if "t" in d else np.nan}


rows = []
PRIMARY_OUTCOME = {"HAZ": "HAZ_valid", "WAZ": "WAZ_valid", "WHZ": "WHZ_valid"}
for product in ["W_IMP", "S_IMP"]:
    for window in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
        exp_col = f"{product}_{window}_complete_exposure"
        if exp_col not in A.columns:
            continue
        for smp in ["GH2014", "KE2014", "NG2018", "ET2016"]:
            if smp == "ET2016":
                cands = ["ET_C2_century_1907_provisional", "ET_C3_century_2015_provisional"]
            else:
                cands = ["GREGORIAN_ESTABLISHED"]
            for cand in cands:
                sub = A[(A["sample"] == smp) & (A["candidate"] == cand)]
                for oc, flag in PRIMARY_OUTCOME.items():
                    r = design(sub, exp_col, flag)
                    if r is None:
                        continue
                    r.update({"product": product, "window": window, "sample": smp, "candidate": cand, "outcome": oc,
                              "variant": "proposed"})
                    rows.append(r)
                    if oc == "HAZ":
                        rv = design(sub, exp_col, flag, add_interview_month=True)
                        if rv is not None:
                            rv.update({"product": product, "window": window, "sample": smp, "candidate": cand,
                                       "outcome": oc, "variant": "plus_interview_CMC_dummies"})
                            rows.append(rv)
                            say(f"  variant+interview-CMC {smp} {cand} {product} {window}: rank={rv['rank_within']}/"
                                f"{rv['columns_used_within']} cond={rv['condition_number_scaled']:.1f} "
                                f"exact_dependence={len(rv['exact_dependence'])}")
                    say(f"{smp} {cand} {product} {window} {oc}: n={r['n']} rank={r['rank_within']}/{r['columns_used_within']} "
                        f"cond={r['condition_number_scaled']:.1f} clusters2+={r['clusters_2plus']} "
                        f"varying={r['clusters_2plus_exposure_varies']} resid_sd={r['exposure_residual_sd_after_controls']:.3f}")
res_df = pd.DataFrame([{k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()} for r in rows])
res_df.to_csv(os.path.join(OUT, "design_diagnostics_by_sample_window.csv"), index=False)
with open(os.path.join(OUT, "design_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump({"script": "scripts/historical_wash/15_design_diagnostics.py", "source": src,
               "source_sha256_before": src_hash, "source_sha256_after": sha(src),
               "source_unchanged": src_hash == sha(src), "rows": len(rows)}, f, indent=1)
say(f"source unchanged: {src_hash == sha(src)}")
