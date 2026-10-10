# Author checklist — administrative and formatting items outside chapter prose (2026-10-07, v6; carried into v12 unchanged)

**Path note (2026-10-10, corrected):** every `build/...` path below refers to `../v6_2026-10-07/build/` specifically. Diagnostic builds and compiling PDFs also exist under `../v3_2026-10-07/build/` through `../v5_2026-10-07/build/`; v6 is referenced here because it is the most recent and most thoroughly verified of the four (32-page main text, 0 LaTeX errors), not because it is the only one that exists — see `MASTER_ASSEMBLY.md`, "Citation processing," for why v7 through this version have no build at all and what a future build must do. These formatting/page-count items were verified against the v6 PDF specifically and have not been re-verified against any later version's prose.

Nothing below is fabricated or assumed anywhere in the chapter text. Supersedes `v5_2026-10-07/AUTHOR_CHECKLIST.md` (unchanged in substance; no new administrative items arose from the v5/v6 passes' source-correction work). Most formatting items below are now **resolved**, using the official university guidelines (`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`) and the author's registration confirmation email (Meldebestätigung, 25 June 2026, Matrikelnummer 50294516), both supplied by the author. Items genuinely still open are marked as such.

## Confirmed metadata (from the registration confirmation email — not inferred, not guessed)

- **Title** (exact, as registered): *"The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa: Evidence from DHS and Geospatial Data."* Used verbatim in `build/titlepage.tex`.
- **Supervisor / first examiner**: Juniorprof. Julia Mink, Ph.D.
- **Submission deadline**: Thursday, 22 October 2026. This is the registered deadline, not necessarily the actual submission date — the two are not assumed equal anywhere in this package.
- **Author**: Bakhodir Izzatulloev, matriculation number 50294516. The full name is taken from the confirmation email's own subject line and university-generated record, not inferred from the email's German salutation ("Sehr geehrter Herr Izzatulloev"), per the author's own instruction not to do so.
- **Degree**: Master of Science (M.Sc.) in Economics, under the MPO Econ examination regulations.

**Author's suggestion for review, not adopted anywhere in the manuscript**: given that every result in this thesis is an association under a cross-sectional design, and the four-country sample is not representative of Sub-Saharan Africa as a region, a title such as *"Household and Community Water and Sanitation Conditions and Child Nutritional Outcomes: Evidence from Four Sub-Saharan African Countries"* would more precisely describe the thesis's actual design and scope. Recorded here only, for the author's and supervisor's discussion; the official guidelines note a title change remains possible up to five days before the submission deadline, with the supervisor's approval communicated to the Examinations Office by the supervisor.

## Formatting — resolved in this pass

- [x] **Page layout**: A4; left/right margins 2.5 cm/4.0 cm (combined 6.5 cm); top/bottom 2.8 cm/2.8 cm (combined 5.6 cm); Times New Roman 11pt, 19.5pt leading for main text (35 lines/page); headings per the guidelines' four levels — all implemented in `build/preamble.tex` and verified by an actual compiling PDF.
- [x] **Page limit**: Master's thesis in Economics, maximum 40 A4 pages of main text (figures/tables/formulas included; table of contents, appendices, references excluded). **Verified main text: 32 pages** (`build/README.md`; grew from 31 in v5 to 32 in v6 when table cells were correctly wrapped instead of left unbounded — see `CORRECTION_LOG.md`). No trimming was needed.
- [x] **Required components**: title page, table of contents, main text, list of references, appendix, signed declaration — all present in `build/main.tex`'s assembly; only the declaration's date and signature are deliberately left blank (see below).
- [x] **No acknowledgements or dedications**: the guidelines state these must **not** be included. None exists in this package (this resolves an item v1/v2 had left as "author's choice" — it is not a choice; it is prohibited).
- [x] **No university seal or logo**: none used anywhere in this package.
- [x] **Page numbering**: Arabic numerals starting at 1 on the first page of the main text (the abstract, immediately after the table of contents); implemented in `build/main.tex`.
- [x] **Citation style**: Chicago author-date, the style the guidelines recommend and state is available via BibLaTeX; implemented via `biblatex` with the `chicago-authordate` style in `build/preamble.tex`, verified working (biber resolved all 20 cited keys with 0 errors).

## Formatting — still open

- [ ] **Exact submission date** for the title page's "Submitted in [month and year] by:" line — cannot be filled in before the thesis is actually finished and submitted; left as a bracketed placeholder in `build/titlepage.tex`, not invented.
- [ ] **Handwritten signature and date** on the declaration page — left blank in `build/declaration.tex` by design; the guidelines require an original handwritten signature on the printed copy (no scans, no electronic signatures), so this cannot be completed in a PDF at all.
- [ ] **Official university LaTeX/Word template** by Dr. Holger Gerhardt was not available locally; `build/preamble.tex` was built directly from the published specification instead (the guidelines explicitly permit this, provided the specification is matched exactly and text-per-page is not increased — verified: this build reproduces the line-spacing/margin combination that yields exactly 35 lines/page).
- [ ] **Hard-copy binding and submission logistics** (professional binding, Einwurfeinschreiben postal submission, etc.) are procedural steps for the author at actual submission time, not something this package can or should prepare.

## Use of AI — explicitly not addressed here, by the author's own instruction

The guidelines' "Use of AI" section exists in the official document but is **not implemented, discussed, or reopened in this package**, per the author's explicit instruction that this has already been discussed and arranged directly with the examination office. No AI-disclosure wording, scope-of-use statement, or related text is drafted anywhere in this package. If this arrangement changes, the exact required wording must come from the supervisor/examination office and be added by the author, not generated here.

## Supervisor-feedback status — unchanged from v2, still accurate

The introduction and literature review are drafted and internally reviewed. **Nothing has been sent to the supervisor; no feedback has been received or incorporated.** See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`. This pass sent no email and submitted nothing.

## Decisions for the author's review, not silently made

- [ ] **Whether to expand the literature review** with the additional verified-but-not-yet-cited sources available in `bibliography.bib` (Momberg 2021, Gebru 2019, and the DHS methodology/JMP/UNICEF reports) — there is room within the 40-page limit (32 of 40 pages used in the v6 build; the current v12 source has not itself been built or page-counted) to do this if desired.
- [ ] **Whether and how to present the historical extension in the main results** vs. moving more of it to an appendix — current treatment follows the empirical package's final reporting map.
- [ ] **Whether to pursue the title-change suggestion above** with the supervisor, and by when (the guidelines' five-day-before-deadline cutoff applies).

## Explicitly not done, and not to be silently added later

- No submission date, examiner name, grade, or confidentiality marking is invented anywhere in this package.
- No supervisor transcript text, confidential working-paper content, or meeting-presentation material is quoted or reproduced in any chapter file.
- No message, chapter, or attachment has been sent to the supervisor, the examination office, or anyone else by this project at any point.
- The diagnostic PDF in `build/` is not represented anywhere as the final submission PDF.

## Quality-review pass still to run before a complete draft

This v3 pass corrected five specific identified problems (`CORRECTION_LOG.md`), re-verified citation resolution via two independent tools (a Python regex check and biber), and produced and verified an actual compiling PDF. A further line-by-line prose-quality pass — checking every in-text number against `claim_evidence_ledger.md` once more after any future edit, checking citation–bibliography correspondence after any future citation is added, checking for internal cross-reference drift against `CROSS_REFERENCE_MAP.md`, and cleaning up the 28 remaining cosmetic overfull-text-box warnings noted in the v6 build's own `build/README.md` (down from the v5 build's 38 — do not cite the earlier v5 figure as the current one) — should be run again immediately before compiling a final submission draft.
