# Master Design Document

**Thesis:** The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa: Evidence from DHS and Geospatial Data
**Author:** Bakhodir Izzatulloev — MSc Economics
**Status:** Methodology locked. Implementation pending data acquisition.
**Last updated:** 2026-08-04

This document is the single source of truth for the thesis's empirical design. It consolidates the approved research proposal and every methodological decision finalized in planning. No analysis code has been written; this document governs what will be implemented once DHS and GIS data are collected.

---

## 1. Research Question

**Main question:** Does improved access to water and sanitation improve child nutritional outcomes in Sub-Saharan Africa?

**Sub-questions:**
1. Does improved sanitation increase child height-for-age z-scores (HAZ)?
2. Does improved water access improve child nutritional outcomes?
3. Are effects stronger in rural households?
4. Do effects differ by household wealth and maternal education?

---

## 2. Objectives

**General objective:** To estimate the causal effect of improved water and sanitation access on child nutritional outcomes in Nigeria, Ghana, Kenya, and Ethiopia, using DHS microdata linked to geospatial covariates.

**Specific objectives:**
1. Quantify the association between household- and community-level sanitation access and HAZ, WAZ, and WHZ.
2. Quantify the association between household- and community-level water access and the same outcomes.
3. Test whether these associations differ between rural and urban households.
4. Test whether these associations differ by household wealth (poverty status) and maternal education level.
5. Assess the robustness of the results to alternative outcome definitions (binary stunting/underweight/wasting), alternative fixed-effects structures, and country-specific estimation.

---

## 3. Hypotheses

Derived directly from the proposal's stated expected signs (Section 4.7):

- **H1:** Improved sanitation coverage is positively associated with HAZ, WAZ, and WHZ (β₁ > 0).
- **H2:** Improved water coverage is positively associated with HAZ, WAZ, and WHZ (β₂ > 0).
- **H3 (robustness form):** Improved sanitation and water coverage are negatively associated with the probability of stunting, underweight, and wasting (β₁ < 0, β₂ < 0).
- **H4 (heterogeneity):** The magnitude of the sanitation/water effect on nutritional outcomes is larger for rural households, poorer households, and households with lower maternal education — i.e., effects are concentrated among the most vulnerable groups.

---

## 4. Conceptual Framework

The theoretical channel, as stated in the proposal's introduction, runs:

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

Two features of this channel motivate the empirical design:

- **Externalities:** because sanitation reduces environmental contamination beyond the household that installs it, a child's nutritional status may depend not only on their own household's facilities but on the surrounding community's coverage. This motivates constructing cluster-level coverage rates (`SanitationRate`, `WaterRate`) as the primary treatment variables, rather than relying solely on household-level access.
- **Non-random assignment:** access to improved WASH infrastructure is correlated with wealth, education, and proximity to infrastructure — all of which independently affect child nutrition. This is the central econometric problem the identification strategy (Section 10) is designed to address.

---

## 5. Data Sources

| Source | File | Content |
|---|---|---|
| DHS | Children's Recode (KR) | Child anthropometry (HAZ/WAZ/WHZ), age, sex, mother characteristics |
| DHS | Household Recode (HR) | Water source, sanitation facility, wealth index, household characteristics |
| DHS | GPS files | DHS cluster coordinates (randomly displaced for confidentiality) |
| Geospatial raster | Rainfall | Time-varying precipitation |
| Geospatial raster | Temperature | Time-varying temperature |
| Geospatial raster | Elevation | Static elevation |
| Geospatial raster | Population density | Population density surface |

**Countries:** Nigeria, Ghana, Kenya, Ethiopia.
**Survey rounds:** the specific DHS rounds used will be determined by whichever rounds are actually downloaded for each country (not fixed in advance).

---

## 6. Unit of Analysis

The unit of analysis is the **child**. The dataset is a pooled repeated cross-section of children across countries and survey years, indexed as:

