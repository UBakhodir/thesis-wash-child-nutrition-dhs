# Language-edit and verification change log: Chapter 5 (Results)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/05_results.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `9f646aa02f72e8656469796c4b0d3b8ad865de174cc9536eaa6d497038f7ce34` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/05_results.md` | `d01694474488ef5e0080f811e40f03c7c577707a76e78e50da67fb976e042c4e` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/05_results.tex` | `bdbe2c1f403ace239af307ac910c5a2feaebd2271d79e4605b4f0125eeb9a6c4` |

The full word-level diff is in `05_results.worddiff.txt` (same folder): `[-…-]` marks removed text, `{+…+}` added text. The numerical verification behind every item below is in `builds/previews/REVIEW-COPY_ch05-results_preview_*.verification.md`.

The author's instruction for this session was to render the whole chapter now and to defer every page-budget adjustment to final assembly. Nothing was shortened, removed or reformatted to save pages. The edited copy has 3,621 words against 2,929 in the canonical file (the increase comes from section B and from the long-format tables in section C).

## A. Verified corrections applied to the publishing copy (canonical file unchanged)

Each correction rests on the stored output named. Whether the canonical v12 file is also corrected is the author's decision.

### A1. §5.4: "more than doubles in magnitude" is not supported by the stored values (numerical statement in prose)

- **Canonical passage.** "The Nigeria community sanitation–HAZ coefficient changes sign and more than doubles in magnitude as controls are added sequentially, …"
- **Source.** `outputs/household_community_wash/11_nigeria_sign_reversal.csv`, `section == M1_M4_reproduction`, `term == sanitation_rate_loo_core`: model 1 = 0.27446377545437994, model 2 = 0.2956051…, model 3 = −0.4570578…, model 4 = −0.1838300….
- **Discrepancy.** The largest absolute value (|−0.457|, model 3) is 1.665 times model 1 and 1.546 times model 2. No step in the sequence more than doubles the coefficient's magnitude. The phrase dates from v1 of the manuscript; no provenance record supports it (searched all `docs/` and `outputs/` Markdown).
- **Correction (publishing copy).** "…changes sign and grows in absolute size as controls are added sequentially, from 0.274 with no controls to −0.457 once socioeconomic controls are included." Both numbers are already displayed in Table 5.4. No new number is introduced.

### A2. Introduction: "Coefficients are reported with 95% confidence intervals throughout" does not hold for Table 5.4

- Table 5.4 shows coefficients and p-values only. The publishing copy now says "…except in Table 5.4, which reports coefficients and p-values only." The table itself is unchanged (see E1 for the option of adding its stored CIs).

### A3. Table 5.9 caption did not mention the Ghana-exclusion row

- The canonical caption names wealth, spatial method and completion rule. The table's last row, "Excluding Ghana (DHS/IHME input overlap)", is the overlap-exclusion model `o003` (`family == sens_overlap_excl_GH_water`, `sample_group == POOLED_KE_NG`), which is none of the three.
- **Corrected caption:** "Historical extension: further sensitivity of pooled water–HAZ to wealth adjustment, spatial method, completion rule and the exclusion of Ghana." The section heading (§5.8) is unchanged.

No coefficient, confidence bound, p-value, sample size or cluster count in any table needed correction: 440 keyed comparisons against the stored files all matched at the displayed precision (verification report §3).

## B. Clarifications added to protect existing qualifications (author to confirm)

These sentences add no new estimate. Each restates a definition or qualification that Chapters 3–4 or the stored outputs already establish, or that Chapter 3 says is restated wherever historical coefficients are reported. The author asked for them to be preserved in Chapter 5. Every number in them was checked against the stored outputs.

