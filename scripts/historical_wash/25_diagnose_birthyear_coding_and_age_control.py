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

RESULT (2026-10-09, second pass, run recorded in
data/processed/estimation/birthyear_coding_diagnostic_20261009T080355Z/):
the two birth-year schemes' RAW surviving column counts differ after
demeaning (local: 12; pooled_single_ref: 13), but after residualizing each
scheme's demeaned birth-year block against the demeaned E10/age_m/AGE/
dummy columns, BOTH residualized subspaces have rank 12, and so does their
combination -- the transformed, residualized spaces are EQUAL (not merely
nested). By Frisch-Waugh-Lovell, this is a sufficient condition for E10's
coefficient to be mathematically identical between the two schemes, and the
fitted results confirm it at floating-point precision: with age_m,
1.0255530672006674 (local) vs. 1.0255530672006667 (pooled_single_ref),
absolute difference 6.661338147750939e-16 -- machine epsilon, not an
approximation. Without age_m, 1.3852855197991372 vs. 1.3852855197991374,
absolute difference 2.220446049250313e-16. The age_m control alone, holding
the birth-year scheme fixed, moves the coefficient from 1.0255530672006674
(with) to 1.3852855197991372 (without) -- the stored authoritative value
is 1.025553 and the documented early-attempt value is approximately 1.385;
this diagnostic's without-age_m result approximately reproduces that
documented discrepancy on this reconstruction, which is evidence the age_m
omission explains it, not a claim of exact recovery of the original,
unpreserved code's output.

CORRECTION (2026-10-09, second pass): the first version of this script
compared the two birth-year schemes' RAW column spaces and found that the
"local" scheme's raw span nests inside "pooled_single_ref"'s raw span, then
concluded this alone explains why the fitted E10 coefficient was unchanged
("it nests, so it does not move beta"). That inference is invalid in
general: PanelOLS does not fit on the raw design matrix, it fits on the
WEIGHTED WITHIN-CLUSTER DEMEANED matrix (the entity-effects transformation),
and raw-space nesting does not imply transformed-space equality -- an
additional column that survives demeaning and is correlated with E10's own
within-cluster residual CAN change beta, nesting or not. The first version
also reported coefficients rounded to 7 decimals and called agreement at
that precision "bit-for-bit identical," which overstates what was actually
shown. Both errors are corrected in this version: the comparison is now
performed on the weighted within-cluster DEMEANED design matrices (the
actual object the estimator uses), with the demeaning implemented
independently here (not re-using 16_estimate_preliminary.py's wdemean(),
though following the identical, standard weighted-within-group-demeaning
definition), and coefficients are reported and compared at full float64
precision with explicit absolute differences, not rounded figures.

