# The Impact of Improved Water and Sanitation on Child Nutritional Outcomes in Sub-Saharan Africa: Evidence from DHS and Geospatial Data

Master's thesis project (Economics) by Bakhodir Izzatulloev. This repository
holds the data-harmonization pipeline, regression analysis, and final results
for a study of how access to improved water and sanitation is associated with
child nutritional outcomes (HAZ, WAZ, WHZ; stunting, underweight, wasting as
robustness outcomes) in Ethiopia, Ghana, Kenya, and Nigeria, using pooled DHS
survey microdata linked to DHS geographic (GE) cluster data.

For a guided walkthrough of where each part of the analysis lives in the
code — anthropometric outcome construction, WASH classification, the
leave-one-out cluster exposure measure, fixed effects, the main regressions,
and the robustness checks — see `docs/code_guide.md`. The full empirical
design is documented in `docs/thesis_design.md` and `docs/data_dictionary.md`,
and provenance notes on how specific methodological questions were resolved
during implementation are collected in `outputs/final_audit/`.

## Data access

This repository does not distribute DHS microdata. The pipeline was built
and run against DHS Program survey files (Ethiopia 2024-25, Ghana 2022,
Kenya 2022, Nigeria 2024) obtained under the DHS Program's own data-use
terms, and those terms do not permit redistributing the underlying
respondent-level data. Reproducing the pipeline from raw data requires your
own DHS Program-authorized access to the same four surveys, placed in the
directory structure that `scripts/dhs_harmonization/00_config.py` expects;
`docs/data_dictionary.md` lists the exact raw variables each stage reads.

## Environment

- **Python**: this project's `.venv` is built on **Python 3.14.0** (confirmed
  from `.venv/pyvenv.cfg` — verify the same way if the venv is ever recreated).
- **Virtual environment**: a `.venv/` is expected at the project root.
- **Dependencies**: install with the venv's own `pip`, from `requirements.txt`
  (unpinned except `svy==0.23.0` and `polars==1.43.2`):
  ```
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  ```
- **Windows/PowerShell note**: PowerShell's default execution policy often
  blocks `.venv\Scripts\Activate.ps1` from running. Rather than changing the
  execution policy, call the venv's Python executable directly — this works
  regardless of activation state and is what every script in this project has
  actually been run with:
  ```
  .venv\Scripts\python.exe scripts\dhs_harmonization\00_config.py
  ```

## The Active Pipeline: `scripts/dhs_harmonization/`

This is the pipeline that was actually built and used for this thesis. Run in
order, 00 → 13. `00`/`01` are definition/configuration modules (no data is
read or written); `02` onward are executable stages that each read the
previous stage's output and write a new file, so no intermediate output is
ever edited in place. Every stage that touches a source DHS file checksums it
before and after execution and hard-fails if it changed — see "Data
Integrity" below.

| Stage | Script | Type | Purpose | Primary input | Primary output |
|---|---|---|---|---|---|
| 00 | `00_config.py` | Configuration | Central paths/constants — country list, source file paths, anthropometric thresholds | — | (constants only) |
| 01 | `01_wash_mapping.py` | Mapping/harmonization | JMP water/sanitation raw-code → category dictionaries | — | (mapping dicts only) |
| 02 | `02_load_flag_anthro.py` | Data preparation | Load + flag anthropometric z-scores per country | Raw KR `.dta` | `staging/<country>/kr_anthro_flagged.parquet` |
| 03 | `03_build_indicators.py` | Mapping + data preparation | Build stunting/wasting/underweight indicators and WASH categories | Step 02 output + raw KR | `staging/<country>/kr_indicators.parquet` |
| 04 | `04_build_country_kr.py` | Data preparation | Add controls, weights, PSU/strata, survey period | Step 03 output + raw KR | `<country>_kr_clean.parquet` |
| 05 | `05_pool_countries.py` | Data preparation | Row-concatenate the four countries; build country-qualified IDs | 4× Step 04 outputs | `pooled_kr_four_country.parquet` |
| 06 | `06_ge_linkage.py` | Linkage | Attach DHS GE geographic columns (region, coordinates, elevation) | Step 05 output + GE shapefiles | `pooled_kr_four_country_geolinked.parquet` |
| 07 | `07_descriptives.py` | Descriptive statistics | Design-based (survey-weighted) descriptive tables | Step 06 output | `outputs/tables/table1-4*.csv` |
| 08 | `08_hr_cluster_wash_exposure.py` | Exposure construction | Household-level leave-one-out cluster WASH coverage rates | Step 06 output + raw HR | `pooled_kr_four_country_wash_exposure.parquet` |
| 09 | `09_admin_region.py` | Data prep / linkage | Country-qualified administrative-region fixed-effect identifier | Step 08 output + raw KR | `pooled_kr_four_country_admin_region.parquet` |
| 10 | `10_birth_order.py` | Data prep / linkage | Birth-order control extraction | Step 09 output + raw KR | `pooled_kr_four_country_birth_order.parquet` |
| 11 | `11_main_regressions.py` | Regression analysis | Models 1–4, continuous outcomes (HAZ/WAZ/WHZ), pooled + country-specific | Step 10 output | `outputs/regressions/main_continuous_models.csv` |
| 12 | `12_robustness.py` | Robustness analysis | 6 robustness families (binary LPM, severe outcomes, Ghana bio-digester, household baseline, alternative weighting, LOO-denominator sensitivity) | Step 10 output + Step 11 outputs (read-only) | 6 CSVs under `outputs/regressions/` |
| 13 | `13_final_outputs.py` | Reporting/final outputs | Thesis-ready tables, figures, descriptive map, and reproducibility audit — reformats already-validated results, computes nothing new | Step 07/11/12 outputs (read-only) | `outputs/final_tables/`, `final_appendix/`, `final_figures/`, `final_audit/` |