| # | Where | Added text (abridged) | Source |
|---|---|---|---|
| B1 | §5.1, first sentence | household water and sanitation entered together, each adjusted for the other | Ch. 4 §4.1–4.2; Table 5.1 columns |
| B2 | §5.1 | FULL_DUMMY_DF "reported only as a labelled sensitivity" | Ch. 4 §4.5; Appendix B.1; `model_label == natural_sample_FULL_DUMMY_DF_SENSITIVITY` |
| B3 | §5.2 | community water and sanitation "entered together at every stage (Section 4.3)" | Ch. 4 §4.3 |
| B4 | §5.3 | "conditional on community water and the other two WASH terms"; note: "with 4,426 clusters in each" | Table 5.3 caption; `05_joint_household_community.csv` `psu_count` = 4426 for all three outcomes |
| B5 | §5.5 | the six age bands and the 12 to 23-month reference band; each test a χ² test of five restrictions; combined ten-term tests (10 df) reject in all six combinations, largest *p* = .019; the comparison is cross-sectional and does not trace growth over time | Ch. 4 §4.4; `14_household_community_wash_models.py` `AGE_BANDS`, `AGE_BAND_REF`; `10_age_heterogeneity_joint_tests.csv` (`df`, `p_value`) |
| B6 | §5.6, opening | exposure is an area average within the buffer, not the population-weighted aggregate or household facilities; estimates are weighted conditional associations among eligible measured children, not population-representative; *t*(*G*−1) inference | Ch. 3 §3.5 ("restated wherever a historical coefficient is reported (Section 5.6…)") and §3.8; Ch. 4 §4.5; reporting map v3 ("every reported cell must carry, every time, the same qualifications") |
| B7 | §5.6, verification | all 24 primary cells re-estimated with the second library on a separately rebuilt sample, with coefficients, SEs, CIs and p-values matching; the other 267 of 291 models internally design-checked, and apart from two unweighted counterparts not re-estimated with a second library | Appendix B.2; `final_empirical_package_v3/02_core_reporting_table.md` status correction; `01_final_reporting_map.md` (267 sensitivity models: internal checks only); `21_validate_all_primary_cells.py`, `24_reconcile_inference_corrections.py` |
| B8 | §5.6, weighting | equal country weight totals do not give equal influence on the pooled slope; neither weighted nor unweighted estimate is population-representative | Ch. 4 §4.5; Ch. 3 §3.8; reporting map v3 |
| B9 | §5.7 | the first four rows of Table 5.8 differ in sample as well as window; only the common-sample row holds the sample fixed | Table 5.8 "Sample" column; `window_common_sample_PRELIMINARY_AGGREGATE.csv` `basis` |
| B10 | Table notes 5.8, 5.9 | coefficients per 10 percentage points; the Ghana-exclusion row pools Kenya and Nigeria only | `model_coefficients_PRELIMINARY_AGGREGATE.csv` (`beta_per_10`; `o003` `sample_group == POOLED_KE_NG`) |
| B11 | §5.9 | "all four confidence intervals include zero" (canonical: "both CIs including zero") | `m0045`, `m0046`, `m0186`, `m0187`: every CI spans zero |

## C. Layout restructuring (contents unchanged)

- **Tables 5.3, 5.5 and 5.6** were too wide for intact "β [95% CI], *p*" cells at the mandated 10 pt. Confidence intervals broke across lines inside the brackets (e.g. "−2.48 [−4.91," / "−0.05], .046"). They are now in long format:
  - one outcome group row (HAZ, WAZ, WHZ), then one row per exposure (5.3) or sample (5.5, 5.6);
  - "β [95% CI]" and "*p*" in separate columns.
  
  The cells were generated by script from the canonical cell strings, not retyped. A keyed check (outcome × exposure or sample) confirms that all 36 recombined cells equal the canonical cells, with bold on the same parts (**.043**; **1.03 [0.51, 1.54]**, **<.001**). Row and group order follow the canonical tables. No comparison is added or removed.
- **Tables 5.1, 5.2, 5.4, 5.7, 5.8 and 5.9**: every row and column is byte-identical to the canonical file.
- **Sample notes as table notes (9/13.5 pt).** The canonical parenthetical notes after Tables 5.2 and 5.3 are now `::: {.tablenote}` notes directly below their tables. Their wording was edited lightly, as recorded in the word diff. The long sub-label above Table 5.7 became a note below it, and new short notes were added under Tables 5.8 and 5.9 (B10).
- **Sub-labels of Tables 5.5 and 5.6.** "**Water (W_IMP)** — coefficient [95% CI], *p*" → "**Water (W_IMP):** coefficients per 10 percentage points" (likewise for sanitation). The column headings now carry "β [95% CI]" and "*p*".
- **Age bands in §5.5** are written "0 to 5, 6 to 11, …" instead of "0–5, 6–11, …". With the dash form, the line broke after a range dash ("48–" / "59"), because pandoc writes en dashes as `--`, which permits a break. Times New Roman 2.82 has no word-joiner glyph.

## D. Shared template change (`template/thesis-preamble.tex`)

Old sha256 `47360741fe1b693e00932fa9c4c0af16095586bfba3215a8f3ba7a8c9c1d3e75` → new `7911858b75bc7da6b5b45a0aaf0152058db245225790b7da58f374f8c6106051`. Chapter 5 is the first unit with captioned tables under headings, tables of 10–20 rows and table notes. Its first builds showed three defects of the shared table macros, each confirmed by a before/after build:

1. `\needspace` in `\ThesisTableCaption` misjudged the room directly after a heading. Headings 5.1 and 5.2 were stranded at page bottoms although Table 5.1 fitted on page 1. Fix: `\Needspace`.
2. A table note could be separated from its table (the Table 5.8 note started the next page), because longtable ends with `\penalty0`. Fix: a note records its table in the `.aux` file, and that table then ends with `\penalty10000`. Tables without notes keep `\penalty0`.
3. A table could split across pages (Table 5.6), and a heading could be stranded when its table moved to the next page (§5.4). Fix: each pass records every longtable's height and its note's height in the `.aux` file. On the next pass the caption requests room for caption + table + note (at least 8 lines). A heading directly followed by a caption requests room for heading + caption + table + note (at least 12 lines). Tables taller than 0.8 × text height get no extra keep and break normally, with repeated column heads.

