# Final empirical package v1 — results index (2026-10-07)

> **Superseded (2026-10-07, later the same day) for §B (historical extension) and the overall status statements.** See `final_empirical_package_v2_2026-10-07/00_results_index.md` for the current authority: the pooled headline estimate is now independently verified, Ethiopia candidate C1 is reclassified invalid, the IHME product definitions are resolved, and the issue list is reconciled. §A (baseline) below is still current and was not changed.

Single entry point to the exact files a thesis chapter should cite. Every path is relative to the repository root `thesis-wash-child-nutrition-dhs/` unless marked RESTRICTED (those live under the master folder's `data/`, are git-ignored, and are not for citation by path in a public manuscript — cite the corresponding public aggregate instead).

## A. Baseline (current four-round, cross-sectional WASH)

| Status | Result | File | Notes |
|---|---|---|---|
| **Validated — main reporting** | Household water/sanitation, cluster FE (HAZ/WAZ/WHZ, PRIMARY inference convention) | `outputs/household_community_wash/03_household_cluster_fe.csv` | Use the `PRIMARY_SAME_CLUSTER_CRV1` rows. Water HAZ p=.062, sanitation HAZ p=.548. |
| **Validated — main reporting** | Household, region FE | `outputs/household_community_wash/02_household_region_fe.csv` | |
| **Validated — main reporting** | Community water/sanitation, 4-stage adjustment (minimal → +child → +SES → +SES+region FE) | `outputs/regressions/main_continuous_models.csv` | Filter `term` in {`water_rate_loo`,`sanitation_rate_loo_core`}, `country_scope`=`pooled`. |
| **Validated — secondary** | Joint household+community model | `outputs/household_community_wash/05_joint_household_community.csv` | Household water HAZ β=−0.085, p=.043 (common sample), unexpected direction, single significant cell — report as such, not as a central finding. |
| **Validated — secondary** | Age-heterogeneity joint tests | `outputs/household_community_wash/10_age_heterogeneity_joint_tests.csv` | 11 of 12 water/sanitation joint tests reject at 5% (exclude the 6 broader "all interactions" rows from that count). |
| **Validated — robustness** | Nigeria community-sanitation specification sensitivity | `outputs/household_community_wash/11_nigeria_sign_reversal.csv` | Shows sign reversal is wealth-quintile-driven, not stable; do not read as a finding about sanitation. |
| **Validated — robustness** | Country-specific household cluster-FE models | `outputs/household_community_wash/15_country_household_cluster_fe.csv` | |
| **Validated — robustness** | Alternative weights, binary LPM, biodigester, LOO-denominator robustness | `outputs/regressions/robustness_*.csv` | Not re-audited in this pass; unchanged since the frozen baseline. |
| Supporting diagnostic | Within-cluster WASH variation (share of informative PSUs) | `outputs/household_community_wash/04_household_cluster_fe_support.csv` | 31.6% water, 50.6% sanitation. |
| Methods/inference convention | — | `docs/provenance/cluster_fe_inference_adjudication.md` | Defines PRIMARY vs. sensitivity DF convention. |
| Reconciliation | — | `docs/provenance/baseline_evidence_reconciliation_v1_2026-10-07.md` | Corrects two stale values found in earlier drafts; everything else in those drafts was re-checked and confirmed accurate. |

Do not cite `outputs/supervisor_development/22_supervisor_roadmap_final.md` or `26_empirical_strategy_final_candidate.md` for numeric values — both contain the superseded sensitivity-convention p-values and the wrong age-heterogeneity count. Cite the files above instead.

## B. Historical WASH extension (IHME 2000–2017, established-date sample: Ghana 2014, Kenya 2014, Nigeria 2018)

| Status | Result | File | Notes |
|---|---|---|---|
| **Exploratory/provisional** | 291 preliminary models (24 primary + 267 sensitivity/window/robustness) | `docs/provenance/historical_wash_preliminary_estimates_v1/` (public aggregate) | Primary results table reproduced in `historical_wash_preliminary_estimation_methods_2026-10-06.md` §6. |
| **Exploratory/provisional** | Methods, literature basis, source resolutions, estimator, unresolved issues | `docs/provenance/historical_wash_preliminary_estimation_methods_2026-10-06.md` | The single authoritative methods note for this extension. |
| **Exploratory/provisional, separately labelled** | Ethiopia 2016 sensitivity (3 interview-date candidates) | §7 of the methods note above | Not an established-date result; keep out of any pooled headline estimate. |
| Validated (as implementation checks, not as thesis findings) | Independent re-estimation of 4 representative models | RESTRICTED: `data/processed/estimation/validation_20261006T185831Z/` → public summary in methods note §5 | Max β diff 2.96×10⁻¹⁴, max CRV1-SE relative diff 7.5×10⁻¹⁰. |
| Validated (design checks) | 24 primary models: key uniqueness, cluster-survey mapping, weight totals, rank, singletons | RESTRICTED: `data/processed/estimation/run_20261006T185646Z/design_checks_20261006T190020Z/` | All checks pass (`design_checks_summary.json`). |
| Supporting | Common-sample (all-window) comparison | RESTRICTED: `data/processed/estimation/common_sample_20261006T185909Z/` | Pooled water HAZ moves from 1.03 (own-eligible post_12m) to 1.64 (common sample, n=16,419) — a sample-composition effect, documented, not a window endorsement. |
| Design | Exposure window, completion rule, displacement handling | `docs/provenance/historical_wash_design_v1.md`, `historical_wash_exposure_construction_spec_v1_2026-10-06.md` | |
| Design | Spatial extraction method (AEQD exact overlap) | `docs/provenance/historical_wash_spatial_extraction_2026-10-06.md`, `historical_wash_spatial_geometry_addendum_2026-10-06.md` | |
| Design | Weights and measurement-universe notes | `docs/provenance/historical_wash_weights_and_measurement_2026-10-06.md` | |
| Supervisor-advice mapping | — | `docs/provenance/historical_wash_supervisor_advice_matrix_2026-10-07.md` | |

**No coefficient in section B is a thesis result yet.** Promotion to "validated for main reporting" requires closing the items in `historical_wash_preliminary_estimation_methods_2026-10-06.md` §9 (measurement-subsample weighting, Nigeria count gap, water-product definition, Ethiopia timing, window choice, DHS/IHME input overlap, pooled-weighting estimand). None of these were closed in this pass; two (DHS biomarker weight documentation) were re-attempted against two further sources and remain unresolved (see the completion report).

## C. Not estimable

None. All 291 historical models and all baseline models planned were estimated; none failed or was dropped.

## D. Superseded (preserved, not for citation)

- `scripts/historical_wash/08_spatial_extraction_PREPARED.py` — superseded by v3.
- `scripts/historical_wash/09_spatial_extraction_v2.py` — failed self-test (non-monotone convergence at small buffers); superseded by v3.
- `data/processed/historical_wash/v1_run1_SUPERSEDED_nodata_parse_bug/` — RESTRICTED; NoData parsed as string, giving spurious valid pixels.
- `data/processed/ipums_import/v2/run_20261006T135809Z`, `135824Z`, `135838Z` — RESTRICTED; superseded/failed import runs, preserved for lineage.
- `outputs/supervisor_development/22_supervisor_roadmap_final.md`, `26_empirical_strategy_final_candidate.md` — contain stale values (§A above); preserved, superseded as a numeric source by the reconciliation note.