Method (revised):
  1. Build the pooled established-date water-HAZ sample exactly as
     20/21/24 do (same filters, same input file).
  2. Construct TWO birth-year dummy schemes (unchanged from the first
     version): "local" (country-local reference year, matching
     21_validate_all_primary_cells.py) and "pooled_single_ref" (one single
     global reference year, the literal reading of Appendix B's "a single
     combined reference cell across countries").
  3. Apply the SAME weighted within-cluster-demeaning transformation
     PanelOLS's entity_effects uses to: the shared non-birth-year columns
     (E10, age_m, AGE, demographic dummies) once, and each birth-year
     scheme's raw block separately. Drop demeaned birth-year columns whose
     post-demeaning norm is numerically zero ("absorbed" by the cluster FE
     -- the same criterion 16_estimate_preliminary.py itself uses, and the
     same phenomenon linearmodels' own AbsorbingEffectWarning flags).
  4. The question that actually determines whether E10's coefficient MUST
     be identical between schemes (by the Frisch-Waugh-Lovell theorem, not
     by nesting alone): after demeaning, residualize each scheme's
     surviving birth-year columns against the shared non-birth-year
     columns (E10, age_m, AGE, dummies) and compare the RESIDUALIZED
     subspaces' ranks (own rank, and combined rank with the other scheme).
     Equal residualized ranks (both nesting directions hold) means the two
     schemes contribute identical "net new information" to the model after
     the fixed effect and other controls are accounted for -- this, not
     raw-space nesting, is what provably forces every other coefficient,
     including E10, to be identical between schemes. Unequal ranks mean no
     such guarantee exists, and any observed agreement in the actual fitted
     coefficients would need to be reported as an empirical finding in this
     specific sample, not a algebraic certainty.
  5. Fit all four combinations (2 birth-year schemes x with/without age_m)
     with linearmodels.PanelOLS, same estimator as scripts 20/21/24, and
     report full float64-precision coefficients and explicit absolute
     differences, not rounded figures.

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

# --- Weighted within-cluster demeaning, applied to the design, not the raw blocks ---
# Same definition 16_estimate_preliminary.py uses (bincount-based weighted
# group demeaning), implemented independently here for this diagnostic.
RANK_TOL = 1e-8          # relative singular-value tolerance for np.linalg.matrix_rank
ABSORB_TOL = 1e-10       # post-demeaning column-norm tolerance for "absorbed"

codes, uniq = pd.factorize(panel.index.get_level_values("cluster_key"))
W = panel["w"].astype(float).values
sw_group = np.bincount(codes, weights=W)

def wdemean(V):
    out_ = np.empty_like(V, dtype=float)
    for j in range(V.shape[1]):
        num = np.bincount(codes, weights=W * V[:, j])
        out_[:, j] = V[:, j] - (num / sw_group)[codes]
    return out_

def drop_absorbed(Xt, names, W_):
    """Same criterion 16_estimate_preliminary.py uses: weighted column norm
    after demeaning must exceed ABSORB_TOL, else the column is collinear
    with the absorbed cluster fixed effect (no within-cluster variation)."""
    scale = np.sqrt(np.sum(W_[:, None] * Xt ** 2, axis=0))
    keep = scale > ABSORB_TOL
    dropped = [n for n, k in zip(names, keep) if not k]
    return Xt[:, keep], [n for n, k in zip(names, keep) if k], dropped

other_raw = panel[["E10", "age_m", "AGE"]].astype(float).values
other_raw = np.hstack([other_raw, dummies.values.astype(float)])
other_names = ["E10", "age_m", "AGE"] + list(dummies.columns)
other_t = wdemean(other_raw)
other_t, other_names_kept, other_dropped = drop_absorbed(other_t, other_names, W)
record(f"Shared non-birth-year columns after demeaning: kept {other_names_kept}, absorbed/dropped {other_dropped}")

local_t_raw = wdemean(byear_local.values.astype(float))
local_t, local_names_kept, local_dropped = drop_absorbed(local_t_raw, list(byear_local.columns), W)
pooled_t_raw = wdemean(byear_pooled.values.astype(float))
pooled_t, pooled_names_kept, pooled_dropped = drop_absorbed(pooled_t_raw, list(byear_pooled.columns), W)
record(f"local scheme, post-demeaning: {len(local_names_kept)} surviving columns (raw {byear_local.shape[1]}); "
       f"absorbed: {local_dropped}")
record(f"pooled_single_ref scheme, post-demeaning: {len(pooled_names_kept)} surviving columns (raw {byear_pooled.shape[1]}); "
       f"absorbed: {pooled_dropped}")

# Residualize each scheme's surviving, demeaned birth-year columns against
# the shared, demeaned non-birth-year columns (weighted OLS residuals) --
# this isolates the "net new information" each scheme's birth-year block
# contributes beyond what E10/age_m/AGE/dummies + the cluster FE already
# explain. By the Frisch-Waugh-Lovell theorem, E10's coefficient (and every
# other non-birth-year coefficient) is mathematically GUARANTEED identical
# between the two schemes if and only if these residualized subspaces are
# EQUAL (not merely one nested in the other).
sw_row = np.sqrt(W)

def wls_residualize(target, regressors, w_sqrt):
    """Weighted-OLS residuals of `target` columns on `regressors`."""
    Xw = regressors * w_sqrt[:, None]
    Yw = target * w_sqrt[:, None]
    coef, *_ = np.linalg.lstsq(Xw, Yw, rcond=None)
    fitted = regressors @ coef
    return target - fitted

local_resid = wls_residualize(local_t, other_t, sw_row)
pooled_resid = wls_residualize(pooled_t, other_t, sw_row)

A_local_r = local_resid * sw_row[:, None]
A_pooled_r = pooled_resid * sw_row[:, None]
rank_local_r = int(np.linalg.matrix_rank(A_local_r, tol=RANK_TOL * np.linalg.norm(A_local_r, 2) if A_local_r.size else None))
rank_pooled_r = int(np.linalg.matrix_rank(A_pooled_r, tol=RANK_TOL * np.linalg.norm(A_pooled_r, 2) if A_pooled_r.size else None))
combined_r = np.hstack([A_pooled_r, A_local_r])
rank_combined_r = int(np.linalg.matrix_rank(combined_r, tol=RANK_TOL * np.linalg.norm(combined_r, 2) if combined_r.size else None))

record(f"\n=== Transformed (weighted within-cluster demeaned, then residualized against "
       f"E10/age_m/AGE/dummies) rank comparison, rank tolerance = {RANK_TOL} relative to the largest singular value ===")
record(f"rank(local, residualized) = {rank_local_r} (of {len(local_names_kept)} surviving raw columns)")
record(f"rank(pooled_single_ref, residualized) = {rank_pooled_r} (of {len(pooled_names_kept)} surviving raw columns)")
record(f"rank(combined [pooled_single_ref | local], residualized) = {rank_combined_r}")

equal_span = (rank_local_r == rank_pooled_r == rank_combined_r)
record(f"Raw column counts: local={byear_local.shape[1]}, pooled_single_ref={byear_pooled.shape[1]} (NOT required to be equal for equal transformed spans)")
record(f"Transformed, residualized column spaces EQUAL: {equal_span}")
if equal_span:
    record(
        "CONCLUSION: the transformed (post-cluster-FE, post-residualization) subspaces are EQUAL "
        "(all three ranks match). By the Frisch-Waugh-Lovell theorem, this is a sufficient condition for "
        "E10's coefficient -- and every other non-birth-year coefficient -- to be mathematically identical "
        "between the two birth-year schemes, not merely an empirical coincidence. The two schemes are "
        "equivalent controls once the cluster fixed effect and the other covariates are accounted for, "
        "despite having different raw column counts (one is not a mere relabelling of the other, but the "
        "two carry the same information after absorption)."
    )
else:
    record(
        "CONCLUSION: the transformed, residualized subspaces are NOT equal (at least one rank differs). "
        "There is therefore NO algebraic guarantee that E10's coefficient must be identical between the two "
        "birth-year schemes. If the fitted coefficients below nonetheless agree closely, that agreement is "
        "reported as an empirical observation in this specific sample, not as a consequence of the design "
        "comparison alone."
    )

# --- Four-way fit: {local, pooled_single_ref} x {with age_m, without age_m} ---
# Full float64 precision retained throughout -- no rounding before differencing.
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
        results[key] = {"beta_per_10": beta, "se_per_10": se, "n_byear_cols": byear_df.shape[1]}
        record(f"{key}: beta_per_10={beta!r}  se_per_10={se!r}  n_byear_cols={byear_df.shape[1]}")

record("\n=== Isolated effects, full precision, explicit absolute differences (not rounded before differencing) ===")
diff_age = results['local__with_age_m']['beta_per_10'] - results['local__without_age_m']['beta_per_10']
record(f"Effect of age_m alone, holding birth-year scheme = local: "
       f"{results['local__with_age_m']['beta_per_10']!r} (with age_m) vs "
       f"{results['local__without_age_m']['beta_per_10']!r} (without age_m), "
       f"diff = {diff_age!r}")
diff_scheme_with_age = results['local__with_age_m']['beta_per_10'] - results['pooled_single_ref__with_age_m']['beta_per_10']
record(f"Effect of birth-year scheme alone, holding age_m included: "
       f"{results['local__with_age_m']['beta_per_10']!r} (local) vs "
       f"{results['pooled_single_ref__with_age_m']['beta_per_10']!r} (pooled_single_ref), "
       f"abs diff = {abs(diff_scheme_with_age)!r}")
diff_scheme_without_age = results['local__without_age_m']['beta_per_10'] - results['pooled_single_ref__without_age_m']['beta_per_10']
record(f"Effect of birth-year scheme alone, holding age_m excluded: "
       f"{results['local__without_age_m']['beta_per_10']!r} (local) vs "
       f"{results['pooled_single_ref__without_age_m']['beta_per_10']!r} (pooled_single_ref), "
       f"abs diff = {abs(diff_scheme_without_age)!r}")
record(f"Stored authoritative value for comparison: 1.025553 (per 10 points, as published in the manuscript/appendix; "
       f"full-precision stored value: see model_results_RESTRICTED_coefficients.csv)")
record(f"Documented early-attempt value for comparison: approximately 1.385 (per 10 points) -- this diagnostic's "
       f"without-age_m results are offered as evidence that omitting age_m approximately reproduces the documented "
       f"early-attempt discrepancy in this reconstruction; this is NOT a claim of exact recovery of the original, "
       f"unpreserved historical script's output, which cannot be independently verified.")

with open(os.path.join(OUT, "execution_log.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print(f"\nOutput written to {OUT}")
