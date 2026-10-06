# Historical WASH extension: analysis sample and estimation specification, v1 (2026-10-06)

Status: specification for review before any outcome model is estimated. No coefficient has been estimated or inspected. The specification is proposed; choices that need author or supervisor input are listed in section 9. Restricted child-level data, cluster identifiers and coordinates are not published.

Historical extension versus baseline: the baseline (current four-round, cross-sectional WASH and nutrition analysis) is documented in empirical_strategy.md and is not changed here. This specification is a separate, complementary historical analysis of child anthropometry against modelled early-life WASH coverage (IHME 2000–2017), using earlier survey rounds.

## 1. Units and variables

- Unit of analysis: child i, in DHS survey s (country-round), cluster c (IDHSPSU, unique across surveys), with a birth-history record (from the IPUMS-DHS children extract).
- Outcomes: HAZ, WAZ and WHZ (Z-scores). Stored values are divided by 100 once (documented scale). Analysis models use one outcome at a time.
- Exposure: E_ic(w, p), the annual-weighted mean of the IHME MEAN estimate for product p (W_IMP water; S_IMP sanitation) over the calendar months of window w, within the cluster's displaced-coordinate buffer (urban 2 km, rural 5 km; complete spatial coverage). Units: IHME percentage points (0–100). Labelled by product code; not a population coverage estimate (section 6).
- Windows (section 3): birth_year; prenatal_9m; post_12m; post_24m.

## 2. Under-five eligibility and age

Rule (applied to every child; no record is deleted):
- Reported age: KIDCURAGEMO (completed months) where delivered. It is delivered for Ethiopia 2016 and Nigeria 2018, and blank for Ghana 2014 and Kenya 2014 (the blank values are not assumed to mean a survey phase rule).
- Derived age: interview CMC minus birth CMC (calendar-month difference). For Ethiopia the Ethiopian-calendar pair (INTDATECMC_ET − KIDDOBCMC_ET) is used, which needs no date conversion. For Ghana, Kenya and Nigeria the Gregorian pair is used.
- under-5 = reported age in 0–59 when reported; otherwise derived age in 0–59.
- Calendar difference of 60 (Ethiopia 70 rows; Nigeria 183): resolved by the reported completed age where delivered (no reported value equals 60). Ghana and Kenya have no calendar difference above 59, so no boundary case arises there.
- Negative derived age (interview before birth) would be excluded as birth_after_interview. No such case occurs in the four samples.
- Disagreement between derived and reported age outside {0, 1} is flagged, not corrected: Ethiopia 2 rows (both −1); Nigeria 11 rows (9 at −1, 2 at +2). These are retained, flagged, and reported as a sensitivity check.

Age variable entering the model: age_months = reported completed months where delivered, otherwise derived calendar months. Because the mixed definition differs by survey, it is applied only within survey (survey-specific fixed effects; section 4). Sensitivity: calendar months for all children.

## 3. Exposure windows

| Window | Months | Birth month | Annual weight | Completion (postnatal) |
|---|---|---|---|---|
| birth_year | calendar year of birth | — | 1 | — |
| prenatal_9m | b−9 … b−1 | excluded | months in year ÷ 9 | — |
| post_12m | b … b+11 | included | months in year ÷ 12 | interview CMC ≥ b+12 |
| post_24m | b … b+23 | included | months in year ÷ 24 | interview CMC ≥ b+24 |

Every calendar year the window touches must have a complete annual value (2000–2017). No extrapolation, shortening, neighbour-year substitution or filling. Birth dates are month-precision, so the completion rule is conservative; the sensitivity rule (one additional month) is reported separately.

## 4. Estimating equation (proposed; not estimated)

    Y_ic = α_c + β · E_ic(w, p) + δ_{s, b_ic} + λ · age_ic + X_ic' γ + ε_ic

- α_c: DHS cluster fixed effect (IDHSPSU). Absorbs all cluster-constant terms, including survey (country) effects, urban/rural residence and any cluster-level WASH or environment.
- δ_{s, b}: survey-specific birth-year effects (country × birth year). Absorb national-level cohort differences. Not absorbed by cluster fixed effects because birth years vary within clusters.
- λ · age_ic: age in months (section 2), linear. Shares its identifying variation with birth year (section 5).
- X_ic: child and maternal controls, reference persons below. Included only where they vary within cluster.
- β: the coefficient of interest, identified from within-cluster variation in E across children whose birth years and interview months differ, after the cohort and age terms.

Controls and reference persons:

| Variable | Reference person | Coding | Within-cluster variation |
|---|---|---|---|
| child female (KIDSEX) | child | 1 female, 0 male | yes |
| mother's age (AGE) | mother (woman) | completed years | yes |
| mother's education (EDUCLVL) | mother | 0 none, 1 primary, 2 secondary, 3 higher; 8 missing (absent in extract) | yes |
| mother's marital status (MARSTAT) | mother | categories as in the codebook | yes |
| urban residence (URBAN) | household (cluster-level in practice) | 1 urban, 2 rural | no (absorbed by α_c) |
| household wealth quintile (WEALTHQ) | household | 1 poorest … 5 richest | sensitivity only (section 9) |

Absorbed or redundant terms (not included): survey dummies (absorbed by α_c, since clusters nest within surveys); interview year (one calendar year per survey; absorbed by survey effects); urban/rural residence (absorbed by α_c); cluster-level WASH or community measures (absorbed by α_c and not separately identified). Dropping any control to obtain identification is not proposed.

## 5. Age, birth cohort and interview timing

