# Appendix C — Historical exposure-assignment diagnostics and the Ethiopia provisional analysis

Clearly labelled exploratory material, consistent with Section 5.9. Nothing in this appendix is part of the established-date pooled headline result and none of it should be cited as such.

## C.1 Ethiopia's three interview-date candidates

Ethiopian survey rounds record interview dates in the Ethiopian calendar, which must be converted to the Gregorian calendar to place a child's postnatal exposure window relative to the (Gregorian-dated) IHME annual rasters. Three candidate conversions were constructed:

- **C1** ("triple," 30-day Ethiopian-calendar arithmetic applied directly to the delivered day and month fields). **Invalid and superseded**: the delivered Ethiopian day and month fields are not themselves original 30-day Ethiopian dates (day value 31 occurs in months the Ethiopian calendar defines as having 30 days), so direct 30-day arithmetic conversion is invalid for these fields — a conclusion reached independently of, and prior to, any WASH-outcome analysis. 275 of 10,641 Ethiopia children have an outright invalid C1 day value under this method; the remainder share the same invalid conversion logic. C1 is excluded from all reporting tables in this thesis and its historical agreement with C2/C3 is not treated as evidence of either candidate's validity.
- **C2** ("century-day route," origin 1 Meskerem 1900 = 12 September 1907). Provisional; not independently validated.
- **C3** ("century-day route," anchored 1 Meskerem 2008 = 12 September 2015, Gregorian cumulative month lengths). Provisional; not independently validated.

## C.2 How much C2 and C3 actually agree (measured directly, not assumed)

| Window | C2 eligible | C3 eligible | Disagree |
|---|---|---|---|
| Birth-year | 9,862 | 9,862 | 0 |
| Prenatal (9 months) | 9,862 | 9,862 | 0 |
| Post-12-month | 7,930 | 7,922 | 8 |
| Post-24-month | 5,974 | 5,969 | 5 |

Out of 10,641 Ethiopia children: C1-vs-C2/C3 differ by exactly the 275 invalid-day exclusions (and C2/C3 never differ from each other on birth year itself — identical across all three candidates for every child, since birth year is derived from the birth-date fields, not the interview date). This supports two precise, narrow claims: (1) C2 and C3 agree almost perfectly on window eligibility, so the remaining uncertainty between them changes very few children's classification; (2) this is *not* evidence that either candidate's absolute date is correct. A working Gregorian interview date is still required for every child regardless of window, because it determines whether a child is validly dated at all and whether their birth genuinely precedes their interview (Section 3.7) — but, as Section 3.7 and the construction script state precisely, this requirement is distinct from the postnatal-window **completion** check specifically: that completion check (whether enough time had elapsed by the interview date for the window itself to have finished) applies only to the two postnatal windows (post-12-month, post-24-month), not to the birth-year window, which has no completion check at all and is satisfied by construction once a child's birth date is validly placed in a calendar year.

## C.3 Ethiopia provisional coefficients (water HAZ, sanitation HAZ, post-12-month window)

| Candidate | Water β per 10 | Sanitation β per 10 |
|---|---|---|
| C2 | −0.39 | −0.45 |
| C3 | −0.39 | −0.45 |

Both confidence intervals include zero. These are reported here, and cross-referenced in Section 5.9, as an exploratory sensitivity with no bearing on the established-date pooled results in Section 5.6.

## C.4 Spatial-extraction and sensitivity diagnostics (established-date models, summarised)

| Diagnostic | Result |
|---|---|
| Buffer coverage-completeness tolerance | Within 10⁻³ of full buffer area |
| Spatial-method sensitivity (containing-pixel vs. exact buffer average) | Pooled water–HAZ: 0.68 vs. main 1.03 |
| Rural-10km buffer sensitivity (urban unchanged) | Pooled water–HAZ: 1.01 vs. main 1.03 |
| Stricter postnatal completion rule (+1 month) | Pooled water–HAZ: 0.95 vs. main 1.03 |
| Calendar-month age construction throughout | Pooled water–HAZ: 1.03 (materially unchanged) |
| DHS/IHME overlap exclusion (Ghana removed) | Pooled water–HAZ: 0.74, Kenya+Nigeria only |

No sensitivity cell was selected or suppressed based on its significance; all are reported together as a pre-specified sensitivity family (`docs/provenance/historical_wash_preliminary_estimation_methods_2026-10-06.md` §7).