Every stage script is independently runnable (each loads `00_config.py` by
file path rather than a package import), and each is self-contained rather
than depending on another stage's in-memory state — the only exception is
Steps 12 and 13, which deliberately import functions from `11_main_regressions.py`
to reuse its model-matrix/weighting code rather than duplicating it.

## Data Integrity

Raw DHS source files under `data/interim/DHS/<country>/<round>/<KR|HR|IR|GE>/`
are **read-only** throughout this pipeline — no script ever opens one in
write mode. Every stage from `05` onward computes an MD5 checksum of its
source file(s) before reading and again after writing its own output, and
raises an error (rather than continuing) if any checksum changed. This is how
the pipeline guarantees that no upstream source or intermediate file was
silently modified by a later stage.

## Final Outputs

The final, thesis-facing results (produced by `13_final_outputs.py` from
already-validated Step 07/11/12 results — no new statistic is computed there)
live under:

- `outputs/final_tables/` — Final Tables 1–6 (sample characteristics,
  anthropometric prevalence, WASH characteristics, main pooled regression,
  preferred-model-by-country, binary LPM robustness).
- `outputs/final_figures/` — Figures 1–3 plus the descriptive survey-cluster
  coverage map.
- `outputs/final_appendix/` — Appendix Tables A1–A8 and Appendix Figure A1.
- `outputs/final_audit/` — the Step 11 bug-provenance note and the Step 13
  final-audit checksum/integrity record.

## Important Methodological Notes

(Full detail lives in `docs/code_guide.md`, `docs/thesis_design.md`, each
script's own docstring, and the provenance notes under
`outputs/final_audit/` — this is a pointer, not a restatement.)

- Four countries (Ethiopia, Ghana, Kenya, Nigeria) analyzed **pooled** (main
  specification) and **country-specific** (robustness/heterogeneity).
- Pooled models use a **temporary, model-specific, equal-total-country
  weight**, computed fresh for each model's own estimation sample and never
  written to any file; country-specific models use the original DHS weight
  (`weight_original`).
- Standard errors are **PSU-clustered** (`country_psu` pooled, `psu`
  country-specific) — a cluster-robust approximation, not a full stratified
  DHS svyset-equivalent design-based variance estimator.
- The preferred specification (Model 4) includes a **country-qualified
  administrative-region fixed effect** (`country_admin_region`); no
  survey-year or spatial-grid fixed effect is included.
- The primary WASH exposures are **continuous, cluster-level, leave-one-out
  household coverage rates** (`water_rate_loo`, `sanitation_rate_loo_core`),
  not a simple household-level binary (that variant exists only as a
  robustness/baseline check, per the original thesis design's Section 9.1).
- All regression coefficients are reported and must be described as
  **associations, not causal effects**.

## Legacy Folders (not part of the active pipeline)

The following `scripts/` subfolders were created by an early project scaffold
and were **superseded** by `scripts/dhs_harmonization/` — they are retained
(nothing is deleted per this project's convention) but contain no active
code and should not be used:

```
scripts/00_setup/
scripts/01_cleaning/
scripts/01_data_cleaning/
scripts/02_data_construction/
scripts/02_variables/
scripts/03_geospatial_merge/
scripts/03_merge/
scripts/04_analysis/
scripts/05_maps/
scripts/05_robustness/
scripts/06_tables/
scripts/helpers/
```

Likewise, `data/final/` (mentioned in this scaffold) was never used — every
pipeline stage's output actually lands under `data/processed/` (see
`00_config.py`'s `DATA_PROCESSED` constant), not `data/final/`.

## Setup

Python dependencies are listed in `requirements.txt`. Project-wide DHS
pipeline paths and constants are defined once in
`scripts/dhs_harmonization/00_config.py` — pipeline scripts import from
there rather than hardcoding paths. (`config/project_paths.py` is part of
the legacy scaffold above and is not used by the active pipeline.)

## Reproducing on another machine

The scripts in this repository are the exact, unmodified files used to
produce the thesis's results, and `00_config.py` and `13_final_outputs.py`
still contain the local Windows path (`PROJECT_ROOT`) used on the machine
where the analysis was run. This is left as-is deliberately, to keep the
frozen scripts byte-identical to what actually generated the reported
results. If you reproduce this pipeline on a different machine, update
`PROJECT_ROOT` in those two files to your own project directory before
running anything. This alone does not make the pipeline runnable — you
also need your own DHS Program-authorized copy of the four surveys (see
"Data access" above); the code describes how that data was processed, but
does not include or grant access to it.
