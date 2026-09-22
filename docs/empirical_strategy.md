# Thesis Roadmap and Empirical Strategy

## 1. Research question and mechanisms

The thesis asks how household-level and surrounding-community water and sanitation conditions are
associated with child nutritional outcomes in Ethiopia, Ghana, Kenya, and Nigeria, and whether these
associations differ across child age. The design is cross-sectional, so every coefficient below should be
read as an association rather than a causal effect.

Two related but distinct exposures are studied, because they correspond to two different mechanisms.
Own-household WASH asks whether a child's own household having improved water or sanitation is
associated with better anthropometric outcomes, on the logic that improved facilities reduce a child's
direct exposure to faecal pathogens and repeated infection. Surrounding-community WASH asks whether WASH
conditions among other households in the same DHS cluster matter as well, on the logic that a child's own
household facilities may not fully protect against environmental contamination when neighbouring
households lack improved water or sanitation. These two exposures are not interchangeable measures of the
same treatment: one is a household attribute, the other a feature of the child's local environment, and
the empirical strategy treats them accordingly.

## 2. Data, exposures, and unit of analysis

The unit of analysis is the child. Every child belongs to a household, every household to a DHS survey
cluster, every cluster to one administrative region, and every region to one of the four countries. The
data pool the most recent DHS round available for each country: Ethiopia (2024–25), Ghana (2022), Kenya
(2022), and Nigeria (2024). Outcomes are height-for-age (HAZ), weight-for-age (WAZ), and weight-for-height
(WHZ).

Four exposures are constructed: own-household improved/non-improved water, own-household
improved/non-improved sanitation, and their community counterparts. The community measures are
leave-one-out: for each child, community coverage is calculated from every other household in the same DHS
cluster, excluding the child's own household, using the DHS household census rather than an average over
the children in the analytical sample. Household WASH is therefore a household-level attribute, while
community WASH is a cluster-level, contextual measure that varies mainly between clusters rather than
within them — a distinction that matters directly for which fixed effects can be used with each exposure,
discussed below. DHS cluster coordinates are randomly displaced for confidentiality; this becomes relevant
later when discussing an extension to early-life exposure.

The full pooled, harmonized child file contains 70,231 children nested in 4,481 DHS clusters. These
clusters in turn fall within 114 administrative-region categories across the four surveys — 14 in
Ethiopia, 16 in Ghana, 47 in Kenya, and 37 in Nigeria. A region is a much coarser unit than a cluster: each
region typically contains dozens of clusters, so the 4,481 and 114 counts describe two different levels of
the same geographic hierarchy rather than two competing counts of the same thing.

None of these three figures — 70,231 children, 4,481 clusters, 114 regions — is the regression sample for
any model. Valid anthropometric measurements are not available for every child, so the outcome-specific
samples are 36,985 (HAZ), 37,260 (WAZ), and 37,088 (WHZ). Comparing the household and community
specifications on identical observations further requires both exposures to be classifiable, giving common
samples of 36,040 (HAZ), 36,308 (WAZ), and 36,145 (WHZ), spread across 4,426 clusters.

## 3. Empirical strategy and identifying variation

Throughout, *i* indexes a child, *h* the child's household, *c* the child's DHS cluster, and *r* the
child's administrative region (each cluster belongs to exactly one region). Five specifications have been
estimated; they are not equally preferred, and the discussion below moves from a baseline to the
specifications that matter most.

**Household WASH, region fixed effects (baseline).**

Y_ihcr = α + β·WASH_ih + X_i'γ + δ_r + ε_ihcr

δ_r is a fixed effect for each of the 114 administrative regions, so it absorbs everything constant within
a region. β is therefore identified only from variation *within* regions: it compares children whose
households differ in WASH status among households located in the same administrative region — including
households in different DHS clusters within that region — net of the included child and household
controls. The limitation is that one region can contain dozens of clusters, so δ_r leaves room for clusters
inside the same region to still differ in local infrastructure, environment, or health-service access —
characteristics that could be related to both household WASH and child nutrition. This motivates the next
specification.

