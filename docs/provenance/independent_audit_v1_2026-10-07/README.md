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
| `07_update_2026-10-07_pass2.md` | **Read this too.** Closes the material-verification gaps named above: all 24 primary historical cells now independently reproduced (was 4 of 24); spatial-extraction data layer independently verified; IPUMS/IHME metadata re-checked from raw files; one literature overclaim found and corrected. Supersedes specific claims in `00`, `02`, `03` (each marked with its own banner); those files are otherwise unchanged. |

## Headline conclusion

Twelve confirmed errors found across this project's history (eleven in pass 1, one more — a literature overclaim about Donohue et al. 2023 — in pass 2), all resolved, none in a stored empirical result. As of pass 2 (`07_update_2026-10-07_pass2.md`), all 24 of 24 primary historical model cells are independently reproduced by a second estimation library (max coefficient discrepancy ≤6×10⁻¹⁴), and the spatial-extraction data layer is independently verified against 48 justified test cases. What remains genuinely unverified by a second implementation: the exact-polygon-overlap buffer-averaging algorithm itself, the 267 non-primary sensitivity-family historical models, and 11 of 20 cited literature sources' specific claims — stated plainly in `07_update_2026-10-07_pass2.md`, not closed by this audit. See `00_executive_readiness_assessment.md` and `07_update_2026-10-07_pass2.md` together for the full, qualified answer on draft-vs-submission readiness.
