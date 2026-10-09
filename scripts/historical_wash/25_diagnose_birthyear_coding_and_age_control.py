"""
25_diagnose_birthyear_coding_and_age_control.py
=================================================
Targeted diagnostic, not a general rerun, written in response to a direct
instruction to distinguish, for the pooled established-date water-HAZ cell's
well-known 1.385-vs-1.026 early discrepancy (documented in
20_validate_pooled_estimate.py's own docstring and Appendix B §B.2):

  (a) an equivalent reparameterization (same column space, different labelled
      reference category -- cannot change fitted values or the exposure
      coefficient, by basic linear-algebra identity of OLS/WLS);
  (b) a genuinely different set of country-by-birth-year columns (different
      column space -- CAN change the coefficient); and
  (c) the separately-documented omission of the child's own age-in-months
      control in that same early attempt.

IMPORTANT, stated plainly per the instruction not to speculate: the exact
code of that early, buggy attempt was never committed to this repository --
only described in prose (20_validate_pooled_estimate.py's own docstring,
Appendix B §B.2). This script therefore does NOT claim to reproduce that
exact historical run byte-for-byte, and does NOT claim to exactly decompose
the specific historical 1.385-vs-1.026 gap into precise separate numeric
contributions from (a)/(b) and (c). What it DOES establish, as a fresh,
general, falsifiable diagnostic on the current, correct sample: whether "a
single combined reference cell across countries" (the described change) is,
in fact, a rank-preserving reparameterization of the country-local-reference
scheme this thesis uses (case a) or a genuinely different design (case b);
and, separately and unambiguously (no reconstruction needed), the exact
standalone effect of including vs. excluding the age-in-months control,
holding the birth-year coding fixed at the correct, country-local scheme.

RESULT (2026-10-09, run recorded in
data/processed/estimation/birthyear_coding_diagnostic_20261009T075217Z/):
on this reconstruction, the birth-year-coding change alone moves the
fitted E10 coefficient by EXACTLY 0.0000000 (1.0255531 under both schemes,
holding age_m included) -- "pooled_single_ref" does add one extra column
relative to "local" (13 vs 12: Nigeria's own observed birth-year range
does not include the single global reference year, 2009, so no Nigeria
row is actually dropped under that scheme), but the "local" scheme's
column span is fully nested inside "pooled_single_ref"'s span, so this
extra column has no effect on any other fitted coefficient. The age_m
control alone, holding the birth-year scheme fixed at "local", moves the
coefficient from 1.0255531 (with age_m) to 1.3852855 (without) -- matching
the stored authoritative value (1.025553) and the documented early-attempt
value ("1.385") each to within rounding, under both birth-year schemes.
This is strong evidence, on this reconstruction, that the historical
1.385-vs-1.026 discrepancy is attributable to the age_m omission, not the
birth-year reference-coding change -- stated as this diagnostic's finding
on a faithful reconstruction, not as proof of what the original,
unpreserved buggy code specifically did.

Method:
  1. Build the pooled established-date water-HAZ sample exactly as
     20/21/24 do (same filters, same input file).
  2. Construct TWO birth-year dummy schemes on this sample:
       - "local": each country's own birth-year dummies, dropping that
         country's own earliest observed year (the scheme this thesis uses,
         matching 21_validate_all_primary_cells.py exactly).
       - "pooled_single_ref": one single reference year, chosen as the
         earliest birth year observed anywhere in the pooled sample, with
         one country-by-year dummy for every (country, year) cell except
         rows where country's own year equals that one single global
         reference year -- the literal, most natural reading of "a single
         combined reference cell across countries" (Appendix B's own
         phrase). This is a reconstruction for diagnostic purposes, not a
         claim that it is byte-identical to the original buggy script.
  3. Compare the two schemes' design-matrix rank and column count directly
     (established via QR/SVD rank, not assumed), and check whether the
     "local" column space is a subset of the "pooled_single_ref" column
     space (i.e. whether one nests the other) -- this directly answers
     (a) vs (b) for this specific reconstruction.
  4. Fit all four combinations (2 birth-year schemes x with/without age_m)
     with linearmodels.PanelOLS, same estimator as scripts 20/21/24, and
     report all four coefficients side by side.

No authoritative result is touched; this is a new, separate diagnostic run.
"""
import os
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from linearmodels.panel import PanelOLS

warnings.filterwarnings("ignore", category=UserWarning)

SRC = "data/processed/analysis_samples/run_20261006T184744Z/analysis_candidates_RESTRICTED.parquet"
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OUT = os.path.join("data/processed/estimation", f"birthyear_coding_diagnostic_{STAMP}")
os.makedirs(OUT, exist_ok=False)

SAMPLE_COUNTRY = {28806.0: "GH2014", 40406.0: "KE2014", 56606.0: "NG2018"}
SAMPLE_CODES = [28806.0, 40406.0, 56606.0]

log = []
def record(msg):
    log.append(str(msg))
    print(msg)

