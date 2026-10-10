# Resolution of the independent thesis reinspection (2026-10-10)

Resolves `Independent_Thesis_Reinspection_ecbd92e_2026-10-10.md`, an external reinspection of commit `ecbd92e79f226feb71899ffb8c152cd9ec2680e3` (the v12 canonical manuscript, unchanged since the prior task). Starting commit for this pass: `ecbd92e` (confirmed `HEAD == origin/main`, clean except the standing untracked `outputs/supervisor_meeting/`; no intervening changes). Canonical manuscript at the end of this pass: `manuscript/v12_2026-10-10/` (same version; corrections applied in place, no new version needed). No PDF was generated, compiled, rebuilt, or rendered.

This reinspection's own "Decision" section states it found no new error in a reported coefficient, SE, CI, p-value, or checked sample reconciliation — its findings (F01–F08) are documentation/cross-reference/explanation corrections, plus one targeted restricted-data check it explicitly left open. Every finding was independently investigated against the actual code and manuscript text before being accepted.

## F01 — Appendix uses the wrong denominator symbol for country weights

**Status: confirmed.** Read `appendices/B_model_specifications_and_independent_verification.md` directly: "country weight totals equal to N/K." Read `scripts/historical_wash/19_check_model_design.py` directly: its own `K` variable (line 53: `K = int(meta["K_regressors"])`) is the regressor count, matching the manuscript's own `K` in the inference formula (Section 4.5) — a *different* quantity from the country count, which the script itself computes separately as `n_samples` and uses in `expected_total = n / n_samples`. The script's own code comment ("N / K" at line 10) uses a third, looser sense of "K" that matches neither the manuscript's `K` nor `M`. **Correction**: Appendix B §B.3 now reads "$N/M$ (the equal-country-total weighting of Section 4.5, with $M=3$ established-date countries)," with a parenthetical noting the script comment's own looser usage is not reproduced. **Changed**: notation/prose only. **Verification**: direct code read of `19_check_model_design.py`'s `K`/`n_samples` variables. **Limitation**: none; fully resolved.

## F02 — Covariance reconciliation paragraph says the library "did apply" a factor it had omitted

**Status: confirmed.** Re-read Appendix B §B.2's reconciliation paragraph: it states the `group_debias=True` flag "was not passed" to the *original* validation call, then two sentences later describes multiplying "the two pieces linearmodels *did* apply" — including the group-debias piece — as if that piece had already been applied by the same call just described as omitting it. This is self-contradictory as written. **Correction**: rewritten to distinguish the *original, incomplete* call (which applied only the `debiased=True` factor) from the *corrected* call (after adding `group_debias=True`), stating explicitly that it is the corrected call's two factors, multiplied together, that match `16`'s declared formula. **Changed**: prose only — the underlying reconciliation (`24_reconcile_inference_corrections.py`, all 24 cells matching to displayed precision) is unchanged and was not rerun. **Verification**: direct re-read of the paragraph's own internal logic. **Limitation**: none; fully resolved.

## F03 — Age-heterogeneity model incompletely specified in the methods

**Status: confirmed.** Read `scripts/dhs_harmonization/14_household_community_wash_models.py` directly: `AGE_BANDS = [(-1, 5, "0-5"), (5, 11, "6-11"), (11, 23, "12-23"), (23, 35, "24-35"), (35, 47, "36-47"), (47, 59, "48-59")]`, `AGE_BAND_REF = "12-23"`; `add_interactions()` builds interaction terms for *both* `HOUSEHOLD_EXPOSURES` (water and sanitation) against every non-reference band; the model's continuous-control list explicitly drops `b19_raw` (continuous age) when the band dummies are used. The joint tests use `wald_test(..., use_f=False)` and, in the second helper, an explicit `chi2.cdf(stat, df=len(terms))` — confirming a $\chi^2$, not $F$, reference distribution. Independently re-read `outputs/household_community_wash/10_age_heterogeneity_joint_tests.csv`'s own `df` column: 5 for each exposure-specific test, 10 for the combined test — matching the audit's stated restriction counts exactly. **Correction**: `04_empirical_strategy.md` §4.4's schematic single-exposure equation replaced with one showing both exposures and both interaction blocks explicitly, naming the six bands, the reference band, the $\chi^2$ reference distribution, and the 5/5/10 degrees of freedom. **Changed**: equation/prose only — no model was rerun; the displayed 11-of-12 result and its arithmetic are unchanged. **Verification**: direct code read plus independent re-read of the stored `df` column. **Limitation**: none; fully resolved.

