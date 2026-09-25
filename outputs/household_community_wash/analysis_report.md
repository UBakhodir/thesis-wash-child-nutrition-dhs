# Household and Community WASH Analysis Report

**Status:** These analyses are maintained separately from the pre-existing Step 13 thesis-facing
regression outputs pending final integration of the empirical specification set.
Script: `scripts/dhs_harmonization/14_household_community_wash_models.py` (new file — no existing
script/path was overwritten). Output directory: `outputs/household_community_wash/` (new directory — did
not previously exist).

---

## 1. Safety / reproducibility

- Git branch: `main` (repo = `thesis-wash-child-nutrition-dhs/`, the packaged subfolder; the working
  directory that actually holds `data/` and `scripts/dhs_harmonization/` is not itself git-tracked).
- Starting commit for the original development run described in this report: `3d8a370cbd32bf0fd62182862535ea4bdbbf2cb7`
  (historical reference — the repository has since advanced through published commits `e2f47de`, `9f1f53c`,
  and `56547be`, including a subsequent cluster-FE inference correction covered in §4 and §16 below).
- Git status before and after: unchanged — only the pre-existing, unrelated untracked
  `?? outputs/supervisor_meeting/` folder (from an earlier session) appears; nothing from this
  development run touches the git-tracked repo at all, since it was written entirely under the
  non-git-tracked master working directory.
