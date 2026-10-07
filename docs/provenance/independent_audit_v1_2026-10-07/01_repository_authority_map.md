# Repository authority map (2026-10-07)

Which file governs each analysis family, as of commit `5da82cf` (branch `main`, confirmed equal to `origin/main` via safe fetch; only untracked item is `outputs/supervisor_meeting/`, confidential, correctly never committed).

## Scripts (active pipelines)

| Family | Active script directory | Entry/exit points |
|---|---|---|
| Baseline harmonisation, construction, estimation | `scripts/dhs_harmonization/00`–`14` | `00_config.py` (paths/constants) → `01_wash_mapping.py` (pure mapping definitions, no execution) → `02_load_flag_anthro.py` (anthropometry scaling/flagging, self-validating) → `03_build_indicators.py` → `04_build_country_kr.py` → `05_pool_countries.py` (self-validating pooling) → `06_ge_linkage.py` (self-validating geo-merge) → `07_descriptives.py` → `08_hr_cluster_wash_exposure.py` (leave-one-out construction, brute-force self-validated) → `09_admin_region.py` → `10_birth_order.py` → `11_main_regressions.py` → `12_robustness.py` → `13_final_outputs.py` → `14_household_community_wash_models.py` (the frozen, do-not-modify model script producing the authoritative baseline tables) |
| Historical extension | `scripts/historical_wash/01`–`20` | `01` (IHME inventory) → `02`/`03`/`04`/`05` (IPUMS import, validation, resolution — `02` is superseded by `03`/`05`, preserved for lineage) → `06` (Ethiopia calendar audit, produces C1/C2/C3) → `07` (coordinate-survey correspondence) → `10` (spatial extraction v3, final — `08`/`09` superseded, preserved) → `11` (spatial validation) → `12`/`13` (exposure construction/validation) → `14` (analysis samples) → `15` (design diagnostics) → `16` (estimation, 291 models) → `17` (independent validation, 4 representative models) → `18` (common-sample windows) → `19` (design checks) → `20` (independent pooled-model verification, added 2026-10-07) |

**No competing or ambiguous script authority found.** Each directory has exactly one active numbered sequence; superseded files are distinctly named (`_PREPARED`, `_v2` where v3 exists) and are not imported by any active script (spot-checked: `16_estimate_preliminary.py` imports only from the `v3` spatial extraction output path and the `run_20261006T184744Z` analysis-sample output, not from any superseded run folder — confirmed by reading its `AN`/`CON` path constants, `scripts/historical_wash/16_estimate_preliminary.py:40-43`).

## Output tables (authoritative vs. superseded)

| Analysis family | Authoritative output | Superseded, preserved, not authoritative |
|---|---|---|
| Baseline household/community models | `outputs/household_community_wash/*.csv` (produced by script `14`) | None found superseding these; `outputs/regressions/main_continuous_models.csv` is a separate, also-authoritative frozen output from an earlier pipeline stage (`11_main_regressions.py`/`13_final_outputs.py`) — the two are **not duplicates**: `main_continuous_models.csv` is the community 4-stage adjustment table; `household_community_wash/*.csv` is the household/community/joint/sensitivity suite. Confirmed non-overlapping by column/content inspection this session and the prior session. |
| Historical preliminary estimates | `data/processed/estimation/run_20261006T185646Z/model_results_RESTRICTED_coefficients.csv` (RESTRICTED) + public aggregate `docs/provenance/final_empirical_package_v3_2026-10-07/02_core_reporting_table.md` | `data/processed/historical_wash/v1_run1_SUPERSEDED_nodata_parse_bug/` (named superseded, excluded from all active script inputs) |
| Independent pooled-model verification | `data/processed/estimation/pooled_independent_validation_20261007T090003Z/` (RESTRICTED) | None — single run |

## Documentation (which doc is current)

| Topic | Current authority | Explicitly superseded |
|---|---|---|
| Baseline numerical claims | `docs/provenance/baseline_evidence_reconciliation_v1_2026-10-07.md` | `outputs/supervisor_development/22_supervisor_roadmap_final.md`, `26_empirical_strategy_final_candidate.md` (stale p-values, wrong age-heterogeneity count — documented, not deleted) |
| Historical extension status, final reporting | `docs/provenance/final_empirical_package_v3_2026-10-07/` | `final_empirical_package_v1_2026-10-07/`, `v2_2026-10-07/` (each carries an explicit pointer banner to the next version — confirmed present in both, this session) |
| Ethiopia candidate status | `docs/provenance/historical_wash_ethiopia_candidate_status_v1_2026-10-07.md` | None (single version) |
| Issue register | `docs/provenance/historical_wash_issue_register_v1_2026-10-07.md` | None (single version; reconciles two earlier partial lists, both cited within it) |
| Supervisor advice | `docs/provenance/historical_wash_supervisor_advice_matrix_2026-10-07.md` + `..._ADDENDUM_2026-10-07.md` (corrects one row) | Original file preserved with a pointer banner to the addendum for that one row |
| Supervisor request status (sent/received) | `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md` | None (single version) |

## Manuscript (which version is canonical)

| Version | Status | Pointer |
|---|---|---|
| `manuscript/v1_2026-10-07/` | Superseded | `POINTER_TO_V2.md` present, confirmed |
| `manuscript/v2_2026-10-07/` | Superseded | `POINTER_TO_V3.md` present, confirmed |
| `manuscript/v3_2026-10-07/` | **Canonical** | `README.md` / `MASTER_ASSEMBLY.md` state this explicitly |

**Single current entry point confirmed**: `manuscript/v3_2026-10-07/README.md` → `MASTER_ASSEMBLY.md`. No file outside `v3_2026-10-07/` claims current authority; both `v1` and `v2` README files carry superseded banners (verified by reading this session).

## Stale-instruction risk for an automated PDF generator

A generator that globs `manuscript/*/` without reading pointer banners, or that reads `docs/provenance/final_empirical_package_v1*` instead of `v3*`, would use stale numbers. **Mitigation already in place**: every superseded file has an explicit, human-and-machine-readable pointer banner at its top (checked: `v1_2026-10-07/README.md`, `v2_2026-10-07/README.md`, `final_empirical_package_v1.../00_results_index.md`, `v2.../00_results_index.md`). `manuscript/v3_2026-10-07/MASTER_ASSEMBLY.md` explicitly lists "Files that must not be used as manuscript sources." No further action identified beyond what already exists.
