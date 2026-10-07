# Manuscript source package v6 (2026-10-07) — PDF clipping fixed, inference discrepancy fully explained, unsupported multiplicity language corrected

Supersedes `manuscript/v5_2026-10-07/` as the canonical manuscript source. v1–v5 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate changed.**

This pass responds to a direct instruction to correct three concrete, verified problems found by inspecting commit `0090c16` and its committed v5 PDF — full detail in `CORRECTION_LOG.md` and `docs/provenance/independent_audit_v1_2026-10-07/09_update_2026-10-07_pass4.md`:

1. **Real PDF clipping**, confirmed by rendering pages to images and looking at them (not by warning counts or text extraction): the table converter (`build/md2tex.py`) used unbounded, non-wrapping columns for every table, which overflowed the page catastrophically for wide or long-celled tables (worst case: 1272pt ≈ 45cm off the right edge, Appendix A). Fixed with explicit wrapping column widths, sample sizes moved out of coefficient cells into a separate table, and breakable inline paths. Verified by rendering and inspecting the previously-clipped pages (and their neighbours) directly — see `build/README.md`.
2. **An unverified "numerical noise" explanation, corrected.** A prior pass attributed small SE/CI/p-value differences between the authoritative pipeline and an independent re-estimation to "two different, correct numerical implementations" without demonstrating this. The actual cause, read directly from the installed `linearmodels` 7.0 source and confirmed by a new reconciliation script, is a single missing keyword argument (`group_debias=True`) in the independent script's covariance configuration — not numerical noise. Adding it closes the gap to exactly 0.0 for all 24 primary historical cells. `appendices/B_model_specifications_and_independent_verification.md` §B.2 is corrected with the full derivation.
3. **Unsupported "unlikely to be a multiplicity artefact" language removed.** Independent computational reproduction of a coefficient establishes it is correctly computed; it does not establish anything about multiple-testing risk, and no multiplicity correction has been applied anywhere in this thesis. Corrected in `05_results.md` §5.6 and `06_discussion_and_limitations.md` §6.1.

## Canonical files and reading order

Unchanged from v5: `08_abstract.md` (read first, written last), `01_introduction.md` through `07_conclusion.md`, three appendices, `bibliography.bib` (26 entries; 20 cited). Full specification: `MASTER_ASSEMBLY.md`.

## Build

`build/` contains a complete, reproducible LaTeX build (xelatex + biblatex/biber). See `build/README.md` for the reproducible command sequence, the fix detail, the rendered-page verification performed, and the verified page-count breakdown (main text now 32 pages, within the 40-page limit). **This PDF is a diagnostic draft, not the final submission PDF.**

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Draft-build readiness vs. submission readiness

**Ready for a complete draft build**: yes, demonstrated by the actual compiling, visually-verified PDF in `build/`, within the page limit.
**Not ready for submission**: exact submission date and handwritten signature are not yet available (by design); a remaining typographic issue (Markdown numbered/bulleted lists rendering as inline prose rather than a formatted list — cosmetic, nothing lost, see `build/README.md`) should be cleaned up before a submission build; a full prose quality-review pass should be run once more. No claim of supervisor approval or university acceptance is made anywhere in this package.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v5 remain superseded, plus `manuscript/v5_2026-10-07/` itself for the items in `CORRECTION_LOG.md`.
