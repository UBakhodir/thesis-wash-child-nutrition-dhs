# Data Dictionary

Companion reference to `docs/thesis_design.md`. Documents every raw DHS source variable and every derived/constructed variable actually used by the frozen pipeline (`scripts/dhs_harmonization/00_config.py` through `13_final_outputs.py`), reconciled directly against the scripts themselves.

**DHS variable-code caveat:** the DHS variable codes below reflect The DHS Program's *Standard Recode* naming conventions for the four survey rounds actually used (Ethiopia 2024-25, Ghana 2022, Kenya 2022, Nigeria 2024). Country-specific category lists for `v113`/`hv201` (water source) and `v116`/`hv205` (sanitation) do vary — e.g. Ghana's DHS sanitation code 16 is a locally-used bio-digester category with no direct JMP equivalent, handled explicitly in `01_wash_mapping.py` (see the `sanitation_rate_loo_core` vs. `sanitation_rate_loo_robustness_biodigester` entries in Section 5). Every mapping below has been verified against the pipeline's own runtime validation checks, not merely assumed.

---

## 1. DHS Children's Recode (KR) — Raw Variables

Source: the raw KR `.dta` file for each country, under `data/interim/DHS/<country>/<round>/KR/` (see `scripts/dhs_harmonization/00_config.py`'s `COUNTRIES` dict for the exact paths). Unit of observation: child. Read across multiple pipeline stages — some variables are read once in Step 02, others are re-read fresh in later stages rather than carried forward, as noted below.

| Variable | Description | Read in | Used to construct |
|---|---|---|---|
| `caseid` | Unique case identifier | Step 02 | Not carried into the analytical dataset directly; superseded by `country_child_id` (Step 05) |
| `v001` | Cluster number (PSU) | Steps 02–04, 09, 10 | Merge key to HR (`hv001`) and GE (`DHSCLUST`); becomes `psu` (Step 04) |
| `v002` | Household number | Steps 02–04, 09, 10 | Merge key to HR (`hv002`); part of `country_household_id` (Step 08) |
| `v003` | Respondent's (mother's) line number | Steps 02–04, 09, 10 | Merge key component only |
| `bidx` | Birth index (child's position among mother's births) | Steps 02–04, 09, 10 | Merge key component only |
| `b4` | Child's sex | Step 04 | `child_sex` (Male/Female) |
| `b19` | Child's current age in months (computed) | Step 04 | `b19_raw`, used as a continuous control from Model 2 |
| `bord` | Birth order number | Step 10 | `birth_order_raw`, preserved unchanged, continuous control from Model 2 |
| `hw1` | Child's age in months (anthropometry) | Step 02; re-read and cross-checked in Step 04 | Cross-check only against `b19`; not itself a model variable |
| `hw70` | Height-for-age standard deviation (HAZ) | Step 02 | `haz` = `hw70` ÷ 100, after excluding DHS special/missing codes |
| `hw71` | Weight-for-age standard deviation (WAZ) | Step 02 | `waz` = `hw71` ÷ 100 |
| `hw72` | Weight-for-height standard deviation (WHZ) | Step 02 | `whz` = `hw72` ÷ 100 |
| `v012` | Mother's current age | Step 04 | `maternal_age`, continuous control from Model 3 |
| `v106` | Mother's highest education level (0=no education, 1=primary, 2=secondary, 3=higher) | Step 04 | `maternal_education`, categorical control from Model 3, reference "No education" |
| `v155` | Mother's literacy (directly-administered reading test; 0=cannot read at all, 1=able to read only parts of sentence, 2=able to read whole sentence, 3=no card with required language, 4=blind/visually impaired) | Step 04 | `literacy`, categorical control from Model 3, reference "Cannot read at all" — see the provenance note in `docs/thesis_design.md` §7.3 |
| `v113` | Drinking water source | Step 03 (re-read fresh, not carried from Step 02) | Household-level `water_category` (JMP-based, `01_wash_mapping.py`) |
| `v116` | Type of toilet facility | Step 03 | Household-level sanitation category (core and bio-digester-robustness variants) |
| `v160` | Shared toilet facility indicator | Step 03 | Refines the sanitation category into Basic/Limited service level |
| `v190` | Household wealth index, categorical (1=poorest…5=richest) | Step 04 | `wealth_quintile`, categorical control from Model 3, reference "Poorest" |
| `v025` | Type of place of residence | Step 04 | `residence` (Urban/Rural), categorical control from Model 3, reference "Rural" |
| `v005` | Women's individual sample weight (×1,000,000) | Step 04 | `weight_original` = `v005` ÷ 1,000,000 |
| `v021` | Primary sampling unit | Step 04 | `psu` (used for country-specific-model standard-error clustering) |
| `v022` | Sample stratification variable | Step 04 (read only to re-verify identity with `v023`) | Not itself used as the strata variable — see `v023` |
| `v023` | Sample stratification variable (alternate) | Step 04 | `strata`, used uniformly across all four countries in place of `v022` (the two are verified numerically identical in every row; `v023` was chosen because Ethiopia's bundled metadata attaches value labels only to `v023`) |
| `v007` | Year of interview | Step 04 | `interview_year` |

Note: earlier project documentation described the household-level water/sanitation source variables as `hv201`/`hv205` only. Household-level classification is actually built twice, from two different files, for two different purposes: `v113`/`v116`/`v160` (KR, this table) build the household-level WASH categories used in the Step 12 household-baseline robustness family; `hv201`/`hv205`/`hv225` (HR, Section 2) independently build the same categories for the cluster-level leave-one-out exposure. The mapping dictionaries in `01_wash_mapping.py` are identical either way.

---

## 2. DHS Household Recode (HR) — Raw Variables

Source: the raw HR `.dta` file for each country, under `data/interim/DHS/<country>/<round>/HR/`. Unit of observation: household. Read only in Step 08, for the leave-one-out cluster WASH exposure construction — this is the DHS household census, not deduplicated to households with children.

| Variable | Description | Used to construct |
|---|---|---|
| `hv001` | Cluster number (PSU) | `cluster_key` (leave-one-out grouping unit) |
| `hv002` | Household number | Part of `country_household_id`, the join key back to the child-level dataset |
| `hv009` | Number of household members | `household_size_raw`, continuous control from Model 3 |
| `hv005` | Household sample weight (×1,000,000) | Read and preserved, but **not used** — the leave-one-out exposure rate is an unweighted household proportion by design; `hv005` is retained only for a possible future weighted-robustness variant, not built in this pipeline |
| `hv201` | Source of drinking water | Household-level water category (same JMP mapping as `v113`), input to `water_rate_loo` |
| `hv205` | Type of toilet facility | Household-level sanitation category (core and bio-digester-robustness variants), input to `sanitation_rate_loo_core` / `sanitation_rate_loo_robustness_biodigester` |
| `hv225` | Shared toilet facility indicator | Refines the sanitation category into Basic/Limited service level (same role as `v160` in Section 1) |

**Not used anywhere in the pipeline:** `hv025` (residence is built from KR's `v025` instead — Section 1), `hv270`/`hv271` (wealth is built from KR's `v190` instead — Section 1), `hv007` (interview year is built from KR's `v007` instead — Section 1). These variables exist in the raw HR files but are not read by any script in this pipeline; they are listed here only to correct an earlier version of this dictionary, which had incorrectly attributed `wealth_quintile`, `residence`, and `interview_year` to HR variables.

**`hv201`/`hv205` coding**, per `01_wash_mapping.py` (verify exact codes against the round's own recode manual if extending to a new survey):
- *Improved water:* piped into dwelling/yard/plot/neighbor, public tap/standpipe, tube well/borehole, protected dug well, protected spring, rainwater, and several country-specific delivered-water categories.
- *Unimproved water:* unprotected dug well, unprotected spring, cart with tank/drum, tanker truck; surface water (river/dam/lake/pond/stream/canal) is tracked as its own explicit category, not merged with "unimproved."
- *Improved sanitation (core):* flush/pour-flush to piped sewer, septic tank, or pit; ventilated improved pit (VIP) latrine; pit latrine with slab; composting toilet. Ghana's sanitation code 16 (a locally-used bio-digester category) is left explicitly unclassified in the core mapping, because no authoritative JMP category for it was identified; a separate robustness mapping reclassifies it as improved (see Section 5).
- *Unimproved sanitation:* pit latrine without slab/open pit, bucket toilet, hanging toilet, no facility/open defecation.
- Codes 96/97 (and their sanitation/water-specific equivalents) map to explicit `"Unknown"`/`"StructuralNotApplicable"` categories, not to missing — these households are excluded from the numerator and denominator of the leave-one-out rate, but are not silently dropped from the dataset.

---

## 3. DHS GE (Geographic) Recode — Raw Variables

Source: the GE shapefile for each country, under `data/interim/DHS/<country>/<round>/GE/`. Unit of observation: cluster. Read only in Step 06.

| Variable | Description | Used to construct |
|---|---|---|
| `DHSCLUST` | Cluster number | Merge key to KR (`v001`) / HR (`hv001`), via a country-qualified key |
| `DHSID`, `DHSYEAR`, `DHSREGNA`, `DHSREGCO` | Cluster-level survey/region metadata | Retained in the geolinked dataset for descriptive/diagnostic use; **not** the source of `country_admin_region` (see Section 5 — the administrative-region fixed effect is built in Step 09 from KR's own `v024`/`sstate1`, not from these GE fields) |
| `URBAN_RURA` | Urban/rural classification of the cluster | Cross-validated (100% agreement required) against KR-derived `residence` in Step 06; not itself used as a model variable |
| `LATNUM`, `LONGNUM` | Cluster latitude/longitude | Retained and carried through unchanged. These are DHS's official **randomly displaced** cluster coordinates (up to 2 km for urban clusters, 5 km for rural, 10 km for a random ~1% of rural clusters), not exact household locations; the pipeline does not reverse displacement, interpolate, or reproject. Used only to plot the descriptive survey-cluster coverage map (Step 13); not used to construct any exposure, control, or fixed effect. |
| `ALT_DEM`, `SOURCE` | Elevation and data-source metadata fields | Retained but not used in any constructed variable |

---

## 4. Geospatial Raster Variables — Not Implemented

An earlier version of this project's design considered extracting rainfall, temperature, elevation, and population-density raster covariates within each cluster's DHS displacement buffer. **No raster data was extracted, and no such covariate exists anywhere in the frozen pipeline or its outputs.** `rasterio` and `rasterstats` remain listed in `requirements.txt` as a leftover from this originally-considered (and not pursued) design element; no script in this pipeline imports either package. This section is retained only so a reader who encounters those package names understands what they were for.

---

## 5. Derived / Constructed Variables (Final Analysis Dataset)

Built across `scripts/dhs_harmonization/02_load_flag_anthro.py` through `10_birth_order.py`, as noted per row. All formulas below are reconciled against the actual code, not assumed.

| Variable | Built in | Type / Units | Constructed from | Missing-value handling |
|---|---|---|---|---|
| `haz`, `waz`, `whz` | Step 02 | Float, SD units | `hw70`/`hw71`/`hw72` ÷ 100 | DHS special codes 9996–9999 excluded before scaling |
| `stunted`, `wasted`, `underweight` | Step 03 | {0,1} | `1[haz < −2]`, `1[whz < −2]`, `1[waz < −2]` | Not created when the source z-score is missing |
| `severe_stunted`, `severe_wasted`, `severe_underweight` | Step 03 | {0,1} | Same construction at a −3 cutoff | Hard-validated that `severe==1` implies the corresponding standard indicator `==1` |
| `water_category`, `sanitation_category_core`, `sanitation_category_robustness_biodigester` | Step 03 (household-level, from KR `v113`/`v116`) | Categorical | JMP-based mapping, `01_wash_mapping.py` | `Unknown`/`StructuralNotApplicable` retained as explicit categories, never merged into Improved/Unimproved |
| `water_rate_loo` | Step 08 (from HR `hv201`, cluster-level) | Float, [0,1] | Leave-one-out mean of household-level improved-water status within `hv001`, excluding the index household from both numerator and denominator | Missing only if zero other eligible households remain in the cluster |
| `sanitation_rate_loo_core` | Step 08 (from HR `hv205`/`hv225`, cluster-level) | Float, [0,1] | Leave-one-out mean of household-level improved-sanitation status (core classification: Ghana bio-digester code left unclassified and excluded) | Same as above |
| `sanitation_rate_loo_robustness_biodigester` | Step 08 | Float, [0,1] | Same construction, using the robustness sanitation classification (Ghana bio-digester code reclassified as improved) | Same as above |
| `wealth_quintile` | Step 04 | Categorical {Poorest…Richest} | `v190` directly | Hard-fails the run on any unmapped/missing code |
| `maternal_education` | Step 04 | Categorical {No education, Primary, Secondary, Higher} | `v106` directly | Same |
| `literacy` | Step 04 | Categorical, 5 levels | `v155` directly, full category set retained (no binary collapse) | Same; reference category in regressions is "Cannot read at all" |
| `residence` | Step 04 | Categorical {Urban, Rural} | `v025` directly; cross-validated 100% against GE's `URBAN_RURA` in Step 06 | Same |
| `child_sex` | Step 04 | Categorical {Male, Female} | `b4` directly | Same |
| `maternal_age` | Step 04 | Float, years | `v012`, cast to float, no recoding | — |
| `b19_raw` | Step 04 | Integer, months | `b19`, preserved unchanged | — |
| `household_size_raw` | Step 08 (from HR `hv009`) | Integer | `hv009`, preserved unchanged | — |
| `birth_order_raw` | Step 10 | Integer | `bord`, preserved unchanged (no categorization, capping, or recoding) | — |
| `country_admin_region` | Step 09 | Categorical | Country name concatenated with the country's own DHS administrative-region code — `v024` for Ethiopia/Ghana/Kenya, `sstate1` for Nigeria (read fresh from KR, not from the GE file's `DHSREGNA`/`DHSREGCO`) | Ethiopia: 14 regions; Ghana: 16 regions; Kenya: 47 counties (not collapsed to DHS's 5-zone `DHSREGNA` malaria-ecology classification); Nigeria: 37 states/FCT |
| `weight_original` | Step 04 | Float | `v005` ÷ 1,000,000, the standard DHS rescaling | Used unmodified in country-specific regression models |
| Pooled model weight | Step 11 (computed in memory only, never written to any file) | Float | `weight_original` divided by its own country's total within that model's estimation sample, so every country contributes an equal total weight to the pooled regression | Not a DHS-standard procedure — see `docs/thesis_design.md` §8 |
| `psu` | Step 04 | — | `v021` directly | Clustering identifier for country-specific-model standard errors |
| `country_psu` | Step 05 | — | Country name concatenated with `psu` | Clustering identifier for pooled-model standard errors |
| `strata` | Step 04 | — | `v023` directly (used uniformly across all four countries; verified identical to `v022` in every row) | Used by Step 07's design-based descriptive statistics only |
| `country_child_id`, `country_household_id` | Steps 05, 08 | — | Country name concatenated with the relevant DHS identifiers | Merge/grouping keys; not analytical variables |
| `interview_year` | Step 04 | Integer | `v007` directly | Retained but not used as a fixed effect or control in any model |

**Not implemented:** `grid_id` (a fixed spatial-grid unit), `rainfall_ckt`/`temperature_ckt`/`elevation_c`/`population_density_ckt` (Section 4), `poor` (a binary wealth-quintile collapse), `low_maternal_education` (a binary education collapse), and `country_year` (a country×year grouping variable) do not exist anywhere in this pipeline. An earlier version of this dictionary listed all of these as derived variables; none was ever built, because the design elements that would have used them (a spatial-grid fixed effect, geospatial raster controls, and heterogeneity/interaction models) were not implemented — see `docs/thesis_design.md` Part I §13 and Part II.

---

## 6. Source File Summary

| Source file | Path pattern | Raw variables read | Derived variables produced |
|---|---|---|---|
| Children's Recode (KR) | `data/interim/DHS/<country>/<round>/KR/` | `caseid, v001, v002, v003, bidx, b4, b19, bord, hw1, hw70, hw71, hw72, v012, v106, v155, v113, v116, v160, v190, v025, v005, v021, v022, v023, v007` | `haz, waz, whz, stunted, wasted, underweight, severe_stunted, severe_wasted, severe_underweight, household-level water/sanitation categories, child_sex, b19_raw, birth_order_raw, maternal_age, maternal_education, literacy, wealth_quintile, residence, weight_original, psu, strata, interview_year, country_admin_region` |
| Household Recode (HR) | `data/interim/DHS/<country>/<round>/HR/` | `hv001, hv002, hv009, hv005, hv201, hv205, hv225` | `water_rate_loo, sanitation_rate_loo_core, sanitation_rate_loo_robustness_biodigester, household_size_raw` |
| GE (geographic) Recode | `data/interim/DHS/<country>/<round>/GE/` | `DHSCLUST, DHSID, DHSYEAR, DHSREGNA, DHSREGCO, URBAN_RURA, LATNUM, LONGNUM, ALT_DEM, SOURCE` | Descriptive map only (Step 13); cross-validation of `residence` (Step 06) |

No rainfall/temperature/elevation/population-density raster source is read anywhere in this pipeline (Section 4).

---

*This dictionary describes the raw and derived variables of the completed, frozen pipeline as implemented in `scripts/dhs_harmonization/`. It has been reconciled directly against the source code, not assumed from planning-stage documentation. `docs/thesis_design.md` documents the corresponding model specifications and the original pre-implementation plan where it differs from what was built.*
