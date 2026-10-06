# Historical WASH extension: preliminary estimation, methods note (2026-10-06)

**PRELIMINARY — measurement-weight documentation and final design review pending.**

These estimates are exploratory outputs of the historical extension. They are not thesis results, they do not replace or update the baseline (current four-round, cross-sectional) analysis, and they do not change the manuscript's conclusions. No association here is a causal effect.

## 1. Working configuration (author choices for preliminary analysis)

- Working main window: first 12 postnatal months (post_12m), birth month included, completion required by interview. This is a **working** window, not a validated primary window (section 2).
- Established-date sample: Ghana 2014, Kenya 2014, Nigeria 2018 (Gregorian timing, month precision). Ethiopia 2016 appears only in separately labelled provisional sensitivity analyses (three interview-date candidates; section 6).
- Complete spatial coverage: every required annual IHME value has full valid coverage (tolerance 10⁻³ of buffer area).
- Controls: cluster fixed effects; survey-qualified country-by-birth-year terms; child sex; maternal age, education and marital status. Wealth excluded from the main specification and included in sensitivity analysis.
- Age: reported completed months where delivered (Ethiopia, Nigeria); otherwise documented calendar-month difference (Ghana, Kenya).
- Weights: PERWEIGHT, with equal country totals in each model's own estimation sample. An unweighted comparison uses the same samples.
- Inference: PSU-clustered CRV1, cluster = IDHSPSU (cross-sample unique, so sample-qualified by construction).

## 2. Literature basis for the window and status

- Cumming and Cairncross (2016), "Can water, sanitation and hygiene help eliminate stunting? Current evidence and policy implications" (PMC5084825), discuss that WASH strategies may need to address exposure pathways in the first two years of life, when stunting is concentrated, and that infancy exposure matters beyond the first year. I read the abstract-level summary only.
- This supports a window in early life. It does not single out 12 months: the stronger literature statement concerns the first two years, so the 24-month window has at least equal, arguably better, support. The 12-month window is kept as the working window because it is an early-life window whose completion can be checked at interview and that avoids pregnancy-period assignment; its choice is documented as a working choice, not a validated result.
- The label "first 1,000 days" is not used for any window.

## 3. Source questions: what can and cannot be resolved

**Ghana 2014 anthropometry sampling.** The official Ghana 2014 final report could not be read (certificate expired on the statsghana host; no alternative official copy was retrieved). A World Bank microdata catalogue summary of the Ghana 2014 survey states that anthropometric and biomarker measurements were taken in "a subsample of respondents whose household had been selected to receive the male questionnaire" and that the male questionnaire was administered in "half of the households". The extract's household measurement share (about 49%) is consistent with that description. This is a secondary description, not a verified rule, and no Ghana-specific weight is known.

**DHS biomarker weighting guidance.** Every official DHS URL tried (biomarker pages, DHS-6 and DHS-8 biomarker documents, Guide to DHS Statistics pages) returned HTTP 403. No authoritative DHS statement on a biomarker or anthropometry weight could be read. Unresolved.

**Nigeria 2018: three different populations.** Equal counts are not expected and no reconciliation is forced.

