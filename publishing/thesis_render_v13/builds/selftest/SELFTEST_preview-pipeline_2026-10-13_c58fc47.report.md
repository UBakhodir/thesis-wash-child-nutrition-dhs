# Build report — REVIEW COPY — selftest preview

- **Output**: `builds/selftest/SELFTEST_preview-pipeline_2026-10-13_c58fc47.pdf`
- Built (UTC): 2026-10-13 13:19:54
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

A review copy of **selftest** only, built with the shared template. Pagination is provisional (the unit starts at page 1 here; in the thesis it will not). The reference list at the end is a verification aid generated at build time; it is not part of `chapters/tex/selftest_unit.tex`.

- md identical to canonical: False

## Input hashes (sha256)

| Role | File | sha256 |
|---|---|---|
| chapter md (publishing copy) | `publishing/thesis_render_v12/diagnostics/template_verification.md` | `07c29033c3f7acd7885795778352a07c67f983e8b38a42ff4012ecfc7fd49e2a` |
| generated tex | `publishing/thesis_render_v12/builds/selftest/work/20261013T131945Z/selftest_unit.tex` | `7950dc5b439b5b20dabda08acead9850d53458a6d5cad14b972df10b19f5ce39` |
| preamble | `publishing/thesis_render_v12/template/thesis-preamble.tex` | `902faa263077ccc1225982a7f7242174480010833c39af136ca666fc699f6470` |
| filter | `publishing/thesis_render_v12/filters/thesis.lua` | `875b078ca7649e153558544544dca36df92e7e8cab82edd01997b5ec6c3683bc` |
| bibliography | `manuscript/v12_2026-10-10/bibliography.bib` | `1d88261e5fc0f1330f65ece35320747361118fa4e51d71fc4791de038d81da49` |
| build script | `publishing/thesis_render_v12/scripts/build.py` | `d051cca0884d0953be60d2f6f46d5ba6377b77e93a7cebee53111d8bd2d42287` |

## Compilation (final xelatex pass, after biber)

- Pages: 8; LaTeX errors: 0; rerun still requested: False
- Missing characters: 0 
- Overfull hbox: 0; overfull vbox: 0; underfull hbox: 0
- Undefined citations: none; undefined references: none
- Biber: 0 errors, 0 warnings 
- Works in the generated reference list (2): Burgert2013, Victora2010
- Font warnings: ['Package fontspec Warning: Font "Times New Roman Italic" does not contain', 'Package fontspec Warning: Font "Times New Roman" does not contain requested', "Package fontspec Warning: OpenType feature 'Style=MathScript' (ssty) not", "Package fontspec Warning: OpenType feature 'Style=MathScriptScript' (ssty) not"]

## Automated layout measurements (PyMuPDF)

- PDF pages: 8; page size 595.28 × 841.89 pt (A4 = 595.28 × 841.89 pt)
- Embedded fonts: CBHQNR+TimesNewRomanPS-BoldMT, GGZHJY+TeXGyreTermesMath-Regular-Identity-H, MZMLZR+LiberationMono, UBHVEN+TimesNewRomanPS-ItalicMT, UZCYGT+TimesNewRomanPSMT
- Allowed text block (pt, x0 y0 x1 y1): [70.87, 79.37, 481.89, 762.52]; measured text extents: {'min_x0': 70.87, 'max_x1': 481.97, 'min_y0': 81.94, 'max_y1': 758.28}
- Measured left margin 2.5 cm (spec 2.5); smallest right margin 3.997 cm (spec ≥ 4.0)
- Most 11pt text lines on one page: 35
- Baseline pitch by font size (pt → count): 7.5pt: {7.75: 1}; 8.5pt: {15.0: 2}; 9.0pt: {13.5: 4}; 10.0pt: {15.0: 17, 20.72: 2, 19.51: 1, 20.71: 1}; 11.0pt: {19.5: 108, 29.25: 3, 15.0: 2, 31.45: 2, 39.0: 1, 2.44: 1}; 14.0pt: {19.5: 1}
- Characters by size/font: 11.0pt TimesNewRomanPSMT: 10460; 10.0pt TimesNewRomanPSMT: 1110; 9.0pt TimesNewRomanPSMT: 403; 12.0pt TimesNewRomanPS-BoldMT: 179; 14.0pt TimesNewRomanPS-BoldMT: 131; 10.0pt TimesNewRomanPS-ItalicMT: 110; 10.0pt TimesNewRomanPS-BoldMT: 106; 8.5pt LiberationMono: 80; 11.0pt TimesNewRomanPS-BoldMT: 72; 9.3pt LiberationMono: 44; 11.0pt TeXGyreTermesMath-Regula: 34; 7.7pt TimesNewRomanPSMT: 30; 7.7pt TimesNewRomanPS-ItalicMT: 30; 11.0pt TimesNewRomanPS-ItalicMT: 16
- Automated issues found: 0

Page images for visual inspection: `builds/selftest/work/20261013T131945Z/pages/` (not committed). Automated checks do not replace looking at every page.
