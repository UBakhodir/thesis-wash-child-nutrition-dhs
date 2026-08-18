# Master Design Document

**Thesis:** The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa: Evidence from DHS and Geospatial Data
**Author:** Bakhodir Izzatulloev — MSc Economics
**Status:** The empirical pipeline (`scripts/dhs_harmonization/00_config.py` through `13_final_outputs.py`) is complete and frozen, and has produced the regression outputs, tables, and figures included in this repository.
**Last updated:** 2026-08-18

This document has two parts. **Part I** describes the empirical design exactly as it was implemented and estimated — this is the authoritative description of the analysis behind the results in this repository. **Part II** preserves the original pre-implementation research plan, since the implemented design departs from that plan in several respects (documented explicitly in Part I). Part II is retained for project history; it does not describe results that exist anywhere in this repository, and nothing in Part II should be read as a description of the frozen analysis.

For a code-level walkthrough of where each element of Part I is implemented, see `docs/code_guide.md`. For exact raw and derived variable definitions, see `docs/data_dictionary.md`.

---

# PART I — AS-IMPLEMENTED DESIGN

## 1. Research Question

**Main question:** Is improved access to water and sanitation associated with better child nutritional outcomes in Sub-Saharan Africa?

**Sub-questions:**
1. Is improved sanitation coverage associated with higher child height-for-age z-scores (HAZ)?
2. Is improved water access associated with better child nutritional outcomes?
3. Do these associations differ across Ethiopia, Ghana, Kenya, and Nigeria?
4. Are the associations robust to alternative outcome coding, alternative sanitation classifications, alternative weighting schemes, and alternative exposure-construction choices?

## 2. Objectives

**General objective:** To estimate the **association** between improved water and sanitation access and child nutritional outcomes in Ethiopia, Ghana, Kenya, and Nigeria, using pooled DHS survey microdata linked to DHS geographic cluster data.

The identification strategy implemented (Part I, §10) does not support a causal interpretation. Every regression coefficient produced by this pipeline is reported and must be interpreted as an association, not a causal effect.

**Specific objectives, as implemented:**
1. Quantify the association between household-level and cluster-level (leave-one-out) sanitation access and HAZ, WAZ, and WHZ.
2. Quantify the equivalent association for water access.
3. Estimate the preferred specification both pooled across all four countries and separately for each country.
4. Assess robustness to: binary outcome coding (stunting/wasting/underweight), an alternative Ghana sanitation classification, alternative pooled-weighting schemes, alternative leave-one-out denominator thresholds, and a household-level (non-cluster) exposure baseline.

## 3. Hypotheses

- **H1:** Cluster-level (leave-one-out) sanitation coverage is positively associated with HAZ, WAZ, and WHZ.
- **H2:** Cluster-level (leave-one-out) water coverage is positively associated with HAZ, WAZ, and WHZ.
- **H3 (robustness form):** Sanitation and water coverage are negatively associated with the probability of stunting, wasting, and underweight.

Hypotheses are stated as expected signs for an associational analysis, not as claims that will be causally tested.

## 4. Conceptual Framework

The motivating channel, unchanged from the original proposal:

```
Improved water/sanitation access (environmental infrastructure)
        │
        ▼
Reduced exposure to fecal-oral pathogens, diarrheal disease,
        and intestinal infections (environmental health shocks)
        │
        ▼
Improved nutrient absorption
        │
        ▼
Improved child growth and nutritional status (HAZ, WAZ, WHZ)
```

Two features of this channel shaped the empirical design that was actually implemented:

- **Externalities:** because sanitation reduces environmental contamination beyond the household that installs it, a child's nutritional status may depend on the surrounding community's coverage, not only on the child's own household's facilities. This is why the primary exposure variables are cluster-level **leave-one-out** coverage rates (`water_rate_loo`, `sanitation_rate_loo_core`) rather than household-level indicators alone — the leave-one-out construction specifically excludes the child's own household from the neighborhood rate it is matched to, so that a household's own WASH status does not mechanically enter its own exposure measure (see §7 and `docs/code_guide.md` §5).
- **Non-random assignment:** access to improved WASH infrastructure correlates with wealth, education, and geography — all of which independently affect child nutrition. The implemented design addresses this by controlling for household/child characteristics and administrative-region fixed effects (§9–§11), not by claiming a causal identification strategy — see §10 for the explicit limits of what this design can and cannot establish.

