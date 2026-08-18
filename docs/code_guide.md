# Code Guide

This guide explains how the analytical pipeline is organized and where each methodological decision is implemented in code. It does not reinterpret or add to any empirical decision — it only points to where each one already lives in the code and the accompanying provenance record.

## 1. Purpose and how to use this guide

This guide lets you verify the pipeline's logic by reading, without needing to execute it (the raw DHS microdata that would be required to actually run Steps 00–10 is not included in this repository — see the main `README.md`). Section 3 is a quick lookup table; Section 4 is a stage-by-stage walkthrough; Sections 5–7 index specific methodological decisions, historical provenance, and key variables. Start with Section 2 for orientation, then use Section 3 as a jump table into the actual code.

## 2. Pipeline at a glance

Fourteen scripts, `scripts/dhs_harmonization/00_config.py` through `13_final_outputs.py`, run in numeric order. Most construction stages (05 through 10) each read the immediately preceding stage's output file and write a new one, never editing a file in place. The two analysis stages draw more broadly: Step 12 reads both Step 10's dataset and Step 11's regression output, and Step 13 reads the validated outputs of Steps 07, 11, and 12 (the exact dependency of each step is listed in Section 4). Every stage that touches a source DHS file checksums it before and after execution and stops if it changed. Steps 00–10 build the analytical dataset; Step 11 estimates the main regressions; Step 12 runs robustness checks by reusing Step 11's own functions rather than duplicating them; Step 13 only reformats already-validated results into tables and figures — it estimates nothing new.

## 3. "Where is X?" quick-reference table

| Question | Script | Function / object |
|---|---|---|
| HAZ / WAZ / WHZ construction | `02_load_flag_anthro.py` | `flag_and_scale()` |
| Stunting / wasting / underweight (+severe) | `03_build_indicators.py` | `build_binary_indicator()`, `ANTHRO_INDICATOR_SPECS` |
| WASH category definitions (water/sanitation, incl. Ghana bio-digester) | `01_wash_mapping.py` | `WATER_CATEGORY_MAP`, `SANITATION_CATEGORY_MAP_CORE`, `SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER`, `classify_sanitation_service()`, `SANITATION_SERVICE_COLLAPSE_MAP` |
| WASH categories applied to data | `03_build_indicators.py` | the `map_wash_code(...)` / `build_sanitation_service(...)` calls |
| Leave-one-out water exposure | `08_hr_cluster_wash_exposure.py` | `compute_leave_one_out()`, called with `prefix="water"` |
| Leave-one-out sanitation exposure (core + bio-digester robustness) | `08_hr_cluster_wash_exposure.py` | `compute_leave_one_out()`, called with `prefix="sanitation_core"` / `"sanitation_robustness"` |
| Pooled country weights | `11_main_regressions.py` | `build_temporary_pooled_weight()` |
| PSU/cluster handling | `04_build_country_kr.py` (`psu` = `v021_raw`); `11_main_regressions.py` (`cluster_col = "country_psu"` pooled / `"psu"` country-specific) | |
| Strata handling | `04_build_country_kr.py` (`strata` = `v023_raw`, see the in-code rationale for using v023 uniformly) | |
| Administrative-region fixed effects | `09_admin_region.py` (`admin_region_code`, `country_admin_region`); `11_main_regressions.py` (`FE_VAR = "country_admin_region"`) | |
| Maternal education | `04_build_country_kr.py` (`literacy`... see below; `maternal_education` from `v106`) | `SES_CONTROLS_CATEGORICAL` in `11_main_regressions.py` |
| Maternal literacy | `04_build_country_kr.py` (`literacy` from `v155`) | `SES_CONTROLS_CATEGORICAL` in `11_main_regressions.py` — see Section 6 for the documentation-provenance note |
| Birth order | `10_birth_order.py` | `birth_order_raw` (from DHS `bord`, unchanged) |
| Main Models 1–4 | `11_main_regressions.py` | `MODEL_SPECS` dict |
| Pooled regressions | `11_main_regressions.py` | `run_single_model()`, `country_scope == "pooled"` branch |
| Country-specific regressions | `11_main_regressions.py` | `run_single_model()`, else branch |
| PSU-clustered standard errors | `11_main_regressions.py` | the `sm.WLS(...).fit(cov_type="cluster", cov_kwds={"groups": groups})` call |
| Robustness checks (all 6 families) | `12_robustness.py` | `run_binary_lpm_family()`, `run_severe_outcomes_family()`, `run_ghana_biodigester_family()`, `run_household_baseline_family()`, `run_alternative_weights_family()`, `run_loo_denominator_family()` |
| Ghana bio-digester sensitivity | `12_robustness.py` | `run_ghana_biodigester_family()`, `GHANA_BIODIGESTER_CONTINUOUS`, `assert_ghana_biodigester_isolated()` |
| Alternative pooled weighting | `12_robustness.py` | `run_alternative_weights_family()` |
| Final tables | `13_final_outputs.py` | `build_final_table1()` through `build_final_table6()` |
| Final figures | `13_final_outputs.py` | `figure1_prevalence()`, `figure2_coefficient_forest()`, `figure3_wash_characteristics()`, `map_survey_cluster_coverage()`, `appendix_figure_a1_binary_forest()` |
| Historical Step-11 bug | `11_main_regressions.py` docstring, "KNOWN ISSUE HISTORY" section | `outputs/final_audit/step11_bug_provenance_note.txt` |
| Literacy specification decision | `outputs/final_audit/literacy_specification_decision.txt` | (documentation decision, not a code location) |
| Empirical freeze / audit documentation | `outputs/final_audit/prefreeze_remediation_report.txt`, `step13_final_audit_summary.txt` | |

