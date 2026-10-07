#!/usr/bin/env python3
"""
md2tex.py — purpose-built Markdown -> LaTeX converter for this manuscript only.
Not a general Markdown parser. Handles exactly the constructs used in
manuscript/v3_2026-10-07/*.md and appendices/*.md: headers (#/##/###),
bold/italic, inline code, pipe tables, inline and display math ($...$, $$...$$),
and pandoc citation syntax ([@key], [@key1; @key2], [@key, locator], "Author [-@key]").
Used because pandoc is not installed in this environment; this script plus
direct xelatex+biblatex is the fallback build path (see MASTER_ASSEMBLY.md).
"""
import re
import sys

MATH_PLACEHOLDER = "@@MATH{}@@"
CODE_PLACEHOLDER = "@@CODE{}@@"


def protect(text, pattern, store, tag):
    out = []
    last = 0
    for m in re.finditer(pattern, text, flags=re.DOTALL):
        out.append(text[last:m.start()])
        idx = len(store)
        store.append(m.group(0))
        out.append(f"\x00{tag}{idx}\x00")
        last = m.end()
    out.append(text[last:])
    return "".join(out)


def restore(text, store, tag, renderer):
    def sub(m):
        idx = int(m.group(1))
        return renderer(store[idx])
    return re.sub(rf"\x00{tag}(\d+)\x00", sub, text)


def latex_escape(s):
    # Escape LaTeX special characters in plain prose (math/code already protected).
    # A literal backslash-underscore in the source (e.g. "FULL\_DUMMY\_DF",
    # written by hand to stop Markdown parsing the underscore as italics)
    # already means exactly the correct final LaTeX escape "\_" -- protect
    # it first so the backslash isn't re-escaped into a visible, unbreakable
    # \textbackslash{} token (a real rendering defect this converter
    # previously produced throughout the manuscript, e.g. "FULL\_DUMMY\_DF"
    # rendering as "FULL\textbackslash{}\_DUMMY...").
    s = re.sub(r"\\_", "\x00ESCUNDER\x00", s)
    s = s.replace("\\", r"\textbackslash{}")
    for ch, esc in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"),
                    ("$", r"\$"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(ch, esc)
    s = s.replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}")
    s = s.replace("\x00ESCUNDER\x00", r"\_")
    return s


def convert_citations(s):
    # [-@key] narrative suppress-author, author already typed: "Author [-@key]" -> "Author (\citeyear{key})"
    s = re.sub(r"\[-@([A-Za-z0-9]+)\]", r"(\\citeyear{\1})", s)
    # [@key, locator] single key with a locator
    s = re.sub(r"\[@([A-Za-z0-9]+),\s*([^\]]+)\]", r"\\parencite[\2]{\1}", s)
    # [@key1; @key2; ...] group, no locator
    def group_sub(m):
        keys = re.findall(r"@([A-Za-z0-9]+)", m.group(0))
        return r"\parencite{" + ",".join(keys) + "}"
    s = re.sub(r"\[@[A-Za-z0-9]+(?:;\s*@[A-Za-z0-9]+)+\]", group_sub, s)
    # [@key] single, no locator
    s = re.sub(r"\[@([A-Za-z0-9]+)\]", r"\\parencite{\1}", s)
    return s


def inline_format(s):
    # Math and inline-code already replaced with NUL-index placeholders by caller.
    s = convert_citations(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s)
    s = re.sub(r"(?<![\w\\])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\\textit{\1}", s)
    s = s.replace("—", "---").replace("–", "--")
    return s


def process_inline(raw):
    code_store, math_store = [], []
    t = protect(raw, r"`[^`]+`", code_store, "C")
    t = protect(t, r"\$\$.+?\$\$|\$[^$\n]+\$", math_store, "M")
    # Escape plain prose (outside math/code placeholders) for LaTeX specials,
    # but do this BEFORE inline_format so **/*/citation syntax still parses,
    # then restore code/math untouched.
    parts = re.split(r"(\x00[CM]\d+\x00)", t)
    esc_parts = []
    for p in parts:
        if re.fullmatch(r"\x00[CM]\d+\x00", p):
            esc_parts.append(p)
        else:
            esc_parts.append(latex_escape(p))
    t = "".join(esc_parts)
    t = inline_format(t)
    def render_code(c):
        inner = latex_escape(c.strip("`"))
        # Allow line-breaking at path/identifier separators (/, escaped _,
        # ., and -) so a long inline path, module path, call expression, or
        # timestamped filename wraps across lines instead of overflowing the
        # text width -- a zero-width break point, harmless on short spans
        # since LaTeX only uses it if the line actually needs it.
        inner = re.sub(r"(/|\\_|\.|-)", r"\1\\allowbreak{}", inner)
        return r"\texttt{" + inner + "}"
    t = restore(t, code_store, "C", render_code)
    t = restore(t, math_store, "M", lambda m: m)  # math passes through verbatim
    return t


