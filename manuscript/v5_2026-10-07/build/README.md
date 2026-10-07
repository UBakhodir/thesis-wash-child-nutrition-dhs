# Diagnostic build (2026-10-07, rebuilt for v5)

Rebuilt from v5's corrected `02_literature_review.md` (the Addae et al. 2024 correction, one sentence). Re-verified: 0 LaTeX errors across 3 passes (`build_xelatex_pass1.log`, `build_biber.log`, `build_xelatex_pass2.log`, `build_xelatex_pass3_final.log`), biber resolved 20/20 citekeys, total PDF 45 pages, main-text page count **unchanged at 31 pages** (the one-sentence edit did not cross a page boundary; section breakdown identical to v4's — see below). Everything below this line describes the build generally and is unchanged from v4's build note except this top paragraph.

This is a **local diagnostic build**, not the final submission PDF, and must not be represented as one. It exists to verify page count, citation resolution, and basic typesetting against the university's formatting specification (`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`), using the "default layout" alternative the guidelines permit when not using the official template (the official LaTeX/Word template by Dr. Holger Gerhardt was not available locally).

## Why this toolchain, not pandoc

`MASTER_ASSEMBLY.md` documents pandoc + citeproc as the recommended workflow for a future whole-document generator. **pandoc is not installed in this environment** (confirmed: `which pandoc`, `Get-Command pandoc` both fail). MiKTeX (xelatex, biber) is installed. This diagnostic build therefore uses xelatex + biblatex/biber directly — which is also exactly what the university guidelines themselves name as the supported toolchain for Chicago-style references ("This citation style is available in Zotero and BibLaTeX"). `md2tex.py` is a small, purpose-built converter (not a general Markdown parser) that turns the canonical `.md` chapter sources into the `.tex` fragments this build `\input`s; it is **not** a substitute for pandoc in the general case and is scoped only to the Markdown constructs actually used in this manuscript (headers, bold/italic, inline code, pipe tables, math, and the project's pandoc-citation syntax).

## Files

- `preamble.tex` — formatting specification (A4; margins 2.5/4.0 cm and 2.8/2.8 cm, combined 6.5 cm and 5.6 cm; Times New Roman 11pt/19.5pt leading for main text; heading sizes/spacing per level 1–4; biblatex chicago-authordate).
- `titlepage.tex` — title page using the university's own sample layout, with the confirmed title, degree, supervisor, author name and matriculation number from the registration confirmation email; submission month/year left as a placeholder (not yet known).
- `declaration.tex` — the exact required declaration wording, with blank date/signature lines for the author to complete by hand on the printed copy.
- `md2tex.py` — converts `../0*.md` and `../appendices/*.md` to `chapters/*.tex` / `appendices/*.tex`. **Generated output — do not hand-edit `chapters/*.tex` or `appendices/*.tex`; edit the canonical `.md` files in `manuscript/v5_2026-10-07/` and regenerate.**
- `main.tex` — assembles title page, table of contents, abstract, the seven numbered chapters, references, the three appendices, and the declaration, with Arabic page numbering starting at 1 on the abstract (first page after the table of contents), per the guidelines.
- `main.pdf` — the diagnostic build output (45 pages total; see page-count breakdown below).
- `build_xelatex_pass1.log`, `build_biber.log`, `build_xelatex_pass2.log`, `build_xelatex_pass3_final.log` — the exact logs from the successful reproducible build sequence below; the final pass had 0 errors (checked: no `! `, no `undefined`, beyond the known cosmetic items noted below).

## Reproducible build command

From this directory (`manuscript/v5_2026-10-07/build/`), with the canonical `.md` files unchanged since the last `md2tex.py` run (re-run it first if they changed):

```sh
python md2tex.py chapters/*.md appendices/*.md   # only if .md sources changed; copy them into chapters/ and appendices/ first (not committed — see note below)
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

Three xelatex passes plus one biber pass are required (standard for biblatex): pass 1 generates `main.bcf` for biber; biber resolves the 20 cited keys against `../bibliography.bib`; passes 2–3 resolve citations and cross-references and stabilise the table of contents and page numbers.

**Note on `.md` inputs**: `md2tex.py` reads from `chapters/*.md` and `appendices/*.md`, which are temporary local copies of the canonical sources (`../0*.md`, `../appendices/*.md`) made during this build and then removed — they are not committed, to keep one canonical copy of the chapter text. To rebuild after an edit to the canonical manuscript, copy the updated `.md` files into `chapters/`/`appendices/` again, run `md2tex.py`, then the xelatex/biber sequence above.

## Verified page count (this is a real compiled count, not an estimate)

Extracted from the actual PDF (`pypdf`, page-by-page text search for section-start markers):

| Section | PDF pages | Count |
|---|---|---|
| Title page | 1 | 1 (excluded from the 40-page limit) |
| Table of contents | 2–4 | 3 (excluded from the 40-page limit) |
| **Main text (abstract through conclusion)** | **5–35** | **31 pages — within the 40-page Master's limit** |
| References | 36–38 | 3 (excluded from the 40-page limit) |
| Appendices A–C | 39–44 | 6 (excluded from the 40-page limit) |
| Declaration | 45 | 1 |

Main text = 31 pages ≤ 40. **No trimming was required.** This includes the abstract, counted conservatively as part of the main text per the task instruction not to assume it is exempt absent an explicit exemption in the guidelines.

## Known cosmetic issues, not fixed in this diagnostic pass

- 38 "Overfull \\hbox" warnings, almost all from long unbroken file-path strings inside `\texttt{}` (e.g. `docs/provenance/historical_wash_preliminary_estimation_methods_2026-10-06.md`) that do not break across lines. Cosmetic only — no content is clipped or lost; confirmed by the page-count extraction above matching the expected section boundaries. A final build should wrap these paths (e.g. with the `seqsplit` package) or shorten in-text path citations.
- Minor LaTeX font-substitution warnings for small math subscript sizes (5.5pt) — standard, harmless, Computer Modern substituted for a size Times New Roman's math support doesn't provide at that exact size.
- `\captionsetup` approximates, rather than exactly reproduces, the guidelines' 10pt/15pt caption specification, because no table or figure in this manuscript currently uses a numbered `\caption{}` (all tables are unlabelled `longtable`s matching the Markdown source) — immaterial to this build, worth revisiting only if captions are added later.
- The table of contents entries are generated via `\addcontentsline` against the manually-numbered heading text already baked into each `.md` heading (e.g. "1.1 Two distinct exposures..."); this was chosen over LaTeX's automatic section numbering specifically to keep exact correspondence with `../CROSS_REFERENCE_MAP.md`'s stable labels, and was verified to reproduce the same section numbers.

## What this build does and does not establish

**Establishes**: the manuscript compiles cleanly under the exact specified formatting; the main text is 31 pages, 9 pages under the 40-page limit; all 20 cited bibliography keys resolve (biber: "Found 20 citekeys", 0 errors); no missing-glyph or undefined-reference errors remain in the final pass.

**Does not establish**: final-submission readiness. Front matter beyond the title page and declaration (e.g. exact binding, print quality) is not assessed by a PDF; the 38 overfull-hbox cosmetic issues should be cleaned up before a submission build; and this PDF has not been reviewed for prose quality, only for compilation correctness and page count.