- `i` = child
- `c` = DHS cluster (mapped to a fixed spatial grid cell for fixed-effects purposes — see Section 11)
- `k` = country
- `t` = survey year

---

## 7. Variables

### 7.1 Dependent Variables

**Main outcomes (continuous z-scores):**
- `HAZ_ickt` — height-for-age z-score (chronic malnutrition, long-run growth)
- `WAZ_ickt` — weight-for-age z-score (overall nutritional status)
- `WHZ_ickt` — weight-for-height z-score (acute malnutrition)

**Robustness outcomes (binary, WHO cutoff of −2 SD):**
- `Stunted_ickt = 1[HAZ_ickt < −2]`
- `Underweight_ickt = 1[WAZ_ickt < −2]`
- `Wasted_ickt = 1[WHZ_ickt < −2]`

### 7.2 Independent Variables

**Household-level (used in the baseline model only):**
- `Sanitation_ickt` — binary, 1 if household has improved sanitation
- `Water_ickt` — binary, 1 if household has improved drinking water

**Cluster-level (used in the preferred model):**
- `SanitationRate_ckt` — leave-one-out share of households in cluster `c` with improved sanitation
- `WaterRate_ckt` — leave-one-out share of households in cluster `c` with improved water

### 7.3 Control Variables

**Household/child-level (`X_ickt`):**
- Child age (months)
- Child sex
- Birth order
- Mother's age
- Mother's education
- Mother's literacy (DHS `v155`) — see implementation note below
- Household wealth quintile
- Household size
- Urban/rural residence

**Geospatial controls:**
- Rainfall
- Temperature
- Elevation
- Population density

**Implementation note (added post-implementation, not part of the original locked design):**
Mother's literacy (DHS `v155`) was not listed in the original version of this
section. It entered the empirical implementation during pipeline
construction, was used consistently as a control from that point forward in
Models 3-4 and every applicable robustness specification, and the final
Steps 11-13 results reflect its inclusion. A dedicated pre-freeze provenance
investigation searched this document, `docs/data_dictionary.md`,
`docs/project_timeline.md`, `README.md`, and all pipeline script
docstrings/comments for evidence that literacy was intentionally approved
as part of the original design; no such record was found. The investigation
also found no evidence that its inclusion was an error - it is technically
valid (full-rank design matrices in every model that includes it), is a
conceptually distinct construct from mother's education (`v106` measures
schooling attainment; `v155` is a directly-administered reading-comprehension
test, and the two are not deterministically related in this sample outside
the "Higher education" category, where DHS itself does not administer the
literacy test and auto-codes literacy), and is a recognized covariate choice
in closely related published DHS child-height research (Spears 2013, one of
this project's core literature sources, uses maternal literacy as a control
in the same type of regression). Given the empirical results were already
known at the time this discrepancy was discovered, the decision was made to
retain literacy exactly as implemented and correct this documentation to
match, rather than remove the variable and re-estimate every affected model.
This note records the as-implemented final specification; it does not assert
that the original design document already contained this variable. Mother's
education and mother's literacy are retained as two separate, independent
controls, not substitutes for one another. Full provenance detail:
`outputs/final_audit/literacy_specification_decision.txt`.

Mother's literacy is represented as the full five-category DHS `v155`
variable (Cannot read at all / Able to read only parts of sentence / Able to
read whole sentence / No card with required language / Blind or visually
impaired), with "Cannot read at all" as the reference category in every
regression that includes it - it is not collapsed to binary.

---

## 8. Construction of Every Variable

