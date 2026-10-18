# 5. Results

Every table in this section is taken directly from the authoritative, validated output files listed in Appendix A; no coefficient was computed for this chapter. Coefficients are reported with 95% confidence intervals, except Table 5.4 (coefficients and p-values only). P-values are shown to three decimal places when at least .0005, and as "<.001" otherwise; full precision is stored in the authoritative files. Where a model has two inference conventions, both are labelled (Section 4.5), and prose uses the primary convention unless the sensitivity is named.

## 5.1 Household WASH

**Table 5.1 — Household WASH: region-FE and cluster-FE results.**

| Outcome | Water β [95% CI], *p* | Sanitation β [95% CI], *p* | N | Clusters |
|---|---|---|---|---|
| **Region FE** |
| HAZ | −0.035 [−0.110, 0.040], .357 | 0.022 [−0.045, 0.089], .522 | 36,040 | 4,426 |
| WAZ | 0.021 [−0.038, 0.081], .487 | 0.045 [−0.010, 0.100], .109 | 36,308 | 4,426 |
| WHZ | 0.050 [−0.015, 0.116], .130 | 0.046 [−0.011, 0.103], .116 | 36,145 | 4,426 |
| **Cluster FE (main household specification; PRIMARY inference convention)** |
| HAZ | −0.085 [−0.175, 0.004], .062 | 0.026 [−0.058, 0.109], .548 | 36,040 | 4,426 |
| WAZ | −0.029 [−0.100, 0.043], .435 | 0.052 [−0.015, 0.120], .130 | 36,308 | 4,426 |
| WHZ | 0.012 [−0.062, 0.085], .758 | 0.053 [−0.014, 0.119], .122 | 36,145 | 4,426 |

Household water and sanitation are entered together in every model (Sections 4.1, 4.2). No household coefficient reaches significance at the 5% level in the cluster-fixed-effects specification, this thesis's main household result and the one least exposed to cluster-level confounding; water–HAZ crosses the 10% threshold. Non-significance is read as inconclusive, not as proof no association exists. Under the more conservative FULL_DUMMY_DF sensitivity, the cluster-FE p-values widen to .080 (water–HAZ) and .574 (sanitation–HAZ) — the same conclusion, using the normal reference distribution the baseline pipeline computes (Section 4.5), not the Student *t*(*G*−1) distribution used for the historical extension.

## 5.2 Community WASH: the adjustment path

**Table 5.2 — Community WASH: the four-stage adjustment path (HAZ).**

| Stage | Water β [95% CI], *p* | Sanitation β [95% CI], *p* |
|---|---|---|
| Minimally adjusted | 0.447 [0.311, 0.584], <.001 | 0.472 [0.356, 0.587], <.001 |
| + child controls | 0.395 [0.263, 0.527], <.001 | 0.452 [0.340, 0.565], <.001 |
| + socioeconomic status | 0.127 [0.010, 0.244], .034 | 0.008 [−0.117, 0.133], .900 |
| + SES + region FE (fully adjusted) | 0.033 [−0.083, 0.150], .573 | 0.008 [−0.113, 0.129], .894 |

::: {.tablenote}
*Note.* HAZ; N = 36,985, 4,434 clusters, all stages; coefficients per full $[0,1]$ unit of community coverage (not per 10 points). Slightly larger than Table 5.1/5.3's 36,040-child sample, since this specification does not require household WASH to be classifiable. Table 5.3's joint model, on the common sample, is this thesis's like-for-like household/community comparison.
:::

