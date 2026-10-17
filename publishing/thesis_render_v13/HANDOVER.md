# Handover — thesis rendering package (Task 1: template set-up)

Read this file first in every later chat. Status as of 2026-10-17, **updated after the consolidated-references session, §22** (Appendix C session: §21) (Appendix B session: §20) (Appendix A session: §19) (abstract session: §18) (Chapter 7
(conclusion) session: §17) (Chapter 6 session: §16; Chapter 5 session: §15; Chapter 4 session: §14; Chapter 3 session: §13; Chapter 2 session: §12; Chapter 1 session: §11).
Deferred corrections and final-assembly tasks are collected in **`FINAL_ASSEMBLY_REGISTER.md`**. Earlier set-up status: revised after the contents-depth
correction, commit `020f721`.

## 1. Where things are

| Item | Value |
|---|---|
| Repository | https://github.com/UBakhodir/thesis-wash-child-nutrition-dhs |
| Working branch | Set-up: `claude/busy-ramanujan-u6qrs8`. Each later session used its own isolated branch (§11–§21); the latest is `claude/sharp-brown-y9zp92` (Appendix C session, §21). Nothing has been pushed to `main`. |
| Source commit (canonical manuscript) | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` — equal to `origin/main` when this session started; the remote had not advanced past the last reviewed commit `c58fc47` |
| Package commits | `4b3055a6df2983295cc35f52af5ac5c91a0f83db` adds `publishing/thesis_render_v12/`; `143810cc75640afd832cc87d5c468d2e652d5170` records that commit here; `020f721` sets the contents depth to 4 (template change only); the following commit adds the revised diagnostic and these documentation updates |
| Canonical manuscript | `manuscript/v12_2026-10-10/` (confirmed by the root README, the v12 README and `MASTER_ASSEMBLY.md`; v1–v11 and the v3–v6 builds are superseded and untouched) |
| Publishing directory | `publishing/thesis_render_v12/` |
| Template-verification PDF (current) | `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` (13 pages, sha256 `e69acceb…5f879`) + `.report.md` |
| Earlier diagnostic (kept, superseded) | `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf` (sha256 `bb75aeee…3637c`); its contents page omitted levels 3–4 |

## 2. Status

- **Chapter 1 (introduction): carried forward by the author after review** (recorded 2026-10-14 in
  `chapters/APPROVED.tsv` on the author's instruction; not supervisor or final-submission approval;
  its open points in §11 remain). Its files are unchanged since the Chapter 1 session.
- **Chapter 2 (literature review): reviewed by the author, with a required correction pending.** Not
  finalised, not unconditionally approved, and not in `APPROVED.tsv`. The author chose to continue
  rendering and to apply the §2.4 correction **at final assembly**. The exact text is in
  `FINAL_ASSEMBLY_REGISTER.md` FA-1 and §13 below. It was not applied, and Chapter 2 was not rebuilt.
- **Chapter 3 (data and variables): awaiting author review, with a required cross-reference
  correction pending at final assembly** (`FINAL_ASSEMBLY_REGISTER.md` FA-7 A) and an open local
  verification question (`hv001`/`v001` vs. `v021`, FA-7 B; not resolved). Not finalised; not in
  `APPROVED.tsv`. Its files were not edited or rebuilt in the Chapter 4 session.
- **Chapter 4 (empirical strategy): awaiting author review, with four required corrections
  pending at final assembly** (`FINAL_ASSEMBLY_REGISTER.md` FA-8, reclassified as required on the
  author's instruction in the Chapter 5 session; exact targets checked). Not applied; Chapter 4
  was not edited or rebuilt. Not in `APPROVED.tsv`. *Chapter 6 session:* a fifth required
  correction was recorded (FA-12, the §4.5 "every pooled coefficient" sentence); not applied.
- **Chapter 5 (results): language-edited and verified publishing copy and review-copy preview,
  awaiting author review** (§15). Three verified corrections applied in the copy, clarifications
  and layout changes to confirm, decisions E1–E7 (FA-9). Not in `APPROVED.tsv`. *Chapter 6
  session:* the §5.4 correction must be synchronised with the canonical chapter at final assembly
  (FA-13, required); E2 is superseded by FA-12.
- **Chapter 6 (discussion and limitations): language-edited and verified publishing copy and
  review-copy preview, awaiting author review** (§16). Ten verified corrections applied in the copy
  (A1–A10), clarifications B1–B13 and decisions F1–F6 for the author (FA-14). Not in `APPROVED.tsv`.
- **New required final-assembly items (Chapter 6 session):** FA-12 (narrow the Chapter 4 §4.5
  "every pooled coefficient" sentence to what Chapter 5 actually presents) and FA-13 (synchronise
  Chapter 5's "more than doubles" correction between the publishing copy and the canonical chapter).
- **Chapter 7 (conclusion): language-edited and verified publishing copy and review-copy preview,
  Awaiting author review** (§17). Eight verified corrections applied in the copy (A1–A8),
  clarifications B1–B12 and decisions F1–F6 for the author (FA-16). Not in `APPROVED.tsv`.
- **New items recorded in the Chapter 7 session:** FA-15 A (required Chapter 6 §6.5 wording
  correction, exact text), FA-15 B (evidence check of "before any model was estimated" against dated
  design records), FA-15 C (Chapter 6 discussion completeness). None applied.
- **Abstract (unnumbered `abstract` unit; not a chapter): verified and language-edited publishing copy and
  review-copy preview, Awaiting author review** (§18). Five verified corrections in the copy (A1–A5, including the
  three FA-16 F4 flags), clarifications B1–B15 and decisions F1–F6 (FA-17). Not in `APPROVED.tsv`; canonical
  `08_abstract.md` unchanged. New template item FA-18 (";" extracted as U+037E in every PDF's text layer).
- **Appendix A (`appA`; numbered Appendix A, not a chapter): verified and language-edited publishing copy and review-copy preview, Awaiting author review** (§19). Six verified definition/source corrections in the copy (A1–A6), clarifications B1–B13, captions Table A.1–A.3 added to the three existing tables, decisions G1–G7 (FA-19). Shared filter and build-script changes (FA-20). Three abstract review items recorded, not applied (FA-21). Not in `APPROVED.tsv`; canonical appendix unchanged. FA-7 B remains unresolved.
- **Appendix B (`appB`; numbered Appendix B, not a chapter): verified and language-edited publishing copy and review-copy preview, Awaiting author review** (§20). Eight verified corrections in the copy (A1–A8: script 17 agreement scope, the 6.7×10⁻⁸ rounding artefact and the stored unweighted value in Table B.2, a stale line pointer, two overstatements in the birth-year diagnostic, an attribution fix and three precision fixes), clarifications B1–B17 (inference conventions and K counting, explicit *t*(*G*−1) CI/*p* reconciliation, verification coverage 24 / 2 / 265 of 291), captions Table B.1–B.2, decisions G1–G7 (FA-22). No shared file changed. Not in `APPROVED.tsv`; canonical appendix unchanged. FA-7 B remains unresolved.
- **Appendix C (`appC`; numbered Appendix C, not a chapter): verified and language-edited publishing copy and review-copy preview, Awaiting author review** (§21). Eight verified corrections in the copy (A1–A8: the 275-child C1 difference limited to the birth-year window; "all four" CIs; the Ghana-exclusion row keeps Kenya's water overlap; what the Ethiopian interview date is needed for; birth-year eligibility not "satisfied by construction"; dating of the C1 finding versus C1's reclassification; pre-specification attributed to the specification §8; "exact buffer average"), clarifications B1–B19, captions Table C.1–C.3, points FA-23 A–G. **No stored number was found to be wrong.** No shared file changed. Not in `APPROVED.tsv`; canonical appendix unchanged. FA-7 B remains unresolved; FA-22 D remains unverified.
- **New required item recorded in the Appendix C session:** FA-22 F (Appendix B §B.1: "Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged."). Not applied; Appendix B not edited or rebuilt.
- **Consolidated references (references only; not a unit): review copy, Awaiting author review** (§22). One list of the 20 works cited across the abstract, Chapters 1–7 and Appendices A–C, built from a publishing copy of the bibliography (`bibliography/bibliography.bib`; canonical unchanged) with 21 evidenced field changes in 13 entries. FA-3 carried out in that copy; FA-4 fixed for the reference list only; follow-ups FA-24; review items FA-25 (A = FA-22 F; B exact postnatal counts, local check; C `m0032` *p* display). No chapter or appendix file changed.
- All seven chapters, the abstract and Appendices A–C now have review-copy previews. No full thesis has been rendered. The abstract,
  appendices and front/back matter have not been rendered as units (inventory in §17). The next step
  is the author's decision.
- *Set-up session status (kept for the record):* at set-up, `chapters/md/` and `chapters/tex/` were
  empty; the only PDFs were the diagnostic document and the preview-pipeline selftest, both built
  from labelled placeholder text.
- No canonical manuscript file, earlier version or earlier build was modified (`git status` showed only
  the new `publishing/` directory).
- Set-up session: no humanizer rewrite was made. Chapter 1 session: humanizer applied to the ch01
  publishing copy only (§11).
- The current full-manuscript page count is unknown; it will be measured at final assembly. (The
  32-page figure belongs to the superseded v6 build.)

## 3. Environment used in this session (cloud container)

| Tool | Version |
|---|---|
| XeTeX | 3.141592653-2.6-0.999995 (TeX Live 2023/Debian), installed this session via apt |
| biber / biblatex-chicago | biber 2.19; TeX Live 2023 `texlive-bibtex-extra` |
| pandoc | 3.1.3 (pre-installed) |
| Python | 3.13; PyMuPDF 1.28.2; fontTools 4.66.1 |
| poppler | 24.02 |
| Times New Roman | 2.82, from Microsoft's core-fonts archive `times32.exe` (SHA-1 `20b79e65…3060`; extracted file hashes match Debian's `ttf-mscorefonts-installer` manifest). The Debian package's own installer failed (python `apt_pkg` missing), so the archive was fetched and checked by hand. |
| Math font | TeX Gyre Termes Math (`fonts-texgyre-math`) |

Container tools do not persist. On a fresh cloud session, reinstall:
`apt-get install texlive-xetex texlive-latex-extra texlive-bibtex-extra biber texlive-fonts-recommended fonts-texgyre-math cabextract`,
`pip install pymupdf fonttools`, and Times New Roman as described above (or let `env` tell you what
is missing). On the author's Windows machine, Times New Roman is already present.

## 4. Design decisions (and why)

1. **pandoc + Lua filter + XeLaTeX + biber/biblatex-chicago (author–date).** pandoc is now available,
   so the v6 regex converter (`md2tex.py`) was not extended; it was read only as a reference. The filter
   does mechanics only (§README).
2. **Numbers stay as written, LaTeX checks them.** The filter removes the typed number from each heading
   and table caption, lets LaTeX number them, and inserts a check that stops the build if the two
   differ. No "1 1. Introduction" duplication; no table number shown twice; table numbers are counted
   per chapter, independent of subsections (§5.6 → Tables 5.5–5.7). In-text "Section 5.6" / "Table 5.3"
   remain plain text, as in the source; `lint` checks every such reference has a target.
3. **PostScript points.** Sizes and spacings are in bp (word-processor points).
4. **`ibidtracker=false`.** Without it, a citation directly following one of the same work printed as
   a bare "(p. 1)" (found in the first diagnostic build).
5. **Captionless `longtable*`.** Plain `longtable` advances the table counter even without a caption;
   found by the number check on its first run (Table 1.2 came out as 1.3) and fixed.
6. **Unicode superscripts** (⁴ ⁵ ⁶ ⁸ ⁻, missing from Times New Roman 2.82) are typeset as superscript
   digits. The characters' meaning is unchanged.
7. **Abstract = page 1; new page per chapter.** Publishing choices carried from v6, **not explicit
   university requirements** (author clarification, 2026-10-13). Both live only in
   `drivers/thesis-body.tex` and can be changed there without touching any chapter.
8. **Contents depth 4.** Every numbered heading level (1 to 1.2.3.4) is listed with its title and
   starting page. The earlier setting (depth 2) hid levels 3–4; corrected in `020f721`.

## 5. Tests actually executed

| Test | Result |
|---|---|
| Repository access: local clone, `git ls-remote`, `git fetch origin main` | HEAD = origin/main = `c58fc47…`; no newer commit |
| `build.py lint` on all 11 canonical units (converter run in memory, no PDF) | 0 problems: 20 cited keys, all in the 26-entry bibliography; 9 captions → 9 captioned tables in ch. 5; 8 uncaptioned appendix tables; every Section/Table reference has a target; no glyph missing after superscript mapping |
| `build.py diagnostic` | 0 LaTeX errors, 0 overfull/underfull boxes, 0 missing characters, 0 undefined citations/references, biber 0 warnings |
| PyMuPDF layout measurement of the diagnostic | A4; margins 2.500 cm / ≥ 3.998 cm; 11/19.5, 10/15, 9/13.5 exact; 35 lines per full page; heading gaps as specified; 0 automated issues |
| Visual inspection | every page of the delivered 13-page PDF rendered at 110 dpi and looked at; earlier builds likewise, which is how the title-page break, the "(p. 1)" citation, the caption spacing and column widths were found and fixed |
| Negative tests | skipped heading number, wrong table number, orphan caption, unnumbered heading → all stop the build |
| Counter offsets | chapter 5 (two tables in one subsection → 5.2, 5.3) and Appendix B (B.1, Table B.1) number correctly |
| `build.py selftest` (preview pipeline on diagnostic text) | 8 pages, 0 errors; review label, chapter numbering and separate verification reference list present |
| Guard rails | `preview`/`convert` refuse without `prepare`; `thesis` and `thesis --final` refuse with no approved units; unknown unit rejected |
| `build.py manifest` | 15/15 canonical inputs recorded and unchanged |
| Contents-depth correction (`020f721` diagnostic) | 0 errors/overfull/missing characters/undefined citations; 13 pages. All 10 contents entries (levels 1–4, references, appendix) checked programmatically: titles match the headings and every listed page equals the page where the heading appears. Contents page and the pages holding the level-3/4 headings inspected visually; all other pages compared with the previous build: identical extracted text, pixel differences ≤ 18/255 (anti-aliasing) |

Not tested here: the full `thesis` command end-to-end (no chapters may be converted yet); a build on
Windows/MiKTeX; the author's newer Times New Roman.

## 6. Unresolved set-up issues

1. **The guideline PDF never reached this session** (no attachment; the university website is blocked
   by the container's network policy). Formatting values come from the task brief and the v6 preamble,
   which agree. The author reports having compared the declaration affirmation and the title-page
   structure with the supplied 23 July 2026 guidelines (recorded as the author's comparison, not
   repeated here). Abstract placement and new-page chapters are publishing choices, not requirements.
2. **Author confirmation still required:** personal metadata on the title page (title, name,
   matriculation number, supervisor, degree line — carried from v6/AUTHOR_CHECKLIST, not re-verified
   against the registration email) and the actual submission month/year (the 22 October 2026
   deadline is not the submission date). `thesis --final` refuses while the placeholder remains.
3. Font version differs between this container (2.82) and Windows; re-run `diagnostic` locally.
4. Monospace font for file paths in prose: author decision (F3 in the checklist).
5. ~~PDF hyperlink of the "References" contents entry jumps to the anchor of the preceding subsection
   rather than to the reference list.~~ **Fixed in the Chapter 1 session (§11):** the shared
   `bibintoc` heading now sets its own anchor. Verified in the ch01 preview's PDF bookmark (page 7,
   reference list) with a negative test (old definition → page 6, §1.8 anchor). The 13-page
   diagnostic was not regenerated; re-run `diagnostic` at the next template check or at final assembly
   to see the contents-page link itself.

## 7. Known issues for specific chapter sessions (layout only; decide with the author)

- **ch02**: some `Cumming2019` locators are long free text (e.g. "pp. 2, 5 and Fig. 2, which reports
  …"); they will print verbatim inside the parentheses. Locators keep "p."/"pp." as written; strict
  Chicago omits them. Do not change wording without approval.
- **ch04**: the §4.4 age-interaction display equation is very long and will probably exceed the line
  width; a line-broken layout (same symbols and terms) may be needed. Check the preview's overfull-box
  count and the page image.
- **ch05** (*resolved in the Chapter 5 session, §15: Tables 5.3, 5.5 and 5.6 in long format; sample notes as 9 pt table notes; table keep logic in the preamble, FA-10*): Tables 5.5–5.7 have five columns; at the mandated 10 pt the *p*-value wraps onto a second
  line inside cells (seen with the same shape in the diagnostic Table 1.2). Not clipped, but check
  readability. Table 5.1 group rows ("Region FE", "Cluster FE …") render as full-width rows. The
  parenthetical sample-size notes after tables are prose and stay main-text size unless the author
  approves marking them as table notes.
- **Appendices**: their 8 tables have no captions in the source, so they are unnumbered. Numbering
  them would need caption lines added to the source — an author decision, not a rendering default.
- **ch03, ch04, appB, appC**: contain the Unicode superscripts handled in decision 6.

## 8. Protocol for each chapter chat

1. Read this file and `README.md`. Run `python scripts/build.py env` and `manifest` (must be
   unchanged; if not, stop and report what changed).
2. `lint <unit>`, `prepare <unit>`, `preview <unit>`.
3. Read the `.report.md`; look at **every** page image in the work directory; check numbers in tables
   against the canonical Markdown (they are copied by the converter, never typed).
4. Report: PDF path, report path, commit, hashes, problems. Do not add the unit to `APPROVED.tsv`; the
   author does that after review.
5. Keep academic content unchanged: no new numbers, citations, claims or qualifications removed; no
   conversion of associations into causal language.

## 9. Humanizer

Available in this cloud session as skill `anthropic-skills:humanizer` (v2.9.1, MIT), file
`/root/.claude/skills/synced/69d9880f-b623-46af-aaf0-34fefa7487f1_a27071fb-20b7-4f8b-9719-c3fdcd784c70/humanizer/SKILL.md`.
Its availability in the local VS Code environment was not checked. Not used in the set-up session.
It was read and used on the ch01, ch02 and ch03 publishing copies (§11–§13).

Rules for later use, per the author's instructions: polishing of natural academic English and flow
only, applied to `chapters/md/` copies, with a diff against canonical reviewed by the author. It must
not change technical meaning, evidential strength, hedging, citations, numbers, variable names or
equations, and it is not to be used to conceal assistance or to target an AI-detection outcome. The
author states that AI assistance was discussed with the supervisor; `manuscript/v12_2026-10-10/AUTHOR_CHECKLIST.md`
records that the guidelines' AI-use question is handled outside this package. No disclosure or
declaration wording has been drafted, and none should be invented.

## 10. Next authorized task

*Updated after the consolidated-references session:* the reference list has a review copy (§22). Remaining for final assembly in local VS Code: the author's review, the required corrections and local checks in the register (now including FA-24 and FA-25), and the full `build.py thesis` (title page, contents, references in place, appendices, declaration). The next step is the author's decision. *Updated after the Appendix C session:* the Appendix C preview is done and awaits author review (§21). Every content unit (abstract, Chapters 1–7, Appendices A–C) now has a review-copy preview. What remains is the author's review and final assembly in local VS Code: the consolidated references, title page, contents and declaration are produced only by `build.py thesis` (inventory and next-stage handover in §21). The next step is the author's decision. *Updated after the Appendix B session:* the Appendix B preview is done and awaits author review (§20). Remaining units: Appendix C and the front/back matter assembled by `build.py thesis` (inventory in §20). Appendix C is the next unit on the appendix continuation path (FA-20). The next unit is the author's decision. *Updated after the Appendix A session:* the Appendix A preview is done and awaits author review (§19). Remaining units: Appendices B and C and the front/back matter assembled by `build.py thesis` (inventory in §19). Appendices B and C are the first units after Appendix A to use the new continuation heads (FA-20). The next unit is the author's decision. *Updated after the abstract session:* the abstract preview is done and awaits author review (§18). Remaining
units: appendices A–C and the front/back matter assembled by `build.py thesis` (inventory in §18). The next unit
is the author's decision. *Updated after the Chapter 7 session:* the conclusion preview is done and awaits author review (§17).
All seven chapters now have previews. The remaining units (abstract, appendices A–C, and front/back
matter assembled by `build.py thesis`) and the final-assembly items are listed in §17 and in
`FINAL_ASSEMBLY_REGISTER.md`. The next unit is the author's decision. *Updated after the Chapter 6 session:* the discussion-and-limitations preview is done and awaits
author review (§16). The next unit is the author's decision; Chapter 7 (`ch07`, conclusion) follows
in order. Page-budget editing remains deferred to final assembly (FA-11). *Updated after the Chapter 5 session:* the results preview is done and awaits author review
(§15). The next unit is the author's decision; Chapter 6 (`ch06`) follows in order. Page-budget
editing is deferred to final assembly on the author's instruction (FA-11). *Updated after the Chapter 4 session:* the empirical-strategy preview is done and awaits author
review (§14). The next unit is the author's decision; Chapter 5 (results, `ch05`) follows in order
(see the §7 notes on Tables 5.5–5.7). *Updated after the Chapter 3 session:* the data-and-variables preview is done and awaits author
review (§13). The author has announced **Chapter 4 (empirical strategy), `ch04`**, as the next unit, in a
separate session (§8 protocol; see the known §4.4 equation-width issue in §7). *After the Chapter 2
session:* the literature-review preview was done and awaited author review (§12). *Earlier, after the Chapter 1 session:* the introduction preview is done and awaits author review
(§11). The next unit is decided by the author; the per-chapter protocol is §8. The original
instruction for ch01 is kept below for the record.

**Introduction preview (`ch01`) only, and only after the author has reviewed this set-up.** Commands:

```sh
cd publishing/thesis_render_v12
python scripts/build.py env
python scripts/build.py manifest
python scripts/build.py lint ch01
python scripts/build.py prepare ch01
python scripts/build.py preview ch01
```

## 11. Session log: Chapter 1 (introduction) preview, 2026-10-13

**Status: awaiting author review. Do not add ch01 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (remote `main` re-checked: unchanged); manifest 15/15 unchanged |
| Package received | `thesis_render_v12_package_b8ceebb.zip` (ZIP comment `b8ceebb5…`); the branch `claude/busy-ramanujan-u6qrs8` and commit `b8ceebb` are **not** on the remote, so the ZIP was imported as received |
| Local commits (branch `render-v12-ch01` on `c58fc47`; **not pushed**, GitHub returns 403 for this session) | `324ae0d` package import; `740f004` ch01 edit, anchor fix, preview title, docs; then a commit adding the preview PDF, its reports and this log. Patches for all three are in the cumulative ZIP (`patches_from_c58fc47/`). |
| Preview | `builds/previews/REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` (7 pages: body pp. 1–6, preview references p. 7) + `.report.md` + `.verification.md` |
| Canonical / edited / tex sha256 | `008f7be5…1d085b` / `2203446d…22c3e` / `13155ac5…d678e` |
| Edit record | `chapters/changes/01_introduction.changelog.md`, `01_introduction.worddiff.txt` |

What was done:
- Humanizer (v2.9.1) language edit of the **publishing copy only**. All numbers (69 tokens), all six citation groups (same order), all headings and every cross-reference target are unchanged (automated check).
- One internal-commentary sentence was removed from §1.8. It is flagged for the author in the changelog, item 1.
- Rendering defects fixed by rewording in the copy:
  - an overfull line at "Household-level";
  - doubled parentheses around the IHME citation;
  - a stranded "(β", fixed with a non-breaking space.
- **Shared change:** `template/thesis-preamble.tex` now gives the `bibintoc` heading its own anchor, which resolves set-up issue 6.5. It was verified in the preview bookmark, with a negative test.
- **Shared change:** `scripts/build.py` titles the preview list "References cited in this chapter --- preview only" and bookmarks it.
- Verification: 0 errors/overfull/underfull/missing glyphs/undefined citations; biber 0 warnings; 9/9 citation links land on their own entries; heading gaps measured at 39.0 pt; every page of the final PDF inspected (details in `.verification.md`).

Open points carried forward (author decisions; none changed without approval):
1. Restore or drop the removed §1.8 sentence.
2. Heading "1.6 A restrained summary of findings": keep, or use "Summary of findings".
3. Bold → italics for emphasis in ch01. If accepted, the same convention should be applied in later chapters.
4. **Bibliography data, which affects the final reference list:**
   - `LBDWaSH2020` has no volume or pages, which produces the stray comma before the DOI;
   - `SkoufiasVinha2026` has no article number;
   - the Rakotomanana title is in title case.
   Correct these only from verified records.
5. **Shared template:** xurl breaks DOIs mid-word ("htt ps://"). Consider allowing breaks only after "/" and "." in a dedicated template step, then re-run `diagnostic`.
6. `citation_map.md`: the `CummingCairncross2016` row predates the R15 full-text check.
7. §1.6 vs Table 5.3: the joint-model household water coefficient has *p* = .043. Decide whether the introduction should mention it.

Environment notes for the next cloud session:
- pandoc 3.1.3 was **not** pre-installed this time. Install it with `apt-get install pandoc`.
- Times New Roman 2.82 was fetched from `times32.exe`; its SHA-1 matched `20b79e65…3060`, as in §3.

## 12. Session log: Chapter 2 (literature review) preview, 2026-10-14

**Status: awaiting author review. Do not add ch02 to `APPROVED.tsv` until the author has done so.**
*Update (Chapter 3 session):* the author has reviewed Chapter 2. A §2.4 correction is **required at final
assembly** (`FINAL_ASSEMBLY_REGISTER.md` FA-1; §13); until it is applied, Chapter 2 is not finalised.

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged. |
| Package received | `thesis_render_v12_package_12a954d.zip` (sha256 `555649bb…57b80`). Restored by `git am` of its three patches onto `c58fc47`; the resulting `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/cool-babbage-4kjqgw`, on `c58fc47`. Package replay: `e9dc05f`, `e10f9a5`, `9b81cc5` (same trees as `324ae0d`, `740f004`, `12a954d`; different committer metadata). Then `b689d34` (ch02 edit, tex, change record, provenance fix) and a commit adding the preview, its reports, the ch01 carry-forward record and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| Preview | `builds/previews/REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` (10 pages: body pp. 1–8, preview references pp. 9–10) + `.report.md` + `.verification.md` |
| Canonical / edited / tex sha256 | `b2569800…30312` / `a9ceca1a…40de9` / `46fccbec…c1547` |
| Edit record | `chapters/changes/02_literature_review.changelog.md`, `02_literature_review.worddiff.txt` |
| Guidelines | The attached 23 July 2026 guideline PDF reached this session and was read directly. Its formatting values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. |

What was done:
- **Humanizer.** v2.9.1 was read in full and used for the ch02 publishing copy only.
  - Unchanged: every number, quotation, heading, and all 30 citation commands (keys and order).
  - All 33 punctuation em dashes were replaced. Bold emphasis was kept, pending the ch01 bold → italics decision.
- **Cumming2019 locator** (§7 known issue). It is now "pp. 2, 5 and Fig. 2". The Fig. 2 wording explanation moved into the prose, still under the same citation.
- **Internal file pointer removed from §2.3** (`bibliography_verification_ledger.md`). The working-paper statement itself is kept.
- **Two overfull lines** (at "WHO/UNICEF" and "cluster-randomised") were fixed by rewording the copy.
- **Shared change:** `scripts/build.py prepare` now records the canonical manuscript's last commit as `source_commit`, instead of HEAD. The ch02 provenance row was corrected to `c58fc47`.
- **Verification** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined citations; biber 0 warnings;
  - 17 keys, 0 unresolved; 31/31 citation links land on their own entries;
  - 21/21 source blocks present in order;
  - every page of the final PDF inspected.
- **Chapter 1.** The author's carry-forward decision is recorded in `APPROVED.tsv` (tex `13155ac5…`). All Chapter 1 files are byte-identical to the received ZIP.

Open points carried forward (author decisions; none changed without approval):
1. **§2.4 vs. Section 5.2 (substantive).** The sentence "community water and sanitation do not behave identically under full adjustment" does not match Table 5.2, where both are null and nearly equal when fully adjusted; they differ at the SES stage, and in the opposite direction to Skoufias and Vinha. Changelog A1.
2. **§2.7 "three design elements".** Two items are listed; a three-way reading is possible. Changelog A2.
3. **Removed internal pointer in §2.3.** Restore or keep removed. Changelog A3.
4. **Optional heading simplifications** (§2.5 "specifically", §2.3). Changelog A4.
5. **Bibliography data for final assembly:**
   - `Cumming2019` has no volume or article number (stray comma);
   - the printed `GerusoSpears2015` note reads as package commentary;
   - "DHS Spatial Analysis Reports" is plural;
   - also all of ch01 open point 4 and the xurl DOI breaks (ch01 open point 5).

   Correct these only from verified records, in a dedicated bibliography or template step.
6. **Evidence-depth labels.** `bibliography_verification_ledger.md` ("full-text read") and `citation_map.md` ("abstract inspected") disagree for Gunther2010, Spears2013, Balk2004 and JohnsonJacobBrown2013. The prose relies on neither; reconcile the records at final assembly.

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed this time.
- TeX Live, biber and the fonts were installed via apt as in §3.
- Times New Roman 2.82 came from `times32.exe`; its SHA-1 `20b79e65…3060` matched.
- Pushing to `main` is not attempted. The session's designated branch is `claude/cool-babbage-4kjqgw`.

## 13. Session log: Chapter 3 (data and variables) preview, 2026-10-14

**Status: awaiting author review. Do not add ch03 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged (checked at start and before the final build). |
| Package received | `thesis_render_v12_package_c7cf945.zip` (sha256 `e8532f84…8c33d`). Restored by `git am` of its five patches onto `c58fc47`. The resulting `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/ecstatic-knuth-j05qq8`, on `c58fc47`. Package replay: `6d8097c`, `cebcde8`, `20bc7ab`, `9e68578`, `a0852ac` (same trees as the earlier sessions' commits). Then `9bf1bfa` (ch03 edit, tex, change record). Then a commit adding the preview, its reports, `FINAL_ASSEMBLY_REGISTER.md` and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| Preview | `builds/previews/REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` (10 pages: body pp. 1–9, preview references p. 10) + `.report.md` + `.verification.md` |
| Canonical / edited / tex sha256 | `ed7b30b0…caa970` / `9f9d9b18…a91176` / `4f5d7937…826e90` |
| Edit record | `chapters/changes/03_data_and_variables.changelog.md`, `03_data_and_variables.worddiff.txt` |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02 session) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. |

What was done:
- **Humanizer.** v2.9.1 was read in full and used for the ch03 publishing copy only.
  - Unchanged: all numbers (103 tokens), the 3 citation commands (keys and order), the 19 code spans, the formula `$[0,1]$`, the 10 headings and the 14 italic spans.
  - All 29 punctuation em dashes were replaced; the 9 range en dashes were kept. Bold was kept (pending the ch01 bold → italics decision).
- **Source checks** against stored code and public provenance only. No restricted data was used and no pipeline was run. Every construction claim and number in the chapter was traced (verification report §9). No statement was found to be wrong.
  - Five author-review points (changelog section A, register FA-6): the leave-one-out grouping key `hv001` vs. the fixed-effect key `v021`; the §3.9 "described above" cross-reference; cluster-year vs. "child-year"; brief items not stated in the chapter; and the data dictionary's "household census" wording.
- **Rendering fixes, made in the copy only:**
  - 3 overfull lines, fixed by small rewordings;
  - "2" / "km" split across a line: non-breaking spaces before "km" (8 places);
  - the script path broke at ".py": "the script" was added before it;
  - Burgert2013 moved out of the parentheses (doubled parentheses).
- **Verification** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined citations; biber 0 warnings;
  - 3/3 citation links land on their own entries; 22/22 source blocks present in order; 65/65 numbers present;
  - heading gaps 39.0 pt;
  - every page of the final PDF covered by direct inspection (pages compared pixel-for-pixel with the inspected build).
- **Shared files:** none changed (template, filter, scripts, drivers, bibliography).
- **Chapters 1 and 2:** all 14 of their files are byte-identical to the received ZIP. The ch01 carry-forward row in `APPROVED.tsv` is unchanged.
- **New `FINAL_ASSEMBLY_REGISTER.md`.** It records:
  - the required Chapter 2 correction (FA-1, below);
  - the ch01 carry-forward (FA-2);
  - bibliography completeness (FA-3, with the new `deOnis2006` note/quotation-mark item);
  - the xurl DOI-break item (FA-4);
  - final pagination and the 40-page check (FA-5);
  - the ch03 review points (FA-6).

**Chapter 2 correction: REQUIRED AT FINAL ASSEMBLY (not applied in this session).** In §2.4 of
`chapters/md/02_literature_review.md`, replace the sentence

> This is a closer and more precise parallel to this thesis's own baseline finding (Section 5.2) that community water and sanitation do not behave identically under full adjustment.

with

> This study motivates considering water and sanitation separately. Its finding contrasts with this thesis's fully adjusted community HAZ models, which provide no statistically significant evidence of an association for either measure (Section 5.2).

Then lint, preview and inspect ch02 again before the author decides on approval. A similar sentence in §2.2 ("…is a closer and more precise parallel to this thesis's own null household- and community-sanitation findings…") is **not** the target. Full instructions: `FINAL_ASSEMBLY_REGISTER.md` FA-1.

**Open points carried forward** (author decisions; none changed without approval):
- the ch03 points A1–A5 above;
- ch01 open points 1–7 (§11);
- ch02 open points 2–6 (§12; point 1 is superseded by the FA-1 correction).

### PDF filename → chapter map (for the local VS Code session)

| Downloaded file | Unit | Chapter | Status |
|---|---|---|---|
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | **awaiting author review** |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

The seven-character code in each filename is the **publishing** commit at build time, not the academic source (always `c58fc47`). Each PDF has a `.report.md` and (for chapters) a `.verification.md` with the same stem in `builds/previews/`.

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed.
- TeX Live, biber, the fonts and `cabextract` were installed via apt as in §3; PyMuPDF via pip.
- Times New Roman 2.82 came from `times32.exe`; its SHA-1 `20b79e65…3060` matched.
- Pushing to `main` is not attempted.

## 14. Session log: Chapter 4 (empirical strategy) preview, 2026-10-14

**Status: awaiting author review. Do not add ch04 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged (checked at the start and before the final build). |
| Package received | `thesis_render_v12_package_7bc4b53_1.zip` (sha256 `cfb77f86253f300fbdeb82cf356e72ac82f1ac8e34fc8216a60970bc6e14cf82`; ZIP comment `7bc4b53…`). Restored by `git am` of its seven patches onto `c58fc47`. The resulting `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/intelligent-goldberg-njxus5`, on `c58fc47`. Package replay: `e9dc05f`, `e10f9a5`, `9b81cc5`, `b689d34`, `c7cf945` (same hashes as the originals), then `ebf22b4`, `116ae12` (same trees as `9bf1bfa`, `7bc4b53`; different committer metadata). Then `4b7535d` (ch04 edit, tex, change record, `build.py` zero-citation page), then a commit adding the preview, its reports and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| Preview | `builds/previews/REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` (sha256 `00684c3042aca85f10d09e5ea622911ac3e4aca04e8b7c7c9ba64a0c0ff9fafc`), 10 pages: **body pp. 1–9; preview-only reference page p. 10**. Also `.report.md` (`c72252e7…047838f`) and `.verification.md` (`d7445d55…e65ff6d1`). |
| Canonical / edited / tex sha256 | `3955ff27f5db6f2076592ffbf5892f36fb07c1960865c527ca73822f6c0389f2` / `61f972e3df2346787af5d7654c37f5d96590d3500df178b9741414c70177fa4e` / `8d508baf09ec5e2d6044db1f4f5d2cb74c42256260b269167817b372ccbd4c37` |
| Edit record | `chapters/changes/04_empirical_strategy.changelog.md` (`04ee74b0…9cbfe915`), `04_empirical_strategy.worddiff.txt` (`ff07dd75…5c82caa8`) |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02 and ch03 sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. |

What was done:
- **Humanizer.** v2.9.1 was read in full and used for the ch04 publishing copy only.
  - Unchanged: all 90 numbers; all 7 display and 73 inline math expressions (apart from layout markup); 14 code spans; 7 headings; 22 bold and 21 italic spans; 2 quoted strings. The chapter has no citations.
  - All 44 punctuation em dashes were replaced; the 15 range or compound en dashes were kept. Bold was kept, pending the ch01 bold → italics decision.
- **Specification check** against the code and stored public outputs only. No restricted data was read, no model was refitted, and no estimator was changed.
  - Checked: `14_household_community_wash_models.py` (Parts 2–7, including the joint model and the age-band code), `11_main_regressions.py`, `12_robustness.py`, `04_build_country_kr.py`, `05_pool_countries.py`, `16_estimate_preliminary.py`, `24_reconcile_inference_corrections.py`, `25_diagnose_birthyear_coding_and_age_control.py`, Appendix B, Table 5.6 and the public historical aggregate table.
  - The baseline normal-reference p-value (.0617391913770433 vs. *t*(*G*−1) .0618052) was reproduced exactly from the stored coefficient and SE.
  - **One substantive notation point** (§4.5: "(equivalently, $N/M$ on average across countries)" conflicts with the baseline implementation, where each country total is 1) and three optional clarifications were found. They are recorded as changelog A1–A4 and register FA-8. None was applied.
- **Rendering fixes, made in the copy only:**
  - the §4.4 age-heterogeneity equation is now a three-line `aligned` display with every term kept (it had been 172 pt too wide; the known §7 issue);
  - a thin space before the $\bar{C}$ superscripts (glyph collision);
  - "a panel" → "a panel design" (overfull line);
  - the weight formula was joined to its sentence (spurious indent).
- **Shared file changed:** `scripts/build.py`. A unit without citation commands now gets the labelled "References cited in this chapter — preview only" page, stating that no works are cited, instead of no page at all.
  - Units with citations take the unchanged code path.
  - Chapters 1–3 were not rebuilt.
  - Template, filter, drivers and bibliography are unchanged.
- **Verification** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined references;
  - heading gaps 39.0 pt;
  - 16/16 prose paragraphs in order; 58/58 distinct numbers present; no raw markup;
  - bookmarks on the correct pages;
  - every page of the delivered PDF inspected directly. Its body is pixel-identical to the previously inspected build.
- **Register:** FA-7 records the author's Chapter 3 decisions: the **required** §3.9 cross-reference correction ("described above" → "described in Section 4.5"; target verified) and the **open** `hv001`/`v001` vs. `v021` local verification question, which is not resolved. FA-8 records the Chapter 4 points. FA-1 (Chapter 2 §2.4) and the FA-3 bibliography and FA-5 pagination items are preserved unchanged.
- **Chapters 1–3:** all 21 of their files are byte-identical to the received ZIP. Not rebuilt or edited.

**Open points carried forward** (author decisions; none changed without approval):
- ch04 changelog A1–A4 (FA-8);
- FA-7 A (required) and FA-7 B (open question);
- FA-1 (required);
- ch03 points A3–A5;
- ch01 open points 1–7 (§11);
- ch02 open points 2–6 (§12).

### PDF filename → chapter map (cumulative)

| Downloaded file | Unit | Chapter | Status |
|---|---|---|---|
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction pending** (FA-7 A); open verification question (FA-7 B) |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | **awaiting author review**; points FA-8 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

The seven-character code in each filename is the **publishing** commit at build time, not the academic source (always `c58fc47`).

Page counts are those of separate previews (ch04: 9 body pages plus 1 preview-reference page). They are not a thesis page count; the 40-page main-text maximum is checked only at final assembly (FA-5).

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed.
- TeX Live, biber, the fonts, `cabextract` and poppler were installed via apt as in §3; PyMuPDF and scipy via pip.
- Times New Roman 2.82 came from `times32.exe`; its SHA-1 `20b79e65…3060` matched, and `Times.TTF` sha256 is `4e98adef…bbe86`.
- Pushing to `main` is not attempted.

## 15. Session log: Chapter 5 (results) preview, 2026-10-14

**Status: awaiting author review. Do not add ch05 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged (checked at the start and before the final build). |
| Package received | `thesis_render_v12_package_90787b4_1.zip` (sha256 `43523e1748ea63161bcc9712c612ec0ef86e1ed418c26be8edb849bcc3e72061`; ZIP comment `90787b47…`). Restored by `git am` of its nine patches onto `c58fc47`. This reproduced the **identical** commit IDs `e9dc05f` … `90787b4`, and the `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/eager-dijkstra-v8e186`, on `c58fc47`. Package replay `e9dc05f` … `90787b4`. Then `c1f74e2` (ch05 edit, tex, change record, shared preamble change). Then a commit adding the preview, its reports and checks, and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| Preview | `builds/previews/REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` (sha256 `d92b9c2973a950c638582c148dd61ece604515c67e274474aa65cd954780f34a`), 11 pages: **body pp. 1–10; preview-only reference page p. 11** (the chapter cites no works). Also `.report.md`, `.verification.md` and the `.checks/` folder (scripts and logs). |
| Canonical / edited / tex sha256 | `9f646aa02f72e8656469796c4b0d3b8ad865de174cc9536eaa6d497038f7ce34` / `d01694474488ef5e0080f811e40f03c7c577707a76e78e50da67fb976e042c4e` / `bdbe2c1f403ace239af307ac910c5a2feaebd2271d79e4605b4f0125eeb9a6c4` |
| Edit record | `chapters/changes/05_results.changelog.md`, `05_results.worddiff.txt` |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–ch04 sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`. |
| Author instructions recorded | Render the whole chapter now. Defer page-budget editing to final assembly (FA-11). Reclassify the Chapter 4 points as required (FA-8). Preserve FA-1, FA-7 A and B, and the bibliography and template items. Do not mark Chapter 5 approved. |

