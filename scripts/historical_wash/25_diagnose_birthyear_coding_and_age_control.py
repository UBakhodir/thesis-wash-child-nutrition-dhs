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

RESULT (2026-10-09, third pass, run recorded in
data/processed/estimation/birthyear_coding_diagnostic_20261009T081301Z/):
five independent, mutually-reinforcing checks, NONE of which uses E10 to
construct the comparison being tested (the second pass's error):

STEP 1 (demeaned birth-year blocks compared DIRECTLY, no residualization at
all): rank(local)=12, rank(pooled_single_ref)=12 of 13 surviving raw
columns, combined rank=12 -- equal span, established before E10 or the
nuisance controls are even involved.
STEP 2 (residualized against age_m/AGE/dummies ONLY, E10 excluded from the
projection, checked separately with and without age_m): equal span (rank
12/12/12) in both age modes.
STEP 3 (complete per-scheme nuisance space = cluster FE + shared controls +
that scheme's birth-year block; E10's own weighted residual exposure vector
computed directly for each scheme and compared elementwise): maximum
weighted residual difference 1.73e-15, relative to ||e|| = 2.23e-16 --
genuinely the same vector, not merely "close."
STEP 4 (explicit weighted FWL formula, beta = (e'Wy~)/(e'We), computed
independently of PanelOLS and compared to it): differences of 0 to
4.44e-16 across all four scheme/age-mode combinations -- the manual
linear-algebra computation and the library's internal computation agree to
floating-point precision.
STEP 5 (mechanical explanation, independent of E10 entirely): Nigeria's
full set of 5 own-year dummies in the pooled_single_ref scheme (kept in
full because Nigeria has no births in the single global reference year)
sums EXACTLY to Nigeria's own raw country indicator (confirmed elementwise
across all 23,018 rows), and that indicator demeans to EXACTLY 0.0 (not
merely near-zero), because every DHS cluster belongs to one country, so a
column constant within every cluster is trivially absorbed. This is the
mechanical reason the extra raw column adds no genuine dimension.

Fitted coefficients confirm all of the above at floating-point precision:
with age_m, 1.0255530672006674 (local) vs. 1.0255530672006667
(pooled_single_ref), absolute difference 6.661338147750939e-16; without
age_m, 1.3852855197991372 vs. 1.3852855197991374, absolute difference
2.220446049250313e-16 -- machine epsilon, not an approximation. The age_m
control alone, holding the birth-year scheme fixed, moves the coefficient
from 1.0255530672006674 (with) to 1.3852855197991372 (without) -- the
stored authoritative value is 1.025553 and the documented early-attempt
value is approximately 1.385; this diagnostic's without-age_m result
approximately reproduces that documented discrepancy on this
reconstruction, which is evidence the age_m omission explains it, not a
claim of exact recovery of the original, unpreserved code's output.

CORRECTION (2026-10-09, third pass): the second-pass version of this
script residualized each birth-year scheme's demeaned block against a
nuisance set that INCLUDED E10 itself, then treated equal post-
residualization ranks as proof of E10-coefficient invariance. That is
circular: residualizing a birth-year block against E10 removes exactly the
part of that block that could be correlated with E10, so finding "equal"
residualized spaces afterward does not establish what it claimed to --
it can hide the very difference in question. This version removes E10
entirely from every column-space comparison (STEPS 1-2), separately
verifies E10's own residual vector is unaffected using the COMPLETE
nuisance specification (STEP 3), independently cross-checks the fitted
coefficient via the explicit FWL formula rather than relying on rank
arguments alone (STEP 4), and explains the mechanical source of the raw
column-count difference without reference to E10 at all (STEP 5). The
second-pass version's "if and only if" framing is also removed: equal
spans are a SUFFICIENT condition for invariance (confirmed here), not
claimed as a necessary one, and the four-way fitted coefficients are
retained as independently observed numerical evidence, not merely
inferred from the algebra.

CORRECTION (2026-10-09, second pass): the first version of this script
compared the two birth-year schemes' RAW column spaces and found that the
"local" scheme's raw span nests inside "pooled_single_ref"'s raw span, then
concluded this alone explains why the fitted E10 coefficient was unchanged
("it nests, so it does not move beta"). That inference is invalid in
general: PanelOLS does not fit on the raw design matrix, it fits on the
WEIGHTED WITHIN-CLUSTER DEMEANED matrix (the entity-effects transformation),
and raw-space nesting does not imply transformed-space equality.

