# Evidence-based correction, pass 4 (2026-10-09)

Corrects a circular-reasoning error in `evidence_based_correction_v3_2026-10-09.md`'s own diagnostic, identified by direct mathematical critique: residualizing a candidate control block against the exposure variable before testing whether that block affects the exposure variable's own coefficient is circular, because the projection can remove exactly the variation that would reveal a difference. Reviewed starting commit: `5b380a5` (confirmed HEAD == `origin/main`, clean tree except the standing untracked `outputs/supervisor_meeting/`). **No PDF was generated, rebuilt, or rendered in this pass.**

## The problem, stated precisely

`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` (pass 3) built `other_t` as the demeaned block `[E10, age_m, AGE, dummies]` — including E10 — and residualized each birth-year scheme's demeaned block against `other_t`. It then found the two residualized subspaces had equal rank and concluded this **guaranteed** E10's coefficient was invariant between schemes. This is invalid: by construction, residualizing a block against a set that includes E10 removes any part of that block correlated with E10. If the two birth-year schemes actually differed in a way that would move E10's coefficient, that very difference could be exactly what gets removed by this projection — so finding "equal" residualized spaces afterward proves nothing about the question being asked. The procedure could not distinguish "the schemes are genuinely equivalent" from "the schemes differ, but that difference was projected away before it could be detected."

## What was done

Rewrote the diagnostic into five steps, none of which uses E10 to construct a comparison being tested:

1. **Direct comparison.** Demean each scheme's birth-year block (weighted within-cluster demeaning) and compare ranks directly — no residualization against anything, E10 or otherwise.
2. **Nuisance-only residualization.** Residualize each scheme's demeaned block against the shared nuisance controls only (age-in-months, child's current age, demographic dummies), with E10 explicitly excluded from this projection matrix. Performed separately with and without age-in-months.
3. **E10's own residual, compared directly.** For each scheme, build the complete nuisance specification (absorbed cluster FE + shared controls + that scheme's birth-year block) and residualize E10 against it. Compare the two resulting weighted residual vectors elementwise, not by rank inference.
4. **Independent FWL cross-check.** Compute β from the explicit weighted Frisch–Waugh–Lovell formula, β = (e′Wỹ)/(e′We), using the residuals from step 3 and the analogously residualized outcome — entirely independently of `PanelOLS`'s internal computation — and compare to `PanelOLS`'s own fitted coefficient.
5. **Mechanical explanation, E10-independent.** Verify directly that Nigeria's full set of own-year dummy columns (kept in full under the pooled-single-reference scheme) sums exactly to Nigeria's raw country indicator, and that this indicator demeans to exactly zero (since every cluster belongs to one country, so a column constant within every cluster is trivially absorbed).

## Result (run recorded in `data/processed/estimation/birthyear_coding_diagnostic_20261009T081301Z/`, RESTRICTED)

| Step | Result |
|---|---|
| 1. Direct comparison (no residualization) | rank(local)=12, rank(pooled)=12 (of 13 surviving columns), combined=12 — equal span |
| 2. Nuisance-only residualization, with age_m | rank(local\|nuisance)=12, rank(pooled\|nuisance)=12, combined=12 — equal span |
| 2. Nuisance-only residualization, without age_m | rank(local\|nuisance)=12, rank(pooled\|nuisance)=12, combined=12 — equal span |
| 3. E10's own residual vector, with age_m | max abs diff 1.2305244964890163×10⁻¹⁵, relative to ‖e‖ = 1.6777078746018557×10⁻¹⁶ |
| 3. E10's own residual vector, without age_m | max abs diff 1.726321226138064×10⁻¹⁵, relative to ‖e‖ = 2.2347931616249113×10⁻¹⁶ |
| 4. FWL β vs. PanelOLS β, all 4 scheme/age combinations | absolute differences of 0 to 4.440892098500626×10⁻¹⁶ |
| 5. Nigeria redundancy | sum of Nigeria's 5 own-year dummies = Nigeria's country indicator, exact match across all 23,018 rows; demeaned weighted norm of that indicator = 0.0 exactly |

All five steps independently confirm the two birth-year schemes are equivalent nuisance specifications for E10's coefficient — Step 1 establishes this before E10 is even involved, Step 2 confirms it after a valid (E10-free) residualization, Step 3 verifies the actual consequence for E10's own residual directly, Step 4 cross-validates the resulting coefficient via an independent computation, and Step 5 explains the underlying mechanism. No step relies on or is undermined by the circularity in the prior version.

Fitted coefficients (unchanged from pass 3, now supported by valid reasoning): with age_m, 1.0255530672006674 (local) vs. 1.0255530672006667 (pooled-single-reference), absolute difference 6.661338147750939×10⁻¹⁶; without age_m, 1.3852855197991372 vs. 1.3852855197991374, absolute difference 2.220446049250313×10⁻¹⁶.

## Manuscript corrections

- `04_empirical_strategy.md` §4.6: rewritten around the five-step, non-circular evidence chain.
- `appendices/B_model_specifications_and_independent_verification.md` §B.2: rewritten with all five steps' evidence reported explicitly, including the prior circularity disclosed for transparency.
- `03_data_and_variables.md` §3.8: no further change required — v9's wording remains accurate under the corrected evidence.

## Targeted checks executed

- Re-ran the corrected diagnostic to completion; checked internal consistency across all five steps (e.g., Step 4's independent FWL computation matching Step 3's residuals and `PanelOLS`'s own output) before writing any manuscript text from it.
- Re-verified bibliography integrity (26 entries, 20 cited, 0 missing, balanced braces).
- Swept the full v10 manuscript for remaining circular-reasoning language or "if and only if" claims — the only remaining mentions of "residualizing against E10" are the prior-error disclosure (for transparency) and Step 3's valid use (residualizing E10 against a complete nuisance space that is not itself the object of comparison).

## What this pass did not do

Did not rerun any of the 291 historical models in general. Did not generate, rebuild, or render any PDF. Did not reopen any item already closed in the three prior evidence-based-correction passes without new evidence requiring it.

## Canonical path

`manuscript/v10_2026-10-07/` supersedes `v9_2026-10-07/` (pointer added there). See `CORRECTION_LOG.md` in v10 for the itemised before/after text.
