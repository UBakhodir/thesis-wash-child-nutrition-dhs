# Evidence-based correction, pass 3 (2026-10-09)

Corrects a methodological error in `evidence_based_correction_v2_2026-10-09.md`'s own new diagnostic and the manuscript text it supported, identified by direct mathematical critique: nesting of raw column spaces does not establish coefficient invariance under a within-cluster fixed-effects transformation. Reviewed starting commit: `5fd00b9` (confirmed HEAD == `origin/main`, clean tree except the standing untracked `outputs/supervisor_meeting/`). **No PDF was generated, rebuilt, or rendered in this pass.**

## The problem, stated precisely

`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` (first version, committed in v8) computed `np.linalg.matrix_rank` on the two birth-year schemes' **raw** dummy blocks, found `rank([pooled | local]) == rank(pooled)` (i.e. local's raw span nests inside pooled's raw span), and concluded this nesting explained why the two schemes gave the same fitted E10 coefficient. This is invalid reasoning for two independent reasons:

1. `linearmodels.PanelOLS` with `entity_effects=True` does not fit on the raw design matrix — it fits on the matrix after weighted within-entity (here, within-cluster) demeaning. Raw-space properties do not transfer to the demeaned space in general; a column that is "redundant" in raw space can become informative after demeaning, and vice versa.
2. Even granting nesting in the *correct* (transformed) space, nesting in only one direction (`local ⊆ pooled`) does not establish that the extra column pooled has is *uncorrelated*, after demeaning and after accounting for the other covariates, with E10's own residual variation — and it is exactly that correlation structure, not nesting per se, that the Frisch–Waugh–Lovell theorem conditions on for a coefficient to be provably invariant.

The script's own numerical reporting compounded this: coefficients were rounded to 7 decimals before comparison and an agreement at that precision was described as "bit-for-bit identical" — a phrase implying exact floating-point equality that was never actually checked.

## What was done

Rewrote the diagnostic (not a new script — the same file, extended) to perform the comparison that actually bears on coefficient invariance:

1. **Weighted within-cluster demeaning**, implemented independently in this script (not imported from `16_estimate_preliminary.py`, though following the identical standard definition: `bincount`-weighted group demeaning), applied to (a) the shared non-birth-year columns (E10, age-in-months, AGE, demographic dummies) once, and (b) each birth-year scheme's raw block separately.
2. **Absorption check**: post-demeaning column norm against a stated tolerance (1×10⁻¹⁰), identifying and naming any column collinear with the absorbed cluster fixed effect — matching the exact criterion `16_estimate_preliminary.py` itself uses, and cross-checked against `linearmodels`' own `AbsorbingEffectWarning` (both flag `by_NG2018_2017` in both schemes, confirming consistency).
3. **Residualization**: each scheme's surviving, demeaned birth-year columns are weighted-OLS-residualized against the demeaned, shared non-birth-year columns — isolating each scheme's "net new information" after the fixed effect and other covariates are accounted for, which is the quantity FWL invariance actually depends on.
4. **Rank comparison on the residualized matrices**: own rank for each scheme, and combined rank (both directions at once, via `rank([A|B])`), with the tolerance stated explicitly (1×10⁻⁸ relative to the largest singular value).
5. **Full float64-precision coefficient reporting** for all four fits (2 birth-year schemes × with/without age-in-months), with explicit absolute differences computed before any rounding, using `repr()` to avoid silent display truncation.

## Result

| Quantity | Local scheme | Pooled-single-reference scheme |
|---|---|---|
| Raw birth-year dummy columns | 12 | 13 |
| Surviving columns after demeaning (none absorbed) | 12 | 13 |
| Rank after residualizing against E10/age_m/AGE/dummies | 12 | 12 |
| Combined residualized rank (`[pooled | local]`) | 12 | |

The two residualized subspaces are **equal** (all three ranks — local, pooled, combined — equal 12), not merely one nested in the other. By Frisch–Waugh–Lovell, equal residualized subspaces are a *sufficient condition* for every non-birth-year coefficient, including E10, to be mathematically identical between the two schemes — not an empirical coincidence requiring further explanation, and not something nesting alone could have established.

Fitted coefficients, full precision (`data/processed/estimation/birthyear_coding_diagnostic_20261009T080355Z/`, RESTRICTED):

| Config | β (E10, per 10 points) |
|---|---|
| local, with age_m | 1.0255530672006674 |
| pooled_single_ref, with age_m | 1.0255530672006667 |
| **Absolute difference** | **6.661338147750939×10⁻¹⁶** |
| local, without age_m | 1.3852855197991372 |
| pooled_single_ref, without age_m | 1.3852855197991374 |
| **Absolute difference** | **2.220446049250313×10⁻¹⁶** |

Both differences are at the level of IEEE 754 double-precision machine epsilon (≈2.22×10⁻¹⁶), i.e. genuinely floating-point noise, not an approximation that happens to round to zero at 7 decimals.

**Age-in-months effect** (holding the birth-year scheme fixed at `local`): 1.0255530672006674 (with) vs. 1.3852855197991372 (without), a difference of −0.35973245259846975. This continues to approximately reproduce the documented early-attempt value (≈1.385) on this reconstruction — stated as approximate reproduction, not exact recovery of the original, unpreserved script's output, which cannot be independently verified.

## Manuscript corrections

- `04_empirical_strategy.md` §4.6: rewritten around the FWL-based residualized-rank result and the exact floating-point coefficient differences; "fully nested... no effect" replaced with the correct mechanism.
- `appendices/B_model_specifications_and_independent_verification.md` §B.2: rewritten with the full rank-comparison evidence (raw counts, transformed ranks, combined rank, explicit tolerances) and exact floating-point coefficient differences; "bit-for-bit identical" removed.
- `03_data_and_variables.md` §3.8: removed the claim that the birth-year reference-coding distinction "matters for the pooled estimate" (now disproven — the choice does not affect the fitted coefficient, though it does change the raw design matrix); corrected to state both facts precisely.

## Targeted checks executed

- Re-ran the corrected diagnostic to completion; checked its first output against the known stored value (1.025553) before writing any manuscript text from it.
- Swept the full v9 manuscript for "bit-for-bit identical," "fully nested," and "it nests, so it does not move beta" — none remain.
- Re-verified bibliography integrity (26 entries, 20 cited, 0 missing, balanced braces) as a matter of course.

## What this pass did not do

Did not rerun any of the 291 historical models in general — only the one, already-authorized, targeted diagnostic, now corrected. Did not generate, rebuild, or render any PDF. Did not reopen any item already closed in the two prior evidence-based-correction passes without new evidence requiring it.

## Canonical path

`manuscript/v9_2026-10-07/` supersedes `v8_2026-10-07/` (pointer added there). See `CORRECTION_LOG.md` in v9 for the itemised before/after text.