What was done:
- **Numerical verification against stored outputs.** Located through the claim–evidence ledger, Appendix A, the v3 results index and the reporting map. Public files only; the historical cells come from the public full-precision aggregate CSV.
  - **440 keyed comparisons** (identifier fields, never row position) cover every coefficient, CI bound, p-value, N, cluster count and test df of all nine tables, and the prose numbers. All match at the displayed precision.
  - Reference distributions were confirmed from the stored β/SE: baseline cells are normal-reference; historical cells are *t*(*G*−1).
  - **One prose discrepancy:** §5.4 "more than doubles in magnitude" (stored ratio 1.546–1.665). It was corrected in the copy (changelog A1). Two descriptive corrections were also applied: the CI convention vs Table 5.4 (A2), and the Table 5.9 caption (A3).
  - No model re-run, no restricted data, no new findings.
- **Humanizer.** v2.9.1 was read in full and used for the ch05 publishing copy only.
  - All table values, headings, code spans and hedges are kept. 27 punctuation em dashes replaced (9 caption separators remain). Bold kept, pending the ch01 decision.
  - Clarifications B1–B11 restate qualifications that Chapters 3–4 establish, or that Chapter 3 says are restated wherever historical coefficients are reported. They cover age bands and df, area-average exposure, weighted conditional associations, *t*(*G*−1), verification coverage (24 of 291 reproduced; 267 internally checked) and equal totals ≠ equal influence. Each is evidenced in the change log.