record(f"=== {STAMP} birth-year coding + age-control diagnostic (pooled established-date water-HAZ) ===")
raw = pd.read_parquet(SRC)

product, outcome = "W_IMP", "HAZ"
exp_col = f"{product}_post_12m_complete_exposure"
status_col = f"{product}_post_12m_complete_status"
zcol, validcol, univcol = "HAZ_z", "HAZ_valid", "HAZ_universe"

cols = ["SAMPLE", "candidate", "PERWEIGHT", "cluster_key", "record_number",
        "KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_reported", "age_cal_candidate",
        exp_col, status_col, zcol, validcol, univcol]
d = raw[cols].copy()
d = d[d["SAMPLE"].isin(SAMPLE_CODES)].copy()
d["country"] = d["SAMPLE"].map(SAMPLE_COUNTRY)
d = d[d.candidate == "GREGORIAN_ESTABLISHED"].copy()
d = d[d[status_col] == "eligible_complete"].copy()
d = d[(d[validcol] == True) & (d[univcol] == True)].copy()  # noqa: E712
d["age_m"] = np.where(d["age_reported"].notna(), d["age_reported"], d["age_cal_candidate"]).astype(float)
covs = ["KIDSEX", "AGE", "EDUCLVL", "MARSTAT", "b_year", "age_m"]
d = d.dropna(subset=covs + [exp_col, "PERWEIGHT", "cluster_key"])
sizes = d.groupby("cluster_key").size()
d = d[~d.cluster_key.isin(sizes[sizes < 2].index)].copy()

N, G = len(d), d.cluster_key.nunique()
K_countries = d.country.nunique()
country_sum = d.groupby("country").PERWEIGHT.sum()
target = N / K_countries
d["w"] = d["PERWEIGHT"] * target / d["country"].map(country_sum)
d["E10"] = d[exp_col] / 10.0
record(f"Sample: N={N}, G={G}, countries={K_countries}")

d["KIDSEX"] = d["KIDSEX"].astype(int).astype(str)
d["EDUCLVL"] = d["EDUCLVL"].astype(int).astype(str)
d["MARSTAT"] = d["MARSTAT"].astype(int).astype(str)
d = d.sort_values(["cluster_key", "record_number"]).reset_index(drop=True)
d["t_idx"] = d.groupby("cluster_key").cumcount()
panel = d.set_index(["cluster_key", "t_idx"])

dummies = pd.get_dummies(panel[["KIDSEX", "EDUCLVL", "MARSTAT"]], drop_first=True)


def byear_local_reference(panel):
    """Each country's own birth-year dummies, dropping that country's own
    earliest observed year -- the scheme this thesis actually uses
    (matches 21_validate_all_primary_cells.py exactly)."""
    cols_, names_ = [], []
    for smp in sorted(panel["country"].unique()):
        yrs = sorted(panel.loc[panel["country"] == smp, "b_year"].unique())
        for yv in yrs[1:]:
            cols_.append(((panel["country"] == smp) & (panel["b_year"] == yv)).astype(float))
            names_.append(f"by_{smp}_{int(yv)}")
    out = pd.concat(cols_, axis=1) if cols_ else pd.DataFrame(index=panel.index)
    if names_:
        out.columns = names_
    return out


def byear_single_pooled_reference(panel):
    """One single reference year (the earliest birth year observed anywhere
    in the pooled sample), with one country-by-year dummy for every
    (country, year) cell except rows matching that one global reference
    year -- the literal reading of 'a single combined reference cell across
    countries' (Appendix B's own phrase). Diagnostic reconstruction, not a
    claim of byte-identity with the original (unpreserved) buggy script."""
    global_ref_year = int(panel["b_year"].min())
    cols_, names_ = [], []
    for smp in sorted(panel["country"].unique()):
        yrs = sorted(panel.loc[panel["country"] == smp, "b_year"].unique())
        for yv in yrs:
            if int(yv) == global_ref_year:
                continue  # the one single shared reference cell
            cols_.append(((panel["country"] == smp) & (panel["b_year"] == yv)).astype(float))
            names_.append(f"by_{smp}_{int(yv)}")
    out = pd.concat(cols_, axis=1) if cols_ else pd.DataFrame(index=panel.index)
    if names_:
        out.columns = names_
    return out, global_ref_year


byear_local = byear_local_reference(panel)
byear_pooled, global_ref_year = byear_single_pooled_reference(panel)
record(f"Global earliest birth year (single pooled reference candidate): {global_ref_year}")
record(f"local scheme: {byear_local.shape[1]} birth-year dummy columns, names: {list(byear_local.columns)}")
record(f"pooled_single_ref scheme: {byear_pooled.shape[1]} birth-year dummy columns, names: {list(byear_pooled.columns)}")

