# Final empirical package v3 — results index (2026-10-07, second pass, reporting-only correction)

Supersedes `final_empirical_package_v2_2026-10-07/00_results_index.md` for the historical-extension language in its §C only. v2 and v1 are preserved unchanged with pointer banners; nothing else in v2 (baseline §A, Ethiopia disposition, IHME resolution, independent verification results) changed — this file does not repeat what did not change.

## What changed in this pass

Reporting language only — no model rerun, no new number. See `historical_wash_reporting_corrections_v1_2026-10-07.md` for the full reasoning behind each correction:

1. **Measurement-sample language**: "population-representative within the measured subsample" → "weighted conditional associations among eligible measured children," with an explicit statement that using unweighted estimates does not resolve the selection concern.
2. **Pooled-estimand language**: equal country weight totals ≠ the pooled coefficient being the arithmetic mean of country-specific coefficients. Shown with the actual numbers: simple mean of the three country water-HAZ coefficients = 0.581; actual pooled coefficient = 1.026. The pooled slope is driven by weight **and** residual exposure variation together.
3. **Historical reporting status**: computational verification (did the number reproduce correctly?) and reporting readiness (is it qualified appropriately for the manuscript?) are now reported as separate axes. The pooled water–HAZ model is no longer in a higher reporting tier than its sibling historical models merely for being significant or independently re-derived.
4. **Confounding language**: "the minimal model is confounded" → "attenuation after adjustment is consistent with confounding but does not establish the sole explanation" (matching `docs/empirical_strategy.md`'s existing, more careful phrasing).

## Current authoritative files

| Topic | File |
|---|---|
| Baseline results, Ethiopia disposition, IHME definitions, independent pooled-model verification numbers | `final_empirical_package_v2_2026-10-07/00_results_index.md` (unchanged, still current for everything except its §C language, corrected below) |
| Corrected historical reporting-status scheme and confounding language | `final_empirical_package_v3_2026-10-07/01_final_reporting_map.md` (this folder) |
| Balanced core reporting table (24 primary cells, water + sanitation × HAZ/WAZ/WHZ × country + pooled) | `final_empirical_package_v3_2026-10-07/02_core_reporting_table.md` (this folder) — reused directly from stored outputs, no new estimation |
| Full reasoning for each of the 4 corrections | `historical_wash_reporting_corrections_v1_2026-10-07.md` |
| Issue register (unchanged; items #1 and #8's "reporting consequence" phrasing is corrected by the language above, not by editing the register's cell text) | `historical_wash_issue_register_v1_2026-10-07.md` |

## Explicit scope statement

This pass corrects language only. It does not re-open, re-estimate, or newly validate anything beyond what the prior two passes already established. It does not draft any thesis chapter text; the core reporting table is data for a chapter to use, not chapter prose.
