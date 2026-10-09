# This manuscript version is superseded — see v9

`manuscript/v8_2026-10-07/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v9_2026-10-07/`**.

v9 corrects a methodological error in this version's own newly-written diagnostic (`scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`). This version's diagnostic compared the two birth-year dummy schemes' *raw* column spaces and concluded, from nesting alone, that the exposure coefficient was necessarily unaffected by the choice between them — an invalid inference, since the estimator fits on the weighted within-cluster-demeaned design, not the raw one. v9's corrected diagnostic compares the schemes on the actual transformed, residualized design and finds the two subspaces genuinely equal (not merely nested), which by the Frisch–Waugh–Lovell theorem is what actually guarantees the result — confirmed at full floating-point precision (absolute difference 6.7×10⁻¹⁶) rather than 7-decimal rounding mislabelled "bit-for-bit identical." `04_empirical_strategy.md` §4.6, Appendix B §B.2, and `03_data_and_variables.md` §3.8 (which had wrongly claimed the reference-coding choice "matters for the pooled estimate") are all corrected accordingly. **No empirical estimate, sample, weight, or reported coefficient changed.**

Full itemised list: `../v9_2026-10-07/CORRECTION_LOG.md`.

Do not cite this version's `03_data_and_variables.md` §3.8, `04_empirical_strategy.md` §4.6, or Appendix B §B.2, or `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`'s first-pass reasoning — use v9's corrected versions. **No PDF has been built from v9.**
