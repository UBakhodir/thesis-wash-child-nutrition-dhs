# Language-edit and verification change log: Chapter 7 (Conclusion)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/07_conclusion.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `56285b5d4d032583ef3d107cf47dc57197356e033b3ef02ba03121e60348e9e6` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/07_conclusion.md` | `de7fa76cd09ced590986388a326bb6f87dcc20a4992df1ba37ef69253d72b3f9` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/07_conclusion.tex` | `8d9594374fc234ec0cdd890953e9a5afa09f1d5d555c85960170a13bc4e1c4d2` |

The preview PDF was built at publishing commit `9c15c96`, which contains the two files with these hashes. Recording the hashes here is the only change to this log after that commit.

The full word-level diff is in `07_conclusion.worddiff.txt` (same folder): `[-…-]` marks removed text, `{+…+}` added text. The keyed numerical checks behind every item below are in `builds/previews/REVIEW-COPY_ch07-conclusion_preview_*.checks/` and summarised in the `.verification.md` report with the same stem.

The author's instruction was to render the whole chapter without shortening it or imposing a page target. Nothing substantive was removed. The edited copy has 1,096 words against 640 in the canonical file. The increase comes from the corrections in section A and the clarifications in section B, which restate qualifications that Chapters 1–6 already establish. The chapter heading "7. Conclusion" is unchanged; the canonical file has no subsections, and none was added. The single citation command (`[@Cumming2019]`) keeps its key. The canonical file had four paragraphs; the copy has nine, in the same order of argument: question → baseline (household, community, literature) → historical extension and its qualifications → contribution → what the evidence cannot establish → future research. Every number in the canonical file is still present in the copy (automated check); numbers added to the copy are listed in section D with their sources.

## A. Verified corrections applied to the publishing copy (canonical file unchanged)

Each correction rests on the stored output or reviewed chapter named. Whether the canonical v12 file is also corrected is the author's decision (register FA-16).

### A1. ¶3 (canonical): the headline was presented as the one result that "stands out"

- **Canonical passage.** "The preliminary historical extension … produces one result that stands out from the rest of this thesis's findings: a positive, statistically significant pooled association between local water coverage and height-for-age (β = 1.03 …)".
- **Evidence.** `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`, `family == primary` (24 rows, all `window == post_12m`, `weighted == True`): six rows have `p_value < .05` (`m0001` Ghana water–HAZ, `m0003` Nigeria water–HAZ, `m0004` pooled water–HAZ, `m0050` Nigeria water–WAZ, `m0051` pooled water–WAZ, `m0142` Ghana sanitation–HAZ, negative). Chapter 5 §5.6 (publishing copy): "It is **not** the only nominally significant cell … A reader … should therefore see six significant cells, not one"; Chapter 6 §6.2.
- **Why it is wrong.** The phrase implies a single significant historical result. It is the selected headline cell, chosen as the pooled established-date estimate for the primary outcome and window, and one of six nominally significant primary cells.
- **Correction.** "The selected headline cell is the pooled established-date association … It is not the only nominally significant historical result. Six of the 24 primary cells have *p* < .05, one of them a negative Ghana sanitation cell (Section 5.6)."

### A2. ¶3 (canonical): "rests on an undocumented measurement-subsample sampling weight"

- **Evidence.** Chapter 3 §3.8: weighting uses PERWEIGHT (normalised to equal country totals); "the documented sampling weight for measured anthropometry specifically … could not be located"; the project's working inference is that within-survey PERWEIGHT normalisation removes a constant measurement-subsample selection factor. Chapter 6 §6.3 says the same; `historical_wash_issue_register_v1_2026-10-07.md` item 1.
- **Why it is wrong.** The estimate does not use an undocumented weight. It uses the documented PERWEIGHT, and what remains undocumented is whether an anthropometry-specific weight exists; the analysis relies on a stated working inference.
- **Correction.** "The weighting of the measured subsample relies on a working inference, because no official documentation of an anthropometry-specific sampling weight could be located (Section 6.3)."

### A3. ¶4 (canonical): the historical extension described as adding temporal variation "into that comparison"

- **Canonical passage.** "…a transparent, side-by-side comparison of household and community WASH exposure … together with a bounded, honestly limited first attempt to introduce genuine temporal exposure variation into that comparison."
- **Evidence.** Chapter 1 §1.5: "two separate contributions in two separate samples, and they should not be read as one combined design … It does not reproduce the household-versus-community comparison: the historical data source does not distinguish a child's own household from its surrounding community."
- **Correction.** The contribution is now stated as two separate contributions in two separate samples (Section 1.5), with the sentence: "Because the historical data cannot separate a child's own household from its community, this second contribution does not extend the household-versus-community comparison."

### A4. ¶4 (canonical): "first attempt"

