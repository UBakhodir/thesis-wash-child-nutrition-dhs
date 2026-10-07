# Core reporting table: historical WASH extension, primary established-date models (2026-10-07)

All 24 cells below are the primary post_12m, weighted models (established-date sample: Ghana 2014, Kenya 2014, Nigeria 2018, pooled). Reused directly from `data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv` (RESTRICTED; public figures only below) — **no model was re-estimated to build this table.** Coefficient is per 10 percentage points of IHME-modelled local coverage (JMP-aligned improved-water/-sanitation definition; see `historical_wash_ihme_product_definitions_v1_2026-10-07.md`). E_resid_SD is the residual within-cluster exposure variation after controls, in percentage points — the quantity that actually identifies each coefficient (see `historical_wash_reporting_corrections_v1_2026-10-07.md` §2 for why this, not the equal country weight total, determines each country's influence on the pooled slope).

**Reporting status for every row below (uniform, per the corrected status scheme — see `01_final_reporting_map.md`):** exploratory; weighted conditional associations among eligible measured children (§1 of the corrections note); not yet ready for unqualified substantive reporting pending the issue-register items that apply to the whole extension (measurement-weight documentation, Nigeria's count gap, DHS/IHME overlap for Ghana/Kenya, residence-as-proxy and displacement/buffer-averaging). No row is privileged over another for being significant.

## Water (W_IMP)

| Outcome | Sample | β per 10 pts | SE | 95% CI | p | N | G (clusters) | E_resid_SD (pts) | Computational check |
|---|---|---|---|---|---|---|---|---|---|
| HAZ | Ghana 2014 | 1.648 | 0.665 | [0.339, 2.956] | .014 | 1,940 | 353 | 0.456 | **Validated: 17_validate_estimates.py (prior session, weighted and unweighted both checked), matches to 3e-14** |
| HAZ | Kenya 2014 | −0.606 | 0.747 | [−2.072, 0.859] | .417 | 14,166 | 1,498 | 0.203 | Internal design checks only (19) |
| HAZ | Nigeria 2018 | 0.700 | 0.282 | [0.148, 1.253] | .013 | 6,912 | 1,263 | 0.652 | Internal design checks only (19) |
| HAZ | **Pooled established** | **1.026** | 0.261 | [0.514, 1.537] | **<.001** | 23,018 | 3,114 | 0.428 | **Independently rebuilt and re-estimated this session (20); matches to 6.7e-08** |
| WAZ | Ghana 2014 | 1.063 | 0.621 | [−0.158, 2.284] | .088 | 1,940 | 353 | 0.456 | Internal design checks only (19) |
| WAZ | Kenya 2014 | −0.219 | 0.549 | [−1.296, 0.858] | .690 | 14,166 | 1,498 | 0.203 | Internal design checks only (19) |
| WAZ | Nigeria 2018 | 0.449 | 0.229 | [0.000, 0.898] | .050 | 6,951 | 1,264 | 0.651 | Internal design checks only (19) |
| WAZ | Pooled established | 0.647 | 0.228 | [0.199, 1.095] | .005 | 23,057 | 3,115 | 0.428 | Internal design checks only (19); not separately rebuilt |
| WHZ | Ghana 2014 | −0.002 | 0.589 | [−1.160, 1.156] | .997 | 1,940 | 353 | 0.456 | Internal design checks only (19) |
| WHZ | Kenya 2014 | −0.163 | 0.573 | [−1.286, 0.961] | .776 | 14,166 | 1,498 | 0.203 | Internal design checks only (19) |
| WHZ | Nigeria 2018 | −0.053 | 0.219 | [−0.482, 0.376] | .809 | 6,942 | 1,264 | 0.651 | Internal design checks only (19) |
| WHZ | Pooled established | −0.078 | 0.216 | [−0.501, 0.345] | .717 | 23,048 | 3,115 | 0.428 | Internal design checks only (19); not separately rebuilt |

## Sanitation (S_IMP)

| Outcome | Sample | β per 10 pts | SE | 95% CI | p | N | G (clusters) | E_resid_SD (pts) | Computational check |
|---|---|---|---|---|---|---|---|---|---|
| HAZ | Ghana 2014 | −2.480 | 1.238 | [−4.915, −0.045] | .046 | 1,940 | 353 | 0.258 | Internal design checks only (19) |
| HAZ | Kenya 2014 | −0.212 | 0.162 | [−0.530, 0.105] | .190 | 14,166 | 1,498 | 0.877 | Internal design checks only (19) |
| HAZ | Nigeria 2018 | 0.203 | 0.279 | [−0.344, 0.750] | .467 | 6,912 | 1,263 | 0.648 | **Validated: 17_validate_estimates.py (prior session), matches to 3e-14** |
| HAZ | Pooled established | −0.096 | 0.137 | [−0.365, 0.173] | .483 | 23,018 | 3,114 | 0.788 | Internal design checks only (19); not separately rebuilt |
| WAZ | Ghana 2014 | −0.081 | 0.997 | [−2.042, 1.879] | .935 | 1,940 | 353 | 0.258 | **Validated: 17_validate_estimates.py (prior session), matches to 3e-14** |
| WAZ | Kenya 2014 | −0.147 | 0.121 | [−0.384, 0.089] | .223 | 14,166 | 1,498 | 0.877 | Internal design checks only (19) |
| WAZ | Nigeria 2018 | 0.019 | 0.234 | [−0.440, 0.477] | .937 | 6,951 | 1,264 | 0.647 | Internal design checks only (19) |
| WAZ | Pooled established | −0.072 | 0.110 | [−0.288, 0.143] | .511 | 23,057 | 3,115 | 0.787 | Internal design checks only (19); not separately rebuilt |
| WHZ | Ghana 2014 | 1.644 | 0.972 | [−0.269, 3.556] | .092 | 1,940 | 353 | 0.258 | Internal design checks only (19) |
| WHZ | Kenya 2014 | 0.003 | 0.112 | [−0.217, 0.222] | .980 | 14,166 | 1,498 | 0.877 | Internal design checks only (19) |
| WHZ | Nigeria 2018 | −0.175 | 0.211 | [−0.589, 0.239] | .407 | 6,942 | 1,264 | 0.647 | Internal design checks only (19) |
| WHZ | Pooled established | −0.035 | 0.106 | [−0.242, 0.173] | .742 | 23,048 | 3,115 | 0.787 | Internal design checks only (19); not separately rebuilt |

## Reading this table

- **Computational check** tells you how much independent numerical scrutiny a specific cell has had — nothing more. "Internal design checks only" still means record keys, cluster-survey mapping, weight totals, rank, and singleton treatment were all verified correct (`19_check_model_design.py`, all pass); it does not mean the coefficient itself was independently re-derived by a second implementation.
- A cell being independently re-derived (pooled water HAZ; the two Ghana/Nigeria cells from the prior session) does not make it more "true" or more reportable than its neighbours — it means a coding error is less likely to be the explanation if the number looks surprising.
- Read p-values and significance across this whole table as a multiplicity problem, not twelve independent tests: with 24 primary cells (and 291 counting every sensitivity family), some p<.05 results are expected by chance alone. The pooled water-HAZ result (p<.001) is the one result in this table unlikely to be a multiplicity artefact on its own; it is reported with exactly the same methodological caveats as the rest of the table, not fewer.
- Unweighted counterparts, window sensitivities, and the full sensitivity families are in `historical_wash_preliminary_estimates_v1/` and the methods note; not repeated here to keep this table to the primary specification only, per the instruction to reuse existing outputs rather than generate new tables beyond what was asked.
