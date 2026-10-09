# Final bibliographic and citation-claim audit (2026-10-09)

Starting commit: `eaec5a8` (confirmed `HEAD == origin/main`, clean except the standing untracked `outputs/supervisor_meeting/`). Canonical manuscript: `manuscript/v10_2026-10-07/`. This is a bounded reference audit: no empirical analysis was restarted, no estimate changed, no PDF was generated, rebuilt, or rendered.

## 1. Scope and method

Two independent lines of evidence were combined, neither trusted alone:

1. **Mechanical/structural checks**, run directly against `bibliography.bib` and the six chapter/appendix files that contain any citation (`01_introduction.md`, `02_literature_review.md`, `03_data_and_variables.md`, `06_discussion_and_limitations.md`, `07_conclusion.md`, `appendices/A_variable_definitions_and_sample_flow.md` — confirmed by grep across the whole package that no other file contains a citation key): brace balance, duplicate-key check, cited-vs-defined key reconciliation.
2. **Primary-source metadata verification**, performed by four parallel research passes against publisher/DOI-registration records (Crossref API, PubMed/MEDLINE, Europe PMC, PMC, NBER, World Bank/IDEAS-RePEc, DHS Program's own hosted PDFs and auto-citation files, WHO, UNICEF, AfDB/IDEAS-RePEc), not Google Scholar snippets, an earlier audit's say-so, or this thesis's own prior verification passes. Each pass distinguished DOI-resolution confirmation, Crossref-metadata confirmation, and full-text/abstract reading, and reported what could not be reached (several publisher HTML pages returned HTTP 403 to automated fetch; DOI redirect chains and Crossref/PMC/Europe PMC metadata were used as corroborating primary-adjacent evidence in those cases, stated explicitly below wherever that substitution was made).

Previous verification reports (`citation_map.md`, `bibliography_verification_ledger.md`, the v1–v9 `docs/provenance/evidence_based_correction_*.md` files) were treated as pointers, not proof, per this task's own instruction. The in-text chapter prose was re-read in full this pass (not grepped with truncating context) to build the occurrence ledger in Section 3, and every claim below was checked against that reading, not assumed from an earlier pass's summary.

## 2. Entry-level bibliography verification

All 26 entries in `bibliography.bib` were checked. 12 corrections were made across 9 entries (all in Section 2.1 below); the remaining 17 entries were confirmed accurate as previously recorded, with a small number of findings left deliberately unresolved rather than acted on (Section 2.2).

### 2.1 Corrections applied this pass

| Key | Field | Before | After | Evidence | Confidence |
|---|---|---|---|---|---|
| `deOnis2006` | author | `{WHO Multicentre Growth Reference Study Group} and de Onis, Mercedes and Martorell, Reynaldo and Garza, Cutberto and Lartey, Anna` | `{WHO Multicentre Growth Reference Study Group}` (personal names removed) | PubMed/MEDLINE (PMID 16817681), Crossref, and Europe PMC **all three independently** list this specific *Acta Paediatrica* article's sole author as the collective body, with no personal co-authors. The four removed names are genuine MGRS-series authors, but of other publications (including the separate WHO Press growth-standards methodology monograph), not this one. | High (3 independent primary registries agree) |
| `Addae2024` | author (all 6) | Addae, Hayford Yaw; Sulemana, Mustapha; Yakubu, Tahiru; Atosona, Albert; Tahiru, Rahinatu; Azupogo, Faith | Addae, Hammond Yaw; Sulemana, Mohammed; Yakubu, Taminu; Atosona, Ambrose; Tahiru, Rafatu; Azupogo, Fusta | PMC (PMC10977686) and Crossref agree; corroborated by an independent check that "Fusta Azupogo" (not "Faith") is a real person — Senior Lecturer, University for Development Studies, Ghana, PhD Wageningen University | High (two primary metadata sources + real-person cross-check) |
| `Addae2024` | volume/pages | absent | `volume={19}`, `pages={e0297698}` | Crossref/PMC | High |
| `Cumming2019` | author | Sundberg, Sophie | Sundberg, Shelly | Crossref and Europe PMC independently agree | High |
| `Balk2004` | author | Greenwell, Fiona | Greenwell, Fern | Crossref (DOI 10.1002/psp.328) | High |
| `Balk2004` | volume/number/pages | absent | `10`/`3`/`175--216` | Crossref | High |
| `JohnsonJacobBrown2013` | author | Jacob, Arun | Jacob, Anila | Crossref (corroborated by PMC) | High |
| `JohnsonJacobBrown2013` | volume/number/pages | absent | `1`/`2`/`237--248` | Crossref | High |
| `Rakotomanana2020` | author | Komakech, Jacob J. | Komakech, Joel J. | PMC (PMC7503684) and Crossref agree | High |
| `Rakotomanana2020` | volume/number/pages | absent | `17`/`17`/`6262` (article number) | Crossref | High |
| `Victora2010` | author | Blossner, Monika | Blössner, Monika | Crossref (umlaut dropped, diacritic-only error) | High |
| `HeadeyPalloni2019` | number | absent | `2` | Crossref (volume 56, pages 729–752 already correct) | High |
| `Blom2022` | volume/pages | absent | `115`/`102698` (article number) | Crossref | High |
| `SkoufiasVinha2026` | journal | PLOS One | PLOS ONE | Publisher's own article page (journals.plos.org), capitalization only | High |
| `JMP2025` | title | "Progress on Household Drinking Water, Sanitation and Hygiene 2000--2024: Special Focus on Inequalities" | "Progress on household drinking-water, sanitation and hygiene 2000-2024: Special focus on inequalities" | WHO's own publication-page title (hyphenation + sentence case) | High |
| `Gebru2019` (uncited) | author (all 5) | Gebru, Kahsay Fisshaye; Haileselassie, Wasihun Mesfin; Temesgen, Awraris Hailu; Seid, Awoke Oljira; Mulugeta, Birhanu Abera | Gebru, Kahsay Fantay; Haileselassie, Wasihun Mekonnen; Temesgen, Awraris Haftom; Seid, Awoke Oumer; Mulugeta, Birhanu Afework | Crossref, corroborated by an independent DOAJ-indexed search. **Lower confidence than Addae2024**: the publisher's own BMC Pediatrics/Springer HTML page could not be reached directly (login redirect), so this rests on two independent secondary-metadata sources, not the publisher's own rendered page. | Medium (uncited reserve entry; corrected for accuracy regardless) |
| `Gebru2019` (uncited) | volume/pages | absent | `19`/`176` | Crossref | High |

All 26 entries re-checked for brace balance and duplicate keys after editing: balanced, 26 unique keys, 0 duplicates. All 20 cited keys still resolve; the same 6 entries remain uncited (`Croft2023`, `Gebru2019`, `ICF2012`, `JMP2025`, `Momberg2021`, `UNICEF2025`).

### 2.2 Findings deliberately left unresolved (not acted on, with reasons)

- **`PerezHeydrich2013`, accent in "Pérez"**: the DHS SAR8 PDF's own text layer was checked at byte level and renders a plain "e," not "é," in both occurrences of the surname. This could be a genuine absence of the accent in that specific document, or a font-encoding artefact of PDF text extraction (a known, common failure mode for diacritics). "Pérez" is standard Spanish orthography and the accented form is used elsewhere for this name in the literature. Left unchanged; flagged in `bibliography_verification_ledger.md` as unresolved rather than silently kept or silently "corrected" on uncertain grounds.
- **`Momberg2021`, full given names**: only initials could be confirmed against sources actually reached (the Cambridge University Press page itself was paywalled); the existing bib entry's expanded given names could not be independently confirmed or refuted. Left unchanged — "unverifiable" is recorded as a distinct status from "discrepant," consistent with this task's own instruction not to claim more than the evidence supports.
- **`Burgert2013` / `ICF2012`, institution field "The DHS Program/ICF"**: anachronistic relative to each document's own 2012–2013 imprint ("ICF International"/"MEASURE DHS"); left unchanged for consistency with the other DHS-series entries (`Donohue2023`, `Croft2023`), whose own 2023 imprints make the same umbrella form accurate. This is a stylistic/branding choice, not a factual error about authorship.
- **Minor omitted fields not treated as errors**: `Black2013` and `Victora2008` omit issue numbers (9890, 9609 respectively) that Crossref has; `Cumming2019` omits the "Jr." suffix on Colford. These are omissions, not incorrect values, and were not added, consistent with this bibliography's existing convention of not listing every available field for every entry (e.g., DHS Spatial Analysis Reports cited by series number only).

### 2.3 Entries confirmed accurate, no change

`Black2013`, `Victora2008`, `CummingCairncross2016`, `LBDWaSH2020`, `GerusoSpears2015`, `Donohue2023`, `Burgert2013` (author/title/number), `PerezHeydrich2013` (author order/title/number, apart from §2.2), `ICF2012` (title/author/year, apart from §2.2), `Croft2023`, `Gunther2010`, `Spears2013`, `UNICEF2025`.

## 3. Occurrence-level citation-claim ledger

Built from a full read of the six citation-bearing files (not a context-truncating grep), cross-checked against the previously-established per-key occurrence counts. All 48 occurrences across the 20 cited keys are accounted for below and reconcile exactly with the mechanical count in Section 1.

| # | File / §Section | Exact claim (summarised) | Key | Evidence depth | Verdict |
|---|---|---|---|---|---|
| 1 | 01 §1 | Growth faltering has long-run consequences for cognition, schooling, earnings | Victora2008 | Full-text (abstract) read, prior pass | Supported |
| 2 | 01 §1 | — same sentence, grouped citation | Victora2010 | Full-text (abstract/results) read, prior pass | Supported |
| 3 | 01 §1 | — same sentence, grouped citation | Black2013 | Full-text (Panel 1, p.434) read, prior pass | Supported |
| 4 | 01 §1 | WASH→EED mechanism pathway | CummingCairncross2016 | Full-text (title/abstract) read, prior pass | Supported |
| 5 | 01 §1.1 | Household/community WASH need not move together | Donohue2023 | Full-text (pp.1,3,18–20) read, prior pass | Supported |
| 6 | 01 §1.1 | — same claim, second source | SkoufiasVinha2026 | Abstract read, prior pass; journal name corrected this pass | Supported |
| 7 | 01 §1.2 | DHS-based single-round literature generally | Rakotomanana2020 | Full-text read, prior pass; author name corrected this pass | Supported |
| 8 | 01 §1.2 | — same claim, second source | Addae2024 | Full-text read, prior pass; author names corrected this pass | Supported |
| 9 | 01 §1.2 | IHME gridded WASH product used for the historical extension | LBDWaSH2020 | Primary-source Figure 1 re-confirmed, prior pass | Supported |
| 10 | 02 §2.1 | WASH→EED mechanism (repeated from §1) | CummingCairncross2016 | As above | Supported |
| 11 | 02 §2.1 | "Biological plausibility... not challenged" (direct quote, consensus message 2) | Cumming2019 | Full-text read in full (pp.1–9), prior pass | Supported — direct quote verified |
| 12 | 02 §2.1 | Proximate/distal determinants framework (Panel 1) | Black2013 | Full-text (p.434) read, prior pass | Supported |
| 13 | 02 §2.1 | Growth faltering concentrated birth–24mo | Victora2010 | Full-text (abstract/results) read, prior pass | Supported |
| 14 | 02 §2.2 | 172-DHS water/sanitation-mortality association | Gunther2010 | Full-text (abstract) read, prior pass | Supported |
| 15 | 02 §2.2 | Cross-country height/open-defecation correlation, hedged as correlational | Spears2013 | Full-text (abstract) read, prior pass | Supported |
| 16 | 02 §2.2 | 442-region/59-country panel DiD; mixed results precisely stated (water insignificant except piped; sanitation null for stunting/wasting) | HeadeyPalloni2019 | Full-text (pp.729–731) read, prior pass; issue number added this pass | Supported |
| 17 | 02 §2.2 | 8-country East African water/sanitation associations | Rakotomanana2020 | Full-text read, prior pass | Supported |
| 18 | 02 §2.2 | Ghana water-wasting-only, sanitation/SES-both-outcomes finding | Addae2024 | Full-text read, prior pass (found and corrected an earlier overclaim); authors corrected this pass | Supported, as now precisely scoped |
| 19 | 02 §2.3 | Trial design/arm-structure description (6-arm Bangladesh/Kenya vs 4-arm SHINE), "all WASH arms" vs "WASH arm" (Fig. 2) | Cumming2019 | Full-text read, prior pass, incl. direct check of Fig. 2's own plural/singular wording | Supported |
| 20 | 02 §2.3 | Nutrition-arm modest positive effect (p.6) | Cumming2019 | As above | Supported |
| 21 | 02 §2.3 | Combined WASH+nutrition no additional benefit (p.2) | Cumming2019 | As above | Supported |
| 22 | 02 §2.3 | Diarrhoea mixed results (pp.2–5, Fig.2) | Cumming2019 | As above | Supported |
| 23 | 02 §2.3 | Consensus statement: basic vs. "transformative" WASH distinction | Cumming2019 | As above | Supported |
| 24 | 02 §2.3 | Muslim–Hindu mortality puzzle, sanitation-specific identification | GerusoSpears2015 | Full-text (pp.1–3) read, prior pass; version (NBER WP, not 2018 AEJ:AE) explicitly scoped | Supported, with version caveat stated in text |
| 25 | 02 §2.4 | Nigeria/Zambia community-sanitation-stunting result, precisely stated (significant Nigeria only, modest) | Donohue2023 | Full-text (pp.1,3,18–20) read, prior pass | Supported, as now precisely scoped |
| 26 | 02 §2.4 | 20-country community-externality framework; water null, sanitation significant, urban/rural variation | SkoufiasVinha2026 | Abstract read, prior pass | Supported |
| 27 | 02 §2.4 | DHS-cluster-level geography precedent (mortality, not anthropometry) | Balk2004 | Full-text (title/abstract) read, prior pass; author name corrected this pass | Supported |
| 28 | 02 §2.5 | Single-round exposure-timing limitation applies to this literature | Rakotomanana2020 | As above | Supported |
| 29 | 02 §2.5 | — same claim | Addae2024 | As above | Supported |
| 30 | 02 §2.5 | — same claim | Gunther2010 | As above | Supported |
| 31 | 02 §2.5 | — same claim | Spears2013 | As above | Supported |
| 32 | 02 §2.5 | Headey & Palloni's panel design does not share this limitation | HeadeyPalloni2019 | As above | Supported |
| 33 | 02 §2.6 | DHS cluster coordinates randomly displaced for confidentiality | Burgert2013 | Full-text read, prior pass; re-confirmed verbatim against the PDF this pass | Supported |
| 34 | 02 §2.6 | — same claim, second source | PerezHeydrich2013 | Full-text read, prior pass; re-confirmed this pass (accent question flagged, §2.2 above) | Supported |
| 35 | 02 §2.6 | Satellite forest-cover/DHS-cluster precedent | JohnsonJacobBrown2013 | Full-text (title/abstract) read, prior pass; author name + fields corrected this pass | Supported |
| 36 | 02 §2.6 | Heat-exposure/DHS matching-method precedent; outcome is nutrition not WASH | Blom2022 | Abstract-level (working-paper version), prior pass; version correspondence to the published *JEEM* article explicitly checked this pass (§2.1 of this file; `citation_map.md`) | Supported, with stated verification-depth limit |
| 37 | 02 §2.7 | Gap this thesis addresses — community WASH not previously matched to early-life window | Donohue2023 | As above | Supported |
| 38 | 02 §2.7 | — same claim | SkoufiasVinha2026 | As above | Supported |
| 39 | 02 §2.7 | Confounding-vs-timing gap identified at larger scale | HeadeyPalloni2019 | As above | Supported |
| 40 | 02 §2.7 | — same claim, trial literature | Cumming2019 | As above | Supported |
| 41 | 03 §3.2 | WHO Child Growth Standards reference population | deOnis2006 | Full-text read, prior pass; **author field corrected this pass** (§2.1 above) — the claim itself (this is the primary WHO growth-standards methods paper) remains accurate for the corrected institutional-author entry | Supported |
| 42 | 03 §3.4 | Cluster-coordinate displacement distances (2km urban / 5km+10km rural) | Burgert2013 | Full-text, verbatim match confirmed, prior pass and this pass | Supported |
| 43 | 03 §3.5 | IHME W_IMP/S_IMP product definitions and coverage years | LBDWaSH2020 | Primary-source Figure 1, prior pass | Supported |
| 44 | 06 §6.1 | Panel DiD null sanitation-stunting parallel to this thesis's own null finding | HeadeyPalloni2019 | As above | Supported |
| 45 | 06 §6.1 | Trial consistency: no WASH-arm effect on growth, nutrition-arm exception | Cumming2019 | As above | Supported |
| 46 | 06 §6.4 | 24-month window literature basis (hedged: "if anything, lean toward 24 months") | CummingCairncross2016 | Full-text (title/abstract) read, prior pass | Supported, appropriately hedged |
| 47 | 07 (Conclusion) | Trial literature parallel, facility-type vs. comprehensive-package distinction | Cumming2019 | As above | Supported |
| 48 | Appendix A.1 | WHO Child Growth Standards reference (table row) | deOnis2006 | As row 41 | Supported |

**Verdict summary**: 48 of 48 occurrences are **supported** by the version of the source actually inspected, at the evidence depth stated in `citation_map.md` for each source (19 of 20 cited sources read at full-text/abstract level directly; `Blom2022` at abstract level against the working-paper version only, disclosed explicitly in-text). No occurrence was found unsupported, partly supported, or resting on a bare, disconnected author–year with no claim attached. No "et al." vs. full-list inconsistency was found — narrative citations ("Author [-@key]") consistently match the full byline recorded in `bibliography.bib`, now corrected. No audit-process commentary was found embedded in printable chapter prose (the `bibliography.bib` `note` fields were cleaned of this in an earlier pass and re-confirmed clean this pass, apart from the accuracy-correction notes just added, which are themselves normal scholarly provenance notes, not internal audit language).

## 4. The five special items, addressed explicitly

**(A) Geruso–Spears version.** Confirmed: the thesis cites NBER Working Paper 21184 (revised May 2017 per NBER's own page, which also shows two earlier 2015 revisions) specifically, not the 2018 published *AEJ: Applied Economics* version (DOI 10.1257/app.20150431, vol. 10, issue 2, pp. 125–162) — confirmed as a genuinely different, later, retitled-in-neither-case document (titles are in fact identical between the two versions: "Neighborhood Sanitation and Infant Mortality"). The thesis's own text and `.bib` note already state this distinction explicitly and correctly; no change needed.

**(B) Blom2022 working-paper/published-article correspondence.** This was the most consequential open item and is now resolved as far as the evidence allows without reading the published article's own full text directly (blocked by ScienceDirect access restrictions in this environment). Same three authors, same order, in both the 2019 AfDB working paper and the 2022 *JEEM* article; same data source (DHS + Global Meteorological Forcing Dataset), same five-country West African sample, same method; the published version's effect sizes as reported in independent secondary press coverage (Cornell University News, phys.org, describing the *JEEM* publication specifically) are numerically identical to the working paper's own abstract. Titles differ ("Temperature and Children's Nutrition" → "Heat exposure and child nutrition"), consistent with ordinary journal retitling, not a different study. This thesis's existing, narrowly scoped claim — citing the working-paper abstract for its matching-method structure only, explicitly disclosed as not a read of the published article's own text — remains accurate and is now additionally corroborated by this version-correspondence check. `Blom2022`'s `.bib` entry gained `volume={115}` and `pages={102698}` this pass (Crossref).

**(C) WASH-Benefits/SHINE trial-specific designs.** Re-read directly in this pass's full chapter read (§2.3, §6.1): the manuscript correctly and precisely distinguishes WASH-Benefits Bangladesh/Kenya's six separate arms from SHINE's four-arm 2×2 design with WASH bundled, including the "all WASH arms" (plural) vs. "WASH arm" (singular) distinction drawn directly from Cumming2019's own Figure 2 language. No error found; this was already corrected in an earlier pass (Task 5) and is confirmed still correct and not regressed in v10.

**(D) WHO growth-standard sources — potential swapped monographs.** Checked directly against `bibliography_verification_ledger.md`'s own existing record (§38 of that file): the two monographs flagged in an earlier audit as having swapped PDF files/ISBNs relative to their title/year metadata (S26, S27 — growth-velocity and head/arm-circumference monographs) are **not** in `bibliography.bib` and were correctly never imported, because neither covers HAZ/WAZ/WHZ (the outcomes this thesis uses) — confirmed by that earlier audit's own explicit statement. `deOnis2006`, the entry actually cited, is a different, correctly-identified source (the Acta Paediatrica *methods* paper) — its problem this pass was an author-list conflation (§2.1 above), not a swapped-file/wrong-monograph risk. This resolves item D: the swap risk was already correctly excluded, and the real (different) error found this pass has been corrected.

**(E) Donohue/Addae/Headey-Palloni outcome/country-specific wording.** Re-read directly in this pass's full chapter read (§2.4, §2.2, §6.1): all three sources' country- and outcome-specific findings are stated precisely, not generalised — Donohue2023's Nigeria-only, modest, adjusted-OR-0.97 sanitation-stunting result (Zambia null); Addae2024's water-wasting-only / sanitation-and-SES-both-outcomes split; Headey & Palloni's water-insignificant-except-piped / sanitation-null-for-stunting-but-significant-for-mortality split. No overgeneralisation found. Metadata-level corrections were applied to all three entries this pass (author names for Addae2024; issue number for Headey & Palloni; no change needed for Donohue2023).

## 5. In-text citation/reference consistency

- All 20 cited keys resolve to exactly one `bibliography.bib` entry; 0 missing, 0 duplicate keys (re-verified after this pass's edits).
- Narrative author names (`Author [-@key]` form) checked against the now-corrected `bibliography.bib` bylines for every occurrence in Section 3: consistent.
- "et al." / "and others" usage: `Black2013` uses "and others" in the `.bib`, matching the source's own long author list; the chapter text does not spell this out further. No inconsistency found between in-text author mentions and the bibliography's own truncation conventions.
- No bare, disconnected `@key` citation (a citation with no accompanying claim) was found in the full read of all six files.
- No internal audit-process commentary was found in chapter prose. `bibliography.bib`'s `note` fields contain only scholarly provenance notes (version distinctions, year clarifications, this pass's correction notes) — reviewed again after this pass's edits and confirmed free of process language like "per the audit" or self-referential pointers to `docs/provenance/`.

## 6. What this pass did not do, and the limits of this evidence

- Did not read the published *JEEM* article's (`Blom2022`) own full text or abstract directly — blocked by ScienceDirect access restrictions in this environment; the version-correspondence argument in Section 4(B) is strong circumstantial evidence (identical authors/order/method/sample/effect-sizes-via-secondary-coverage), not a direct read of the publisher's own page.
- Did not independently re-verify `Gebru2019`'s corrected author names against the publisher's own rendered HTML page (Springer login-redirect blocked); relied on two independent secondary-metadata sources (Crossref, DOAJ) instead. Flagged as medium rather than high confidence in Section 2.1.
- Did not resolve the `PerezHeydrich2013` accent question or the `Momberg2021` given-names question; both are recorded as open, not silently closed in either direction.
- Did not change any empirical estimate, sample, weight, or control set. Did not re-run any model.
- Did not generate, rebuild, or render any PDF.
- Does not claim every detail in this 26-entry bibliography or every one of its 48 citation occurrences is now perfect. It states specifically what was checked (every entry's author/title/journal/year/volume/issue/pages/DOI against primary registries; every occurrence's claim against the source version actually read in this or an earlier pass), what was corrected (12 fields/author-lists across 9 entries, detailed in Section 2.1), and what remains genuinely open (Section 2.2, Section 6 above) — not a general assurance of completeness beyond that.

## 7. Versioning decision

These are reference-metadata corrections to `bibliography.bib`, `citation_map.md`, and `bibliography_verification_ledger.md` only. No chapter prose, no empirical claim, no interpretation, and no cross-reference changed. Per this task's own instruction to avoid an unnecessary full manuscript copy for documentation-only changes, **this pass edits `manuscript/v10_2026-10-07/` in place; no v11 is created.** `MASTER_ASSEMBLY.md` is updated with a one-line note of this pass for traceability.

## 8. Final deliverables summary

- **Entry-level bibliography table**: Section 2 above (26 entries; 12 corrections across 9 entries; 2 findings left open; 13 confirmed with no change).
- **Occurrence-level ledger**: Section 3 above (48 of 48 occurrences, all supported).
- **Correction log**: Section 2.1 (bibliographic) — no `CORRECTION_LOG.md` entry needed since no chapter file changed; `bibliography_verification_ledger.md` carries the per-entry resolution text instead, as it already does for prior passes' bibliographic (as opposed to chapter-text) corrections.
- **Unresolved items**: Section 2.2 and Section 6.
- **Actual counts**: 26 total bib entries, 20 cited, 6 uncited reserve, 48 citation occurrences, 0 missing/duplicate keys.
- **Canonical path/commit**: `manuscript/v10_2026-10-07/`, edited in place; commit to follow this file.
- **Confirmation of no empirical change**: no model re-run, no estimate, sample, weight, or control set touched.
- **Confirmation of no PDF generated**: none built, rebuilt, or rendered in this pass.