- **Evidence.** Chapter 1 §1.5 calls it "a transparently documented, preliminary attempt" and states that a particular combination of countries is not by itself evidence of novelty. No reviewed chapter or citation record establishes that it is the first such attempt in the literature.
- **Correction.** "a documented, preliminary attempt". The wording no longer carries an unsupported priority claim.

### A5. ¶4 (canonical): future work on "a genuinely panel or repeated-cross-section design"

- **Evidence.** Chapter 1 §1.2 places the baseline itself in "the cross-sectional, repeated-survey-round observational literature", and the historical extension also pools cross-sections. The design class that Chapter 1 §1.2 and Chapter 2 contrast with this one is the panel design that tracks indicators over successive rounds within the same geographic units (`HeadeyPalloni2019`, Section 2.2).
- **Why it is wrong.** A repeated cross-section is not a different design from the one this thesis already uses, so recommending it as the next step is inconsistent with Chapter 1.
- **Correction.** "…geospatial WASH matching could be combined with a design that follows the same geographic units over successive survey rounds (Section 1.2)."

### A6. ¶4 (canonical): "extending the historical approach to all four countries"

- **Evidence.** Chapter 1 §1.4, Chapter 5 §5.9 and Appendix C: Ethiopia's 2016 round is already estimated, as a provisional sensitivity (18 `sens_ethiopia_PROVISIONAL` rows), because the Ethiopian-calendar interview-date conversion could not be validated.
- **Why it is imprecise.** The approach has been applied to Ethiopia; what is missing is a validated date conversion that would let Ethiopia enter the established-date family.
- **Correction.** "…validating the Ethiopian interview-date conversion would allow the historical approach to cover all four countries on an established-date basis (Appendix C)."

### A7. ¶3 (canonical): the historical result "cannot be cleanly attributed to exposure timing alone"

- **Evidence.** Chapter 1 §1.3 and Chapter 6 §6.2: the historical question is asked within its own sample; what cannot be attributed to timing is the *contrast* between the baseline and historical results, because the samples differ in children and rounds, exposure construction, eligibility rules and control sets.
- **Correction.** "…the contrast with the baseline results cannot be attributed to exposure timing, because the two samples differ at the same time in their children and survey rounds, exposure construction, eligibility rules and control sets (Section 6.2)." The four respects are Chapter 6 §6.2's list.

### A8. ¶1 (canonical): the early-life measure described as distinguished "throughout" for four countries

- **Evidence.** Chapter 1 §1.4: the historical extension uses an earlier round for three countries; Ethiopia is a provisional sensitivity only.
- **Correction.** A sentence was added: "The second measure was constructed for an earlier survey round in three of the four countries, with Ethiopia retained only as a provisional sensitivity analysis (Section 1.4)." "Local WASH coverage" became "modelled local WASH coverage" (Chapter 3 §3.5).

## B. Clarifications added to protect existing qualifications (author to confirm)

These sentences add no new estimate. Each restates a qualification that Chapters 1–6 or the stored outputs already establish, and that the task brief requires wherever the corresponding result is summarised.

| # | Where (copy) | Added text (abridged) | Source |
|---|---|---|---|
| B1 | ¶2 | "Under this design, that is an inconclusive result, not evidence that no association exists." | Ch. 5 §5.1; Ch. 6 §6.6 |
| B2 | ¶3 | community measure "answers a related but distinct question"; leave-one-out rate among the other sampled households; region rather than cluster fixed effects | Ch. 1 §1.1; Ch. 4 §4.3; Ch. 5 §5.2 and Table 5.2 note |
| B3 | ¶3 | "no longer statistically significant for any pair" (canonical: "attenuates to statistical insignificance") | `main_continuous_models.csv`, `country_scope == pooled`, `model == 4`: all six water/sanitation × HAZ/WAZ/WHZ cells *p* ≥ .05 |
| B4 | ¶4 | the exposure is "not a randomised, comprehensive intervention package" | Ch. 2 §2.3; Ch. 6 §6.1 |
| B5 | ¶5 | area average of modelled coverage around displaced coordinates; "neither observed historical household access nor population-weighted coverage" | Ch. 3 §3.5; Ch. 5 §5.6; Ch. 6 §6.5 |
| B6 | ¶5 | verification coverage: headline and all 24 primary cells reproduced with a second library on a separately rebuilt sample; 267 of 291 internally checked; reproduction "does not adjust for the number of cells tested, and it does not make the association causal" (canonical: "independently reconstructed and confirmed computationally during this project") | Ch. 5 §5.6; Ch. 6 §6.1; aggregate register |
| B7 | ¶6 | "equal country weight totals do not give the three countries equal influence on the pooled slope" | Ch. 4 §4.5; Ch. 5 §5.6; Ch. 6 §6.4 |
| B8 | ¶6 | "weighted conditional associations among eligible measured children, not population-representative effects" | Ch. 3 §3.8; Ch. 6 §6.3 |
| B9 | ¶6 | DHS/IHME input overlap (Ghana, Kenya); current residence as proxy for early-life residence; residual within-cluster variation much smaller than the 10-point reporting scale | Ch. 1 §1.7; Ch. 5 §5.6 (0.43 pp); Ch. 6 §6.5 |
| B10 | ¶6 | Ethiopia's estimates "remain provisional and outside the established-date pooled family" | Ch. 5 §5.9; Ch. 6 §6.5 |
| B11 | ¶8 | "Fixed effects remove only what is shared within a region or cluster"; four countries selected for data availability and recency, not to represent Sub-Saharan Africa | Ch. 1 §1.4; Ch. 6 §6.6 |
| B12 | ¶8 | weak or inconclusive associations "do not show that such investment lacks value, and no causal policy effect or cost-effectiveness was estimated" | Ch. 1 §1.6; Ch. 6 §6.6; no such estimate exists in Ch. 5 or the stored outputs |

