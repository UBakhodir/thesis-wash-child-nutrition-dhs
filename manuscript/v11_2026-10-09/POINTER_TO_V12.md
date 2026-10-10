# This manuscript version is superseded — see v12

`manuscript/v11_2026-10-09/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v12_2026-10-10/`**.

v12 resolves `Independent_Thesis_Audit_2026-10-10.md`, an external audit of this exact version (commit `ceec506`). The audit found and this pass corrected: six wrong confidence intervals in the joint household/community results table (§5.3); a methods-description error stating baseline inference uses Student's t(G−1) when it actually uses a normal reference distribution; a claim that baseline singleton-cluster exclusion mirrors the historical pipeline's, when the baseline pipeline has no such step; equations that omitted showing water and sanitation entered together in every baseline specification; a code-level defect in the historical estimator that could, under a specific absorption pattern, mislabel another variable's coefficient as the exposure's own (fixed, and verified against all 291 published models with zero numerical change); wrong model-family counts; inconsistent significance-threshold language; a reintroduced pooled-estimand misinterpretation in the Discussion; several naming errors (fixed effects, maternal age, KR vs. BR); an overstated description of the community WASH exposure as a full household census; unstated buffer radii; a literature-source misclassification (Addae et al. 2024 is MICS, not DHS); a biological-mechanism overclaim; and assembly/reproduction documentation gaps.

**No published historical-model coefficient, standard error, confidence interval, or p-value changed** — the one code fix was verified, by a full re-run against the actual restricted inputs, to leave all 291 stored model rows numerically identical.

Full itemised list: `../v12_2026-10-10/CORRECTION_LOG.md`; full evidence for every finding: `docs/provenance/independent_audit_resolution_v1_2026-10-10.md`.

Do not cite this version's `05_results.md` §5.3 confidence intervals, `04_empirical_strategy.md`'s inference/singleton/equation descriptions, or any of the other items above — use v12's corrected text. **No PDF has been built from v12.**
