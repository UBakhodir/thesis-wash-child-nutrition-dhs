# Executive readiness assessment (2026-10-07)

> **Partially superseded (2026-10-07, later the same day).** §2 and §5's independent-reproduction count ("exactly two things") is out of date. See `07_update_2026-10-07_pass2.md`: all 24 primary historical model cells are now independently reproduced, the spatial-extraction data layer is independently verified, and one literature overclaim (Donohue et al. 2023) is corrected in `manuscript/v4_2026-10-07/`. Everything else in this file is unaffected.

Independent audit of commit `5da82cf` (branch `main`, confirmed equal to `origin/main`). Full evidence in `02_audit_checklist_and_evidence_log.md`; full issue list in `03_issue_register.md`; authority map in `01_repository_authority_map.md`.

## 1. What was actually inspected

This audit combined (a) fresh code-level reads performed in this pass — `scripts/dhs_harmonization/01_wash_mapping.py`, `02_load_flag_anthro.py`, `05_pool_countries.py`, `06_ge_linkage.py`, `08_hr_cluster_wash_exposure.py`, `14_household_community_wash_models.py` (targeted sections), `outputs/household_community_wash/01_development_sample_flow.csv`, the full manuscript's citation and language sweep, and the diagnostic build logs — with (b) genuinely-performed, artifact-backed work from earlier in this same project history (the independent pooled-model reconstruction, the Ethiopia C1 invalidity finding, the baseline numerical reconciliation, the citation-map source re-reads). Every "carried forward" item in the evidence log is traceable to a specific file or command, not to a prior report's narrative alone. Items not inspected at all, in any session, are listed explicitly in the evidence log's closing section and repeated in §5 below.

## 2. What was independently reproduced

Exactly two things in this project have been reproduced by a second, differently-implemented calculation, and only these two should be described as "independently verified" in the strong sense:

1. **The pooled established-date water-HAZ historical model** (the thesis's single most-cited historical result): rebuilt from the analysis-candidates stage (not the stored model dataset) and estimated with `linearmodels.PanelOLS`, a different library from the project's hand-written estimator. Matches the stored coefficient to 6.7×10⁻⁸ and its SE to 3.6×10⁻⁵, with N, G, K, rank, and residual exposure SD all exact. The unweighted counterpart also matches.
2. **The leave-one-out community WASH exposure construction**, verified by a brute-force, non-vectorized per-household recomputation built into the pipeline itself (`08_hr_cluster_wash_exposure.py`), on the three largest clusters per country.

Everything else described as "verified" in this project rests on **internal self-consistency checks** (programmatic `RuntimeError` assertions on scaling, merge cardinality, duplicate keys, N reconciliation against a prior audit) rather than a second independent implementation. This is good evidence — these checks would have halted the pipeline on the specific failure modes they test for — but it is a different, weaker standard than full independent reproduction, and this report does not conflate the two.

## 3. What errors were found

Eleven confirmed errors (issue register IDs A-01 through A-11), **all resolved** as of this audit. All eleven were in manuscript prose, stale documentation, or a verification script's first draft (caught before being relied upon) — **none was in a stored, reported empirical coefficient**. The most consequential were: Ethiopia candidate C1 using an already-known-invalid date-conversion method (now excluded), a false claim that wealth is absorbed by cluster fixed effects in the baseline model (it is included and estimated — corrected), and three manuscript passages that overstated or imprecisely characterised methodology or cited literature (spatial-assignment wording, trial-arm attribution, Headey and Palloni's actual finding) — all corrected with direct source verification.

## 4. Did any correction change results or conclusions?

**No.** Every correction found and fixed in this project's history (including this audit) was to language, documentation, or a pre-release script — not to a stored coefficient, standard error, sample count, or inference result. This claim is checkable: `claim_evidence_ledger.md` in the manuscript records that numeric sections were re-diffed against the prior version after every manuscript correction pass, and no diff touched a number.

## 5. What remains unverified, and why

- **20 of the 24 primary historical model cells** have no independent second-implementation check — only internal design checks. Not closed because doing so for all 20 would mean estimating each a second time, which the audit's own instructions caution against doing reflexively; this is recorded as the single largest remaining verification gap (issue B-05), not glossed over.
- **DHS biomarker/anthropometry weight documentation** remains unresolved after genuine, repeated attempts at the DHS-8 Biomarker Manual and alternative sources (issue B-03) — an external documentation gap, not something more effort on this project's part can close.
- **Nigeria 2018's measured-count gap** (12,806 official vs. 11,704 extract) remains an open, disclosed, unverified hypothesis (issue B-02).
- **IPUMS idhs_00002's structural validation and the IHME raster inventory** were not re-read in this specific audit pass; they rest on earlier-session validation that was not re-executed now.
- **The AEQD spatial-extraction geometry code itself** has never been independently re-implemented by a second method in any session — only its outputs' coverage/validity checks have been inspected.
- **17 of 20 cited literature sources** have bibliographic identity verified (author/title/DOI) but their specific claims as used in this manuscript were not re-read against the full source text.

## 6. Limitations that remain even after every technical check passes

These are not fixable by more engineering: DHS/IHME input overlap for Ghana and Kenya (the exposure surface partly reflects the same survey being analysed); current residence used as a proxy for historical residence (no migration history available); confidentiality-driven coordinate displacement (the true cluster location is never recovered, under any extraction method); the historical extension's cross-sectional-with-a-time-dimension design does not establish causation; and the baseline's four-country sample is not representative of Sub-Saharan Africa. All are disclosed explicitly in the canonical manuscript, not held back for this audit alone to state.

## 7. Are local files and GitHub synchronised?

Yes, confirmed this audit via a safe fetch: local `HEAD` and `origin/main` are both `5da82cf88bd41fe2bf5ef3154a87527afc2ad4c8`. Only one untracked item exists, `outputs/supervisor_meeting/` (the confidential supervisor presentation), which has been correctly and consistently excluded from every commit across this project's history.

## 8. Authoritative manuscript and empirical paths

- **Manuscript**: `manuscript/v3_2026-10-07/README.md` (entry point) → `MASTER_ASSEMBLY.md` (assembly spec and build instructions).
- **Empirical reporting package**: `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md`.
- **This audit**: `docs/provenance/independent_audit_v1_2026-10-07/` (this directory).

No competing current-authority claim was found anywhere in the repository (full detail in `01_repository_authority_map.md`).

## 9. Is the package ready for a complete thesis draft PDF?

**Yes**, in the sense the task defines: chapter prose is substantive and internally consistent, numerical claims trace to authoritative files, citations resolve, and an actual compiling PDF exists with a verified 31-page main text against the 40-page limit. This is a demonstrated, not asserted, readiness.

## 10. What still separates it from final submission

Front matter the author alone can supply (exact submission date, handwritten signature — both correctly left blank, not invented); the five open, disclosed evidence gaps in §5; the 38 cosmetic LaTeX overfull-box warnings; a final line-by-line prose pass after any further edits; and — stated because it bears directly on whether this package should be treated as finished — the supervisor has not yet seen the introduction or literature review, and no feedback has been incorporated. **This audit does not conclude the project is error-free or fully independently verified; it concludes that every check actually performed passed, that eleven real errors were found and fixed, and that the specific remaining gaps are named rather than hidden.**
