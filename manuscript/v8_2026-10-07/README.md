# Manuscript source package v8 (2026-10-09) — targeted correction of remaining v7 inconsistencies

Supersedes `manuscript/v7_2026-10-07/` as the canonical manuscript source. v1 through v7 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate, sample, weight, control set, or reported coefficient changed.**

This pass closes six specific issues identified in v7 itself — full detail in `CORRECTION_LOG.md` and `docs/provenance/evidence_based_correction_v2_2026-10-09.md`. Most significant: v7's own fix to the baseline age-construction claim (§3.2) was never propagated to §3.8, which still said the historical extension's age field matches the baseline's — directly contradicting the §3.2 fix; three further cross-references pointed historical content at the wrong sections; the long-standing "1.39 vs. 1.03" account is now resolved by a dedicated diagnostic rather than left hedged — it isolates the two simultaneous changes behind the original discrepancy and finds, decisively, that the age-in-months omission alone explains it, not the birth-year reference-coding change; `v005` is now described with its precise DHS definition (the woman's individual weight, not a household weight); and Blom2022's citation is upgraded from "no local PDF, web-search only" to a direct, abstract-level read of an accessible publisher-hosted working-paper version.

## What this pass did

1. Fixed a direct self-contradiction v7 left between §3.2 and §3.8 on how historical vs. baseline child age is constructed.
2. Corrected three further cross-reference errors (product definitions, birth-year-reference justification, wealth-inclusion justification), each verified by reading the destination section's actual content.
3. Built and ran a dedicated, targeted diagnostic (`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`) that isolates the birth-year-reference-coding change from the age-control omission using rank/column-space comparison and a four-way fit — resolving, rather than merely re-hedging, the 1.39-vs-1.03 account.
4. Corrected `v005`'s description to the precise DHS definition appropriate to the recode actually used (KR, not HR).
5. Removed two remaining instances of internal drafting/correction-process commentary from chapter prose.
6. Directly fetched and read an accessible primary-source abstract (AfDB Working Paper 315, via EconPapers/RePEc) to verify Blom2022's matching-method claim, rather than treating a missing local PDF as itself disqualifying.
7. Re-verified bibliography integrity and swept for stray cross-reference errors after all edits.

## Canonical files and reading order

Unchanged from v7: `08_abstract.md` (now without its drafting note), `01_introduction.md` through `07_conclusion.md`, three appendices, `bibliography.bib` (26 entries; 20 cited).

## Build

**No PDF was generated, rebuilt, or rendered in this pass**, consistent with v7's own boundary. The existing `../v6_2026-10-07/build/main.pdf` reflects neither v7's nor v8's prose corrections. A fresh build, with a freshly verified page count and rendered-page check, remains an explicit PDF-stage task.

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard both the v7 and v8 investigations could establish.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; a full prose quality-review pass should be run once more before a submission build.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v7 remain superseded, plus `manuscript/v7_2026-10-07/` itself for the six items in `CORRECTION_LOG.md`.
