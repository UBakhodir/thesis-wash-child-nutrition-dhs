# Master assembly specification — WASH and Child Nutrition thesis, manuscript v1 (2026-10-07)

This is the canonical assembly order for the full thesis. A future generator (human or automated) producing a complete document should concatenate the files below, in this order, with no other chapter-prose source used.

## Canonical reading / assembly order

| Order | File | Status |
|---|---|---|
| — | `08_abstract.md` | Complete (placed first in the assembled document, written last in drafting order) |
| 1 | `01_introduction.md` | Complete |
| 2 | `02_literature_review.md` | Complete |
| 3 | `03_data_and_variables.md` | Complete |
| 4 | `04_empirical_strategy.md` | Complete |
| 5 | `05_results.md` | Complete |
| 6 | `06_discussion_and_limitations.md` | Complete |
| 7 | `07_conclusion.md` | Complete |
| App. A | `appendices/A_variable_definitions_and_sample_flow.md` | Complete |
| App. B | `appendices/B_model_specifications_and_independent_verification.md` | Complete |
| App. C | `appendices/C_historical_diagnostics_and_ethiopia.md` | Complete |
| — | `bibliography.bib` | Complete (24 entries; see `bibliography_verification_ledger.md` for the full verification record) |

## What is not yet in this package

- Front matter: title page, declaration of authorship, acknowledgements, submission date. **Not fabricated anywhere in this package.** See `AUTHOR_CHECKLIST.md`.
- Tables/figures as typeset objects: all numerical content is in the chapter text and appendices as Markdown tables; converting these to LaTeX `table`/`figure` environments or Word tables is a formatting step for the generator, not a content step.
- A formal word count per university regulations (not located locally; see `AUTHOR_CHECKLIST.md`).

## How a later generator should assemble the full document

1. Concatenate the files in the order above, converting each Markdown chapter to the target format (LaTeX chapter files or Word sections). The Markdown is structured with `#`/`##` headings that map directly to chapter/section/subsection levels.
2. Pull every citation key referenced in the chapter text from `bibliography.bib`; do not introduce a citation not already present in the chapter text or `claim_evidence_ledger.md`.
3. Do not alter any numerical claim during formatting. If a number appears to need correction, stop and re-derive it from the authoritative file listed in `claim_evidence_ledger.md` — do not silently adjust it to "read better."
4. Insert front matter from a separately supplied, author-approved source (see `AUTHOR_CHECKLIST.md`); do not generate declaration, acknowledgement, or submission-date text.
5. Do not add new substantive claims, literature citations, or results not already present in this package without repeating the verification steps in `bibliography_verification_ledger.md` and `claim_evidence_ledger.md`.

## Superseded files — do not use

- Any file under `outputs/supervisor_development/18`–`26` (introduction and roadmap drafts). These predate the v3 empirical package and this manuscript, contain stale p-values and an incorrect age-heterogeneity count (corrected in `docs/provenance/baseline_evidence_reconciliation_v1_2026-10-07.md`), and are not editable manuscript sources for this package.
- `writing/thesis.tex` (master folder, outside this repository) — an empty 223-byte shell, not a source.
- `thesis/chapters/` (master folder, outside this repository) — empty placeholder directories (`.gitkeep` only).
- `thesis_design_FOR_REVIEW.md` and `docs/thesis_design.md` — design documents, useful as background, not chapter sources; this manuscript package supersedes them as the editable chapter source.
- `docs/provenance/final_empirical_package_v1_2026-10-07/` and `v2_2026-10-07/` for any numeric claim — superseded by `v3_2026-10-07/` (see those folders' own pointer banners).

## Empirical package used

`docs/provenance/final_empirical_package_v3_2026-10-07/` at commit `1690d99` (branch `main`), extended by this manuscript-preparation pass's own independent verification (`scripts/historical_wash/20_validate_pooled_estimate.py`, Appendix B).
