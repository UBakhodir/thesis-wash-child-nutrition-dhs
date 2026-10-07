# Remaining actions (2026-10-07)

Consolidated from the issue register (`03_issue_register.md`, Class 2 items) and the audit evidence log's "not verified" list. Ordered by who can act on them.

## Actions only the author/supervisor can take

1. Send `manuscript/v3_2026-10-07/01_introduction.md` and `02_literature_review.md` to the supervisor and obtain feedback — nothing has been sent to date (`historical_wash_supervisor_request_status_v1_2026-10-07.md`).
2. Decide whether to pursue direct contact with DHS/IPUMS or the Bonn library/department for the measurement-subsample weight documentation (issue B-03) — this project has exhausted the locally/remotely accessible sources it can reach on its own.
3. Read the full IHME Free-of-Charge Non-Commercial User Agreement directly on the GHDx download page (issue B-04); the agreement's existence and general scope are confirmed, its complete text is not.
4. Confirm whether a specific CSL/citation-style file is required by the department beyond the recommended Chicago author-date already implemented.
5. Supply the exact submission date and handwritten signature at actual submission time (cannot be done earlier).

## Actions a future work session could take, time budget permitting

6. Independently re-estimate (second implementation) a larger sample of the 20 not-yet-independently-checked historical primary cells, beyond the pooled water-HAZ headline (issue B-05). Not done this audit because the audit's own instructions caution against reflexive re-estimation; recommended only if a specific cell's number is going to be prominently cited or if time allows a broader pass.
7. Re-read `scripts/historical_wash/03_import_validate_idhs_00002.py` and `01_inventory_ihme_rasters.py` fresh, rather than relying on an earlier session's validation record, if the IPUMS extract or IHME rasters are ever re-pulled or modified.
8. Independently re-implement the AEQD spatial-extraction geometry (exact disk-pixel overlap) in a second, differently-written script, as was done for the pooled estimation model — the strongest remaining gap in the historical pipeline's independent verification.
9. Re-read the remaining 17 of 20 cited literature sources' full text against the specific claims made about them (currently bibliographic-identity-only verification), if the literature review is expanded.
10. Clean up the 38 cosmetic LaTeX overfull-box warnings (long file paths not wrapping) before a final submission build.

## Not recommended

- Re-running the baseline pipeline (00–14) or the full historical pipeline (01–19) "to be sure" — no evidence from this audit suggests any stored coefficient is wrong, and the pipeline's own extensive self-validation (merge-cardinality asserts, scaling asserts, brute-force leave-one-out checks, N-reconciliation-against-prior-audit asserts) would have halted on the specific failure modes this audit was asked to check for. Rerunning without a concrete, named reason would not be independent verification — it would be the same code producing the same answer.
