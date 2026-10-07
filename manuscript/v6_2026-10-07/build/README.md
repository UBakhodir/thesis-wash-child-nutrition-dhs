# Diagnostic build (2026-10-07, rebuilt for v6 — table-overflow fix)

Rebuilt from v6, which fixes real, confirmed PDF clipping found by direct visual inspection of v5's committed PDF (`manuscript/v5_2026-10-07/build/main.pdf`, commit `0090c16`) — not merely the overfull-hbox warning count. **This build README corrects a false claim made in the v5 build README**, which stated the overfull-hbox warnings were "cosmetic only — no content is clipped or lost" without having rendered and looked at the actual pages. That claim was wrong: the v5 PDF had genuine, severe table clipping (see "What was actually broken" below). This v6 build fixes the root cause and the fix is verified by rendering pages to images and inspecting them, not by text extraction or warning counts alone.

This is a **local diagnostic build**, not the final submission PDF, and must not be represented as one. It exists to verify page count, citation resolution, and basic typesetting against the university's formatting specification (`merkblatt-abschlussarbeiten-ba-ma-2026-07-23-eng.pdf`), using the "default layout" alternative the guidelines permit when not using the official template.

## What was actually broken in v5, found by rendering and looking at the pages

`md2tex.py`'s table converter gave every table column an unbounded `l` (left-aligned, non-wrapping) LaTeX column type regardless of how many columns the table had or how long its cells were. For tables with several columns, or any cell containing a long sentence, path, or (in the historical results tables) a coefficient crammed together with its CI, *p*-value, and sample size in one string, this produced LaTeX "Overfull hbox" warnings ranging up to **1272pt (≈45cm) too wide** — not a rounding error, but entire table columns running off the right edge of the page and being rendered off-page, invisible in the PDF. Rendered and visually confirmed on the two pages the user identified directly:

- **PDF page 27 (printed page 23)**: the historical water-results table (Results §5.6) — each cell packed a coefficient, 95% CI, *p*-value, and "N.../G..." sample-size string into one unwrapped line; the rightmost ("Pooled established") column ran off the page.
- **PDF page 39 (printed page 35)**: Appendix A's variable-definitions table — a 3-column table with long prose/path cells, worst single warning 1272pt, by far the most severe clipping in the document.

