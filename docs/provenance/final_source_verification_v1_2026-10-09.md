# Final source-package verification (2026-10-09)

> **Correction (2026-10-09, later pass, commit `068ee4c`→): §3.3's and §5's "Category C" claim that the two historical-core-table rounding-boundary ambiguities "could not be adjudicated further" and that the full-precision RESTRICTED source "no longer exists on disk" was wrong. The restricted source directory does exist, fully intact — it was searched for only inside this git repository's own (gitignored, largely empty) `data/` subdirectory, not in the master `C:\Users\user\Documents\Graduation_Thesis\data\` directory one level above the repository root, which is where this project's scripts actually read and write all restricted data (hardcoded as `MASTER = r"C:\Users\user\Documents\Graduation_Thesis"` in, e.g., `scripts/historical_wash/16_estimate_preliminary.py`). This was a path-mismatch error in this pass's own search, not evidence of a deleted artifact. Both rounding questions are now resolved using that source; see `docs/provenance/source_lineage_correction_v1_2026-10-09.md` for the full evidence and correction. The specific passages below are corrected in place; the rest of this file is otherwise unchanged from its original text.**

Starting commit: `5b98a71` (confirmed `HEAD == origin/main`, clean except the standing untracked `outputs/supervisor_meeting/`). Canonical manuscript at the start of this task: `manuscript/v10_2026-10-07/`; at the end: `manuscript/v11_2026-10-09/`. This task's own instruction stopped and withdrew authorization for any PDF-build task; this pass is a bounded source-package verification only — no PDF was generated, compiled, rebuilt, or rendered.

## 0. PDF-build task status

Checked for any in-progress or recent PDF-build process at the start of this task: no background agent was running (`ListAgents` returned none reachable), no file in this repository was modified in the preceding two hours, and no `build/` directory exists under `v10` or `v11` (only the pre-existing, untouched `v3`–`v6` build directories). **Nothing was found to stop or preserve beyond what was already tracked and unchanged.** If a PDF-build task was run in a separate session or window not visible to this one, its artifacts (if any) were not located in this repository and were not touched by this pass.

## 1. State recovery

`HEAD` and `origin/main` both at `5b98a71` at the start, matching the task's stated expected commit exactly; no intervening changes. Working tree clean except the standing untracked `outputs/supervisor_meeting/`, left untouched throughout.

## 2. Verification of the immediately preceding bibliographic corrections

Re-checked directly (not assumed from the prior task's own report): `Momberg2021` and `PerezHeydrich2013` entries in `bibliography.bib` have no `note` field (confirmed via direct string search of each entry's block); both entries' resolution explanations remain recorded in `bibliography_verification_ledger.md`; `deOnis2006`'s author field is `{{WHO Multicentre Growth Reference Study Group}}` and `citation_map.md` displays "WHO Multicentre Growth Reference Study Group (2006)" for this key; `MASTER_ASSEMBLY.md`'s bibliography-status row states "12 entries," consistent with every other count reference in the package. All confirmed correct; no further bibliographic change was needed in this pass (beyond carrying these files forward into v11 unchanged, and correcting two stale self-referential version labels — `citation_map.md`'s header and `bibliography_verification_ledger.md`'s title — that had not been updated for the version renumbering).

## 3. Source-to-result consistency: every numerical claim checked against its authoritative output

