# Manuscript source package v11 (2026-10-09) — final source-package verification

Supersedes `manuscript/v10_2026-10-07/` as the canonical manuscript source. v1 through v10 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**. **No empirical estimate, sample, weight actually used in any model, control set, or reported coefficient/SE/CI/p-value changed.**

This pass is the result of a bounded final source-package verification: every numerical claim in the canonical chapters and appendices was checked directly against its authoritative output file (not assumed from an earlier pass's say-so), and variable/weight/fixed-effect descriptions were checked against the actual implemented code. Full detail: `docs/provenance/final_source_verification_v1_2026-10-09.md`.

## What this pass found and corrected

1. **`01_introduction.md` §1.6** stated the household sanitation–HAZ confidence interval's upper bound as `0.110`. The authoritative source (`outputs/household_community_wash/03_household_cluster_fe.csv`, value 0.109150) and this manuscript's own Table 5.1 (`05_results.md`) both correctly round this to `0.109`. One-digit correction; the coefficient, p-value, and every other reported figure for this cell were already correct and unchanged.
2. **`04_empirical_strategy.md` §4.5** stated a single weighting formula (scaling to sum to exactly $N/M$ per country) as applying "generically across both samples." Checking this against the actual code found that only the historical pipeline (`scripts/historical_wash/16_estimate_preliminary.py`) implements the $N/M$ scaling; the baseline pipeline (`scripts/dhs_harmonization/11_main_regressions.py`'s `build_temporary_pooled_weight()`) normalises each country's weights to sum to exactly $1$ instead, omitting that constant. This was confirmed to have **zero effect on any reported number**: WLS and its cluster-robust sandwich variance are both invariant to rescaling every observation's weight by one constant shared by every observation in a given model — confirmed directly by refitting a synthetic model under both conventions and finding identical coefficients and standard errors to machine precision. The formula was rewritten to state precisely what each pipeline implements and why the difference is inert.

## What this pass checked and found already correct

Every coefficient, SE, CI, p-value, N, and cluster count in `05_results.md`'s nine tables (household region-FE and cluster-FE, community adjustment path, joint household/community model, Nigeria specification-sensitivity, age-heterogeneity joint tests, the 24-cell historical core table, window comparison, further sensitivity, and Ethiopia provisional) was checked directly against its authoritative CSV/output file and matched exactly (to the displayed precision) in every case but the one corrected above. The abstract, conclusion, and discussion sections' numerical claims were checked and matched. Variable-construction claims (`v005`→`weight_original` via the documented 1,000,000 divisor, `v021`→`psu`, `hv005`'s absence from the baseline models, `b19` as the baseline age field, the historical extension's country-varying `age_m` construction) were checked directly against the harmonization and historical-pipeline code and matched exactly. Appendix B's independent-verification figures and Appendix C's Ethiopia diagnostic figures were checked against their own restricted source outputs where still available and matched.

Two minor rounding-boundary questions raised by this pass — the historical core table's Ghana sanitation–HAZ CI lower bound (displayed `−4.91` from a 3-decimal source value of `−4.915`) and Kenya sanitation–HAZ CI upper bound (displayed `0.11` from `0.105`) — were, at the time, reported as unresolvable because the full-precision restricted source could not be found. That was a path-mismatch error, corrected the same day: the source file exists, fully intact, in the master `C:\Users\user\Documents\Graduation_Thesis\data\` directory (one level above this git repository, where this project's scripts actually read and write all restricted data), not inside the repository's own `data/` subdirectory. Both values are now confirmed correct directly from that source (row ids `m0142`, `m0143`: full-precision values `−4.9146807319418855` and `0.1053050394220738` round to `−4.91` and `0.11` respectively). See `docs/provenance/source_lineage_correction_v1_2026-10-09.md`.

## Canonical files and reading order

Unchanged from v10 except `01_introduction.md` §1.6 and `04_empirical_strategy.md` §4.5 (both corrected as above).

## Build

**No PDF was generated, compiled, rebuilt, or rendered in this pass** — PDF generation is explicitly not authorized for this task. The existing `../v6_2026-10-07/build/main.pdf` reflects none of v7's through v11's prose corrections. Any in-progress or prior PDF-build artifacts from outside this manuscript package were checked for at the start of this pass: none were found (no running build process, no file modified in this repository in the preceding two hours, no `build/` directory under v10 or v11).

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this and prior verification passes could establish — every numerical claim checked against its authoritative source, every bibliographic entry checked against primary registries, every variable/weight/FE description checked against the implemented code. This is not a claim that every conceivable error has been eliminated; it is a statement of what was specifically checked and what was found.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; the next stage (a separately authorized complete draft PDF build and page-by-page review) has not begun.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v10 remain superseded, plus `manuscript/v10_2026-10-07/` itself for the two items in `CORRECTION_LOG.md`.