The community coefficients, entered together at every stage, are large and highly significant before adjustment, attenuating sharply as controls are added; neither is significant fully adjusted. This pattern is consistent with confounding by local socioeconomic conditions, but does not, alone, establish it as the sole explanation — a change in measurement structure as controls absorb variance could produce the same pattern. The same four-stage pattern holds for WAZ and WHZ, except WHZ's water association is already small and insignificant before adjustment (0.033, *p* = .545). Across all three outcomes, the fully adjusted specifications (here and Table 5.1) show no consistent WASH–outcome association — inconclusive evidence, not proof WASH has no true relationship with child growth.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.92\textwidth]{\ThesisRoot/figures/figure2_model4_coefficient_forest.png}
\ThesisFigureCaption{5.1}{Fully adjusted community water and sanitation coefficients (Table 5.2's final stage), pooled and by country, with 95\% confidence intervals.}
\end{figure}
```

Figure 5.1 breaks the fully adjusted stage out by country, for the same model, not a separate adjustment path. Of 30 country–outcome–exposure cells, one reaches significance at 5%: Nigeria's community sanitation–HAZ coefficient (−0.184, *p* = .035), already in Table 5.4. Several non-significant cells have comparable or larger point estimates — Ethiopia's sanitation coefficients for WAZ (0.186) and WHZ (0.187) exceed Nigeria's in magnitude — but wider confidence intervals that include zero, consistent with Ethiopia's smaller country subsample; their non-significance reflects imprecision, not a smaller true association, and the pooled null in Table 5.2 should not be read as averaging a uniformly small set of country effects.

## 5.3 Joint household/community model

**Table 5.3 — Joint household/community model: all four WASH terms entered together.**

| Exposure | β [95% CI] | *p* |
|---|---|---|
| **HAZ** |
| Household water | −0.085 [−0.167, −0.003] | **.043** |
| Household sanitation | 0.024 [−0.047, 0.096] | .507 |
| Community water | 0.120 [−0.008, 0.248] | .066 |
| Community sanitation | −0.018 [−0.148, 0.112] | .784 |
| **WAZ** |
| Household water | −0.015 [−0.084, 0.055] | .677 |
| Household sanitation | 0.039 [−0.020, 0.098] | .191 |
| Community water | 0.081 [−0.021, 0.184] | .121 |
| Community sanitation | 0.022 [−0.092, 0.136] | .706 |
| **WHZ** |
| Household water | 0.039 [−0.038, 0.117] | .318 |
| Household sanitation | 0.036 [−0.025, 0.096] | .244 |
| Community water | 0.019 [−0.099, 0.137] | .750 |
| Community sanitation | 0.045 [−0.070, 0.160] | .446 |

::: {.tablenote}
*Note.* N = 36,040 (HAZ), 36,308 (WAZ), 36,145 (WHZ); 4,426 clusters each.
:::

One cell reaches significance at 5%: household water for HAZ, conditional on the other three terms (β = −0.085, *p* = .043), unexpectedly negative. Household and community water are correlated, and this is one significant cell among twelve in this table; it is reported as a single finding, not treated as central, and not read as evidence that improved household water is harmful.

```{=latex}
\clearpage
```
## 5.4 Specification sensitivity: Nigeria community sanitation

**Table 5.4 — Nigeria community sanitation–HAZ: specification-sensitivity results.**

| Specification | Sanitation–HAZ β | *p* |
|---|---|---|
| No controls | 0.274 | .004 |
| + child controls | 0.296 | .001 |
| + socioeconomic controls | −0.457 | <.001 |
| + region FE | −0.184 | .035 |
| Household cluster FE (own-household sanitation) | −0.007 | .919 |

The coefficient changes sign and grows in absolute size as controls are added sequentially. Removing wealth quintile alone from the full control set moves it from −0.457 back to −0.196, the largest movement from any single block — sensitivity to specification, not proof wealth drives the reversal. The household-level coefficient for Nigeria is close to zero and not significant: the community-level, region-FE estimate is **not stable across specifications**, not evidence that improved sanitation harms growth in Nigeria. Appendix B.5 re-estimates the same fully adjusted community model under the binary WHO cutoffs, an alternative operationalisation of the same anthropometric measurements rather than an independent sample: it finds three, not one, nominally significant cells among 30, including Nigeria's sanitation–stunted coefficient in the same direction as here.

## 5.5 Current-age heterogeneity

Six current-age bands (0–5 to 48–59 completed months, 12–23 as reference) replace the continuous age control (Section 4.4). Of twelve exposure-specific joint interaction tests (two exposures × three outcomes × two fixed-effects structures, $\chi^2$, 5 restrictions each), eleven of twelve reject no heterogeneity at 5% (exception: water–WHZ under region FE, *p* = .300); the combined ten-term tests reject in all six combinations (largest *p* = .019). The household-WASH association with current outcomes therefore varies with current age in most specifications tested — secondary evidence about the *current* survey-date association only, which does not reconstruct any child's actual early-life exposure, the question the historical extension addresses under its own limitations.

## 5.6 Historical extension: primary established-date models

All cells come from the primary weighted models, post-12-month window, established-date sample (Ghana 2014, Kenya 2014, Nigeria 2018), per 10 percentage points of IHME-modelled local coverage — an area average within each child's buffer, not a household record (Section 3.5). These are weighted conditional associations among eligible measured children, not population-representative, with confidence intervals and p-values from the Student *t*(*G*−1) distribution.

**Table 5.5 — Historical extension: primary established-date water (W_IMP) estimates, with sample sizes.**

**Water (W_IMP):** coefficients per 10 percentage points

| Sample | β [95% CI] | *p* | N / G |
|---|---|---|---|
| **HAZ** |
| Ghana 2014 | 1.65 [0.34, 2.96] | .014 | N1,940 / G353 |
| Kenya 2014 | −0.61 [−2.07, 0.86] | .417 | N14,166 / G1,498 |
| Nigeria 2018 | 0.70 [0.15, 1.25] | .013 | N6,912 / G1,263 |
| Pooled established | **1.03 [0.51, 1.54]** | **<.001** | N23,018 / G3,114 |
| **WAZ** |
| Ghana 2014 | 1.06 [−0.16, 2.28] | .088 | N1,940 / G353 |
| Kenya 2014 | −0.22 [−1.30, 0.86] | .690 | N14,166 / G1,498 |
| Nigeria 2018 | 0.45 [0.00, 0.90] | .050 | N6,951 / G1,264 |
| Pooled established | 0.65 [0.20, 1.10] | .005 | N23,057 / G3,115 |
| **WHZ** |
| Ghana 2014 | −0.00 [−1.16, 1.16] | .997 | N1,940 / G353 |
| Kenya 2014 | −0.16 [−1.29, 0.96] | .776 | N14,166 / G1,498 |
| Nigeria 2018 | −0.05 [−0.48, 0.38] | .809 | N6,942 / G1,264 |
| Pooled established | −0.08 [−0.50, 0.35] | .717 | N23,048 / G3,115 |

::: {.tablenote}
*Note.* N and G are children and clusters in each country/outcome's own estimation sample.
:::

**Table 5.6 — Historical extension: primary established-date sanitation (S_IMP) estimates.**

**Sanitation (S_IMP):** coefficients per 10 percentage points

| Sample | β [95% CI] | *p* |
|---|---|---|
| **HAZ** |
| Ghana 2014 | −2.48 [−4.91, −0.05] | .046 |
| Kenya 2014 | −0.21 [−0.53, 0.11] | .190 |
| Nigeria 2018 | 0.20 [−0.34, 0.75] | .467 |
| Pooled established | −0.10 [−0.37, 0.17] | .483 |
| **WAZ** |
| Ghana 2014 | −0.08 [−2.04, 1.88] | .935 |
| Kenya 2014 | −0.15 [−0.38, 0.09] | .223 |
| Nigeria 2018 | 0.02 [−0.44, 0.48] | .937 |
| Pooled established | −0.07 [−0.29, 0.14] | .511 |
| **WHZ** |
| Ghana 2014 | 1.64 [−0.27, 3.56] | .092 |
| Kenya 2014 | 0.00 [−0.22, 0.22] | .980 |
| Nigeria 2018 | −0.17 [−0.59, 0.24] | .407 |
| Pooled established | −0.03 [−0.24, 0.17] | .742 |

::: {.tablenote}
*Note.* Sample sizes identical to Table 5.5 for each outcome/country; shown once there.
:::

The pooled water–HAZ coefficient (1.03, *p* < .001) is this section's selected headline. It is **not** the only nominally significant cell: six of 24 reach *p* < .05 — pooled water–HAZ, pooled water–WAZ, Ghana water–HAZ, Nigeria water–HAZ, Nigeria water–WAZ (*p* = .0498) and Ghana sanitation–HAZ (negative). It was chosen as headline because it is the pooled estimate for this thesis's primary outcome and window, proposed in a dated specification document before any coefficient was estimated (Section 6.4), not because it is the only significant result. All 24 primary cells were independently reconstructed with a different estimation library on a separately rebuilt sample, matching stored values (Appendix B.2) — confirming the specification, correctly implemented, produces these numbers, not a multiplicity correction and not evidence of causality.

**Weighted vs. unweighted.** The pooled coefficient is sensitive to the equal-country weighting convention: 1.03 weighted versus 0.41 [0.03, 0.80], *p* = .035, unweighted on the identical 23,018 observations — a disclosed sensitivity (Section 4.5), not evidence either weighting is more "correct"; equal weight totals do not give equal influence on the pooled slope, which also depends on each country's residual exposure variation.

**Residual exposure variation.** The pooled model's residual within-cluster exposure standard deviation is 0.43 percentage points; the conventional 10-point coefficient scale is therefore approximately 23 times that standard deviation — a scale benchmark, not a single identifying contrast or a bound on observed changes. One residual SD corresponds to approximately 0.044 HAZ standard deviations.

## 5.7 Alternative windows and common-sample comparison

**Table 5.7 — Historical extension: alternative exposure-window and common-sample comparison (pooled water–HAZ).**

| Window | Pooled water–HAZ β [95% CI] | Sample |
|---|---|---|
| Post-12-month (main) | 1.03 [0.51, 1.54] | Own-eligible, N = 23,018 |
| Birth-year | 0.54 [0.12, 0.96] | Own-eligible |
| Prenatal (9 months) | 0.64 [0.24, 1.03] | Own-eligible |
| Post-24-month | 1.75 [0.81, 2.70] | Own-eligible |
| Post-12-month, common-sample | 1.64 [0.68, 2.60] | All-window-eligible, N = 16,419 |

::: {.tablenote}
*Note.* Per 10 percentage points, as Table 5.5. "Own-eligible" is each window's own sample; the common sample is eligible under all four.
:::

The first four rows each use their own window's eligible sample, so comparing them changes window and sample at once. The last row instead holds post-12-month fixed and changes only the sample, 1.03 to 1.64 — a **sample-composition effect**, not evidence favouring one window's validity. The table gives no like-for-like comparison of all four windows on one sample. No window was selected for its coefficient's significance; all four were listed together in the same dated pre-estimation specification (Appendix C).

## 5.8 Further sensitivity: wealth, spatial method, completion rule

**Table 5.8 — Historical extension: further sensitivity of pooled water–HAZ.**

| Sensitivity | Pooled water–HAZ β [95% CI] |
|---|---|
| Main (post_12m, weighted) | 1.03 [0.51, 1.54] |
| Wealth quintile added | 1.01 [0.50, 1.52] |
| Containing-pixel assignment (vs. buffer average) | 0.68 [0.26, 1.10] |
| Rural 10 km buffer (urban unchanged) | 1.01 [0.42, 1.60] |
| Stricter completion rule (+1 month) | 0.95 [0.43, 1.47] |
| Excluding Ghana (DHS/IHME input overlap) | 0.74 [0.24, 1.24] |

::: {.tablenote}
*Note.* Excluding Ghana pools Kenya and Nigeria only and is not overlap-free: Kenya's own DHS survey also feeds the IHME water product (Section 6.5).
:::

Adding wealth leaves the coefficient essentially unchanged, showing only that it is not sensitive to this adjustment; it neither establishes mediation nor adjudicates the competing confounding concern (Section 3.8), nor bears on cluster-fixed-effects absorption (Section 4.2). The spatial-method and completion-rule sensitivities move the coefficient by amounts smaller than, or comparable to, the weighted/unweighted gap; none is privileged over the main specification.

## 5.9 Ethiopia: provisional, outside the established-date sample

Ethiopia's three interview-date candidates are not equally valid. Candidate C1's 30-day Ethiopian-calendar arithmetic has already been shown invalid for the delivered date fields, independently of the WASH analysis (Appendix C); it is excluded from every reporting table. Candidates C2 and C3 remain provisional, neither independently validated; they agree closely (water–HAZ: −0.39 both; sanitation–HAZ: −0.45 both; all four confidence intervals include zero). These are reported only as an exploratory sensitivity, never pooled into or compared with the established-date headline results.
