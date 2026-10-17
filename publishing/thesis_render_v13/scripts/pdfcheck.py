"""pdfcheck.py -- measured layout checks on a built PDF (PyMuPDF).

Measures what can be measured from the PDF itself: page size, text-block
extents against the specified margins, embedded fonts, font sizes, baseline
distances per font size, lines per full page, heading spacing, raw
citation tokens and replacement characters. Renders every page to PNG for
visual inspection. A clean result here is NOT a substitute for looking at
the rendered pages.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

PT_PER_CM = 72 / 2.54
A4 = (595.28, 841.89)
MARGIN_CM = {"left": 2.5, "right": 4.0, "top": 2.8, "bottom": 2.8}
BOX = (
    MARGIN_CM["left"] * PT_PER_CM,
    MARGIN_CM["top"] * PT_PER_CM,
    A4[0] - MARGIN_CM["right"] * PT_PER_CM,
    A4[1] - MARGIN_CM["bottom"] * PT_PER_CM,
)
TOL = 1.0  # pt
EXPECTED_PITCH = {11.0: 19.5, 10.0: 15.0, 9.0: 13.5}
RAW_CITE = re.compile(r"\[@|\[-@|(?<![\w.])@[A-Z][A-Za-z]+\d{4}")


def _lines(page):
    """Yield (baseline_y, x0, x1, size, font, text, bbox) for horizontal lines."""
    d = page.get_text("dict")
    for b in d["blocks"]:
        for ln in b.get("lines", []):
            if ln.get("dir", (1, 0)) != (1, 0) or not ln["spans"]:
                continue
            spans = [s for s in ln["spans"] if s["text"].strip()]
            if not spans:
                continue
            # dominant span by character count
            dom = max(spans, key=lambda s: len(s["text"]))
            text = "".join(s["text"] for s in ln["spans"])
            x0 = min(s["bbox"][0] for s in spans)
            x1 = max(s["bbox"][2] for s in spans)
            y0 = min(s["bbox"][1] for s in spans)
            y1 = max(s["bbox"][3] for s in spans)
            # size bucketed to 0.5pt (headings 14/12, text 11, tables 10, notes 9)
            yield (round(dom["origin"][1], 2), x0, x1, round(dom["size"] * 2) / 2,
                   dom["font"], text, (x0, y0, x1, y1), spans)


def inspect(pdf: Path, png_dir: Path | None = None, dpi: int = 110,
            heading_patterns: list[str] | None = None) -> dict:
    import pymupdf

    doc = pymupdf.open(pdf)
    res: dict = {"pdf": str(pdf), "pages": doc.page_count, "issues": []}
    sizes = Counter()
    fonts = set()
    pitch = defaultdict(Counter)
    lines_per_page = {}
    extents = {"min_x0": 1e9, "max_x1": 0, "min_y0": 1e9, "max_y1": 0}
    heading_gaps = []

    for pno in range(doc.page_count):
        page = doc[pno]
        w, h = page.rect.width, page.rect.height
        if abs(w - A4[0]) > 0.5 or abs(h - A4[1]) > 0.5:
            res["issues"].append(f"page {pno+1}: size {w:.2f}x{h:.2f}pt is not A4")
        for f in page.get_fonts(full=True):
            fonts.add(f[3])
        text = page.get_text()
        if RAW_CITE.search(text):
            res["issues"].append(f"page {pno+1}: raw citation token: "
                                 f"{RAW_CITE.search(text).group(0)!r}")
        if "�" in text:
            res["issues"].append(f"page {pno+1}: replacement character (missing glyph)")

        body = []
        for ln in _lines(page):
            base, x0, x1, size, font, t, bbox, spans = ln
            in_header = bbox[3] < BOX[1] - 2 and size <= 8.5
            in_footer = bbox[1] > BOX[3] + 2 and t.strip().isalnum()
            if in_header or in_footer:
                continue
            body.append(ln)
            for s in spans:
                sizes[(round(s["size"], 1), s["font"])] += len(s["text"].strip())
            extents["min_x0"] = min(extents["min_x0"], x0)
            extents["max_x1"] = max(extents["max_x1"], x1)
            extents["min_y0"] = min(extents["min_y0"], bbox[1])
            extents["max_y1"] = max(extents["max_y1"], bbox[3])
            if x1 > BOX[2] + TOL:
                res["issues"].append(f"page {pno+1}: text extends {x1 - BOX[2]:.1f}pt into the "
                                     f"right margin: {t[:60]!r}")
            if x0 < BOX[0] - TOL:
                res["issues"].append(f"page {pno+1}: text starts {BOX[0] - x0:.1f}pt into the "
                                     f"left margin: {t[:60]!r}")
            if bbox[3] > BOX[3] + 3 or bbox[1] < BOX[1] - 3:
                res["issues"].append(f"page {pno+1}: text outside top/bottom margin: {t[:60]!r}")

        # baseline pitch between consecutive lines of the same size
        body.sort(key=lambda l: (l[0], l[1]))
        merged = []
        for ln in body:  # merge pieces sharing a baseline (table cells, heading number + title)
            if merged and abs(merged[-1][0] - ln[0]) < 0.6:
                prev = merged[-1]
                big = prev if prev[3] >= ln[3] else ln
                merged[-1] = (prev[0], prev[1], max(prev[2], ln[2]), big[3], big[4],
                              prev[5] + " " + ln[5], prev[6], prev[7] + ln[7])
                continue
            merged.append(ln)
        for a, b in zip(merged, merged[1:]):
            if a[3] == b[3]:
                pitch[a[3]][round(b[0] - a[0], 2)] += 1
        lines_per_page[pno + 1] = sum(1 for l in merged if l[3] == 11.0)

        for pat in heading_patterns or []:
            for k, ln in enumerate(merged):
                if re.search(pat, ln[5]):
                    prev_gap = round(ln[0] - merged[k - 1][0], 2) if k > 0 else None
                    next_gap = round(merged[k + 1][0] - ln[0], 2) if k + 1 < len(merged) else None
                    heading_gaps.append({"page": pno + 1, "pattern": pat, "text": ln[5][:50],
                                         "size": ln[3], "font": ln[4],
                                         "gap_from_previous_baseline": prev_gap,
                                         "gap_to_next_baseline": next_gap})

        if png_dir is not None:
            png_dir.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(dpi=dpi).save(png_dir / f"page-{pno+1:03d}.png")

    res["page_size_pt"] = [round(doc[0].rect.width, 2), round(doc[0].rect.height, 2)]
    res["fonts_embedded"] = sorted(fonts)
    res["text_block_allowed_pt"] = [round(v, 2) for v in BOX]
    res["text_extents_pt"] = {k: round(v, 2) for k, v in extents.items()}
    res["measured_margins_cm"] = {
        "left": round(extents["min_x0"] / PT_PER_CM, 3),
        "right_min": round((A4[0] - extents["max_x1"]) / PT_PER_CM, 3),
    }
    res["chars_by_size_font"] = {f"{s}pt {f}": n for (s, f), n in sizes.most_common()}
    res["baseline_pitch_by_size"] = {
        str(s): dict(c.most_common(6)) for s, c in sorted(pitch.items())}
    for s, want in EXPECTED_PITCH.items():
        c = pitch.get(s)
        if c:
            mode = c.most_common(1)[0][0]
            if abs(mode - want) > 0.05:
                res["issues"].append(f"{s}pt text: most common baseline pitch {mode}pt, "
                                     f"expected {want}pt")
    res["lines_11pt_per_page"] = lines_per_page
    res["max_11pt_lines_on_a_page"] = max(lines_per_page.values()) if lines_per_page else 0
    res["heading_gaps"] = heading_gaps
    return res


def to_markdown(r: dict) -> str:
    out = [f"- PDF pages: {r['pages']}; page size {r['page_size_pt'][0]} × {r['page_size_pt'][1]} pt "
           f"(A4 = 595.28 × 841.89 pt)",
           f"- Embedded fonts: {', '.join(r['fonts_embedded'])}",
           f"- Allowed text block (pt, x0 y0 x1 y1): {r['text_block_allowed_pt']}; "
           f"measured text extents: {r['text_extents_pt']}",
           f"- Measured left margin {r['measured_margins_cm']['left']} cm (spec 2.5); "
           f"smallest right margin {r['measured_margins_cm']['right_min']} cm (spec ≥ 4.0)",
           f"- Most 11pt text lines on one page: {r['max_11pt_lines_on_a_page']}",
           "- Baseline pitch by font size (pt → count): "
           + "; ".join(f"{s}pt: {d}" for s, d in r["baseline_pitch_by_size"].items()),
           "- Characters by size/font: "
           + "; ".join(f"{k}: {v}" for k, v in list(r["chars_by_size_font"].items())[:14])]
    if r["heading_gaps"]:
        out.append("- Heading baseline gaps (pt):")
        for g in r["heading_gaps"]:
            out.append(f"  - p.{g['page']} {g['size']}pt {g['font']} “{g['text']}”: "
                       f"from previous baseline {g['gap_from_previous_baseline']}, "
                       f"to next baseline {g['gap_to_next_baseline']}")
    out.append(f"- Automated issues found: {len(r['issues'])}")
    out += [f"  - {i}" for i in r["issues"]]
    return "\n".join(out)


if __name__ == "__main__":
    import sys
    r = inspect(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    print(json.dumps(r, indent=1, ensure_ascii=False))
