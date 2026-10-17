# Language-edit change log: Chapter 3 (Data and variable construction)

Status: **awaiting author review.** Not added to `chapters/APPROVED.tsv`.

| | File | sha256 |
|---|---|---|
| Canonical (unchanged) | `manuscript/v12_2026-10-10/03_data_and_variables.md` at `c58fc478e7b31789fc68e3c88cd25de4a6567c78` | `ed7b30b004ebf928cd159b1454c8f4fbfdc7dde7056e5e6367d4fd6eeecaa970` |
| Publishing copy (edited) | `publishing/thesis_render_v12/chapters/md/03_data_and_variables.md` | `9f9d9b187abd367c5412b128d55e234e6bb78acb5f18419d851390a9a1a91176` |

The full word-level diff is in `03_data_and_variables.worddiff.txt` (same folder). In that file, `[-…-]` marks removed text and `{+…+}` marks added text.

## How the edit was done

- **Tool.** The `humanizer` skill (v2.9.1, `/root/.claude/skills/synced/…/humanizer/SKILL.md`) was read in full in this session and applied to the publishing copy only. It was applied with judgement for academic prose, as in Chapters 1 and 2:
  - The "personality" section was not applied; the skill limits it to opinion and personal writing.
  - All 29 em dashes used as punctuation were replaced with commas, colons, semicolons, parentheses or new sentences.
  - The 9 en dashes are typographic ranges or compounds (2024–25, 2000–2017, 0–100, 2–10 km, Sections 3.5–3.8, disk–polygon, WASH–nutrition, water–HAZ) and were kept.
  - Long sentences were split, and a few defensive or idiomatic phrases were made plainer ("not an oversight papered over by…" → "not an oversight concealed by…").
- **Not targeted.** No AI-detection outcome was targeted. The edit addresses clarity, sentence length and punctuation only.
- **Unchanged.**
  - All ten headings (wording and numbering).
  - All three citation commands (`deOnis2006`, `Burgert2013`, `LBDWaSH2020`): same keys, same order, each attached to the same claim.
  - Every number, unit, formula (`$[0,1]$`), superscript, variable name and file path. All 19 code spans are identical.
  - Every qualification and hedge. Examples: "not a census", "not independently verified", "an open, unresolved measurement-universe question", "does not by itself adjudicate", "weighted conditional associations among eligible measured children", "does not claim that every historical exposure value is strictly measured before the outcome".
  - All bold and italic emphasis. Bold was kept, pending the Chapter 1 bold → italics decision. Four bold sentences now end inside the bold, and one changed subject, see below.
- **Length.** Whitespace-separated tokens rose from 3,369 to 3,418. The canonical count includes 29 free-standing em dashes. The rest of the increase comes from splitting sentences, which needs new subjects ("This is…", "The reason is…"). Nothing was added to lengthen the chapter, and nothing was cut to shorten it.
- **Self-reference kept as "section".** The chapter calls itself "this section", and the thesis refers to chapters as "Section 5" and so on. Both were kept, for consistency with the rest of the manuscript.

## Automated fidelity checks (canonical vs. edited copy)

| Check | Result |
|---|---|
| Numbers outside code spans (103 tokens: counts, years, km, percentages, 10⁻¹²/10⁻⁸/10⁻³, 1.01/1.03, section numbers) | identical multiset |
| Citation commands in order (3) | identical sequence |
| Code spans (19: `b19`, `age_m`, `v005`, `hv005`, `v021`, `country_psu`, `IDHSPSU`, `PERWEIGHT`, `RADIUS_M`, two script paths) | identical multiset |
| Math | identical (`$[0,1]$`) |
| Headings (10) | identical |
| Italic spans (14) | identical |
| Bold spans (13) | same content. Four now include the sentence's closing period. "**This control is constructed differently…**" → "**The age control is constructed differently…**", because the sentence now follows an inserted sentence, so "This" would be ambiguous. Wording otherwise identical. |
| Cross-references (25) | same targets; "Section 3.5–3.8" → "Sections 3.5–3.8" (as in Chapters 1 and 2) |
| Quoted strings (4) | identical apart from capitalisation: "exact" → "Exact" (now starts a sentence) |
| `build.py lint ch03` and `lint --publishing-copies` | 0 problems |

