# Language-edit and verification change log: Chapter 6 (Discussion and limitations)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/06_discussion_and_limitations.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `eefb55945a6830f4ed5b85141efae690fa0bf5cfa8f4e2beb414220e0ea45a94` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/06_discussion_and_limitations.md` | `1f6ba062869ff6915417d5748793e58e63a493b114b1761480f93ec09f16443f` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/06_discussion_and_limitations.tex` | `e1f9f3de16f1aea6b50c6d75139238e5330676e83c3222680e796994c8115ebe` |

The full word-level diff is in `06_discussion_and_limitations.worddiff.txt` (same folder): `[-…-]` marks removed text, `{+…+}` added text. The keyed numerical checks behind every item below are in `builds/previews/REVIEW-COPY_ch06-discussion-and-limitations_preview_*.checks/` and summarised in the `.verification.md` report with the same stem.

The author's instruction was to render the whole chapter without shortening it, removing substantive material or imposing a page target. Nothing was removed. The edited copy has 2,895 words against 2,239 in the canonical file; the increase comes from the corrections in section A and the clarifications in section B. The six headings and their numbers are unchanged, and the three citation commands (`HeadeyPalloni2019` narrative, `Cumming2019`, `CummingCairncross2016` narrative) keep their keys and order. Every number in the canonical file is still present in the copy (automated check); numbers added to the copy are listed in section D with their sources.

## A. Verified corrections applied to the publishing copy (canonical file unchanged)

Each correction rests on the stored output or reviewed chapter named. Whether the canonical v12 file is also corrected is the author's decision.

### A1. §6.2, item 4: region fixed effects are not used "only" in the community specification

- **Canonical passage.** "…region fixed effects are used only in the baseline's separate community specification (Section 4.3), not stacked with the household model's cluster fixed effects."
- **Evidence.** Chapter 4 §4.1 (household WASH with region fixed effects) and §4.4 (joint household–community model with $\delta_r$). Table 5.1 reports a household "Region FE" panel. Stored files: `outputs/household_community_wash/02_household_region_fe.csv` (`model_label` ∈ {`A1_household_natural_sample`, `A2_common_comparison_sample`}) and `05_joint_household_community.csv` (`development_family == model_C_joint_household_community`) both carry `fe_region_count == 114`.
- **Correction.** "In the baseline, region fixed effects appear in the household region-fixed-effects comparison (Section 4.1), in the separate community specification (Section 4.3) and in the joint household–community model (Section 4.4); they are never stacked with the household model's cluster fixed effects." The point the canonical sentence was making (no stacking with cluster fixed effects) is kept.

### A2. §6.1, paragraph 1: the "detectable, then not detectable" pattern does not hold for household sanitation

- **Canonical passage.** "…both studies find that a sanitation–stunting association that is detectable in less-controlled specifications is not detectable once a design better suited to netting out confounding is used…", attached to "null household- and community-sanitation associations".
- **Evidence.** Household sanitation–HAZ is not significant in the less-controlled household specification either: region FE, *p* = .522 (Table 5.1; `02_household_region_fe.csv`, `outcome == haz`, `term == _sani_hh_binary`, both sample labels *p* ≥ .05). Only community sanitation shows the pattern: 0.472, *p* < .001 minimally adjusted → 0.008, *p* = .900 with SES → 0.008, *p* = .894 fully adjusted (Table 5.2; `outputs/regressions/main_continuous_models.csv`, `term == sanitation_rate_loo_core`, `country_scope == pooled`, `outcome == haz`, models 1, 3, 4). For Headey and Palloni, Chapter 2 §2.2 and `citation_map.md` support only "not associated … once the within-region panel design is used"; they do not document a detectable association in a less-controlled specification of that study.
- **Correction.** The shared point is now that sanitation shows no detectable association with linear growth under the design better suited to netting out confounding. A new sentence states that the route differs: community sanitation is strongly associated with HAZ when minimally adjusted and loses the association once socioeconomic controls are added, with region fixed effects leaving it null (Table 5.2); household sanitation is not significant in either household specification (Table 5.1). No new number is introduced.

### A3. §6.1, paragraph 2: "despite high measured compliance" was attached to the WASH arms

- **Canonical passage.** "…every WASH-related arm in all three sites showed no statistically detectable effect on linear growth, despite high measured compliance…"
- **Evidence.** `citation_map.md` (row `Cumming2019`, full text read) and Chapter 2 §2.3 attach "despite high compliance" to the nutrition arm's small growth gain (`Cumming2019`, p. 6). Neither records a compliance statement for the WASH-only arms.
- **Correction.** The compliance phrase now sits with the nutrition arm, in Chapter 2's wording ("which the trial authors describe as a small gain despite high compliance"). Flag for the author: if the full text also reports high adherence in the WASH arms, the phrase could be restored there with a page locator, but no such record exists in this package.

