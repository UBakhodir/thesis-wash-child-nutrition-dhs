# Chapter source locations

At set-up (2026-10-13) this folder was empty. Since the Chapter 1 session (2026-10-13): `ch01` has been
prepared, language-edited, converted and previewed, and is **awaiting author review** (not in
`APPROVED.tsv`). The edit record is in `changes/` (`01_introduction.changelog.md`, word diff).
On 2026-10-14 the author's decision to carry `ch01` forward after review was recorded in
`APPROVED.tsv` (not supervisor or final-submission approval). Since the Chapter 2 session
(2026-10-14): `ch02` has been prepared, language-edited, converted and previewed, and is **awaiting
author review** (not in `APPROVED.tsv`); edit record `changes/02_literature_review.changelog.md`
and word diff. In the Chapter 3 session the author's review of `ch02` was recorded: a §2.4 correction is
required at final assembly (`../FINAL_ASSEMBLY_REGISTER.md` FA-1), so `ch02` is not finalised. Since the
Chapter 3 session (2026-10-14): `ch03` has been prepared, language-edited, converted and previewed, and is
**awaiting author review** (not in `APPROVED.tsv`); edit record `changes/03_data_and_variables.changelog.md`
and word diff. In the Chapter 4 session the author's decisions on `ch03` were recorded: a §3.9
cross-reference correction is required at final assembly and the `hv001`/`v021` question stays open
(`../FINAL_ASSEMBLY_REGISTER.md` FA-7). Since the Chapter 4 session (2026-10-14): `ch04` has been
prepared, language-edited, converted and previewed, and is **awaiting author review** (not in
`APPROVED.tsv`); edit record `changes/04_empirical_strategy.changelog.md` and word diff; points for
the author in FA-8. In the Chapter 5 session the author reclassified the four `ch04` points as
required final-assembly corrections (FA-8; not applied). Since the Chapter 5 session
(2026-10-14): `ch05` has been prepared, verified against the stored outputs, language-edited,
converted and previewed, and is **awaiting author review** (not in `APPROVED.tsv`); edit record
`changes/05_results.changelog.md` and word diff; points for the author in FA-9. Since the Chapter 6
session (2026-10-14): `ch06` has been prepared, verified against the stored outputs, language-edited,
converted and previewed, and is **awaiting author review** (not in `APPROVED.tsv`); edit record
`changes/06_discussion_and_limitations.changelog.md` and word diff; points for the author in FA-14. Since the Chapter 7 session: `ch07` previewed, awaiting author review (FA-16). Since the abstract
session (2026-10-14): `abstract` has been prepared, verified against the stored outputs, language-edited,
converted and previewed, and is **awaiting author review** (not in `APPROVED.tsv`); edit record
`changes/08_abstract.changelog.md` and word diff; points for the author in FA-17. The abstract is an
unnumbered unit, not a chapter; `08_` is a filename prefix only.

- `md/` — publishing copies of the canonical Markdown, created only by
  `python scripts/build.py prepare <unit>` (byte-identical copy; never overwritten).
  `md/PROVENANCE.tsv` records the canonical hash and commit at copy time. Approved language
  polishing, if any, is applied here and nowhere else; the canonical `manuscript/v12_2026-10-10/`
  files stay untouched.
- `tex/` — LaTeX generated from `md/` by `convert`/`preview`. Each file begins with a comment
  recording the md hash, canonical hash and filter hash. Regenerate rather than hand-edit; if a
  hand-edit is ever unavoidable, record it in `../HANDOVER.md` and re-approve the unit.
- `APPROVED.tsv` — one line per unit after the author has reviewed its preview:
  `unit<TAB>tex_sha256<TAB>approved_by<TAB>approved_utc<TAB>note`.

| Unit | Canonical source | Generated LaTeX |
|---|---|---|
| abstract | `08_abstract.md` | `tex/08_abstract.tex` |
| ch01 | `01_introduction.md` | `tex/01_introduction.tex` |
| ch02 | `02_literature_review.md` | `tex/02_literature_review.tex` |
| ch03 | `03_data_and_variables.md` | `tex/03_data_and_variables.tex` |
| ch04 | `04_empirical_strategy.md` | `tex/04_empirical_strategy.tex` |
| ch05 | `05_results.md` | `tex/05_results.tex` |
| ch06 | `06_discussion_and_limitations.md` | `tex/06_discussion_and_limitations.tex` |
| ch07 | `07_conclusion.md` | `tex/07_conclusion.tex` |
| appA | `appendices/A_variable_definitions_and_sample_flow.md` | `tex/A_variable_definitions_and_sample_flow.tex` |
| appB | `appendices/B_model_specifications_and_independent_verification.md` | `tex/B_model_specifications_and_independent_verification.tex` |
| appC | `appendices/C_historical_diagnostics_and_ethiopia.md` | `tex/C_historical_diagnostics_and_ethiopia.tex` |
