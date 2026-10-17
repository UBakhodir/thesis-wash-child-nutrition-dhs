# Final-assembly register

Created 2026-10-14 in the Chapter 3 session. This file lists corrections and tasks that are **deferred to final assembly** (local VS Code session). Each item stays open until that session applies it and records the result here. Nothing in this file has been applied yet. *Updated in the Chapter 4 session (2026-10-14):* FA-7 (Chapter 3 required cross-reference correction and open `hv001`/`v021` question) and FA-8 (Chapter 4 points) added; FA-1 to FA-6 unchanged except for pointers to FA-7. Still nothing applied. *Updated in the Chapter 5 session (2026-10-14):* FA-8 reclassified on the author's instruction: its four Chapter 4 points are now **required** final-assembly corrections, with exact target strings checked. Added: FA-9 (Chapter 5 points), FA-10 (shared table-macro change in the preamble, re-check at final assembly) and FA-11 (page-budget note: the author's instruction to defer page-budget editing). FA-1 to FA-7 are unchanged. Still nothing from FA-1 to FA-8 applied. *Updated in the Chapter 6 session (2026-10-14):* added FA-12 (**required** cross-chapter correction: narrow the Chapter 4 §4.5 sentence promising per-country components and residual exposure variation for every pooled coefficient), FA-13 (**required** synchronisation of Chapter 5's verified "more than doubles" correction between the publishing copy and the canonical GitHub chapter) and FA-14 (Chapter 6 points); one new bibliography item in FA-3 (`HeadeyPalloni2019` title case). FA-1 to FA-11 are otherwise unchanged and still open. *Updated in the Chapter 7 session (2026-10-14):* added FA-15 (three Chapter 6 review points recorded on the author's instruction: **A**, a required wording correction; **B**, an evidence check; **C**, a discussion-completeness question) and FA-16 (Chapter 7 points, including the abstract consistency flags). FA-1 to FA-14 are unchanged and still open. *Updated in the abstract session (2026-10-14):* added FA-17 (abstract points, including the canonical synchronisation of five verified abstract corrections) and FA-18 (template text-layer item: ";" extracted as U+037E). FA-16 F4 (the abstract consistency flags) is addressed in the abstract's publishing copy only; FA-16 itself stays open. FA-1 to FA-16 are otherwise unchanged and still open. *Updated in the Appendix A session (2026-10-14):* added FA-19 (Appendix A points, including canonical synchronisation of six verified definition/source corrections), FA-20 (shared filter and build-script changes: re-check at final assembly) and FA-21 (three abstract review items recorded on the author's instruction: **A** and **B** required wording corrections, **C** an author decision on the 59-country comparison). FA-1 to FA-18 are unchanged and still open; FA-7 B remains **unresolved**. *Updated in the Appendix B session (2026-10-15):* added FA-22 (Appendix B points: **A** canonical synchronisation of eight verified corrections; **B** Chapter 4 §4.6 wording that the Appendix B copy narrows; **C** title versus content; **D** a local check of the baseline PanelOLS cross-validation; **E** stale line pointers in script docstrings). FA-1 to FA-21 are unchanged and still open; FA-7 B remains **unresolved**; no shared file changed. *Updated in the Appendix C session (2026-10-17):* added FA-22 F (**required** Appendix B §B.1 wording: standard errors, confidence intervals and *p*-values differ; recorded on the author's instruction) and FA-23 (Appendix C points: **A** canonical synchronisation of eight verified corrections; **B** Chapter 3 §3.5 wording on what the Ethiopian interview date is needed for; **C** Chapter 5 Table 5.9 Ghana-exclusion label; **D** the candidate-status record's completion-rule statement; **E** a local check of the exact postnatal eligibility counts; **F** dated records relevant to FA-15 B; **G** layout). FA-1 to FA-22 E are unchanged and still open; FA-7 B remains **unresolved**; FA-22 D remains **unverified**; no shared file changed. *Updated in the consolidated-references session (2026-10-17):* the FA-3 bibliography step was carried out **in a publishing copy of the bibliography** (`bibliography/bibliography.bib`; canonical file unchanged), and FA-4 was addressed **for the reference list only**; see the status notes under FA-3 and FA-4. Added FA-24 (references follow-ups: shared-code re-check, entries to confirm locally, the Blom2022 record contradiction, data and software citations, canonical ledger and citation-map annotations, canonical bibliography synchronisation) and FA-25 (three review items recorded on the author's instruction: **A** Appendix B §B.1 wording, which is FA-22 F; **B** the exact Ethiopian postnatal eligibility counts, a required local check; **C** the `m0032` *p*-value display). FA-1 to FA-23 are otherwise unchanged and still open; FA-7 B remains **unresolved**; FA-22 D remains **unverified**; no chapter or appendix file was edited. **Apart from the FA-3 and FA-4 steps just named, nothing in this register has been applied, and no item is supervisor-approved.**

## FA-1. Chapter 2, §2.4: REQUIRED AT FINAL ASSEMBLY

**Status: required; not applied.** The author chose to continue chapter rendering and to apply this correction at final assembly. Chapter 2 is therefore **reviewed, with a required correction pending**. It is not finalised and not unconditionally approved, and it is not in `chapters/APPROVED.tsv`.

- **File to edit:** `chapters/md/02_literature_review.md` (publishing copy; currently sha256 `a9ceca1ad5baf93494b2a80eac3111d452cdf0f75b9fb596053bc63557b40de9`). Line 27 is the paragraph under "## 2.4 Household versus community exposure".
- **Sentence to replace** (exact text in the publishing copy; it begins "This is a closer and more precise parallel…"):

  > This is a closer and more precise parallel to this thesis's own baseline finding (Section 5.2) that community water and sanitation do not behave identically under full adjustment.

- **Replacement** (exact wording supplied by the author):

  > This study motivates considering water and sanitation separately. Its finding contrasts with this thesis's fully adjusted community HAZ models, which provide no statistically significant evidence of an association for either measure (Section 5.2).

- **Do not touch the similar sentence in §2.2.** §2.2 (line 11) contains "This last finding, a null sanitation–stunting association …, is a closer and more precise parallel to this thesis's own null household- and community-sanitation findings (Section 5) …". That sentence begins differently and is **not** the target.
- **Context check after applying:**
  - The preceding sentence is the Skoufias and Vinha result, so "This study" refers to `SkoufiasVinha2026`.
  - The following sentence ("Neither source's result, however, should be read as confirming this thesis's specific coefficients…") stays unchanged.
- **Canonical source.** In the canonical file, the same sentence continues with ", though neither source's result…". Whether the canonical v12 file is also corrected is the author's decision. The publishing copy is what the thesis build uses.
- **Background:** Chapter 2 changelog item A1 and `HANDOVER.md` §12 open point 1 (Table 5.2: both community measures are null and nearly equal when fully adjusted).
- **Steps at final assembly:**
  1. Apply the replacement.
  2. Run `python scripts/build.py lint ch02`, then `preview ch02`.
  3. Inspect the changed page(s).
  4. Record the new md/tex hashes here and in the Chapter 2 change log.
  5. The author then decides whether ch02 goes into `APPROVED.tsv`.

## FA-2. Chapter 1: carry-forward record (preserved)

`chapters/APPROVED.tsv` row `ch01` (tex `13155ac5…d678e`, 2026-10-14) records the author's decision to carry Chapter 1 forward after review. That is not supervisor approval and not final-submission approval. Chapter 1 open points 1–7 (`HANDOVER.md` §11) remain as recorded. Unchanged in the Chapter 3 session.

## FA-3. Bibliography completeness (one dedicated bibliography step; verified records only)

Do not restart this during chapter rendering. Collected items:

- `LBDWaSH2020`: no volume or pages, which produces a stray comma before the DOI (ch01 point 4).
- `SkoufiasVinha2026`: no article number (ch01 point 4).
- Rakotomanana entry: title in title case (ch01 point 4).
- `Cumming2019`: no volume or article number; stray comma (ch02 point 5).
- `GerusoSpears2015`: the printed note reads as package commentary (ch02 point 5).
- `Burgert2013`: "DHS Spatial Analysis Reports" is plural (ch02 point 5; also visible in the ch03 preview).
- `deOnis2006` (**new in ch03**): the printed entry shows the `note` field's publisher-metadata commentary ("Print/issue year 2006 … not an error in this citation's year field"), and has a wrong opening quotation mark (”first published”).
- `HeadeyPalloni2019` (**new in ch06**): the title prints in title case ("Water, Sanitation, and Child Health: Evidence From Subnational Panel Data in 59 Countries"), unlike the sentence-case titles of the other entries. Correct only from the verified record and the chosen Chicago title-case convention.
- Evidence-depth labels: `bibliography_verification_ledger.md` and `citation_map.md` disagree for Gunther2010, Spears2013, Balk2004 and JohnsonJacobBrown2013 (ch02 point 6). `citation_map.md` row `CummingCairncross2016` predates the R15 check (ch01 point 6).

**Status (consolidated-references session, 2026-10-17): carried out in the publishing copy; canonical synchronisation open (FA-24 F).** All items above were checked; record in `bibliography/REFERENCES_VERIFICATION.md` §7, every field change in `bibliography/field_changes.tsv` (21 rows, 13 entries).
- Fixed in the publishing copy: `LBDWaSH2020` (8 (9): e1162–e1185; the stray comma is gone), `SkoufiasVinha2026` (e0341218), `Cumming2019` (17:173), `GerusoSpears2015` (note reduced to "Revised May 2017"), `deOnis2006` (commentary note and its wrong quotation mark removed; locator Acta Paediatrica Supplement 450:76–85), `HeadeyPalloni2019` ("From" → "from").
- Rakotomanana title: no change needed. Chicago's preferred headline style was applied to all 20 cited titles (case only, same words); Rakotomanana2020 already follows it.
- `Burgert2013`: plural series name **kept**; it is the title page's own wording ("DHS SPATIAL ANALYSIS REPORTS 7", quoted in the audit CSV).
- Evidence-depth labels: **not upgraded**; reconciled in `REFERENCES_VERIFICATION.md` §8. Annotating the canonical ledger and map is FA-24 E.
- Not applied: anything resting on a primary registry that could not be reached in this session (registries blocked; see FA-24 B).

## FA-4. Template item

- xurl breaks DOIs mid-word or mid-number: "htt ps://" in ch01; "…2227.20 / 06.tb02378.x" in ch03. Consider allowing breaks only after "/" and "." in a dedicated template step, then re-run `diagnostic` and re-check every approved unit (ch01 point 5).
- **Status (2026-10-17): addressed for the reference list only.** `template/thesis-preamble.tex` now sets, inside the bibliography, URL breaks only after "/" and ragged-right entries; every DOI in the consolidated references review copy prints whole (checked, `pdfcheck_references.tsv`). The "htt ps://" and "…2227.20 / 06…" examples above came from the per-unit preview reference pages, which use the same bibliography environment and will therefore also change when those units are next built. URLs in body text keep xurl's behaviour. **Open:** re-run `diagnostic` and re-check the units at final assembly (FA-24 A).

## FA-5. Final pagination and page budget

- All preview pagination is provisional. Each preview starts at page 1.
- The 40-page main-text maximum (guidelines, 23 July 2026) excludes the contents, appendices and references. It is measured only by `build.py thesis`, which reports label `ThesisEndOfMainText`. It is a maximum, not a target. Do not change type size, leading or margins to meet it.
- New-page chapters (R-15) and the abstract as page 1 (R-14a) are publishing choices that add pages. Revisit them only if the limit becomes tight.
- Re-run `diagnostic` locally with the Windows Times New Roman before the final build (checklist F1).

## FA-6. Chapter 3 points for author review (from the ch03 session)

Not corrections, and nothing has been decided. See `chapters/changes/03_data_and_variables.changelog.md`, section A:
- A1: leave-one-out grouping key `hv001` vs. fixed-effect key `v021` (now recorded as an open local verification question, **FA-7 B**);
- A2: the §3.9 "described above" cross-reference for singleton exclusions (now a **required** correction, **FA-7 A**);
- A3: "child-year" vs. cluster-year;
- A4: brief items not stated in the chapter;
- A5: the data-dictionary "household census" wording.

## FA-7. Chapter 3: one required correction and one open verification question (recorded in the Chapter 4 session, 2026-10-14)

Recorded on the author's instructions in the Chapter 4 session. Neither item was applied or resolved in that session, and Chapter 3 was not edited or rebuilt. Chapter 3 therefore **has a required correction pending** and is not unconditionally finalised. It remains awaiting author review and is not in `chapters/APPROVED.tsv`.

**A. REQUIRED AT FINAL ASSEMBLY: cross-reference in §3.9** (supersedes FA-6 point A2, which listed this as undecided).

- **File:** `chapters/md/03_data_and_variables.md` (publishing copy; currently sha256 `9f9d9b187abd367c5412b128d55e234e6bb78acb5f18419d851390a9a1a91176`).
- **Replace** "singleton-cluster exclusions described above"
- **with** "singleton-cluster exclusions described in Section 4.5."
- **Location check (done in the Chapter 4 session):** the phrase occurs exactly once, on line 43 under "## 3.9 A documented measurement-universe discrepancy: Nigeria 2018", and is already followed by a full stop ("…described above. These three counts…"). Replace only the words, so that the result reads "…singleton-cluster exclusions described in Section 4.5. These three counts…", with no doubled full stop.
- **Target check (done in the Chapter 4 session):** Section 4.5 of the Chapter 4 publishing copy contains the paragraph "Singleton-cluster treatment, stated separately for each pipeline". The target exists.
- **Steps:** apply → `lint ch03` → `preview ch03` → inspect the changed page → record the new md/tex hashes here and in the Chapter 3 change log.

**B. OPEN LOCAL VERIFICATION QUESTION: `hv001`/`v001` vs. `v021`** (supersedes FA-6 point A1's wording).

- Community exposure is built from Household Recode cluster `hv001` and linked to children through `v001`. Baseline fixed effects and standard-error clustering use `v021` (`country_psu`).
- Whether these correspond one-to-one in every baseline country must be checked with the **restricted baseline data in the local VS Code environment**.
- This is an **unanswered verification question, not a confirmed calculation error**. Nothing in the cloud sessions resolved it, and no chapter may state that it has been resolved.
- Chapter 4 §4.3 (the leave-one-out value differs within a cluster only by the excluded household) depends on the same correspondence; see the Chapter 4 changelog, A5.

## FA-8. Chapter 4: FOUR REQUIRED CORRECTIONS AT FINAL ASSEMBLY (reclassified in the Chapter 5 session, 2026-10-14)

**Status: required; not applied.** In the Chapter 4 session these four points were recorded as awaiting the author's decision (A1 proposed; A2–A3 optional; A4 proposed). In the Chapter 5 session the author instructed that all four are **required final-assembly corrections**. Chapter 4 was **not edited or rebuilt** in that session. It remains **awaiting author review, with required corrections pending**, and is not in `chapters/APPROVED.tsv`.

- **File:** `chapters/md/04_empirical_strategy.md` (publishing copy; sha256 `61f972e3df2346787af5d7654c37f5d96590d3500df178b9741414c70177fa4e`, unchanged since the Chapter 4 session). All targets are in §4.5 "Inference, weighting, and the pooled estimand". Each location below was checked in the Chapter 5 session.

**A. Delete the weighting parenthetical** (line 45, paragraph "**Weighting.**"; occurs exactly once).
- Current: "…so that each country's weights sum to exactly $1$ (equivalently, $N/M$ on average across countries). Here…"
- Required: "…so that each country's weights sum to exactly $1$. Here…" (delete the space and the parenthetical; keep the full stop).
- Reason (author's wording): the displayed baseline normalisation gives country totals of 1; the historical implementation subsequently multiplies by $N/M$. The later sentences on the historical $N/M$ scaling stay unchanged. Evidence: Chapter 4 changelog A1.

**B. State the region-FE inference convention separately** (line 49, paragraph "**Estimator and inference, stated separately for each pipeline…**").
- Required content (author's wording): these models use explicit-dummy WLS, clustered on `country_psu`; their finite-sample correction counts the explicit region dummies and the constant in $K$; confidence intervals and p-values use the normal reference distribution.
- Suggested placement: directly after the sentence ending "…records `use_t: False` for the primary cluster-fixed-effects fits." Suggested sentence (from Chapter 4 changelog A2; it carries exactly that content): "The region-fixed-effects models (Sections 4.1, 4.3 and 4.4) are fitted as weighted least squares with explicit region dummies and clustered on `country_psu`; their finite-sample correction counts the region dummies and the constant in $K$, and their confidence intervals and p-values also use the normal reference distribution."
- Evidence: `run_explicit_wls()` in `14_household_community_wash_models.py`. Stored p-values were recomputed under both references (Chapter 4 changelog A2), and again for all 20 region-FE cells of Tables 5.1–5.3 in the Chapter 5 session (Chapter 5 verification report §3): all are normal-reference.

**C. Describe rank handling separately for the two pipelines** (line 53, paragraph "**Rank and identification are computational properties, not causal ones.**").
- Current: "Any column found to carry no within-group variation (fully absorbed) is dropped and named explicitly, rather than silently producing an unstable coefficient."
- Required content (author's wording): the historical pipeline drops and records absorbed columns; the baseline pipeline stops on rank deficiency, and excludes residence in advance under cluster fixed effects.
- Suggested replacement (Chapter 4 changelog A3): "The historical pipeline drops any fully absorbed column and records it by name; the baseline pipeline stops if the design is rank-deficient, and its only pre-specified exclusion (`residence` under cluster fixed effects) is stated in Section 4.2. Neither pipeline silently reports an unstable coefficient."

**D. Cross-reference** (line 51, paragraph "**Singleton-cluster treatment…**"; "the baseline tables above" occurs exactly once).
- Replace "the baseline tables above" with "the baseline tables in Section 5" (author's wording). Target checked: Section 5 contains the baseline Tables 5.1–5.4.

**Steps at final assembly:**
1. Apply A–D to the publishing copy.
2. Run `python scripts/build.py lint ch04`, then `preview ch04`.
3. Inspect the changed page(s).
4. Record the new md/tex hashes here and in the Chapter 4 change log.

Whether the canonical v12 file is also corrected is the author's decision.

**Page-budget note (FA-5).** The Chapter 4 preview body is 9 pages, plus a 1-page preview-only reference page.

## FA-9. Chapter 5: points from the Chapter 5 session (awaiting author review)

Source: `chapters/changes/05_results.changelog.md` and `builds/previews/REVIEW-COPY_ch05-results_preview_2026-10-14_c1f74e2.verification.md`. Chapter 5 is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `d01694474488ef5e0080f811e40f03c7c577707a76e78e50da67fb976e042c4e`; tex `bdbe2c1f403ace239af307ac910c5a2feaebd2271d79e4605b4f0125eeb9a6c4`.

- **A. Verified corrections already applied to the publishing copy.** The canonical file is unchanged; whether it is also corrected is the author's decision.
  - A1: §5.4 "more than doubles in magnitude" → "grows in absolute size …, from 0.274 … to −0.457". The stored ratio is 1.5–1.7, not > 2.
  - A2: introduction, the CI convention now names Table 5.4 as the exception.
  - A3: the Table 5.9 caption now names the Ghana-exclusion row.
- **B. Clarifications B1–B11** (age bands, df and combined tests; area-average exposure; weighted conditional associations; *t*(*G*−1); verification coverage 24 / 267 / 291; equal totals ≠ equal influence; and others). Each is evidenced in the change log. Author to confirm.
- **C. Layout.**
  - Tables 5.3, 5.5 and 5.6 are in long format, with contents verified identical.
  - The sample notes are now 9/13.5 pt table notes.
  - Age bands are written "0 to 5, …".
- **E. Decisions for the author** (nothing changed):
  - E1: add the stored CIs to Table 5.4?
  - E2: Chapter 4 §4.5 promises per-country residual exposure variation alongside every pooled coefficient; Chapter 5 shows only the pooled 0.43. Add per-country values (stored), or soften the Chapter 4 sentence?
  - E3: model-1 label "Minimally adjusted" (Table 5.2) vs "No controls" (Table 5.4).
  - E4: confirm the reading of the §5.7 final sentence.
  - E5: "six significant digits" vs "to the displayed precision".
  - E6: add the own-eligible Ns to Table 5.8?
  - E7: bold → italics (ch01 open point 3).
- **Cross-chapter consistency checked.**
  - FA-1's replacement text (Chapter 2, "fully adjusted community HAZ models … no statistically significant evidence … for either measure (Section 5.2)") matches Table 5.2: fully adjusted water *p* = .573, sanitation *p* = .894.
  - Chapter 3 §3.6's pointer "Section 5.8" (rural 10 km sensitivity) has its target in Table 5.9.
  - Chapter 1 open point 7 (*p* = .043, Table 5.3) is unchanged.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/05_results.md` → `lint ch05` → `preview ch05` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-10. Shared template: table macros changed in the Chapter 5 session (re-check at final assembly)

`template/thesis-preamble.tex`, sha256 `47360741…c1d3e75` → `7911858b75bc7da6b5b45a0aaf0152058db245225790b7da58f374f8c6106051`.

What changed:
- `\ThesisTableCaption` uses `\Needspace`.
- Captions, tables and notes are kept together using longtable and note heights recorded in the `.aux` file.
- A heading directly followed by a caption requests room for the table.
- A table followed by a note ends with `\penalty10000`.
- Table notes are unindented.

Details are in Chapter 5 changelog D. Chapters 1–4 contain no tables, so their layout cannot change, and they were not rebuilt. **At final assembly:**
1. Re-run `diagnostic` and `selftest` and inspect their tables (the diagnostic has captioned tables).
2. In the full `thesis` build, check the appendix tables, which are uncaptioned and so outside the caption logic.
3. Check that no table is split unexpectedly and that no heading or note is detached.

The mechanism needs the usual three xelatex passes (as in `build.py`), because heights from one pass are used on the next.

## FA-11. Page budget: author's instruction (Chapter 5 session)

The author instructed that the whole chapter be rendered now, without shortening it, removing tables, omitting qualifications or changing formatting to meet a page target. **Page-limit adjustments are deferred until all chapters are ready and assembled in the local VS Code environment.** The Chapter 5 preview has a body of **10 pages (pp. 1–10)**, plus a **1-page preview-only reference page (p. 11)**. These are separate-preview figures, not a thesis page count. The 40-page main-text maximum is measured only by `build.py thesis` (FA-5).

## FA-12. Chapter 4 §4.5 vs. Chapter 5: REQUIRED CROSS-CHAPTER CONSISTENCY CORRECTION (recorded in the Chapter 6 session, 2026-10-14)

**Status: required; not applied.** Recorded on the author's instruction in the Chapter 6 session. It supersedes FA-9 E2, which listed the same point as an undecided option. Chapter 4 was **not edited or rebuilt** in the Chapter 6 session.

- **File:** `chapters/md/04_empirical_strategy.md` (publishing copy; sha256 `61f972e3df2346787af5d7654c37f5d96590d3500df178b9741414c70177fa4e`, unchanged since the Chapter 4 session). Line 47, §4.5, paragraph beginning "The actual estimand is the single common slope…", last sentence. The sentence occurs exactly once (checked in the Chapter 6 session); the canonical file has the same sentence (line 41).
- **Current sentence:**

  > Every pooled coefficient in this thesis is reported alongside its country-specific components and each country's residual exposure variation, so a reader can see which countries actually drive a pooled result rather than inferring equal influence from the weighting description.

- **Why it must change.** Chapter 5 does not display this throughout. Country-specific components are shown for the 24 primary established-date cells (Tables 5.5 and 5.6) but not for the pooled sensitivity coefficients (Tables 5.8 and 5.9). Residual exposure variation is displayed in Chapter 5 only for the pooled water–HAZ model (0.43 percentage points, §5.6). Chapter 4 §4.5 itself gives the three country values for water–HAZ (Kenya 0.20, Nigeria 0.65, Ghana 0.46) and §4.6 the range 0.20–0.88 across countries and products.
- **Required action at final assembly:** narrow the sentence so that it describes only what is actually presented. Do not claim complete coverage, and do not add unverified quantities (stored per-country values exist in `02_core_reporting_table.md`, column E_resid_SD, but adding them to Chapter 5 would be a separate author decision, FA-9 E2).
- **Suggested wording (author to confirm or replace):** "For the primary established-date models, each pooled coefficient is reported alongside its country-specific components (Tables 5.5 and 5.6). Residual exposure variation is reported for the three countries' water–HAZ models in this section and for the pooled water–HAZ model in Section 5.6, and its range across countries and products is given in Section 4.6, so a reader can see which countries drive the headline pooled result rather than inferring equal influence from the weighting description." Every figure this sentence points to exists in the current publishing copies.
- **Steps:** apply (together with FA-8 A–D) → `lint ch04` → `preview ch04` → inspect the changed page → record the new md/tex hashes here and in the Chapter 4 change log. Whether the canonical v12 file is also corrected is the author's decision.

## FA-13. Chapter 5: SYNCHRONISE THE "MORE THAN DOUBLES" CORRECTION WITH THE CANONICAL CHAPTER (required; recorded in the Chapter 6 session)

**Status: required; not applied to the canonical file.** The verified Chapter 5 correction (changelog A1; FA-9 A1) is applied in the publishing copy `chapters/md/05_results.md` (line 79: "…changes sign and grows in absolute size as controls are added sequentially, from 0.274 with no controls to −0.457 once socioeconomic controls are included.") but **not** in the canonical GitHub chapter `manuscript/v12_2026-10-10/05_results.md` (line 59 still reads "…changes sign and more than doubles in magnitude as controls are added sequentially…"; stored ratio 1.546–1.665, `11_nigeria_sign_reversal.csv`).

- **Required at final assembly:** synchronise the two so that the canonical chapter and the publishing copy carry the same corrected statement. Editing the canonical v12 file changes the canonical input hash recorded in `source_manifest.tsv`, so `build.py manifest` will then report a change (and `manifest --write` refuses to overwrite). Update the manifest deliberately as a recorded step, record the new canonical hash, and note it in the Chapter 5 change log.
- This item does not mean Chapter 5 is approved; FA-9 remains open.
- The same consideration applies to the verified Chapter 6 corrections (FA-14 A): they exist only in the publishing copy. Whether the canonical v12 Chapter 6 is synchronised is the author's decision; if the canonical files are being synchronised for Chapter 5, the Chapter 6 corrections should be considered in the same step.

## FA-14. Chapter 6: points from the Chapter 6 session (awaiting author review)

Source: `chapters/changes/06_discussion_and_limitations.changelog.md` and `builds/previews/REVIEW-COPY_ch06-discussion-and-limitations_preview_2026-10-14_bdfebe6.verification.md`. Chapter 6 is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `1f6ba062869ff6915417d5748793e58e63a493b114b1761480f93ec09f16443f`; tex `e1f9f3de16f1aea6b50c6d75139238e5330676e83c3222680e796994c8115ebe`; canonical unchanged (`eefb5594…a45a94`).

- **A. Verified corrections already applied to the publishing copy (author to confirm):** A1 region FE not "only" in the community specification (§6.2 item 4); A2 sanitation parallel restricted to what Tables 5.1–5.2 show (§6.1); A3 "high compliance" moved to the nutrition arm, per Chapter 2 and `citation_map.md` (§6.1); A4 unweighted 0.41 [0.03, 0.80], *p* = .035 reported with 1.03 (§6.1); A5 verification coverage 24 of 291 reproduced, 267 internally checked (§6.1); A6 "the next section" → "Section 7" (§6.6); A7 displacement wording (§6.5); A8 IHME "supplied lower and upper bounds" (§6.5); A9 Ethiopia "provisional sensitivity", not "excluded" (§6.2); A10 residual-variation pointers (§6.5).
- **B. Clarifications B1–B13** (restating qualifications from Chapters 1–5; author to confirm).
- **F. Decisions for the author** (nothing changed): F1 "before any model was estimated" vs. Chapter 5's "before any coefficient was examined"; F2 stored Ghana-and-Kenya overlap-exclusion family (`o002`/`o005`/`o008`, Nigeria only) reported nowhere; F3 §5.4, §5.5 and the negative Ghana sanitation cell not discussed in Chapter 6; F4 covariate examples; F5 no policy passage; F6 "Section N" vs. "Chapter N".
- **Cross-chapter consistency checked in this session:** FA-1's replacement text (Chapter 2 §2.4) is not touched by Chapter 6, which does not cite `SkoufiasVinha2026`. Chapter 6 §6.1's Headey–Palloni and trial descriptions now match Chapter 2 §§2.2–2.3. Chapter 6's pointer to Chapter 3 §3.9 (Nigeria counts) has its target. FA-7 B (`hv001`/`v001` vs. `v021`) is unaffected by Chapter 6 and remains open.
- **Page budget (FA-11):** the Chapter 6 preview body is **7 pages (pp. 1–7)**, plus a **1-page preview-only reference list (p. 8)**. These are separate-preview figures, not a thesis page count.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/06_discussion_and_limitations.md` → `lint ch06` → `preview ch06` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-15. Chapter 6: three review points recorded in the Chapter 7 session (2026-10-14)

Recorded on the author's instruction. **None was applied**, and Chapter 6 was **not edited or rebuilt** in the Chapter 7 session. Chapter 6 remains **awaiting author review** (FA-14) and is not in `chapters/APPROVED.tsv`. Publishing copy `chapters/md/06_discussion_and_limitations.md`, sha256 `1f6ba062869ff6915417d5748793e58e63a493b114b1761480f93ec09f16443f` (unchanged).

**A. REQUIRED WORDING CORRECTION AT FINAL ASSEMBLY (§6.5, residence proxy).** Status: required; not applied.
- **Sentence to replace** (exact text; occurs exactly once in the publishing copy, §6.5, second paragraph; checked in the Chapter 7 session):

  > Any child who moved between that window and the survey date is assigned the exposure of the wrong location, under the primary buffer-average method and under the containing-pixel sensitivity alike.

- **Replacement** (author's exact wording):

  > Children whose survey residence differs from their early-life residence may be assigned an exposure that does not represent their early-life location, under both the primary buffer-average method and the containing-pixel sensitivity.

- **Reason (author):** the original is too absolute. The following sentence ("This is a form of exposure measurement error whose extent in these samples is unknown.") stays unchanged.
- The canonical file has a differently worded sentence (canonical §6.5); whether it is synchronised is the author's decision (see FA-13 on canonical synchronisation).
- **Steps:** apply → `lint ch06` → `preview ch06` → inspect the changed page → record the new md/tex hashes here and in the Chapter 6 change log.

**B. EVIDENCE CHECK AT FINAL ASSEMBLY (§6.4, "before any model was estimated").** Status: open; not checked.
- §6.4 says the 12-month window "was chosen during the design phase, before any model was estimated". Verify this against **dated design records** (for example, dated specification documents in `docs/provenance/` whose dates precede the first estimation run). If those records do not establish it, narrow the wording to what they actually establish.
- Do **not** infer prior specification merely from a statement in another chapter (Chapter 5 §5.6 says "a choice made before any coefficient was examined"; that statement is not itself a dated record).
- Related: FA-14 F1. No record was examined and nothing was concluded in the Chapter 7 session.

**C. DISCUSSION COMPLETENESS (for final review).** Status: open; author decision.
- Decide whether Chapter 6 should briefly discuss three findings already reported in Chapter 5: the Nigeria community-sanitation specification instability (§5.4, Table 5.4), the current-age heterogeneity (§5.5) and the negative Ghana sanitation–HAZ historical cell (Table 5.6).
- These are existing findings. This item does **not** authorise new results, analyses or mechanisms. Any text must keep Chapter 5's qualifications (instability ≠ harm; current-age heterogeneity ≠ developmental mechanism; a negative cell ≠ evidence that sanitation harms children).
- Related: FA-14 F3. The same question arises for Chapter 7 (FA-16 F2).

## FA-16. Chapter 7: points from the Chapter 7 session (awaiting author review)

Source: `chapters/changes/07_conclusion.changelog.md` and `builds/previews/REVIEW-COPY_ch07-conclusion_preview_2026-10-14_9c15c96.verification.md`. Chapter 7 is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `de7fa76cd09ced590986388a326bb6f87dcc20a4992df1ba37ef69253d72b3f9`; tex `8d9594374fc234ec0cdd890953e9a5afa09f1d5d555c85960170a13bc4e1c4d2`; canonical unchanged (`56285b5d…48e9e6`).

- **A. Verified corrections already applied to the publishing copy (author to confirm):**
  - A1: "one result that stands out" → selected headline; six of 24 primary cells *p* < .05;
  - A2: "rests on an undocumented measurement-subsample sampling weight" → working inference; anthropometry-specific weight not located;
  - A3: the historical extension does not extend the household-versus-community comparison (Ch. 1 §1.5);
  - A4: "first attempt" → "preliminary attempt";
  - A5: future "panel or repeated-cross-section design" → a design following the same geographic units over successive rounds;
  - A6: "extending to all four countries" → validating the Ethiopian date conversion;
  - A7: it is the baseline–historical contrast that cannot be attributed to timing;
  - A8: the early-life measure covers three countries; Ethiopia provisional.
- **Canonical synchronisation (not done):** A1–A8 exist only in the publishing copy. Whether `manuscript/v12_2026-10-10/07_conclusion.md` is synchronised is the author's decision. If it is, update the manifest deliberately, as FA-13 describes.
- **B. Clarifications B1–B12** (restating qualifications from Chapters 1–6; author to confirm).
- **F. Decisions for the author** (nothing changed):
  - F1: joint-model household water *p* = .043 not mentioned (cf. ch01 open point 7);
  - F2: §5.4 and §5.5 findings not mentioned (cf. FA-15 C);
  - F3: "Section N" vs. "Chapter N";
  - F4: **abstract consistency** (see below);
  - F5: "promising" removed;
  - F6: no new future-research direction added.
- **F4, abstract consistency (check when the abstract is rendered).** The canonical `08_abstract.md` (not rendered; unchanged) contains "an undocumented measurement-subsample sampling weight" (cf. A2) and "a carefully bounded first attempt" (cf. A4). It also reports the headline cell without saying that six of 24 primary cells are nominally significant (cf. A1). These are flags for the abstract session, not corrections applied. *Abstract session (2026-10-14):* all three flags were corrected in the abstract's **publishing copy** (`chapters/md/08_abstract.md`, changelog A1–A3; see FA-17). The canonical `08_abstract.md` is unchanged.
- **Page budget (FA-11):** the Chapter 7 preview body is **3 pages (pp. 1–3)**, plus a **1-page preview-only reference list (p. 4)**. These are separate-preview figures, not a thesis page count.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/07_conclusion.md` → `lint ch07` → `preview ch07` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-17. Abstract: points from the abstract session (awaiting author review)

Source: `chapters/changes/08_abstract.changelog.md` and `builds/previews/REVIEW-COPY_abstract-abstract_preview_2026-10-14_a881337.verification.md`. The abstract is the unnumbered `abstract` unit, not a chapter. It is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `ba56a2f44f86bb9f92d53c2ce281068dc2eca52f3c3d04248323f5c6e1950def`; tex `48fdd5de16348d793dd9696bd235f2aab196491229ad62c27e654544e6fd27cc`; canonical unchanged (`ec903ca5…eb44`).

- **A. Verified corrections applied to the publishing copy (author to confirm):**
  - A1: "an undocumented measurement-subsample sampling weight" → PERWEIGHT is used; no official documentation of an anthropometry-specific weight could be located; working inference; weighted conditional associations among eligible measured children;
  - A2: "a carefully bounded first attempt" → "a preliminary, qualified extension" (no priority claim);
  - A3: the headline is the selected primary finding, one of six nominally significant cells among 24 primary cells, with no multiplicity adjustment;
  - A4: verification coverage: 24 primary cells reproduced with a second library on a rebuilt sample; the other 267 of 291 internally checked and, apart from two unweighted counterparts, not re-estimated; reproduction ≠ causality or multiple-testing robustness;
  - A5: the 59-country (Headey–Palloni) parallel restricted to the null sanitation results, as in Chapter 2 §2.2 and Chapter 6 §6.1.
- **Canonical synchronisation (not done; author decision, as for FA-14 A and FA-16 A):** A1–A5 exist only in the publishing copy. If `manuscript/v12_2026-10-10/08_abstract.md` is synchronised, update `source_manifest.tsv` deliberately as FA-13 describes. A1–A3 correspond to the FA-16 F4 flags and to Chapter 7's corrections A2, A4 and A1, so synchronising Chapter 7 without the abstract (or the reverse) would leave the canonical files inconsistent.
- **B. Clarifications B1–B15** (restating qualifications from Chapters 1–7; author to confirm).
- **F. Decisions for the author** (nothing changed): F1 the Headey–Palloni sentence has no citation command (keep uncited / add `[@HeadeyPalloni2019]` / remove); F2 five paragraphs and 835 words (canonical: one paragraph, 440 words); F3 the joint-model *p* = .043 not mentioned (cf. FA-16 F1); F4 baseline sample sizes not stated; F5 IPUMS-DHS and IHME now named; F6 placement as the first numbered page is a publishing choice (R-14a); the guidelines list no abstract among the required components, and under the current driver the abstract counts toward the main-text pages.
- **Page budget (FA-11):** abstract body **2 pages (pp. 1–2)**, plus a **1-page preview-only reference page (p. 3)** stating that no works are cited. These are separate-preview figures, not a thesis page count.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/08_abstract.md` → `lint abstract` → `preview abstract` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-18. Template item: semicolon text-layer mapping (found in the abstract session)

- In every preview PDF and both diagnostic PDFs, the text layer maps the semicolon glyph to U+037E (GREEK QUESTION MARK) instead of U+003B. Counts: ch01 11, ch02 6, ch03 18, ch04 11, ch05 25, ch06 11, ch07 3, abstract 4, diagnostics 26 each; no U+003B anywhere.
- The printed glyph is correct. Copy-and-paste, PDF search and accessibility tools receive U+037E.
- The likely cause is the Times New Roman 2.82 cmap, which maps the glyph to both code points. This is not verified here.
- **At final assembly:** check whether the author's Windows Times New Roman shows the same mapping (FA-5 local `diagnostic` re-run). If it does, consider a dedicated template step, then re-run `diagnostic` and re-check every unit. Nothing was changed in this session; Chapters 1–7 were not rebuilt.

## FA-19. Appendix A: points from the Appendix A session (awaiting author review)

Source: `chapters/changes/A_variable_definitions_and_sample_flow.changelog.md` and `builds/previews/REVIEW-COPY_appA-appendix-A_preview_2026-10-14_ea658b8.verification.md`. Appendix A (`appA`) is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `5cef286b6bd07d56c4c3b9b0eb10ac8a0e6903020e9ddaa91f23c492d88e4427`; tex `681783a13b8782508864bce34b4a060c8407c119ea7a4a9c723f38b1ac51c100`; canonical unchanged (`bc883e5b…0ae528`).

- **A. Verified corrections applied to the publishing copy only (author to confirm; canonical synchronisation is the author's decision, FA-13 procedure):**
  - A1: HAZ/WAZ/WHZ source and validity rule (`hw70`–`hw72`, ×100 stored, ÷ 100 once, special codes 9996–9999 and system-missing → missing, bounds are a validation check);
  - A2: WASH rows' authoritative source = implementing scripts (not `docs/empirical_strategy.md` §2, which uses "household census" wording);
  - A3: community definition (unweighted LOO among other sampled, classifiable HR households; exclusions; 0–1; missing rule; not a census; not an average over children);
  - A4: `cluster_key` is a copy of `IDHSPSU`, not a separately built composite key;
  - A5: issue-register pointer made exact; A6: A.5 index statement limited to what the index files show.
- **B.** Clarifications B1–B13 (verified restatements of code, stored outputs and Chapters 3–5). **C.** Captions Table A.1–A.3 added to the three existing tables (no table added; all rows and columns kept); flows as numbered lists. **D.** Layout: no-break spaces; raggedright blocks around four path-heavy paragraphs.
- **B (register). Chapter 3 §3.2 wording (author decision).** Chapter 3 states two conditions ("flagged valid … and … within the … measurement universe"); the code applies one rule (not system-missing, not 9996–9999) and no separate universe filter. Consider aligning Chapter 3 at final assembly. Not a correction of any number.
- **C (register). `docs/data_dictionary.md` inconsistency (author decision).** Row `v001` says "becomes `psu` (Step 04)", while `04_build_country_kr.py` sets `psu = v021`. Documentation only. It bears on FA-7 B but **does not resolve it**; code reading cannot establish how `hv001`/`v001` and `v021` correspond in the restricted data.
- **Open note kept in the appendix:** the Table A.1 note states that the `hv001`/`v001` vs `v021` correspondence has not been checked against the restricted data. Revise that sentence when FA-7 B is checked locally.
- **Page budget (FA-11):** Appendix A preview body **7 pages (pp. 1–7)**, plus a **1-page preview-only reference page (p. 8)**. Appendices are outside the 40-page main-text count. Preview figures, not thesis pagination.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/A_variable_definitions_and_sample_flow.md` → `lint appA` → `preview appA` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-20. Shared code changed in the Appendix A session (re-check at final assembly)

- **`filters/thesis.lua`** `875b078ca7649e153558544544dca36df92e7e8cab82edd01997b5ec6c3683bc` → `396c91097c881993bcd2e433e51e3f72c32ab14e820fa613277c56b07f4b3ca9`. New item 7: tables whose caption number is an appendix number (`A.1`, `B.2`, …) get `\endfirsthead` and a continuation head "**Table A.1** (continued)" above the repeated column heads. Chapter tables are written by the unchanged path.
  - Evidence: `REVIEW-COPY_appA-…_ea658b8.checks/reconvert_earlier_units.tsv`: the eight earlier units (ch01–ch07, abstract) convert byte-identically with the old and new filter, and identically to their committed `.tex` bodies.
  - **Re-check:** (1) Appendices B and C are the next units on this path; inspect their continuation pages. (2) If any earlier unit is re-converted, only its `% filter sha256` comment changes, but its file hash changes; for ch01 (in `APPROVED.tsv`) the approval hash would then need renewing. `build.py thesis` does not re-convert. (3) Decide whether chapter tables (Chapter 5) should also get continuation labels; that would change their `.tex` and require re-previewing ch05.
- **`scripts/build.py`** `e4676f211e2c635cab4066c65fd868c83abc2dff733367ab60dbe6f0c9d0a286` → `8568a446a6628d2e8a990a18309fa9b11101a5ba1289eab95058dc9f068655cb`. Preview only: appendix units' reference page reads "References cited in this appendix — preview only" and the chapter-style heading format is restored before it (the appendix format printed a stray "—"). Chapter and abstract previews generate the same strings as before. The full-thesis driver prints the reference list before the appendices and is not affected.
- `template/thesis-preamble.tex`, drivers and bibliography: unchanged.

## FA-21. Abstract: three review items recorded in the Appendix A session (2026-10-14)

Recorded on the author's instruction. **None was applied**, and the abstract was **not edited or rebuilt**. The abstract remains **awaiting author review** (FA-17) and is not in `chapters/APPROVED.tsv`. Publishing copy `chapters/md/08_abstract.md`, sha256 `ba56a2f44f86bb9f92d53c2ce281068dc2eca52f3c3d04248323f5c6e1950def` (unchanged). Each target string below was checked: it occurs exactly once in the publishing copy.

**A. REQUIRED AT FINAL ASSEMBLY.** Status: required; not applied.
- Replace "It distinguishes throughout" with "The baseline analysis distinguishes" (paragraph 1; current sentence: "It distinguishes throughout between a child's own household facilities and the WASH conditions of the surrounding community.").
- Reason (author): the historical extension does not separate household from community exposure.

**B. REQUIRED AT FINAL ASSEMBLY.** Status: required; not applied.
- Replace "unadjusted association" with "association before covariate adjustment" (paragraph 2; current sentence: "Community coverage shows a large, significant unadjusted association for most outcome and exposure pairs; …").
- Reason (author): water and sanitation are already mutually adjusted in the first community model.

**C. AUTHOR DECISION AT FINAL ASSEMBLY.** Status: open.
- The 59-country literature comparison ("The null sanitation results at both levels parallel subnational panel evidence from 59 countries …", paragraph 2) needs either an explicit citation or removal from the abstract. This narrows FA-17 F1: leaving it uncited is no longer an option. If cited, the key in `citation_map.md` and Chapters 2 and 6 is `HeadeyPalloni2019` (FA-3 title-case item applies).

**Steps:** apply A and B, and the C decision → `lint abstract` → `preview abstract` → inspect the changed page → record the new md/tex hashes here and in the abstract change log. Whether the canonical `08_abstract.md` is synchronised is the author's decision (FA-17).

## FA-22. Appendix B: points from the Appendix B session (awaiting author review)

Source: `chapters/changes/B_model_specifications_and_independent_verification.changelog.md` and `builds/previews/REVIEW-COPY_appB-appendix-B_preview_2026-10-15_2796974.verification.md`. Appendix B (`appB`) is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `99b61c66d1440f2faf49f2cb192d0792c92e49231dce12d76aaa78f7fb9979d6`; tex `d83b2e1d8e4ebcfe843a59ca078744603e28be0787ad32ac2e12526d58b0e316`; canonical unchanged (`0bb6281a…2075f`).

- **A. Verified corrections applied to the publishing copy only (author to confirm; canonical synchronisation is the author's decision, FA-13 procedure):**
  - A1: script 17 "matching to 3×10⁻¹⁴" applied to β only; SE agrees to a relative 7.5×10⁻¹⁰; `m0005` is an unweighted-comparison cell;
  - A2: Table B.2 β difference 6.7×10⁻⁸ is against a six-decimal constant in script 20 (stored 1.025553067200643; full-precision difference 2.4×10⁻¹⁴ from script 21); unweighted stored value 0.4146971 (`m0008`), not "0.41 (documented)";
  - A3: "lines 209–212" (pre-safeguard version `be71d57`) → `fit()` lines 248, 251 and 264–265 at `c58fc47`;
  - A4: "fully accounts for the gap on its own" → "accounts for the gap on this reconstruction"; "faithful reconstruction" → "reconstruction of the described design";
  - A5: SE reconciliation attributed to the pass-4 record at its displayed eight-decimal precision;
  - A6: Step 3 relative figure 2.23×10⁻¹⁶ = max |difference| / weighted norm (not the norm);
  - A7: "at the level of machine epsilon" → three and one units in the last place;
  - A8: B.4 column list: `p_value` is one column (count 15 unchanged).
  - The same "matches to 6.7×10⁻⁸" figure appears in `manuscript/v12_2026-10-10/claim_evidence_ledger.md`, `docs/provenance/final_empirical_package_v3_2026-10-07/01_final_reporting_map.md` and `02_core_reporting_table.md`, and the v2 results index; whether those records are annotated is part of the same decision.
- **B. Chapter 4 §4.6 wording (author decision; not applied).** The Chapter 4 publishing copy (`chapters/md/04_empirical_strategy.md`, sha256 `61f972e3…77fa4e`, unchanged) says "The age-in-months control, by contrast, fully accounts for the gap on its own" and "This diagnostic is a faithful reconstruction of the described early attempt". Appendix B now says "accounts for the gap on this reconstruction" and "a reconstruction of the described design" (A4). Consider aligning Chapter 4 at final assembly together with FA-8 and FA-12; otherwise the two units differ in emphasis (no number differs).
- **C. Title versus content (author decision).** The title says "Model specifications", but the appendix points to Chapter 4 for the equations and does not restate them. No specification summary was added (it would duplicate Chapter 4, which has pending corrections).
- **D. Baseline PanelOLS cross-validation (local check; open).** `docs/provenance/cluster_fe_inference_adjudication.md` reports PanelOLS agreeing with the baseline statsmodels SEs "to four to five decimal places". Whether that cross-validation call also omitted `group_debias=True` is not recorded publicly; an omission would explain a relative SE difference of about 1×10⁻⁴ at G = 4,426, N = 36,040. This is an inference, not a finding, and does not affect any stored baseline SE (those come from statsmodels). Check locally if the author wants the record to state the cause.
- **E. Stale line pointers in script docstrings (repository hygiene; author decision).** `21_validate_all_primary_cells.py` addendum ("line 124", the fit call is line 137); `24_reconcile_inference_corrections.py` ("lines 157-237", "lines 212, 225", which match `be71d57`); pass-4 record ("21 (line 124)"). Not in the appendix text; no code change made.
- **Carried forward unchanged:** FA-19 B (Chapter 3 measurement-validity wording vs the implemented rule; no separate measurement-universe filter), FA-19 C (data dictionary `v001` → `psu` vs the implemented `v021`), FA-7 B (`hv001`/`v001` vs `v021`, **unresolved** until checked with restricted baseline data locally), and the 42,052 count carried from the restricted validation log (Appendix A B12, not freshly verified). None is marked complete. Appendix B makes no statement that depends on them.
- **Shared code:** none changed. The FA-20 continuation path is present in the Appendix B tex for both tables; no table breaks in this preview, and a scratch stress test printed the continuation head correctly. FA-20 stays open for Appendix C and the full build.
- **Page budget (FA-11):** Appendix B preview body **11 pages (pp. 1–11)**, plus a **1-page preview-only reference page (p. 12)**. Appendices are outside the 40-page main-text count. Preview figures, not thesis pagination.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/B_model_specifications_and_independent_verification.md` → `lint appB` → `preview appB` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

- **F. REQUIRED AT FINAL ASSEMBLY: §B.1 wording on what differs between the two inference conventions** (recorded in the Appendix C session, 2026-10-17, on the author's instruction). Status: required; not applied. Appendix B was **not edited or rebuilt** in the Appendix C session.
  - **File:** `chapters/md/B_model_specifications_and_independent_verification.md` (publishing copy; sha256 `99b61c66d1440f2faf49f2cb192d0792c92e49231dce12d76aaa78f7fb9979d6`, unchanged).
  - **Target (exact text; occurs exactly once, §B.1, the paragraph after the Table B.1 note; checked in the Appendix C session):** "Point estimates are identical by construction; only standard errors and *p*-values differ."
  - **Author's instruction:** replace "only standard errors and p-values differ" with wording that includes confidence intervals: "Only standard errors, confidence intervals and p-values differ; the point estimates remain unchanged."
  - **Application note:** the author's sentence already states that the point estimates are unchanged, so inserting it after "Point estimates are identical by construction;" would repeat that clause. Replacing the whole target sentence gives "Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged." (italic *p* as elsewhere in the copy). This drops the words "by construction"; the author confirms at final assembly which form is used.
  - **Canonical:** the same phrase occurs once in `manuscript/v12_2026-10-10/appendices/B_model_specifications_and_independent_verification.md` ("only standard errors and p-values differ"); synchronisation is the author's decision (FA-22 A procedure).
  - **Unchanged by this item:** FA-22 D. Whether the baseline PanelOLS cross-validation call omitted `group_debias=True` remains **unverified**; neither this wording correction nor FA-22 D implies an error in the stored baseline estimates, whose standard errors come from statsmodels.
  - **Steps:** apply → `lint appB` → `preview appB` → inspect the changed page → record the new md/tex hashes here and in the Appendix B change log.

## FA-23. Appendix C: points from the Appendix C session (awaiting author review)

Source: `chapters/changes/C_historical_diagnostics_and_ethiopia.changelog.md` and `builds/previews/REVIEW-COPY_appC-appendix-C_preview_2026-10-17_3d0a3a8.verification.md`. Appendix C (`appC`) is **awaiting author review** and is not in `chapters/APPROVED.tsv`. Publishing copy sha256 `208f5020a0cbd59231c9aa63ae06807caa3452e55fda00939f549648916cffac`; tex `1b1f1e8cc277fc218604f6d848490d45deaf525c54c37781bc8b679324cce5e2`; canonical unchanged (`a189ffb5…ef79ea3`).

- **A. Verified corrections applied to the publishing copy only (author to confirm; canonical synchronisation is the author's decision, FA-13 procedure):**
  - A1: the 275-child C1 versus C2/C3 difference is documented for the birth-year window only (stored attribution JSON);
  - A2: "Both confidence intervals include zero" → all four (`m0045`, `m0046`, `m0186`, `m0187`);
  - A3: the Ghana-exclusion row (`o003`, `sens_overlap_excl_GH_water`, Kenya + Nigeria) keeps Kenya's water overlap; relabelled, and described as a two-country pooled model, not an overlap-free estimate;
  - A4: the Ethiopian interview date governs date validity, birth-before-interview, postnatal completion and the post-interview flag; windows and exposure values are placed from the birth date;
  - A5: the birth-year window has no completion check, but its eligibility is not "satisfied by construction" (valid dates, raster span, complete coverage);
  - A6: the C1 finding is dated before the estimation run, but C1 was estimated in that run and reclassified on 7 October 2026;
  - A7: pre-specification attributed to the estimation specification §8 (commit `03953cc`), reporting to the methods note §7; "all are reported together" narrowed to the stored file;
  - A8: "exact buffer average" → "buffer average" (Chapter 3 §3.6 meaning of "exact").
  - No stored number was found to be wrong.
- **B. Chapter 3 §3.5 wording (author decision; not applied).** The Chapter 3 publishing copy (`chapters/md/03_data_and_variables.md`, sha256 `9f9d9b18…a91176`, unchanged) says the conversion is "required to place Ethiopian children's exposure windows". Appendix C (A4) now says the windows are placed from the birth date and the interview date governs eligibility. Consider aligning Chapter 3 at final assembly together with FA-7 A; Chapter 3 §3.7 already describes the eligibility role correctly.
- **C. Chapter 5 Table 5.9 Ghana-exclusion label (author decision; not applied).** Row "Excluding Ghana (DHS/IHME input overlap)" with the note "pools Kenya and Nigeria only". Appendix C (A3) states that Kenya's water overlap remains in this model. Consider adding that clause to the Chapter 5 note (no number changes).
- **D. Candidate-status record §4 (provenance annotation; author decision).** `docs/provenance/historical_wash_ethiopia_candidate_status_v1_2026-10-07.md` §4 says the completion rule applies to every window including the birth year (citing the design draft). The implemented construction (`12_construct_exposure_windows.py`, `eligibility()`), Chapter 3 §3.7 and Appendix C apply it to the postnatal windows only. No result depends on the record's wording; whether to annotate it is the author's decision.
- **E. Exact postnatal eligibility counts (local check; open).** Table C.1's 7,930 / 7,922 (post-12-month) and 5,974 / 5,969 (post-24-month) are carried from the canonical appendix; the public status record gives "~7,930" and "~5,970". A local aggregate count from the restricted analysis file would confirm them. Not altered; the table note states their status.
- **F. Dated records relevant to FA-15 B (information; FA-15 B stays open).** Specification commit `03953cc` (2026-10-06 20:51:28 +02:00; "No coefficient has been estimated or inspected"; sensitivity list in §8) precedes the recorded estimation run `run_20261006T185646Z` (20:56:46 +02:00). FA-15 B concerns the window choice in Chapter 6 §6.4 and remains the author's evidence check; these records establish order of recording, not the absence of unrecorded earlier runs.
- **G. Layout.** Page 4 of the preview is about half empty because the shared keep logic holds the C.3 heading with Table C.2 (FA-10). No table breaks in this preview; the FA-20 continuation path was exercised in a scratch stress test (continuation head, repeated column heads, note with the last rows). FA-20 stays open for the full build.
- **Carried forward unchanged:** FA-7 B (`hv001`/`v001` vs `v021`, **unresolved**), the 42,052 count carried from the restricted validation log (Appendix A B12, not freshly verified), FA-19 B and C, FA-22 A–E. Appendix C makes no statement that depends on them.
- **Shared code:** none changed.
- **Page budget (FA-11):** Appendix C preview body **8 pages (pp. 1–8)**, plus a **1-page preview-only reference page (p. 9)**. Appendices are outside the 40-page main-text count. Preview figures, not thesis pagination.
- **Steps at final assembly:** the author reviews; any accepted change → edit `chapters/md/C_historical_diagnostics_and_ethiopia.md` → `lint appC` → `preview appC` → inspect → record hashes. Then the author decides on `APPROVED.tsv`.

## FA-24. Consolidated references: follow-ups (recorded in the consolidated-references session, 2026-10-17)

Source: `bibliography/REFERENCES_VERIFICATION.md`; review copy `builds/previews/REVIEW-COPY_references-consolidated_preview_2026-10-17_c613d28.pdf` (2 pages, 20 works) with `.report.md` and `.checks/`. No chapter or appendix file was edited or rebuilt.

- **A. Shared code changed (re-check at final assembly).** (1) `scripts/build.py`: every build now reads the publishing copy `bibliography/bibliography.bib`; `manifest` still checks the canonical file; new command `references`. (2) `template/thesis-preamble.tex`: `\AtBeginBibliography{\raggedright\def\UrlBreaks{\do\/}\def\UrlBigBreaks{\do\:}}`, which affects reference lists only. Earlier previews were **not rebuilt**; their preview-only reference pages show the old bibliography. At final assembly: re-run `diagnostic`, `selftest`, and `thesis`, and check the reference list, contents entry and bookmark. A unit already in `APPROVED.tsv` (ch01) is unaffected in its tex hash, because the bibliography is not part of a unit's tex.
- **B. Entries to confirm locally against a primary record** (registries were unreachable in this session; no value below was invented):
  1. `LBDWaSH2020` issue 9 (two repository records only);
  2. `deOnis2006` representation "Acta Paediatrica Supplement 450:76–85" versus a possible Wiley form "Acta Paediatrica 95 (S450)", and the online date of 2 January 2007 recorded in the ledger;
  3. `Black2013`: Chicago prints seven of more than ten authors; the bibliography stores six plus "others". Add the seventh author only after checking the byline order on the publisher page;
  4. optional: the DHS reports' imprint ("ICF International, Calverton, Maryland" in the DHS recommended citations, versus the umbrella "The DHS Program/ICF") and URLs for DHS and NBER reports.
- **C. Blom2022 record contradiction (author check).** Audit CSV row S04 says "Yes (full-text read)" and names `1-s2.0-S0095069622000626-main.pdf`; the ledger and citation map say the published article was never read and no local PDF exists. Check the local source folder. Until then, claim support stays **indirect version correspondence**; do not upgrade.
- **D. Data and software citations (author decision).** The guidelines require "a list of all sources and materials used". DHS recode files, the IPUMS-DHS extract, the IHME gridded product and `statsmodels`/`linearmodels` are used but have no reference entries. Decide whether to add them, with the citation wording each provider asks for. Any addition needs a citation in the text and a re-run of `build.py references`. Nothing was added.
- **E. Canonical ledger and citation map (author decision).** Annotate, without upgrading, `bibliography_verification_ledger.md` "full-text read" statements for Victora2008, CummingCairncross2016, Gunther2010, Spears2013, Balk2004 and JohnsonJacobBrown2013 as acquisition-stage identity checks. For CummingCairncross2016, decide after checking whether the passages quoted in R15 (PMC5084825 fetch, 2026-10-10) are in the abstract or the body. Not edited (canonical frozen at `c58fc47`).
- **F. Canonical bibliography synchronisation (author decision).** The publishing copy differs from `manuscript/v12_2026-10-10/bibliography.bib` by the 21 rows of `bibliography/field_changes.tsv`. Whether to carry them into the canonical file is the author's decision; if done, re-record `source_manifest.tsv` deliberately (it is never overwritten automatically).
- **G. Page-budget note (FA-5, FA-11).** The review copy has 2 pages at page 1–2 of its own. This says nothing about the thesis's reference pages or page count, and references are outside the 40-page main-text maximum.

## FA-25. Three review items recorded in the consolidated-references session (2026-10-17, author's instruction)

None applied; Appendices B and C were **not edited or rebuilt**.

- **A. REQUIRED: Appendix B §B.1 inference sentence.** Already recorded as **FA-22 F** (unchanged). Replace the incomplete sentence with wording that includes confidence intervals: "Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged." Target (checked again in this session; occurs once in `chapters/md/B_model_specifications_and_independent_verification.md`, sha256 `99b61c66…79d6`, unchanged): "Point estimates are identical by construction; only standard errors and *p*-values differ." Application note and steps as in FA-22 F.
- **B. REQUIRED LOCAL CHECK BEFORE FINAL ASSEMBLY: exact Ethiopian postnatal timing-eligibility counts** (Appendix C, Table C.1). Post-12 months: C2 7,930; C3 7,922. Post-24 months: C2 5,974; C3 5,969. These are carried from the canonical appendix text; no public output contains them (the public status record gives "~7,930" and "~5,970"). **Their presence in the manuscript text is not independent validation.** Confirm them against the local restricted analysis file or an aggregate count produced from it, and record the result here. If any count differs, correct Table C.1 and its note and rebuild Appendix C. This supersedes the "local check; open" wording of FA-23 E, which stays open until this is done. Not done in the cloud: no restricted data read, nothing rerun.
- **C. FORMATTING CONSISTENCY: `m0032` *p*-value display** (Appendix C). The rural-10-km sensitivity model `m0032` has stored *p* = 0.000806724998905555 (`docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`, row `m0032`, checked in this session). The manuscript's declared rule (Chapter 5 introduction: three decimals when the value is at least .0005, "<.001" when smaller) gives ".001", not "<.001".
  - **File:** `chapters/md/C_historical_diagnostics_and_ethiopia.md` (publishing copy, sha256 `208f5020…6cffac`, unchanged), Table C.3 note. **Target (occurs once):** "Rural 10 km `m0032`: 1.01 [0.42, 1.60], *p* < .001," → "Rural 10 km `m0032`: 1.01 [0.42, 1.60], *p* = .001,". In the file, the spaces in "10 km" and around "<" in "*p* < .001" are U+00A0 no-break spaces (Appendix C rendering fix); a plain-space search will not find the target. Keep U+00A0 around "=" in the replacement.
  - The canonical appendix does not contain this display (the note was added in the publishing copy, FA-23 A).
  - This is a display-consistency correction, **not a changed result**: coefficient, interval, N and G are unchanged.
  - Scan in this session: the three other "*p* < .001" displays next to a model ID in the appendix copies (`m0004`, `m0036`, `m0044`) have stored values below .0005 and are correct. Table cells without a model ID were not scanned.
  - **Steps:** apply → `lint appC` → `preview appC` → inspect the changed page → record the new md/tex hashes here and in the Appendix C change log.

## Open-item summary (as of the consolidated-references session; none applied except FA-3 and FA-4 as noted)

| Item | Chapter | Kind | Status |
|---|---|---|---|
| FA-1 | 2 (§2.4) | required correction (exact text) | open |
| FA-2 | 1 | carry-forward record; open points 1–7 | preserved |
| FA-3 | all | bibliography completeness (incl. new `HeadeyPalloni2019` item) | carried out in the publishing copy (2026-10-17); canonical sync FA-24 F |
| FA-4 | template | xurl DOI breaks | fixed in the reference list only; re-check FA-24 A |
| FA-5 | thesis | final pagination; 40-page check only in `build.py thesis` | open |
| FA-6 | 3 | review points A3–A5 (A1, A2 superseded by FA-7) | open |
| FA-7 A | 3 (§3.9) | required cross-reference correction | open |
| FA-7 B | 3, 4 | `hv001`/`v001` vs. `v021` local verification with restricted data | **open, unresolved** |
| FA-8 A–D | 4 (§4.5) | four required methodological-description corrections | open |
| FA-9 | 5 | A1–A3 applied in the copy, B1–B11, C, E1–E7 to confirm (E2 superseded by FA-12) | open |
| FA-10 | template | table-macro re-check (diagnostic, selftest, appendix tables) | open |
| FA-11 | thesis | defer page-budget editing to final assembly | standing instruction |
| FA-12 | 4 (§4.5) vs. 5 | required: narrow the "every pooled coefficient" sentence | open |
| FA-13 | 5 | required: synchronise "more than doubles" correction with canonical | open |
| FA-14 | 6 | A1–A10 applied in the copy, B1–B13, F1–F6 to confirm | open |
| FA-15 A | 6 (§6.5) | required wording correction (residence proxy; exact text) | open |
| FA-15 B | 6 (§6.4) | evidence check: "before any model was estimated" vs. dated design records | open |
| FA-15 C | 6 | discussion completeness (§5.4, §5.5, negative Ghana sanitation cell) | open, author decision |
| FA-16 | 7 | A1–A8 applied in the copy, B1–B12, F1–F6 to confirm; abstract flags (F4) addressed in the abstract's publishing copy only (FA-17); canonical synchronisation | open |
| FA-17 | abstract | A1–A5 applied in the copy, B1–B15, F1–F6 to confirm; canonical synchronisation | open |
| FA-18 | template | ";" extracted as U+037E in all PDFs (text layer only) | open |
| FA-19 | Appendix A | A1–A6 applied in the copy, B1–B13, C, D to confirm; Chapter 3 §3.2 wording (B); data-dictionary `v001` row (C); canonical synchronisation | open |
| FA-20 | filter, build script | appendix continuation heads; appendix preview reference title: re-check with Appendices B–C; ch01 hash caution | open |
| FA-21 A | abstract | required: "It distinguishes throughout" → "The baseline analysis distinguishes" | open |
| FA-21 B | abstract | required: "unadjusted association" → "association before covariate adjustment" | open |
| FA-21 C | abstract | author decision: cite or remove the 59-country comparison | open, author decision |
| FA-22 A | Appendix B | A1–A8 applied in the copy, B1–B17, C, D to confirm; canonical synchronisation (and the 6.7×10⁻⁸ figure in provenance records) | open |
| FA-22 B | 4 (§4.6) vs Appendix B | "fully accounts" / "faithful reconstruction" wording | open, author decision |
| FA-22 C | Appendix B | title "Model specifications" vs content (equations in Chapter 4) | open, author decision |
| FA-22 D | baseline provenance | cause of the 4–5-decimal PanelOLS agreement (`group_debias`?) | open, local check |
| FA-22 E | scripts | stale line pointers in docstrings of scripts 21 and 24 and the pass-4 record | open, author decision |
| FA-22 F | Appendix B (§B.1) | required: "Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged." | open |
| FA-23 A | Appendix C | A1–A8 applied in the copy, B1–B19 to confirm; canonical synchronisation | open |
| FA-23 B | 3 (§3.5) vs Appendix C | what the Ethiopian interview date is needed for | open, author decision |
| FA-23 C | 5 (Table 5.9) vs Appendix C | Ghana exclusion keeps Kenya's water overlap | open, author decision |
| FA-23 D | provenance record | candidate-status record §4 completion-rule wording vs implementation | open, author decision |
| FA-23 E | Appendix C (Table C.1) | exact postnatal eligibility counts (restricted data) | open, local check |
| FA-23 F | 6 (§6.4) | dated records bearing on FA-15 B (information only) | FA-15 B still open |
| FA-23 G | Appendix C layout | p. 4 white space from keep logic; continuation path not exercised in the delivered PDF | open (FA-10, FA-20) |
| FA-24 A | build script, preamble | publishing bibliography copy; `references` command; reference-list URL breaks | open, re-check at final assembly |
| FA-24 B | bibliography | LBDWaSH2020 issue; deOnis2006 form and online date; Black2013 seventh author; optional DHS imprint and URLs | open, local check |
| FA-24 C | records | Blom2022: audit CSV "full-text read" vs ledger "no local PDF" | open, author check |
| FA-24 D | references | data and software used but not in the reference list | open, author decision |
| FA-24 E | canonical records | ledger and citation-map evidence-depth annotations (no upgrades) | open, author decision |
| FA-24 F | canonical bibliography | synchronise the 21 field changes | open, author decision |
| FA-24 G | thesis | references preview pages are not thesis pages | standing note |
| FA-25 A | Appendix B (§B.1) | required: confidence-interval wording (= FA-22 F) | open |
| FA-25 B | Appendix C (Table C.1) | required local check: exact postnatal counts 7,930 / 7,922 / 5,974 / 5,969 (FA-23 E) | open, local check |
| FA-25 C | Appendix C (Table C.3 note) | `m0032` *p* display "< .001" → "= .001" (stored 0.000807) | open |

### Status classes (kept distinct; added in the Chapter 7 session)

1. **Corrections already applied to publishing copies** (awaiting the author's confirmation; not approved):
   - Chapter 5: FA-9 A1–A3;
   - Chapter 6: FA-14 A1–A10;
   - Chapter 7: FA-16 A1–A8;
   - Abstract: FA-17 A1–A5;
   - Appendix A: FA-19 A1–A6;
   - Appendix B: FA-22 A (A1–A8);
   - Appendix C: FA-23 A (A1–A8);
   - plus the language edits of Chapters 1–7 recorded in each change log.
2. **Corrections still pending** (required or open; not applied anywhere):
   - required wording: FA-1 (ch02), FA-7 A (ch03), FA-8 A–D and FA-12 (ch04), FA-15 A (ch06), FA-21 A and B (abstract), FA-22 F (Appendix B §B.1);
   - author decisions: FA-21 C (abstract 59-country comparison), FA-19 B and C, FA-22 B, C and E, FA-23 B, C and D;
   - local check: FA-22 D (baseline PanelOLS cross-validation record; unverified), FA-23 E (exact postnatal eligibility counts);
   - evidence check: FA-15 B (ch06);
   - required wording added 2026-10-17: FA-25 A (= FA-22 F), FA-25 C (display consistency);
   - required local check added 2026-10-17: FA-25 B (exact postnatal counts; FA-23 E);
   - bibliography: FA-3 carried out in the publishing copy only, follow-ups FA-24 B–F; template and shared code: FA-4 (reference list done, body open), FA-10, FA-18, FA-20, FA-24 A.
3. **Canonical GitHub files still needing synchronisation**:
   - required: FA-13 (ch05 "more than doubles");
   - author decisions: ch06 FA-14 A, ch07 FA-16 A, abstract FA-17 A, Appendix A FA-19 A, Appendix B FA-22 A, Appendix C FA-23 A, and whether the required publishing-copy corrections above are also carried into `manuscript/v12_2026-10-10/`;
   - none of these has been done, and the canonical files are unchanged at `c58fc47`.
4. **Unresolved research limitations** (not fixable by rendering, and not to be described as resolved):
   - FA-7 B (`hv001`/`v001` vs. `v021`, restricted-data check);
   - the undocumented anthropometry-subsample weight;
   - the Nigeria 2018 measurement-count gap;
   - DHS/IHME input overlap; current residence as a proxy for early-life residence; coordinate displacement;
   - the unvalidated Ethiopian date conversion;
   - no multiplicity adjustment.
5. **Deferred page-budget work:** FA-5, FA-11 (standing instruction).

---

### Superseded record: FA-8 as written in the Chapter 4 session (kept for the record)

**FA-8 (Chapter 4 session wording). Chapter 4: points from the Chapter 4 session (awaiting the author's decision; nothing applied)**

Source: `chapters/changes/04_empirical_strategy.changelog.md`, section A. Chapter 4 is **awaiting author review** and is not in `chapters/APPROVED.tsv`. The publishing copy keeps the canonical wording at every point below.

- **A1, substantive, correction proposed.** §4.5 "Weighting": "…so that each country's weights sum to exactly $1$ (equivalently, $N/M$ on average across countries)."
  - The baseline code (`build_temporary_pooled_weight()`) makes each country total 1. The historical code (`equal_country_weights()`) makes each country total $N/M$.
  - The parenthetical states the historical total in the sentence describing the baseline formula.
  - **Proposed:** delete the parenthetical, or replace it with "(so the weights sum to $M$ across the pooled sample)".
  - If the author accepts, it should be applied to `chapters/md/04_empirical_strategy.md` (now sha256 `61f972e3df2346787af5d7654c37f5d96590d3500df178b9741414c70177fa4e`), followed by `lint ch04`, `preview ch04` and an inspection of the changed page. Whether the canonical v12 file is also corrected is the author's decision.
- **A2, optional addition.** One sentence stating that the region-FE models (§4.1, §4.3, §4.4) are explicit-dummy WLS fits clustered on `country_psu`, with region dummies and the constant counted in $K$, and normal-reference inference. Proposed wording: changelog A2.
- **A3, optional precision.** The §4.5 rank paragraph describes the historical drop-and-name mechanism. The baseline instead stops on rank deficiency, and its only pre-specified exclusion is `residence` under cluster FE.
- **A4, cross-reference.** In §4.5, "the baseline tables above" refers to tables in Section 5. **Proposed:** "the baseline tables in Section 5".
- **Page budget note (FA-5).** The Chapter 4 preview body is 9 pages, plus a 1-page preview-only reference page. That page states that the chapter cites no works and is not part of the chapter source. These are separate-preview figures, not a thesis page count.