### A4. §6.1, paragraph 3: the headline coefficient was cited without its unweighted counterpart

- **Canonical passage.** "The historical extension's positive, significant pooled water–HAZ association (1.03 per 10 points, *p* < .001) is independently computationally verified…"
- **Evidence.** Chapter 5 §5.6: "both are reported together whenever this coefficient is cited". Chapter 6 §6.4 itself says the weighting consequence is "reported alongside the main estimate in every instance". Stored: `m0004` (primary, weighted) 1.0256, *p* = 8.6×10⁻⁵; `m0008` (`unweighted_comparison`, same N = 23,018) 0.4147 [0.0290, 0.8008], *p* = .0352.
- **Correction.** "…1.03 per 10 percentage points, *p* < .001, or 0.41 [0.03, 0.80], *p* = .035, when the same observations are unweighted (Section 5.6)."

### A5. §6.1, paragraph 3: verification coverage stated precisely

- **Canonical passage.** "…is independently computationally verified (Section 5.6, Appendix B)…"
- **Evidence.** Chapter 5 §5.6 (publishing copy); `final_empirical_package_v3_2026-10-07/01_final_reporting_map.md` and `02_core_reporting_table.md` (status correction 2026-10-09); `model_coefficients_PRELIMINARY_AGGREGATE.csv`: 291 rows, 24 with `family == primary`.
- **Correction.** "The coefficient was independently reproduced with a second estimation library on a separately rebuilt sample, as were all 24 primary established-date cells. The other 267 of the 291 historical models passed internal design checks and, apart from two unweighted counterparts, were not re-estimated with a second library (Section 5.6, Appendix B)." This is Chapter 5's wording. It does not claim that all 291 models were reproduced.

### A6. §6.6, last sentence: wrong target for "the next section"

- **Canonical.** "…the next section draws together what this thesis's evidence does, modestly, support." §6.6 is the last subsection of Chapter 6, so the next section is Chapter 7 (`07_conclusion.md`, heading "7. Conclusion").
- **Correction.** "…Section 7 draws together what the evidence of this thesis does, modestly, support." ("Section" follows the cross-reference convention of Chapters 4–5, e.g. "discussed fully in Section 6".)

### A7. §6.5: DHS displacement wording

- **Canonical.** "…does not validate or correct for the (undisclosed, per-cluster) displacement distribution DHS actually applies…"
- **Evidence.** Chapter 3 §3.4 states the published displacement rule (urban up to 2 km; rural 99% up to 5 km, 1% up to 10 km) (citing `Burgert2013`). What is undisclosed is the displacement applied to each cluster, as Chapter 2 §2.6 says ("the displacement actually applied, which is undisclosed and specific to each cluster").
- **Correction.** "…it does not validate or correct for the displacement that DHS actually applied to each cluster, which is not disclosed…", with a pointer to Section 3.4. Buffer averaging is now described explicitly as "an assignment choice".

### A8. §6.5: IHME bounds terminology

- **Canonical.** "…its reported upper/lower confidence bounds are not used as regression inputs."
- **Evidence.** `docs/provenance/historical_wash_exposure_construction_spec_v1_2026-10-06.md` line 65 ("LOWER and UPPER are not used as exposure variables. They are not child-level confidence intervals.") and `historical_wash_analysis_specification_v1_2026-10-06.md` line 72 ("supplied bounds, not confidence intervals for the buffer mean or the regression coefficient"); issue register item 9.
- **Correction.** "…its supplied lower and upper bounds are not used as regression inputs."

### A9. §6.2, item 1: Ethiopia is not simply "excluded"

- **Canonical.** "…the historical extension uses 2014–2018 rounds across three (Ethiopia excluded; Section 1.4)."
- **Evidence.** Chapter 1 §1.4 and Chapter 5 §5.9: Ethiopia's 2016 round is retained as a provisional sensitivity analysis outside the established-date pooled sample (18 `sens_ethiopia_PROVISIONAL` rows; no pooled established-date row contains Ethiopia).
- **Correction.** "…2014–2018 rounds from three; Ethiopia's 2016 round enters only as a provisional sensitivity analysis outside the established-date pooled sample (Section 1.4)."

### A10. §6.5: residual-variation cross-reference

