# Baseline evidence reconciliation, v1 (2026-10-07)

Every number in this note was re-read in this pass directly from the stored CSV outputs named below — none is carried over from a chat transcript, the roadmap PDF, or memory. Where the roadmap PDF's numbers are repeated for comparison, that is stated explicitly.

## 1. Authoritative source files

| Specification | File |
|---|---|
| Community, minimally adjusted / + child controls / + SES / + SES + region FE (models 1–4) | `outputs/regressions/main_continuous_models.csv` |
| Household, cluster FE (primary convention and labelled sensitivity) | `outputs/household_community_wash/03_household_cluster_fe.csv` |
| Household, region FE | `outputs/household_community_wash/02_household_region_fe.csv` |
| Joint household + community model | `outputs/household_community_wash/05_joint_household_community.csv` |
| Age-heterogeneity joint tests | `outputs/household_community_wash/10_age_heterogeneity_joint_tests.csv` |
| Nigeria community-sanitation specification sensitivity | `outputs/household_community_wash/11_nigeria_sign_reversal.csv` |
| Within-cluster WASH variation (share of informative PSUs) | `outputs/household_community_wash/04_household_cluster_fe_support.csv` |
| Country-specific household cluster-FE models | `outputs/household_community_wash/15_country_household_cluster_fe.csv` |
| Inference convention | `docs/provenance/cluster_fe_inference_adjudication.md` |

## 2. Core results table (HAZ, re-derived)

| Specification | Water β [95% CI], p | Sanitation β [95% CI], p | N | PSUs |
|---|---|---|---|---|
| Community, minimally adjusted (model 1) | 0.447 [0.311, 0.584], p = 1.4×10⁻¹⁰ | 0.472 [0.356, 0.587], p = 1.2×10⁻¹⁵ | 36,985 | 4,434 |
| Community + SES + region FE (model 4) | 0.033 [−0.083, 0.150], p = .573 | 0.008 [−0.113, 0.129], p = .894 | 36,985 | 4,434 |
| Household + cluster FE, PRIMARY convention | −0.085 [−0.175, 0.004], p = .062 | 0.026 [−0.058, 0.110], p = .548 | 36,040 | 4,426 |
| Household + cluster FE, FULL_DUMMY_DF sensitivity | −0.085 [−0.181, 0.010], p = .080 | 0.026 [−0.064, 0.117], p = .574 | 36,040 | 4,426 |
| Joint model, household water \| community water (common sample) | −0.085 [−0.167, −0.003], p = .043 | 0.024 [−0.047, 0.096], p = .507 | 36,040 | 4,426 |

All five rows reproduce exactly from the files listed in §1 (checked to 3 decimal places on the reported scale; p-values checked to the exponent).

## 3. Resolution of the two flagged discrepancies

**(a) Household cluster-FE p-values (water .080, sanitation .574) in the roadmap/strategy drafts.**

These are **not arithmetic errors**. They are the exact values of the `FULL_DUMMY_DF_SENSITIVITY` row in `03_household_cluster_fe.csv` — a labelled sensitivity check that penalises degrees of freedom for the absorbed cluster dummies in addition to clustering on the same PSU variable. The project's adjudicated convention (`cluster_fe_inference_adjudication.md`), used throughout the rest of the analysis and validated against `linearmodels.PanelOLS(auto_df=True)`, is the `PRIMARY_SAME_CLUSTER_CRV1` row: no additional degrees-of-freedom penalty when the fixed-effect grouping and the clustering grouping are the same variable. That row gives p = .062 (water) and p = .548 (sanitation).

Consequence: the roadmap and strategy-candidate drafts report a real, documented number, but without naming which convention it comes from, which makes it read as the primary result when it is the sensitivity variant. **Correction for any new document: report .062 / .548 as the primary household cluster-FE p-values, and .080 / .574 only if explicitly labelled as the FULL_DUMMY_DF sensitivity.**

**(b) Age-heterogeneity count ("10 of 12" vs. 11 of 12).**

Re-counted directly from `10_age_heterogeneity_joint_tests.csv`, restricting to the 12 water/sanitation joint-interaction rows (excluding the 6 "all interactions" rows, which are a different, broader hypothesis): 11 of 12 reject at the 5% level. The single non-rejection is `H1_household_region_fe, whz, water_interactions_jointly_zero` (p = .300). **11 of 12 is correct; "10 of 12" in the roadmap is wrong and should be corrected.**

## 4. Other roadmap numbers checked and confirmed accurate

These were re-verified against the files in §1 and matched to the precision reported in the roadmap PDF (no corrections needed):

- WAZ and WHZ attenuation figures (community, all four adjustment stages).
- Joint-model household water HAZ, β = −0.085, p = .043 (common sample).
- Nigeria community sanitation–HAZ specification path: 0.274 (p=.004) → 0.296 (p=.001) → −0.457 (p<.001) → −0.184 (p=.035), and the block-removal finding that dropping wealth quintile is the largest single swing (sanitation moves from −0.457 to −0.196 when wealth is removed from the full control set).
- Nigeria household cluster-FE sanitation: β = −0.007, p = .919.
- Within-cluster WASH variation: 31.6% of PSUs vary in own-water status, 50.6% in own-sanitation status (reported as "about 32%" / "about 51%" in the roadmap — consistent).

## 5. Why community WASH is not also estimated with cluster fixed effects

Restated here because it is a design decision, not an omission, and belongs with the reconciled evidence: the leave-one-out community rate is a cluster-level quantity. Within a cluster, each child's value differs from every other child's only because a different household is excluded from their own calculation — a mechanical artefact of the leave-one-out construction, not a substantive difference in exposure. A cluster FE would absorb nearly all of the real, between-cluster variation in community coverage (its within-cluster SD is about 0.007–0011 against an overall SD of about 0.35) and leave β identified almost entirely by that small mechanical residual. This is a different situation from the **historical** extension's within-cluster, cross-cohort variation (item 6 of the supervisor advice matrix), where the time dimension provides real, non-mechanical within-cluster variation for the cluster FE to use. Community WASH under the current single-round design has no such time dimension, so cluster FE remains appropriate for household WASH and for the historical extension, but not for current-round community WASH.

## 6. Recommended action on `docs/empirical_strategy.md`

`docs/empirical_strategy.md` is the tracked, GitHub-synced strategy document. Its baseline numbers (lines ~147–149 per the prior audit) already match the validated outputs. Its Section 6 status text ("data preparation in progress"; "remains open before raster matching and estimation can begin") is now out of date, since the historical extension has since been built, extracted, and estimated (291 preliminary models, validated). This reconciliation note documents the correct state; updating `docs/empirical_strategy.md` itself is a separate, reviewable edit and is not made here, consistent with the author's instruction not to alter other tracked manuscript-adjacent documents without a specific go-ahead. Recommendation: replace Section 6 with a short status paragraph pointing to `historical_wash_preliminary_estimation_methods_2026-10-06.md` and this reconciliation note, in a dedicated, reviewed commit.
