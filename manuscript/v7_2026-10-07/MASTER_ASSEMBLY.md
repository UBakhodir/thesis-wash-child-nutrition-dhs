# Master assembly specification — manuscript v7 (2026-10-09, evidence-based correction and consistency review)

Supersedes `../v6_2026-10-07/MASTER_ASSEMBLY.md` (and, transitively, v1–v5's). v1 through v6 are preserved unchanged; see each version's own pointer file. This file is the current authority for assembling the full thesis. New in v7: substantive corrections found by direct inspection of the implemented code against the manuscript's own descriptions, not a repetition of prior audits — baseline weight/cluster/age fields were wrongly described using the historical extension's IPUMS field names (`03_data_and_variables.md` §3.2, §3.4; Appendix A); the region-FE identifying-variation description was wrong (`04_empirical_strategy.md` §4.1); a notation collision between country-count and regressor-count both using $K$ was fixed; the 1.39-vs-1.03 independent-validation narrative wrongly isolated one of two simultaneous changes; the historical spatial-geometry and exposure-window-completion descriptions overstated what AEQD and the completion rule actually guarantee; the SHINE trial's arm structure was described identically to the two WASH-Benefits trials when it is materially different; Blom2022's nutrition outcome was wrongly disclaimed, and its citation's "read" status was found to be false (no local PDF exists); household WASH was corrected from an unqualified "private good" framing to acknowledge its externality; a concrete multiplicity disclosure (5–6 of 24 cells nominally significant, not only the headline) was added. Full detail: `CORRECTION_LOG.md` (this version's) and `docs/provenance/evidence_based_correction_v1_2026-10-09.md`. **No empirical estimate, sample, weight, or reported coefficient changed** — every correction is to prose description, variable-naming accuracy, or documentation synchronization.

## Canonical files and document order

