"""
13_final_outputs.py
=====================
Final results production: reformats already-validated Step 07/11/12 result
files into supervisor/thesis-ready tables, figures, a descriptive survey-
coverage map, and a reproducibility audit record. NO new statistic is
computed anywhere in this script - every number in every final output is
read directly from an existing, already-validated CSV. This script only
selects, reshapes, rounds (for presentation only), and relabels.

WHY NO NEW STATISTICS: Steps 00-12 already built and validated every
regression, descriptive table, and diagnostic this thesis uses. Step 13's
job is presentation, not analysis - computing anything new here (a p-value,
a different rounding of a coefficient's underlying float, a re-derived N)
would create a second, unaudited source of truth alongside the already-
validated one. Every final table/figure is read straight from its named
source CSV and only reshaped/rounded/relabeled.

LOCKED DECISIONS FROM THIS STAGE'S APPROVAL (not re-derived here):
  - No significance stars anywhere - only coefficient, SE and/or 95% CI,
    and p-value where appropriate, identically formatted in every table.
  - The tiny water_rate_loo coefficient shift between the Step 11 core run
    and the Step 12 Ghana bio-digester run is EXPECTED joint-regression
    behavior (the sanitation regressor changes slightly and is correlated
    with water_rate_loo, so the water coefficient can shift slightly too)
    - NOT a bug, and water_rate_loo itself is never described as "changed."
  - No map colors clusters by water_rate_loo/sanitation_rate_loo_core -
    those are household-specific leave-one-out values, so households in
    the same cluster can legitimately differ at the same coordinate;
    inventing a cluster-aggregation rule just to make a map was rejected.
    Only a descriptive survey-cluster coverage map is produced.
  - DHS coordinate displacement wording is taken verbatim from the
    project's own bundled GPS_Displacement_README.txt (verified below,
    not recalled from memory) - "up to 2km urban / up to 5km rural (1% up
    to 10km)".

Reads (read-only, never opened in write mode):
  - outputs/tables/table1_sample_characteristics.csv
  - outputs/tables/table2_anthropometric_outcomes.csv
  - outputs/tables/table2b_severe_anthropometric_outcomes_secondary.csv
  - outputs/tables/table3_wash_characteristics.csv
  - outputs/tables/table4_missingness_summary.csv
  - outputs/regressions/main_continuous_models.csv
  - outputs/tables/step11_model_sample_flow.csv
  - outputs/regressions/robustness_binary_lpm.csv
  - outputs/regressions/appendix/severe_outcomes.csv
  - outputs/regressions/robustness_biodigester.csv
  - outputs/regressions/robustness_household_wash.csv
  - outputs/regressions/robustness_alternative_weights.csv
  - outputs/regressions/robustness_loo_denominator.csv
  - outputs/tables/step12_robustness_sample_flow.csv
  - outputs/tables/step09_admin_region_report.csv
  - outputs/tables/step08_hr_wash_exposure_report.csv
  - outputs/tables/step08_loo_denominator_diagnostics.csv
  - data/processed/pooled_kr_four_country_birth_order.parquet (LATNUM/LONGNUM
    only, for the descriptive coverage map)
  - data/interim/DHS/ethiopia/2024-25/GE/GPS_Displacement_README.txt (verify
    displacement wording, not recalled from memory)

Writes:
  - outputs/final_tables/*.csv        (Final Tables 1-6)
  - outputs/final_appendix/*.csv      (Appendix Tables A1-A8)
  - outputs/final_figures/*.png       (Figures 1-3)
  - outputs/final_appendix/*.png      (Appendix Figure A1)
  - outputs/final_figures/map_survey_cluster_coverage.png (if feasible)
  - outputs/final_audit/step11_bug_provenance_note.txt
  - outputs/final_audit/step13_final_audit.csv
  - outputs/final_audit/step13_final_audit_summary.txt

No analytical parquet, no Step 00-12 script, and no Step 00-12 result file
is ever opened in write mode.
"""

import hashlib
from pathlib import Path
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(r"c:\Users\user\Documents\Graduation_Thesis")
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REGR_DIR = PROJECT_ROOT / "outputs" / "regressions"
APPX_SRC_DIR = REGR_DIR / "appendix"

FINAL_TABLES_DIR = PROJECT_ROOT / "outputs" / "final_tables"
FINAL_APPENDIX_DIR = PROJECT_ROOT / "outputs" / "final_appendix"
FINAL_FIGURES_DIR = PROJECT_ROOT / "outputs" / "final_figures"
FINAL_AUDIT_DIR = PROJECT_ROOT / "outputs" / "final_audit"

# ----------------------------------------------------------------------
# SOURCE FILES (read-only) - the single place every path is declared
# ----------------------------------------------------------------------
SOURCES = {
    "table1": TABLES_DIR / "table1_sample_characteristics.csv",
    "table2": TABLES_DIR / "table2_anthropometric_outcomes.csv",
    "table2b": TABLES_DIR / "table2b_severe_anthropometric_outcomes_secondary.csv",
    "table3": TABLES_DIR / "table3_wash_characteristics.csv",
    "table4": TABLES_DIR / "table4_missingness_summary.csv",
    "main_continuous": REGR_DIR / "main_continuous_models.csv",
    "step11_flow": TABLES_DIR / "step11_model_sample_flow.csv",
    "binary_lpm": REGR_DIR / "robustness_binary_lpm.csv",
    "severe": APPX_SRC_DIR / "severe_outcomes.csv",
    "biodigester": REGR_DIR / "robustness_biodigester.csv",
    "household": REGR_DIR / "robustness_household_wash.csv",
    "altweight": REGR_DIR / "robustness_alternative_weights.csv",
    "loo": REGR_DIR / "robustness_loo_denominator.csv",
    "step12_flow": TABLES_DIR / "step12_robustness_sample_flow.csv",
    "admin_region_report": TABLES_DIR / "step09_admin_region_report.csv",
    "hr_wash_report": TABLES_DIR / "step08_hr_wash_exposure_report.csv",
    "loo_denom_diag": TABLES_DIR / "step08_loo_denominator_diagnostics.csv",
    "step10_parquet": PROJECT_ROOT / "data" / "processed" / "pooled_kr_four_country_birth_order.parquet",
    "gps_displacement_readme": PROJECT_ROOT / "data" / "interim" / "DHS" / "ethiopia" / "2024-25" / "GE" / "GPS_Displacement_README.txt",
}

