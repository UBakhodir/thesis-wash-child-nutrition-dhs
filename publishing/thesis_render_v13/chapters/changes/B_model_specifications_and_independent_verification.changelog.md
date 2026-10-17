# Verification and language-edit change log: Appendix B

Status: **Awaiting author review.** Not added to `chapters/APPROVED.tsv`. Nothing in this log is supervisor-approved.

Appendix B is the publishing system's `appB` unit. It is numbered **Appendix B** (sections B.1–B.4, Tables B.1–B.2); it is not a chapter and not "Chapter 9".

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/appendices/B_model_specifications_and_independent_verification.md` at academic source commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78` (last changed in `1621294`) | `0bb6281ace37a772536a64938d50fae9cfa7232e1bbaa988957c3be772f2075f` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/B_model_specifications_and_independent_verification.md` | `99b61c66d1440f2faf49f2cb192d0792c92e49231dce12d76aaa78f7fb9979d6` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/B_model_specifications_and_independent_verification.tex` | `d83b2e1d8e4ebcfe843a59ca078744603e28be0787ad32ac2e12526d58b0e316` |
| Word diff | `chapters/changes/B_model_specifications_and_independent_verification.worddiff.txt` | recorded in `HANDOVER.md` §20 |

The word diff marks removed text as `[-…-]` and added text as `{+…+}`; `<nbsp>` marks a no-break space. Raw-LaTeX layout blocks (D) appear in it as added text.

**Sources checked against.** The canonical appendix was read in full against:
- the reviewed publishing copies of Chapter 4 (§§4.1–4.6), Chapter 5 (§5.1, §5.6), Appendix A (§A.3) and the abstract, introduction and conclusion (the *p* = .062 statements);
- the reporting map and core reporting table (`docs/provenance/final_empirical_package_v3_2026-10-07/`), the v2 results index, and the independent-audit records (pass 2, pass 3, pass 4; `cluster_fe_inference_adjudication.md`; `independent_audit_resolution_v1_2026-10-10.md`; the issue register);
- the implementing code at `c58fc47`: `scripts/dhs_harmonization/14_household_community_wash_models.py` (and `11` for singletons) and `scripts/historical_wash/16`, `17`, `19`, `20`, `21`, `24`, `25`, `26`, `27`, `28`, plus `16` at `be71d57` (pre-safeguard);
- the stored public outputs: `outputs/household_community_wash/03_household_cluster_fe.csv` and `run_log.txt`; `docs/provenance/historical_wash_preliminary_estimates_v1/` (`model_coefficients_…`, `independent_validation_…`, `design_checks_per_model_…`); `docs/provenance/fit_safeguard_verification_comparison_v2_2026-10-10.json` (and `_v1`);
- the third-party library source the appendix cites: `linearmodels` 7.0 and `statsmodels` 0.14.6 (sdists from PyPI, read only).

No restricted data was read, no model or pipeline was run, no estimator or sample was changed, and no new empirical result was generated. Every check, with its evidence class, is in `verify_appB.tsv` (204/204 OK; see the verification report).

**Length.** No page target was imposed and nothing was removed. The copy has about 4,010 words against 2,549 in the canonical file; the increase comes from the verified clarifications in B. The rendered body is 11 pages (preview pp. 1–11). Page-budget editing is deferred to final assembly (FA-5, FA-11).

**Citations.** None in the canonical file; none added.

## A. Verified corrections (canonical file unchanged)

Each item corrects a statement that is wrong, imprecise in a way that overstates what was checked, or points to the wrong place. Whether the canonical v12 file is also corrected is the author's decision (register FA-22 A).

### A1. Script 17's agreement applied to β only

- **Canonical.** "…re-estimated four representative *country-specific* cells … with an explicit-dummy-variable statsmodels implementation, matching to 3×10⁻¹⁴."
- **Evidence (stored output).** `independent_validation_summary.json`: `max_beta_abs_diff` 2.9639×10⁻¹⁴, `max_se_rel_diff` 7.5165×10⁻¹⁰, all N and G match; pass thresholds 10⁻⁶ in `17_validate_estimates.py`. The SEs agree to a relative 7.5×10⁻¹⁰, not 3×10⁻¹⁴. One of the four cells (Ghana water–HAZ unweighted, `m0005`) is in the unweighted-comparison family, not a primary cell.
- **Correction.** States β within 3×10⁻¹⁴ (maximum 2.96×10⁻¹⁴), SE within a relative 7.5×10⁻¹⁰, identical N and G, names the public output, identifies `m0005`, and describes the implementation (own filters; `statsmodels` WLS with explicit cluster dummies; CRV1 by hand with K counting only non-fixed-effect regressors).

