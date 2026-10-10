"""
27_compare_fit_safeguard_verification_run.py
==============================================
Produces a machine-readable, non-sensitive comparison summary between the
original stored historical-estimation output and the 2026-10-10 verification
re-run of 16_estimate_preliminary.py after the R05 estimator-safeguard fix
(see docs/provenance/independent_audit_resolution_v1_2026-10-10.md).

Purpose: confirm, with an explicit, reproducible comparison rather than a
narrative claim, whether the safeguard fix changed any of the 291 published
historical model rows. It did not (see the generated summary), but this
script is what actually establishes that, and can be re-run against any two
runs by passing different --original/--verification paths.

Corrected 2026-10-10 (v2): the original version of this script computed
"n_mismatched_finiteness" per numeric column but never let it affect
"identical_within_stated_tolerance" - a column where a finite value was
replaced by NaN (or vice versa) could still report overall success, because
the difference-based check only ever looked at rows where *both* sides were
finite. Likewise, duplicate IDs were reported but did not gate the result (a
plain inner merge on a duplicated key silently fans out rather than failing),
a missing numeric/status/spec column caused that check to be skipped rather
than counted as a failure, and np.isfinite() alone cannot distinguish NaN
from +/-infinity, so a NaN-vs-infinity difference in the same column would
never be flagged (both are simply "not finite" on both sides). All five are
fixed below: every value is classified into one of {"finite", "nan",
"+inf", "-inf"}; any mismatch in that classification between the two runs is
itself a failure, independent of the numeric-difference check; the merge
uses pandas' own `validate="one_to_one"` (raising, and being caught and
reported as an explicit failure, rather than silently fanning out, if either
side has a duplicate key); every required id/status/spec/numeric column is
checked present in both inputs *before* any comparison runs, with a missing
column recorded as a failure rather than a skipped check; and row-count
equality is checked as its own explicit condition alongside the id-set
difference check. See 28_test_compare_fit_safeguard_run.py for synthetic
regression tests proving each of these failure modes is now detected, and an
unchanged-input case that still passes.

Inputs (both RESTRICTED; read-only; never written to by this script):
  --original      path to the original run's model_results_RESTRICTED_coefficients.csv
                   and its manifest.json (same directory)
  --verification   path to the verification run's equivalents

Output: a JSON summary written to --out (default: a path under
docs/provenance/, which is this repository's own tracked, non-restricted
directory). The JSON contains only aggregate statistics (counts, hashes,
max/mean differences, lists of model IDs) - no row-level restricted data,
no microdata, no coordinates, no respondent identifiers.

Usage:
    python 27_compare_fit_safeguard_verification_run.py \
        --original "C:\\Users\\user\\Documents\\Graduation_Thesis\\data\\processed\\estimation\\run_20261006T185646Z" \
        --verification "C:\\Users\\user\\Documents\\Graduation_Thesis\\data\\processed\\estimation\\run_20261010T140944Z" \
        --out "..\\..\\docs\\provenance\\fit_safeguard_verification_comparison_v2_2026-10-10.json"

(paths above are the actual runs used for this project's own R05 verification;
pass different --original/--verification to compare any other pair of runs.)
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ID_COLUMN = "id"
STATUS_COLUMN = "status"
SPEC_COLUMNS = ["family", "product", "outcome", "sample_group", "window", "weighted"]
NUMERIC_COLUMNS = [
    "beta_per_point", "se_CRV1", "ci95_low_per_point", "ci95_high_per_point", "p_value",
    "beta_per_10", "se_per_10", "ci95_low_per_10", "ci95_high_per_10",
    "E_within_sd", "E_residual_sd_after_controls",
    "N", "G_clusters", "K_regressors", "rank",
]
REQUIRED_COLUMNS = [ID_COLUMN, STATUS_COLUMN] + SPEC_COLUMNS + NUMERIC_COLUMNS
TOLERANCE_ABS = 0.0  # exact-match tolerance used for this comparison; stated explicitly in the output


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_run(run_dir):
    run_dir = Path(run_dir)
    csv_path = run_dir / "model_results_RESTRICTED_coefficients.csv"
    manifest_path = run_dir / "manifest.json"
    df = pd.read_csv(csv_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else None
    return df, manifest, str(csv_path), (str(manifest_path) if manifest_path.exists() else None)


def classify_value(x):
    """Classify a single value into exactly one of 'finite', 'nan', '+inf', '-inf'.
    Distinguishing these (rather than collapsing everything non-finite into one
    bucket) is what lets a NaN-vs-infinity difference be detected as a mismatch,
    not just a finite-vs-nonfinite one."""
    if pd.isna(x):
        return "nan"
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return "nan"
    if np.isnan(xf):
        return "nan"
    if np.isposinf(xf):
        return "+inf"
    if np.isneginf(xf):
        return "-inf"
    return "finite"


def compare_runs(orig_df, new_df):
    """Core, file-I/O-free comparison logic, factored out so it can be driven
    directly by synthetic DataFrames in tests, not only via the CLI against
    real restricted CSVs. Returns a summary dict (without the file-hash /
    script-hash fields, which main() adds afterward since they need file
    paths this function does not take)."""
    summary = {}

    # --- required-column check, performed before anything else ---
    missing_from_orig = [c for c in REQUIRED_COLUMNS if c not in orig_df.columns]
    missing_from_new = [c for c in REQUIRED_COLUMNS if c not in new_df.columns]
    summary["required_columns"] = {
        "required": REQUIRED_COLUMNS,
        "missing_from_original": missing_from_orig,
        "missing_from_verification": missing_from_new,
    }
    any_missing_columns = bool(missing_from_orig) or bool(missing_from_new)
    if any_missing_columns:
        # Cannot safely proceed with id-based comparison if "id" itself is
        # missing; stop here with an explicit failure rather than guessing.
        summary["overall_result"] = {
            "identical_within_stated_tolerance": False,
            "failure_reason": "missing_required_columns",
            "coverage_note": (
                "Comparison aborted before row-level checks: one or both inputs "
                "are missing required columns (see 'required_columns' above). "
                "This is reported as a failure, not a skipped check."
            ),
        }
        return summary

    # --- duplicate-id check, performed before any merge ---
    orig_ids = orig_df[ID_COLUMN]
    new_ids = new_df[ID_COLUMN]
    dup_orig = sorted(orig_ids[orig_ids.duplicated()].unique().tolist())
    dup_new = sorted(new_ids[new_ids.duplicated()].unique().tolist())
    summary["duplicate_ids"] = {"original": dup_orig, "verification": dup_new}
    any_duplicates = bool(dup_orig) or bool(dup_new)

    # --- row counts and id-set differences (computed regardless of duplicates,
    # since these are meaningful even if we must abort before merging) ---
    orig_id_set, new_id_set = set(orig_ids), set(new_ids)
    missing_from_verification = sorted(orig_id_set - new_id_set)
    extra_in_verification = sorted(new_id_set - orig_id_set)
    summary["model_counts"] = {
        "original_rows": int(len(orig_df)),
        "verification_rows": int(len(new_df)),
        "original_unique_ids": int(orig_df[ID_COLUMN].nunique()),
        "verification_unique_ids": int(new_df[ID_COLUMN].nunique()),
    }
    summary["matching_key"] = ID_COLUMN
    summary["id_set_differences"] = {
        "missing_from_verification": missing_from_verification,
        "extra_in_verification": extra_in_verification,
    }
    any_row_count_mismatch = len(orig_df) != len(new_df)
    any_id_set_mismatch = bool(missing_from_verification) or bool(extra_in_verification)

    if any_duplicates:
        summary["overall_result"] = {
            "identical_within_stated_tolerance": False,
            "failure_reason": "duplicate_model_ids",
            "coverage_note": (
                "Comparison aborted before merging: a one-to-one merge on "
                "'id' is required, and at least one input has a duplicated "
                "id (see 'duplicate_ids' above). A merge on a duplicated key "
                "would silently fan out rather than compare rows 1:1, so no "
                "row-level comparison was attempted."
            ),
        }
        return summary

    # --- one-to-one merge, enforced structurally by pandas (not only by the
    # duplicate pre-check above, as defense in depth), plus an outer join so
    # id-only-on-one-side rows are visible in the merged frame too ---
    try:
        merged = orig_df.merge(
            new_df, on=ID_COLUMN, suffixes=("_orig", "_new"), how="outer",
            indicator=True, validate="one_to_one",
        )
    except pd.errors.MergeError as exc:
        summary["overall_result"] = {
            "identical_within_stated_tolerance": False,
            "failure_reason": "merge_validation_failed",
            "merge_error": str(exc),
            "coverage_note": "pandas' own one-to-one merge validation rejected this pair of inputs.",
        }
        return summary

    both_sides = merged[merged["_merge"] == "both"].drop(columns=["_merge"])
    only_orig = merged.loc[merged["_merge"] == "left_only", ID_COLUMN].tolist()
    only_new = merged.loc[merged["_merge"] == "right_only", ID_COLUMN].tolist()
    # Cross-check the outer-merge indicator against the set-based computation above.
    assert sorted(only_orig) == missing_from_verification
    assert sorted(only_new) == extra_in_verification

    # --- spec-identity correspondence, required columns, checked on matched rows only ---
    spec_mismatches = {}
    for c in SPEC_COLUMNS:
        co, cn = f"{c}_orig", f"{c}_new"
        bad = both_sides[both_sides[co].astype(str) != both_sides[cn].astype(str)]
        if len(bad):
            spec_mismatches[c] = bad[ID_COLUMN].tolist()
    summary["spec_correspondence_mismatches_by_field"] = spec_mismatches
    summary["spec_correspondence_fields_checked"] = SPEC_COLUMNS
    any_spec_mismatch = bool(spec_mismatches)

    # --- status agreement (status is now a required column, checked above) ---
    status_mismatch = both_sides[both_sides["status_orig"] != both_sides["status_new"]]
    summary["status_agreement"] = {
        "original_status_counts": orig_df[STATUS_COLUMN].value_counts().to_dict(),
        "verification_status_counts": new_df[STATUS_COLUMN].value_counts().to_dict(),
        "rows_with_differing_status": status_mismatch[ID_COLUMN].tolist(),
    }
    any_status_mismatch = bool(status_mismatch[ID_COLUMN].tolist())

    # --- numeric column comparison, now classification-based ---
    summary["numeric_columns_compared"] = NUMERIC_COLUMNS
    summary["comparison_tolerance_absolute"] = TOLERANCE_ABS
    numeric_results = {}
    any_numeric_mismatch = False
    for col in NUMERIC_COLUMNS:
        co, cn = f"{col}_orig", f"{col}_new"
        a_raw, b_raw = both_sides[co], both_sides[cn]
        cat_a = a_raw.map(classify_value)
        cat_b = b_raw.map(classify_value)
        category_mismatch_mask = cat_a != cat_b
        category_mismatch_ids = both_sides.loc[category_mismatch_mask, ID_COLUMN].tolist()

        finite_mask = (cat_a == "finite") & (cat_b == "finite")
        a_num = pd.to_numeric(a_raw[finite_mask], errors="coerce")
        b_num = pd.to_numeric(b_raw[finite_mask], errors="coerce")
        diffs = (a_num - b_num).abs()
        beyond_tol_mask = diffs > TOLERANCE_ABS
        differing_ids = both_sides.loc[finite_mask, ID_COLUMN][beyond_tol_mask.values].tolist()

        col_has_mismatch = bool(category_mismatch_ids) or bool(differing_ids)
        any_numeric_mismatch = any_numeric_mismatch or col_has_mismatch

        numeric_results[col] = {
            "n_rows_compared": int(len(both_sides)),
            "n_finite_pairs": int(finite_mask.sum()),
            "value_category_counts_original": cat_a.value_counts().to_dict(),
            "value_category_counts_verification": cat_b.value_counts().to_dict(),
            "n_category_mismatches": len(category_mismatch_ids),
            "ids_with_category_mismatch": category_mismatch_ids,
            "max_abs_difference_among_finite_pairs": float(diffs.max()) if len(diffs) else None,
            "mean_abs_difference_among_finite_pairs": float(diffs.mean()) if len(diffs) else None,
            "n_finite_pairs_differing_beyond_tolerance": len(differing_ids),
            "ids_differing_beyond_tolerance": differing_ids,
            "column_has_any_mismatch": col_has_mismatch,
        }
    summary["numeric_comparison_by_column"] = numeric_results

    all_max_diffs = [
        v["max_abs_difference_among_finite_pairs"] for v in numeric_results.values()
        if v.get("max_abs_difference_among_finite_pairs") is not None
    ]

    overall_fail_reasons = []
    if any_row_count_mismatch:
        overall_fail_reasons.append("unequal_row_counts")
    if any_id_set_mismatch:
        overall_fail_reasons.append("missing_or_extra_ids")
    if any_spec_mismatch:
        overall_fail_reasons.append("spec_correspondence_mismatch")
    if any_status_mismatch:
        overall_fail_reasons.append("status_mismatch")
    if any_numeric_mismatch:
        overall_fail_reasons.append("numeric_value_or_category_mismatch")

    summary["overall_result"] = {
        "rows_compared_both_sides": int(len(both_sides)),
        "unequal_row_counts": any_row_count_mismatch,
        "all_ids_matched": not any_id_set_mismatch,
        "all_specs_matched": not any_spec_mismatch,
        "all_statuses_matched": not any_status_mismatch,
        "all_numeric_values_and_categories_matched": not any_numeric_mismatch,
        "max_absolute_difference_among_finite_pairs_across_all_numeric_columns": (
            max(all_max_diffs) if all_max_diffs else None
        ),
        "failure_reasons": overall_fail_reasons,
        "identical_within_stated_tolerance": len(overall_fail_reasons) == 0,
        "coverage_note": (
            f"This comparison requires exactly these columns to be present in both inputs: "
            f"'{ID_COLUMN}', '{STATUS_COLUMN}', the {len(SPEC_COLUMNS)} spec-identity columns "
            f"{SPEC_COLUMNS}, and the {len(NUMERIC_COLUMNS)} numeric columns listed in "
            "'numeric_columns_compared'. A missing required column, a duplicated id, a "
            "finite-vs-nonfinite difference, or a NaN-vs-infinity difference are each treated "
            "as a failure on their own, independent of whether any finite numeric value differs "
            "beyond the stated tolerance. It does not claim every column in the source CSV was "
            "compared - any column not in the required list above was not checked."
        ),
    }
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--original", required=True, help="Directory of the original run")
    ap.add_argument("--verification", required=True, help="Directory of the verification run")
    ap.add_argument("--out", required=True, help="Output path for the JSON comparison summary")
    args = ap.parse_args()

    orig_df, orig_manifest, orig_csv_path, orig_manifest_path = load_run(args.original)
    new_df, new_manifest, new_csv_path, new_manifest_path = load_run(args.verification)

    header = {
        "comparison_script": "scripts/historical_wash/27_compare_fit_safeguard_verification_run.py",
        "comparison_script_sha256": sha256_of_file(__file__),
        "original_run_dir": str(args.original),
        "verification_run_dir": str(args.verification),
        "original_csv_sha256": sha256_of_file(orig_csv_path),
        "verification_csv_sha256": sha256_of_file(new_csv_path),
        "estimator_script_sha256": {
            "original_manifest_value": (orig_manifest or {}).get("script_sha256"),
            "verification_manifest_value": (new_manifest or {}).get("script_sha256"),
            "note": (
                "These differ because the verification run used the patched fit() "
                "(script content changed by the R05 fix itself); this is expected "
                "and does not indicate an unintended difference. What matters is "
                "whether the *inputs* were identical (next field) and whether the "
                "*outputs* were identical (see numeric comparison below)."
            ),
        },
        "input_hashes": (lambda oi, ni: {
            "original_run": oi, "verification_run": ni,
            "agree": bool(oi) and bool(ni) and oi == ni,
        })(
            (orig_manifest or {}).get("inputs_before") or (orig_manifest or {}).get("inputs_after"),
            (new_manifest or {}).get("inputs_before") or (new_manifest or {}).get("inputs_after"),
        ),
    }

    body = compare_runs(orig_df, new_df)
    summary = {**header, **body}

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"Wrote comparison summary to: {out_path}")
    print(json.dumps(summary["overall_result"], indent=2))


if __name__ == "__main__":
    main()