- Identity: age_ic = t_ic − b_ic (calendar months; interview CMC minus birth CMC), so any two of age, birth cohort and interview timing determine the third only with the birth or interview month added.
- Within a survey, interview CMC spans the fieldwork months (about six months in Ethiopia 2016; several months elsewhere). Birth-year effects, age and the exposure therefore share a within-cohort, within-cluster structure: children born in the same year but interviewed in different months have different ages.
- Checked (section 7): the within-cluster design with the proposed controls has full rank, and no column is an exact linear combination of the others. Adding interview-month dummies (a variant that tests the timing structure) also keeps full rank, with no exact dependence. The age coefficient is then identified from birth-month variation within birth year and interview month, which is not a cohort effect; its interpretation must be stated when estimates are reported.
- Correlation between age and birth year is strong: −0.89 to −0.98 across samples, windows and outcomes (mean −0.96). This is a precision concern, not an exact collinearity. No control is dropped to address it. The identity age = interview CMC − birth CMC holds exactly in the analysis data (maximum difference 0).

## 6. Area averaging versus population coverage

- The exposure is a geographic area average of modelled coverage within the displaced-coordinate buffer (area-weighted over valid overlap area). It is not a population-weighted coverage estimate and is not described as one.
- The buffer is centred on a displaced cluster location; displacement (urban up to 2 km; rural up to 5 km for 99% and up to 10 km for 1%) means the true location is not recovered. Sensitivity: rural 10 km.
- Current residence is a proxy for historical residence; migration between birth and interview is not observed.
- IHME values are modelled estimates. The LOWER and UPPER bounds are supplied bounds, not confidence intervals for the buffer mean or the regression coefficient.
- IHME/DHS input overlap: Ghana 2014 is a DHS input for both products; Kenya 2014 for water only. These overlaps are disclosed in every output that uses these samples and tested in a sensitivity analysis that excludes the overlapping product.

## 7. Design diagnostics (no outcome estimated)

Computed on the candidate samples (within-cluster transformation; exposure projected on the controls only). Full table: restricted diagnostic output; summary for the proposed primary configuration (water, post_12m, HAZ):

| Sample | Records | Clusters | Singleton clusters | Clusters with ≥2 children | Of which exposure varies | Columns (proposed) | Absorbed | Rank | Scaled condition number | Residual exposure SD after controls |
|---|---|---|---|---|---|---|---|---|---|---|
| Ghana 2014 | 1,967 | 380 | 27 | 353 | 353 | 16 | urban_hh | 15/15 | 14.9 | 0.45 |
| Kenya 2014 | 14,182 | 1,514 | 16 | 1,498 | 1,497 | 16 | urban_hh | 15/15 | 13.5 | 0.20 |
| Nigeria 2018 | 6,986 | 1,337 | 74 | 1,263 | 1,259 | 16 | urban_hh | 15/15 | 11.7 | 0.65 |
| Ethiopia 2016 (candidate C2, provisional) | 6,580 | 598 | 12 | 586 | 586 | 16 | urban_hh | 15/15 | 11.5 | 1.25 |

Interpretation: full rank and moderate conditioning mean the proposed design is not exactly collinear. Residual exposure variation after the controls is positive in most clusters with two or more children. Small residual variation (for example Kenya, 0.20 points) is a precision concern and does not, on its own, show that β is unidentified. Causal interpretation is not supported by this design; the historical design improves temporal alignment, not identification of a causal effect (repository empirical strategy, section 6).

## 8. Weights, normalization, inference and sensitivity

Weights (see historical_wash_weights_and_measurement_2026-10-06.md for the sources and their limits):
- Proposed: the standard person/child weight PERWEIGHT, used for child-level tabulations in the measured sample, normalized within survey to mean 1. Within a survey, this normalization removes any constant one-third factor from the measurement subsample.
- KIDWT is not used as an analysis weight (population factor for counts).
- Pooled estimand (open, section 9): baseline convention is equal country totals (weight divided by its country total in the estimation sample, repository script 11_main_regressions.py). Alternatives: country-proportional pooling of within-survey normalized weights; unweighted.

Inference:
- Standard errors clustered at the DHS primary sampling unit (IDHSPSU), which is also the fixed-effect unit. Because the fixed effects and clustering share the same grouping, the repository's adjudicated inference convention applies: native CRV1 cluster-robust variance with no additional degrees-of-freedom penalty for the absorbed cluster effects (cluster-robust standard errors that match the baseline convention; the choice is documented in the repository's cluster-FE inference record).

Sensitivity analyses (pre-specified; reported together; none selected by results):
1. Windows: birth_year, prenatal_9m, post_24m (in addition to the primary window).
2. Spatial method: containing pixel; partial-diagnostic buffer means (reported separately, never merged with complete coverage); rural 10 km buffers.
3. Completion rule: sensitivity requiring one additional month.
4. Age definition: calendar months for all children.
5. Ethiopia: excluded; included with each provisional interview-date candidate (C2, C3; C1 where its day is valid).
6. Product overlap: exclude the product with a DHS input for that survey (Ghana 2014 both products; Kenya 2014 water).
7. Wealth quintile added (overlap with WASH components; section 9).
8. Weights: unweighted; pooled alternatives.

## 9. Decisions that require author or supervisor input

See the decision table in historical_wash_decisions_2026-10-06.md (also public). Short list: primary window; Nigeria round (2018 retained vs 2013, which needs a new extract); Ethiopia's role; pooled weighting estimand; wealth adjustment; the age definition; and whether a measurement-subsample flag should be requested.

## 10. What this specification does not claim

- No coefficient exists yet, and no result is reported.
- No causal identification is claimed.
- Ethiopia's timing remains provisional, and its results cannot be treated as established Gregorian timing.
- The sample and design checks are preparation, not evidence about the association.