**Household WASH, DHS cluster fixed effects (the main current household specification).**

Y_ihc = α_c + β·WASH_ih + X_i'γ + ε_ihc

α_c is now a separate fixed effect for each DHS cluster rather than each region. Concretely, this compares
two children living in different households inside the same cluster, one with improved WASH status and one
without, while α_c holds constant everything the two households share simply by being in that cluster. β is
identified from differences in household WASH status among households within the same cluster, conditional
on the controls. The cluster fixed effect absorbs observed and unobserved characteristics common to the
cluster — local infrastructure, environment, market access, anything a region fixed effect could not
distinguish between clusters. It does not absorb differences between households within the same cluster:
two neighbouring households can still differ in wealth, education, or behaviour in ways connected to both
their own WASH investment and their children's growth, and none of that is removed by comparing households
within a cluster. The specification therefore remains associational.

One consequence of using cluster fixed effects is that residence (urban/rural) cannot be separately
estimated: every DHS cluster in the data is entirely urban or entirely rural, so residence is absorbed
automatically by α_c. This reflects how DHS clusters are sampled, not an error in the specification.

For this comparison to be informative, own-household WASH status must actually vary within clusters, and
it does: in the estimation sample, about 32% of clusters contain households with different own-water
status, and about 51% contain households with different own-sanitation status. This is the variation that
identifies β.

**Community WASH, administrative-region fixed effects (the current community specification).**

Y_ihcr = α + β·C_(−h,c) + X_i'γ + δ_r + ε_ihcr

C_(−h,c) is the leave-one-out community coverage described above. Because this exposure is essentially a
property of the cluster, β here is identified mainly by comparing clusters with different community
coverage within the same administrative region, net of the same controls. As with the household region-FE
model, unobserved differences between clusters inside the same region are not removed, so this remains an
associational estimate of a contextual exposure, not a causal spillover effect.

**Identification of the community-WASH coefficient.** A natural question is whether the community exposure
could also be estimated with cluster fixed effects, matching what is done for household WASH. It can be,
but the resulting estimate would not be informative. The leave-one-out community rate is itself a
cluster-level quantity: within a given cluster, every child's value differs from every other child's only
because a different household happens to be excluded from each child's own calculation. Measured directly,
the within-cluster standard deviation of this rate is about 0.007 for water and 0.011 for sanitation,
against an overall standard deviation of about 0.35 for both. A cluster fixed effect would absorb nearly
all of the genuine variation in community coverage, leaving a coefficient identified almost entirely by
this small mechanical residual rather than by real differences in community environments. Cluster fixed
effects are central to this strategy — they are how household WASH is identified in Model B — but for the
community exposure specifically, they would remove the variation the estimate is meant to capture.

**Household and community WASH jointly (secondary).**

Y_ihcr = α + β_H·WASH_ih + β_C·C_(−h,c) + X_i'γ + δ_r + ε_ihcr

β_H is the household association conditional on the surrounding community's coverage, and β_C is the
community association conditional on the household's own status. Household and community WASH are fairly
closely correlated in this sample (about 0.75 for water and 0.67 for sanitation), so this specification is
treated as a secondary decomposition rather than a preferred model.

**Current-age heterogeneity (secondary).**

Y_i = α + β·WASH_i + Σ_a θ_a·AgeGroup_ia + Σ_a λ_a·(WASH_i × AgeGroup_ia) + X_i'γ + FE + ε_i

The λ_a terms test whether the association between survey-date WASH and nutritional outcomes differs
across children's current ages — for example, whether the association estimated for a younger child
differs from that for an older child. This is a heterogeneity test on the existing cross-sectional design,
not a reconstruction of what WASH conditions an older child actually experienced during infancy, and it
does not speak to the exposure-timing problem discussed in Section 5.

## 4. Current empirical results

