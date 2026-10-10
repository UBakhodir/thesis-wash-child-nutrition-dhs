"""
28_test_compare_fit_safeguard_run.py
======================================
Synthetic regression tests for 27_compare_fit_safeguard_verification_run.py's
compare_runs() function, added 2026-10-10 after a targeted correction to that
script: its original version computed several per-row mismatch signals
(mismatched finiteness, duplicate ids, missing columns) but did not let them
affect the overall "identical_within_stated_tolerance" flag, and collapsed
NaN and +/-infinity into one "non-finite" bucket, so a NaN-vs-infinity
difference in the same column was never detected as a mismatch at all. These
tests exercise the actual corrected compare_runs() function via direct
import (not a reimplementation), on small synthetic DataFrames built in
memory - no restricted records, coordinates, or respondent identifiers of
any kind are read or written by this file.

Each test builds two small, synthetic "original" and "verification" style
DataFrames with the columns compare_runs() requires (id, status, the spec
columns, and the numeric columns), calls compare_runs(orig, new) directly,
and asserts that overall_result["identical_within_stated_tolerance"] is
False for every injected defect and True only for the unchanged-input case.

Run with:
    python 28_test_compare_fit_safeguard_run.py
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
TARGET_PATH = SCRIPT_DIR / "27_compare_fit_safeguard_verification_run.py"

spec = importlib.util.spec_from_file_location("compare27", TARGET_PATH)
compare27 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare27)  # defines functions/constants only; argparse CLI is under __main__

compare_runs = compare27.compare_runs
ID_COLUMN = compare27.ID_COLUMN
STATUS_COLUMN = compare27.STATUS_COLUMN
SPEC_COLUMNS = compare27.SPEC_COLUMNS
NUMERIC_COLUMNS = compare27.NUMERIC_COLUMNS


def make_rows(n=5, start_id=1):
    """A small, fully synthetic, internally consistent set of rows with every
    column compare_runs() requires, deterministic (no randomness needed for
    these structural tests)."""
    rows = []
    for i in range(n):
        rows.append({
            ID_COLUMN: f"m{start_id + i:04d}",
            STATUS_COLUMN: "estimated",
            "family": "primary",
            "product": "W_IMP",
            "outcome": "HAZ",
            "sample_group": "GH2014",
            "window": "post_12m",
            "weighted": True,
            "beta_per_point": 0.1 + 0.01 * i,
            "se_CRV1": 0.05,
            "ci95_low_per_point": 0.0,
            "ci95_high_per_point": 0.2,
            "p_value": 0.03,
            "beta_per_10": 1.0 + 0.1 * i,
            "se_per_10": 0.5,
            "ci95_low_per_10": 0.0,
            "ci95_high_per_10": 2.0,
            "E_within_sd": 1.5,
            "E_residual_sd_after_controls": 0.4,
            "N": 1000 + i,
            "G_clusters": 200,
            "K_regressors": 10,
            "rank": 10,
        })
    return pd.DataFrame(rows)


def test_unchanged_input_passes():
    """Baseline sanity check: identical data on both sides must pass."""
    orig = make_rows()
    new = orig.copy(deep=True)
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is True, (
        f"expected pass on unchanged input, got: {res['overall_result']}"
    )
    print("  [unchanged input] PASS, as expected")


def test_finite_vs_nonfinite_mismatch_fails():
    """The exact bug this correction targets: se_CRV1 is finite in the
    original but NaN in the verification run for one row. Must fail."""
    orig = make_rows()
    new = orig.copy(deep=True)
    new.loc[new[ID_COLUMN] == "m0001", "se_CRV1"] = np.nan
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False, (
        "a finite-vs-NaN difference in se_CRV1 must be detected as a failure"
    )
    assert "numeric_value_or_category_mismatch" in res["overall_result"]["failure_reasons"]
    col_report = res["numeric_comparison_by_column"]["se_CRV1"]
    assert col_report["n_category_mismatches"] == 1
    assert "m0001" in col_report["ids_with_category_mismatch"]
    print("  [finite-vs-nonfinite mismatch] correctly detected as FAIL")


def test_duplicate_ids_fail():
    """A duplicated id in the verification run must fail, not silently fan out
    through an inner/outer merge."""
    orig = make_rows()
    new = pd.concat([orig.copy(deep=True), orig.iloc[[0]].copy(deep=True)], ignore_index=True)
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False
    assert res["overall_result"].get("failure_reason") == "duplicate_model_ids"
    assert "m0001" in res["duplicate_ids"]["verification"]
    print("  [duplicate ids] correctly detected as FAIL")


def test_missing_id_fails():
    """An id present in the original but absent from the verification run
    must fail, and must be reflected as both a row-count and an id-set
    mismatch."""
    orig = make_rows(n=5)
    new = orig[orig[ID_COLUMN] != "m0003"].copy(deep=True)
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False
    assert res["overall_result"]["unequal_row_counts"] is True
    assert "missing_or_extra_ids" in res["overall_result"]["failure_reasons"]
    assert "m0003" in res["id_set_differences"]["missing_from_verification"]
    print("  [missing id / unequal row counts] correctly detected as FAIL")


def test_missing_required_column_fails():
    """Dropping a required numeric column entirely from one input must fail
    the comparison, not silently skip that check."""
    orig = make_rows()
    new = orig.copy(deep=True).drop(columns=["se_CRV1"])
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False
    assert res["overall_result"].get("failure_reason") == "missing_required_columns"
    assert "se_CRV1" in res["required_columns"]["missing_from_verification"]
    print("  [missing required column] correctly detected as FAIL")


def test_nan_vs_infinity_fails():
    """A NaN in the original and +infinity in the verification run for the
    same cell: both are 'non-finite', but they are not the same thing, and
    this must be detected as a mismatch rather than silently treated as
    agreeing because neither side is finite."""
    orig = make_rows()
    orig.loc[orig[ID_COLUMN] == "m0002", "beta_per_10"] = np.nan
    new = orig.copy(deep=True)
    new.loc[new[ID_COLUMN] == "m0002", "beta_per_10"] = np.inf
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False, (
        "a NaN-vs-infinity difference must be detected, not treated as an agreeing non-finite pair"
    )
    col_report = res["numeric_comparison_by_column"]["beta_per_10"]
    assert col_report["n_category_mismatches"] == 1
    assert "m0002" in col_report["ids_with_category_mismatch"]
    print("  [NaN-vs-infinity mismatch] correctly detected as FAIL")


def test_negative_vs_positive_infinity_fails():
    """-infinity and +infinity are also distinct categories and must not be
    treated as matching just because both are infinite."""
    orig = make_rows()
    orig.loc[orig[ID_COLUMN] == "m0004", "ci95_low_per_point"] = -np.inf
    new = orig.copy(deep=True)
    new.loc[new[ID_COLUMN] == "m0004", "ci95_low_per_point"] = np.inf
    res = compare_runs(orig, new)
    assert res["overall_result"]["identical_within_stated_tolerance"] is False
    col_report = res["numeric_comparison_by_column"]["ci95_low_per_point"]
    assert "m0004" in col_report["ids_with_category_mismatch"]
    print("  [-infinity-vs-+infinity mismatch] correctly detected as FAIL")


if __name__ == "__main__":
    print(f"Running synthetic regression tests for {TARGET_PATH.name} (synthetic data only)...")
    test_unchanged_input_passes()
    test_finite_vs_nonfinite_mismatch_fails()
    test_duplicate_ids_fail()
    test_missing_id_fails()
    test_missing_required_column_fails()
    test_nan_vs_infinity_fails()
    test_negative_vs_positive_infinity_fails()
    print("\nAll regression tests passed.")
