# Literature Evidence Summary

*This is a structured summary of the project's literature collection and evidence base. It is NOT thesis prose — it is a working reference document for planning the thesis's literature review, methods justification, and discussion sections. Generated from `literature_evidence_matrix.csv`, `literature_design_comparison.csv`, `literature_results_comparison.csv`, and `bibliography_source_audit.csv` in this same folder/`sources/bibliography/`.*

## 1. What literature we now have

35 PDFs across 7 folders: `sources/articles/01_Child_Nutrition/` (6), `02_WASH/` (7), `03_DHS/` (3), `04_GIS/` (1), `06_Methodology/` (2), `sources/reports/` (13), `sources/papers/` (3). 25 were part of the initial literature collection; 10 were added to address identified evidence gaps (Kenya/Nigeria/Ghana-specific WASH evidence, leave-one-out exposure methodology, and official DHS sampling/GPS documentation). Of the 35, 25 have been read in full or near-full; the remaining large institutional reports (JMP 2025, the WHO growth-standard monographs, `Guide to DHS Statistics`) were read via targeted sections rather than cover-to-cover, given their length (up to 834 pages).

By priority: **6 Core**, **17 Supporting**, **12 Background** (not forced — many sources genuinely are background/contextual only).

## 2. Major evidence themes

- **WASH's association with child anthropometric outcomes is real but inconsistent across studies, populations, and exposure definitions.** Systematic-review evidence (Momberg et al. 2021, S08) finds water significant in only 21/46 and sanitation in only 15/46 reviewed SSA studies. Individual country studies swing between significant protective associations (Addae et al. 2024, Ghana; DHS SAR23, Nigeria community-level) and null findings (Gebru et al. 2019, Ethiopia; multiple Nigeria NDHS studies found during the gap search).
- **Causal RCT evidence is a genuine, unresolved counterweight.** The three largest WASH RCTs to date (WASH-Benefits Bangladesh/Kenya, SHINE Zimbabwe — synthesized in Cumming et al. 2019, S10) found **no causal effect** of basic WASH interventions on child linear growth. This must be addressed explicitly in the thesis discussion, not glossed over: our own cross-sectional associational design cannot confirm or refute this causal null result, and any observed association should be framed accordingly.
- **Cluster/community-level WASH exposure aggregation has real precedent in this literature, but true leave-one-out construction is rare.** Of every cluster-level exposure source examined (Günther & Fink 2010, Spears 2013, Skoufias & Vinha 2026, DHS SAR23), only **one** — Geruso & Spears (2018/NBER WP 2015) — implements a genuine leave-one-out (own-household-excluded) measure, and it does so for infant mortality in India, not anthropometry in SSA.
- **HAZ is the most theoretically justified single outcome.** Victora et al. (2008, S03) shows HAZ at age 2 is the strongest predictor of adult human capital across five international cohorts, and Spears (2013, S34) is the closest empirical match using HAZ as its sole outcome against a sanitation-coverage exposure.

## 3. Strongest methodological precedents

- **Leave-one-out exposure construction**: Geruso & Spears (2018/NBER WP 21184, S18) — the only Type A source found. Explicit equation and rationale, verified directly from the PDF (p.11).
- **Administrative-region FE over a spatial grid**: Blom, Ortiz-Bobea & Hoddinott (2022, S04) and Headey & Palloni (2019, S19) both independently justify admin-region FE on the same grounds our design uses (DHS clusters not repeated / DHS representativeness), from two different research groups and periods.
- **PSU-clustered SEs and DHS weight/pooling mechanics**: The DHS Program's own official documentation (`Guide to DHS Statistics` DHS-8, S32; `Sampling and Household Listing Manual`, S31) is now in the collection and gives the exact formulas — critically, the **pooled-weight de-normalization procedure that directly underlies our pooled equal-total-country weighting choice exists only in the Sampling Manual (S31, §1.13.5–1.13.7), not in the Guide to DHS Statistics.** Both documents are needed; neither alone is sufficient.
- **GPS displacement and cluster-to-region linkage**: DHS SAR7 (S29) gives the exact displacement parameters (urban ≤2km, rural ≤5km, 1% of rural ≤10km, admin-2 boundary restriction); DHS SAR8 (S30) gives the official recommendation for areal-unit linkage (weighted-average / most-probable-value over naive point extraction) with simulation evidence that misclassification risk is low (~4.5%) at coarser administrative levels comparable to our own linkage scale.

## 4. Country-specific evidence coverage