The central question is whether children exposed to better household or community WASH have better HAZ,
WAZ, and WHZ. In the minimally adjusted community models, several associations are positive and
statistically significant, particularly for HAZ. Once socioeconomic controls and
administrative-region fixed effects are added, those associations attenuate substantially. When household
WASH is instead examined by comparing households within the same DHS cluster, the estimates are also
small and, for HAZ, not statistically significant at the 5% level.

| Specification | Water β (95% CI), p | Sanitation β (95% CI), p |
|---|---|---|
| Community, minimally adjusted | 0.447 (0.31, 0.58), p<.001 | 0.472 (0.36, 0.59), p<.001 |
| Community + SES + region FE | 0.033 (−0.08, 0.15), p=.573 | 0.008 (−0.11, 0.13), p=.894 |
| Household + cluster FE | −0.085 (−0.18, 0.01), p=.080 | 0.026 (−0.06, 0.11), p=.574 |

(HAZ; N=36,985 for the community rows and 36,040 for the household-cluster-FE row, reflecting the sample
restrictions described in Section 2.)

Community coverage is measured on a 0–1 scale, so a 10-percentage-point increase corresponds to 0.10×β —
for the adjusted community model, 0.10×0.033 is about 0.0033 HAZ units. Household WASH is binary, so its β
is the adjusted outcome difference between improved and non-improved household status, not a
per-percentage-point change; the two coefficients are not directly comparable in magnitude.

WAZ and WHZ show broadly the same attenuation, with one nuance worth stating precisely. For WAZ, the
minimally adjusted associations (water 0.296, sanitation 0.368, both p<.001) attenuate to 0.066 (p=.146)
and 0.059 (p=.275) after full adjustment, and the household cluster-FE estimates are −0.029 (p=.465) and
0.052 (p=.156). For WHZ, the sanitation association attenuates from 0.121 (p=.005) to 0.076 (p=.165); the
water association, unlike the other cases, is already small and not statistically significant even before
adjustment (0.033, p=.545), and remains so after adjustment (0.057, p=.261) and in the household
cluster-FE specification (0.012, p=.773). Across HAZ, WAZ, and WHZ, the adjusted specifications do not
show a consistent statistically significant protective association between improved WASH and child
anthropometric outcomes, at either the household or the community level. The attenuation shows that the
minimally adjusted associations are sensitive to socioeconomic and geographic adjustment, although the
current analysis cannot determine which factors account for that change. This should not be read as
evidence that WASH has no effect on child nutrition.

**Specification sensitivity: Nigeria.** One estimate changes sign depending on the control set. The
Nigeria community sanitation–HAZ coefficient moves from +0.274 (p=.004) with no controls, to +0.296
(p=.001) with child controls, to −0.457 (p<.001) once socioeconomic controls are added, to −0.184 (p=.035)
with region fixed effects as well. Wealth quintile accounts for the largest single movement in this
sequence, though that shows sensitivity to specification rather than proving wealth is the mechanism. In
the household cluster-fixed-effects specification, the corresponding coefficient is close to zero and
insignificant (β=−0.007, p=.919), so the result should not be read as evidence that improved sanitation
harms child growth in Nigeria.

The current-age heterogeneity tests described in Section 3 comprise 12 individual tests — three outcomes
and two WASH exposures, each estimated under both region and cluster fixed effects. Ten of these twelve
reject the null of no heterogeneity at the 5% level; the two exceptions are both water and WHZ, under
either fixed-effect structure. This indicates that the association with survey-date WASH varies by a
child's current age in most specifications; it is secondary evidence, and, as discussed in Section 5, it
does not identify a developmental mechanism or reconstruct what WASH conditions a child experienced
earlier in life.

## 5. Exposure timing across child birth cohorts