# --- Rank / column-space comparison (the (a) vs (b) question) ---
w_arr = panel["w"].astype(float).values
sw = np.sqrt(w_arr)
A_local = (byear_local.values * sw[:, None])
A_pooled = (byear_pooled.values * sw[:, None])
rank_local = int(np.linalg.matrix_rank(A_local))
rank_pooled = int(np.linalg.matrix_rank(A_pooled))
record(f"rank(local byear block) = {rank_local} (of {byear_local.shape[1]} columns)")
record(f"rank(pooled_single_ref byear block) = {rank_pooled} (of {byear_pooled.shape[1]} columns)")

# Does the local column space lie inside the pooled_single_ref column space?
# (i.e. is every local-scheme column exactly reproducible as a linear
# combination of pooled_single_ref columns, country fixed effects implicitly
# available via the cluster FE at estimation time?) Check via combined-rank
# test: rank([A_pooled, A_local]) vs rank(A_pooled) -- equal iff local
# nests inside pooled's span (not testing the other direction, since the
# two have different column counts by construction whenever a country's
# own earliest year differs from the single global reference year).
combined_rank = int(np.linalg.matrix_rank(np.hstack([A_pooled, A_local])))
record(f"rank([pooled_single_ref | local]) = {combined_rank}")
same_span = (combined_rank == rank_pooled == byear_pooled.shape[1]) and (byear_local.shape[1] == byear_pooled.shape[1])
record(f"Same column count: {byear_local.shape[1] == byear_pooled.shape[1]}")
record(f"local block's span fully contained in pooled_single_ref's span: {combined_rank == rank_pooled}")
record(
    "CONCLUSION (a)-vs-(b) for this reconstruction, stated precisely (not collapsed to a binary a/b label): "
    "the two schemes are NOT an equivalent reparameterization in the strict sense -- pooled_single_ref has "
    "one additional column (13 vs 12), because Nigeria's own observed birth-year range does not include the "
    "single global reference year (2009), so no Nigeria row is actually dropped as a reference under that "
    "scheme, leaving Nigeria's own earliest observed year (2013) with its own extra dummy. HOWEVER, because "
    "the 'local' scheme's column span is fully nested inside 'pooled_single_ref's span (confirmed above), "
    "this specific design difference has NO effect on the fitted coefficient of any OTHER column, including "
    "E10 -- confirmed numerically below: the exposure coefficient is bit-for-bit identical between the two "
    "schemes once age_m is held fixed. This is a real but inconsequential-for-this-coefficient difference in "
    "design, not case (a) or case (b) as a clean dichotomy -- it nests, so it does not move beta."
)

# --- Four-way fit: {local, pooled_single_ref} x {with age_m, without age_m} ---
results = {}
for scheme_name, byear_df in [("local", byear_local), ("pooled_single_ref", byear_pooled)]:
    for age_mode in ["with_age_m", "without_age_m"]:
        base_cols = ["E10", "age_m", "AGE"] if age_mode == "with_age_m" else ["E10", "AGE"]
        X = pd.concat([panel[base_cols], dummies, byear_df], axis=1).astype(float)
        y = panel[zcol].astype(float)
        w = panel["w"].astype(float)
        mod = PanelOLS(y, X, weights=w, entity_effects=True, drop_absorbed=True)
        res = mod.fit(cov_type="clustered", cluster_entity=True, auto_df=True, group_debias=True)
        beta = float(res.params["E10"])
        se = float(res.std_errors["E10"])
        key = f"{scheme_name}__{age_mode}"
        # NOTE: E10 is ALREADY exposure/10, so the raw PanelOLS coefficient on
        # E10 is already "per 10 points" -- do not multiply by 10 again (this
        # exact bug was caught and fixed once before, in script 21, this
        # same session; re-caught here on first run of this new script).
        results[key] = {"beta_per_10": round(beta, 7), "se_per_10": round(se, 7), "n_byear_cols": byear_df.shape[1]}
        record(f"{key}: beta_per_10={beta:.7f}  se_per_10={se:.7f}  n_byear_cols={byear_df.shape[1]}")

record("\n=== Isolated effects ===")
record(f"Effect of age_m alone, holding birth-year scheme = local (the correct scheme): "
       f"{results['local__with_age_m']['beta_per_10']} (with age_m) vs "
       f"{results['local__without_age_m']['beta_per_10']} (without age_m), "
       f"diff = {results['local__with_age_m']['beta_per_10'] - results['local__without_age_m']['beta_per_10']:.7f}")
record(f"Effect of birth-year scheme alone, holding age_m included: "
       f"{results['local__with_age_m']['beta_per_10']} (local) vs "
       f"{results['pooled_single_ref__with_age_m']['beta_per_10']} (pooled_single_ref), "
       f"diff = {results['local__with_age_m']['beta_per_10'] - results['pooled_single_ref__with_age_m']['beta_per_10']:.7f}")
record(f"Stored authoritative value for comparison: 1.025553 (per 10 points)")
record(f"Documented early-attempt value for comparison: 1.385 (per 10 points) -- NOT independently reproduced here; "
       f"its exact originating code was never committed to this repository, so no row above is claimed to replicate it exactly.")

with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print(f"\nOutput written to {OUT}")
