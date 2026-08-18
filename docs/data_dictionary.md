# Data Dictionary

Companion reference to `docs/thesis_design.md`. Documents every raw source variable and every derived/constructed variable used in the pipeline, with units, missing-value handling, and transformations.

**Important caveat:** the DHS variable codes below reflect The DHS Program's *Standard Recode* naming conventions, which are stable across most Standard DHS surveys but can vary slightly by phase, round, or country (e.g., a country-specific water/sanitation category such as "sachet water" in Nigeria/Ghana). Once actual files are downloaded, every entry below must be verified against that specific round's recode manual in `docs/dhs_documentation/recode_manuals/` before use in `scripts/01_cleaning/`. Nothing here has been confirmed against a real file yet.

---

## 1. DHS Children's Recode (KR) — Raw Variables

Source file: `data/raw/DHS/<country>/children_recode/`. Unit of observation: child.

| Variable | Description | Type / Units | Valid range | Missing value handling | Transformation | 
|---|---|---|---|---|---|
| `caseid` | Unique case identifier | String | — | Should never be missing | Used as merge key with mother's line number |
| `v001` | Cluster number (PSU) | Integer | 1–N clusters | Never missing | Merge key to HR (`hv001`) and GE (`DHSCLUST`) |
| `v002` | Household number | Integer | 1–N per cluster | Never missing | Merge key to HR (`hv002`) |
| `v003` | Respondent's (mother's) line number | Integer | 1–N per household | Never missing | Merge key to HR member-level data if needed |
| `b4` | Child's sex | Categorical: 1=male, 2=female | {1,2} | Not expected missing | Recode to `sex` (1=male, 0=female) |
| `b19` | Child's current age in months (computed) | Integer, months | 0–59 (post-restriction) | Rarely missing; drop if missing | Used for the 0–59 month sample restriction |
| `bord` | Birth order number | Integer | 1+ | Missing coded per DHS convention (98/99) | Drop/flag if missing code present |
| `hw1` | Child's age in months (anthropometry) | Integer, months | 0–59 | Should match `b19`; discrepancies flagged | Cross-check against `b19` |
| `hw70` | Height-for-age standard deviation (HAZ) | Integer, z-score ×100 | −600 to 600 valid; 9998=flagged; 9999=missing | 9998 and 9999 dropped per official DHS/WHO flag convention | Divide by 100 → `haz` |
| `hw71` | Weight-for-age standard deviation (WAZ) | Integer, z-score ×100 | −600 to 600 valid; 9998=flagged; 9999=missing | 9998 and 9999 dropped | Divide by 100 → `waz` |
| `hw72` | Weight-for-height standard deviation (WHZ) | Integer, z-score ×100 | −500 to 500 valid; 9998=flagged; 9999=missing | 9998 and 9999 dropped | Divide by 100 → `whz` |
| `v012` | Mother's current age | Integer, years | 15–49 | Not expected missing | Used as control `mother_age` |
| `v106` | Mother's highest education level | Categorical: 0=no education, 1=primary, 2=secondary, 3=higher | {0,1,2,3} | Not expected missing | Used as control `mother_education`; also collapsed into `low_maternal_education` flag (Section 5) |
| `v155` | Mother's literacy (directly-administered reading test, distinct from `v106` schooling attainment) — added to the implementation post-dating the original version of this table; see the implementation note in `docs/thesis_design.md` Section 7.3 | Categorical: 0=cannot read at all, 1=able to read only parts of sentence, 2=able to read whole sentence, 3=no card with required language, 4=blind/visually impaired | {0,1,2,3,4} | Not expected missing | Used as control `literacy`, retained as the full five-category variable (no binary collapse); reference category in regressions = "Cannot read at all". Kept as a separate control from `mother_education`, not a substitute for it. |
| `v005` | Women's individual sample weight | Integer, weight ×1,000,000 | Positive integer | Never missing | Divide by 1,000,000 → `child_weight`; input to Section 5 weight normalization |