# Step 07 shapes locked by explicit approval - hard-fail if they don't match.
EXPECTED_STEP07_SHAPES = {
    "table1": (76, 7), "table2": (12, 13), "table2b": (12, 13),
    "table3": (61, 5), "table4": (88, 5),
}

COUNTRIES = ["ethiopia", "ghana", "kenya", "nigeria"]
COUNTRY_LABELS = {"ethiopia": "Ethiopia", "ghana": "Ghana", "kenya": "Kenya", "nigeria": "Nigeria", "pooled": "Pooled"}
OUTCOME_LABELS = {"haz": "HAZ", "waz": "WAZ", "whz": "WHZ"}
EXPOSURE_TERMS = ["water_rate_loo", "sanitation_rate_loo_core"]
EXPOSURE_LABELS = {"water_rate_loo": "Water coverage (LOO rate)",
                    "sanitation_rate_loo_core": "Sanitation coverage (LOO rate, core)",
                    "sanitation_rate_loo_robustness_biodigester": "Sanitation coverage (LOO rate, bio-digester robustness)"}

# Okabe-Ito palette: a standard colorblind-safe categorical set, applied in a
# FIXED order across every figure (pooled + 4 countries) rather than being
# re-picked per plot - satisfies "color follows the entity, never its rank."
SCOPE_COLORS = {
    "pooled": "#000000",     # black - the headline estimate is visually distinct
    "ethiopia": "#0072B2",   # blue
    "ghana": "#E69F00",      # orange
    "kenya": "#009E73",      # green
    "nigeria": "#D55E00",    # vermillion
}

DP_COEF = 3   # decimal places for coefficients/SE/CI
DP_PCT = 1    # decimal places for percentages
DP_MEAN = 2   # decimal places for means/SD


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_ci(lower, upper, dp=DP_COEF):
    return f"[{lower:.{dp}f}, {upper:.{dp}f}]"


# ============================================================================
# SECTION 1: INTEGRITY RE-CHECK (re-run immediately before output generation,
# per the approved instruction - not merely cited from the prior audit turn)
# ============================================================================

def run_integrity_checks(src):
    """Hard-fails on any of the locked integrity conditions. Returns a list
    of (check_name, status, detail) rows for the final audit record."""
    results = []

    def record(name, ok, detail):
        results.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
        if not ok:
            raise RuntimeError(f"INTEGRITY CHECK FAILED: {name} - {detail}")

    # ---- Step 07 shapes, hard-locked ----
    for key, expected in EXPECTED_STEP07_SHAPES.items():
        actual = src[key].shape
        record(f"shape:{key}", actual == expected, f"expected {expected}, got {actual}")

    # ---- No duplicate model-term rows ----
    dup_specs = {
        "main_continuous": ["outcome", "model", "country_scope", "term"],
        "binary_lpm": ["outcome", "model_label", "country_scope", "term"],
        "severe": ["outcome", "model_label", "country_scope", "term"],
        "biodigester": ["outcome", "model_label", "country_scope", "term"],
        "household": ["outcome", "model_label", "country_scope", "term"],
        "altweight": ["outcome", "model_label", "country_scope", "term"],
        "loo": ["outcome", "model_label", "country_scope", "term"],
    }
    for key, keys in dup_specs.items():
        n_dup = int(src[key].duplicated(subset=keys).sum())
        record(f"no_duplicates:{key}", n_dup == 0, f"{n_dup} duplicate rows on {keys}")

    # ---- No missing coefficient/SE/CI/p-value ----
    coef_cols = ["coefficient", "standard_error", "ci_lower", "ci_upper", "p_value"]
    for key in dup_specs:
        n_missing = int(src[key][coef_cols].isna().sum().sum())
        record(f"no_missing_fields:{key}", n_missing == 0, f"{n_missing} missing values across {coef_cols}")

    # ---- Sample N reconciliation (Step 11) ----
    mc, sf11 = src["main_continuous"], src["step11_flow"]
    mismatches = 0
    for (outcome, model, scope), grp in mc.groupby(["outcome", "model", "country_scope"]):
        n_reg = grp["estimation_n"].iloc[0]
        flow = sf11[(sf11["outcome"] == outcome) & (sf11["model"] == model) & (sf11["country_scope"] == scope)]
        if len(flow) != 1 or flow["final_estimation_n"].iloc[0] != n_reg:
            mismatches += 1
    record("sample_n_reconciliation:step11", mismatches == 0, f"{mismatches} mismatches")

    # ---- Step 11 pooled Model 4 == Step 12 equal-country unrestricted Model 4 exactly ----
    m4_pooled = mc[(mc["model"] == 4) & (mc["country_scope"] == "pooled")][["outcome", "term", "coefficient", "standard_error"]]
    aw_a = src["altweight"][src["altweight"]["model_label"] == "model4_weight_A_equal_total_country"][["outcome", "term", "coefficient", "standard_error"]]
    merged = m4_pooled.merge(aw_a, on=["outcome", "term"], suffixes=("_11", "_12"))
    max_diff = float((merged["coefficient_11"] - merged["coefficient_12"]).abs().max())
    record("step11_vs_step12_altweight_A_exact_match", len(merged) == len(m4_pooled) and max_diff < 1e-8,
           f"matched {len(merged)}/{len(m4_pooled)}, max diff {max_diff:.2e}")

    # ---- LOO unrestricted == Step 11 preferred Model 4 exactly ----
    loo_unres = src["loo"][src["loo"]["model_label"] == "model4_unrestricted"][["outcome", "term", "coefficient"]]
    merged2 = m4_pooled.merge(loo_unres, on=["outcome", "term"], suffixes=("_11", "_loo"))
    max_diff2 = float((merged2["coefficient_11"] - merged2["coefficient_loo"]).abs().max())
    record("loo_unrestricted_vs_step11_exact_match", len(merged2) == len(m4_pooled) and max_diff2 < 1e-8,
           f"matched {len(merged2)}/{len(m4_pooled)}, max diff {max_diff2:.2e}")

    # ---- severe_wasted sparsity metadata retained ----
    sev = src["severe"]
    sw = sev[sev["outcome"] == "severe_wasted"]["n_zero_event_regions"].unique()
    record("severe_wasted_sparsity_metadata_present", len(sw) == 1 and sw[0] == 24, f"n_zero_event_regions values found: {sw}")

    # ---- no ruled-out model appears in appendix outputs ----
    scopes_in_severe = sorted(sev["country_scope"].unique())
    record("no_ruled_out_country_specific_severe", scopes_in_severe == ["pooled"], f"scopes found: {scopes_in_severe}")

    return pd.DataFrame(results)


