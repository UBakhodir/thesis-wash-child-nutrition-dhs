# Manuscript source package v3 (2026-10-07) — final targeted corrections + university-compliant build

Supersedes `manuscript/v2_2026-10-07/` as the canonical manuscript source. v1 and v2 are preserved unchanged; see `../v2_2026-10-07/POINTER_TO_V3.md` and `../v1_2026-10-07/POINTER_TO_V2.md`. This is the **single current entry point** — do not treat v1 or v2 as an alternative authority for anything corrected here (full list: `CORRECTION_LOG.md`). **No empirical estimate changed.**

## What this pass did

1. Corrected five identified problems (spatial-assignment wording, randomised-trial precision, an introduction/contribution overclaim, inconsistent bibliography counts, and two missed plain-text citations) — full itemised log in `CORRECTION_LOG.md`.
2. Produced a genuine, compiling diagnostic PDF build under the University of Bonn Economics Department's exact formatting specification (`build/`), with a **verified** main-text page count of **31 pages** (limit: 40) — not an estimate.
3. Confirmed the registered title, supervisor, submission deadline, author name, and matriculation number from the author's registration confirmation email, used in the diagnostic build's title page; recorded the still-unknown items (exact submission date, signature) as blanks, not inventions (`AUTHOR_CHECKLIST.md`).

## Canonical files and reading order

Unchanged from v2: `08_abstract.md` (read first, written last), `01_introduction.md` through `07_conclusion.md`, three appendices, `bibliography.bib` (26 entries; 20 cited — see `citation_map.md` and `CORRECTION_LOG.md` §D for the corrected, reproducible count). Full specification: `MASTER_ASSEMBLY.md`.

## Build

`build/` contains a complete, reproducible LaTeX build (xelatex + biblatex/biber, since pandoc is not installed in this environment) implementing the university's formatting specification exactly. See `build/README.md` for the reproducible command sequence, the verified page-count breakdown, and known cosmetic issues (not blockers) left for a final build pass. **This PDF is a diagnostic draft, not the final submission PDF, and is not represented as one anywhere in this package.**

## Supervisor-feedback status — unchanged, still accurate

Unchanged from v2: the introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Draft-build readiness vs. submission readiness

**Ready for a complete draft build**: yes, demonstrated by the actual compiling PDF in `build/`, within the page limit.
**Not ready for submission**: exact submission date and handwritten signature are not yet available (by design — they cannot be filled in before the thesis is actually finished and printed); the 38 cosmetic overfull-text-box warnings should be cleaned up; a full prose quality-review pass (noted in `AUTHOR_CHECKLIST.md`) should be run once more before a submission build. No claim of supervisor approval or university acceptance is made anywhere in this package.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1 and v2 (see those packages' own README/MASTER_ASSEMBLY files) remain superseded, plus `manuscript/v2_2026-10-07/` itself for the five items in `CORRECTION_LOG.md`.
