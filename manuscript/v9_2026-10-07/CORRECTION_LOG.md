# Correction log: v8 → v9 (2026-10-09)

Corrects a methodological error in v8's own new diagnostic script and the manuscript text drawn from it. v8 is preserved unchanged; see `../v8_2026-10-07/` (a `POINTER_TO_V9.md` is added there). **No empirical estimate, sample, weight, control set, or reported coefficient changed.** Full investigation detail: `docs/provenance/evidence_based_correction_v3_2026-10-09.md`.

## What changed

**The problem.** v8's `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` compared the two birth-year dummy schemes' *raw* column spaces, found the country-local scheme nested inside the single-pooled-reference scheme, and concluded this nesting alone explained why the fitted exposure coefficient was unaffected ("it nests, so it does not move beta"). This reasoning is invalid: `PanelOLS` does not fit on the raw design matrix — it fits on the weighted within-cluster-demeaned matrix — and raw-space nesting does not imply the demeaned, residualized spaces are equal; an extra column that survives demeaning and correlates with the exposure variable's own within-cluster residual can change the fitted coefficient regardless of raw nesting. v8 also reported coefficients rounded to 7 decimals and called agreement at that precision "bit-for-bit identical," overstating what had actually been shown.

**The fix.** The diagnostic now compares the two schemes on the actual transformed design: both birth-year blocks are demeaned using the identical weighted within-cluster transformation `PanelOLS`'s entity effects use, columns absorbed by that transformation are identified and reported by name, and the surviving columns are then residualized against the demeaned E10/age-in-months/AGE/demographic-dummy columns — isolating the "net new information" each scheme's birth-year block contributes once the fixed effect and other covariates are accounted for. The two residualized subspaces are compared by rank (own rank, and combined rank in both directions), with the explicit numerical tolerance stated (1×10⁻⁸ relative to the largest singular value for rank; 1×10⁻¹⁰ for absorption).

**The result.** Local scheme: 12 raw columns survive demeaning, residualized rank 12. Pooled-single-reference scheme: 13 raw columns survive demeaning, residualized rank also 12 (one column is redundant once residualized against the other covariates) — combined rank 12. The two residualized subspaces are **equal**, not merely nested, which by the Frisch–Waugh–Lovell theorem is a sufficient condition for the exposure coefficient to be mathematically identical between schemes, not an empirical coincidence. Full-precision fitted coefficients confirm this: 1.0255530672006674 (local) vs. 1.0255530672006667 (pooled-single-reference), absolute difference 6.661338147750939×10⁻¹⁶ — machine-precision floating-point noise, correctly reported as such rather than as rounded "0.0000000." The age-in-months control's standalone effect (1.0255530672006674 with it vs. 1.3852855197991372 without it) is unchanged in substance from v8, but is now explicitly described as "approximately reproduces" the documented early-attempt value, not exact recovery of unpreserved code.

| # | File | Change |
|---|---|---|
| 1 | `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py` | Rewritten: demeaned-and-residualized rank comparison replaces raw-block nesting; full float64 coefficient precision and explicit absolute differences replace 7-decimal rounding; docstring RESULT section rewritten |
| 2 | `04_empirical_strategy.md` §4.6 | Rewritten around the FWL-based residualized-rank result, with the exact floating-point differences |
| 3 | `appendices/B_model_specifications_and_independent_verification.md` §B.2 | Rewritten with the full rank-comparison evidence (own rank, combined rank, numerical tolerances) and exact floating-point coefficient differences |
| 4 | `03_data_and_variables.md` §3.8 | Removed the claim that the birth-year reference-coding distinction "matters for the pooled estimate" — the diagnostic proves it does not affect the fitted coefficient, though it does change the raw design matrix; wording corrected to state both facts precisely |

## Targeted checks executed

- Re-ran the corrected diagnostic script to completion; its own first run (of this corrected version) was reviewed for the same class of scaling or precision error already caught twice this session and found clean.
- Re-verified bibliography integrity (26 entries, 20 cited, 0 missing, balanced braces) — unaffected by this pass, re-checked as a matter of course.
- Swept the full v9 manuscript for any remaining "bit-for-bit identical," "fully nested," or "it nests, so it does not move beta" language — none found.

## What remains open (unaffected by this pass)

Unchanged from `v8_2026-10-07/CORRECTION_LOG.md`. No PDF was generated, rebuilt, or rendered in this pass.
