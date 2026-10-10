# Appendix A — Variable definitions, sample flow, and authoritative sources

## A.1 Variable definitions

**Baseline and historical variables are listed in separate blocks below, because the two samples are built from different source pipelines (country-specific DHS recodes for the baseline; IPUMS-DHS for the historical extension) and use different native field names for the same kind of quantity — a baseline field is never the same field as its historical counterpart under a different name, even where the two serve an analogous purpose (Section 3.4, Section 3.8).**

**Baseline (Section 3.1–3.4)**

| Variable | Definition | Source file (authoritative) |
|---|---|---|
| HAZ, WAZ, WHZ | Height-for-age, weight-for-age, weight-for-height z-scores, WHO Child Growth Standards reference [@deOnis2006] | DHS recode, flagged valid per DHS convention |
| Household water (binary) | JMP-improved household water source | `docs/empirical_strategy.md` §2 |
| Household sanitation (binary) | JMP-improved household sanitation facility | `docs/empirical_strategy.md` §2 |
| Community water/sanitation (`water_rate_loo`, `sanitation_rate_loo_core`) | Leave-one-out share of other households in the same cluster with the improved facility | `docs/empirical_strategy.md` §2 |
| `v005` → `weight_original` | The woman's individual sample weight from the DHS Children's Recode (KR) — not the distinct Births Recode (BR), which this thesis does not use — rescaled by the documented factor of 1,000,000; inherited by each of her children's birth records (DHS computes no separate per-child weight within KR) — **not** the household-level weight, `hv005`, which lives only in the Household Recode (HR) and is not used in the baseline models | `scripts/dhs_harmonization/04_build_country_kr.py` |
| `v021` → `psu` → `country_psu` | DHS's native primary sampling unit code, combined with a country prefix into a country-qualified cluster key | `scripts/dhs_harmonization/04_build_country_kr.py`, `05_pool_countries.py` |
| `b19` (child's own age in months) | DHS recode's own standard current-age-in-months field, used uniformly for all four baseline countries (no country-varying construction) | `scripts/dhs_harmonization/04_build_country_kr.py`, `11_main_regressions.py` |

**Historical extension (Section 3.5–3.8)**

| Variable | Definition | Source file (authoritative) |
|---|---|---|
| IDHSPSU | Sample-qualified DHS cluster code (unique across survey rounds), from IPUMS-DHS — **the historical extension's own cluster identifier, distinct from the baseline's `country_psu` above** | IPUMS-DHS / DHS recode |
| PERWEIGHT | DHS/IPUMS standard child-level sampling weight, from IPUMS-DHS — **the historical extension's own weight field, distinct from the baseline's `weight_original` above** | IPUMS-DHS documentation |
| W\_IMP, S\_IMP | IHME modelled annual local coverage of JMP-improved water/sanitation, 0–100, ~5×5 km, 2000–2017 | `docs/provenance/historical_wash_ihme_product_definitions_v1_2026-10-07.md` |
| `age_m` (child's own age in months) | **The historical extension's own age field, distinct from the baseline's `b19` above.** Reported completed months where delivered (Ethiopia, Nigeria); documented calendar-month difference otherwise (Ghana, Kenya) | `scripts/historical_wash/16_estimate_preliminary.py` |
| `b_year` (birth year) | Child's birth year, used for survey-qualified country-by-birth-year fixed effects in the historical models | Derived in the analysis-sample construction stage; confirmed independent of the Ethiopia interview-date candidate (Appendix C) |
| `cluster_key` | Composite key encoding survey + cluster, sample-qualified by construction | `data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet` (RESTRICTED; schema only cited here) |

## A.2 Baseline sample flow

Pooled harmonised child file (70,231 children, 4,481 clusters, 114 regions) → outcome-valid, measurement-universe-restricted samples (36,985 HAZ / 37,260 WAZ / 37,088 WHZ) → common samples requiring both household and community exposures classifiable (36,040 / 36,308 / 36,145, 4,426 clusters). Full flow: `outputs/household_community_wash/01_development_sample_flow.csv`.

## A.3 Historical sample flow (established-date, post-12-month window, water, HAZ, as a worked example)

Raw analysis candidates, established countries (60,772) → candidate == GREGORIAN_ESTABLISHED (60,772; no further loss for the three established countries) → complete postnatal window + complete spatial coverage (42,052) → HAZ valid and within measured universe (23,135) → complete-case on covariates (23,135; no further loss) → singleton-cluster exclusion (−117 clusters, −117 observations) → **final: 23,018 children, 3,114 clusters**. Reproduced independently in `scripts/historical_wash/20_validate_pooled_estimate.py`'s execution log (`data/processed/estimation/pooled_independent_validation_20261007T090003Z/execution_log.txt`, RESTRICTED).

## A.4 DHS/IPUMS official documentation sources attempted for the measurement-subsample weight (Section 3.8, Section 6.3)

| Source tried | Result |
|---|---|
| DHS-8 Biomarker Manual (dhsprogram.com PDF) | HTTP 403, tried twice across two sessions |
| Guide to DHS Statistics (dhsprogram.com) | HTTP 403 |
| World Bank microdata catalogue, child anthropometry variable page | Accessible; no weighting guidance found |
| Nigeria 2018 NDHS final report | Accessible; describes sampling weights by stage/cluster and a domestic-violence special weight, but no anthropometry/biomarker-specific weight |
| IPUMS-DHS PERWEIGHT and KIDWT documentation pages | Accessible; confirms PERWEIGHT as the documented child-level tabulation weight; KIDWT is a population factor, not used |

No source documents a measurement-subsample-specific weight. This is recorded as an unresolved documentation gap (issue register item #1), not inferred or substituted with an invented correction.

## A.5 Full authoritative-file index

See `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and `02_core_reporting_table.md` for the complete, current index of every baseline and historical output file this manuscript cites, with status labels (validated for main reporting / validated sensitivity / exploratory / invalid-superseded / not estimable).
