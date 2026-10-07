# Manuscript source package v1 (2026-10-07)

Developed chapter sources for the thesis *"The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa: Evidence from DHS and Geospatial Data"* (registered title, unchanged — see `01_introduction.md` §1.8 for a suggested, not adopted, alternative). This package is the **canonical, current manuscript source**. It does not replace or overwrite any earlier manuscript material (Section "Superseded files" below); it is a new version.

## What this is

Substantive, developed academic prose for all required thesis chapters, built directly from the validated empirical package at `docs/provenance/final_empirical_package_v3_2026-10-07/` (commit `1690d99`), with every numerical claim traced to its source file in `claim_evidence_ledger.md` and every citation verified in `bibliography_verification_ledger.md`. **No PDF is compiled from this package** — that is a separate, later task.

## Canonical files and reading order

See `MASTER_ASSEMBLY.md` for the full, authoritative assembly specification. In brief:

```
08_abstract.md                 (read first in the assembled document; written last)
01_introduction.md
02_literature_review.md
03_data_and_variables.md
04_empirical_strategy.md
05_results.md
06_discussion_and_limitations.md
07_conclusion.md
appendices/A_variable_definitions_and_sample_flow.md
appendices/B_model_specifications_and_independent_verification.md
appendices/C_historical_diagnostics_and_ethiopia.md
bibliography.bib
```

## Bibliography

`bibliography.bib` — machine-readable BibTeX, 24 entries (every source cited in the chapter text, plus a small reserve of verified-but-uncited sources). Full verification record, including sources deliberately excluded and why, in `bibliography_verification_ledger.md`. The complete 35-source audit this bibliography draws from is `sources/bibliography/bibliography_source_audit.csv`.

## Authoritative tables and figures

Every table in the chapter text is reused directly from the stored, validated output files indexed in `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and `02_core_reporting_table.md`. No table in this manuscript package was computed for the manuscript itself; `claim_evidence_ledger.md` traces each one. No figures have been generated yet — a future pass should render figures from the same authoritative CSVs listed in the ledger, not from numbers re-typed by hand.

## Empirical package and commit used

`docs/provenance/final_empirical_package_v3_2026-10-07/`, as of commit `1690d99` on `main`. This manuscript-preparation pass additionally ran one new independent-verification script (`scripts/historical_wash/20_validate_pooled_estimate.py` was already present from the prior closure milestone; its output is cited in Appendix B) — no new estimation was performed for the manuscript itself.

## Known limitations and remaining author inputs

See `AUTHOR_CHECKLIST.md` for the full list (university formatting requirements, title page, declaration, submission date, citation-style confirmation, and three open content decisions for author review). None of these is fabricated or silently assumed anywhere in the chapter text.

## Formatting requirements still needed

Not located locally in any prior session: university margin/font/line-spacing requirements, required front-matter order, and any department-specific citation-style mandate. `bibliography_verification_ledger.md` records that author–year style was used as a default in the absence of a located requirement.

## How a later whole-document generator should assemble this

Follow `MASTER_ASSEMBLY.md` step by step. In short: concatenate the canonical files in order, convert Markdown headings to the target format's chapter/section structure, pull citations only from `bibliography.bib`, do not alter any number without re-deriving it from `claim_evidence_ledger.md`'s source file, and insert front matter only from material the author separately supplies (never generate declaration/acknowledgement/submission-date text).

## Files that must not be used as manuscript sources (superseded or non-editable)

- `outputs/supervisor_development/18`–`26` (prior introduction/roadmap drafts; contain stale, corrected p-values and an incorrect age-heterogeneity count)
- `writing/thesis.tex` (master folder, outside this repository; empty shell)
- `thesis/chapters/` (master folder, outside this repository; empty placeholders)
- `docs/provenance/final_empirical_package_v1_2026-10-07/` and `v2_2026-10-07/` for any numeric claim (superseded by `v3`; each has its own pointer banner)

Full detail and reasoning for each: `MASTER_ASSEMBLY.md`.

## What this package is not

It is not a readiness audit (two of those already exist, outside this repository, in `audit_reports/`). It is not a PDF or a compiled document. It does not include front matter, and it does not include an AI-use disclosure of any kind (see `AUTHOR_CHECKLIST.md`).
