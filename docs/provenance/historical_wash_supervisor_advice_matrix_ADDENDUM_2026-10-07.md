# Addendum to the supervisor-advice matrix (2026-10-07)

Supersedes row 1 of `historical_wash_supervisor_advice_matrix_2026-10-07.md` (2026-10-07, same day, earlier in this work session). The original file is preserved unchanged; this addendum is the authority on the point below.

## Correction

Row 1 of the original matrix stated: "cluster-FE household model omits wealth from the main specification by design (collinear with the cluster FE in many clusters) and reports it as a sensitivity." **This is wrong for the baseline household cluster-FE model.**

Checked directly against `outputs/household_community_wash/03_household_cluster_fe.csv`, filtered to `model_label == natural_sample_PRIMARY_SAME_CLUSTER_CRV1`: the term list includes `wealth_quintile_Middle`, `wealth_quintile_Poorer`, `wealth_quintile_Richer`, `wealth_quintile_Richest` alongside the water/sanitation exposure terms. **Wealth quintile is estimated as a standard covariate in the primary household cluster-FE model**, exactly as in the household region-FE and community models — consistent with the supervisor's explicit request ("insist a little more that you control for household characteristics, like wealth, et cetera").

Cluster fixed effects do **not** automatically absorb household characteristics. A cluster fixed effect absorbs only what is constant *within* a cluster; wealth varies across households within the same cluster (this is exactly why 31.6%/50.6% of clusters have within-cluster variation in own-water/own-sanitation status, per `04_household_cluster_fe_support.csv` — the same logic applies to wealth, which is not cluster-constant either). There was no documented or code-level reason for wealth to be collinear with cluster FE in the baseline model, and it is not: it is included and estimated.

## Where wealth genuinely is excluded from a main specification, and why

The **historical** WASH extension (not the baseline) does exclude wealth from its main specification — for a different, documented reason, unrelated to cluster-FE collinearity: `historical_wash_design_v1.md` states "current wealth or current residence may be mediators or post-exposure" for a historical (early-life) exposure, and the preliminary estimation methods note adds "wealth overlaps with WASH components." This is a **substantive post-treatment/mediator concern plus multicollinearity with the WASH exposure itself**, not a fixed-effects-absorption claim, and it is estimated as a documented sensitivity (`historical_wash_preliminary_estimation_methods_2026-10-06.md` §7: pooled water HAZ with wealth added = 1.01 [0.50, 1.52], materially unchanged from the main 1.03).

## Corrected row 1 (replaces the original table row for citation purposes)

| # | Suggestion | Evidence | Implementation | Validation | Status |
|---|---|---|---|---|---|
| 1 | Control for household characteristics (wealth etc.) so results read as *conditional* associations | Explicit: "insist a little more that you control for household characteristics, like wealth, et cetera." | Wealth quintile (and maternal education, literacy, household size) is included as a standard covariate in **every** baseline specification — household region-FE, household cluster-FE, and community models alike. In the **historical extension only**, wealth is excluded from the main specification for a documented post-treatment/mediator and WASH-overlap reason, and reported as a sensitivity (materially unchanged result). | Confirmed directly from `outputs/household_community_wash/03_household_cluster_fe.csv` (baseline) and `historical_wash_preliminary_estimation_methods_2026-10-06.md` §7 (historical sensitivity). | Implemented correctly; prior write-up of the reason was wrong and is corrected here. |

No other row of the original matrix is affected by this correction.
