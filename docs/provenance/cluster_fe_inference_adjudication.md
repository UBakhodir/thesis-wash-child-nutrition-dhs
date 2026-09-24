# Cluster Fixed-Effects Inference Convention — Adjudication Note

Date: 2026-09-22

This note documents a methodological correction to the standard-error convention used for the
household-WASH, cluster-fixed-effects specifications produced by
`scripts/dhs_harmonization/14_household_community_wash_models.py`, and records the basis on which the
correction was made.

## 1. Affected specifications

The correction applies to every specification in this script that (a) identifies household WASH from
weighted within-DHS-PSU demeaning (equivalent to absorbing a full set of PSU dummy variables) and (b)
clusters standard errors on that same DHS-PSU grouping. In both cases the fixed-effect grouping and the
clustering grouping are identical. Concretely, this covers:

- The pooled household cluster-FE specification (`03_household_cluster_fe.csv`, primary rows).
- The flexible-age robustness rows built on the same specification (`08_flexible_age_sensitivity.csv`).
- The current-age heterogeneity interaction tests estimated under cluster fixed effects
  (`09_age_heterogeneity.csv` and `10_age_heterogeneity_joint_tests.csv`, cluster-FE rows only).
- The corresponding rows of the pooled model summary (`16_development_model_summary.csv`).

The country-specific cluster-FE estimates (`15_country_household_cluster_fe.csv`,
`15b_country_cluster_fe_support.csv`) and the Nigeria specification-sensitivity diagnostic
(`11_nigeria_sign_reversal.csv`, `12_nigeria_sign_reversal_covariate_diagnostics.csv`) already used the
convention adopted below and did not require numerical revision.

## 2. Previous convention

The previous implementation reported cluster-robust standard errors after applying an additional
degrees-of-freedom penalty on top of the native cluster-robust variance estimate, computed as though the
absorbed PSU fixed effects had instead been estimated as free dummy-variable parameters
(`k_full_dummy = k_reported + n_clusters`, with a corresponding inflation factor applied to the
variance). This penalty was applied only to the pooled household cluster-FE and age-heterogeneity
specifications; it was not applied to the country-specific or Nigeria cluster-FE estimates, which used
the native cluster-robust variance directly. This inconsistency, and the appropriateness of the
additional penalty, motivated the review recorded here.

## 3. Adopted convention

The adopted convention uses each estimator's native cluster-robust variance (CRV1-type) directly, with
no additional degrees-of-freedom penalty for the absorbed fixed effects, whenever the fixed-effect
grouping and the clustering grouping are the same variable. Point estimates are unaffected by this
change; only reported standard errors, confidence intervals, and p-values for the specifications listed
in Section 1 change, and they become smaller (more precise) than under the previous convention.

## 4. Basis for the correction

Three independent lines of evidence were reviewed:

**a. `statsmodels` cluster-robust variance implementation.** The installed `statsmodels` 0.14.6
cluster-robust covariance routine (`sandwich_covariance.cov_cluster`, invoked via
`RegressionResults.get_robustcov_results(cov_type="cluster", ...)`) scales the sandwich estimator using
`k_params`, the number of columns in the design matrix actually passed to the estimator. It has no
mechanism for being told about, or for penalizing, fixed effects that were absorbed prior to estimation
via demeaning rather than included as explicit dummy columns. Applying a manual post-hoc penalty for
those absorbed columns is therefore an assumption external to the estimator, not a correction it is
implicitly missing.

**b. `linearmodels` documented convention for the same-grouping case.** The installed `linearmodels`
7.0 `PanelOLS` estimator implements an `auto_df` option (the package default) whose documentation states
that clustered standard errors "that are clustered using the same variable as an effect do not require
degree of freedom correction." Inspection of the implementation confirms this: `PanelOLS` determines
whether to apply an additional degrees-of-freedom adjustment for absorbed effects via a nestedness check
between the effect grouping and the cluster grouping (`_is_effect_nested`); when the two coincide, the
check is trivially satisfied, no additional adjustment is applied, and the reported standard errors match
the native cluster-robust computation.

**c. Empirical cross-validation.** The pooled and country-specific household cluster-FE specifications
were independently re-estimated with `linearmodels.PanelOLS`, specifying DHS-PSU as both the entity
(absorbed) effect and the clustering variable, with `auto_df=True` (the package default) and the same
survey weights. Point estimates and standard errors from this independent estimator agreed with the
native (non-penalized) `statsmodels` cluster-robust standard errors to four to five decimal places, and
disagreed with the previously reported, additionally-penalized standard errors.

These three lines of evidence are mutually consistent and were not qualified by any conflicting result
encountered during review. Corroboration from the Stata `reghdfe` convention was not independently
verified against installed software and is not asserted here.

## 5. Resulting numerical changes

Point estimates for every affected coefficient are unchanged. Reported standard errors, confidence
intervals, and p-values for the specifications in Section 1 are now generally smaller than under the
previous convention. The clearest downstream change is in the current-age heterogeneity joint tests: of
the twelve individual heterogeneity tests, eleven now reject the null of no heterogeneity at the 5%
level (previously ten), with the water×WHZ interaction under cluster fixed effects moving from a
non-rejection to a rejection (p≈.048). The sole remaining non-rejection among the twelve tests is
water×WHZ under the region-fixed-effects specification (p≈.300), which was not affected by this
correction and is unchanged. No coefficient sign changes, and no result that was previously significant
at the 5% level becomes non-significant under the corrected convention.

## 6. What did not change

This correction is limited to the inference convention described above. It does not alter: the
construction of the WASH exposure or anthropometric outcome variables; the sample-definition or
restriction logic; the community-WASH region-fixed-effects specifications (which do not share a grouping
variable between fixed effect and cluster, and were therefore never subject to this issue); survey
weighting; or any Step 00–13 script, output, or result. No final tables, final figures, or final appendix
content have yet been integrated with the outputs described in this note; this correction is confined to
the household/community-WASH specification-development outputs under
`outputs/household_community_wash/`.
