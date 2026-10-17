# Cross-reference map (2026-10-07)

Chapter text refers to sections by number (e.g. "Section 6.2") rather than by heading text, because section numbers are stable under copy-editing while heading wording may change. This map gives the stable label a later rendering system (e.g. pandoc-crossref) should bind to each numbered section, so that in-text references resolve correctly even if headings are reworded. A renderer that supports only heading-text anchors should use the "Current heading text" column directly; a renderer using explicit labels should insert the label immediately after the heading as `{#sec:label}` (pandoc-crossref syntax) before processing.

| Section | Stable label | Current heading text | File |
|---|---|---|---|
| 1 | `sec:intro` | Introduction | `01_introduction.md` |
| 1.1 | `sec:intro-household-community` | Two distinct exposures: a household's own facilities and its surroundings | `01_introduction.md` |
| 1.2 | `sec:intro-timing` | Exposure timing in cross-sectional survey designs | `01_introduction.md` |
| 1.3 | `sec:intro-questions` | Research questions | `01_introduction.md` |
| 1.4 | `sec:intro-scope` | Scope: four countries, two time horizons | `01_introduction.md` |
| 1.5 | `sec:intro-contribution` | Contribution | `01_introduction.md` |
| 1.6 | `sec:intro-summary` | A restrained summary of findings | `01_introduction.md` |
| 1.7 | `sec:intro-limitations` | Design and principal limitations, stated at the outset | `01_introduction.md` |
| 1.8 | `sec:intro-structure` | Structure | `01_introduction.md` |
| 2 | `sec:litrev` | Literature review and conceptual framework | `02_literature_review.md` |
| 2.1 | `sec:litrev-plausibility` | From biological plausibility to demonstrated association | `02_literature_review.md` |
| 2.2 | `sec:litrev-confounding` | Observational evidence and the confounding problem | `02_literature_review.md` |
| 2.3 | `sec:litrev-trials` | Credible causal evidence: what the major trials actually found, and what they did not test | `02_literature_review.md` |
| 2.4 | `sec:litrev-household-community` | Household versus community exposure | `02_literature_review.md` |
| 2.5 | `sec:litrev-timing` | Exposure timing in single-round, cross-sectional survey designs specifically | `02_literature_review.md` |
| 2.6 | `sec:litrev-geospatial` | Geospatial exposure assignment, and a matching-method precedent from outside the WASH literature | `02_literature_review.md` |
| 2.7 | `sec:litrev-contribution` | This thesis's contribution and the gap it addresses | `02_literature_review.md` |
| 3 | `sec:data` | Data and variable construction | `03_data_and_variables.md` |
| 3.1–3.2 | `sec:data-baseline-sample` | Baseline sample / anthropometric outcomes | `03_data_and_variables.md` |
| 3.3 | `sec:data-baseline-exposure` | Baseline WASH exposures: household and leave-one-out community | `03_data_and_variables.md` |
| 3.4 | `sec:data-baseline-covariates` | Baseline covariates, geography, and weights | `03_data_and_variables.md` |
| 3.5 | `sec:data-historical-scope` | Historical extension: rounds, exposure source, and scope | `03_data_and_variables.md` |
| 3.6 | `sec:data-historical-spatial` | Historical spatial extraction: buffers, displacement, and coverage | `03_data_and_variables.md` |
| 3.7 | `sec:data-historical-windows` | Historical exposure windows and completion rules | `03_data_and_variables.md` |
| 3.8 | `sec:data-historical-covariates` | Historical covariates, weights, and the established-date measurement universe | `03_data_and_variables.md` |
| 3.9 | `sec:data-nigeria-gap` | A documented measurement-universe discrepancy: Nigeria 2018 | `03_data_and_variables.md` |
| 4 | `sec:methods` | Empirical strategy | `04_empirical_strategy.md` |
| 4.1–4.2 | `sec:methods-household` | Household WASH specifications (region FE, cluster FE) | `04_empirical_strategy.md` |
| 4.3 | `sec:methods-community` | Community WASH, region fixed effects | `04_empirical_strategy.md` |
| 4.4 | `sec:methods-joint-age` | Joint model and current-age heterogeneity | `04_empirical_strategy.md` |
| 4.5 | `sec:methods-inference` | Inference, weighting, and the pooled estimand | `04_empirical_strategy.md` |
| 4.6 | `sec:methods-historical` | Historical extension: cluster fixed effects with cohort controls | `04_empirical_strategy.md` |
| 5.1–5.3 | `sec:results-baseline` | Household WASH / Community WASH / Joint model | `05_results.md` |
| 5.4–5.5 | `sec:results-sensitivity-age` | Nigeria sensitivity / Age heterogeneity | `05_results.md` |
| 5.6 | `sec:results-historical-primary` | Historical extension: primary established-date models | `05_results.md` |
| 5.7–5.8 | `sec:results-historical-sensitivity` | Alternative windows / further sensitivity | `05_results.md` |
| 5.9 | `sec:results-ethiopia` | Ethiopia: provisional, excluded from the established-date pooled sample | `05_results.md` |
| 6.1 | `sec:discussion-literature` | Relating the findings to the literature | `06_discussion_and_limitations.md` |
| 6.2 | `sec:discussion-noncomparability` | Why the baseline and historical results cannot be compared as a test of exposure timing | `06_discussion_and_limitations.md` |
| 6.3–6.5 | `sec:discussion-limitations` | Limitations (documentation / design choices / inherent) | `06_discussion_and_limitations.md` |
| 6.6 | `sec:discussion-disclaimers` | What this thesis does not claim | `06_discussion_and_limitations.md` |
| 7 | `sec:conclusion` | Conclusion | `07_conclusion.md` |
| App. A | `sec:appA` | Variable definitions, sample flow, and authoritative sources | `appendices/A_variable_definitions_and_sample_flow.md` |
| App. B | `sec:appB` | Model specifications, inference conventions, and independent verification | `appendices/B_model_specifications_and_independent_verification.md` |
| App. C | `sec:appC` | Historical exposure-assignment diagnostics and the Ethiopia provisional analysis | `appendices/C_historical_diagnostics_and_ethiopia.md` |

## Note for a later renderer

Section numbers in the chapter prose (e.g. "Section 6.2") are not currently implemented as live cross-references (no `\ref{}` or pandoc-crossref `@sec:label` markup is embedded in the Markdown source, to keep the source readable as plain text). A renderer producing LaTeX or Word output should either (a) insert `{#sec:label}` after each heading using the labels above and convert in-text "Section X.Y" mentions to `@sec:label` before running pandoc-crossref, or (b) verify, after conversion, that the numbered section references in the rendered output still match this map's current section numbers (they will, as long as no section is inserted, deleted, or reordered without updating this map). This map must be updated in the same edit that adds, removes, or reorders any section.
