# Manuscript source package v12 (2026-10-10) — independent-audit correction pass

Supersedes `manuscript/v11_2026-10-09/` as the canonical manuscript source. v1 through v11 are preserved unchanged; see each version's own pointer file. This is the **single current entry point**.

This pass resolves an external, independent audit (`Independent_Thesis_Audit_2026-10-10.md`) of commit `ceec506` (the v11 manuscript). The audit's 18 findings (R01–R18) were each independently investigated against the actual code and authoritative output files — none was accepted on the audit's say-so alone — and are fully documented in `docs/provenance/independent_audit_resolution_v1_2026-10-10.md`. Full before/after detail: `CORRECTION_LOG.md`.

## What this pass found and corrected

**A genuine, confirmed numerical transcription error**: `05_results.md`'s joint household/community table (§5.3) displayed six wrong confidence-interval bounds for the WAZ and WHZ rows — the coefficients and p-values were already correct, only the CI bounds were wrong. Corrected against the authoritative CSV, matched by outcome and term, not by finding a similar-looking number elsewhere (R01).

**A confirmed code-level defect, now fixed and verified against all 291 published models**: the historical estimator (`16_estimate_preliminary.py`) could, in principle, mislabel another variable's coefficient as the exposure's own if the exposure were absorbed by the cluster fixed effect in a specific way (varying between clusters but constant within each one) that its own pre-check does not catch, and could silently return a pseudoinverse-based estimate for a rank-deficient design rather than flagging non-identifiability. Both are now checked explicitly, with four targeted tests confirming the fix. **A full re-run against the actual restricted inputs confirms all 291 published model rows are numerically identical (to the last reported digit) to the original stored output — no published result was affected** (R05; detail in Appendix B §B.4).

**Confirmed methods-description errors, corrected to match the implemented code precisely**: the baseline pipeline's inference actually uses a normal reference distribution, not Student's *t*(*G*−1) as previously stated for "both samples" (confirmed by independent recomputation matching the stored p-value to >10 decimal places); the baseline pipeline has no singleton-cluster exclusion step, contrary to a previous claim that it mirrors the historical pipeline's explicit filter; the reported equations omitted that water and sanitation are always entered together, mutually adjusted, in every baseline specification; and the historical model's second continuous age-related control is maternal age, not a second child-age variable (R02–R04, R09).

**Confirmed interpretation and wording issues, corrected**: significance language now specifies the 5% threshold consistently and no longer describes the historical extension's selected pooled headline as its only significant result (it is one of six, Section 5.6); the pooled-estimand description in the Discussion no longer reintroduces the "arithmetic average of country coefficients" framing that Methods §4.5 explicitly disclaims; the wealth-adjustment sensitivity (§5.8) is no longer described as establishing a mediator mechanism; model-family counts in §5.7 now reconcile exactly against the 291-row register (R06–R08, R18).

**Confirmed data/measurement-description errors, corrected**: the community WASH exposure is now described precisely as implemented (an unweighted leave-one-out proportion among other *classifiable* sampled HR households, not a census of the geographical community); "Births Recode (KR)" corrected to "Children's Recode (KR)" (DHS's Births Recode, BR, is a different, unused file); the primary spatial buffer radii (2 km urban, 5 km rural) are now stated explicitly rather than left to be inferred (R11–R13).

**Confirmed literature-source errors, corrected against primary sources directly (not the audit's say-so)**: Addae et al. (2024) is a Ghana 2017/18 MICS study, confirmed directly from the publisher's own text, not a DHS study — reclassified throughout, with "most recent national survey" replaced by the named dataset; the opening paragraph's "well established and not disputed" biological-mechanism claim, checked directly against its own cited source, overstated that source's own more hedged framing of three separately-evidenced pathways of varying strength — corrected (R14–R15).

**Confirmed handover/documentation gaps, corrected**: the assembly instructions referred to build files that exist only under `../v6_2026-10-07/build/`, not under this version, creating an internal contradiction with the file's own later statement that no v7–v11 build exists — corrected with the exact procedure a future build should follow; the root README's reproduction instructions did not document the historical pipeline's two different path conventions (absolute master-directory paths vs. working-directory-relative paths) or their different working-directory requirements — added; `scipy`, `pyproj`, and `Pillow`, imported directly by several historical scripts, were missing from `requirements.txt` — added (R16–R17).

## What this pass checked and found already correct, or chose not to change

The audit's remaining recommendations (Section 3 of its own report) were reviewed; none required a correction beyond what is listed above, and this pass did not add unsupported claims or new analyses to make the manuscript appear more sophisticated. Household/community exposure as a coherent economic distinction, region/cluster-FE identification logic, and the baseline/historical non-comparability for exposure timing were all re-confirmed accurate and left unchanged, consistent with the audit's own "findings that passed" section.

## Canonical files and reading order

Unchanged from v11 except `01_introduction.md`, `02_literature_review.md`, `03_data_and_variables.md`, `04_empirical_strategy.md`, `05_results.md`, `06_discussion_and_limitations.md`, `07_conclusion.md`, `08_abstract.md`, `appendices/A_variable_definitions_and_sample_flow.md`, `appendices/B_model_specifications_and_independent_verification.md`, and `appendices/C_historical_diagnostics_and_ethiopia.md` (all corrected as above; see `MASTER_ASSEMBLY.md` for the per-file detail).

## Build

**No PDF was generated, compiled, rebuilt, or rendered in this pass** — explicitly not authorized for this task. The existing `../v6_2026-10-07/build/main.pdf` reflects none of v7's through v12's corrections. `MASTER_ASSEMBLY.md` now states precisely which build artifacts exist, where, and the procedure a future build should follow (R16).

## Supervisor-feedback status — unchanged, still accurate

The introduction and literature review are drafted and internally reviewed; nothing has been sent to the supervisor; no feedback has been received. See `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md`.

## Source readiness vs. submission readiness

**Source-complete and internally consistent**: yes, to the standard this and the prior passes could establish — including, this pass, an external independent audit whose findings were each investigated and, where confirmed, corrected with traceable evidence. This is not a claim that every conceivable error has been eliminated from a thesis of this scope.
**Not ready for submission**: a PDF has not been built from this version; the exact submission date and handwritten signature are not yet available; the next stage (a separately authorized complete draft PDF build and page-by-page review) has not begun.

## Files that must not be used as manuscript sources (superseded or non-editable)

All items superseded in v1–v11 remain superseded, plus `manuscript/v11_2026-10-09/` itself for the items in `CORRECTION_LOG.md`.