| Variable | Construction rule |
|---|---|
| HAZ / WAZ / WHZ | Taken from DHS-computed anthropometric z-scores (KR), rescaled from DHS's stored ×100 integer format. |
| Stunted / Underweight / Wasted | Binary indicator, 1 if the corresponding z-score < −2, else 0. |
| Sanitation | Recoded from DHS toilet-facility-type variable per JMP definition: improved = flush toilets, ventilated improved pit (VIP) latrines, pit latrines with slabs. |
| Water | Recoded from DHS water-source variable per JMP definition: improved = piped water, protected wells, boreholes, protected springs. |
| SanitationRate / WaterRate | Leave-one-out mean of the household-level binary within the child's cluster (excludes the child's own household from the average it is matched to), computed separately per survey round. |
| Household wealth quintile | DHS-provided wealth quintile variable, used directly rather than the raw continuous wealth index, to preserve within-country-survey comparability across the four countries. |
| Poverty flag | 1 if household is in the bottom two wealth quintiles (poorest + poorer), else 0. |
| Low maternal education flag | 1 if mother's education is no education or primary only, else 0 (secondary+ is the reference). |
| Rural | DHS urban/rural residence classification, taken directly from HR. |
| Sample restriction | Children aged 0–59 months only. |
| Anthropometric data cleaning | Observations flagged as biologically implausible by the official DHS/WHO anthropometric flag variable are dropped. |
| Multiple births/siblings | Retained in the sample (not excluded); non-independence addressed via clustered standard errors, not sample restriction. |
| Grid ID (`grid_id`) | DHS cluster GPS coordinates (used within their DHS-defined confidentiality buffer — 2km urban / 5km rural / 10km for the ~1% displaced rural clusters) are spatially joined to a fixed-resolution grid; the grid resolution is calibrated empirically from the actual distribution of inter-cluster distances once real GPS data is available, rather than fixed a priori. `grid_id` is the spatial fixed-effects unit (α_c), chosen instead of raw DHS cluster ID because DHS clusters are typically redrawn each survey round and are not a temporally stable panel unit. |
| Geospatial covariates (rainfall, temperature, elevation, population density) | Extracted as zonal statistics (mean) within each cluster's DHS confidentiality buffer, matched to the cluster's survey year for time-varying layers (rainfall, temperature). |
| Sampling weights | DHS sampling weights, renormalized across pooled countries/survey rounds so no single country dominates the pooled weighted estimates. |

---

## 9. Econometric Models

### 9.1 Baseline Model

$$
Nutrition_{ickt} = \beta_0 + \beta_1 Sanitation_{ickt} + \beta_2 Water_{ickt} + X'_{ickt}\gamma + \varepsilon_{ickt}
$$

where `Nutrition_ickt ∈ {HAZ, WAZ, WHZ}`. Household-level treatment variables, no fixed effects. Included as a transparent baseline; expected to suffer from omitted variable bias, as noted in the proposal.

### 9.2 Preferred Fixed-Effects Model

$$
Nutrition_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

Cluster-level (leave-one-out) treatment variables, spatial grid fixed effects (α_c), and country×survey-year fixed effects (θ_kt). This is the primary specification for hypothesis testing (expected: β₁ > 0, β₂ > 0).

### 9.3 Robustness: Linear Probability Model

$$
Y_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

where `Y_ickt ∈ {Stunted, Underweight, Wasted}` (expected: β₁ < 0, β₂ < 0).

### 9.4 Heterogeneity Models (estimated separately)

$$
Nutrition_{ickt} = \beta_1 SanitationRate_{ckt} + \beta_2 (SanitationRate_{ckt} \times M_{ickt}) + \beta_3 WaterRate_{ckt} + X'_{ickt}\gamma + \alpha_c + \theta_{kt} + \varepsilon_{ickt}
$$

estimated once for each moderator `M ∈ {Rural, Poor, LowMaternalEducation}`, as three separate models (not one combined triple-interaction model).

---

## 10. Identification Strategy

The core econometric problem is endogeneity: access to improved WASH is not randomly assigned — it correlates with wealth, education, and proximity to infrastructure, all of which independently affect child nutrition.

