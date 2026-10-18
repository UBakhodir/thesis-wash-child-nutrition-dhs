# Requirements checklist — rendering package (2026-10-13, revised after the contents-depth correction)

**Source of the requirements, stated plainly.** The attached guideline PDF
(`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`, updated 23 July 2026) was **not available in
this session**: it is not in the repository and no attachment reached the container (searched the whole
file system). The values below come from (a) the task brief for this session, which lists them
explicitly, and (b) `manuscript/v6_2026-10-07/build/preamble.tex`, whose comments record that it was
built from that PDF. The two agree on every value. Items that depend on wording or layout only the PDF
can settle were marked for verification; see the update below. The university's own LaTeX/Word template (Dr. Holger
Gerhardt) is not in the repository either, so the specification is reproduced directly, as the v6 build
did.

**Update (2026-10-13, author-reported).** The author reports that the declaration affirmation and the
title-page structure have been independently compared with the supplied 23 July 2026 guidelines. This
session still could not open that PDF (no attachment reached the container; the university website is
blocked by the container's network policy), so the comparison is recorded as the author's, not
repeated here. The author also clarified that abstract placement and starting chapters on new pages
are publishing choices of this package, not explicit university requirements (R-14a, R-15).

Measured = taken from the built PDF with PyMuPDF (`scripts/pdfcheck.py`) on
`builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf` (every page inspected) and, for the
contents correction, `TEMPLATE-VERIFICATION_2026-10-13_020f721.pdf` (contents page and the pages it
lists inspected; all other pages compared with the earlier build: identical text, pixel differences
≤ 18/255 from glyph anti-aliasing only). All type sizes and spacings are implemented in PostScript points (bp, 1/72 in), the
word-processor unit; TeX points (1/72.27 in) measured 0.36 % small in the first build and were replaced.

| # | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|
| R-01 | A4 paper | `geometry a4paper` | every page 595.28 × 841.89 pt | Measured ✔ |
| R-02 | Margins L 2.5, R 4.0, T 2.8, B 2.8 cm | `geometry`; page number and review line sit in the margins | left edge 2.500 cm; nearest right edge 3.998 cm (0.07 pt glyph overhang of a justified line); no text above 2.8 cm or below 2.8 cm from the edges | Measured ✔ |
| R-03 | Times New Roman | `\setmainfont{Times New Roman}` | embedded: TimesNewRomanPSMT, -BoldMT, -ItalicMT; 0 missing characters | Measured ✔ (see note F1) |
| R-04 | Main text 11 pt, exact 19.5 pt | `\normalsize` = 11bp/19.5bp, `\linespread{1}` | 11 pt lines: most common baseline pitch 19.5 (126 consecutive-line pairs; the other 11 pt gaps are heading, contents and quotation spacing); 35 lines on a full page | Measured ✔ |
| R-05 | Contents and block quotations 15 pt | `\ThesisTocFont`, `quote` hook = 11bp/15bp | contents and quotation lines: pitch 15.0 | Measured ✔ |
| R-06 | Tables, captions, references 10 pt / 15 pt | `\small` = 10bp/15bp for longtable, caption, `\bibfont` | 10 pt pitch 15.0 in tables, captions and reference list | Measured ✔ |
| R-07 | Footnotes and table/figure notes 9 pt / 13.5 pt | `\footnotesize` = 9bp/13.5bp; `ThesisTableNote` environment | footnote and table-note lines: pitch 13.5 | Measured ✔ |
| R-08 | Headings L1 14 bold 39/19.5; L2 12 bold 19.5/19.5; L3 11 bold 9.75/9.75; L4 11 regular 9.75/0; heading baseline 19.5 | `titlesec`, values in bp | baseline gaps: L1→text 39.0 (19.5 after + 19.5 line); L2 39.0 before and after; L3 29.25 / 29.25; L4 29.25 before, 19.5 after (= 0 after); L1 is always at a page top in the diagnostic, so its 39 pt "before" is applied but not measurable there | Measured ✔ (interpretation: "before/after" is space added to the 19.5 pt line pitch, as in a word processor) |
| R-09 | Numbering 1 / 1.2 / 1.2.3 / 1.2.3.4 | LaTeX numbers; converter strips typed numbers and inserts `\ThesisCheckNumber` | diagnostic shows 1, 1.1, 1.1.1, 1.1.1.1, A, A.1; negative tests: a skipped number and a wrong table number both stop the build | Tested ✔ |
| R-10 | Avoid unnecessary 4th-level headings | style exists; `lint` flags any level-4 heading | v12 sources contain none (lint) | ✔ |
| R-11 | No acknowledgements, dedication, logo or seal | none in template or drivers | — | ✔ |
| R-12 | Main text ≤ 40 pages (maximum, not target) | not manipulated: no size/spacing/margin is adjustable per build | `thesis` report prints the last main-text page | **Measured only at final assembly** |
| R-13 | Chicago author–date via BibLaTeX | `biblatex-chicago` (authordate, biber); `ibidtracker=false` so every citation shows author and year | parenthetical, multi-work, narrative `[-@key]` and locator citations resolve; reference list contains only cited works (2 in the diagnostic); no raw `[@…]` in the PDF | Tested ✔; consolidated references review copy (2026-10-17): 20 cited works only, explicit key list, 10/15 measured, DOIs unbroken (FA-24) |
| R-14 | Arabic page 1 after preliminary material | title page and contents unnumbered; `\pagenumbering{arabic}` at first main-text page | diagnostic: cover/title/contents unnumbered, pages 1–10 continuous | Tested ✔ |
| R-14a | Abstract placed as the first numbered page | `drivers/thesis-body.tex` (carried from v6) | — | **Publishing choice, not an explicit university requirement** (author clarification); can be changed in the driver without touching any chapter |
| R-15 | Each chapter starts on a new page | **Removed 2026-10-17**: `\clearpage` no longer separates abstract/ch01–ch07 in `drivers/thesis-body.tex`; chapters flow continuously, each still opening with its own numbered heading. References and each appendix still start on their own page (unaffected; outside the main-text count) | — | **Publishing choice, not an explicit university requirement** (author clarification); removed because it was adding pages to the main-text count once the 40-page maximum became tight (54→46 pages at the first removal) |
| R-16 | Numbering continues through references, appendices, declaration | single document, no counter resets | diagnostic: references p. 8, appendix p. 9, declaration p. 10 | Tested ✔ |
| R-17 | Declaration on final separate page, unsigned | `template/declaration.tex` (`\clearpage`, numbered, blank place/date/signature) | diagnostic final page | Tested ✔; affirmation wording (copied verbatim from v6) **compared with the 23 July 2026 guidelines by the author** (reported 2026-10-13; not repeated in this session). Place, date and handwritten signature remain for the author |
| R-18 | Title page structure and details | `template/titlepage.tex` + `metadata.tex` (values from v6 / AUTHOR_CHECKLIST "Confirmed metadata") | rendered in diagnostic; `thesis --final` refuses while the submission month/year is a placeholder | Structure **compared with the 23 July 2026 guidelines by the author** (reported 2026-10-13). **Still requires author confirmation:** personal metadata (title, name, matriculation number, supervisor, degree line) and the actual submission month/year (not the 22 October 2026 deadline) |
| R-19 | Text per page not increased versus the specification | exact sizes/leading, 35 lines per full page | measured 35 | ✔ |
| R-21 | Contents lists every heading level used, with exact title and starting page | `tocdepth` = 4 (was 2, which hid levels 3–4); level-4 indent added | `020f721` diagnostic: 10 contents entries, levels 1–4, each title and page checked against the heading's actual page; contents still 11/15 | Corrected and verified ✔ |
| R-20 | Use of AI section of the guidelines | not addressed in the template; no disclosure wording drafted | `AUTHOR_CHECKLIST.md` records the existing arrangement | Unchanged by design |

## Notes and deviations

- **F1 — font version.** This container has Times New Roman 2.82 (Microsoft core fonts, sha256 of
  `times.ttf` 4e98adef…bbe86, matching Debian's published checksum). It lacks the Unicode superscripts
  ⁴ ⁵ ⁶ ⁸ ⁻ used in chapters 3, 4 and Appendices B–C; the converter typesets those as ordinary
  superscript digits (`\textsuperscript`), so no glyph is missing. The author's Windows Times New Roman
  is a later version; re-run `diagnostic` locally and compare before the final build.
- **F2 — mathematics.** Times New Roman has no OpenType math table. Letters and digits in formulas are
  taken from Times New Roman; operators, Greek and large symbols from TeX Gyre Termes Math (a Times
  design). This is the closest available configuration, stated here rather than substituted silently.
  fontspec prints four harmless warnings about the missing `ssty` (script-size) feature.
- **F3 — monospace.** Inline file names use Liberation Mono (Courier New on Windows). Whether file
  paths in the prose should stay in a monospaced face is an author decision for the chapter sessions.
- **F5 — table keep logic (Chapter 5 session, 2026-10-14).** `\ThesisTableCaption` now uses
  `\Needspace`, and captions, tables and notes are kept together using heights recorded in the `.aux`
  file. Table notes (9pt/13.5pt, R-07) are unindented. Sizes, leading and margins are unchanged. Measured in
  the ch05 preview: 10 pt table pitch 15.0, 9 pt note pitch 13.5, 11 pt text pitch 19.5. Re-run
  `diagnostic` at final assembly (register FA-10).
- **F6 — appendix tables (Appendix A session, 2026-10-14).** Appendix tables are numbered A.1, A.2, … per appendix (captions added to the existing tables on the author's instruction) and break across pages as `longtable`; the filter gives them a continuation head "Table A.1 (continued)" above the repeated column heads (filter item 7). Rows are not split. Sizes, leading and margins are unchanged (10/15 tables, 9/13.5 notes measured in the Appendix A preview). Chapter tables are unaffected. Register FA-20.
- **F6, Appendix B (Appendix B session, 2026-10-15).** Tables B.1 and B.2 are captioned and numbered in order of appearance; the generated tex carries the continuation head for both. Neither table breaks in the Appendix B preview (Table B.2 is kept whole on p. 4), so the continuation path was exercised only in a scratch stress test (continuation label and repeated heads printed; note kept with the last rows). Measured in the Appendix B preview: A4, left 2.5 cm, right ≥ 3.998 cm, 11/19.5 text, 10/15 tables, 9/13.5 notes. No shared file changed. Register FA-22.
- **F6, Appendix C (Appendix C session, 2026-10-17).** Tables C.1–C.3 are captioned and numbered in order of appearance; the generated tex carries the continuation head for all three. No table breaks in the Appendix C preview, so the continuation path was exercised in a scratch stress test (Table C.3 lengthened; "Table C.3 (continued)" and the repeated column heads printed at the top of the next page; note kept with the last rows; not delivered). The attached 23 July 2026 guidelines (sha256 `06c21b2b…9ebdb`) were read directly in this session; their values match this checklist. Measured in the Appendix C preview: A4, left 2.5 cm, right ≥ 3.998 cm, 11/19.5 text, 10/15 tables and captions, 9/13.5 notes, level-1 heading 14 pt bold, level-2 headings 12 pt bold with 39.0 pt baseline-to-baseline before and after. No shared file changed. Register FA-23.
- **F4 — v6 differences.** The v6 declaration page had no page number; here it is numbered, because
  numbering must continue through the declaration. v6's forced line break in the title left one word
  alone on a line; the title now wraps naturally.
- **Reference list (consolidated-references session, 2026-10-17).** Guideline values for references: 10 pt, 15 pt line spacing (Times New Roman); "a list of all sources and materials used"; Chicago recommended. Measured in `REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf`: A4, left 2.5 cm, right 3.999 cm, entries 10 pt at 15.0 pt pitch, heading 14 pt bold. Publishing choices (not specified by the guidelines): hanging indent 22.0 pt, no extra space between entries, ragged right with URL breaks after "/" only (reference list only), Chicago headline-style titles. Whether data sets and software count as "materials used" that must be listed is open (register FA-24 D).
