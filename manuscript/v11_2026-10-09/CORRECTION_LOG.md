# Correction log: v10 → v11 (2026-10-09)

Corrects two small issues found during a bounded final source-package verification (every numerical claim in the canonical chapters/appendices checked against its authoritative output file; variable/weight/FE descriptions checked against the implemented code). v10 is preserved unchanged; see `../v10_2026-10-07/` (a `POINTER_TO_V11.md` is added there). **No empirical estimate, sample, weight actually used in any model, control set, or reported coefficient/SE/CI/p-value changed.** Full investigation detail: `docs/provenance/final_source_verification_v1_2026-10-09.md`.

## What changed

| # | File | Change |
|---|---|---|
| 1 | `01_introduction.md` §1.6 | Household sanitation–HAZ confidence-interval upper bound corrected from `0.110` to `0.109`, matching the authoritative source (`outputs/household_community_wash/03_household_cluster_fe.csv`, value 0.109150) and this manuscript's own Table 5.1 (`05_results.md`), which already stated `0.109` correctly. This was an internal inconsistency between two sections of the same document, not an error traceable to the data or the estimation code. |
| 2 | `04_empirical_strategy.md` §4.5 | The weighting-formula paragraph rewritten. It previously stated a single formula (scaling to sum to $N/M$ per country) as applying "generically across both samples." Checking against the actual code (`scripts/historical_wash/16_estimate_preliminary.py` for the historical pipeline; `scripts/dhs_harmonization/11_main_regressions.py`'s `build_temporary_pooled_weight()` for the baseline pipeline) found only the historical pipeline implements the $N/M$ scaling; the baseline pipeline normalises to sum-to-$1$ per country instead. The paragraph now describes what each pipeline actually implements and states explicitly, with a confirmed numerical demonstration, that this difference has no effect on any reported coefficient, SE, CI, or p-value (WLS and its cluster-robust sandwich variance are invariant to a uniform per-observation weight rescaling). |

## Targeted checks executed

- Read every numerical claim in `01_introduction.md`, `04_empirical_strategy.md`, `05_results.md`, `06_discussion_and_limitations.md`, `07_conclusion.md`, `08_abstract.md`, and Appendices A–C, and checked each directly against its authoritative source file: `outputs/household_community_wash/02_household_region_fe.csv`, `03_household_cluster_fe.csv`, `04_household_cluster_fe_support.csv`, `05_joint_household_community.csv`, `10_age_heterogeneity_joint_tests.csv`, `11_nigeria_sign_reversal.csv`, `15_country_household_cluster_fe.csv`; `outputs/regressions/main_continuous_models.csv`; `docs/provenance/final_empirical_package_v3_2026-10-07/02_core_reporting_table.md`; `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` and `window_common_sample_PRELIMINARY_AGGREGATE.csv`; `docs/provenance/historical_wash_preliminary_estimation_methods_2026-10-06.md`; `docs/empirical_strategy.md`. Every figure matched exactly except the one corrected above.
- Checked variable-construction claims against the actual harmonization/historical-pipeline code: `v005`→`weight_original` (the 1,000,000 divisor), `v021`→`psu`, `hv005`'s confinement to the Household Recode and absence from the baseline models, `b19` as the baseline age field, and the historical extension's country-varying `age_m` construction (reported for Ethiopia/Nigeria, calendar-difference for Ghana/Kenya) — all confirmed to match the manuscript's descriptions exactly.
- Numerically confirmed the weight-rescaling invariance claim (item 2) by refitting a synthetic weighted-least-squares model with cluster-robust SE under both weighting conventions and finding identical coefficients and standard errors to machine precision.
- Re-checked the four bibliographic/reference-package corrections from the immediately preceding task (`459c84c`→`5b98a71`): confirmed the two remaining printable audit notes (Momberg2021, PerezHeydrich2013) remain removed, their explanations remain in `bibliography_verification_ledger.md`, the WHO collective-author label is correct, and version headings/correction counts are consistent. No further bibliographic change was needed.
- Checked for any in-progress or recent PDF-build process at the start of this task: none found (no running agent, no file in this repository modified in the preceding two hours, no `build/` directory under v10 or v11).

## What this pass did not do

Did not re-run any of the 291 historical models or any baseline model. Did not generate, compile, rebuild, or render any PDF — explicitly not authorized for this task. Did not begin the next-stage draft-PDF build or page-by-page review.

**Addendum (same day, later pass, commit `068ee4c`→):** the two rounding-boundary values noted above as unresolved were in fact resolvable — this pass's own search for the full-precision restricted source checked only this git repository's own `data/` subdirectory, not the master `C:\Users\user\Documents\Graduation_Thesis\data\` directory one level above, where the source actually resides, fully intact. Both values are now confirmed correct from that source; see `README.md` and `docs/provenance/source_lineage_correction_v1_2026-10-09.md`.

## Canonical path

`manuscript/v11_2026-10-09/` supersedes `v10_2026-10-07/` (pointer added there).
