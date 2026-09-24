# Historical-WASH Extension — Feasibility Audit (Provenance Record)

Date: 2026-09-24. Status: read-only research/design audit; no historical-WASH exposure has been
constructed and no historical-WASH regression has been estimated as of this record. This note
consolidates verified findings gathered across several audit passes into one place, so that
verification work is not repeated or restated inconsistently. It supersedes no other document;
`docs/empirical_strategy.md` Section 6 remains the canonical thesis-facing summary.

## 1. Decision

**MODIFY.** A defensible historical-WASH design exists in principle, but two concrete blockers must
be resolved before any exposure construction or estimation: (a) the IPUMS DHS extract built for the
four candidate historical samples has no accompanying codebook, so its actual variable content is
unverified; (b) the current thesis's own latest-round samples cannot support a historical match at
all — proven below, not inferred — so the older IPUMS samples (or equivalent original-DHS downloads)
are structurally required, not merely preferred.

## 2. IHME source — verified facts

Product: Local Burden of Disease WaSH Collaborators, "Mapping geographical inequalities in access to
drinking water and sanitation facilities in low-income and middle-income countries, 2000–17," *The
Lancet Global Health*, 2020 (doi:10.1016/S2214-109X(20)30278-3). Bayesian geostatistical model, ~600–634
household-survey sources across 88–90 LMICs, annual 2000–2017, ~5×5km. No newer version of this
specific product extending past 2017 was found in a public search this pass; only an interactive
visualization tool built on the same 2000–2017 data was found.

Directly verified from the actual GeoTIFF files (not filenames), for all 18 years, both `W_IMP` and
`S_IMP`, `PERCENT_MEAN` (36 files total): grid-aligned, identical size (6,610×2,123), pixel scale
0.041667° (≈4.6km), CRS EPSG:4326/WGS84 (from each file's own GeoKeys), NoData −999999, values 0–100
at four African-capital test coordinates across all years, with plausible year-over-year trends (e.g.
Ghana/Accra water 58%→96.5%, 2000→2017).

**Not established from any locally or publicly available documentation this pass:** the exact
statistical definition of LOWER/UPPER (credible-interval level unspecified in available search
results); explicit licensing/reuse terms (GHDx catalog page returned HTTP 403 to automated fetch,
never independently re-tried by direct browser visit).

DHS survey data are confirmed among the model's inputs (directly read from the local
`WATER_DATA_INPUT_SOURCES`/`SANI_DATA_INPUT_SOURCES` spreadsheets): Ghana DHS 2014 appears as a
direct input to both the water and sanitation models; Kenya DHS 2014 appears as a water-model input
only; Ethiopia and Nigeria have no exact-round match. This is a genuine, disclosed circularity
concern for two of the four candidate country/rounds — it does not invalidate the design, but the
exposure must be described as partly-survey-derived for those two cases, not fully external.

## 3. Current-thesis-round temporal infeasibility — proven, not inferred

Computed directly from the raw KR `.dta` files already in the project (`data/interim/DHS/<country>/.../KR/*.dta`),
using the actual `b1`/`b2`/`b3` (birth month/year/CMC) fields, restricted to children with any valid
anthropometric measurement (`hw70`/`hw71`/`hw72` < 9990):

| Country | Round | N anthro-eligible | Birth-year ≤2017 | % |
|---|---|---|---|---|
| Ethiopia | 2024–25 | 5,971 | 0 | 0.00% |
| Ghana | 2022 | 4,420 | 73 | 1.65% |
| Kenya | 2022 | 17,415 | 2,050 | 11.77% |
| Nigeria | 2024 | 9,533 | 0 | 0.00% |

Pooled: birth-year-exposure coverable 5.69%; prenatal-proxy (birth year −1) coverable 16.62%;
first-two-years exposure (birth year AND birth year+1 both ≤2017) coverable **0.00%**, for every
country, with zero exceptions. **The current four thesis rounds cannot support any two-year historical
exposure window, and can barely support a one-year window even under the most permissive definition.**
This is why the historical layer must use different, older survey rounds — a structural requirement of
the 2017 data ceiling, not a design preference.

Internal check, same computation: `b3` (birth CMC) equals `(b2−1900)×12+b1` for all 70,231 children in
all four countries with zero mismatches, including Ethiopia — confirming Ethiopia's raw DHS birth
variables are already Gregorian-converted in the current-round file (b2 range 2019–2025 for a survey
fielded 2024–25). This does not by itself confirm the IPUMS-derived `KIDDOBCMC` for the *historical*
Ethiopia 2016 sample is equally Gregorian-converted — that remains to be checked once the codebook
exists — but it is strong supporting evidence in the same direction, since IPUMS derives from the same
underlying DHS standard recode files.