| Order | File | Status |
|---|---|---|
| — | `08_abstract.md` | Complete (placed first in the assembled document, written last in drafting order); lightly corrected in v7 (weighted/unweighted pairing added) |
| 1 | `01_introduction.md` | Complete; corrected in v7 (household-WASH externality framing) |
| 2 | `02_literature_review.md` | Complete; substantially corrected in v7 (SHINE trial arms, Blom2022 description, citation-ledger honesty) |
| 3 | `03_data_and_variables.md` | Complete; substantially corrected in v7 (baseline weight/cluster/age field names; spatial-geometry and window-completion precision) |
| 4 | `04_empirical_strategy.md` | Complete; substantially corrected in v7 (region-FE identifying variation; pooled-estimand wording and symbol collision; 1.39-vs-1.03 narrative) |
| 5 | `05_results.md` | Complete; corrected in v7 (sample-composition note in §5.2; concrete multiplicity disclosure in §5.6) |
| 6 | `06_discussion_and_limitations.md` | Complete, unchanged since v6 |
| 7 | `07_conclusion.md` | Complete; lightly corrected in v7 (weighted/unweighted pairing added) |
| App. A | `appendices/A_variable_definitions_and_sample_flow.md` | Complete; substantially corrected in v7 (baseline vs. historical variable tables now kept separate) |
| App. B | `appendices/B_model_specifications_and_independent_verification.md` | Complete, unchanged since v6 |
| App. C | `appendices/C_historical_diagnostics_and_ethiopia.md` | Complete, unchanged since v1 |
| — | `bibliography.bib` | Complete (26 entries total; 20 cited; 6 uncited reserve — see `citation_map.md`; count corrected in v3, see that version's `CORRECTION_LOG.md`) |

Do not rely on heading text alone to resolve in-text "Section X.Y" references; use `CROSS_REFERENCE_MAP.md` for stable labels, and update that map in the same edit that changes section structure.

## Citation processing: the rendering workflow this package assumes

All in-text citations use **pandoc Markdown citation syntax** referencing `bibliography.bib`:
- Parenthetical, one or more sources: `[@key]` or `[@key1; @key2]`, optionally with a locator: `[@key, p. 5]`.
- Narrative, author already named in the prose: `Author [-@key]` (suppresses the duplicate author name, renders only the year).
- No bare `@key` with no brackets and no suppression dash is used anywhere in this package; every citation was checked for this in `citation_map.md`.

**To render — two supported paths:**

1. **pandoc + citeproc** (recommended for a future generator producing Word or a different LaTeX structure from this one): run `pandoc` with `--citeproc`, passing `--bibliography=bibliography.bib` and a citation style file (`--csl=<style>.csl`). By default, pandoc-citeproc renders a reference list containing only the keys actually cited — the six uncited reserve entries in `bibliography.bib` do not need manual exclusion; do not add a `nocite: '@*'` metadata field. **Not verified in this environment**: pandoc is not installed here (`which pandoc` / `Get-Command pandoc` both fail), so this path is documented but untested by this project; a future session with pandoc available should verify it before relying on it.
2. **xelatex + biblatex/biber** (used for this pass's actual diagnostic build, `build/`, and consistent with the university guidelines' own named toolchain for Chicago-style references, "available in Zotero and BibLaTeX"): a small converter, `build/md2tex.py`, turns the `.md` chapters into `.tex`, and `[@key]`/`Author [-@key]` syntax maps to biblatex's `\parencite{key}`/`Author (\citeyear{key})`. This path **was run and verified** this pass: biber found and resolved all 20 cited keys with 0 errors (`build/build_biber.log`). This is the currently working path; use it unless/until pandoc is confirmed available.

By default, biblatex also renders a reference list containing only the keys actually cited in the document (the six uncited reserve entries in `bibliography.bib` are correctly absent from `build/main.pdf`'s reference list — confirmed by inspection).

**Validation already performed** (programmatic, this pass): every citation key used in the chapter text exists in `bibliography.bib` (20 of 26 keys used); no duplicate keys in the bibliography; no bare, unresolved `@key` citation syntax remains. Re-run this check after any future edit that adds a citation:
```
python -c "import re,glob; bib=open('bibliography.bib',encoding='utf-8').read(); keys=re.findall(r'@\w+\{([A-Za-z0-9]+),',bib); used=set(); [used.update(re.findall(r'@([A-Za-z0-9]+)',open(f,encoding='utf-8').read())) for f in glob.glob('0*.md')+glob.glob('appendices/*.md')]; print('missing:', used-set(keys))"
```

## Authoritative tables and figures

Unchanged from v1: every table in the chapter text is reused directly from the stored, validated output files indexed in `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and `02_core_reporting_table.md`. `claim_evidence_ledger.md` traces each one; this pass re-confirmed (by diff) that no number changed from v1 to v2. No figures have been generated yet.

## What is now resolved, and what is still not in this package

**Resolved in v3**: university formatting requirements are now known in full (`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`, supplied by the author) and implemented exactly in `build/preamble.tex`; the registered title, supervisor (Juniorprof. Julia Mink, Ph.D.), submission deadline (22 October 2026), author name, and matriculation number are confirmed from the author's registration confirmation email and used in `build/titlepage.tex`; citation style is resolved as Chicago author-date via biblatex (the guidelines' own named option), implemented and verified in `build/`.

**Still not in this package, and not invented**: the actual submission date (the 22 October 2026 deadline is not necessarily the submission date), the handwritten signature on the declaration, and acknowledgements (which the guidelines state must **not** be included, resolving that open question from v1/v2 as "omit entirely," not "author's choice"). See `AUTHOR_CHECKLIST.md`.

## Draft-build readiness vs. submission readiness

**Ready for a draft build**: the v6 diagnostic PDF (`../v6_2026-10-07/build/main.pdf`) is an actual compiling PDF under the exact university formatting specification, with a verified 32-page main text (40-page limit), 0 LaTeX errors, and all 20 cited keys resolving. Its rendered-page verification checked a justified, non-exhaustive sample of pages by direct visual rendering — specifically, both pages previously reported as clipped plus their immediate neighbours (PDF pages 26–28, 39–46 of 48) — not every page in the document; `../v6_2026-10-07/build/README.md` states exactly which pages were checked. **This v7 pass made source-only corrections and explicitly did not rebuild, regenerate, or re-render any PDF** (per this task's own boundary), so no v7 PDF or page-count claim exists yet; the v6 PDF does not reflect this pass's prose corrections.

**Not ready for submission**: the actual submission date and a handwritten signature cannot be filled in before the thesis is finished and printed; the v6 build had 28 remaining cosmetic overfull-text-box warnings (long file paths and a few dense new paragraphs not breaking across lines; see `../v6_2026-10-07/build/README.md` for the exact count and why it dropped from the v5 build's 38), none of which were found to clip any content on visual inspection; the quality-review pass noted in `AUTHOR_CHECKLIST.md` should be re-run once more immediately before a submission build, after any further edits, and a v7 PDF should be built and its page count and rendered pages freshly verified before relying on it. No claim of supervisor approval or university acceptance is made anywhere in this package.

## How a later generator should assemble this

1. Concatenate the canonical files in the order above (or use `build/main.tex`'s `\input` sequence directly, which already does this).
2. Render via xelatex + biblatex/biber (verified working this pass, `build/`) or pandoc + citeproc (documented but not verified in this environment — confirm pandoc is installed first).
3. Resolve in-text "Section X.Y" prose references using `CROSS_REFERENCE_MAP.md`.
4. Do not alter any numerical claim without re-deriving it from `claim_evidence_ledger.md`'s source file.
5. Insert remaining front matter (submission date, signature) only from author-supplied material at the time of actual submission; never generate it. The title page and declaration are already implemented in `build/titlepage.tex` and `build/declaration.tex` with confirmed metadata and correctly blank signature/date fields.
6. Do not introduce an uncited bibliography entry into the rendered reference list via `nocite`.

## Files that must not be used as manuscript sources (superseded or non-editable)

Unchanged from v1/v2 (see those files for the full list and reasoning): `outputs/supervisor_development/18`–`26`; `writing/thesis.tex` and `thesis/chapters/` (master folder, outside this repository); `docs/provenance/final_empirical_package_v1_2026-10-07/` and `v2_2026-10-07/` for any numeric claim (superseded by `v3`, the current empirical package, itself unchanged since v1 of the manuscript). `manuscript/v1_2026-10-07/` through `v6_2026-10-07/` are each superseded as a manuscript source by the next version in sequence, down to this file's own `manuscript/v7_2026-10-07/` (this folder), the current canonical source; all six are preserved and readable, each with a pointer to the next version at its own top level.

## Empirical package used

`docs/provenance/final_empirical_package_v3_2026-10-07/`, unchanged from v1 and v2 — no new estimation was performed in this correction pass.