## C. Language edit (Humanizer v2.9.1)

The Humanizer skill was read in full and applied to this publishing copy only.

- All 10 punctuation em dashes were replaced by full stops, colons, commas or restructured sentences. The compound en dash in "water–HAZ" was kept, as in Chapters 2–6. There is no bold or italic emphasis apart from the italic *p*.
- The four long canonical paragraphs (the second had a 115-word sentence) were divided into nine, in the same order of argument.
- Self-evaluative and audit-style phrases were removed or replaced with what they refer to: "transparent", "honestly limited", "a careful accounting", "has tried to describe honestly", "and this thesis does not claim otherwise", "This result is reported with the full set of qualifications". The repeated "this thesis does not …" pattern was replaced by positive, bounded statements where possible.
- "a promising, carefully qualified preliminary finding, not a settled result" became "a preliminary, qualified finding rather than a settled one". "Promising" is an evaluative word not supported by a stated criterion; the author may restore it (section F, F5).
- "sit consistently alongside, rather than in contradiction to" became "are broadly consistent with", the wording of Chapter 6 §6.1. "suggestive rather than confirmatory" is kept.
- Hedges kept: "consistent with", "cannot establish … as the only explanation", "broadly consistent", "suggestive rather than confirmatory", "preliminary", "could".

## D. Numbers added to the copy, with sources

| Number | Where | Source |
|---|---|---|
| six, 24 (significant / primary cells) | ¶5 | aggregate register, `family == primary`, `p_value < .05`; Ch. 5 §5.6 |
| 267, 291 | ¶5 | aggregate register (291 rows; 267 not `primary`); Ch. 5 §5.6 |
| "two unweighted counterparts" | ¶5 | Ch. 5 §5.6; Ch. 6 §6.1 (Appendix B) |
| three outcomes, two exposures | ¶2 | `03_household_cluster_fe.csv`, primary label (3 × 2 cells) |
| 10-point reporting scale | ¶6 | Ch. 5 §5.6 |

All other numbers (1.03, [0.51, 1.54], < .001, 0.41, [0.03, 0.80], .035, 23,018, .062, 5%, 10%) are canonical and were re-checked against the stored rows (`verify_ch07.tsv`). Other added digits are section numbers in cross-references (Sections 1.2, 1.4, 1.5, 2.3, 3.5, 4.3, 5.1, 5.2, 5.6, 6.2, 6.3, 6.5, 6.6; Appendices B and C). `lint --publishing-copies` confirms each has a target.

## E. Rendering changes (copy only)

- "Section", "Sections" and "Appendix" are tied to the following number or letter with a no-break space (U+00A0; 16 places), as Chapter 6 did for "Appendix". The first build broke "(Section" / "1.2)" across lines on page 3.
- Shared files (template, filter, scripts, drivers, bibliography) were **not** changed.

## F. Points for the author (nothing below was changed)

- **F1.** The joint-model household water–HAZ cell (*p* = .043, negative; Table 5.3) is not mentioned. The conclusion's household statement refers to the cluster-fixed-effects specification, which is correct as written. Same question as Chapter 1 open point 7.
- **F2.** The Nigeria community-sanitation specification instability (§5.4) and the current-age heterogeneity (§5.5) are not mentioned, as in the canonical file. This parallels the Chapter 6 completeness question (register FA-15 C). No text was added.
- **F3.** "Section N" refers to whole chapters (e.g. "Section 6"), following the thesis's convention (Chapter 6 changelog F6).
- **F4.** The abstract (`08_abstract.md`, not rendered in this session) still contains two phrasings corrected here: "an undocumented measurement-subsample sampling weight" (A2) and "a carefully bounded first attempt" (A4). It also gives the headline cell without saying that six of 24 primary cells are nominally significant. Check these when the abstract is rendered (register FA-16).
- **F5.** "promising" was removed (section C). Restore it if intended.
- **F6.** The three future-research directions are the canonical three, sharpened by A5 and A6. No new direction, recommendation or effect magnitude was added.
