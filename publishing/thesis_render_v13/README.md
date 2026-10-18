# Thesis rendering package (v12 manuscript)

One shared template, one bibliography and one build script for rendering the MSc thesis from the
canonical manuscript `manuscript/v12_2026-10-10/`. Created 2026-10-13. **Rendered so far: Chapter 1
(introduction), carried forward by the author after review (recorded in `chapters/APPROVED.tsv`), and
Chapter 2 (literature review), reviewed with a required §2.4 correction pending at final assembly
(`FINAL_ASSEMBLY_REGISTER.md` FA-1), Chapter 3 (data and variables) as a review-copy preview, awaiting author review with a required
cross-reference correction pending at final assembly (FA-7), Chapter 4 (empirical strategy) as a
review-copy preview, awaiting author review with four required corrections pending at final
assembly (FA-8, FA-12), Chapter 5 (results) as a verified review-copy preview, awaiting author review
(points in FA-9; canonical synchronisation required, FA-13), and Chapter 6 (discussion and limitations)
as a verified review-copy preview, awaiting author review (points in FA-14, FA-15), and Chapter 7
(conclusion) as a verified review-copy preview, awaiting author review (points in FA-16), and the abstract
(unnumbered `abstract` unit, not a chapter) as a verified review-copy preview, awaiting author review (points in FA-17; new review items FA-21),
and Appendix A (`appA`, numbered Appendix A) as a verified review-copy preview, awaiting author review (points in FA-19; shared-code note FA-20),
and Appendix B (`appB`, numbered Appendix B) as a verified review-copy preview, awaiting author review (points in FA-22; required §B.1 wording FA-22 F),
and Appendix C (`appC`, numbered Appendix C) as a verified review-copy preview, awaiting author review (points in FA-23), and the consolidated reference list (references only, 20 works) as a review copy, awaiting author review (FA-3 carried out in a publishing copy of the bibliography; follow-ups FA-24; review items FA-25)**;
no full thesis.
The other PDFs are the template-verification document and the preview-pipeline selftest (diagnostic
text only).

Start with `HANDOVER.md` (status, decisions, open issues; its §21 maps each preview PDF filename to its
unit and lists what final assembly still needs). `FINAL_ASSEMBLY_REGISTER.md` lists the deferred corrections and final-assembly tasks. `REQUIREMENTS_CHECKLIST.md` lists each
formatting requirement and how it was checked.

## Layout

| Path | Purpose |
|---|---|
| `template/thesis-preamble.tex` | The shared formatting preamble (page, fonts, sizes, headings, tables, captions, citations, page styles). Used by every build. |
| `template/metadata.tex` | Title, author, matriculation number, supervisor, submission month/year (placeholder). |
| `template/titlepage.tex`, `template/declaration.tex` | Title page and final declaration page. |
| `filters/thesis.lua` | pandoc Lua filter: heading numbers, table captions, column widths, superscripts, code spans (conversion mechanics only). |
| `scripts/build.py` | The single build entry point (all commands below). |
| `scripts/pdfcheck.py` | Measured layout checks on a built PDF and page images. |
| `drivers/thesis-body.tex` | Master assembly order for the full thesis (one document, one contents page, one reference list). |
| `chapters/md/` | Publishing copies of the canonical chapter Markdown (created per chapter by `prepare`; empty now). |
| `chapters/tex/` | LaTeX generated from `chapters/md/` by `convert` (empty now). These are the editable sources the full assembly includes. |
| `bibliography/bibliography.bib` | Publishing copy of the canonical bibliography; the one file every build reads. `field_changes.tsv` lists each change against canonical; `REFERENCES_VERIFICATION.md` gives evidence, counts and open points. |
| `chapters/APPROVED.tsv` | Author approvals (unit, tex hash). `thesis --final` requires every unit to be approved and unchanged. |
| `diagnostics/` | Diagnostic content for the template-verification PDF (not thesis text). |
| `source_manifest.tsv` | sha256 of every canonical input at commit `c58fc47…`; `build.py manifest` checks it. |
| `builds/` | Outputs: `diagnostic/`, `selftest/`, later `previews/` and `thesis/`. PDFs and `.report.md` files are kept; `builds/*/work/` (logs, aux, page images) is git-ignored and regenerable. |

