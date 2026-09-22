# Literature-to-Empirical-Design Gap Audit

This document assesses the consistency between the project's literature evidence base and the empirical
design actually implemented. All claims below are drawn directly from `sources/bibliography/` and
`sources/summaries/` (the git-tracked, verified copy — see §1) and, where explicitly noted, the
underlying source PDFs already deep-read and quoted in that evidence matrix. Nothing here is inferred
from a title alone.

---

## 1. Reference integrity status

- **Source count:** 35 (S01–S35), confirmed directly from `literature_master_inventory.csv`,
  `bibliography_source_audit.csv`, and `literature_evidence_matrix.csv` (all three: 35 data rows).
- **IDs:** S01–S35 contiguous, no gaps, no duplicates.
- **Verification status:** every one of the 35 rows in `bibliography_source_audit.csv`'s
  `metadata_verified_from_pdf` column reads "Yes" (full-text read, partial read with pages specified, or
  Crossref-confirmed) — none unverified.
- **Outstanding reference-integrity warnings:** none. The `discrepancy_notes` column contains 35
  non-blank entries, but on inspection every one is either "None found" or a **resolved** historical
  note (e.g., S06's 2006-vs-2007 year clarification, S28's "Donohoe→Donohue" spelling correction, S18's
  explicit working-paper-vs-published-article flag, S33's uninformative filename note). No entry
  describes a live, unresolved problem. This matches the prior full bibliographic audit's conclusion
  (zero critical/high-severity errors).
- **New observation this stage (not a correction, a disclosure):** the project currently has **two
  non-identical copies** of the bibliography/summary CSVs — one under the git-tracked
  `thesis-wash-child-nutrition-dhs/sources/` (this report's source, containing the richer, corrected
  provenance wording from the earlier bibliographic-correction stage) and one under the master working
  directory's `sources/` (same 35 sources, same IDs/titles/authors/findings, but older/generic provenance
  wording, e.g. "Included in the initial literature collection" instead of "Original 25 (prior literature
  audit)"). The **substantive content is identical** — same sources, same findings, same numbers — only
  provenance/status phrasing differs, and only in the git-tracked copy has that phrasing been updated to
  reflect the corrections already applied. Recommend using the git-tracked copy as authoritative and
  syncing the master copy in a later documentation pass (not done here, per the read-only rule).

---

## 2. Existing literature composition

35 sources spanning: nutrition burden/measurement (S01–S03, S06, S25–S27), WASH-nutrition primary
studies and reviews (S05, S07, S08, S10–S13, S15, S18, S19, S28, S33, S34), DHS/GIS methodology
(S29–S32), a non-WASH heat-exposure econometric analogue (S04), country-context/policy reports (S14,
S16, S20–S24), a geospatial-precipitation dataset paper (S17), and two aid/mortality panel-design
contrast cases (S16, S35). 17 of 35 are tagged `priority=Core`, the rest `Supporting` or `Background`.
No source was added, removed, or re-tagged in this audit.

---

## 3. Source-to-claim matrix

Organized by category (only STRONG/PARTIAL classifications shown, with a short evidence note; sources
not listed under a category are NO/UNCLEAR for it — omitted for space, per the size of a full 35×25
grid). All notes are drawn verbatim/near-verbatim from the verified evidence matrix, not paraphrased
into stronger claims.

