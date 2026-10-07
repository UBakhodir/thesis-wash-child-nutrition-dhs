# This manuscript version is superseded — see v6

`manuscript/v5_2026-10-07/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v6_2026-10-07/`**.

v6 fixes real, confirmed PDF clipping in this version's own `build/main.pdf` (found by rendering pages to images and inspecting them, not by warning counts — worst case 1272pt/≈45cm of a table running off the page in Appendix A); corrects an unverified "numerical noise" explanation for the historical-model SE/CI/p-value differences (the actual cause was a missing `linearmodels` covariance flag, now identified and fixed — closes to exactly 0.0 for all 24 cells); and removes unsupported "unlikely to be a multiplicity artefact" language from Results §5.6 and Discussion §6.1. **No empirical estimate changed.**

Full itemised list: `../v6_2026-10-07/CORRECTION_LOG.md`.

Do not build from this version's `build/md2tex.py` — it has the table-overflow and double-escaping bugs described above. Use v6 unless specifically comparing versions.