---

## 2. DHS Household Recode (HR) — Raw Variables

Source file: `data/raw/DHS/<country>/household_recode/`. Unit of observation: household.

| Variable | Description | Type / Units | Valid range | Missing value handling | Transformation |
|---|---|---|---|---|---|
| `hv001` | Cluster number (PSU) | Integer | 1–N clusters | Never missing | Merge key to KR (`v001`) and GE (`DHSCLUST`) |
| `hv002` | Household number | Integer | 1–N per cluster | Never missing | Merge key to KR (`v002`) |
| `hv009` | Number of household members | Integer | 1+ | Not expected missing | Control `household_size` |
| `hv025` | Type of place of residence | Categorical: 1=urban, 2=rural | {1,2} | Not expected missing | Recode to `rural` (1=rural, 0=urban) |
| `hv201` | Source of drinking water | Categorical, DHS standard water-source codes (see below) | Country-specific code list | "Other"/missing codes (99) treated as missing, not imputed | Recoded to `water` (improved/unimproved) per JMP classification |
| `hv205` | Type of toilet facility | Categorical, DHS standard sanitation codes (see below) | Country-specific code list | "Other"/missing codes (99) treated as missing, not imputed | Recoded to `sanitation` (improved/unimproved) per JMP classification |
| `hv270` | Wealth index combined, categorical | Categorical: 1=poorest, 2=poorer, 3=middle, 4=richer, 5=richest | {1..5} | Never missing (DHS-constructed) | Used directly as `wealth_quintile`; bottom two categories → `poor` flag |
| `hv271` | Wealth index factor score combined | Integer, factor score ×100000 | Continuous | Never missing | Not used directly (raw index excluded per locked decision favoring quintiles) — retained only for diagnostic/validation use |
| `hv007` | Year of interview | Integer, year | Survey-specific | Never missing | Used to construct `survey_year` |
| `hv005` | Household sample weight | Integer, weight ×1,000,000 | Positive integer | Never missing | Divide by 1,000,000; cross-check consistency with KR `v005` |

