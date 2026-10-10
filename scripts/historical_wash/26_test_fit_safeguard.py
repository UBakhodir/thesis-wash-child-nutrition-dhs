"""
26_test_fit_safeguard.py
=========================
Targeted, synthetic-data-only regression tests for the R05 estimator
safeguard added to 16_estimate_preliminary.py's fit() on 2026-10-10
(see docs/provenance/independent_audit_resolution_v1_2026-10-10.md).

What this tests and why: an external independent audit found that fit()
could, under a specific configuration (the exposure E varying between
clusters but constant within every cluster), silently report another
retained variable's coefficient as if it were E's own, because the
absorbed-column filter could drop E itself and the code then read the
exposure coefficient/variance by fixed array position rather than by
name. A second defect allowed a rank-deficient retained design to
silently return a pseudoinverse-based estimate rather than flagging
non-identifiability. Both are now checked explicitly in fit(); this file
exercises the actual patched function (imported by file path, not
reimplemented) against four cases: an ordinary estimable exposure, the
exact between-cluster-only-E failure mode, an exposure collinear with a
retained control, and a directly rank-deficient retained design.

Import safety (no refactor was needed): 16_estimate_preliminary.py's own
module-level code (path constants, dictionaries, log_lines = []) does no
file I/O and triggers no estimation; its full pipeline only runs under
`if __name__ == "__main__": main()`. Loading it via
importlib.util.spec_from_file_location gives it a module name other than
"__main__" (this file imports it as "hist16"), so exec_module() defines
its functions/constants without ever calling main() or touching the
restricted master-directory data. This was verified, not assumed: the
tests below run to completion without any restricted file present.

Data: synthetic only, generated with numpy's default_rng. No restricted
records, coordinates, or respondent identifiers of any kind appear here
or are read by this file.

Run with:
    python 26_test_fit_safeguard.py
(no special flags required; this directory does not contain untrusted
downloaded files, so -I is not necessary here, unlike a scratch/download
directory elsewhere in the project).
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
TARGET_PATH = SCRIPT_DIR / "16_estimate_preliminary.py"

spec = importlib.util.spec_from_file_location("hist16", TARGET_PATH)
hist16 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hist16)  # defines functions/constants only; does not call main()

fit = hist16.fit

rng = np.random.default_rng(0)


def make_base_df(n_clusters, per_cluster, rng):
    rows = []
    for g in range(n_clusters):
        for _ in range(per_cluster):
            rows.append(g)
    n = len(rows)
    return pd.DataFrame({
        "IDHSPSU": rows,
        "SAMPLE": 28806,  # a single synthetic "country" code; must be a key in hist16.SAMPLE_LABEL
        "KIDSEX": rng.choice([1, 2], size=n),
        "AGE": rng.uniform(18, 45, size=n),
        "EDUCLVL": rng.choice([0, 1, 2], size=n),
        "MARSTAT": rng.choice([0, 1], size=n),
        "age_m": rng.uniform(0, 59, size=n),
        "b_year": rng.choice([2014, 2015, 2016], size=n),
        "PERWEIGHT": np.ones(n),
    })


def test_a_ordinary_estimable():
    """E varies both between AND within clusters -> should estimate normally."""
    n_clusters, per_cluster = 40, 6
    df = make_base_df(n_clusters, per_cluster, rng)
    n = len(df)
    df["E"] = rng.uniform(0, 100, size=n)  # genuine within-cluster variation
    true_beta = 0.05
    df["Y"] = true_beta * df["E"] + 0.01 * df["age_m"] + rng.normal(0, 1, size=n)
    res = fit(df, "Y", weighted=False, wealth=False)
    assert res["status"] == "estimated", f"expected estimated, got {res['status']}"
    assert "E" not in res.get("columns_absorbed", [])
    assert abs(res["beta_per_point"] - true_beta) < 0.02, (
        f"recovered coefficient {res['beta_per_point']} too far from simulated {true_beta}"
    )
    print(f"  [A] ordinary estimable: status={res['status']}, "
          f"beta_per_point={res['beta_per_point']:.4f} (true {true_beta}), "
          f"N={res['N']}, G={res['G_clusters']}, rank={res['rank']}")


def test_b_exposure_absorbed_between_cluster_only():
    """E varies BETWEEN clusters but is CONSTANT within each cluster. Raw SD > 0
    (passes the early raw-variation check) but weighted within-cluster demeaning
    zeroes E entirely. This is the exact failure mode R05 describes: before the
    fix, this configuration silently mislabeled the next retained column's
    coefficient as E's own. The fixed function must refuse instead, and must not
    return any beta_per_point/se_CRV1/p_value as if E had been estimated."""
    n_clusters, per_cluster = 40, 6
    df = make_base_df(n_clusters, per_cluster, rng)
    cluster_e = rng.uniform(0, 100, size=n_clusters)
    df["E"] = df["IDHSPSU"].map(lambda g: cluster_e[g])
    n = len(df)
    df["Y"] = 0.02 * df["age_m"] + rng.normal(0, 1, size=n)
    res = fit(df, "Y", weighted=False, wealth=False)
    assert res["status"] == "non_estimable_exposure_absorbed", (
        f"expected non_estimable_exposure_absorbed, got {res['status']} "
        f"(beta_per_point={res.get('beta_per_point')!r})"
    )
    assert "beta_per_point" not in res
    assert "se_CRV1" not in res
    assert "p_value" not in res
    assert "E" in res.get("columns_absorbed", [])
    print(f"  [B] exposure absorbed (between-cluster-only E): status={res['status']} "
          f"(correctly refused; previous code would have mislabeled another "
          f"column's coefficient as E's own)")


def test_c_exposure_collinear_with_controls():
    """E is an exact linear combination of a retained nuisance control after
    demeaning (here: E := age_m exactly, within every cluster). This leaves E
    in the design (not absorbed to zero) but makes the retained design matrix
    rank-deficient once both E and age_m are kept."""
    n_clusters, per_cluster = 30, 6
    df = make_base_df(n_clusters, per_cluster, rng)
    df["E"] = df["age_m"].values.copy()  # exact collinearity with age_m
    n = len(df)
    df["Y"] = 0.03 * df["E"] + rng.normal(0, 1, size=n)
    res = fit(df, "Y", weighted=False, wealth=False)
    assert res["status"] == "non_estimable_rank_deficient", (
        f"expected non_estimable_rank_deficient, got {res['status']}"
    )
    assert "beta_per_point" not in res
    print(f"  [C] exposure collinear with a retained control: status={res['status']} "
          f"(correctly refused rather than reporting a pseudoinverse solution)")


def test_d_rank_deficient_nuisance_design():
    """A directly rank-deficient retained design via a duplicated dummy block:
    force MARSTAT to be a deterministic function of EDUCLVL within this
    synthetic sample, so the marstat dummy block is an exact linear function of
    the educlvl dummy block, independent of E."""
    n_clusters, per_cluster = 30, 8
    df = make_base_df(n_clusters, per_cluster, rng)
    n = len(df)
    df["E"] = rng.uniform(0, 100, size=n)
    df["MARSTAT"] = df["EDUCLVL"]  # marstat block collinear with educlvl block
    df["Y"] = 0.04 * df["E"] + rng.normal(0, 1, size=n)
    res = fit(df, "Y", weighted=False, wealth=False)
    assert res["status"] == "non_estimable_rank_deficient", (
        f"expected non_estimable_rank_deficient, got {res['status']}"
    )
    assert "beta_per_point" not in res
    print(f"  [D] rank-deficient retained nuisance design (duplicated dummy block): "
          f"status={res['status']} (correctly refused)")


if __name__ == "__main__":
    print("Running R05 estimator-safeguard tests against the patched fit() "
          f"in {TARGET_PATH.name} (synthetic data only)...")
    test_a_ordinary_estimable()
    test_b_exposure_absorbed_between_cluster_only()
    test_c_exposure_collinear_with_controls()
    test_d_rank_deficient_nuisance_design()
    print("\nAll four targeted tests passed.")
