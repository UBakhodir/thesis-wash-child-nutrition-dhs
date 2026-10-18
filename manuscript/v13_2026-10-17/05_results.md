# 5. Results

Every table in this section is taken directly from the authoritative, validated output files listed in Appendix A; no coefficient was computed for this chapter. Coefficients are reported with 95% confidence intervals, except in Table 5.4, which reports coefficients and p-values only. P-values are shown to three decimal places when the underlying value is at least .0005 and as "<.001" when it is smaller. Both forms are display precision only; the full-precision value of every cell is stored in the authoritative output files. Where a model has two inference conventions, both are labelled explicitly (Section 4.5), and the prose uses the primary convention unless the sensitivity convention is named.

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

Household water and sanitation are entered together in every model in Table 5.1 (Sections 4.1, 4.2). No household coefficient reaches significance **at the 5% level** in the cluster-fixed-effects specification, this thesis's main household result and the one least exposed to cluster-level confounding; water–HAZ does cross the 10% threshold. Non-significance is read as inconclusive, not as proof no association exists. Under the more conservative FULL_DUMMY_DF sensitivity (Section 4.5), the cluster-FE p-values widen to .080 (water–HAZ) and .574 (sanitation–HAZ), the same substantive conclusion, using the normal reference distribution the baseline pipeline's code actually computes (Section 4.5), not the Student *t*(*G*−1) distribution used for the historical extension (Section 4.6).

## 5.2 Community WASH: the adjustment path

**Table 5.2 — Community WASH: the four-stage adjustment path (HAZ).**

| Stage | Water β [95% CI], *p* | Sanitation β [95% CI], *p* |
|---|---|---|
| Minimally adjusted | 0.447 [0.311, 0.584], <.001 | 0.472 [0.356, 0.587], <.001 |
| + child controls | 0.395 [0.263, 0.527], <.001 | 0.452 [0.340, 0.565], <.001 |
| + socioeconomic status | 0.127 [0.010, 0.244], .034 | 0.008 [−0.117, 0.133], .900 |
| + SES + region FE (fully adjusted) | 0.033 [−0.083, 0.150], .573 | 0.008 [−0.113, 0.129], .894 |

::: {.tablenote}
*Note.* HAZ; N = 36,985 and 4,434 clusters in all four stages. This is the outcome-valid sample. It is slightly larger than the 36,040-child, 4,426-cluster common sample used in Table 5.1 and Table 5.3, because this table's community-only specification does not also require household WASH to be classifiable for every child. The attenuation pattern described below should therefore not be compared cell for cell with Table 5.1's household coefficients as if the two samples were identical. Table 5.3's joint model, estimated on the common sample, is this thesis's like-for-like comparison of household and community exposure.
:::

The community water and sanitation coefficients, entered together at every stage (Section 4.3), are large and highly significant before adjustment, attenuating sharply as socioeconomic status and region fixed effects are added; neither is significant at the fully adjusted stage. **This pattern is consistent with confounding by local socioeconomic conditions, but does not, on its own, establish it as the sole explanation**; a change in measurement structure as controls absorb variance could produce the same pattern. The same four-stage pattern holds for WAZ and WHZ, except that the WHZ water association is already small and insignificant before adjustment (0.033, *p* = .545) and remains so throughout. Across all three outcomes, the fully adjusted specifications (here and the household models in Table 5.1) show no consistent WASH–outcome association at either level — inconclusive evidence, not proof that WASH has no true relationship with child growth, a materially stronger claim than this design can support.

```{=latex}
\begin{figure}[H]
\centering
\includegraphics[width=0.65\textwidth]{\ThesisRoot/figures/figure2_model4_coefficient_forest.png}
\ThesisFigureCaption{5.1}{Fully adjusted community water and sanitation coefficients (Table 5.2's final stage), pooled and by country, with 95\% confidence intervals.}
\end{figure}
```

Figure 5.1 breaks that fully adjusted stage out by country, for the same model (region fixed effects, full control set), not a separate adjustment path. Of the 30 country–outcome–exposure cells shown, only one reaches significance at the 5% level: Nigeria's community sanitation–HAZ coefficient (−0.184, *p* = .035), already reported in Table 5.4. No other country shows a comparably sized or significant association, so the pooled null in Table 5.2 is not masking a consistent country-level pattern that happens to average to zero.

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
*Note.* N = 36,040 for the HAZ model, 36,308 for WAZ and 36,145 for WHZ, with 4,426 clusters in each. Each outcome uses its own common sample, so the sample is not literally identical across outcomes.
:::

One cell in this table reaches significance at the 5% level: household water for HAZ, conditional on community water and the other two WASH terms (β = −0.085, *p* = .043), and its sign is unexpectedly negative. Household and community water measures are correlated, and this is one significant cell among the twelve estimated in this table alone. The result is therefore reported as a single finding rather than treated as a central conclusion of this thesis, and it is not interpreted as evidence that improved household water is harmful.

## 5.4 Specification sensitivity: Nigeria community sanitation

**Table 5.4 — Nigeria community sanitation–HAZ: specification-sensitivity results.**

