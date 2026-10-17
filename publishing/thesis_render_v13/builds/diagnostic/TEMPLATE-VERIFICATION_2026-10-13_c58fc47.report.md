# Build report — TEMPLATE VERIFICATION (diagnostic, not a thesis chapter)

- **Output**: `builds/diagnostic/TEMPLATE-VERIFICATION_2026-10-13_c58fc47.pdf`
- Built (UTC): 2026-10-13 13:19:14
- Repository: https://github.com/UBakhodir/thesis-wash-child-nutrition-dhs; branch `claude/busy-ramanujan-u6qrs8`; commit `c58fc478e7b31789fc68e3c88cd25de4a6567c78`
- Uncommitted changes in build inputs at build time: ?? publishing/thesis_render_v12/chapters/
?? publishing/thesis_render_v12/diagnostics/
?? publishing/thesis_render_v12/drivers/
?? publishing/thesis_render_v12/filters/
?? publishing/thesis_render_v12/scripts/
?? publishing/thesis_render_v12/template/
- Tools: python 3.13.16; pandoc pandoc 3.1.3; xelatex XeTeX 3.141592653-2.6-0.999995 (TeX Live 2023/Debian); biber biber version: 2.19; pymupdf 1.28.2
- Main font: Times New Roman (Version 2.82) at /usr/local/share/fonts/msttcore/Times.TTF, sha256 4e98adeff8ccc8ef

## What this is

Diagnostic content only. Nothing in it is a thesis finding; it must not be copied into the manuscript.

## Input hashes (sha256)

| Role | File | sha256 |
|---|---|---|
| diagnostic md | `publishing/thesis_render_v12/diagnostics/template_verification.md` | `07c29033c3f7acd7885795778352a07c67f983e8b38a42ff4012ecfc7fd49e2a` |
| diagnostic appendix md | `publishing/thesis_render_v12/diagnostics/template_verification_appendix.md` | `514f7048dcf13218a8085df07a0d71062dbfaf6d6b3d923eafa7c3d72f992e0c` |
| preamble | `publishing/thesis_render_v12/template/thesis-preamble.tex` | `902faa263077ccc1225982a7f7242174480010833c39af136ca666fc699f6470` |
| metadata | `publishing/thesis_render_v12/template/metadata.tex` | `95434f858b348554f2197527096ca5bf854c862755f170995690b707571939e2` |
| title page | `publishing/thesis_render_v12/template/titlepage.tex` | `b27cc7d119ef5fe6bc5d46760795871891d08eba548dac3dc2b5cbcd3367adbd` |
| declaration | `publishing/thesis_render_v12/template/declaration.tex` | `a0ccc2c50c837803e307e3e130116c2161c14985494218af35070f35c3f18010` |
| filter | `publishing/thesis_render_v12/filters/thesis.lua` | `875b078ca7649e153558544544dca36df92e7e8cab82edd01997b5ec6c3683bc` |
| bibliography | `manuscript/v12_2026-10-10/bibliography.bib` | `1d88261e5fc0f1330f65ece35320747361118fa4e51d71fc4791de038d81da49` |
| build script | `publishing/thesis_render_v12/scripts/build.py` | `d051cca0884d0953be60d2f6f46d5ba6377b77e93a7cebee53111d8bd2d42287` |

## Compilation (final xelatex pass, after biber)

- Pages: 13; LaTeX errors: 0; rerun still requested: False
- Missing characters: 0 
- Overfull hbox: 0; overfull vbox: 0; underfull hbox: 0
- Undefined citations: none; undefined references: none
- Biber: 0 errors, 0 warnings 
- Works in the generated reference list (2): Burgert2013, Victora2010
- Font warnings: ['Package fontspec Warning: Font "Times New Roman Italic" does not contain', 'Package fontspec Warning: Font "Times New Roman" does not contain requested', "Package fontspec Warning: OpenType feature 'Style=MathScript' (ssty) not", "Package fontspec Warning: OpenType feature 'Style=MathScriptScript' (ssty) not"]

## Automated layout measurements (PyMuPDF)