## 5. Data Sources

| Source | File | Content |
|---|---|---|
| DHS | Children's Recode (KR) | Child anthropometry (HAZ/WAZ/WHZ), age, sex, birth order, mother characteristics |
| DHS | Household Recode (HR) | Water source, sanitation facility, household size, used to build the leave-one-out cluster WASH exposure |
| DHS | GE (geographic) files | DHS cluster coordinates (randomly displaced for confidentiality) and administrative-region codes, used for country-qualified administrative-region linkage |

**Countries and survey rounds actually used** (fixed, not exploratory): Ethiopia 2024-25, Ghana 2022, Kenya 2022, Nigeria 2024 — one DHS round per country. No geospatial raster covariates (rainfall, temperature, elevation, population density) were extracted or used anywhere in the implemented pipeline; the original plan to include them (Part II) was not carried into implementation. No IR (individual women's recode) data beyond what is already present in KR was used.

## 6. Unit of Analysis

The unit of analysis is the **child**. The dataset is a pooled **cross-section** of children across the four countries — one DHS round per country, not a multi-round panel. Indexing:

- `i` = child
- `c` = DHS cluster, linked to a country-qualified administrative region for fixed-effects purposes (§11)
- `k` = country

There is no survey-year dimension `t` in the implemented design: each country contributes exactly one cross-sectional DHS round, so there is no within-country variation over time to exploit, and none is claimed.

## 7. Variables

### 7.1 Dependent Variables

**Primary outcomes (continuous z-scores):**
- `haz` — height-for-age z-score
- `waz` — weight-for-age z-score
- `whz` — weight-for-height z-score

**Robustness outcomes (binary, WHO cutoff of −2 SD):**
- `stunted = 1[haz < −2]`
- `wasted = 1[whz < −2]`
- `underweight = 1[waz < −2]`

**Secondary/appendix outcomes (binary, severe, cutoff of −3 SD):** `severe_stunted`, `severe_wasted`, `severe_underweight` — estimated pooled only, because `severe_wasted` has 24 of 114 administrative-region fixed-effect cells with zero events (18 of them in Kenya alone; verified independently, see `outputs/final_audit/kenya_zero_event_region_verification.txt`), which would make country-specific severe-outcome models unstable.

### 7.2 Independent Variables

**Cluster-level, leave-one-out (the primary exposures, used in every model):**
- `water_rate_loo` — leave-one-out share of other households in the child's DHS cluster with improved water access
- `sanitation_rate_loo_core` — leave-one-out share of other households in the child's DHS cluster with improved sanitation access (core classification; see §7.3 on the Ghana sanitation-code judgment call)

**Household-level (robustness-only, not part of the preferred specification):**
- A household-level binary water indicator and a household-level binary sanitation indicator are used only in one robustness family (§12, family 4), without administrative-region fixed effects, to test whether the cluster-level result is sensitive to using a simple household-level measure instead.

### 7.3 Control Variables

**Included from Model 2 onward:** child sex, child age in months (`b19_raw`), birth order (`birth_order_raw`, entered linearly).

**Included from Model 3 onward:** maternal age, maternal education (`maternal_education`, from DHS `v106`, 4 categories, reference "No education"), maternal literacy (`literacy`, from DHS `v155`, 5 categories, reference "Cannot read at all"), household wealth quintile (DHS-constructed, reference "Poorest"), household size (`household_size_raw`, entered linearly), urban/rural residence (`residence`, reference "Rural").

**Maternal literacy — provenance note.** Maternal literacy was not listed as a control in the earliest version of this document (Part II, §7.3 original). It entered the empirical implementation during pipeline construction and was used consistently from that point forward in Models 3–4 and every applicable robustness specification; the frozen results reflect its inclusion. A dedicated provenance investigation searched this document, `docs/data_dictionary.md`, `README.md`, and all pipeline script docstrings for evidence that its inclusion was a reviewed, intentional departure from the original plan; no such record was found, and none is asserted here. The investigation also found no evidence its inclusion was an error: it is technically valid (the design matrix is full rank in every model that includes it), it is a construct distinct from maternal education (DHS `v106` measures schooling attainment; `v155` is a directly-administered reading-comprehension test, and the two are not deterministically related in this sample outside the "Higher education" category, where DHS does not administer the literacy test and auto-codes literacy), and maternal literacy is a recognized covariate in closely related published DHS child-height research (Spears 2013, one of this project's literature sources, uses maternal literacy as a control in the same type of regression). Because the empirical results were already known when this discrepancy was discovered, the decision was to retain literacy exactly as implemented and correct the documentation to match, rather than remove the variable and re-estimate every affected model. Maternal education and maternal literacy are retained as two separate, independent controls, not substitutes for one another. Full provenance detail: `outputs/final_audit/literacy_specification_decision.txt`.

**Not implemented:** the original plan's geospatial raster controls (rainfall, temperature, elevation, population density) were never extracted or used (Part II, §7.3 original; §5 above).

## 8. Construction of Every Variable

| Variable | Construction rule (as implemented) |
|---|---|
| `haz` / `waz` / `whz` | DHS-computed anthropometric z-scores (`hw70`/`hw71`/`hw72`), rescaled from DHS's stored ×100 integer format; DHS special/missing codes (9996–9999) excluded before scaling. |
| `stunted` / `wasted` / `underweight` | Binary indicator, 1 if the corresponding z-score < −2, else 0; not created when the source z-score is missing. |
| `severe_stunted` / `severe_wasted` / `severe_underweight` | Same construction at a −3 cutoff; a hard-coded check enforces that severe==1 implies the corresponding standard indicator==1. |
| Water / sanitation category | Recoded from DHS `hv201`/`hv205` (household file) and `v113`/`v116` (children's file, used for household-level construction in the harmonization stage) per JMP-based category dictionaries defined once in `01_wash_mapping.py`. Sanitation has two variants: a **core** classification, in which Ghana's DHS sanitation code 16 (a locally-used bio-digester category) is left explicitly unclassified because no authoritative JMP mapping for it was found, and a **robustness** classification, in which the same code is reclassified as improved. |
| `water_rate_loo`, `sanitation_rate_loo_core`, `sanitation_rate_loo_robustness_biodigester` | Leave-one-out cluster coverage rate, computed from the DHS household (HR) file: for household *i* in cluster *j*, the rate equals the improved-WASH share among all *other* eligible households in *j*, excluding household *i* itself, computed on the full HR household census (not deduplicated to households with children) and unweighted. Households with an excluded WASH state (unknown, structurally not applicable, or — in the core sanitation variant — the unclassified Ghana bio-digester code) are excluded from both the numerator and denominator; a rate is left missing only if zero other eligible households remain in the cluster. |
| `country_admin_region` | Each country's own DHS administrative-region sampling variable (Ethiopia and Ghana: `v024`; Kenya: `v024`, all 47 counties preserved; Nigeria: `sstate1`, all 37 states/FCT preserved), prefixed with the country name so codes never collide across countries. |
| `maternal_education`, `literacy`, `wealth_quintile`, `residence` | Decoded directly from DHS `v106`, `v155`, the DHS-constructed wealth-quintile variable, and `v025`, respectively; no collapsing or recoding beyond label decoding. |
| `birth_order_raw`, `household_size_raw`, `b19_raw` | DHS `bord`, `hv009`, and `b19`, preserved as the original integer values with no categorization or transformation. |
| `weight_original` | DHS sampling weight (`v005`/`hv005`) divided by 1,000,000, the standard DHS rescaling; used unmodified in country-specific models. |
| Pooled model weight | A temporary, model-specific weight computed only in memory for pooled regressions (never written to any file): each observation's `weight_original` is divided by the sum of `weight_original` within its own country in that model's estimation sample, so every country contributes an equal total weight to the pooled regression. This is a thesis-specific equal-country-weighting construction; it is not the DHS Sampling and Household Listing Manual's population-proportional pooled-survey de-normalization procedure, and should not be described as implementing that procedure (see `outputs/final_audit/prefreeze_remediation_report.txt` for the detailed comparison). |
| Sample restriction | Children with a valid outcome and non-missing values for the relevant model's exposures and controls; no separate age restriction beyond what DHS's own KR file structure implies. |
| Multiple births/siblings | Retained in the sample; non-independence is addressed through PSU-clustered standard errors, not sample restriction. |

Not implemented: `grid_id` (a fixed spatial-grid spatial unit) and the geospatial raster covariates described in the original plan (Part II) were never constructed.

## 9. Econometric Models

Estimated in `scripts/dhs_harmonization/11_main_regressions.py` for each of `haz`, `waz`, `whz`, both pooled across all four countries and separately for each country (60 regressions in total). All four models retain both exposure variables; each successive model adds one further control block.

- **Model 1:** exposures only.
- **Model 2:** Model 1 + child controls (child sex, age, birth order).
- **Model 3:** Model 2 + maternal/household controls (maternal age, maternal education, maternal literacy, wealth quintile, household size, residence).
- **Model 4 (preferred):** Model 3 + `country_admin_region` fixed effects.

$$
\text{Nutrition}_{ick} = \beta_1\, \text{WaterRateLOO}_{ck} + \beta_2\, \text{SanitationRateLOO}_{ck} + X'_{ick}\gamma + \alpha_{ck} + \varepsilon_{ick}
$$

where $\text{Nutrition}_{ick} \in \{\text{haz}, \text{waz}, \text{whz}\}$, $\alpha_{ck}$ is the country-qualified administrative-region fixed effect (Model 4 only), and $X_{ick}$ is the relevant control block. Estimated by weighted least squares (`statsmodels.WLS`); fixed effects are entered as explicit categorical dummy variables (`pandas.get_dummies`), not through a panel-data absorption estimator such as `linearmodels.PanelOLS` — no such estimator is used anywhere in this pipeline, since the design is cross-sectional, not a panel.

Binary-outcome robustness models (§12, family 1) use the same right-hand side as Model 4, estimated as a linear probability model — i.e. the same `WLS` estimator applied to a 0/1 outcome, not a new estimator.

## 10. Identification Strategy and Its Limits

Access to improved WASH infrastructure is not randomly assigned: it correlates with wealth, education, and geography, all of which independently affect child nutrition. The implemented design addresses part of this through the control variables in §7.3 and the administrative-region fixed effect in §11, which absorbs time-invariant differences across administrative regions within each country (infrastructure, geography, and other regional characteristics common to all clusters in the same region).

This is **not** a causal identification strategy. There is no instrument, no exogenous source of variation in WASH coverage, no panel structure to exploit, and no claim that remaining variation in cluster-level WASH coverage is uncorrelated with unobserved determinants of child nutrition. The design is cross-sectional (one DHS round per country), so it cannot separate a region fixed effect from any other time-invariant regional characteristic, and it cannot rule out reverse causality or omitted time-varying confounders. Every coefficient this pipeline produces is reported, and must be interpreted, as an association net of the included controls and region fixed effects — not as an estimate of a causal effect.

The original plan (Part II, §10) described a quasi-experimental panel design using within-spatial-unit variation over survey years; that design was not implemented, because a genuine multi-round panel was not available with one DHS round per country (see §11 for how the fixed-effects choice was adapted accordingly).

## 11. Fixed Effects

| Fixed effect | Included in | Absorbs |
|---|---|---|
| Country-qualified administrative region (`country_admin_region`) | Model 4 (and every robustness family that uses the Model 4 specification) | Time-invariant differences across administrative regions within each country (Ethiopia: 14 regions; Ghana: 16 regions; Kenya: 47 counties; Nigeria: 37 states/FCT) |

No spatial-grid fixed effect, no survey-year fixed effect, and no country×survey-year fixed effect is used anywhere in the implemented pipeline. The administrative-region fixed effect was chosen specifically because a genuine multi-round panel structure — which the original plan's spatial-grid and country×year fixed effects were designed for — is not available with a single DHS round per country; the region fixed effect instead absorbs cross-sectional differences between administrative regions within each country. This fixed effect is estimated via explicit categorical dummy encoding, not `linearmodels.PanelOLS` (see §9).

## 12. Robustness Checks

Implemented in `scripts/dhs_harmonization/12_robustness.py`, reusing Model 4's design-matrix, weighting, and clustering logic from Step 11 rather than duplicating it. Six independent families, each written to its own output file:

1. **Binary outcome LPM** — `stunted`/`wasted`/`underweight` in place of the continuous outcomes, Model 4 specification, pooled and all four countries separately.
2. **Severe outcomes** — `severe_stunted`/`severe_wasted`/`severe_underweight`, Model 4 specification, pooled only (§7.1 explains why country-specific severe models were not run).
3. **Ghana sanitation-classification sensitivity** — re-estimates Model 4 with the robustness sanitation variant (Ghana bio-digester code reclassified as improved) in place of the core variant; pooled and Ghana-only, since the two sanitation variants are identical outside Ghana by construction.
4. **Household-level WASH baseline** — replaces the two cluster-level leave-one-out exposures with simple household-level binary water/sanitation indicators, without the administrative-region fixed effect.
5. **Alternative pooled weighting** — re-estimates the pooled Model 4 under three weighting schemes: the equal-total-country weight used in the main results, the raw DHS weight with no rescaling, and no weight at all. This comparison shows that at least one exposure-outcome coefficient's sign is sensitive to the weighting scheme used; this sensitivity is reported, not resolved, and must be discussed rather than treated as settled by the main specification alone.
6. **Leave-one-out denominator sensitivity** — re-estimates the pooled Model 4 restricting the sample to clusters with at least 5 or at least 10 other eligible households behind each leave-one-out rate, in addition to the unrestricted sample used in the main results.

The original plan's country-by-country estimation, alternative fixed-effects specification, and weighted-vs-unweighted comparison (Part II, §12) are reflected here, though not in identical form: country-specific estimation is part of the main Model 1–4 results (§9) rather than a separate robustness family, and the alternative-weighting and alternative-fixed-effects comparisons take the specific forms described above rather than the region×year alternative originally planned.

## 13. Heterogeneity Analyses

**Not implemented.** The original plan (Part II, §13) described three separate interaction models testing whether the water/sanitation association differs by rural residence, household poverty, or maternal education. No heterogeneity or interaction model was estimated in the frozen pipeline; no output file in this repository reports one. This remains a documented direction for future work, not a result that exists in this repository.

## 14. Data Pipeline: Raw Data to Final Regression

The actual pipeline is `scripts/dhs_harmonization/00_config.py` through `13_final_outputs.py`, run in that numeric order. A full stage-by-stage description — purpose, inputs, outputs, and which methodological decision is implemented where — is maintained in `docs/code_guide.md` and the pipeline table in `README.md`, rather than restated here. In summary: Steps 00–01 are configuration/mapping definitions; Steps 02–10 build the pooled, harmonized analytical dataset (anthropometric outcomes, WASH categories, controls, the leave-one-out cluster exposure, the administrative-region identifier, and birth order); Step 11 estimates the main regressions (§9); Step 12 runs the robustness families (§12); Step 13 reformats the already-validated Step 07/11/12 results into the final tables and figures listed in §15 — it computes no new statistic.

The original plan's 16-stage pipeline (Part II, §14), including a fixed spatial grid, geospatial raster extraction, and a separate heterogeneity-modeling stage, was not implemented as described there.

## 15. Final Outputs

**Tables** (`outputs/final_tables/`): sample characteristics by country (Table 1); anthropometric prevalence by country (Table 2); WASH characteristics by country (Table 3); the pooled Model 1–4 results for HAZ/WAZ/WHZ (Table 4); the preferred Model 4 results by country (Table 5); the binary LPM robustness results (Table 6).

**Appendix tables** (`outputs/final_appendix/`): severe-outcome results (A1); the Ghana sanitation-classification comparison (A2); the household-level WASH baseline (A3); the alternative-pooled-weighting comparison (A4); the leave-one-out denominator sensitivity (A5); the full binary LPM coefficient table (A6); a missingness/availability summary (A7); administrative-region and leave-one-out support diagnostics (A8).

**Figures** (`outputs/final_figures/`): anthropometric prevalence by country (Figure 1); a Model 4 coefficient forest plot (Figure 2); WASH characteristics by country (Figure 3); a descriptive map of surveyed DHS cluster locations (using DHS's own displaced coordinates, not exact locations); and, in the appendix, a binary LPM coefficient forest plot.

No maps of coverage rates or outcome means by country/cluster were produced (the original plan, Part II §15, described several such maps); the one map produced is a descriptive survey-coverage map, not a coverage-rate or outcome map.

---

# PART II — ORIGINAL PRE-IMPLEMENTATION PLAN (HISTORICAL — NOT IMPLEMENTED AS SUCH)

This part reproduces the design as it stood before implementation began. It is preserved for project history. **It does not describe the analysis behind any result in this repository** — see Part I for that. Where Part I's sections above are numbered the same as sections here, Part I is the authoritative, current description; the corresponding section below is the superseded original.

## 7.3 (original) Control Variables

**Household/child-level (`X_ickt`):**
- Child age (months)
- Child sex
- Birth order
- Mother's age
- Mother's education
- Household wealth quintile
- Household size
- Urban/rural residence

Maternal literacy was not listed here; see Part I §7.3 for how and when it entered the implementation.

**Geospatial controls (not implemented):**
- Rainfall
- Temperature
- Elevation
- Population density

## 9 (original) Econometric Models

### 9.1 Baseline Model

$$
Nutrition_{ickt} = \beta_0 + \beta_1 Sanitation_{ickt} + \beta_2 Water_{ickt} + X'_{ickt}\gamma + \varepsilon_{ickt}
$$

Household-level treatment variables, no fixed effects. Included as a transparent baseline; expected to suffer from omitted variable bias, as noted in the original proposal. (In the implemented pipeline, the closest counterpart is the household-level WASH baseline robustness family, §12 family 4 in Part I — but that family reuses the Model 4 control set, not this simpler baseline specification.)

### 9.2 Preferred Fixed-Effects Model

$$
Nutrition_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

Cluster-level (leave-one-out) treatment variables, spatial grid fixed effects (α_c), and country×survey-year fixed effects (θ_kt). This was the primary planned specification for hypothesis testing. **Not implemented as such** — see Part I §9 and §11 for the fixed effect actually used (administrative-region, not spatial grid; no survey-year dimension, since the implemented design is cross-sectional).

### 9.3 Robustness: Linear Probability Model

$$
Y_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

where `Y_ickt ∈ {Stunted, Underweight, Wasted}`. Implemented in spirit (Part I §12, family 1), using the Model 4 administrative-region fixed effect in place of α_c/θ_kt.

### 9.4 Heterogeneity Models (not implemented)

$$
Nutrition_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 (SanitationRate_{ckt} \times M_{ickt}) + \beta_3 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

planned for each moderator `M ∈ {Rural, Poor, LowMaternalEducation}`. See Part I §13.

## 10 (original) Identification Strategy

The identification strategy as originally planned relied on **within-spatial-unit variation in water and sanitation coverage across survey years**, net of spatial fixed effects (α_c, absorbing permanent local characteristics) and country×survey-year fixed effects (θ_kt, absorbing national shocks specific to a country-year). α_c was planned to be defined on a fixed spatial grid rather than raw DHS cluster IDs, because DHS clusters are typically redrawn each survey round. This approach was explicitly planned as quasi-experimental, not causal in the randomized-experiment sense, even before implementation. See Part I §10 for what was actually implemented and why the panel structure this section describes was not available.

## 11 (original) Fixed Effects

| Fixed effect | Symbol | Absorbs |
|---|---|---|
| Spatial grid cell | α_c | Time-invariant local geography, culture, long-run poverty, persistent infrastructure |
| Country × survey year | θ_kt | Country-specific macro shocks, epidemics, national programs in a given year |
| Region × survey year (robustness alternative) | — | Coarser version of θ_kt combined with sub-national region, planned as an alternative specification |

Planned estimator: `linearmodels.PanelOLS` with multi-way fixed effects. **Not implemented** — see Part I §9/§11.

## 12 (original) Robustness Checks

1. Binary outcome LPM.
2. Country-by-country estimation.
3. Alternative fixed effects — region×survey-year in place of grid×country-year.
4. Weighted vs. unweighted comparison.
5. Standard error clustering at the DHS PSU/cluster level in all models.

See Part I §12 for the six robustness families actually implemented, which overlap with but are not identical to this list.

## 13 (original) Heterogeneity Analyses

Three separate interaction models, each testing one moderator at a time: rural residence, household poverty (bottom two DHS wealth quintiles), and maternal education (`SanitationRate × LowMaternalEducation`, where `LowMaternalEducation` = no education or primary only). **Not implemented** — see Part I §13.

## 14 (original) Data Pipeline: Raw Data to Final Regression

| Stage | Description | Key output |
|---|---|---|
| 0 | Lock configuration parameters and shared helper functions | `config/params.py`, `scripts/helpers/` |
| 1 | Inventory downloaded DHS/GIS raw files | `data/raw/MANIFEST.yaml` |
| 2 | Clean KR/HR: age restriction, anthropometric flag drop, JMP water/sanitation recode | `data/interim/*_clean.parquet` |
| 3 | Construct outcomes, controls, wealth quintiles, poverty/education flags | `data/interim/*_child_level.parquet` |
| 4 | Build fixed spatial grid; construct DHS displacement buffers; assign clusters to grid cells | `data/interim/spatial_grid.gpkg`, `cluster_to_grid.parquet` |
| 5 | Extract rainfall, temperature, elevation, population density via buffer zonal statistics | `data/interim/cluster_geo_covariates.parquet` |
| 6 | Construct leave-one-out `SanitationRate`/`WaterRate` | `data/interim/coverage_rates.parquet` |
| 7 | Merge all components into final dataset; normalize sampling weights | `data/final/analysis_dataset.parquet` |
| 8 | Descriptive statistics and data validation report | `outputs/tables/summary_statistics.*` |
| 9 | Baseline model | `outputs/regressions/baseline_*` |
| 10 | Preferred fixed-effects model | `outputs/regressions/preferred_*` |
| 11 | LPM robustness | `outputs/regressions/lpm_*` |
| 12 | Country-by-country, alternative FE, unweighted comparison | `outputs/regressions/robustness_*` |
| 13 | Heterogeneity models (rural, poverty, maternal education) | `outputs/regressions/het_*` |
| 14 | Maps of coverage and outcomes | `outputs/maps/*` |
| 15 | Final formatted tables | `outputs/tables/*`, copied into `thesis/tables/` |

This stage list and its script/folder names (`scripts/helpers/`, `scripts/01_cleaning/`-equivalent stages, `data/final/`) were superseded by the actual `scripts/dhs_harmonization/00`–`13` pipeline; see Part I §14 and `README.md`'s "Legacy Folders" section.

## 15 (original) Expected Outputs

**Tables:** summary statistics (weighted and unweighted), baseline model results, preferred fixed-effects model results, LPM robustness results, country-by-country estimates, alternative fixed-effects specification (region×year), weighted vs. unweighted comparison, heterogeneity results (one table per moderator).

**Figures/Maps:** cluster/grid-level maps of sanitation coverage rate, water coverage rate, and mean HAZ, each by country; coefficient plots comparing baseline vs. preferred vs. robustness specifications.

See Part I §15 for what was actually produced.