- **All nine tables preserved** (5.1–5.9, in order, captions checked).
  - Tables 5.3, 5.5 and 5.6 are in long format, because their cells broke inside CI brackets. They were generated from the canonical cells; a keyed equivalence check confirms all 36 cells.
  - The sample notes are now 9/13.5 pt table notes.
  - Captions are unique and numbered by `\ThesisCheckNumber`.
- **Shared change: `template/thesis-preamble.tex`** (FA-10). It fixes stranded headings after `\needspace`, detached table notes, split tables and indented notes, using heights recorded in the `.aux` file. Chapters 1–4 have no tables and were not rebuilt. Filter, scripts, drivers and bibliography are unchanged.
- **Verification of the PDF** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined references.
  - Heading gaps 39.0 pt. Text pitch 11/19.5, tables 10/15, notes 9/13.5.
  - Bookmarks on the correct pages.
  - 76/76 table rows and 176/176 prose numbers found in the extracted PDF text.
  - Every page of the delivered PDF inspected directly.
- **Chapters 1–4:** all 28 of their files are byte-identical to the received ZIP. Not edited or rebuilt.
- **Register:**
  - FA-8 (Chapter 4 A–D) is now **required**, with exact targets.
  - New: FA-9 (Chapter 5), FA-10 (template re-check) and FA-11 (page budget).
  - FA-1, FA-7 A (required) and FA-7 B (open), FA-3 bibliography and FA-4 xurl are preserved unchanged.

**Open points carried forward** (author decisions; none changed without approval):
- ch05 E1–E7, plus confirmation of A1–A3, B1–B11 and the layout (FA-9);
- FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open question);
- FA-1 (required);
- ch03 points A3–A5;
- ch01 open points 1–7 (§11);
- ch02 open points 2–6 (§12).

### PDF filename → chapter map (cumulative)

| Downloaded file | Unit | Chapter | Status |
|---|---|---|---|
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction pending** (FA-7 A); open verification question (FA-7 B) |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **four required corrections pending** (FA-8) |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | **awaiting author review**; points FA-9 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic (built before the FA-10 preamble change; re-run at final assembly) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

The seven-character code in each filename is the **publishing** commit at build time, not the academic source (always `c58fc47`).

