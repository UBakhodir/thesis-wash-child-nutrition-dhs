# Consolidated references: verification and change report (2026-10-17)

Scope: the one reference list printed for the whole thesis (abstract, Chapters 1–7, Appendices A–C). No chapter or appendix text was edited, converted or rebuilt. No estimate, sample, control, weight or model was touched. No full thesis PDF was built.

## 1. Inputs actually used

| Item | Value |
|---|---|
| Academic source | `manuscript/v12_2026-10-10/` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78`. `git fetch origin main` in this session returned `c58fc47`; the remote has not advanced. `build.py manifest`: 15/15 canonical inputs unchanged. |
| Publishing package received | `thesis_render_v12_package_100f8df_1.zip`, sha256 `12c81ede8ff4e9cf796f05b4341ae27fe2cf6fb960c29bc3a83ead2ba2d98e78`, ZIP comment `100f8dfe…` ("local publishing commit; academic source c58fc47…"). Its 32 patches were applied with `git am --committer-date-is-author-date` onto `c58fc47`; the last commit reproduced the identical ID `100f8df`, and `publishing/` was byte-identical to the ZIP (`diff -r`). |
| University requirements | `merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf` (Thesis Guidelines, last updated 23.07.2026), sha256 `06c21b2b28b0090eb5a8d82a59fce7383b3569bf5ac6756e0db4dc0d2299ebdb`, the same file as in earlier sessions. Text extracted and read. |
| Publishing commits of this session | `85fb8d8` (bibliography copy, `build.py`), `c613d28` (reference-list URL breaks, three issue numbers), then the commit adding this report, the review copy and the updated records. |

**Requirements vs. choices.** From the guidelines: A4; references at 10 pt with 15 pt line spacing (Times New Roman); level-1 heading 14 pt bold, 39 pt before and 19.5 pt after; "a list of all sources and materials used"; Chicago Manual of Style *recommended*. Not specified by the guidelines, so these are publishing choices: the hanging-indent amount (template: 22.0 pt), entry spacing (0 pt), headline-style title capitalization (Chicago's preferred style; §5), ragged-right setting of the list (§7), and the heading text "References".

## 2. Access limits in this session (read before relying on any "verified" below)

- **Primary registries could not be reached.** `api.crossref.org` was refused by the container's network policy (proxy answered 403). WebFetch could not resolve any host (Crossref, PubMed, Europe PMC, journals.plos.org). No publisher page, registry record or source PDF was opened in this session.
- **What was available:** (a) the project's own dated records of earlier primary checks: `sources/bibliography/bibliography_source_audit.csv` (35 rows), `docs/provenance/bibliographic_citation_audit_v1/v2/v3_2026-10-09.md`, `manuscript/v12_2026-10-10/bibliography_verification_ledger.md` and `citation_map.md`; (b) a web-search tool whose results list pages (PMC, PubMed, publisher, DOAJ, DHS Program, NBER, institutional repositories) and summarise them. Search summaries are secondary evidence. They were used to corroborate values, never as the only basis for a change.
- **Rule applied:** a bibliographic value was changed only when the project's earlier primary-check record and at least one independent search-surfaced record agree. The one exception, the LBDWaSH2020 issue number, is listed in §4 and FA-24 B.
- Source PDFs held by the author (`pdf_filename` column of the audit CSV) are not in the repository and were not read.

## 3. Citation inventory (counted from the actual files)

Method: every `[@key]` and `[-@key]` inside bracketed citations in the eleven publishing copies `chapters/md/*.md` (the rule `build.py lint` uses), cross-checked against `\autocite`/`\textcite` commands in the eleven generated `chapters/tex/*.tex` and against the canonical chapters. Preview drivers, reports and verification documents were not counted. Script: `builds/previews/REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.checks/README.md` describes it; `build.py references` repeats the collection at build time.

| Count | Value |
|---|---|
| Bibliography entries (canonical and publishing copy) | 26, 26 unique keys, 0 duplicates |
| Distinct keys cited | **20** (publishing md = generated tex = canonical chapters) |
| Citation occurrences | **48** (md 48, tex 48, canonical 48) |
| Keys cited but missing from the bibliography | 0 |
| Uncited entries (kept in the `.bib`, not printed) | 6: `Croft2023`, `Gebru2019`, `ICF2012`, `JMP2025`, `Momberg2021`, `UNICEF2025` |
| Units with citations | ch01 (9 occurrences), ch02 (31), ch03 (3), ch06 (3), ch07 (1), Appendix A (1). None in the abstract, ch04, ch05, Appendices B–C. |

These match the earlier reported 26 entries and 20 cited keys; they were recounted, not carried.

**Narrative mentions and coverage.** Every narrative author mention ("Cumming and Cairncross themselves note", "which Geruso and Spears do not study", "Headey and Palloni's") sits next to a citation of the same work in the same paragraph. Items for the author (not changed here):
- The abstract's 59-country comparison is uncited (already FA-21 C; `HeadeyPalloni2019` if cited).
- The guidelines require "a list of all sources and materials used". The thesis names data sets and software without reference entries: the DHS recode files (Ghana 2022, Kenya 2022, Nigeria 2024), the IPUMS-DHS extract, the IHME gridded WASH product (the method paper `LBDWaSH2020` is cited, the data product itself is not), and `statsmodels` / `linearmodels`. Whether and how to cite them, and the citation wording each provider's terms ask for, is an author decision (FA-24 D). No entry was invented.
- The WHO/UNICEF JMP "improved" classification is used in ch02, ch03 and Appendix A without a citation. `JMP2025` exists as an uncited reserve entry; whether it is the right source for the classification is the author's call.

**Publishing vs. canonical bibliography.** Before this session there was one bibliography (`build.py` read the canonical file directly). There are now two files: the canonical file (unchanged, still in the manifest) and the publishing copy `bibliography/bibliography.bib`, which every build reads. They differ only in the 21 field rows of §4.

## 4. Field changes (old → new, with evidence)

Full machine-readable list: `field_changes.tsv` (21 rows, 13 entries). Evidence codes:

| Code | Evidence |
|---|---|
| LBD | Audit CSV S09: `8:e1162-e1185`, "title, journal, volume, and pages all match exactly" (Crossref, recorded 2026-10). Search: Warwick WRAP and UTMB repository records give "8 (9). e1162-e1185" / "8(9): e1162–e1185". **Issue 9 rests on the two repository records only** (not in the CSV). |
| CUM | Audit CSV S10: `17:173`. Search: DOAJ / repository summaries give "BMC Medicine, Volume 17, Article number: 173". |
| SKO | Audit CSV S12: `21(1):e0341218`, "Volume/issue/article number positively verified via Crossref". Search: PLOS article page, PMC12822979 and PubMed 41564084 listed together with "21(1): e0341218". |
| DEONIS | Audit CSV S06: `Suppl 450:76-85`. Search: records citing "Acta Paediatr Suppl 450:76-85, PMID 16817681". |
| ISSUE | Black2013 9890 and Victora2008 9609: audit v1 §2.2 records that Crossref has these issue numbers; search summaries give "382(9890)" and "371 (9609)". Addae2024 3: audit CSV S13 `19(3):e0297698`; search: PMC10977686 / PubMed 38547113 "19(3):e0297698". |
| NOTE / NOTE_GS | Printed note text that was audit commentary, removed (no metadata value changed). The GerusoSpears2015 revision date is kept: audit CSV S18 quotes the PDF title page "May 2015, Revised May 2017". |
| CAP | Capitalization only (§5). A script confirmed that every changed title equals the old one when compared case-insensitively. |

| Key | Field | Old (canonical) | New (publishing copy) | Code |
|---|---|---|---|---|
| LBDWaSH2020 | volume, number, pages | absent (printed a comma straight before the DOI) | 8, 9, e1162--e1185 | LBD |
| Cumming2019 | volume, pages | absent | 17, 173 (article number) | CUM |
| SkoufiasVinha2026 | pages | absent | e0341218 (article number) | SKO |
| deOnis2006 | journal, volume, pages | Acta Paediatrica; no locator | Acta Paediatrica Supplement; 450; 76--85 | DEONIS |
| deOnis2006 | note | "Print/issue year 2006 (Acta Paediatrica supplement 450, April 2006) … not an error in this citation's year field." | removed; the explanation now lives here (§6) and in the canonical ledger | NOTE |
| GerusoSpears2015 | note | "Revised May 2017. This thesis cites this working-paper version specifically; … differs. Page references elsewhere …" | "Revised May 2017" | NOTE_GS |
| Black2013 | number | absent | 9890 | ISSUE |
| Victora2008 | number | absent | 9609 | ISSUE |
| Addae2024 | number | absent | 3 | ISSUE |
| Black2013, Victora2008, Blom2022, deOnis2006, CummingCairncross2016, LBDWaSH2020, Cumming2019, SkoufiasVinha2026, Addae2024, JohnsonJacobBrown2013, Spears2013 | title | sentence case | headline style (same words) | CAP |
| HeadeyPalloni2019 | title | "… Evidence From Subnational …" | "… Evidence from Subnational …" | CAP |

Not changed: every author field, year, DOI, report number and institution; all six uncited entries; the citation keys.

The first commit message of this session (`85fb8d8`) says "18 field changes in 15 entries". The correct count at that commit was 18 rows in **13** entries; with `c613d28` it is 21 rows in 13 entries. The commit was not rewritten.

## 5. Title capitalization

biblatex-chicago 3.18 prints titles exactly as stored (no automatic case conversion; checked in `chicago-authordate.bbx`). The canonical file mixed sentence case (11 cited titles) and headline style (9). The guidelines recommend Chicago, whose preferred style for titles in reference lists is headline style; sentence style is an accepted Chicago option. Search summaries of university Chicago author–date guides point the same way, but the *Manual*'s own wording could not be opened here. Headline style was applied to all 20 cited titles:
- Prepositions, articles and coordinating conjunctions are lower case unless first or after a colon ("from", "among", "with", "and").
- Both parts of hyphenated compounds are capitalized ("Low-Income", "Community-Level"), except after a prefix that cannot stand alone ("Socio-economic").
- Proper nouns, acronyms and numbers are kept ("WHO", "JMP", "DHS", "GPS", "2000–17", "6–23").

Under this rule **Rakotomanana2020 needed no change**, and HeadeyPalloni2019 needed only "From" → "from". If the author prefers sentence style, it is a one-file change to `bibliography.bib`. Apply it to every cited title, not just the two flagged in FA-3.

## 6. Known source-version distinctions (checked, preserved)

| Key | Finding |
|---|---|
| deOnis2006 | Key unchanged. Author `{{WHO Multicentre Growth Reference Study Group}}` (double-braced corporate author, prints and sorts under W). Year 2006 is the supplement issue year (April 2006 per the project's note). The ledger's record that Crossref gives an online "first published" date of 2 January 2007 is preserved here, not printed; it was **not re-checked** this session. No personal authors added. Volume 95 (the Wiley journal volume that some records give for supplement 450) was not added: no record reached in this session states it. |
| GerusoSpears2015 | Still NBER Working Paper 21184, year 2015, with the printed note "Revised May 2017". It was not replaced by the 2018 *AEJ: Applied Economics* article (10(2):125–162, DOI 10.1257/app.20150431; both from the audit CSV). A search result also shows a November 2015 revision (rev1); together with audit v1 ("two earlier 2015 revisions") this agrees with May 2017 being the latest revision. Chapter 2 §2.3 states the version in the text. |
| Blom2022 | Prints the published *JEEM* article (115:102698), the cited version. Claim support stays **indirect version correspondence** to the AfDB working-paper abstract (citation map). Search results again surfaced only press coverage and the working paper. Nothing was upgraded. Open contradiction: the audit CSV row S04 says "Yes (full-text read)" and names a *JEEM* PDF (`1-s2.0-S0095069622000626-main.pdf`), while the ledger says no local PDF of the article exists. Only the author can check this locally (FA-24 C). |
| Momberg2021 | Uncited, not printed. Initials kept as recorded (D. J., B. C., …); no full given names added. |
| PerezHeydrich2013 | "Perez-Heydrich" without an accent, as in the report's own byline (ledger). The DHS Program's recommended citation, as summarised by search, also has no accent. Not changed. |
| Cumming2019 | Colford encoded as `Colford, Jr., John M.` (family, suffix, given), which biber parses correctly. Chicago author–date lists the first seven of more than ten authors, so Colford is not printed in this 22-author entry. "Sundberg, Shelly" (corrected 2026-10-09) is unchanged; search summaries list "John M. Colford Jr." and "Shelly Sundberg" among the authors. |
| Addae2024 | Authors unchanged: Hammond Yaw Addae, Mohammed Sulemana, Taminu Yakubu, Ambrose Atosona, Rafatu Tahiru, Fusta Azupogo. A search summary of the PMC/PubMed record gives the same six names in the same order. The earlier wrong names were not reintroduced. |
| Burgert2013 | Series kept as "DHS Spatial Analysis Reports" 7. The plural is the title page's own wording, quoted verbatim in the audit CSV ("DHS SPATIAL ANALYSIS REPORTS 7"); the DHS publication page URL uses the same series name. FA-3's singular/plural item is closed as **no change, evidence for the plural**. Byline (Clara R. Burgert, Josh Colston, Thea Roy, Blake Zachary) agrees with the search summary. |

## 7. FA-3 items: resolution

| FA-3 item | Result |
|---|---|
| LBDWaSH2020: no volume/pages, stray comma | Fixed (§4); the comma before the DOI is gone. |
| SkoufiasVinha2026: no article number | Fixed (§4). |
| Rakotomanana title case | No change needed under the headline rule (§5). |
| Cumming2019: no volume/article number, stray comma | Fixed (§4). |
| GerusoSpears2015 note reads as commentary | Fixed: note reduced to "Revised May 2017". |
| Burgert2013 plural series name | Kept, evidence in §6. |
| deOnis2006 note commentary and wrong opening quote | Note removed (the wrong quote was inside it). |
| HeadeyPalloni2019 title case | "From" → "from" (§5). |
| Evidence-depth label disagreements | Recorded in §8; canonical records not edited. |
| FA-4 xurl DOI breaks | Fixed **inside the reference list only** (§9). Body text is unchanged; FA-4 stays open for DOIs/URLs in chapter text, if any. |

## 8. Verification-status consistency (ledger vs. citation map)

The two canonical files answer different questions, and part of the apparent conflict comes from that. The ledger's "Verification status" column largely carries the audit CSV's acquisition-stage statement about bibliographic identity. `citation_map.md` records how deeply the passage supporting each claim was read. For claim support, the more conservative citation-map category stands. Nothing was upgraded.

| Key | Ledger | Citation map | Treatment |
|---|---|---|---|
| Victora2008, Gunther2010, Spears2013, Balk2004, JohnsonJacobBrown2013 | "Yes (full-text read)" | Abstract inspected | Claim support: **abstract inspected**. The ledger statement describes acquisition-stage reading without locators. Annotating the ledger is FA-24 E. |
| CummingCairncross2016 | "Yes (full-text read)" | Abstract inspected (title + abstract), dated 2026-10-09 | Correction R15 (2026-10-10, `docs/provenance/independent_audit_resolution_v1_2026-10-10.md`) records a direct fetch of the PMC full-text page (PMC5084825) and quotes passages on the three mechanisms. The record does not say whether those passages are in the abstract or the body. The map was not updated after R15. **Left as "abstract inspected"**; the author can check the quoted passages and update the map (FA-24 E). |
| Blom2022 | "Partial — abstract-level, working paper" (but CSV S04: "Yes (full-text read)", *JEEM* PDF named) | Indirect version correspondence | Indirect correspondence stands; CSV contradiction open (FA-24 C). |
| SkoufiasVinha2026 | "Yes (Crossref-verified …)" | Abstract inspected | No conflict: identity vs. claim depth. |
| Others (12 keys) | consistent | consistent | No change. |

Broad statements in the canonical records that go beyond the evidence:
- The ledger's header calls the audit CSV "independently verified".
- The citation map says "All 48 occurrences were found supported at the evidence depth stated below".

Both are true only at the stated depth: identity fields against registries, and claim support at abstract or passage level as tabulated. Neither establishes that every claim was checked against a full text. This report does not repeat either statement as a general assurance.

**Substantive claim gaps found in this session:** none new. The known limits remain:
- Blom2022's claim rests on the working-paper abstract.
- Seven sources are abstract-level for claim support.
- The abstract's 59-country comparison is uncited (FA-21 C).

The thesis already describes Addae et al. (2024) as a Ghana MICS 2017/18 study (correction R14), which matches the search summary of the article.

## 9. Rendering

- **Build:** `python scripts/build.py references` (new). It collects the cited keys from the eleven publishing copies, writes an explicit `\nocite{…}` list (never `\nocite{*}`), and prints the list with the same `\printbibliography[heading=bibintoc,title={References}]` as `drivers/thesis-body.tex`. It stops if the generated list differs from the collected keys.
- **Template change (scope: reference list only):** `\AtBeginBibliography{\raggedright\def\UrlBreaks{\do\/}\def\UrlBigBreaks{\do\:}}` in `template/thesis-preamble.tex`. The DOI text and link targets are unchanged; no characters are inserted. Body text, tables and notes keep xurl's break-anywhere behaviour. Earlier previews were not rebuilt; FA-24 A records the re-check.
- **Output:** `builds/previews/REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf`, 2 pages, built from a clean tree at `c613d28`.
- **Compiler results:** 0 LaTeX errors, 0 overfull/underfull boxes, 0 missing characters, 0 undefined citations, biber 0 errors / 0 warnings. The four fontspec warnings (script features, a requested glyph feature) are the same kind that earlier preview reports list.
- **Measured** (`pdfcheck_references.tsv`, 47/47 OK):
  - layout: A4; 2.5 cm left / 3.999 cm right margin; entries 10 pt at 15.0 pt pitch (64 of 64 line pairs); heading "References" 14 pt bold;
  - entries: 20, alphabetical, no duplicates; one hanging-indent position (22.0 pt);
  - DOIs: all 16 printed whole on one line, each with exactly one link annotation equal to `https://doi.org/<doi>`; no other links; no spaces in any target;
  - text: no audit vocabulary printed; opening quotes U+201C; "Günther" and "Blössner" intact; Times New Roman only.
- **Negative test:** the same checks run on a scratch build with the received inputs (canonical `.bib`, preamble at `100f8df`) fail 15 checks: split DOIs, printed audit commentary and the wrong opening quote (`negative_test_received_inputs.tsv`).
- **Pages inspected:** both pages of the delivered PDF, viewed as full-page images. The LBDWaSH2020 entry runs across the page break (two lines on p. 2); this is readable and pagination will differ in the thesis. Page numbers in this preview start at 1 and say nothing about the thesis's reference pages or page count.

## 10. Remaining uncertainties

1. No value was re-read in a primary registry or publisher page in this session (§2).
2. LBDWaSH2020 issue 9 rests on two repository records, not on the project's Crossref record (FA-24 B).
3. deOnis2006: the supplement representation follows PubMed's (Acta Paediatrica Supplement 450:76–85). Wiley may present it as *Acta Paediatrica* 95 (S450). The online date of 2 January 2007 was not re-checked.
4. Black2013 is stored as six named authors plus "others". Chicago's more-than-ten rule would print seven names. The seventh author and the byline order were not verified here; one search summary gives a different order from the bibliography. Not changed (FA-24 B).
5. Institution "The DHS Program/ICF" for the 2013 reports. The documents' own imprint, per the DHS recommended citations surfaced by search, is "ICF International, Calverton, Maryland". The ledger already records the anachronism as a consistency choice; left unchanged and recorded as an author decision (FA-24 B).
6. Working papers and reports print their titles in italics (biblatex-chicago `@report`). Some Chicago examples put working-paper titles in quotation marks. Entry types were not changed.
7. Report and working-paper entries have no URLs (DHS reports, NBER). Chicago allows a URL; the project's audit CSV records the URLs. Adding them is optional (FA-24 B).
8. A correct reference list does not establish that every literature claim in the thesis has been independently verified (§8).