The results above share a common measurement feature. Own-household WASH is recorded at the DHS household
interview, and community WASH is constructed from other households interviewed in the same survey round;
both are therefore observed once, at the survey date, and applied to every child in that round regardless
of the child's age. Suppose two children are interviewed in the same 2022 survey: a four-year-old and an
infant. Both are assigned WASH measured around 2022. But the four-year-old experienced infancy around
2018–2019, in conditions the current data cannot describe, while the infant's early life is much closer to
the survey date. Age controls or age interactions, including Section 3's heterogeneity model, describe how
the current association varies with a child's current age; they do not reconstruct what each child's
environment actually was during the developmental period relevant to their own growth. These are different
questions: does the association with today's WASH differ by how old a child is today, versus what WASH
conditions did this particular child experience at the relevant point in their own early life. The current
design can answer the first question but not the second.

## 6. Extending the design to early-life WASH exposure

Suppose two children live in the same DHS cluster but were born several years apart — one in 2018, one in
2022. If local WASH conditions genuinely changed between those two periods, the two children could have
experienced different WASH environments during the same stage of their own development, despite sharing a
location. Same location, different birth cohorts, and WASH that changes over calendar time together could
potentially provide within-location temporal variation in early-life WASH exposure that is unavailable in
the current survey-date community measure: a cluster fixed effect could in principle absorb whatever is
persistent about that location, leaving β to be identified from how WASH in that location changed across
the years the two children were born into.

Conceptually:

Y_ic = α_c + β·HistoricalWASH_ic(w) + X_i'γ + τ_b + ε_ic

HistoricalWASH_ic(w) would be the WASH condition assigned to child *i* in cluster *c* during a common
developmental window *w* tied to that child's own birth date — candidates include the first year after
birth and the prenatal period, with the choice left open here on theoretical grounds — and τ_b would be
birth-cohort or calendar-time controls with no counterpart in the models above.

Whether this design would actually work cannot be answered without the data. It would require a historical
or time-varying WASH source with enough temporal and spatial resolution to distinguish different years
within the same cluster; coverage of the relevant birth years in all four countries; compatibility with
DHS's randomly displaced cluster coordinates; a WASH measure that is substantively meaningful rather than a
coarse proxy; independence from DHS data itself, to avoid circularity; and, above all, genuine
within-location temporal variation once all of that is in place. None
of this has been assessed, because no candidate dataset has yet been identified.

A related design appears in Blom, Ortiz-Bobea and Hoddinott (2022), who match historical, geocoded weather
data to each child's own developmental window across repeated DHS rounds. This illustrates the matching
logic for a different exposure — temperature, which is continuously observed over time, unlike WASH in
this project — not evidence about WASH and nutrition.

No suitable historical or time-varying WASH dataset has yet been identified and verified for this project,
so this specification has not been estimated. Its feasibility must first be established before any results
from it could be reported.

## 7. What the current analysis tells us and what remains unresolved

The analysis asks whether better own-household and surrounding-community WASH are associated with better
child anthropometric outcomes. The minimally adjusted community models show sizeable positive
associations, particularly for HAZ. These attenuate substantially once socioeconomic and geographic
controls are added. The household cluster-fixed-effects specification, which compares households with
different WASH status within the same DHS cluster, likewise does not show a consistent statistically
significant protective association. The large, simple relationship visible before adjustment is therefore
not robust across the more demanding specifications — though this does not by itself prove that the
original relationship was purely confounding.

Nor does it establish that WASH has no causal effect on child nutrition. For community WASH, identification
still relies mainly on differences between clusters within the same administrative region, so unobserved
cluster-level differences may remain. For household WASH, cluster fixed effects remove characteristics
shared by the local cluster but cannot remove every unobserved household-level difference. And WASH
throughout is measured at the survey date rather than during a common developmental period for each child,
so the timing problem in Section 5 is unresolved by any of the current specifications. The next
methodological question is whether credible historical or time-varying WASH data could construct a
comparable early-life exposure and provide meaningful within-location temporal variation. If no such data
can be found, the current DHS evidence should remain explicitly interpreted as cross-sectional
associations — not as evidence for or against a causal effect of WASH on child growth.