def strip_markup_for_width(s):
    # Rough content-length estimate for column-width allocation: strip
    # Markdown emphasis/code markers so they don't inflate the estimate.
    return re.sub(r"[`*]", "", s)


def column_widths_cm(header, rows, ncol, total_width_cm, min_col_cm=1.6):
    """Allocate each column a wrapping width proportional to its longest
    cell's content length, so wide cells wrap instead of overflowing the
    page, and no column is squeezed below a readable minimum. This is an
    estimate (exact wrapping is then done by LaTeX itself at that width),
    not an exact character-metric computation."""
    col_lens = []
    for ci in range(ncol):
        lens = [len(strip_markup_for_width(header[ci]))]
        for r in rows:
            if ci < len(r):
                lens.append(len(strip_markup_for_width(r[ci])))
        col_lens.append(max(lens) if lens else 1)
    raw_total = sum(col_lens) or ncol
    widths = [max(min_col_cm, total_width_cm * l / raw_total) for l in col_lens]
    scale = total_width_cm / sum(widths)
    return [w * scale for w in widths]


def convert_table(lines):
    header = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    body_lines = lines[2:]
    ncol = len(header)
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in body_lines]
    rows_full = [r for r in rows if len(r) == ncol]

    # Text width is 14.5cm (A4 minus the 2.5cm/4.0cm left/right margins);
    # reserve space for \tabcolsep padding (reduced below) on each column.
    total_width_cm = 14.5 - 0.22 * ncol
    widths = column_widths_cm(header, rows_full, ncol, total_width_cm)
    colspec = "".join(
        f">{{\\raggedright\\arraybackslash}}p{{{w:.2f}cm}}" for w in widths
    )

    out = ["\\begingroup\\fontsize{10}{15}\\selectfont\\setlength{\\tabcolsep}{3pt}",
           f"\\begin{{longtable}}{{{colspec}}}", "\\toprule"]
    out.append(" & ".join(process_inline(h) for h in header) + " \\\\")
    out.append("\\midrule")
    out.append("\\endhead")
    for cells in rows:
        if len(cells) == ncol:
            out.append(" & ".join(process_inline(c) for c in cells) + " \\\\")
        elif len(cells) == 1 and cells[0]:
            # A short row (one cell) is an in-table section label spanning all columns.
            out.append(f"\\multicolumn{{{ncol}}}{{l}}{{{process_inline(cells[0])}}} \\\\")
        # else: malformed row (e.g. stray blank), skip
    out.append("\\bottomrule")
    out.append("\\end{longtable}")
    out.append("\\endgroup")
    return out


def convert_file(path):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("### "):
            title = process_inline(line[4:])
            out.append(f"\\subsubsection*{{{title}}}")
            out.append(f"\\addcontentsline{{toc}}{{subsubsection}}{{{title}}}")
        elif line.startswith("## "):
            title = process_inline(line[3:])
            out.append(f"\\subsection*{{{title}}}")
            out.append(f"\\addcontentsline{{toc}}{{subsection}}{{{title}}}")
        elif line.startswith("# "):
            title = process_inline(line[2:])
            out.append(f"\\section*{{{title}}}")
            out.append(f"\\addcontentsline{{toc}}{{section}}{{{title}}}")
        elif line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            j = i
            tbl = []
            while j < len(lines) and lines[j].strip().startswith("|"):
                tbl.append(lines[j])
                j += 1
            out.extend(convert_table(tbl))
            i = j
            continue
        elif line.strip() == "":
            out.append("")
        else:
            out.append(process_inline(line))
        i += 1
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for src in sys.argv[1:]:
        dst = src.rsplit(".", 1)[0] + ".tex"
        with open(dst, "w", encoding="utf-8") as f:
            f.write(convert_file(src))
        print("wrote", dst)
