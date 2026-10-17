# Source manifest

## Academic source (read-only for this package)

Canonical manuscript: `manuscript/v12_2026-10-10/` at commit
`c58fc478e7b31789fc68e3c88cd25de4a6567c78` (= `origin/main` on 2026-10-13; the remote had not advanced
beyond the last reviewed commit `c58fc47`). The sha256 of every canonical input is recorded in
`source_manifest.tsv` (15 files: the 11 chapter/abstract/appendix Markdown files, `bibliography.bib`,
`CROSS_REFERENCE_MAP.md`, `citation_map.md`, `MASTER_ASSEMBLY.md`). Check with
`python scripts/build.py manifest` at the start of every chapter session; any change means the canonical
source moved and must be reviewed before previewing.

Supporting documents read for this package (not inputs to the build): repository `README.md`,
`manuscript/v12_2026-10-10/README.md`, `AUTHOR_CHECKLIST.md`, `CROSS_REFERENCE_MAP.md`,
`citation_map.md`, `MASTER_ASSEMBLY.md`, `05_results.md` (table structure),
`docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and
`01_final_reporting_map.md`.

Implementation references inspected, not reused as content: `manuscript/v6_2026-10-07/build/`
(`preamble.tex`, `titlepage.tex`, `declaration.tex`, `md2tex.py`, `README.md`). Title-page metadata and
declaration wording were carried over from there (see `REQUIREMENTS_CHECKLIST.md`, R-17/R-18). No
generated chapter text from v3–v6 was used.

Not used and not needed: restricted DHS/IPUMS/IHME data, coordinates, respondent identifiers.

## Files created by this package

| File | Role |
|---|---|
| `README.md` | Build instructions and commands |
| `HANDOVER.md` | Progress record for future sessions |
| `REQUIREMENTS_CHECKLIST.md` | Requirement-by-requirement evidence |
| `SOURCE_MANIFEST.md`, `source_manifest.tsv` | This file; canonical input hashes |
| `.gitignore` | Ignores `builds/*/work/` and generated diagnostic `.tex` |
| `template/thesis-preamble.tex` | Shared formatting |
| `template/metadata.tex`, `titlepage.tex`, `declaration.tex` | Front/back matter components |
| `filters/thesis.lua` | pandoc conversion filter |
| `scripts/build.py`, `scripts/pdfcheck.py` | Build orchestration; PDF measurement |
| `drivers/thesis-body.tex` | Master assembly order |
| `chapters/README.md`, `chapters/APPROVED.tsv`, `chapters/md/`, `chapters/tex/` | Chapter source locations (empty) |
| `diagnostics/template_verification.md`, `template_verification_appendix.md`, `diagnostic-cover.tex`, `component-titlepage.tex` | Diagnostic content only |
| `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` + `.report.md` | Current template-verification PDF (contents lists all four heading levels) and its build report |
| `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf` + `.report.md` | First template-verification PDF (kept; its contents page omitted levels 3–4) |
| `builds/selftest/SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` + `.report.md` | Preview pipeline run on diagnostic text |

## Files added in the Chapter 1 session (2026-10-13)

The academic source is unchanged: `c58fc478…`, and `build.py manifest` reports 15/15 inputs unchanged.

| File | Role |
|---|---|
| `chapters/md/01_introduction.md`, `chapters/md/PROVENANCE.tsv` | Language-edited publishing copy of the introduction; provenance of the copy |
| `chapters/tex/01_introduction.tex` | Reusable chapter LaTeX generated from the publishing copy (no preview reference list inside) |
| `chapters/changes/01_introduction.changelog.md`, `01_introduction.worddiff.txt` | Edit record against canonical |
| `builds/previews/REVIEW-COPY_ch01-introduction_preview_*.pdf` + `.report.md` + `.verification.md` | Introduction preview, build report and verification report |
| `template/thesis-preamble.tex` (changed) | `bibintoc` heading now sets its own hyperlink anchor |
| `scripts/build.py` (changed) | Preview reference list titled "References cited in this chapter --- preview only" and given a PDF bookmark |

## Files added in the Chapter 2 session (2026-10-14)

The academic source is unchanged: `c58fc478…` (remote `main` re-checked), and `build.py manifest`
reports 15/15 inputs unchanged. Additional canonical documents read (not build inputs):
`bibliography_verification_ledger.md`, `claim_evidence_ledger.md`, the R14/R15 entries of
`docs/provenance/independent_audit_resolution_v1_2026-10-10.md`, and `05_results.md` §5.2.

| File | Role |
|---|---|
| `chapters/md/02_literature_review.md`, `chapters/md/PROVENANCE.tsv` (row added) | Language-edited publishing copy of the literature review; provenance of the copy |
| `chapters/tex/02_literature_review.tex` | Reusable chapter LaTeX generated from the publishing copy (no preview reference list inside) |
| `chapters/changes/02_literature_review.changelog.md`, `02_literature_review.worddiff.txt` | Edit record against canonical |
| `builds/previews/REVIEW-COPY_ch02-literature-review_preview_*.pdf` + `.report.md` + `.verification.md` | Literature-review preview, build report and verification report |
| `chapters/APPROVED.tsv` (row added) | Author's carry-forward decision for `ch01`, recorded on the author's instruction |
| `scripts/build.py` (changed) | `prepare` records the canonical manuscript's last commit as `source_commit` (not HEAD) |

## Files added in the Chapter 3 session (2026-10-14)

The academic source is unchanged: `c58fc478…` (remote `main` re-checked), and `build.py manifest`
reports 15/15 inputs unchanged. Additional repository material read (not build inputs):
- `docs/data_dictionary.md`, canonical Appendix A, `04_empirical_strategy.md` (§4.3, §4.5, §4.6), `05_results.md` (§5.8, Table 5.9), `06_discussion_and_limitations.md` §6.4, `01_introduction.md` §1.2, and Appendix C;
- `scripts/dhs_harmonization/02, 04, 05, 08, 14`; `scripts/historical_wash/10, 12` (headers and the lines cited in the change log);
- the provenance notes `historical_wash_ihme_product_definitions_v1`, `historical_wash_spatial_extraction`, `historical_wash_spatial_geometry_addendum`, `historical_wash_weights_and_measurement`, `historical_wash_decisions`, `historical_wash_issue_register_v1`, `evidence_based_correction_v1`, `historical_wash_exposure_validation/selftest_temporal_and_geometry_AGGREGATE.json`, and the preliminary model register.

No restricted data was read.

| File | Role |
|---|---|
| `chapters/md/03_data_and_variables.md`, `chapters/md/PROVENANCE.tsv` (row added) | Language-edited publishing copy of Chapter 3; provenance of the copy |
| `chapters/tex/03_data_and_variables.tex` | Reusable chapter LaTeX generated from the publishing copy (no preview reference list inside) |
| `chapters/changes/03_data_and_variables.changelog.md`, `03_data_and_variables.worddiff.txt` | Edit record against canonical, including author-review points A1–A5 |
| `builds/previews/REVIEW-COPY_ch03-data-and-variables_preview_*.pdf` + `.report.md` + `.verification.md` | Chapter 3 preview, build report and verification report |
| `FINAL_ASSEMBLY_REGISTER.md` | Deferred corrections and final-assembly tasks (Chapter 2 §2.4 correction FA-1, bibliography, template, pagination) |

No shared template, filter, script or driver file changed in this session.

## Files added in the Chapter 6 session (2026-10-14)

(The Chapter 4 and Chapter 5 sessions recorded their files in `HANDOVER.md` §14–§15 rather than here.)

The academic source is unchanged: `c58fc478…` (remote `main` re-checked), and `build.py manifest`
reports 15/15 inputs unchanged. Additional repository material read (not build inputs): the Chapter 1–5
publishing copies; canonical Appendices A–C; `claim_evidence_ledger.md`, `citation_map.md`,
`bibliography_verification_ledger.md`; `final_empirical_package_v3_2026-10-07/01_final_reporting_map.md`
and `02_core_reporting_table.md`; `historical_wash_issue_register_v1_2026-10-07.md`,
`historical_wash_exposure_construction_spec_v1_2026-10-06.md`,
`historical_wash_analysis_specification_v1_2026-10-06.md`; stored outputs
`outputs/household_community_wash/02_…`, `03_…`, `05_…`, `outputs/regressions/main_continuous_models.csv`,
`historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` and
`window_common_sample_PRELIMINARY_AGGREGATE.csv`. No restricted data was read.

| File | Role |
|---|---|
| `chapters/md/06_discussion_and_limitations.md`, `chapters/md/PROVENANCE.tsv` (row added) | Language-edited and verified publishing copy of Chapter 6; provenance of the copy |
| `chapters/tex/06_discussion_and_limitations.tex` | Reusable chapter LaTeX generated from the publishing copy (no preview reference list inside) |
| `chapters/changes/06_discussion_and_limitations.changelog.md`, `06_discussion_and_limitations.worddiff.txt` | Edit record against canonical: corrections A1–A10, clarifications B1–B13, author points F1–F6 |
| `builds/previews/REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` + `.report.md` + `.verification.md` + `.checks/` | Chapter 6 preview, build report, verification report, check scripts and logs |
| `FINAL_ASSEMBLY_REGISTER.md` (updated) | FA-12, FA-13 (required), FA-14, FA-3 item, open-item summary |

No shared template, filter, script or driver file changed in this session.

## Files added in the abstract session (2026-10-14)

(The Chapter 7 session recorded its files in `HANDOVER.md` §17.) The academic source is unchanged: `c58fc478…`
(remote `main` re-checked), and `build.py manifest` reports 15/15 inputs unchanged. Additional repository material read
(not build inputs): the Chapter 1–7 publishing copies; `claim_evidence_ledger.md`, `citation_map.md`, `MASTER_ASSEMBLY.md`,
`CORRECTION_LOG.md`; `final_empirical_package_v3_2026-10-07/00_results_index.md`, `01_final_reporting_map.md`,
`02_core_reporting_table.md`; canonical Appendix B; `independent_audit_v1_2026-10-07/07_update_2026-10-07_pass2.md` and
`09_update_2026-10-07_pass4.md`; stored outputs `outputs/household_community_wash/03_household_cluster_fe.csv`,
`outputs/regressions/main_continuous_models.csv`, `historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`
and `independent_validation_*`. No restricted data was read.

| File | Role |
|---|---|
| `chapters/md/08_abstract.md`, `chapters/md/PROVENANCE.tsv` (row added) | Verified and language-edited publishing copy of the abstract; provenance of the copy |
| `chapters/tex/08_abstract.tex` | Reusable abstract LaTeX generated from the publishing copy (no preview reference page inside) |
| `chapters/changes/08_abstract.changelog.md`, `08_abstract.worddiff.txt` | Edit record against canonical: corrections A1–A5, clarifications B1–B15, author points F1–F6 |
| `builds/previews/REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` + `.report.md` + `.verification.md` + `.checks/` | Abstract preview, build report, verification report, check scripts and logs |
| `scripts/build.py` (changed) | Preview-only reference page titled "…the abstract…" for the abstract unit; chapter units unchanged |
| `FINAL_ASSEMBLY_REGISTER.md` (updated) | FA-17 (abstract), FA-18 (template text layer), FA-16 F4 note, summary table |

## Consolidated-references session (2026-10-17)

Inputs read (not edited): the eleven `chapters/md` and `chapters/tex` units; `manuscript/v12_2026-10-10/bibliography.bib`,
`bibliography_verification_ledger.md`, `citation_map.md`, `CORRECTION_LOG.md`; `sources/bibliography/bibliography_source_audit.csv`;
`docs/provenance/bibliographic_citation_audit_v1/v2/v3_2026-10-09.md`, `independent_audit_resolution_v1_2026-10-10.md`;
`historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` (row `m0032`, FA-25 C). No restricted data was read.

| File | Role |
|---|---|
| `bibliography/bibliography.bib` (new) | Publishing copy of the canonical bibliography; read by every build |
| `bibliography/field_changes.tsv`, `bibliography/REFERENCES_VERIFICATION.md` (new) | Each field change with old/new value and evidence; verification and change report |
| `scripts/build.py` (changed) | Reads the publishing copy; `manifest` keeps the canonical file; new `references` command |
| `template/thesis-preamble.tex` (changed) | Inside the bibliography only: URL breaks after "/" and ragged-right entries |
| `builds/previews/REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf` + `.report.md` + `.checks/` | Consolidated references review copy, build report, checks |
| `FINAL_ASSEMBLY_REGISTER.md`, `HANDOVER.md`, `README.md`, `REQUIREMENTS_CHECKLIST.md` (updated) | FA-3/FA-4 status, FA-24, FA-25; session log §22 |