## Changes made for rendering (copy only; template unchanged)

| Item | Change | Reason |
|---|---|---|
| §3.4, Burgert2013 | "(urban clusters up to 2 km; rural clusters 99% up to 5 km and 1% up to 10 km; [@Burgert2013])" → "(urban clusters … 10 km) [@Burgert2013]" | A citation inside parentheses prints doubled parentheses. Same key, same claim, same position after the displacement distances. |
| §3.2 first sentence | "Three outcomes are constructed following standard DHS/WHO…" → "…constructed according to standard DHS/WHO…"; "Each is a standard-deviation z-score" → "Each outcome is a standard-deviation z-score" | Overfull lines: unbreakable "DHS/WHO" and "weight-for-height". |
| §3.3 first sentences | "Four exposures are constructed for the baseline sample:" → "The baseline sample has four exposures:"; "and similar sources for water" (a draft wording) reverted to the canonical "and similar for water" | Overfull lines at "improved/non-improved" and "wells/springs". |
| §3.3 script path | "implemented in `scripts/…/08_hr_cluster_wash_exposure.py`" → "implemented in the script `…`" | The path broke as "…exposure." / "py". It now breaks inside the file name, at an underscore. |
| §3.8 first sentence | "Historical models control for…" → "The historical models control for…" | Overfull line at "country-by-birth-year". |
| "2 km", "5 km", "10 km", "~5×5 km", "2–10 km" (8 places) | normal space → non-breaking space | "2" and "km" were split across lines on page 3. |

## Edits, by section (summary; full detail in the word diff)

- **Opening paragraph.** "They are built…" → "The two samples are built…"; the em-dash aside on Section 5 became its own clause.
- **§3.1.** The em dash before "it is the universe…" became a sentence break.
- **§3.2.** The outcome definitions were split into two sentences. The common-sample sentence was split at "This gives…". In the `b19` sentence, the em dash became a semicolon. The parenthetical on `age_m` was split into two sentences inside the same parentheses.
- **§3.3.** The JMP classification list moved out of an em-dash aside into a colon clause and a following sentence. The bold definition now ends at "own household."; the "not a census…" qualification follows as its own sentence, unchanged in content. The exclusion rule ("excluded from **both** the numerator and the denominator…; they are not merely treated as unimproved") is unchanged in content. The Basic+Limited and Ghana-biodigester sentences were split.
- **§3.4.** The KR / BR / `v005` / `hv005` / `PERWEIGHT` / `v021` / `country_psu` / `IDHSPSU` passage was broken into shorter sentences. Every field name, every "not the same field under two names" qualification, and the 1,000,000 rescaling are kept. "lives only in" → "exists only in".
- **§3.5.** The country list is now set off with commas, not em dashes. The W_IMP and S_IMP definitions became separate sentences. "The reason is that…" now introduces the Ethiopia calendar explanation. "which this or any other available data source cannot provide" → "which neither this nor any other available data source can provide".
- **§3.6.** The displacement-versus-radius distinction became a separate sentence ("The displacement distances are a different matter: they describe the *uncertainty*…, whereas the buffer radius defines the *area averaged*…"). The AEQD, overlap, validation and coverage sentences were split, and every figure is kept.
- **§3.7.** The completion-check sentence (previously one sentence with three em-dash clauses) became four sentences, one per window type. Content and bold emphasis are unchanged.
- **§3.8.** The country-by-birth-year explanation moved out of the control list into its own sentence. "for a documented, non-fixed-effects reason" → "for a documented reason that does not rest on fixed effects". The wealth trade-off passage is unchanged in content. The final paragraph's em dashes became commas and parentheses.
- **§3.9.** The three-count explanation, previously one em-dash sentence, became four sentences: "These three counts differ by construction. The official count is… The extract is… The estimation sample further requires…".

