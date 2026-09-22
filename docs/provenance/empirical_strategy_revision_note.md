# Empirical Strategy Document — Revision Note

This note records the final wording revisions applied to `docs/empirical_strategy.md` during drafting,
relative to its immediate predecessor draft. The revision was a surgical wording pass only: it inherits
all empirical numbers, sample sizes, geographic-hierarchy counts, and equations unchanged from the
preceding, separately validated draft. No new verification of numbers was required or performed in this
pass, since no number was touched.

## 1. All empirical numbers inherited unchanged from the preceding draft

Confirmed programmatically: every numeric token in the two drafts is identical, in the same order (see
diff below). No coefficient, confidence interval, p-value, sample size, cluster count, region count, or
percentage differs between the preceding draft and the final wording.

## 2. The four textual changes made

**Change 1 — Section 4, results introduction.**
Before: *"In the minimally adjusted community models, they do: community WASH coverage is associated with
sizeable, statistically significant gains, particularly for HAZ."*
After: *"In the minimally adjusted community models, several associations are positive and statistically
significant, particularly for HAZ."*

**Change 2 — Section 4, interpretation of attenuation.**
Before: *"This pattern is consistent with residual confounding in the unadjusted associations, but the
data here do not establish that as the only explanation, and it should not be read as evidence that WASH
has no effect on child nutrition."*
After: *"The attenuation shows that the minimally adjusted associations are sensitive to socioeconomic and
geographic adjustment, although the current analysis cannot determine which factors account for that
change. This should not be read as evidence that WASH has no effect on child nutrition."*

**Change 3 — Section 6, within-location variation.**
Before: *"...together could produce exactly the kind of within-location variation the current design
lacks: a cluster fixed effect could..."*
After: *"...together could potentially provide within-location temporal variation in early-life WASH
exposure that is unavailable in the current survey-date community measure: a cluster fixed effect
could..."*

**Change 4 — Section 6, feasibility paragraph.**
Before: *"...a WASH measure that is substantively meaningful rather than a coarse proxy, and ideally
observed rather than modelled; independence from DHS data itself..."*
After: *"...a WASH measure that is substantively meaningful rather than a coarse proxy; independence from
DHS data itself..."* (the clause "and ideally observed rather than modelled" was deleted; no replacement
clause was added, keeping the feasibility discussion neutral on observed-vs-modelled historical sources).

## 3. No empirical number changed

Confirmed: a token-level comparison of every numeric string in both files (coefficients, CIs, p-values,
sample/cluster/region counts, percentages) shows an identical, identically-ordered set in Version 25 and
Version 26.

## 4. No equation changed

Confirmed: all display equations (Models A–E and the conceptual historical-exposure equation) are
byte-identical between the two files. `diff` confirms zero lines changed inside Sections 1–3, and Section
6's equation line is untouched — only the surrounding prose sentence was reworded.

## 5. Section 7 preserved

Confirmed: Section 7 ("What the current analysis tells us and what remains unresolved") is byte-identical
between Version 25 and Version 26 — no grammatical adjustment was needed there.

## 6. No new regression was run

Confirmed. This pass made only text substitutions in a Markdown file; no code was executed against any
data file, and no statistical model was estimated or re-estimated.

## 7. No data/script/output/bibliography file was modified

Confirmed via file-listing checks: no file under `data/`, `scripts/dhs_harmonization/`,
`outputs/regressions/`, `outputs/final_tables/`, `outputs/final_figures/`, `outputs/final_appendix/`, or
`thesis-wash-child-nutrition-dhs/sources/bibliography/` was touched. `24_empirical_strategy_revised.md`,
`24_empirical_strategy_revised.pdf`, `25_empirical_strategy_final_revision.md`,
`25_empirical_strategy_validation_report.md`, `Thesis_Empirical_Strategy.md`, and
`Thesis_Empirical_Strategy.pdf` are all unmodified.

## 8. No web or historical-data research was performed

Confirmed. No web search, no dataset lookup, and no historical-WASH feasibility research occurred in this
pass — only a wording edit was made to the existing feasibility-discussion paragraph.

## 9. No Git operation occurred

Confirmed. No `git add`, `git commit`, or `git push` was run.

## 10. No PDF was created or modified

Confirmed. Only two new Markdown files were written this pass (`26_empirical_strategy_final_candidate.md`
and this validation note). No `.pdf` file was created, regenerated, or modified.
