# Final small reference cleanup and source handover (2026-10-09)

Starting commit: `1892a39` (confirmed `HEAD == origin/main`, clean except the standing untracked `outputs/supervisor_meeting/`). Canonical manuscript: `manuscript/v10_2026-10-07/`. No literature audit was restarted, no model was rerun, and no PDF was generated, compiled, rebuilt, or rendered.

This is a small, targeted finish to `_v1`/`_v2`'s bibliographic cleanup, not a new audit.

## 1. Two remaining printable audit notes removed

Removed from `bibliography.bib`:
- `Momberg2021`: the note "Author initials as given by Crossref/the publisher record; expanded given names could not be substantiated..." Removed; the verified initials themselves (`D. J. Momberg`, etc., set in the `_v2` pass) are unchanged in the `author` field.
- `PerezHeydrich2013`: the note describing the accent investigation and residual uncertainty. Removed; the spelling itself ("Perez-Heydrich," unaccented, matching the source PDF's own byline, set in the `_v2` pass) is unchanged.

Both explanations remain fully recorded in `bibliography_verification_ledger.md` (rows for `Momberg2021` and `PerezHeydrich2013`), each updated this pass to note that the corresponding `.bib` note was removed and that the ledger is now the sole location for the explanation.

**All remaining note fields re-inspected** (`deOnis2006`, `GerusoSpears2015`, `Croft2023`, `JMP2025`, `UNICEF2025`): confirmed to contain only scholarly content (publication-year ambiguity, working-paper-vs-published-version distinction, edition identity, absence-of-DOI explanation) — no internal audit commentary remains in any printable bibliography note.

## 2. WHO author label corrected

`citation_map.md` displayed "de Onis et al. (2006)" for the `deOnis2006` key, which no longer matches that entry's corrected `author` field (the collective "WHO Multicentre Growth Reference Study Group," corrected in `_v1`). Changed the displayed citation wording to "WHO Multicentre Growth Reference Study Group (2006)." The citation key `deOnis2006` itself was kept unchanged, per the task's own instruction that an internal key need not reproduce the displayed author name.

**Checked for the same mismatch elsewhere**: grepped the full manuscript package for "de Onis." The only other occurrences are genuine personal co-author "de Onis, Mercedes" entries on two *different* sources (`Victora2010`, `Black2013`), which are correct and unrelated to this issue. No chapter or appendix file narrates this author by name for the `deOnis2006` citation — all chapter-text occurrences use bracket-style `[@deOnis2006]` with no narrative author name (confirmed by the same grep returning no chapter/appendix hits), so no mismatch existed there and none was introduced. The supported growth-standard claim itself (WHO Child Growth Standards methods paper, BCPE method) was not changed.

## 3. Citation-map header corrected; one further contradictory pointer found and fixed

Replaced `citation_map.md`'s stale "(2026-10-07, v6; bibliographic metadata corrected 2026-10-09)" heading with "(manuscript v10_2026-10-07; this file last updated 2026-10-09)," matching the actual canonical manuscript version.

**Checked the immediate canonical documentation** (`MASTER_ASSEMBLY.md`, `README.md`) for contradictory version pointers. Found one: `MASTER_ASSEMBLY.md`'s own bibliography-status row still said "12 author-name/field corrections applied across 9 entries" — the same miscount (12 entries, not 9) that `bibliography_verification_ledger.md` had already corrected in the `_v2` pass but that this specific file had been missed for. Corrected to match: "12 entries received author-name and/or missing-field corrections," with pointers updated to include `_v2` and this file. `README.md` was checked and contains no citation-count or version-pointer language affected by this cleanup.

## 4. Targeted validation (re-run after all edits)

- Brace balance: 0 (balanced).
- Total entries: 26; unique keys: 26; duplicate keys: none.
- Cited keys: 20; missing from bibliography: none; uncited reserve: 6 (`Croft2023`, `Gebru2019`, `ICF2012`, `JMP2025`, `Momberg2021`, `UNICEF2025`) — unchanged from `_v1`/`_v2`, since no chapter text or citation structure was touched.
- `deOnis2006`'s `author` field confirmed still correct (institutional author only); `citation_map.md`'s displayed wording now matches it.
- `Momberg2021` and `PerezHeydrich2013` `.bib` entries confirmed to contain no `note` field (removed); both explanations confirmed present in `bibliography_verification_ledger.md`.
- `git diff --stat` against the starting commit touches exactly 4 files — `bibliography.bib`, `bibliography_verification_ledger.md`, `citation_map.md`, `MASTER_ASSEMBLY.md` — all in the reference package. No chapter file, appendix, script, or empirical output file was touched.
- `Blom2022`'s indirect-version-correspondence disclosure (set in `_v2`) was re-read and left unchanged: the published *JEEM* article's own text is still stated as not directly inspected, and secondary press coverage is still described only as evidence of correspondence between the working-paper and published versions, not as a primary read of the published article.

## 5. What this pass did not do

Did not re-verify any entry's fields against primary sources again. Did not change any chapter prose, claim, cross-reference, empirical estimate, sample, weight, or control set. Did not generate, compile, rebuild, or render any PDF. Did not begin the next-stage draft-PDF build or page-by-page review, which remains separately authorized and not started.

## Files changed this pass

`manuscript/v10_2026-10-07/bibliography.bib` (2 notes removed), `manuscript/v10_2026-10-07/bibliography_verification_ledger.md` (2 rows updated to reflect the note removal; still carry the full explanations), `manuscript/v10_2026-10-07/citation_map.md` (header corrected; `deOnis2006` row's displayed author corrected), `manuscript/v10_2026-10-07/MASTER_ASSEMBLY.md` (stale "9 entries" corrected to "12 entries"), this file.

## Canonical path

`manuscript/v10_2026-10-07/`, edited in place — no new manuscript version, consistent with `_v1`/`_v2` and this task's own instruction that these small fixes do not require one.
