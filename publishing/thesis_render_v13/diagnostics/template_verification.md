# 1. Diagnostic heading level 1: template verification

Diagnostic paragraph, not thesis text. Every sentence in this document is a placeholder written only to occupy lines so that the layout can be measured; none of it describes the thesis data, methods or findings, and none of it may be copied into the manuscript. This paragraph tests the main-text setting: Times New Roman at 11 pt on an exact 19.5 pt baseline distance, justified, on A4 paper with a 2.5 cm left margin, a 4.0 cm right margin and 2.8 cm top and bottom margins.

Citation test using keys from the canonical bibliography; the citations below are attached to no claim. Parenthetical form [@Victora2010]. Two works in one citation [@Victora2010; @Burgert2013]. Narrative form with the author names written in the text, as in the manuscript: Burgert, Colston, Roy, and Zachary [-@Burgert2013]. Locator syntax, with an arbitrary page value that supports nothing [@Burgert2013, p. 1]. Footnote test.^[Diagnostic footnote: Times New Roman 9 pt on an exact 13.5 pt baseline distance. This second sentence exists only to make the footnote wrap onto a further line, so that the footnote baseline distance can be measured from the PDF.]

## 1.1 Diagnostic heading level 2

Line-count test paragraph. A full page of main text should hold thirty-five lines at the specified size and baseline distance. Placeholder sentence one. Placeholder sentence two continues the paragraph so that it runs over many lines. Placeholder sentence three adds further words with no meaning beyond their length. Placeholder sentence four keeps the paragraph going across the page. Placeholder sentence five is here for the same reason. Placeholder sentence six adds a few more words. Placeholder sentence seven continues the measurement text. Placeholder sentence eight fills another part of a line. Placeholder sentence nine is similar. Placeholder sentence ten closes the first block of filler.

Second line-count test paragraph. Placeholder text continues with ordinary words of ordinary length, so that hyphenation and justification behave as they would in prose. Placeholder sentence eleven. Placeholder sentence twelve adds length. Placeholder sentence thirteen continues. Placeholder sentence fourteen continues further. Placeholder sentence fifteen fills space. Placeholder sentence sixteen fills more space. Placeholder sentence seventeen completes another line. Placeholder sentence eighteen adds the next line. Placeholder sentence nineteen is nearly the last. Placeholder sentence twenty ends this paragraph.

Third line-count test paragraph. Placeholder sentence twenty-one starts it. Placeholder sentence twenty-two follows. Placeholder sentence twenty-three adds words. Placeholder sentence twenty-four adds more words. Placeholder sentence twenty-five continues across the line. Placeholder sentence twenty-six continues again. Placeholder sentence twenty-seven fills the line. Placeholder sentence twenty-eight fills the next. Placeholder sentence twenty-nine is nearly done. Placeholder sentence thirty ends the third paragraph of filler text.

### 1.1.1 Diagnostic heading level 3

Diagnostic paragraph after a level-3 heading (11 pt bold, 9.75 pt before and after). Placeholder sentence thirty-one makes this paragraph two lines long so that the baseline distance after the heading can be measured.

#### 1.1.1.1 Diagnostic heading level 4

Diagnostic paragraph after a level-4 heading (11 pt regular, 9.75 pt before, 0 pt after). The thesis sources contain no level-4 heading; this one exists only to test the style. Placeholder sentence thirty-two extends the paragraph.

## 1.2 Diagnostic heading level 2: tables

Table 1.1 and Table 1.2 both sit in Section 1.2. They test that table numbers are counted within the level-1 section and independently of subsection numbers, as in the results chapter where Section 5.6 holds three separately numbered tables. All digits in these tables are arbitrary test strings, not estimates.

**Table 1.1 — Diagnostic table with wrapping cells (arbitrary test digits, not results).**

| Row label | A column whose header is long enough to wrap inside its cell | Coefficient [95% CI], *p* | N |
|---|---|---|---|
| **Group-row label spanning all columns** |
| Test row a | A deliberately long cell that must wrap across several lines inside its column without entering the right margin of the page. | −1.234 [−5.678, 9.012], .345 | 12,345 |
| Test row b | Short cell. | 0.000 [−0.111, 0.222], <.001 | 6,789 |
| **Second group-row label** |
| Test row c | `docs/provenance/final_empirical_package_v3_2026-10-07/02_core_reporting_table.md` | **9.999 [1.111, 2.222], .043** | N1,940 / G353 |

