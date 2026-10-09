# Integrated source review (2026-10-09)

**Scope**: a full-manuscript, whole-project academic review of `manuscript/v6_2026-10-07/` against the implemented empirical pipeline and the tracked GitHub repository (`UBakhodir/thesis-wash-child-nutrition-dhs`), covering economic coherence, econometric defensibility, statistical accuracy, internal consistency, data/definition transparency, literature positioning, and academic writing quality. This is an integrated reading of the finished manuscript as a whole, not a repetition of the computational audits already completed and documented in `independent_audit_v1_2026-10-07/`. Those audits are treated here as evidence to cite, not re-derived.

**Reviewed at**: commit `fb75d2a` (confirmed HEAD == `origin/main` at the start of this review; no uncommitted changes other than the standing untracked `outputs/supervisor_meeting/`).

**No PDF was generated, rebuilt, or rendered in this review.** All findings below come from reading the Markdown chapter sources, the appendices, the top-level manuscript metadata files, the authoritative output CSVs, the active construction/estimation scripts, and the git history directly.

---

## 1. Authority map

| Analysis family | Active script(s) | Input | Validated output (authoritative) | Reporting table | Manuscript section |
|---|---|---|---|---|---|
| Baseline household/community WASH construction | `scripts/dhs_harmonization/01_wash_mapping.py`–`08_hr_cluster_wash_exposure.py` | Raw DHS KR/HR recodes (`data/raw/DHS/`) | `data/processed/pooled_kr_four_country_wash_exposure.parquet` (RESTRICTED) | `outputs/household_community_wash/01_development_sample_flow.csv` | §3.1–3.4 |
| Household region-FE / cluster-FE / joint models | `scripts/dhs_harmonization/11_main_regressions.py`, `12_robustness.py`, `14_household_community_wash_models.py` | Pooled WASH-exposure parquet above | `outputs/household_community_wash/02_household_region_fe.csv`, `03_household_cluster_fe.csv`, `05_joint_household_community.csv` | Results §5.1, §5.3 | §4.1–4.4 |
| Nigeria sign-reversal / specification-sensitivity diagnostic | `scripts/dhs_harmonization/14_household_community_wash_models.py` | Same | `outputs/household_community_wash/11_nigeria_sign_reversal.csv` | Results §5.4 | §4.3 |
| Age-heterogeneity tests | Same family | Same | `outputs/household_community_wash/09_age_heterogeneity.csv`, `10_age_heterogeneity_joint_tests.csv` | Results §5.5 | §4.4 |
| Historical WASH exposure (IHME spatial extraction) | `scripts/historical_wash/10_spatial_extraction_v3.py` | IHME gridded rasters + IPUMS-DHS GPS | `data/processed/spatial_extraction/run_v3_20261006T183003Z/cluster_year_extraction_RESTRICTED.parquet` (RESTRICTED) | Appendix C §C.4 | §3.5–3.6 |
| Historical exposure-window/completion construction | `scripts/historical_wash/*` window-construction scripts | Spatial extraction above + IPUMS birth/interview dates | `data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet` (RESTRICTED) | Appendix A §A.3 | §3.7 |
| Historical primary model estimation (24 cells) | `scripts/historical_wash/16_estimate_preliminary.py` | Analysis-candidates parquet above | `data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv` (RESTRICTED) | Results §5.6 | §4.6 |
| Historical model independent verification | `scripts/historical_wash/20_validate_pooled_estimate.py`, `21_validate_all_primary_cells.py`, `24_reconcile_inference_corrections.py` | Same analysis-candidates parquet, rebuilt independently | `data/processed/estimation/inference_reconciliation_20261007T190417Z/` (RESTRICTED) | Appendix B §B.2 | — |
| Ethiopia provisional interview-date candidates | `scripts/historical_wash/*` Ethiopia-specific date-conversion scripts | Ethiopian-calendar interview dates | Ethiopia-specific CSVs under `data/processed/estimation/` (RESTRICTED) | Appendix C §C.1–C.3 | §5.9 |