| Country | Dedicated WASH-anthropometric DHS/MICS evidence | Notes |
|---|---|---|
| **Ethiopia** | Gebru et al. 2019 (S05) — general determinants study, water/toilet as secondary covariates, national null finding for water | No dedicated *WASH-focused* (not general-determinants) Ethiopia study found |
| **Ghana** | Addae et al. 2024 (S13) — dedicated, significant findings | **MICS, not DHS** — must not be conflated or pooled with our DHS-based results |
| **Kenya** | Rakotomanana et al. 2020 (S11) — dedicated, DHS-based | Kenya-specific numeric coefficient confirmed: beta=0.13 (p<0.01), R2=0.20 (Table 4, p.8) |
| **Nigeria** | DHS SAR23 (S28) — official DHS Program, dedicated, cluster-vs-household contrast | Own-inclusive, not leave-one-out; mixed regional pattern (significant in only 2 of 6 geopolitical zones) |

All four countries now have at least one dedicated source; Ethiopia's remains the weakest (general-determinants only, not WASH-focused).

## 5. Where findings agree / disagree with our own results

Using our own already-completed, unmodified pooled Model 4 and binary-LPM results (`outputs/final_tables/final_table4...csv`, `final_table6...csv`):

- **Agreement**: our pooled Model 4 continuous-outcome coefficients (HAZ: water 0.033 SE 0.059, sanitation 0.008 SE 0.062; both far from significant once full controls + admin-region FE are added) are broadly consistent with the literature's general pattern that WASH associations shrink substantially once socioeconomic/geographic confounders are controlled (e.g., Gebru et al. 2019's null water finding after full adjustment; Model 1→4 in our own table shows the same attenuation pattern, from 0.447 down to 0.033 for water on HAZ).
- **Notable disagreement worth discussing explicitly**: DHS SAR23 (S28) finds a small but statistically significant **protective** association between community sanitation coverage and Nigeria stunting (adjusted OR=0.97 per 10pp, i.e. ~3% lower odds). Our own Nigeria-specific binary-LPM result for `sanitation_rate_loo_core` is **0.077 [0.024, 0.130] — significant and in the opposite (harmful) direction.** This is a genuine, substantively important discrepancy. Plausible explanations (not adjudicated here) include: the own-inclusive vs. leave-one-out construction difference, different DHS survey rounds, or genuine underlying heterogeneity — this deserves explicit treatment in the thesis discussion rather than being smoothed over.
- Water coverage shows a significant protective LPM association with Nigeria stunting in our results (-0.059 [-0.111,-0.006]), consistent in direction with the general WASH-protective literature.

## 6. Remaining evidence gaps

- **No source anywhere in the literature implements leave-one-out cluster exposure for a WASH→anthropometric-outcome relationship specifically** (Geruso & Spears's leave-one-out precedent is for mortality in India).
- **Ethiopia** still lacks a WASH-focused (rather than general-determinants) DHS study.
- **JMP's own estimation methodology** (Annex 1 of the 2025 report) has not been independently read — relevant if the methods chapter wants to describe JMP's interpolation approach in detail.
- No dedicated environmental-enteropathy / biological-mechanism paper is in the collection — the water→gut inflammation→growth pathway is only referenced secondhand via review articles.

## 7. Which sources should support each future thesis chapter

- **Introduction/Motivation**: S02, S03, S17(background only), S20, S21, S23, S35(contrast case)
- **Literature Review — child nutrition background**: S01, S02, S03, S06
- **Literature Review — WASH-nutrition evidence**: S07, S08, S09, S10 (critical tension source), S11, S12, S13, S28, S33, S34
- **Data/Methods — anthropometric outcome construction**: S06, S25 (S26/S27 are NOT relevant — wrong indicator type)
- **Data/Methods — DHS sampling, weights, PSU structure**: S31, S32 (both needed; complementary, not redundant)
- **Data/Methods — GPS/cluster-to-region linkage**: S29, S30
- **Methods — WASH exposure construction / leave-one-out justification**: S18 (primary), S12, S28, S33, S34 (all as explicit contrast cases, not validation)
- **Methods — administrative-region FE justification**: S04, S16, S19
- **Results comparison / Discussion**: S05, S12, S13, S28, S33, S34 — see `literature_results_comparison.csv` for the specific directional comparisons and caveats
- **Discussion — causal vs. associational framing**: S10 (essential), S15, S16
- **Limitations**: S09 (spatial-grid alternative not taken), S17 (unused geospatial-covariate extension), S25 (LMS-derived -2SD/-3SD cutoff formulas now confirmed, p.303 - cite for outcome-construction methodology, not as an unread gap)
- **Policy implications**: S21, S22

---
*Sources: `literature_master_inventory.csv`, `literature_evidence_matrix.csv`, `literature_design_comparison.csv`, `literature_results_comparison.csv`, `bibliography_source_audit.csv` (all in this project's `sources/summaries/` and `sources/bibliography/` folders).*