### A2. Table B.2: the β difference and the unweighted stored value

- **Canonical.** Row "β per 10 points | 1.0255531 | 1.025553 | 6.7×10⁻⁸"; row "Unweighted counterpart β per 10 | 0.4147 | 0.41 (documented) | consistent"; residual SD difference "~0".
- **Evidence.** `20_validate_pooled_estimate.py` holds `STORED = {"beta_per_10": 1.025553, "se_per_10": 0.260730, …}` (six-decimal constants) and computes `beta_match_abs_diff` against that constant. The stored public value (`model_coefficients_PRELIMINARY_AGGREGATE.csv`, `m0004`) is 1.025553067200643, so 6.7×10⁻⁸ is the rounding of the constant, not an estimator difference. The full-precision comparison for this cell (script 21) is 2.4×10⁻¹⁴ (pass-3 record, row W_IMP HAZ POOLED). The stored unweighted counterpart (`m0008`, N 23,018, G 3,114) is 0.4146971.
- **Correction.** Stored column shows 1.025553067 (`m0004`) and 0.4146971 (`m0008`); the β difference cell says it is measured against the six-decimal value, with a table note giving the full-precision value and script 21's 2.4×10⁻¹⁴; "consistent" → "none at four decimals"; "~0" → "none at six decimals" (the independent values are recorded only at those precisions). The SE row is kept as originally run (3.6×10⁻⁵, explained in the text). The note also states that the independent rank is of the raw regressor matrix and the stored rank of the within-transformed matrix (`20…py` line 182 vs `16…py` `fit()`).

### A3. Stale line pointer in `16_estimate_preliminary.py`

- **Canonical.** "(read directly from its source, lines 209–212)".
- **Evidence (code).** At `c58fc47` the correction is on line 248, the *t*(*G*−1) critical value on line 251, the CI bounds on line 264 and the *p*-value on line 265. Lines 209/212 hold these statements in `be71d57`, before the 2026-10-10 safeguard inserted about 40 lines.
- **Correction.** "(function `fit()`, lines 248, 251 and 264–265 at commit `c58fc47`)", with K defined (retained non-fixed-effect regressors; 24 for the pooled cell; absorbed cluster effects not counted).

### A4. Diagnostic: overstatement of what the reconstruction shows

- **Canonical.** "The age-in-months control, in contrast, fully accounts for the gap on its own"; "a faithful reconstruction of the described design" (twice).
- **Evidence.** `25_diagnose_birthyear_coding_and_age_control.py` calls its scheme a "Diagnostic reconstruction, not a claim of byte-identity with the original (unpreserved) buggy script" and its result "evidence the age_m omission explains it, not a claim of exact recovery". The reconstruction reproduces 1.3852855 against the documented "1.385" only approximately; faithfulness to the unpreserved code cannot be checked.
- **Correction.** "accounts for the gap on this reconstruction"; "a reconstruction of the described design"; the no-exact-recovery sentence is kept. *The same wording occurs in Chapter 4 §4.6 (publishing copy); it was not changed there (register FA-22 B).*

### A5. SE reconciliation: attribution and precision

- **Canonical.** "**every one of the 24 cells' SE now matches the stored value to the displayed precision (max remaining difference 0.0 at 8 decimal places)**".
- **Evidence.** The pass-4 record reports the maximum and mean |diff| as 0.0 "to the displayed 8-decimal precision"; the per-cell table is RESTRICTED.
- **Correction.** "…the pass-4 audit record reports a maximum absolute SE difference of 0.0 against the stored value at its displayed eight-decimal precision." The algebraic-residual sentence is kept and attributed in the same way. Script 24 is described as using sample code copied from script 21 (its docstring), so it is the same second implementation, not a third.

