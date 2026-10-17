# Verification and language-edit change log: Appendix A

Status: **Awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

Appendix A is the publishing system's `appA` unit. It is numbered **Appendix A** (sections A.1–A.5, Tables A.1–A.3); it is not a chapter and not "Chapter 8".

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/appendices/A_variable_definitions_and_sample_flow.md` at academic source commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (last changed in `5563d33`) | `bc883e5b4dcc75ed21e63e4bef493a1b301197843c9dec96deef8211490ae528` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/A_variable_definitions_and_sample_flow.md` | recorded in the verification report and `HANDOVER.md` §19 |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/A_variable_definitions_and_sample_flow.tex` | recorded in the verification report and `HANDOVER.md` §19 |
| Word diff | `chapters/changes/A_variable_definitions_and_sample_flow.worddiff.txt` | recorded in `HANDOVER.md` §19 |

The word diff marks removed text as `[-…-]` and added text as `{+…+}`; `<nbsp>` marks a no-break space.

**Sources checked against.** The canonical appendix was read in full against the reviewed publishing copies of Chapter 3 (all of it), Chapter 4 (§4.3, §4.5, §4.6), Chapter 5 (sample counts and model labels), `docs/data_dictionary.md`, `docs/empirical_strategy.md` §2, the implementing code (`scripts/dhs_harmonization/00`–`05`, `08`, `11`, `12`, `14`; `scripts/historical_wash/10`, `12`, `14`, `16`, `20`), and the stored public outputs located through `final_empirical_package_v3_2026-10-07/00_results_index.md` and the provenance folders: `outputs/tables/step08_hr_wash_exposure_report.csv`, `step09_admin_region_report.csv`, `step11_model_sample_flow.csv`, `outputs/household_community_wash/01_development_sample_flow.csv`, `docs/provenance/historical_wash_analysis_samples_v1/sample_flow_AGGREGATE.csv`, `age_rule_reconciliation_AGGREGATE.csv`, `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv`, the issue register and the weights-and-measurement record. No restricted data was read, no pipeline or model was run, no classification or sample was changed, and no new empirical result was generated. Every check, with its evidence class (code, stored output, arithmetic, carried, open), is in `verify_appA.tsv` (129/129 OK).

**Length.** No page target was imposed and nothing was removed. The copy has about 2,010 words against about 790 in the canonical file; the increase comes from the verified definitions in A and B. The rendered body is 7 pages (preview pp. 1–7). Page-budget editing is deferred to final assembly (FA-5, FA-11).

**Citations.** One citation command (`deOnis2006`), unchanged. None added.

**No numerical error was found.** Every count in the canonical appendix (70,231; 4,481; 114; 36,985 / 37,260 / 37,088; 36,040 / 36,308 / 36,145; 4,426; 60,772; 23,135; 117; 23,018; 3,114) matches the stored public outputs by named key, except 42,052, which exists only in the restricted execution log of `20_validate_pooled_estimate.py` and is carried, not re-verified (see B12).

## A. Verified definition and source corrections (canonical file unchanged)

Each item corrects a statement in the canonical appendix that is imprecise, incomplete in a way that misleads, or points to the wrong authority, against the implementing code. Whether the canonical v12 file is also corrected is the author's decision (register FA-19 A).

### A1. HAZ, WAZ, WHZ: source and validity rule

- **Canonical.** Definition "…z-scores, WHO Child Growth Standards reference"; source "DHS recode, flagged valid per DHS convention".
- **Evidence (code).** `02_load_flag_anthro.py`: `ANTHRO_RAW_VARS = ["hw70", "hw71", "hw72"]`; valid = not system-missing and not 9996/9997/9998/9999; `scaled = raw / SCALE` for valid rows only, `SCALE = 100.0` (`00_config.py`); no other baseline script divides the z-scores again; the bounds (−6, 6), (−6, 5), (−6, 5) raise an error and never reclassify.
- **Correction.** The row now names the fields, the ×100 stored scale and the single division by 100, the four special codes with their DHS labels, the treatment of all five non-valid states as missing, the bounds as a validation check, and the script. "Flagged valid per DHS convention" is replaced by the implemented rule. The table note adds that the code applies the same code list to every country without asserting that DHS's own criteria behind code 9998 are identical across surveys.

### A2. Household and community WASH: authoritative source

- **Canonical.** Source "`docs/empirical_strategy.md` §2" for all three WASH rows.
- **Evidence.** §2 of that document is a narrative description; it describes the community measure as using "the DHS household census". The construction is implemented in `01_wash_mapping.py`, `03_build_indicators.py`, `12_robustness.py` (`build_household_wash_indicators()`) and `08_hr_cluster_wash_exposure.py`. Chapter 3 §3.3 states that the measure "is not a census of every household physically present".
- **Correction.** The source cells name the implementing scripts; the Table A.1 note keeps `docs/empirical_strategy.md` §2 as a description. The "census" wording is not repeated.

### A3. Community WASH definition

- **Canonical.** "Leave-one-out share of other households in the same cluster with the improved facility".
- **Evidence (code).** `08_hr_cluster_wash_exposure.py`: unweighted; HR fields `hv201`/`hv205`/`hv225`; Unknown, StructuralNotApplicable and (core) UnclassifiedBioDigester excluded from numerator and denominator; `other_n = cluster_n − own_included`, `other_sum = cluster_sum − own_value`; rate missing unless `other_n >= 1`; grouping key `country + hv001`. `14_household_community_wash_models.py` asserts the 0–1 range.
- **Correction.** The definition now states: unweighted; other sampled, classifiable HR households; own household excluded from numerator and denominator; exclusions; 0–1 scale; missing rule; not a census of every household and not an average over children; the biodigester robustness variant. This matches Chapter 3 §3.3.

### A4. `cluster_key`

- **Canonical.** "Composite key encoding survey + cluster, sample-qualified by construction".
- **Evidence (code).** `14_build_analysis_samples.py`: `out["cluster_key"] = out["IDHSPSU"]  # IDHSPSU is unique across samples (documented)`.
- **Correction.** "A copy of `IDHSPSU` (`cluster_key = IDHSPSU`), which already encodes survey and cluster, so the key is sample-qualified by construction." The canonical wording suggested a separately built composite.

