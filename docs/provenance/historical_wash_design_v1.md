# Historical Local WASH Extension — Design Note, Version 1 (Draft, pre-estimation)

Status: design draft prepared before any historical exposure has been constructed or any outcome
regression estimated. Nothing in this note reports a result. Decisions marked OPEN are not yet
locked. This note supplements, and does not replace, `docs/empirical_strategy.md` §6 and
`docs/provenance/historical_wash_feasibility_audit.md`.

## A. Research question and interpretation

The historical layer asks whether children exposed during a defined early-life window to higher
modelled local coverage of improved water (or sanitation) differ in later anthropometric status,
after comparisons among children in the same survey cluster and after broad calendar controls.

The exposure is a modelled, area-level, annual coverage estimate for the location of a child's
survey cluster. It is not observed household WASH and not the leave-one-out community measure of
the current analysis (which uses same-round household census data at the survey date). The three
measures therefore answer different questions and are not interchangeable.

## B. Exposure timing

Primary window (proposed): mean modelled coverage over the first 12 completed postnatal months, i.e.
the 12 months beginning at the birth month. Rationale: a single early-life window at a fixed,
biologically motivated age, applied identically to all children, which avoids choosing a window by
its results. Literature support for the exact window must be documented before estimation (OPEN).

Sensitivity set (pre-specified, not selected by results):
- Birth-year value (annual coverage in the calendar year of birth).
- Prenatal window: the nine months before birth (cannot be a full-year value; see the month-weighting rule).
- First 24 postnatal months (distinct from the first 1,000 days, which also includes pregnancy).

Mapping of birth dates to annual rasters: each window is a set of calendar months. Annual values
are weighted by the number of window months falling in each calendar year. Example: a window
starting in October covers three months of the birth year and nine of the following year.
Weighted exposure = sum over calendar years of (months in year / window months) × annual coverage.

Completeness rule: a child contributes to a window only if every calendar year it touches has a
verified raster and the window has been completed by the interview date. Children whose window is
incomplete at interview are excluded from that window, not assigned partial exposure. Children
with missing birth month are excluded from month-based windows (birth-year-only sensitivity may
retain them if the year is known).

No extrapolation: years outside the verified raster range (2000–2017) are unavailable. A window
requiring any unavailable year is excluded. Nothing is carried forward or interpolated.

Note: coverage of a birth year does not establish coverage of a multi-year window; each
window must be checked against the full set of years it touches.

## C. Spatial assignment

Primary rule (proposed): mean of valid pixels within a buffer around the displaced cluster
coordinate, with buffer radius matched to the DHS displacement rule (urban 2 km, rural 5 km),
computed in a metric projection (for example an equal-area or local UTM projection chosen for the
study extent). Buffers must not be computed in degrees.

Sensitivity: (i) point extraction at the displaced coordinate, (ii) a larger rural radius (for the
1% of rural clusters displaced up to 10 km) as a robustness check only.

Coordinate order: longitude then latitude in the stored raster geotransform (EPSG:4326). Coordinate
inputs must be verified for order and range before extraction.

NoData (-999999 in these rasters) is never assigned a zero. Buffers containing only NoData are
flagged, not averaged to zero. The valid fraction of each buffer is recorded.

Limitations: displacement means the true cluster location is not recovered by any buffer. The
rasters are ~4.6 km, comparable to the displacement scale, so pixel assignment near boundaries is
uncertain. Current residence is used as a proxy for historical residence; migration between birth
and interview is not observed, and this is reported as a limitation.

## D. Empirical specification (proposed; not estimated)

For child i in survey-cluster c of survey s, country k, birth cohort b, with window exposure E:

    Y_ics = a + beta * E_i + X_i' gamma + lambda_s + tau_k,b + delta_c + e_ics

- Y: HAZ, WAZ or WHZ (Z-score units; never percentages or centimetres).
- E: one exposure per estimand (water or sanitation), entered separately; joint models only as a
  secondary decomposition.
- X: child and household characteristics measured at interview. Contemporaneous variables such
  as current wealth or current residence may be mediators or post-exposure; the primary historical
  specification should keep a minimal set (child age, sex, birth order, maternal age) and treat
  wealth-adjusted versions as sensitivity (OPEN, decided before estimation).
- lambda_s: survey-round effects (within one survey, a constant).
- tau_k,b: country-by-birth-year (or country-by-birth-month) controls absorbing national cohort shocks.
- delta_c: cluster fixed effects, qualified by country and survey (country-survey-cluster key).
- Weights: DHS sample weights, normalised within country and then pooled with equal country totals
  on the exact estimation sample, as in the existing pooled model (OPEN: confirm the estimand).
- Inference: standard errors clustered at the DHS PSU (country-survey-PSU key). Same-group FE and
  clustering use the adjudicated native CRV1 convention; no full-dummy penalty.

Identifying variation: after cluster fixed effects, beta is identified from differences in window
exposure between children of different birth cohorts living in the same cluster, net of country-by-
cohort shocks. This is a comparison across children and cohorts. It is not a panel following the same
children, and it does not, by itself, constitute a difference-in-differences design.

Diagnostics before any estimation (required):
- Within-cluster standard deviation of E after removing cluster means and cohort controls.
- Number of clusters with more than one distinct birth-year exposure.
- Share of within-cluster exposure variation that remains after country-by-cohort controls.
- Correlation between E and birth year within country, and between E and interview year.
- Variance inflation for E against age, birth year and interview year.

Collinearity: age at interview, birth cohort and interview year satisfy age = interview year − birth
year (up to month precision). Including all three is not identified without restriction. The
primary specification uses birth cohort (country-by-year) and omits interview-year controls unless
the diagnostics show they are needed. OPEN until the design diagnostics exist.

Remaining confounding: local infrastructure, income, health services and urbanisation can change over
the same years and be correlated with modelled WASH. Cluster and cohort controls do not remove these.
The design improves the temporal alignment of the exposure. It does not establish causality.

Location linkage: clusters are indexed within survey. Cluster numbers are not linked across survey
rounds; there is no validated spatial correspondence between rounds in this project.

## E. Sample choice (summary; see readiness report)

- Ethiopia 2016, Ghana 2014, Kenya 2014: candidate samples on temporal grounds (fieldwork and birth
  cohort fall within the 2000–2017 raster range). Ghana 2014 and Kenya 2014 (water) are inputs to the
  modelled surfaces; this is disclosed and not treated as disqualifying.
- Nigeria: 2018 places some children's birth years after 2017; 2013 avoids this on temporal grounds.
  The trade-off (2013 vs 2018) is decided on coverage and access, not on outcome associations.
  OPEN until the Nigeria extract or DHS access is confirmed.
- The historical sample complements the current four-round analysis. It does not replace it.

## F. Inputs and their status (see readiness report for evidence)

- IHME rasters (W_IMP, S_IMP; MEAN, LOWER, UPPER; 2000–2017): verified format and grid.
- IPUMS extract idhs_00001: present, but no codebook; layout, geographic linkage and birth-date
  fields are not verified. Blocks all child-level construction.
- LOWER/UPPER semantics and licence: not established from available documentation.