### A6. Step 3: what "2.23×10⁻¹⁶" is

- **Canonical.** "…differ by a maximum of 1.73×10⁻¹⁵ in absolute terms (relative to the vector's own norm, 2.23×10⁻¹⁶)" (readable as the norm being 2.23×10⁻¹⁶).
- **Evidence (code).** `rel_diff = max_abs_diff / ‖e_local·√W‖`.
- **Correction.** "…differ by at most 1.73×10⁻¹⁵ in absolute terms; divided by the weighted norm of the residual vector, that maximum is 2.23×10⁻¹⁶."

### A7. "At the level of machine epsilon"

- **Canonical.** "both differences at the level of floating-point machine epsilon, not an approximation".
- **Evidence (arithmetic).** 6.661338147750939×10⁻¹⁶ is three units in the last place of a double near 1.03; 2.220446049250313×10⁻¹⁶ is one unit (machine epsilon 2.2×10⁻¹⁶).
- **Correction.** "These differences are three and one units in the last place of a double-precision number near 1 (machine epsilon 2.2×10⁻¹⁶)."

### A8. B.4: the 15 compared columns

- **Canonical.** "…(coefficient, SE, both CI bounds, and p-value at both the per-point and per-10-point scale, plus …)".
- **Evidence (stored JSON).** `numeric_columns_compared` lists `p_value` once; 4 quantities × 2 scales + `p_value` + 6 others = 15.
- **Correction.** "the coefficient, SE and both CI bounds at both the per-point and the per-10-point scale, the *p*-value, `E_within_sd`, …". The count (15) and the result (0.0) are unchanged.

## B. Clarifications added (verified; no new estimate)

