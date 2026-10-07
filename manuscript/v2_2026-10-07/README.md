# Manuscript source package v2 (2026-10-07) — correction pass

Supersedes `manuscript/v1_2026-10-07/` as the canonical manuscript source. v1 is preserved unchanged; see `../v1_2026-10-07/POINTER_TO_V2.md`. This package applies a focused scholarly correction to v1: fixing an overstated exposure-timing comparison, several overgeneralized literature claims, converting to machine-readable citations, and moving administrative/title discussion out of chapter prose. **No empirical estimate changed.** See `CORRECTION_LOG.md` for the full, itemised list.

## What this is

The same developed, substantive chapter prose as v1, corrected for the issues above, built from the same validated empirical package (`docs/provenance/final_empirical_package_v3_2026-10-07/`, commit `1690d99`). Three central literature sources (Cumming et al. 2019, Headey and Palloni 2019, Geruso and Spears 2015) were re-read in full or substantial part during this pass specifically to verify the claims made about them — see `citation_map.md` for exactly what was checked and what was not. **No PDF is compiled from this package.**

## Canonical files and reading order

See `MASTER_ASSEMBLY.md` for the full specification. In brief: `08_abstract.md` (read first, written last), `01_introduction.md` through `07_conclusion.md`, three appendices, `bibliography.bib`.

## Citations

Machine-readable pandoc Markdown citation syntax (`[@key]` / `Author [-@key]`) throughout, resolved against `bibliography.bib`. `citation_map.md` gives, for every citation, the exact bibliographic key, which version of the source was used, and what passage supports the specific claim made. `MASTER_ASSEMBLY.md` documents the exact rendering workflow (pandoc + citeproc) a later generator should use.

## What changed from v1

See `CORRECTION_LOG.md` for the complete, itemised correction log. In summary: (1) the exposure-timing argument no longer implies the baseline-vs-historical comparison isolates a timing effect; (2) several overgeneralized literature claims are corrected with precise, source-grounded replacements, including a materially more accurate characterisation of Headey and Palloni's (2019) actual findings; (3) citations are now machine-readable; (4) the title-change discussion and other administrative commentary are removed from chapter prose and live only in `AUTHOR_CHECKLIST.md`; (5) supervisor-request status is corrected in a separate public-safe record (`docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`) to avoid overstating what has been sent to or received from the supervisor.

## Known limitations and remaining author inputs

See `AUTHOR_CHECKLIST.md`. Unchanged in substance from v1, with the title-change discussion now relocated there in full.

## Empirical package and commit used

`docs/provenance/final_empirical_package_v3_2026-10-07/`, unchanged from v1. No new estimation was performed in this pass.

## How a later whole-document generator should assemble this

Follow `MASTER_ASSEMBLY.md`, which now also specifies the citation-rendering workflow and gives `CROSS_REFERENCE_MAP.md` for resolving in-text section references.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items listed in v1's README remain superseded, plus `manuscript/v1_2026-10-07/` itself for any content corrected in `CORRECTION_LOG.md` (v1's empirical numbers and un-corrected sections remain accurate and may still be consulted, but v2 is the citable source).