- **Canonical.** "…(0.20–0.88 percentage points depending on country and product) is modest relative to the 10-point scale used for reporting (Section 5.6)."
- **Evidence.** The range is correct (primary cells, `E_residual_sd_after_controls` min 0.2031 (Kenya W_IMP), max 0.8771 (Kenya S_IMP); `02_core_reporting_table.md` column E_resid_SD). Chapter 4 §4.6 states the range; Chapter 5 §5.6 displays only the pooled water–HAZ value, 0.43 (`m0004`, 0.4283).
- **Correction.** "…0.20 to 0.88 percentage points, depending on country and product (Section 4.6), and 0.43 percentage points for the pooled water–HAZ model (Section 5.6)." See also register FA-12 (the Chapter 4 §4.5 promise of per-country residual variation).

## B. Clarifications added to protect existing qualifications (author to confirm)

These sentences add no new estimate. Each restates a qualification that Chapters 1–5 or the stored outputs already establish.

| # | Where | Added text (abridged) | Source |
|---|---|---|---|
| B1 | §6.1 ¶2 | "No WASH-only arm …"; "adding WASH to nutrition brought no additional growth benefit over nutrition alone" (under the existing `Cumming2019` citation) | Ch. 2 §2.3 (`Cumming2019`, p. 2); `citation_map.md` row `Cumming2019` (full text) |
| B2 | §6.1 ¶2 | "The similarity of the findings does not validate this thesis's coefficients." | Ch. 2 §2.3–2.4 ("should not be read as confirming this thesis's specific coefficients") |
| B3 | §6.1 ¶2 | the joint-model cell's *p* = .043, "lies only just below that threshold" (canonical: "borderline significant") | Table 5.3; `05_joint_household_community.csv` (`model_C_joint_household_community`, `haz`, `_water_hh_binary`, *p* = .0434; 1 of 12 WASH cells < .05) |
| B4 | §6.2 ¶3 | no formal test of the baseline–historical difference; a significant coefficient beside non-significant ones does not show a significant difference | No such test exists in Chapter 5 or the stored outputs |
| B5 | §6.2 ¶4 | Table 5.8's common-sample row: 1.03 (own-eligible) vs. 1.64 (common sample), "a change in sample composition rather than in the window"; own-sample window differences combine both | Ch. 5 §5.7 and Table 5.8; `window_common_sample_PRELIMINARY_AGGREGATE.csv` (W_IMP, HAZ, POOLED_ESTABLISHED, post_12m, both bases) |
| B6 | §6.3 ¶2 | if measurement or non-response were related to both WASH and growth, the associations could differ from the full eligible population, direction unknown | Ch. 3 §3.8 (cannot correct for differential non-response) |
| B7 | §6.4 ¶2 | "so equal weight totals do not imply equal influence"; "Neither the weighted nor the unweighted estimate is population-representative" | Ch. 4 §4.5; Ch. 3 §3.8; Ch. 5 §5.6 |
| B8 | §6.4 ¶4 | the competing confounder reading of wealth and the wealth sensitivity (1.01 vs. 1.03), which "does not adjudicate between the two readings" | Ch. 3 §3.8; Ch. 5 §5.8; `sens_wealth` pooled W_IMP HAZ (`m0024`) = 1.0088 |
| B9 | §6.5 ¶1 | the exposure is "not fully independent of the survey data used in the analysis"; the Ghana-excluded row pools Kenya and Nigeria, so Kenya's overlap remains and the sensitivity "addresses only part of the overlap" | Ch. 5 Table 5.9 note; `o003` (`sens_overlap_excl_GH_water`, `sample_group == POOLED_KE_NG`) |
| B10 | §6.5 ¶2 | migration misassignment is "a form of exposure measurement error whose extent in these samples is unknown" | Issue register item 9 ("cannot be resolved with available data") |
| B11 | §6.5 ¶4 | the historical standard errors "do not reflect uncertainty in the exposure surface itself" | Follows from the bounds not being used as inputs (A8 sources) |
| B12 | §6.5 ¶5 | Ethiopia's estimates "remain provisional and outside the established-date pooled family" | Ch. 5 §5.9; Appendix C |
| B13 | §6.6 | both analyses cross-sectional and observational; fixed effects remove only what is shared within a region or cluster, so within-cluster confounding may remain (Section 4.2); non-significance = inconclusive, not absence; four countries selected for data availability and recency (Section 1.4) | Ch. 4 §4.2; Ch. 5 §5.1; Ch. 1 §1.4 |

## C. Language edit (Humanizer v2.9.1)