## F04 — Results attributes a competing wealth-confounding rationale to a section that did not state it

**Status: confirmed.** Re-read `03_data_and_variables.md` §3.8: it stated only the mediator/post-exposure concern and the correlation-with-exposure rationale for excluding wealth from the historical main specification. `05_results.md` §5.8 (from an earlier correction pass) already said "(Section 3.8 states both the mediator concern and this competing concern...)," which was not yet true. **Correction**: §3.8 now also states the competing concern explicitly — that current wealth could instead proxy *prior* socioeconomic circumstances during the exposure window, which would make omitting wealth leave real confounding unaddressed rather than avoiding over-adjustment — and states plainly that correlation between wealth and exposure alone is not a sufficient reason to omit a potential confounder. This makes §5.8's cross-reference accurate rather than rewriting §5.8 itself. **Changed**: prose only; the wealth-sensitivity coefficient (1.01 vs. 1.03) is unchanged and was not rerun. **Verification**: direct re-read of both sections together after editing. **Limitation**: this remains a genuinely unresolved question about wealth's causal role; the correction states the trade-off honestly rather than resolving it, which this thesis's design cannot do.

## F05 — Root repository guidance mixes an earlier model hierarchy with the final design

**Status: confirmed, three sub-findings.** (1) The root `README.md`'s "Important Methodological Notes" section described the original Steps 00–13 pipeline's own "Model 4 preferred" / "household WASH as robustness only" hierarchy without a scope label, immediately after a paragraph that *does* correctly scope the current, final design — creating exactly the contradiction the audit describes. **Correction**: added an explicit scope note at the section header and within the two specific bullets (preferred specification, primary exposure) stating these describe the original pipeline's own terminology, with a pointer to the current manuscript's actual, different hierarchy. (2) "The scripts in this repository are the exact, unmodified files" — true for `scripts/dhs_harmonization/`, but `scripts/historical_wash/16_estimate_preliminary.py` received a disclosed defensive patch on 2026-10-10 (R05) and three new scripts (`26`–`28`) were added since. **Correction**: scoped the "exact, unmodified" claim to `scripts/dhs_harmonization/` specifically, with an explicit note on the historical pipeline's own patch and its verified zero effect on published results. (3) "25 scripts" — the directory now contains 28 (confirmed via `ls scripts/historical_wash/*.py`), because of the three scripts just added for R05's own tests and verification. **Correction**: replaced the hard-coded count with an instruction to list the directory directly, since this number will keep changing as tooling is added. **Changed**: documentation only. **Verification**: direct `ls` count; direct re-read of the surrounding paragraphs. **Limitation**: none; fully resolved.

## F06 — Author checklist repeats obsolete build and page-count claims

