# Manuscript source package v10 (2026-10-09) — non-circular column-space diagnostic

Supersedes `manuscript/v9_2026-10-07/` as the canonical manuscript source. v1 through v9 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate, sample, weight, control set, or reported coefficient changed.**

This pass corrects a circular-reasoning error in v9's own diagnostic (itself a correction of v8's invalid raw-nesting argument) — full detail in `CORRECTION_LOG.md` and `docs/provenance/evidence_based_correction_v4_2026-10-09.md`. v9 residualized each birth-year scheme's block against a nuisance set that included the exposure variable itself, then treated equal post-residualization ranks as proof the exposure coefficient was invariant to the choice of scheme. This is circular: residualizing against the exposure variable can remove exactly the part of a block that would otherwise reveal a difference affecting that variable's own coefficient.

## What this pass did

Rewrote the diagnostic into a five-step chain that never uses the exposure variable (E10) to construct any comparison being tested:

1. Compare the two birth-year schemes' demeaned blocks **directly**, before touching E10 or any other covariate.
2. Residualize against the shared nuisance controls **only** (age-in-months, child's age, demographic dummies — E10 excluded), checked with and without age-in-months.
3. Compare E10's own weighted residual exposure vector **directly, elementwise**, under each scheme's complete nuisance specification.
4. Independently cross-check the fitted coefficient via the **explicit weighted Frisch–Waugh–Lovell formula**, computed from scratch and compared against `PanelOLS`'s own output.
5. Explain the mechanical source of the raw column-count difference **without reference to E10 at all** (Nigeria's full own-year dummy set sums exactly to its country indicator, which the cluster fixed effect absorbs).

All five steps agree, reaching the same substantive conclusion as v9 — the two birth-year schemes are equivalent nuisance specifications and the age-in-months omission alone explains the historical 1.385-vs-1.026 discrepancy — now on valid, non-circular grounds, with five independent, mutually-reinforcing lines of evidence instead of one potentially-invalid rank comparison.

## Canonical files and reading order

Unchanged from v9 except `04_empirical_strategy.md` §4.6 and Appendix B §B.2 (both corrected).

## Build

**No PDF was generated, rebuilt, or rendered in this pass.** The existing `../v6_2026-10-07/build/main.pdf` reflects none of v7's, v8's, v9's, or v10's prose corrections.

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this investigation could establish.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; a full prose quality-review pass should be run once more before a submission build.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v9 remain superseded, plus `manuscript/v9_2026-10-07/` itself for the items in `CORRECTION_LOG.md`.
