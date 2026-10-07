# Independent audit v1 (2026-10-07)

Full-chain audit of the thesis repository: raw sources → harmonisation → constructed variables → sample selection → exposure construction → model specification/estimation → inference → tables/figures → manuscript claims/references → final document assembly. Audited commit: `5da82cf` (branch `main`, confirmed equal to `origin/main`).

**Start here**: `00_executive_readiness_assessment.md` — answers the ten summary questions this audit was asked to answer, each with its own evidence pointer.

## Files

| File | Content |
|---|---|
| `00_executive_readiness_assessment.md` | Ten-question summary: what was inspected, what was independently reproduced, errors found, whether any changed results, what remains unverified, inherent limitations, sync status, authoritative paths, draft/submission readiness |
| `01_repository_authority_map.md` | Which file governs each analysis family; confirms no competing/ambiguous authority exists |
| `02_audit_checklist_and_evidence_log.md` | Phase-by-phase (1–10) checklist with evidence and verdict for every item checked, including an explicit list of what was **not** verified |
| `03_issue_register.md` | Every issue found across this project's history, classified (confirmed error / unresolved gap / inherent limitation / defensible choice / superseded-file inconsistency), with severity, consequence, action, and status |
| `04_numerical_claim_reconciliation.md` | This audit's own fresh numerical spot-checks, with results |
| `05_correction_change_impact_report.md` | Confirms no empirical result changed; explains why no new manuscript version was needed |
| `06_remaining_actions.md` | Concrete next actions, split by who can take them |
| `07_update_2026-10-07_pass2.md` | Closes the material-verification gaps named above: all 24 primary historical cells now independently reproduced (was 4 of 24); spatial-extraction data layer independently verified; IPUMS/IHME metadata re-checked from raw files; one literature overclaim found and corrected. Supersedes specific claims in `00`, `02`, `03` (each marked with its own banner); those files are otherwise unchanged. |
| `08_update_2026-10-07_pass3.md` | Full SE/CI/p-value/rank comparison for all 24 historical cells (not just coefficients); leave-one-out community exposure independently rebuilt from raw DHS records (a real bug was found and fixed in the new validation script itself, not the pipeline); region-FE/joint-model baseline check, buffer-averaging Monte Carlo validation, and the remaining 11 literature sources. **Its explanation of the SE/CI/p-value differences as "numerical noise" (§1) is wrong and corrected in `09_update_2026-10-07_pass4.md` §1 — read that instead.** |
| `09_update_2026-10-07_pass4.md` | **Read this too.** Corrects pass 3's unverified "numerical noise" claim with the actual, demonstrated cause (a missing `linearmodels` covariance flag — closes the SE gap to exactly 0.0 for all 24 cells); corrects unsupported "unlikely to be a multiplicity artefact" language in the manuscript; documents real PDF clipping found by rendering pages to images (not previously caught by text extraction or warning counts) and its fix. |

## Headline conclusion

Seventeen confirmed errors found across this project's history, all resolved, none in a stored empirical result: eleven in pass 1; one literature overclaim (Donohue et al. 2023) in pass 2; one more literature overclaim (Addae et al. 2024) in pass 3; and four in pass 4 — a real PDF table-clipping bug and a separate double-escaping rendering bug (both in `md2tex.py`), an unsupported "unlikely to be a multiplicity artefact" claim in the manuscript, and the audit's own prior "numerical noise" explanation for a validation-script SE discrepancy, which pass 4 found was asserted without being demonstrated and replaced with the actual, demonstrated cause (a missing `linearmodels` covariance flag).

As of pass 4 (`09_update_2026-10-07_pass4.md`), all 24 of 24 primary historical model cells are independently reproduced by a second estimation library with their full SE/CI/p-value comparison exactly reconciled (not merely close); all four distinct baseline estimator/inference paths (household cluster-FE, household region-FE, community 4-stage, joint household/community) have an independently reproduced headline cell; the buffer-averaging algorithm's output (not only its data layer) is independently validated by Monte Carlo spatial sampling; and all 20 of 20 cited literature sources have claim-level verification. What remains genuinely unverified by a second implementation: the 267 non-primary sensitivity-family historical models. See `00_executive_readiness_assessment.md`, `08_update_2026-10-07_pass3.md`, and `09_update_2026-10-07_pass4.md` together for the full, qualified answer on draft-vs-submission readiness.
