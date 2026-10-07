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

## Headline conclusion

Eleven confirmed errors found across this project's history, all already resolved before or during this audit, none in a stored empirical result. The strongest independent evidence in the project is the from-scratch reconstruction of the pooled historical water–HAZ model with a different estimation library, matching the stored coefficient to 6.7×10⁻⁸. The largest remaining verification gap is that 20 of 24 primary historical model cells have not been independently re-estimated by a second implementation — stated plainly, not closed by this audit. See `00_executive_readiness_assessment.md` for the full, qualified answer on draft-vs-submission readiness.
