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
        --out "..\\..\\docs\\provenance\\fit_safeguard_verification_comparison_v1_2026-10-10.json"

(paths above are the actual runs used for this project's own R05 verification;
pass different --original/--verification to compare any other pair of runs.)
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

NUMERIC_COLUMNS = [
    "beta_per_point", "se_CRV1", "ci95_low_per_point", "ci95_high_per_point", "p_value",
    "beta_per_10", "se_per_10", "ci95_low_per_10", "ci95_high_per_10",
    "E_within_sd", "E_residual_sd_after_controls",
    "N", "G_clusters", "K_regressors", "rank",
]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--original", required=True, help="Directory of the original run")
    ap.add_argument("--verification", required=True, help="Directory of the verification run")
    ap.add_argument("--out", required=True, help="Output path for the JSON comparison summary")
    args = ap.parse_args()

    orig_df, orig_manifest, orig_csv_path, orig_manifest_path = load_run(args.original)
    new_df, new_manifest, new_csv_path, new_manifest_path = load_run(args.verification)

    summary = {
        "comparison_script": "scripts/historical_wash/27_compare_fit_safeguard_verification_run.py",
        "comparison_script_sha256": sha256_of_file(__file__),
        "original_run_dir": str(args.original),
        "verification_run_dir": str(args.verification),
        "original_csv_sha256": sha256_of_file(orig_csv_path),
        "verification_csv_sha256": sha256_of_file(new_csv_path),
    }

    # --- estimator script hashes, where available ---
    summary["estimator_script_sha256"] = {
        "original_manifest_value": (orig_manifest or {}).get("script_sha256"),
        "verification_manifest_value": (new_manifest or {}).get("script_sha256"),
        "note": (
            "These differ because the verification run used the patched fit() "
            "(script content changed by the R05 fix itself); this is expected "
            "and does not indicate an unintended difference. What matters is "
            "whether the *inputs* were identical (next field) and whether the "
            "*outputs* were identical (see numeric comparison below)."
        ),
    }

    # --- input-hash agreement ---
    orig_inputs = (orig_manifest or {}).get("inputs_before") or (orig_manifest or {}).get("inputs_after")
    new_inputs = (new_manifest or {}).get("inputs_before") or (new_manifest or {}).get("inputs_after")
    summary["input_hashes"] = {
        "original_run": orig_inputs,
        "verification_run": new_inputs,
        "agree": bool(orig_inputs) and bool(new_inputs) and orig_inputs == new_inputs,
    }

    # --- model counts ---
    summary["model_counts"] = {
        "original_rows": int(len(orig_df)),
        "verification_rows": int(len(new_df)),
        "original_unique_ids": int(orig_df["id"].nunique()),
        "verification_unique_ids": int(new_df["id"].nunique()),
    }

    # --- matching key, duplicates, missing/extra IDs ---
    orig_ids = orig_df["id"]
    new_ids = new_df["id"]
    summary["matching_key"] = "id"
    summary["duplicate_ids"] = {
        "original": sorted(orig_ids[orig_ids.duplicated()].unique().tolist()),
        "verification": sorted(new_ids[new_ids.duplicated()].unique().tolist()),
    }
    orig_id_set, new_id_set = set(orig_ids), set(new_ids)
    summary["id_set_differences"] = {
        "missing_from_verification": sorted(orig_id_set - new_id_set),
        "extra_in_verification": sorted(new_id_set - orig_id_set),
    }

    # Join on id; also verify spec correspondence on a few key descriptive columns
    spec_cols = [c for c in ["family", "product", "outcome", "sample_group", "window", "weighted"] if c in orig_df.columns]
    merged = orig_df.merge(new_df, on="id", suffixes=("_orig", "_new"), how="inner")
    spec_mismatches = {}
    for c in spec_cols:
        co, cn = f"{c}_orig", f"{c}_new"
        if co in merged.columns and cn in merged.columns:
            bad = merged[merged[co].astype(str) != merged[cn].astype(str)]
            if len(bad):
                spec_mismatches[c] = bad["id"].tolist()
    summary["spec_correspondence_mismatches_by_field"] = spec_mismatches
    summary["spec_correspondence_fields_checked"] = spec_cols

    # --- status agreement ---
    if "status_orig" in merged.columns and "status_new" in merged.columns:
        status_mismatch = merged[merged["status_orig"] != merged["status_new"]]
        summary["status_agreement"] = {
            "original_status_counts": orig_df["status"].value_counts().to_dict(),
            "verification_status_counts": new_df["status"].value_counts().to_dict(),
            "rows_with_differing_status": status_mismatch["id"].tolist(),
        }

    # --- numeric column comparison ---
    summary["numeric_columns_compared"] = NUMERIC_COLUMNS
    summary["comparison_tolerance_absolute"] = TOLERANCE_ABS
    numeric_results = {}
    for col in NUMERIC_COLUMNS:
        co, cn = f"{col}_orig", f"{col}_new"
        if co not in merged.columns or cn not in merged.columns:
            numeric_results[col] = {"note": "column not present in both runs; not compared"}
            continue
        a = pd.to_numeric(merged[co], errors="coerce")
        b = pd.to_numeric(merged[cn], errors="coerce")
        a_nonfinite = ~np.isfinite(a)
        b_nonfinite = ~np.isfinite(b)
        both_nonfinite = a_nonfinite & b_nonfinite
        mismatched_finiteness = a_nonfinite != b_nonfinite
        finite_mask = np.isfinite(a) & np.isfinite(b)
        diffs = (a[finite_mask] - b[finite_mask]).abs()
        differing_rows = merged.loc[finite_mask, "id"][diffs > TOLERANCE_ABS].tolist()
        numeric_results[col] = {
            "n_compared_finite_pairs": int(finite_mask.sum()),
            "n_both_non_finite": int(both_nonfinite.sum()),
            "n_mismatched_finiteness": int(mismatched_finiteness.sum()),
            "ids_with_mismatched_finiteness": merged.loc[mismatched_finiteness, "id"].tolist(),
            "max_abs_difference": float(diffs.max()) if len(diffs) else None,
            "mean_abs_difference": float(diffs.mean()) if len(diffs) else None,
            "n_rows_differing_beyond_tolerance": len(differing_rows),
            "ids_differing_beyond_tolerance": differing_rows,
        }
    summary["numeric_comparison_by_column"] = numeric_results

    all_max_diffs = [v["max_abs_difference"] for v in numeric_results.values() if v.get("max_abs_difference") is not None]
    any_status_mismatch = bool(summary.get("status_agreement", {}).get("rows_with_differing_status"))
    any_numeric_mismatch = any(v.get("n_rows_differing_beyond_tolerance", 0) > 0 for v in numeric_results.values())
    any_id_mismatch = bool(summary["id_set_differences"]["missing_from_verification"]) or bool(summary["id_set_differences"]["extra_in_verification"])
    any_spec_mismatch = bool(spec_mismatches)

    summary["overall_result"] = {
        "rows_compared": int(len(merged)),
        "all_ids_matched": not any_id_mismatch,
        "all_specs_matched": not any_spec_mismatch,
        "all_statuses_matched": not any_status_mismatch,
        "max_absolute_difference_across_all_numeric_columns": max(all_max_diffs) if all_max_diffs else None,
        "identical_within_stated_tolerance": (
            not any_id_mismatch and not any_spec_mismatch and not any_status_mismatch and not any_numeric_mismatch
        ),
        "coverage_note": (
            f"This comparison covers exactly the {len(NUMERIC_COLUMNS)} numeric columns listed in "
            "'numeric_columns_compared' above, plus the 'status' column and the spec-identity columns "
            "listed in 'spec_correspondence_fields_checked'. It does not claim every column in the "
            "source CSV was compared - any column not listed there was not checked by this script."
        ),
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(f"Wrote comparison summary to: {out_path}")
    print(json.dumps(summary["overall_result"], indent=2))


if __name__ == "__main__":
    main()
