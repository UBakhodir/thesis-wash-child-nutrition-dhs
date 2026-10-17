# Language-edit change log: Chapter 2 (Literature review and conceptual framework)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/02_literature_review.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `b25698000bee440ded9fbd77187dfbb94a18a8c46d42c6b2ddb44669a0f30312` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/02_literature_review.md` | `a9ceca1ad5baf93494b2a80eac3111d452cdf0f75b9fb596053bc63557b40de9` |

The full word-level diff is in `02_literature_review.worddiff.txt` (same folder). In that file, `[-…-]` marks removed text and `{+…+}` marks added text.

## How the edit was done

- **Tool.** The `humanizer` skill (v2.9.1, file `/root/.claude/skills/synced/…/humanizer/SKILL.md`) was read in full in this session and applied as a language edit to the publishing copy only, in its file mode. It was applied with judgement for academic prose:
  - Its "personality" section was not applied. The skill itself limits that section to opinion and personal writing; neutral register is correct for a thesis.
  - Em dashes used as punctuation (33 in the canonical file) were replaced with commas, colons, parentheses or new sentences.
  - En dashes in ranges and compounds (6–23, 18–24, pp. 2–5, faecal–oral, sanitation–stunting) are typographic and were kept, as in Chapter 1.
- **Not targeted.** No AI-detection outcome was targeted. The edit addresses clarity, sentence length, repetition and punctuation only.
- **Unchanged.**
  - All eight headings (wording and numbering).
  - All 30 citation commands: same keys, same order, each still attached to the same claim.
  - Every number and every quotation from a source.
  - All bold emphasis. Unlike Chapter 1, it was kept as bold, because Chapter 1's bold → italics change still awaits the author's decision (Chapter 1 open point 3).
- **Length.** Whitespace-separated tokens rose from 3,243 to 3,307. The canonical count includes 33 free-standing em dashes. The remaining increase comes from splitting long sentences, which needs new sentence subjects ("They…", "It is not…"). No content was added to lengthen the chapter, and nothing was cut to shorten it.

## Automated fidelity checks (canonical vs. edited copy)

| Check | Result |
|---|---|
| Numbers outside citations (53 tokens: years, sample sizes, 442/59, 172, 25 percentage points, OR 0.97 [0.95, 0.99], 10-percentage-point, twenty, 15 rounds, five countries, 18–24 months, 6–23 months, section numbers) | identical multiset. The one extra token is "Figure 2", moved from the Cumming2019 locator into the prose (item C1) |
| Citation commands in order (30) | identical key sequence; one locator shortened (item C1) |
| Quoted source wording ("the biological plausibility of WASH …", "all WASH arms", "WASH arm", "safely managed,", "transformative", "carries explanatory relevance beyond", etc.) | identical set |
| Headings | identical |
| Cross-references | same targets; "Section 2.2 and 2.5" → "Sections 2.2 and 2.5" (twice), as in Chapter 1 |
| `build.py lint ch02` and `lint --publishing-copies` | 0 problems |

## C. Citation and locator changes

**C1. Cumming2019 long locator (handover §7 item for ch02).** Canonical:

> … **SHINE's single combined WASH arm likewise showed no statistically detectable effect** [@Cumming2019, pp. 2, 5 and Fig. 2, which reports "all WASH arms" (plural) for Bangladesh/Kenya and "WASH arm" (singular) for Zimbabwe, reflecting this exact design difference].

Publishing copy:

> … **SHINE's single combined WASH arm likewise showed no statistically detectable effect**. Figure 2 of the consensus paper reflects this design difference in its own wording: it refers to "all WASH arms" (plural) for Bangladesh and Kenya and to the "WASH arm" (singular) for Zimbabwe [@Cumming2019, pp. 2, 5 and Fig. 2].

- The real locator, "pp. 2, 5 and Fig. 2", is unchanged character for character.
- The explanation now sits in the sentence the citation closes, so both the growth result and the Figure 2 wording stay attached to the same citation and pages.
- The quoted figure wording is unchanged. "Bangladesh/Kenya" → "Bangladesh and Kenya".
- This rests on `citation_map.md`, which records Cumming2019 as *full-text passage inspected (read in full, pp. 1–9)* and gives this exact Fig. 2 wording.
- The other Cumming2019 locators ("consensus message 2", "p. 6", "p. 2", "pp. 2–5, Fig. 2") were already short and are unchanged.

**C2. Removed internal pointer (§2.3).** The canonical sentence "This thesis cites the working-paper version of this study specifically (`bibliography_verification_ledger.md` records which version); it is cited for…" referred the reader to a repository file. That is internal package commentary, not scholarly content. It now reads "This thesis cites the working-paper version of the study. It is cited for…".
- The scholarly fact (working paper, not the published article) is kept in the prose.
- The reference list entry also identifies it as NBER Working Paper 21184.
- **Author decision:** restore the pointer if you want it (item A3).