### A5. A.4 internal pointer made exact

- "(issue register item #1)" → "(item 1 of `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md`)". Evidence: that file, row 1. "not inferred or substituted with an invented correction" → "No substitute weight or correction was invented; Section 3.8 states the working inference used instead."

### A6. A.5 index statement

- **Canonical.** "…for the complete, current index of every baseline and historical output file this manuscript cites…".
- **Evidence.** `final_empirical_package_v3_2026-10-07/00_results_index.md` itself refers to `final_empirical_package_v2_2026-10-07/00_results_index.md` for the baseline results and to `01_final_reporting_map.md` for the status scheme. Completeness ("every … file") was not verified.
- **Correction.** The paragraph names the three files and drops "complete" and "every"; the status labels are kept.

## B. Clarifications added (verified against code, stored outputs or the chapters; no new estimate)

| # | Location | Added (abridged) | Evidence |
|---|---|---|---|
| B1 | Household water | "Improved" is a facility-type category, not a measure of a safe or safely managed service; codes 96/97 → missing, not 0 | `01_wash_mapping.py`, `12_robustness.py` (`water_map`) |
| B2 | Household sanitation | Shared improved facilities count as improved (Basic + Limited); sharing code 7 and Ghana code 16 → missing | `classify_sanitation_service()`, `SANITATION_SERVICE_COLLAPSE_MAP`, `build_household_wash_indicators()` |
| B3 | `v005` | KR weight carried by each child's record; BR not used; `hv005` exists only in HR and is not used; pooled models rescale within each estimation sample, country models use it unchanged | `04_build_country_kr.py`, `11_main_regressions.py` (`build_temporary_pooled_weight()`), `08_…py` docstring; Chapter 3 §3.4, Chapter 4 §4.5 |
| B4 | `v021` | `psu = v021`; `country_psu = <country>_<psu>`; pooled FE and clustering on `country_psu`, country models on `psu` | `04_…py`, `05_pool_countries.py`, `11_…py`, `14_…py` |
| B5 | `b19` | Stored as `b19_raw`; linear control from Model 2 | `04_…py`, `11_…py` (`CHILD_CONTROLS_CONTINUOUS`) |
| B6 | Table A.1 note | Baseline rounds; no IPUMS-DHS; `hv001` grouping and `v001`/`v002` linkage vs `v021` for FE and clustering; correspondence **not checked against the restricted data, open** | `00_config.py`, `08_…py`; register FA-7 B (unchanged, unresolved) |
| B7 | `IDHSPSU` | Used for cluster FE and clustered SEs | `16_estimate_preliminary.py` |
| B8 | `PERWEIGHT` | IPUMS-DHS standard weight for child-level tabulations; rescaled to equal country totals; not a documented anthropometry-specific weight; `KIDWT` not used | weights-and-measurement record (quoted IPUMS text); `16_…py`; Chapter 3 §3.8 |
| B9 | W\_IMP, S\_IMP | Percent of population; area average of the MEAN surface within urban 2 km / rural 5 km buffers; not population-weighted; containing pixel and rural 10 km are sensitivities | IHME product-definition record; `10_spatial_extraction_v3.py` (`RADIUS_M`); `12_…py` (MEAN only); Chapter 3 §3.5–3.6 |
| B10 | Table A.2 note | Historical extract and family; Ethiopia provisional; outcome fields and codes; NoData not zero; 10⁻³ coverage tolerance; partial coverage diagnostic only; LOWER/UPPER not CIs and unused; window definitions, month weighting, 2000–2017 with no extrapolation, postnatal-only completion check, post-interview flag | `14_build_analysis_samples.py`, `10_…py`, `12_construct_exposure_windows.py`; Chapter 3 §3.5–3.7 |
| B11 | A.2 | Counts unweighted; outcome-valid samples in 4,434 clusters; no loss at exposure or covariate step; households 25,627 / 25,759 / 25,665; validity is the only outcome condition in code (no separate measurement-universe filter); no baseline singleton step; second flow file | `step11_model_sample_flow.csv` (model 4, pooled), `01_development_sample_flow.csv`; `11_…py` (`build_estimation_sample()`); Chapter 4 §4.5 |
| B12 | A.3 | Model identified (primary pooled, W\_IMP, primary method, weighted); per-country candidates and final N/G; singleton removal is model-specific (27, 16, 74 in the country models); which steps are publicly checkable; step 3 (42,052) in the restricted log only, because the public flow file uses first-failing-condition categories in another order; pointer to the unresolved Nigeria count gap | `sample_flow_AGGREGATE.csv`, `model_coefficients_PRELIMINARY_AGGREGATE.csv` (`m0001`–`m0004`), `14_build_analysis_samples.py` (`np.select` order), `20_validate_pooled_estimate.py` (step order); Chapter 3 §3.9 |
| B13 | `age_m`, `b_year` | `KIDCURAGEMO` named; Ethiopia and Nigeria deliver reported age for every record, Ghana and Kenya for none; `b_year` from the birth CMC | `age_rule_reconciliation_AGGREGATE.csv`; `14_…py`, `16_…py` |

