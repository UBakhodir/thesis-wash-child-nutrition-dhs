# Manuscript source package v9 (2026-10-09) — corrected column-space diagnostic

Supersedes `manuscript/v8_2026-10-07/` as the canonical manuscript source. v1 through v8 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate, sample, weight, control set, or reported coefficient changed.**

This pass corrects a methodological error in v8's own newly-written diagnostic (`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`) and the manuscript text it supported — full detail in `CORRECTION_LOG.md` and `docs/provenance/evidence_based_correction_v3_2026-10-09.md`. v8 claimed that because the country-local birth-year dummy scheme's *raw* column space nested inside the single-pooled-reference scheme's raw column space, the exposure coefficient was necessarily unaffected by the choice between them ("it nests, so it does not move beta"). This is not a valid inference: the estimator fits on the weighted within-cluster-demeaned design, not the raw one, and raw-space nesting does not establish anything about the demeaned, residualized spaces the fitted coefficients actually depend on.

## What this pass did

1. Rewrote the diagnostic to compare the two birth-year schemes on the actual transformed design: both blocks demeaned using the identical weighted within-cluster transformation the estimator itself uses, then residualized against the other covariates (E10, age-in-months, AGE, demographic dummies) to isolate each scheme's "net new information." Reported: raw column counts, transformed ranks, combined transformed rank, whether the transformed spaces are equal, which columns are absorbed, and the explicit numerical tolerances used.
2. Found the two residualized subspaces are genuinely **equal** (rank 12 in both directions, not merely nested) — which, by the Frisch–Waugh–Lovell theorem, is what actually guarantees the exposure coefficient's invariance between schemes.
3. Reported full float64-precision coefficients and explicit absolute differences (6.661338147750939×10⁻¹⁶ — floating-point machine epsilon) rather than values rounded to 7 decimals mislabelled "bit-for-bit identical."
4. Softened the age-control conclusion to "approximately reproduces" the documented early-attempt discrepancy, not exact recovery of unpreserved original code.
5. Corrected `03_data_and_variables.md` §3.8, which had claimed the birth-year reference-coding choice "matters for the pooled estimate" — the corrected diagnostic shows it does not affect the fitted coefficient, though it does change the raw design matrix; both facts are now stated precisely.

## Canonical files and reading order

Unchanged from v8 except `03_data_and_variables.md` §3.8 and `04_empirical_strategy.md` §4.6 (corrected) and Appendix B §B.2 (corrected).

## Build

**No PDF was generated, rebuilt, or rendered in this pass.** The existing `../v6_2026-10-07/build/main.pdf` reflects none of v7's, v8's, or v9's prose corrections.

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this investigation could establish.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; a full prose quality-review pass should be run once more before a submission build.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v8 remain superseded, plus `manuscript/v8_2026-10-07/` itself for the items in `CORRECTION_LOG.md`.
