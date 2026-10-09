# Final reporting map, v3 — corrected (2026-10-07, second pass)

Supersedes `final_empirical_package_v2_2026-10-07/01_final_reporting_map.md`. v2 is preserved unchanged with a pointer banner. Two corrections from `historical_wash_reporting_corrections_v1_2026-10-07.md` are applied here: (1) confounding language is changed from a definitive claim to an attenuation-consistent-with-confounding claim; (2) the historical extension's status scheme is flattened — computational verification and reporting readiness are now separate columns, and the pooled water–HAZ model is no longer placed in a higher reporting tier than its sibling models.

## Baseline (current four-round, cross-sectional) — unchanged except row 3

| Analysis family | Status | Note |
|---|---|---|
| Household water/sanitation, cluster FE, PRIMARY convention | Validated for main reporting | p=.062 water, p=.548 sanitation (HAZ) |
| Household water/sanitation, region FE | Validated for main reporting | |
| **Community water/sanitation, 4-stage adjustment** | Validated for main reporting | **Corrected:** the community association attenuates sharply and loses significance once SES and region controls are added (0.447/0.472 unadjusted → 0.033/0.008 adjusted, both p>.5). This pattern is consistent with confounding by socioeconomic status but does not, on its own, establish confounding as the sole explanation for the unadjusted association. (Was: "minimal model is confounded" — corrected per §4 of the corrections note.) |
| Household cluster-FE, FULL_DUMMY_DF convention | Validated sensitivity | p=.080/.574 — label explicitly if cited |
| Joint household+community model | Validated sensitivity | Single significant cell (p=.043) — report, do not treat as central |
| Age-heterogeneity joint tests | Validated sensitivity | 11 of 12 reject (corrected count) |
| Nigeria community-sanitation specification path | Validated sensitivity | Demonstrates instability, not a finding of harm |
| Country-specific household cluster-FE models | Validated sensitivity | |
| Alternative weights / binary LPM / biodigester / LOO-denominator robustness | Validated sensitivity | Not re-audited; unchanged since frozen |

## Historical extension — corrected status scheme

Two separate axes, not one. See `02_core_reporting_table.md` for the full 24-cell table with both columns populated.

| Analysis family | Computational check | Reporting status (uniform across the family) | Note |
|---|---|---|---|
| Pooled established water–HAZ, post_12m, weighted (headline) | Independently rebuilt and re-estimated this session (`20_validate_pooled_estimate.py`); matches stored value to 6.7×10⁻⁸ | Exploratory; weighted conditional association among eligible measured children; not yet ready for unqualified substantive reporting | **No longer labelled "Validated for main reporting."** Being significant (p<.001) and being independently reconfirmed are both true and both stated, but neither changes its reporting tier relative to its sibling cells — see §3 of the corrections note. |
| Pooled unweighted counterpart, same observations | Independently rebuilt this session; matches documented 0.41 | Same as above | Confirms sensitivity to the equal-country-weighting choice; this is a disclosed, authorized design choice (issue register #8), not evidence either weighting is "more correct." |
| 3 of the 4 country-specific cells validated by the prior session's 4-model check (Ghana water HAZ; Ghana sanitation WAZ; Nigeria sanitation HAZ — the 4th, Ghana water HAZ unweighted, is not a primary-table cell) | Independently validated prior session (`17_validate_estimates.py`); matches to 3×10⁻¹⁴ | Same as above | |
| All other 20 primary established-date cells (water/sanitation × HAZ/WAZ/WHZ × country/pooled, not listed above) | **Status correction (2026-10-09): now independently re-derived.** All 20 (and, with the rows above, all 24) have since been independently re-estimated by a second library/sample (`21_validate_all_primary_cells.py`, coefficients to ≤6×10⁻¹⁴) with SE/CI/p subsequently reconciled to floating-point precision (`24_reconcile_inference_corrections.py`). Row preserved below for the historical record only; do not read "Internal design checks only" as the current state: ~~Internal design checks only (`19_check_model_design.py`): unique keys, rank full, singleton-free, weight totals correct~~ | Same as above | All 24 primary cells are now independently re-derived by a second implementation, not only internally consistent. |
| 267 sensitivity-family models (windows, wealth, containing-pixel, rural-10km, stricter completion, calendar age, overlap exclusions) | Internal design checks only | Same as above | |
| Ethiopia C1 (6 models) | N/A — method itself invalid | **Invalid/superseded** | Do not cite, including as corroborating evidence for C2/C3. |
| Ethiopia C2, C3 (12 models) | Internal design checks only; not independently re-estimated | Exploratory, provisional (same methodological caveats as the established-date family, plus Ethiopia's own unresolved interview-timing issue) | Close C2/C3 eligibility agreement (register item #5) is not validation. |
| All 291 planned models | — | Not estimable: none | Unchanged from prior sessions. |

## Which historical analyses can be reported, and how

All 24 primary established-date cells (water and sanitation, HAZ/WAZ/WHZ, three countries and pooled) **can** be reported in the thesis now, reused directly from `02_core_reporting_table.md` — this is not withheld pending Ethiopia, which remains a separate, clearly-labelled provisional sensitivity and does not block reporting the established-date family. Every reported cell must carry, every time, the same qualifications: weighted conditional associations among eligible measured children (not population estimates); pooled estimates reflect equal country weight totals but country-specific *influence* on the slope depends on residual exposure variation, which differs substantially by country; associations, not causal effects; DHS/IHME input overlap for Ghana and Kenya is disclosed, not removed.

## Explicit statement on technical replication vs. causal identification (unchanged from v2)

Everything "computationally checked" in this document means the reported number is confirmed to be what the stated specification, correctly implemented, actually produces — nothing more. It is not a claim that the specification identifies a causal effect, and it is not a claim that the number is ready for unqualified substantive reporting; reporting readiness is governed by the issue register (`historical_wash_issue_register_v1_2026-10-07.md`), which applies uniformly across the historical family regardless of which cells have received extra computational scrutiny.