## C. Captions and structure (no table added, no row or column removed)

- **Captions added to the three existing tables**, numbered in order of appearance: Table A.1 "Baseline variables (Sections 3.1–3.4)" (replaces the bold label "Baseline (Section 3.1–3.4)"), Table A.2 "Historical-extension variables (Sections 3.5–3.8)" (replaces the bold label "Historical extension (Section 3.5–3.8)"), Table A.3 "Official documentation sources consulted for a measurement-subsample weight" (new caption for the A.4 table). LaTeX numbers them and checks the typed number (`\ThesisCheckNumber`). All rows (7, 6 and 5) and columns (3, 3 and 2) are kept.
- **Table notes.** Two 9/13.5 pt notes (after Tables A.1 and A.2) carry the clarifications B6 and B10.
- **Sample flows.** The arrow chains in A.2 and A.3 are numbered lists with the same steps in the same order.
- **Paths.** Source cells give script file names; the directories are stated once in A.1 ("Scripts named in Table A.1 are in `scripts/dhs_harmonization/`…"). Full paths remain in running text.
- **Formatting.** `IDHSPSU`, `PERWEIGHT`, `KIDWT` and `GREGORIAN_ESTABLISHED` are set as code (identifiers), as in Chapter 3. Bold emphasis is kept (ch01 bold → italics decision pending).

