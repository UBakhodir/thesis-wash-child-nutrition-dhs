"""
19_check_model_design.py
========================
Design checks on the preliminary model datasets (run 16). Aggregate output only.
PRELIMINARY - measurement-weight documentation and final design review pending.

Checks per primary model (and per sensitivity family where the dataset is stored):
  - record key uniqueness within each model dataset;
  - cluster identifier (IDHSPSU) maps to exactly one survey (sample-qualified cluster keys);
  - country weight totals equal N / K within each model's estimation sample;
  - regressor rank equals the number of retained regressors (no residual collinearity);
  - singleton clusters absent from the estimation dataset (they were dropped before estimation);
  - residual exposure variation: clusters with varying exposure.
Usage: python 19_check_model_design.py <estimation_run_folder>
"""
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import pandas as pd

if len(sys.argv) != 2:
    sys.exit("usage: 19_check_model_design.py <estimation_run_folder>")
RUN = sys.argv[1]
OUT = os.path.join(RUN, f"design_checks_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
os.makedirs(OUT, exist_ok=False)
PRELIM = "PRELIMINARY - measurement-weight documentation and final design review pending."


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


res = pd.read_csv(os.path.join(RUN, "model_results_RESTRICTED_coefficients.csv"))
D = pd.read_parquet(os.path.join(RUN, "primary_model_datasets_RESTRICTED.parquet"))
src = os.path.join(RUN, "primary_model_datasets_RESTRICTED.parquet")
h_before = sha(src)
rows = []
for mid, g in D.groupby("model_id"):
    meta = res[res["id"] == mid].iloc[0]
    n = len(g)
    key_dup = int(g.duplicated(["record_number"]).sum())
    survey_per_psu = g.groupby("IDHSPSU")["SAMPLE"].nunique()
    psu_multi_survey = int((survey_per_psu > 1).sum())
    sizes = g.groupby("IDHSPSU").size()
    singletons_present = int((sizes < 2).sum())
    K = int(meta["K_regressors"])
    rank = int(meta["rank"])
    wt = json.loads(meta["weights_country_total"])
    n_samples = len(wt)
    expected_total = n / n_samples if n_samples else float("nan")
    weight_ok = all(abs(v - expected_total) < 1e-6 * max(expected_total, 1) for v in wt.values())
    rows.append({
        "model_id": mid, "label": PRELIM, "family": meta["family"], "product": meta["product"],
        "outcome": meta["outcome"], "samples": meta["samples"], "window": meta["window"], "method": meta["method"],
        "N_dataset": n, "N_reported": int(meta["N"]), "N_match": n == int(meta["N"]),
        "G_clusters": int(sizes.size), "G_reported": int(meta["G_clusters"]), "G_match": int(sizes.size) == int(meta["G_clusters"]),
        "record_key_duplicates": key_dup, "psu_mapping_to_multiple_surveys": psu_multi_survey,
        "singleton_clusters_in_dataset": singletons_present,
        "country_weight_totals_equal_N_over_K": bool(weight_ok),
        "K_regressors": K, "rank": rank, "rank_full": rank == K,
        "absorbed_terms": meta["columns_absorbed"],
        "clusters_with_exposure_variation": int(meta["clusters_with_exposure_variation"]),
    })
chk = pd.DataFrame(rows)
chk.to_csv(os.path.join(OUT, "design_checks_per_model_AGGREGATE.csv"), index=False)
summary = {"label": PRELIM, "models_checked": int(len(chk)),
           "all_N_match": bool(chk["N_match"].all()), "all_G_match": bool(chk["G_match"].all()),
           "no_record_key_duplicates": bool((chk["record_key_duplicates"] == 0).all()),
           "no_psu_across_surveys": bool((chk["psu_mapping_to_multiple_surveys"] == 0).all()),
           "no_singletons_in_estimation": bool((chk["singleton_clusters_in_dataset"] == 0).all()),
           "weight_totals_equal_N_over_K": bool(chk["country_weight_totals_equal_N_over_K"].all()),
           "all_rank_full": bool(chk["rank_full"].all()),
           "inputs_unchanged": h_before == sha(src)}
with open(os.path.join(OUT, "design_checks_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=1)
print(json.dumps(summary))