**Status: confirmed, three sub-findings, all self-inflicted by an earlier pass of mine.** (1) My own "Path note," added in an earlier task to `AUTHOR_CHECKLIST.md`, itself called v6 "the only manuscript version with an actual build directory and compiling PDF" — the identical overclaim already found and fixed in `MASTER_ASSEMBLY.md` in a prior pass, but missed here. (2) Line stating "31 of 40 pages used," contradicting this same file's own, correct "32 pages" figure two sections earlier. (3) "the 38 cosmetic overfull-text-box warnings" — 38 is the *v5* build's count; `MASTER_ASSEMBLY.md` already correctly states the *v6* build (what this checklist's own build-path note points to) has 28. **Correction**: all three fixed — the path note now names v3–v6 as the four diagnostic builds, v6 referenced as the most-verified rather than the only one; the page count corrected to 32 with a note that v12 itself is unbuilt; the warning count corrected to 28, with an explicit instruction not to cite the v5 figure as current. **Changed**: documentation only. **Verification**: direct re-read of `MASTER_ASSEMBLY.md`'s own already-correct figures, used as the source of truth for this file's corrections. **Limitation**: none; fully resolved.

## F07 — Citation-map descriptions inconsistent with the corrected source-verification scope

**Status: confirmed, two sub-findings.** (1) `citation_map.md`'s Cumming2019 row described the trial evidence as one factorial design with "separate water/sanitation/hygiene/combined-WASH/nutrition/combined-WASH-plus-nutrition arms," without the SHINE-specific bundled-four-arm distinction that `02_literature_review.md` §2.3 itself carefully draws. **Correction**: the row rewritten to state the Bangladesh/Kenya separate-arms design and SHINE's bundled four-arm design as two distinct things, with a pointer to §2.3 for full detail. (2) The map's own header paragraph said "all 20 cited sources' claim-level support was read directly" — directly contradicted by the very next entries, where Blom2022 is explicitly categorised as "indirect version correspondence," not a direct read. **Correction**: changed to "19 of the 20... read directly... the sole exception is Blom2022." **Changed**: documentation only — no citation, bibliographic entry, or claim verdict changed. **Verification**: direct comparison of the map's summary language against its own detailed rows and against §2.3's text. **Limitation**: none; fully resolved.

## F08 — Remaining cross-reference and reporting-scope wording

**Status: confirmed, four sub-findings.** (1) Three passages cited "Section 3.4" (baseline covariates/weights) or a range starting at "3.4" for purely historical topics (IHME exposure construction, population-weighted-vs-area-averaged comparison, the historical exposure-window equation) — confirmed by re-reading `03_data_and_variables.md`'s own section headers (§3.4 = baseline; §3.5 = historical extension scope/IHME products) that these should start at or reference §3.5, not §3.4. **Correction**: all four instances (two in `06_discussion_and_limitations.md`, one each in `04_empirical_strategy.md` and `06_discussion_and_limitations.md`'s exposure-definition bullet) corrected to §3.5 or §3.5–3.7 as appropriate. (2) `05_results.md`'s opening sentence claimed "exact p-values throughout," while many displayed values are rounded to three decimals or shown as "<.001." **Correction**: rewritten to state the actual displayed precision. (3) Appendix B §B.1 claimed both inference conventions "are reported wherever this coefficient is cited in the main text" — not true of the abstract, introduction, or conclusion, which present only the primary convention. **Correction**: scoped to the two sections where the sensitivity convention is actually reported (`04_empirical_strategy.md` §4.5, `05_results.md` §5.1). **Changed**: prose/cross-references only. **Verification**: direct re-read of the cited sections' actual headers and content; direct re-read of the abstract/introduction/conclusion to confirm the sensitivity convention's absence there. **Limitation**: none; fully resolved.

## Targeted restricted-data check: baseline-age (`b19`) eligibility

**Status: checked directly against the actual frozen restricted data; no sample defect found.**

The reinspection correctly identified that the manuscript describes under-five eligibility and a uniform `b19` age control, but that the inspected code does not visibly impose an explicit 0–59 filter *in the main estimation path* — and correctly declined to assume this means a defect exists.

Investigated directly: `scripts/dhs_harmonization/14_household_community_wash_models.py` (lines 175–177) contains a hard-fail runtime assertion —

```python
if df["b19_raw"].min() < 0 or df["b19_raw"].max() > 59:
    raise RuntimeError(f"b19_raw out of expected [0,59] range: min={df['b19_raw'].min()} max={df['b19_raw'].max()}. STOP.")
```

— run immediately on load, before any model is estimated. This is a **check**, not an active filter: it halts the entire script if violated, rather than silently dropping out-of-range rows. Since the pipeline's own stored outputs exist (used as the authoritative source throughout this manuscript), this assertion did not trigger when the actual pipeline ran — but to confirm this directly rather than by inference, the actual frozen input file was read:

```python
df = pd.read_parquet('data/processed/pooled_kr_four_country_birth_order.parquet')  # 70,231 rows, the full pooled file, read-only
```

**Result**: across all 70,231 children in the full pooled baseline file (the superset of every outcome-specific estimation sample used anywhere in this thesis) —
- Missing (`NaN`) `b19_raw`: **0**
- Non-finite values among non-missing: **0**
- Values outside `[0, 59]`: **0**
- Observed range: **min = 0, max = 59** (exactly the boundary values, confirming the full range is used, not an artificially narrow sub-range)

Since every outcome-specific estimation sample used in this thesis is a *subset* of this 70,231-row file (restricted further only by outcome validity and WASH classifiability, not by age), a universally compliant superset guarantees every subset is too — no further subset-level check could find a violation this superset-level check would have missed, and none was found.

