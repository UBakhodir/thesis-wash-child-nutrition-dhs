# Historical WASH: decisions required before any outcome model (2026-10-06)

Only choices that genuinely require author or supervisor input are listed. Items settled by documentation, data checks or the repository's existing conventions are not listed.

Proposed configuration for review. Choices are not made from any result; the proposals are based on design, documentation and the temporal-coverage reasons already recorded in the repository's empirical strategy.

| # | Issue | Evidence | Proposed (reviewable) | Alternatives and consequence | Next action |
|---|---|---|---|---|---|
| 1 | Primary exposure window | All four windows are constructed; sample sizes differ by completion (for example Nigeria: birth-year 9,214 vs post-12 months 6,986 final intersection for HAZ water) | First 12 postnatal months: a fixed early-life window with birth month included and a clear completion rule; not described as the "first 1,000 days" | 24 postnatal months (fewer complete children; longer exposure averaging); prenatal 9 months (pregnancy-period assignment, depends on birth month); birth year (coarse, one calendar year) | Author to choose; all four are pre-specified sensitivity analyses |
| 2 | Nigeria round | Extract has 2018 (retained for construction). Repository empirical strategy recommends 2013 on temporal-coverage grounds (2018 births extend past 2017). The DHS account page lists Nigeria 2013 (survey and GPS download) | Keep 2018 for the current extraction; decide whether a revised extract adding 2013 is wanted | 2013 needs a new IPUMS extract (not requested here; instructions would follow). 2018 has large window-exclusion counts (5,601 births in 2018 fall outside the birth-year window; 4,240 post-12-month records extend into 2018) | Author decision; if 2013 is chosen, a revised extract is requested separately |
| 3 | Ethiopia's role | Interview timing remains provisional (candidates C2 and C3 agree on exposure; they differ in completion for some rows) | Sensitivity analysis only, with provisional labels; excluded from the primary estimate | Pooled with established samples under explicit provisional labels; excluded permanently (not recommended while timing is unresolved) | Author decision; keep the support question to IPUMS/DHS open |
| 4 | Pooled weighting estimand | Official text: normalized weights are relative and not valid for pooled totals (World Bank catalogue, Nigeria 2018). Baseline pools equal country totals | Within-survey normalized PERWEIGHT, pooled with equal country totals (baseline convention) | Country-proportional pooling; unweighted pooling | Author and supervisor decision; no estimate until chosen |
| 5 | Wealth adjustment | WEALTHQ is a household index that includes water and sanitation assets, so it overlaps with the exposure | Primary: no wealth control (avoids adjusting for an exposure component). Sensitivity: wealth quintile included | Include wealth in primary (conventional SES control, with overlap risk) | Author decision |
| 6 | Measurement-subsample flag | Official design: anthropometry only in one-third of households. The extract has no subsample flag | Analyse measured children with standard weights; report the non-response limitation | Request a household subsample variable (name not verified; would need IPUMS check and a revised extract); or accept the measured-sample definition | Author decision on whether to request a revised extract; not requested here |
| 7 | Under-five age definition | Reported completed age is delivered only for Ethiopia and Nigeria; derived calendar age for Ghana and Kenya | Reported completed months where delivered, otherwise derived calendar months (within survey) | Calendar months for all children (consistent across surveys; one month larger than completed at most) | Author decision (small; sensitivity analysis already specified) |
| 8 | Ghana and Kenya water overlap with DHS inputs | Repository empirical strategy and the IHME input workbooks | Keep, with disclosure; sensitivity excludes the overlapping product | Exclude overlapping products in primary | Author and supervisor decision |

## What is already settled (not decisions)

- The within-cluster inference convention (repository adjudication record).
- The exposure construction rules (completion, annual weights, complete spatial coverage, containing-pixel and rural 10 km as sensitivity).
- Ethiopia's Candidate 1 invalid days (275 rows; exclusion is explained by the day values, not by interview timing).
- The area-averaging denominator (valid overlap area) and its geometry approximation (addendum).
- Ghana, Kenya and Nigeria Gregorian timing (established month-level).

## Essential blockers (not closable from available documents)

1. Ghana 2014 subsample rule and any Ghana weight: report not readable (certificate expired); no official alternative located.
2. DHS biomarker weight documentation: blocked (HTTP 403).
3. Nigeria measured count: official 12,806 vs extract 11,704 non-NIU; likely absence of children whose mothers are not interviewed, not verified.
4. Ethiopia interview timing: provisional; support question drafted (not sent).
5. KIDCURAGEMO for Ghana and Kenya: blank; the phase explanation is contradicted by the account labels (all four rounds DHS-7), so the cause is unknown.
