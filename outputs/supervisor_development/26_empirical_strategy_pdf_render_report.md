# PDF Rendering Report — Version 26 → Supervisor-Facing PDF

## 1. Source Markdown used
`outputs\supervisor_development\26_empirical_strategy_final_candidate.md` (content-approved, unchanged in
this pass).

## 2. Final supervisor-facing Markdown path
`outputs\supervisor_development\Thesis_Empirical_Strategy.md` — copied byte-for-byte from
`26_empirical_strategy_final_candidate.md`. Prior hash of the file being replaced was recorded before
overwrite: `656dd2baf2445cf8c5b0f7f24f267b1ccf3d3fc4254a50ab1da3e2cb192dfd0e` (matching the hash recorded at
the end of Stage 5G, confirming it was untouched between then and now).

## 3. Final PDF path
`outputs\supervisor_development\Thesis_Empirical_Strategy.pdf`

## 4. Archival Version 26 PDF path
`outputs\supervisor_development\26_empirical_strategy_final_candidate.pdf` — byte-identical to the file in
item 3 (same SHA-256: `81108a6f711a501e6919c222d089113213f4045e9f5bbf1401d1eaef130e6269`).

## 5. Page count
4 pages.

## 6. HAZ table syntax repair
Not required. The HAZ results table in `26_empirical_strategy_final_candidate.md` already used correct
three-column Markdown table syntax (header row, `|---|---|---|` delimiter row, three data rows). No repair
was made; the supervisor-facing Markdown is a byte-identical copy of Version 26 (`diff` confirms zero
differences).

## 7. Exact syntax-only change
None — no change of any kind was needed or made to the Markdown content in this pass.

## 8. Confirmation: no substantive content changed
Confirmed. `diff` between `26_empirical_strategy_final_candidate.md` and `Thesis_Empirical_Strategy.md`
returns zero differences. This task only (a) copied that file to the supervisor-facing filename and (b)
built a separate, hand-written LaTeX source for rendering — the LaTeX source was authored as a direct
typographic transcription of the same approved wording, with no wording added, removed, or altered beyond
Unicode-to-LaTeX symbol substitutions (e.g. "α" → `\alpha`, "—" → `---`) and one non-visible typesetting
aid (see item 14).

## 9. Confirmation: all empirical numbers identical to approved Version 26
Confirmed by direct comparison of every coefficient, CI, p-value, sample size, cluster count, region
count, and percentage between the Markdown and the LaTeX source used for rendering; all match exactly
(70,231 / 4,481 / 114 / 14-16-47-37 / 36,985-37,260-37,088 / 36,040-36,308-36,145 / 4,426 / 32%/51% /
0.007/0.011/0.35 / 0.75/0.67 / the HAZ table / the WAZ/WHZ paragraph / the Nigeria M1–M4 sequence and
cluster-FE result / the 10-of-12 age-heterogeneity result).

## 10. Confirmation: all equations substantively identical
Confirmed. Model A, Model B, Model C, Model D, Model E, and the conceptual historical-exposure equation
are all rendered with the same structure, terms, and subscripts as the Markdown source (Section 3 and
Section 6 of the PDF, pages 1–2 and page 4).

## 11. Confirmation: Section 7 identical
Confirmed. "7. What the current analysis tells us and what remains unresolved" on PDF page 4 reproduces
the two-paragraph text from Version 26 verbatim in substance (LaTeX-escaped dashes/quotes only).

## 12. Confirmation: the old Section 4 page-break problem is absent
Confirmed and fixed directly. A `\needspace{14\baselineskip}` control was placed immediately before the
Section 4 heading, forcing the heading, its full introductory paragraph, and the three-row HAZ table to
move together onto page 3 rather than splitting the heading/opening sentence across a page boundary. Page
2 ends with intentional trailing white space as a direct consequence of this control (see item 13) — this
is the accepted trade-off explicitly permitted by the task instructions ("move the entire Section 4 opening
to the following page rather than leaving an orphan heading").

## 13. Page-by-page visual inspection (rasterized at 130 DPI and inspected directly)

- **Page 1:** Title, Sections 1–2, and the start of Section 3 (Model A). Clean justified text, no clipping,
  no broken characters. One paragraph (the four-exposures sentence) shows visibly loose word-spacing
  because the two words "own-household" and "improved/non-improved" are long and hyphenation is disabled
  project-wide (an established convention carried over unchanged from Versions 22–24). This is a pre-
  existing characteristic of this exact sentence, present in the already-approved Version 24 PDF as well,
  not a new defect introduced in this render — flagged transparently in item 14 below.
- **Page 2:** Remainder of Section 3 — Models B, C ("Identification of the community-WASH coefficient"), D,
  and E, all five equations rendering correctly (proper minus signs, Greek letters, subscripts). Page ends
  with intentional trailing white space (~30%) caused by the `\needspace` control pushing Section 4 to page
  3 — not a stray formatting defect.
- **Page 3:** Section 4 in full — heading, introductory paragraph, and the three-row HAZ table all appear
  together at the top of the page, resolving the previously reported bad break. WAZ/WHZ paragraph, Nigeria
  subsection, and the age-heterogeneity paragraph follow cleanly. Section 5 heading appears with a full
  paragraph beneath it on the same page (not an orphan heading) before the paragraph continues onto page 4.
- **Page 4:** Remainder of Section 5, all of Section 6 (with its equation rendering correctly, no clipping,
  no wrapping outside margins) and all of Section 7. Page ends with normal trailing white space at document
  end. No title-discussion note present. No isolated joint-model p=.043 sentence present.

No malformed tables, no clipped equations, no encoding problems, no broken minus/multiplication signs, no
malformed subscripts, and no stray Markdown artifacts were found on any page.

## 14. Remaining layout concern

One cosmetic, pre-existing issue: the "Four exposures are constructed..." paragraph on page 1 has two
lines with looser-than-ideal word spacing (LaTeX `Underfull \hbox` badness 5533/1215), a direct consequence
of the project-wide no-automatic-hyphenation convention colliding with two long compound words in that
sentence. This is not new — the identical sentence produced the same underfull warning when Version 24 was
rendered. It does not cause clipping, overlap, or unreadable text, and fixing it would require either (a)
re-enabling hyphenation project-wide, which would reverse an explicit prior design decision across four
prior rendering stages, or (b) rewording the sentence, which is outside the scope of this rendering-only
task. Flagged here for awareness; no action taken without further instruction.

## 15. Confirmation: no analytical/data/web/Git work occurred
Confirmed. No regression was run, no data file was modified, no analytical script was modified, no
bibliography file was modified, no web search was performed, no historical-WASH data was searched for or
downloaded, and no Git command beyond a read-only `git status --short` was executed (status unchanged:
only the pre-existing untracked `outputs/supervisor_meeting/` folder). `24_empirical_strategy_revised.md`
and `24_empirical_strategy_revised.pdf` were preserved untouched (verified by unchanged SHA-256:
`07fe46bffd82d9a6298d33a698d9d2666156d36fe4fd550a2a310af15aa8d83a` for the PDF).