**No contradictory authority pointers were found.** Every reporting table traced resolves to exactly one script family and one output file, consistent with `01_repository_authority_map.md`'s own conclusion (re-checked here, not merely cited). The one place a reader could plausibly be confused — `17_validate_estimates.py`, `20_validate_pooled_estimate.py`, and `21_validate_all_primary_cells.py` all producing SE columns, two of which (20, 21) are now explicitly superseded for SE-comparison purposes by `24_reconcile_inference_corrections.py` — is already handled by addendum docstrings added to 20 and 21 in the prior pass (`c22b4bf`), re-confirmed present in this review.

## 2. Material project evolution

| Dimension | Original proposal (`docs/thesis_design.md` Part II, pre-2026-08-18) | Implemented, final | Evidence |
|---|---|---|---|
| Identification strategy | Quasi-experimental panel design: within-spatial-unit variation over multiple survey years, spatial-grid + survey-year fixed effects | Cross-sectional design; administrative-region and DHS-cluster fixed effects (no survey-year dimension in the baseline — only one DHS round per country was available) | `docs/thesis_design.md` §10–11, explicitly documented as a departure, not silently dropped |
| Geospatial controls | Rainfall, temperature, elevation, population-density raster covariates | Never extracted or used in the baseline; the *historical extension* (added later, not part of the original plan at all) uses IHME WASH-coverage rasters specifically, for exposure construction, not as a control | `docs/thesis_design.md` §5, §7, §8 |
| Heterogeneity analysis | Interaction models by rural residence, household poverty, maternal education | Not implemented as planned. A *different* heterogeneity dimension (child's current age) was added later, during manuscript development, and is not a substitute for the originally planned one | `docs/thesis_design.md` §13; manuscript §4.4, §5.5 |
| Maternal literacy control | Not in the earliest control list | Entered during pipeline construction, used consistently from that point; retained after a dedicated provenance investigation found no evidence of error and a literature precedent (Spears 2013) | `docs/thesis_design.md` §7 provenance note; `outputs/final_audit/literacy_specification_decision.txt` |
| Historical/temporal exposure design | Not in the original baseline plan at all | Added as a distinct, separately-labelled extension (IHME-linked, 2014–2018 rounds, three countries), explicitly in response to supervisor advice (`historical_wash_supervisor_advice_matrix_2026-10-07.md`, row 5) | Git commits `fd93ac9` through `59a4d34`; manuscript §1.2–1.3, §3.5–3.8, §4.6 |
| Cluster-FE inference convention | — | Corrected at least twice during development (commits `9f1f53c`, `a709290`) before settling on the "same-group, no-double-penalty" convention, independently cross-validated against `linearmodels.PanelOLS(auto_df=True)` | `docs/provenance/cluster_fe_inference_adjudication.md`; manuscript §4.5, Appendix B §B.1 |
| Reporting/causal language | Associational framing stated from the start (`docs/thesis_design.md` §2) | Maintained and progressively tightened across manuscript v1→v6 (measurement-sample representativeness, pooled-estimand-as-average, status tiering, confounding language, exposure-timing comparison, literature overclaims, multiplicity language — each a distinct corrected issue across the version history) | `CORRECTION_LOG.md` in `v3`, `v5`, `v6`; `historical_wash_reporting_corrections_v1_2026-10-07.md` |

**Outdated-proposal-as-final-method check**: confirmed clean. Every occurrence of "panel," "difference-in-differences," or "instrumental variable" in the current v6 manuscript text (swept directly, not assumed) either describes a *cited external study*'s design (Headey and Palloni 2019) with explicit attribution, or appears in an explicit disclaimer stating this thesis's own design is none of those things (§1.7, §4 opening paragraph). No leftover description of an abandoned design survives as a description of what this thesis actually estimates.

**Preserved old files**: v1 through v5 of the manuscript, and the full `docs/thesis_design.md` Part II original plan, remain in the repository. Each superseded manuscript version carries its own pointer file (`POINTER_TO_Vn.md`) directing a reader to the current version, and `docs/thesis_design.md` itself explicitly labels Part II as "retained for project history... nothing in Part II should be read as a description of the frozen analysis." This is the correct pattern — preservation with clear current-entry-point signposting, not deletion — and no change was needed here.

## 3. Research question and economic logic (Stage 3)

The thesis has a clear, narrowly stated central question (§1.3): three related associational questions (household WASH, community WASH, historical early-life WASH coverage), explicitly not posed as causal-effect estimates. The economic motivation — household WASH as a private good vs. community WASH as a local environmental/public-infrastructure condition, via a faecal-oral pathogen exposure channel — is stated once, precisely, and not re-derived differently in different chapters (§1, §2.1, §4.3 all describe the same mechanism consistently).

Checked explicitly against the "do not imply" list in this review's brief: no instance was found anywhere in the current chapter text implying that improved facilities guarantee safe water or effective sanitation, that modelled local coverage equals household access, that area-weighted coverage equals population-weighted coverage, that baseline/historical differences isolate exposure timing, or that four countries represent Sub-Saharan Africa as a region — each of these is explicitly and separately disclaimed (§1.4, §3.5, §3.6, §6.2, §6.5, §6.6).

**Registered title**: preserved verbatim (`AUTHOR_CHECKLIST.md`), as required. The mismatch between the registered title's causal-sounding "Impact" and the thesis's own associational framing is already flagged as an open author/supervisor discussion item, not silently resolved either by changing the title or by ignoring the mismatch. No action was needed or taken here beyond confirming this treatment is still in place.

## 4. Data, definitions, and sample transparency (Stage 4)

Checked §3.1–3.9 against the construction scripts and sample-flow outputs directly (not against an earlier completion report). All of the following were confirmed present and consistent: survey-round membership per sample (baseline vs. historical, by country), unit of observation (child), outcome definitions and valid-value rules (DHS-flagged z-scores), household WASH classification (JMP-improved), the leave-one-out community construction and its denominator logic, the historical exposure's spatial/temporal construction and completion rule, exclusions (singleton clusters, incomplete windows, incomplete spatial coverage), the Nigeria 2018 measurement-universe discrepancy (stated as unresolved, not explained away), and control-variable definitions.

Outcome-specific sample sizes are reported separately throughout (36,985 HAZ / 37,260 WAZ / 37,088 WHZ for outcome validity; 36,040 / 36,308 / 36,145 for the common household-and-community-classifiable sample) and are never collapsed into a single misleading "N" — confirmed by direct comparison against the §5.1–5.3 result tables, whose N columns match these figures exactly for every reported cell.

Ethiopia's C1 (invalid, excluded from all reporting) is kept visibly distinct from C2/C3 (provisional, reported only in Appendix C) throughout — confirmed in §1.4, §3.5, §5.9, and Appendix C itself; no table anywhere pools C1 with C2/C3 or presents Ethiopia alongside the three established-date countries as if on equal footing.

## 5. Econometric coherence (Stage 5)

Each reported model family (§4.1–4.6) was checked against its underlying equation, its stated identifying variation, and its own table in §5. The logic is coherent and consistently applied:

- Region-FE models are explicitly motivated as a weaker baseline (room for within-region cluster heterogeneity) that justifies moving to cluster-FE.
- Cluster-FE is correctly scoped as absorbing *between-cluster* but not *within-cluster* confounding, and the manuscript does not claim otherwise.
- The decision to exclude cluster-FE for the current-round community exposure, but include it for the historical exposure, is justified with an actual measured quantity (within-cluster SD of the LOO rate: ≈0.007/0.011 vs. an overall SD of ≈0.35) rather than an assertion — this is good econometric practice, and the number was spot-checked against `04_household_cluster_fe_support.csv`'s equivalent within-cluster-variation reporting style and found consistent in kind.
- The equal-country-weighting vs. equal-slope-influence distinction (§4.5) is handled unusually carefully: the manuscript does not claim equal weight totals imply equal influence on the pooled slope, and demonstrates the point with an actual number (simple country-average 0.58 vs. pooled 1.03), which this review independently re-confirms is arithmetically correct (1.65 + (−0.61) + 0.70)/3 = 0.58, matching §5.6's table.
- Full column rank is correctly described as a computational property, not a strength-of-identification claim (§4.5, explicit disclaimer) — the specific conflation this review's brief warned against was checked for and not found.
- The inference convention (same-group CRV1, t(G−1)) is now fully reconciled end-to-end against an independent re-implementation, including the CI/p-value step specifically (prior pass, `09_update_2026-10-07_pass4.md` §1) — this review treats that reconciliation as settled evidence and did not re-run it, per the instruction not to reopen a completed computational check absent a new inconsistency. No new inconsistency was found that would warrant reopening it.

No instance was found of a control variable being added or a specification being altered that appeared to chase a particular sign or significance level — confirmed by cross-checking §5.4's own candid admission that the Nigeria community-sanitation coefficient is unstable across specifications and is reported as such, not selectively presented.

## 6. Statistical and economic interpretation (Stage 6)

Spot-checked every main coefficient cited in §1.6, §5, and §7 against its source CSV (`outputs/household_community_wash/*.csv`, `outputs/regressions/main_continuous_models.csv`, `data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv`) for sign, scale, CI, and p-value. All matched. The historical per-10-point coefficients are explicitly related back to the much smaller residual exposure variation that actually identifies them (§4.6, §5.6: 0.20–0.88 percentage points vs. the 10-point reporting scale), with the arithmetic translation (≈0.044 HAZ-SD per residual-exposure-SD) clearly labelled as a translation of the existing estimate, not a simulated intervention — this matches the brief's specific instruction on this point exactly.

Checked against the explicit "do not" list: non-significance is consistently read as inconclusive, not as proof of zero association (§5.1, §1.6); no claim anywhere infers that two coefficients differ merely because one is significant and the other is not (the one place this risk is highest, §5.3's single significant joint-model cell, is explicitly hedged: "reported as a single finding... not treated as a central conclusion"); attenuation is consistently described as "consistent with, not proof of" confounding (§5.2, §6.1, repeated verbatim pattern each time); the one unexpected-sign coefficient (household water | community water, HAZ) is explicitly not read as evidence WASH is harmful (§5.3, §6.1); and robustness/sensitivity checks are never presented as resolving the thesis's stated identification limitations — each sensitivity table (§5.7, §5.8, Appendix C §C.4) is introduced with language scoping exactly what it does and does not hold constant.

## 7. Tables and results organisation (Stage 7)

All canonical source tables in §5 and the appendices were checked against their manuscript rendering for: explicit titles, units/scale statements, labelled CIs and p-values, N/cluster counts, identified FE/controls/weights, primary-vs-sensitivity labelling, and rounded-value agreement with the stored CSVs (spot-checked, not exhaustively re-diffed, since `claim_evidence_ledger.md` already performs this trace for every number and was itself checked for staleness in §9 below). Reporting is balanced across water/sanitation, the three outcomes, country/pooled cells, and baseline/historical — no inconvenient cell (the Nigeria sign reversal, the unexpected joint-model sign, the Ethiopia C1 invalidity, the weighted-vs-unweighted sensitivity) is omitted or minimised relative to the favourable ones.

**Source-layout review, not a PDF check**: the table-wrapping and list-rendering source conventions fixed in the prior pass (`md2tex.py`, commit `c22b4bf`) were reviewed at the source level only, per this task's explicit boundary. The known remaining cosmetic issue (Markdown numbered/bulleted lists rendering as inline prose rather than an indented list — documented in `build/README.md`, affecting no content) is a **Category E, PDF-stage item**, not re-litigated here.

## 8. Literature and contribution (Stage 8)

Read Section 2 as an argument. It distinguishes observational, quasi-experimental (panel/DID), and randomised-trial designs explicitly and consistently (§2.1–2.3), states a specific and proportionate contribution (§1.5, §2.7 — "a particular combination of four countries is not, by itself, evidence of substantive novelty"), and does not claim a comprehensive literature search (§2.4: "does not claim to have conducted an exhaustive search... sufficient to assert this combination is unprecedented"). Biological plausibility is explicitly kept separate from the growth-effect question throughout (§1, §2.1, §2.3), and the major trials are described arm-by-arm rather than generalised beyond their tested intervention packages (§2.3) — this review re-read §2.3 directly against this standard and found no instance of overgeneralisation. This chapter, and the claim-level literature verification underlying it (all 20 of 20 cited sources, per `citation_map.md`), were treated as settled by the prior passes; this review re-read the chapter text itself (not merely the verification ledger) to confirm the verified claims are accurately reflected in the prose, and found them to be.

## 9. Whole-manuscript consistency and writing (Stage 9)

Read all eight chapter files and three appendices in full this session (not reused from an earlier completion report). Findings:

- Abstract accurately summarises the final thesis, including its hedges — spot-checked every number in the abstract against §5 and found all consistent.
- Introduction's three research questions (§1.3) are each answered, with the same hedging, in Results and Conclusion — no question is raised and left unaddressed, and no new question or claim is introduced in the Conclusion that was not already scoped in the Introduction.
- Methods (§4) describe only the implemented analyses; the explicit "none of the designs below is a panel/DID/IV" line removes any risk of a reader inferring an unimplemented design.
- Results (§5) separates estimates from interpretation consistently — each table is followed by prose that states what the number is and is not evidence of, not a bare restatement.
- Discussion (§6) explains findings and limitations without repeating the result tables themselves — confirmed by comparing §6's prose against §5's tables; no table is reproduced verbatim in §6.
- Appendices supply supporting detail (inference-convention derivations, Ethiopia diagnostics, design checks) without hiding limitations — Appendix C's own first line states plainly that nothing in it belongs to the headline result.
- Writing quality: precise, consistently hedged, internally cross-referenced by stable section number (not heading text, per `CROSS_REFERENCE_MAP.md`'s own documented rationale), no exaggerated contribution claims found, no internal task-management or audit-process language found inside chapter prose (process/audit detail is consistently kept in `docs/provenance/` and the manuscript's own non-chapter files — `CORRECTION_LOG.md`, `citation_map.md`, etc. — exactly where this review's brief says it belongs).

**Confirmed source errors found and corrected in this pass** (documentation-layer, not chapter-content; full detail in Section 11 below): `AUTHOR_CHECKLIST.md` and `MASTER_ASSEMBLY.md` both stated the verified main-text page count as 31 pages, which was true for v5 but became 32 pages in v6 once the table-wrapping fix (commit `c22b4bf`) made cells wrap correctly instead of running off the page — neither file had been updated when that fix landed. Additionally, `MASTER_ASSEMBLY.md`, `bibliography_verification_ledger.md`, `citation_map.md`, and `claim_evidence_ledger.md` still carried v3/v4/v5 version headers despite v6 being canonical. None of these affected any chapter's content, any empirical number, or the built PDF (none of these four files is part of the LaTeX build chain) — they are pure documentation-consistency errors, now corrected (Section 11).

## 10. Supervisor advice and remaining decisions (Stage 10)

Compared the final package against the two tracked, public supervisor-advice records (`historical_wash_supervisor_advice_matrix_2026-10-07.md` + its `ADDENDUM`, and `historical_wash_supervisor_request_status_v1_2026-10-07.md`). No confidential transcript or meeting-presentation content was read or reproduced beyond what these already-public, already-paraphrased files contain; `outputs/supervisor_meeting/` was not opened.

- **Advice implemented**: control for household characteristics (wealth etc., corrected via the addendum to note wealth *is* included in the baseline cluster-FE model); own-vs-community WASH comparison; IPUMS-DHS use for the historical extension; the historical/geocoded exposure-timing extension itself; within-cluster cross-cohort ("mini panel") identification for the historical model; explicit discussion of confounding once controls are added; reporting a null historical result honestly rather than suppressing it; not citing the supervisor's own unpublished working paper.
- **Advice addressed in writing but not yet supervisor-reviewed**: the literature-positioning request ("say what you do differently") — the literature review chapter now exists, fully claim-verified, but has not been sent to or reviewed by the supervisor.
- **Material sent for feedback**: none. Confirmed directly: no email, message, or attachment has been sent to the supervisor by this project at any point in its history (`historical_wash_supervisor_request_status_v1_2026-10-07.md`, re-confirmed as still accurate — no new send event exists in the repository since that file was written).
- **Feedback received**: none.
- **Unresolved author/supervisor decisions**: (1) whether to pursue the title-change suggestion recorded in `AUTHOR_CHECKLIST.md`; (2) whether to expand the literature review using the already-verified-but-uncited sources in `bibliography.bib` (Momberg 2021, Gebru 2019, DHS/JMP/UNICEF methodology reports); (3) whether and how much of the historical extension to keep in the main text vs. appendices. None of these was decided in this review, consistent with the instruction not to invent missing supervisor instructions or treat a completed chapter as supervisor approval.

## 11. Findings and corrections implemented in this pass

Recorded before editing, per the task's own requirement.

| # | File/section | Evidence | Why it matters | Correction | Affects numbers/interpretation/presentation? |
|---|---|---|---|---|---|
| 1 | `AUTHOR_CHECKLIST.md`, page-limit item | `build/README.md` (v6) states the verified main text is 32 pages; `AUTHOR_CHECKLIST.md` still said 31 | A reader checking the formatting checklist would be told a stale, now-incorrect verified page count | Updated to 32 pages, with a one-line explanation of why it changed (table-wrapping fix) | Presentation only — no empirical number affected |
| 2 | `MASTER_ASSEMBLY.md`, header and readiness statement (two locations) | Same page-count fact; header also still said "v4" and described v4-era content as current | Same reader-facing staleness; the assembly spec is the stated "current authority for assembling the full thesis" and should describe v6 | Header rewritten for v6, superseded-chain updated, both page-count mentions corrected to 32, readiness statement updated to also note the PDF-clipping fix and rendered-page verification | Presentation only |
| 3 | `bibliography_verification_ledger.md`, `citation_map.md`, `claim_evidence_ledger.md` headers | Headers said v3/v5/v4 respectively while the files' own content (correctly) already reflected v6-era facts | Internal inconsistency between a file's header and its own body is exactly the kind of documentation drift an integrated review should catch | Headers updated to v6; `claim_evidence_ledger.md` additionally got one new sentence noting the v6 inference reconciliation, since that fact postdated its last content update | Presentation only |

No chapter-content, table-value, citation, or empirical-output file was altered in this pass. No new manuscript version was created — these are documentation-consistency fixes within v6 itself, not substantive changes requiring a v7 (per the task's own instruction to version-bump only when substantive changes justify it).

**No material issue requiring author judgment was found this pass** beyond the three already-recorded open decisions in Section 10, which are not new.

## 12. What this review did not find

No instance of: a specification altered to obtain a preferred sign or significance; a resolved-sounding claim about an actually-unresolved limitation; a table inconsistent with its own prose; an outdated panel/DID/IV description surviving as a description of the implemented method; a literature claim overstated beyond its source (beyond the two already corrected in prior passes); or a chapter-content numerical discrepancy against its authoritative source file.

---

## Canonical assembly path

`manuscript/v6_2026-10-07/` remains canonical and unchanged in substance by this review (only the three documentation-consistency items above were corrected, none in chapter content). Entry point: `manuscript/v6_2026-10-07/README.md`. Build (not touched this pass): `manuscript/v6_2026-10-07/build/`.

## Explicit PDF-stage tasks (deferred, not performed here)

1. Rebuild the PDF to confirm the page-count and content are unaffected by this pass's documentation-only edits (expected: unaffected, since none of the three corrected files are part of the LaTeX build chain — but this should still be verified mechanically before a submission build, not assumed from this review).
2. Clean up the known cosmetic Markdown-list-rendering issue in `md2tex.py` (numbered/bulleted list items render as inline prose; documented, not yet fixed; no content affected).
3. A further line-by-line prose-quality pass, as already flagged in `AUTHOR_CHECKLIST.md`'s own closing section, before a final submission build.
4. Author/supervisor decisions on the three open items in Section 10 above.
