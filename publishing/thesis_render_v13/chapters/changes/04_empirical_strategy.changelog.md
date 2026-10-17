# Language-edit change log: Chapter 4 (Empirical strategy)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/04_empirical_strategy.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `3955ff27f5db6f2076592ffbf5892f36fb07c1960865c527ca73822f6c0389f2` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/04_empirical_strategy.md` | `61f972e3df2346787af5d7654c37f5d96590d3500df178b9741414c70177fa4e` |
| Generated LaTeX | `publishing/thesis_render_v12/chapters/tex/04_empirical_strategy.tex` | `8d508baf09ec5e2d6044db1f4f5d2cb74c42256260b269167817b372ccbd4c37` |

The full word-level diff is in `04_empirical_strategy.worddiff.txt` (same folder). In that file, `[-…-]` marks removed text and `{+…+}` marks added text.

## A. Points for author review (found by checking the chapter against the code; nothing below was changed in the chapter)

The chapter was checked against the estimation code and the stored, public outputs only. No restricted data was read, no model was refitted and no estimator was changed. Each point gives the passage, the evidence, why it matters and a proposed correction. **The wording of the publishing copy still follows the canonical text in every one of these places**, so the author can decide.

### A1. §4.5 "Weighting": the parenthetical "(equivalently, $N/M$ on average across countries)" (substantive notation point; correction proposed)

- **Passage.** "…so that each country's weights sum to exactly $1$ (equivalently, $N/M$ on average across countries)."
- **Evidence.**
  - `scripts/dhs_harmonization/11_main_regressions.py`, `build_temporary_pooled_weight()`, computes `weight_original / W_k` and stops the run unless every country's weights sum to 1.0.
  - `scripts/historical_wash/16_estimate_preliminary.py`, `equal_country_weights()`, computes `w0 * (n / K) / tot`, with `K` = number of samples (countries). Its country totals are therefore $N/M$.