**1. Biological/environmental mechanism (WASH→infection→growth):**
S07 STRONG (Cochrane synthesis: WASH RCTs → HAZ 0.08 SD overall, 0.25 SD <2y); S08 STRONG (systematic
review of the mechanism literature, 46 SSA studies); S10 STRONG (states the mechanism explicitly while
reporting null RCT effects — cuts both ways, see §9); S18 PARTIAL (neighbor open-defecation→infection→
mortality pathway, not growth); S33 PARTIAL (WASH→diarrhea pathway tested directly, not growth); S34
PARTIAL (implicit environmental-enteric-dysfunction framing, not the paper's main test).

**2. Household-level water and child nutrition:**
S11 STRONG (Kenya, household JMP water ladder→LAZ, β=0.13 p<.01); S13 STRONG (Ghana, unprotected
water→wasting AOR=2.55); S33 PARTIAL (household water technology→diarrhea/mortality, not anthropometry);
S16 PARTIAL (household water as a control in a mortality model).

**3. Household-level sanitation and child nutrition:**
S13 STRONG (Ghana, sanitation→stunting/wasting AORs); S28 STRONG (Nigeria/Zambia, household sanitation
tested — not significant once community coverage added, itself informative, see §6); S05 PARTIAL
(community-aggregated toilet type, not strictly household).

**4. Community/neighbourhood sanitation coverage and child nutrition:**
S28 STRONG, DIRECT (Nigeria: community sanitation coverage→stunting, adjusted OR=0.97 per 10pp,
p<.05); S12 STRONG, DIRECT (Ghana+Nigeria: community toilet coverage→HAZ, urban positive/significant,
rural negative — see §6); S34 STRONG, DIRECT (village open-defecation→HAZ, includes Ethiopia/Kenya/
Nigeria, not Ghana); S19 PARTIAL (subnational-*region*-level, coarser than cluster, sanitation→stunting/
mortality panel).

**5. Community/neighbourhood water coverage and child nutrition:**
S12 STRONG, DIRECT (community water coverage tested, though less emphasized than its sanitation result);
S19 PARTIAL (subnational water coverage→stunting, coefficient not significant in the survey-FE
specification); S9 PARTIAL (geospatial water-access inequality mapping, not a nutrition regression).

**6. Community WASH spillovers/externalities/environmental exposure:**
S18 STRONG, DIRECT (the project's only true leave-one-out precedent — neighbor OD rate→own infant
mortality, explicit "leave-out mean" construction and equation); S33 STRONG (explicit externality test:
cluster-level sanitation coefficient >2× household coefficient); S12 PARTIAL ("externalities" in the
paper's own title/framing, but own-inclusive, not LOO); S28 PARTIAL (same own-inclusive caveat).

**7. Household-vs-community distinction:**
S18 STRONG (household and LOO-neighbor terms entered jointly — the closest precedent to Development
Model C); S34 STRONG (household and village terms entered jointly); S12 STRONG (explicitly frames the
choice between own-inclusive and leave-one-out as "an empirical question" it does not resolve); S28
PARTIAL (both levels tested, household loses significance once community is added — informative but not
framed conceptually as a household-vs-community question); S33 PARTIAL (magnitude-ratio comparison, not
a joint-model framing).

**8. Child age/developmental heterogeneity in WASH/nutrition relationships:**
S07 PARTIAL (reports a different HAZ effect size for <2y vs. overall — a descriptive split, not a
formal interaction test); S11 PARTIAL (restricts sample to 6–23 months by design, reflecting a
developmental-window belief, not a within-sample heterogeneity test); S04 PARTIAL (restricts to 3–36
months; separately models chronic vs. acute outcomes by construction, not a WASH×age interaction).
**No source formally tests a WASH×age interaction the way Stage 2 did** — see §7/§12.

**9. First 1,000 days / early-life nutritional vulnerability:**
S01 STRONG (the "window of opportunity" / growth-faltering-timing source); S02 STRONG (canonical
Lancet framing); S03 STRONG (life-course consequences of early HAZ); S07 PARTIAL (early-childhood <2y
WASH effect).

**10. Exposure timing / historical exposure measurement:**
S04 PARTIAL (uses genuinely time-varying, historically-resolved *heat* data linked to birth timing —
the closest available methodological analogue, not a WASH precedent). **No source addresses historical/
time-varying WASH exposure reconstruction** — genuine gap, see §8/§12.

**11. DHS child anthropometry methodology:** S32 STRONG (hv/v variable definitions); S06/S25 STRONG
(WHO standards underlying HAZ/WAZ/WHZ construction).

**12. HAZ interpretation/stunting:** S01, S02, S03, S05, S06, S25 all STRONG.

**13. WAZ interpretation/underweight:** S06, S25 STRONG (construction); S02 PARTIAL (general framing).

**14. WHZ interpretation/wasting:** S04 STRONG (uses WHZ as a primary outcome); S06, S25 STRONG
(construction); S13 STRONG (Ghana wasting outcome).

**15. WHO child-growth standards:** S06, S25 STRONG (HAZ/WAZ/WHZ, the thesis's actual indicators);
S26, S27 PARTIAL (same MGRS methodology family, but for velocity/circumference indicators the thesis
does not use — explicitly flagged low-relevance in the matrix itself).

**16. DHS sampling/survey weights/PSU clustering:** S31 STRONG (Taylor-linearization/JRR variance basis,
pooled-weight de-normalization procedure); S32 STRONG (hv005/v005 definitions, PSU/strata variables).

**17. DHS GPS displacement/geospatial measurement error:** S29 STRONG (displacement distances, admin-2
boundary rule); S30 STRONG (misclassification-rate simulation, weighted-linkage recommendation).

**18. Fixed effects/within-location identification:** S04 STRONG (admin-region FE precedent, explicit
"clusters not repeated" justification); S19 STRONG (independent, more recent admin-region-FE precedent
across 59 countries); S16 PARTIAL (country FE, not admin-region, explicitly excludes Nigeria); S09
PARTIAL (the spatial-grid alternative not adopted).

**19. Repeated cross-sections/pseudo-panel or birth-cohort exposure logic:** S04 STRONG (grid×month×year
FE using repeated DHS rounds); S19 STRONG (subnational panel across repeated DHS rounds); S35 PARTIAL
(genuine country-year panel, contrast case, no WASH content).

**20. Residual confounding/observational WASH identification:** S10 STRONG (the central RCT-vs-
observational tension source); S19 STRONG (explicit "cannot rule out time-varying omitted variables");
S34 STRONG (explicit OVB acknowledgment); S05 STRONG (explicit "could not show causal inferences"); S14
STRONG (explicit non-causal framing, parallel context).

**21. Evidence of beneficial WASH effects/associations:** S07, S11, S13, S28, S12 (urban only), S34,
S33 — all STRONG, each with a specific quoted coefficient.

**22. Evidence of null/weak/mixed/context-dependent WASH effects:** S10 STRONG (all 3 major RCTs null
on linear growth); S05 STRONG (Ethiopia water AOR=1.05, not significant); S12 STRONG (rural HAZ
coefficient negative, only urban positive); S08 STRONG (mixed: significant in 21/46 and 15/46 reviewed
studies only); S15 STRONG (null stunting result, flagged by the paper's own authors as anomalous); S28
STRONG (household sanitation not significant once adjusted; only 2 of 6 Nigerian zones significant).

**23. Sub-Saharan Africa relevance:** S04, S05, S08, S12, S13, S14, S16, S20, S21, S22, S28, S34 (partial)
— broad coverage, see §11/§P for the important caveat about *combined four-country* coverage.

**24. Country-specific relevance** — see §11 below for the full breakdown.

**25. Policy relevance:** S02, S09, S19, S21, S22, S23, S28 — STRONG, official/policy-oriented sources.

---

## 4. Household WASH coverage

**ADEQUATELY COVERED.** Direct household-level WASH→anthropometry regressions exist for Ghana (S13),
Kenya (S11), and (as a control/comparator) Nigeria/Zambia (S28), plus the broader household-technology→
health evidence in S33 and S16. Ethiopia's direct household-WASH evidence is thinner (S05 uses a
community-aggregated, not household, measure, and finds no significant association) — this is itself a
useful, disclosed null finding, not a gap in coverage.

## 5. Community WASH coverage

**ADEQUATELY COVERED for sanitation, THINNER for water specifically.** S28 (Nigeria), S12 (Ghana+
Nigeria), S34 (Ethiopia/Kenya/Nigeria, no Ghana), and S19 (59-country subnational panel) together give
solid direct precedent for community-level *sanitation* coverage and child growth/health. Community
*water* coverage evidence is comparatively thinner: only S12 tests it directly (secondary to its
sanitation result) and S19's water coefficient was not significant in its preferred specification. This
asymmetry mirrors the thesis's own results (community sanitation literature is richer than community
water literature) and should be named explicitly rather than glossed over.

## 6. Household-vs-community evidence

**ADEQUATELY COVERED — this is the strongest, most directly relevant thread in the entire literature
base for the thesis's current architecture.** S18 (Geruso & Spears) is the only true leave-one-out
precedent found and explicitly enters household + neighbor terms jointly, exactly mirroring Development
Model C's structure (different domain: infant mortality, India). S34 (Spears 2013) does the same with
household + village terms. S12 and S28 both estimate household and community sanitation *side by side*
and both find the household term loses significance once community coverage is added (S28: household
aOR=1.09 n.s. once community coverage entered; S12: frames the household/community choice as an
unresolved empirical question) — a real, literature-documented precedent for exactly the pattern Stage 2
found in the thesis's own joint model (household coefficient becoming more prominent once community
coverage is included). **Distinguishing DIRECT vs. INDIRECT vs. NOT RELEVANT, per the request:**

- **DIRECT** (paper actually studies community/contextual WASH): S12, S18, S28, S34, S19, S33 (secondary
  externality test).
- **INDIRECT** (supports the environmental mechanism without estimating community WASH): S07, S08, S10.
- **NOT RELEVANT** (household-only, no community implication): S11, S13, S05, S16 (WASH as controls
  only).

**Is there enough DIRECT literature to motivate the LOO exposure specifically?** Partially. There is
strong DIRECT literature motivating *community-level WASH coverage as a meaningful exposure distinct
from household WASH* (S12, S28, S34, S19, S33). There is only **one** source (S18) that uses a genuine
leave-one-out construction, and it is in a different country/outcome domain. The matrix itself already
flags this precisely: S12, S28, S33, and S34 must be cited as precedent for *community-level exposure*,
not as validating the *leave-one-out* construction specifically — only S18 does that, and even S18
should be cited with its domain/geography caveat stated plainly.

## 7. Age/developmental literature

**A. Literature supports broad developmental heterogeneity:** YES — S01, S03, S07 (the <2y vs. overall
HAZ-effect split) establish that early childhood is a period of heightened nutritional vulnerability in
general, and specifically for WASH in S07's case.

**B. Literature supports the exact age categories used in Stage 2 (0–5/6–11/12–23/24–35/36–47/48–59):**
NO. These bands were built as a diagnostic device for this thesis (explicitly labeled as such in Stage
2), not retrofitted from a paper that uses them. S11 uses 6–23 months as an analytic restriction (a
different, narrower window, chosen for its own reasons); S04 uses 3–36 months. Neither matches the
thesis's six bands, and no source formally tests a WASH×age interaction at all. **This is a genuine, if
modest, gap** — the age-heterogeneity finding in Stage 2 currently has no direct WASH-specific
precedent to be compared against, only general developmental-vulnerability literature (S01/S03) and one
descriptive age-split (S07).

## 8. Historical exposure / Blom methodology

**What can legitimately be adapted from Blom, Ortiz-Bobea & Hoddinott (2022, S04):** the
continuous-primary/binary-robustness outcome tiering (already mirrored in the thesis); the
admin-region-FE-over-spatial-grid justification, explicitly grounded in "DHS clusters not repeated"
(already mirrored); the general idea of a defined analytic age window (their 3–36 months) as a
deliberate design choice; explicit acknowledgment of GPS-displacement and survivor-selection risk
(directly relevant to the thesis's own §B/§9 selection-diagnostic discussion).

**What cannot be transferred directly:** heat is not WASH — S04's exposure of interest is temperature;
household water/latrine appear in S04 only as controls, never as the exposure, so **S04 does not
validate the thesis's WASH exposure construction, only its FE/tiering choices** (this exact caveat is
already recorded in the verified matrix and must not be dropped in any future draft). Weather is
naturally high-frequency and continuously observed for decades; WASH coverage is not similarly available
as a historical series in this project (§10 of the prior audit, reconfirmed here — no historical WASH
data exists in the repository, and this audit found none among the 35 sources either). S04's repeated-
DHS-round structure (15 rounds, 1993–2014) is structurally different from the thesis's one-round-
per-country design; do not describe Blom's grid×month×year FE as something the thesis's design could
adopt without first acquiring genuinely time-varying WASH data. **S04 must never be described as
evidence that WASH improves nutrition** — it says nothing empirical about WASH's effect; every mention
of it in prior work correctly restricts its role to methodology.

## 9. Null and mixed WASH evidence

**ADEQUATELY COVERED, and this is important given the thesis's own mostly-null results.** S10 (Cumming
et al. 2019 consensus statement) is the anchor: all three major cluster-randomized trials (WASH-Benefits
Bangladesh, WASH-Benefits Kenya, SHINE Zimbabwe) found **no causal effect** of basic WASH interventions
on child linear growth — a genuine causal null, not an artifact of weak observational design. This is
already flagged in the matrix as the "critical tension source" requiring explicit engagement, not
glossing-over. Supporting the null/mixed side further: S05 (Ethiopia, non-significant household water);
S08 (systematic review: only 21/46 and 15/46 reviewed studies find significant water/sanitation
associations respectively); S12 (rural HAZ association negative, only urban positive); S28 (household
term loses significance once community coverage is controlled; only 2 of 6 Nigerian zones significant).
Priority sources for this discussion, ranked: S10 (RCT consensus — highest evidentiary weight), S08
(systematic review), S05/S12/S28 (DHS observational nulls/mixed results directly comparable in design
to the thesis). **The thesis's own predominantly null/weak adjusted associations can be discussed as
consistent with, not contradicted by, this existing literature** — this is a defensible, literature-
grounded framing, not something that needs new sources to support.