Page counts are those of separate previews (ch05: 10 body pages plus 1 preview-reference page). They are not a thesis page count. The 40-page main-text maximum is checked only at final assembly (FA-5, FA-11).

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed.
- TeX Live, biber, the fonts, `cabextract` and poppler were installed via apt as in §3; PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86`).
- Pushing to `main` is not attempted.

## 16. Session log: Chapter 6 (discussion and limitations) preview, 2026-10-14

**Status: awaiting author review. Do not add ch06 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged (checked at the start and before the final build). Canonical chapter `manuscript/v12_2026-10-10/06_discussion_and_limitations.md`, last changed in `e3fa699` (contained in `c58fc47`). |
| Package received | `thesis_render_v12_package_3e31cc7_1.zip` (sha256 `4fe45541c2b290507fc08c4688a0cffa892b72f8e95779889319c650f329e2d5`; ZIP comment `3e31cc7c…`). Restored by `git am` of its 11 patches onto `c58fc47`. Commits 1–10 reproduced the **identical** IDs `e9dc05f` … `c1f74e2`; the 11th (`3e31cc7` originally) became `8cd9a58`, same tree, because its committer timestamp is not in the patch. The `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/clever-davinci-tn2piv` (the session's designated branch), on `c58fc47`. Package replay `e9dc05f` … `c1f74e2`, `8cd9a58`. Then `bdfebe647ca9147e010973e3ad5463c3460df630` (ch06 edit, tex, provenance row, change record, word diff). Then a commit adding the preview, its reports and checks, and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| Preview | `builds/previews/REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` (sha256 `dd72252da331442b1f4e2935698c859192cb9126dc133c79cad9ee47935ba8ed`), 8 pages: **body pp. 1–7; preview-only reference list p. 8** (3 works). Also `.report.md`, `.verification.md` and the `.checks/` folder (scripts and logs). |
| Canonical / edited / tex sha256 | `eefb55945a6830f4ed5b85141efae690fa0bf5cfa8f4e2beb414220e0ea45a94` / `1f6ba062869ff6915417d5748793e58e63a493b114b1761480f93ec09f16443f` / `e1f9f3de16f1aea6b50c6d75139238e5330676e83c3222680e796994c8115ebe` |
| Edit record | `chapters/changes/06_discussion_and_limitations.changelog.md`, `06_discussion_and_limitations.worddiff.txt` (`65c1b8cf…8a21b`) |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–ch05 sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. |
| Author instructions recorded | Render the whole chapter; do not shorten or impose a page target (FA-11). Record the Chapter 4 §4.5 vs. Chapter 5 correction as required (FA-12) and the Chapter 5 canonical synchronisation (FA-13). Preserve FA-1, FA-7 A/B, FA-8 A–D, FA-3/FA-4 and the page-budget instruction. Do not treat pending corrections as completed or approved. Status "awaiting author review". |

What was done:
- **Evidence review.** Chapter 6 was read in full against the Chapter 5 publishing copy, the reporting map and core reporting table, the claim–evidence ledger, `citation_map.md`, Chapters 1–4 and Appendices A–C. Every number was checked against stored public outputs by named keys (31/31 keyed checks OK; `verify_ch06.tsv`). No restricted data, no model run, no new result.
- **Ten verified corrections in the copy** (changelog A1–A10). The most substantive:
  - A1: region fixed effects are also used in the household region-FE and joint models;
  - A2: the sanitation "detectable, then not" pattern holds for community, not household, sanitation;
  - A3: "high compliance" belongs to the nutrition arm;
  - A4: the unweighted 0.41 now accompanies the headline 1.03;
  - A5: verification coverage stated as 24 of 291 reproduced;
  - A6: "the next section" → "Section 7".
- **Clarifications B1–B13** restate qualifications from Chapters 1–5 (no new estimates). **Decisions F1–F6** are left for the author.
- **Humanizer.** v2.9.1 was read in full and used for the ch06 publishing copy only. 19 punctuation em dashes replaced; range and compound en dashes kept; 8 bold spans kept (ch01 bold → italics decision pending); the long §6.5 paragraph split into six paragraphs, order unchanged.
- **Rendering fixes, copy only:** doubled parentheses before the Cumming citation; en-dash section ranges that broke across lines; "Appendix" tied to its letter (4 places).
- **Verification of the PDF** (details in `.verification.md`): 0 errors, overfull/underfull boxes, missing glyphs or undefined references; biber 0 warnings; heading gaps 39.0 pt; 30/30 blocks in order; 140/140 sentences; 65/65 numbers; 3/3 citation links to their own entries; 7/7 bookmarks on the right pages; every page of the delivered PDF inspected directly.
- **Shared files:** none changed (template, filter, scripts, drivers, bibliography).
- **Chapters 1–5:** all 42 of their files (md, tex, change logs, word diffs, preview PDFs, reports, verification reports, the ch05 `.checks/` folder) and `APPROVED.tsv` are byte-identical to the received ZIP (sha256 comparison). `PROVENANCE.tsv` gained only the ch06 row. Not edited or rebuilt.
- **Register:** FA-12 and FA-13 added as **required**; FA-14 records the Chapter 6 points; FA-3 gained the `HeadeyPalloni2019` title-case item; an open-item summary table lists every pending item. FA-1, FA-7 A (required) and FA-7 B (open, unresolved), FA-8 A–D (required), FA-9, FA-10 and FA-11 are preserved unchanged.

**Open points carried forward** (author decisions; none changed without approval):
- ch06 A1–A10 to confirm, B1–B13, F1–F6 (FA-14);
- FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus confirmation of A1–A3, B1–B11 and the layout (FA-9);
- FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open question; restricted-data check in local VS Code);
- FA-1 (required);
- FA-3 bibliography and FA-4 xurl items; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-11: page-budget editing deferred to final assembly.

### PDF filename → chapter map (cumulative)

| Downloaded file | Unit | Chapter | Status |
|---|---|---|---|
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction pending** (FA-7 A); open verification question (FA-7 B) |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections pending** (FA-8 A–D, FA-12) |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; points FA-9; **canonical synchronisation required** (FA-13) |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | **awaiting author review**; points FA-14 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic (built before the FA-10 preamble change; re-run at final assembly) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

The seven-character code in each filename is the **publishing** commit at build time, not the academic source (always `c58fc47`).

Page counts are those of separate previews (ch06: 7 body pages plus 1 preview-reference page). They are not a thesis page count. The 40-page main-text maximum is checked only at final assembly (FA-5, FA-11).

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed.
- TeX Live, biber, the fonts, `cabextract` and poppler were installed via apt as in §3; PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86`).
- Pushing to `main` is not attempted. A single push of the session branch `claude/clever-davinci-tn2piv` returned HTTP 403 (the Claude GitHub App has no access to this repository for the organisation); it was not retried. The work is delivered as the cumulative ZIP (13 patches from `c58fc47` plus the `publishing/` tree). To push later, reconnect GitHub / install the Claude GitHub App, or apply the patches locally with `git am`.

## 17. Session log: Chapter 7 (conclusion) preview, 2026-10-14

**Status: Awaiting author review. Do not add ch07 to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` was re-fetched and is unchanged; manifest 15/15 unchanged (checked at the start and before the final build). Canonical chapter `manuscript/v12_2026-10-10/07_conclusion.md`, sha256 `56285b5d4d032583ef3d107cf47dc57197356e033b3ef02ba03121e60348e9e6`, last changed in `5563d33` (contained in `c58fc47`). |
| Package received | `thesis_render_v12_package_68a0363_1.zip` (sha256 `f1b729061dcb7d173a84dd2b4f62a83259c916f4da190e3d965fd3f807a265cf`; ZIP comment `68a03631…`). Restored by `git am --committer-date-is-author-date` of its 14 patches onto `c58fc47`. All 14 commits reproduced the **identical** IDs `e9dc05f` … `804ace9`, `68a0363`. The `publishing/` tree is byte-identical to the ZIP. |
| Branch and local commits | Branch `claude/affectionate-goodall-25j2hx` (the session's designated branch), on `c58fc47`. Package replay `e9dc05f` … `68a0363`. Then `9c15c96f21afc768237e54ea89c10f1ea3cb733f` (ch07 edit, tex, provenance row, change log, word diff). Then a commit adding the preview, its reports and checks, and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| **Local publishing commit vs. academic commit** | The seven-character code in the PDF filename (`9c15c96`) is the **publishing** commit at build time. The academic source is always `c58fc47`. |
| Preview | `builds/previews/REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` (sha256 `37b166e20a013988cd6fe4bd9623da4cbe8452125449f0afb8c00cb1a14d3962`), 4 pages: **body pp. 1–3; preview-only reference list p. 4** (1 work). Also `.report.md`, `.verification.md` and the `.checks/` folder (scripts and logs). |
| Canonical / edited / tex sha256 | `56285b5d4d032583ef3d107cf47dc57197356e033b3ef02ba03121e60348e9e6` / `de7fa76cd09ced590986388a326bb6f87dcc20a4992df1ba37ef69253d72b3f9` / `8d9594374fc234ec0cdd890953e9a5afa09f1d5d555c85960170a13bc4e1c4d2` |
| Edit record | `chapters/changes/07_conclusion.changelog.md`, `07_conclusion.worddiff.txt` |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–ch06 sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. |
| Author instructions recorded | Render the complete chapter, without shortening it or imposing a page target (FA-11). Preserve Chapters 1–6 byte-for-byte and every register item. Record the three Chapter 6 review points (FA-15 A–C). Status "Awaiting author review". Do not approve on the author's behalf, delete earlier files, publish restricted data or overwrite `main`. |

What was done:
- **Evidence review.** The canonical conclusion was read in full and compared with:
  - Chapter 1's research questions, scope, contribution and principal limitations;
  - Chapters 2–6 (publishing copies);
  - the claim–evidence ledger and the v3 reporting map and core reporting table;
  - the stored public CSVs.

  Every empirical statement was checked by named keys (27/27 OK; `verify_ch07.tsv`). No restricted data was accessed, no model was run, and no new result was created.
- **Eight verified corrections in the copy** (change log A1–A8). The most substantive:
  - A1: the headline is the selected cell and one of six nominally significant primary cells, not "one result that stands out";
  - A2: the estimates rely on a working inference about the measured subsample, not on "an undocumented … sampling weight";
  - A3: the historical extension does not extend the household–community comparison;
  - A5: the future-design recommendation is now a design following the same units over successive rounds, because the thesis is already in the repeated-cross-section class.
- **Clarifications B1–B12** restate qualifications from Chapters 1–6 (no new estimates). **Decisions F1–F6** are left for the author.
- **Humanizer.** v2.9.1 was read in full and used for the ch07 publishing copy only.
  - 10 punctuation em dashes replaced; the compound en dash in "water–HAZ" kept.
  - 4 paragraphs → 9, order unchanged; self-evaluative phrases ("transparent", "honestly", "careful accounting") removed.
  - Hedges and the single citation kept.
- **Rendering fix, copy only:** no-break spaces after "Section", "Sections" and "Appendix" (16 places), after "(Section" / "1.2)" broke across lines.
- **Verification of the PDF** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined references; biber 0 warnings;
  - L1 heading gap 39.0 pt;
  - 48/48 sentences in order; 33/33 numbers; 1/1 citation link to its own entry; bookmarks on the right pages;
  - every page of the delivered PDF inspected directly.
- **Shared files:** none changed (template, filter, scripts, drivers, bibliography).
- **Chapters 1–6:** all 53 of their files (md, tex, change logs, word diffs, preview PDFs, reports, verification reports, the ch05 and ch06 `.checks/` folders) and `APPROVED.tsv` are byte-identical to the received ZIP (sha256 taken before the first edit and re-checked after the final build). `PROVENANCE.tsv` gained only the ch07 row. Not edited or rebuilt.
- **Register:** FA-15 A–C (Chapter 6 points) and FA-16 (Chapter 7) added. A status-class block now separates applied copy corrections, pending corrections, canonical synchronisation and unresolved research limitations. FA-1 to FA-14 are preserved unchanged.

**Open points carried forward** (author decisions; none changed without approval):
- ch07 A1–A8 to confirm, B1–B12, F1–F6 (FA-16), including the abstract consistency flags (F4);
- FA-15 A (required), FA-15 B (evidence check), FA-15 C (author decision);
- ch06 A1–A10, B1–B13, F1–F6 (FA-14);
- FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus confirmation of A1–A3, B1–B11 and the layout (FA-9);
- FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open question; restricted-data check in local VS Code);
- FA-1 (required);
- FA-3 bibliography and FA-4 xurl items; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-5 and FA-11: page-budget editing deferred to final assembly.

### PDF filename → chapter map (cumulative)

| Downloaded file | Unit | Chapter | Status |
|---|---|---|---|
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction pending** (FA-7 A); open verification question (FA-7 B) |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections pending** (FA-8 A–D, FA-12) |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; points FA-9; **canonical synchronisation required** (FA-13) |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | awaiting author review; points FA-14; **required wording correction pending** (FA-15 A); evidence check (FA-15 B); completeness question (FA-15 C) |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | 7 Conclusion | **Awaiting author review**; points FA-16 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic (built before the FA-10 preamble change; re-run at final assembly) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

Page counts of the separate previews (body + preview-only reference pages): ch01 6 + 1, ch02 8 + 2, ch03 9 + 1, ch04 9 + 1, ch05 10 + 1, ch06 7 + 1, **ch07 3 + 1**. The body pages sum to 52, but this is **not** a thesis page count. Each preview starts at page 1 and a new page, and final assembly changes the pagination. The 40-page main-text maximum is measured only by `build.py thesis` (FA-5, FA-11), and no claim of compliance is made.

### Inventory of the remaining supporting units (as of this session)

| Unit | Editable source | Rendered so far | Still required |
|---|---|---|---|
| Abstract (`abstract`) | canonical `manuscript/v12_2026-10-10/08_abstract.md` (lint passes). No publishing copy in `chapters/md/` and no `chapters/tex/08_abstract.tex`. | none | `prepare`/`preview abstract`, language and evidence check, author review. Check against FA-16 F4 (phrasings corrected in Chapter 7) and the Chapter 5 and 6 corrections. |
| Title page | `template/titlepage.tex` + `template/metadata.tex` | diagnostic previews only (`TEMPLATE-VERIFICATION_…`) | Author confirmation of personal metadata, and the actual submission month/year (a placeholder now; `thesis --final` refuses while it remains); render in the full `thesis` build. |
| Contents | generated by `\ThesisTableOfContents` in `drivers/thesis-body.tex` (depth 4) | diagnostic only (placeholder headings) | Generate and verify in the full `thesis` build (titles and page numbers against the headings). |
| Consolidated references | one shared `manuscript/v12_2026-10-10/bibliography.bib`, printed once by the driver | per-chapter preview-only lists (labelled, not part of any chapter `.tex`) | Consolidated list exists only after the full `thesis` build; FA-3 bibliography corrections and the FA-4 DOI-break item pending. |
| Appendix A | canonical `appendices/A_variable_definitions_and_sample_flow.md` (lint passes) | none | Preview, verification, author review; uncaptioned tables (§7 known issue); FA-10 check. |
| Appendix B | canonical `appendices/B_model_specifications_and_independent_verification.md` (lint passes) | none | as Appendix A |
| Appendix C | canonical `appendices/C_historical_diagnostics_and_ethiopia.md` (lint passes) | none | as Appendix A |
| Declaration | `template/declaration.tex` (wording copied from v6; compared with the guidelines by the author) | diagnostic only | Place, date and handwritten signature by the author; render in the full `thesis` build. No wording drafted or changed. |

None of these units is complete merely because a template or canonical source exists.

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed. TeX Live, biber, `fonts-texgyre-math`, `cabextract` and poppler were installed via apt (an `apt-get update` was needed first); PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86`).
- Pushing to `main` is not attempted. A single push of the session branch `claude/affectionate-goodall-25j2hx` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"); it was not retried. The work is delivered as the cumulative ZIP (17 patches from `c58fc47` plus the `publishing/` tree). To push later: connect or reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am`.