| Specification | Sanitation–HAZ β | *p* |
|---|---|---|
| No controls | 0.274 | .004 |
| + child controls | 0.296 | .001 |
| + socioeconomic controls | −0.457 | <.001 |
| + region FE | −0.184 | .035 |
| Household cluster FE (own-household sanitation) | −0.007 | .919 |

The Nigeria community sanitation–HAZ coefficient changes sign and grows in absolute size as controls are added sequentially (Table 5.4). Removing wealth quintile alone from the full control set moves the coefficient from −0.457 back to −0.196, the largest movement from any single control block — sensitivity to specification, not proof that wealth is the mechanism behind the reversal. The corresponding household-level coefficient for Nigeria is close to zero and not significant: this instability shows the community-level, region-fixed-effects estimate is **not stable across specifications**, not that improved sanitation harms child growth in Nigeria. The same fully adjusted coefficient, re-estimated with the binary WHO stunting cutoff in place of the continuous HAZ z-score, points the same direction and remains significant (Appendix B.5).

## 5.5 Current-age heterogeneity

In the heterogeneity models, six current-age bands (0 to 5, 6 to 11, 12 to 23, 24 to 35, 36 to 47, 48 to 59 completed months) replace the continuous age control, 12–23 months as reference (Section 4.4). Of twelve exposure-specific joint interaction tests (two exposures × three outcomes × two fixed-effects structures, each a $\chi^2$ test of five restrictions), **eleven of twelve reject the null of no heterogeneity** at the 5% level (the exception: the water interaction for WHZ under region fixed effects, *p* = .300); the combined ten-term tests ($\chi^2$, 10 df) reject in all six combinations (largest *p* = .019). The household-WASH association with current outcomes therefore varies with current age in most specifications tested. As Section 4.4 states, this is secondary evidence about the *current* survey-date association only: it compares children of different current ages at one survey date and does not reconstruct any child's actual early-life exposure, a question the historical extension below addresses under its own separate limitations.

## 5.6 Historical extension: primary established-date models

All cells below come from the primary weighted models with the post-12-month window, on the established-date sample (Ghana 2014, Kenya 2014, Nigeria 2018), reported per 10 percentage points of IHME-modelled local coverage: an area average within each child's buffer, not the source study's population-weighted aggregate or a record of household facilities (Section 3.5). These are weighted conditional associations among eligible measured children, not population-representative estimates, with confidence intervals and p-values from the Student *t*(*G*−1) reference distribution (Sections 3.8, 4.5). Every cell carries the same qualifications, discussed fully in Section 6; none is promoted above the others for being significant.

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
*Note.* Sample sizes (N children / G clusters) are identical to Table 5.5 for each outcome and country, because both exposures are estimated on the same anthropometric sample; shown once there rather than repeated here.
:::

The pooled established-date water–HAZ coefficient (1.03, *p* < .001) is this section's selected headline, the cell this thesis discusses in most depth. It is **not** the only nominally significant cell among the 24 shown above. At conventional *p* < .05, **six** of the 24 cells reach significance: pooled water–HAZ, pooled water–WAZ, Ghana water–HAZ, Nigeria water–HAZ, Nigeria water–WAZ (*p* = .0498) and Ghana sanitation–HAZ, the last in an unexpected negative direction. The displayed, rounded *p* = .050 for Nigeria water–WAZ in Table 5.5 should not be read as lying exactly at the threshold, because the underlying value is below .05. The pooled water–HAZ cell was chosen as the headline because it is the pooled, established-date estimate for this thesis's primary outcome and primary window, proposed as the primary configuration in a dated specification document before any coefficient was estimated (Section 6.4), not because it is the only significant result. Six cells reach significance, not one, and all six are shown in Table 5.5 and Table 5.6.

All 24 primary cells, including this headline, were independently reconstructed and re-estimated with a different estimation library on a separately rebuilt sample, matching the stored coefficients, standard errors, confidence intervals and p-values (Appendix B.2). This shows the documented specification, correctly implemented, produces these numbers; it is **not** a multiplicity correction, since no formal adjustment for testing 24 cells has been applied, and it does not establish causality.

**Weighted vs. unweighted, same observations.** The pooled water–HAZ coefficient is sensitive to the equal-country weighting convention: 1.03 weighted (equal country totals) versus 0.41 [0.03, 0.80], *p* = .035, unweighted on the identical 23,018 observations. This is a disclosed sensitivity to a stated design choice (Section 4.5), not evidence that either weighting is more "correct." Equal country weight totals do not give each country equal influence on the pooled slope, which also depends on each country's residual exposure variation. Neither estimate is population-representative (Section 3.8).

**Residual exposure variation and the 10-point scale.** The pooled water–HAZ model's residual within-cluster exposure standard deviation after all controls is 0.43 percentage points. The conventional 10-percentage-point coefficient scale is therefore approximately 23 times the residual exposure standard deviation that actually identifies the model — a scale benchmark, not a single identifying contrast or a bound on all observed within-cluster changes. One residual standard deviation of exposure corresponds to approximately 0.044 HAZ standard deviations. The 10-point coefficient should therefore be read as a reporting convention for comparability across studies, not as a description of a change that is typically observed within a cluster.