| Population | Count | Definition |
|---|---|---|
| Official measured-child count (NDHS 2018 final report) | 12,806 (unweighted) | Children under five "eligible to be measured in the 2018 NDHS subsample households" and measured (one-third of households, selected for the men's survey) |
| IPUMS birth-history extract (validated) | 33,924 records; 11,704 measured or flagged (non-NIU); 11,364 valid HAZ | Birth-history child records of interviewed women, born within about five years before the survey |
| Outcome-valid estimation sample (this work, water, HAZ, post_12m) | 6,912 (after singleton clusters) from 6,986 complete-timing, complete-spatial children | Children satisfying the working rules (under five, complete window and spatial coverage, outcome valid, covariates present), with clusters of at least two children |

The official population is the eligible children in subsample households. The extract is birth-history children of interviewed women and can omit children whose mothers are not in the sample (a hypothesis, not verified). The estimation sample further requires complete windows and complete spatial coverage. The three populations differ by design, so their counts are not expected to match. The gap between the official count and the extract is not closed.

**IHME water product (W_IMP).** The codebook labels the sanitation metric "Percent" and leaves the water metric blank. The IHME study (Local Burden of Disease WaSH Collaborators, Lancet Global Health 2020) describes annual estimates of access to drinking water and sanitation facilities at about 5 × 5 km resolution. The exact water definition (which improved-source classes, and whether population-weighted) was not verified from the study text. Output labels therefore use the product code (W_IMP), values are interpreted as IHME percentage points on the 0–100 scale, and no percentage-of-population interpretation is asserted.

**Weights.** Verified from official text (Nigeria 2018 final report; IPUMS-DHS PERWEIGHT and KIDWT pages): PERWEIGHT is the documented weight for child-level tabulations; the report describes sampling weights calculated by stage and cluster and the domestic-violence special weight, and no anthropometry or biomarker weight. KIDWT is a population factor and is not used. Inference (not documented): within-survey normalization of PERWEIGHT removes a constant measurement-subsample factor when selection is random at household level; differential non-response among eligible but unmeasured children is not corrected. Claims of representative population estimates are **not** made.

## 4. Estimator and inference

For outcome y, product p, window w, child i in cluster c and survey s:

    y_ic = α_c + β·E_ic(w,p) + λ·age_ic + γ'X_ic + δ_{s,b_ic} + ε_ic

- E: annual-weighted IHME MEAN over the window within the buffer (0–100 percentage points). β is reported per 1 percentage point and per 10 percentage points.
- α_c: cluster fixed effects. δ_{s,b}: survey-specific birth-year terms. X: child sex, maternal age, maternal education and marital status (wealth in sensitivity).
- Weights: w_i = PERWEIGHT_i × (n / K) / Σ_{j in country(i)} PERWEIGHT_j, so that each country's weights sum to n/K within the model's own sample (K = number of countries in that model).
- Estimation: weighted within-cluster least squares (weighted demeaning by cluster). Singleton clusters are dropped before estimation because they carry no within information (counts in the tables).
- CRV1 variance: V = c · B M B with M = Σ_g s_g s_g', s_g = X̃_g' w_g û_g, B = (X̃'WX̃)⁻¹, and c = G/(G−1) × (N−1)/(N−K), where K counts the non-fixed-effect regressors kept (absorbed fixed effects are not counted, following the repository's native CRV1 convention for same-group fixed effects and clustering). Confidence intervals use t with G−1 degrees of freedom.
- Rank and conditioning: rank of the weighted, cluster-demeaned design, and the scaled condition number. Absorbed terms are reported by name.

## 5. Verification performed

- Estimator and CRV1 check: four representative models (Ghana water HAZ weighted; Ghana sanitation WAZ weighted; Nigeria sanitation HAZ weighted; Ghana water HAZ unweighted) were re-estimated with an independent implementation (statsmodels WLS with explicit cluster dummies, sandwich computed by hand, the same correction convention) on a separately rebuilt sample. Coefficients agree to 3 × 10⁻¹⁴ and CRV1 standard errors to 8 × 10⁻¹⁰; sample sizes and cluster counts match exactly. This validates the implementation, not the convention.
- Design checks (24 primary models): record keys unique; each cluster identifier maps to one survey; country weight totals equal N/K; rank full; no singleton clusters in the estimation data.
- Not performed: an external replication of any coefficient against published results (none exists for this design).

## 6. Results: preliminary, weighted, working window (post_12m)

Coefficient per 10 percentage points of IHME coverage (z-score units), 95% CI in brackets, n = children, G = clusters.

**Water (W_IMP)**

| Outcome | Ghana 2014 | Kenya 2014 | Nigeria 2018 | Pooled established |
|---|---|---|---|---|
| HAZ | 1.65 [0.34, 2.96], n 1,940, G 353 | −0.61 [−2.07, 0.86], n 14,166, G 1,498 | 0.70 [0.15, 1.25], n 6,912, G 1,263 | 1.03 [0.51, 1.54], n 23,018, G 3,114 |
| WAZ | 1.06 [−0.16, 2.28] | −0.22 [−1.30, 0.86] | 0.45 [0.00, 0.90] | 0.65 [0.20, 1.10], n 23,057 |
| WHZ | −0.00 [−1.16, 1.16] | −0.16 [−1.29, 0.96] | −0.05 [−0.48, 0.38] | −0.08 [−0.50, 0.35], n 23,048 |

**Sanitation (S_IMP)**

| Outcome | Ghana 2014 | Kenya 2014 | Nigeria 2018 | Pooled established |
|---|---|---|---|---|
| HAZ | −2.48 [−4.91, −0.05] | −0.21 [−0.53, 0.11] | 0.20 [−0.34, 0.75] | −0.10 [−0.37, 0.17] |
| WAZ | −0.08 [−2.04, 1.88] | −0.15 [−0.38, 0.09] | 0.02 [−0.44, 0.48] | −0.07 [−0.29, 0.14] |
| WHZ | 1.64 [−0.27, 3.56] | 0.00 [−0.22, 0.22] | −0.17 [−0.59, 0.24] | −0.03 [−0.24, 0.17] |

Residual exposure variation after the controls (within-cluster SD of the exposure residual, percentage points): water 0.46 (Ghana), 0.20 (Kenya), 0.65 (Nigeria), 0.43 (pooled); sanitation 0.26, 0.88, 0.65, 0.79. Small values (Kenya water) mean imprecise estimates, not non-identification; no model was non-estimable.

Unweighted comparison (identical samples), water HAZ: Ghana 1.56 [0.46, 2.67]; Kenya −1.17 [−2.38, 0.04]; Nigeria 0.28 [−0.12, 0.69]; pooled 0.41 [0.03, 0.80]. The pooled water HAZ estimate is therefore sensitive to the weighting choice (1.03 weighted against 0.41 unweighted). Model-specific unweighted results for all outcomes are in the coefficient table.

## 7. Sensitivity analyses (planned; no specification search)

Pooled water HAZ (other rows in the coefficient table):

| Sensitivity | Pooled water HAZ per 10 points [CI] | Note |
|---|---|---|
| Main (post_12m, weighted) | 1.03 [0.51, 1.54] | |
| Birth-year window (own sample) | 0.54 [0.12, 0.96] | |
| Prenatal 9 months | 0.64 [0.24, 1.03] | |
| 24 postnatal months | 1.75 [0.81, 2.70] | |
| Wealth quintile added | 1.01 [0.50, 1.52] | Wealth overlaps with WASH components |
| Containing-pixel assignment | 0.68 [0.26, 1.10] | |
| Rural 10 km (urban unchanged) | 1.01 [0.42, 1.60] | |
| Stricter completion (one extra month) | 0.95 [0.43, 1.47] | |
| Calendar-month age throughout | 1.03 [0.52, 1.53] | |
| Excluding Ghana (water overlap) | 0.74 [0.24, 1.24] | Kenya + Nigeria |
| Common sample, all four windows (post_12m) | 1.64 [0.68, 2.60], n 16,419 | Different sample: see below |

Results are reported for every family; none was selected by significance. Sample changes:
- Window eligibility: each window has its own eligible sample; the 24-month window shrinks the pooled sample to 16,419 and the common-sample comparison changes the post_12m estimate from 1.03 to 1.64. This is a sample-composition effect (children whose 24-month window is complete differ from the full post_12m sample), not evidence about the window.
- Overlap: Ghana's IHME inputs include its own DHS survey for both products; Kenya's include its DHS survey for water. Excluding Ghana from sanitation leaves a Kenya and Nigeria pooled model (n 21,078 for HAZ); excluding Ghana from water leaves Kenya and Nigeria (n 21,078 for HAZ); excluding Kenya and Ghana from water leaves Nigeria only, which is labelled a country-specific estimate.
- Stricter completion removes about 0.5–3% of children (for example, 23,018 → 22,639 for pooled water HAZ).
- Calendar-month age throughout changes almost no estimate.

**Ethiopia 2016 (provisional sensitivity only):** water HAZ per 10 points: −0.43 (candidate C1, days valid only), −0.39 (C2), −0.39 (C3); CIs include zero. Sanitation HAZ: −0.54, −0.45, −0.45. The three candidates give the same sign and nearly the same estimate, but none of the candidate timings is validated; these are not established-date results.

## 8. Non-estimable models

None. All 291 planned models estimated (24 primary, 24 unweighted, 72 window, 24 wealth, 24 containing-pixel, 24 rural-10 km, 48 stricter completion, 24 calendar age, 18 Ethiopia provisional, 9 overlap exclusions). Several Kenya water models have small residual variation (0.20 points) and wide intervals, which is reported as imprecision.

## 9. Unresolved issues (must be closed before any estimate becomes a thesis result)

1. Measurement-subsample weighting: no documented anthropometry or biomarker weight; the Ghana and DHS official documents could not be read. The within-survey normalization of PERWEIGHT is an inference from the design.
2. Differential non-response among eligible children in subsample households: not corrected; not measurable from the extract.
3. The Nigeria measured-count difference (12,806 official vs 11,704 extract non-NIU): unexplained, plausibly children whose mothers are not in the sample.
4. Water product definition (W_IMP) and scale: unverified; interpreted only as IHME 0–100 percentage points.
5. Ethiopia interview timing: provisional; no established Gregorian interview date.
6. Window choice: the 12-month window is a working choice; the literature points more strongly to the first two years.
7. Overlap of Ghana and Kenya DHS surveys with IHME inputs: disclosed and tested by exclusion; not removed from the primary estimates.
8. Pooled weighting estimand: equal country totals are the working convention; the unweighted comparison shows the result depends on it (for water HAZ, 1.03 against 0.41).
9. Current residence as a proxy for historical residence; modelled exposure uncertainty; area averages rather than population-weighted coverage.
10. The exposure is an average over the buffer; displacement means the true location is not recovered.

No coefficient in this note supports a causal claim.
