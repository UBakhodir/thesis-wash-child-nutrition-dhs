# Correction log: v9 → v10 (2026-10-09)

Corrects a circular-reasoning error in v9's own diagnostic (itself a correction of v8's invalid raw-nesting argument) and the manuscript text drawn from it. v9 is preserved unchanged; see `../v9_2026-10-07/` (a `POINTER_TO_V10.md` is added there). **No empirical estimate, sample, weight, control set, or reported coefficient changed.** Full investigation detail: `docs/provenance/evidence_based_correction_v4_2026-10-09.md`.

## What changed

**The problem.** v9's `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` residualized each birth-year scheme's demeaned block against a nuisance set that **included the exposure variable (E10) itself**, then treated equal post-residualization ranks as proof that E10's own coefficient was invariant to the choice of scheme. This is circular: residualizing a candidate control block against E10 removes exactly the part of that block that could be correlated with E10, so finding the residualized spaces "equal" afterward does not establish what it claimed to — it can hide the very difference in question, rather than ruling it out.

**The fix.** The diagnostic was rewritten into a five-step chain that never uses E10 to construct any comparison being tested:

1. Compare the two schemes' demeaned birth-year blocks **directly** (no residualization against anything).
2. Residualize each scheme's block against the shared nuisance controls **only** (age-in-months, child's age, demographic dummies — E10 excluded from this projection), checked separately with and without age-in-months.
3. Build each scheme's **complete** nuisance specification (cluster FE + shared controls + that scheme's birth-year block) and compare E10's own weighted residual exposure vector **directly, elementwise** under each specification — a genuine empirical check, not a rank inference.
4. Independently compute the fitted coefficient via the **explicit weighted Frisch–Waugh–Lovell formula**, from scratch, and cross-check it against `PanelOLS`'s own reported coefficient.
5. Explain the mechanical source of the raw column-count difference **without reference to E10 at all**: verify directly that Nigeria's full set of own-year dummy columns sums exactly to Nigeria's country indicator, and that this indicator is absorbed by the cluster fixed effect (demeans to exactly 0.0) because clusters never span countries.

**The result.** All five steps agree: Step 1 (direct, no residualization) already shows equal rank (12/12/12); Step 2 (nuisance-only, E10 excluded) confirms it in both age-control modes; Step 3 shows E10's own residual vector differs by at most 1.73×10⁻¹⁵ in absolute terms (relative difference 2.23×10⁻¹⁶) between schemes — the same vector; Step 4's from-scratch FWL computation matches `PanelOLS`'s own fitted coefficient to within 4.4×10⁻¹⁶; Step 5 confirms the mechanical redundancy exactly (elementwise match across all 23,018 observations; the resulting country indicator demeans to exactly 0.0). The substantive conclusion — that the two birth-year schemes are equivalent nuisance specifications for the exposure coefficient, and that the age-in-months omission alone explains the documented 1.385-vs-1.026 discrepancy — is **unchanged from v9**, but it is now established by a valid, non-circular argument with five independent, mutually-reinforcing lines of evidence rather than one potentially-invalid rank comparison.

| # | File | Change |
|---|---|---|
| 1 | `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` | Rewritten into the five-step chain above; docstring RESULT and Method sections rewritten to match |
| 2 | `04_empirical_strategy.md` §4.6 | Rewritten around the non-circular, five-step evidence chain |
| 3 | `appendices/B_model_specifications_and_independent_verification.md` §B.2 | Rewritten with all five steps' evidence reported explicitly (direct comparison, nuisance-only residualization, E10's own residual vector, independent FWL cross-check, mechanical redundancy explanation) |

`03_data_and_variables.md` §3.8 required no further change — its v9 wording ("this specific choice does not itself change the fitted exposure coefficient, though it does change the raw design matrix") remains accurate under the corrected evidence.

## Targeted checks executed

- Re-ran the corrected diagnostic to completion; reviewed its own first output for internal consistency across all five steps before writing manuscript text from it.
- Re-verified bibliography integrity (26 entries, 20 cited, 0 missing, balanced braces).
- Swept the full v10 manuscript for remaining circular-reasoning or "if and only if" language — the only remaining mentions of "residualizing against E10" are the two legitimate, correct cases (describing the prior error for transparency, and Step 3's valid residualization of E10 against the *complete* nuisance space, which is not part of the comparison being tested).

## What remains open (unaffected by this pass)

Unchanged from `v9_2026-10-07/CORRECTION_LOG.md`. No PDF was generated, rebuilt, or rendered in this pass.