## 18. Session log: abstract preview, 2026-10-14

**Status: Awaiting author review. Do not add `abstract` to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` re-fetched: unchanged. `build.py manifest` 15/15 unchanged at the start and before the final build. Canonical abstract `manuscript/v12_2026-10-10/08_abstract.md`, sha256 `ec903ca5a0d281dfeb4313b16a14c4132a79f391957c5592e42ca7ae46a3eb44`, last changed in `5563d33` (contained in `c58fc47`). |
| Package received | `thesis_render_v12_package_82d7e65_1.zip` (sha256 `b543fd5d2f585f1fcb247730d5c09aa90989657aee9f357beba55ec2bf9be025`; ZIP comment `82d7e65…`). Restored by `git am --committer-date-is-author-date` of its 17 patches onto `c58fc47`. The `publishing/` tree is **byte-identical** to the ZIP (`diff -r`). The replayed commits got new IDs (`daebb72` … `0c20ec8`) because this container's committer identity differs. A hard reset to replay with the original committer was refused by the session's permission policy, so the replay was kept. Trees are identical, as in the Chapter 2–4 sessions. |
| Branch and local commits | Branch `claude/busy-hamilton-jy2tnh` (the session's designated branch), on `c58fc47`. Package replay `daebb72` … `0c20ec8`. Then: `d2ddabc` (abstract copy, tex, provenance row, word diff, `build.py` title change); `91dd641` (CI line-break fix); `a881337` (restored motivation sentence; the final preview's source); then a commit adding the preview, its reports and checks, the change log and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| **Local publishing commit vs. academic commit** | `a881337` in the PDF filename is the **publishing** commit at build time. The academic source is always `c58fc47`. |
| Unit mapping | Unit `abstract` ← canonical `08_abstract.md` → copy `chapters/md/08_abstract.md` → `chapters/tex/08_abstract.tex` → driver slot before Chapter 1 in `drivers/thesis-body.tex`. Unnumbered (`\section*{Abstract}`). **Not "Chapter 8"**: the thesis has seven chapters, and `08_` is a filename prefix only. |
| Preview | `builds/previews/REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` (sha256 `beea839066ecbdf8ca3c6fe31ccdd83e31a0666ad7d205266c5ed03472b82478`), 3 pages: **abstract body pp. 1–2; preview-only reference page p. 3** (no works cited). Also `.report.md` (`c0ca6c08…14e357f3`), `.verification.md` and `.checks/` (scripts and logs). |
| Canonical / edited / tex sha256 | `ec903ca5a0d281dfeb4313b16a14c4132a79f391957c5592e42ca7ae46a3eb44` / `ba56a2f44f86bb9f92d53c2ce281068dc2eca52f3c3d04248323f5c6e1950def` / `48fdd5de16348d793dd9696bd235f2aab196491229ad62c27e654544e6fd27cc` |
| Edit record | `chapters/changes/08_abstract.changelog.md`, `08_abstract.worddiff.txt` (`2d3c6c59…274f8e`) |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–ch07 sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`, and the template was not changed. The guidelines do not mention an abstract (it is not among the required components), so abstract placement as page 1 remains a publishing choice (R-14a). |
| Author instructions recorded | Verify, polish and render only the abstract. No page target; do not shorten it to save thesis pages (FA-11). Preserve Chapters 1–7 byte-for-byte and every pending register item. Fix flags A–D. Do not label the abstract "Chapter 8". Status "Awaiting author review". Do not approve on the author's behalf, publish restricted data or overwrite `main`. |

What was done:
- **Evidence review.** The canonical abstract was read in full against:
  - the publishing copies of Chapters 1–7 (with their documented corrections);
  - the claim–evidence ledger and the v3 results index, reporting map and core reporting table;
  - Appendix B and the independent-audit records (pass 2 and pass 4);
  - the stored public CSVs.

  Every number and status claim was checked by named keys (48/48 OK; `verify_abstract.tsv`). No restricted data was accessed, no model was run, and nothing was recomputed. **No numerical error was found** in the canonical abstract.
- **Five verified corrections in the copy** (change log A1–A5):
  - A1: PERWEIGHT is used; the documentation gap concerns an anthropometry-specific weight; working inference.
  - A2: "carefully bounded first attempt" → "preliminary, qualified extension".
  - A3: the headline is a selected primary finding, one of six nominally significant cells among 24.
  - A4: 24 cells reproduced vs. 291 estimated; reproduction ≠ causality or multiple-testing robustness.
  - A5: the 59-country parallel is restricted to sanitation, as in Chapter 2 §2.2 and Chapter 6 §6.1.
- **Clarifications B1–B15** restate qualifications from Chapters 1–7 (no new estimates). **Decisions F1–F6** are left for the author, including whether the uncited Headey–Palloni sentence should cite, stay uncited or go (F1).
- **Humanizer.** v2.9.1 was read in full and used for the abstract copy only.
  - One paragraph became five, in the canonical order of argument.
  - Both em-dash pairs were removed; the copy has no em or en dashes.
  - Nothing promotional, no novelty or policy claim, and no new source was added. IPUMS-DHS and IHME were already used and named in Chapters 1 and 3.
  - 440 → 835 words. Nothing substantive was removed: the extension's motivation sentence was restored after a comparison with the canonical text.
- **Rendering fixes, copy only:** no-break spaces in *p*-values and CI brackets; a break allowed between "CI" and "[" (two overfull lines).
- **Shared file changed:** `scripts/build.py` (sha256 `1927f30b…e30410` → `e4676f21…a0d286`). The preview-only reference page of the `abstract` unit is now titled "References cited in the abstract — preview only". Chapter units produce the identical string as before ("this chapter"); no chapter was rebuilt.
  - Template, filter, drivers and bibliography are unchanged.
  - `chapters/md/PROVENANCE.tsv` gained only the `abstract` row (written by `prepare`, which made a byte-identical copy first).
- **Verification of the PDF** (details in `.verification.md`):
  - 0 errors, overfull/underfull boxes, missing glyphs or undefined references;
  - A4; margins 2.5 / ≥ 3.998 cm; 11/19.5 pt; heading 14 pt bold, 39.0 pt gap; only Times New Roman embedded;
  - 33/33 sentences once and in order; every number present; no raw markup; no "Chapter 8"; bookmarks correct;
  - every page of the delivered PDF inspected directly.
- **New template finding (FA-18):** every PDF's text layer maps ";" to U+037E (printed glyph correct). Recorded, not changed.
- **Chapters 1–7:** all 63 of their files (md, tex, change logs, word diffs, preview PDFs, reports, verification reports, `.checks/` folders) and `APPROVED.tsv` are byte-identical to the received ZIP. A sha256 snapshot was taken before the first edit and re-checked after the final build. Not edited or rebuilt.
- **Register:** FA-17 (abstract) and FA-18 (template text layer) added; FA-16 F4 annotated as addressed in the abstract's publishing copy only. FA-1 to FA-16 are otherwise preserved and still open.

**Abstract corrections requiring canonical GitHub synchronisation (author decision, FA-17):** A1–A5 exist only in `chapters/md/08_abstract.md`. They are coupled to Chapter 7's A1, A2 and A4 (FA-16), which are also unsynchronised. Synchronise both or neither, and update `source_manifest.tsv` deliberately (FA-13 procedure).

**Open points carried forward** (author decisions; none changed without approval):
- abstract A1–A5 to confirm, B1–B15, F1–F6 (FA-17); FA-18 (template text layer);
- ch07 A1–A8, B1–B12, F1–F6 (FA-16);
- FA-15 A (required), FA-15 B (evidence check of Chapter 6's "before any model was estimated" against dated design records), FA-15 C (author decision);
- ch06 A1–A10, B1–B13, F1–F6 (FA-14);
- FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus confirmation of A1–A3, B1–B11 and the layout (FA-9);
- FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open question: `hv001`/`v001` vs. `v021` cluster-identifier correspondence, restricted-data check in local VS Code; **unresolved**);
- FA-1 (required);
- FA-3 bibliography and FA-4 xurl items; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-5 and FA-11: page-budget editing deferred to final assembly.

### PDF filename → unit map (cumulative)

| Downloaded file | Unit | Chapter / part | Status |
|---|---|---|---|
| `REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` | abstract | Abstract (unnumbered; first numbered page in the driver, a publishing choice) | **Awaiting author review**; points FA-17 |
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending at final assembly** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction pending** (FA-7 A); open verification question (FA-7 B) |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections pending** (FA-8 A–D, FA-12) |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; points FA-9; **canonical synchronisation required** (FA-13) |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | awaiting author review; points FA-14; **required wording correction pending** (FA-15 A); evidence check (FA-15 B); completeness question (FA-15 C) |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | 7 Conclusion | Awaiting author review; points FA-16 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only (template check) | current diagnostic (built before the FA-10 preamble change; re-run at final assembly) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

Page counts of the separate previews (body + preview-only reference pages): **abstract 2 + 1**, ch01 6 + 1, ch02 8 + 2, ch03 9 + 1, ch04 9 + 1, ch05 10 + 1, ch06 7 + 1, ch07 3 + 1. This is **not** a thesis page count: each preview starts at page 1 on a new page, and final assembly changes the pagination. The 40-page main-text maximum is measured only by `build.py thesis` (FA-5, FA-11). No claim of compliance is made.

### Inventory of the remaining supporting units (as of this session)

| Unit | Editable source | Rendered so far | Still required |
|---|---|---|---|
| Abstract (`abstract`) | `chapters/md/08_abstract.md` (publishing copy) → `chapters/tex/08_abstract.tex` | review-copy preview (this session) | author review (FA-17); canonical synchronisation decision |
| Title page | `template/titlepage.tex` + `template/metadata.tex` | diagnostic previews only | author confirmation of personal metadata and the actual submission month/year; render in the full `thesis` build |
| Contents | `\ThesisTableOfContents` in `drivers/thesis-body.tex` (depth 4) | diagnostic only | generate and verify in the full `thesis` build |
| Consolidated references | `manuscript/v12_2026-10-10/bibliography.bib`, printed once by the driver | per-unit preview-only lists | full `thesis` build; FA-3, FA-4 pending |
| Appendix A / B / C | canonical `appendices/*.md` (lint passes) | none | preview, verification, author review; uncaptioned tables (§7); FA-10 check |
| Declaration | `template/declaration.tex` (wording unchanged; compared with the guidelines by the author) | diagnostic only | place, date and handwritten signature by the author; full `thesis` build. No wording drafted or changed. |

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed. TeX Live, biber, `fonts-texgyre-math`, `cabextract` and poppler were installed via apt (after `apt-get update`); PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86` matched).
- Pushing to `main` is not attempted. Push of the session branch: see the delivery note below.

**Delivery note (abstract session).** A single push of the session branch `claude/busy-hamilton-jy2tnh` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"). It was not retried. Nothing was pushed to any branch, and `main` is untouched. The work is delivered as the cumulative ZIP `thesis_render_v12_package_<commit>.zip` (all patches from `c58fc47`, i.e. the 17 received plus this session's, and the `publishing/` tree). To push later: connect or reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am` onto `c58fc47`.

## 19. Session log: Appendix A preview, 2026-10-14

