# Appendix B — Model specifications, inference conventions, and independent verification

## B.1 Inference-convention comparison (baseline household cluster-FE model, HAZ)

| Convention | Water β | SE | p | Sanitation β | SE | p |
|---|---|---|---|---|---|---|
| PRIMARY (same-group CRV1; this thesis's main convention) | −0.085 | 0.046 | .062 | 0.026 | 0.043 | .548 |
| FULL\_DUMMY\_DF sensitivity | −0.085 | 0.049 | .080 | 0.026 | 0.046 | .574 |

The two conventions differ only in whether the small-sample CRV1 correction additionally penalises degrees of freedom for the absorbed cluster dummies (FULL\_DUMMY\_DF does; PRIMARY does not, following the project's cross-validated adjudication against `linearmodels.PanelOLS(auto_df=True)`; see `docs/provenance/cluster_fe_inference_adjudication.md`). Point estimates are identical by construction; only standard errors and p-values differ. Both are reported wherever this coefficient is cited in the main text, with the convention always named.

## B.2 Independent verification of the pooled historical model (Section 4.6, Section 5.6)

This thesis's own pipeline (`scripts/historical_wash/16_estimate_preliminary.py`) estimates all 291 historical models using a hand-written weighted within-cluster demeaning estimator. A prior independent check (`scripts/historical_wash/17_validate_estimates.py`) re-estimated four representative *country-specific* cells (Ghana water HAZ weighted and unweighted; Ghana sanitation WAZ; Nigeria sanitation HAZ) with an explicit-dummy-variable statsmodels implementation, matching to 3×10⁻¹⁴.

This did not cover the pooled, multi-country model, which is the headline result of the historical extension. `scripts/historical_wash/20_validate_pooled_estimate.py`, written for this manuscript-preparation phase of the project, independently:

1. Rebuilds the estimation sample from the analysis-candidates stage directly (not from the stored, already-estimated model dataset), applying every filtering step explicitly and logging row counts (reproduced in Appendix A.3).
2. Estimates with `linearmodels.PanelOLS` — a different software library from the project's own hand-written estimator — using entity (cluster) fixed effects and clustered CRV1 standard errors.
3. Reports both the PRIMARY (`auto_df=True`) and FULL\_DUMMY\_DF (`auto_df=False`) conventions.
4. Estimates the unweighted counterpart on exactly the same final observations.

**First attempt and its correction, reported for transparency.** An initial run of this independent script used a single pooled reference birth-year cell (rather than a separate reference year per country) and omitted the child's own age-in-months as a linear control. This produced β per 10 points = 1.385 against the stored 1.026 — a roughly 35% discrepancy — despite the sample size (N=23,018), cluster count (G=3,114), and exposure mean/SD matching the stored values exactly, which is what indicated a specification difference rather than a sample-construction error. After matching the documented design exactly (country-local-reference birth-year dummies; child age-in-months included), the independent estimate converged to:

**Which of the two changes actually explains the 1.385-vs-1.026 gap (2026-10-09 diagnostic, not speculation).** Because both changes were made at once in the original attempt, and that attempt's exact code was never committed to this repository, this gap could not originally be decomposed. A dedicated diagnostic (`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`) isolates them on a faithful reconstruction of the described design. Result: the single-pooled-reference birth-year scheme does change the design matrix (13 birth-year dummy columns vs. the country-local scheme's 12 — Nigeria's own observed birth-year range does not include the single global reference year, so Nigeria keeps an extra dummy for its own earliest year) — but because the country-local scheme's column space is **fully nested** inside the single-pooled-reference scheme's column space, this extra column changes no other fitted coefficient: the exposure coefficient is bit-for-bit identical between the two birth-year schemes (1.0255531, holding the age-in-months control fixed either way). The age-in-months control, in contrast, fully accounts for the gap on its own: 1.0255531 with it included vs. 1.3852855 without it — matching the stored value and the documented early-attempt value respectively, under *either* birth-year scheme. This is strong evidence, on this reconstruction, that the age-in-months omission alone explains the historical 1.385-vs-1.026 gap, and that the birth-year reference-coding choice, despite changing the design matrix technically, did not contribute to it. Stated as this diagnostic's finding on a faithful reconstruction (not as certainty about the specific, unpreserved original code).

| Quantity | Independent (corrected) | Stored | Absolute difference |
|---|---|---|---|
| β per 10 points | 1.0255531 | 1.025553 | 6.7×10⁻⁸ |
| SE per 10 points (as originally run) | 0.260694 | 0.260730 | 3.6×10⁻⁵ |
| N | 23,018 | 23,018 | 0 |
| G (clusters) | 3,114 | 3,114 | 0 |
| K (regressors) / rank | 24 / 24 | 24 / 24 | 0 |
| Residual exposure SD (points) | 0.428348 | 0.428348 | ~0 |
| Unweighted counterpart β per 10 | 0.4147 | 0.41 (documented) | consistent |

Full execution log and comparison JSON: `data/processed/estimation/pooled_independent_validation_20261007T090003Z/` (RESTRICTED; aggregate figures only, reproduced above).

**The SE difference above is fully explained, not residual numerical noise.** `16_estimate_preliminary.py`'s declared small-sample correction is `(G/(G-1)) × ((N-1)/(N-K))` applied to the raw cluster-robust sandwich, with CIs/p-values from a Student's *t* distribution on *G*−1 degrees of freedom (read directly from its source, lines 209–212). `20_validate_pooled_estimate.py`'s and `21_validate_all_primary_cells.py`'s `PanelOLS.fit(cov_type="clustered", cluster_entity=True, auto_df=True)` call applies only part of the equivalent correction: `auto_df=True` correctly sets the same-group, no-double-penalty degrees-of-freedom convention (confirmed by reading the installed `linearmodels` 7.0 source, `panel/model.py`'s `_determine_df_adjustment`), and `debiased=True` (the library's own default) applies a `N/(N-K)` scale — but the *separate*, opt-in `group_debias=True` flag, which applies linearmodels' own `(G/(G-1)) × ((N-1)/N)` cluster-count adjustment (`shared/covariance.py`, `group_debias_coefficient`), was not passed. Multiplying the two pieces linearmodels *did* apply, `[N/(N-K)] × [(G/(G-1))×(N-1)/N]`, is algebraically identical to `16`'s declared `(G/(G-1))×(N-1)/(N-K)` — so the missing flag, not a different formula and not floating-point noise, is the entire explanation. `scripts/historical_wash/24_reconcile_inference_corrections.py` (new) re-fits all 24 primary cells with `group_debias=True` added: **every one of the 24 cells' SE now matches the stored value to the displayed precision (max remaining difference 0.0 at 8 decimal places)**, and a direct algebraic check (uncorrected sandwich SE × the manually computed combined scalar vs. the library's own corrected SE) confirms a zero residual for all 24 cells. Full detail and the per-cell table: `docs/provenance/independent_audit_v1_2026-10-07/09_update_2026-10-07_pass4.md`. This does not change the stored, authoritative SE in `16_estimate_preliminary.py`'s own output anywhere — that estimator's formula was correct throughout; what was corrected is the *validation* scripts' covariance configuration, not the pipeline being validated.

**What this verification establishes, and what it does not.** It establishes that the reported pooled coefficient and its standard error are computationally correct — the numbers the documented specification, correctly implemented in a second, independent library with an equivalent covariance configuration, actually produce. It does not establish that the specification identifies a causal effect, and it does not place this one cell in a higher *reporting* tier than its sibling historical models, all of which share the same unresolved documentation issues (Section 6; `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md`).

## B.3 Design checks applied to all 24 primary historical models

Record-key uniqueness, cluster-to-survey mapping (one survey per cluster), country weight totals equal to N/K within each model's own estimation sample, full design-matrix rank, and absence of singleton clusters in the final estimation data were checked programmatically for all 24 primary models (`scripts/historical_wash/19_check_model_design.py`; all checks pass, `data/processed/estimation/run_20261006T185646Z/design_checks_20261006T190020Z/design_checks_summary.json`, RESTRICTED).
