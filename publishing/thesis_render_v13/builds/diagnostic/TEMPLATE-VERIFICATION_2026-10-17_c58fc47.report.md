# Build report — TEMPLATE VERIFICATION (diagnostic, not a thesis chapter)

- **Output**: `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-17_c58fc47.pdf`
- Built (UTC): 2026-10-17 20:11:07
- Repository: https://github.com/UBakhodir/thesis-wash-child-nutrition-dhs.git; branch `assembly/v13-final-2026-10-17`; commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78`
- Uncommitted changes in build inputs at build time: ?? manuscript/v13_2026-10-17/
?? publishing/thesis_render_v13/chapters/
?? publishing/thesis_render_v13/diagnostics/
?? publishing/thesis_render_v13/drivers/
?? publishing/thesis_render_v13/filters/
?? publishing/thesis_render_v13/scripts/
?? publishing/thesis_render_v13/template/
- Tools: python 3.14.0; pandoc pandoc 3.12.1; xelatex MiKTeX-XeTeX 4.16 (MiKTeX 25.12); biber biber version: 2.21; pymupdf 1.28.2
- Main font: Times New Roman (Version 7.00) at C:\Windows\Fonts\times.ttf, sha256 2cff2a03d8034801

## What this is

Diagnostic content only. Nothing in it is a thesis finding; it must not be copied into the manuscript.

## Input hashes (sha256)

| Role | File | sha256 |
|---|---|---|
| diagnostic md | `publishing/thesis_render_v13/diagnostics/template_verification.md` | `07c29033c3f7acd7885795778352a07c67f983e8b38a42ff4012ecfc7fd49e2a` |
| diagnostic appendix md | `publishing/thesis_render_v13/diagnostics/template_verification_appendix.md` | `514f7048dcf13218a8085df07a0d71062dbfaf6d6b3d923eafa7c3d72f992e0c` |
| preamble | `publishing/thesis_render_v13/template/thesis-preamble.tex` | `96fadee0043662c67d146fd2e1e04fef15aa163b0f6850505a1a33a282b58be2` |
| metadata | `publishing/thesis_render_v13/template/metadata.tex` | `95434f858b348554f2197527096ca5bf854c862755f170995690b707571939e2` |
| title page | `publishing/thesis_render_v13/template/titlepage.tex` | `b27cc7d119ef5fe6bc5d46760795871891d08eba548dac3dc2b5cbcd3367adbd` |
| declaration | `publishing/thesis_render_v13/template/declaration.tex` | `a0ccc2c50c837803e307e3e130116c2161c14985494218af35070f35c3f18010` |
| filter | `publishing/thesis_render_v13/filters/thesis.lua` | `396c91097c881993bcd2e433e51e3f72c32ab14e820fa613277c56b07f4b3ca9` |
| bibliography | `publishing/thesis_render_v13/bibliography/bibliography.bib` | `1132b0a226767004f476994273c643c38bada038f49f965771dbb752b058e9e6` |
| build script | `publishing/thesis_render_v13/scripts/build.py` | `95a48118a94e09dacd5aeb2349171628f531947df984f933236296c49e3ee4fd` |

## Compilation (final xelatex pass, after biber)

- Pages: 12; LaTeX errors: 0; rerun still requested: False
- Missing characters: 0 
- Overfull hbox: 0; overfull vbox: 0; underfull hbox: 0
- Undefined citations: none; undefined references: none
- Biber: 0 errors, 0 warnings 
- Works in the generated reference list (2): Burgert2013, Victora2010
- Font warnings: none

## Automated layout measurements (PyMuPDF)

- PDF pages: 12; page size 595.28 × 841.89 pt (A4 = 595.28 × 841.89 pt)
- Embedded fonts: DLVCIR+CourierNewPSMT, GVAIUN+TimesNewRomanPSMT, HPTKWZ+TeXGyreTermesMath-Regular-Identity-H, HYCFTM+TimesNewRomanPS-BoldMT, WTENXR+TimesNewRomanPS-ItalicMT
- Allowed text block (pt, x0 y0 x1 y1): [70.87, 79.37, 481.89, 762.52]; measured text extents: {'min_x0': 70.87, 'max_x1': 481.97, 'min_y0': 79.72, 'max_y1': 765.13}
- Measured left margin 2.5 cm (spec 2.5); smallest right margin 3.997 cm (spec ≥ 4.0)
- Most 11pt text lines on one page: 35
- Baseline pitch by font size (pt → count): 7.5pt: {7.76: 1}; 9.0pt: {13.5: 3}; 10.0pt: {15.0: 18, 20.72: 3, 19.5: 1, 23.07: 1}; 10.5pt: {15.0: 4}; 11.0pt: {19.5: 127, 15.0: 10, 29.25: 3, 28.01: 2, 28.0: 2, 31.45: 2}; 14.0pt: {19.5: 2}
- Characters by size/font: 11.0pt TimesNewRomanPSMT: 12387; 10.0pt TimesNewRomanPSMT: 1492; 9.0pt TimesNewRomanPSMT: 403; 11.0pt TimesNewRomanPS-ItalicMT: 372; 14.0pt TimesNewRomanPS-BoldMT: 329; 11.0pt TimesNewRomanPS-BoldMT: 270; 12.0pt TimesNewRomanPS-BoldMT: 212; 10.0pt TimesNewRomanPS-ItalicMT: 121; 10.0pt TimesNewRomanPS-BoldMT: 117; 10.6pt CourierNewPSMT: 98; 11.6pt CourierNewPSMT: 74; 11.0pt TeXGyreTermesMath-Regula: 34; 7.7pt TimesNewRomanPSMT: 30; 7.7pt TimesNewRomanPS-ItalicMT: 30
- Heading baseline gaps (pt):
  - p.3 11.0pt TimesNewRomanPS-BoldMT “1 Diagnostic heading level 1: template verificatio”: from previous baseline 34.5, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.1 Diagnostic heading level 2 . . . . . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.2 Diagnostic heading level 2: tables . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.3 Diagnostic heading level 2: mathematics and sp”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.4 Diagnostic heading level 2: full-page line cou”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.1.1 Diagnostic heading level 3 . . . . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.1.1.1 Diagnostic heading level 4 . . . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.4 14.0pt TimesNewRomanPS-BoldMT “1 Diagnostic heading level 1: template verificatio”: from previous baseline None, to next baseline 39.0
  - p.4 12.0pt TimesNewRomanPS-BoldMT “1.1 Diagnostic heading level 2”: from previous baseline 39.0, to next baseline 39.0
  - p.5 12.0pt TimesNewRomanPS-BoldMT “1.2 Diagnostic heading level 2: tables”: from previous baseline 39.0, to next baseline 39.0
  - p.5 11.0pt TimesNewRomanPS-BoldMT “1.1.1 Diagnostic heading level 3”: from previous baseline 29.25, to next baseline 29.25
  - p.5 11.0pt TimesNewRomanPSMT “1.1.1.1 Diagnostic heading level 4”: from previous baseline 29.25, to next baseline 19.5
  - p.6 12.0pt TimesNewRomanPS-BoldMT “1.3 Diagnostic heading level 2: mathematics and sp”: from previous baseline 46.34, to next baseline 39.0
  - p.7 12.0pt TimesNewRomanPS-BoldMT “1.4 Diagnostic heading level 2: full-page line cou”: from previous baseline 39.0, to next baseline 39.0
- Automated issues found: 0

Page images for visual inspection: `builds/diagnostic/work/20261017T201049Z/pages/` (not committed). Automated checks do not replace looking at every page.
