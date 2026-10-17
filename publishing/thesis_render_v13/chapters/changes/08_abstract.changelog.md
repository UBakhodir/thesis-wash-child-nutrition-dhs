# Verification and language-edit change log: Abstract

Status: **Awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

The abstract is the publishing system's `abstract` unit. It is unnumbered (`\section*{Abstract}`), is not a chapter and is not "Chapter 8": `08_abstract.md` is only a source filename. The thesis has seven main chapters.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/08_abstract.md` at academic source commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `ec903ca5a0d281dfeb4313b16a14c4132a79f391957c5592e42ca7ae46a3eb44` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/08_abstract.md` | `ba56a2f44f86bb9f92d53c2ce281068dc2eca52f3c3d04248323f5c6e1950def` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/08_abstract.tex` | `48fdd5de16348d793dd9696bd235f2aab196491229ad62c27e654544e6fd27cc` |
| Word diff | `chapters/changes/08_abstract.worddiff.txt` | `2d3c6c593cc92ee9b3f4c8d86e54ca79268a87d4adc6304859837f4749274f8e` |

The preview PDF was built at local publishing commit `a881337`, which contains the md and tex files with these hashes. The word diff marks removed text as `[-…-]` and added text as `{+…+}`; `<nbsp>` marks a no-break space.

**Sources checked against.** The canonical abstract was read in full alongside the reviewed **publishing copies** of Chapters 1–7 (which carry documented corrections not yet in the canonical files: FA-9, FA-14, FA-16), the claim–evidence ledger, `final_empirical_package_v3_2026-10-07/00_results_index.md`, `01_final_reporting_map.md`, `02_core_reporting_table.md`, Appendix B, the independent-audit records `07_update_2026-10-07_pass2.md` and `09_update_2026-10-07_pass4.md`, `citation_map.md`, and the stored public outputs `outputs/household_community_wash/03_household_cluster_fe.csv`, `outputs/regressions/main_continuous_models.csv` and `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`. No restricted data was read, no model was run, no specification was changed and nothing was recomputed under another inference convention.

**Length.** The author instructed that no page target be imposed and that the abstract not be shortened to save pages. The copy has 835 words against 440 in the canonical file. The increase comes from sections A and B, and from splitting one paragraph into five. The rendered abstract body is 2 pages (preview pp. 1–2). Page-budget editing is deferred to final assembly (FA-5, FA-11).

**Citations.** The canonical abstract has no citation commands, and none was added (see F1).

## A. Verified substantive corrections (canonical file unchanged)

Each item corrects a statement that is inaccurate or misleading against the reviewed chapters or the stored outputs. Whether the canonical v12 file is also corrected is the author's decision (register FA-17).

### A1. "an undocumented measurement-subsample sampling weight" (author's flag A; FA-16 F4)

- **Canonical.** "…substantial, explicitly documented methodological qualifications: sensitivity to the pooled weighting convention …, an undocumented measurement-subsample sampling weight, and area- rather than population-weighted exposure averaging…"
- **Evidence.** Chapter 3 §3.8: weighting uses `PERWEIGHT`, normalised to equal country totals; "the documented sampling weight for measured anthropometry specifically … could not be located in official DHS documentation"; the working inference is that within-survey PERWEIGHT normalisation removes a constant measurement-subsample selection factor, and it cannot correct for differential non-response among eligible children. Chapter 6 §6.3; Chapter 7 publishing copy A2.
- **Why it is misleading.** The weight actually used (PERWEIGHT) is documented. What is undocumented is whether an anthropometry-specific (measurement-subsample) weight exists or is required. The open question is how selection into measurement affects which children the estimates describe.
- **Correction.** "The models are weighted with the IPUMS-DHS PERWEIGHT variable. No official documentation of an anthropometry-specific weight for the measured subsample could be located, so the treatment of measurement selection rests on a stated working inference, and the estimates are weighted conditional associations among eligible measured children rather than population-representative estimates."

### A2. "a carefully bounded first attempt" (author's flag B; FA-16 F4)

- **Evidence.** Chapter 1 §1.5 ("a transparently documented, preliminary attempt"; a particular combination of countries is not by itself evidence of novelty); Chapter 7 publishing copy A4 ("a documented, preliminary attempt"). No reviewed chapter or citation record establishes priority.
- **Correction.** The contribution sentence now reads "…and a preliminary, qualified extension that assigns modelled local coverage to each child's early-life window, each read with its own limitations." "Carefully bounded" (self-evaluative) and "first" (an unsupported priority claim) are removed.

### A3. Historical headline presented without its selection status (author's flag C; FA-16 F4)