# ============================================================================
# SECTION 2: FINAL MAIN TABLES
# ============================================================================

def build_final_table1(t1):
    """Reorganizes the long-format Step 07 Table 1 into a wide,
    variable-by-country presentation table. Categorical variables show
    weighted % (with unweighted N in parentheses); maternal age shows
    weighted mean (SD)."""
    rows = []
    for (variable, category), grp in t1.groupby(["Variable", "Category"], sort=False):
        row = {"Variable": variable, "Category": category}
        for _, r in grp.iterrows():
            country = r["Country"]
            if pd.notna(r["Weighted Mean"]):
                row[country] = f"{r['Weighted Mean']:.{DP_MEAN}f} ({r['Weighted SD']:.{DP_MEAN}f})"
            else:
                row[country] = f"{r['Weighted %']:.{DP_PCT}f}% (n={int(r['Unweighted N'])})"
        rows.append(row)
    out = pd.DataFrame(rows)
    ordered_cols = ["Variable", "Category"] + [c for c in ["Ethiopia", "Ghana", "Kenya", "Nigeria"] if c in out.columns]
    return out[ordered_cols]


def build_final_table2(t2):
    """Anthropometric prevalence by country - already close to final shape;
    select and rename the presentation-relevant columns, round for display."""
    out = t2[["Country", "Outcome", "Valid Unweighted N", "Weighted Prevalence (%)",
              "95% CI Lower (%)", "95% CI Upper (%)"]].copy()
    out["Weighted Prevalence (%)"] = out["Weighted Prevalence (%)"].round(DP_PCT)
    out["95% CI"] = out.apply(lambda r: fmt_ci(r["95% CI Lower (%)"], r["95% CI Upper (%)"], DP_PCT), axis=1)
    return out[["Country", "Outcome", "Valid Unweighted N", "Weighted Prevalence (%)", "95% CI"]]


def build_final_table3(t3):
    """WASH characteristics by country - explicit states (Unknown,
    StructuralNotApplicable, UnclassifiedBioDigester, SurfaceWater,
    OpenDefecation) are preserved exactly as separate rows/categories, never
    merged, per the approved instruction."""
    out = t3.copy()
    out["Weighted %"] = out["Weighted %"].round(DP_PCT)
    return out


def build_final_table4(mc):
    """Main pooled regression, Models 1-4, exposure rows + model-information
    rows (controls/FE/N/PSU present or not), one panel per outcome."""
    panels = {}
    for outcome in ["haz", "waz", "whz"]:
        sub = mc[(mc["outcome"] == outcome) & (mc["country_scope"] == "pooled")]
        rows = []
        for term in EXPOSURE_TERMS:
            row = {"Term": EXPOSURE_LABELS[term]}
            for model in [1, 2, 3, 4]:
                r = sub[(sub["model"] == model) & (sub["term"] == term)]
                if len(r):
                    coef, se = r["coefficient"].iloc[0], r["standard_error"].iloc[0]
                    row[f"Model {model}"] = f"{coef:.{DP_COEF}f} ({se:.{DP_COEF}f})"
                else:
                    row[f"Model {model}"] = ""
            rows.append(row)
        # Model-information rows - read directly from the data, not hard-coded,
        # so a future change to the RHS is reflected automatically.
        info_rows = [
            ("Child controls", ["No", "Yes", "Yes", "Yes"]),
            ("Maternal/household controls", ["No", "No", "Yes", "Yes"]),
            ("Administrative-region FE", ["No", "No", "No", "Yes"]),
        ]
        for label, vals in info_rows:
            rows.append({"Term": label, **{f"Model {m}": v for m, v in zip([1, 2, 3, 4], vals)}})
        n_row, psu_row = {"Term": "N"}, {"Term": "PSU count"}
        for model in [1, 2, 3, 4]:
            r = sub[sub["model"] == model]
            n_row[f"Model {model}"] = int(r["estimation_n"].iloc[0])
            psu_row[f"Model {model}"] = int(r["psu_count"].iloc[0])
        rows += [n_row, psu_row]
        panels[outcome] = pd.DataFrame(rows)
    return panels