::: {.tablenote}
Table-note test: 9 pt on an exact 13.5 pt baseline distance. This style is available through a fenced `tablenote` block; the converter never applies it to manuscript text unless a chapter session is explicitly approved to mark a note this way.
:::

**Table 1.2 — Second diagnostic table in the same subsection, with a sub-label line between caption and table.**

**Sub-label line** — kept as an ordinary line between the caption and the table, as above Tables 5.5 to 5.7 in the results chapter

| Outcome | Column 1 | Column 2 | Column 3 | Column 4 |
|---|---|---|---|---|
| Test A | 1.65 [0.34, 2.96], .014 | −0.61 [−2.07, 0.86], .417 | 0.70 [0.15, 1.25], .013 | 1.03 [0.51, 1.54], <.001 |
| Test B | −0.00 [−1.16, 1.16], .997 | −0.16 [−1.29, 0.96], .776 | −0.05 [−0.48, 0.38], .809 | −0.08 [−0.50, 0.35], .717 |

Uncaptioned-table test: a table without a caption line gets no number, and the numbering of captioned tables is unaffected.

| Key | Value |
|---|---|
| Uncaptioned row | Test text |

## 1.3 Diagnostic heading level 2: mathematics and special characters

Display-equation test with the macros the manuscript uses (a generic expression, not a thesis equation):

$$y_{ihc} = a_c + b_1\,\text{Label}_{ih} + b_2\,\bar{C}^{x}_{-h,c} + \sum_{k \neq \text{ref}} \theta_k\,(\text{Label}_{i} \times z_{ik}) + Z_i'\gamma + \varepsilon_{ihc}$$

$$w_i = \text{raw}_i \big/ \sum_{j \in \text{group}(i)} \text{raw}_j, \qquad \forall\, i, \qquad \chi^2 = \frac{a}{b}$$

Inline mathematics: $\beta_W$, $\hat{\beta} \times 10$, $\delta_{s,b_{ic}}$, $\lambda^{S}_{a}$, $E_{ic}(w, p)$.

Special characters in text: en dash 2022–2025; em dash — here; minus sign −0.035; multiplication 2 × 3; approximately ≈ 23; arrow →; section sign §5.6; prime X′; Greek β; diacritics Günther, Blössner, ỹ; quotation marks “double” and ‘single’; percent 95%; ampersand &. Unicode superscripts from the sources (several are missing from Times New Roman and are typeset as superscript digits): 10⁻⁶, 10⁴, 10⁵, 10⁻⁸, x² and x³. Text subscripts: H~2~O and W~IMP~; mathematical subscripts $W_{\text{IMP}}$ and $S_{\text{IMP}}$. Underscores in code: `model_coefficients_PRELIMINARY_AGGREGATE.csv`.

> Block-quotation test: 11 pt on a 15 pt baseline distance, indented. A second sentence makes the quotation wrap onto another line so that its baseline distance can be measured.

Numbered and bulleted list test:

1. **First item.** Placeholder text long enough to wrap onto a second line of the list item for measurement purposes.
2. **Second item.** Placeholder text.

- **C1** — first bulleted placeholder item.
- **C2** — second bulleted placeholder item.

Cross-reference test: the in-text numbers “Section 1.2” and “Table 1.1” are written as plain text, as in the manuscript; the converter checks that LaTeX produced exactly these numbers.

## 1.4 Diagnostic heading level 2: full-page line count

The next page starts with a forced page break and is filled entirely with placeholder text, so that the number of 11 pt lines on a full page can be counted (expected: 35).

\clearpage

