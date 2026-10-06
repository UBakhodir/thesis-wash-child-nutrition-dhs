"""
02_import_ipums_idhs_00001.py
=============================
Reproducible, read-only import of the IPUMS DHS extract idhs_00001.

Layout source: idhs_00001.xml (IPUMS DDI codebook). Cross-checked against
idhs_00001.do (Stata infix block). The script refuses to import unless the two
layouts agree on every variable, the field positions are contiguous, and every
record has the documented width.

Inputs (read-only, never modified):
  <DOWNLOADS>\\idhs_00001.dat.gz   data (gzip-compressed fixed-width)
  <DOWNLOADS>\\idhs_00001.xml      DDI codebook
  <DOWNLOADS>\\idhs_00001.do       Stata infix dictionary

Outputs (new, versioned, outside tracked repository content):
  <MASTER>/data/processed/ipums_import/v1/idhs_00001_raw_strings_v1.parquet
  <MASTER>/data/processed/ipums_import/v1/idhs_00001_manifest_v1.json
  <MASTER>/data/processed/ipums_import/v1/idhs_00001_import_log_v1.txt

Design:
  - Raw layer keeps every field as the exact 280-character slice (after removing
    the record terminator). Nothing is coerced in the raw layer.
  - Typed diagnostics are produced separately and never overwrite the raw layer.
  - Refuses to overwrite any existing output.
  - Records source and output SHA-256 before and after execution.
"""
import gzip
import hashlib
import json
import os
import platform
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import pandas as pd
import pyarrow as pa

DOWNLOADS = r"C:\Users\user\Downloads"
MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
OUT_DIR = os.path.join(MASTER, "data", "processed", "ipums_import", "v1")
SRC_DAT = os.path.join(DOWNLOADS, "idhs_00001.dat.gz")
SRC_XML = os.path.join(DOWNLOADS, "idhs_00001.xml")
SRC_DO = os.path.join(DOWNLOADS, "idhs_00001.do")
EXPECTED_WIDTH = 280
NS = "{ddi:codebook:2_5}"

log_lines = []


def log(msg):
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line)
    log_lines.append(line)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_xml_layout(path):
    root = ET.parse(path).getroot()
    out = []
    for v in root.iter(NS + "var"):
        loc = v.find(NS + "location")
        vf = v.find(NS + "varFormat")
        name = v.get("name")
        start = int(loc.get("StartPos"))
        end = int(loc.get("EndPos"))
        out.append({
            "name": name,
            "start": start,
            "end": end,
            "width": end - start + 1,
            "ddi_type": vf.get("type") if vf is not None else None,
            "ddi_schema": vf.get("schema") if vf is not None else None,
            "ddi_decimals": vf.get("DCML") if vf is not None else None,
            "n_categories": len(v.findall(NS + "catgry")),
        })
    return out


def parse_do_layout(path):
    text = open(path, encoding="latin-1").read()
    block = text.split("infix", 1)[1].split("using", 1)[0]
    fields = re.findall(r"(byte|int|long|float|double|str\d*)\s+(\w+)\s+(\d+)-(\d+)", block)
    return [{"stata_type": t, "name": n, "start": int(s), "end": int(e)} for t, n, s, e in fields]


