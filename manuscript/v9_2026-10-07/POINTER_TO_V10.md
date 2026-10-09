# This manuscript version is superseded — see v10

`manuscript/v9_2026-10-07/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v10_2026-10-07/`**.

v10 corrects a circular-reasoning error in this version's own diagnostic. This version's script residualized each birth-year scheme's block against a nuisance set that included the exposure variable (E10) itself, then treated equal post-residualization ranks as proof the exposure coefficient was invariant to the choice of scheme — circular, since residualizing against E10 can remove exactly the part of a block that would otherwise reveal a difference affecting E10's own coefficient. v10's corrected diagnostic uses a five-step chain that never involves E10 in constructing the comparison being tested (direct block comparison; nuisance-only residualization with E10 excluded; E10's own residual vector compared directly; an independent from-scratch FWL cross-check; and a mechanical, E10-independent explanation of the redundant column). All five steps confirm the same substantive conclusion as this version, now on valid grounds. **No empirical estimate, sample, weight, or reported coefficient changed.**

Full itemised list: `../v10_2026-10-07/CORRECTION_LOG.md`.

Do not cite this version's `04_empirical_strategy.md` §4.6 or Appendix B §B.2, or `scripts/historical_wash/25_diagnose_birthyear_coding_and_age_control.py`'s reasoning — use v10's corrected versions. **No PDF has been built from v10.**