**Typical `hv201` (water source) coding used for the improved/unimproved recode** (verify exact codes against the round's recode manual):
- *Improved:* piped into dwelling/yard/plot, public tap/standpipe, tube well/borehole, protected dug well, protected spring, rainwater, bottled water (with an improved secondary source).
- *Unimproved:* unprotected dug well, unprotected spring, cart with small tank/drum, tanker truck, surface water (river/dam/lake/pond/stream/canal/irrigation channel).

**Typical `hv205` (toilet facility) coding used for the improved/unimproved recode:**
- *Improved:* flush/pour-flush to piped sewer, septic tank, or pit; ventilated improved pit (VIP) latrine; pit latrine with slab; composting toilet.
- *Unimproved:* flush/pour-flush to elsewhere; pit latrine without slab/open pit; bucket toilet; hanging toilet/hanging latrine; no facility (open defecation/bush/field).

---

## 3. DHS GPS Recode (GE) — Raw Variables

Source file: `data/raw/DHS/<country>/gps/`. Unit of observation: cluster.

| Variable | Description | Type / Units | Valid range | Missing value handling | Transformation |
|---|---|---|---|---|---|
| `DHSCLUST` | Cluster number | Integer | 1–N clusters | Never missing | Merge key to KR (`v001`) / HR (`hv001`) |
| `LATNUM` | Displaced cluster latitude | Float, decimal degrees | Approx. −35 to 15 (SSA extent) | `0.000000`/`0` indicates missing/unlocated cluster — excluded, not treated as equator coordinates | Used to build DHS displacement buffer (Stage 4) |
| `LONGNUM` | Displaced cluster longitude | Float, decimal degrees | Approx. −20 to 50 (SSA extent) | Same as `LATNUM` — `0.000000` excluded | Used to build DHS displacement buffer (Stage 4) |
| `URBAN_RURA` | Urban/rural classification of cluster | Categorical: U/R | {U,R} | Not expected missing | Determines displacement buffer radius: 2km if urban, 5km if rural (10km for the ~1% of rural clusters DHS displaces further) |
| `ADM1NAME` / `ADM1FIPS` | First-level administrative unit name/code | String/code | Country-specific | May be absent in some rounds | Used only if region×year alternative fixed effects (Section 12 robustness) require a region identifier |

---

## 4. GIS Raster Variables

Source: `data/raw/{rainfall, temperature, elevation, population_density}/`. Unit of observation: raster cell, aggregated to cluster buffer via zonal statistics (Stage 5).

| Variable | Description | Expected units | Temporal resolution | Missing value handling | Transformation |
|---|---|---|---|---|---|
| `rainfall` | Precipitation | mm (per month or per year, depending on source product) | Time-varying — must be matched to each cluster's survey year | No-data pixels within a buffer excluded from the zonal mean; a cluster with zero valid pixels flagged, not silently imputed | Zonal mean within DHS displacement buffer → `rainfall_ckt` |
| `temperature` | Air temperature | °C (or source-native units, e.g., ×10 °C for some products — confirm at extraction) | Time-varying — matched to survey year | Same as rainfall | Zonal mean within buffer → `temperature_ckt` |
| `elevation` | Elevation above sea level | Meters | Static (does not vary by survey year) | No-data (e.g., ocean pixels) not expected inland; flagged if encountered | Zonal mean within buffer → `elevation_c` |
| `population_density` | Population per unit area | Persons per km² | Depends on source vintage — matched to nearest available year to the survey | Zero-population pixels are valid data (not missing); no-data pixels excluded from the mean | Zonal mean within buffer → `population_density_ckt` |

**Note on units:** the exact unit/scaling of each raster (e.g., whether temperature is stored in °C or ×10 °C, whether rainfall is a monthly or annual total) depends on the specific product chosen (e.g., CHIRPS for rainfall, WorldClim/ERA5/CHIRTS for temperature, SRTM for elevation, WorldPop/GPWv4 for population density) — none has been selected/downloaded yet. This table will be updated with the confirmed unit and native resolution once a specific source is chosen for each layer.

---

## 5. Derived / Constructed Variables (Final Analysis Dataset)

These do not come directly from a single raw file — they are built during `scripts/02_variables/` and `scripts/03_merge/` per `docs/thesis_design.md` Section 8.

| Variable | Description | Type / Units | Constructed from | Missing value handling |
|---|---|---|---|---|
| `haz`, `waz`, `whz` | Rescaled anthropometric z-scores | Float, SD units | `hw70`/`hw71`/`hw72` ÷ 100 | Rows with source flag 9998/9999 already dropped upstream |
| `stunted`, `underweight`, `wasted` | Binary malnutrition indicators | {0,1} | `1[haz < −2]`, `1[waz < −2]`, `1[whz < −2]` | Inherits missingness from source z-score |
| `sanitation`, `water` | Household-level improved access | {0,1} | `hv205`, `hv201` recoded per JMP definitions | Households with "other"/missing source codes excluded from both numerator and denominator of coverage rates |
| `sanitation_rate_loo`, `water_rate_loo` | Cluster-level leave-one-out coverage rate | Float, [0,1] | Leave-one-out mean of `sanitation`/`water` within `v001`/`hv001`, per survey round | Undefined (null) for clusters where all other households have missing WASH data; flagged, not imputed |
| `wealth_quintile` | Household wealth quintile | Categorical {1..5} | `hv270` directly | Never missing (DHS-constructed) |
| `poor` | Poverty flag | {0,1} | `1[wealth_quintile ∈ {1,2}]` | Inherits `hv270` (never missing) |
| `mother_education` | Mother's education level | Categorical {0,1,2,3} | `v106` directly | Not expected missing |
| `low_maternal_education` | Low maternal education flag | {0,1} | `1[v106 ∈ {0,1}]` (no education or primary only) | Inherits `v106` |
| `literacy` | Mother's literacy — added post-implementation (see `docs/thesis_design.md` Section 7.3 implementation note); a separate, independent control from `mother_education` | Categorical {0,1,2,3,4} | `v155` directly, full five-category variable, no binary collapse | Not expected missing; reference category in regressions = "Cannot read at all" |
| `rural` | Urban/rural residence | {0,1} | `hv025` recoded (1=rural, 0=urban) | Not expected missing |
| `child_age_months` | Child's age in months | Integer | `b19` | Sample restricted to 0–59; missing dropped |
| `child_sex` | Child's sex | {0,1} | `b4` recoded | Not expected missing |
| `birth_order` | Birth order | Integer | `bord` | DHS missing codes (98/99) dropped |
| `mother_age` | Mother's age | Integer, years | `v012` | Not expected missing |
| `household_size` | Number of household members | Integer | `hv009` | Not expected missing |
| `grid_id` | Fixed spatial-grid cell identifier | Categorical | Spatial join of `LATNUM`/`LONGNUM` to the fixed grid (Stage 4) | A cluster with missing/zero GPS coordinates cannot be assigned and is excluded from grid-FE models (documented as a sample restriction, not silently dropped) |
| `survey_year` | Survey year | Integer | `hv007` (cross-checked against `v007` in KR if present) | Not expected missing |
| `country` | Country identifier | Categorical | Fixed per source folder (`data/raw/DHS/<country>/`) | Not expected missing |
| `country_year` | Country × survey-year fixed-effect group | Categorical | `country` concatenated with `survey_year` | Not expected missing |
| `rainfall_ckt`, `temperature_ckt`, `elevation_c`, `population_density_ckt` | Geospatial covariates | See Section 4 | Zonal statistics extraction (Stage 5) | See Section 4 |
| `child_weight` | Normalized sampling weight | Float | `v005` (or `hv005`) ÷ 1,000,000, renormalized across pooled countries/rounds (Stage 7) | Never missing at source; renormalization documented in `scripts/helpers/weights.py` |

---

## 6. Source File Summary

| Source file | Path pattern | Raw variables used | Derived variables produced |
|---|---|---|---|
| Children's Recode (KR) | `data/raw/DHS/<country>/children_recode/` | `caseid, v001, v002, v003, b4, b19, bord, hw1, hw70, hw71, hw72, v012, v106, v155, v005` | `haz, waz, whz, stunted, underweight, wasted, child_age_months, child_sex, birth_order, mother_age, mother_education, low_maternal_education, literacy, child_weight` |
| Household Recode (HR) | `data/raw/DHS/<country>/household_recode/` | `hv001, hv002, hv009, hv025, hv201, hv205, hv270, hv271, hv007, hv005` | `sanitation, water, sanitation_rate_loo, water_rate_loo, wealth_quintile, poor, household_size, rural, survey_year` |
| GPS Recode (GE) | `data/raw/DHS/<country>/gps/` | `DHSCLUST, LATNUM, LONGNUM, URBAN_RURA, ADM1NAME/ADM1FIPS` | `grid_id` |
| Rainfall raster | `data/raw/rainfall/` | Raster band values | `rainfall_ckt` |
| Temperature raster | `data/raw/temperature/` | Raster band values | `temperature_ckt` |
| Elevation raster | `data/raw/elevation/` | Raster band values | `elevation_c` |
| Population density raster | `data/raw/population_density/` | Raster band values | `population_density_ckt` |

---

*This dictionary must be reconciled against each downloaded round's actual recode manual before `scripts/01_cleaning/` is implemented — country/round-specific variable code differences (especially `hv201`/`hv205` category lists) are common and must be verified, not assumed.*