## 10. Identification and causal-language literature

| Methodological statement needed | Supported by | Adequacy |
|---|---|---|
| Cross-sectional DHS associations are not automatically causal | S05, S14, S34 (explicit statements), S10 (causal RCT vs. associational tension) | ADEQUATE |
| Region FE do not eliminate within-region cluster confounding | Not explicitly stated by any source as a general methodological point — inferred from S04/S19's own admin-region-FE limitations sections, which discuss what their FE does and does not absorb | THIN — see gap below |
| Cluster FE remove cluster-level time-invariant confounding | S18's design (household + LOO-neighbor jointly) implicitly demonstrates this logic but does not state it as a general methodological principle | THIN |
| Household-level confounding can remain under cluster FE | Not directly stated by any source; this is Stage 2's own reasoning, consistent with but not sourced from the literature | GAP |
| Historical exposure timing matters | S01/S03 (general developmental timing), S04 (methodological analogue) — general support, no WASH-specific source | THIN |
| GPS displacement may attenuate geospatial relationships | S29, S30 STRONG — direct, quantified, exactly on point | ADEQUATE |

**Genuine gap flagged:** none of the 35 sources is an econometrics/methods reference that explicitly
states, in general terms, why a cluster (or region) fixed effect controls for shared-but-not-individual
confounding while leaving household-level confounding unaddressed. This is currently supported only by
the logic of the design itself (correctly reasoned in Stage 2's own report) and by *inference* from
applied papers (S04, S18, S19), not by a citable methodological statement. This is a minor gap for an
introduction (the applied precedents are enough to write the paragraph) but would benefit from one
general fixed-effects/panel-econometrics methods citation if the thesis later wants a more textbook-level
identification discussion. **No econometric citation is invented here to fill this gap.**

## 11. Country and SSA coverage

| Country | Direct WASH-nutrition sources | Assessment |
|---|---|---|
| Ethiopia | S05 (community-aggregated, null result); S21/S17/S34 (context/validation only) | THIN BUT USABLE — one direct source, and it's a null result (itself useful for §9) |
| Ghana | S04, S12, S13, plus S06/S25 (MGRS site), S16, S21, S22 | ADEQUATELY COVERED |
| Kenya | S11 (single direct source); S10 (RCT site, intervention not coverage); S34 (included); S21 | THIN BUT USABLE — only one direct coverage→anthropometry regression |
| Nigeria | S28 (strong, direct, with regional breakdown), S12, S14, S34, S21–S23; **explicitly excluded from S16** | ADEQUATELY COVERED |

**Broader SSA framing (§10 of the request):** the literature base includes genuinely pan-SSA evidence
(S08: 46 SSA studies; S09: 88–89 LMICs incl. most of SSA; S21: JMP SSA aggregates), which supports
discussing SSA-wide patterns and context in the introduction/background. **It does not, however, support
describing the thesis's own empirical results as generalizable evidence "for Sub-Saharan Africa"** — no
single source studies exactly Ethiopia+Ghana+Kenya+Nigeria together, one country (Nigeria) is explicitly
excluded from one otherwise-relevant regional source (S16), and the thesis's own four countries were
selected for DHS-round recency, not representativeness. **Recommend the more precise framing "evidence
from four Sub-Saharan African countries" (or naming them) rather than unqualified "Sub-Saharan African
evidence."** This is a wording/framing flag for supervisor discussion, not a request to rename the
thesis.

---

## 12. Genuine literature gaps

| Area | Status |
|---|---|
| A. WASH–nutrition mechanism | ADEQUATELY COVERED |
| B. Household WASH | ADEQUATELY COVERED |
| C. Community WASH | ADEQUATELY COVERED (sanitation); THIN (water-specific) |
| D. Household/community distinction | ADEQUATELY COVERED |
| E. Child-age heterogeneity | THIN BUT USABLE |
| F. First-1,000-days/early-life timing | ADEQUATELY COVERED |
| G. Historical exposure methodology | **GENUINE GAP** |
| H. DHS anthropometry | ADEQUATELY COVERED |
| I. DHS geospatial displacement | ADEQUATELY COVERED |
| J. Fixed-effect/identification logic | THIN BUT USABLE (applied precedent strong; general methodological statement absent — §10) |
| K. Null/mixed WASH evidence | ADEQUATELY COVERED |
| L. Ethiopia context | THIN BUT USABLE |
| M. Ghana context | ADEQUATELY COVERED |
| N. Kenya context | THIN BUT USABLE |
| O. Nigeria context | ADEQUATELY COVERED |
| P. Broader SSA framing | THIN BUT USABLE (see §11 caveat) |

---

## 13. Exact additional-publication needs

**GAP 1 — Historical/time-varying WASH exposure reconstruction (area G).**
NEEDED: 1–2 methodological or applied papers documenting a spatially- and temporally-resolved WASH
coverage product (e.g., a gridded or subnational time series built from repeated JMP/DHS/MICS rounds)
with a demonstrated method for linking it to individual birth cohorts' early-life windows.
WHY: Required before Development 6 (historical WASH) can be scoped at all — currently blocked on
dataset identification, not just literature.
SEARCH PRIORITY: MEDIUM (not blocking the introduction — this extension is already explicitly deferred).

**GAP 2 — Direct WASH×age-heterogeneity test in comparable data (area E).**
NEEDED: 1–2 peer-reviewed studies from DHS/MICS or comparable LMIC contexts that formally test (via
interaction terms or a rigorous stratified comparison, not just a sample restriction) whether the
WASH-anthropometry association differs by child age.
WHY: Needed to situate Stage 2's own joint-test heterogeneity finding against prior work — currently it
can only be compared to general developmental-timing literature (S01/S03), not WASH-specific
heterogeneity literature.
SEARCH PRIORITY: MEDIUM.

**GAP 3 — Direct community WATER coverage → anthropometry evidence (area C, water-specific).**
NEEDED: 1 additional study focused specifically on community/cluster-level water coverage (not
sanitation) and child anthropometric outcomes, ideally DHS-based.
WHY: Balances the currently sanitation-heavy direct-community literature (S28, S34 are sanitation-only)
so the introduction does not implicitly over-justify `sanitation_rate_loo_core` while under-justifying
`water_rate_loo`.
SEARCH PRIORITY: MEDIUM.

**GAP 4 — Kenya-specific WASH-nutrition breadth (area N).**
NEEDED: 1–2 additional Kenya-inclusive (or East-Africa DHS) WASH→anthropometry studies.
WHY: Reduces reliance on a single source (S11) for all Kenya-specific empirical framing.
SEARCH PRIORITY: LOW–MEDIUM (S11 alone is solid and directly on point; this is a robustness-of-citation
concern, not a blocking gap).

**Target total: 5–7 additional sources across all four gaps** — a modest, targeted number, not a
general literature expansion. None of these four gaps blocks drafting the introduction (see §17).

---

## 14. Introduction-ready source set

| Heading | Source IDs | Contribution | Introduction-strong? | Must NOT claim |
|---|---|---|---|---|
| 1. Why child undernutrition matters | S02, S03, S01 | Burden of disease; life-course consequences of HAZ; growth-faltering timing | YES | That these are WASH studies — they are not |
| 2. Why WASH could affect nutrition | S07, S08, S18 | Biological/infection mechanism; SSA-specific review; externality mechanism | YES, with caution | That the mechanism guarantees a detectable effect at DHS-cross-section scale — S07's own RCT numbers are small (0.08–0.25 SD) |
| 3. What previous WASH/nutrition evidence finds | S10, S34, S28, S11, S13, S12 | Both the causal RCT null (S10) and DHS-observational associations (S34/S28/S11/S13/S12) | YES — use both sides together, never S10 alone or the positive set alone | Cherry-picking either side |
| 4. Why household and community WASH may differ | S12, S18, S34, S33 | Direct joint household+community precedent, incl. the "empirical question" framing (S12) | YES | That S18/S34's household+community joint estimates are causal — they are not (S18 uses an IV for its causal claim in a different context; S34 is explicitly non-causal) |
| 5. Why child age/timing may matter | S01, S03, S07 | General early-life vulnerability framing | YES, general only | That this literature establishes WASH-specific age heterogeneity — it does not (§7); that is the thesis's own finding |
| 6. What DHS/geospatial literature contributes | S29, S30, S31, S32, S06/S25 | Displacement mechanics, weighting/clustering basis, HAZ/WAZ/WHZ construction | YES | That S06/S25's MGRS reference population (unconstrained-growth-screened, not representative) validates anything beyond z-score construction |
| 7. Why identification remains challenging | S10, S19, S05, S14, S34, S04 | Causal-vs-associational tension; explicit OVB caveats across multiple contexts | YES | That any of these sources make the thesis's own design causal — none do |
| 8. How our thesis contributes | (synthesis of S12, S18, S28, S33, S34) | These sources collectively show the household/community distinction and LOO technique exist *separately* elsewhere, but not combined exactly as the thesis does, across these four countries, for continuous anthropometry | Frame cautiously — see §15 | "First," "novel," or "unique" — not supported |

Aim achieved: 12 distinct source IDs (S01, S02, S03, S04, S05, S06/S25, S07, S08, S10, S11, S12, S13,
S14, S18, S19, S28, S29, S30, S31, S32, S33, S34 appear across the table — a focused set drawn from
roughly two-thirds of the 35, not all of them, and not a fixed "top 10" list since different headings
legitimately need different sources).

---

## 15. Defensible contribution statement

Testing: *"This thesis distinguishes own-household WASH conditions from surrounding community WASH
coverage and examines their associations with child anthropometric outcomes across four recent DHS
surveys, while investigating within-cluster household comparisons and age heterogeneity."*

- **"Distinguishes own-household WASH from community WASH coverage"** — factual description of Stage-2
  work (true). As a novelty claim: NOT novel as a *concept* — S12, S18, S28, S33, S34 all do this
  distinction already, in other countries/outcomes. Defensible framing: *"applies an
  already-established household/community distinction to a setting where it has not previously been
  applied this way."*
- **"Examines... across four recent DHS surveys"** — factual (true). As a novelty claim: no source among
  the 35 verified references studies exactly Ethiopia+Ghana+Kenya+Nigeria together with a
  household-vs-community WASH design; this combination is plausibly under-studied *within the verified
  literature base*, but Stage 3 conducted no internet search, so this cannot be asserted as globally
  unstudied — only as "not found among 35 systematically verified sources."
  Defensible framing: *"contributes new evidence from a four-country combination not covered in the
  reviewed literature."*
- **"Within-cluster household comparisons"** (household+cluster FE) — factual description of Model B.
  As a novelty claim: the *technique* (household + leave-one-out neighbor term) is directly precedented
  by S18 (India, infant mortality) and S34 (household+village, cross-country). Not a novel method;
  novel only in domain (SSA child anthropometry) and country set. Defensible framing: *"adapts an
  established leave-one-out identification technique (Geruso & Spears) to child anthropometric
  outcomes in Sub-Saharan Africa."*
- **"Age heterogeneity"** — factual description of Stage 2's heterogeneity tests. This is the
  **weakest-supported** component for a novelty claim: no WASH-specific precedent exists for a formal
  age-interaction test (§7, GAP 2). Defensible framing: *"explores age heterogeneity in this
  association, an underexplored dimension in the reviewed literature"* — explicitly modest, not "first
  to test."

**Overall verdict:** the combination is plausibly under-studied *as verified against these 35 sources*,
which supports a "contributes by examining/applying/adapting" framing throughout. **Do not use "first,"
"novel," or "unique" anywhere** — the literature base can support "not found in the reviewed literature"
or "contributes new evidence," which is a materially weaker and fully defensible claim, not the same as
"establishes this is the first study."

---

## 16. Claims we must NOT make

- WASH "improves" or "causes" better nutrition — S10's causal RCT evidence is null; the thesis's own
  design is associational (already established in the empirical audits).
- Blom et al. (S04) as evidence WASH affects nutrition — it studies heat, not WASH; WASH appears only as
  a control.
- Any of S12/S18/S28/S33/S34's household+community joint estimates as causal spillover/externality
  effects — only S18 has a causal (IV) claim, and only for its own India/mortality context, not
  transferable to this thesis's cross-sectional design.
- That the thesis's four countries constitute representative "Sub-Saharan African" evidence in general —
  use "evidence from four Sub-Saharan African countries" instead (§11).
- That the reviewed literature establishes WASH-specific age heterogeneity as an expected/known pattern —
  it does not; only general early-life vulnerability is established (§7).
- That S06/S26/S27's WHO growth-standard reference population validates general population
  applicability — the MGRS sample was deliberately screened for "unconstrained growth," not
  representative.
- "First," "novel," or "unique" for any component of the contribution statement (§15).
- That S16's country-FE, non-PSU-clustered design or S19's genuine multi-round panel validate the
  thesis's own cross-sectional, PSU-clustered, single-round design as equivalent — both are structurally
  different and each source's own matrix entry says so explicitly.

---

## 17. Is the literature sufficient to draft the supervisor introduction?

**YES — sufficient for drafting, but targeted additions needed before final thesis.**

The core narrative the introduction needs — why undernutrition matters, why WASH could plausibly matter,
what prior WASH/nutrition evidence finds (both positive and null), why household and community WASH are
conceptually distinct, why identification is hard, and what DHS/geospatial methodology underpins the
design — is all solidly and specifically supported by verified sources already in hand (§3–§10, §14).
Two areas are explicitly thin rather than empty (age-heterogeneity precedent, Kenya-specific breadth),
and one is a genuine, already-acknowledged-as-deferred gap (historical exposure methodology, not needed
for the current architecture). None of these three blocks a defensible introduction draft: the
introduction can accurately state that age heterogeneity is "an underexplored question this thesis
examines" and that Kenya's country-specific framing rests on one directly-verified source plus general
DHS/regional context — both are honest, citable framings, not gaps that need to be silently papered
over. The four targeted gaps in §13 (5–7 additional sources) should be pursued before the *final* thesis
for a more balanced citation base, particularly Gap 3 (community water evidence, to match the
sanitation-heavy direct literature) and Gap 2 (age-heterogeneity precedent) — but their absence does not
prevent writing an accurate, appropriately-hedged 2–3 page introduction now.
