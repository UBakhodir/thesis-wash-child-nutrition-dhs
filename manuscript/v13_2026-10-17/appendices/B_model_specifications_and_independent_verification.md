# Appendix B — Model specifications, inference conventions, and independent verification

The estimating equations are stated in Chapter 4 (Sections 4.1–4.6). This appendix records how they are implemented for inference and how far the implementation has been verified. It covers the baseline household cluster-fixed-effects model (Section B.1), the historical extension (Sections B.2–B.4) and the estimator safeguard added after an external audit (Section B.4). Figures marked RESTRICTED come from execution logs and output folders that contain or derive from restricted microdata; they are carried here from those records and from the public provenance documents named in the text. They were not re-executed in preparing this appendix.

## B.1 Inference-convention comparison (baseline household cluster-FE model, HAZ)

**Table B.1 — Household water and sanitation coefficients for HAZ under the two inference conventions (baseline household cluster-fixed-effects model)**

| Convention | Water β | SE | p | Sanitation β | SE | p |
|---|---|---|---|---|---|---|
| PRIMARY (same-group CRV1; this thesis's main convention) | −0.085 | 0.046 | .062 | 0.026 | 0.043 | .548 |
| FULL\_DUMMY\_DF sensitivity | −0.085 | 0.049 | .080 | 0.026 | 0.046 | .574 |

::: {.tablenote}
```{=latex}
\raggedright
```

Note: Household water and sanitation are entered together; N = 36,040 children in G = 4,426 PSUs (`country_psu`). Both rows use the normal reference distribution for *p*-values and confidence intervals. Source: `outputs/household_community_wash/03_household_cluster_fe.csv`, rows `natural_sample_PRIMARY_SAME_CLUSTER_CRV1` and `natural_sample_FULL_DUMMY_DF_SENSITIVITY`, outcome `haz`.
:::

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

The two conventions differ only in whether the small-sample CRV1 correction also penalises degrees of freedom for the absorbed cluster dummies. FULL\_DUMMY\_DF does; PRIMARY does not, following the project's cross-validated adjudication against `linearmodels.PanelOLS(auto_df=True)` [@Sheppard2024Linearmodels] (see `docs/provenance/cluster_fe_inference_adjudication.md`). Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged. The adjudicated PRIMARY convention is the one presented in the abstract, the introduction and the conclusion. The FULL\_DUMMY\_DF sensitivity is documented here and reported next to the primary values in Section 4.5 and Section 5.1, where it is named explicitly. This does not mean that both conventions are repeated wherever else this coefficient is mentioned.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**How the two conventions are computed.** The model is fitted as weighted least squares on data demeaned within each PSU (weighted within-cluster demeaning, which uses only within-cluster variation and is equivalent to including a full set of PSU dummies), with `statsmodels` `cov_type="cluster"` clustered on the same `country_psu` grouping. The library's correction is
$$c = \frac{G}{G-1}\times\frac{N-1}{N-K},$$
where $K$ is the number of columns in the design matrix it receives. Under PRIMARY that is $K = 18$: the household exposures and covariates after demeaning, with no constant and no PSU dummies. FULL\_DUMMY\_DF counts every absorbed PSU dummy as an estimated parameter, $K = 18 + 4{,}426 = 4{,}444$, which multiplies the PRIMARY standard error by $\sqrt{(N-18)/(N-4{,}444)}$ (1.0677 for HAZ) and recomputes *p*-values and confidence intervals from the normal distribution. The executed run log records `use_t: False` for these fits, so the PRIMARY *p*-values are normal-reference values as well (Section 4.5). The equivalence of demeaning and explicit PSU dummies was checked in the same script on a Ghana subset (N = 4,287, 613 PSUs): the two coefficients differ by 2.59×10⁻¹⁵ (water) and 5.57×10⁻¹⁵ (sanitation). The baseline code contains no singleton-cluster exclusion step, so $G$ counts every PSU in the estimation sample (Section 4.5). The region-fixed-effects models are fitted differently: they use explicit region dummies, so $K$ counts the constant, the covariates and the region dummies, and they too use the normal reference distribution. They are not part of Table B.1.

```{=latex}
\par\endgroup
```

**Why the baseline/`linearmodels` cross-validation agrees only to four or five decimal places, not further (2026-10-17 addendum).** `docs/provenance/cluster_fe_inference_adjudication.md` records that an independent `linearmodels.PanelOLS(auto_df=True)` re-estimation of this model agreed with the native `statsmodels` standard errors "to four to five decimal places" but does not state whether that call also passed `group_debias=True`, the same opt-in flag whose omission is the entire explanation for the analogous, larger residual gap in the historical pipeline's own validation scripts (Section B.2 below). The call itself was not preserved as committed code, so this could not be settled by reading it. It was instead checked freshly in this pass: the PRIMARY household cluster-FE model (water and sanitation, HAZ) was re-estimated with `PanelOLS(entity_effects=True, drop_absorbed=True)` on the same sample and weights, first with `auto_df=True` alone, then adding `group_debias=True`. Without the flag, the standard errors differ from the stored PRIMARY values by a relative 9.0e-05 (water) and 7.5e-05 (sanitation); with it added, the differences shrink to a relative 8.8e-06 and 2.5e-05. Both relative gaps are of the same order as the figure this appendix's own adjudication note anticipated, and adding the flag reduces each by roughly an order of magnitude, the same pattern Section B.2 documents for the historical pipeline. This supports, without proving beyond doubt for the specific unpreserved call, that the same omission explains the residual gap here. It changes nothing: the stored, published PRIMARY standard errors in Table B.1 come from `statsmodels`, not from this (or any) `linearmodels` cross-validation, and neither this check nor its predecessor altered any reported coefficient, standard error, confidence interval, or *p*-value.

## B.2 Independent verification of the pooled historical model (Section 4.6, Section 5.6)

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

This thesis's own pipeline (`scripts/historical_wash/16_estimate_preliminary.py`) estimates all 291 historical models with a hand-written estimator based on weighted within-cluster demeaning. An earlier independent check (`scripts/historical_wash/17_validate_estimates.py`) re-estimated four representative *country-specific* cells: Ghana water–HAZ, weighted and unweighted; Ghana sanitation–WAZ; and Nigeria sanitation–HAZ. Three are primary cells; the unweighted Ghana cell (`m0005`) belongs to the unweighted comparison family. That script rebuilds each sample with its own filters, fits weighted least squares with explicit cluster dummies in `statsmodels`, and computes the CRV1 sandwich by hand with $K$ counting only the non-fixed-effect regressors. Coefficients agreed within 3×10⁻¹⁴ (maximum absolute difference 2.96×10⁻¹⁴), standard errors within a relative difference of 7.5×10⁻¹⁰, and N and G were identical in all four cells (public output: `docs/provenance/historical_wash_preliminary_estimates_v1/independent_validation_PRELIMINARY_AGGREGATE.csv`).

```{=latex}
\par\endgroup
```

That check did not cover the pooled multi-country model, which is the headline result of the historical extension. `scripts/historical_wash/20_validate_pooled_estimate.py`, written for this manuscript-preparation phase of the project, independently:

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

1. Rebuilds the estimation sample directly from the analysis-candidates stage (not from the stored, already-estimated model dataset), applying every filtering step explicitly and logging row counts (reproduced in Appendix A, Section A.3).
2. Estimates with `linearmodels.PanelOLS`, a different software library from the project's own hand-written estimator, using entity (cluster) fixed effects and clustered CRV1 standard errors.
3. Reports both the PRIMARY (`auto_df=True`) and FULL\_DUMMY\_DF (`auto_df=False`) conventions.
4. Estimates the unweighted counterpart on exactly the same final observations.

```{=latex}
\par\endgroup
```

The rebuild is independent in its filtering, weighting, design construction and estimation. It reads the same analysis-candidates file as the main pipeline, so the variables constructed upstream of that file are shared: the exposure assignment, the outcome validity flags, the birth year, the calendar age and the weight field. The check therefore does not re-verify those constructions.

**First attempt and its correction, reported for transparency.** An initial run of this independent script used a single pooled reference birth-year cell (rather than a separate reference year per country) and omitted the child's own age in months as a linear control. It produced β per 10 points = 1.385 against the stored 1.026, a discrepancy of roughly 35%. The sample size (N = 23,018), cluster count (G = 3,114) and exposure mean and SD nevertheless matched the stored values exactly, which pointed to a specification difference rather than a sample-construction error. After the documented design was matched exactly (country-local-reference birth-year dummies; child age in months included), the independent estimate converged to the values in Table B.2.

**Table B.2 — Independent re-estimation of the pooled established-date water–HAZ model compared with the stored estimate**

| Quantity | Independent (corrected) | Stored (`m0004`) | Absolute difference |
|---|---|---|---|
| β per 10 points | 1.0255531 | 1.025553067 | 6.7×10⁻⁸ against the six-decimal value 1.025553 (see note) |
| SE per 10 points (as originally run) | 0.260694 | 0.260730 | 3.6×10⁻⁵ (explained below) |
| N | 23,018 | 23,018 | 0 |
| G (clusters) | 3,114 | 3,114 | 0 |
| K (regressors) / rank | 24 / 24 | 24 / 24 | 0 |
| Residual exposure SD (points) | 0.428348 | 0.428348 | none at six decimals |
| Unweighted counterpart β per 10 | 0.4147 | 0.4146971 (`m0008`) | none at four decimals |

::: {.tablenote}
```{=latex}
\raggedright
```

Note: Stored values are from `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` (rows `m0004` and `m0008`; β per 10 for `m0004` is 1.025553067200643 at full precision). Script 20 compared its estimate with six-decimal constants written into the script (β 1.025553, SE 0.260730), so the 6.7×10⁻⁸ in the β row measures that rounding, not a disagreement between estimators; the full-precision comparison for this cell, made by `21_validate_all_primary_cells.py`, is 2.4×10⁻¹⁴ (pass-3 audit record). The independent rank is that of the regressor matrix before the fixed-effect transformation; the stored rank is that of the weighted within-transformed matrix. Independent values are carried from the RESTRICTED execution log; where only rounded values are recorded, agreement is stated at that precision.
:::

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

Full execution log and comparison JSON: `data/processed/estimation/pooled_independent_validation_20261007T090003Z/` (RESTRICTED; aggregate figures only, reproduced above).

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**Which of the two changes explains the 1.385-versus-1.026 gap (2026-10-09 diagnostic).** Both changes were made together in the original attempt, and that attempt's code was never committed to this repository, so the gap could not at first be decomposed. A dedicated diagnostic (`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`) separates them on a reconstruction of the described design. It compares the two birth-year schemes on the transformed design the estimator actually uses, the weighted within-cluster-demeaned matrix, not on the raw matrix, because raw-space comparisons alone cannot show whether a fitted coefficient must be unaffected. **The exposure variable (E10, exposure in units of 10 percentage points) is never used to construct any of the comparisons below.** An earlier version of the diagnostic residualized the birth-year blocks against a set that included E10 itself before comparing ranks. That is circular: residualizing against E10 can remove exactly the part of a block that would otherwise affect E10's own coefficient. The corrected version keeps E10 out of every column-space comparison and instead checks directly that E10's own residual values do not depend on the choice of scheme. The script's tolerances are a rank tolerance of 10⁻⁸ relative to the largest singular value, a weighted column-norm threshold of 10⁻¹⁰ for treating a demeaned column as absorbed, and a relative tolerance of 10⁻⁸ for "the same residual vector".

```{=latex}
\par\endgroup
```

*Raw design matrix.* The single-pooled-reference birth-year scheme does change the raw design matrix: it has 13 birth-year dummy columns against the country-local scheme's 12. Nigeria's observed birth-year range (2013–2017) does not include the single global reference year (2009, the earliest birth year observed anywhere in the pooled sample), so Nigeria keeps a dummy for its own earliest year, which the country-local scheme drops as its reference category. This extra column survives the cluster-fixed-effect demeaning on its own; it is not itself absorbed.

*Step 1: direct comparison, before E10 or any other covariate is involved.* Each scheme's birth-year block is demeaned (weighted within-cluster demeaning, the transformation that `PanelOLS`’s entity effects use) and the weighted blocks' ranks are compared directly: local 12 (of 12 surviving columns), pooled single reference 12 (of 13 surviving columns, one of which is already redundant at this stage), combined 12. The two demeaned blocks span **equal** subspaces before any residualization.

*Step 2: residualized against the shared nuisance controls only.* The blocks are residualized against age in months, maternal age and the demographic dummies, with E10 explicitly excluded from the projection, and the check is run separately with and without age in months. The spans are equal in both cases (rank 12/12/12 throughout).

*Step 3: E10's own residual, compared directly.* For each scheme, the complete nuisance specification is built (the absorbed cluster fixed effect, the shared controls and that scheme's own birth-year block) and E10 is residualized against it. The two weighted residual-exposure vectors differ by at most 1.73×10⁻¹⁵ in absolute terms; divided by the weighted norm of the residual vector, that maximum is 2.23×10⁻¹⁶. The vectors are the same, which is confirmed elementwise rather than inferred from rank alone.

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