def main():
    for p in (SRC_DAT, SRC_XML, SRC_DO):
        if not os.path.isfile(p):
            log(f"FATAL missing input: {p}")
            sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)
    targets = [
        os.path.join(OUT_DIR, "idhs_00001_raw_strings_v1.parquet"),
        os.path.join(OUT_DIR, "idhs_00001_manifest_v1.json"),
        os.path.join(OUT_DIR, "idhs_00001_import_log_v1.txt"),
    ]
    for t in targets:
        if os.path.exists(t):
            log(f"FATAL output exists, refusing to overwrite: {t}")
            sys.exit(1)

    log(f"python={platform.python_version()} pandas={pd.__version__} pyarrow={pa.__version__}")
    hash_before = {p: sha256_file(p) for p in (SRC_DAT, SRC_XML, SRC_DO)}
    for p, h in hash_before.items():
        log(f"source before: {os.path.basename(p)} bytes={os.path.getsize(p)} sha256={h}")

    xml_layout = parse_xml_layout(SRC_XML)
    do_layout = parse_do_layout(SRC_DO)
    log(f"XML variables={len(xml_layout)} Stata fields={len(do_layout)}")
    if len(xml_layout) != len(do_layout):
        log("FATAL variable count differs between XML and Stata layouts")
        sys.exit(1)
    xml_map = {x["name"].lower(): x for x in xml_layout}
    mismatches = []
    for d in do_layout:
        x = xml_map.get(d["name"].lower())
        if x is None or (x["start"], x["end"]) != (d["start"], d["end"]):
            mismatches.append((d["name"], d["start"], d["end"], x and (x["start"], x["end"])))
    if mismatches:
        log(f"FATAL XML/Stata position mismatches: {mismatches}")
        sys.exit(1)
    spans = sorted((x["start"], x["end"], x["name"]) for x in xml_layout)
    if spans[0][0] != 1:
        log("FATAL layout does not start at column 1")
        sys.exit(1)
    for (s1, e1, n1), (s2, e2, n2) in zip(spans, spans[1:]):
        if s2 != e1 + 1:
            log(f"FATAL gap or overlap between {n1} ({s1}-{e1}) and {n2} ({s2}-{e2})")
            sys.exit(1)
    record_width = spans[-1][1]
    if record_width != EXPECTED_WIDTH:
        log(f"FATAL layout width {record_width} != expected {EXPECTED_WIDTH}")
        sys.exit(1)
    log(f"layout verified: XML == Stata for all {len(xml_layout)} fields, contiguous 1-{record_width}")

    names = [x["name"] for x in sorted(xml_layout, key=lambda x: x["start"])]
    slices = [(x["name"], x["start"] - 1, x["end"]) for x in sorted(xml_layout, key=lambda x: x["start"])]

    rows = []
    bad_width = 0
    n_records = 0
    with gzip.open(SRC_DAT, "rb") as f:
        for raw in f:
            n_records += 1
            line = raw.rstrip(b"\r\n")
            if len(line) != record_width:
                bad_width += 1
                continue
            text = line.decode("iso-8859-1")
            rows.append([text[a:b] for _, a, b in slices])
    log(f"records read={n_records} records with width != {record_width}={bad_width}")
    if bad_width:
        log("FATAL record-width failures present; no output written")
        sys.exit(1)

    raw_df = pd.DataFrame(rows, columns=names, dtype="string")
    raw_df.insert(0, "record_number", pd.Series(range(1, len(raw_df) + 1), dtype="int64"))
    raw_df.to_parquet(targets[0], index=False)
    log(f"wrote raw string layer: rows={len(raw_df)} cols={raw_df.shape[1]} -> {targets[0]}")

    hash_after = {p: sha256_file(p) for p in (SRC_DAT, SRC_XML, SRC_DO)}
    unchanged = all(hash_before[p] == hash_after[p] for p in hash_before)
    log(f"source unchanged after import: {unchanged}")
    if not unchanged:
        log("FATAL source changed during import")
        sys.exit(1)

    out_hash = sha256_file(targets[0])
    manifest = {
        "script": "scripts/historical_wash/02_import_ipums_idhs_00001.py",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "pyarrow": pa.__version__,
        "sources": {os.path.basename(p): {"path": p, "bytes": os.path.getsize(p),
                                           "sha256_before": hash_before[p],
                                           "sha256_after": hash_after[p]}
                    for p in (SRC_DAT, SRC_XML, SRC_DO)},
        "records_read": n_records,
        "records_imported": int(len(raw_df)),
        "record_width": record_width,
        "output_raw_parquet": {"path": targets[0], "sha256": out_hash},
        "layout": xml_layout,
        "layout_agreement": "XML and Stata infix agree on all fields; contiguous",
    }
    with open(targets[1], "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    log(f"wrote manifest -> {targets[1]}")
    with open(targets[2], "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