## 4. Stage-by-stage guide, Steps 00–13

| Step | Methodological title | Purpose | Major inputs | Major outputs | Principal operation | Depends on | Close reading recommended? |
|---|---|---|---|---|---|---|---|
| 00 | Pipeline Configuration and Constants | Paths, cutoffs, weight divisor | — | — | Constants only | — | No |
| 01 | WASH Classification Mapping Definitions | JMP water/sanitation code→category dictionaries | — | — | Mapping definitions only | — | **Yes** |
| 02 | Anthropometric Outcome Loading and Flagging | HAZ/WAZ/WHZ per country, 6-way state classification | Raw KR | staging parquet | Load, classify, scale | — | Light |
| 03 | Anthropometric Indicator and WASH Category Construction | Stunting/wasting/underweight(+severe); WASH categories built | Step 02 + raw KR | staging parquet | Threshold indicators + WASH mapping applied | 02, 01 | **Yes** |
| 04 | Household, Child, and Maternal Control Variable Construction | child_sex, education, literacy, wealth, residence, age, weight, PSU, strata | Step 03 + raw KR | `<country>_kr_clean.parquet` | Decode + construct controls | 03 | **Yes** |
| 05 | Four-Country Dataset Pooling | Row-concatenate 4 countries | 4× Step 04 | pooled parquet | Concat + country-qualified IDs | 04 | Light |
| 06 | DHS Geographic (GE) Cluster Linkage | Attach GE coordinates/region/urban-rural | Step 05 + GE shapefiles | geolinked parquet | Cluster-level join | 05 | Light |
| 07 | Design-Based Descriptive Statistics | Country-specific weighted tables | Step 06 | 5 CSVs | `svy`-package Taylor-linearized estimation | 06 | Light |
| 08 | Leave-One-Out Community WASH Exposure Construction | `water_rate_loo`, `sanitation_rate_loo_core`, bio-digester robustness rate | Step 06 + raw HR | wash-exposure parquet + 2 CSVs | Cluster-level leave-one-out arithmetic | 06 | **Yes** |
| 09 | Administrative-Region Fixed-Effect Construction | `country_admin_region` | Step 08 + raw KR | admin-region parquet + 2 CSVs | Region-code join, per-country source variable | 08 | **Yes** |
| 10 | Birth-Order Control Extraction | `birth_order_raw` | Step 09 + raw KR | birth-order parquet + CSV | Direct extraction, double-checked | 09 | Light |
| 11 | Main Continuous-Outcome Regression Models | 60 WLS fits: HAZ/WAZ/WHZ × Models 1–4 × 5 scopes | Step 10 | 2 CSVs | Pooled/country-specific WLS, cluster-robust SEs | 10 | **Yes** |
| 12 | Robustness and Sensitivity Analysis | 6 robustness families | Step 10 + Step 11 (read-only) | 7 CSVs | Reuses Step 11's own functions | 10, 11 | **Yes** |
| 13 | Final Table, Figure, and Audit Production | Reformat only, zero new statistics | Step 07/11/12 (read-only) | 6 tables, 8 appendix, 5 figures, 3 audit files | Rounding/relabeling/reshaping only | 07, 11, 12 | **Yes** |

