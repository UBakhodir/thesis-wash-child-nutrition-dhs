# Build report — REVIEW COPY — selftest preview

- **Output**: `builds/selftest/SELFTEST_preview-pipeline_2026-10-17_c58fc47.pdf`
- Built (UTC): 2026-10-17 20:11:51
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

A review copy of **selftest** only, built with the shared template. Pagination is provisional (the unit starts at page 1 here; in the thesis it will not). The reference list at the end is a verification aid generated at build time; it is not part of `chapters/tex/selftest_unit.tex`.

- md identical to canonical: False

## Input hashes (sha256)

| Role | File | sha256 |
|---|---|---|
| chapter md (publishing copy) | `publishing/thesis_render_v13/diagnostics/template_verification.md` | `07c29033c3f7acd7885795778352a07c67f983e8b38a42ff4012ecfc7fd49e2a` |
| generated tex | `publishing/thesis_render_v13/builds/selftest/work/20261017T201132Z/selftest_unit.tex` | `f00bfa21f9356d5766d2f039df3a2a1a17f7cf73c32347f55607f4d5bb807412` |
| preamble | `publishing/thesis_render_v13/template/thesis-preamble.tex` | `96fadee0043662c67d146fd2e1e04fef15aa163b0f6850505a1a33a282b58be2` |
| filter | `publishing/thesis_render_v13/filters/thesis.lua` | `396c91097c881993bcd2e433e51e3f72c32ab14e820fa613277c56b07f4b3ca9` |
| bibliography | `publishing/thesis_render_v13/bibliography/bibliography.bib` | `1132b0a226767004f476994273c643c38bada038f49f965771dbb752b058e9e6` |
| build script | `publishing/thesis_render_v13/scripts/build.py` | `95a48118a94e09dacd5aeb2349171628f531947df984f933236296c49e3ee4fd` |

## Compilation (final xelatex pass, after biber)

- Pages: 7; LaTeX errors: 0; rerun still requested: False
- Missing characters: 0 
- Overfull hbox: 0; overfull vbox: 0; underfull hbox: 0
- Undefined citations: none; undefined references: none
- Biber: 0 errors, 0 warnings 
- Works in the generated reference list (2): Burgert2013, Victora2010
- Font warnings: none

## Automated layout measurements (PyMuPDF)

- PDF pages: 7; page size 595.28 × 841.89 pt (A4 = 595.28 × 841.89 pt)
- Embedded fonts: HXEDLD+CourierNewPSMT, KIUMFL+TimesNewRomanPSMT, LSQKIC+TeXGyreTermesMath-Regular-Identity-H, XGRUQS+TimesNewRomanPS-BoldMT, XSRGAY+TimesNewRomanPS-ItalicMT
- Allowed text block (pt, x0 y0 x1 y1): [70.87, 79.37, 481.89, 762.52]; measured text extents: {'min_x0': 70.87, 'max_x1': 481.97, 'min_y0': 81.94, 'max_y1': 765.13}
- Measured left margin 2.5 cm (spec 2.5); smallest right margin 3.997 cm (spec ≥ 4.0)
- Most 11pt text lines on one page: 35
- Baseline pitch by font size (pt → count): 7.5pt: {7.76: 1}; 9.0pt: {13.5: 3}; 10.0pt: {15.0: 18, 20.72: 3, 19.5: 1}; 10.5pt: {15.0: 4}; 11.0pt: {19.5: 109, 29.25: 3, 31.45: 2, 31.46: 2, 39.01: 1, 2.44: 1}
- Characters by size/font: 11.0pt TimesNewRomanPSMT: 10471; 10.0pt TimesNewRomanPSMT: 1355; 9.0pt TimesNewRomanPSMT: 403; 12.0pt TimesNewRomanPS-BoldMT: 179; 10.0pt TimesNewRomanPS-ItalicMT: 121; 10.0pt TimesNewRomanPS-BoldMT: 106; 14.0pt TimesNewRomanPS-BoldMT: 96; 10.6pt CourierNewPSMT: 80; 11.0pt TimesNewRomanPS-BoldMT: 72; 11.6pt CourierNewPSMT: 44; 11.0pt TeXGyreTermesMath-Regula: 34; 7.7pt TimesNewRomanPSMT: 30; 7.7pt TimesNewRomanPS-ItalicMT: 30; 11.0pt TimesNewRomanPS-ItalicMT: 16
- Automated issues found: 0

Page images for visual inspection: `builds/selftest/work/20261017T201132Z/pages/` (not committed). Automated checks do not replace looking at every page.
