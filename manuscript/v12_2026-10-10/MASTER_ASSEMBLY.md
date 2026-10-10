# Master assembly specification — manuscript v12 (2026-10-10, independent-audit correction pass)

Supersedes `../v11_2026-10-09/MASTER_ASSEMBLY.md` (and, transitively, v1–v10's). v1 through v11 are preserved unchanged; see each version's own pointer file. This file is the current authority for assembling the full thesis. New in v12: resolves `Independent_Thesis_Audit_2026-10-10.md`, an external audit of commit `ceec506`. Full detail: `CORRECTION_LOG.md` (this version's) and `docs/provenance/independent_audit_resolution_v1_2026-10-10.md` (the complete R01–R18 resolution register). **No empirical estimate, sample, weight actually used in any model, control set, or published historical-model coefficient/SE/CI/p-value changed** — one code-level defensive safeguard was added to the historical estimator and verified, by a full re-run against the actual restricted inputs, to leave all 291 stored model rows numerically identical (see `appendices/B_model_specifications_and_independent_verification.md` §B.4 and the resolution register).

## Canonical files and document order

| Order | File | Status |
|---|---|---|
| — | `08_abstract.md` | Complete; corrected in v12 (significance-threshold wording, community-association scoping — R07) |
| 1 | `01_introduction.md` | Complete; corrected in v12 (biological-mechanism overclaim R15; Addae/MICS classification R14; significance-threshold and community-association scoping R07) |
| 2 | `02_literature_review.md` | Complete; corrected in v12 (biological-mechanism framing R15; Addae/MICS dataset identity, Günther–Fink/Spears outcome-scoping R14) |
| 3 | `03_data_and_variables.md` | Complete; corrected in v12 (community-exposure construction description R11; KR/BR naming R12; explicit buffer radii R13) |
| 4 | `04_empirical_strategy.md` | Complete; corrected in v10 (1.39-vs-1.03 account), v11 (§4.5 weighting-formula paragraph), and v12 (inference-distribution and singleton-exclusion descriptions split by pipeline R02/R03; equations show simultaneous water/sanitation adjustment R04; maternal-age naming R09) |
| 5 | `05_results.md` | Complete; corrected in v12 (six joint-model confidence intervals R01; significance-threshold wording and inference-distribution note R02/R07; model-family count reconciliation R06; wealth-sensitivity interpretation R18) |
| 6 | `06_discussion_and_limitations.md` | Complete; corrected in v12 (fixed-effect naming, socioeconomic-control naming R09; pooled-estimand interpretation R08; "one significant result" framing R07) |
| 7 | `07_conclusion.md` | Complete; corrected in v12 (significance-threshold wording and community-association scoping R07) |
| App. A | `appendices/A_variable_definitions_and_sample_flow.md` | Complete; corrected in v12 (KR/BR naming R12) |
| App. B | `appendices/B_model_specifications_and_independent_verification.md` | Complete; corrected in v10 (§B.2) and v12 (maternal-age naming R09; §B.4 added documenting the R05 estimator-safeguard fix and its all-291-model verification) |
| App. C | `appendices/C_historical_diagnostics_and_ethiopia.md` | Complete; corrected in v12 (completion-rule contradiction and appendix-exclusivity claim R10) |
| — | `bibliography.bib` | Complete (26 entries total; 20 cited; 6 uncited reserve — see `citation_map.md`); unchanged in v12 — the independent audit's bibliography-structure check (26/20/48/0-missing) confirmed the existing count, and no literature correction in v12 required a bibliographic-metadata change |

Do not rely on heading text alone to resolve in-text "Section X.Y" references; use `CROSS_REFERENCE_MAP.md` for stable labels, and update that map in the same edit that changes section structure.

## Citation processing: the rendering workflow this package assumes

All in-text citations use **pandoc Markdown citation syntax** referencing `bibliography.bib`:
- Parenthetical, one or more sources: `[@key]` or `[@key1; @key2]`, optionally with a locator: `[@key, p. 5]`.
- Narrative, author already named in the prose: `Author [-@key]` (suppresses the duplicate author name, renders only the year).
- No bare `@key` with no brackets and no suppression dash is used anywhere in this package; every citation was checked for this in `citation_map.md`.

**To render — two supported paths, with their actual current locations stated precisely (corrected in v12; see R16):**

1. **pandoc + citeproc** (recommended for a future generator producing Word or a different LaTeX structure from this one): run `pandoc` with `--citeproc`, passing `--bibliography=bibliography.bib` and a citation style file (`--csl=<style>.csl`). By default, pandoc-citeproc renders a reference list containing only the keys actually cited — the six uncited reserve entries in `bibliography.bib` do not need manual exclusion; do not add a `nocite: '@*'` metadata field. **Not verified in this environment**: pandoc is not installed here (`which pandoc` / `Get-Command pandoc` both fail), so this path is documented but untested by this project; a future session with pandoc available should verify it before relying on it.
2. **xelatex + biblatex/biber**, consistent with the university guidelines' own named toolchain for Chicago-style references ("available in Zotero and BibLaTeX"): a converter, `md2tex.py`, and supporting templates (`preamble.tex`, `titlepage.tex`, `declaration.tex`) exist **only under `../v6_2026-10-07/build/`** — there is **no `build/` directory under this version (`v12_2026-10-10/`), nor under v7 through v11**. The v6 build's own generated chapter `.tex` files and `main.pdf` reflect v6's prose, not v7 through v12's corrections (including every correction in this pass); they must not be reused as if they contained current text. A future build of this canonical v12 source must: (a) copy or point the converter/template files from `../v6_2026-10-07/build/` to a **new** output location (e.g. a fresh `build/` under this version, not reusing v6's own generated `chapters/`/`appendices/` `.tex` output), (b) regenerate every chapter `.tex` file freshly from this version's own `.md` files via `md2tex.py`, and (c) include an explicit source-version check (e.g. recording this file's own header version string, or a hash of the canonical `.md` files, in the build log) so a reader of the resulting PDF's build log can confirm which manuscript version it was actually built from. **No such build has been run for v12** (or for v7 through v11); this is documented as the build procedure a future pass should follow, not as a claim that it has already happened.

By default, biblatex also renders a reference list containing only the keys actually cited in the document (confirmed by inspection of the v6 build, the only build that exists).

**Validation already performed** (programmatic, this pass): every citation key used in the chapter text exists in `bibliography.bib` (20 of 26 keys used); no duplicate keys in the bibliography; no bare, unresolved `@key` citation syntax remains. Re-run this check after any future edit that adds a citation:
```
python -c "import re,glob; bib=open('bibliography.bib',encoding='utf-8').read(); keys=re.findall(r'@\w+\{([A-Za-z0-9]+),',bib); used=set(); [used.update(re.findall(r'@([A-Za-z0-9]+)',open(f,encoding='utf-8').read())) for f in glob.glob('0*.md')+glob.glob('appendices/*.md')]; print('missing:', used-set(keys))"
```

## Authoritative tables and figures

Unchanged from v1: every table in the chapter text is reused directly from the stored, validated output files indexed in `docs/provenance/final_empirical_package_v3_2026-10-07/00_results_index.md` and `02_core_reporting_table.md`. `claim_evidence_ledger.md` traces each one; this pass corrected one table (05_results.md §5.3's six joint-model confidence intervals, R01) after a keyed, outcome-and-term-specific comparison against `outputs/household_community_wash/05_joint_household_community.csv` found a transcription error, and otherwise re-confirmed every other displayed figure against its authoritative source unchanged. No figures have been generated yet.

## What is now resolved, and what is still not in this package

**Resolved in v3**: university formatting requirements are now known in full (`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`, supplied by the author) and implemented exactly in `../v6_2026-10-07/build/preamble.tex`; the registered title, supervisor (Juniorprof. Julia Mink, Ph.D.), submission deadline (22 October 2026), author name, and matriculation number are confirmed from the author's registration confirmation email and used in `../v6_2026-10-07/build/titlepage.tex`; citation style is resolved as Chicago author-date via biblatex (the guidelines' own named option), implemented and verified in that v6 build.

**Still not in this package, and not invented**: the actual submission date (the 22 October 2026 deadline is not necessarily the submission date), the handwritten signature on the declaration, and acknowledgements (which the guidelines state must **not** be included, resolving that open question from v1/v2 as "omit entirely," not "author's choice"). See `AUTHOR_CHECKLIST.md`.

## Draft-build readiness vs. submission readiness

**Ready for a draft build**: the v6 diagnostic PDF (`../v6_2026-10-07/build/main.pdf`) is an actual compiling PDF under the exact university formatting specification, with a verified 32-page main text (40-page limit), 0 LaTeX errors, and all 20 cited keys resolving. Its rendered-page verification checked a justified, non-exhaustive sample of pages by direct visual rendering — specifically, both pages previously reported as clipped plus their immediate neighbours (PDF pages 26–28, 39–46 of 48) — not every page in the document; `../v6_2026-10-07/build/README.md` states exactly which pages were checked. **v7 through this v12 pass all made source-only corrections and explicitly did not rebuild, regenerate, or re-render any PDF** (per each task's own boundary), so no v7 through v12 PDF or page-count claim exists yet; the v6 PDF reflects none of these six passes' prose corrections. The next stage — a separately authorized complete draft PDF build and page-by-page review — has not begun.

**Not ready for submission**: the actual submission date and a handwritten signature cannot be filled in before the thesis is finished and printed; the v6 build had 28 remaining cosmetic overfull-text-box warnings (long file paths and a few dense new paragraphs not breaking across lines; see `../v6_2026-10-07/build/README.md` for the exact count and why it dropped from the v5 build's 38), none of which were found to clip any content on visual inspection; the quality-review pass noted in `AUTHOR_CHECKLIST.md` should be re-run once more immediately before a submission build, after any further edits, and a v12 PDF should be built (per the rendering procedure stated above) and its page count and rendered pages freshly verified before relying on it. No claim of supervisor approval or university acceptance is made anywhere in this package.

## How a later generator should assemble this

1. Concatenate the canonical files in the order above.
2. Render via xelatex + biblatex/biber, following the procedure stated in "Citation processing" above (copy the converter/templates from `../v6_2026-10-07/build/`, regenerate every chapter `.tex` fresh from this version's `.md` files, build to a new output location, and record a source-version check in the build log) — or pandoc + citeproc (documented but not verified in this environment — confirm pandoc is installed first).
3. Resolve in-text "Section X.Y" prose references using `CROSS_REFERENCE_MAP.md`.
4. Do not alter any numerical claim without re-deriving it from `claim_evidence_ledger.md`'s source file.
5. Insert remaining front matter (submission date, signature) only from author-supplied material at the time of actual submission; never generate it. A title page and declaration template exist in `../v6_2026-10-07/build/titlepage.tex` and `declaration.tex` with confirmed metadata and correctly blank signature/date fields; copy and adapt rather than regenerate from scratch.
6. Do not introduce an uncited bibliography entry into the rendered reference list via `nocite`.

## Files that must not be used as manuscript sources (superseded or non-editable)

Unchanged from v1/v2 (see those files for the full list and reasoning): `outputs/supervisor_development/18`–`26`; `writing/thesis.tex` and `thesis/chapters/` (master folder, outside this repository); `docs/provenance/final_empirical_package_v1_2026-10-07/` and `v2_2026-10-07/` for any numeric claim (superseded by `v3`, the current empirical package, itself unchanged since v1 of the manuscript). `manuscript/v1_2026-10-07/` through `v11_2026-10-09/` are each superseded as a manuscript source by the next version in sequence, down to this file's own `manuscript/v12_2026-10-10/` (this folder), the current canonical source; all eleven are preserved and readable, each with a pointer to the next version at its own top level. `../v6_2026-10-07/build/`'s generated chapter `.tex` files specifically must not be read as containing v7-through-v12 prose — they are v6's own generated output, frozen at that version.

## Empirical package used

`docs/provenance/final_empirical_package_v3_2026-10-07/`, unchanged from v1–v11 for every published coefficient. One new, read-only verification run of the historical estimator (`scripts/historical_wash/16_estimate_preliminary.py`, patched per R05) was performed this pass against the unchanged restricted inputs, confirmed byte-for-byte identical to the stored v1 output across all 291 model rows, and written to a new timestamped directory (`data/processed/estimation/run_20261010T140944Z/`, RESTRICTED, outside this repository) without altering the original `run_20261006T185646Z/` — see the resolution register for the comparison.