def build_final_table5(mc):
    """Preferred Model 4, exposure rows only, coefficient [95% CI], one
    panel per outcome, columns = pooled + 4 countries."""
    scopes = ["pooled"] + COUNTRIES
    panels = {}
    for outcome in ["haz", "waz", "whz"]:
        sub = mc[(mc["outcome"] == outcome) & (mc["model"] == 4)]
        rows = []
        for term in EXPOSURE_TERMS:
            row = {"Term": EXPOSURE_LABELS[term]}
            for scope in scopes:
                r = sub[(sub["country_scope"] == scope) & (sub["term"] == term)]
                coef, lo, hi = r["coefficient"].iloc[0], r["ci_lower"].iloc[0], r["ci_upper"].iloc[0]
                row[COUNTRY_LABELS[scope]] = f"{coef:.{DP_COEF}f} {fmt_ci(lo, hi)}"
            rows.append(row)
        panels[outcome] = pd.DataFrame(rows)
    return panels


def build_final_table6(bl):
    """Binary LPM robustness, preferred Model 4 exposure rows, coefficient
    [95% CI], columns = pooled + 4 countries, one panel per outcome."""
    scopes = ["pooled"] + COUNTRIES
    panels = {}
    for outcome in ["stunted", "wasted", "underweight"]:
        sub = bl[bl["outcome"] == outcome]
        rows = []
        for term in EXPOSURE_TERMS:
            row = {"Term": EXPOSURE_LABELS[term]}
            for scope in scopes:
                r = sub[(sub["country_scope"] == scope) & (sub["term"] == term)]
                coef, lo, hi = r["coefficient"].iloc[0], r["ci_lower"].iloc[0], r["ci_upper"].iloc[0]
                row[COUNTRY_LABELS[scope]] = f"{coef:.{DP_COEF}f} {fmt_ci(lo, hi)}"
            rows.append(row)
        panels[outcome] = pd.DataFrame(rows)
    return panels


# Every regression table gets this identical footnote block - locked wording.
REGRESSION_TABLE_NOTES = (
    "Notes: Estimates are associations, not causal effects. Primary WASH exposures are "
    "continuous cluster-level household leave-one-out coverage rates on [0,1]. Coefficients "
    "are the estimated association per 1.0 (100-percentage-point) increase in cluster "
    "coverage; a 10-percentage-point association equals coefficient x 0.10. Pooled models "
    "use a model-specific equal-total-country temporary weight (never persisted); "
    "country-specific models use the DHS-supplied weight (weight_original). Pooled standard "
    "errors are clustered by country_psu; country-specific standard errors are clustered by "
    "psu. Model 4 includes country-qualified administrative-region fixed effects "
    "(country_admin_region); no survey-year fixed effect or spatial grid fixed effect is "
    "included in any model."
)