No narrative author name needed changing. Every one already agrees with the `author` field of `bibliography.bib`: Black et al., Victora et al., Rakotomanana et al., Addae et al., Günther and Fink, Spears, Headey and Palloni, Geruso and Spears, "Donohue, Church, Assaf, and Mayala", Skoufias and Vinha, Balk et al., "Johnson, Jacob, and Brown", and "Blom, Ortiz-Bobea, and Hoddinott".

## Edits, by section

**2.1**
- The 100-word opening sentence is now three sentences:
  - the pathways ("distinct, separately evidenced");
  - the three conditions, with "(EED)" added at first use, since the abbreviation was used undefined in this chapter;
  - "The strength of the evidence varies across the three, and EED specifically is the least settled".
- "This biological plausibility is not challenged even by the strongest recent evidence…" → "Even the strongest recent evidence … does not challenge this biological plausibility". Same claim, active voice.
- The quotation is now its own sentence, with the same quotation and locator.
- "What this literature review is concerned with is a narrower, empirical question: does a facility-type classification — … — show…" → "This literature review is concerned with a narrower, empirical question. It asks whether a facility-type classification, that is, …, shows…". The final contrast with "whether WASH-related infection can plausibly affect growth at all" is kept as its own sentence.

**2.2**
- Addae et al. is now two sentences. The survey description stays: MICS, "comparable to, but distinct from, a DHS round". The findings are unchanged: sanitation and SES with both stunting and wasting; unprotected water with wasting **but not stunting**; children aged 6–23 months.
- Rakotomanana et al.: "link WHO/UNICEF JMP water and sanitation indicators" → "link the water and sanitation indicators of the WHO/UNICEF JMP". This fixes an unbreakable overfull line at "WHO/UNICEF". The non-universal "associations in the expected direction" is unchanged.
- "common to this literature, and squarely faced in this thesis" → "in this literature, and one this thesis faces directly".
- Headey and Palloni:
  - The design description is now its own sentence: 442 regions, 59 countries, difference-in-differences, region fixed effects, within-region change.
  - The mixed findings are two sentences. Piped water predicts reduced stunting. Sanitation predicts reduced diarrhoea and mortality but is *not* associated with stunting or wasting.
- The closing sentence is now three sentences: the parallel to Section 5; Section 6's use of it; and the warning against a "generally weaken" reading. "which overstates what this one study, on its own, establishes" → "which would overstate what this one study establishes on its own".

**2.3**
- First paragraph: the 70-word opening sentence is now two, which name the "two errors" a loose paraphrase risks. The timing sentence is split. "Section 2.2 and 2.5" → "Sections 2.2 and 2.5".
- "The randomised evidence…" (article added). This fixes an overfull line at "cluster-randomised".
- Trial design:
  - "each compared against a control" moved before the arm list, so it no longer reads as attached only to the last arm.
  - The SHINE dash clause became its own sentence: "SHINE therefore never tested … in the way the other two trials did."
  - The arms, their contents, "**four arms only**" and "2×2" are unchanged.
- The bold growth findings: the em-dash list inside the bold became a parenthesis. The bold wording is otherwise identical. For the Fig. 2 change see C1.
- Nutrition arm: "described by the trial authors as" → "which the trial authors describe as".
- Combined arm: "— that is, adding WASH to nutrition did not improve on nutrition by itself, in any of the three trials" → ": in none of the three trials did adding WASH to nutrition improve on nutrition by itself". The scope is unchanged (all three trials).
- The "not read as a WASH finding" sentence is now two sentences. "trial-component by trial-component" → "component by component".
- Diarrhoea: the em dash became a colon. All three site results are unchanged, as is "(against a low baseline prevalence)".
- "No statistically detectable effect" paragraph: split into three sentences. "adequately powered", "high internal validity", "consistent evidence across three sites" and the "absence of detected effect … not mathematical certainty" distinction are all kept.
- Consensus-statement paragraph: split into shorter sentences. Kept unchanged:
  - basic vs. "safely managed," piped, networked services;
  - "may be needed";
  - "transformative";
  - "consistent with, though it does not on its own confirm";
  - the three alternative explanations (confounding, measurement error, own limitations);
  - the closing disclaimer.
- Geruso and Spears:
  - Split into shorter sentences.
  - "a puzzle documented by prior literature and not explained by household characteristics alone" → "Prior literature had documented this puzzle, and household characteristics alone do not explain it."
  - "with one specific, striking exception: open defecation" → "Open defecation is the one specific, striking exception."
  - "roughly 25 percentage points", "not explained by relative wealth", "a substantial share", the working-paper version and "which Geruso and Spears do not study" are unchanged. For the removed file pointer see C2.

**2.4**
- Donohue et al.:
  - "in a DHS Spatial Analysis Report" moved to the front of the sentence.
  - The Nigeria and Zambia results are now separate sentences: aOR 0.97 [0.95, 0.99] per 10 points; household sanitation not significant; Zambia null in both models.
  - "which overstates a result significant in one of the two countries studied" → "that claim would overstate a result that was significant in only one of the two countries studied". Same scope.