- **Canonical.** "This extension's pooled, established-date water coverage–height-for-age association is positive and statistically significant (β = 1.03 …)". Nothing indicates that other primary cells are also nominally significant.
- **Evidence.** `model_coefficients_PRELIMINARY_AGGREGATE.csv`, `family == primary` (24 rows, all `window == post_12m`, `weighted == True`). Six rows have `p_value < .05`: `m0001`, `m0003`, `m0004`, `m0050`, `m0051`, `m0142`. Chapter 5 §5.6; Chapter 6 §6.2; Chapter 7 publishing copy A1.
- **Correction.** "The selected primary finding is the pooled established-date association … It is one of six nominally significant cells (*p* < .05) among the 24 primary cells, and no adjustment for multiple testing was applied." The six cells are not listed individually.

### A4. Computational verification stated without its coverage (author's flag D)

- **Canonical.** "…independently reconstructed and numerically confirmed with a separate implementation and sample during this project…" This is true of the headline cell, but it says nothing about how far the verification extends or what it does not establish.
- **Evidence.** The 24 primary cells were reproduced with `linearmodels.PanelOLS` on a separately rebuilt sample (`07_update_2026-10-07_pass2.md`; SE, CI and *p* reconciled for 24/24 cells in `09_update_2026-10-07_pass4.md`; Appendix B). The register has 291 rows, 267 of them non-primary. Chapter 5 §5.6: the other 267 "passed internal design checks; apart from two unweighted counterparts verified in Appendix B, they were not re-estimated with a second library."
- **Correction.** "All 24 primary cells were reproduced with a second estimation library on a separately rebuilt sample; the other 267 of the 291 historical models passed internal checks and, apart from two unweighted counterparts, were not re-estimated with a second library. This reproduction confirms the computation, not causality or robustness to multiple testing."

### A5. The 59-country literature parallel attached to the whole community attenuation pattern

- **Canonical.** "…a pattern consistent with, though not conclusive evidence of, confounding by local socioeconomic conditions, and one with a specific parallel in panel evidence from 59 countries that similarly finds no sanitation–stunting association…"
- **Evidence.** Chapter 2 §2.2 and Chapter 6 §6.1 (publishing copy, correction A2) restrict the Headey–Palloni parallel to the null **sanitation** findings, at both household and community level. Headey and Palloni report that piped water does predict reduced stunting (`citation_map.md` row `HeadeyPalloni2019`), so the parallel does not extend to the water attenuation.
- **Correction.** "The null sanitation results at both levels parallel subnational panel evidence from 59 countries in which sanitation is not associated with stunting once time-invariant regional confounding is netted out." The word "panel" describes the cited study's design, not this thesis.

No numerical error was found in the canonical abstract. All of its numbers (.062; the 5% and 10% thresholds; 1.03, [0.51, 1.54], *p* < .001; 0.41, [0.03, 0.80], .035; 59) match the stored records by named key (59 matches Chapter 2 and `citation_map.md`).

## B. Clarifications added (existing qualifications restated; no new estimate)

| # | Added text (abridged) | Source |
|---|---|---|
| B1 | four countries "selected for data availability and recency, not to represent the region as a whole" | Ch. 1 §1.4; Ch. 6 §6.6 |
| B2 | data sources and rounds: most recent DHS round, 2022 to 2025; earlier rounds Ghana 2014, Kenya 2014, Nigeria 2018 harmonised by IPUMS-DHS; IHME modelled annual gridded coverage | Ch. 1 §1.4; Ch. 3 §§3.1, 3.4, 3.5, 3.9 |
| B3 | household = improved/unimproved facility classification; community = leave-one-out rate among the other **sampled** households in the same DHS cluster | Ch. 3 §3.3 |
| B4 | why each fixed-effects structure: cluster FE compare households within a cluster; the community rate "varies almost only between clusters" | Ch. 4 §§4.2–4.3 (within-cluster SD ≈ 0.007/0.011 vs. overall ≈ 0.35) |
| B5 | household sanitation–HAZ *p* = .548; "inconclusive rather than evidence that no association exists" | Table 5.1; Ch. 5 §5.1; Ch. 7 |
| B6 | fully adjusted community HAZ water *p* = .573 and sanitation *p* = .894, "both inconclusive"; "none of the community associations remains statistically significant" | Table 5.2; `main_continuous_models.csv` model 4, 0 of 6 cells *p* < .05; Ch. 7 B3 |
| B7 | "does not establish confounding as the explanation" (canonical: "though not conclusive evidence of") | Ch. 5 §5.2; Ch. 7 |
| B8 | the historical sample is independently constructed; it asks its question "within this sample" | Ch. 1 §§1.3–1.4; Ch. 3 opening |
| B9 | window "the first 12 postnatal months"; cluster fixed effects and country-specific birth-year terms | Ch. 3 §3.7; Ch. 4 §4.6; record `m0004` `window == post_12m` |
| B10 | Ethiopia 2016 enters only as a provisional sensitivity analysis | Ch. 1 §1.4; Ch. 5 §5.9; 18 `sens_ethiopia_PROVISIONAL` rows |
| B11 | exposure "neither observed household access nor population-weighted coverage" (canonical had "area- rather than population-weighted exposure averaging") | Ch. 3 §3.5; Ch. 7 B5 |
| B12 | the extension "does not repeat the household-versus-community comparison" | Ch. 1 §1.5; Ch. 7 A3 |
| B13 | "equal country weight totals do not give the three countries equal influence on the pooled slope" | Ch. 4 §4.5; Ch. 5 §5.6 |
| B14 | DHS/IHME input overlap (Ghana, Kenya); current residence as proxy for early-life residence | Ch. 1 §1.7; Ch. 6 §6.5 |
| B15 | the historical result "does not overturn the more cautious baseline conclusions" | Ch. 7 ¶6 |

