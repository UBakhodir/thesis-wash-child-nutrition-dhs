# Manuscript source package v13 (2026-10-17) — final assembly

Supersedes `manuscript/v12_2026-10-10/` as the canonical manuscript source. v1 through v12 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**.

This version is the final-assembly pass, produced in the local VS Code environment. It merges v12's canonical text with the accumulated, verified language editing from eleven separate per-chapter publishing sessions (`publishing/thesis_render_v12/chapters/md/`, each individually reviewed and tracked in that package's own `FINAL_ASSEMBLY_REGISTER.md`), applies every register item still marked "required; not applied" at the start of this pass, resolves four author-decision items, performs three restricted-data local checks the register had left open, and reconciles the bibliography against Crossref and DHS Program records. Full itemised list: `CORRECTION_LOG.md`.

## What changed

Fourteen required wording/methods-description corrections (Chapters 2–6, the abstract, Appendix B, Appendix C) and four author-decision alignments (Chapter 3 twice, Chapter 4, Chapter 5) — see `CORRECTION_LOG.md` for the exact before/after text of each. None of these fourteen or four items changes a reported coefficient, standard error, confidence interval, p-value, sample, weight, or control set; every one is a prose, cross-reference, or methods-description precision fix.

**Three restricted-data local checks, all confirmatory.** The register had left open whether the community-exposure cluster key corresponds one-to-one with the clustering/fixed-effect key in every baseline country, whether an undocumented baseline cross-validation call explains a small residual SE gap, and whether Appendix C's exact Ethiopian eligibility counts match the restricted data. All three were checked directly against the actual restricted files in this pass: all three confirmed the manuscript's existing statements with no error found, and none required a correction. Detail in `CORRECTION_LOG.md` and, for the PanelOLS check, a new addendum in Appendix B §B.1.

**Bibliography**: the publishing package's 21 verified field changes (title capitalisation to Chicago headline style for all 20 cited titles; added volume/issue/page locators for five entries) were applied, plus further corrections verified directly against Crossref and the DHS Program's own recommended citations in this pass: Black2013's author list completed to all eleven Crossref-confirmed authors (previously six names and "others"); deOnis2006's volume/issue corrected to the publisher's own record (volume 95, issue S450, not "supplement 450" read as a volume number); Burgert2013 and PerezHeydrich2013's institution corrected to "ICF International" and Donohue2023's to "ICF", matching each report's own era-appropriate recommended citation. Two software citations (`statsmodels`, `linearmodels`) were added and cited in text. DHS/IPUMS-DHS/IHME *dataset* citations were considered and not added, because no extract version is recorded anywhere in this repository and inventing one would violate this project's own evidentiary standard; this is recorded as an open item for the author.

## Canonical files and reading order

Unchanged from v12 except `01_introduction.md`, `02_literature_review.md`, `03_data_and_variables.md`, `04_empirical_strategy.md`, `05_results.md`, `06_discussion_and_limitations.md`, `07_conclusion.md`, `08_abstract.md`, `bibliography.bib`, `bibliography_verification_ledger.md`, `appendices/A_variable_definitions_and_sample_flow.md`, `appendices/B_model_specifications_and_independent_verification.md`, and `appendices/C_historical_diagnostics_and_ethiopia.md` (all corrected as above; see `CORRECTION_LOG.md` for the per-item detail). `MASTER_ASSEMBLY.md`, `AUTHOR_CHECKLIST.md`, `CROSS_REFERENCE_MAP.md` and `citation_map.md` are updated to describe this version.

## Build

A thesis PDF build was authorised and attempted from this version using `publishing/thesis_render_v13/` (copied and updated from `publishing/thesis_render_v12/`, which this version's text supersedes as a rendering source). See `publishing/thesis_render_v13/README.md` and its build reports for the current build status, page count, and any remaining defect.

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this and the prior passes could establish, including every item this pass's own register tracked as outstanding. This is not a claim that every conceivable error has been eliminated from a thesis of this scope.
**Not ready for submission**: the exact submission date and handwritten signature are not yet available, and no chapter has supervisor approval; see the thesis PDF build's own report for its remaining page-by-page and formatting status.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v12 remain superseded, plus `manuscript/v12_2026-10-10/` itself for the items in `CORRECTION_LOG.md`.