Separately, visual inspection also surfaced a **second, unrelated rendering bug**: plain prose containing a manually backslash-escaped underscore (e.g. `FULL\_DUMMY\_DF`, written by hand in the Markdown source to stop Markdown's own parser reading `_..._` as italics) was being double-escaped by `md2tex.py`'s LaTeX-escaping function into garbled, visible text like `FULL\textbackslash{}\_DUMMY\textbackslash{}\_DF` — present in v5 and likely every earlier build, not previously noticed because no one had rendered and looked at the affected pages.

## Fixes made (in `md2tex.py`, affecting every table and every inline code span in the document, not just the two flagged pages)

1. **Explicit, content-proportional wrapping column widths.** `convert_table()` now estimates each column's needed width from its longest cell's content length and allocates a `p{<width>cm}` wrapping column (via the `array` package, already loaded) proportionally, within the actual text width (14.5cm, computed from the specified 2.5cm/4.0cm margins), with a 1.6cm floor so no column is squeezed unreadably. `\tabcolsep` is reduced to 3pt per table so padding overhead doesn't eat into that budget on tables with several columns.
2. **Sample sizes moved out of coefficient cells.** `05_results.md`'s two historical-results tables (water, sanitation) previously packed "β [CI], *p*, N.../G..." into one cell. N/G is identical between the water and sanitation tables for a given outcome/country (verified directly against the stored model-results CSV before making this change), so it is now shown once, in a separate, clearly labelled table, rather than repeated and crammed into every coefficient cell.
3. **Inline code/paths can now break.** `\texttt{}` spans (file paths, module paths, flags) can now break at `/`, `_`, `.`, and `-` via zero-width `\allowbreak` insertions — zero-width means harmless on short spans (LaTeX only uses a break point if a line actually needs one) but lets a long path like `docs/provenance/independent_audit_v1_2026-10-07/09_update_2026-10-07_pass4.md` wrap across lines instead of overflowing.
4. **The double-escaping bug fixed.** `latex_escape()` now recognises a literal `\_` in the source as already being the correct final LaTeX escape and passes it through unchanged, instead of re-escaping the backslash into a visible `\textbackslash{}`.

## Verification performed: rendered pages, not just warnings or text extraction

Overfull-hbox warnings dropped from 38 (v5) to 28 (v6), but **the warning count is not what was checked** — per the explicit instruction that produced this fix, every remaining instance was investigated by rendering the actual PDF pages to images (`pymupdf`, 150 DPI) and visually inspecting them directly, not by re-running text extraction. Rendered and inspected: both originally-flagged pages (now PDF pages 27 and 40–41 after the page-count shift below) plus the surrounding Results, Appendix A, Appendix B, Appendix C, and References pages (PDF pages 26–28, 39–46).

**Result: every table and every path-wrapping case checked renders completely, with no clipped, hidden, or off-page content.** The 28 remaining overfull-hbox warnings (max ≈44pt ≈1.5cm) come from a few single long unbroken runs inside dense new prose (Appendix B §B.2) that still slightly exceed the line box; visually, `\raggedright` absorbs this as a small amount of extra space at the right edge of the line, not as clipped text — confirmed by direct inspection of the rendered page (PDF page 44), not asserted. This is the honest basis for calling the *remaining* warnings cosmetic, unlike the prior v5 README's unverified claim.

## Verified page count (real compiled count; page-boundary markers found via `pymupdf` text search on the rendered PDF, same method as before)

| Section | PDF pages | Count |
|---|---|---|
| Title page | 1 | 1 (excluded from the 40-page limit) |
| Table of contents | 2–4 | 3 (excluded from the 40-page limit) |
| **Main text (abstract through conclusion)** | **5–36** | **32 pages — within the 40-page Master's limit** |
| References | 37–39 | 3 (excluded from the 40-page limit) |
| Appendix A | 40–42 | 3 (excluded from the 40-page limit) |
| Appendix B | 43–45 | 3 (excluded from the 40-page limit) |
| Appendix C | 46–47 | 2 (excluded from the 40-page limit) |
| Declaration | 48 | 1 |

Main text = 32 pages ≤ 40 (8 pages of headroom). Total PDF length grew from 45 to 48 pages relative to v5 — expected and intentional: wrapped table cells take more vertical space than the unwrapped single lines they replace, and the N/G table and the new Appendix B explanation (§1 above) add content. **No trimming was required**, and nothing was removed to make it fit; every coefficient, interval, *p*-value, and variable definition from v5 is preserved, just correctly wrapped.

## Why this toolchain, not pandoc

Unchanged from v5: pandoc is not installed in this environment (`which pandoc` / `Get-Command pandoc` both fail); this diagnostic build uses xelatex + biblatex/biber directly, the toolchain the university guidelines themselves name for Chicago-style references. `md2tex.py` is a small, purpose-built converter, not a general Markdown parser, scoped to this manuscript's actual constructs.

## Files

- `preamble.tex` — formatting specification (A4; margins 2.5/4.0 cm and 2.8/2.8 cm; Times New Roman 11pt/19.5pt leading for main text; biblatex chicago-authordate).
- `titlepage.tex`, `declaration.tex` — unchanged from v5.
- `md2tex.py` — **fixed this pass** (see above). Converts `../0*.md` and `../appendices/*.md` to `chapters/*.tex` / `appendices/*.tex`. Generated output — do not hand-edit the `.tex` fragments; edit the canonical `.md` files in `manuscript/v6_2026-10-07/` and regenerate.
- `main.tex` — assembles title page, TOC, abstract, seven chapters, references, three appendices, declaration; Arabic pagination starting at 1 on the abstract.
- `main.pdf` — this build's output (48 pages total; see breakdown above).
- `build_xelatex_pass1.log`, `build_biber.log`, `build_xelatex_pass2.log`, `build_xelatex_pass3_final.log` — 0 errors in the final pass; biber: "Found 20 citekeys", 0 missing.

## Reproducible build command

From this directory, with the canonical `.md` files unchanged since the last `md2tex.py` run:

```sh
cp ../0*.md chapters/ && cp ../appendices/*.md appendices/   # temporary local copies, not committed
python md2tex.py chapters/*.md appendices/*.md
rm chapters/*.md appendices/*.md                              # remove the temporary copies again
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

## Other known cosmetic issues, not fixed in this pass (none involve lost or hidden content)

- Numbered-list items and bulleted items written as consecutive Markdown lines (no LaTeX list environment) render as inline-concatenated prose with the list markers kept as plain text (e.g. "1. ... 2. ... 3. ..." or "- C1 ... - C2 ...") rather than as a proper indented list. Visually inspected (Appendix B §B.2, Appendix C §C.1) and confirmed every item's full text is present and readable; this is a typographic style issue (`md2tex.py` has no list-environment support), not a clipping issue, and is left for a future pass.
- A narrow table header ("Sanitation" / "SE" / "β" wrapping onto two lines, Appendix B.1) is cosmetically tight but not clipped — confirmed by direct inspection.
- Minor LaTeX font-substitution warnings for small math subscript sizes — standard and harmless.
- `\captionsetup` approximates rather than exactly reproduces the guidelines' caption spec; immaterial since no table in this manuscript uses a numbered `\caption{}`.

## What this build does and does not establish

**Establishes**: the manuscript compiles cleanly; the main text is 32 pages, 8 under the 40-page limit; all 20 cited bibliography keys resolve; no missing-glyph or undefined-reference errors; **every page checked by direct visual rendering shows complete, unclipped content**, correcting the prior version's unverified claim to the same effect.

**Does not establish**: final-submission readiness. The list-environment typographic issue above should be cleaned up before a submission build; front matter beyond the title page and declaration is not assessed by a PDF; this PDF has not been reviewed for prose quality beyond the checks already described in `v6_2026-10-07/AUTHOR_CHECKLIST.md`.
