# This manuscript version is superseded — see v7

`manuscript/v6_2026-10-07/` (this folder) is preserved unchanged for the record. The current canonical manuscript source is **`manuscript/v7_2026-10-07/`**.

v7 responds to a direct, evidence-based correction task: sixteen confirmed, substantive discrepancies between this version's prose and the implemented code or primary literature sources, found by direct inspection and corrected. Most significant: the baseline sample's weight and cluster-identifier fields were wrongly described using the historical extension's IPUMS field names (`PERWEIGHT`, `IDHSPSU`) when the baseline actually uses DHS-native `v005`/`v021`-derived fields; the baseline's child-age construction was wrongly described as having a country-varying fallback that belongs only to the historical extension; the SHINE trial's design was described identically to the two WASH-Benefits trials when it is materially different (SHINE bundled water/sanitation/hygiene into one combined arm, never tested separately); a citation (Blom2022) was found to have no local PDF despite this version's claim of having read it in full; and four cross-reference errors pointed historical-extension content at baseline sections (§5.3, §4.1) instead of their correct destinations (§5.6, §5.8, §6.4). **No empirical estimate, sample, weight, or reported coefficient changed.**

Full itemised list: `../v7_2026-10-07/CORRECTION_LOG.md`.

Do not cite or build from v6's data/variables, empirical-strategy, or literature-review chapters, or its bibliography — use v7's. **No PDF has been built from v7 yet** (this correction pass was explicitly source-only); v6's own PDF (`build/main.pdf`) still reflects v6's content, not v7's corrections.