| # | Location | Added (abridged) | Evidence (class) |
|---|---|---|---|
| B1 | Opening paragraph | Equations are in Chapter 4; scope of each section; what RESTRICTED means; nothing re-executed | Chapter 4 headings (TEXT) |
| B2 | Table B.1 note | N 36,040; G 4,426 PSUs (`country_psu`); joint water and sanitation; normal reference for both rows; source rows | `03_household_cluster_fe.csv` (OUTPUT); p and CI recomputed from stored β and SE under normal and *t*(*G*−1) (ARITH) |
| B3 | B.1 "How the two conventions are computed" | Weighted within-PSU demeaning (within-cluster variation; equivalent to PSU dummies); `statsmodels` `cov_type="cluster"`; c = G/(G−1)×(N−1)/(N−K); K = 18 (PRIMARY) vs 18 + 4,426 = 4,444 (FULL_DUMMY_DF); SE scale √((N−18)/(N−4,444)) = 1.0677; `use_t: False`; Ghana-subset equivalence 2.59×10⁻¹⁵ / 5.57×10⁻¹⁵ (N 4,287, 613 PSUs); no baseline singleton step; region-FE models use explicit dummies with the constant and region dummies in K and the normal reference | `14_…py` (CODE), `statsmodels` 0.14.6 `cov_cluster` (LIB), `03_…csv`, `run_log.txt` (OUTPUT) |
| B4 | B.2 opening | Script 17's implementation; `m0005` | A1 |
| B5 | B.2 after the list | Independence scope: filtering, weighting, design and estimation are separate; upstream construction in the shared analysis-candidates file (exposure, validity flags, birth year, calendar age, weight field) is not re-verified | `20`, `21`, `24`, `25` read the same file; imports contain no project module (CODE) |
| B6 | Diagnostic | E10 = exposure/10; tolerances 10⁻⁸ (rank, relative), 10⁻¹⁰ (absorption), 10⁻⁸ (same vector, relative) | `25_…py` constants (CODE) |
| B7 | Step 4 | Displayed formula with W, e and ỹ defined | `25_…py` FWL code (CODE) |
| B8 | Step 5 | "Exactly" = elementwise with absolute tolerance 10⁻¹² for 0/1 columns | `np.allclose(…, atol=1e-12)` (CODE) |
| B9 | SE paragraph | `auto_df` nested case → no extra df; `debiased` scale N/(N−K); `group_debias` factor; aligned display of the product | `linearmodels` 7.0 source (LIB); identity checked numerically (ARITH) |
| B10 | New paragraph after the SE paragraph | CI and *p* explicitly from *t*(*G*−1), not `linearmodels`' native `df_resid` = N − K − G (1,571 to 19,918 vs G − 1 of 352 to 3,114); maxima 1.4×10⁻¹³ / 7.6×10⁻¹⁴ / 1.2×10⁻¹³ within the 10⁻⁹ "exact" tolerance; native contrast up to 0.0065 / 0.00069 in three of the six Ghana cells (G = 353); script 20's own native CIs and *p* not reported | pass-4 record (CARRIED); `24_…py` (CODE); df ranges recomputed from stored N, K, G (ARITH); `results.py` (LIB) |
| B11 | New "Coverage across the 291 historical models" | 24 primary cells (21: β, SE, N, G; 24: SE, CI, *p*); `m0005` (17) and `m0008` (20); remaining 265 not re-estimated with a second implementation; checked only internally (estimator safeguards; same-function rerun) | stored CSV families (OUTPUT); 291 − 24 − 2 = 265 (ARITH) |
| B12 | "What this verification establishes" | Adds: not representativeness, not external validity, not resolution of weighting and selection limitations, not robustness to multiple testing; no multiplicity adjustment | Restates the abstract's A4 and Chapters 5–6 qualifications (TEXT) |
| B13 | B.3 | Public per-model file (24 rows, all pass); relative tolerance 10⁻⁶; "full rank" = recorded rank equals retained regressors | `design_checks_per_model_…csv` (OUTPUT); `19_…py` (CODE) |
| B14 | B.3 second paragraph | Baseline country totals 1, historical N/M; common constant leaves WLS β and the cluster sandwich unchanged (bread ∝ 1/c, meat ∝ c²); equal totals ≠ equal influence; K/M notation in `19` and `16` stated precisely (replaces the canonical parenthetical, same content) | Chapter 4 §4.5; `19_…py`, `16_…py` (CODE); synthetic numerical demonstration (ARITH) |
| B15 | B.4 opening | The external audit file is not in the repository; R05 and its resolution are recorded in `independent_audit_resolution_v1_2026-10-10.md` | repository search (TEXT); resolution document (CARRIED) |
| B16 | B.4 tests | The four tests pass according to the project's recorded run; not re-run here | (OPEN for re-execution; code inspected) |
| B17 | B.4 rerun | The verification rerun is the same function on the same inputs; it shows the patch left the output unchanged and is not an independent implementation | comparison JSON (OUTPUT) |

## C. Captions and structure (no table added, no row or column removed)

- **Captions added to the two existing tables**, numbered in order of appearance: Table B.1 "Household water and sanitation coefficients for HAZ under the two inference conventions (baseline household cluster-fixed-effects model)" and Table B.2 "Independent re-estimation of the pooled established-date water–HAZ model compared with the stored estimate". LaTeX numbers them and checks the typed number (`\ThesisCheckNumber`). All rows (2 and 7) and columns (7 and 4) are kept.
- **Table notes.** Two 9/13.5 pt notes carry B2 and the A2 explanation.
- **Order.** The canonical "…the independent estimate converged to:" was followed by the diagnostic, not by the table. Table B.2 and its log pointer now follow that paragraph directly ("…converged to the values in Table B.2"); the diagnostic follows the table. Content unchanged.
- **References.** "`04_empirical_strategy.md` §4.5 and `05_results.md` §5.1" → "Section 4.5 and Section 5.1"; "(reproduced in Appendix A.3)" → "(reproduced in Appendix A, Section A.3)"; "`16`'s declared" → "the declared … of `16_estimate_preliminary.py`".
- **Formulas.** The canonical code-span formulas (`(G/(G-1)) × ((N-1)/(N-K))`, `N/(N-K)`, `(G/(G-1)) × ((N-1)/N)`, the product) are set as mathematics; the product is an aligned display equation. Same terms.
- **Formatting.** Bold emphasis kept as in the canonical file (ch01 bold → italics decision pending).

## D. Layout fixes (publishing copy only; words unchanged unless stated)