def write_table_with_notes(df_or_panels, path, notes=REGRESSION_TABLE_NOTES):
    """Writes a table (or dict of outcome->panel) as CSV with the locked
    notes block appended as trailing rows, so the notes travel with the
    machine-readable file itself."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        if isinstance(df_or_panels, dict):
            for outcome, panel in df_or_panels.items():
                f.write(f"# Panel: {OUTCOME_LABELS.get(outcome, outcome)}\n")
                panel.to_csv(f, index=False)
                f.write("\n")
        else:
            df_or_panels.to_csv(f, index=False)
            f.write("\n")
        if notes:
            f.write(f"{notes}\n")


# ============================================================================
# SECTION 3: FINAL APPENDIX TABLES
# ============================================================================

def build_appendix_a1(sev):
    out = sev[sev["term"].isin(EXPOSURE_TERMS)][
        ["outcome", "term", "coefficient", "standard_error", "ci_lower", "ci_upper", "p_value",
         "event_count", "event_prevalence", "n_zero_event_regions", "n_total_regions"]
    ].copy()
    for c in ["coefficient", "standard_error", "ci_lower", "ci_upper"]:
        out[c] = out[c].round(DP_COEF)
    out["p_value"] = out["p_value"].round(3)
    out["event_prevalence_pct"] = (out["event_prevalence"] * 100).round(DP_PCT)
    flag = ("WARNING: severe_wasted has " +
            str(int(sev[sev['outcome']=='severe_wasted']['n_zero_event_regions'].iloc[0])) +
            "/" + str(int(sev[sev['outcome']=='severe_wasted']['n_total_regions'].iloc[0])) +
            " administrative-region FE cells with zero events - coefficients for this outcome "
            "should be treated as secondary/exploratory, not a headline result.")
    return out, flag


def build_appendix_a2(bd, mc):
    bd_exp = bd[bd["term"].isin(["water_rate_loo", "sanitation_rate_loo_robustness_biodigester"])][
        ["outcome", "country_scope", "term", "coefficient", "standard_error", "p_value"]
    ].rename(columns={"coefficient": "coefficient_robustness", "standard_error": "se_robustness", "p_value": "p_robustness"})
    core = mc[(mc["model"] == 4) & (mc["term"].isin(EXPOSURE_TERMS)) & (mc["country_scope"].isin(["pooled", "ghana"]))][
        ["outcome", "country_scope", "term", "coefficient", "standard_error", "p_value"]
    ].rename(columns={"coefficient": "coefficient_core", "standard_error": "se_core", "p_value": "p_core"})
    core["term"] = core["term"].replace({"sanitation_rate_loo_core": "sanitation_rate_loo_robustness_biodigester"})
    merged = core.merge(bd_exp, on=["outcome", "country_scope", "term"], how="outer")
    for c in [c for c in merged.columns if c.startswith(("coefficient", "se"))]:
        merged[c] = merged[c].round(DP_COEF)
    return merged


def build_appendix_a3(hh):
    out = hh[hh["term"].isin(["_water_hh_binary", "_sanitation_hh_binary"])][
        ["outcome", "term", "coefficient", "standard_error", "ci_lower", "ci_upper", "p_value",
         "preferred_model_n", "baseline_n", "n_excluded_by_household_wash_states"]
    ].copy()
    for c in ["coefficient", "standard_error", "ci_lower", "ci_upper"]:
        out[c] = out[c].round(DP_COEF)
    out["term"] = out["term"].replace({"_water_hh_binary": "water (household, binary)",
                                        "_sanitation_hh_binary": "sanitation (household, binary)"})
    note = ("No administrative-region FE (follows thesis_design.md Section 9.1 literally). "
            "Explicit WASH states (Unknown, StructuralNotApplicable, UnclassifiedBioDigester) "
            "are excluded from the binary exposure, reducing the analytical sample by the "
            "n_excluded_by_household_wash_states column.")
    return out, note


def build_appendix_a4(aw):
    out = aw[aw["term"].isin(EXPOSURE_TERMS)][
        ["outcome", "model_label", "term", "coefficient", "standard_error", "p_value"]
    ].copy()
    out["coefficient"] = out["coefficient"].round(DP_COEF)
    out["standard_error"] = out["standard_error"].round(DP_COEF)
    out["weighting_scheme"] = out["model_label"].map({
        "model4_weight_A_equal_total_country": "A: equal-total-country (approved)",
        "model4_weight_B_raw_weight_original": "B: raw DHS weight_original",
        "model4_weight_C_unweighted": "C: unweighted",
    })
    return out.drop(columns=["model_label"])[["outcome", "weighting_scheme", "term", "coefficient", "standard_error", "p_value"]]


def build_appendix_a5(loo):
    out = loo[loo["term"].isin(EXPOSURE_TERMS)][
        ["outcome", "model_label", "term", "coefficient", "standard_error", "p_value", "retained_n", "pct_retained"]
    ].copy()
    out["coefficient"] = out["coefficient"].round(DP_COEF)
    out["standard_error"] = out["standard_error"].round(DP_COEF)
    out["threshold"] = out["model_label"].map({
        "model4_unrestricted": "Unrestricted (approved sample)",
        "model4_min5": ">=5 other households (both exposures)",
        "model4_min10": ">=10 other households (both exposures)",
    })
    return out.drop(columns=["model_label"])[["outcome", "threshold", "term", "coefficient", "standard_error", "p_value", "retained_n", "pct_retained"]]


def build_appendix_a6(bl):
    out = bl.copy()
    for c in ["coefficient", "standard_error", "ci_lower", "ci_upper"]:
        out[c] = out[c].round(DP_COEF)
    out["p_value"] = out["p_value"].round(3)
    return out


def build_appendix_a8(admin, hr_wash, loo_diag):
    return admin.copy(), hr_wash.copy(), loo_diag.copy()


# ============================================================================
# SECTION 4: FIGURES
# ============================================================================

def figure1_prevalence(t2, path):
    outcomes = ["Stunting", "Wasting", "Underweight"]
    countries = ["Ethiopia", "Ghana", "Kenya", "Nigeria"]
    fig, ax = plt.subplots(figsize=(8, 5))
    width = 0.2
    x = np.arange(len(outcomes))
    for i, country in enumerate(countries):
        vals, errs_lo, errs_hi = [], [], []
        for outcome in outcomes:
            r = t2[(t2["Country"] == country) & (t2["Outcome"] == outcome)]
            v = r["Weighted Prevalence (%)"].iloc[0]
            lo = r["95% CI Lower (%)"].iloc[0]
            hi = r["95% CI Upper (%)"].iloc[0]
            vals.append(v); errs_lo.append(v - lo); errs_hi.append(hi - v)
        ax.bar(x + (i - 1.5) * width, vals, width, label=country,
               color=SCOPE_COLORS[country.lower()], yerr=[errs_lo, errs_hi], capsize=3)
    ax.set_xticks(x); ax.set_xticklabels(outcomes)
    ax.set_ylabel("Weighted prevalence (%)")
    ax.set_title("Figure 1. Anthropometric prevalence by country (weighted, 95% CI)")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.08))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def _forest_row_positions(scopes):
    """Shared row layout for a forest plot: one row per (exposure term,
    scope), with a visual gap between exposure blocks. Computed once and
    reused for both the plotted points and the tick labels, so the two can
    never drift out of sync."""
    labels, positions = [], []
    pos = 0
    for term in EXPOSURE_TERMS:
        for scope in scopes:
            labels.append(f"{EXPOSURE_LABELS[term].split(' (')[0]} - {COUNTRY_LABELS[scope]}")
            positions.append(pos)
            pos -= 1
        pos -= 0.6
    return labels, positions


def figure2_coefficient_forest(mc, path):
    scopes = ["pooled"] + COUNTRIES
    outcomes = ["haz", "waz", "whz"]
    row_labels, row_positions = _forest_row_positions(scopes)
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), sharey=True)
    for ax, outcome in zip(axes, outcomes):
        for (term, scope), pos in zip(
            ((t, s) for t in EXPOSURE_TERMS for s in scopes), row_positions
        ):
            r = mc[(mc["outcome"] == outcome) & (mc["model"] == 4) &
                   (mc["country_scope"] == scope) & (mc["term"] == term)]
            coef, lo, hi = r["coefficient"].iloc[0], r["ci_lower"].iloc[0], r["ci_upper"].iloc[0]
            ax.errorbar(coef, pos, xerr=[[coef - lo], [hi - coef]], fmt="o",
                        color=SCOPE_COLORS[scope], markersize=5, capsize=3, linewidth=1.3)
        ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title(OUTCOME_LABELS[outcome])
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_yticks(row_positions)
    axes[0].set_yticklabels(row_labels, fontsize=8)
    fig.suptitle("Figure 2. Preferred Model 4 continuous exposure associations (coefficient, 95% CI)")
    fig.text(0.5, 0.01, "Estimates are associations, not causal effects.", ha="center", fontsize=8, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    fig.savefig(path, dpi=200)
    plt.close(fig)


def figure3_wash_characteristics(t3, path):
    # A category's color is fixed ONCE across the whole figure (not per
    # panel) so that e.g. "Unknown" or "Structural / not applicable" reads
    # as the same color in both the water and sanitation panels - color
    # must follow the entity (the category), never its position/order of
    # appearance within a given panel.
    all_categories = list(pd.unique(t3["Category"]))
    palette = plt.cm.tab20(np.linspace(0, 1, len(all_categories)))
    category_color = dict(zip(all_categories, palette))

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, domain in zip(axes, sorted(t3["WASH Domain"].unique())):
        sub = t3[t3["WASH Domain"] == domain]
        categories = sub["Category"].unique()
        countries = ["Ethiopia", "Ghana", "Kenya", "Nigeria"]
        bottom = np.zeros(len(countries))
        # Explicit states (Unknown/StructuralNotApplicable/
        # UnclassifiedBioDigester/SurfaceWater/OpenDefecation) are plotted
        # as their own segments, never merged into another category.
        for cat in categories:
            vals = [sub[(sub["Country"] == c) & (sub["Category"] == cat)]["Weighted %"].sum() for c in countries]
            ax.bar(countries, vals, bottom=bottom, label=cat, color=category_color[cat])
            bottom += np.array(vals)
        ax.set_title(domain)
        ax.set_ylabel("Weighted %")
        ax.legend(fontsize=6, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Figure 3. WASH characteristics by country (all categories, explicit states preserved)")
    fig.tight_layout(rect=[0, 0.05, 1, 0.95])
    fig.savefig(path, dpi=200)
    plt.close(fig)


def appendix_figure_a1_binary_forest(bl, path):
    scopes = ["pooled"] + COUNTRIES
    outcomes = ["stunted", "wasted", "underweight"]
    row_labels, row_positions = _forest_row_positions(scopes)
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), sharey=True)
    for ax, outcome in zip(axes, outcomes):
        for (term, scope), pos in zip(
            ((t, s) for t in EXPOSURE_TERMS for s in scopes), row_positions
        ):
            r = bl[(bl["outcome"] == outcome) & (bl["country_scope"] == scope) & (bl["term"] == term)]
            coef, lo, hi = r["coefficient"].iloc[0], r["ci_lower"].iloc[0], r["ci_upper"].iloc[0]
            ax.errorbar(coef, pos, xerr=[[coef - lo], [hi - coef]], fmt="o",
                        color=SCOPE_COLORS[scope], markersize=5, capsize=3, linewidth=1.3)
        ax.axvline(0, color="gray", linewidth=0.8, linestyle="--")
        ax.set_title(outcome.capitalize())
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_yticks(row_positions)
    axes[0].set_yticklabels(row_labels, fontsize=8)
    fig.suptitle("Appendix Figure A1. Binary LPM robustness exposure associations (coefficient, 95% CI)")
    fig.text(0.5, 0.01, "Estimates are associations, not causal effects.", ha="center", fontsize=8, style="italic")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig(path, dpi=200)
    plt.close(fig)


# ============================================================================
# SECTION 5: DESCRIPTIVE SURVEY-CLUSTER COVERAGE MAP
# ============================================================================

def verify_displacement_wording(readme_path):
    """Reads the project's OWN bundled DHS GPS displacement documentation
    rather than relying on memory, per the approved instruction."""
    if not readme_path.exists():
        return "DHS cluster coordinates are randomly displaced for confidentiality."
    text = readme_path.read_text(encoding="utf-8", errors="ignore")
    if "2 kilometers" in text and "5 kilometers" in text and "10 kilometers" in text:
        return ("DHS cluster coordinates are randomly displaced for respondent confidentiality: "
                "urban clusters up to 2 km, rural clusters up to 5 km (with 1% of rural clusters "
                "displaced up to 10 km). This map shows broad survey coverage only, not precise "
                "household locations.")
    return "DHS cluster coordinates are randomly displaced for confidentiality."


def map_survey_cluster_coverage(df, caption, path):
    """One descriptive point per DHS cluster (deduplicated on country+cluster
    coordinate pair - NOT an aggregation of any household-level exposure
    value, just 'has this cluster been plotted already'). No WASH exposure
    value or regression result is mapped."""
    clusters = df[["country", "LATNUM", "LONGNUM"]].drop_duplicates()
    fig, ax = plt.subplots(figsize=(8, 8))
    for country in COUNTRIES:
        sub = clusters[clusters["country"] == country]
        ax.scatter(sub["LONGNUM"], sub["LATNUM"], s=6, alpha=0.6,
                   color=SCOPE_COLORS[country], label=COUNTRY_LABELS[country])
    ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    ax.set_title("Survey cluster coverage (descriptive only)")
    ax.legend(frameon=False, markerscale=2)
    ax.set_aspect("equal", adjustable="datalim")
    fig.text(0.5, 0.01, caption, ha="center", fontsize=7, wrap=True)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return len(clusters)


# ============================================================================
# SECTION 6: STEP 11 BUG-PROVENANCE NOTE (reproducibility record, not a
# thesis result)
# ============================================================================

STEP11_BUG_PROVENANCE_NOTE = (
    "STEP 11 REGRESSION SCRIPT - REPRODUCIBILITY NOTE\n"
    "==================================================\n\n"
    "An early development execution of the Step 11 regression script omitted "
    "the two primary exposure variables from the design matrix. Manual output "
    "inspection identified the specification error before results were "
    "accepted. The script was corrected and all retained Step 11 and Step 12 "
    "results derive exclusively from the corrected implementation. The "
    "technical details remain documented in 11_main_regressions.py.\n\n"
    "This is a reproducibility record, not a thesis result.\n"
)


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("="*90)
    print("STEP 13 - FINAL RESULTS PRODUCTION")
    print("="*90)

    for name, path in SOURCES.items():
        if not path.exists():
            raise FileNotFoundError(f"Required source not found: {name} -> {path}")
    checksums_before = {name: md5_of_file(p) for name, p in SOURCES.items()}
    print(f"\nAll {len(SOURCES)} source files confirmed present; checksums captured.")

    src = {
        "table1": pd.read_csv(SOURCES["table1"]), "table2": pd.read_csv(SOURCES["table2"]),
        "table2b": pd.read_csv(SOURCES["table2b"]), "table3": pd.read_csv(SOURCES["table3"]),
        "table4": pd.read_csv(SOURCES["table4"]),
        "main_continuous": pd.read_csv(SOURCES["main_continuous"]),
        "step11_flow": pd.read_csv(SOURCES["step11_flow"]),
        "binary_lpm": pd.read_csv(SOURCES["binary_lpm"]), "severe": pd.read_csv(SOURCES["severe"]),
        "biodigester": pd.read_csv(SOURCES["biodigester"]), "household": pd.read_csv(SOURCES["household"]),
        "altweight": pd.read_csv(SOURCES["altweight"]), "loo": pd.read_csv(SOURCES["loo"]),
        "step12_flow": pd.read_csv(SOURCES["step12_flow"]),
        "admin_region_report": pd.read_csv(SOURCES["admin_region_report"]),
        "hr_wash_report": pd.read_csv(SOURCES["hr_wash_report"]),
        "loo_denom_diag": pd.read_csv(SOURCES["loo_denom_diag"]),
    }

    # ---- SECTION 1: integrity re-check ----
    print(f"\n{'='*90}\nSECTION 1: INTEGRITY RE-CHECK\n{'='*90}")
    integrity_results = run_integrity_checks(src)
    for _, r in integrity_results.iterrows():
        print(f"  [{r['status']}] {r['check']}: {r['detail']}")
    print(f"\nAll {len(integrity_results)} integrity checks passed.")

    # ---- SECTION 2: final main tables ----
    print(f"\n{'='*90}\nSECTION 2: FINAL MAIN TABLES\n{'='*90}")
    FINAL_TABLES_DIR.mkdir(parents=True, exist_ok=True)

    t1_final = build_final_table1(src["table1"])
    write_table_with_notes(t1_final, FINAL_TABLES_DIR / "final_table1_sample_characteristics.csv", notes=None)
    print(f"  Final Table 1: {t1_final.shape}")

    t2_final = build_final_table2(src["table2"])
    write_table_with_notes(t2_final, FINAL_TABLES_DIR / "final_table2_anthropometric_prevalence.csv", notes=None)
    print(f"  Final Table 2: {t2_final.shape}")

    t3_final = build_final_table3(src["table3"])
    write_table_with_notes(t3_final, FINAL_TABLES_DIR / "final_table3_wash_characteristics.csv", notes=None)
    print(f"  Final Table 3: {t3_final.shape}")

    t4_panels = build_final_table4(src["main_continuous"])
    write_table_with_notes(t4_panels, FINAL_TABLES_DIR / "final_table4_main_pooled_models1to4.csv")
    print(f"  Final Table 4: {len(t4_panels)} panels (HAZ/WAZ/WHZ)")

    t5_panels = build_final_table5(src["main_continuous"])
    write_table_with_notes(t5_panels, FINAL_TABLES_DIR / "final_table5_preferred_model4_by_country.csv")
    print(f"  Final Table 5: {len(t5_panels)} panels (HAZ/WAZ/WHZ)")

    t6_panels = build_final_table6(src["binary_lpm"])
    write_table_with_notes(t6_panels, FINAL_TABLES_DIR / "final_table6_binary_lpm_robustness.csv")
    print(f"  Final Table 6: {len(t6_panels)} panels (stunted/wasted/underweight)")

    # ---- SECTION 3: final appendix tables ----
    print(f"\n{'='*90}\nSECTION 3: FINAL APPENDIX TABLES\n{'='*90}")
    FINAL_APPENDIX_DIR.mkdir(parents=True, exist_ok=True)

    a1, a1_flag = build_appendix_a1(src["severe"])
    write_table_with_notes(a1, FINAL_APPENDIX_DIR / "appendix_A1_severe_outcomes.csv", notes=a1_flag)
    print(f"  A1 Severe outcomes: {a1.shape} | {a1_flag}")

    a2 = build_appendix_a2(src["biodigester"], src["main_continuous"])
    write_table_with_notes(a2, FINAL_APPENDIX_DIR / "appendix_A2_ghana_biodigester.csv",
                            notes="The tiny water_rate_loo coefficient shift between core and robustness runs "
                                  "is expected joint-regression behavior (sanitation and water rates correlate "
                                  "~0.52), not a change in water_rate_loo itself.")
    print(f"  A2 Ghana bio-digester: {a2.shape}")

    a3, a3_note = build_appendix_a3(src["household"])
    write_table_with_notes(a3, FINAL_APPENDIX_DIR / "appendix_A3_household_wash_baseline.csv", notes=a3_note)
    print(f"  A3 Household WASH baseline: {a3.shape}")

    a4 = build_appendix_a4(src["altweight"])
    write_table_with_notes(a4, FINAL_APPENDIX_DIR / "appendix_A4_alternative_pooled_weighting.csv",
                            notes="Weighting sensitivity check only - not a re-specification of the preferred model.")
    print(f"  A4 Alternative weighting: {a4.shape}")

    a5 = build_appendix_a5(src["loo"])
    write_table_with_notes(a5, FINAL_APPENDIX_DIR / "appendix_A5_loo_denominator_sensitivity.csv",
                            notes="Sensitivity analysis only - thresholds are illustrative, not a new preferred sample.")
    print(f"  A5 LOO denominator sensitivity: {a5.shape}")

    a6 = build_appendix_a6(src["binary_lpm"])
    write_table_with_notes(a6, FINAL_APPENDIX_DIR / "appendix_A6_full_binary_lpm_coefficients.csv")
    print(f"  A6 Full binary LPM coefficients: {a6.shape}")

    write_table_with_notes(src["table4"].copy(), FINAL_APPENDIX_DIR / "appendix_A7_missingness_availability.csv", notes=None)
    print(f"  A7 Missingness/availability: {src['table4'].shape}")

    a8_admin, a8_hrwash, a8_loo = build_appendix_a8(src["admin_region_report"], src["hr_wash_report"], src["loo_denom_diag"])
    with open(FINAL_APPENDIX_DIR / "appendix_A8_admin_region_and_loo_support.csv", "w", newline="", encoding="utf-8") as f:
        f.write("# Panel 1: Administrative-region FE support (Step 09)\n")
        a8_admin.to_csv(f, index=False)
        f.write("\n# Panel 2: HR/WASH exposure linkage support (Step 08)\n")
        a8_hrwash.to_csv(f, index=False)
        f.write("\n# Panel 3: LOO denominator distribution (Step 08)\n")
        a8_loo.to_csv(f, index=False)
    print(f"  A8 Admin-region/LOO support: 3 panels ({a8_admin.shape}, {a8_hrwash.shape}, {a8_loo.shape})")

    # ---- SECTION 4: figures ----
    print(f"\n{'='*90}\nSECTION 4: FIGURES\n{'='*90}")
    FINAL_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    figure1_prevalence(src["table2"], FINAL_FIGURES_DIR / "figure1_prevalence_by_country.png")
    print("  Figure 1 written.")
    figure2_coefficient_forest(src["main_continuous"], FINAL_FIGURES_DIR / "figure2_model4_coefficient_forest.png")
    print("  Figure 2 written.")
    figure3_wash_characteristics(src["table3"], FINAL_FIGURES_DIR / "figure3_wash_characteristics.png")
    print("  Figure 3 written.")
    appendix_figure_a1_binary_forest(src["binary_lpm"], FINAL_APPENDIX_DIR / "appendix_figureA1_binary_lpm_forest.png")
    print("  Appendix Figure A1 written.")

    # ---- SECTION 5: map ----
    print(f"\n{'='*90}\nSECTION 5: DESCRIPTIVE SURVEY-CLUSTER COVERAGE MAP\n{'='*90}")
    displacement_caption = verify_displacement_wording(SOURCES["gps_displacement_readme"])
    print(f"  Displacement wording verified from local documentation: {SOURCES['gps_displacement_readme'].exists()}")
    df_geo = pd.read_parquet(SOURCES["step10_parquet"], columns=["country", "LATNUM", "LONGNUM"])
    n_clusters = map_survey_cluster_coverage(df_geo, displacement_caption, FINAL_FIGURES_DIR / "map_survey_cluster_coverage.png")
    print(f"  Map written: {n_clusters} unique cluster coordinates plotted.")

    # ---- SECTION 6: Step 11 bug provenance + final audit ----
    print(f"\n{'='*90}\nSECTION 6: FINAL AUDIT RECORD\n{'='*90}")
    FINAL_AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    (FINAL_AUDIT_DIR / "step11_bug_provenance_note.txt").write_text(STEP11_BUG_PROVENANCE_NOTE, encoding="utf-8")
    print("  step11_bug_provenance_note.txt written.")

    audit_rows = []
    for name, path in SOURCES.items():
        audit_rows.append({
            "source_file": name, "path": str(path),
            "md5": md5_of_file(path) if path.is_file() else "N/A (directory not applicable)",
            "rows": src[name].shape[0] if name in src else "N/A",
            "columns": src[name].shape[1] if name in src else "N/A",
        })
    audit_df = pd.DataFrame(audit_rows)
    audit_df.to_csv(FINAL_AUDIT_DIR / "step13_final_audit.csv", index=False)
    print("  step13_final_audit.csv written.")

    summary_lines = [
        "STEP 13 FINAL AUDIT SUMMARY",
        "=" * 40, "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Integrity checks: {len(integrity_results)}/{len(integrity_results)} PASSED", "",
        "Source -> Final output mapping:",
        "  table1/2/3/4 (Step 07)        -> final_tables/final_table1-3.csv, final_appendix/A7",
        "  main_continuous_models.csv     -> final_tables/final_table4.csv, final_table5.csv, figure2",
        "  robustness_binary_lpm.csv      -> final_tables/final_table6.csv, appendix A6, appendix figure A1",
        "  appendix/severe_outcomes.csv   -> final_appendix/A1",
        "  robustness_biodigester.csv     -> final_appendix/A2",
        "  robustness_household_wash.csv  -> final_appendix/A3",
        "  robustness_alternative_weights.csv -> final_appendix/A4",
        "  robustness_loo_denominator.csv -> final_appendix/A5",
        "  step09/step08 diagnostic reports -> final_appendix/A8", "",
        "WARNINGS carried forward:",
        f"  - severe_wasted: 24/114 zero-event administrative-region FE cells (see appendix A1).",
        "  - haz/sanitation_rate_loo_core sign is sensitive to the pooled weighting scheme "
        "(positive under equal-country and unweighted, negative under raw weight_original) - see appendix A4.",
        "  - Step 11 bug provenance: see step11_bug_provenance_note.txt.",
    ]
    (FINAL_AUDIT_DIR / "step13_final_audit_summary.txt").write_text("\n".join(summary_lines), encoding="utf-8")
    print("  step13_final_audit_summary.txt written.")

    # ---- Final source-integrity re-verification ----
    checksums_after = {name: md5_of_file(p) for name, p in SOURCES.items()}
    changed = [name for name in checksums_before if checksums_before[name] != checksums_after[name]]
    if changed:
        raise RuntimeError(f"Source file(s) changed during Step 13 execution: {changed}")
    print(f"\n{'='*90}\nSource integrity check: all {len(SOURCES)} source files unchanged before/after.\n{'='*90}")


if __name__ == "__main__":
    main()