**Status: Awaiting author review. Do not add `appA` to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` re-fetched: unchanged. `build.py manifest` 15/15 unchanged at the start and before the final build. Canonical appendix `manuscript/v12_2026-10-10/appendices/A_variable_definitions_and_sample_flow.md`, sha256 `bc883e5b4dcc75ed21e63e4bef493a1b301197843c9dec96deef8211490ae528`, last changed in `5563d33` (contained in `c58fc47`); unchanged. |
| Package received | `thesis_render_v12_package_39005d6_1.zip` (sha256 `10170fb0b0ff7250325cb36bb889b1aa5a7db2917f88446c4b37a5b7df0ce9e6`; ZIP comment `39005d69…`, "local publishing commit; academic source c58fc47…"). Restored by `git am --committer-date-is-author-date` of its 22 patches onto `c58fc47`. Commits 1–17 reproduced the identical IDs `e9dc05f` … `82d7e65`; the five abstract-session commits got new IDs (`3e5ba62`, `10991e1`, `c1a2617`, `4c30903`, `7b7aa14`) because this container's committer identity differs. The `publishing/` tree is **byte-identical** to the ZIP (`diff -r`). |
| Branch and local commits | Branch `claude/nifty-einstein-ilvj65` (the session's designated branch), on `c58fc47`. Package replay `e9dc05f` … `7b7aa14`. Then `ea658b844f4fcbf36ea98a41f62e5b61533ce245` (Appendix A copy, tex, provenance row, change log, word diff, filter item 7, build-script preview title). Then a commit adding the preview, its report, verification report and checks, and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| **Local publishing commit vs. academic commit** | `ea658b8` in the PDF filename is the **publishing** commit at build time. The academic source is always `c58fc47`. |
| Unit mapping | Unit `appA` ← canonical `appendices/A_variable_definitions_and_sample_flow.md` → copy `chapters/md/A_variable_definitions_and_sample_flow.md` → `chapters/tex/A_variable_definitions_and_sample_flow.tex` → driver slot after the reference list in `drivers/thesis-body.tex` (`\ThesisAppendixStart`). Numbered **Appendix A**, A.1–A.5, Tables A.1–A.3. Not "Chapter 8". |
| Preview | `builds/previews/REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.pdf` (sha256 `826351ea1a358c4950ad78ffb9388719ea57af43e7afb27484e2f0d668fb9147`), 8 pages: **Appendix A body pp. 1–7; preview-only reference page p. 8** (1 work, `deOnis2006`). Also `.report.md` (`b645f841…cb878`), `.verification.md` and `.checks/` (scripts and logs). |
| Canonical / edited / tex sha256 | `bc883e5b4dcc75ed21e63e4bef493a1b301197843c9dec96deef8211490ae528` / `5cef286b6bd07d56c4c3b9b0eb10ac8a0e6903020e9ddaa91f23c492d88e4427` / `681783a13b8782508864bce34b4a060c8407c119ea7a4a9c723f38b1ac51c100` |
| Edit record | `chapters/changes/A_variable_definitions_and_sample_flow.changelog.md` (`b4ef01b5…87e5c3`), `A_variable_definitions_and_sample_flow.worddiff.txt` (`6678ba76…e31842`) |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–abstract sessions) was read directly. Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. Appendices are outside the 40-page main-text count. |
| Author instructions recorded | Render the entire appendix; no shortening, row removal or page target (FA-11). Preserve Chapters 1–7 and the abstract byte-for-byte; do not edit or rebuild them. Carry forward every register item; record the three abstract review items (FA-21) without applying them. Keep the `hv001`/`v001` vs `v021` question unresolved. Appendix numbering, captions for existing tables, breakable long tables. Status "Awaiting author review". Do not approve, delete earlier files, expose restricted data or overwrite `main`. Render Appendix A only. |

What was done:
- **Verification against the implementation** (details in `.verification.md`; `verify_appA.tsv` 129/129 OK). Definitions were checked directly in the code (63 checks), counts against stored public outputs by named fields (33) with arithmetic reconciliation of mutually exclusive categories and per-country parts (20), statements carried from documented checks (7), and two questions needing restricted data (recorded open). No restricted data was read, no pipeline or model was run, nothing was reclassified or re-sampled, and no new result was produced.
- **No numerical error** in the canonical appendix. 42,052 (A.3 step 3) exists only in the restricted log of `20_validate_pooled_estimate.py`; it is carried, and the copy says so.
- **Six verified corrections in the copy** (change log A1–A6): HAZ/WAZ/WHZ fields, scale and validity rule; WASH sources point to the implementing scripts; full community-exposure definition; `cluster_key` = copy of `IDHSPSU`; exact issue-register pointer; A.5 index statement. **Clarifications B1–B13**; **decisions G1–G7** (FA-19).
- **Captions added to the three existing tables**: Table A.1 (baseline variables), Table A.2 (historical-extension variables), Table A.3 (documentation sources). No table added; all 18 rows and all columns kept. Two 9 pt table notes. Sample flows as numbered lists.
- **Humanizer** (v2.9.1, read in full; applied conservatively): six punctuation em dashes replaced; identifiers, units, scales, rules, counts and qualifications unchanged. 790 → about 2,010 words (verified definitions; nothing removed).
- **Rendering fixes, copy only:** no-break spaces; raggedright blocks for four path-heavy paragraphs (indent restored, widow/club penalties); one rewording for an overfull list line.
- **Shared files changed (FA-20):** `filters/thesis.lua` (appendix tables get a continuation head "Table A.n (continued)"; chapter tables unchanged; the eight earlier units convert byte-identically, `reconvert_earlier_units.tsv`); `scripts/build.py` (appendix previews: reference page "References cited in this appendix — preview only" without the stray dash). Template, drivers and bibliography unchanged. Old versions are in git history (`7b7aa14`).
- **Verification of the PDF:** 0 errors, overfull/underfull boxes, missing glyphs or undefined references; biber 0 warnings; A4, margins 2.5 / 3.998 cm, 11/19.5, 10/15, 9/13.5; headings 14/12 pt bold, 39.0 pt; `pdfcheck_appA.tsv` 31/31 OK (all 80 source blocks present and in order; numbers; captions; continuation heads; notes with their tables; bookmarks; citation link; cross-reference targets); every page of the delivered PDF inspected.
- **Chapters 1–7 and the abstract:** all their files (md, tex, change logs, word diffs, preview PDFs, reports, verification reports, `.checks/` folders), `APPROVED.tsv`, the diagnostic and selftest builds, the template and the drivers are byte-identical to the received ZIP (sha256 snapshot before the first edit, re-checked after the final build). Not edited or rebuilt. `PROVENANCE.tsv` gained only the `appA` row.
- **Register:** FA-19 (Appendix A), FA-20 (shared code), FA-21 (abstract review items A, B required; C author decision) added. FA-1 to FA-18 preserved; FA-7 B unresolved.

**Open points carried forward** (author decisions; none changed without approval):
- Appendix A A1–A6 to confirm, B1–B13, G1–G7 (FA-19), including Chapter 3 §3.2 wording (FA-19 B) and the data-dictionary `v001` row (FA-19 C);
- FA-20 (filter and build-script re-check; ch01 hash caution);
- FA-21 A and B (required abstract wording) and C (cite or remove the 59-country comparison);
- abstract A1–A5, B1–B15, F1–F6 (FA-17); FA-18 (template text layer);
- ch07 A1–A8, B1–B12, F1–F6 (FA-16); FA-15 A (required), B (evidence check), C (author decision);
- ch06 A1–A10, B1–B13, F1–F6 (FA-14); FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus A1–A3, B1–B11 and layout (FA-9); FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open: `hv001`/`v001` vs `v021`, restricted-data check in local VS Code; **unresolved**);
- FA-1 (required); FA-3 bibliography; FA-4 xurl; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-5 and FA-11: page-budget editing deferred to final assembly.

### PDF filename → unit map (cumulative)

| Downloaded file | Unit | Part | Status |
|---|---|---|---|
| `REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` | abstract | Abstract (unnumbered) | Awaiting author review; FA-17; **new review items FA-21** |
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction** (FA-7 A); open question (FA-7 B); wording point FA-19 B |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections** (FA-8 A–D, FA-12) |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; FA-9; **canonical synchronisation required** (FA-13) |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | awaiting author review; FA-14; FA-15 A–C |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | 7 Conclusion | awaiting author review; FA-16 |
| `REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.pdf` | appA | **Appendix A** Variable definitions, sample flow, and authoritative sources | **Awaiting author review**; FA-19, FA-20 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only | current diagnostic (re-run at final assembly; FA-10, FA-20) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

Page counts of the separate previews (body + preview-only reference pages): abstract 2 + 1, ch01 6 + 1, ch02 8 + 2, ch03 9 + 1, ch04 9 + 1, ch05 10 + 1, ch06 7 + 1, ch07 3 + 1, **Appendix A 7 + 1**. These are **not** thesis page counts; each preview starts at page 1. The appendix is outside the 40-page main-text maximum, which is measured only by `build.py thesis` (FA-5, FA-11). No claim of compliance is made.

### Inventory of the remaining supporting units (as of this session)

| Unit | Editable source | Rendered so far | Still required |
|---|---|---|---|
| Appendix A (`appA`) | `chapters/md/A_variable_definitions_and_sample_flow.md` → `chapters/tex/A_variable_definitions_and_sample_flow.tex` | review-copy preview (this session) | author review (FA-19); canonical synchronisation decision |
| Appendix B / C | canonical `appendices/B_…md`, `C_…md` (lint passes) | none | preview, verification, author review; captions for their existing tables; first other units with continuation heads (FA-20) |
| Title page, contents, consolidated references, declaration | as in §18 | diagnostic only | as in §18 |

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed. TeX Live, biber, `fonts-texgyre-math`, `cabextract` and poppler were installed via apt (after `apt-get update`); PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86` matched).
- Pushing to `main` is not attempted. Push of the session branch: see the delivery note below.

**Delivery note (Appendix A session).** A single push of the session branch `claude/nifty-einstein-ilvj65` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"). It was not retried. Nothing was pushed to any branch, and `main` is untouched. The work is delivered as the cumulative ZIP `thesis_render_v12_package_<commit>.zip` (all patches from `c58fc47`, i.e. the 22 received plus this session's, and the `publishing/` tree; the ZIP comment names the final local publishing commit). To push later: connect or reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am` onto `c58fc47`.

## 20. Session log: Appendix B preview, 2026-10-15

**Status: Awaiting author review. Do not add `appB` to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` re-fetched: unchanged. `build.py manifest` 15/15 unchanged at the start and before the final build. Canonical appendix `manuscript/v12_2026-10-10/appendices/B_model_specifications_and_independent_verification.md`, sha256 `0bb6281ace37a772536a64938d50fae9cfa7232e1bbaa988957c3be772f2075f`, last changed in `1621294` (contained in `c58fc47`); unchanged. |
| Package received | `thesis_render_v12_package_5d222d5_1.zip` (sha256 `57b66c25b9d6cde4d374f7656833c1e6df08fd637986732bb712a471bf612aa7`; ZIP comment `5d222d55…`, "local publishing commit; academic source c58fc47…"). Restored by `git am --committer-date-is-author-date` of its 25 patches onto `c58fc47`. All 25 commits reproduced the identical IDs `e9dc05f` … `5d222d5`. The `publishing/` tree is **byte-identical** to the ZIP (`diff -r`). |
| Branch and local commits | Branch `claude/determined-shannon-6b7wn2` (the session's designated branch), on `c58fc47`. Package replay `e9dc05f` … `5d222d5`. Then `2796974a54397c33620fb6384296045fe93a7f07` (Appendix B copy, tex, provenance row). Then a commit adding the preview, its report, verification report and checks, the change log, word diff and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| **Local publishing commit vs. academic commit** | `2796974` in the PDF filename is the **publishing** commit at build time. The academic source is always `c58fc47`. |
| Unit mapping | Unit `appB` ← canonical `appendices/B_model_specifications_and_independent_verification.md` → copy `chapters/md/B_model_specifications_and_independent_verification.md` → `chapters/tex/B_model_specifications_and_independent_verification.tex` → driver slot after Appendix A in `drivers/thesis-body.tex`. Numbered **Appendix B**, B.1–B.4, Tables B.1–B.2. Not "Chapter 9". |
| Preview | `builds/previews/REVIEW-COPY_appB-appendix-B_preview_2026-10-15_2796974.pdf` (sha256 `ebd8b9aafa86e55791f0405b6c3a26ed04efcf88300655783f8b517ce413e821`), 12 pages: **Appendix B body pp. 1–11; preview-only reference page p. 12** (no works cited). Also `.report.md` (`2505a2d1…e81c757`), `.verification.md` (`44925c11…05beb`) and `.checks/` (scripts and outputs). |
| Canonical / edited / tex sha256 | `0bb6281ace37a772536a64938d50fae9cfa7232e1bbaa988957c3be772f2075f` / `99b61c66d1440f2faf49f2cb192d0792c92e49231dce12d76aaa78f7fb9979d6` / `d83b2e1d8e4ebcfe843a59ca078744603e28be0787ad32ac2e12526d58b0e316` |
| Edit record | `chapters/changes/B_model_specifications_and_independent_verification.changelog.md` (`66f242d3…eabe5`), `B_model_specifications_and_independent_verification.worddiff.txt` (`51c1607a…08fb95`) |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, the same file as in the ch02–Appendix A sessions). Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. Appendices are outside the 40-page main-text count. |
| Author instructions recorded | Render the complete appendix; no shortening or page target (FA-11). Preserve Chapters 1–7, the abstract and Appendix A byte-for-byte; do not edit or rebuild them. Carry forward every register item, including the Appendix A review points (Chapter 3 measurement-validity wording; data-dictionary `v001`/`v021`; `hv001`/`v001` vs `v021` unresolved; 42,052 carried) without marking any complete. Distinguish evidence classes A–D; do not rerun models or read restricted data; do not call a same-function rerun independent. Appendix numbering and captions; breakable long tables. Status "Awaiting author review". Do not approve, delete earlier files, expose restricted data or overwrite `main`. Render Appendix B only. |

What was done:
- **Verification against the implementation** (details in `.verification.md`; `verify_appB.tsv` 204/204 OK): code (CODE 75), third-party library source read from the PyPI sdists `linearmodels` 7.0 and `statsmodels` 0.14.6 (LIB 10), stored public outputs by named identifiers (OUTPUT 48) and arithmetic on them (ARITH 29), statements carried from named provenance records (CARRIED 22), restricted-only items recorded open (OPEN 5), guard rails (TEXT 15). No restricted data was read; no model, test or pipeline was run; nothing was re-estimated.
- **Eight verified corrections in the copy** (change log A1–A8): script 17 matched β to 3×10⁻¹⁴ but SE only to a relative 7.5×10⁻¹⁰; Table B.2's 6.7×10⁻⁸ is a difference against a six-decimal constant in script 20 (full-precision 2.4×10⁻¹⁴ via script 21), and the stored unweighted value is 0.4146971 (`m0008`); "lines 209–212" → `fit()` lines 248, 251, 264–265 at `c58fc47`; "fully accounts" and "faithful reconstruction" narrowed; SE reconciliation attributed to the pass-4 record; Step 3 relative figure explained; "machine epsilon" made exact (3 and 1 ulp); `p_value` is one of the 15 compared columns. **No stored number was found to be wrong**; the corrections concern what was compared and how it is described.
- **Clarifications B1–B17**: K counting per estimator (baseline PRIMARY 18, FULL_DUMMY_DF 4,444, region FE with constant and dummies; historical retained non-FE regressors); normal reference (baseline) vs *t*(*G*−1) (historical); the `group_debias` omission as a covariance-setting discrepancy with the algebra displayed; CI and *p* computed explicitly with *t*(*G*−1), not linearmodels' native `df_resid`; the independence scope of the rebuilds (upstream variables shared); coverage of the 291 models (24 primary reproduced; `m0005`, `m0008`; 265 internal only); weight normalisation invariance and equal totals ≠ equal influence; the same-function rerun is not independent; what verification does not establish.
- **Captions** Table B.1 and Table B.2 on the two existing tables (all rows and columns kept); two 9 pt notes; Table B.2 moved to follow the paragraph that announces it; file-name references replaced by Section numbers; code-span formulas set as mathematics (one aligned display).
- **Humanizer** (read in full; applied conservatively): prose em dashes removed (18 lines → 3 separators the converter requires); long sentences split; identifiers, numbers, equations, tolerances and qualifications unchanged. 2,549 → about 4,010 words (verified clarifications; nothing removed).
- **Rendering fixes, copy only:** ragged-right groups for path-heavy paragraphs (19 lines into the margin → 0), no-break spaces, apostrophes after code spans, one rephrasing to stop a hyphenated code word and a widow line.
- **Shared files: none changed.** Template, filter, build script, drivers, bibliography byte-identical. The FA-20 continuation path is in the tex for both tables; no table breaks in this PDF, so it was exercised in a scratch stress test (continuation head and repeated column heads printed; note kept with the last rows; not delivered).
- **Verification of the PDF:** 0 errors, overfull/underfull boxes, missing glyphs or undefined references; A4, margins 2.5 / 3.998 cm, 11/19.5, 10/15, 9/13.5; `pdfcheck_appB.tsv` 52/52 (all 86 source blocks present and in order, formulas, numbers, captions, notes with their tables, bookmarks, fonts, page numbers, cross-reference targets, cited public paths); negative tests failed as intended; **every page of the delivered PDF inspected**.
- **Chapters 1–7, the abstract and Appendix A:** all 122 files of the received package were hashed before the first edit and re-checked after the final build: 121 identical; `chapters/md/PROVENANCE.tsv` differs only by the appended `appB` row (`.checks/earlier_units_unchanged.tsv`). Not edited or rebuilt.
- **Register:** FA-22 added (A–E). FA-1 to FA-21 preserved; FA-7 B unresolved.

**Open points carried forward** (author decisions; none changed without approval):
- Appendix B A1–A8 to confirm, B1–B17, G1–G7 (FA-22 A–E), including Chapter 4 §4.6 wording (FA-22 B) and the local check of the baseline PanelOLS cross-validation (FA-22 D);
- Appendix A A1–A6, B1–B13, G1–G7 (FA-19), including Chapter 3 §3.2 measurement-validity wording (FA-19 B) and the data-dictionary `v001` row (FA-19 C); 42,052 carried from the restricted log;
- FA-20 (filter and build-script re-check; ch01 hash caution); FA-21 A and B (required abstract wording) and C;
- abstract A1–A5, B1–B15, F1–F6 (FA-17); FA-18 (template text layer);
- ch07 A1–A8, B1–B12, F1–F6 (FA-16); FA-15 A (required), B (evidence check), C (author decision);
- ch06 A1–A10, B1–B13, F1–F6 (FA-14); FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus A1–A3, B1–B11 and layout (FA-9); FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open: `hv001`/`v001` vs `v021`, restricted-data check in local VS Code; **unresolved**);
- FA-1 (required); FA-3 bibliography; FA-4 xurl; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-5 and FA-11: page-budget editing deferred to final assembly.

### PDF filename → unit map (cumulative)

| Downloaded file | Unit | Part | Status |
|---|---|---|---|
| `REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` | abstract | Abstract (unnumbered) | Awaiting author review; FA-17; review items FA-21 |
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction** (FA-7 A); open question (FA-7 B); wording point FA-19 B |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections** (FA-8 A–D, FA-12); wording point FA-22 B |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; FA-9; **canonical synchronisation required** (FA-13) |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | awaiting author review; FA-14; FA-15 A–C |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | 7 Conclusion | awaiting author review; FA-16 |
| `REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.pdf` | appA | Appendix A Variable definitions, sample flow, and authoritative sources | awaiting author review; FA-19, FA-20 |
| `REVIEW-COPY_appB-appendix-B_preview_2026-10-15_2796974.pdf` | appB | **Appendix B** Model specifications, inference conventions, and independent verification | **Awaiting author review**; FA-22 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only | current diagnostic (re-run at final assembly; FA-10, FA-20) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

Page counts of the separate previews (body + preview-only reference pages): abstract 2 + 1, ch01 6 + 1, ch02 8 + 2, ch03 9 + 1, ch04 9 + 1, ch05 10 + 1, ch06 7 + 1, ch07 3 + 1, Appendix A 7 + 1, **Appendix B 11 + 1**. These are **not** thesis page counts; each preview starts at page 1. Appendices are outside the 40-page main-text maximum, which is measured only by `build.py thesis` (FA-5, FA-11). No claim of compliance is made.

### Inventory of the remaining supporting units (as of this session)

| Unit | Editable source | Rendered so far | Still required |
|---|---|---|---|
| Appendix A (`appA`) | `chapters/md/A_…md` → `chapters/tex/A_…tex` | review-copy preview (§19) | author review (FA-19); canonical synchronisation decision |
| Appendix B (`appB`) | `chapters/md/B_model_specifications_and_independent_verification.md` → `chapters/tex/B_model_specifications_and_independent_verification.tex` | review-copy preview (this session) | author review (FA-22); canonical synchronisation decision |
| Appendix C | canonical `appendices/C_historical_diagnostics_and_ethiopia.md` (lint passes) | none | preview, verification, author review; captions for its existing tables; continuation heads (FA-20) |
| Title page, contents, consolidated references, declaration | as in §18 | diagnostic only | as in §18 |

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed. TeX Live, biber, `fonts-texgyre-math`, `cabextract` and poppler were installed via apt (after `apt-get update`); PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86` matched).
- `linearmodels` 7.0 and `statsmodels` 0.14.6 sdists (hashes in `.checks/library_sources.sha256`) were downloaded from PyPI only to read their source for the LIB checks; neither was installed or run.
- Pushing to `main` is not attempted. Push of the session branch: see the delivery note below.

