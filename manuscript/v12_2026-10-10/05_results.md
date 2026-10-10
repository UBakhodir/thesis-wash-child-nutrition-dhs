# 5. Results

Every table in this section is reused directly from the authoritative, validated output files listed in Appendix A; no coefficient was computed for this chapter. Coefficients are reported with 95% confidence intervals and exact p-values throughout. Where two inference conventions exist for a model, both are labelled explicitly (Section 4.5); the primary convention is used in prose discussion unless the sensitivity convention is named.

## 5.1 Household WASH

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

No household-level water or sanitation coefficient reaches conventional significance **at the 5% level** in the cluster-fixed-effects specification, which is the specification this thesis treats as the main household result (Section 4.2): it compares households within the same DHS cluster, net of the covariates, and is the specification least exposed to cluster-level confounding of the two. (Household water–HAZ, *p* = .062, does cross a 10% threshold; this is stated explicitly here rather than left implicit in a blanket "not significant.") Non-significance here is read as an inconclusive association in this sample under this design, not as proof that no association exists — the confidence intervals remain wide enough (for example, water–HAZ spans −0.175 to +0.004) to be consistent with a range of true associations. Under the alternative, more conservative FULL_DUMMY_DF inference convention (Section 4.5), the household cluster-FE water–HAZ p-value is .080 and sanitation–HAZ is .574; both conventions lead to the same substantive conclusion for this pair of coefficients. These p-values and confidence intervals use the normal reference distribution, as the baseline pipeline's code actually computes (Section 4.5) — not the Student *t*(*G*−1) distribution used for the historical extension's inference (Section 4.6).

## 5.2 Community WASH: the adjustment path

| Stage | Water β [95% CI], *p* | Sanitation β [95% CI], *p* |
|---|---|---|
| Minimally adjusted | 0.447 [0.311, 0.584], <.001 | 0.472 [0.356, 0.587], <.001 |
| + child controls | 0.395 [0.263, 0.527], <.001 | 0.452 [0.340, 0.565], <.001 |
| + socioeconomic status | 0.127 [0.010, 0.244], .034 | 0.008 [−0.117, 0.133], .900 |
| + SES + region FE (fully adjusted) | 0.033 [−0.083, 0.150], .573 | 0.008 [−0.113, 0.129], .894 |

(HAZ; N = 36,985, 4,434 clusters, all four stages — the outcome-valid sample, slightly larger than the 36,040-child, 4,426-cluster common sample used in Table 5.1 and Table 5.3, because this table's community-only specification does not also require household WASH to be classifiable for every child. The attenuation pattern below should not be read as directly comparable, cell for cell, against Table 5.1's household coefficients on a literally identical sample; Table 5.3's joint model, estimated on the common sample, is this thesis's apples-to-apples household-versus-community comparison.) The community water and sanitation coefficients are large and highly significant before adjustment and attenuate sharply — losing significance entirely by the fully adjusted stage — as socioeconomic status and region fixed effects are added. **This attenuation pattern is consistent with confounding by local socioeconomic conditions, but it does not, on its own, establish confounding as the sole explanation**: the same pattern would also be produced by, for example, measurement structure changing as additional controls absorb variance, or by other specification features that happen to coincide with the added controls. The same four-stage pattern holds for WAZ and WHZ, with one difference worth stating precisely: the WHZ water association is already small and statistically insignificant even before adjustment (0.033, *p* = .545) and remains so throughout, unlike the HAZ and WAZ water associations, which start large and attenuate to insignificance. Across all three outcomes, the fully adjusted community specifications do not show a consistent association between improved WASH and child anthropometric outcomes, at either the household or the community level — a conclusion read here as "this sample does not provide clear evidence of an association once the obvious confounders are controlled," not as "WASH has no true relationship with child growth," a materially stronger claim this design cannot support.

## 5.3 Joint household/community model