## 4. Current-round GPS — already present, already linked, no gap here

`data/processed/pooled_kr_four_country_geolinked.parquet` (output of the project's own Step 06)
carries `LATNUM`/`LONGNUM`/`DHSCLUST`/`URBAN_RURA` for all 70,231 current-round children, 100%
non-missing, verified 1:1 at the cluster level (0 of 4,481 clusters with more than one distinct
coordinate pair). DHS's own displacement documentation is present locally
(`data/interim/DHS/*/GE/GPS_Displacement_README.txt`): urban clusters displaced up to 2km, rural up to
5km (1% up to 10km), displacement restricted to stay within the same admin2 area. This is not a gap for
the current rounds; it is only a gap for the *older* candidate rounds, whose raw files are not present
locally (confirmed by directory search — only the four current-round countries' raw files exist under
`data/raw/DHS`).

## 5. IPUMS extract — current state

`idhs_00001.dat.gz` (in the user's Downloads folder, not the repository) contains 71,413 fixed-width
rows, confirmed by string search to comprise exactly the four intended samples in plausible proportions
(ET2016 10,641 / GH2014 5,884 / KE2014 20,964 / NG2018 33,924). **No DDI codebook or Stata/SPSS/R
command file exists anywhere in Downloads or the project tree.** Without it, no individual variable
(birth timing, anthropometry, controls, GPS) can be read from the 281-character rows without guessing
column boundaries — which this project's standing rule explicitly forbids. This is the single blocking
item for all downstream work.

Nigeria 2018's youngest children (born 2018) fall outside the 2000–2017 IHME window; Nigeria 2013 was
identified as a preferable substitute on temporal-coverage grounds alone (not significance), since it
removes this truncation and, per the source-overlap spreadsheets, does not worsen circularity (Nigeria
never appears in the sanitation-input list at any year).

## 6. Literature leads (public sources only; the supervisor's confidential paper is not cited or quoted anywhere in this document, and was not saved to any file in this project)

- Local Burden of Disease WaSH Collaborators (2020), *Lancet Global Health* — the IHME exposure source itself (§2).
- Blom, Ortiz-Bobea & Hoddinott (2022), *JEEM* — historical geocoded weather matched to child developmental windows across repeated DHS rounds; already cited in `docs/empirical_strategy.md` §6 as a matching-logic analogue, not a WASH finding.
- Skoufias & Vinha (2026), *PLOS ONE*, "Community-level externalities in child health: Evidence from Sub-Saharan Africa" — already present in this project's own `sources/summaries/literature_evidence_matrix.csv` (entry S12); directly relevant to the household-vs-community strand.
- A PMC-indexed individual-level meta-analysis of community-level sanitation access and child stunting/anemia/diarrhea using DHS/MICS data (PMC5464528) — found via public search this pass, not yet independently read in full; relevant to the household-vs-community strand.
- A Mali-focused study on community latrine coverage (200m radius) vs. household latrine ownership and child growth, and a Mozambique spatial cohort study on neighbors' WASH facility use — both found via public search this pass, exact citations not yet independently confirmed; relevant to the community-exposure-definition strand.

These are leads for the introduction's literature review, not yet verified in full or written into any thesis document.

## 7. What must happen before any exposure construction or estimation

1. Obtain the IPUMS codebook (or rebuild the extract with Nigeria 2013 in place of 2018, then obtain its codebook).
2. Repeat the §3-style birth-year/IHME-overlap calculation on the actual older-round microdata once the codebook exists — the current 2000–2017-vs-2011–2016-style approximate ranges are not a substitute for this.
3. Confirm the Ethiopia 2016 IPUMS `KIDDOBCMC` Gregorian-conversion status directly (§3's evidence is suggestive, not conclusive, for the IPUMS-derived version specifically).
4. Confirm DHS Program GPS-download authorization status for the user's account.
5. Only then: lock the primary exposure window (birth-year vs. first-12-months vs. other) on literature grounds, lock the spatial-matching rule (buffer vs. point), and write the first matching script.

No further file was created or modified as part of resolving these five items; they require external
action (downloads, account verification) that cannot be completed from within this repository.