Read every numerical claim in `01_introduction.md`, `04_empirical_strategy.md`, `05_results.md`, `06_discussion_and_limitations.md`, `07_conclusion.md`, `08_abstract.md`, and Appendices A–C in full, and checked each one directly against its authoritative source file using Python/pandas reads of the actual CSVs (not a re-statement of an earlier pass's summary). Sources checked:

- `outputs/household_community_wash/02_household_region_fe.csv`, `03_household_cluster_fe.csv`, `04_household_cluster_fe_support.csv`, `05_joint_household_community.csv`, `10_age_heterogeneity_joint_tests.csv`, `11_nigeria_sign_reversal.csv`, `15_country_household_cluster_fe.csv`, `01_development_sample_flow.csv`.
- `outputs/regressions/main_continuous_models.csv`.
- `docs/provenance/final_empirical_package_v3_2026-10-07/02_core_reporting_table.md` (the public, git-tracked copy of the 24-cell historical core table; the original RESTRICTED source, `C:\Users\user\Documents\Graduation_Thesis\data\processed\estimation\run_20261006T185646Z\`, was not checked directly in this pass — see the correction note at the top of this file and §3.3 below).
- `docs/provenance/historical_wash_preliminary_estimates_v1/model_coefficients_PRELIMINARY_AGGREGATE.csv` and `window_common_sample_PRELIMINARY_AGGREGATE.csv` (291-model sensitivity family, including the window comparison, further-sensitivity, Ethiopia-provisional, and Ghana-overlap-exclusion cells).
- `docs/provenance/historical_wash_preliminary_estimation_methods_2026-10-06.md` (Nigeria measurement-universe counts).
- `docs/empirical_strategy.md` (full pooled-universe sample counts).

### 3.1 Household and community results (Tables 5.1–5.5)

Every coefficient, SE, 95% CI, p-value, N, and cluster count in the region-FE and cluster-FE household tables, the four-stage community adjustment path, the joint household/community model, the Nigeria specification-sensitivity table, and the age-heterogeneity joint-test results matched its authoritative CSV exactly, to the displayed rounding precision, in every cell checked (72 household/region-FE/cluster-FE coefficient cells across both tables' two conventions; 8 community-adjustment cells; 12 joint-model cells; 5 Nigeria specification cells plus the wealth-block-removal figure; 12 age-heterogeneity joint tests). One result worth noting explicitly: the manuscript's claim that "the single exception is the water interaction for WHZ under region fixed effects (p = .300)" was verified against the full 18-row joint-test table and is exactly correct — this is the only one of the twelve substantive water/sanitation joint tests that fails to reject at 5%.

### 3.2 One error found and corrected: `01_introduction.md` §1.6

The Introduction's summary paragraph stated the household sanitation–HAZ 95% CI as `[−0.058, 0.110]`. The authoritative source (`03_household_cluster_fe.csv`, `model_label == natural_sample_PRIMARY_SAME_CLUSTER_CRV1`, sanitation row: `ci_upper = 0.109150`) and this manuscript's own Table 5.1 in `05_results.md` (`0.026 [−0.058, 0.109], .548`) both correctly round this value to `0.109`. This was an internal inconsistency between two sections of the same document — not an error traceable to the underlying data or estimation code — and is corrected in `01_introduction.md` §1.6 (now `[−0.058, 0.109]`) in v11.

### 3.3 Historical extension (Tables 5.6–5.9, Appendices B–C)

All 24 primary historical cells (water and sanitation × HAZ/WAZ/WHZ × Ghana/Kenya/Nigeria/pooled) matched the public core reporting table exactly, including the pooled headline (1.026→displayed 1.03), the six nominally significant cells, and every N/G count. The window-comparison table (5.7, including the 16,419-N common-sample row), the further-sensitivity table (5.8, including the Ghana-exclusion 0.741→0.74 figure), and the Ethiopia provisional table (5.9/Appendix C, C2/C3 water and sanitation coefficients and their CI-includes-zero property) all matched their authoritative 291-model aggregate file exactly. Appendix B's independent-verification figures (the five-step birth-year diagnostic's floating-point-precision coefficients, the SE-correction explanation) were re-read and found internally consistent with the already-established record from the immediately preceding correction passes (not re-derived from scratch in this pass, since the diagnostic itself was not in question here).

**Two minor rounding-boundary questions, raised in this pass and resolved in a later pass the same day**: the core reporting table's own 3-decimal-precision values for Ghana sanitation–HAZ's CI lower bound (`−4.915`, displayed in the manuscript as `−4.91`) and Kenya sanitation–HAZ's CI upper bound (`0.105`, displayed as `0.11`) could plausibly round either way at the 4th decimal place that the 3-decimal public table does not show. This pass incorrectly stated the full-precision source could not be found; it was searched for only inside this git repository's own `data/` subdirectory, not the master `C:\Users\user\Documents\Graduation_Thesis\data\` directory one level above, which is where it actually resides, fully intact. A later pass located it directly (`data\processed\estimation\run_20261006T185646Z\model_results_RESTRICTED_coefficients.csv`, row ids `m0142` and `m0143`) and confirmed both displayed values were already correct: `−4.9146807319418855` rounds to `−4.91`, and `0.1053050394220738` rounds to `0.11`. See `docs/provenance/source_lineage_correction_v1_2026-10-09.md` for the full evidence; this is now closed, not an open item.

### 3.4 Internal arithmetic cross-checks

Confirmed, as independent arithmetic checks not requiring any restricted file: the simple mean of the three established-date countries' water–HAZ coefficients, (1.648 + (−0.606) + 0.700)/3 = 0.5807 ≈ 0.58, matches the manuscript's own stated comparison to the pooled 1.03 exactly (§4.5); the historical sample-flow cascade's singleton-exclusion arithmetic, 23,135 − 117 = 23,018, matches the final reported N exactly (Appendix A.3); the Nigeria 2018 measurement-universe counts (12,806 official; 11,704 extract non-missing; 6,912 final estimation sample) match the methods note and the core table's own Nigeria-HAZ N exactly (§3.9).

## 4. Factual and methodological consistency: manuscript text checked against implemented code

### 4.1 Baseline variable construction

Checked directly against `scripts/dhs_harmonization/04_build_country_kr.py`: `weight_original = v005_raw / 1,000,000` (matches §3.4's documented divisor exactly, including the script's own hard assertion that this holds exactly); `psu = v021_raw` (matches §3.4 exactly). Checked against `scripts/dhs_harmonization/08_hr_cluster_wash_exposure.py`: `hv005` (the household-level weight) is read only in the Household Recode context and explicitly commented as "not used" for the KR/child-level models — matching §3.4's claim that `hv005` "lives only in the Household Recode (HR) file and is not used anywhere in the baseline models" precisely, down to the code's own comment making the same distinction. Checked against `scripts/dhs_harmonization/11_main_regressions.py`: `b19_raw` is the age control used throughout the baseline models, matching §3.2/§3.4's description of `b19` as the uniform baseline age field.

### 4.2 Historical `age_m` construction

Checked directly against `scripts/historical_wash/14_build_analysis_samples.py`'s own documented rule: `age_reported = KIDCURAGEMO (completed months) where delivered (Ethiopia 2016, Nigeria 2018)`; `age_derived = interview CMC − birth CMC (calendar-month difference)` used otherwise (Ghana 2014, Kenya 2014). This matches §3.8's claim of a country-varying construction — reported directly for Ethiopia/Nigeria, calendar-difference for Ghana/Kenya — exactly.

### 4.3 Weighting formula: one real mismatch found, confirmed inert, and corrected

§4.5 stated a single pooled-weighting formula, $w_i = \text{raw}_i \times (N/M) / \sum_{j\in\text{country}(i)}\text{raw}_j$, as applying "generically across both samples." Checked against the actual code:

- `scripts/historical_wash/16_estimate_preliminary.py` (line 154): `w0 * (n / K) / tot` — implements the documented $N/M$-scaled formula exactly.
- `scripts/dhs_harmonization/11_main_regressions.py`'s `build_temporary_pooled_weight()` (lines 289–312): `weight_model = sample_df["weight_original"] / W_k`, asserted (and verified in the code's own runtime check) to sum to exactly `1.0` per country, **not** $N/M$. This function is imported and reused by `scripts/dhs_harmonization/14_household_community_wash_models.py`, the script producing every household and joint-model table (5.1, 5.3) and the community-model table (5.2), so this applies to every baseline pooled model, not an isolated case.

**Confirmed this difference is inert.** Weighted least squares and its cluster-robust sandwich variance are both invariant to rescaling every observation's weight by one constant shared by every observation in a given model (since $N/M$ is the same number for every row in a given model, regardless of country). This was verified two ways: (a) algebraically — the bread–meat–bread cluster-robust variance formula is scale-invariant under a uniform weight rescaling, since the bread scales by $c^{-1}$ and the meat by $c^{2}$, cancelling to $c^{0}$; (b) numerically — a synthetic weighted-least-squares model with cluster-robust SE was fit under both the code's actual weight and the same weight multiplied by a global $N/M$ constant, using hand-rolled matrix algebra (bread–meat–bread sandwich) since `statsmodels` was not available in this environment; the two fits produced identical coefficients and standard errors to at least 12 decimal places. §4.5 was rewritten in v11 to state precisely what each pipeline implements and why the difference does not affect any reported number — this is a documentation correction with zero effect on any result already reported.

### 4.4 Cluster fixed-effects implementation and inference convention

Checked against `scripts/dhs_harmonization/14_household_community_wash_models.py`'s Model B block (household cluster FE): the demeaned-WLS approach and the "same-group CRV1, no additional absorbed-FE degrees-of-freedom penalty" convention are implemented and commented exactly as Appendix B.1 describes, including the explicit adjudication note cross-referencing `docs/provenance/cluster_fe_inference_adjudication.md`. The within-cluster variation support figures (31.6% water, 50.6% sanitation, used in §4.2) were confirmed directly against `04_household_cluster_fe_support.csv`'s HAZ row (31.61%, 50.56%), matching the manuscript's rounding exactly.

### 4.5 `11_main_regressions.py`'s own documented bug history

This script's docstring records a first-run bug (exposures omitted from `MODEL1_CONTINUOUS`/`MODEL2_CONTINUOUS`) that was caught by manual inspection and fixed before any number was reported, with a defensive runtime assertion (`_assert_exposures_in_every_model`) now guarding against recurrence. This is pre-existing, disclosed provenance, not a finding of this pass — noted here only because reading this file surfaced it; nothing in this history affects any currently reported number, per the script's own documented account (the corrected re-run's output is the only output ever reported).

## 5. Classification of remaining items

**A. Correctable implementation or calculation error.** None found in this pass. The weighting-formula mismatch (§4.3 above) is a documentation/code mismatch with a code that is internally correct (it does what it asserts and checks); it is classified under B, not A, because no calculation anywhere produced a wrong number.

**B. Correctable manuscript/reference error — fixed this pass.** (1) `01_introduction.md` §1.6's CI typo (0.110→0.109). (2) `04_empirical_strategy.md` §4.5's weighting-formula description, corrected to match each pipeline's actual code.

**C. Unresolved external documentation or data question — unchanged, not newly introduced.** The two historical-core-table rounding-boundary questions raised in §3.3 above were resolved (not left open) in a same-day later pass once the full-precision restricted source was correctly located — see `docs/provenance/source_lineage_correction_v1_2026-10-09.md`. All previously disclosed issue-register items (measurement-subsample weight documentation, Nigeria's count gap, DHS/IHME overlap, Ethiopia's interview-date candidates) are unchanged by this pass; none was re-opened or re-closed.

**D. Inherent research limitation.** Unchanged from prior passes: cross-sectional associational design, confidentiality-displaced coordinates, area- vs. population-weighted exposure, the baseline/historical samples' multiple simultaneous differences precluding an exposure-timing comparison. Re-running any model does not resolve any of these; none was treated in this pass as resolvable by computation.

**E. Author/supervisor decision.** Unchanged: actual submission date, handwritten signature, acknowledgements policy, and the timing/scope of supervisor feedback remain author/administrative decisions outside this verification's scope.

**F. Later PDF-layout check.** Explicitly deferred per this task's own instruction: the next stage (a separately authorized complete draft PDF build and page-by-page review) has not begun and was not started in this pass.

## 6. What this pass did not do

Did not rerun any of the 291 historical models or any baseline model — every check in §3 and §4 used already-computed, stored output files and already-written code, read directly, not re-executed. Did not change any specification to obtain a preferred result. Did not claim that any source check in this pass verifies PDF layout, page count, or rendering — no PDF was touched. Did not check the master `C:\Users\user\Documents\Graduation_Thesis\data\` directory (outside this git repository) for the full-precision historical source, leading this pass to incorrectly describe the two rounding-boundary values as unresolvable — corrected in a later same-day pass. Did not reopen any bibliographic item already closed in the immediately preceding task beyond the two stale version-label corrections noted in §2.

## 7. Versioning decision

Two chapter files changed (`01_introduction.md`, `04_empirical_strategy.md`) — both substantive corrections to manuscript content, not documentation-only metadata. Per this project's established convention, this required a new canonical version: `manuscript/v11_2026-10-09/` now supersedes `manuscript/v10_2026-10-07/` (pointer added there; `CORRECTION_LOG.md`, `README.md`, and `MASTER_ASSEMBLY.md` updated in v11).

## 8. Source-readiness conclusion

The empirical code, authoritative results, manuscript chapter text, and bibliography/reference package were checked for agreement across essentially every numerical claim in the canonical chapters and appendices (pooled and country-specific household, community, joint, Nigeria-sensitivity, age-heterogeneity, and historical-extension results; variable, weight, and fixed-effect descriptions against the implemented code) and found to agree, with two small corrections now applied (one CI digit; one weighting-formula description). Two rounding-boundary questions raised by this pass's own precision-level check were, at the time this pass concluded, incorrectly reported as unresolvable due to a path-mismatch search error; both were resolved the same day in a later pass (`docs/provenance/source_lineage_correction_v1_2026-10-09.md`) using the correctly located restricted source, confirming the manuscript's existing displayed values were already correct. This is not a claim that every conceivable error has been eliminated from a thesis of this scope — it is a statement of what was specifically checked in this pass, on top of the extensive verification already recorded across the prior independent-audit and evidence-based-correction passes, and what was found. **Source-complete and internally consistent to the standard this and subsequent passes could establish; not yet ready for submission**, pending the separately authorized PDF build and page-by-page review.

## Canonical path and commit

`manuscript/v11_2026-10-09/`. Commit follows this file.