- **Why it matters.** Under the formula as displayed (the baseline implementation), each country total is 1: the totals average 1, the weights add up to $M$, and the mean weight per child is $M/N$. "$N/M$ on average across countries" is the historical pipeline's country total, which the same paragraph introduces two sentences later as a *difference* between the pipelines. A reader can take the parenthetical to mean that the baseline totals are $N/M$, which contradicts the next sentences and the code.
- **Proposed correction** (author's decision). Delete the parenthetical: "…so that each country's weights sum to exactly $1$." Alternatively, replace it with "(so the weights sum to $M$ across the pooled sample)". Both keep the following sentences on the historical $N/M$ scaling unchanged.

### A2. §4.5 "Estimator and inference": the convention for the region-fixed-effects models is not stated (description gap; optional addition)

- **Passage.** The paragraph states the CRV1 correction and the normal reference distribution for the *cluster-fixed-effects* fits only ("`use_t: False` for the primary cluster-fixed-effects fits"). The region-FE models (§4.1, §4.3, the joint model in §4.4 and the region-FE age-heterogeneity model) are not covered.
- **Evidence.**
  - In `14_household_community_wash_models.py`, `run_explicit_wls()` fits the region-FE models as explicit-dummy WLS with `cov_type="cluster"`, clustered on `country_psu`. The region dummies and the constant are columns of the design, so the statsmodels correction counts them in $K$.
  - These fits use the same statsmodels default as the cluster-FE fits. Recomputed from the stored coefficient and SE, the stored p-values match the normal reference exactly:
    - `02_household_region_fe.csv`, water–HAZ: .3573831290379641 (normal) vs. .3574333 (*t*(*G*−1));
    - `05_joint_household_community.csv`, household water–HAZ: .04344011591052318 (normal) vs. .0435003 (*t*(*G*−1)).
- **Why it matters.** The chapter's general statement ("the baseline pipeline … does not select *t* inference") is correct. The finite-sample correction given ($K$ = non-fixed-effect regressors only) applies to the cluster-FE case, however, and a reader could carry it over to the region-FE models.
- **Proposed optional addition** (author's decision): "The region-fixed-effects models (Sections 4.1, 4.3 and 4.4) are fitted as weighted least squares with explicit region dummies and clustered on `country_psu`; their finite-sample correction counts the region dummies and the constant in $K$, and their confidence intervals and p-values also use the normal reference distribution."

### A3. §4.5 "Rank and identification": "is dropped and named explicitly" describes the historical mechanism (precision; optional)

- **Evidence.**
  - `16_estimate_preliminary.py` drops absorbed columns automatically and records them in `columns_absorbed`.
  - The baseline code (`run_explicit_wls()`, `run_cluster_fe_demeaned()`) checks rank and **stops** with an error if the design is rank-deficient; it does not drop columns. The only column removed in baseline cluster-FE models is `residence`, excluded by explicit pre-specification and documented in §4.2.
- **Why it matters.** The outcome is the same: no unstable coefficient is reported. The mechanism differs, though, and the chapter otherwise describes the two pipelines separately.
- **Proposed optional wording:** "…the historical pipeline drops any fully absorbed column and names it; the baseline pipeline stops if the design is rank-deficient, and its only pre-specified exclusion (`residence` under cluster fixed effects) is stated in Section 4.2."

### A4. §4.5 "Singleton-cluster treatment": "the baseline tables above" (cross-reference)

- The baseline tables are in Section 5, which follows Chapter 4. **Proposed:** "the baseline tables in Section 5".

### A5. Dependence on the open Chapter 3 verification question (FA-6 / FA-7 B; not resolved here)

- §4.3 says that within a cluster each child's leave-one-out value differs only by the excluded household. The community exposure is built from `hv001` (linked through `v001`), while the fixed effects and clustering use `v021` (`country_psu`).
- Whether `hv001`/`v001` and `v021` correspond one-to-one in every baseline country can only be checked with the restricted baseline data, in the local VS Code environment. This session did **not** check it, and nothing here should be read as resolving it. The question is recorded in `FINAL_ASSEMBLY_REGISTER.md`.

### A6. Items checked with no change needed

- **`group_debias`.** Chapter 4 does not mention it.
  - Appendix B describes it accurately, and `24_reconcile_inference_corrections.py` confirms the description: the *validation* scripts' `PanelOLS.fit(..., auto_df=True)` call lacked `group_debias=True`; adding it makes linearmodels' $[N/(N-K)]\times[(G/(G-1))(N-1)/N]$ equal to `16_estimate_preliminary.py`'s $\frac{G}{G-1}\frac{N-1}{N-K}$.
  - The CI and p-value are computed explicitly from *t*(*G*−1), not from linearmodels' native `df_resid`-based output.
  - No addition to Chapter 4 is proposed.
- **Measurement-subsample weighting qualification.** It is not part of Chapter 4 (it is stated in Chapter 3). Nothing was added or removed here.
- **Ethiopia.** Chapter 4 does not mention Ethiopia. $M=3$ (Ghana, Kenya, Nigeria) for the established-date pooled models matches the code; Ethiopia enters only `sens_ethiopia_PROVISIONAL` models.

## B. How the edit was done

- **Tool.** The `humanizer` skill (v2.9.1) was read in full in this session and applied to the publishing copy only, as in Chapters 1–3.
  - The "personality" section was not applied.
  - No AI-detection outcome was targeted.
  - The edit addresses sentence length, punctuation and flow.
- **Em dashes.** All 44 em dashes (all used as punctuation) were replaced with commas, colons, semicolons, parentheses or sentence breaks. The 15 en dashes, all ranges or compounds, were kept (15 in the canonical file, 15 in the copy): 0–5 … 48–59, 12–23, 0–100, Frisch–Waugh–Lovell, water–HAZ, Sections 3.5–3.7.
- **Unchanged.**
  - All 7 headings (wording and numbering).
  - All 90 numbers outside code and math (identical multiset).
  - All 14 code spans: `v005`, `PERWEIGHT`, `use_t: False`, `run_log.txt`, `sizes >= 2`, `statsmodels`, script paths, `build_temporary_pooled_weight()`.
  - All 22 bold spans; two (the wealth sentence in §4.2 and the baseline-singleton sentence in §4.5) now include their closing full stop.
  - All 21 italic spans.
  - Both quoted strings ("minimally adjusted", "1.385").
  - All 7 display equations and 73 inline math expressions, apart from the layout markup in section C.
  - There are no citations, in the canonical file or in the copy.
- **Hedges, qualifications and evidential strength kept.** Examples:
  - "associational, not causal";
  - "not a formal proof that the 0.58-versus-1.03 gap is explained by this mechanism alone";
  - "a description gap, not assumed to be numerically inconsequential";
  - "not a byte-for-byte rerun of its original, unpreserved code";
  - "not as certainty about exactly what that specific, no-longer-existing script did";
  - "does not interpret a 10-point coefficient as describing an exposure contrast that is typically observed within a cluster";
  - "It does not establish that the equation identifies a causal parameter".
- **Length.** Whitespace-separated tokens rose from 3,500 to 3,561. The canonical count includes free-standing em dashes. The rest of the increase comes from splitting long sentences, which needs new subjects ("They…", "Here…", "This…").

## C. Changes made for rendering (copy only; template unchanged)

| Item | Change | Reason |
|---|---|---|
| §4.4 age-heterogeneity equation | Set as a three-line `aligned` display (break before the interaction sums and before $X_i'\gamma$). Every term, subscript, superscript and summation range is unchanged. | It was 172 pt wider than the text block (known issue in `HANDOVER.md` §7). Type size and margins were not changed. |
| $\bar{C}^{water}$, $\bar{C}^{san}$ (6 places) | `^{water}` → `^{\,water}`, `^{san}` → `^{\,san}` (thin space) | The superscript touched the italic C, because Times New Roman has no math italic correction (checklist note F2). The symbols are unchanged. |
| Opening paragraph | "is a panel, a difference-in-differences design…" → "is a panel design, a difference-in-differences design…" | Overfull line (12.7 pt): the hyphenated compounds can only break at their own hyphens. The meaning is unchanged; the wording now parallels the other two terms. |
| §4.5 weight formula | Blank lines around the display removed | The continuation "so that each country's weights sum…" was indented as a new paragraph. |
| §4.6 "(Section 3.5–3.7)" | → "(Sections 3.5–3.7)" | Plural, as in Chapters 1–3. Same targets. |

## D. Edits by section (summary; full detail in the word diff)

- **Opening.** The sentence on panel/DiD/IV designs was split from the sentence on how those terms are used.
- **§4.1.**
  - The em-dash aside on joint estimation became its own sentence.
  - The long within-region identification sentence was split: "They compare households inside the same administrative region…; variation between regions does not enter, because the region fixed effect removes it by construction."
  - "$\delta_r$ leaves room for clusters … to still differ" → "$\delta_r$ still allows clusters … to differ".
- **§4.2.**
  - The absorption sentence was split; the em-dash list (local infrastructure, environment, market access) is now in parentheses.
  - "One mechanical consequence:" → "One consequence is mechanical."
  - The bold wealth sentence now stands alone, and the parenthetical support figures follow it.
  - "and none was observed to" → "and no such removal was observed".
- **§4.3.**
  - The definition sentence was split.
  - "It can be, but" → "It could be, but".
  - The comparison with §4.6 now reads "is in a fundamentally different situation: there, a real time dimension (birth-cohort variation within the same cluster)…".
- **§4.4.** Em-dash lists became parentheses. The Wald-test sentence was split before "Each is referred to a $\chi^2$ distribution…". "not a reconstruction" became its own sentence.
- **§4.5.**
  - **Weighting.** The definition of $\text{raw}_i$ now begins "Here…". "computed within that model's own final estimation sample" now has an explicit subject ("The weight is computed…"). The machine-precision confirmation is a parenthetical sentence.
  - **Estimand.** "It is important to be precise about…" → "What the weighting scheme does and does not imply for that single pooled $\beta$ therefore needs to be stated precisely."
  - **Inference.** "(`…14_household_community_wash_models.py`'s `statsmodels` calls)" → "(the `statsmodels` calls in `…14_household_community_wash_models.py`)". The recomputation evidence now opens with "Independent recomputation confirms this:". "a rounded-table check" → "a check of the rounded table". The final sentence was split.
  - **Singletons.** "Before estimation" moved to the front.
  - **Rank.** "This is a statement that … it is not a statement that…" → "This establishes that … It does not establish that…".
- **§4.6.**
  - The birth-year paragraph was split into shorter sentences.
  - The Nigeria mechanism is now three sentences ("Under the pooled scheme, Nigeria keeps…").
  - The $X_{ic}$ and wealth clause became two sentences.
  - "conditional on there being enough…" was kept; "quantified, per model, as…" now opens with "That variation is quantified…".