- PDF pages: 13; page size 595.28 × 841.89 pt (A4 = 595.28 × 841.89 pt)
- Embedded fonts: DFQYRV+TimesNewRomanPS-BoldMT, DQFYAR+TimesNewRomanPS-ItalicMT, EPRNXF+TeXGyreTermesMath-Regular-Identity-H, HDPTQD+LiberationMono, MFBLZS+TimesNewRomanPSMT
- Allowed text block (pt, x0 y0 x1 y1): [70.87, 79.37, 481.89, 762.52]; measured text extents: {'min_x0': 70.87, 'max_x1': 481.97, 'min_y0': 79.72, 'max_y1': 758.28}
- Measured left margin 2.5 cm (spec 2.5); smallest right margin 3.997 cm (spec ≥ 4.0)
- Most 11pt text lines on one page: 35
- Baseline pitch by font size (pt → count): 7.5pt: {7.75: 1}; 8.5pt: {15.0: 2}; 9.0pt: {13.5: 4}; 10.0pt: {15.0: 18, 20.72: 2, 20.71: 2, 19.51: 1, 23.07: 1}; 11.0pt: {19.5: 126, 15.0: 9, 29.25: 3, 28.01: 2, 28.0: 2, 31.45: 2}; 14.0pt: {19.5: 2}
- Characters by size/font: 11.0pt TimesNewRomanPSMT: 12266; 10.0pt TimesNewRomanPSMT: 1247; 9.0pt TimesNewRomanPSMT: 403; 11.0pt TimesNewRomanPS-ItalicMT: 372; 14.0pt TimesNewRomanPS-BoldMT: 329; 11.0pt TimesNewRomanPS-BoldMT: 270; 12.0pt TimesNewRomanPS-BoldMT: 212; 10.0pt TimesNewRomanPS-BoldMT: 117; 10.0pt TimesNewRomanPS-ItalicMT: 110; 8.5pt LiberationMono: 98; 9.3pt LiberationMono: 74; 11.0pt TeXGyreTermesMath-Regula: 34; 7.7pt TimesNewRomanPSMT: 30; 7.7pt TimesNewRomanPS-ItalicMT: 30
- Heading baseline gaps (pt):
  - p.3 11.0pt TimesNewRomanPS-BoldMT “1 Diagnostic heading level 1: template verificatio”: from previous baseline 34.5, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.1 Diagnostic heading level 2 . . . . . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.2 Diagnostic heading level 2: tables . . . . . .”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.3 Diagnostic heading level 2: mathematics and sp”: from previous baseline 15.0, to next baseline 15.0
  - p.3 11.0pt TimesNewRomanPSMT “1.4 Diagnostic heading level 2: full-page line cou”: from previous baseline 15.0, to next baseline 15.0
  - p.4 14.0pt TimesNewRomanPS-BoldMT “1 Diagnostic heading level 1: template verificatio”: from previous baseline None, to next baseline 39.0
  - p.4 12.0pt TimesNewRomanPS-BoldMT “1.1 Diagnostic heading level 2”: from previous baseline 39.0, to next baseline 39.0
  - p.5 12.0pt TimesNewRomanPS-BoldMT “1.2 Diagnostic heading level 2: tables”: from previous baseline 39.0, to next baseline 39.0
  - p.5 11.0pt TimesNewRomanPS-BoldMT “1.1.1 Diagnostic heading level 3”: from previous baseline 29.25, to next baseline 29.25
  - p.5 11.0pt TimesNewRomanPSMT “1.1.1.1 Diagnostic heading level 4”: from previous baseline 29.25, to next baseline 19.5
  - p.7 12.0pt TimesNewRomanPS-BoldMT “1.3 Diagnostic heading level 2: mathematics and sp”: from previous baseline 46.35, to next baseline 39.0
  - p.8 12.0pt TimesNewRomanPS-BoldMT “1.4 Diagnostic heading level 2: full-page line cou”: from previous baseline 39.0, to next baseline 39.0
- Automated issues found: 0

Page images for visual inspection: `builds/diagnostic/work/20261013T131905Z/pages/` (not committed). Automated checks do not replace looking at every page.
