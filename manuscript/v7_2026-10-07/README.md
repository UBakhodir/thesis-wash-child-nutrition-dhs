# Manuscript source package v7 (2026-10-09) — evidence-based correction and consistency review

Supersedes `manuscript/v6_2026-10-07/` as the canonical manuscript source. v1 through v6 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate, sample, weight, control set, or reported coefficient changed.**

This pass responds to a direct evidence-based correction task: sixteen confirmed, substantive discrepancies between the manuscript's prose and the implemented code or primary literature sources, each investigated directly (not assumed) and corrected — full detail in `CORRECTION_LOG.md` and `docs/provenance/evidence_based_correction_v1_2026-10-09.md`. Highlights: the baseline sample's weight and cluster-identifier fields were wrongly named using the historical extension's IPUMS field names; the baseline's child-age construction was wrongly described as having a country-varying fallback that belongs only to the historical extension; a region-FE identifying-variation claim and a notation collision were corrected in the empirical strategy chapter; the historical spatial-geometry and exposure-window-completion descriptions were found to overstate what the code actually guarantees and were corrected with the project's own measured validation numbers; the SHINE trial's arm structure was found to be materially different from the two WASH-Benefits trials and had been described identically; a citation (Blom2022) was found to have no local PDF despite an earlier false claim of having been read in full; and four cross-reference errors (historical content pointing to baseline sections) were found and fixed.

## What this pass did

1. Investigated and corrected 16 confirmed issues spanning data-chapter variable accuracy, econometric description precision, historical-exposure construction claims, literature-source accuracy, results-chapter disclosure, and documentation synchronization (`CORRECTION_LOG.md`).
2. Re-verified bibliography integrity after editing `bibliography.bib`'s note fields (26 entries, 20 cited, 0 missing keys, balanced braces).
3. Independently re-queried the stored coefficients CSV to verify a new numeric claim before publishing it (six, not five, of the 24 primary cells are nominally significant at *p* < .05) — catching and correcting an error in this same pass's own first draft.
4. Synchronized two previously-unaddressed provenance files (`docs/provenance/final_empirical_package_v3_2026-10-07/01_final_reporting_map.md`, `02_core_reporting_table.md`) that still carried stale validation-status labels and the same unsupported multiplicity language already removed from the manuscript chapters in v6.

## Canonical files and reading order

Unchanged from v6: `08_abstract.md` (read first, written last), `01_introduction.md` through `07_conclusion.md`, three appendices (Appendix A now split into separate baseline/historical variable-definition blocks), `bibliography.bib` (26 entries; 20 cited — see `citation_map.md`).

## Build

**No PDF was generated, rebuilt, or rendered in this pass**, per this task's explicit boundary. The existing `../v6_2026-10-07/build/main.pdf` reflects v6's content only and does not include this pass's prose corrections; it should not be cited as this version's build. A v7 build, with a freshly verified page count and a freshly rendered-page check, remains an explicit PDF-stage task (see `MASTER_ASSEMBLY.md`).

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this pass's investigation could establish — every claim checked against its underlying code, primary source, or authoritative output file, not merely checked for internal textual consistency.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; Blom2022's local PDF should be obtained before its citation can be upgraded to this thesis's normal verification standard; a full prose quality-review pass should be run once more before a submission build.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v6 remain superseded, plus `manuscript/v6_2026-10-07/` itself for the sixteen items in `CORRECTION_LOG.md`.