- Ragged-right groups (indent restored, widow and club penalties 10000) around 18 path-heavy or long-number paragraphs and the list, and `\raggedright` inside the two table notes. Justified, they produced 19 lines extending 3–63 pt into the right margin. The same technique as Appendix A.
- No-break spaces after "Section(s)", "Table", "Appendix", "Chapter" and "script" before a number (30), not in headings or caption lines (the filter detects those by an ordinary space).
- Apostrophe after a code span: `PanelOLS`'s printed with a left quote; the curly apostrophe is now typed (3 places).
- Step 4: "Computed from first principles rather than read from `PanelOLS`'s output, this β matches `PanelOLS`'s own fitted coefficient within 4.4×10⁻¹⁶…" → "This β is computed from first principles, not read from the output of `PanelOLS`, and it agrees with the coefficient that `PanelOLS` itself fits to within 4.4×10⁻¹⁶…" (the code font was hyphenated "Pan-elOLS" and a one-word widow line followed).

## E. Language edit (Humanizer, applied conservatively)

- Em dashes in prose replaced (18 lines → 3, the heading and caption separators the converter requires); range and name en dashes kept (4.1–4.6, 2013–2017, water–HAZ, Frisch–Waugh–Lovell).
- Long sentences split (B.2 opening, first attempt, diagnostic introduction, Steps 2–5, the SE paragraph, B.3, B.4); "not speculation" dropped from the diagnostic heading because the following text already states the evidence and its limits; "fully" kept in "fully explained" for the SE difference because pass 4 demonstrates it algebraically.
- Not changed: identifiers, numbers, equations, tolerances, record paths, model labels and every methodological qualification. No causal, panel, DiD or IV language was introduced (checked).

## F. Shared files

- **None changed.** Template, filter (`396c9109…3ca9`), build script (`8568a446…655cb`), drivers and bibliography are byte-identical to the received package. The FA-20 appendix continuation path was exercised: the generated `.tex` carries `\endfirsthead` and "Table B.n (continued)" for both tables. Neither table breaks in the delivered PDF, so a scratch stress test (Table B.2 rows repeated eight times, compiled outside the package and not delivered) confirmed that the continuation label and repeated column heads print on the continuation page and the note stays with the last rows.
- No earlier unit was converted or rebuilt.

## G. Decisions and follow-ups for the author (nothing changed)

- **G1. Canonical synchronisation** of A1–A8 (and B, C as accepted) with the canonical Appendix B; if done, update `source_manifest.tsv` deliberately (FA-13 procedure). The same "6.7×10⁻⁸" figure appears in `claim_evidence_ledger.md`, `01_final_reporting_map.md`, `02_core_reporting_table.md` and the v2 results index; whether those records are annotated is the author's decision. Register FA-22 A.
- **G2. Chapter 4 §4.6** carries "fully accounts for the gap on its own" and "a faithful reconstruction of the described early attempt". Consider aligning with A4 at final assembly. Register FA-22 B.
- **G3. "Model specifications" in the title.** The appendix does not restate the estimating equations; it points to Chapter 4. Adding a specification summary would duplicate Chapter 4 (which has pending corrections FA-8, FA-12). Not added. Register FA-22 C.
- **G4. Baseline PanelOLS cross-validation (observation, unresolved).** The adjudication record reports PanelOLS agreeing with the baseline statsmodels SEs "to four to five decimal places". An omitted `group_debias=True` would produce a relative SE difference of about 1×10⁻⁴ at G = 4,426, N = 36,040, which would fit that agreement level, but the call used for the baseline cross-validation is not in a public record and was not checked. The stored baseline SEs come from statsmodels and are not affected either way. Register FA-22 D (local check).
- **G5. Script docstrings with stale line pointers** (not in the appendix): `21_…py` addendum ("line 124" for the fit call, which is line 137), `24_…py` ("lines 157-237", "lines 212, 225"), pass-4 record ("21 (line 124)"). Repository hygiene; author decision. Register FA-22 E.
- **G6. Layout.** Table B.2 is kept whole on p. 4 and leaves white space at the foot of p. 3 (keep logic, FA-10). Final pagination at assembly.
- **G7. Length.** About 4,010 words vs 2,549; nothing to shorten now (FA-11).