*Step 4: independent cross-check with the explicit weighted Frisch–Waugh–Lovell formula*
$$\hat\beta = \frac{e'W\tilde y}{e'We},$$
where $W$ is the diagonal matrix of model weights, $e$ is the demeaned E10 residualized on that scheme's nuisance columns, and $\tilde y$ is the demeaned HAZ residualized on the same columns. This β is computed from first principles, not read from the output of `PanelOLS`, and it agrees with the coefficient that `PanelOLS` itself fits to within 4.4×10⁻¹⁶ in all four scheme and age-control combinations.

```{=latex}
\par\endgroup
```

*Step 5: mechanical explanation of the redundant column, without reference to E10.* In the pooled-single-reference scheme, Nigeria's five own-year dummy columns sum to Nigeria's own raw country indicator, confirmed elementwise across all 23,018 observations (absolute tolerance 10⁻¹² for these 0/1 columns). That indicator demeans to exactly 0.0: every DHS cluster belongs to exactly one country, so a column that is constant within every cluster is absorbed by the cluster fixed effect. This is the mechanism behind the equal-span result above.

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

Steps 1–3 establish directly, not by inference from a single rank comparison, that the two birth-year schemes are equivalent nuisance specifications for the exposure coefficient. Step 4 confirms the resulting coefficient by an independent computation, and Step 5 explains the mechanism. The fitted values agree with this result at floating-point precision. With the age-in-months control included, the exposure coefficient is 1.0255530672006674 (local) against 1.0255530672006667 (pooled single reference), an absolute difference of 6.661338147750939×10⁻¹⁶. With the control excluded, it is 1.3852855197991372 against 1.3852855197991374, an absolute difference of 2.220446049250313×10⁻¹⁶. These differences are three and one units in the last place of a double-precision number near 1 (machine epsilon 2.2×10⁻¹⁶). They are reported as independently observed numerical evidence consistent with the algebraic result, not merely inferred from it.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

