# Language-edit change log: Chapter 1 (Introduction)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/01_introduction.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `008f7be57b61420ca36387b28fb8b699ca85a4b3473b0e1833de8815531d085b` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/01_introduction.md` | `2203446d80d78f2e13a82d1a65c735657a31e1046951b2c668920561a9f22c3e` |

The full word-level diff is in `01_introduction.worddiff.txt` (same folder). In that file, `[-…-]` marks removed text and `{+…+}` marks added text.

## How the edit was done

- **Tool.** The `humanizer` skill (v2.9.1) was read and applied as a language edit to the publishing copy only. Its rules were applied with judgement for academic prose:
  - Em dashes used as punctuation were replaced with commas, colons, parentheses or new sentences.
  - En dashes in numeric ranges and compound terms (2024–25, 2000–2017, water–HAZ, WASH–child-growth, Sections 5–6) are typographic, not stylistic, and were kept.
- **Not targeted.** No AI-detection outcome was targeted. The edit fixes clarity, repetition, sentence length and punctuation only.
- **Unchanged.** All nine headings (wording and numbering), all six citation groups (same keys, same order, same claim attached) and every number.

## Automated fidelity checks (canonical vs. edited copy)

| Check | Result |
|---|---|
| Every number and its rounding (69 numeric tokens, including signs, CIs, *p*-values, years, percentages, section numbers) | identical multiset |
| Citation groups, in order | identical: `[@Victora2008; @Victora2010; @Black2013]`, `[@CummingCairncross2016]`, `[@Donohue2023; @SkoufiasVinha2026]`, `[@Rakotomanana2020]`, `[-@Addae2024]`, `[@LBDWaSH2020]` |
| Headings | identical |
| Cross-references | same targets; "Section 4.2–4.3" → "Sections 4.2–4.3" and "Section 3.5–3.8" → "Sections 3.5–3.8" (plural for a range) |
| `build.py lint --publishing-copies` | 0 problems |
| Whitespace-separated tokens | 2,061 → 2,063. The canonical count includes 17 free-standing em dashes; one non-substantive sentence was removed (see item 1 below) |

## Edits, by section

**Opening paragraph**
- Split the long mechanism sentence into three. Kept the content and hedges unchanged:
  - "distinct, separately evidenced pathways";
  - diarrhoea "supported by association … demonstrating causation is challenging";
  - helminths "strongly associated";
  - EED "the least settled … explicitly flagged as needing more research".
- "None of this plausibility is disputed even by the strongest recent causal evidence…" → "Even the strongest recent causal evidence … does not dispute this plausibility". Same claim, active voice.
- "(Section 2.3 discusses this distinction precisely)" → "(Section 2.3 discusses the distinction in detail)".
- "is the right exposure to look for it in" → "is the right exposure in which to look for it".

**1.1**
- Removed the em-dash interruption around the definition of the two exposures.
- "is not a modelling convenience; it corresponds…" → "is not a modelling convenience: it corresponds…".
- "The distinction is not a claim that…" → "Nor is it a claim that…".
- **Merged a repeated sentence.** The canonical text says the thesis "constructs and reports both" and then, in the next sentence, "constructs and compares both". The two are merged into one sentence that keeps every element: why both are needed (the Donohue/Skoufias–Vinha point), what they are, and the leave-one-out guarantee.
- Bold on "own-household WASH" / "surrounding-community WASH" changed to italics, as defined terms. The same bold → italic change was made for the research question in 1.2, "associations under a cross-sectional design" (1.3), "not the same children" (1.4) and "baseline/historical sample" (1.5).
- In 1.5, the bold on "does **not** reproduce" was dropped; the word "not" stays.