## 5. Methodological decision index

- **WASH classification** — `01_wash_mapping.py` (definitions) applied in `03_build_indicators.py`.
- **Leave-one-out arithmetic** — `08_hr_cluster_wash_exposure.py`, `compute_leave_one_out()`: for household *i* in cluster *j*, `other_n = cluster_n - own_included`, `other_sum = cluster_sum - own_value`, `rate = other_sum / other_n` where `other_n >= 1`. This explicitly excludes the index household's own observation from both numerator and denominator.
- **Pooled weighting** — `11_main_regressions.py`, `build_temporary_pooled_weight()`: `w_i = weight_original_i / W_k`, where `W_k` is the sum of `weight_original` within country *k* in that specific model's estimation sample, forcing every country's total weight to equal 1.0. This is a thesis-specific equal-country-weighting construction, not an implementation of the DHS Sampling and Household Listing Manual's population-proportional de-normalization procedure — the two are different, not interchangeable (see the pre-freeze remediation report for the full comparison).
- **Fixed effects** — `09_admin_region.py` builds `country_admin_region` directly from each country's own DHS administrative-region variable (`v024` for Ethiopia/Ghana/Kenya, `sstate1` for Nigeria); `11_main_regressions.py` applies it as explicit dummy encoding (`pd.get_dummies`), Model 4 only.
- **Standard-error methodology** — Step 07 (`07_descriptives.py`) uses the `svy` package's genuine stratified Taylor-linearized design-based estimator. Steps 11/12 use `statsmodels` PSU-clustered sandwich (cluster-robust) standard errors, which account for intra-PSU clustering but not stratification or finite-population correction. These are two different variance methodologies for two different purposes — not interchangeable, and not both "the same as DHS's own design-based estimator."
- **Ghana bio-digester decision** — `01_wash_mapping.py`: DHS sanitation code 16 (Ghana-specific) is left unclassified ("UnclassifiedBioDigester") in the core specification, with an explicit code comment that no authoritative JMP source was found; a separate robustness variant reclassifies it as "Improved." This is an open methodological judgment, handled through the robustness analysis (`12_robustness.py`, `run_ghana_biodigester_family()`), not a settled classification.
- **Literacy inclusion** — `11_main_regressions.py`, `SES_CONTROLS_CATEGORICAL` includes `literacy` (from DHS `v155`) alongside `maternal_education` (from `v106`) as two independent controls. See Section 6 for the documentation-provenance history of this variable.

None of the above decisions were reinterpreted, revisited, or changed in writing this guide — this section only locates them.

## 6. Provenance / known-issues index

All full-detail documents live in `outputs/final_audit/` (see `outputs/final_audit/README_AUDIT.md` in this package for a one-line-per-file index):