- New files created (historical reference — the script was later renamed to
  `scripts/dhs_harmonization/14_household_community_wash_models.py` and its output directory to
  `outputs/household_community_wash/`, both current as of this document's header above): originally
  `scripts/dhs_harmonization/14_supervisor_development.py`; `outputs/supervisor_development/` (20 files:
  18 CSVs incl. two supplementary, `_run_log.txt`, this report).
- Baseline hash verification: SHA-256 of the four files this development reads
  (`11_main_regressions.py`, `12_robustness.py`, `main_continuous_models.csv`,
  `robustness_household_wash.csv`) was computed **before** any estimation ran and **re-verified
  identical** immediately before writing outputs (Part 12) and again independently from the terminal
  after the script exited. All four match exactly — see `baseline_file_hashes.csv`.
- Confirmation existing pipeline unchanged: Steps 00–13 were never opened in write mode; only their
  functions/constants were imported (their `if __name__=="__main__"` blocks never executed). No file
  under `data/`, `outputs/final_tables/`, `outputs/final_figures/`, `outputs/regressions/`,
  `outputs/final_appendix/` was written to.
- Part-0 pre-run validation (10 checks specified in the brief) **all passed** on the first run except
  two genuine, disclosed adjustments discovered *during* implementation (not before) — see §16.

---

## 2. Common comparison sample

Built by additionally requiring non-missing own-household water/sanitation classification on top of
the existing Model-4 requirements (outcome, both community exposures, all controls, FE, weight).

| Outcome | Common-sample N | Model-4 N | Difference | Unique HH | Unique PSU | Admin cells |
|---|---|---|---|---|---|---|
| HAZ | 36,040 | 36,985 | −945 | 25,627 | 4,426 | 114 |
| WAZ | 36,308 | 37,260 | −952 | 25,759 | 4,426 | 114 |
| WHZ | 36,145 | 37,088 | −943 | 25,665 | 4,426 | 114 |

The loss (~2.5%) matches almost exactly the household-baseline robustness family's own
"`n_excluded_by_household_wash_states`" (943–952) already on record in the frozen
`robustness_household_wash.csv` — internally consistent, no discrepancy.

---

## 3. Household WASH + region FE (Model A)

Common-sample (A2) results, pooled:

| Outcome | Water β (SE, p) | Sanitation β (SE, p) |
|---|---|---|
| HAZ | −0.035 (0.038, p=.357) | +0.022 (0.034, p=.522) |
| WAZ | +0.021 (0.030, p=.487) | +0.045 (0.028, p=.109) |
| WHZ | +0.050 (0.033, p=.130) | +0.046 (0.029, p=.116) |

Interpretation: `β_water` (HAZ) = the mean HAZ difference associated with living in a household with
an improved water source vs. not, holding child/maternal/household controls and administrative-region
fixed effects constant — an association, not a causal effect. All six coefficients are small and
statistically insignificant at 5%, similar in magnitude/precision to the *existing* no-region-FE
household baseline (`robustness_household_wash.csv`: e.g. HAZ water 0.020/p=.606, sanitation
0.021/p=.578). Adding region FE moved every coefficient only modestly (largest shift: HAZ water
0.020→−0.035) — region FE does not qualitatively change the household-level picture.

---

## 4. Household WASH + cluster FE (Model B)

**Support/within-cluster variation** (natural Model-B sample, ~4,426 PSUs, pooled): 31.6–31.7% of PSUs
have within-cluster water variation, 50.6–50.8% have within-cluster sanitation variation (slightly
lower than the earlier audit's whole-sample figures of 37.4%/60.4% because this sample additionally
requires all Model-4 controls, not just classifiable WASH).

**Estimator implementation:** weighted within-cluster demeaning (the weighted Frisch–Waugh–Lovell
"within" transformation), **not** explicit PSU dummies for the full pooled sample (~4,426 clusters
would need a ~36,000×4,440 dense design matrix — computationally unsafe for this task) and **not**
`linearmodels.PanelOLS` (installed, v7.0, but avoided for consistency with this project's own
documented convention of avoiding "artificial panel structure" estimators). **Validated** against
explicit-dummy WLS on a tractable subset (Ghana, N=4,287, 613 PSUs): max |coefficient difference|
across all 6 non-FE terms = **5.6×10⁻¹⁵** (machine precision) — mathematically exact agreement, not an
approximation.

**Genuine finding required a control-set adjustment:** the first run was rank-deficient. Diagnosis
(SVD null-space inspection) showed the entire deficiency loaded on `residence_Urban`. Direct
verification: **every one of the 4,481 DHS PSUs in this dataset is 100% urban or 100% rural, with zero
exceptions** — a structural property of the DHS cluster/EA sampling frame, not a data error.
`residence` therefore has exactly zero within-cluster variation and is unidentified under cluster FE.
**`residence` was excluded from every cluster-FE specification only** (Models B, H2, country-specific
cluster-FE models, and the cluster-FE arm of Part 6); it is retained unchanged in every region-FE
model. This is disclosed here and in the script's own log/comments, not silently done.

**Inference convention (Part 3C; adjudicated — see
`docs/provenance/cluster_fe_inference_adjudication.md`):** `res.cov_kwds` confirms statsmodels applies
`use_correction=True` by default for `cov_type='cluster'` on the demeaned fit. The fixed-effect grouping
absorbed by demeaning and the clustering grouping used for this cluster-robust covariance are the *same*
PSU variable, so statsmodels' native cluster-robust SE/CI/p (`res.bse`, `res.conf_int()`, `res.pvalues`)
are used directly as the **primary** inference, with no additional degrees-of-freedom penalty for the
absorbed PSU effects. This was cross-validated against `linearmodels.PanelOLS(entity_effects=True)
.fit(cov_type="clustered", cluster_entity=True, auto_df=True)` on this project's own data, which matches
the native statsmodels values to 4–5 decimal places and documents (in its own `auto_df` parameter) that
clustered SEs sharing their grouping variable with an absorbed effect do not require an extra
degrees-of-freedom correction. A full-dummy-style scale (treating every absorbed PSU dummy as an
explicitly estimated parameter, `k_full_dummy = k_reported + n_clusters`, ≈1.067–1.068 pooled) remains
available in `03_household_cluster_fe.csv` as a clearly labelled `FULL_DUMMY_DF_SENSITIVITY` row-set, for
transparency only — it is not the primary convention.

**Headline (primary, native same-cluster CRV1), pooled, natural sample:**

| Outcome | Water β (SE, p) | Sanitation β (SE, p) |
|---|---|---|
| HAZ | −0.085 (0.046, p=.062) | +0.026 (0.043, p=.548) |
| WAZ | −0.029 (0.037, p=.435) | +0.052 (0.035, p=.130) |
| WHZ | +0.012 (0.038, p=.758) | +0.053 (0.034, p=.122) |

**Comparison to region-FE (Model A):** the HAZ-water coefficient moves from −0.035 (region FE, n.s.)
to −0.085 (cluster FE, p=.062, not statistically significant at the 5% level) — a larger magnitude once
local cluster-level confounding is removed, but still not conventionally significant. Sanitation
coefficients are similar in both specifications (small, positive, insignificant).

**What identifies β:** comparisons between households that differ in own WASH status *within the same
DHS cluster* (31.6–50.8% of clusters have such variation, §above), after also holding demographic/SES
controls constant. **What remains uncontrolled:** household-level confounding that also varies within
a cluster — wealth, parental preferences/behavior, unobserved health inputs correlated with WASH
investment. Cluster FE is a real improvement over Model A (removes all cluster-level confounding, e.g.
local infrastructure, market access) but does **not** make this causal.

---

## 5. Household + community joint model (Model C)

Common sample, region FE, all four exposures simultaneously:

| Outcome | HH water | HH sanitation | Community water | Community sanitation |
|---|---|---|---|---|
| HAZ | **−0.085 (p=.043)** | +0.024 (p=.507) | +0.120 (p=.066) | −0.018 (p=.784) |
| WAZ | −0.015 (p=.677) | +0.039 (p=.191) | +0.081 (p=.121) | +0.022 (p=.706) |
| WHZ | +0.039 (p=.318) | +0.036 (p=.244) | +0.019 (p=.750) | +0.045 (p=.446) |

**HAZ household-water is the one coefficient in this entire development pass that crosses p<.05**
(β=−0.085, 95% CI [−0.167, −0.003]). It is not causal evidence, and given r=0.74 between household and
community water (below), some caution about precision/instability is warranted even though VIF stays
low (see §6).

**Diagnostics:** VIF among the 4 exposures alone: 1.84–2.61; with full controls added: 1.99–2.70 — well
below conventional concern thresholds (e.g. 10), interpreted substantively as "collinearity is present
but not numerically dangerous." Pairwise correlations: HH-water↔community-water r=0.745,
HH-sanitation↔community-sanitation r=0.675, cross-terms (HH-water↔community-sanitation etc.) r=0.37–0.40
— lower than the same-domain pairs, as expected. Condition number of the exposures+controls design
matrix ≈ 1,880 — moderate, not extreme. **No sign flips or wild SE inflation** were observed between
the separate (A2/D) and joint (C) fits; coefficients moved in magnitude (e.g. HH-water HAZ −0.035→−0.085)
but stayed numerically stable — the model appears estimable, not degenerate.

---

## 6. Common-sample comparison (community-only vs. household-only vs. joint)

Full table: `07_common_sample_community_vs_household.csv`. HAZ row, illustrative:

| Spec | Water term | β (p) | Sanitation term | β (p) |
|---|---|---|---|---|
| Community-only | water_rate_loo | +0.040 (.503) | sanitation_rate_loo_core | +0.003 (.965) |
| Household-only | HH water | −0.035 (.357) | HH sanitation | +0.022 (.522) |
| Joint (household term) | HH water | −0.085 (.043) | HH sanitation | +0.024 (.507) |
| Joint (community term) | water_rate_loo | +0.120 (.066) | sanitation_rate_loo_core | −0.018 (.784) |

All observations are now identical across the three specifications (N=36,040/36,308/36,145 by outcome,
same 4,426 PSUs), so differences reflect specification, not sample composition. The clearest pattern:
adding community coverage to the household model pulls the household-water coefficient more negative
and pushes it past p=.05 for HAZ; the reverse also happens (community water gets *more* positive,
p=.066) — consistent with the two exposures partly competing for the same variance (r=0.745), not with
either being a clean, independent "true" effect.

---

## 7. Flexible age controls

Linear `b19_raw` vs. full age-in-month (59-dummy) FE, for Models A, B, D, all three outcomes (18
comparisons total): **zero sign changes, zero significance-threshold crossings**, coefficient
magnitudes shifted by no more than ~0.006 in any case (see `08_flexible_age_sensitivity.csv`).
**Conclusion: the linear-age functional form used in the frozen Models 1–4 is not driving any of the
existing null/non-significant results — a materially more flexible age control changes nothing
substantive.**

---

## 8. Age heterogeneity

Reference band: 12–23 months (largest, most central band — fixed before any result was seen).
Household water/sanitation × age-band interactions, region-FE (H1) and cluster-FE (H2). H2 uses the
same primary native same-cluster CRV1 inference convention as Model B (see §4 and
`docs/provenance/cluster_fe_inference_adjudication.md`) — no additional absorbed-PSU-FE
degrees-of-freedom penalty.

**Joint Wald tests** (all 5 interaction terms jointly zero) — `10_age_heterogeneity_joint_tests.csv`:

| Outcome | Exposure | H1 (region FE) p | H2 (cluster FE) p |
|---|---|---|---|
| HAZ | water | .0005 | .0042 |
| HAZ | sanitation | <.0001 | .0023 |
| WAZ | water | .0074 | .0131 |
| WAZ | sanitation | .0055 | .0033 |
| WHZ | water | .300 (n.s.) | .0485 |
| WHZ | sanitation | .0421 | .0020 |

11 of 12 joint tests reject "no heterogeneity" at 5%; the sole non-rejection is water×WHZ under the
region-FE (H1) specification (p=.300) — the cluster-FE (H2) counterpart for the same outcome/exposure
now also rejects (p=.0485). This is a genuine, pre-specified joint test — not a single cherry-picked
band — so **there is real evidence that the household-WASH/HAZ-WAZ association differs by child age.**
The pattern is not
uniform across outcomes, though: for HAZ, the youngest band (0–5 months) shows the most negative
implied water association (H1: −0.231, H2: −0.279) and the association becomes positive by 36+ months;
for WHZ the youngest-band water association is instead *positive* (+0.12 to +0.21). Sample sizes per
band are adequate (3,893–7,405; `09b_age_heterogeneity_descriptive_bands.csv`), so this is not a
small-sample artifact of one band. **This is evidence of heterogeneity, not evidence of a specific
developmental mechanism** — it does not tell us *why* the association differs by age, and it says
nothing about historical exposure timing (§10 of the prior audit).

---

## 9. Nigeria sanitation → HAZ sign reversal

**M1→M4 reproduction** (exact match to frozen output, confirmed via direct comparison,
`11_nigeria_sign_reversal.csv`): +0.274 (p=.004) → +0.296 (p=.001) → **−0.457 (p<.0001)** → −0.184 (p=.035).

**Sequential block addition** (from M2, no FE): the coefficient stays positive through `+maternal_age`
(+0.183) and only turns negative at `+maternal_education` (−0.030), then keeps moving negative through
`+literacy` (−0.057) and jumps sharply at **`+wealth_quintile` (−0.389)** — by far the single largest
move of the six blocks — then changes little through `+household_size` (−0.390) and `+residence`
(−0.457, = full M3).

**Leave-one-block-out** (from full M3): removing **wealth_quintile** pulls the coefficient furthest back
toward zero (−0.457 → **−0.196**), a far larger swing than removing any other block (maternal_age:
−0.486; maternal_education: −0.501; literacy: −0.444; household_size: −0.457; residence: −0.390). Both
designs agree on a purely descriptive fact: **the wealth-quintile block produces the largest observed
coefficient movement among the six tested blocks.** This demonstrates that the estimate is sensitive to
specification; a sequential-addition and leave-one-block-out diagnostic of this kind cannot, on its own,
establish *why* the coefficient moves — only that it does, and by how much, when each block is added or
removed.

**Why wealth plausibly matters:** community sanitation coverage in Nigeria is strongly stratified by
wealth (mean sanitation LOO 0.27 in the poorest quintile vs. 0.93 in the richest) and by residence
(0.42 rural vs. 0.82 urban) and maternal education (0.43 no-education vs. 0.88 higher-education) —
`12_nigeria_sign_reversal_covariate_diagnostics.csv`. This is a strong, monotonic descriptive
association, consistent with — but not proof of — wealth or a correlated measured/unmeasured
characteristic accounting for part of the coefficient's movement: once wealth is held fixed, what's
"left" of the sanitation-coverage variation may pick up something that correlates negatively with HAZ
(e.g., historically under-resourced or targeted areas). **This diagnostic does not establish that wealth
causally explains the reversal. Reverse causality / targeted investment remains only a hypothesis, not
something this data can confirm.**

**Four-way comparison, Nigeria HAZ, sanitation:**

| Spec | β | p | N |
|---|---|---|---|
| 1. Community + region FE (existing M4) | −0.184 | .035 | 9,410 |
| 2. Household + region FE | −0.106 | .053 | 9,315 |
| 3. **Household + cluster FE** | **−0.007** | **.919** | 9,315 |
| 4. Joint household+community + region FE | HH: −0.077 (p=.17); community: −0.138 (p=.12) | | 9,315 |

The negative association **essentially disappears** once cluster FE removes remaining local
confounding (spec 3), and weakens under the joint model (spec 4) too. This pattern is consistent with
the coefficient being substantially, though perhaps not entirely, a confounding artifact rather than a
robust household- or community-specific relationship — stated as a pattern in the data, not a causal
conclusion.

---

## 10. Anthropometric availability

Overall HAZ availability by country: **Ethiopia 43.1%, Ghana 47.1%, Kenya 88.7%, Nigeria 33.9%** (ALL
52.7%). **Country is by far the dominant driver of availability** — not age band, not household WASH
status, not wealth, not residence (all of which show only modest, sub-10-point gradients even where
present). Within-country checks (all four countries) show a modest, inconsistent WASH-availability
gradient (e.g. Nigeria: Improved water 35.1% vs. Unimproved 29.1% available — a real ~6pp gap in the
expected direction; sanitation gap in Nigeria is much smaller, 34.2% vs. 33.2%). Community-WASH-LOO
quartile shows no clean monotonic pattern once country composition dominates.

**What cannot be established:** `b5` (child survival status) is confirmed present in the raw KR `.dta`
metadata (read-only column-name check, Ethiopia) but was not extracted here, so death vs. non-residence
vs. absence vs. refusal cannot be distinguished with currently-processed data. This diagnostic
establishes *that* availability varies sharply (mostly by country) and *modestly* by WASH status — not
*why*.

**Implication for limitations:** the ~47% pooled non-availability is not a uniform phenomenon; it is
heavily concentrated in three of the four countries, with Kenya's ~89% availability a clear outlier.
Any discussion of selection risk should say so explicitly rather than treating "47%" as representative
of all four countries equally.

---

## 11. Country-specific household results

**Household + region FE**, HAZ: Ethiopia −0.095 (p=.346) / +0.067 (p=.430); Ghana −0.002 (p=.975) /
+0.064 (p=.351); Kenya −0.018 (p=.551) / +0.044 (p=.178); Nigeria −0.002 (p=.977) / **−0.106 (p=.053)**
(water/sanitation respectively).

**Household + cluster FE**, HAZ: Ethiopia −0.174 (p=.140) / +0.044 (p=.691); Ghana −0.002 (p=.985) /
+0.059 (p=.514); **Kenya −0.083 (p=.032)** / +0.043 (p=.223); Nigeria −0.064 (p=.397) / −0.007 (p=.919).

Among the country-specific HAZ cluster-FE household-WASH coefficients above, Kenya's household-water
term is the only one to cross p<.05 (negative). This is not true across all outcomes: the full
country-specific results (`15_country_household_cluster_fe.csv`) also include Kenya WAZ household
sanitation (p=.043) and Ethiopia WHZ household sanitation (p=.014) crossing p<.05 — cells not narrated
in this section. Cluster-FE support (% of PSUs with within-cluster variation) ranges 20.7–41.7% for
water and 40.0–58.8% for sanitation across the four countries (`15b_country_cluster_fe_support.csv`) —
Ghana has the least support (20.7% water), Kenya the most (41.7% water). These are exploratory,
development-stage country splits with smaller N per cell; no single country-specific p<.05 result
should be read as a headline finding at this stage.

---

## 12. What changed relative to our previous empirical understanding

- The audit's "37.4%/60.4% mixed-cluster" figures are confirmed (this run's comparable natural-sample
  figures are 31.6%/50.6%, slightly lower only because of the additional Model-4-control requirement).
