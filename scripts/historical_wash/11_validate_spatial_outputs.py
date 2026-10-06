"""
11_validate_spatial_outputs.py
==============================
Aggregate validation of a spatial-extraction run (restricted cluster-year table).
Reads the restricted parquet read-only; writes aggregate tables only to a new folder
(inside the restricted run folder, never in the repository). Prints counts and
summaries only; no cluster identifiers or coordinates.

Usage: python 11_validate_spatial_outputs.py <run_folder>
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

if len(sys.argv) != 2:
    sys.exit("usage: 11_validate_spatial_outputs.py <run_folder>")
RUN = sys.argv[1]
PARQ = os.path.join(RUN, "cluster_year_extraction_RESTRICTED.parquet")
OUT = os.path.join(RUN, "validation_aggregates")
os.makedirs(OUT, exist_ok=False)
YEARS = list(range(2000, 2018))
SAMPLES = {23104: "ET2016", 28806: "GH2014", 40406: "KE2014", 56606: "NG2018"}
expected = {"clusters_primary": 4011, "clusters_rural_sensitivity": 2408}
log = []


def say(msg):
    print(f"{datetime.now(timezone.utc).isoformat()} {msg}", flush=True)
    log.append(msg)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


src_hash = sha256(PARQ)
df = pd.read_parquet(PARQ)
df["sample"] = df["SAMPLE"].map(SAMPLES)
say(f"rows={len(df)} columns={df.shape[1]}")

res = {}
res["rows_total"] = int(len(df))
res["by_method_rows"] = df.groupby("method").size().to_dict()
prim = df[df["method"] == "primary_area_buffer"]
res["clusters_primary"] = int(prim["IDHSPSU"].nunique())
res["clusters_rural_sensitivity"] = int(df.loc[df["method"] == "sensitivity_rural_10km_buffer", "IDHSPSU"].nunique())
res["clusters_point"] = int(df.loc[df["method"] == "sensitivity_containing_pixel", "IDHSPSU"].nunique())
res["reconciles_expected_4011"] = bool(res["clusters_primary"] == expected["clusters_primary"])
res["reconciles_rural_2408"] = bool(res["clusters_rural_sensitivity"] == expected["clusters_rural_sensitivity"])
res["years_present"] = sorted(int(y) for y in df["year"].unique())
res["years_complete_2000_2017"] = bool(res["years_present"] == YEARS)
res["products"] = sorted(df["product"].unique().tolist())
res["estimates"] = sorted(df["estimate"].unique().tolist())

key = ["IDHSPSU", "product", "estimate", "year", "method"]
dup = df.duplicated(subset=key, keep=False)
res["duplicate_keys"] = int(dup.sum())
per_cluster_method = df.groupby(["IDHSPSU", "method"]).size()
expected_per = len(YEARS) * 2 * 3
res["cluster_method_with_expected_108_rows"] = int((per_cluster_method == expected_per).sum())
res["cluster_method_total"] = int(len(per_cluster_method))

# finite values and range
done = df[df["status"].isin(["full", "partial"])]
res["covered_rows"] = int(len(done))
res["covered_values_nonfinite"] = int((~np.isfinite(done["value"])).sum())
res["covered_values_outside_0_100"] = int(((done["value"] < 0) | (done["value"] > 100)).sum())
res["missing_rows"] = int((df["status"] == "missing").sum())
res["missing_rows_with_nonnan_value"] = int((df["status"].eq("missing") & df["value"].notna()).sum())

# coverage by method and product
cov = df.groupby(["method", "product", "status"]).size().unstack(fill_value=0)
cov.to_csv(os.path.join(OUT, "coverage_by_method_product_status.csv"))
say("coverage by method/product/status:\n" + cov.to_string())

# missingness reasons
rs = df[df["status"] != "full"].groupby(["method", "reason"]).size().reset_index(name="rows")
rs.to_csv(os.path.join(OUT, "missingness_reasons.csv"), index=False)
say("missingness reasons:\n" + rs.to_string(index=False))

# bound ordering: LOWER <= MEAN <= UPPER where all three are covered
wide = done.pivot_table(index=["IDHSPSU", "product", "year", "method"], columns="estimate",
                        values="value", aggfunc="first")
both = wide.dropna(subset=["LOWER", "MEAN", "UPPER"])
viol_lm = int((both["LOWER"] > both["MEAN"]).sum())
viol_mu = int((both["MEAN"] > both["UPPER"]).sum())
res["bound_triples_compared"] = int(len(both))
res["violations_LOWER_gt_MEAN"] = viol_lm
res["violations_MEAN_gt_UPPER"] = viol_mu
res["violation_share"] = round(float((viol_lm + viol_mu) / max(len(both), 1)), 6)
say(f"bound triples={len(both)} LOWER>MEAN={viol_lm} MEAN>UPPER={viol_mu}")

# value distribution by sample, product, estimate (method = primary)
dist = prim[prim["status"].isin(["full", "partial"])].groupby(["sample", "product", "estimate"])["value"].describe(
    percentiles=[0.05, 0.5, 0.95]).round(3)
dist.to_csv(os.path.join(OUT, "value_distribution_primary.csv"))
say("primary value distribution (rows = sample/product/estimate):\n" + dist.head(12).to_string())

# buffer vs point (mean across years, for MEAN estimate; aggregate differences only)
pt = df[(df["method"] == "sensitivity_containing_pixel") & (df["estimate"] == "MEAN")][["IDHSPSU", "product", "year", "value"]]
pb = prim[(prim["estimate"] == "MEAN")][["IDHSPSU", "product", "year", "value", "status"]]
mm = pb.merge(pt, on=["IDHSPSU", "product", "year"], suffixes=("_buffer", "_point"))
mm["diff"] = mm["value_buffer"] - mm["value_point"]
dd = mm.dropna(subset=["diff"]).groupby("product")["diff"].describe(percentiles=[0.05, 0.5, 0.95]).round(3)
dd.to_csv(os.path.join(OUT, "buffer_minus_point_MEAN.csv"))
say("buffer minus point (MEAN, both defined):\n" + dd.to_string())
res["buffer_point_pairs_both_defined"] = int(len(mm.dropna(subset=["diff"])))

# valid-area fraction distribution for primary buffers
vf = prim.groupby(["sample", "stratum"])["valid_fraction"].describe(percentiles=[0.1, 0.5]).round(4)
vf.to_csv(os.path.join(OUT, "valid_fraction_primary.csv"))
say("valid-area fraction (primary):\n" + vf.to_string())

with open(os.path.join(OUT, "validation_summary.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=1, default=str)
say("summary: " + json.dumps(res, default=str))
say(f"source sha256 unchanged: {sha256(PARQ) == src_hash}")
with open(os.path.join(OUT, "validation_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
