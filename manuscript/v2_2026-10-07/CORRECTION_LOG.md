# Correction log: v1 → v2 (2026-10-07)

Concise, itemised record of every substantive correction made in this pass. No empirical estimate changed (confirmed by diff against v1; `claim_evidence_ledger.md`).

## 1. Exposure-timing argument

| Problem in v1 | Correction in v2 |
|---|---|
| The historical extension's research question was framed in a way that invited reading the baseline-vs-historical comparison as isolating "the effect of" exposure timing, even though the two samples differ in survey rounds, exposure definitions, eligibility, and controls. | Reframed the historical research question (Introduction §1.2–1.3) as a self-contained question within the historical sample only: "is modelled early-life local WASH coverage associated with outcomes within this sample?" Added a dedicated subsection, Discussion §6.2, stating precisely what differs between the two samples (four dimensions, enumerated) and what the within-historical-sample window comparison does and does not hold constant. |
| The extension was at risk of being read as establishing children's actual historical household conditions. | Added explicit statements (Introduction §1.2, Data §3.5) that the extension assigns a *modelled, area-level* coverage estimate, not a record of any individual household's actual historical facilities. |

## 2. Overgeneralized literature claims

| Problem in v1 | Correction in v2 |
|---|---|
| "Every study reviewed above shares a measurement limitation" (single-round exposure) — false for the RCTs and Headey and Palloni's panel design. | Restricted the claim to cross-sectional, single-round DHS studies specifically (Literature Review §2.5); explicitly stated the WASH trials assign exposure prospectively near birth and Headey-Palloni use a panel, so the limitation does not apply to them. |
| "Biological plausibility is not in serious dispute" — asserted without a precise source. | Now directly grounded in Cumming et al. (2019)'s own stated consensus message, quoted precisely with page/section location (Literature Review §2.1, §2.3; verified by reading the source in full this pass). |
| Attenuation described as an established "stylised fact." | Reframed as a specific, source-grounded parallel to one study's finding (Headey and Palloni 2019's null sanitation–stunting result under their panel design), with an explicit statement that generalising beyond that to "WASH associations generally attenuate" overstates what any one study establishes (Discussion §6.1). |
| "Most of the DHS-based observational literature measures WASH at the household level only" stated as established fact about the wider literature. | Scoped to "studies reviewed here" (Literature Review §2.4). |
| Implicit claim that the household/community comparison "has never been implemented." | Rephrased to "the author is not aware of" this combination in the sources reviewed, explicitly disclaiming an exhaustive search (Literature Review §2.4, §2.7); Introduction §1.5 now states explicitly that a particular country combination is not, by itself, evidence of novelty. |
| Phrasing implying buffer-area averaging is the only possible geospatial-assignment method. | Rephrased to state area-average and population-weighted aggregation are both possible, and that this thesis makes the area-average choice explicitly (Literature Review §2.6). |
| Geruso and Spears described vaguely as "a design intended to isolate sanitation's own contribution." | Replaced with the actual identification strategy, read directly from the source: Muslim neighbourhoods in India are worse on most observable predictors of child health but *better* specifically on sanitation (lower open defecation, a religious behavioural difference independent of wealth), letting the authors isolate a sanitation-specific channel because it moves opposite to general neighbourhood quality (Literature Review §2.3). |
| Blom, Ortiz-Bobea, and Hoddinott (2022) cited with an implicit claim about what it establishes, without having been independently re-read in this project. | Added an explicit statement that this source was reviewed at the abstract/design level only, not independently re-verified claim-by-claim, and is cited only for its matching-method structure (Literature Review §2.6; `citation_map.md`). |

## 3. Central literature descriptions — verified, not assumed, this pass

Three sources were read in full or substantial part specifically to check the claims made about them (full detail in `citation_map.md`): Cumming et al. (2019) — read pp. 1–9 (entire article); Headey and Palloni (2019) — read pp. 729–731 (abstract, introduction, start of results); Geruso and Spears (2015) — read pp. 1–3 (title page, abstract, introduction). This produced one substantive correction beyond phrasing: **Headey and Palloni's actual finding is more specific and mixed than v1's paraphrase suggested** — sanitation reduces diarrhoea and mortality but is *not* associated with stunting or wasting in their panel design; water is insignificant for most outcomes except piped water specifically predicting reduced stunting. v1 had summarised this as "the association weakens substantially, though does not vanish," which both oversimplified and slightly mischaracterised the direction of the stunting-specific finding. Corrected in Literature Review §2.2 and Discussion §6.1.

## 4. Administrative content moved out of chapter prose

| Item | Where it was (v1) | Where it is now (v2) |
|---|---|---|
| Title-change discussion | `01_introduction.md` §1.8 | `AUTHOR_CHECKLIST.md` only; chapter prose no longer discusses or claims to verify the registered title |
| Publication-version explanation for Geruso and Spears | Inline parenthetical in `02_literature_review.md` | `citation_map.md` and `bibliography_verification_ledger.md`; chapter prose keeps one short clause pointing to the ledger, not the full explanation |
| Workflow/verification commentary ("this source was reviewed at the level of its abstract...") | Not present in v1 (v1 did not flag verification depth in-line) | Added to v2 chapter prose only where necessary for honesty about depth (one sentence, Literature Review §2.6), with full detail in `citation_map.md` |

## 5. Machine-readable citations

All in-text citations converted from plain English author-year prose to pandoc Markdown citation syntax (`[@key]` / `Author [-@key]`), validated programmatically (20 keys used, all resolve, no duplicates, no bare unresolved `@key` syntax remaining). `citation_map.md` is new in v2. `MASTER_ASSEMBLY.md` documents the rendering workflow.

## 6. Empirical narrative checked against v3 — no discrepancy found requiring a number change

Re-confirmed against `docs/provenance/final_empirical_package_v3_2026-10-07/`: primary vs. FULL_DUMMY_DF labelling intact; balanced water/sanitation and HAZ/WAZ/WHZ reporting intact (and strengthened — Results §5.7 now explicitly states the window/sensitivity families cover all products and outcomes, not only water-HAZ, to avoid appearing to privilege the one significant cell); model-specific sample counts, units, and ten-point scaling unchanged; weighted/unweighted comparison unchanged; equal-country-weighting language already correctly distinguished from an average of country slopes in v1 and retained; measurement-selection qualifications unchanged; Ethiopia C1 invalid/C2-C3 provisional unchanged.

## 7. Supervisor-request status

Corrected in a separate public-safe record, not in the manuscript package itself: `docs/provenance/historical_wash_supervisor_request_status_v1_2026-10-07.md` now distinguishes "literature positioning drafted and reviewed in this milestone" from "introduction drafted" from "introduction/design not yet sent to the supervisor" from "supervisor feedback not yet received or incorporated" — none of these is marked complete merely because a chapter now exists. No message was sent to the supervisor by this correction pass.