- **New, not previously known:** DHS clusters here are perfectly urban/rural-homogeneous (0 exceptions
  across 4,481 PSUs) — `residence` cannot enter any cluster-FE model.
- **New:** the Nigeria sign reversal shows clear specification sensitivity — the wealth-quintile block
  produces by far the largest coefficient movement in both the sequential and leave-one-out diagnostics,
  and the cluster-FE analogue of the same coefficient is essentially zero. This demonstrates the
  unadjusted association is not robust to specification; it does not, on its own, establish that wealth
  causally explains the reversal (see §9).
- **New:** genuine (joint-test-confirmed) age heterogeneity exists in the household-WASH/HAZ and
  WAZ associations, not previously tested.
- **New:** anthropometric availability is overwhelmingly a country-level phenomenon (34–89% range), not
  a uniform "~47% missing" story, and not strongly driven by WASH status.
- **New:** among the pooled, whole-sample primary WASH-exposure coefficients across the region-FE,
  cluster-FE, and joint comparisons (Models A/B/C/D), the one specification that crosses p<.05 is
  household water in the joint model (Model C, HAZ, β=−0.085, p=.043) — a genuinely new result, not
  previously estimated, and one that should not be over-weighted given it sits inside a moderately
  collinear joint specification. (This does not describe country-specific splits or the age-interaction
  joint tests, which are separate analyses with their own p<.05 cells reported in §8 and §11.)

