# Appendix A — Variable definitions, sample flow, and authoritative sources

## A.1 Variable definitions

**Baseline and historical variables are listed in separate tables, because the two samples are built by different source pipelines (country-specific DHS recode files for the baseline; IPUMS-DHS for the historical extension) and use different native field names for the same kind of quantity. A baseline field is never the same field as its historical counterpart under another name, even where the two serve an analogous purpose (Section 3.4, Section 3.8).**

The unit of analysis in both samples is the child. Scripts named in Table A.1 are in `scripts/dhs_harmonization/` and those in Table A.2 in `scripts/historical_wash/`; all paths are relative to the repository root.

**Table A.1 — Baseline variables (Sections 3.1–3.4)**

| Variable | Definition | Source file (authoritative) |
|---|---|---|
| HAZ, WAZ, WHZ | Height-for-age, weight-for-age and weight-for-height z-scores, WHO Child Growth Standards reference [@deOnis2006]. Read from the KR fields `hw70`, `hw71` and `hw72`, which store each z-score multiplied by 100; every valid value is divided by 100 once, giving the analysis scale in standard deviations. A value is valid unless it is system-missing or one of the DHS special codes 9996 (height out of plausible limits), 9997 (age in days out of plausible limits), 9998 (flagged cases) or 9999 (missing). All five non-valid states become missing, never a number. The bounds −6 to 6 (HAZ) and −6 to 5 (WAZ, WHZ) are a validation check that stops the pipeline if a valid value falls outside them; they do not reclassify any value. | DHS Children's Recode (KR); `02_load_flag_anthro.py` |
| Household water (binary) | 1 if the household drinking-water source on the child's KR record (`v113`) is JMP-improved; 0 if it is unimproved or surface water. Code 96 (other; "Unknown") and code 97 (not a de jure resident; "structurally not applicable") are set to missing, not to 0. "Improved" is a facility-type category; it is not a measure of a safe or safely managed service. | `01_wash_mapping.py`, `03_build_indicators.py`, `12_robustness.py` |
| Household sanitation (binary) | 1 if the KR sanitation facility (`v116`) is JMP-improved, including an improved facility shared with other households (the Basic and Limited service levels derived from `v160` are both counted as improved); 0 if it is unimproved or open defecation. Code 96 ("Unknown"), code 97 ("structurally not applicable"), an improved facility whose sharing code is 7 (also structurally not applicable) and Ghana's flush-to-biodigester code 16 (unclassified in the core specification) are set to missing. | `01_wash_mapping.py`, `03_build_indicators.py`, `12_robustness.py` |
| Community water/sanitation (`water_rate_loo`, `sanitation_rate_loo_core`) | Unweighted leave-one-out proportion of improved facilities among the *other* sampled, classifiable Household Recode (HR) households in the child's DHS cluster, classified from `hv201`, `hv205` and `hv225` with the same mapping as the household variables. The child's own household is excluded from both the numerator and the denominator, so all children in one household receive the same value. Households recorded as Unknown or structurally not applicable, and, in the core sanitation variant, households using Ghana's unclassified biodigester, are also excluded from both. The value lies on the 0–1 scale and is missing when no other classifiable household remains in the cluster. HR covers sampled households only, so the measure is not a census of every household in the physical community, and it is not an average over children. A robustness variant, `sanitation_rate_loo_robustness_biodigester`, counts code 16 as improved; it differs from the core variant only in Ghana. | HR; `08_hr_cluster_wash_exposure.py`, `01_wash_mapping.py` |
| `v005` → `weight_original` | The woman's individual sample weight from the DHS Children's Recode (KR), divided by the documented factor of 1,000,000. Each child's KR record carries the mother's weight, because DHS computes no separate per-child weight within KR. The distinct Births Recode (BR) is not used. This is **not** the household weight `hv005`, which exists only in the Household Recode (HR) and is not used in the baseline models. Pooled models rescale `weight_original` to equal country totals within each model's estimation sample (Section 4.5); country-specific models use it unchanged. | `04_build_country_kr.py`; pooled rescaling in `11_main_regressions.py` |
| `v021` → `psu` → `country_psu` | DHS's native primary sampling unit code, copied to `psu` and combined with a country prefix into the country-qualified cluster key `country_psu`. Pooled models use `country_psu` for cluster fixed effects and clustered standard errors; country-specific models cluster on `psu`. | `04_build_country_kr.py`, `05_pool_countries.py` |
| `b19` (child's own age in months) | The DHS recode's standard current-age-in-months field, stored unchanged as `b19_raw` and used uniformly for all four baseline countries (no country-varying construction); a linear control from Model 2 onwards. | `04_build_country_kr.py`, `11_main_regressions.py` |

::: {.tablenote}
*Note.* Baseline source files: DHS KR and HR recodes for Ethiopia 2024–25, Ghana 2022, Kenya 2022 and Nigeria 2024; the baseline does not use IPUMS-DHS. The household and community WASH constructions are also described in `docs/empirical_strategy.md` §2. The pipeline applies the same special-code list to all four countries; whether DHS's own criteria behind code 9998 are identical across these surveys is not established here. Community exposure groups HR households by the HR cluster number `hv001` and links them to children through `v001` and `v002`, whereas cluster fixed effects and clustered standard errors use `v021`. Whether these identifiers correspond one-to-one in every baseline country has not been checked against the restricted data and remains an open verification question.
:::

**Table A.2 — Historical-extension variables (Sections 3.5–3.8)**

| Variable | Definition | Source file (authoritative) |
|---|---|---|
| `IDHSPSU` | Sample-qualified DHS cluster code from IPUMS-DHS, unique across survey rounds; used for cluster fixed effects and clustered standard errors. **It is the historical extension's own cluster identifier, distinct from the baseline's `country_psu` above.** | IPUMS-DHS / DHS recode; `16_estimate_preliminary.py` |
| `PERWEIGHT` | The IPUMS-DHS standard sampling weight for child-level tabulations, rescaled to equal country totals within each model's final estimation sample (Section 4.5). **It is the historical extension's own weight field, distinct from the baseline's `weight_original` above.** It is not a documented anthropometry-specific weight (Section A.4). `KIDWT`, an IPUMS population adjustment factor, is not used. | IPUMS-DHS documentation; `16_estimate_preliminary.py` |
| W\_IMP, S\_IMP | IHME modelled annual local coverage of JMP-improved water and sanitation: percent of the population with access, on a 0–100 scale, ~5×5 km grid, 2000–2017. W\_IMP sums piped water (on- or off-premises) and other JMP-improved sources (protected wells and springs, bottled water, rainwater collection, bought water); S\_IMP sums sewer/septic sanitation and other JMP-improved facilities (improved and ventilated improved latrines, composting toilets); both verified directly from the primary source, not inferred from the raster scale or file names. Each child's value is the area average of the MEAN surface within a buffer of 2 km (urban) or 5 km (rural) around the displaced cluster coordinates; it is not population-weighted. Containing-pixel assignment and a rural 10 km buffer are sensitivity methods. | `docs/provenance/historical_wash_ihme_product_definitions_v1_2026-10-07.md`; `10_spatial_extraction_v3.py` |
| `age_m` (child's own age in months) | **The historical extension's own age field, distinct from the baseline's `b19` above.** Reported completed months (`KIDCURAGEMO`) where the source delivers them (Ethiopia, Nigeria); otherwise the documented calendar-month difference between interview and birth dates (Ghana, Kenya). | `16_estimate_preliminary.py`, `14_build_analysis_samples.py` |
| `b_year` (birth year) | The child's birth year, from the birth-date century-month code; used for survey-qualified country-by-birth-year terms in the historical models. Derived in the analysis-sample construction stage and confirmed independent of the Ethiopian interview-date candidate (Appendix C). | `14_build_analysis_samples.py` |
| `cluster_key` | A copy of `IDHSPSU` (`cluster_key = IDHSPSU`), which already encodes survey and cluster, so the key is sample-qualified by construction. | `14_build_analysis_samples.py`; stored in `data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet` (RESTRICTED; schema only cited here) |

::: {.tablenote}
*Note.* Historical source: the IPUMS-DHS child-level extract for Ghana 2014, Kenya 2014 and Nigeria 2018 (the established-date family); Ethiopia 2016 enters only as a provisional sensitivity analysis (Appendix C). Historical HAZ, WAZ and WHZ come from the IPUMS fields `HWHAZWHO`, `HWWAZWHO` and `HWWHZWHO` (stored multiplied by 100 and divided by 100 once); code 9999 marks a child outside the measurement universe, and codes 9995–9998 and system-missing values are not valid. IHME raster values are percentages; NoData pixels are excluded from the valid area rather than treated as zero. A child-year counts as complete only when the valid area covers the buffer to within 10⁻³; partial-coverage values are kept for diagnostics only. The supplied LOWER and UPPER surfaces are not regression confidence intervals and do not enter the models. Exposure windows (`12_construct_exposure_windows.py`): the birth-year window is the full calendar year of birth; the prenatal window is the nine months before the birth month (birth month excluded); the post-12- and post-24-month windows start with the birth month (included). Each calendar year is weighted by its share of the window's months, and a window needing any year outside 2000–2017 is not assigned a value. Only the two postnatal windows require every window month to have ended before the interview month; the prenatal and birth-year windows have no interview-date completion check. Because the surface is annual, a value may include months after the interview; such cases are flagged, not excluded (Section 3.7).
:::

## A.2 Baseline sample flow

Counts are unweighted numbers of children.

1. Pooled harmonised child file: 70,231 children, 4,481 clusters and 114 regions.
2. Outcome-valid samples within the measurement universe: 36,985 children for HAZ, 37,260 for WAZ and 37,088 for WHZ, in 4,434 clusters. Validity is the outcome rule in Table A.1; the code applies no separate measurement-universe filter. No child is lost at the exposure or covariate step.
3. Common samples requiring both household and community exposures to be classifiable: 36,040 (HAZ), 36,308 (WAZ) and 36,145 (WHZ) children, in 4,426 clusters and 25,627, 25,759 and 25,665 households.

The baseline code contains no singleton-cluster exclusion step (Section 4.5), so no baseline singleton count exists.

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

Full flow: `outputs/household_community_wash/01_development_sample_flow.csv` and, for the outcome-valid samples, `outputs/tables/step11_model_sample_flow.csv`.

```{=latex}
\par\endgroup
```

## A.3 Historical sample flow (established-date, post-12-month window, water, HAZ, as a worked example)

The example is the primary pooled model (Ghana 2014, Kenya 2014, Nigeria 2018; W\_IMP; primary buffer method; weighted).

1. Raw analysis candidates in the three established-date samples: 60,772 child records (Ghana 5,884; Kenya 20,964; Nigeria 33,924).
2. Candidate label `GREGORIAN_ESTABLISHED`: 60,772 (no further loss for the three established countries).
3. Complete postnatal window and complete spatial coverage: 42,052.
4. HAZ valid and within the measured universe: 23,135.
5. Complete cases on covariates, exposure, weight and cluster key: 23,135 (no further loss).
6. Singleton-cluster exclusion: −117 clusters and −117 observations.
7. **Final: 23,018 children in 3,114 clusters** (Ghana 1,940 in 353; Kenya 14,166 in 1,498; Nigeria 6,912 in 1,263).

Singleton clusters are removed separately from each model's own final sample, so the number removed differs between models; the three country models remove 27, 16 and 74. Section 3.9 explains why the Nigeria counts differ from the official 2018 anthropometry count; that gap remains unresolved.

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

Steps 1, 2, 4, 6 and 7 can be checked against two public aggregate files in `docs/provenance/`: `historical_wash_analysis_samples_v1/sample_flow_AGGREGATE.csv` and `historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`. Step 3 is recorded only in the restricted log, because the public flow file assigns each excluded record to its first failing condition in a different order. The steps were reproduced independently in the execution log of `scripts/historical_wash/20_validate_pooled_estimate.py` (`data/processed/estimation/pooled_independent_validation_20261007T090003Z/execution_log.txt`, RESTRICTED).

```{=latex}
\par\endgroup
```

## A.4 DHS/IPUMS official documentation sources attempted for the measurement-subsample weight (Section 3.8, Section 6.3)

**Table A.3 — Official documentation sources consulted for a measurement-subsample weight**

| Source tried | Result |
|---|---|
| DHS-8 Biomarker Manual (dhsprogram.com PDF) | HTTP 403, tried twice across two sessions |
| Guide to DHS Statistics (dhsprogram.com) | HTTP 403 |
| World Bank microdata catalogue, child anthropometry variable page | Accessible; no weighting guidance found |
| Nigeria 2018 NDHS final report | Accessible; describes sampling weights by stage and cluster and a domestic-violence special weight, but no anthropometry- or biomarker-specific weight |
| IPUMS-DHS PERWEIGHT and KIDWT documentation pages | Accessible; confirms PERWEIGHT as the documented child-level tabulation weight; KIDWT is a population factor and is not used |

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

No source documents a measurement-subsample-specific weight. This is recorded as an unresolved documentation gap (item 1 of `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md`). No substitute weight or correction was invented; Section 3.8 states the working inference used instead.

```{=latex}
\par\endgroup
```

## A.5 Full authoritative-file index

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

The current index of baseline and historical output files cited in this thesis, with their status labels (validated for main reporting, validated sensitivity, exploratory, invalid or superseded, not estimable), is `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md`, together with `02_core_reporting_table.md` in the same folder. That index refers to `final_empirical_package_v2_2026-10-07/00_results_index.md` for the baseline entries and to `01_final_reporting_map.md` for the status of each result.

```{=latex}
\par\endgroup
```

## A.6 Descriptive figures (baseline sample)

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.78\textwidth]{\ThesisRoot/figures/figure1_prevalence_by_country.png}
\end{figure}
```

**Figure A.1 — Weighted anthropometric prevalence by country (stunting, wasting, underweight), with 95% confidence intervals.** Baseline sample, Section 3.2; underlying values in `outputs/final_tables/final_table2_anthropometric_prevalence.csv`.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.85\textwidth]{\ThesisRoot/figures/figure3_wash_characteristics.png}
\end{figure}
```

**Figure A.2 — Weighted household WASH characteristics by country, full category breakdown (water and sanitation panels).** Explicit states (Unknown, structurally not applicable, Ghana's unclassified bio-digester, surface water, open defecation) are shown as their own segments, never merged into Improved/Unimproved. Source: `outputs/final_tables/final_table3_wash_characteristics.csv`.