Every build reads **one** bibliography, the publishing copy `bibliography/bibliography.bib`
(created 2026-10-17 from `manuscript/v12_2026-10-10/bibliography.bib`, which stays unchanged and is
still checked by `manifest`). Until 2026-10-17 builds read the canonical file directly; previews built
before then show the earlier reference entries.

## Requirements

- Python ≥ 3.9; `pip install pymupdf fonttools` (layout checks, glyph check)
- pandoc ≥ 3.1 (tested: 3.1.3)
- XeLaTeX + biber with: biblatex-chicago, unicode-math, titlesec, tocloft, caption (incl. ltcaption),
  longtable, booktabs, needspace, fancyhdr, xurl, hyperref, csquotes, babel (tested: TeX Live 2023,
  XeTeX 0.999995, biber 2.19). MiKTeX works if these packages are installed.
- Fonts: **Times New Roman** (installed on Windows/macOS by default); TeX Gyre Termes Math
  (`texgyretermes-math.otf`, part of TeX Live/MiKTeX) for mathematical symbols; Liberation Mono, or
  Courier New as automatic fallback, for inline file names.

Check everything with: `python scripts/build.py env`

## Commands (run from this directory; Windows: `python` or `py`)

```sh
python scripts/build.py env                 # tools, font, repository state
python scripts/build.py manifest            # canonical v12 inputs unchanged since setup?
python scripts/build.py lint                # all units: citations, numbering, cross-refs, glyphs, converter dry run (no PDF)
python scripts/build.py diagnostic          # rebuild the TEMPLATE-VERIFICATION PDF
python scripts/build.py selftest            # run the preview pipeline on diagnostic text
python scripts/build.py references          # REVIEW-COPY of the consolidated reference list only
```

`references` collects the cited keys from the eleven `chapters/md` copies, prints them with an explicit
`\nocite{…}` list (never `\nocite{*}`) and the same `\printbibliography` call as the thesis driver, and
stops if the printed list differs from the collected keys.

### Single-chapter preview (one chapter per new chat)

```sh
python scripts/build.py manifest            # must report all inputs unchanged
python scripts/build.py lint ch01
python scripts/build.py prepare ch01        # byte-identical copy -> chapters/md/01_introduction.md (never overwrites)
python scripts/build.py preview ch01        # converts, builds, measures, renders page images
```

Units: `abstract`, `ch01`–`ch07`, `appA`–`appC`. Output:
`builds/previews/REVIEW-COPY_ch01-introduction_preview_<date>_<commit7>.pdf` plus a `.report.md`
recording the commit, every input hash, tool versions, compiler warnings, the works cited, and the
layout measurements. Page images for inspection are in the `work/` directory named in the output.
Every preview page carries a grey "REVIEW COPY" line in the top margin; pagination starts at 1 and is
provisional. A preview ends with a separately titled verification reference list generated at build
time; it is not part of the chapter source.

If an approved language edit is made, edit `chapters/md/<file>.md` (never the canonical v12 file),
then run `preview` again; the report states whether the copy is still identical to canonical.

### Full thesis (later, local VS Code)

```sh
python scripts/build.py manifest
python scripts/build.py lint --publishing-copies
python scripts/build.py thesis              # DRAFT: review header on every page, still one complete document
# after every unit is in chapters/APPROVED.tsv and the author has set the submission month/year:
python scripts/build.py thesis --final
# banner-free reading copy at any time, not gated on approvals or the submission-month placeholder,
# and not a claim of supervisor/university approval (added 2026-10-17):
python scripts/build.py thesis-clean
```

`thesis` compiles `drivers/thesis-body.tex` once (xelatex → biber → xelatex → xelatex): title page and
contents unnumbered; Arabic page 1 at the first main-text page; numbering continues through
references, appendices and the declaration (final page). The report prints the last page of the main
text (label `ThesisEndOfMainText`), which is the figure to check against the 40-page maximum.

## Safeguards built in

- A heading or table number in the Markdown that differs from the number LaTeX generates **stops the
  build** (`\ThesisCheckNumber`). A caption line not followed by a table, or a heading without a
  number, stops the conversion.
- `prepare` never overwrites; `manifest --write` never overwrites; `thesis --final` refuses
  unapproved/changed units and the placeholder submission date.
- Builds fail on LaTeX errors, undefined citations or missing glyphs.