The Humanizer skill was read in full and applied to this publishing copy only.

- All 19 punctuation em dashes were replaced by full stops, commas, colons, semicolons or parentheses. Range and compound en dashes (2022–2025, water–HAZ, WASH–growth) were kept, as in Chapters 2–5.
- Very long sentences were split, notably the opening Headey–Palloni sentence and the SHINE/WASH-Benefits sentence in §6.1, and the single §6.5 paragraph was divided into six paragraphs (overlap; residence; displacement; modelled and annual surface; residual variation and Ethiopia). The order of the arguments is unchanged.
- §6.4 now opens with its framing sentence as a separate paragraph, followed by one paragraph per design choice.
- Audit-style self-reference was reduced ("which this paragraph is careful to keep separate" → "this paragraph keeps the two separate"; "This is stated as its own subsection because it is the single most tempting…" → "This point has its own subsection because it is the most tempting…").
- Bold emphasis was kept (8 spans, as in the canonical file), pending the ch01 bold → italics decision. Italics were kept.
- Hedges kept: "broadly consistent", "consistent with", "could instead, or in addition", "if anything", "modestly", "may".

## D. Numbers added to the copy, with sources

| Number | Where | Source |
|---|---|---|
| 0.41, [0.03, 0.80], .035 | §6.1 ¶3 | `m0008`; Ch. 5 §5.6 |
| 24, 267, 291 | §6.1 ¶3 | aggregate register (291 rows, 24 `primary`); Ch. 5 §5.6 |
| .043 | §6.1 ¶2 | Table 5.3; `05_joint_household_community.csv` |
| 1.64 (and 1.03) | §6.2 ¶4 | Table 5.8; `window_common_sample_PRELIMINARY_AGGREGATE.csv` |
| 2016 | §6.2 item 1 | Ch. 1 §1.4; Ch. 3 §3.5 |
| 1.01 (and 1.03) | §6.4 ¶4 | Table 5.9; `sens_wealth` |
| 0.43 | §6.5 ¶5 | `m0004` `E_residual_sd_after_controls` = 0.4283; Ch. 5 §5.6 |

Other added digits are section numbers in cross-references (Sections 1.4, 3.4, 3.8, 3.9, 4.1, 4.2, 4.4, 4.6, 5.6, 5.8, 7; Tables 5.1, 5.2, 5.8). `lint` confirms each has a target.

## E. Rendering changes (copy only)

- "(Section 2.3) [@Cumming2019]" printed as doubled parentheses "(Section 2.3) (Cumming et al. 2019)". The cross-reference moved earlier in the sentence ("In the same trials (Section 2.3), …"); the citation stays at the end of the sentence.
- Section ranges written with an en dash broke across lines after the dash ("Sections 1.2–" / "1.3"); pandoc emits `--`, which permits a break, as recorded in the Chapter 5 log. They are now "Sections 1.2 and 1.3", "Sections 5.1 and 5.2" and "Sections 3.5 to 3.7".
- "Appendix A/B/C" are tied with a non-breaking space (4 places); "Appendix" and "B)" had been split across lines.
- Shared files (template, filter, scripts, drivers, bibliography) were **not** changed.

## F. Points for the author (nothing below was changed)

- **F1.** §6.4 says the 12-month window was chosen "before any model was estimated"; Chapter 5 §5.6 says the headline choice was "made before any coefficient was examined". The two are compatible, but only the second is documented in the reviewed chapters; the stronger wording was kept as written.
- **F2.** Stored family `sens_overlap_excl_GH_KE_water` (`o002`, `o005`, `o008`) excludes both overlap countries and leaves Nigeria alone (water–HAZ 0.70, identical to Nigeria's own primary cell). Chapter 5 does not report it, so Chapter 6 does not cite it. Decide whether either chapter should mention it.
- **F3.** Chapter 6 does not discuss the current-age heterogeneity results (§5.5), the Nigeria community-sanitation instability (§5.4) or the significant negative Ghana sanitation–HAZ historical cell. No text was added; Chapter 5 already qualifies each.
- **F4.** Section 6.2 item 4 lists "maternal age and education, literacy, household size and wealth quintile" as examples ("including"); Section 3.4's full covariate list also has child sex, current age, birth order and urban/rural residence (the last absorbed under cluster fixed effects).
- **F5.** The chapter has no policy-implications passage and none was added. Any such text should stay within the limits in §6.6.
- **F6.** "Section 2" (the literature review) and "Section 7" follow the thesis's "Section N" convention for whole chapters. Change to "Chapter N" throughout at assembly if preferred.
