# This manuscript version is superseded — see v11

`manuscript/v10_2026-10-07/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v11_2026-10-09/`**.

v11 corrects two small issues found during a bounded final source-package verification (reading every numerical claim in the canonical chapters/appendices against its authoritative output file, and checking variable/weight/FE descriptions against the actual implemented code):

1. `01_introduction.md` §1.6 stated the household sanitation–HAZ confidence interval as `[−0.058, 0.110]`; the authoritative source (`outputs/household_community_wash/03_household_cluster_fe.csv`, value 0.109150) and this manuscript's own Table 5.1 (`05_results.md`) both correctly round this to `0.109`. One digit corrected.
2. `04_empirical_strategy.md` §4.5's weighting formula stated that baseline and historical pooled weights are both scaled to sum to exactly $N/M$ per country. Only the historical pipeline (`scripts/historical_wash/16_estimate_preliminary.py`) does this; the baseline pipeline (`scripts/dhs_harmonization/11_main_regressions.py`'s `build_temporary_pooled_weight()`, reused by the household-model script) normalises each country's weights to sum to exactly $1$, omitting the $N/M$ multiplier. This difference was confirmed to have **no effect on any reported coefficient, standard error, confidence interval, or p-value** — weighted least squares and its cluster-robust sandwich variance are both invariant to rescaling every observation's weight by one constant shared by every observation in the model, confirmed directly by refitting a model under both conventions and finding identical results to machine precision. The formula was rewritten to describe what each pipeline actually implements, with this invariance stated explicitly.

**No empirical estimate, sample, weight value actually used in any model, or reported coefficient/SE/CI/p-value changed.** Every other numerical claim checked in this pass (the full household, community, joint, Nigeria-sensitivity, age-heterogeneity, and historical-extension tables, plus the abstract, conclusion, and appendices) matched its authoritative source exactly.

Full detail: `docs/provenance/final_source_verification_v1_2026-10-09.md`.

Do not cite this version's `01_introduction.md` §1.6 CI value or `04_empirical_strategy.md` §4.5's weighting formula — use v11's corrected text. **No PDF has been built from v11.**
