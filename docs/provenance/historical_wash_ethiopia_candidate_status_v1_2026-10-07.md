# Ethiopia interview-date candidate status, v1 (2026-10-07)

## 1. C1 is invalid and is reclassified as superseded

`06_ethiopia_calendar_audit.py` documents (and `historical_wash_milestone_2026-10-06.md` states explicitly): "The delivered Ethiopian day and month fields are not original 30-day Ethiopian dates: the day value 31 occurs in months with 30 days. Converting them directly would be invalid." Candidate C1 ("ET_C1_triple_provisional") is defined as exactly this: "30-day Ethiopian arithmetic on the delivered day and month" (`historical_wash_exposure_construction_spec_v1_2026-10-06.md`, line 41). **C1 uses the method already identified as invalid for these fields.**

**Correction:** C1 is reclassified from "provisional" to **invalid/superseded**, effective immediately.

- Its files, run outputs, and the 275-row day-validity exclusion remain exactly where they are (`data/processed/ipums_import/v2/ethiopia_calendar_audit_PROVISIONAL_20261006T180523Z/`, and every C1 column/row in the analysis-sample and estimation parquet files). Nothing is deleted or moved.
- C1 is removed from the set of defensible sensitivity analyses in any new reporting table. It must not appear as a candidate alongside C2/C3 in future tables without the word "invalid" attached.
- The prior methods note (`historical_wash_preliminary_estimation_methods_2026-10-06.md` §7) reports C1's coefficient (water HAZ −0.43, sanitation HAZ −0.54) alongside C2 and C3 without flagging it as invalid, and states "the three candidates give the same sign and nearly the same estimate" — this sentence is corrected here: **agreement between C1 and C2/C3 is not evidence of robustness**, because C1's own date values are constructed by a method already known to be invalid for this field; any apparent agreement is not informative about which conversion is correct. That note is not edited in place (preserved for lineage); this document is the authority on C1's status going forward.

## 2. C2 and C3 remain provisional

Neither has been independently validated. The milestone doc states their shared weakness precisely: "The century-day code follows a month-length structure that differs from a 30-day count; its origin and the source of a constant two-day offset are not yet fully established." No new validation was performed in this pass. **C2 and C3 stay provisional**, reported only as separately labelled sensitivity, never pooled into the established-date headline sample, and never promoted on the basis of mutual agreement alone (see §3).

## 3. How much C2 and C3 actually agree, measured directly (new in this pass)

Re-checked directly from `analysis_candidates_RESTRICTED.parquet` (aggregate counts only):

- **Birth year itself does not depend on the interview-date candidate.** `b_year` is identical across C1, C2, and C3 for all 10,641 Ethiopia children (0 differences) — birth year is derived from the birth-date fields, not from the interview date.
- **Birth-year window eligibility is identical between C2 and C3** (9,862 eligible for each), and differs from C1 only by exactly the 275 invalid-day exclusions (plus incidental agreement on the rest). C2 and C3 do not disagree on which children have a complete birth-year window.
- **Post-natal window eligibility (which does depend on the precise interview date) shows small, quantified C2/C3 disagreement**: post_12m, 8 of ~7,930 eligible children disagree between C2 and C3 (0.1%); post_24m, 5 of ~5,970 (0.08%); prenatal_9m, 0 of 9,862 (0%).

This supports a precise, narrow claim: the remaining C2-vs-C3 uncertainty (a few days around the interview date) changes window-completion eligibility for a small number of borderline children, not the bulk of the sample, which is consistent with the near-identical C2/C3 coefficients already reported (water HAZ −0.39 both; sanitation HAZ −0.45 both). It is **not** evidence that either candidate's absolute date is correct — only that whichever candidate is right, the two give very similar postnatal-window classifications.

## 4. Can birth-year exposure be established without the uncertain Gregorian interview conversion?

**No, not entirely**, even though the exposure value and most of the eligibility classification do not depend on which candidate (C2 vs C3) is used (§3). The completeness rule documented in `historical_wash_design_v1.md` requires, for every window including birth_year, that "the window has been completed by the interview date" — so determining whether a child is even eligible still requires *some* valid Gregorian interview date, even if the birth-year window's eligibility is insensitive to the specific remaining C2-vs-C3 disagreement. Concretely:

- Children whose only available interview-date conversion is the invalid C1 method (the 275 excluded rows) cannot be assigned a birth-year exposure at all under the current candidates.
- For the remaining ~10,366 children, the birth-year window's eligibility classification is robust to the C2-vs-C3 choice, but its validity still rests on C2/C3 being approximately correct in absolute terms (both unvalidated).
- Postnatal windows (post_12m, post_24m) depend on interview timing more directly (completion is a month-level test relative to the interview date) and show the C2/C3 disagreement described above, though it is small.

**Consequence:** Ethiopia cannot be promoted to the established-date pooled sample on the strength of C2/C3 agreement alone. It remains a separate, provisional, exploratory analysis, reported only with both remaining candidates shown and C1 excluded.

## 5. Action taken on reporting

- `00_results_index.md` (final empirical package) is updated in this pass to mark C1 invalid and to state that only C2 and C3 may appear in future Ethiopia sensitivity tables.
- No existing output file is altered. This document and the final reporting map (`03_final_reporting_map_2026-10-07.md`) are the authority for how Ethiopia results may be cited going forward.