The identification strategy relies on **within-spatial-unit variation in water and sanitation coverage across survey years**, net of:
- **Spatial fixed effects (α_c):** absorb permanent local characteristics — geography, culture, long-run poverty, persistent infrastructure differences.
- **Country×survey-year fixed effects (θ_kt):** absorb macroeconomic shocks, epidemics, and national development programs specific to a country in a given year.

**Design refinement locked during planning:** α_c is defined on a **fixed spatial grid**, not raw DHS cluster IDs. DHS enumeration-area clusters are generally redrawn each survey round, so raw cluster IDs are not a stable panel unit across rounds — using them directly would leave little genuine within-unit variation over time, undermining the "across survey years" identification claim. A fixed grid gives a spatial unit whose identity is stable across rounds, so that changes in coverage within a cell between survey years are meaningfully observed.

This approach is explicitly **quasi-experimental, not a randomized design** — remaining within-cell, within-country-year variation in access is assumed (not proven) to be uncorrelated with unobserved determinants of child nutrition. This is a real assumption, not a guarantee, and is presented as such in the thesis.

---

## 11. Fixed Effects

| Fixed effect | Symbol | Absorbs |
|---|---|---|
| Spatial grid cell | α_c | Time-invariant local geography, culture, long-run poverty, persistent infrastructure |
| Country × survey year | θ_kt | Country-specific macro shocks, epidemics, national programs in a given year |
| Region × survey year (robustness alternative) | — | Coarser version of θ_kt combined with sub-national region, tested as an alternative specification |

Estimated via `linearmodels.PanelOLS` with multi-way fixed effects.

---

## 12. Robustness Checks

1. **Binary outcome LPM** — re-estimate the preferred model using Stunted/Underweight/Wasted (Section 9.3).
2. **Country-by-country estimation** — preferred model estimated separately for Nigeria, Ghana, Kenya, and Ethiopia.
3. **Alternative fixed effects** — region×survey-year in place of grid×country-year.
4. **Weighted vs. unweighted comparison** — main results use DHS sampling weights; unweighted estimates reported alongside as a robustness comparison.
5. **Standard error clustering** — standard errors clustered at the DHS primary sampling unit (PSU/cluster) level in all models (baseline, preferred, and robustness), not only as a separate check — required given that cluster-level regressors are constant within cluster by construction.

---

## 13. Heterogeneity Analyses

Three separate interaction models (Section 9.4), each testing one moderator at a time:

1. **Rural residence** — `SanitationRate × Rural`, `WaterRate` uninteracted.
2. **Household poverty** — `SanitationRate × Poor`, where `Poor` = bottom two DHS wealth quintiles.
3. **Maternal education** — `SanitationRate × LowMaternalEducation`, where `LowMaternalEducation` = no education or primary only.

Each model retains the base (uninteracted) moderator term alongside the interaction, and uses the same fixed-effects and clustering structure as the preferred model.

---

## 14. Data Pipeline: Raw Data to Final Regression

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

Full detail (objectives, inputs, scripts, dependencies, validation checks per stage) is maintained in the implementation roadmap agreed during planning.

---

## 15. Expected Outputs

**Tables:**
- Summary statistics (weighted and unweighted), by country and pooled.
- Baseline model results (HAZ/WAZ/WHZ).
- Preferred fixed-effects model results (HAZ/WAZ/WHZ).
- LPM robustness results (Stunted/Underweight/Wasted).
- Country-by-country estimates.
- Alternative fixed-effects specification (region×year).
- Weighted vs. unweighted comparison.
- Heterogeneity results (rural, poverty, maternal education), one table per moderator.

**Figures/Maps:**
- Cluster/grid-level maps of sanitation coverage rate, by country.
- Cluster/grid-level maps of water coverage rate, by country.
- Cluster/grid-level maps of mean HAZ, by country.
- Coefficient plots comparing baseline vs. preferred vs. robustness specifications.

---

*This document reflects the design as finalized in planning. Any future change to a variable definition, model specification, or fixed-effects structure should be updated here first, before any script is modified.*