Full-page filler sentence 1 has no content beyond its length and is used only to count lines. Full-page filler sentence 2 has no content beyond its length and is used only to count lines. Full-page filler sentence 3 has no content beyond its length and is used only to count lines. Full-page filler sentence 4 has no content beyond its length and is used only to count lines. Full-page filler sentence 5 has no content beyond its length and is used only to count lines. Full-page filler sentence 6 has no content beyond its length and is used only to count lines. Full-page filler sentence 7 has no content beyond its length and is used only to count lines. Full-page filler sentence 8 has no content beyond its length and is used only to count lines. Full-page filler sentence 9 has no content beyond its length and is used only to count lines. Full-page filler sentence 10 has no content beyond its length and is used only to count lines. Full-page filler sentence 11 has no content beyond its length and is used only to count lines. Full-page filler sentence 12 has no content beyond its length and is used only to count lines. Full-page filler sentence 13 has no content beyond its length and is used only to count lines. Full-page filler sentence 14 has no content beyond its length and is used only to count lines. Full-page filler sentence 15 has no content beyond its length and is used only to count lines. Full-page filler sentence 16 has no content beyond its length and is used only to count lines. Full-page filler sentence 17 has no content beyond its length and is used only to count lines. Full-page filler sentence 18 has no content beyond its length and is used only to count lines. Full-page filler sentence 19 has no content beyond its length and is used only to count lines. Full-page filler sentence 20 has no content beyond its length and is used only to count lines. Full-page filler sentence 21 has no content beyond its length and is used only to count lines. Full-page filler sentence 22 has no content beyond its length and is used only to count lines. Full-page filler sentence 23 has no content beyond its length and is used only to count lines. Full-page filler sentence 24 has no content beyond its length and is used only to count lines. Full-page filler sentence 25 has no content beyond its length and is used only to count lines. Full-page filler sentence 26 has no content beyond its length and is used only to count lines. Full-page filler sentence 27 has no content beyond its length and is used only to count lines. Full-page filler sentence 28 has no content beyond its length and is used only to count lines. Full-page filler sentence 29 has no content beyond its length and is used only to count lines. Full-page filler sentence 30 has no content beyond its length and is used only to count lines. Full-page filler sentence 31 has no content beyond its length and is used only to count lines. Full-page filler sentence 32 has no content beyond its length and is used only to count lines. Full-page filler sentence 33 has no content beyond its length and is used only to count lines. Full-page filler sentence 34 has no content beyond its length and is used only to count lines. Full-page filler sentence 35 has no content beyond its length and is used only to count lines. Full-page filler sentence 36 has no content beyond its length and is used only to count lines. Full-page filler sentence 37 has no content beyond its length and is used only to count lines. Full-page filler sentence 38 has no content beyond its length and is used only to count lines. Full-page filler sentence 39 has no content beyond its length and is used only to count lines. Full-page filler sentence 40 has no content beyond its length and is used only to count lines. Full-page filler sentence 41 has no content beyond its length and is used only to count lines. Full-page filler sentence 42 has no content beyond its length and is used only to count lines. Full-page filler sentence 43 has no content beyond its length and is used only to count lines. Full-page filler sentence 44 has no content beyond its length and is used only to count lines. Full-page filler sentence 45 has no content beyond its length and is used only to count lines. Full-page filler sentence 46 has no content beyond its length and is used only to count lines. Full-page filler sentence 47 has no content beyond its length and is used only to count lines. Full-page filler sentence 48 has no content beyond its length and is used only to count lines. Full-page filler sentence 49 has no content beyond its length and is used only to count lines. Full-page filler sentence 50 has no content beyond its length and is used only to count lines. Full-page filler sentence 51 has no content beyond its length and is used only to count lines. Full-page filler sentence 52 has no content beyond its length and is used only to count lines. Full-page filler sentence 53 has no content beyond its length and is used only to count lines. Full-page filler sentence 54 has no content beyond its length and is used only to count lines. Full-page filler sentence 55 has no content beyond its length and is used only to count lines. Full-page filler sentence 56 has no content beyond its length and is used only to count lines. Full-page filler sentence 57 has no content beyond its length and is used only to count lines. Full-page filler sentence 58 has no content beyond its length and is used only to count lines. Full-page filler sentence 59 has no content beyond its length and is used only to count lines. Full-page filler sentence 60 has no content beyond its length and is used only to count lines.