## C. Language edits (Humanizer v2.9.1; meaning unchanged)

- The single 440-word paragraph became five paragraphs in the canonical order of argument: question and design → baseline → historical extension → historical findings and qualifications → interpretation and contribution. The canonical text's explanation of why the baseline–historical contrast is not a timing test moved from the extension's introduction to the closing paragraph. The motivation sentence ("It responds to one limitation of the baseline design, which records WASH once, at the survey date…") keeps the canonical point that the extension is "a measurement response to one dimension of the single-round baseline design's inability to assign exposure near each child's own developmental period".
- Long multi-clause sentences were split; "examines associations between … and …" → "asks whether … are associated with …".
- Both punctuation em-dash pairs were removed. The copy contains no em or en dashes; the range "2022 to 2025" is written out. Compound slashes ("outcome/exposure") became "outcome and exposure".
- "attenuates to statistical insignificance" → "none … remains statistically significant"; "falling to" → "unweighted, on the same 23,018 observations, it is 0.41".
- The serial comma before "and Nigeria" was dropped, matching the publishing copies of Chapters 6–7.
- Abbreviations HAZ, WAZ, WHZ, WASH, DHS and IHME are defined at first use. "IHME" is spelled out as the Institute for Health Metrics and Evaluation (factual expansion of an existing source, not a new source).
- No generic claims of importance, novelty or policy impact were added. The policy sentence keeps the canonical meaning ("not … evidence either for or against the effectiveness of WASH investment as a policy instrument").

## D. Rendering fixes (copy only)

- No-break spaces in "*p* = …", "*p* < …", "95% CI" and inside CI brackets, after the first build broke "*p* =" / ".548" and "[0.51," / "1.54]" across lines. Tying the whole "95% CI [a, b]" unit produced two overfull lines, so a break is allowed between "CI" and "[" (commit `91dd641`).

## E. Numbers in the copy

Every number in the canonical abstract is still present. Numbers added, all traced by named key in `verify_abstract.tsv`: *p* = .548 (household sanitation–HAZ, primary); *p* = .573 and .894 (community HAZ, model 4); 23,018 (N, `m0004` = `m0008`); 24, six, 267, 291 (aggregate register); 2014, 2014, 2018, 2016 and "2022 to 2025" (survey rounds, Ch. 1 §1.4); 12 (post-12-month window); 59 (canonical, kept).

## F. Decisions for the author (nothing changed)

- **F1. Uncited literature parallel.** The 59-country sentence (Headey and Palloni) has no citation command, as in the canonical abstract. Options: keep it uncited, add `[@HeadeyPalloni2019]`, or remove the sentence. Adding a citation would put a reference in the abstract and is left to the author.
- **F2. Paragraphing and length.** Five paragraphs, 835 words, against one paragraph of 440. Keep, or condense at final assembly (FA-11).
- **F3. Joint-model household water–HAZ *p* = .043** (Table 5.3) is not mentioned, consistent with Chapter 7 (FA-16 F1; ch01 open point 7).
- **F4. Sample sizes.** Only N = 23,018 is stated (to show the weighted and unweighted fits use identical observations). Baseline N (36,040 common HAZ sample; 36,985 community HAZ) could be added.
- **F5. Naming of data sources.** IPUMS-DHS and IHME are now named; the canonical named only DHS.
- **F6. Placement.** The abstract is the first numbered page in `drivers/thesis-body.tex`. This is a recorded publishing choice (R-14a), not a university requirement: the 23 July 2026 guidelines list no abstract among the required components. Under that driver the abstract counts toward the main-text pages (FA-5).
