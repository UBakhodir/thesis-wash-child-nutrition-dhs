# Historical WASH: authorization status and design checks (2026-10-06)

Status: public-safe update. Contains no respondent data, identifiers, coordinates or provisional readiness counts. Supersedes the earlier "GPS authorization unconfirmed" status in the 2026-10-06 milestone document. That document is unchanged.

## 1. GPS data authorization (country-level confirmed)

- The thesis author's DHS Program dataset account shows approved access, under the project "data collection to master thesis" (submitted 2026-06-21), for GPS data in Ethiopia, Ghana, Kenya and Nigeria. Three countries also list SPA; Nigeria lists SURVEY and GPS.
- The account page lists approvals by country, not by survey round. Round-level confirmation for the four samples (2016, 2014, 2014, 2018) is pending a check of the per-round dataset list.
- Restricted evidence (screenshot, account details) is kept outside the repository.
- DHS GPS data-use conditions (for example, on redistribution or publication) are not verified here. Coordinates are not published.

## 2. Coordinate-to-survey correspondence (verified)

Checked on the validated extract, aggregate only:

| Sample | Rows | DHSID matches country and survey year | DHSID one-to-one with PSU | Usable coordinates inside approximate national box |
|---|---|---|---|---|
| ET2016 | 10,641 | 100% | yes | 100% of usable |
| GH2014 | 5,884 | 100% | yes | 100% of usable |
| KE2014 | 20,964 | 100% | yes | 100% of usable |
| NG2018 | 33,924 | 100% | yes | 100% of usable |

The DHSID structure is defined in the DHS documentation as a 2-character country code, a 4-digit survey year and an 8-digit cluster number. The national boxes are coarse sanity limits, not official boundaries.

## 3. Measurement design (aggregate consistency)

- Nigeria 2018: one-third of households were selected for biomarker and anthropometry measurement (secondary description of the final report). Among households with listed children, the share with at least one measured child is 39%, and it varies by cluster (cluster mean 0.41; 11 clusters with no measured household; 12 with all measured). The pattern is consistent with a household-level subsample. It is not a verification of the design.
- Ghana 2014: anthropometry was collected from a household subsample (secondary description). Household measured share 49%.
- Ethiopia 2016 and Kenya 2014: most households with listed children are measured (91% and 96%).
- Children not listed in the household are not measured in any sample.

## 4. Weighting (position, not a decision)

- PERWEIGHT: documented as the weight for nearly all child- or woman-level tabulations. Applicable to the full listed-children sample.
- Measurement subsample: if analysis is restricted to measured households, a subsample weight may be needed. No subsample weight is verified in these extracts. The DHS forum guidance to select households flagged for the module (v042 = 1) refers to a variable whose IPUMS equivalent is unverified.
- KIDWT: population adjustment factor for counts. Not a sampling weight. Not used.
- Pooled cross-country estimand and normalisation: open. Normalised weights are not valid for pooled totals (documented in the World Bank catalogue for Nigeria 2018).

## 5. Spatial extraction (prepared, not run)

- Implementation: scripts/historical_wash/08_spatial_extraction_PREPARED.py.
- Rules: urban buffer 2 km, rural buffer 5 km (primary); rural 10 km sensitivity; refugee clusters excluded from the primary specification (no documented displacement rule); metric equal-area buffers (proposed CRS, to be confirmed); NoData never treated as zero; coordinate-order check using national boxes; zero pairs never extracted; nearest-pixel sensitivity.
- Self-test on synthetic points passes (8 of 8 rules, including swapped-coordinate rejection and NoData handling). The raster reader was checked on one real IHME file (metadata and value range only). No extraction has been run.
- Execution requires an explicit authorization flag and is not part of this milestone.

## 6. Ethiopia interview dates

Still provisional. Not validated as primary-analysis dates. Gregorian interview timing for Ethiopia 2016 is unresolved; the candidate constructions and the open support question are recorded in the local audit folder.

## 7. Remaining actions

1. Check the per-round dataset list in the DHS account for ET2016, GH2014, KE2014 and NG2018.
2. Read the DHS GPS data-use conditions before any publication.
3. Confirm the KIDAGEMO sample list on the IPUMS page and decide whether to request a revised extract.
4. Decide the measurement-subsample weighting approach once the Nigeria 2018 and Ghana 2014 final reports are checked.
5. Decide whether to send the Ethiopia support inquiry (drafted, not sent).
