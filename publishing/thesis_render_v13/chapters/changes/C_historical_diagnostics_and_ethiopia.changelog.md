# Verification and language-edit change log: Appendix C

Status: **Awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

Appendix C is the publishing system's `appC` unit. It is numbered **Appendix C** (sections C.1–C.4, Tables C.1–C.3); it is not a chapter and not "Chapter 10".

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/appendices/C_historical_diagnostics_and_ethiopia.md` at academic source commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (last changed in `5563d33`) | `a189ffb59b3156d65f6635a4144f28b7fcc2fb9db62f6bc80a251da84ef79ea3` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/C_historical_diagnostics_and_ethiopia.md` | `208f5020a0cbd59231c9aa63ae06807caa3452e55fda00939f549648916cffac` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/C_historical_diagnostics_and_ethiopia.tex` | `1b1f1e8cc277fc218604f6d848490d45deaf525c54c37781bc8b679324cce5e2` |
| Word diff | `chapters/changes/C_historical_diagnostics_and_ethiopia.worddiff.txt` | `207c5c198746bc173e14299e1b1c0416e429d4d2940787dea4cf2c5ce7c25b0d` |

The word diff marks removed text as `[-…-]` and added text as `{+…+}`; `<nbsp>` marks a no-break space. Raw-LaTeX layout blocks (E) appear in it as added text.

**Sources checked against.** The canonical appendix was read in full against:
- the reviewed publishing copies of Chapter 3 (§3.5–§3.8), Chapter 4 (§4.6), Chapter 5 (§5.6–§5.9), Chapter 6, and Appendices A and B (§A.3; §B.2–§B.4 verification coverage);
- the reporting map and core reporting table (`docs/provenance/final_empirical_package_v3_2026-10-07/`), the issue register (`historical_wash_issue_register_v1_2026-10-07.md`), the Ethiopia candidate-status record (`historical_wash_ethiopia_candidate_status_v1_2026-10-07.md`), the milestone, decisions, specification and methods records of 6 October 2026, and the reproduction-and-lineage record (`final_empirical_package_v1_2026-10-07/01_reproduction_and_lineage.md`);
- the implementing code at `c58fc47`: `scripts/historical_wash/06_ethiopia_calendar_audit.py`, `10_spatial_extraction_v3.py`, `12_construct_exposure_windows.py`, `14_build_analysis_samples.py`, `16_estimate_preliminary.py` (and `16` at `be71d57`, the first estimation commit);
- the stored public outputs: `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` (rows selected by `id` with every identifying field asserted), `docs/provenance/historical_wash_analysis_samples_v1/` (`design_diagnostics_by_sample_window_…`, `ethiopia_birthyear_attribution_…`, `ethiopia_birthyear_candidate_rules_…`, `age_rule_reconciliation_…`) and `historical_wash_exposure_validation/construction_validation_checks_AGGREGATE.json`;
- git metadata for the dated records (`fd93ac9`, `03953cc`, `be71d57`).

No restricted data was read, no exposure was extracted, no model or pipeline was run, no candidate date was changed, no primary specification was selected and no new empirical result was generated. Every check, with its evidence class, is in `verify_appC.tsv` (197/197 OK; see the verification report).

**Length.** No page target was imposed and nothing was removed. The copy has about 2,940 words against 678 in the canonical file; the increase comes from the verified corrections (A) and clarifications (B). Every number token and every code span of the canonical file is retained in the copy (`pdfcheck_appC.tsv`). The rendered body is 8 pages (preview pp. 1–8). Page-budget editing is deferred to final assembly (FA-5, FA-11).

**Citations.** None in the canonical file; none added.

## A. Verified corrections (canonical file unchanged)

Each item corrects a statement that is wrong, imprecise in a way that overstates the evidence, or points to the wrong record. **No stored number was found to be wrong**: every coefficient, count and tolerance in the canonical appendix matches its source at the displayed rounding. Whether the canonical v12 file is also corrected is the author's decision (register FA-23 A).

### A1. C1 versus C2/C3: the 275-child difference is documented for the birth-year window only

- **Canonical (C.2).** "Out of 10,641 Ethiopia children: C1-vs-C2/C3 differ by exactly the 275 invalid-day exclusions …" (no window named).
- **Evidence (stored output).** `ethiopia_birthyear_attribution_AGGREGATE.json`: `records_differing` 275, `dates_missing_C1_only` 275, `birth_after_interview_by_candidate` 0 for all three. `ethiopia_birthyear_candidate_rules_AGGREGATE.csv`: three mutually exclusive rows summing to 275, all with C1 status `dates_missing` and equal C2/C3 status. The candidate-status record (section 3) makes the same statement for birth-year eligibility only. No public output compares C1 with C2/C3 for the other windows.
- **Correction.** "For the birth-year window, the stored aggregate shows that C1 differs from C2 and C3 for exactly 275 children, all of them the children without a C1 date; no candidate places any birth after the interview … This stored comparison covers the birth-year window only."

### A2. "Both confidence intervals include zero" → all four

- **Canonical (C.3).** "Both confidence intervals include zero." The table has four cells (two candidates × two products).
- **Evidence (stored output).** `m0045` [−0.84, 0.06], `m0046` [−0.84, 0.06], `m0186` [−1.32, 0.41], `m0187` [−1.31, 0.42] (per 10 points). Chapter 5 §5.9 says "all four confidence intervals include zero".
- **Correction.** "All four confidence intervals include zero."

### A3. The Ghana-exclusion row is not an overlap exclusion for water

- **Canonical (Table C.3, then unnumbered).** Row "DHS/IHME overlap exclusion (Ghana removed) | Pooled water–HAZ: 0.74, Kenya+Nigeria only".
- **Evidence.** Kenya 2014 is an IHME input for water (specification §6; issue register item 7; `16_estimate_preliminary.py` `overlap_specs()`: "Ghana both products; Kenya water only"). The 0.74 cell is `o003`, family `sens_overlap_excl_GH_water`, samples `KE2014+NG2018`, N 21,078, G 2,761: Kenya's water overlap remains. The family that removes both overlapping surveys for water (`sens_overlap_excl_GH_KE_water`) leaves Nigeria only.
- **Correction.** Row label "Ghana excluded (DHS/IHME overlap; Kenya's water overlap remains)"; result "Kenya and Nigeria pooled water–HAZ: 0.74 vs. three-country main 1.03". The text states that this is a two-country pooled model, not a three-country one, and not an estimate free of DHS/IHME overlap, and that the both-country water exclusion is a Nigeria-only, country-specific model (no number added). *Chapter 5 Table 5.9 uses "Excluding Ghana (DHS/IHME input overlap)" with a note "pools Kenya and Nigeria only"; it was not changed (register FA-23 C).*

### A4. What the interview-date conversion is needed for

- **Canonical (C.1).** "… must be converted to the Gregorian calendar to place a child's postnatal exposure window relative to the (Gregorian-dated) IHME annual rasters."
- **Evidence (code).** `12_construct_exposure_windows.py`: every window is placed from the birth century-month code (`KIDDOBCMC`, Gregorian, IPUMS-converted for Ethiopia; `window_calc()` uses `b` only); the interview CMC `t` enters `eligibility()` (date validity, birth after interview, postnatal completion) and the post-interview-year flag. `14_build_analysis_samples.py`: the under-five rule uses reported age where delivered (all 10,641 Ethiopian children, `age_rule_reconciliation_AGGREGATE.csv`). The milestone record (§4) states that no Gregorian interview CMC is provided for Ethiopia 2016.
- **Correction.** The interview date is described as deciding date validity, birth-before-interview (all windows), postnatal completion (two windows) and the post-interview flag; window placement, exposure values, birth year and the age control do not depend on the candidate. A three-item list separates birth date, interview date and age (B2).

### A5. Birth-year window: no completion check, but eligibility is not "satisfied by construction"

- **Canonical (C.2).** "… the birth-year window, which has no completion check at all and is satisfied by construction once a child's birth date is validly placed in a calendar year."
- **Evidence (code).** `eligibility()` in script 12 applies to the birth-year window the conditions unmatched cluster, valid dates, birth not after interview, years inside 2000–2017, no missing year and complete coverage; only the completion test is restricted to `kind == "post"`.
- **Correction.** "The birth-year window has no completion check at all … Eligibility in the birth-year window still requires valid dates, a birth year inside the 2000–2017 raster span and complete spatial coverage." The prenatal window is named as also having no completion check (it ends before birth).

### A6. Timing of the C1 finding and of C1's reclassification

- **Canonical (C.1).** "… a conclusion reached independently of, and prior to, any WASH-outcome analysis."
- **Evidence (dated records).** The day-31 finding is in the milestone record, commit `fd93ac9` (2026-10-06 20:07:53 +02:00), before the recorded estimation run `run_20261006T185646Z` (18:56:46 UTC = 20:56:46 +02:00; lineage record). C1 was nevertheless estimated in that run as `ET_C1_triple_provisional` (six models) and reclassified as invalid/superseded on 7 October 2026 (candidate-status record §1).
- **Correction.** The finding is dated and its independence from outcome results stated; the copy adds that C1 was estimated as a provisional candidate in that run and reclassified on 7 October 2026. This prevents the reading that C1's invalid *status* predated estimation.

### A7. Pre-specification pointer and the scope of "reported together"

- **Canonical (C.4, last paragraph).** "No sensitivity cell was selected or suppressed based on its significance; all are reported together as a pre-specified sensitivity family (`…preliminary_estimation_methods_2026-10-06.md` §7)."
- **Evidence (dated records).** The methods note §7 ("planned; no specification search") reports results after estimation. The list of sensitivity analyses marked "pre-specified; reported together; none selected by results" is in the estimation specification §8, whose header states "No coefficient has been estimated or inspected"; it was committed in `03953cc` (2026-10-06 20:51:28 +02:00), before the recorded estimation run. All three overlap families were already in script 16 at `be71d57`. The appendix shows only pooled water–HAZ cells, not the whole family.
- **Correction.** The pre-specification is attributed to the specification §8 with its dating, the methods note §7 is cited for reporting, and "all are reported together" becomes "every one of the 291 models … is in the stored coefficient file. Table C.3 shows the pooled water–HAZ cells only." Dated records establish order of recording, not the absence of unrecorded earlier runs (recorded OPEN in the verification).

### A8. "exact buffer average"

- **Canonical (Table C.3 row 2).** "containing-pixel vs. exact buffer average".
- **Evidence.** Chapter 3 §3.6 explains that "exact" refers to exact arithmetic on a corner-projected approximation of each pixel, not to the true pixel boundary.
- **Correction.** "containing-pixel vs. buffer average"; the coverage paragraph describes the overlap computation with the corner projection and points to Section 3.6.

## B. Clarifications (verified restatements; no new result)

- **B1.** Opening: two parts and their reporting status from the reporting map (C1 invalid/superseded; C2/C3 provisional, exploratory; Table C.3 rows sensitivity family; all conditional associations among eligible measured children).
- **B2.** C.1 list separating birth date (window placement, exposure value, birth year), interview date (date validity, birth-before-interview, postnatal completion, post-interview flag) and age (reported age for all Ethiopian children; calendar age only in the established-date calendar-age sensitivity; `sens_calendar_age` has no Ethiopia model).
- **B3.** C1 detail: 30-day arithmetic on year, month and day; day 31 rows get no date (`tripleok = ed <= 30`); the other conversions share the invalid logic (status record §1); why agreement with C1 corroborates nothing.
- **B4.** C2 and C3 described by the delivered fields they use (C2: century-day code with origin 1 Meskerem 1900; C3: month and day fields with Gregorian cumulative lengths anchored at 1 Meskerem 2008) and their shared weakness quoted from the status record §2; neither validated; the support inquiry was drafted and, per the dated records, not sent; no record of sending or answer.
- **B5.** Table C.1 note: what "eligible" and "Disagree" count; rows overlap and must not be added; evidence status (status record §3 gives 9,862 and the disagreements exactly but the postnatal counts only approximately; the exact postnatal counts are carried from the canonical appendix); the difference of counts equals the disagreements (arithmetic consistency only).
- **B6.** Stored model-sample pattern: water–HAZ birth-year and prenatal samples 8,250 under both candidates; post-12-month 6,580 (C2) and 6,573 (C3) before singleton removal, 6,568 and 6,561 in `m0045`/`m0046` (6,580 − 12 = 6,568; 6,573 − 12 = 6,561).
- **B7.** C2/C3 agreement is not independent validation; their difference is not a confidence interval, uncertainty bound or guaranteed range (both could be wrong in the same direction). Canonical "the remaining uncertainty between them changes very few children's classification" → "the choice between C2 and C3 changes the window classification of very few children" (the canonical phrase could be read as describing uncertainty about the true date).
- **B8.** Prenatal window needs no completion check; annual values may cover post-interview months (flagged, not excluded; Section 3.7). The candidate-status record §4 describes the completion rule as applying to every window including the birth year (citing the design draft); the implementation, Chapter 3 §3.7 and this appendix do not (register FA-23 D).
- **B9.** Table C.2 note: model IDs, 95% CIs, *p*-values, N, G, specification and inference convention (CRV1; Student *t* with G − 1 degrees of freedom); C1 estimates exist but are not shown.
- **B10.** C.3: Ethiopia not pooled under any established-date label; similar C2/C3 coefficients follow from similar samples and validate neither; the gap between them is not a distance to a true-date estimate.
- **B11.** C.4 opening: definition of the main model `m0004` and of what each row changes; each sensitivity uses its own eligible sample.
- **B12.** Table C.3 note: model ID, CI, *p*, N and G for each row; units per 10 percentage points.
- **B13.** Coverage rule: exact disk–pixel overlap on corner-projected pixels; outside-raster, NoData and out-of-range values excluded from the valid area and never set to zero; mean over the valid area; `FULL_TOL` = 10⁻³; complete coverage for every year within 2000–2017, no extrapolation; partial-coverage values enter none of the 291 models; buffers do not recover true locations and are area, not population-weighted, averages.
- **B14–B17.** Containing pixel (single pixel, NoData → missing, no nearest-cell substitution, different sample N 23,642); rural 10 km (urban 2 km unchanged; not a validation of displacement probabilities); stricter completion (L + 1; postnatal windows only; sample 23,018 → 22,639); calendar age (affects only Nigeria within the established family; same N; 1.027 vs 1.026).
- **B18.** Weighting: equal country totals within each model's sample; equal totals ≠ equal influence; unweighted counterpart 0.41 (Section 5.6, Appendix B); neither corrects for selection into measurement; window and wealth sensitivities are in Sections 5.7–5.8 (not added here).
- **B19.** Verification coverage (291 estimated; 24 primary reproduced, including `m0004`; `m0005` and `m0008` checked individually; the other 265, including every other row of Table C.3 and all 18 Ethiopia models, internal checks only) and the research qualifications these checks do not resolve.

## C. Tables and captions

- Captions added to the three existing tables, in order of appearance: **Table C.1** (C2/C3 window eligibility), **Table C.2** (Ethiopia provisional HAZ coefficients), **Table C.3** (spatial-extraction rule and pooled water–HAZ sensitivity). No table added or removed; all 4 + 2 + 6 rows and all columns kept; numbers unchanged.
- Cell wording changed in Table C.3 only: row 1 result adds "(valid-area fraction ≥ 1 − 10⁻³)"; row 2 "exact buffer average" → "buffer average" (A8); row 3 "Rural-10km buffer sensitivity" → "Rural 10 km buffer sensitivity"; row 6 label and result (A3).
- Three 9 pt table notes (B5, B9, B12). Each table carries the FA-20 continuation head; no table breaks in this PDF (stress test in the verification report).

## D. Language (humanizer v2.9.1, read in full; applied conservatively)

- Prose em dashes removed (the canonical had three in prose; the heading and caption separators the converter requires remain). En dashes kept only in ranges and compound labels (2000–2017, C.1–C.3, water–HAZ), as in the earlier units.
- Long sentences split; "genuinely", "precisely" and similar intensifiers removed; the C.2 heading "How much C2 and C3 actually agree (measured directly, not assumed)" → "How closely C2 and C3 agree on window eligibility" (the direct measurement was made on restricted data in an earlier session and is carried, B5).
- Record-internal section numbers written as "section N" of the named record, so that they are not read (or linted) as thesis sections.
- Identifiers, candidate labels, units, tolerances, numbers and qualifications unchanged.

## E. Layout (copy only; no shared file changed)

- Thirteen ragged-right groups (`\begingroup … \raggedright … \endgroup`, indent kept, widow/club penalties) around paragraphs and lists with long paths: 8 lines into the right margin → 0.
- 101 no-break spaces (Section/Table/Appendix numbers, "*p* =", "N =", "G =", "km").
- Page 4 ends after the C.2 text with the lower part of the page empty, because the shared keep logic holds the C.3 heading with Table C.2. Not changed (FA-10, FA-11).

## F. Points for the author (not applied)

- **F1.** Confirm A1–A8 and decide on canonical synchronisation (FA-23 A).
- **F2.** Chapter 3 §3.5 says the conversion is "required to place Ethiopian children's exposure windows"; A4 shows that windows are placed from the birth date and the interview date governs eligibility. Consider aligning Chapter 3 at final assembly (FA-23 B).
- **F3.** Chapter 5 Table 5.9 "Excluding Ghana (DHS/IHME input overlap)": consider adding that Kenya's water overlap remains (FA-23 C).
- **F4.** Candidate-status record §4 versus the implemented completion rule: annotate the record or leave it (FA-23 D).
- **F5.** Exact postnatal eligibility counts (7,930 / 7,922 / 5,974 / 5,969) are carried; a local aggregate check of the restricted analysis file would confirm them (FA-23 E).
- **F6.** The dated records cited in A7 (specification `03953cc` before run `20261006T185646Z`) bear on FA-15 B, but FA-15 B concerns the window choice in Chapter 6 §6.4 and remains the author's check (FA-23 F).
- **F7.** Whether the CI, *p*, N and G detail in the three table notes should stay in the appendix (it repeats stored values; no number is new).
