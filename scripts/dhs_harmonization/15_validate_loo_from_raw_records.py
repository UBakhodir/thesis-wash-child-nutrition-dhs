"""
15_validate_loo_from_raw_records.py
====================================
Independent rebuild of the leave-one-out (LOO) community WASH exposure
directly from the raw DHS household recode (.DTA inside the official HR
zip archive), without calling 01_wash_mapping.py's category dictionaries or
08_hr_cluster_wash_exposure.py's compute_leave_one_out()/build_indicator()
functions. Written for the 2026-10-07 audit continuation
(docs/provenance/independent_audit_v1_2026-10-07/): item 2, "Rebuild
leave-one-out community exposure directly from source records without
calling the original construction function."

Independence, stated precisely: this script re-derives the water/sanitation
"improved" classification from the standard, externally documented DHS/JMP
v113/v116-equivalent (native hv201/hv205) code scheme -- the classification
itself is an external standard, not a project-specific choice to
independently verify; what this script verifies independently is the
CONSTRUCTION (classification application, denominator handling, leave-one-
out computation), using a brute-force per-cluster computation (not the
project's vectorized groupby/transform) and reading the raw .DTA directly
(not the project's staged/cleaned parquet).

Run on Ghana 2022 (one of the four baseline countries; chosen because it is
the smallest baseline round, making a full, non-sampled brute-force
comparison computationally cheap).
"""
import io
import zipfile
import pandas as pd

MASTER = r"C:\Users\user\Documents\Graduation_Thesis"
HR_ZIP = MASTER + r"\data\raw\DHS\ghana\2022\HR\GHHR8CDT.zip"
HR_MEMBER = "GHHR8CFL.DTA"
STORED_PATH = MASTER + r"\data\processed\pooled_kr_four_country_wash_exposure.parquet"

# Independently re-derived from the standard DHS/JMP "improved" facility
# classification (not copied from scripts/dhs_harmonization/01_wash_mapping.py):
WATER_IMPROVED = {11, 12, 13, 14, 21, 31, 41, 51, 61, 62, 71, 72}
WATER_UNIMPROVED = {32, 42, 43}
WATER_EXCLUDED = {96, 97}

SANI_IMPROVED = {11, 12, 13, 21, 22, 41}
SANI_UNIMPROVED = {14, 15, 23, 31, 42, 43}  # 31 (open defecation) grouped as "not improved" here
SANI_EXCLUDED = {16, 96, 97}  # 16 = Ghana bio-digester, excluded in the core spec (matches project's own
                              # documented treatment -- "no authoritative JMP source found" -- not re-derived
                              # independently here, since it is a documented data-quality exclusion, not a
                              # classification question)


def classify(code, improved_set, unimproved_set):
    if pd.isna(code):
        return None
    code = int(code)
    if code in improved_set:
        return 1
    if code in unimproved_set:
        return 0
    return None  # excluded (96/97/16): neither numerator nor denominator


def brute_force_loo(df, indicator_col):
    """Per-cluster, per-household, explicit O(n^2) recomputation: for each
    household, average the indicator over every OTHER household in the same
    cluster with a non-missing indicator. No vectorised groupby/transform."""
    out = {}
    for cluster, g in df.groupby("hv001"):
        idx = g.index.tolist()
        vals = g[indicator_col].tolist()
        for i, hh_i in enumerate(idx):
            # NOTE (found during this validation pass): `classify()` returns
            # Python None for excluded households, but once stored in a
            # pandas float64 column (because the same column also holds
            # 1.0/0.0 floats), None is silently upcast to NaN -- pandas has
            # no way to hold None in a float64 Series. A plain `is not None`
            # check does NOT catch this (float('nan') is not None is True),
            # so an earlier version of this script let excluded households
            # leak into the "others" list, contaminating the sum with NaN
            # and making the whole leave-one-out rate NaN even when enough
            # genuinely classified neighbours existed. pd.notna() catches
            # both None and NaN correctly.
            others = [vals[j] for j in range(len(idx)) if j != i and pd.notna(vals[j])]
            out[hh_i] = (sum(others) / len(others)) if others else None
    return out


def main():
    print("=== Independent LOO rebuild from raw HR records (Ghana 2022) ===")
    with zipfile.ZipFile(HR_ZIP) as z:
        with z.open(HR_MEMBER) as f:
            raw = pd.read_stata(io.BytesIO(f.read()), convert_categoricals=False)
    print(f"raw HR records loaded: {len(raw)} households, {raw.shape[1]} columns")

    df = raw[["hv001", "hv002", "hv201", "hv205"]].copy()
    df["water_ind"] = df["hv201"].apply(lambda c: classify(c, WATER_IMPROVED, WATER_UNIMPROVED))
    df["sani_ind"] = df["hv205"].apply(lambda c: classify(c, SANI_IMPROVED, SANI_UNIMPROVED))
    print(f"water classified: {df.water_ind.notna().sum()} of {len(df)} "
          f"({df.water_ind.isna().sum()} excluded/unknown/structural)")
    print(f"sanitation classified: {df.sani_ind.notna().sum()} of {len(df)} "
          f"({df.sani_ind.isna().sum()} excluded/unknown/structural/bio-digester)")

    water_loo = brute_force_loo(df, "water_ind")
    sani_loo = brute_force_loo(df, "sani_ind")
    df["water_rate_loo_independent"] = df.index.map(water_loo)
    df["sanitation_rate_loo_independent"] = df.index.map(sani_loo)
    df["country_household_id"] = "ghana_" + df.hv001.astype(str) + "_" + df.hv002.astype(str)

    stored = pd.read_parquet(STORED_PATH, columns=[
        "country", "country_household_id", "water_rate_loo", "sanitation_rate_loo_core",
        "water_rate_loo_n_other_hh", "sanitation_rate_loo_core_n_other_hh"])
    stored_gh = stored[stored.country == "ghana"].drop_duplicates(subset="country_household_id")

    m = df.merge(stored_gh, on="country_household_id", how="inner")
    print(f"\nmatched {len(m)} of {len(df)} raw households to the stored, "
          f"processed household-level records (duplicates in the stored file, e.g. multiple "
          f"children per household, are dropped before this join)")

    for label, indep_col, stored_col in [
        ("water", "water_rate_loo_independent", "water_rate_loo"),
        ("sanitation", "sanitation_rate_loo_independent", "sanitation_rate_loo_core"),
    ]:
        both = m[[indep_col, stored_col]].dropna()
        diff = (both[indep_col] - both[stored_col]).abs()
        print(f"\n{label}: n_compared={len(both)} (of {len(m)} matched households)")
        print(f"  max_abs_diff={diff.max():.10f}  mean_abs_diff={diff.mean():.10f}")
        mismatch = (diff > 1e-9).sum()
        print(f"  mismatches (diff > 1e-9): {mismatch} of {len(both)}")
        # NaN-pattern agreement (households that should be excluded from the
        # comparison in both the independent and stored constructions):
        indep_na = m[indep_col].isna()
        stored_na = m[stored_col].isna()
        print(f"  NaN-pattern agreement: {(indep_na == stored_na).sum()} of {len(m)}")

    out_path = MASTER + r"\data\processed\loo_independent_validation_ghana.csv"
    m[["country_household_id", "water_rate_loo_independent", "water_rate_loo",
       "sanitation_rate_loo_independent", "sanitation_rate_loo_core"]].to_csv(out_path, index=False)
    print(f"\nComparison table written to {out_path} (RESTRICTED, household-level, not committed to git)")


if __name__ == "__main__":
    main()
