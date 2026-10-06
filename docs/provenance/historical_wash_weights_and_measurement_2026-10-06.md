# Weights and measurement subsampling: documented requirements, inference and open items (2026-10-06)

Purpose: decide what can be documented about the within-survey weight and the anthropometry eligibility before the specification is estimated. Three categories are kept apart: (A) quoted official text; (B) verified facts from the validated extract; (C) inference, not documented.

## 1. Official sources and access

| Source | Status | Use here |
|---|---|---|
| Nigeria DHS 2018 final report (national repository copy) | Read in full (local extraction of the report PDF) | Quoted below (A) |
| IPUMS-DHS PERWEIGHT, KIDWT and HWHAZWHO pages | Read (WebFetch summaries) | Quoted below (A) |
| Ghana DHS 2014 final report | Not retrievable: the statsghana host returned an expired certificate; search summaries only | Not used as a source; limitation stated |
| DHS Program biomarker guidance (DHS-6 and DHS-8 documents, Guide to DHS Statistics) | Blocked (HTTP 403) on every official DHS URL tried | Not used; limitation stated |

Blocked DHS URLs do not establish that the documentation is unavailable. The Nigeria report was retrieved from the national repository, which is an authoritative alternative location for the same report.

## 2. What the Nigeria 2018 final report states (A, quoted)

Subsample design:
- "The men's survey was conducted in one-third of the sample households, and all men age 15-59 in these households were included. ... Similarly, biomarker information was collected only in those households selected for the men's survey. The biomarkers included in this survey were height and weight for women age 15-49 and children age 0-59 months ..."
- "One-third of the households (14,000) were selected for malaria, anaemia, and genotype testing of children age 6-59 months."

Eligibility:
- "All children age 0-59 months and all women age 15-49 were eligible for height and weight measurements" (in the subsample households; the biomarker questionnaire was administered only to that subsample).

Anthropometric sample:
- "Height and weight measurements were obtained for 12,806 (unweighted) children under age 5 who were eligible to be measured in the 2018 NDHS subsample households at the time of the survey. The analysis of anthropometric indices ... included valid dates of birth and measures of both height and weight. Valid height data were available for 86% of children, and valid weight data were available for 87% of children."

Weights:
- "Due to the non-proportional allocation of the sample to the different states and the possible differences in response rates, sampling weights were calculated, added to the data file, and applied so that the results would be representative at the national level as well as the domain level. ... sampling weights were calculated based on sampling probabilities separately for each sampling stage and for each cluster."
- The only additional weight described in the report is the domestic-violence special weight ("a special weight for domestic violence was calculated that account[s] for the selection of one woman per household"). No anthropometry or biomarker weight is described.
- Quality control: re-measurement of all children with values outside pre-specified flags on a subsequent day, and of a random 10% of children.

IPUMS-DHS (A, quoted):
- PERWEIGHT: "should be used to weight nearly all tabulations made using IPUMS-DHS data when women or children are the unit of analysis." Subsample modules: "a specialized weight such as DVWEIGHT should be used instead."
- KIDWT: "a population adjustment factor created by IPUMS to generate count estimates of children under the age of 5" based on population sources outside the DHS.
- HWHAZWHO: Z-score × 100; special codes 9995–9999; WHO MGRS 2006 reference.

## 3. What the validated extract shows (B)

- Nigeria 2018: 33,924 birth-history child records. Non-NIU (measured or flagged) 11,704; valid HAZ 11,364; all three Z-scores valid 11,314. Not-listed-in-household children are not measured in any sample (100%).
- Household clustering of measurement (listed children): in Nigeria 5,762 households are entirely unmeasured, 2,974 entirely measured and 876 mixed. The measured share of households with listed children is 38.6%, close to the one-third design. Cluster-level shares vary (mean 0.41, standard deviation 0.16; 11 clusters with no measured household, 12 with all measured).
- Ghana 2014: measured share of listed children 47.8%; household share 49.5%; household clustering of non-measurement (692 all unmeasured, 623 all measured, 91 mixed among households with at least two listed children).
- Ethiopia 2016 and Kenya 2014: most households with listed children are measured (91% and 96%).
- The extract has no variable that identifies the measurement subsample (household selection flag) and no measurement-eligibility or consent flag.

## 4. Reconciliation that is not resolved (B vs A)

| Quantity | Official report (Nigeria 2018) | Extract (validated) | Status |
|---|---|---|---|
| Children measured (under 5) | 12,806 unweighted, "eligible ... in the subsample households" | 11,704 non-NIU (measured or flagged); 11,364 valid HAZ | Not reconciled. The extract covers birth-history children of interviewed women; children whose mothers are not in the sample may be absent. This is a hypothesis and cannot be checked without the household file. |
| Valid height share | 86% of children (with valid birth dates and both measures) | 97% of non-NIU children have valid HAZ | Not reconciled. Different denominators and validity definitions. |

The valid-count difference does not change the analysis rule (valid outcome), but it means the extract's measured sample is not a complete census of eligible children.

## 5. Inference: what the weight question requires (C, not documented)

1. Within-survey weight. PERWEIGHT (the person/child weight) is the documented weight for child-level tabulations (A). It is therefore the appropriate default for the measured sample.
2. Subsample factor. The measured households are a one-third subsample by design (A). If the subsample is a random selection of households, its probability of selection is constant, and within-survey normalization removes the constant factor. Relative weights within the subsample are then unchanged. This is inference from the design, not a documented rule for anthropometry.
3. Differential non-response. Eligible children in subsample households who were not measured (listed, not measured; 20,477 in Nigeria) may differ from measured children. No documented weight corrects for this. Whether a non-response adjustment is needed is unresolved.
4. Measurement-subsample weight. The NDHS report describes no separate anthropometry or biomarker weight (A). Whether the DHS recode provides one (for example a biomarker weight) cannot be checked, because the DHS documentation was blocked.

Conclusion for the specification (proposed):
- Use PERWEIGHT, normalized within survey to mean 1 over the analysis sample; treat the measured sample as the analysis population, which the report defines as the eligible population for analysis of anthropometric indices (the report's own anthropometry analyses use measured children with valid dates).
- Do not use KIDWT.
- Report the non-response uncertainty explicitly; do not claim a population-representative estimate of all eligible children.

## 6. Open items (unresolved; cannot be closed from available documents)

- The Ghana 2014 subsample rule and any Ghana-specific weight: the report could not be read.
- A DHS biomarker weight, if one exists: the DHS documents were blocked.
- Whether the IPUMS children extract includes all children in subsample households: requires the household-level file or the IPUMS variable list; not verified.
- The subsample household flag: not in the extract. Requesting it is a decision (section 7 of the decision table).

No weight has been finalized for any estimate.