| Outcome | Household water | Household sanitation | Community water | Community sanitation |
|---|---|---|---|---|
| HAZ | −0.085 [−0.167, −0.003], **.043** | 0.024 [−0.047, 0.096], .507 | 0.120 [−0.008, 0.248], .066 | −0.018 [−0.148, 0.112], .784 |
| WAZ | −0.015 [−0.084, 0.055], .677 | 0.039 [−0.020, 0.098], .191 | 0.081 [−0.021, 0.184], .121 | 0.022 [−0.092, 0.136], .706 |
| WHZ | 0.039 [−0.038, 0.117], .318 | 0.036 [−0.025, 0.096], .244 | 0.019 [−0.099, 0.137], .750 | 0.045 [−0.070, 0.160], .446 |

(N = 36,040 for the HAZ row, 36,308 for WAZ, 36,145 for WHZ — each this table's own common sample, not a literally identical sample across outcomes.) One cell in this table reaches conventional significance (5% level): household water conditional on community water, HAZ (β = −0.085, *p* = .043), in an unexpected (negative) direction. Given the correlation between household and community water measures, and that this is one significant cell among twelve estimated in this table alone, this result is reported as a single finding rather than treated as a central conclusion of this thesis; it is not interpreted as evidence that improved household water is harmful.

## 5.4 Specification sensitivity: Nigeria community sanitation

| Specification | Sanitation–HAZ β | *p* |
|---|---|---|
| No controls | 0.274 | .004 |
| + child controls | 0.296 | .001 |
| + socioeconomic controls | −0.457 | <.001 |
| + region FE | −0.184 | .035 |
| Household cluster FE (own-household sanitation) | −0.007 | .919 |

The Nigeria community sanitation–HAZ coefficient changes sign and more than doubles in magnitude as controls are added sequentially, and a block-by-block audit finds that removing wealth quintile alone from the full control set moves the coefficient from −0.457 back to −0.196 — the single largest movement of any control block, though this demonstrates sensitivity to specification, not proof that wealth is the specific mechanism behind the reversal. The corresponding household-level (cluster-fixed-effects) coefficient for Nigeria is close to zero and not significant. This instability is reported as evidence that the community-level, region-fixed-effects estimate for Nigeria sanitation is **not stable across specifications** and should not be read as evidence that improved sanitation harms child growth in Nigeria.

## 5.5 Current-age heterogeneity

Across the twelve water/sanitation joint-interaction tests estimated (two exposures × three outcomes × two fixed-effects structures), **eleven of twelve reject the null of no heterogeneity** at the 5% level; the single exception is the water interaction for WHZ under region fixed effects (*p* = .300). This indicates that the household-WASH association with current anthropometric outcomes varies with a child's current age in most of the specifications tested. As stated in Section 4.4, this is secondary evidence about the *current* survey-date association and does not identify a developmental mechanism or reconstruct any child's actual early-life exposure — that question is addressed only by the historical extension below, under its own, separate limitations.

## 5.6 Historical extension: primary established-date models

All cells below are the primary, post-12-month-window, weighted models (established-date sample: Ghana 2014, Kenya 2014, Nigeria 2018). Coefficient is per 10 percentage points of IHME-modelled local coverage. Every cell carries the same methodological qualifications stated in Section 3.8 and discussed fully in Section 6 — none is promoted above the others for being significant.

**Water (W_IMP)** — coefficient [95% CI], *p*

| Outcome | Ghana 2014 | Kenya 2014 | Nigeria 2018 | Pooled established |
|---|---|---|---|---|
| HAZ | 1.65 [0.34, 2.96], .014 | −0.61 [−2.07, 0.86], .417 | 0.70 [0.15, 1.25], .013 | **1.03 [0.51, 1.54], <.001** |
| WAZ | 1.06 [−0.16, 2.28], .088 | −0.22 [−1.30, 0.86], .690 | 0.45 [0.00, 0.90], .050 | 0.65 [0.20, 1.10], .005 |
| WHZ | −0.00 [−1.16, 1.16], .997 | −0.16 [−1.29, 0.96], .776 | −0.05 [−0.48, 0.38], .809 | −0.08 [−0.50, 0.35], .717 |

**Sanitation (S_IMP)** — coefficient [95% CI], *p*

| Outcome | Ghana 2014 | Kenya 2014 | Nigeria 2018 | Pooled established |
|---|---|---|---|---|
| HAZ | −2.48 [−4.91, −0.05], .046 | −0.21 [−0.53, 0.11], .190 | 0.20 [−0.34, 0.75], .467 | −0.10 [−0.37, 0.17], .483 |
| WAZ | −0.08 [−2.04, 1.88], .935 | −0.15 [−0.38, 0.09], .223 | 0.02 [−0.44, 0.48], .937 | −0.07 [−0.29, 0.14], .511 |
| WHZ | 1.64 [−0.27, 3.56], .092 | 0.00 [−0.22, 0.22], .980 | −0.17 [−0.59, 0.24], .407 | −0.03 [−0.24, 0.17], .742 |

**Sample sizes (N children / G clusters)** — identical for the water and sanitation tables above, since both exposures are estimated on the same anthropometric sample per outcome/country; shown once here rather than repeated in every coefficient cell

| Outcome | Ghana 2014 | Kenya 2014 | Nigeria 2018 | Pooled established |
|---|---|---|---|---|
| HAZ | N1,940 / G353 | N14,166 / G1,498 | N6,912 / G1,263 | N23,018 / G3,114 |
| WAZ | N1,940 / G353 | N14,166 / G1,498 | N6,951 / G1,264 | N23,057 / G3,115 |
| WHZ | N1,940 / G353 | N14,166 / G1,498 | N6,942 / G1,264 | N23,048 / G3,115 |

The pooled established-date water–HAZ coefficient (1.03, *p* < .001) is this section's selected headline — the cell this thesis discusses in the most depth — but it is **not** the only nominally significant cell among the 24 shown above: at conventional *p* < .05, **six** of the 24 cells reach significance (pooled water–HAZ, pooled water–WAZ, Ghana water–HAZ, Nigeria water–HAZ, Nigeria water–WAZ at *p* = .0498, and Ghana sanitation–HAZ, the last in an unexpected negative direction; the displayed, rounded *p* = .050 for Nigeria water–WAZ in the table above should not be read as exactly at the threshold — the underlying value is below .05). The pooled water–HAZ cell was selected as the headline because it is the pooled, established-date estimate for this thesis's primary outcome and primary window, decided before any coefficient was examined (Section 6.4), not because it is the only significant result — a reader comparing this table against this prose should see six significant cells, not one. It was independently reconstructed and re-estimated with a different estimation library and a separately rebuilt sample, matching the figures above to six significant digits (Appendix B). This establishes that the reported number is what the documented specification, correctly implemented, actually produces. It is not a multiplicity correction: no formal adjustment for testing 24 cells (2 products × 3 outcomes × 4 sample groups) has been applied anywhere in this section, and computational reproduction of a single coefficient does not substitute for one or establish that this result, or any of its five other nominally significant siblings, is any less likely to reflect chance given the number of cells examined. This coefficient's reporting status relative to its sibling cells is therefore unchanged by the computational check — all 24 cells carry the same unresolved documentation issues (Section 3.8, Section 6) — and the check does not establish causality.

**Weighted vs. unweighted, same observations.** The pooled water–HAZ coefficient is sensitive to the equal-country weighting convention: 1.03 (weighted, equal country totals) vs. 0.41 [0.03, 0.80], *p* = .035 (unweighted, identical 23,018 observations). This is a disclosed, authorised sensitivity to a stated design choice (Section 4.5), not evidence that either weighting is more "correct"; both are reported together whenever this coefficient is cited.

**Residual exposure variation and the 10-point scale.** The pooled water–HAZ model's residual within-cluster exposure standard deviation after all controls is 0.43 percentage points — meaning the conventional 10-percentage-point coefficient scale is roughly 23 times larger than the exposure contrast that actually identifies the model. The effect corresponding to one residual-exposure standard deviation is approximately 0.044 HAZ standard deviations. The 10-point coefficient should therefore be read as a reporting convention for comparability across studies, not as a description of a change that is typically observed within a cluster.

## 5.7 Alternative windows and common-sample comparison

The 291-model register (`docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`) decomposes exactly into: 24 primary established-date models; 24 unweighted-comparison models; 72 alternative-window models (window choice, §5.7, three further windows × 2 products × 3 outcomes × 4 sample groups); 24 wealth-adjustment models; 24 containing-pixel models; 24 rural-10km models; 48 stricter-completion-rule models (two postnatal windows); 24 calendar-age-construction models; 18 Ethiopia-provisional models; and three overlap-exclusion families of 3 models each (9 total) — summing to 291. A separate file, `window_common_sample_PRELIMINARY_AGGREGATE.csv` (192 rows: 96 own-eligible-sample fits and 96 common-sample-across-all-four-windows fits), re-presents the window comparison on two different sample bases; its own-eligible-sample rows overlap with, rather than add distinctly to, the primary-plus-alternative-window rows already counted in the 291-model register above — this is not a further 192 distinct registered specifications. The pooled water–HAZ cells from the relevant families are shown below as the headline case to avoid repeating every cell in the main text. The corresponding sanitation and WAZ/WHZ sensitivity cells are not more or less favourable to a WASH association than the water–HAZ cells shown — most show the same pattern of wide, zero-spanning confidence intervals as the primary sanitation and WAZ/WHZ results in Section 5.6 — and are reported in full in the public aggregate tables (`docs/provenance/historical_wash_preliminary_estimates_v1/`), not reproduced here solely because water–HAZ happened to be significant.

| Window | Pooled water–HAZ β [95% CI] | Sample |
|---|---|---|
| Post-12-month (main) | 1.03 [0.51, 1.54] | Own-eligible, N = 23,018 |
| Birth-year | 0.54 [0.12, 0.96] | Own-eligible |
| Prenatal (9 months) | 0.64 [0.24, 1.03] | Own-eligible |
| Post-24-month | 1.75 [0.81, 2.70] | Own-eligible |
| Post-12-month, common-sample | 1.64 [0.68, 2.60] | All-window-eligible common sample, N = 16,419 |

The post-12-month estimate changes from 1.03 (its own eligible sample) to 1.64 when restricted to the smaller common sample eligible under all four windows — a **sample-composition effect** (children with complete 24-month windows differ systematically from the full post-12-month sample), not evidence favouring one window's validity over another. No window was selected because of its coefficient's significance; all four are reported together, as planned before any coefficient was examined (Appendix C).

## 5.8 Further sensitivity: wealth, spatial method, completion rule

| Sensitivity | Pooled water–HAZ β [95% CI] |
|---|---|
| Main (post_12m, weighted) | 1.03 [0.51, 1.54] |
| Wealth quintile added | 1.01 [0.50, 1.52] |
| Containing-pixel assignment (vs. buffer average) | 0.68 [0.26, 1.10] |
| Rural 10 km buffer (urban unchanged) | 1.01 [0.42, 1.60] |
| Stricter completion rule (+1 month) | 0.95 [0.43, 1.47] |
| Excluding Ghana (DHS/IHME input overlap) | 0.74 [0.24, 1.24] |

Adding wealth leaves the coefficient essentially unchanged (1.01 vs. 1.03). This shows only that the reported conditional coefficient is not sensitive to this particular adjustment; it does not establish that wealth is a mediator of the historical WASH exposure, and a small change under adjustment is not itself evidence against the competing possibility that wealth is a confounder the main specification should have included (Section 3.8 states both the mediator concern and this competing concern; this sensitivity adjudicates neither). It also does not, on its own, support or contradict a cluster-fixed-effects absorption mechanism, which this thesis's own baseline model separately demonstrates is not how cluster fixed effects behave (Section 4.2). The spatial-method and completion-rule sensitivities move the coefficient by amounts smaller than, or comparable to, the gap between the main weighted and unweighted estimates, and are reported without privileging any one over the main specification.

## 5.9 Ethiopia: provisional, excluded from the established-date pooled sample

Ethiopia's three interview-date candidates are not treated as equally valid sensitivity evidence. Candidate C1 uses a 30-day Ethiopian-calendar arithmetic conversion already shown, independently of the WASH analysis, to be invalid for the delivered recoded date fields (Appendix C); it is excluded from this section and from any reporting table, and its past numerical agreement with the other two candidates is not treated as evidence of robustness. Candidates C2 and C3 remain provisional (neither independently validated) and agree closely with each other (water–HAZ: −0.39 both; sanitation–HAZ: −0.45 both, both CIs including zero), reported here, in Appendix C, only as an explicitly exploratory sensitivity, never pooled into or compared against the established-date headline results above.