- **Historical Step-11 exposure-omission bug** — an early execution of `11_main_regressions.py` omitted the two primary exposures from the design matrix; caught by manual spot-check, corrected, and the corrected code is what produced every result now in this package. Full detail: `11_main_regressions.py`'s own "KNOWN ISSUE HISTORY" docstring, and `step11_bug_provenance_note.txt`.
- **Pre-freeze remediation** — `prefreeze_remediation_report.txt`: documents a `requirements.txt` dependency fix, a new defensive assertion added to `11_main_regressions.py` guarding against recurrence of the bug above, and independent verification of a sparsity diagnostic claim.
- **Kenya zero-event verification** — `kenya_zero_event_region_verification.txt`: independently re-confirms a specific sparsity statistic underlying the decision to run severe-outcome robustness models pooled-only.
- **Literacy specification decision** — `literacy_specification_decision.txt`: documents that the `literacy` control's presence was not traceable to the original design documentation, the resulting provenance investigation, and the explicit decision to retain it rather than re-estimate the frozen results.
- **Step-13 final audit** — `step13_final_audit.csv` / `step13_final_audit_summary.txt`: the 24-point automated integrity check Step 13 runs on every final output before writing it.

## 7. Key-variable glossary

| Variable | Meaning |
|---|---|
| `water_rate_loo` | Cluster-level leave-one-out share of other households with improved water access |
| `sanitation_rate_loo_core` | Cluster-level leave-one-out share of other households with improved sanitation (core/conservative Ghana bio-digester treatment) |
| `sanitation_rate_loo_robustness_biodigester` | Same as above, robustness variant with Ghana bio-digester reclassified as improved |
| `country_admin_region` | Country-qualified administrative-region identifier, the Model 4 fixed effect |
| `weight_original` | DHS-standard rescaled sampling weight (`v005`/`hv005` ÷ 1,000,000), used unmodified in country-specific models |
| `literacy` | Mother's literacy (DHS `v155`, 5-category, reference "Cannot read at all") |
| `maternal_education` | Mother's education level (DHS `v106`, 4-category, reference "No education") — a separate, independent control from `literacy` |
| `birth_order_raw` | DHS `bord`, preserved unchanged |
| `country_psu` / `psu` | Clustering identifiers for standard errors — pooled models cluster on `country_psu`, country-specific models on `psu` |

## 8. Reproducibility prerequisites

**DHS microdata are NOT included in this package.** Nothing under `data/raw/`, `data/interim/`, or `data/processed/` is packaged, because these contain DHS respondent-level microdata governed by the DHS Program's own data-use terms. This package lets you read and verify the pipeline's logic; it does not itself grant DHS data access. To actually re-run any stage, you would need your own DHS Program-authorized access to the same four surveys (Ethiopia 2024-25, Ghana 2022, Kenya 2022, Nigeria 2024) and would need to place the raw KR/HR/GE files in the directory structure `00_config.py`'s `COUNTRIES` dict expects.

**Environment**: Python 3.14.0; install dependencies from `requirements.txt` via the venv's own pip. On Windows, if `Activate.ps1` is blocked by PowerShell's execution policy, call the venv's Python executable directly (e.g., `.venv\Scripts\python.exe scripts\dhs_harmonization\11_main_regressions.py`) rather than changing the execution policy — this works regardless of activation state.

**Run order**: strictly numeric, 00 through 13; each stage from 05 onward reads only the immediately preceding stage's output file (see Section 4's dependency column).

**Hard-fail validation philosophy**: every script raises `RuntimeError` rather than silently continuing whenever an assumption it depends on is violated (unexpected row counts, checksum mismatches, rank-deficient design matrices, unmapped codes, etc.). A `RuntimeError` from any script is the pipeline working as intended — it means a specific, named assumption failed, not that the code crashed unexpectedly. Read the specific error message; it names the exact check that failed.

No master pipeline runner is provided or recommended — see the project's package-design audit for the reasoning (raw and processed DHS data are both access-gated, so a runner cannot itself be run by anyone without independent DHS authorization regardless of tooling).