## 5.7 Alternative windows and common-sample comparison

The historical pipeline estimates 291 models in total: the 24 primary established-date cells of Section 5.6, their unweighted counterparts, and several further sensitivity families — alternative exposure windows, wealth adjustment, spatial-assignment method, completion-rule strictness, calendar-age construction, Ethiopia's provisional candidates, and DHS/IHME overlap exclusions (full counts in Appendix C). To avoid repeating every cell, only the pooled water–HAZ cells are shown below as the headline case; the corresponding sanitation and WAZ/WHZ sensitivity cells are neither more nor less favourable to a WASH association (most show the same wide, zero-spanning intervals as Section 5.6) and are available in full in the project's output tables, omitted here for brevity, not because water–HAZ happened to be significant.

**Table 5.7 — Historical extension: alternative exposure-window and common-sample comparison (pooled water–HAZ).**

| Window | Pooled water–HAZ β [95% CI] | Sample |
|---|---|---|
| Post-12-month (main) | 1.03 [0.51, 1.54] | Own-eligible, N = 23,018 |
| Birth-year | 0.54 [0.12, 0.96] | Own-eligible |
| Prenatal (9 months) | 0.64 [0.24, 1.03] | Own-eligible |
| Post-24-month | 1.75 [0.81, 2.70] | Own-eligible |
| Post-12-month, common-sample | 1.64 [0.68, 2.60] | All-window-eligible common sample, N = 16,419 |

::: {.tablenote}
*Note.* Coefficients are per 10 percentage points, as in Table 5.5. "Own-eligible" denotes each window's own eligible sample; the common sample contains only the children eligible under all four windows.
:::

Two different comparisons are possible in this table, and they answer different questions. The first four rows each use their own window's eligible sample, so comparing them changes both the window and the eligibility sample at once; a difference between, say, the birth-year and post-24-month rows cannot be attributed to the window alone. The last row instead holds the post-12-month specification fixed and changes only the sample, from that window's own eligible children (1.03) to the smaller set eligible under all four windows at once (1.64). This second comparison is the one that isolates a sample effect: children with complete 24-month windows differ systematically from the full post-12-month sample, so the shift from 1.03 to 1.64 is a **sample-composition effect**, not evidence favouring the validity of one window over another. The table does not give a like-for-like comparison of all four windows on one common sample; only the post-12-month window is shown on both its own sample and the common one. No window was selected because of the significance of its coefficient; all four were listed together in the same dated pre-estimation specification (Appendix C) and are reported together here.

## 5.8 Further sensitivity: wealth, spatial method, completion rule

**Table 5.8 — Historical extension: further sensitivity of pooled water–HAZ to wealth adjustment, spatial method, completion rule and the exclusion of Ghana.**

| Sensitivity | Pooled water–HAZ β [95% CI] |
|---|---|
| Main (post_12m, weighted) | 1.03 [0.51, 1.54] |
| Wealth quintile added | 1.01 [0.50, 1.52] |
| Containing-pixel assignment (vs. buffer average) | 0.68 [0.26, 1.10] |
| Rural 10 km buffer (urban unchanged) | 1.01 [0.42, 1.60] |
| Stricter completion rule (+1 month) | 0.95 [0.43, 1.47] |
| Excluding Ghana (DHS/IHME input overlap) | 0.74 [0.24, 1.24] |

::: {.tablenote}
*Note.* Coefficients are per 10 percentage points, as in Table 5.5. The row excluding Ghana pools Kenya and Nigeria only, and is not an overlap-free estimate: Kenya's own DHS survey also feeds into the IHME water product used as its exposure (Section 6.5), so excluding Ghana removes only one of the two established-date countries with this input overlap; every other row uses the three-country established-date sample.
:::

Adding wealth leaves the coefficient essentially unchanged (1.01 vs. 1.03), showing only that it is not sensitive to this particular adjustment; it neither establishes that wealth mediates the exposure nor adjudicates the competing mediator/confounder concern stated in Section 3.8, and it does not bear on cluster-fixed-effects absorption, which Section 4.2 separately shows is not how cluster fixed effects behave. The spatial-method and completion-rule sensitivities move the coefficient by amounts smaller than, or comparable to, the gap between the main weighted and unweighted estimates, and none is privileged over the main specification.

## 5.9 Ethiopia: provisional, outside the established-date sample

Ethiopia's three interview-date candidates are not treated as equally valid sensitivity evidence. Candidate C1 uses a 30-day Ethiopian-calendar arithmetic conversion that has already been shown, independently of the WASH analysis, to be invalid for the delivered recoded date fields (Appendix C). It is excluded from this section and from every reporting table, and its past numerical agreement with the other two candidates is not treated as evidence of robustness. Candidates C2 and C3 remain provisional, since neither has been independently validated. They agree closely with each other (water–HAZ: −0.39 for both; sanitation–HAZ: −0.45 for both; all four confidence intervals include zero). These estimates are reported here and in Appendix C only as an explicitly exploratory sensitivity analysis. They are never pooled into, or compared with, the established-date headline results above.