**1.2**
- Broke the first 90-word sentence into three: the affected literature; its examples (Rakotomanana et al., Addae et al., this thesis's baseline); and the measurement problem.
- "does not describe the major WASH-intervention trials … nor does it describe panel designs" → "does not apply to the major WASH-intervention trials … nor to panel designs". Same scope.
- Second paragraph: the "rather than asking … — which … — the extension asks" construction is now two sentences: "It does not ask whether … Instead, the extension asks…".
- "(Section 6.2 states this precisely)" → "(Section 6.2 sets this out)".
- **Citation placement.** The IHME source was moved out of a parenthetical. In the canonical sentence, `[@LBDWaSH2020]` sits inside parentheses, so it rendered as "…estimates (Local Burden of Disease WaSH Collaborators 2020))", with doubled parentheses. It now reads "…for a defined early-life window, using IHME's gridded 2000–2017 drinking-water and sanitation access estimates (Local Burden … 2020)". Same source, same claim.
- "This is a measurement improvement on one specific dimension — …— not a resolution … and not a reconstruction …" → "The extension improves measurement on one specific dimension, by …. It does not resolve … and it does not reconstruct …". Both negations are kept.
- The parenthetical list of the extension's four limitations is kept word for word, with "and" added before the last item.

**1.3**
- "after accounting for household and cluster-level confounding" → "after accounting for household- and cluster-level confounding". This is a hyphenation fix with the same meaning.
- "within the historical sample's own three countries" → "within the three countries of the historical sample".
- The causal disclaimer and the warning against reading the comparison as an exposure-timing test are kept in full. They are now split over shorter sentences.

**1.4**
- The historical rounds are now given as "(Ghana 2014, Kenya 2014, and Nigeria 2018)" instead of a list set off by dashes.
- "the Ethiopian-calendar interview-date conversion required to place…" → "the conversion of Ethiopian-calendar interview dates that is required to place…". It still says the conversion "could not be fully validated" and that Ethiopia is "provisional".
- The last sentence was split in two.

**1.5**
- "which should not be read as one combined design" → "and they should not be read as one combined design".
- "Section 4.2–4.3" / "Section 3.5–3.8" → "Sections …".
- "genuine early-life temporal exposure variation" → "genuine temporal variation in early-life exposure".
- "Having a particular combination of four countries is not…" → "A particular combination of four countries is not…".
- The final sentence was split. The limitations are still described as "integral to [the] interpretation rather than … closing caveats".

**1.6**
- Lead-in: "Stated briefly here and developed with full uncertainty in Sections 5–6: household-level WASH…" → "The main findings are summarised briefly here; Sections 5–6 develop them with full uncertainty. Household-level WASH…". The first rewording caused an unbreakable overfull line at "Household-level", so this version was chosen.
- The WHZ exception and the sentence "consistent with, but not conclusive proof of, confounding" are now separate sentences.
- The historical estimate's sensitivity is now its own sentence: "It is, however, sensitive to the weighting convention used…".
- Non-breaking spaces were inserted in "β per 10 percentage points" so that "(β" does not end a line. They are invisible in the PDF.
- **Every number, CI, *p*-value and qualifier is unchanged.** This includes "crossing a 10% but not a 5% threshold", "0.41 unweighted on the same observations" and "nothing more".

**1.7**
- "It is not a panel, not a difference-in-differences design, and not an instrumental-variables design" → "It is not a panel, difference-in-differences, or instrumental-variables design".
- The em-dash list of limitations is now a sentence ("The principal limitations are …"). All five items are kept.

**1.8**
- The first sentence was split in two.
- "reports results" → "reports the results".
- "states in detail why" → "explains in detail why".

## Items for the author to decide

1. **Removed sentence (1.8).** This sentence was removed from the publishing copy: "A note on the thesis title, and other administrative items not yet confirmed, are recorded in the author checklist accompanying this manuscript package, not in the chapter text." It is an internal note about the manuscript package, not thesis content, and the task excluded internal commentary from the chapter prose. The canonical file still contains it. If you want it back, restore it in `chapters/md/01_introduction.md` and run `preview ch01` again.
2. **Heading 1.6, "A restrained summary of findings".** This heading was left unchanged. To match the contents page and the cross-reference map, every heading was kept as written. "Restrained" is unusual in a thesis heading; "Summary of findings" would be the plainer choice. Your call.
3. **Bold → italics** for emphasis (listed above). This is a typographic choice; revert in the publishing copy if you prefer bold.
