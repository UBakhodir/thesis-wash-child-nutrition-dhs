# Reporting-language corrections, v1 (2026-10-07, second pass)

Reporting-only correction. No model was rerun, no new estimation was performed, and no number in any stored output changed. This document corrects four pieces of language in the prior session's documents (`final_empirical_package_v2_2026-10-07/`, `historical_wash_issue_register_v1_2026-10-07.md`) that overstated, understated, or mischaracterised what the validated numbers support. All prior files are preserved unchanged; pointer banners added to the files whose language this supersedes.

## 1. Measurement-sample language

**Prior wording** (issue register item #1, "Reporting consequence"; echoed in `final_empirical_package_v2_2026-10-07/00_results_index.md` §C.1): *"Report as population-representative only within the measured subsample"* / *"an association within the measured anthropometry subsample, not a population-representative estimate."*

**Problem:** "population-representative within the measured subsample" is close to self-contradictory — representativeness is exactly what is in question, since neither the measurement-subsample selection probability nor differential non-response among eligible children is documented (register items #1–#2). Calling the result representative of *any* population, qualified or not, overstates what a PERWEIGHT-normalized estimate on an unverified subsample weight can support.

**Corrected wording:** The historical coefficients are **weighted conditional associations among eligible measured children** — conditional on cluster, survey-qualified country-by-birth-year, child sex, and maternal age/education/marital status. They are not population estimates for any defined population, measured or otherwise, because:
- the anthropometry/biomarker measurement-subsample selection weight is undocumented (DHS-8 Biomarker Manual blocked twice; no alternative official source located; register #1), so the within-survey PERWEIGHT normalization is an *inference*, not a documented correction for subsample selection; and
- differential non-response among eligible-but-unmeasured children is not observable from the extract and is not corrected by any weight (register #2).

**Explicit correction to a likely misreading:** using the **unweighted** estimate does not resolve this. The unweighted model (§3's core table) answers a different question — the association in the sample as drawn, with no attempt to reweight toward any population — but it carries exactly the same unresolved subsample-selection and non-response concerns as the weighted model. Neither weighting choice removes the selection issue; they differ only in whether within-sample composition is reweighted toward equal-country mass. This is stated once here and should not be re-derived or contradicted elsewhere.

## 2. Pooled-estimand language

**Prior wording** (issue register item #8; `00_results_index.md` §C.2): the pooled estimate *"targets 'the average country-level association, each of the three established-date countries weighted equally.'"*

**Problem:** this phrasing reads as "the pooled coefficient is the arithmetic mean of the three country-specific coefficients." It is not, and equal country weight totals do not make it so. Equal-country **total observation weight** (each country's weights sum to N/K within the estimation sample) is a statement about how much aggregate weight mass each country contributes to the weighted least-squares objective function — it is not a statement about how much each country's *slope* contributes to the pooled common-slope coefficient.

**Why these differ, shown with the actual numbers:** the simple arithmetic mean of the three country-specific primary coefficients (water, HAZ, post_12m, weighted) is (1.648 + (−0.606) + 0.700) / 3 = **0.581**. The actual pooled coefficient is **1.026** — not close to the simple average, and in fact outside the range you would get from any convex combination of only Ghana's and Nigeria's coefficients unless Kenya's negative, imprecise estimate is downweighted by something other than equal country totals. The reason: a pooled common-slope WLS/fixed-effects regression weights each observation's contribution to the slope by its weight **times** its squared residual exposure variation (information), not by its weight alone. Kenya has by far the smallest residual within-cluster exposure variation after controls (0.203 percentage points, against Ghana's 0.456 and Nigeria's 0.652 — see the core table in §3), so Kenya's imprecise, negative country-specific estimate contributes comparatively little *information* to the pooled slope even though it contributes an equal *weight total*. The pooled coefficient is therefore better described as a precision-weighted (inverse-variance-like) combination of the within-country associations, under equal country weight totals, not an average of the three country slopes.

**Corrected wording:** The pooled estimate is a **pooled common-slope association, estimated with each country assigned equal total observation weight** (not equal influence on the slope). Each country's actual contribution to the estimated slope depends jointly on its weight and on how much residual, within-cluster, cross-cohort exposure variation it has after the controls — which differs substantially across the three countries (Kenya's residual exposure variation is roughly a third of Nigeria's and under half of Ghana's). Report the pooled coefficient, the country-specific coefficients, and the residual-exposure-SD column together (§3's table), so a reader can see which countries are actually driving the pooled result, rather than assuming equal contribution from the equal-weighting-total description alone.

## 3. Historical reporting status: separating computational verification from reporting readiness

**Prior wording** (`final_empirical_package_v2_2026-10-07/00_results_index.md` §B): the pooled established water–HAZ estimate was labelled **"Validated for main reporting"**, a tier above the other 23 primary historical models ("Exploratory with specified limitations"), on the basis that it alone had been independently rebuilt from scratch in `20_validate_pooled_estimate.py`.

**Problem:** this conflates two different things. *Computational verification* (does the number match what the documented specification, correctly implemented, actually produces?) is now true of the pooled water–HAZ model to a higher degree than the other 23 cells, because it alone received a full from-scratch independent reconstruction this session (the other 23 only have the original pipeline's internal design checks, or — for four specific cells — the prior session's four-model independent check). But *reporting readiness* (is this number ready to be presented as a substantive finding, net of the extension's open methodological issues) is governed by the issue register, and every item in that register — undocumented measurement weight, Nigeria's count gap, Ethiopia's exclusion, DHS/IHME overlap, residence-as-proxy, displacement/buffer averaging — applies identically to the pooled water–HAZ model and to every other historical estimate. Being independently reconfirmed does not resolve any of those issues, and being statistically significant (p<.001) is not evidence that it does.

**Corrected status scheme** (replaces the two-tier scheme in v2):

- **Computational-check column** (new, orthogonal to reporting status): which models received which level of independent numerical verification. This is a statement about arithmetic correctness, not about substantive readiness.
- **Reporting-status column**: every primary established-date model (all 24 water/sanitation × HAZ/WAZ/WHZ × GH/KE/NG/pooled cells) carries the **same** status — *"Exploratory, internally and (for some cells) independently verified; not yet ready for unqualified substantive reporting"* — until the issue-register items that apply to the whole extension (not to any one cell) are closed or are carried as explicit, permanent caveats in the manuscript text. The pooled water–HAZ model is not promoted above its siblings for being significant or for having received extra replication.

See §4 for the corrected table carrying both columns, reusing only already-validated stored numbers.

## 4. Confounding language

**Prior wording** (`final_empirical_package_v2_2026-10-07/01_final_reporting_map.md`, baseline table): *"Minimal model is confounded (large, unadjusted)."*

**Problem:** this states confounding as an established fact about the data-generating process. What is actually shown is an **attenuation pattern** (community coefficients shrink from 0.447/0.472 to 0.033/0.008 and lose significance as SES and region controls are added) — attenuation on adding plausible confounders is *consistent with* confounding, but it is also consistent with, for example, measurement error in the added controls changing precision, or other specification changes coinciding with the same control additions. The data here do not isolate confounding as the sole mechanism.

**Corrected wording:** *"The community association attenuates sharply and loses significance once socioeconomic and region controls are added (0.447/0.472 unadjusted → 0.033/0.008 adjusted, both p>.5). This pattern is consistent with confounding by socioeconomic status but does not, on its own, establish confounding as the sole explanation for the unadjusted association."* This matches language already used correctly elsewhere in the repository (`docs/empirical_strategy.md`: "consistent with residual confounding in the unadjusted associations, but the data here do not establish that as the only explanation") — the final reporting map's wording is brought into line with that existing, more careful phrasing, not a new position.

## 5. What is not changed

- Ethiopia candidate C1 remains invalid/superseded; C2/C3 remain provisional (unchanged from `historical_wash_ethiopia_candidate_status_v1_2026-10-07.md`).
- The IHME product-definition resolution is unchanged.
- The independent numerical verification of the pooled model (coefficient, SE, N, G match to the precision reported previously) is unchanged — only how that verification is *described in relation to reporting readiness* is corrected here.
- No baseline number changed.
