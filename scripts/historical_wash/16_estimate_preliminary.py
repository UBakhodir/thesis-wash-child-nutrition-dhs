"""
16_estimate_preliminary.py
==========================
PRELIMINARY historical WASH estimates (working configuration). Labelled PRELIMINARY throughout;
measurement-weight documentation and final design review are pending. Not thesis results.

Working configuration (author choices for preliminary analysis):
  - Working main window: first 12 postnatal months (post_12m); complete spatial coverage.
  - Established-date samples: Ghana 2014, Kenya 2014, Nigeria 2018. Ethiopia only as separately
    labelled provisional sensitivity (candidates C1/C2/C3).
  - Model: y = a_cluster + b*E + survey-qualified country-by-birth-year + age + child sex
    + maternal age, education, marital status. Wealth excluded from main, included in sensitivity.
  - Age: reported completed months where delivered, otherwise calendar months.
  - Weights: PERWEIGHT with equal country totals within each model's estimation sample.
  - Inference: PSU-clustered CRV1 (cluster = IDHSPSU, sample-qualified). Fixed-effect terms are
    absorbed by the within transformation and are not counted in the small-sample correction.

Estimator: weighted within-cluster least squares (exact equivalent of WLS with cluster dummies).
Singleton clusters are dropped (they carry no within information) and counted.
CRV1 small-sample correction: G/(G-1) * (N-1)/(N-K), K = non-fixed-effect regressors kept.
CI: t distribution with G-1 degrees of freedom (cluster-robust convention).

Inputs (read-only): analysis candidates run 20261006T184744Z; child exposure construction run
20261006T183803Z (containing-pixel, rural-10 km columns).
Outputs: new restricted run folder (estimates and model datasets) plus aggregate tables.
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
from scipy import stats

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
AN = os.path.join(MASTER, "data", "processed", "analysis_samples", "run_20261006T184744Z", "analysis_candidates_RESTRICTED.parquet")
CON = os.path.join(MASTER, "data", "processed", "child_exposure", "run_20261006T183803Z", "child_exposure_candidates_RESTRICTED.parquet")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "estimation")
PRELIM = "PRELIMINARY - measurement-weight documentation and final design review pending."
OUTCOMES = {"HAZ": "HAZ_z", "WAZ": "WAZ_z", "WHZ": "WHZ_z"}
OUT_VALID = {"HAZ": "HAZ_valid", "WAZ": "WAZ_valid", "WHZ": "WHZ_valid"}
SAMPLE_LABEL = {28806: "GH2014", 40406: "KE2014", 56606: "NG2018", 23104: "ET2016"}
EST = [28806, 40406, 56606]
log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line, flush=True)
    log_lines.append(line)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def load():
    A = pd.read_parquet(AN)
    C = pd.read_parquet(CON)
    cols = ["record_number", "candidate"]
    for p in ["W_IMP", "S_IMP"]:
        for w in ["birth_year", "prenatal_9m", "post_12m", "post_24m"]:
            cols += [f"{p}_{w}_containing_exposure", f"{p}_{w}_containing_status",
                     f"{p}_{w}_rural10_exposure", f"{p}_{w}_rural10_status"]
    M = A.merge(C[cols], on=["record_number", "candidate"], how="left", validate="one_to_one")
    assert len(M) == len(A), "row multiplication in merge"
    return M


def window_L(window):
    return {"birth_year": 12, "prenatal_9m": 9, "post_12m": 12, "post_24m": 24}[window]


def frame(M, product, window, method, candidate, samples, age_mode="reported_first", stricter=False,
          wealth=False, overlap_exclude=None):
    """Estimation frame before the outcome is chosen. method: primary | containing | rural10_urban_primary."""
    sub = M[(M["candidate"] == candidate) & (M["SAMPLE"].isin(samples))].copy()
    p, w = product, window
    if method == "primary":
        E = sub[f"{p}_{w}_complete_exposure"].values
        ok = (sub[f"{p}_{w}_complete_status"] == "eligible_complete").values
    elif method == "containing":
        E = sub[f"{p}_{w}_containing_exposure"].values
        ok = (sub[f"{p}_{w}_containing_status"] == "eligible_complete").values
    elif method == "rural10_urban_primary":
        urban = (sub["URBAN"] == 1).values
        Ep = sub[f"{p}_{w}_complete_exposure"].values
        Er = sub[f"{p}_{w}_rural10_exposure"].values
        E = np.where(urban, Ep, Er)
        okp = (sub[f"{p}_{w}_complete_status"] == "eligible_complete").values
        okr = (sub[f"{p}_{w}_rural10_status"] == "eligible_complete").values
        ok = np.where(urban, okp, okr)
    else:
        raise ValueError(method)
    sub["E"] = E
    sub["ok"] = ok
    if stricter and window in ("post_12m", "post_24m"):
        L = window_L(window)
        sub = sub[sub["t"].astype(float) >= sub["b"].astype(float) + L + 1]
    if age_mode == "reported_first":
        age = np.where(sub["age_reported"].notna(), sub["age_reported"], sub["age_cal_candidate"])
    else:
        age = sub["age_cal_candidate"].values
    sub["age_m"] = age.astype(float)
    base = (sub["ok"].astype(bool) & sub["under5"].astype(bool) & sub["E"].notna() & sub["age_m"].notna()
            & sub["AGE"].notna() & sub["EDUCLVL"].notna() & sub["MARSTAT"].notna() & sub["KIDSEX"].notna()
            & sub["IDHSPSU"].notna() & sub["date_ok"].astype(bool) & sub["PERWEIGHT"].notna())
    if wealth:
        base &= sub["WEALTHQ"].notna()
    sub = sub[base.values].copy()
    sub["overlap_excluded"] = False
    return sub


def design_matrix(df, wealth):
    cols, names = [], []
    cols.append(df["E"].values.astype(float)); names.append("E")
    cols.append(df["age_m"].values.astype(float)); names.append("age_months")
    cols.append((df["KIDSEX"] == 2).values.astype(float)); names.append("child_female")
    cols.append(df["AGE"].values.astype(float)); names.append("mother_age")
    for lev in sorted(df["EDUCLVL"].dropna().unique())[1:]:
        cols.append((df["EDUCLVL"] == lev).values.astype(float)); names.append(f"educ_{int(lev)}")
    for lev in sorted(df["MARSTAT"].dropna().unique())[1:]:
        cols.append((df["MARSTAT"] == lev).values.astype(float)); names.append(f"marstat_{int(lev)}")
    if wealth:
        for lev in sorted(df["WEALTHQ"].dropna().unique())[1:]:
            cols.append((df["WEALTHQ"] == lev).values.astype(float)); names.append(f"wealth_{int(lev)}")
    for smp in sorted(df["SAMPLE"].unique()):
        s = df[df["SAMPLE"] == smp]
        yrs = sorted(s["b_year"].dropna().unique())
        for y in yrs[1:]:
            cols.append(((df["SAMPLE"] == smp) & (df["b_year"] == y)).values.astype(float))
            names.append(f"by_{int(smp)}_{int(y)}")
    return np.column_stack(cols), names


def equal_country_weights(df, weighted):
    """Equal country totals within this estimation sample; mean 1 overall. Unweighted -> 1."""
    if not weighted:
        return np.ones(len(df))
    w0 = df["PERWEIGHT"].values.astype(float)
    K = df["SAMPLE"].nunique()
    n = len(df)
    tot = df.assign(_w=w0).groupby("SAMPLE")["_w"].transform("sum").values
    return w0 * (n / K) / tot


def fit(df, ycol, weighted=True, wealth=False):
    """Weighted within-cluster least squares with CRV1 inference. Returns a dict."""
    out = {"N_input": int(len(df))}
    df = df[df[ycol].notna()].copy()
    out["N_outcome_valid"] = int(len(df))
    n_before = len(df)
    n_clusters_before = df["IDHSPSU"].nunique()
    sizes = df.groupby("IDHSPSU")["IDHSPSU"].transform("size").values
    df = df[sizes >= 2].copy()
    out["singleton_clusters_dropped"] = int(n_clusters_before - df["IDHSPSU"].nunique())
    out["singleton_obs_dropped"] = int(n_before - len(df))
    if len(df) < 5 or df["E"].std() == 0:
        out.update({"status": "non_estimable_no_within_variation", "N": int(len(df))})
        return out
    w = equal_country_weights(df, weighted)
    df = df.assign(_w=w)
    X, names = design_matrix(df, wealth)
    y = df[ycol].values.astype(float)
    g = df["IDHSPSU"].values
    codes, uniq = pd.factorize(g)
    W = w
    # weighted within-cluster demeaning
    sw = np.bincount(codes, weights=W)
    def wdemean(V):
        out_ = np.empty_like(V)
        for j in range(V.shape[1]):
            num = np.bincount(codes, weights=W * V[:, j])
            out_[:, j] = V[:, j] - (num / sw)[codes]
        return out_
    Xt = wdemean(X)
    yt = wdemean(y.reshape(-1, 1))[:, 0]
    # drop absorbed (zero within variation) columns
    scale = np.sqrt(np.sum(W[:, None] * Xt ** 2, axis=0))
    keep = scale > 1e-10
    absorbed = [n_ for n_, k_ in zip(names, keep) if not k_]
    Xt, names_k = Xt[:, keep], [n_ for n_, k_ in zip(names, keep) if k_]

    # --- Exposure-safety safeguard (added 2026-10-10; see R05, independent audit
    # 2026-10-10). The absorbed-column filter above can drop E itself (e.g. when
    # E varies between clusters but is constant within every cluster: the raw-SD
    # check above does not catch this, since it only tests raw, not within-cluster,
    # variation). If E is absorbed, the previous code still read beta[0]/V[0,0]
    # positionally and silently reported the next retained column's coefficient as
    # if it were E's own. E's coefficient and variance are now retrieved by name,
    # not position, and the fit is refused outright if E does not survive. ---
    if "E" not in names_k:
        out.update({
            "status": "non_estimable_exposure_absorbed",
            "N": int(Xt.shape[0]), "G_clusters": int(len(uniq)),
            "columns_absorbed": absorbed,
            "note": "E was absorbed by the cluster fixed effect (zero within-cluster "
                    "variation after weighted demeaning); the exposure coefficient is "
                    "not estimable in this configuration.",
        })
        out["_df"] = df
        return out
    e_idx = names_k.index("E")

    sW = np.sqrt(W)
    A_ = Xt * sW[:, None]
    rank = int(np.linalg.matrix_rank(A_))
    K_retained = Xt.shape[1]

    # --- Rank-deficiency safeguard (added 2026-10-10; see R05). A pseudoinverse
    # always returns *some* coefficient vector even when the retained design is
    # not full column rank, silently mislabelling an unidentified, minimum-norm
    # solution as an ordinary estimate. Refuse rather than report one. ---
    if rank < K_retained:
        out.update({
            "status": "non_estimable_rank_deficient",
            "N": int(Xt.shape[0]), "G_clusters": int(len(uniq)), "K_regressors": int(K_retained),
            "rank": rank, "columns_absorbed": absorbed,
            "note": f"Retained design matrix has rank {rank} < {K_retained} retained columns "
                    "after absorption; the exposure coefficient is not uniquely identified.",
        })
        out["_df"] = df
        return out

    sv = np.linalg.svd(A_ / np.linalg.norm(A_, axis=0), compute_uv=False)
    cond = float(sv[0] / sv[-1]) if sv[-1] > 0 else float("inf")
    XtWX = Xt.T @ (Xt * W[:, None])
    B = np.linalg.pinv(XtWX)
    beta = B @ (Xt.T @ (W * yt))
    res = yt - Xt @ beta
    G = len(uniq)
    N, K = Xt.shape[0], Xt.shape[1]
    meat = np.zeros((K, K))
    for c_ in range(G):
        idx = codes == c_
        s = Xt[idx].T @ (W[idx] * res[idx])
        meat += np.outer(s, s)
    corr = (G / (G - 1)) * ((N - 1) / (N - K))
    V = corr * B @ meat @ B
    b_e, se_e = beta[e_idx], float(np.sqrt(V[e_idx, e_idx]))
    tcrit = stats.t.ppf(0.975, G - 1)
    # residual exposure variation: E projected on the other regressors (weighted, within)
    if K > 1:
        other = [j for j in range(K) if j != e_idx]
        Z = Xt[:, other] * sW[:, None]
        bz, *_ = np.linalg.lstsq(Z, Xt[:, e_idx] * sW, rcond=None)
        eres = Xt[:, e_idx] - Xt[:, other] @ bz
    else:
        eres = Xt[:, e_idx]
    out.update({
        "status": "estimated", "N": int(N), "G_clusters": int(G), "K_regressors": int(K),
        "rank": rank, "columns_absorbed": absorbed, "condition_number_scaled": cond,
        "beta_per_point": float(b_e), "se_CRV1": se_e,
        "ci95_low_per_point": float(b_e - tcrit * se_e), "ci95_high_per_point": float(b_e + tcrit * se_e),
        "p_value": float(2 * stats.t.sf(abs(b_e / se_e), G - 1)) if se_e > 0 else np.nan,
        "beta_per_10": float(10 * b_e), "se_per_10": float(10 * se_e),
        "ci95_low_per_10": float(10 * (b_e - tcrit * se_e)), "ci95_high_per_10": float(10 * (b_e + tcrit * se_e)),
        "E_within_sd": float(np.sqrt(np.sum(W * Xt[:, e_idx] ** 2) / np.sum(W))),
        "E_residual_sd_after_controls": float(np.std(eres, ddof=1)),
        "clusters_with_exposure_variation": int(df.assign(_E=df["E"]).groupby("IDHSPSU")["_E"].nunique().gt(1).sum()),
        "weights_country_total": {str(SAMPLE_LABEL[int(k)]): float(v) for k, v in
                                  pd.Series(W).groupby(df["SAMPLE"].values).sum().items()},
        "weight_mean": float(np.mean(W)),
        "E_mean": float(df["E"].mean()), "E_sd_raw": float(df["E"].std()),
    })
    out["_df"] = df
    return out


def run_model(M, spec, rows, frames):
    product, outcome, window, method = spec["product"], spec["outcome"], spec["window"], spec["method"]
    fr = frame(M, product, window, method, spec["candidate"], spec["samples"], spec.get("age_mode", "reported_first"),
               spec.get("stricter", False), spec.get("wealth", False))
    res = fit(fr, OUTCOMES[outcome], weighted=spec.get("weighted", True), wealth=spec.get("wealth", False))
    df_model = res.pop("_df", None)
    if df_model is not None:
        frames[spec["id"]] = df_model.assign(model_id=spec["id"])
    row = {k: v for k, v in spec.items() if k not in ("samples", "candidate_all")}
    row["samples"] = "+".join(SAMPLE_LABEL[s] for s in spec["samples"])
    row.update({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()})
    row["label"] = PRELIM
    rows.append(row)
    return res


def model_specs():
    specs = []
    def add(**kw):
        kw["id"] = f"m{len(specs)+1:04d}"
        specs.append(kw)
    cand = "GREGORIAN_ESTABLISHED"
    for product in ["W_IMP", "S_IMP"]:
        for outcome in ["HAZ", "WAZ", "WHZ"]:
            # primary: country-specific and pooled established, weighted
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="primary", product=product, outcome=outcome, window="post_12m", method="primary",
                    candidate=cand, samples=samples, weighted=True, wealth=False, stricter=False,
                    age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # unweighted comparison on the same samples
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="unweighted_comparison", product=product, outcome=outcome, window="post_12m",
                    method="primary", candidate=cand, samples=samples, weighted=False, wealth=False,
                    stricter=False, age_mode="reported_first",
                    sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # window sensitivity (each window's own eligible sample)
            for w in ["birth_year", "prenatal_9m", "post_24m"]:
                for smp in EST + ["POOLED"]:
                    samples = EST if smp == "POOLED" else [smp]
                    add(family="sens_window", product=product, outcome=outcome, window=w, method="primary",
                        candidate=cand, samples=samples, weighted=True, wealth=False, stricter=False,
                        age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # wealth adjustment
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="sens_wealth", product=product, outcome=outcome, window="post_12m", method="primary",
                    candidate=cand, samples=samples, weighted=True, wealth=True, stricter=False,
                    age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # containing pixel
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="sens_containing_pixel", product=product, outcome=outcome, window="post_12m",
                    method="containing", candidate=cand, samples=samples, weighted=True, wealth=False,
                    stricter=False, age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # rural 10 km with urban assignment unchanged
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="sens_rural10km", product=product, outcome=outcome, window="post_12m",
                    method="rural10_urban_primary", candidate=cand, samples=samples, weighted=True, wealth=False,
                    stricter=False, age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # one-month-stricter completion (postnatal windows)
            for w in ["post_12m", "post_24m"]:
                for smp in EST + ["POOLED"]:
                    samples = EST if smp == "POOLED" else [smp]
                    add(family="sens_stricter_completion", product=product, outcome=outcome, window=w,
                        method="primary", candidate=cand, samples=samples, weighted=True, wealth=False,
                        stricter=True, age_mode="reported_first", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # calendar-month age throughout
            for smp in EST + ["POOLED"]:
                samples = EST if smp == "POOLED" else [smp]
                add(family="sens_calendar_age", product=product, outcome=outcome, window="post_12m",
                    method="primary", candidate=cand, samples=samples, weighted=True, wealth=False,
                    stricter=False, age_mode="calendar", sample_group=("POOLED_ESTABLISHED" if smp == "POOLED" else SAMPLE_LABEL[smp]))
            # Ethiopia provisional candidates (separately labelled)
            for c_ in ["ET_C2_century_1907_provisional", "ET_C3_century_2015_provisional", "ET_C1_triple_provisional"]:
                add(family="sens_ethiopia_PROVISIONAL", product=product, outcome=outcome, window="post_12m",
                    method="primary", candidate=c_, samples=[23104], weighted=True, wealth=False, stricter=False,
                    age_mode="reported_first", sample_group="ET2016_PROVISIONAL_" + c_.split("_")[1])
    return specs


def overlap_specs():
    """IHME/DHS input overlap: Ghana both products; Kenya water only."""
    specs = []
    def add(**kw):
        kw["id"] = f"o{len(specs)+1:03d}"
        specs.append(kw)
    cand = "GREGORIAN_ESTABLISHED"
    for outcome in ["HAZ", "WAZ", "WHZ"]:
        # sanitation: exclude Ghana (its overlap applies to both products); Kenya retained
        add(family="sens_overlap_excl_GH_sanitation", product="S_IMP", outcome=outcome, window="post_12m",
            method="primary", candidate=cand, samples=[40406, 56606], weighted=True, wealth=False, stricter=False,
            age_mode="reported_first", sample_group="POOLED_KE_NG")
        # water: exclude Ghana and Kenya (Kenya overlaps water); Nigeria only (country-specific)
        add(family="sens_overlap_excl_GH_KE_water", product="W_IMP", outcome=outcome, window="post_12m",
            method="primary", candidate=cand, samples=[56606], weighted=True, wealth=False, stricter=False,
            age_mode="reported_first", sample_group="NG2018_only_after_overlap_exclusion")
        # water: exclude Ghana only (pooled Kenya + Nigeria)
        add(family="sens_overlap_excl_GH_water", product="W_IMP", outcome=outcome, window="post_12m",
            method="primary", candidate=cand, samples=[40406, 56606], weighted=True, wealth=False, stricter=False,
            age_mode="reported_first", sample_group="POOLED_KE_NG")
    return specs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="print the planned model count and exit")
    args = ap.parse_args()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    specs = model_specs() + overlap_specs()
    log(f"planned models={len(specs)}")
    if args.dry:
        print(json.dumps({"planned": len(specs)}))
        return
    out_dir = os.path.join(OUT_ROOT, f"run_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    log(f"python={platform.python_version()} pandas={pd.__version__} numpy={np.__version__} pyarrow={pa.__version__}")
    log(f"script_sha256={sha(__file__)}")
    before = {"analysis": sha(AN), "construction": sha(CON)}
    M = load()
    log(f"merged candidate rows={len(M)}")
    rows, frames = [], {}
    for spec in specs:
        res = run_model(M, spec, rows, frames)
        log(f"{spec['id']} {spec['family']} {spec['product']} {spec['outcome']} {spec.get('sample_group')} "
            f"w={spec.get('window')} m={spec.get('method')}: status={res.get('status')} "
            f"N={res.get('N')} G={res.get('G_clusters')} beta10={res.get('beta_per_10', float('nan')):.4f}"
            if res.get("status") == "estimated" else f"{spec['id']} {spec['family']}: {res.get('status')}")
    results = pd.DataFrame(rows)
    results.to_csv(os.path.join(out_dir, "model_results_RESTRICTED_coefficients.csv"), index=False)
    # restricted model datasets for the primary configuration only
    prim_frames = [f_ for k, f_ in frames.items() if k in set(results.loc[results["family"] == "primary", "id"])]
    if prim_frames:
        pd.concat(prim_frames).to_parquet(os.path.join(out_dir, "primary_model_datasets_RESTRICTED.parquet"), index=False)
    after = {"analysis": sha(AN), "construction": sha(CON)}
    manifest = {"label": PRELIM, "script": "scripts/historical_wash/16_estimate_preliminary.py",
                "script_sha256": sha(__file__), "interpreter": sys.executable, "python": platform.python_version(),
                "packages": {"numpy": np.__version__, "pandas": pd.__version__, "pyarrow": pa.__version__},
                "inputs_before": before, "inputs_after": after, "inputs_unchanged": before == after,
                "models_planned": len(specs), "models_estimated": int((results["status"] == "estimated").sum()),
                "models_non_estimable": int((results["status"] != "estimated").sum())}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    with open(os.path.join(out_dir, "execution_log.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")
    log(f"done: {out_dir}")


if __name__ == "__main__":
    main()
