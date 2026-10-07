# Final empirical package v2 — results index (2026-10-07, closure milestone)

Supersedes `final_empirical_package_v1_2026-10-07/00_results_index.md` (same day, earlier). v1 is preserved unchanged with a pointer banner added at its top; this file is the current authority. Changes from v1: the pooled headline historical estimate is now independently verified (new); Ethiopia candidate C1 is reclassified invalid; the IHME water/sanitation product definitions are resolved; a reporting error about wealth and cluster FE is corrected; the unresolved-issues list is reconciled into one register.

## A. Baseline (current four-round, cross-sectional WASH) — unchanged from v1

No baseline numbers changed in this pass. See `baseline_evidence_reconciliation_v1_2026-10-07.md` and v1's index §A; both remain current.

## B. Historical WASH extension — status changes this session

| Status | Result | File | Notes |
|---|---|---|---|
| **Validated for main reporting (within the established-date, provisional-extension scope — see §C)** | Pooled established water–HAZ, post_12m, weighted (the headline estimate) | `data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv` (RESTRICTED; row id m0004) | β per 10 points = 1.0256 [0.514, 1.537], p<.001, N=23,018, G=3,114. **Independently re-verified this session** with a separately rebuilt sample and a different estimation library (linearmodels.PanelOLS): β matches to 6.7×10⁻⁸, SE to 3.6×10⁻⁵ (`20_validate_pooled_estimate.py`, output in `data/processed/estimation/pooled_independent_validation_20261007T090003Z/`, RESTRICTED). Still labelled PRELIMINARY overall because issues #1, #3, #4(partly), #9, #10 in the issue register remain open — "validated" here means the number is confirmed correctly computed, not that every design question is closed. |
| **Validated sensitivity** | Pooled unweighted counterpart, same observations | Same source as above | β per 10 = 0.4147 [0.029, 0.800], p=.035. Independently confirmed (matches the documented 0.41 [0.03, 0.80]). Shows the result is sensitive to the equal-country weighting choice (register item #8), as already disclosed — not newly concerning. |
| **Validated sensitivity (new this session)** | Pooled headline estimate under the FULL_DUMMY_DF convention | `data/processed/estimation/pooled_independent_validation_20261007T090003Z/independent_estimates_AGGREGATE.csv` | SE = 0.280 (vs. PRIMARY 0.261); CI [0.476, 1.575], still p<.001. A new, previously unreported sensitivity check on the DF convention for the pooled model specifically (the stored coefficients CSV only carries the PRIMARY convention for historical models). |
| **Exploratory with specified limitations** | All other 288 historical models (window sensitivities, wealth, containing-pixel, rural-10km, stricter completion, calendar age, overlap exclusions) | `historical_wash_preliminary_estimates_v1/`, methods note §6–7 | Unchanged from v1; not independently re-verified beyond the implementation-level checks already done (design checks, 4-model independent validation). |
| **Invalid/superseded** | Ethiopia candidate C1 (all 6 C1 models: water/sanitation × HAZ/WAZ/WHZ) | `historical_wash_ethiopia_candidate_status_v1_2026-10-07.md` | Uses a date-conversion method already shown invalid for the delivered fields. Do not cite C1 coefficients, including as corroborating evidence for C2/C3. |
| **Exploratory, provisional (unchanged status, now better characterised)** | Ethiopia candidates C2, C3 (12 models) | Same note, §3 | Still provisional; C2/C3 shown to agree closely on eligibility (0–8 disagreements per window out of ~9,800–10,600 children) but neither is independently validated. |
| **Not estimable** | None | — | All 291 planned models estimated; this is unchanged. |

## C. What "validated for main reporting" means here — read before citing

The pooled headline water–HAZ estimate can be reported in the thesis as a **correctly computed, independently confirmed number**, with these qualifications stated alongside it every time, per the issue register:
1. It is an association within the measured anthropometry subsample, not a population-representative estimate (register #1).
2. It targets "each established-date country weighted equally," not a population-size-weighted pooled sample — the unweighted counterpart is less than half the size and barely significant (register #8).
3. It reflects JMP-defined improved-water coverage, as an area average over a displaced buffer, not a population-weighted estimate at the true cluster location (register #4, #9, #10).
4. It does not include Ethiopia (register #5) or correct for DHS/IHME input overlap in Ghana/Kenya (register #7) in its primary form — both are reported as separate, disclosed sensitivities.
5. It is an association, not a causal effect, under a cross-sectional-with-one-time-dimension design (country×birth-year + cluster FE) — see the baseline reconciliation's §5 discussion of why this differs from the current-round community model's purely mechanical cluster-level variation.

This is a materially stronger evidentiary basis than "preliminary and unverified," but it is not a basis for dropping the PRELIMINARY label from the extension as a whole — that label stays until the remaining open register items (overwhelmingly items #1–#3, #9–#10, which are about measurement documentation and inherent geocoding limitations, not computational correctness) are closed or the thesis text explicitly carries these five caveats.

## D. Full issue accounting

See `historical_wash_issue_register_v1_2026-10-07.md` for all 12 items (10 reconciled from the prior two partial lists, plus 2 new from this session), each typed as a correctable error, missing documentation, an authorized design choice, or an inherent limitation, with required action stated or explicitly "none available."

## E. Authority chain

- Supersedes: `final_empirical_package_v1_2026-10-07/00_results_index.md` (baseline §A content still current there and not repeated here).
- Superseded supervisor-advice-matrix row: see `historical_wash_supervisor_advice_matrix_ADDENDUM_2026-10-07.md`.
- Superseded Ethiopia candidate treatment: see `historical_wash_ethiopia_candidate_status_v1_2026-10-07.md`.
- Resolved issue: see `historical_wash_ihme_product_definitions_v1_2026-10-07.md`.
