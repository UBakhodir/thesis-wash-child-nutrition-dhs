"""
18_common_sample_windows.py
===========================
PRELIMINARY window comparison on a COMMON sample. Each window is estimated on (a) its own eligible
sample (run 16 results) and (b) the common sample: children eligible for all four windows for the
same product. Reuses the frame and estimator of script 16 (imported unchanged).
Labelled PRELIMINARY. No new specification is added; the same working model is used.
Runs with the repository virtual environment.
"""
import hashlib
import importlib.util
import json
import os
from datetime import datetime, timezone

import pandas as pd

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
E16 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "16_estimate_preliminary.py")
OUT_ROOT = os.path.join(MASTER, "data", "processed", "estimation")
PRELIM = "PRELIMINARY - measurement-weight documentation and final design review pending."
EST = [28806, 40406, 56606]
WINDOWS = ["birth_year", "prenatal_9m", "post_12m", "post_24m"]
OUTC = {"HAZ": "HAZ_z", "WAZ": "WAZ_z", "WHZ": "WHZ_z"}
SL = {28806: "GH2014", 40406: "KE2014", 56606: "NG2018", 23104: "ET2016"}


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def load_e16():
    spec = importlib.util.spec_from_file_location("e16", E16)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    e16 = load_e16()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = os.path.join(OUT_ROOT, f"common_sample_{stamp}")
    os.makedirs(out_dir, exist_ok=False)
    src = [e16.AN, e16.CON]
    before = {p: sha(p) for p in src}
    M = e16.load()
    rows = []
    for product in ["W_IMP", "S_IMP"]:
        frames = {w: e16.frame(M, product, w, "primary", "GREGORIAN_ESTABLISHED", EST) for w in WINDOWS}
        common = None
        for w in WINDOWS:
            ids = set(zip(frames[w]["record_number"], frames[w]["SAMPLE"]))
            common = ids if common is None else common & ids
        for w in WINDOWS:
            f = frames[w]
            keep_common = f.apply(lambda r: (r["record_number"], r["SAMPLE"]) in common, axis=1)
            for oc, col in OUTC.items():
                for smp in EST + ["POOLED"]:
                    samples_ids = EST if smp == "POOLED" else [smp]
                    for basis, dfb in [("own_eligible_sample", f), ("common_sample_all_windows", f[keep_common])]:
                        d = dfb[dfb["SAMPLE"].isin(samples_ids)]
                        res = e16.fit(d, col, weighted=True)
                        res.pop("_df", None)
                        row = {"label": PRELIM, "product": product, "outcome": oc, "window": w,
                               "sample_group": "POOLED_ESTABLISHED" if smp == "POOLED" else SL[smp], "basis": basis,
                               "status": res.get("status")}
                        for k in ["N", "G_clusters", "singleton_clusters_dropped", "singleton_obs_dropped",
                                  "beta_per_10", "se_per_10", "ci95_low_per_10", "ci95_high_per_10", "p_value",
                                  "E_residual_sd_after_controls", "rank", "K_regressors"]:
                            row[k] = res.get(k)
                        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(out_dir, "window_common_sample_AGGREGATE_PRELIMINARY.csv"), index=False)
    after = {p: sha(p) for p in src}
    manifest = {"label": PRELIM, "script": "scripts/historical_wash/18_common_sample_windows.py",
                "script_sha256": sha(__file__), "rows": len(df), "inputs_unchanged": before == after}
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