**Delivery note (Appendix B session).** A single push of the session branch `claude/determined-shannon-6b7wn2` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"). It was not retried. Nothing was pushed to any branch, and `main` is untouched. The work is delivered as the cumulative ZIP `thesis_render_v12_package_<commit>.zip` (all patches from `c58fc47`, i.e. the 25 received plus this session's, and the `publishing/` tree; the ZIP comment names the final local publishing commit). To push later: connect or reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am` onto `c58fc47`.

## 21. Session log: Appendix C preview, 2026-10-17

**Status: Awaiting author review. Do not add `appC` to `APPROVED.tsv` until the author has done so.**

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (frozen). Remote `main` re-fetched at the start: unchanged. `build.py manifest` 15/15 unchanged at the start and before the final build. Canonical appendix `manuscript/v12_2026-10-10/appendices/C_historical_diagnostics_and_ethiopia.md`, sha256 `a189ffb59b3156d65f6635a4144f28b7fcc2fb9db62f6bc80a251da84ef79ea3`, last changed in `5563d33` (contained in `c58fc47`); unchanged. |
| Package received | `thesis_render_v12_package_0679ac3_1.zip` (sha256 `3e542f48b3ec9adfb9118a978d18e47e98df1b8eea77a6d187f1c38d316d03b3`; ZIP comment `0679ac3f…`, "local publishing commit; academic source c58fc47…"). Restored by `git am --committer-date-is-author-date` of its 29 patches onto `c58fc47`. Commits 1–26 reproduced the identical IDs `e9dc05f` … `2796974`; the last three got the IDs `9959e44`, `5b3063f`, `f16b4a4` (the ZIP comment names `0679ac3`), as expected when the committer identity or date differs. The `publishing/` tree is **byte-identical** to the ZIP (`diff -r`). |
| Branch and local commits | Branch `claude/sharp-brown-y9zp92` (the session's designated branch), on `c58fc47`. Package replay `e9dc05f` … `f16b4a4`. Then `3d0a3a8c04dbd8bc7c1aa07eb7e819fa2ad3c004` (Appendix C copy, tex, provenance row). Then a commit adding the preview, its report, verification report and checks, the change log, word diff and these documents. Patches from `c58fc47` are in the cumulative ZIP. |
| **Local publishing commit vs. academic commit** | `3d0a3a8` in the PDF filename is the **publishing** commit at build time. The academic source is always `c58fc47`. |
| Unit mapping | Unit `appC` ← canonical `appendices/C_historical_diagnostics_and_ethiopia.md` → copy `chapters/md/C_historical_diagnostics_and_ethiopia.md` → `chapters/tex/C_historical_diagnostics_and_ethiopia.tex` → driver slot after Appendix B in `drivers/thesis-body.tex`. Numbered **Appendix C**, C.1–C.4, Tables C.1–C.3. Not "Chapter 10". |
| Preview | `builds/previews/REVIEW-COPY_appC-appendix-C_preview_2026-10-17_3d0a3a8.pdf` (sha256 `8865f5dc9f45502ac2d4f9397c836d6cc2108396baf51116942ed99cb20c8406`), 9 pages: **Appendix C body pp. 1–8; preview-only reference page p. 9** (no works cited). Also `.report.md` (`8ae9d27b…883f6e5`), `.verification.md` and `.checks/` (scripts and outputs). |
| Canonical / edited / tex sha256 | `a189ffb59b3156d65f6635a4144f28b7fcc2fb9db62f6bc80a251da84ef79ea3` / `208f5020a0cbd59231c9aa63ae06807caa3452e55fda00939f549648916cffac` / `1b1f1e8cc277fc218604f6d848490d45deaf525c54c37781bc8b679324cce5e2` |
| Edit record | `chapters/changes/C_historical_diagnostics_and_ethiopia.changelog.md` (`63da01ab…1e0ede`), `C_historical_diagnostics_and_ethiopia.worddiff.txt` (`207c5c19…20b0d`); verification report `…3d0a3a8.verification.md` |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b28b0090eb5a8d82a59fce7383b3569bf5ac6756e0db4dc0d2299ebdb`, the same file as in the ch02–Appendix B sessions) was read directly (text extracted). Its values match `REQUIREMENTS_CHECKLIST.md`; the template was not changed. Appendices are outside the 40-page main-text count. The declaration wording in `template/declaration.tex` matches the guideline text verbatim, and the title-page structure matches the guideline sample. |
| Author instructions recorded | Render the entire appendix; no shortening, row removal or page target (FA-11). Preserve Chapters 1–7, the abstract and Appendices A–B byte-for-byte; do not edit or rebuild them. Carry forward every register item; record the Appendix B §B.1 correction (FA-22 F) and keep FA-22 D unverified without implying any error in the stored baseline estimates; keep FA-7 B unresolved and the 42,052 count carried. Distinguish C1 (invalid/superseded) from C2/C3 (provisional); never pool Ethiopia under an established-date label; do not claim support inquiries were sent or answered. Distinguish evidence classes; do not read restricted data, rerun extraction, re-estimate, change candidate dates or choose a new primary specification. Appendix numbering and captions; breakable long tables. Status "Awaiting author review". Do not approve, delete earlier files, expose restricted data or overwrite `main`. |

What was done:
- **Verification against the implementation** (details in `.verification.md`; `verify_appC.tsv` 197/197 OK): code at `c58fc47` (CODE 39: scripts 06, 10, 12, 14, 16, and 16 at `be71d57`), stored public outputs selected by named identifiers with every identifying field asserted (OUTPUT 58) and arithmetic on them (ARITH 36, including the *t*(G − 1) reconstruction of every displayed CI and *p*-value and the per-10 = 10 × per-point check), statements carried from named provenance records and git metadata (CARRIED 38), restricted-only items recorded open (OPEN 3), guard rails (TEXT 23). No restricted data was read; no extraction, model, test or pipeline was run.
- **No stored number was found to be wrong.** Every coefficient, count and tolerance in the canonical appendix matches its source at the displayed rounding. The exact postnatal eligibility counts in Table C.1 (7,930 / 7,922 / 5,974 / 5,969) are not in any public output; they are carried and labelled as such (FA-23 E).
- **Eight verified corrections in the copy** (change log A1–A8; see the status bullet in §2). **Clarifications B1–B19**: Ethiopia components separated (birth date / interview date / age; exposure values do not depend on the candidate; eligibility does), C2/C3 agreement not independent and not a CI or bound, model IDs with CIs, *p*, N and G in the table notes, what each sensitivity changes and holds fixed, own-eligible samples, weighting, verification coverage (24 + `m0005`, `m0008`; the other 265 internal only, including every other Table C.3 row and all 18 Ethiopia models) and the unresolved research limitations.
- **Captions** Table C.1–C.3 on the three existing tables, in order of appearance (all 12 rows and all columns kept); three 9 pt notes.
- **Humanizer** (v2.9.1, read in full, file sha256 `70938f3c…77b1a`; applied conservatively): three prose em dashes removed; intensifiers removed; long sentences split; the C.2 heading reworded; identifiers, candidate labels, numbers, units and qualifications unchanged. 678 → about 2,940 words (verified clarifications; nothing removed; every canonical number token and code span retained).
- **Rendering fixes, copy only:** ragged-right groups for path-heavy paragraphs (8 lines into the margin → 0); 101 no-break spaces; record-internal "§N" written as "section N" (the lint read "§8" as a thesis cross-reference).
- **Shared files: none changed.** Template, filter, build script, drivers, bibliography byte-identical. The FA-20 continuation path is in the tex for all three tables; no table breaks in this PDF, so it was exercised in a scratch stress test (Table C.3 lengthened: "Table C.3 (continued)" and repeated column heads on the next page; note kept with the last rows; not delivered).
- **Verification of the PDF:** 0 errors, overfull/underfull boxes, missing glyphs or undefined references; A4, margins 2.5 / 3.998 cm, 11/19.5, 10/15, 9/13.5; level-2 headings 39.0 pt before and after; `pdfcheck_appC.tsv` 63/63 (all 72 source blocks present, in order and not duplicated; every number; captions; notes with their tables; bookmarks; fonts; page numbers; minus signs and CI brackets; status labels; cross-reference targets with their content; cited public paths); negative tests failed as intended; **every page of the delivered PDF inspected**.
- **Chapters 1–7, the abstract and Appendices A–B:** all 138 files of the received package were hashed before the first edit and re-checked after the final build (`.checks/earlier_units_unchanged.tsv`); every unit file is identical. Not edited, converted or rebuilt.
- **Register:** FA-22 F and FA-23 (A–G) added. FA-1 to FA-22 E preserved; FA-7 B unresolved; FA-22 D unverified.

**Open points carried forward** (author decisions; none changed without approval):
- Appendix C A1–A8 to confirm, B1–B19 (FA-23 A); Chapter 3 §3.5 wording (FA-23 B); Chapter 5 Table 5.9 Ghana-exclusion label (FA-23 C); candidate-status record §4 (FA-23 D); exact postnatal counts, local check (FA-23 E); dated records for FA-15 B (FA-23 F); layout (FA-23 G);
- **FA-22 F (required):** Appendix B §B.1 "Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged." (application note in the register);
- Appendix B A1–A8, B1–B17, G1–G7 (FA-22 A–E); FA-22 D (baseline PanelOLS cross-validation; **unverified**; no implication of error in the stored baseline estimates);
- Appendix A A1–A6, B1–B13, G1–G7 (FA-19), including Chapter 3 §3.2 measurement-validity wording (FA-19 B) and the data-dictionary `v001` row (FA-19 C); 42,052 carried from the restricted log, not freshly verified;
- FA-20 (filter and build-script re-check; ch01 hash caution); FA-21 A and B (required abstract wording) and C;
- abstract A1–A5, B1–B15, F1–F6 (FA-17); FA-18 (template text layer);
- ch07 A1–A8, B1–B12, F1–F6 (FA-16); FA-15 A (required), B (evidence check), C (author decision);
- ch06 A1–A10, B1–B13, F1–F6 (FA-14); FA-12 and FA-13 (required);
- ch05 E1–E7 (E2 superseded by FA-12), plus A1–A3, B1–B11 and layout (FA-9); FA-8 A–D (required);
- FA-7 A (required) and FA-7 B (open: `hv001`/`v001` vs `v021`, restricted-data check in local VS Code; **unresolved**);
- FA-1 (required); FA-3 bibliography; FA-4 xurl; FA-10 table-macro re-check;
- ch03 points A3–A5; ch01 open points 1–7 (§11); ch02 open points 2–6 (§12);
- FA-5 and FA-11: page-budget editing deferred to final assembly.

### PDF filename → unit map (cumulative)

| Downloaded file | Unit | Part | Status |
|---|---|---|---|
| `REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` | abstract | Abstract (unnumbered) | Awaiting author review; FA-17; review items FA-21 |
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | 1 Introduction | carried forward by the author (`APPROVED.tsv`); open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | 2 Literature review and conceptual framework | reviewed; **required correction pending** (FA-1) |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | 3 Data and variable construction | awaiting author review; **required cross-reference correction** (FA-7 A); open question (FA-7 B); wording points FA-19 B, FA-23 B |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | 4 Empirical strategy | awaiting author review; **five required corrections** (FA-8 A–D, FA-12); wording point FA-22 B |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | 5 Results | awaiting author review; FA-9; **canonical synchronisation required** (FA-13); label point FA-23 C |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | 6 Discussion and limitations | awaiting author review; FA-14; FA-15 A–C |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | 7 Conclusion | awaiting author review; FA-16 |
| `REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.pdf` | appA | Appendix A Variable definitions, sample flow, and authoritative sources | awaiting author review; FA-19, FA-20 |
| `REVIEW-COPY_appB-appendix-B_preview_2026-10-15_2796974.pdf` | appB | Appendix B Model specifications, inference conventions, and independent verification | awaiting author review; FA-22; **required §B.1 correction** (FA-22 F) |
| `REVIEW-COPY_appC-appendix-C_preview_2026-10-17_3d0a3a8.pdf` | appC | **Appendix C** Historical exposure-assignment diagnostics and the Ethiopia provisional analysis | **Awaiting author review**; FA-23 |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` | — | diagnostic text only | current diagnostic (re-run at final assembly; FA-10, FA-20) |
| `TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`, `SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf` | — | diagnostic / selftest text only | superseded / reference |

Page counts of the separate previews (body + preview-only reference pages): abstract 2 + 1, ch01 6 + 1, ch02 8 + 2, ch03 9 + 1, ch04 9 + 1, ch05 10 + 1, ch06 7 + 1, ch07 3 + 1, Appendix A 7 + 1, Appendix B 11 + 1, **Appendix C 8 + 1**. These are **not** thesis page counts; each preview starts at page 1. Appendices are outside the 40-page main-text maximum, which is measured only by `build.py thesis` (FA-5, FA-11). No claim of compliance is made.

### Inventory of the remaining supporting units (as of this session)

| Unit | Editable source | Rendered so far | Still required |
|---|---|---|---|
| Appendix A (`appA`) | `chapters/md/A_…md` → `chapters/tex/A_…tex` | review-copy preview (§19) | author review (FA-19); canonical synchronisation decision |
| Appendix B (`appB`) | `chapters/md/B_…md` → `chapters/tex/B_…tex` | review-copy preview (§20) | author review (FA-22); **FA-22 F (required)**; canonical synchronisation decision |
| Appendix C (`appC`) | `chapters/md/C_historical_diagnostics_and_ethiopia.md` → `chapters/tex/C_historical_diagnostics_and_ethiopia.tex` | review-copy preview (this session) | author review (FA-23); canonical synchronisation decision |
| Title page, contents, consolidated references, declaration | see the next-stage handover below | diagnostic only | full `thesis` build in local VS Code |

### Next-stage handover inventory (final assembly; nothing below was generated in this session)

- **Consolidated references.**
  - Existing sources: one bibliography, `manuscript/v12_2026-10-10/bibliography.bib` (26 entries; 20 keys cited across the eleven publishing copies, `lint --publishing-copies`); Appendices A–C cite none. It is printed once, by `drivers/thesis-body.tex`, before the appendices; the per-unit "References cited … preview only" pages are verification aids and are not the reference list.
  - Pending verified-metadata fixes (FA-3; only from verified records): `LBDWaSH2020` (no volume/pages; stray comma), `SkoufiasVinha2026` (no article number), the Rakotomanana title case, `Cumming2019` (no volume/article number; stray comma), `GerusoSpears2015` (note prints as commentary), `Burgert2013` (plural series name), `deOnis2006` (note field commentary; wrong opening quote), `HeadeyPalloni2019` (title case); the evidence-depth label disagreements between `bibliography_verification_ledger.md` and `citation_map.md`. FA-21 C may add a `HeadeyPalloni2019` citation to the abstract.
  - Rendering work: FA-4 (xurl breaks DOIs mid-word), FA-18 (";" extracted as U+037E), re-run `diagnostic` (FA-10). Chicago author–date via biblatex-chicago (the guidelines recommend Chicago).
- **Title page** (`template/titlepage.tex` + `template/metadata.tex`).
  - Confirmed in this session: the layout matches the guideline sample (title; "Master's Thesis presented to the Department of Economics at the Rheinische Friedrich-Wilhelms-Universität Bonn"; degree line; supervisor; "Submitted in … by"; name; matriculation number); no logo or seal.
  - Not confirmed by any cloud session: the title, author name, matriculation number, supervisor and the degree line "Master of Science (M.Sc.) in Economics" are carried from `AUTHOR_CHECKLIST.md` ("Confirmed metadata", from the author's registration confirmation of 25 June 2026) and were not re-verified against the registration email (not in the repository). The guidelines allow title wording changes only up to five days before the deadline, approved by the supervisor.
  - Missing: the actual submission month and year (placeholder; the 22 October 2026 deadline is not the submission date). `thesis --final` refuses while the placeholder remains.
- **Contents.** Generated by `\ThesisTableOfContents` (depth 4) from the headings of the assembled document in the full `thesis` build, never from preview pages. The guidelines require every chapter and subchapter with its starting page and titles that match the headings exactly; check it after the pending corrections (FA-22 C could change a heading) and include Appendices A–C and the reference list.
- **Declaration** (`template/declaration.tex`, final separate page, numbered). Wording matches the 23 July 2026 guideline text verbatim (re-checked in this session); not changed. Remaining: place, date and the original handwritten signature on the printed copy, supplied by the author. The guidelines also require any approved AI use to be disclosed as agreed with the supervisor; the author reports having discussed AI assistance with the supervisor, and `AUTHOR_CHECKLIST.md` records that this is handled outside this package. No disclosure or declaration wording was drafted.
- **Final assembly** (local VS Code; editable sources are `chapters/md/*.md` → `chapters/tex/*.tex`):
  1. Apply the patches (`git am` onto `c58fc47`) or unpack the ZIP; `build.py env` (Windows Times New Roman) and `manifest`.
  2. Apply the required corrections: FA-1, FA-7 A, FA-8 A–D, FA-12, FA-13, FA-15 A, FA-21 A–B, **FA-22 F**; decide the author items (FA-9, FA-14, FA-16, FA-17, FA-19, FA-21 C, FA-22 A–C and E, FA-23 A–D) and canonical synchronisation.
  3. Local restricted-data checks: FA-7 B (unresolved), FA-22 D (unverified), FA-23 E; evidence check FA-15 B (FA-23 F lists the dated records).
  4. Bibliography step (FA-3) and template items (FA-4, FA-10, FA-18, FA-20).
  5. For each changed unit: `lint` → `preview` → inspect → record hashes; then `lint --publishing-copies`.
  6. `build.py thesis`; check the reported `ThesisEndOfMainText` page against the 40-page **maximum** (not a target); do not change type size, leading or margins to fit (FA-5, FA-11). Inspect the contents page, reference list, appendix continuation pages and the declaration.
  7. The author records approvals in `APPROVED.tsv`, sets the submission month/year, and runs `thesis --final`.

Environment notes for the next cloud session:
- pandoc 3.1.3 was pre-installed. TeX Live, biber, `fonts-texgyre-math`, `cabextract`, poppler and `fonts-liberation` were installed via apt (after `apt-get update`); PyMuPDF, fontTools and scipy via pip.
- Times New Roman 2.82 came from `times32.exe` (SHA-1 `20b79e65…3060` matched; `Times.TTF` sha256 `4e98adef…bbe86` matched).
- Pushing to `main` is not attempted. Push of the session branch: see the delivery note below.

**Delivery note (Appendix C session).** A single push of the session branch `claude/sharp-brown-y9zp92` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"). It was not retried. Nothing was pushed to any branch, and `main` is untouched. The work is delivered as the cumulative ZIP `thesis_render_v12_package_<commit>.zip` (all patches from `c58fc47`, i.e. the 29 received plus this session's, and the `publishing/` tree; the ZIP comment names the final local publishing commit). To push later: connect or reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am` onto `c58fc47`.

## 22. Session log: consolidated references review copy, 2026-10-17

**Status: Awaiting author review.** This is the reference list only. No chapter, appendix or full thesis was rendered, and nothing was added to `APPROVED.tsv`.

| Item | Value |
|---|---|
| Academic source | `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. `git fetch origin main` at the start returned the same commit. `build.py manifest` 15/15 unchanged at the start and at the end. |
| Package received | `thesis_render_v12_package_100f8df_1.zip` (sha256 `12c81ede8ff4e9cf796f05b4341ae27fe2cf6fb960c29bc3a83ead2ba2d98e78`; ZIP comment `100f8dfe…`). Its 32 patches were applied with `git am --committer-date-is-author-date` onto `c58fc47`. The last commit reproduced the identical ID `100f8df`, and the `publishing/` tree was byte-identical to the ZIP. |
| Branch and commits | `claude/determined-tesla-vt6zkk`. `85fb8d8` adds the bibliography copy and the build command. `c613d28` adds the reference-list URL breaks and three issue numbers. The next commit adds the review copy, the reports and these records. |
| **Publishing vs. academic commit** | `c613d28` in the PDF filename is the publishing commit at build time. The academic source is `c58fc47`. |
| Guidelines | The attached 23 July 2026 PDF (sha256 `06c21b2b…9ebdb`, same file as before) was read directly. Values for references: 10 pt / 15 pt, Chicago recommended, "a list of all sources and materials used". |
| Review copy | `builds/previews/REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf`, 2 pages, 20 works, plus `.report.md` and `.checks/` |
| Report | `bibliography/REFERENCES_VERIFICATION.md` (counts, every field change with evidence, safeguards, status reconciliation, open points); `bibliography/field_changes.tsv` |
| Environment | TeX Live 2023 (XeTeX 0.999995), biber 2.19, biblatex-chicago 3.18, pandoc 3.1.3, Python 3.13, PyMuPDF 1.28.2. Times New Roman 2.82 from `times32.exe` (sha256 `db56595e…07ab`, the value in Debian's `ttf-mscorefonts-installer` manifest; SHA-1 `20b79e65…3060`; `Times.TTF` sha256 `4e98adef…bbe86`). |

What was done:
- **Inventory from the actual files.** There are 26 entries and 20 cited keys with 48 occurrences, identical in the eleven `chapters/md` copies, the generated tex and the canonical chapters. No key is missing and none is duplicated. Six reserve entries stay in the `.bib` unprinted. Narrative author mentions all sit beside a citation of the same work. Coverage questions for the author: the abstract's uncited 59-country comparison (FA-21 C), and data and software used without reference entries (FA-24 D).
- **One bibliography for publishing.** `bibliography/bibliography.bib` is a copy of the canonical file with 21 field changes in 13 entries, and every build now reads it. The changes are missing locators for `LBDWaSH2020`, `Cumming2019`, `SkoufiasVinha2026` and `deOnis2006`; issue numbers for `Black2013`, `Victora2008` and `Addae2024`; audit commentary removed from the printed notes of `deOnis2006` and `GerusoSpears2015`; and Chicago headline-style capitalization of cited titles (same words). The canonical file is unchanged; synchronising it is FA-24 F.
- **Evidence limits.** Crossref, PubMed, Europe PMC and publisher pages could not be reached from this container. The network policy refused `api.crossref.org`, and the fetch tool could not resolve hosts. A value was changed only where the project's own earlier primary-check record and an independent search-surfaced record agree. The exception is the `LBDWaSH2020` issue number, which rests on two repository records (FA-24 B). No source PDF was read in this session.
- **Safeguards checked and preserved.** `deOnis2006` keeps its key, its corporate author and the year 2006; the later online date stays in the records, not in print. `GerusoSpears2015` is still the NBER working paper, revised May 2017. `Blom2022` keeps indirect version correspondence, and a record contradiction is noted (FA-24 C). `Momberg2021` initials, `Perez-Heydrich` without an accent, `Colford, Jr., John M.` and the six `Addae2024` authors are unchanged. `Burgert2013` keeps the plural series name, which is the title page's own wording.
- **Status labels.** No evidence-depth label was upgraded. The disagreements between the ledger and the citation map are explained in the report (§8) and left for the author to annotate (FA-24 E).
- **Rendering.** `python scripts/build.py references` (new) prints the list with an explicit key list collected from the publishing copies, never `\nocite{*}`, and uses the same heading and `\printbibliography` call as the thesis driver. The template change is limited to the reference list: URLs break only after "/" and entries are ragged right. Results: 0 errors, 0 overfull or underfull boxes, 0 missing glyphs, biber 0 warnings. `pdfcheck_references.tsv` passed 47/47, including all 16 DOIs printed whole with exact link targets, no audit text, A4, 10/15 pt and the 14 pt bold heading. A negative test on the received inputs fails 15 of those checks as intended. **Both pages were inspected as full-page images.**
- **Preservation.** All 153 files of the received `publishing/` tree were hashed before the first edit and again after the final build (`.checks/earlier_files_unchanged.tsv`). The only files that differ are the ones changed on purpose: `scripts/build.py`, `template/thesis-preamble.tex` and the records (this file, the register, `README.md`, `REQUIREMENTS_CHECKLIST.md`, `SOURCE_MANIFEST.md`). Every chapter and appendix md and tex file, every earlier preview and every change log is identical. `manuscript/`, `docs/`, `sources/`, `scripts/` and `outputs/` show no diff.
- **Register.** FA-3 was carried out in the publishing copy. FA-4 is fixed for the reference list only. FA-24 A–G were added (shared-code re-check, local confirmations, the Blom2022 record, data and software citations, canonical annotations, canonical synchronisation, page-budget note). FA-25 records the three review items: **A** is FA-22 F unchanged; **B** is the exact Ethiopian postnatal counts 7,930 / 7,922 / 5,974 / 5,969, which require a local check against the restricted or aggregate source before final assembly because their presence in the text is not validation; **C** is `m0032` *p* = 0.000807, which should display as ".001", not "< .001", under the declared rule (a display fix; the result is unchanged). FA-1 to FA-23 are preserved and still open; FA-7 B is unresolved and FA-22 D unverified.
- **Humanizer** (`anthropic-skills:humanizer`, read in full) was used only as guidance for the prose of this section and of the report. Titles, names, journals, DOIs, report numbers and keys were not touched by it.

**Open points carried forward:** everything listed under §21, plus FA-24 A–G and FA-25 A–C. Local VS Code actions:
- FA-25 B (restricted counts);
- FA-24 B (primary-record confirmations);
- FA-24 C (Blom2022 PDF check);
- FA-7 B (unresolved);
- FA-22 D (unverified);
- the `diagnostic` re-run with the Windows font (FA-5, FA-24 A).

### PDF filename → unit map (cumulative)

| Downloaded file | Unit | Status |
|---|---|---|
| `REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf` | consolidated references (not a unit) | **Awaiting author review**; FA-3, FA-24, FA-25 |
| `REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.pdf` | abstract | Awaiting author review; FA-17, FA-21 |
| `REVIEW-COPY_ch01-introduction_preview_2026-10-13_740f004.pdf` | ch01 | carried forward by the author; open points §11 |
| `REVIEW-COPY_ch02-literature-review_preview_2026-10-14_b689d34.pdf` | ch02 | reviewed; required correction FA-1 |
| `REVIEW-COPY_ch03-data-and-variables_preview_2026-10-14_9bf1bfa.pdf` | ch03 | awaiting review; FA-7 A/B, FA-19 B, FA-23 B |
| `REVIEW-COPY_ch04-empirical-strategy_preview_2026-10-14_4b7535d.pdf` | ch04 | awaiting review; FA-8 A–D, FA-12, FA-22 B |
| `REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.pdf` | ch05 | awaiting review; FA-9, FA-13, FA-23 C |
| `REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.pdf` | ch06 | awaiting review; FA-14, FA-15 |
| `REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.pdf` | ch07 | awaiting review; FA-16 |
| `REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.pdf` | appA | awaiting review; FA-19, FA-20 |
| `REVIEW-COPY_appB-appendix-B_preview_2026-10-15_2796974.pdf` | appB | awaiting review; FA-22; required FA-22 F (= FA-25 A) |
| `REVIEW-COPY_appC-appendix-C_preview_2026-10-17_3d0a3a8.pdf` | appC | awaiting review; FA-23; FA-25 B and C |
| `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf`, `…_c58fc47.pdf`, `SELFTEST_…_c58fc47.pdf` | — | diagnostic / selftest text only |

The per-unit previews end with preview-only reference pages built from the canonical bibliography as it was then. They are not the thesis reference list, and the consolidated review copy supersedes them for checking references. Pages 1–2 of the review copy are not thesis page numbers; the reference list's place and page count are known only from `build.py thesis`.

**Delivery note (consolidated-references session).** One push of `claude/determined-tesla-vt6zkk` returned HTTP 403 ("Claude doesn't have GitHub access to UBakhodir/thesis-wash-child-nutrition-dhs for your organization"). It was not retried. Nothing was pushed to any branch, and `main` is untouched (still `c58fc47`). The work is delivered as the cumulative ZIP `thesis_render_v12_package_<commit>.zip`. It holds all patches from `c58fc47` (the 32 received plus this session's) and the `publishing/` tree, and its ZIP comment names the final local publishing commit. To push later, reconnect GitHub at https://claude.ai/connect-github and install the Claude GitHub App on the repository, or apply the patches locally with `git am` onto `c58fc47`.
