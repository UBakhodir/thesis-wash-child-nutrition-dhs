# Status and limitations (2026-10-07)

## Status labels used across this package

- **Validated for main reporting** — baseline specifications in `00_results_index.md`§A; reproduced directly from stored CSVs in this pass.
- **Validated secondary / robustness** — joint model, age-heterogeneity, Nigeria sensitivity, country-specific models; correct and reproducible, but not the headline specifications.
- **Exploratory/provisional** — the entire historical WASH extension (§B). Internally validated (independent re-estimation, design checks) but not promoted to a thesis finding because the items below are still open.
- **Superseded** — preserved, not cited (§D of the index).
- **Not estimable** — none in this package.

## What changed in this pass versus the prior state

1. Confirmed local HEAD and `origin/main` both at `be71d576918e090476e69dc57d071918fba320a1`, 0 ahead/0 behind, via a safe fetch.
2. Re-derived the baseline reporting numbers from source CSVs rather than from any prior chat or document, and found the earlier audit's two flagged items were real but one was mischaracterised: the roadmap's household cluster-FE p-values (.080/.574) are an exact, labelled sensitivity-convention output, not a computational error; the project's own adjudicated primary convention gives .062/.548. The age-heterogeneity count is confirmed wrong in the roadmap (10 of 12) versus correct (11 of 12).
3. Built the first supervisor-advice implementation matrix from the actual meeting transcript (previously only a roadmap PDF existed, which is the author's own document, not the supervisor's words).
4. Re-attempted DHS biomarker-weight documentation via two further sources; both unsuccessful.
5. Did not rerun any estimation. All 291 historical models and all baseline models were already estimated and validated in the prior session; their manifests show unchanged inputs.

## Unresolved issues that must be closed before the historical extension can become a thesis result

Carried from `historical_wash_preliminary_estimation_methods_2026-10-06.md` §9, with this pass's status:

1. **Measurement-subsample/biomarker weight** — still undocumented. Re-tried DHS-8 Biomarker Manual (403) and a World Bank microdata catalogue variable page (no weighting guidance). The within-survey PERWEIGHT-normalization inference remains an assumption, not a documented rule. *Consequence if left unresolved: historical coefficients can be reported only as associations within the measured subsample, with this caveat stated, not as population-representative estimates.*
2. **Nigeria 2018 measured-count gap** (12,806 official vs. 11,704 extract non-NIU) — unexplained; plausibly mothers absent from the IPUMS birth-history extract. Not closed.
3. **Water product definition (W_IMP)** — not verified from the IHME source study text beyond "annual estimates of access to drinking water... at about 5×5 km resolution." Not closed.
4. **Ethiopia interview timing** — three candidates (C1–C3), all provisional; kept out of established-date estimates.
5. **Window choice** — 12-month window is a working choice; literature (Cumming & Cairncross 2016, abstract-level) supports an early-life window generally but points more toward 24 months specifically. Not resolved; both are reported, neither is privileged.
6. **DHS/IHME input overlap** (Ghana, Kenya) — disclosed and tested by exclusion, not removed from primary estimates.
7. **Pooled weighting estimand** — equal-country-total PERWEIGHT is the working convention; the unweighted comparison shows material sensitivity (pooled water HAZ 1.03 weighted vs. 0.41 unweighted). Not resolved; both reported.

None of these is a blocker to using the **baseline** (current four-round) results in the manuscript. They are blockers only to presenting the historical extension as more than a labelled, preliminary, exploratory addition.

## What is explicitly out of scope here (by the author's own instruction)

- Drafting any thesis chapter, introduction, or literature review (supervisor-advice matrix items 3 and 10).
- Resolving the "Impact" / "Sub-Saharan Africa" title question (matrix item 11) — this is the author's own open question to the supervisor, not something the empirical package can answer.
- Generating a thesis PDF.

See `docs/provenance/historical_wash_supervisor_advice_matrix_2026-10-07.md` for the full mapping and `thesis_readiness_audit_v1_2026-10-06.md` (outside this repository, in the master folder's `audit_reports/`) for the broader manuscript-readiness assessment, which this package's findings should be read alongside.