Also: table notes are no longer indented.

**Scope.** Chapters 1–4 contain no tables, captions or notes. For them the only active code is a heading counter that emits nothing, so their layout cannot change. They were **not** rebuilt, and their files are byte-identical to the received package. The appendices' tables are uncaptioned and have no notes, so for them the change only writes heights to the `.aux` file. Re-run `diagnostic` and inspect its tables at final assembly (register FA-10).

## E. Points for author review (nothing below was changed)

- **E1. Table 5.4 has no confidence intervals.** The stored CIs exist (`11_nigeria_sign_reversal.csv` `ci_lower`/`ci_upper`; `15_country_household_cluster_fe.csv`). Adding them would make the chapter's convention uniform; A2 currently records the exception instead.
- **E2. Per-country residual exposure variation.** Chapter 4 §4.5 says "every pooled coefficient in this thesis is reported alongside its country-specific components and each country's residual exposure variation". Chapter 5 shows the country components (Tables 5.5–5.6) but only the pooled residual SD (0.43). Per-country values are stored (`E_residual_sd_after_controls`: water Ghana 0.456, Kenya 0.203, Nigeria 0.652; sanitation 0.258, 0.877, 0.648). Either add a column or row, or soften the Chapter 4 sentence.
- **E3. Model 1 labels.** Table 5.2 calls model 1 "Minimally adjusted" and Table 5.4 calls it "No controls". The code labels model 1 "Exposures only" (`11_main_regressions.py`, `MODEL_SPECS`); both community measures are in the model in each case. Harmonise if desired.
- **E4. §5.7 final sentence.** The canonical wording ("…not reproduced here solely because water–HAZ happened to be significant") is ambiguous. The copy reads it as "left out here to avoid repetition, not because water–HAZ happened to be significant", consistent with the paragraph's earlier "to avoid repeating every cell". Please confirm.
- **E5. "Six significant digits".** The independent pooled β matches the stored value to 6.7 × 10⁻⁸. The SE "as originally run" differed by 3.6 × 10⁻⁵, and after the `group_debias` reconciliation it matches exactly (Appendix B.2). The sentence is accurate for the displayed figures; "to the displayed precision" would be an alternative.
- **E6. Own-eligible sample sizes in Table 5.8.** Only the main and common-sample rows show N. The stored Ns of the other rows are birth-year 29,372, prenatal 29,573 and post-24-month 16,419 (`window_common_sample_PRELIMINARY_AGGREGATE.csv`). They could be added.
- **E7. Bold emphasis** is kept, pending the Chapter 1 bold → italics decision (ch01 open point 3).

## F. How the edit was done

- **Tool.** The `humanizer` skill (v2.9.1) was read in full in this session and applied to the publishing copy only, as in Chapters 1–4.
  - The "personality" section was not applied.
  - No AI-detection outcome was targeted.
  - The edit addresses sentence length, punctuation, repetition and flow.
- **Em dashes.** The canonical file has 36. The 27 used as punctuation (in the prose, the three table sub-labels and inside the Table 5.9 caption) were replaced with commas, colons, semicolons, parentheses or sentence breaks. The 9 that remain are the "Table 5.x —" caption separators the converter requires.
- **En dashes.** Compound en dashes (water–HAZ, sanitation–HAZ …) were kept: 27 in the canonical file, 27 in the copy. The six age-band ranges were rewritten with "to" (section C).
- **Unchanged.**
  - All 10 headings.
  - All 3 code spans (the two aggregate-file paths and the folder path).
  - Every table value (section C).
  - Every number in the canonical prose (identical multiset, plus the numbers added in A1 and B).
  - All bold emphasis (the attenuation sentence now includes its full stop).
  - There are no citations, in the canonical file or in the copy.
- **Hedges, qualifications and evidential strength kept.** Examples:
  - "consistent with confounding … does not, on its own, establish confounding as the sole explanation";
  - "not as proof that no association exists";
  - "not interpreted as evidence that improved household water is harmful";
  - "should not be read as evidence that improved sanitation harms child growth in Nigeria";
  - "not a multiplicity correction" and "does not establish causality";
  - "sample-composition effect … not evidence favouring the validity of one window over another";
  - "this sensitivity adjudicates neither";
  - "never pooled into, or compared with, the established-date headline results".
- **No internal audit commentary was added to the academic prose.** File paths already in the canonical text (§5.7) were kept.
