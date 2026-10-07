# Manuscript source package v5 (2026-10-07) — remaining literature verification closed

Supersedes `manuscript/v4_2026-10-07/` as the canonical manuscript source. v1–v4 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate changed.**

This pass responds to `docs/provenance/independent_audit_v1_2026-10-07/08_update_2026-10-07_pass3.md`: the remaining 11 of 20 cited literature sources (previously verified only at the bibliographic-identity level) were read directly against their specific claims. 10 of 11 were fully supported as cited; 1 (Addae et al. 2024) was found overstated and corrected — full detail in `CORRECTION_LOG.md`.

## What this pass did

1. Read all 11 remaining sources directly (Victora2008, Victora2010, Black2013, deOnis2006, Rakotomanana2020, Addae2024, Gunther2010, Spears2013, Burgert2013, PerezHeydrich2013, LBDWaSH2020) against the specific claims attributed to them in `02_literature_review.md` and elsewhere.
2. Corrected one overclaim: Addae et al. (2024)'s finding on household water was country/outcome-specific (associated with wasting, not stunting) and had been generalised in the manuscript to both outcomes. Corrected to state the result precisely — same pattern already caught once for Donohue et al. (2023) in v4.
3. Rebuilt the LaTeX PDF and re-verified the main-text page count under the identical university formatting specification (see `build/README.md` for the result).

All 20 of 20 cited sources now have claim-level verification (not merely bibliographic-identity verification). No other manuscript text changed in this pass.

## Canonical files and reading order

Unchanged from v4: `08_abstract.md` (read first, written last), `01_introduction.md` through `07_conclusion.md`, three appendices, `bibliography.bib` (26 entries; 20 cited — see `citation_map.md`). Full specification: `MASTER_ASSEMBLY.md`.

## Build

`build/` contains a complete, reproducible LaTeX build (xelatex + biblatex/biber). See `build/README.md` for the reproducible command sequence and the verified page-count breakdown. **This PDF is a diagnostic draft, not the final submission PDF, and is not represented as one anywhere in this package.**

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Draft-build readiness vs. submission readiness

**Ready for a complete draft build**: yes, demonstrated by the actual compiling PDF in `build/`, within the page limit.
**Not ready for submission**: exact submission date and handwritten signature are not yet available (by design); a full prose quality-review pass should be run once more before a submission build. No claim of supervisor approval or university acceptance is made anywhere in this package.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v4 (see those packages' own README/CORRECTION_LOG files) remain superseded, plus `manuscript/v4_2026-10-07/` itself for the one item corrected in this pass's `CORRECTION_LOG.md`.
