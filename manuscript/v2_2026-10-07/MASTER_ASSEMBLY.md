# Master assembly specification — manuscript v2 (2026-10-07, correction pass)

Supersedes `v1_2026-10-07/MASTER_ASSEMBLY.md`. v1 is preserved unchanged; see `v1_2026-10-07/POINTER_TO_V2.md` for the pointer. This file is the current authority for assembling the full thesis.

## Canonical v2 files and document order

| Order | File | Status |
|---|---|---|
| — | `08_abstract.md` | Complete (placed first in the assembled document, written last in drafting order) |
| 1 | `01_introduction.md` | Complete, corrected |
| 2 | `02_literature_review.md` | Complete, substantially corrected |
| 3 | `03_data_and_variables.md` | Complete, lightly corrected |
| 4 | `04_empirical_strategy.md` | Complete, unchanged from v1 (reviewed, no correction needed) |
| 5 | `05_results.md` | Complete, lightly corrected |
| 6 | `06_discussion_and_limitations.md` | Complete, substantially corrected |
| 7 | `07_conclusion.md` | Complete, lightly corrected |
| App. A | `appendices/A_variable_definitions_and_sample_flow.md` | Complete, citation syntax only |
| App. B | `appendices/B_model_specifications_and_independent_verification.md` | Complete, unchanged from v1 |
| App. C | `appendices/C_historical_diagnostics_and_ethiopia.md` | Complete, unchanged from v1 |
| — | `bibliography.bib` | Complete, unchanged content from v1 (24 entries) |

Do not rely on heading text alone to resolve in-text "Section X.Y" references; use `CROSS_REFERENCE_MAP.md` for stable labels, and update that map in the same edit that changes section structure.

## Citation processing: the rendering workflow this package assumes

All in-text citations use **pandoc Markdown citation syntax** referencing `bibliography.bib`:
- Parenthetical, one or more sources: `[@key]` or `[@key1; @key2]`, optionally with a locator: `[@key, p. 5]`.
- Narrative, author already named in the prose: `Author [-@key]` (suppresses the duplicate author name, renders only the year).
- No bare `@key` with no brackets and no suppression dash is used anywhere in this package; every citation was checked for this in `citation_map.md`.

**To render:** run `pandoc` with `--citeproc` (or `pandoc-citeproc` for older pandoc versions), passing `--bibliography=bibliography.bib` and a citation style file (`--csl=<style>.csl`; no specific style is mandated here — see `AUTHOR_CHECKLIST.md` for the open question of whether the department requires one). By default, pandoc-citeproc renders a reference list containing **only the keys actually cited** in the processed document — this is why the six uncited reserve entries in `bibliography.bib` (listed in `citation_map.md`) do not need to be manually excluded; do not add a `nocite: '@*'` metadata field, which would force all 26 entries to render regardless of citation.

**Validation already performed** (programmatic, this pass): every citation key used in the chapter text exists in `bibliography.bib` (20 of 26 keys used); no duplicate keys in the bibliography; no bare, unresolved `@key` citation syntax remains. Re-run this check after any future edit that adds a citation:
```
python -c "import re,glob; bib=open('bibliography.bib',encoding='utf-8').read(); keys=re.findall(r'@\w+\{([A-Za-z0-9]+),',bib); used=set(); [used.update(re.findall(r'@([A-Za-z0-9]+)',open(f,encoding='utf-8').read())) for f in glob.glob('0*.md')+glob.glob('appendices/*.md')]; print('missing:', used-set(keys))"
```

## Authoritative tables and figures

Unchanged from v1: every table in the chapter text is reused directly from the stored, validated output files indexed in `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and `02_core_reporting_table.md`. `claim_evidence_ledger.md` traces each one; this pass re-confirmed (by diff) that no number changed from v1 to v2. No figures have been generated yet.

## What is not yet in this package (missing front-matter and formatting inputs)

Unchanged from v1, see `AUTHOR_CHECKLIST.md` for the full list: university formatting requirements, title page, declaration of authorship, acknowledgements, submission date, and confirmation of citation style. **New in v2**: the title-change discussion has been removed from chapter prose entirely (it previously appeared in `01_introduction.md` §1.8 in v1) and now lives only in `AUTHOR_CHECKLIST.md`, where it is marked as a decision for author/supervisor review, not a verified fact about the thesis's registration.

## Draft-build readiness vs. submission readiness

**Ready for a draft build**: yes. Every chapter has substantive, internally consistent prose; every citation key resolves; every numerical claim traces to an authoritative file; the pandoc + citeproc workflow above is sufficient to produce a readable PDF or Word draft with working citations, given a bibliography style file.

**Not ready for submission**: front matter (title page, declaration, acknowledgements, submission date) does not exist and must not be generated without author-supplied content (`AUTHOR_CHECKLIST.md`); university formatting requirements are unconfirmed; the quality-review pass noted in `AUTHOR_CHECKLIST.md` should be re-run once more immediately before a submission build, after any further edits.

## How a later generator should assemble this

1. Concatenate the canonical files in the order above.
2. Run pandoc with `--citeproc --bibliography=bibliography.bib` and a chosen CSL style.
3. Resolve in-text "Section X.Y" prose references using `CROSS_REFERENCE_MAP.md`.
4. Do not alter any numerical claim without re-deriving it from `claim_evidence_ledger.md`'s source file.
5. Insert front matter only from author-supplied material; never generate it.
6. Do not introduce an uncited bibliography entry into the rendered reference list via `nocite`.

## Files that must not be used as manuscript sources (superseded or non-editable)

Unchanged from v1 (see that file for the full list and reasoning): `outputs/supervisor_development/18`–`26`; `writing/thesis.tex` and `thesis/chapters/` (master folder, outside this repository); `docs/provenance/final_empirical_package_v1_2026-10-07/` and `v2_2026-10-07/` for any numeric claim (superseded by `v3`). **Added in this pass**: `manuscript/v1_2026-10-07/` itself is superseded as a manuscript source by `manuscript/v2_2026-10-07/` (this folder) for the corrections listed in `CORRECTION_LOG.md`; v1 remains preserved and readable, with a pointer to v2 at its own top level.

## Empirical package used

`docs/provenance/final_empirical_package_v3_2026-10-07/`, unchanged from v1 — no new estimation was performed in this correction pass.
