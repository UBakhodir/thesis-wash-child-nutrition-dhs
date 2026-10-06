# Historical WASH extension: validation milestone (2026-10-06)

Status: methodological and data-validation milestone. Contains no outcome estimates, no exposure extraction and no provisional readiness counts. Nothing here is a thesis result.

Scope: IPUMS-DHS extracts `idhs_00001` (superseded, retained for audit) and `idhs_00002` (current), for the samples Ethiopia 2016, Ghana 2014, Kenya 2014 and Nigeria 2018. Historical exposure is IHME modelled coverage for 2000–2017, not yet linked to any child.

Restricted microdata, respondent-level outputs, identifiers and coordinates are kept outside this repository and are not published here.

## 1. Structural validation (verified)

- `idhs_00002`: 60 selected variables; 71,413 records; each record exactly 340 characters; LF line endings; ASCII only; no malformed records.
- The XML codebook and the Stata infix file agree on the name, start and end column, and type of every variable. Columns are contiguous from 1 to 340 with no gaps or overlaps.
- Sample codes observed match the four expected samples. Rows per sample: Ethiopia 2016 10,641; Ghana 2014 5,884; Kenya 2014 20,964; Nigeria 2018 33,924.
- Source file hashes were unchanged after each import.

## 2. Observation unit (corrected)

- `idhs_00001` was earlier described as a woman-level extract. That was incorrect. Both extracts contain the same child-level birth-history rows: keyed on sample, case identifier and birth-history index, the keys are unique in each extract and identical across the two.
- The earlier problem with `idhs_00001` was missing child variables (anthropometry, child birth dates, child sex), not the observation unit. Maternal age on child records (15–49) does not identify the unit.
- Each mother can contribute several child rows (up to five or six).

## 3. Verified variable documentation

| Variable | Verified content | Note |
|---|---|---|
| HWHAZWHO, HWWAZWHO, HWWHZWHO | Z-score × 100; WHO reference (MGRS 2006); special codes 9995–9999 (height implausible, age-days implausible, flagged, missing, not in universe) | Stored values divided by 100 once, in derived fields only |
| KIDCURAGEMO | Current age in months; documented as available from Phase VII onward | Blank in Ghana 2014 and Kenya 2014 in this extract |
| KIDAGEMO | Documented as age in months at interview, computed as interview CMC minus birth CMC (calendar-month difference); no independent measurement date | Corrected: listed as available for all four samples (see correction note in section 7) |
| KIDDOBCMC | Gregorian birth CMC; for Ethiopia, documented as converted by IPUMS | Month precision only |
| INTDATECMC | Gregorian interview CMC; not provided for Ethiopia 2016 | Documented |
| INTDATECDC_ET | Century-day code for Ethiopian interview date; documented origin corresponding to 12 Sep 1907 | Provisional use only (section 4) |
| MONTHINT_ET | Months 1–12 only; 13th month documented as coded 12 | Not affected by 2016 fieldwork window |
| PERWEIGHT | Documented as the weight for nearly all child- or woman-level tabulations; six implied decimals | Not divided in this extract |
| KIDWT | Population adjustment factor for under-5 counts, based on external population sources | Not a sampling weight; not used |
| GPSLAT, GPSLONG | Displaced cluster coordinates (WGS84); zero means missing (documented) | Authorization required per sample |
| GPSLATLONG | Selection field returning GPSLAT and GPSLONG; not a separate coordinate | Not used |

## 4. Ethiopia 2016 interview dates (PROVISIONAL)

- Gregorian interview CMC is not provided for Ethiopia 2016 (documented). The Ethiopian-calendar fields are provided.
- The delivered Ethiopian day and month fields are not original 30-day Ethiopian dates: the day value 31 occurs in months with 30 days. Converting them directly would be invalid.
- The century-day code follows a month-length structure that differs from a 30-day count; its origin and the source of a constant two-day offset are not yet fully established.
- All candidate reconstructions are provisional. They fall within the official fieldwork window. Their month assignments differ for a material share of rows depending on method. None is validated.
- Ethiopia is retained in the analysis plan. Its timing is kept separate from established Gregorian timing and will be reported with explicit provisional labels.

## 5. Anthropometric measurement design (partly verified)

- Nigeria 2018: one-third of households were selected for biomarker and anthropometry measurement (secondary description of the final report). In this extract, 35% of listed children have a valid HAZ, consistent with that design. Non-measurement in Nigeria clusters within households.
- Ghana 2014: anthropometry was collected from a household subsample (secondary description; the official report PDF could not be read). Non-measurement clusters within households.
- Ethiopia 2016 and Kenya 2014: non-measurement is rare among listed children in this extract.
- Children not listed in the household are not measured in any sample (verified).
- The subsample design means anthropometric analysis may need a household-level measurement subsample weight. Whether such a weight exists in these extracts has not been verified.

## 6. Flags and plausibility

- Special codes are taken from the IPUMS labels in the extract. A secondary DHS source assigns different codes to the same categories; that conflict is unresolved.
- Proposed WHO plausibility limits (HAZ −6 to +6; WAZ −6 to +5; WHZ −5 to +5) are from secondary sources. The official WHO page was not read in full. They are used as flags only, not exclusions.
- No valid value in the extract lies beyond these limits, which is consistent with out-of-range measurements having been replaced by special codes. This does not validate the flag rule.

## 7. Corrections to earlier internal notes

- KIDAGEMO was earlier recorded as unavailable for the four samples. That was based on a session message. The availability list includes all four samples; the variable adds no measurement date beyond interview CMC minus birth CMC.
- Earlier notes that treated the Nigeria prenatal surplus as January–September 2018 births are corrected: the surplus equals the January 2018 births only.

## 8. Remaining decisions and actions for the author

1. Check the thesis author's DHS Program account for GPS-coordinate approvals for all four samples. Delivery of coordinates does not establish authorization.
2. Confirm KIDAGEMO on the IPUMS sample list directly and decide whether to revise the extract (instructions are in the local correction note; no extract was submitted).
3. Confirm whether an IPUMS-DHS child survival-status variable exists for these samples before requesting it. No variable name has been verified.
4. Check the official Nigeria 2018 and Ghana 2014 final reports for the measurement subsample and the weight to use.
5. Decide the primary Ethiopia treatment once the calendar question is answered (support inquiry drafted; not sent).
6. Decide the Nigeria round (2013 or 2018), the primary exposure window, and the pooled weighting estimand.

## 9. Not included in this milestone

- Outcome regressions, IHME exposure extraction and spatial matching.
- Any provisional readiness or eligibility counts.
- Respondent-level data, identifiers, coordinates and restricted outputs.
- Supervisor-meeting material and the untracked design note, which predates these findings and is superseded.
