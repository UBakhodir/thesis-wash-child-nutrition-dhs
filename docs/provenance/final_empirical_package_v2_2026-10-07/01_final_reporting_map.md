# Final reporting map (2026-10-07)

Every analysis family, assigned one of: **Validated for main reporting**, **Validated sensitivity**, **Exploratory with specified limitations**, **Invalid/superseded**, **Not estimable**.

## Baseline (current four-round, cross-sectional)

| Analysis family | Status | Note |
|---|---|---|
| Household water/sanitation, cluster FE, PRIMARY convention | Validated for main reporting | p=.062 water, p=.548 sanitation (HAZ) |
| Household water/sanitation, region FE | Validated for main reporting | |
| Community water/sanitation, 4-stage adjustment | Validated for main reporting | Minimal model is confounded (large, unadjusted); the fully adjusted model (0.033/0.008, both p>.5) is the reporting-relevant one |
| Household cluster-FE, FULL_DUMMY_DF convention | Validated sensitivity | p=.080/.574 — label explicitly if cited |
| Joint household+community model | Validated sensitivity | Single significant cell (p=.043) — report, do not treat as central |
| Age-heterogeneity joint tests | Validated sensitivity | 11 of 12 reject (corrected count) |
| Nigeria community-sanitation specification path | Validated sensitivity | Demonstrates instability, not a finding of harm |
| Country-specific household cluster-FE models | Validated sensitivity | |
| Alternative weights / binary LPM / biodigester / LOO-denominator robustness | Validated sensitivity | Not re-audited this session; unchanged since frozen |

## Historical extension

| Analysis family | Status | Note |
|---|---|---|
| Pooled established water–HAZ, post_12m, weighted (headline) | **Validated for main reporting** (with §C caveats in `00_results_index.md`) | Independently reconfirmed this session |
| Pooled unweighted counterpart (same observations) | Validated sensitivity | Confirms weighting sensitivity |
| Pooled, FULL_DUMMY_DF convention | Validated sensitivity | New this session |
| Country-specific established models (Ghana/Kenya/Nigeria, all outcomes/products) | Exploratory with specified limitations | Independently validated at the estimator level (prior session, 4 representative models) but not re-verified for every one of the 24 primary cells this session |
| Window sensitivities (birth_year, prenatal_9m, post_24m), wealth, containing-pixel, rural-10km, stricter completion, calendar-age, overlap exclusions (267 models) | Exploratory with specified limitations | Design-checked and internally consistent; not independently re-estimated this session |
| Ethiopia C1 (6 models: water/sanitation × HAZ/WAZ/WHZ, within the 291) | **Invalid/superseded** | Uses a date-conversion method already shown invalid; do not cite |
| Ethiopia C2, C3 (12 models) | Exploratory with specified limitations, provisional | Not independently validated; close mutual agreement does not establish either as correct |
| All 291 planned models | Not estimable: none | Confirmed in prior session (`manifest.json`: `models_planned: 291, models_estimated: 291, models_non_estimable: 0`) |

## Explicit statement on technical replication vs. causal identification

Everything labelled "validated" in this document means the reported number is confirmed to be what the stated specification, correctly implemented, actually produces — nothing more. It is not a claim that the specification identifies a causal effect. The baseline is explicitly associational throughout (cross-sectional design); the historical extension adds a real time dimension (within-cluster, cross-birth-cohort variation) that moves it closer to controlling for persistent local confounders than the current-round community model, but it remains vulnerable to the limitations in issue-register items #7, #9, and #10 (DHS/IHME overlap, migration/residence-proxy, and buffer/displacement uncertainty) and is not a causal estimate. No document in this package should be read as asserting otherwise, and none does.
