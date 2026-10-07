# Reproduction instructions and lineage (2026-10-07)

## Environment

- Interpreter: `C:\Users\user\Documents\Graduation_Thesis\.venv\Scripts\python.exe` (Python 3.14.0)
- Key packages (historical pipeline, from `data/processed/estimation/run_20261006T185646Z/manifest.json`): numpy 2.5.1, pandas 3.0.5, pyarrow 25.0.0.
- Full dependency list: `requirements.txt` at the repository root.

## Baseline pipeline (frozen; do not modify)

Scripts `scripts/` steps 00–14 (harmonization through `14_household_community_wash_models.py`). Outputs in `outputs/household_community_wash/` and `outputs/regressions/`. This pipeline is frozen and must not be rerun or edited; it was not rerun in this pass.

## Historical extension pipeline

Run in order from `scripts/historical_wash/`:

1. `01_inventory_ihme_rasters.py` — IHME raster inventory and NoData/value-range checks.
2. `02_import_ipums_idhs_00001.py` — initial IPUMS-DHS import (superseded by `03`/`05` for structural issues; preserved).
3. `03_import_validate_idhs_00002.py`, `04_supplementary_checks_idhs_00002.py`, `05_resolve_idhs_00002.py` — corrected import, validation and resolution of the IPUMS-DHS extract.
4. `06_ethiopia_calendar_audit.py` — Ethiopian-calendar interview-date reconciliation (produces the three provisional candidates C1–C3).
5. `07_coordinate_survey_correspondence.py` — cluster coordinate-to-survey/DHSID correspondence check.
6. `10_spatial_extraction_v3.py` — AEQD exact disk/pixel-overlap spatial extraction (final method; `08` and `09` are superseded, preserved for lineage).
7. `11_validate_spatial_outputs.py` — spatial-extraction validation.
8. `12_construct_exposure_windows.py`, `13_validate_exposure_construction.py` — exposure-window construction and validation.
9. `14_build_analysis_samples.py` — analysis-sample construction.
10. `15_design_diagnostics.py` — pre-estimation design diagnostics.
11. `16_estimate_preliminary.py` — estimates all 291 models.
12. `17_validate_estimates.py` — independent re-estimation of 4 representative models.
13. `18_common_sample_windows.py` — common-sample window comparison.
14. `19_check_model_design.py` — per-model design checks (key uniqueness, weight totals, rank, singletons).

Each script writes a timestamped run folder under `data/processed/<stage>/run_<UTC timestamp>/` (RESTRICTED, git-ignored) containing a `manifest.json` with script SHA-256, environment, and input/output content hashes, so any run's exact inputs can be confirmed unchanged. Public aggregate outputs (no microdata, no coordinates, no identifiers) are written to `docs/provenance/historical_wash_*` and `docs/provenance/historical_wash_*_v1/`.

## Key run identifiers (for audit trail; RESTRICTED paths, not for manuscript citation)

- Final spatial extraction: `data/processed/spatial_extraction/run_v3_20261006T183003Z/`
- Exposure construction: `data/processed/child_exposure/run_20261006T183803Z/`
- Analysis samples: `data/processed/analysis_samples/run_20261006T184744Z/`
- Estimation (291 models): `data/processed/estimation/run_20261006T185646Z/` — `models_planned: 291, models_estimated: 291, models_non_estimable: 0`, `inputs_unchanged: true`.
- Independent validation: `data/processed/estimation/validation_20261006T185831Z/` — `max_beta_abs_diff: 2.96e-14`, `passed: true`.
- Design checks: `data/processed/estimation/run_20261006T185646Z/design_checks_20261006T190020Z/` — all 7 checks pass across 24 primary models.
- Common-sample window comparison: `data/processed/estimation/common_sample_20261006T185909Z/`.

## What was and was not rerun in this pass (2026-10-07)

**Not rerun:** the baseline pipeline (00–14) and the entire historical pipeline (01–19). All outputs referenced in `00_results_index.md` are reused from the runs above; their `manifest.json` files confirm inputs were unchanged at execution time, and no corrected script or unresolved validation failure was found that would justify a rerun.

**Newly done in this pass:** re-derivation of the baseline reporting table directly from the CSVs (not from any chat or document) to resolve the two flagged discrepancies (`baseline_evidence_reconciliation_v1_2026-10-07.md`); the supervisor-advice matrix built from the provided meeting transcript; two further attempts to locate DHS biomarker-weight documentation (DHS-8 Biomarker Manual PDF, World Bank microdata catalogue variable page) — both unsuccessful, so issue #1 in the methods note's unresolved list (§9) remains open.