## D. Layout fixes (publishing copy only; words unchanged unless stated)

- No-break spaces after "Section", "Sections", "Table", "Appendix", "Model" and before "km" (inline references broke across lines, e.g. "Section / 3.8").
- Four path-heavy paragraphs (A.2 file sentence, A.3 evidence paragraph, A.4 closing paragraph, A.5) are wrapped in raw LaTeX `\begingroup\raggedright … \endgroup` blocks that restore the paragraph indent and set widow and club penalties. Justified, they produced five overfull lines (up to 64 pt) and a one-line widow.
- "Outcome-valid, measurement-universe-restricted samples: 36,985 (HAZ), …" → "Outcome-valid samples within the measurement universe: 36,985 children for HAZ, …" (overfull line; same counts).

## E. Language edit (Humanizer v2.9.1, applied conservatively)

- Six punctuation em dashes replaced (sentence breaks, semicolons, parentheses); the heading and caption separators remain because the converter requires them. Range en dashes kept (3.1–3.4, 0–100, 2000–2017, 2024–25).
- The long `v005` and intro sentences split; "lives only in" → "exists only in"; "Reproduced independently in …'s execution log" → "The steps were reproduced independently in the execution log of …".
- Not changed: variable identifiers, units and scales, classification and exclusion rules, counts, sample labels, section references, the citation, and every methodological qualification. Code spans: 31 → 100 (identifiers and file names added in A and B, all from the code).

## F. Shared files changed (scope and evidence)

1. **`filters/thesis.lua`** (sha256 `875b078c…3683bc` → recorded in `HANDOVER.md` §19; old file kept in the session scratch copy and in git history). New item 7: a table whose caption number is an **appendix** number (`^%u%.%d+$`, e.g. "A.1") is written by the filter itself with `\endfirsthead` and a continuation head "**Table A.1** (continued)" above the repeated column heads. Chapter tables ("5.1" …) take the unchanged path. **Evidence of no effect on earlier units:** all eight earlier publishing copies (ch01–ch07, abstract) were converted with the old and the new filter; the outputs are byte-identical to each other and to the committed `.tex` bodies. Only the `% filter sha256` provenance comment would change if an earlier unit were re-converted; `build.py thesis` does not re-convert, so approved hashes are unaffected (register FA-20).
2. **`scripts/build.py`** (sha256 `e4676f21…a0d286` → recorded in `HANDOVER.md` §19). Preview only: for appendix units, the preview-only reference page is titled "References cited in this appendix — preview only", and the chapter-style section format is restored before it (the appendix format printed a stray "—" before the unnumbered heading). For chapter and abstract units the generated strings are identical to before (`reset` is empty, `scope` unchanged). The full-thesis driver prints the reference list before the appendices and is not affected.
3. Template (`thesis-preamble.tex`), drivers and bibliography: unchanged.

## G. Decisions and follow-ups for the author (nothing changed)

- **G1. Canonical synchronisation** of A1–A6 (and B, C as accepted) with `manuscript/v12_2026-10-10/appendices/A_variable_definitions_and_sample_flow.md`; if done, update `source_manifest.tsv` deliberately (FA-13 procedure). Register FA-19 A.
- **G2. Chapter 3 §3.2 wording.** Chapter 3 says a child contributes if the z-score "is flagged valid in the DHS recode (implausible values, per DHS's own flagging convention, are excluded) and the child falls within the DHS-defined under-five anthropometric-measurement universe". The code applies one rule (not system-missing, not 9996–9999) and no separate universe filter. Consider aligning Chapter 3 at final assembly. FA-19 B.
- **G3. `docs/data_dictionary.md`** row `v001` says "becomes `psu` (Step 04)", but `04_build_country_kr.py` sets `psu = v021`. Documentation inconsistency only; it bears on FA-7 B and does not resolve it. FA-19 C.
- **G4. Open `hv001`/`v001` vs `v021` note** in the Table A.1 note: keep while FA-7 B is open; revise the sentence when the restricted-data check is done.
- **G5. Bold emphasis** (whole intro paragraph and three cell sentences): ch01 bold → italics decision.
- **G6. Continuation labels** for chapter tables (currently appendix tables only): FA-20.
- **G7. Length.** 2,010 words vs 790; nothing to shorten now (FA-11).
