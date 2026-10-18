# Appendix B — Model specifications, inference conventions, and independent verification

The estimating equations are stated in Chapter 4 (Sections 4.1–4.6). This appendix records how they are implemented for inference and how far the implementation has been verified: the baseline household cluster-fixed-effects model (Section B.1), the historical extension's independent re-estimation (Section B.2), the design checks applied to all 24 primary historical models (Section B.3), and an estimator safeguard added after an external audit (Section B.4). Figures marked RESTRICTED come from execution logs and output folders that contain or derive from restricted microdata; the full execution logs, diagnostic scripts, and byte-for-byte comparison records underlying every verification summarised in this appendix are preserved in the project's own `docs/provenance/` directory and are not reproduced step by step here.

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

The two conventions differ only in whether the small-sample CRV1 correction also penalises degrees of freedom for the absorbed cluster dummies. FULL\_DUMMY\_DF does; PRIMARY does not, following the project's cross-validated adjudication against `linearmodels.PanelOLS(auto_df=True)` [@Sheppard2025Linearmodels] (`docs/provenance/cluster_fe_inference_adjudication.md`). Only standard errors, confidence intervals and *p*-values differ; the point estimates remain unchanged. The adjudicated PRIMARY convention is the one presented in the abstract, the introduction and the conclusion; the FULL\_DUMMY\_DF sensitivity is reported next to it in Section 4.5 and Section 5.1. The correction is $c = \frac{G}{G-1}\times\frac{N-1}{N-K}$, where PRIMARY counts $K=18$ demeaned regressors (no constant, no PSU dummies) and FULL\_DUMMY\_DF counts every absorbed PSU dummy as an estimated parameter ($K = 18+4{,}426$), multiplying the PRIMARY standard error by $\sqrt{(N-18)/(N-4{,}444)}$ (1.0677 for HAZ). The baseline code applies no singleton-cluster exclusion, so $G$ counts every PSU in the estimation sample (Section 4.5); the region-fixed-effects models instead use explicit region dummies and the normal reference distribution throughout, and are not part of Table B.1. The baseline pipeline's own executed run log records `use_t: False`; independent recomputation confirms its stored p-values match a normal (z) reference distribution, not *t*(*G*−1), to more than ten decimal places (e.g. the household water–HAZ cell's two candidate values, 0.0617391913770433 vs. 0.0618052, both round to the displayed .062, which is why a rounded-table check alone would miss the difference). A secondary cross-check against `linearmodels.PanelOLS` reproduces the stored PRIMARY standard errors once the library's `group_debias` adjustment is matched to the native estimator's own convention; the stored, published standard errors in Table B.1 come from `statsmodels`, not from this or any `linearmodels` cross-validation.

**The historical and baseline pooled-weighting conventions differ only by a reporting-level constant (Section 4.5).** Both give every country an equal total weight; the historical pipeline additionally multiplies every weight by $N/M$ ($N$ = estimation-sample size, $M$ = number of countries), so each country's weights sum to $N/M$ rather than $1$. Because $N/M$ is the same constant for every observation in a given model, and weighted least squares with its cluster-robust sandwich variance is invariant to rescaling every weight by one common constant, this changes no reported coefficient, standard error, confidence interval, or p-value — confirmed directly by refitting under both conventions, which reproduces identical coefficients and SEs to machine precision.

```{=latex}
\par\endgroup
```

## B.2 Independent verification of the pooled historical model (Section 4.6, Section 5.6)

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

This thesis's own pipeline (`scripts/historical_wash/16_estimate_preliminary.py`) estimates all 291 historical models with a hand-written estimator based on weighted within-cluster demeaning. An independent check re-estimated four representative country-specific cells (Ghana water–HAZ, weighted and unweighted; Ghana sanitation–WAZ; Nigeria sanitation–HAZ) using a separately rebuilt sample and an explicit-dummy CRV1 implementation: coefficients agreed within $3\times10^{-14}$, standard errors within a relative $7.5\times10^{-10}$, and N and G were identical in all four cells.

```{=latex}
\par\endgroup
```

That check did not cover the pooled multi-country model, the headline result of the historical extension. A separate, independent re-estimation rebuilt the estimation sample directly from the analysis-candidates stage (reproduced in Appendix A, Section A.3) and estimated it with `linearmodels.PanelOLS`, a different library from the project's own hand-written estimator, using cluster fixed effects and clustered CRV1 standard errors, under both inference conventions and both the weighted and unweighted specification. The rebuild is independent in filtering, weighting, design construction and estimation, but reads the same analysis-candidates file as the main pipeline, so it does not re-verify the variable constructions (exposure assignment, outcome validity, birth year, calendar age, weight field) built upstream of that file.

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

Note: Stored values are from `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` (rows `m0004` and `m0008`; β per 10 for `m0004` is 1.025553067200643 at full precision). The independent script compared its estimate with six-decimal constants written into its own code, so the 6.7×10⁻⁸ in the β row measures that rounding, not a disagreement between estimators; a full-precision comparison for this cell gives $2.4\times10^{-14}$. The independent rank is that of the regressor matrix before the fixed-effect transformation; the stored rank is that of the weighted within-transformed matrix. Independent values are carried from a RESTRICTED execution log; where only rounded values are recorded, agreement is stated at that precision.
:::

An initial run of the independent script used a single pooled birth-year reference cell (rather than a country-specific reference year) and omitted the child's own age in months as a control, producing β per 10 points = 1.385 against the stored 1.026 — a roughly 35% discrepancy, despite the sample size, cluster count, and exposure mean/SD matching the stored values exactly. A dedicated diagnostic traced this gap by decomposing the two changes on the transformed (weighted, within-cluster-demeaned) design the estimator actually uses, the space in which the exposure coefficient is identified. The two birth-year reference schemes were shown to be equivalent nuisance specifications for the exposure coefficient: both demeaned birth-year blocks span equal subspaces, the exposure's own residual after each full nuisance specification is identical at floating-point precision ($\le2.2\times10^{-16}$ relative), and the mechanism is that Nigeria's birth-year dummies under the single-reference scheme sum to its country indicator, which the cluster fixed effect absorbs regardless of scheme. The age-in-months control, not birth-year coding, accounts for the full gap: including it reproduces the stored coefficient (1.0255530672006674) under either birth-year scheme, and excluding it reproduces the original attempt's value (1.3852855197991372) under either scheme — differences of one to three units in the last place of a double-precision number. This is the diagnostic's finding on a reconstruction of the described design; it is not a claim about what the specific, unpreserved original code did, and not an exact recovery of that code's reported output. The complete five-step decomposition, tolerances, and execution log are in `docs/provenance/` and the diagnostic script's own docstring (RESTRICTED execution log; the values above are reproduced from it).

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

**The SE difference in Table B.2 is a validation-script covariance-setting discrepancy, not a flaw in the published numbers.** The pipeline's declared small-sample correction is $\frac{G}{G-1}\times\frac{N-1}{N-K}$, applied to the raw cluster-robust sandwich, with confidence intervals and *p*-values from a Student *t*(*G*−1) distribution; $K$ counts only the non-fixed-effect regressors (24 for the pooled cell). The independent script's original `PanelOLS` call applied only one of the two multiplicative factors this requires (`auto_df=True`, which correctly sets the degrees-of-freedom convention, but not the separate, opt-in `group_debias=True`, which applies the library's cluster-count adjustment). Adding `group_debias=True` and computing confidence intervals and *p*-values explicitly from the corrected SE with Student *t*(*G*−1) — rather than `linearmodels`' own native reference, which counts every absorbed entity effect in its degrees of freedom and differs by up to 0.0065 in a CI bound in the smallest-cluster-count cells — reconciles all 24 primary cells to the stored values at better than $10^{-9}$ precision. None of this changes the stored, authoritative standard errors in the output of the pipeline's own estimator; what was corrected is the covariance configuration of the independent validation script, not the pipeline being validated. The SE in Table B.2 is kept as originally run.

```{=latex}
\par\endgroup
```

**Coverage across the 291 historical models.** The verification described above covers the following, and no more: all 24 primary established-date cells (2 exposures × 3 outcomes × Ghana, Kenya, Nigeria and pooled) were re-estimated with a second library on separately rebuilt samples; two further unweighted-counterpart cells were re-estimated individually; the remaining 265 models were not re-estimated with a second implementation, and were checked only by the estimator's own internal safeguards (Section B.4).

**What this verification establishes, and what it does not.** It establishes that the reported pooled coefficient and its standard error are computationally correct: they are the numbers the documented specification produces when correctly implemented in a second, independent library with an equivalent covariance configuration. It does not establish that the specification identifies a causal effect, that the samples represent the surveyed countries' populations, that the weighting and selection limitations are resolved, or that the result is robust to the number of cells tested (no multiplicity adjustment is applied). Nor does it place this cell in a higher reporting tier than its sibling historical models, which share the same unresolved documentation issues (Section 6; `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md`).

## B.3 Design checks applied to all 24 primary historical models

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

The following were checked programmatically for all 24 primary models: record-key uniqueness; the cluster-to-survey mapping (one survey per cluster); country weight totals equal to $N/M$ within each model's own estimation sample (relative tolerance $10^{-6}$); full design-matrix rank (the rank recorded by the estimator equals the number of retained regressors); and the absence of singleton clusters in the final estimation data. All checks pass. The per-model results are public (`docs/provenance/historical_wash_preliminary_estimates_v1/design_checks_per_model_PRELIMINARY_AGGREGATE.csv`, 24 rows); the summary file is RESTRICTED.

```{=latex}
\par\endgroup
```

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

$M$ is the number of countries in that particular model: $M=1$ for the 18 country-specific models and $M=3$ for the 6 established-date pooled models, not $M=3$ for all 24. The historical scripts set each country's weight total to $N/M$; the baseline pooled models set each country's total to 1 (Section 4.5). The two differ by the common constant $N/M$, which changes neither the weighted least-squares coefficients nor the cluster-robust variance, since multiplying every weight by the same constant scales the sandwich's bread by its inverse and its meat by its square, and the two cancel. Equal country weight totals do not mean equal influence on the pooled slope, which depends on each country's residual exposure variation (Section 4.5).

```{=latex}
\par\endgroup
```

## B.4 Estimator safeguard: the exposure-absorption and rank-deficiency defect, and its resolution (2026-10-10)

```{=latex}
\begingroup\edef\ThesisSavedIndent{\the\parindent}\raggedright\parindent=\ThesisSavedIndent\relax\widowpenalty=10000\clubpenalty=10000
```

An external independent audit identified a genuine code defect in the historical pipeline's estimator (`docs/provenance/independent_audit_resolution_v1_2026-10-10.md`, finding R05): the absorbed-column filter dropped any column with zero within-cluster variation after demeaning, but the exposure coefficient and its variance were then read by fixed array position rather than by the retained variable's name. Had the exposure itself ever been absorbed by this filter, the next retained column would silently have occupied its position, and its coefficient would have been reported as if it were the exposure's. Separately, the function computed the design-matrix rank but never compared it with the retained column count before solving by pseudoinverse, so an accidental exact collinearity would have returned a silently under-identified estimate rather than an error.

```{=latex}
\par\endgroup
```

**Fix.** The estimator now refuses to proceed (rather than silently misreporting) whenever the exposure variable does not survive the absorbed-column filter, or whenever the retained design matrix is rank-deficient; when the exposure does survive, its coefficient and variance are retrieved by name, not by position. Neither change alters the computation for an estimable, full-rank case, since the exposure is always constructed as the first design-matrix column and so still occupies position 0 whenever it is retained. Four synthetic test cases (an ordinary estimable exposure; an exposure absorbed within every cluster; an exposure made exactly collinear with a retained control; a directly rank-deficient design) confirm the safeguard triggers exactly where intended and leaves the ordinary case unaffected.

**Verification that no published model was affected.** The patched estimator was re-run in full against the actual restricted inputs (confirmed by SHA-256 to be bit-identical to the inputs of the original stored run), writing a fresh 291-model output to a new run folder and leaving the original run's output unchanged. A machine comparison of the two runs found all 291 model IDs present in both with no duplicates, identical specification fields and `estimated` status in every row, and a maximum absolute difference of exactly 0.0 across all 15 numeric columns checked (coefficient, SE, both CI bounds at both scales, *p*-value, exposure variation diagnostics, N, G, K, rank); the two output files are byte-for-byte identical. This confirms directly, not by inference from the design checks alone, that none of the 291 published historical models was affected by this defect: in every one, the exposure was retained and the design matrix had full rank.
