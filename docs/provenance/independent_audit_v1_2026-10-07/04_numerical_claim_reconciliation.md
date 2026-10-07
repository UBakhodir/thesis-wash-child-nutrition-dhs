# Numerical claim reconciliation (2026-10-07)

This audit's own fresh numerical checks (full detail and sourcing in `02_audit_checklist_and_evidence_log.md`):

| Claim | Source re-read this audit | Result |
|---|---|---|
| Baseline sample-flow reconciliation (country sub-samples sum to common sample) | `outputs/household_community_wash/01_development_sample_flow.csv` | Confirmed exactly for HAZ (36,040), WAZ (36,308), WHZ (36,145) |
| Household water/sanitation binary construction reuses validated earlier-step function, self-checks against prior audit's N | `scripts/dhs_harmonization/14_household_community_wash_models.py:117–156` | Confirmed — hard `RuntimeError` STOP on any mismatch |
| No "proves no effect" / "proof of no" language anywhere in the manuscript | Full-text grep, `manuscript/v3_2026-10-07/*.md` | Zero matches |
| DF-convention labelling consistent everywhere the sensitivity p-values are cited | Full-text grep + read, `04_empirical_strategy.md`, `Appendix B` | Confirmed — every .080/.574 citation is labelled FULL_DUMMY_DF |
| Established-date and Ethiopia-provisional results never mixed in one table | Re-read `05_results.md` §5.6–5.9, Appendix C | Confirmed — Ethiopia appears only in §5.9 and Appendix C, both explicitly labelled |

For the complete, pre-existing numerical claim-to-source mapping covering every figure in the manuscript's Sections 1 and 5–6 (not repeated here), see `manuscript/v3_2026-10-07/claim_evidence_ledger.md`, which this audit spot-checked (the five rows above) rather than re-deriving in full — re-deriving all ~40 rows from scratch a second time was judged lower-value than the fresh code-level checks in `02_audit_checklist_and_evidence_log.md`, given this audit's time budget, and is recorded here as a scope decision, not an oversight.

**No discrepancy found in any claim checked this audit.**
