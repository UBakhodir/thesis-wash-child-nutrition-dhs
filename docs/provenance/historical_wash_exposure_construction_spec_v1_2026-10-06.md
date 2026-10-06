# Historical WASH: child exposure-window construction, specification v1 (2026-10-06)

Status: construction specification and validation record. The windows are constructed, but no primary window is selected, no outcome is estimated, and nothing here is a thesis result. Child-level outputs, cluster identifiers, coordinates and the readiness and variation tables are restricted and are not published.

## 1. Inputs

- Validated IPUMS-DHS idhs_00002 run (child birth-history records; 71,413).
- Cluster-year IHME extraction (MEAN estimate; S_IMP and W_IMP; 2000–2017), with the buffer rules in historical_wash_spatial_extraction_2026-10-06.md and the geometry addendum.
- Ethiopia 2016 provisional interview-date candidates (see section 5).

## 2. Definitions (calendar months)

CMC = (year − 1900) × 12 + month. b = birth CMC (KIDDOBCMC; month precision); t = interview CMC.

| Window | Included months | Birth month | Length L | Annual weight |
|---|---|---|---|---|
| birth_year | the 12 calendar months of the birth year | (not separate) | 12 | weight 1 on the birth year |
| prenatal_9m | b−9 … b−1 | excluded | 9 | months in year ÷ 9 |
| post_12m | b … b+11 | included | 12 | months in year ÷ 12 |
| post_24m | b … b+23 | included | 24 | months in year ÷ 24 |

The annual weight for year y is (months of the window falling in y) ÷ L. Weights sum to one for every complete window (tested).

## 3. Completion and date precision

- Birth dates are known to the month only (KIDDOBCMC). Postnatal windows are complete at interview only if t ≥ b + L (every window month has ended before the interview month).
- Sensitivity: t ≥ b + L + 1, because the birth day is unknown and the true birth may fall later in the month. This is reported separately and is not used for the construction.
- Interview dates are month-level for Ghana, Kenya and Nigeria (INTDATECMC).
- A birth after the interview month is excluded (birth_after_interview).

## 4. Raster coverage and annual values

- Required annual values: every calendar year touched by the window. The raster years are 2000–2017.
- A window needing any other year is excluded (window_outside_2000_2017). No extrapolation, no shortening, no neighbouring-year substitution, no filling.
- Annual values that include post-interview months (the annual value for the interview's own calendar year) are flagged in the child-level output, not altered.

## 5. Ethiopia 2016 (provisional; kept separate)

Three candidate interview-date constructions, each labelled PROVISIONAL, are carried separately; they are never combined with established Gregorian timing.

- ET_C1: 30-day Ethiopian arithmetic on the delivered day and month; available only where the day is valid (10,366 of 10,641; 275 rows have impossible day values).
- ET_C2: century-day route with origin 1 Meskerem 1900 = 12 September 1907.
- ET_C3: century-day route anchored to 1 Meskerem 2008 = 12 September 2015 with Gregorian cumulative month lengths.

Birth CMC for Ethiopia is KIDDOBCMC (documented as IPUMS-converted from Ethiopian dates; month precision). Exposure values depend on the window and the birth; the candidates affect only the interview CMC and therefore completion and interview-year flags. Verified in the validation: the exposure values are identical across C2 and C3 wherever both are eligible (maximum difference 0).

Eligibility is reported as: eligible under all three candidates; eligible under none; or dependent on the candidate. Dependence is not treated as a proven uncertainty bound.

## 6. Spatial coverage rules (per required annual value; MEAN estimate)

| Construction | Rule | Status |
|---|---|---|
| complete_primary | every required annual value has status full (valid-area fraction ≥ 1 − 10⁻³); urban 2 km, rural 5 km buffers | primary candidate construction |
| partial_diagnostic_primary | valid-area mean accepted when partial; minimum valid fraction retained | diagnostic only |
| containing_pixel | containing-pixel value; NoData → missing (no nearest-cell substitution) | sensitivity |
| rural_10km | rural children only; 10 km buffer | sensitivity |

These constructions are separately named and never merged. The coverage threshold is the numerical tolerance (not chosen on outcomes).

The mean used is the area-weighted mean over valid overlap area: Σ(value × valid overlap area) ÷ Σ(valid overlap area). Missing area adds to neither the numerator nor the denominator (section 8 of the geometry addendum).

## 7. Products and labels

- W_IMP (water) and S_IMP (sanitation), MEAN estimate only. The water product's metric is not populated in the codebook, so the variable is labelled by its product code and documented source scale; no denominator or interpretation is assigned beyond that.
- LOWER and UPPER are not used as exposure variables. They are not child-level confidence intervals.

## 8. Merge and record checks (validated)

- Unique record identifiers in the typed run: yes (71,413).
- Child-candidate pairs unique: yes (60,772 established Gregorian rows plus 3 × 10,641 Ethiopian candidate rows).
- Annual extraction keys (cluster, product, year, method) unique for MEAN: yes (375,480 rows; zero duplicates).
- Many-to-one merge: children attach to one cluster; the row count before and after the merge is identical.
- Unmatched children: 765 (420 Ethiopia, 83 Ghana, 113 Kenya, 149 Nigeria). All have no usable coordinates. They are preserved with their eligibility flag and are not deleted.

## 9. Coverage reconciliation

- Annual rows equal clusters × 18 years for every product, estimate and method (verified).
- Exclusion categories are mutually exclusive and ordered; they sum to the record count in every row of the readiness table (verified).
- The final category equals the final-intersection count in every row (verified after correcting two category-logic errors, preserved in earlier validation folders).

## 10. Temporal tests (synthetic, independent expectations)

Nine tests pass: within one year (birth-year, prenatal); spanning years (post-12 July birth: 2010.5; post-24 March birth: three years); January birth; prenatal spanning two years; birth near raster end (out of range); incomplete postnatal (flagged); missing annual value (no fill). Expected weights are computed by calendar-month enumeration, independently of the array arithmetic.

Independent cross-check: 2,400 sampled constructions recomputed from the annual table by a separate path; maximum absolute difference 1.4 × 10⁻¹⁴; weights sum to one in all sampled rows.

## 11. Geometry and denominator checks

- Denominator: the implemented mean is the valid-area mean (section 6). Using total buffer area instead would bias partial buffers by up to 73 points on the test clusters, so the implemented formula is the required one.
- Geometry: pixel boundaries are straight corner-to-corner segments in the cluster-centred projection; the disk boundary is exact. Against a 16-point-per-edge densified boundary, per-pixel area differs by at most 2.1 × 10⁻⁸ (relative), and buffer means by at most 0.001 points (median 0.00002) on 150 clusters.

## 12. Outputs (restricted, local)

- Child-candidate exposure table (restricted; child identifiers and exposures).
- Validation folders with readiness, exclusion, coverage, variation and candidate-agreement tables.
- Manifest with input hashes (unchanged), script hash, interpreter and package versions.

## 13. Decisions not made here

- The primary window.
- The Nigeria round (2013 or 2018).
- The analysis weights (weighting and measurement-subsample questions remain open).
- The Ethiopia timing candidate for any primary analysis.
- Any outcome model specification.