## A. Points for author review (not changed)

**A1. Grouping key of the leave-one-out exposure versus the cluster fixed effect (documentation precision).**
- §3.4 names `v021` (→ `country_psu`) as "the baseline's cluster identifier". §3.3 defines community WASH over "HR households in the same DHS cluster".
- In code, the leave-one-out rate is grouped on country + `hv001` (`08_hr_cluster_wash_exposure.py`, lines 412–416) and linked to children through country + `v001` + `v002` (Phase F, line 489).
- The fixed effects and standard-error clustering use `country_psu` = country + `v021` (`04_build_country_kr.py` line 170; `05_pool_countries.py` line 133; `14_household_community_wash_models.py`).
- No check that `v001` equals `v021` in every row was found in the stored code. Whether they coincide in the four KR files cannot be checked here: it needs the restricted DHS files, which were not used.
- The chapter is not shown to be wrong. If the two codes ever differ, "cluster" means slightly different units for the exposure and for the fixed effect. Consider confirming this locally and, if useful, stating it in Appendix A.

**A2. "singleton-cluster exclusions described above" (§3.9).** Chapter 3 does not describe a singleton-cluster exclusion. It is described in Sections 4.5–4.6 and Appendix A.3. A cross-reference such as "(Section 4.5)" would make the sentence accurate. Not changed, because it alters a reference target.

**A3. "child-year" in §3.6.**
- Coverage status is computed per cluster-year (`10_spatial_extraction_v3.py`, `FULL_TOL = 1e-3`). Every child in the cluster inherits it.
- A child's window is "complete" only if every annual value it needs has status `full` (`12_construct_exposure_windows.py`, `complete_primary`).
- The chapter's wording has the same effect. Optional precision only.

**A4. Details the task brief lists that the canonical chapter does not state.** Nothing was added; all of them are recorded elsewhere in the repository.
- `hw70`–`hw72` ÷ 100 scaling and the special codes 9996–9999. Recorded in `docs/data_dictionary.md` and `02_load_flag_anthro.py`. The chapter says only "flagged valid … per DHS's own flagging convention".
- `KIDWT`. Appendix A.4 records it as a population factor, not used.
- IHME `LOWER`/`UPPER`. The extraction stores LOWER, MEAN and UPPER; the windows use MEAN. The chapter does not mention the bounds, so nothing presents them as confidence intervals.
- Birth-month rule. In code, the prenatal window is b−9 … b−1 (birth month excluded) and the post-12/24 windows are b … b+L−1 (birth month included). The chapter's "nine months before birth" and "first 12 completed postnatal months" are consistent with this but do not state it.

  If you want any of these in the chapter, add them to the canonical v12 file and re-run this preview.

**A5. Outside Chapter 3.** `docs/data_dictionary.md` §2 calls the HR file "the DHS household census". The chapter correctly says the leave-one-out rate is "not a census of every household physically present". The repository's data dictionary could be aligned. This package does not edit it.

## B. Bibliography data seen in this preview (for the final-assembly bibliography step)

- **`deOnis2006` (new).** The printed entry includes the `note` field's publisher-metadata commentary ("Print/issue year 2006 … not an error in this citation's year field"). It also shows a wrong opening quotation mark ("”first published”"). This is the same kind of issue as the `GerusoSpears2015` note (Chapter 2 open point 5).
- **`Burgert2013`.** "DHS Spatial Analysis Reports" is plural (already open, Chapter 2 point 5).
- **`LBDWaSH2020`.** No volume or pages; stray comma before the DOI (already open, Chapter 1 point 4).
- **DOI breaks.** The `deOnis2006` DOI breaks inside a number ("…2227.20 / 06.tb02378.x"). This is the shared xurl issue (Chapter 1 open point 5).

Correct these only from verified records, in a dedicated bibliography or template step.
