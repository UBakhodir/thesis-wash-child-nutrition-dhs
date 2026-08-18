# Audit and Provenance Guide

A short index to the files in this folder. It does not add new findings — it only orients you to what is already recorded in each file below.

| File | Type | What it documents |
|---|---|---|
| `step11_bug_provenance_note.txt` | Historical issue | An early execution of the main regression script (`11_main_regressions.py`) omitted the two primary exposure variables from the design matrix. This is the standing record of that bug: what happened, and that it was caught and corrected before any result was ever reported. |
| `prefreeze_remediation_report.txt` | Remediation | A later, separate stage that fixed a build dependency gap, added a permanent defensive check to `11_main_regressions.py` guarding against recurrence of the bug above, and independently re-verified one sparsity diagnostic claim. Confirms (via before/after checksums) that none of this changed any analytical result. |
| `kenya_zero_event_region_verification.txt` | Verification | Independent read-only re-computation confirming a specific sparsity statistic (zero-event fixed-effect regions) that justifies running one robustness family pooled-only rather than country-specific. |
| `literacy_specification_decision.txt` | Documentation decision | Records that the `literacy` control variable's presence in the regressions was not traceable to the original design documentation, the resulting provenance investigation, and the explicit decision to retain it as-implemented rather than remove it and re-estimate the (by then already-known) results. Corresponding updates were made to `docs/thesis_design.md` and `docs/data_dictionary.md`. |
| `step13_final_audit.csv` / `step13_final_audit_summary.txt` | Final freeze status | The automated 24-point integrity check the final-output script runs on every table before writing it (shape locks, duplicate checks, cross-file coefficient consistency, etc.), and a plain-language summary of the result. |

**How to read this folder:** these five records are presented in full, not summarized away, because the project's standing practice is to document issues transparently rather than hide them. None of them indicates an unresolved problem with the results in this package — each one documents either a caught-and-fixed historical issue, an independent verification, or a documentation decision, with an explicit confirmation in every case that no regression coefficient, table, or figure was altered as a result.
