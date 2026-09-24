# Reproducibility Package Manifest

This package is a read-only copy of the frozen DHS data-harmonization and regression pipeline (Steps 00–13) behind the thesis "The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa," together with its methodological documentation, already-validated results, provenance record, and literature evidence base. It lets a reviewer inspect the empirical methodology and results without requiring DHS microdata access and without redistributing restricted or copyrighted material.

Built: 2026-08-17.
Updated: 2026-09-22 — added household- and community-WASH specification outputs (see below); the
original Steps 00–13 pipeline and its frozen results are unchanged from the 2026-08-17 build.

## What's included

- The 14 pipeline scripts, `scripts/dhs_harmonization/00_config.py` through `13_final_outputs.py`
- `README.md`, `requirements.txt`, `CONTRIBUTORS.md`
- `docs/thesis_design.md` and `docs/data_dictionary.md`, the project's empirical design documents, and `docs/code_guide.md`, a guide to where each methodological decision is implemented
- Generated results: `outputs/tables/` (pipeline diagnostics), `outputs/regressions/` (raw coefficient tables), `outputs/final_tables/`, `outputs/final_appendix/`, `outputs/final_figures/`, and `outputs/final_audit/` (the project's provenance and audit record, with a short index written for this package)
- Derived literature materials: `sources/summaries/` and `sources/bibliography/`
- Household- and community-WASH specification outputs, `scripts/dhs_harmonization/14_household_community_wash_models.py`
  and `outputs/household_community_wash/` — see the dedicated section below for exactly what this contains.
  The canonical empirical-strategy document, `docs/empirical_strategy.md`, and its drafting provenance
  under `docs/provenance/` are tracked alongside the project's other design documents.

## Household and Community WASH Specification Outputs (added 2026-09-22)

Following methodological feedback on the frozen Steps 00–13 results, `scripts/dhs_harmonization/14_household_community_wash_models.py`
was added, together with its outputs under `outputs/household_community_wash/`. This is additive: it reads
the already-frozen Step 00–13 outputs read-only (see `outputs/household_community_wash/baseline_file_hashes.csv`
and `run_log.txt`) and does not alter Step 00–13 analytical logic or generated results.

Included from this specification-outputs directory:

- The 16 numbered aggregate diagnostic CSVs (`01_development_sample_flow.csv` through
  `16_development_model_summary.csv`, including the `09b`/`15b` sub-parts — 18 files in total) —
  household-vs-community WASH identification diagnostics, within-cluster variation checks,
  age-heterogeneity joint tests, and Nigeria specification-sensitivity checks.
- Provenance/reproducibility records: `baseline_file_hashes.csv`, `run_log.txt`.
- The full analysis narrative, `analysis_report.md`.

Tracked separately, alongside the project's other design documents rather than under
`outputs/household_community_wash/`:

- The canonical empirical-strategy document, `docs/empirical_strategy.md`.
- A literature/design consistency check, `docs/literature_design_consistency.md`.
- Its drafting provenance — a wording-revision note and a PDF-rendering/QA record — under
  `docs/provenance/empirical_strategy_revision_note.md` and
  `docs/provenance/empirical_strategy_render_qa.md`.
- A methodological adjudication note for the household cluster-FE standard-error convention, under
  `docs/provenance/cluster_fe_inference_adjudication.md`.

These extended specification outputs are not yet integrated into `outputs/final_tables/`,
`outputs/final_appendix/`, or `outputs/final_figures/`; that integration is planned once the final
specification set is fixed (see README.md, "Final Outputs").

Intentionally excluded from this package:

- The intermediate drafting chain of prior empirical-strategy documents in the working project —
  superseded by `docs/empirical_strategy.md`; not copied, to avoid presenting superseded wording as
  current.
- Every rendered PDF, including the empirical-strategy PDF — the working project already holds the PDF
  actually sent to the supervisor; this package tracks the Markdown source and its validation provenance,
  not a duplicate generated binary.
- `render_temp/` and all other LaTeX build/rasterization artifacts — regenerable build debris, not
  reproducibility-relevant.
- `outputs/data_audit/`, `data/raw/`, `data/interim/`, `data/processed/`, and any DHS GPS/geospatial file
  — restricted DHS microdata remains excluded from this package exactly as it was from the original
  2026-08-17 build (see "What's excluded, and why" below, which continues to apply unchanged).

## What's excluded, and why

DHS microdata — `data/raw/`, `data/interim/`, `data/processed/`, and the entire `outputs/data_audit/` folder — are not included. These contain DHS respondent-level microdata governed by the DHS Program's own data-use terms, which do not permit redistribution; this package documents how that data was processed, not the data itself.

The 35 literature source PDFs (`sources/articles/`, `sources/reports/`, `sources/papers/`, `sources/books/`) are also not included, to avoid any question of redistributing copyrighted material to a third party. `sources/bibliography/bibliography_source_audit.csv` records the exact title, authors, year, publication, and (where verified) DOI or URL for every source, so a reader can independently obtain any of them.

Also excluded: the local Python environment (`.venv/`), editor and tool configuration (`.vscode/`, `.claude/`), the in-progress thesis manuscript (`writing/`), and a number of empty legacy scaffold folders that were superseded early in the project and are already documented as inactive in `README.md`.

## Verification

All 70 files copied into this package were checksummed against their source in the working project; all 70 matched exactly, and the sources were re-checksummed after the build to confirm the working project was not altered. A safety scan of the full package for restricted data types (`.dta`, `.sav`, `.sas7bdat`, `.parquet`, shapefiles, `.zip`, hidden or cache directories, raw DHS filenames, and row-level DHS columns such as `caseid`, `hv001`, `hv002`) found nothing.

## Notes

- This package does not include, and does not grant access to, any DHS microdata. Reproducing the pipeline requires your own DHS Program-authorized access to the same four surveys (Ethiopia 2024-25, Ghana 2022, Kenya 2022, Nigeria 2024).
- Three documents were written specifically for this package rather than copied from the working project: `docs/code_guide.md`, `outputs/final_audit/README_AUDIT.md`, and this manifest.
- No script in this package was run to build it, and no analytical result changed in assembling it — the pipeline and its results remain exactly as frozen in the working project.