- Skoufias and Vinha: unchanged in content (twenty countries; **no significant externality from community-level water coverage**; sanitation with fever/diarrhoea and HAZ; urban/rural variation). The "closer parallel" sentence is kept as written; see item A1.
- The 95-word novelty sentence is now three sentences. Every hedge is kept: "not aware of"; "does not … claim to have searched the literature exhaustively enough to assert … unprecedented more broadly"; "claims only…"; "not found replicated in the sources reviewed here".
- Balk et al.: "is an earlier methodological precedent" → "provide an earlier methodological precedent"; "though applied to mortality" → "although they apply it to mortality".
- Identification paragraph: the 70-word sentence is now three sentences. Kept: "nearly all", "almost entirely", "small mechanical residual", "(Section 4 derives this precisely)" and "region, not cluster, fixed effects".

**2.5**
- The first sentence was split at the em dash. "the anthropometric-outcome studies" → "the two anthropometric-outcome studies" (the two named immediately after).
- Günther and Fink and Spears now have separate sentences.
- "an individual child's current-age-varying anthropometric outcome" → "an analysis of an individual child's anthropometric outcome at varying current ages".
- "Nor does it describe the major WASH trials …, nor Headey and Palloni's…" → "The limitation also does not describe the major WASH trials …, or Headey and Palloni's…". Same scope.
- "this thesis is explicit that these are different empirical questions" → "this thesis treats these as different empirical questions".
- "is the reason this thesis's historical extension…" → "is the reason why…". The final clause is now its own sentence: "It is not a reason to expect a comparison of the two samples' results to isolate an exposure-timing effect (Section 6.2)."

**2.6**
- Displacement: "(undisclosed, per-cluster) displacement actually applied" → "the displacement actually applied, which is undisclosed and specific to each cluster". "whichever pixel or pixels are read … recorded, displaced coordinates" is unchanged.
- Extraction methods: now their own sentence. Containing-pixel vs. buffer average, area vs. population weighting, and "if population data for the area are available" are all kept. "labelled sensitivity" → "labelled sensitivity analysis".
- Blom et al.:
  - "— a design this thesis's historical extension borrows structurally" → ", a design whose structure this thesis's historical extension borrows".
  - The "cited here, and only here" sentence is now two sentences.
  - "15 rounds", "five West African countries", "is found to worsen" and both negative scope statements (no numerical finding; not WASH evidence) are kept.

**2.7**
- First sentence: "household and leave-one-out community WASH compared directly…" → "household and leave-one-out community WASH, compared directly…". "within the historical sample's own three countries" → "within the three countries of the historical sample". See item A2 for the "three design elements" count.
- "The methodological contribution claimed is narrower: a direct…" → "… is narrower. It consists of a direct…".
- The em-dash clause "— including its own unresolved issues —" became commas.
- Long sentence split:
  - "Both of those studies examine current-round community WASH exposure (geospatially modelled and DHS-census-based, respectively)…". The canonical "or" became "and" with "respectively", as the pairing intends.
  - "Neither source is cited here as calling for that specific extension: the gap is this thesis's own observation, not an attributed recommendation."
- "The gap this leaves open, and does not claim to close, is the same one…" → "The gap that remains open, and that this thesis does not claim to close, is the one that…".
- "local development improved facilities tend to accompany" → "local development that improved facilities tend to accompany".
- The final sentence was split. Both "does not resolve" clauses are kept.

## Items for the author to decide

- **A1. Possible inconsistency with Section 5.2 (substantive; not changed).** §2.4 says Skoufias and Vinha's result is "a closer and more precise parallel to this thesis's own baseline finding (Section 5.2) that community water and sanitation do not behave identically under full adjustment." In `05_results.md` Table 5.2, the two community coefficients are almost the same *under full adjustment*: water 0.033 [−0.083, 0.150], *p* = .573; sanitation 0.008 [−0.113, 0.129], *p* = .894. They differ at the earlier "+ socioeconomic status" stage: water 0.127, *p* = .034; sanitation 0.008, *p* = .900. And there the direction is the opposite of Skoufias and Vinha's, where sanitation, not water, carries the association. The sentence was kept as written because it states a thesis result, which this language edit must not change. Please check whether it should say "at the socioeconomic-adjustment stage", or whether "do not behave identically" refers to the joint model (§5.3) or to another outcome. Evidence: `manuscript/v12_2026-10-10/05_results.md` §5.2, Table 5.2.
- **A2. "Three design elements" (§2.7).** The sentence names two items joined by a semicolon. Read as three (household WASH; leave-one-out community WASH; early-life matching), the count is right. The comma added after "community WASH" keeps that reading possible. If you meant "two", change the number.
- **A3. Internal file pointer removed (C2).** Restore it if you prefer.
- **A4. Heading wording.** All headings were kept as written for contents and cross-reference stability. Two read awkwardly and could be shortened if you wish:
  - §2.5: "… survey designs specifically"; "specifically" could be dropped.
  - §2.3: "what the major trials actually found, and what they did not test".
