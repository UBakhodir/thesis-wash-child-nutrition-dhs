"""
17_validate_estimates.py
========================
Independent validation of representative preliminary estimates (run 16). The validation uses a
different algebra and a separately written data assembly:
  - Data: rebuilt directly from the analysis-candidate table with its own filters.
  - Estimator: statsmodels WLS with explicit cluster dummies (fixed effects as columns), not the
    within transformation used in script 16.
  - Standard errors: CRV1 sandwich computed by hand from the dummy-model scores, with the
    small-sample correction using only the non-fixed-effect regressors (same convention).
Compares coefficients, standard errors, sample sizes, cluster counts and country weight totals.

Output: a validation table (aggregate) in a new folder, labelled PRELIMINARY. Runs with the
repository virtual environment (statsmodels available).
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
AN = os.path.join(MASTER, "data", "processed", "analysis_samples", "run_20261006T184744Z", "analysis_candidates_RESTRICTED.parquet")
RES = os.path.join(MASTER, "data", "processed", "estimation", "run_20261006T185646Z", "model_results_RESTRICTED_coefficients.csv")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "estimation")
PRELIM = "PRELIMINARY - measurement-weight documentation and final design review pending."
SL = {28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
log = []


def say(m):
    print(f"{datetime.now(timezone.utc).isoformat()} {m}", flush=True)
    log.append(m)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def rebuild(A, samples, product, outcome, weighted):
    """Independent frame: own filters (not the functions in script 16)."""
    d = A[(A["candidate"] == "GREGORIAN_ESTABLISHED") & (A["SAMPLE"].isin(samples))].copy()
    E = d[f"{product}_post_12m_complete_exposure"]
    ok = d[f"{product}_post_12m_complete_status"] == "eligible_complete"
    age = d["age_reported"].where(d["age_reported"].notna(), d["age_cal_candidate"])
    keep = (ok & E.notna() & d["under5"].astype(bool) & d[f"{outcome}_z"].notna() & age.notna()
            & d["AGE"].notna() & d["EDUCLVL"].notna() & d["MARSTAT"].notna() & d["KIDSEX"].notna()
            & d["date_ok"].astype(bool))
    d = d[keep].copy()
    d["E"] = E[keep]
    d["age_m"] = age[keep].astype(float)
    d["y"] = d[f"{outcome}_z"].astype(float)
    sizes = d.groupby("IDHSPSU")["IDHSPSU"].transform("size")
    d = d[sizes >= 2].copy()
    if weighted:
        K = d["SAMPLE"].nunique()
        tot = d.groupby("SAMPLE")["PERWEIGHT"].transform("sum")
        d["w"] = d["PERWEIGHT"] * (len(d) / K) / tot
    else:
        d["w"] = 1.0
    return d


def design(d):
    X = pd.DataFrame(index=d.index)
    X["E"] = d["E"]
    X["age_months"] = d["age_m"]
    X["child_female"] = (d["KIDSEX"] == 2).astype(float)
    X["mother_age"] = d["AGE"].astype(float)
    for lev in sorted(d["EDUCLVL"].unique())[1:]:
        X[f"educ_{int(lev)}"] = (d["EDUCLVL"] == lev).astype(float)
    for lev in sorted(d["MARSTAT"].unique())[1:]:
        X[f"marstat_{int(lev)}"] = (d["MARSTAT"] == lev).astype(float)
    for smp in sorted(d["SAMPLE"].unique()):
        yrs = sorted(d.loc[d["SAMPLE"] == smp, "b_year"].unique())
        for y in yrs[1:]:
            X[f"by_{int(smp)}_{int(y)}"] = ((d["SAMPLE"] == smp) & (d["b_year"] == y)).astype(float)
    return X


def check(samples, product, outcome, weighted, label):
    A = pd.read_parquet(AN, columns=["record_number", "candidate", "SAMPLE", "IDHSPSU", "under5", "date_ok",
                                     "AGE", "EDUCLVL", "MARSTAT", "KIDSEX", "age_reported", "age_cal_candidate",
                                     "b_year", "PERWEIGHT", f"{outcome}_z", f"{product}_post_12m_complete_exposure",
                                     f"{product}_post_12m_complete_status"])
    d = rebuild(A, samples, product, outcome, weighted)
    X = design(d)
    Xf = X.copy()
    # cluster dummies (fixed effects) appended; drop one cluster for identification is not needed
    # because the regressor set has no intercept; include an intercept for the dummy model
    dummies = pd.get_dummies(d["IDHSPSU"].astype(int), prefix="cl", drop_first=False).astype(float)
    Xfull = pd.concat([Xf, dummies], axis=1)
    mod = sm.WLS(d["y"].values, Xfull.values, weights=d["w"].values).fit()
    beta_E = mod.params[0]
    u = mod.resid
    W = d["w"].values
    cl = pd.factorize(d["IDHSPSU"])[0]
    G = int(cl.max() + 1)
    N = len(d)
    Kfull = Xfull.shape[1]
    Knon = Xf.shape[1]
    B = np.linalg.pinv(Xfull.values.T @ (Xfull.values * W[:, None]))
    meat = np.zeros((Kfull, Kfull))
    Xw = Xfull.values * W[:, None]
    for g in range(G):
        idx = cl == g
        s = Xw[idx].T @ u[idx]
        meat += np.outer(s, s)
    corr = (G / (G - 1)) * ((N - 1) / (N - Knon))
    V = corr * B @ meat @ B
    se_E = float(np.sqrt(V[0, 0]))
    tc = stats.t.ppf(0.975, G - 1)
    tot = d.assign(_w=W).groupby("SAMPLE")["_w"].sum().to_dict()
    row = {"label": label, "samples": "+".join(SL[s] for s in samples), "product": product, "outcome": outcome,
           "weighted": weighted, "N_rebuilt": N, "G_rebuilt": G,
           "beta_per_point_independent": float(beta_E), "se_CRV1_independent": se_E,
           "country_weight_totals": json.dumps({SL[int(k)]: round(float(v), 6) for k, v in tot.items()})}
    return row


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(OUT_ROOT, f"validation_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    before = {"analysis": sha(AN), "results": sha(RES)}
    res = pd.read_csv(RES)
    targets = [
        ([28806], "W_IMP", "HAZ", True, "GH2014 water HAZ weighted"),
        ([28806], "S_IMP", "WAZ", True, "GH2014 sanitation WAZ weighted"),
        ([56606], "S_IMP", "HAZ", True, "NG2018 sanitation HAZ weighted"),
        ([28806], "W_IMP", "HAZ", False, "GH2014 water HAZ unweighted"),
    ]
    rows = []
    for samples, product, outcome, weighted, label in targets:
        row = check(samples, product, outcome, weighted, label)
        mrow = res[(res["family"] == ("primary" if weighted else "unweighted_comparison"))
                   & (res["product"] == product) & (res["outcome"] == outcome)
                   & (res["samples"] == "+".join(SL[s] for s in samples))]
        if len(mrow):
            m = mrow.iloc[0]
            row.update({"beta_per_point_script16": float(m["beta_per_point"]), "se_CRV1_script16": float(m["se_CRV1"]),
                        "N_script16": int(m["N"]), "G_script16": int(m["G_clusters"])})
            row["beta_abs_diff"] = abs(row["beta_per_point_independent"] - row["beta_per_point_script16"])
            row["se_rel_diff"] = abs(row["se_CRV1_independent"] / row["se_CRV1_script16"] - 1)
            row["N_match"] = row["N_rebuilt"] == row["N_script16"]
            row["G_match"] = row["G_rebuilt"] == row["G_script16"]
        rows.append(row)
        say(f"{label}: beta indep={row['beta_per_point_independent']:.6f} "
            f"script16={row.get('beta_per_point_script16', float('nan')):.6f} "
            f"se indep={row['se_CRV1_independent']:.6f} script16={row.get('se_CRV1_script16', float('nan')):.6f} "
            f"N={row['N_rebuilt']} G={row['G_rebuilt']} match={row.get('N_match')}/{row.get('G_match')}")
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(out_dir, "independent_validation_AGGREGATE.csv"), index=False)
    after = {"analysis": sha(AN), "results": sha(RES)}
    summary = {"label": PRELIM, "checks": len(rows),
               "max_beta_abs_diff": float(df["beta_abs_diff"].max()), "max_se_rel_diff": float(df["se_rel_diff"].max()),
               "all_N_match": bool(df["N_match"].all()), "all_G_match": bool(df["G_match"].all()),
               "inputs_unchanged": before == after,
               "passed": bool(df["beta_abs_diff"].max() < 1e-6 and df["se_rel_diff"].max() < 1e-6
                              and df["N_match"].all() and df["G_match"].all())}
    with open(os.path.join(out_dir, "validation_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    with open(os.path.join(out_dir, "validation_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    say(f"summary: {json.dumps(summary)}")


if __name__ == "__main__":
    main()