The age-in-months control, by contrast, accounts for the gap on this reconstruction: 1.0255530672006674 with it and 1.3852855197991372 without it, under *either* birth-year scheme. The first value matches the stored value (1.025553). The second approximately reproduces the documented early-attempt value ("1.385"). On this reconstruction, therefore, the age-in-months omission explains the 1.385-versus-1.026 gap. The birth-year reference coding does change the raw design matrix, and this is not dismissed as a non-issue, but it does not affect the fitted exposure coefficient, because the two schemes carry the same information after cluster-fixed-effect absorption. This is the diagnostic's finding on a reconstruction of the described design. It is not a claim about what the specific, unpreserved original code did, and it is not an exact recovery of that code's reported output. The full tolerances and the complete five-step evidence chain are in the diagnostic's own execution log (`data/processed/estimation/birthyear_coding_diagnostic_20261009T081301Z/`, RESTRICTED); the values above are also recorded in the script's docstring.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**The SE difference in Table B.2 is fully explained; it is not residual numerical noise.** The declared small-sample correction of `16_estimate_preliminary.py` is $(G/(G-1)) \times ((N-1)/(N-K))$, applied to the raw cluster-robust sandwich, with confidence intervals and *p*-values from a Student *t* distribution on $G-1$ degrees of freedom. Here $K$ counts the non-fixed-effect regressors retained (24 for the pooled cell); the absorbed cluster effects are not counted (function `fit()`, lines 248, 251 and 264–265 at commit `c58fc47`). The **original, incomplete** call in `20_validate_pooled_estimate.py` and `21_validate_all_primary_cells.py`, `PanelOLS.fit(cov_type="clustered", cluster_entity=True, auto_df=True)`, applied only one of the two factors that this correction requires. `auto_df=True` correctly sets the same-group, no-double-penalty degrees-of-freedom convention: with the entity effect nested in the clusters, `_determine_df_adjustment` in `panel/model.py` sets the extra degrees of freedom to zero (confirmed in the `linearmodels` 7.0 source). `debiased=True`, the library's own default, applies the scale $N/(N-K)$. The original call did not pass the *separate*, opt-in `group_debias=True` setting, so it never applied the library's cluster-count adjustment $(G/(G-1)) \times ((N-1)/N)$ (`group_debias_coefficient` in `shared/covariance.py`). With that setting added, the two factors multiply out to the declared correction:
$$
\begin{aligned}
\frac{N}{N-K}\times\left(\frac{G}{G-1}\times\frac{N-1}{N}\right) &= \frac{G}{G-1}\times\frac{N-1}{N-K}.
\end{aligned}
$$
The difference between the two pipelines is therefore a covariance-setting discrepancy in the validation scripts, not a different formula and not floating-point noise. `scripts/historical_wash/24_reconcile_inference_corrections.py` refits all 24 primary cells with `group_debias=True` added, using sample-construction code copied from script 21. For every one of the 24 cells, the pass-4 audit record reports a maximum absolute SE difference of 0.0 against the stored value at its displayed eight-decimal precision. A direct algebraic check (the uncorrected sandwich SE multiplied by the manually computed combined scalar, compared with the library's own corrected SE) leaves a residual of 0.0 in all 24 cells.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

A reconciled SE does not by itself reconcile confidence intervals and *p*-values, because these also depend on the reference distribution. `linearmodels` computes its native intervals and *p*-values from a *t* distribution on `df_resid` $= N - K - G$, which counts every absorbed entity effect (1,571 to 19,918 in these cells, against $G-1$ of 352 to 3,114). Script 24 therefore computes confidence intervals and *p*-values explicitly from the corrected SE with Student *t*(*G*−1), the stored pipeline's reference distribution, and does not use the library's native values. Against the stored values, the maximum absolute differences over the 24 cells are 1.4×10⁻¹³ (lower CI bound), 7.6×10⁻¹⁴ (upper CI bound) and 1.2×10⁻¹³ (*p*), all within the script's "exact" tolerance of 10⁻⁹. The native `df_resid`-based values, shown for contrast only, differ by up to 0.0065 in a CI bound and 0.00069 in *p* in three of the six Ghana cells, which have the smallest cluster count (*G* = 353). Full detail is in `docs/provenance/independent_audit_v1_2026-10-07/09_update_2026-10-07_pass4.md`; the per-cell table is RESTRICTED. None of this changes the stored, authoritative SE in the output of `16_estimate_preliminary.py`. That estimator's formula was correct throughout; what was corrected is the covariance configuration of the *validation* scripts, not the pipeline being validated. The SE in Table B.2 is kept as originally run, and the CIs and *p*-values printed by script 20 itself, which use the native reference, are not reported here.

```{=latex}
\par\endgroup
```

**Coverage across the 291 historical models.** The verification described above covers the following, and no more:

1. All 24 primary established-date cells (2 products × 3 outcomes × Ghana, Kenya, Nigeria and pooled) were re-estimated with a second library on separately rebuilt samples: β, SE, N and G by script 21, then SE, CI and *p* under the corrected covariance setting by script 24.
2. Two further cells, both unweighted counterparts, were re-estimated individually: `m0005` by script 17 and `m0008` by script 20.
3. The remaining 265 models were not re-estimated with a second implementation. They were checked only internally: by the estimator's own absorbed-column and rank safeguards and by the same-function verification rerun described in Section B.4, which reproduces the output but is not an independent implementation.

**What this verification establishes, and what it does not.** It establishes that the reported pooled coefficient and its standard error are computationally correct: they are the numbers that the documented specification produces when it is implemented correctly in a second, independent library with an equivalent covariance configuration. It does not establish that the specification identifies a causal effect. It does not show that the samples represent the populations of the surveyed countries, that the results hold outside them, that the weighting and selection limitations are resolved, or that the result is robust to the number of cells tested; no multiplicity adjustment is applied. Nor does it place this cell in a higher *reporting* tier than its sibling historical models, all of which share the same unresolved documentation issues (Section 6; `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md`).

## B.3 Design checks applied to all 24 primary historical models

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

The following were checked programmatically for all 24 primary models (`scripts/historical_wash/19_check_model_design.py`): record-key uniqueness; the cluster-to-survey mapping (one survey per cluster); country weight totals equal to $N/M$ within each model's own estimation sample (relative tolerance 10⁻⁶); full design-matrix rank, meaning that the rank recorded by the estimator equals the number of retained regressors; and the absence of singleton clusters in the final estimation data. All checks pass. The per-model results are public (`docs/provenance/historical_wash_preliminary_estimates_v1/design_checks_per_model_PRELIMINARY_AGGREGATE.csv`, 24 rows); the summary file is RESTRICTED (`data/processed/estimation/run_20261006T185646Z/design_checks_20261006T190020Z/design_checks_summary.json`).

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

$M$ is the number of countries in that particular model: $M = 1$ for the 18 country-specific models and $M = 3$ for the 6 established-date pooled models, not $M = 3$ for all 24. The historical scripts set each country's weight total to $N/M$; the baseline pooled models set each country's total to 1 (Section 4.5). The two differ by the common constant $N/M$, which changes neither the weighted least-squares coefficients nor the cluster-robust variance: multiplying every weight by the same constant scales the bread of the sandwich by its inverse and the meat by its square, and the two cancel. Equal country weight totals do not mean equal influence on the pooled slope, which depends on each country's residual exposure variation (Section 4.5). In the design-check script itself, the weight check is described as "N / K" (comment and output field `country_weight_totals_equal_N_over_K`), with K meaning the number of countries; `equal_country_weights()` in `16_estimate_preliminary.py` uses K in the same sense. This appendix writes $M$ for that count. Elsewhere in the design-check script, the variable `K` is the regressor count, which is also this appendix's $K$.

```{=latex}
\par\endgroup
```

## B.4 Estimator safeguard: the exposure-absorption and rank-deficiency defect, and its resolution (2026-10-10)

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

An external independent audit (`Independent_Thesis_Audit_2026-10-10.md`, which is not in this repository; its finding R05 and the resolution are recorded in `docs/provenance/independent_audit_resolution_v1_2026-10-10.md`) identified a genuine code defect in the `fit()` function of `scripts/historical_wash/16_estimate_preliminary.py`. The function's absorbed-column filter dropped any column with zero within-cluster variation after weighted demeaning, but the exposure coefficient and its variance were then read by **fixed array position** (`beta[0]`, `V[0,0]`), not by the retained variable's name. Suppose the exposure variable $E$ itself were absorbed by this filter. The function's earlier check on the raw standard deviation would not catch this, because it tests *raw* (between-cluster) variation, not *within-cluster* variation. The next retained column would then silently occupy position 0 after the drop, and its coefficient would be reported as if it were $E$'s. Separately, the function computed a design-matrix rank but never compared it with the number of retained columns before using a pseudoinverse to solve for the coefficients. A rank-deficient retained design (for example, from an accidental exact collinearity between the exposure and a retained control) would therefore have returned a minimum-norm pseudoinverse solution silently, instead of flagging that the coefficient is not identified.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**Fix.** The function now (a) checks explicitly that `"E"` survives the absorbed-column filter and refuses to proceed if it does not (`status: "non_estimable_exposure_absorbed"`); when $E$ survives, its coefficient and variance are retrieved by its retained name and index rather than by position. It also (b) checks that the rank of the retained design matrix equals its column count before computing coefficients, and refuses (`status: "non_estimable_rank_deficient"`) rather than returning a pseudoinverse-based estimate if not. Neither change alters the computation for an estimable, full-rank case with $E$ retained. The ordinary path recovers the identical coefficient, standard error and every other reported statistic, because $E$ is always constructed as the first design-matrix column and so still occupies position 0 whenever it is retained.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**Targeted tests** are tracked at `scripts/historical_wash/26_test_fit_safeguard.py`. They use synthetic data only, run against the actual patched function through a direct import (not a reimplementation), and are re-run with `python 26_test_fit_safeguard.py` from that directory. The four cases are: (a) an ordinary estimable exposure, with genuine between- and within-cluster variation, which is estimated normally and recovers the simulated coefficient; (b) an exposure that varies between clusters but is constant within each cluster, the exact failure mode described above, which is correctly refused as `non_estimable_exposure_absorbed` with no `beta_per_point`, `se_CRV1` or `p_value` returned; (c) an exposure made exactly collinear with a retained nuisance control after demeaning, correctly refused as `non_estimable_rank_deficient`; and (d) a directly rank-deficient retained design created by a duplicated dummy block, correctly refused as `non_estimable_rank_deficient`. All four tests pass, according to the project's recorded run; they were not re-run in preparing this appendix.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**Verification that no published model was affected.** The patched script was re-run in full against the actual restricted inputs (`data/processed/analysis_samples/run_20261006T184744Z/` and `data/processed/child_exposure/run_20261006T183803Z/`, confirmed by SHA-256 to be bit-identical to the inputs of the original stored run). It wrote a fresh 291-model output to a new timestamped folder (`data/processed/estimation/run_20261010T140944Z/`, RESTRICTED) and left the original `run_20261006T185646Z/` unchanged. This rerun uses the same estimator function and the same inputs, so it shows that the patch left the output unchanged; it is not an independent implementation. A tracked comparison script, `scripts/historical_wash/27_compare_fit_safeguard_verification_run.py` (paths passed as `--original` and `--verification`; no restricted path is hard-coded as a requirement), produced a public, machine-readable comparison summary. All 291 model IDs are present in both runs, with no duplicates. All six specification fields (`family`, `product`, `outcome`, `sample_group`, `window`, `weighted`) match in every row, and both runs' `status` column reads `estimated` for all 291 rows. The maximum absolute difference is exactly 0.0 in each of the 15 numeric columns checked: the coefficient, SE and both CI bounds at both the per-point and the per-10-point scale, the *p*-value, `E_within_sd`, `E_residual_sd_after_controls`, `N`, `G_clusters`, `K_regressors` and `rank`. This is the exact list, not an unenumerated "every column". The two runs' output CSV files are also byte-for-byte identical (identical SHA-256 hash), a stronger result than the per-column check requires.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**Same-day correction (2026-10-10).** The comparison script's overall-success flag was found not to account for a value that is finite on one side and NaN or infinite on the other, for duplicate IDs, for missing required columns, or for a NaN-versus-infinity difference. All of these are now fixed and covered by synthetic regression tests (`scripts/historical_wash/28_test_compare_fit_safeguard_run.py`). Re-running the corrected, stricter comparison on the same two runs reaches the same conclusion (`docs/provenance/fit_safeguard_verification_comparison_v2_2026-10-10.json`); the original, pre-correction summary is kept at `_v1_2026-10-10.json` for the record. Together, these results confirm directly, rather than by inference from the earlier design checks, that none of the 291 published historical models was affected by this defect: in every one, $E$ was retained and the design matrix had full rank.


```{=latex}
\par\endgroup
```