---

## 13. Recommended provisional architecture

Based on identifying variation and research-question alignment, **not** on significance:

- **Candidate MAIN:** Model B (household WASH + cluster FE) — the cleanest available identification
  given real within-cluster variation (§4), directly answers "does own-household WASH matter net of
  everything the neighborhood shares," and is now a validated, documented estimator.
- **SECONDARY/COMPLEMENTARY:** Model A (household + region FE, for continuity with the existing
  community Model 4's FE choice); Model C (joint household+community) as an explicit test of whether
  community coverage adds anything net of household WASH — report VIFs alongside it, always.
- **ROBUSTNESS/HETEROGENEITY:** flexible age-month FE (§7 — shown not to matter, worth one robustness
  line, not a main result); age-band interactions (§8 — genuine heterogeneity, presentable as a
  secondary finding with the joint-test p-values, not as a headline "critical window" claim); the
  Nigeria block diagnostic (§9 — belongs in a case-study/discussion subsection, not a robustness table).
- **NOT USEFUL as a standalone model:** community WASH + cluster FE (never estimated here, per
  instruction — confirmed still mechanical per the prior audit, no new evidence changes that).

---

## 14. Historical WASH

**Updated since the original development pass described above** (see `docs/empirical_strategy.md` §6
and `docs/provenance/historical_wash_feasibility_audit.md` for the current, authoritative status): a
candidate historical WASH source (IHME gridded improved-water/improved-sanitation estimates, 2000–2017)
and a candidate geocoded child data source (IPUMS DHS) have since been identified and independently
verified against their own documentation, and the corresponding raster files have been obtained.
Exposure matching, extraction, and estimation have **not** been carried out, and no historical-WASH
result exists in this repository. If later completed, it would extend rather than replace the
household/cluster-FE architecture above, most naturally by re-defining the exposure window for the
cluster-FE model rather than requiring a new estimator.

---

## 15. Readiness for supervisor introduction

**NOT YET — but close.** The core household-vs-community empirical picture the supervisor asked for is
now built, validated, and internally consistent (Model A/B/C all estimated, cluster-FE estimator
mathematically validated to 1e-15, age-flexibility and age-heterogeneity tested, the Nigeria
specification-sensitivity diagnostic completed). What's still missing before drafting:

1. A decision from you on which of Models A/B/C is the "provisional main" household specification (§13
   gives a recommendation, not a decision).
2. A brief written framing of the single p<.05 joint-model result (§5) so it isn't accidentally
   over-stated in the introduction — this needs your judgment, not just a p-value.
3. Confirmation of whether the age-heterogeneity finding (§8) belongs in the introduction at all, or is
   better held for a later results chapter.
4. No new data or re-estimation is required — this is a writing/scoping decision, not an empirical gap.

---

## 16. Problems / warnings

- **Coding issue, caught and fixed before any coefficient was reported:** the first cluster-FE attempt
  was rank-deficient because a constant term was (incorrectly) included after weighted demeaning;
  fixed by omitting the constant, which is standard/correct practice for a within-transformed
  regression, then verified via the 1e-15 validation.
- **Genuine methodological finding requiring disclosure, not a bug:** `residence` must be dropped from
  every cluster-FE specification (DHS clusters are always 100% urban or 100% rural). Applied
  consistently everywhere cluster FE is used in this script.
- **Collinearity:** present but not numerically dangerous in Model C (VIF 1.8–2.7, condition number
  ~1,880) — flagged, not treated as disqualifying.
- **Weak support in places:** Ghana's cluster-FE water support is the lowest of the four countries
  (20.7% of PSUs) — country-specific Ghana cluster-FE water coefficients should be read with that in
  mind.
- **Inference convention, reviewed and adjudicated:** for the demeaned cluster-FE fit, the fixed-effect
  grouping and the clustering grouping are the same DHS PSU variable; the primary reported inference is
  therefore statsmodels' native PSU-cluster CRV1 output, with no additional absorbed-PSU/full-dummy
  degrees-of-freedom penalty (see §4 and `docs/provenance/cluster_fe_inference_adjudication.md`). A
  full-dummy-style degrees-of-freedom scaling is retained in the output file only as a labelled
  sensitivity (`FULL_DUMMY_DF_SENSITIVITY`), not as the primary convention. Point estimates are
  unaffected by this inference-convention choice.
- **Sample-size note:** all Part 8 Nigeria diagnostics and the country-specific splits in Part 10/11 use
  smaller N than the pooled models — treat any single p<.05 country-specific cell as exploratory.
- **Nothing here required your decision to proceed** — every adjustment above was resolved within the
  stated safety rules (additive-only, no baseline modification) and disclosed rather than silently
  applied.
