#!/usr/bin/env python3
"""build.py -- the single build entry point of the thesis rendering package.

    python scripts/build.py env                  tool / font check
    python scripts/build.py lint [UNIT ...]      source checks, no PDF
    python scripts/build.py prepare UNIT         copy canonical .md into chapters/md/
    python scripts/build.py convert UNIT         chapters/md/*.md -> chapters/tex/*.tex
    python scripts/build.py preview UNIT         convert + REVIEW-COPY PDF + report
    python scripts/build.py diagnostic           TEMPLATE-VERIFICATION PDF + report
    python scripts/build.py selftest             preview pipeline run on diagnostic text
    python scripts/build.py thesis [--final]     full assembly from chapters/tex/
    python scripts/build.py references           REVIEW-COPY of the consolidated reference list only
    python scripts/build.py inspect PDF          layout checks + page images
    python scripts/build.py manifest             check canonical inputs against source_manifest.tsv

UNIT: abstract, ch01 ... ch07, appA, appB, appC (also accepted: 1-7, A-C).
Run from anywhere; paths are resolved from this file. Cross-platform
(Windows/macOS/Linux): needs Python 3.9+, pandoc >= 3.1, xelatex, biber;
PyMuPDF (pip install pymupdf) for `inspect`; fontTools optional for `lint`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]           # publishing/thesis_render_v13
REPO = PKG.parents[1]
CANON = REPO / "manuscript" / "v13_2026-10-17"       # canonical academic source
CANON_BIB = CANON / "bibliography.bib"               # canonical bibliography (frozen; manifest)
# The ONE bibliography every build reads: the publishing copy of the canonical file, with the
# verified field changes of the consolidated-references session (bibliography/field_changes.tsv).
BIB = PKG / "bibliography" / "bibliography.bib"
TEMPLATE = PKG / "template"
FILTER = PKG / "filters" / "thesis.lua"
MD_DIR = PKG / "chapters" / "md"
TEX_DIR = PKG / "chapters" / "tex"
BUILDS = PKG / "builds"
APPROVALS = PKG / "chapters" / "APPROVED.tsv"
MANIFEST = PKG / "source_manifest.tsv"

UNITS = [
    # id, canonical source (relative to CANON), kind, number, short name
    ("abstract", "08_abstract.md", "abstract", None, "abstract"),
    ("ch01", "01_introduction.md", "chapter", 1, "introduction"),
    ("ch02", "02_literature_review.md", "chapter", 2, "literature-review"),
    ("ch03", "03_data_and_variables.md", "chapter", 3, "data-and-variables"),
    ("ch04", "04_empirical_strategy.md", "chapter", 4, "empirical-strategy"),
    ("ch05", "05_results.md", "chapter", 5, "results"),
    ("ch06", "06_discussion_and_limitations.md", "chapter", 6, "discussion-and-limitations"),
    ("ch07", "07_conclusion.md", "chapter", 7, "conclusion"),
    ("appA", "appendices/A_variable_definitions_and_sample_flow.md", "appendix", "A", "appendix-A"),
    ("appB", "appendices/B_model_specifications_and_independent_verification.md", "appendix", "B", "appendix-B"),
    ("appC", "appendices/C_historical_diagnostics_and_ethiopia.md", "appendix", "C", "appendix-C"),
]
UNIT = {u[0]: u for u in UNITS}
ALIAS = {**{str(i): f"ch0{i}" for i in range(1, 8)}, **{f"0{i}": f"ch0{i}" for i in range(1, 8)},
         "A": "appA", "B": "appB", "C": "appC", "a": "appA", "b": "appB", "c": "appC"}


# ---------------------------------------------------------------- helpers
def die(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def unit(uid: str):
    uid = ALIAS.get(uid, uid)
    if uid not in UNIT:
        die(f"unknown unit {uid!r}; use one of: {', '.join(UNIT)}")
    return UNIT[uid]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(cmd, cwd=None, check=True) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode != 0:
        print(r.stdout[-4000:], r.stderr[-4000:], sep="\n", file=sys.stderr)
        die(f"command failed ({r.returncode}): {' '.join(map(str, cmd))}")
    return r


def git(*args) -> str:
    r = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else "unavailable"


def git_state() -> dict:
    dirty = git("status", "--porcelain", "--", str(CANON.relative_to(REPO)),
                str(PKG.relative_to(REPO) / "template"), str(PKG.relative_to(REPO) / "filters"),
                str(PKG.relative_to(REPO) / "scripts"), str(PKG.relative_to(REPO) / "drivers"),
                str(PKG.relative_to(REPO) / "chapters"), str(PKG.relative_to(REPO) / "diagnostics"))
    return {"remote": git("remote", "get-url", "origin"), "branch": git("branch", "--show-current"),
            "commit": git("rev-parse", "HEAD"), "uncommitted_changes_in_inputs": dirty or "none"}


def first_line(cmd) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).strip().splitlines()[0]
    except (OSError, IndexError):
        return "NOT AVAILABLE"


def tool_versions() -> dict:
    v = {"python": sys.version.split()[0],
         "pandoc": first_line(["pandoc", "--version"]),
         "xelatex": first_line(["xelatex", "--version"]),
         "biber": first_line(["biber", "--version"])}
    try:
        import pymupdf
        v["pymupdf"] = pymupdf.VersionBind
    except ImportError:
        v["pymupdf"] = "NOT AVAILABLE"
    return v


def find_tnr() -> Path | None:
    cands = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / "times.ttf",
             Path("/usr/local/share/fonts/msttcore/Times.TTF"),
             Path("/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf"),
             Path("/Library/Fonts/Times New Roman.ttf"),
             Path("/System/Library/Fonts/Supplemental/Times New Roman.ttf")]
    if shutil.which("fc-match"):
        r = subprocess.run(["fc-match", "-f", "%{file}", "Times New Roman:style=Regular"],
                           capture_output=True, text=True)
        if r.returncode == 0 and "times" in r.stdout.lower():
            cands.insert(0, Path(r.stdout))
    return next((c for c in cands if c.exists()), None)


def font_info(path: Path | None) -> str:
    if not path:
        return "Times New Roman NOT FOUND"
    try:
        from fontTools.ttLib import TTFont
        f = TTFont(path)
        ver = f["name"].getDebugName(5)
        return f"{f['name'].getDebugName(4)} ({ver}) at {path}, sha256 {sha256(path)[:16]}"
    except Exception:  # fontTools missing
        return f"Times New Roman at {path}"


def tex_path(p: Path, start: Path) -> str:
    return Path(os.path.relpath(p, start)).as_posix()


def escape_label(s: str) -> str:
    return re.sub(r"([#$%&_{}])", r"\\\1", s)


def md_copy(u) -> Path:
    return MD_DIR / Path(u[1]).name


def tex_out(u) -> Path:
    return TEX_DIR / (Path(u[1]).stem + ".tex")


# ------------------------------------------------------------------- lint
CITE_KEY = re.compile(r"@([A-Za-z][A-Za-z0-9]+)")
REF_SECTION = re.compile(r"(?:Sections?|§)\s*((?:\d+|[A-C])(?:\.\d+)*)")
REF_TABLE = re.compile(r"Tables?\s+(\d+\.\d+|[A-C]\.\d+)")


def lint(units: list, source: str = "canonical") -> int:
    bib = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@\w+\{([^,\s]+),", bib))
    problems, used = [], set()
    sections, tables = set(), set()
    texts = {}
    for u in UNITS:   # targets are collected from ALL units so cross-chapter refs resolve
        src = CANON / u[1] if source == "canonical" else md_copy(u)
        if not src.exists():
            src = CANON / u[1]
        t = src.read_text(encoding="utf-8")
        texts[u[0]] = (src, t)
        for m in re.finditer(r"^#{1,4} (?:Appendix )?((?:\d+|[A-C])(?:\.\d+)*)\.? ", t, re.M):
            sections.add(m.group(1))
        tables.update(re.findall(r"^\*\*Table (\S+) [—–]", t, re.M))
    tnr = find_tnr()
    cmap = None
    if tnr:
        try:
            from fontTools.ttLib import TTFont
            cmap = set(TTFont(tnr).getBestCmap())
        except Exception:
            pass
    sup = set("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
    for u in units:
        src, t = texts[u[0]]
        rel = src.relative_to(REPO).as_posix()
        # citations
        for k in set(CITE_KEY.findall(" ".join(re.findall(r"\[[^\]]*@[^\]]*\]", t)))):
            used.add(k)
            if k not in bib_keys:
                problems.append(f"{rel}: citation key @{k} not in bibliography.bib")
        if re.search(r"@[A-Z][A-Za-z]+\d{4}", re.sub(r"\[[^\]]*@[^\]]*\]", "", t)):
            problems.append(f"{rel}: bare @Key citation outside brackets")
        # heading numbers
        nums = re.findall(r"^(#{1,4}) (.*)$", t, re.M)
        expect = u[3]
        for hashes, title in nums:
            lvl = len(hashes)
            if lvl == 1 and title == "Abstract":
                continue
            m = re.match(r"(?:Appendix )?((?:\d+|[A-C])(?:\.\d+)*)\.?\s", title)
            if not m:
                problems.append(f"{rel}: heading without number: {title[:60]!r}")
                continue
            if not m.group(1).startswith(str(expect)):
                problems.append(f"{rel}: heading {m.group(1)} does not belong to unit {expect}")
            if m.group(1).count(".") + 1 != lvl:
                problems.append(f"{rel}: heading {m.group(1)} written at level {lvl}")
            if lvl == 4:
                problems.append(f"{rel}: level-4 heading present (guidelines: avoid): {title[:50]!r}")
        # table caption sequence
        caps = re.findall(r"^\*\*Table (\S+) [—–]", t, re.M)
        if caps and expect is not None:
            want = [f"{expect}.{i}" for i in range(1, len(caps) + 1)]
            if caps != want:
                problems.append(f"{rel}: caption sequence {caps} != {want}")
        n_tables = len(re.findall(r"^\|[-:| ]+\|\s*$", t, re.M))
        if caps and n_tables != len(caps):
            problems.append(f"{rel}: {n_tables} tables but {len(caps)} captions (mixed captioning)")
        # cross references
        for ref in REF_SECTION.findall(t):
            if ref not in sections:
                problems.append(f"{rel}: reference to Section {ref} has no matching heading")
        for ref in REF_TABLE.findall(t):
            if ref not in tables:
                problems.append(f"{rel}: reference to Table {ref} has no matching caption")
        # glyphs
        if cmap is not None:
            missing = sorted({c for c in t if ord(c) > 127 and ord(c) not in cmap and c not in sup})
            if missing:
                problems.append(f"{rel}: characters missing from Times New Roman: "
                                + " ".join(f"U+{ord(c):04X}" for c in missing))
        # converter dry run (LaTeX text only, discarded; no PDF)
        r = run(["pandoc", "-f", "markdown", "-t", "latex", "--biblatex", "--wrap=none",
                 f"--lua-filter={FILTER}", str(src)], check=False)
        if r.returncode != 0:
            problems.append(f"{rel}: converter error: {r.stderr.strip()[:300]}")
        elif re.search(r"\[@|\[-@", r.stdout):
            problems.append(f"{rel}: unconverted citation syntax remains after conversion")
        n_cap = r.stdout.count("\\ThesisTableCaption{")
        n_lt = r.stdout.count("\\begin{longtable}")
        n_cite = len(re.findall(r"\\autocites?\*?[\[{]", r.stdout))
        print(f"  {u[0]:9s} {rel}: {len(nums)} headings, {len(caps)} captions, {n_tables} tables; "
              f"converter: {n_cap} captions, {n_lt} longtables, {n_cite} cite commands")
    print(f"  cited keys in checked units: {len(used)}; bibliography entries: {len(bib_keys)}")
    for p in problems:
        print("  PROBLEM:", p)
    print(f"lint: {len(problems)} problem(s)")
    return len(problems)


# ----------------------------------------------------------- conversion
def prepare(u) -> None:
    src, dst = CANON / u[1], md_copy(u)
    if dst.exists():
        same = sha256(dst) == sha256(src)
        die(f"{dst.relative_to(PKG)} already exists ({'identical to' if same else 'DIFFERS from'} "
            f"canonical). It is never overwritten; inspect it, or delete it deliberately first.")
    MD_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    log = MD_DIR / "PROVENANCE.tsv"
    if not log.exists():
        log.write_text("unit\tfile\tcanonical_sha256\tsource_commit\tprepared_utc\n", encoding="utf-8")
    with log.open("a", encoding="utf-8") as f:
        # source_commit = last commit that changed the canonical manuscript (the academic
        # source), not HEAD, which may be a later publishing-only commit.
        f.write(f"{u[0]}\t{dst.name}\t{sha256(src)}\t"
                f"{git('log', '-1', '--format=%H', '--', CANON.relative_to(REPO).as_posix())}\t"
                f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%dT%H:%M:%SZ}\n")
    print(f"prepared {dst.relative_to(PKG)} (byte-identical copy of {src.relative_to(REPO)})")


def convert_md(src: Path, dst: Path, provenance: str) -> None:
    r = run(["pandoc", "-f", "markdown", "-t", "latex", "--biblatex", "--wrap=preserve",
             f"--lua-filter={FILTER}", str(src)])
    # Captions are emitted by \ThesisTableCaption outside the table, so every
    # table is a caption-less longtable*, which (unlike longtable) does not
    # advance the table counter.
    # pandoc emits \def\LTcaptype{none} for every such table, on the
    # assumption that an uncaptioned longtable* never references \LTcaptype
    # at all. A newer LaTeX kernel's PDF-tagging hooks inside \endlongtable
    # call \refstepcounter regardless of that assumption, and ltcaption
    # redirects it through \LTcaptype -- which then fails with "No counter
    # 'none' defined". Redirecting to a dedicated, always-defined, never-read
    # dummy counter (template/thesis-preamble.tex) keeps that redirection
    # harmless instead of fatal, without touching the real \c@table counter
    # \ThesisTableCaption's own \captionof{table} call legitimately steps.
    tex = r.stdout.replace("\\begin{longtable}", "\\begin{longtable*}") \
                  .replace("\\end{longtable}", "\\end{longtable*}") \
                  .replace("\\def\\LTcaptype{none}", "\\def\\LTcaptype{ThesisDummyLTCaptype}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(provenance + tex, encoding="utf-8")


def convert(u) -> Path:
    src = md_copy(u)
    if not src.exists():
        die(f"{src.relative_to(PKG)} missing: run `build.py prepare {u[0]}` first")
    canon = CANON / u[1]
    head = (f"% GENERATED by scripts/build.py convert {u[0]} -- do not hand-edit; edit\n"
            f"% chapters/md/{src.name} and regenerate.\n"
            f"% md sha256 {sha256(src)}\n"
            f"% canonical {canon.relative_to(REPO).as_posix()} sha256 {sha256(canon)}\n"
            f"% md identical to canonical: {sha256(src) == sha256(canon)}\n"
            f"% filter sha256 {sha256(FILTER)}\n\n")
    dst = tex_out(u)
    convert_md(src, dst, head)
    print(f"converted {src.relative_to(PKG)} -> {dst.relative_to(PKG)}")
    return dst


# ---------------------------------------------------------------- compile
def compile_tex(work: Path, job: str) -> dict:
    logs = {}
    steps = [["xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{job}.tex"],
             ["biber", job],
             ["xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{job}.tex"],
             ["xelatex", "-interaction=nonstopmode", "-halt-on-error", f"{job}.tex"]]
    for i, cmd in enumerate(steps, 1):
        r = run(cmd, cwd=work, check=False)
        (work / f"step{i}_{cmd[0]}.out").write_text(r.stdout + r.stderr, encoding="utf-8")
        if r.returncode != 0:
            tail = (work / f"{job}.log").read_text(errors="replace")[-3000:] \
                if (work / f"{job}.log").exists() else r.stdout[-3000:]
            print(tail, file=sys.stderr)
            die(f"{cmd[0]} failed at step {i}; see {work / (job + '.log')}")
    log = (work / f"{job}.log").read_text(encoding="utf-8", errors="replace")
    blg = (work / f"{job}.blg").read_text(encoding="utf-8", errors="replace") \
        if (work / f"{job}.blg").exists() else ""
    bbl = (work / f"{job}.bbl").read_text(encoding="utf-8", errors="replace") \
        if (work / f"{job}.bbl").exists() else ""
    logs["errors"] = len(re.findall(r"^! ", log, re.M))
    logs["missing_characters"] = re.findall(r"Missing character: There is no .*", log)
    logs["overfull_hbox"] = len(re.findall(r"^Overfull \\hbox", log, re.M))
    logs["overfull_vbox"] = len(re.findall(r"^Overfull \\vbox", log, re.M))
    logs["underfull_hbox"] = len(re.findall(r"^Underfull \\hbox", log, re.M))
    logs["undefined_citations"] = sorted(set(re.findall(r"Citation '([^']+)'.*undefined", log)))
    logs["undefined_references"] = sorted(set(re.findall(r"Reference `([^']+)' .*undefined", log)))
    logs["rerun_needed"] = "Label(s) may have changed" in log or "Please rerun" in log
    logs["font_warnings"] = sorted(set(re.findall(r"(Font shape .* undefined.*|"
                                                   r"Package fontspec Warning: .*)", log)))[:10]
    logs["biber_warnings"] = re.findall(r"WARN - .*", blg)
    logs["biber_errors"] = re.findall(r"ERROR - .*", blg)
    logs["cited_keys_in_bbl"] = sorted(set(re.findall(r"\\entry\{([^}]+)\}", bbl)))
    m = re.search(r"Output written on .*\((\d+) pages?", log)
    logs["pages"] = int(m.group(1)) if m else None
    aux = (work / f"{job}.aux").read_text(errors="replace") if (work / f"{job}.aux").exists() else ""
    m = re.search(r"\\newlabel\{ThesisEndOfMainText\}\{\{[^}]*\}\{(\d+)\}", aux)
    logs["main_text_last_page"] = int(m.group(1)) if m else None
    return logs


def wrapper(work: Path, label: str | None, body: str, final: bool = False) -> str:
    root = tex_path(PKG, work)
    mode = r"\ThesisFinalMode" if final else r"\ThesisReviewMode{" + escape_label(label) + "}"
    return (f"\\def\\ThesisRoot{{{root}}}\n"
            f"\\input{{\\ThesisRoot/template/thesis-preamble.tex}}\n"
            f"\\addbibresource{{{tex_path(BIB, work)}}}\n"
            f"\\input{{\\ThesisRoot/template/metadata.tex}}\n"
            f"\\begin{{document}}\n{mode}\n{body}\n\\end{{document}}\n")


def hashes_for(paths: dict) -> str:
    return "\n".join(f"| {k} | `{Path(p).relative_to(REPO).as_posix()}` | `{sha256(Path(p))}` |"
                     for k, p in paths.items())


def write_report(kind: str, pdf: Path, logs: dict, inputs: dict, extra: str, insp: dict | None,
                 png_dir: Path | None) -> Path:
    from pdfcheck import to_markdown  # type: ignore
    gs, tv = git_state(), tool_versions()
    rep = pdf.with_suffix(".report.md")
    lines = [f"# Build report — {kind}", "",
             f"- **Output**: `{pdf.relative_to(PKG).as_posix()}`",
             f"- Built (UTC): {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S}",
             f"- Repository: {gs['remote']}; branch `{gs['branch']}`; commit `{gs['commit']}`",
             f"- Uncommitted changes in build inputs at build time: {gs['uncommitted_changes_in_inputs']}",
             f"- Tools: " + "; ".join(f"{k} {v}" for k, v in tv.items()),
             f"- Main font: {font_info(find_tnr())}", "", extra, "",
             "## Input hashes (sha256)", "", "| Role | File | sha256 |", "|---|---|---|",
             hashes_for(inputs), "",
             "## Compilation (final xelatex pass, after biber)", "",
             f"- Pages: {logs['pages']}; LaTeX errors: {logs['errors']}; rerun still requested: "
             f"{logs['rerun_needed']}",
             f"- Missing characters: {len(logs['missing_characters'])} "
             + (str(logs['missing_characters'][:5]) if logs['missing_characters'] else ""),
             f"- Overfull hbox: {logs['overfull_hbox']}; overfull vbox: {logs['overfull_vbox']}; "
             f"underfull hbox: {logs['underfull_hbox']}",
             f"- Undefined citations: {logs['undefined_citations'] or 'none'}; undefined references: "
             f"{logs['undefined_references'] or 'none'}",
             f"- Biber: {len(logs['biber_errors'])} errors, {len(logs['biber_warnings'])} warnings "
             + (str(logs['biber_warnings'][:5]) if logs['biber_warnings'] else ""),
             f"- Works in the generated reference list ({len(logs['cited_keys_in_bbl'])}): "
             + ", ".join(logs["cited_keys_in_bbl"]),
             f"- Font warnings: {logs['font_warnings'] or 'none'}", ""]
    if insp:
        lines += ["## Automated layout measurements (PyMuPDF)", "", to_markdown(insp), ""]
    if png_dir:
        lines += [f"Page images for visual inspection: `{png_dir.relative_to(PKG).as_posix()}/` "
                  "(not committed). Automated checks do not replace looking at every page.", ""]
    rep.write_text("\n".join(lines), encoding="utf-8")
    return rep


def stamp() -> tuple[str, str]:
    now = dt.datetime.now(dt.timezone.utc)
    return now.strftime("%Y-%m-%d"), now.strftime("%Y%m%dT%H%M%SZ")


def finish(kind, work, job, out_pdf, inputs, extra, heading_patterns=None):
    sys.path.insert(0, str(PKG / "scripts"))
    logs = compile_tex(work, job)
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(work / f"{job}.pdf", out_pdf)
    insp, png_dir = None, None
    try:
        import pdfcheck  # type: ignore
        png_dir = work / "pages"
        insp = pdfcheck.inspect(out_pdf, png_dir, heading_patterns=heading_patterns)
        (work / "layout.json").write_text(json.dumps(insp, indent=1, ensure_ascii=False), encoding="utf-8")
    except ImportError:
        print("PyMuPDF not installed: layout measurements and page images skipped")
    rep = write_report(kind, out_pdf, logs, inputs, extra, insp, png_dir)
    print(f"PDF:    {out_pdf}\nReport: {rep}\nWork:   {work}")
    if logs["errors"] or logs["undefined_citations"] or logs["missing_characters"]:
        die("build finished with errors / undefined citations / missing characters (see report)")
    return logs, insp


# --------------------------------------------------------------- commands
def cmd_preview(u, selftest: bool = False) -> None:
    """Chapter preview. With selftest=True the identical pipeline runs on the
    diagnostic Markdown (as stand-in unit 1) so the preview path can be tested
    without rendering any thesis chapter; nothing is written to chapters/."""
    day, ts = stamp()
    sha7 = git("rev-parse", "--short=7", "HEAD")
    if selftest:
        md = PKG / "diagnostics" / "template_verification.md"
        u = ("selftest", "template_verification.md", "chapter", 1, "preview-pipeline")
        tex = BUILDS / "selftest" / "work" / ts / "selftest_unit.tex"
        convert_md(md, tex, "% GENERATED selftest (diagnostic content only)\n\n")
        work = tex.parent
        rel_tex = tex_path(tex, PKG)
        out = BUILDS / "selftest" / f"SELFTEST_preview-pipeline_{day}_{sha7}.pdf"
    else:
        tex = convert(u)
        md = md_copy(u)
        work = BUILDS / "previews" / "work" / f"{u[0]}-{u[4]}_{ts}"
        rel_tex = f"chapters/tex/{tex.name}"
        out = BUILDS / "previews" / f"REVIEW-COPY_{u[0]}-{u[4]}_preview_{day}_{sha7}.pdf"
    work.mkdir(parents=True, exist_ok=True)
    name = f"{u[0]}-{u[4]}"
    label = (f"REVIEW COPY -- {u[0]} preview only -- source {sha7}, md sha256 {sha256(md)[:12]} "
             f"-- provisional pagination -- not the thesis")
    setup = ""
    if u[2] == "chapter":
        setup = f"\\setcounter{{section}}{{{u[3] - 1}}}"
    elif u[2] == "appendix":
        setup = f"\\ThesisAppendixStart\\setcounter{{section}}{{{ord(u[3]) - ord('A')}}}"
    cites = bool(re.search(r"\[[^\]]*@", md.read_text(encoding="utf-8")))
    # The abstract is not a chapter: its preview-only page says "the abstract" (chapter units unchanged).
    scope = "the abstract" if u[2] == "abstract" else "this chapter"
    # Appendix units (added in the Appendix A session): the page says "this appendix", and the
    # chapter-style L1 heading format is restored first, because \ThesisAppendixStart's format
    # would print its "---" separator before the unnumbered heading. In the full thesis the
    # reference list precedes the appendices, so this affects previews only.
    reset = ""
    if u[2] == "appendix":
        scope = "this appendix"
        reset = ("\\titleformat{\\section}[block]{\\fontsize{14bp}{19.5bp}\\selectfont\\bfseries"
                 "\\raggedright}{\\thesection}{0.8em}{}\n")
    # Preview-only reference list (generated here, never part of chapters/tex/). bibintoc gives it
    # a PDF bookmark, so the anchor fix in the preamble can be checked in every preview.
    bib = ("\\clearpage\n" + reset + "\\printbibliography[heading=bibintoc,title={References cited in "
           + scope + " --- preview only}]") if cites else (
        # A unit with no citation commands (ch04) still gets the labelled preview-only page, which
        # states that the list is empty instead of silently omitting it. No entry is generated.
        "\\clearpage\n" + reset + "\\printbibheading[heading=bibintoc,title={References cited in "
        + scope + " --- preview only}]\n{\\bibfont\\noindent This unit contains no citation commands, so no "
        "works are listed. This page is generated at build time for the review copy only and is "
        "not part of the unit's source.\\par}")
    body = (f"\\pagenumbering{{arabic}}\\setcounter{{page}}{{1}}\n{setup}\n"
            f"\\input{{\\ThesisRoot/{rel_tex}}}\n{bib}")
    (work / "preview.tex").write_text(wrapper(work, label, body), encoding="utf-8")
    extra = (f"## What this is\n\nA review copy of **{u[0]}** only, built with the shared template. "
             f"Pagination is provisional (the unit starts at page 1 here; in the thesis it will not). "
             f"The reference list at the end is a verification aid generated at build time; it is "
             f"not part of `chapters/tex/{tex.name}`.\n\n- md identical to canonical: "
             f"{(not selftest) and sha256(md) == sha256(CANON / u[1])}")
    finish(f"REVIEW COPY — {u[0]} preview", work, "preview", out,
           {"chapter md (publishing copy)": md,
            **({} if selftest else {"canonical md": CANON / u[1]}), "generated tex": tex,
            "preamble": TEMPLATE / "thesis-preamble.tex", "filter": FILTER, "bibliography": BIB,
            "build script": Path(__file__)}, extra)


def cmd_diagnostic() -> None:
    src = PKG / "diagnostics" / "template_verification.md"
    tex = PKG / "diagnostics" / "template_verification.tex"
    convert_md(src, tex, f"% GENERATED from template_verification.md (diagnostic content only)\n\n")
    day, ts = stamp()
    sha7 = git("rev-parse", "--short=7", "HEAD")
    work = BUILDS / "diagnostic" / "work" / ts
    work.mkdir(parents=True)
    label = f"TEMPLATE VERIFICATION -- diagnostic content only, not thesis text -- source {sha7}"
    body = (r"\pagenumbering{gobble}" "\n"
            r"\input{\ThesisRoot/diagnostics/diagnostic-cover.tex}\clearpage" "\n"
            r"\input{\ThesisRoot/diagnostics/component-titlepage.tex}" "\n"
            r"\ThesisTableOfContents\clearpage" "\n"
            r"\pagenumbering{arabic}\setcounter{page}{1}" "\n"
            r"\input{\ThesisRoot/diagnostics/template_verification.tex}" "\n"
            r"\label{ThesisEndOfMainText}" "\n"
            r"\clearpage\printbibliography[heading=bibintoc,title={References (diagnostic: works "
            r"cited in this test document)}]" "\n"
            r"\clearpage\ThesisAppendixStart" "\n"
            r"\input{\ThesisRoot/diagnostics/template_verification_appendix.tex}" "\n"
            r"\input{\ThesisRoot/template/declaration.tex}")
    app_src = PKG / "diagnostics" / "template_verification_appendix.md"
    convert_md(app_src, app_src.with_suffix(".tex"), "% GENERATED (diagnostic content only)\n\n")
    (work / "diagnostic.tex").write_text(wrapper(work, label, body), encoding="utf-8")
    out = BUILDS / "diagnostic" / f"TEMPLATE-VERIFICATION_{day}_{sha7}.pdf"
    finish("TEMPLATE VERIFICATION (diagnostic, not a thesis chapter)", work, "diagnostic", out,
           {"diagnostic md": src, "diagnostic appendix md": app_src,
            "preamble": TEMPLATE / "thesis-preamble.tex", "metadata": TEMPLATE / "metadata.tex",
            "title page": TEMPLATE / "titlepage.tex", "declaration": TEMPLATE / "declaration.tex",
            "filter": FILTER, "bibliography": BIB, "build script": Path(__file__)},
           "## What this is\n\nDiagnostic content only. Nothing in it is a thesis finding; it "
           "must not be copied into the manuscript.",
           heading_patterns=[r"^\d+\s*Diagnostic heading", r"^\d+\.\d+\s*Diagnostic heading",
                             r"^\d+\.\d+\.\d+\s*Diagnostic heading",
                             r"^\d+\.\d+\.\d+\.\d+\s*Diagnostic heading"])


def cmd_thesis(final: bool) -> None:
    missing = [u[0] for u in UNITS if not tex_out(u).exists()]
    if missing:
        die("chapters/tex is missing: " + ", ".join(missing) + " (prepare/convert/approve them first)")
    approved = {}
    if APPROVALS.exists():
        for ln in APPROVALS.read_text(encoding="utf-8").splitlines()[1:]:
            if ln.strip() and not ln.startswith("#"):
                parts = ln.split("\t")
                approved[parts[0]] = parts[1]
    not_ok = [u[0] for u in UNITS if approved.get(u[0]) != sha256(tex_out(u))]
    meta = (TEMPLATE / "metadata.tex").read_text(encoding="utf-8")
    if final:
        if not_ok:
            die("--final refused: not approved, or changed since approval: " + ", ".join(not_ok))
        if "to be supplied by the author" in meta:
            die("--final refused: submission month/year placeholder still in template/metadata.tex")
    day, ts = stamp()
    sha7 = git("rev-parse", "--short=7", "HEAD")
    work = BUILDS / "thesis" / "work" / ts
    work.mkdir(parents=True)
    label = (f"DRAFT -- full assembly -- source {sha7} -- not for submission"
             + (f" -- unapproved: {','.join(not_ok)}" if not_ok else ""))
    body = r"\input{\ThesisRoot/drivers/thesis-body.tex}"
    (work / "thesis.tex").write_text(wrapper(work, label, body, final=final), encoding="utf-8")
    out = BUILDS / "thesis" / f"{'FINAL' if final else 'DRAFT'}_full-thesis_{day}_{sha7}.pdf"
    inputs = {f"tex {u[0]}": tex_out(u) for u in UNITS}
    inputs.update({"assembly order": PKG / "drivers" / "thesis-body.tex",
                   "preamble": TEMPLATE / "thesis-preamble.tex", "metadata": TEMPLATE / "metadata.tex",
                   "bibliography": BIB, "build script": Path(__file__)})
    logs, _ = finish("FULL THESIS " + ("FINAL" if final else "DRAFT"), work, "thesis", out, inputs,
                     f"## Status\n\n- Units not approved or changed since approval: {not_ok or 'none'}")
    print(f"Main text runs from page 1 to page {logs['main_text_last_page']} (limit: 40).")


def cited_keys_in_publishing_copies() -> dict:
    """Citation keys actually used by the thesis: every [@key] / [-@key] inside a bracketed
    citation in the eleven chapters/md publishing copies (the same rule as `lint`). Preview
    drivers, reports and verification documents are not read."""
    keys = {}
    for u in UNITS:
        t = md_copy(u).read_text(encoding="utf-8")
        for k in CITE_KEY.findall(" ".join(re.findall(r"\[[^\]]*@[^\]]*\]", t))):
            keys.setdefault(k, []).append(u[0])
    return keys


def cmd_references() -> None:
    """References-only review copy: the consolidated list exactly as the full thesis prints it
    (same preamble, same heading, same bibliography), from an explicit \\nocite list of the keys
    collected from the publishing copies. Never \\nocite{*}."""
    missing = [u[0] for u in UNITS if not md_copy(u).exists()]
    if missing:
        die("chapters/md is missing: " + ", ".join(missing))
    keys = cited_keys_in_publishing_copies()
    bib_keys = set(re.findall(r"@\w+\{([^,\s]+),", BIB.read_text(encoding="utf-8")))
    if set(keys) - bib_keys:
        die("cited keys not in the bibliography: " + ", ".join(sorted(set(keys) - bib_keys)))
    day, ts = stamp()
    sha7 = git("rev-parse", "--short=7", "HEAD")
    work = BUILDS / "previews" / "work" / f"references-consolidated_{ts}"
    work.mkdir(parents=True)
    label = (f"REVIEW COPY -- consolidated references only -- source {sha7}, bib sha256 "
             f"{sha256(BIB)[:12]} -- provisional pagination -- not the thesis")
    body = ("\\pagenumbering{arabic}\\setcounter{page}{1}\n"
            "\\nocite{" + ",".join(sorted(keys)) + "}\n"
            "\\printbibliography[heading=bibintoc,title={References}]")
    (work / "references.tex").write_text(wrapper(work, label, body), encoding="utf-8")
    out = BUILDS / "previews" / f"REVIEW-COPY_references-consolidated_preview_{day}_{sha7}.pdf"
    rows = "\n".join(f"| `{k}` | {', '.join(sorted(set(v)))} | {len(v)} |" for k, v in sorted(keys.items()))
    extra = ("## What this is\n\nA review copy of the **consolidated reference list only**, built "
             "with the shared preamble and the same `\\printbibliography[heading=bibintoc,title="
             "{References}]` call as `drivers/thesis-body.tex`. No chapter is typeset. Pagination is "
             "provisional (the list starts at page 1 here; in the thesis it follows Chapter 7).\n\n"
             "## How the printed works were selected\n\nThe thesis text is not typeset here, so the "
             "works are requested with an explicit `\\nocite{...}` list (never `\\nocite{*}`). The "
             f"list is generated at build time from the {len(UNITS)} publishing copies in `chapters/md/` "
             "(bracketed `[@key]` and `[-@key]` citations; the rule `lint` uses). Preview drivers, "
             f"reports and verification documents are not read. **{len(keys)} keys, "
             f"{sum(len(v) for v in keys.values())} citation occurrences**; bibliography entries: "
             f"{len(bib_keys)}; uncited entries not printed: {len(bib_keys - set(keys))} "
             f"({', '.join(sorted(bib_keys - set(keys)))}).\n\n| Key | Units | Occurrences |\n"
             "|---|---|---|\n" + rows)
    logs, _ = finish("REVIEW COPY — consolidated references", work, "references", out,
                     {**{f"md {u[0]}": md_copy(u) for u in UNITS},
                      "bibliography (publishing copy)": BIB, "canonical bibliography": CANON_BIB,
                      "preamble": TEMPLATE / "thesis-preamble.tex", "build script": Path(__file__)},
                     extra)
    if set(logs["cited_keys_in_bbl"]) != set(keys):
        die("the generated list differs from the collected keys: "
            f"{sorted(set(logs['cited_keys_in_bbl']) ^ set(keys))}")
    print(f"references: {len(keys)} works printed; generated list equals the collected keys")


def cmd_manifest(write: bool) -> None:
    """Record (once) or check the sha256 of every canonical input."""
    files = [CANON / u[1] for u in UNITS] + [CANON_BIB, CANON / "CROSS_REFERENCE_MAP.md",
                                             CANON / "citation_map.md", CANON / "MASTER_ASSEMBLY.md"]
    rows = {f.relative_to(REPO).as_posix(): sha256(f) for f in files}
    if write:
        if MANIFEST.exists():
            die(f"{MANIFEST.name} exists; it is never overwritten (check it instead)")
        MANIFEST.write_text("path\tsha256\n" + "".join(f"{k}\t{v}\n" for k, v in rows.items())
                            + f"# recorded at commit {git('rev-parse', 'HEAD')}\n", encoding="utf-8")
        print(f"wrote {MANIFEST.name} ({len(rows)} files)")
        return
    rec = {}
    for ln in MANIFEST.read_text(encoding="utf-8").splitlines()[1:]:
        if ln and not ln.startswith("#"):
            k, v = ln.split("\t")
            rec[k] = v
    changed = [k for k in rows if rec.get(k) != rows[k]]
    for k in changed:
        print(f"CHANGED since manifest: {k}")
    print(f"manifest check: {len(rows) - len(changed)}/{len(rows)} canonical inputs unchanged")
    if changed:
        sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["env", "lint", "prepare", "convert", "preview",
                                        "diagnostic", "selftest", "thesis", "inspect", "manifest",
                                        "references"])
    ap.add_argument("--write", action="store_true", help="manifest: record hashes (first time only)")
    ap.add_argument("args", nargs="*")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--publishing-copies", action="store_true",
                    help="lint chapters/md copies instead of the canonical sources")
    a = ap.parse_args()
    if a.command == "env":
        for k, v in tool_versions().items():
            print(f"{k:8s} {v}")
        print("font    ", font_info(find_tnr()))
        print("repo    ", git_state())
        print("canon   ", CANON, "exists" if CANON.exists() else "MISSING")
    elif a.command == "lint":
        us = [unit(x) for x in a.args] if a.args else UNITS
        sys.exit(1 if lint(us, "publishing" if a.publishing_copies else "canonical") else 0)
    elif a.command in ("prepare", "convert", "preview"):
        if len(a.args) != 1:
            die(f"{a.command} takes exactly one unit")
        {"prepare": prepare, "convert": convert, "preview": cmd_preview}[a.command](unit(a.args[0]))
    elif a.command == "diagnostic":
        cmd_diagnostic()
    elif a.command == "manifest":
        cmd_manifest(a.write)
    elif a.command == "selftest":
        cmd_preview(None, selftest=True)
    elif a.command == "thesis":
        cmd_thesis(a.final)
    elif a.command == "references":
        cmd_references()
    elif a.command == "inspect":
        sys.path.insert(0, str(PKG / "scripts"))
        import pdfcheck  # type: ignore
        pdf = Path(a.args[0]).resolve()
        r = pdfcheck.inspect(pdf, pdf.parent / (pdf.stem + "_pages"))
        print(pdfcheck.to_markdown(r))


if __name__ == "__main__":
    main()