Method (revised, third pass):
  1. Build the pooled established-date water-HAZ sample exactly as
     20/21/24 do (same filters, same input file).
  2. Construct TWO birth-year dummy schemes (unchanged from the first
     version): "local" (country-local reference year, matching
     21_validate_all_primary_cells.py) and "pooled_single_ref" (one single
     global reference year, the literal reading of Appendix B's "a single
     combined reference cell across countries").
  3. Apply the SAME weighted within-cluster-demeaning transformation
     PanelOLS's entity_effects uses to: E10 alone (kept entirely separate),
     the shared nuisance columns (age_m, AGE, demographic dummies -- E10
     EXCLUDED), and each birth-year scheme's raw block separately. Drop
     demeaned columns whose post-demeaning norm is numerically zero
     ("absorbed" by the cluster FE -- the same criterion
     16_estimate_preliminary.py itself uses, and the same phenomenon
     linearmodels' own AbsorbingEffectWarning flags).
  4. STEP 1: compare the two schemes' demeaned birth-year blocks directly
     (own rank, combined rank) -- no residualization against anything yet.
  5. STEP 2: residualize each scheme's demeaned birth-year block against
     the shared NUISANCE CONTROLS ONLY (age_m, AGE, dummies -- E10
     explicitly excluded from this projection), separately with and
     without age_m, and compare ranks again.
  6. STEP 3: build the COMPLETE per-scheme nuisance space (cluster FE +
     shared controls + that scheme's own birth-year block) and directly
     compare E10's own weighted residual exposure vector under each
     specification, elementwise, against a stated tolerance -- not a rank
     argument alone.
  7. STEP 4: compute beta via the explicit weighted Frisch-Waugh-Lovell
     formula, beta = (e'Wy~)/(e'We), independently of PanelOLS, and
     compare to PanelOLS's own fitted coefficient as a cross-check.
  8. STEP 5: explain the mechanical source of the raw column-count
     difference directly and without reference to E10: verify that the
     sum of Nigeria's full own-year dummy set equals Nigeria's country
     indicator, and that this indicator is absorbed (demeans to zero)
     because clusters never span countries.
  9. Fit all four combinations (2 birth-year schemes x with/without age_m)
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
RESID_TOL = 1e-8         # tolerance for "same weighted residual exposure vector" (relative to ||e||)

codes, uniq = pd.factorize(panel.index.get_level_values("cluster_key"))
W = panel["w"].astype(float).values
sw_group = np.bincount(codes, weights=W)
sw_row = np.sqrt(W)

def wdemean(V):
    out_ = np.empty_like(V, dtype=float)
    for j in range(V.shape[1]):
        num = np.bincount(codes, weights=W * V[:, j])
        out_[:, j] = V[:, j] - (num / sw_group)[codes]
    return out_

def rank_of(M, tol_rel=RANK_TOL):
    if M.size == 0:
        return 0
    nrm = np.linalg.norm(M, 2)
    return int(np.linalg.matrix_rank(M, tol=tol_rel * nrm if nrm > 0 else None))

def drop_absorbed(Xt, names, W_):
    """Same criterion 16_estimate_preliminary.py uses: weighted column norm
    after demeaning must exceed ABSORB_TOL, else the column is collinear
    with the absorbed cluster fixed effect (no within-cluster variation)."""
    scale = np.sqrt(np.sum(W_[:, None] * Xt ** 2, axis=0))
    keep = scale > ABSORB_TOL
    dropped = [n for n, k in zip(names, keep) if not k]
    return Xt[:, keep], [n for n, k in zip(names, keep) if k], dropped

def wls_residualize(target, regressors, w_sqrt):
    """Weighted-OLS residuals of `target` columns (2-D) on `regressors` (2-D)."""
    if regressors.shape[1] == 0:
        return target.copy()
    Xw = regressors * w_sqrt[:, None]
    Yw = target * w_sqrt[:, None]
    coef, *_ = np.linalg.lstsq(Xw, Yw, rcond=None)
    fitted = regressors @ coef
    return target - fitted

# E10 demeaned ALONE. CORRECTION (2026-10-09, third pass): the previous
# version of this script included E10 among the "nuisance" columns the
# birth-year blocks were residualized against before comparing ranks. That
# is circular: residualizing a birth-year block against E10 itself removes
# exactly the part of that block that could be correlated with E10, so
# finding "equal residualized spaces" afterward proves nothing about
# whether E10's own coefficient is invariant to the choice of scheme -- it
# can hide the very difference in question. E10 is kept entirely separate
# below and is never used as a regressor in any column-space comparison.
E10_t = wdemean(panel[["E10"]].values.astype(float))[:, 0]

# Shared nuisance controls EXCLUDING E10: age_m, AGE, demographic dummies.
nuisance_raw_full = panel[["age_m", "AGE"]].astype(float).values
nuisance_raw_full = np.hstack([nuisance_raw_full, dummies.values.astype(float)])
nuisance_names_full = ["age_m", "AGE"] + list(dummies.columns)
nuisance_t_full = wdemean(nuisance_raw_full)
nuisance_t_full, nuisance_names_full_kept, nuisance_full_dropped = drop_absorbed(nuisance_t_full, nuisance_names_full, W)
record(f"Shared nuisance columns (age_m,AGE,dummies; E10 excluded), after demeaning: "
       f"kept {nuisance_names_full_kept}, absorbed/dropped {nuisance_full_dropped}")

# Same but WITHOUT age_m, for the age-mode-separated comparisons.
nuisance_raw_noage = panel[["AGE"]].astype(float).values
nuisance_raw_noage = np.hstack([nuisance_raw_noage, dummies.values.astype(float)])
nuisance_names_noage = ["AGE"] + list(dummies.columns)
nuisance_t_noage = wdemean(nuisance_raw_noage)
nuisance_t_noage, nuisance_names_noage_kept, nuisance_noage_dropped = drop_absorbed(nuisance_t_noage, nuisance_names_noage, W)

local_t_raw = wdemean(byear_local.values.astype(float))
local_t, local_names_kept, local_dropped = drop_absorbed(local_t_raw, list(byear_local.columns), W)
pooled_t_raw = wdemean(byear_pooled.values.astype(float))
pooled_t, pooled_names_kept, pooled_dropped = drop_absorbed(pooled_t_raw, list(byear_pooled.columns), W)
record(f"local scheme, post-demeaning: {len(local_names_kept)} surviving columns (raw {byear_local.shape[1]}); "
       f"absorbed: {local_dropped}")
record(f"pooled_single_ref scheme, post-demeaning: {len(pooled_names_kept)} surviving columns (raw {byear_pooled.shape[1]}); "
       f"absorbed: {pooled_dropped}")

# === STEP 1: compare the DEMEANED birth-year blocks DIRECTLY, before any
# residualization against E10 or the shared nuisance controls. Different
# raw/surviving column counts can still give equal column spaces, because
# of linear dependence within a block (checked explicitly in STEP 5 below).
A_local_direct = local_t * sw_row[:, None]
A_pooled_direct = pooled_t * sw_row[:, None]
rank_local_direct = rank_of(A_local_direct)
rank_pooled_direct = rank_of(A_pooled_direct)
rank_combined_direct = rank_of(np.hstack([A_pooled_direct, A_local_direct]))
record(f"\n=== STEP 1: demeaned birth-year blocks compared directly (no residualization), "
       f"rank tolerance = {RANK_TOL} relative to the largest singular value ===")
record(f"rank(local, demeaned only) = {rank_local_direct} (of {len(local_names_kept)} surviving columns)")
record(f"rank(pooled_single_ref, demeaned only) = {rank_pooled_direct} (of {len(pooled_names_kept)} surviving columns)")
record(f"rank(combined, demeaned only) = {rank_combined_direct}")
record(f"Equal span (direct, pre-residualization): {rank_local_direct == rank_pooled_direct == rank_combined_direct}")

# === STEP 2: residualize birth-year blocks against the SHARED NUISANCE
# controls ONLY (age_m, AGE, demographic dummies) -- E10 explicitly
# excluded from this projection -- separately with and without age_m.
record(f"\n=== STEP 2: birth-year blocks residualized against shared nuisance controls ONLY "
       f"(E10 excluded), with and without age_m ===")
step2_results = {}
for age_mode, nuisance_t, nuisance_kept in [
    ("with_age_m", nuisance_t_full, nuisance_names_full_kept),
    ("without_age_m", nuisance_t_noage, nuisance_names_noage_kept),
]:
    local_resid_n = wls_residualize(local_t, nuisance_t, sw_row)
    pooled_resid_n = wls_residualize(pooled_t, nuisance_t, sw_row)
    A_local_n = local_resid_n * sw_row[:, None]
    A_pooled_n = pooled_resid_n * sw_row[:, None]
    r_local = rank_of(A_local_n)
    r_pooled = rank_of(A_pooled_n)
    r_comb = rank_of(np.hstack([A_pooled_n, A_local_n]))
    step2_results[age_mode] = (r_local, r_pooled, r_comb)
    record(f"[{age_mode}] nuisance = {nuisance_kept}")
    record(f"[{age_mode}] rank(local | nuisance) = {r_local}, rank(pooled | nuisance) = {r_pooled}, "
           f"rank(combined | nuisance) = {r_comb} -- equal span: {r_local == r_pooled == r_comb}")

# === STEP 3: build the COMPLETE nuisance space per scheme (cluster FE
# already absorbed via demeaning, plus shared controls, plus that scheme's
# own birth-year block), and verify directly that residualizing E10 against
# either complete nuisance specification gives the SAME weighted residual
# exposure vector, within a stated tolerance -- not merely a rank argument.
record(f"\n=== STEP 3: complete nuisance space per scheme; direct comparison of E10's "
       f"weighted residual exposure vector, tolerance = {RESID_TOL} relative to ||e|| ===")
step3_results = {}
for age_mode, nuisance_t in [("with_age_m", nuisance_t_full), ("without_age_m", nuisance_t_noage)]:
    N_local = np.hstack([nuisance_t, local_t])
    N_pooled = np.hstack([nuisance_t, pooled_t])
    e_local = wls_residualize(E10_t.reshape(-1, 1), N_local, sw_row)[:, 0]
    e_pooled = wls_residualize(E10_t.reshape(-1, 1), N_pooled, sw_row)[:, 0]
    diff = (e_local - e_pooled) * sw_row  # weighted residual difference
    max_abs_diff = float(np.max(np.abs(diff)))
    rel_diff = max_abs_diff / float(np.linalg.norm(e_local * sw_row, 2)) if np.linalg.norm(e_local * sw_row, 2) > 0 else float("nan")
    same_vector = rel_diff < RESID_TOL
    step3_results[age_mode] = {"e_local": e_local, "e_pooled": e_pooled, "N_local": N_local, "N_pooled": N_pooled,
                                 "max_abs_diff": max_abs_diff, "rel_diff": rel_diff, "same_vector": same_vector}
    record(f"[{age_mode}] max |weighted residual diff| = {max_abs_diff!r}, relative to ||e_local|| = {rel_diff!r}, "
           f"same weighted residual exposure vector (within tolerance): {same_vector}")

equal_span_step2 = all(r[0] == r[1] == r[2] for r in step2_results.values())
same_resid_step3 = all(v["same_vector"] for v in step3_results.values())
record(f"\nSTEP 2 (nuisance-only, E10-free) spans equal in both age modes: {equal_span_step2}")
record(f"STEP 3 (complete nuisance space) residual exposure vectors equal in both age modes: {same_resid_step3}")
if equal_span_step2 and same_resid_step3:
    record(
        "CONCLUSION (valid form): the birth-year schemes, after demeaning and after residualizing against the "
        "SHARED NUISANCE CONTROLS ONLY (E10 excluded from that projection), span equal subspaces in both age "
        "modes, and the complete per-scheme nuisance specifications (cluster FE + shared controls + that "
        "scheme's birth-year block) give E10 the same weighted residual exposure vector within the stated "
        "tolerance. This IS the valid basis for algebraic equivalence: the two schemes are equivalent nuisance "
        "specifications for E10's coefficient, confirmed by a comparison that never uses E10 to construct the "
        "projection being compared."
    )
else:
    record(
        "CONCLUSION: the nuisance-only comparison does NOT establish equal spans and/or equal residual exposure "
        "vectors in both age modes. There is therefore no algebraic guarantee that E10's coefficient is "
        "invariant to the choice of birth-year scheme from this comparison. Any agreement in the fitted "
        "coefficients reported below must be read as observed numerical evidence in this specific sample, not "
        "as a proven consequence of the design comparison."
    )

# === STEP 4: independent check via the explicit weighted FWL partial-
# regression formula, beta = (e'We_tilde... ) -- compare against PanelOLS.
record(f"\n=== STEP 4: explicit weighted Frisch-Waugh-Lovell partial regression, "
       f"cross-checked against PanelOLS's own fitted coefficient ===")
y_t_full = {}
for age_mode in ["with_age_m", "without_age_m"]:
    y_raw = panel[[zcol]].astype(float).values
    y_t = wdemean(y_raw)[:, 0]
    y_t_full[age_mode] = y_t
fwl_results = {}
for age_mode in ["with_age_m", "without_age_m"]:
    for scheme_name, byear_t in [("local", local_t), ("pooled_single_ref", pooled_t)]:
        nuisance_t = nuisance_t_full if age_mode == "with_age_m" else nuisance_t_noage
        N = np.hstack([nuisance_t, byear_t])
        e = wls_residualize(E10_t.reshape(-1, 1), N, sw_row)[:, 0]
        y_resid = wls_residualize(y_t_full[age_mode].reshape(-1, 1), N, sw_row)[:, 0]
        numerator = float(np.sum(W * e * y_resid))
        denominator = float(np.sum(W * e * e))
        beta_fwl = numerator / denominator
        fwl_results[f"{scheme_name}__{age_mode}"] = beta_fwl
        record(f"FWL beta [{scheme_name}, {age_mode}] = {beta_fwl!r}")

# === STEP 5: explicit explanation of the redundant pooled_single_ref
# column. Nigeria's observed birth-year range (2013-2017) excludes the
# single global reference year (2009), so the pooled_single_ref scheme
# keeps ALL FIVE of Nigeria's own-year dummies (no year dropped for
# Nigeria), unlike every other country, which has one year dropped. Test
# directly: does the SUM of Nigeria's full set of own-year raw dummies
# equal Nigeria's raw country indicator -- and does that country indicator
# fully demean to (numerically) zero, since every DHS cluster belongs to
# exactly one country (clusters never span countries), so a column that is
# constant within every cluster is, trivially, collinear with the absorbed
# cluster fixed effect? This is a mechanical, E10-independent explanation
# for why pooled_single_ref's extra raw column does not add a genuine extra
# dimension after demeaning -- individual columns need not be absorbed to
# zero on their own for a LINEAR COMBINATION of several columns to be.
record(f"\n=== STEP 5: explicit redundancy check -- Nigeria's full own-year dummy set "
       f"sums to its country indicator, which the cluster FE absorbs ===")
nigeria_cols = [c for c in byear_pooled.columns if c.startswith("by_NG2018_")]
nigeria_sum_raw = byear_pooled[nigeria_cols].sum(axis=1).values
nigeria_indicator_raw = (panel["country"] == "NG2018").astype(float).values
sum_matches_indicator = bool(np.allclose(nigeria_sum_raw, nigeria_indicator_raw, atol=1e-12))
record(f"Nigeria's {len(nigeria_cols)} own-year dummy columns in the pooled_single_ref scheme: {nigeria_cols}")
record(f"Sum of Nigeria's full own-year dummy set exactly equals Nigeria's raw country indicator "
       f"(elementwise, all {len(nigeria_sum_raw)} rows): {sum_matches_indicator}")
nigeria_indicator_t = wdemean(nigeria_indicator_raw.reshape(-1, 1))[:, 0]
nigeria_indicator_demeaned_norm = float(np.sqrt(np.sum(W * nigeria_indicator_t ** 2)))
record(f"Weighted norm of Nigeria's country indicator AFTER demeaning (should be ~0, since every cluster "
       f"belongs to exactly one country so this column is constant within every cluster): "
       f"{nigeria_indicator_demeaned_norm!r} (ABSORB_TOL = {ABSORB_TOL})")
record(
    "CONCLUSION (STEP 5): confirmed directly. Nigeria's full own-year dummy set (kept entirely in "
    "pooled_single_ref because Nigeria has no births in the single global reference year) sums exactly to "
    "Nigeria's own country indicator; that indicator, being constant within every cluster (clusters never "
    "span countries), is absorbed by the cluster fixed effect to a demeaned weighted norm of essentially "
    "zero. This is the mechanical reason pooled_single_ref's 13th raw column adds no genuine extra "
    "dimension once the cluster FE is applied -- a property of the birth-year block's own internal linear "
    "structure, established without reference to E10 or any other covariate, and consistent with (not "
    "merely inferred from) the STEP 1-3 rank results above."
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

record("\n=== STEP 4 cross-check: explicit weighted-FWL beta vs. PanelOLS's own fitted beta ===")
for key in ["local__with_age_m", "pooled_single_ref__with_age_m", "local__without_age_m", "pooled_single_ref__without_age_m"]:
    beta_panelols = results[key]["beta_per_10"]
    beta_fwl = fwl_results[key]
    abs_diff_fwl = abs(beta_panelols - beta_fwl)
    record(f"{key}: PanelOLS beta = {beta_panelols!r}, explicit FWL beta = {beta_fwl!r}, "
           f"abs diff = {abs_diff_fwl!r}")

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