**Conclusion**: under-five eligibility for `b19` is **inherited from the DHS source/measurement universe itself** (the Children's Recode's own current-age-in-months field, populated only for children within the survey's own under-five birth-history frame), not actively imposed by a drop/filter step anywhere in this pipeline's code. Script 14's assertion is a defensive confirmation of this inherited property, not evidence that a filter was needed or that one was silently applied. **No sample defect was found, no observation was dropped, and no model was rerun or re-estimated as a result of this check.**

## Literature checks (reinspection's own, confirmatory — no correction required)

The reinspection's fresh Crossref/primary-source checks (Cumming et al. 2019 and Headey and Palloni 2019, read directly; 16 of 18 DOI requests resolved, two rate-limited) found no new title/author/DOI discrepancy and found the corrected chapter descriptions consistent with the primary sources. This is confirmatory of work already done in prior passes; no action was required or taken here.

## Summary table

| ID | Status | Changed |
|---|---|---|
| F01 | Confirmed | Notation only |
| F02 | Confirmed | Prose only |
| F03 | Confirmed | Equation/prose only |
| F04 | Confirmed | Prose only |
| F05 | Confirmed (3 sub-findings) | Documentation only |
| F06 | Confirmed (3 sub-findings, self-inflicted) | Documentation only |
| F07 | Confirmed (2 sub-findings) | Documentation only |
| F08 | Confirmed (4 sub-findings) | Prose/cross-references only |
| `b19` check | Checked against actual restricted data; no defect found | Nothing changed — confirmatory |

**All eight findings were confirmed.** None required changing an estimate, sample, or control set. The targeted restricted-data check found no sample defect — eligibility is inherited from the source, not imposed by a filter, confirmed directly against the full 70,231-row frozen baseline file.

## What this pass did not do

Did not change any published coefficient, standard error, confidence interval, p-value, sample, weight, or control set. Did not drop any observation or rerun any model — the `b19` check was read-only against the existing frozen file. Did not generate, compile, rebuild, or render any PDF. Did not reopen any item already closed in prior passes beyond what this reinspection specifically identified.

## Canonical path and commit

`manuscript/v12_2026-10-10/` (unchanged version; corrections applied in place). Commit follows this file.

## Addendum (2026-10-10): two residual wording corrections from `Correction_Verification_e3fa699_2026-10-10.md`

A further independent verification of commit `e3fa699` (the commit resulting from the F01–F08 pass above) checked the eight corrections directly against the repository and confirmed all eight present and correct, with a battery of fresh numerical/synthetic checks (291 historical model rows, 1,323 baseline rows, 56 displayed-value spot checks, leave-one-out and temporal-window synthetic reconstructions, bibliography-key resolution, and others) passing. It identified two further, narrower wording issues in the F01 and F07 corrections themselves — not new findings against the original audit, but imprecisions introduced by this pass's own fixes:

**Residual 1 (refines F01).** Appendix B §B.3's corrected sentence stated "$M=3$ established-date countries" unconditionally, but the 24 primary historical models are not all pooled: confirmed directly from `scripts/historical_wash/21_validate_all_primary_cells.py`'s own header ("2 products x 3 outcomes x {GH2014, KE2014, NG2018, POOLED_ESTABLISHED}" = 2×3×4 = 24), 18 of the 24 are single-country models (`M=1`) and only 6 are established-date pooled models (`M=3`). **Correction**: the sentence now states $M$ as the country count *for that particular model*, with $M=1$ for the 18 country-specific models and $M=3$ for the 6 pooled models, explicitly flagging that $M=3$ does not hold uniformly across all 24. **Changed**: wording only; the underlying weighting code and all design-check results are unaffected.

**Residual 2 (refines F07).** The Cumming2019 row's own prior fix (from the F07 pass) still contained an internal inconsistency: it said "every WASH-related arm in all three trials" showed no detectable linear-growth effect, in the same clause that then describes the combined WASH-plus-nutrition arm as showing "no *additional* growth benefit over nutrition alone" — the first clause's "WASH-related" is broad enough to include the WASH-plus-nutrition arm, contradicting the second clause's more qualified claim about it. Cross-checked directly against `02_literature_review.md` §2.3, which already draws this distinction correctly. **Correction**: narrowed to "the WASH-only arms showed no statistically detectable effect on linear growth... nutrition interventions produced modest growth improvements... and adding WASH to nutrition showed no additional growth benefit over nutrition alone" — matching §2.3's own, already-correct phrasing. **Changed**: wording only; no citation, bibliography key, or claim-support verdict changed.

Both residuals are confirmed as real (self-inflicted, within-pass) wording imprecisions, corrected exactly as specified by the verification report. Neither affects any coefficient, standard error, sample, weight, control set, or bibliography entry. No model was rerun; no PDF was generated, compiled, or rendered.
