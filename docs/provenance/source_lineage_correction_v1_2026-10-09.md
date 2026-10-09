# Source-lineage correction (2026-10-09)

Starting commit: `068ee4c` (confirmed `HEAD == origin/main`, clean except the standing untracked `outputs/supervisor_meeting/`). Canonical manuscript: `manuscript/v11_2026-10-09/`, unchanged by this pass (no chapter text, claim, or displayed value required a change — see §1). No PDF was generated, compiled, rebuilt, or rendered. No model was rerun.

This pass corrects two false claims made in `docs/provenance/final_source_verification_v1_2026-10-09.md` (the immediately preceding task): that two historical-table rounding values "could not be adjudicated" and that their full-precision restricted source "no longer exists on disk." Both claims were wrong, caused by an incomplete search (checking only this git repository's own `data/` subdirectory, not the master project directory one level above it). Both specific files have been corrected in place (§4); this file is the full record of the evidence.

## 1. Rounding evidence

Read `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` (291 rows, git-tracked) directly by row `id`, not by positional index (the task's stated row numbers, `m0142`/`m0143`, are the `id` column's values, not 0-indexed row positions — row `id == "m0142"` sits at pandas positional index 141, not 142; confirming this distinction matters for anyone re-deriving this independently).

**Row identity, confirmed:**

| | `id` | `family` | `product` | `outcome` | `sample_group` | `window` | `weighted` | `N` | `G_clusters` |
|---|---|---|---|---|---|---|---|---|---|
| Ghana | `m0142` | `primary` | `S_IMP` | `HAZ` | `GH2014` | `post_12m` | `True` | 1,940 | 353 |
| Kenya | `m0143` | `primary` | `S_IMP` | `HAZ` | `KE2014` | `post_12m` | `True` | 14,166 | 1,498 |

This exactly matches the task's own description ("Ghana sanitation–HAZ, primary weighted post-12-month model" / "Kenya counterpart") and the manuscript's Table 5.6 cells (Ghana/Kenya sanitation–HAZ, established-date, primary specification).

**Full-precision values, read directly from the CSV:**

- `m0142.ci95_low_per_10` = `-4.9146807319418855` → rounds to **`-4.91`** (not `-4.92`: the value is `0.0053193` away from `-4.92` and only `0.0046807` away from `-4.91`, so it rounds down in magnitude, to `-4.91`, unambiguously).
- `m0143.ci95_high_per_10` = `0.1053050394220738` → rounds to **`0.11`** (the value exceeds the `0.105` midpoint, so standard rounding gives `0.11`, unambiguously).

Both values were independently re-confirmed by reading the **primary, non-aggregated** restricted source directly (§2 below), not only the git-tracked aggregate file, and the two match to full float64 precision (`-4.9146807319418855` and `0.1053050394220738` / `0.1053050394220738` respectively — identical).

**Specification and internal consistency, verified:** both rows' other fields (`beta_per_10`, `se_per_10`, `p_value`, `N`, `G_clusters`) match the public core reporting table (`docs/provenance/final_empirical_package_v3_2026-10-07/02_core_reporting_table.md`) to its displayed 3-decimal precision exactly: Ghana β=-2.480 (source: -2.479998), SE≈1.238, p=.046 (source: .0459079); Kenya β=-0.212 (source: -0.212242), SE≈0.162, p=.190 (source: .1900385). This confirms `m0142`/`m0143` are the identical specification already reported in the manuscript, not a different model that happens to share an outcome/country label.

**Conclusion: the manuscript's existing displayed values, `−4.91` and `0.11` (in `05_results.md` Table 5.6 and `appendices/C_historical_diagnostics_and_ethiopia.md`), were already correct.** No manuscript value changed. What was wrong was the immediately preceding pass's claim that this could not be verified.

## 2. Artifact-location finding: path mismatch, not a missing or deleted file

**Checked both locations specified in this task:**

1. **This git repository's `data/` directory** (`thesis-wash-child-nutrition-dhs/data/processed/estimation/`): contains only one directory, `inference_reconciliation_20261007T184447Z/` — a different, smaller, unrelated run. This is the directory the preceding pass checked, and finding nothing matching there, incorrectly concluded the source was deleted.
2. **The master `Graduation_Thesis/` directory outside the repository** (`C:\Users\user\Documents\Graduation_Thesis\data\processed\estimation\`, one level above the git repository root): contains **14 run directories**, including `run_20261006T185646Z/` — fully intact, with `model_results_RESTRICTED_coefficients.csv` (291 rows, 41 columns, last modified 2026-10-06 20:57), `execution_log.txt`, `manifest.json`, `primary_model_datasets_RESTRICTED.parquet`, and a `design_checks_20261006T190020Z/` subdirectory. Also present and intact: `pooled_independent_validation_20261007T090003Z/`, `all_primary_independent_validation_20261007T173736Z/`, `birthyear_coding_diagnostic_20261009T081301Z/`, and every other restricted output directory referenced throughout this manuscript's provenance files across the entire session.

**Manifest inspected** (`run_20261006T185646Z/manifest.json`): records the generating script (`scripts/historical_wash/16_estimate_preliminary.py`, with its own SHA-256), the Python/package versions, and SHA-256 hashes for both inputs, recorded identically both before and after the run (`"inputs_unchanged": true`), with `models_planned: 291`, `models_estimated: 291`, `models_non_estimable: 0`. This is a complete, self-verifying provenance record, not a partial or corrupted artifact.

**Finding: this is a path mismatch in the preceding pass's own search, not a genuinely missing or deleted artifact, and not evidence of any gitignore-related loss.** The confusion arose because this git repository (`thesis-wash-child-nutrition-dhs/`) and the master project folder that contains it (`Graduation_Thesis/`) each have their own, separate `data/processed/estimation/` directory at the same relative sub-path, and only the master one is actually used by the estimation scripts (confirmed in §3). The repository's own `data/` directory is gitignored and largely unused for this project's actual restricted-data workflow; checking only it, as the preceding pass did, will reliably miss this project's real restricted outputs.

## 3. Reproduction path: scripts, inputs, and working directory

Inspected `scripts/historical_wash/16_estimate_preliminary.py` (the script that produced `run_20261006T185646Z/`) directly. It hardcodes its root as an absolute path, not a path relative to the script file or any working directory:

```python
MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
AN = os.path.join(MASTER, "data", "processed", "analysis_samples", "run_20261006T184744Z", "analysis_candidates_RESTRICTED.parquet")
CON = os.path.join(MASTER, "data", "processed", "child_exposure", "run_20261006T183803Z", "child_exposure_candidates_RESTRICTED.parquet")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "estimation")
```

This means the script's inputs and outputs are always resolved against the master `Graduation_Thesis` directory regardless of the working directory the script happens to be invoked from, or where the script file itself lives (inside the `thesis-wash-child-nutrition-dhs` git repository's `scripts/historical_wash/`). **Both declared inputs were checked and confirmed to still exist**, intact, at their hardcoded master-directory paths:

- `data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet` — exists.
- `data/processed/child_exposure/run_20261006T183803Z/child_exposure_candidates_RESTRICTED.parquet` — exists.

**Consequence: nothing is actually missing, and no recovery is needed.** The authoritative output (`run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv`) is directly available and was read directly in §1 above; reproduction from the preserved inputs would also be possible if ever needed (both inputs and the generating script are intact), but is not necessary here since the output itself is already available and has now been read.

## 4. Provenance synchronized

- `docs/provenance/final_source_verification_v1_2026-10-09.md`: corrected in place. The false "no longer exists on disk" / "could not be adjudicated" claims (§3.3, Category C, and the closing sections) are replaced with accurate statements pointing to this file, with a correction notice added at the top of the document.
- `manuscript/v11_2026-10-09/README.md` and `CORRECTION_LOG.md`: the "unresolved, not corrected" rounding-ambiguity passages corrected to state the resolution and point to this file.
- `manuscript/v11_2026-10-09/claim_evidence_ledger.md`: a dating note added to the header distinguishing the original 2026-10-07 session's "this session" wording (which, read literally today, could be misread as a claim by a later session) from an actually-current re-verification; the historical established-date models' row updated with an explicit 2026-10-09 re-verification entry naming the master-directory path, the two row ids, and their full-precision values.

No chapter file (`01_introduction.md` through `08_abstract.md`, or any appendix) required any change — the manuscript's displayed values were already correct throughout. No new manuscript version was created; this pass corrects provenance/ledger documentation only.

## 5. What this pass did not do

Did not rerun `16_estimate_preliminary.py` or any other model — the existing, intact output was read directly and was sufficient to resolve both rounding questions. Did not modify `run_20261006T185646Z/` or any other restricted output or input file. Did not copy restricted data into the git repository or otherwise change where it lives. Did not generate, compile, rebuild, or render any PDF.

## 6. Final status

Both rounding-boundary values are resolved and confirmed correct as already displayed in the manuscript. The restricted-data lineage is fully intact and reproducible from preserved inputs if ever needed, located at `C:\Users\user\Documents\Graduation_Thesis\data\` (the master project directory, outside this git repository), not at `thesis-wash-child-nutrition-dhs\data\`. Future passes checking for restricted outputs should search the master directory first.

## Canonical path and commit

`manuscript/v11_2026-10-09/` (unchanged by this pass). Commit follows this file.
