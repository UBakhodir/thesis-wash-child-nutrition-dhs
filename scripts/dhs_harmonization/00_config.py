"""
00_config.py
=============
Single source of truth for the four-country DHS harmonization pipeline
(Ethiopia 2024-25, Ghana 2022, Kenya 2022, Nigeria 2024).

Paths, approved reference categories, anthropometric thresholds, and
weight-handling settings only. No data-loading or transformation logic.
"""

from pathlib import Path

# ----------------------------------------------------------------------
# Project root and top-level data directories
# ----------------------------------------------------------------------
PROJECT_ROOT = Path(r"c:\Users\user\Documents\Graduation_Thesis")

DATA_RAW = PROJECT_ROOT / "data" / "raw" / "DHS"           # untouched ZIP archives
DATA_INTERIM = PROJECT_ROOT / "data" / "interim" / "DHS"   # untouched extracted DHS files
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"        # pipeline-generated outputs ONLY
DATA_STAGING = DATA_PROCESSED / "staging"                   # intermediate analytical files

# ----------------------------------------------------------------------
# Per-country survey metadata and source file paths (read-only sources)
# ----------------------------------------------------------------------
COUNTRIES = {
    "ethiopia": {
        "survey_label": "Ethiopia DHS 2024-25",
        "country_round": "2024-25",
        "kr_path": DATA_INTERIM / "ethiopia" / "2024-25" / "KR" / "ETKR8AFL.dta",
        "hr_path": DATA_INTERIM / "ethiopia" / "2024-25" / "HR" / "ETHR8AFL.dta",
        "ir_path": DATA_INTERIM / "ethiopia" / "2024-25" / "IR" / "ETIR8AFL.dta",
        "ge_path": DATA_INTERIM / "ethiopia" / "2024-25" / "GE" / "ETGE8AFL.shp",
        "staging_dir": DATA_STAGING / "ethiopia",
        "processed_file": DATA_PROCESSED / "ethiopia_kr_clean.parquet",
    },
    "ghana": {
        "survey_label": "Ghana DHS 2022",
        "country_round": "2022",
        "kr_path": DATA_INTERIM / "ghana" / "2022" / "KR" / "GHKR8CFL.DTA",
        "hr_path": DATA_INTERIM / "ghana" / "2022" / "HR" / "GHHR8CFL.DTA",
        "ir_path": DATA_INTERIM / "ghana" / "2022" / "IR" / "GHIR8CFL.DTA",
        "ge_path": DATA_INTERIM / "ghana" / "2022" / "GE" / "GHGE8AFL.shp",
        "staging_dir": DATA_STAGING / "ghana",
        "processed_file": DATA_PROCESSED / "ghana_kr_clean.parquet",
    },
    "kenya": {
        "survey_label": "Kenya DHS 2022",
        "country_round": "2022",
        "kr_path": DATA_INTERIM / "kenya" / "2022" / "KR" / "KEKR8CFL.DTA",
        "hr_path": DATA_INTERIM / "kenya" / "2022" / "HR" / "KEHR8CFL.DTA",
        "ir_path": DATA_INTERIM / "kenya" / "2022" / "IR" / "KEIR8CFL.DTA",
        "ge_path": DATA_INTERIM / "kenya" / "2022" / "GE" / "KEGE8AFL.shp",
        "staging_dir": DATA_STAGING / "kenya",
        "processed_file": DATA_PROCESSED / "kenya_kr_clean.parquet",
    },
    "nigeria": {
        "survey_label": "Nigeria DHS 2024",
        "country_round": "2024",
        "kr_path": DATA_INTERIM / "nigeria" / "2024" / "KR" / "NGKR8BFL.dta",
        "hr_path": DATA_INTERIM / "nigeria" / "2024" / "HR" / "NGHR8BFL.dta",
        "ir_path": DATA_INTERIM / "nigeria" / "2024" / "IR" / "NGIR8BFL.dta",
        "ge_path": DATA_INTERIM / "nigeria" / "2024" / "GE" / "NGGE8AFL.shp",
        "staging_dir": DATA_STAGING / "nigeria",
        "processed_file": DATA_PROCESSED / "nigeria_kr_clean.parquet",
    },
}

POOLED_OUTPUT = DATA_PROCESSED / "pooled_kr_four_country.parquet"
POOLED_GEOLINKED_OUTPUT = DATA_PROCESSED / "pooled_kr_four_country_geolinked.parquet"

# ----------------------------------------------------------------------
# DHS identifier / survey-design variable names (differ KR/IR vs HR)
#
# NOTE (added during the Step 13 supervisor-readability audit): ID_VARS and
# GE_CLUSTER_VAR below are early planning-stage references and are NOT
# currently imported by any downstream script - every stage script (02
# onward) hardcodes its own ID_COLS/cluster-variable names inline instead
# (e.g. 02_load_flag_anthro.py's ID_COLS, 06_ge_linkage.py's GE_RETAINED_COLS
# handling of DHSCLUST). Kept here as documentation of the DHS identifier
# naming convention across file types, not as active configuration. If you
# are trying to trace where a script gets its identifier column names from,
# look at that script's own ID_COLS constant, not here.
# ----------------------------------------------------------------------
ID_VARS = {
    "KR": {"cluster": "v001", "household": "v002", "line": "v003",
           "weight": "v005", "psu": "v021", "strata": "v022"},
    "IR": {"cluster": "v001", "household": "v002", "line": "v003",
           "weight": "v005", "psu": "v021", "strata": "v022"},
    "HR": {"cluster": "hv001", "household": "hv002", "line": "hv003",
           "weight": "hv005", "psu": "hv021", "strata": "hv022"},
}
GE_CLUSTER_VAR = "DHSCLUST"  # not imported downstream - see note above

# ----------------------------------------------------------------------
# Anthropometric thresholds (DHS/WHO standard - approved)
# ----------------------------------------------------------------------
# NOT imported by any downstream script (verified by pre-freeze audit, grep
# across scripts/dhs_harmonization/ finds only this definition, no
# consumer). 02_load_flag_anthro.py independently redefines the same
# hw70/hw71/hw72 mapping via its own ANTHRO_RAW_VARS/SCALED_NAMES. Retained
# here for reference only - see 00_config.py's other documented-dead
# constants below for the established pattern of flagging these explicitly.
ANTHRO_VARS = {"haz": "hw70", "waz": "hw71", "whz": "hw72"}
ANTHRO_FLAG_IMPLAUSIBLE = 9998
ANTHRO_FLAG_MISSING = 9999
ANTHRO_SCALE_DIVISOR = 100.0
STUNTING_CUTOFF = -2.0
WASTING_CUTOFF = -2.0
UNDERWEIGHT_CUTOFF = -2.0
SEVERE_CUTOFF = -3.0   # secondary/robustness outcomes only

# ----------------------------------------------------------------------
# Approved reference categories
#
# NOTE (added during the Step 13 supervisor-readability audit):
# REFERENCE_CATEGORIES below is NOT currently imported by any downstream
# script, and its lowercase snake_case values ("male", "no_education", ...)
# do not match the actual decoded DHS label strings used as reference
# categories in the regression stage (11_main_regressions.py uses the
# Title Case label text itself, e.g. "Male", "No education", "Cannot read
# at all", "Poorest", "Rural" - see CHILD_CONTROLS_CATEGORICAL /
# SES_CONTROLS_CATEGORICAL there). This dict predates that later, more
# specific implementation and was never wired up to it. Kept here only as
# a historical record of the originally-planned reference categories - the
# authoritative reference-category source is 11_main_regressions.py itself.
# ----------------------------------------------------------------------
REFERENCE_CATEGORIES = {
    "child_sex": "male",
    "maternal_education": "no_education",
    "literacy": "cannot_read",
    "wealth_quintile": "poorest",
    "urban_rural": "rural",
    "country": "ethiopia",
}

# ----------------------------------------------------------------------
# Weight handling (approved)
#
# NOTE (added during the Step 13 supervisor-readability audit):
# PRESERVE_ORIGINAL_WEIGHT and POOLED_WEIGHT_RESCALE_METHOD below are NOT
# currently imported by any downstream script. WEIGHT_DIVISOR (used to
# rescale v005/hv005 to weight_original) IS actively used, in
# 04_build_country_kr.py. The other two constants document early planning
# intent - "preserve the original DHS weight unchanged alongside any
# derived weight" and "if a pooled weight is built, rescale so each
# country's total weight is equal" - both of which were ultimately
# implemented, but independently, inside 11_main_regressions.py's
# build_temporary_pooled_weight() (a model-specific, never-persisted
# weight computed fresh for each regression's own estimation sample, per
# the approved Step 11 design) rather than by reading these constants.
# ----------------------------------------------------------------------
WEIGHT_DIVISOR = 1_000_000
PRESERVE_ORIGINAL_WEIGHT = True  # not imported downstream - see note above
POOLED_WEIGHT_RESCALE_METHOD = "equal_total_weight_per_country"  # not imported downstream - see note above

# ----------------------------------------------------------------------
# Nigeria data-quality flags (documented limitation, NOT an exclusion
# rule - core pipeline retains all children; used only by the dedicated
# robustness/sensitivity script)
# ----------------------------------------------------------------------
NIGERIA_UNEXPLAINED_CLUSTERS = [880, 891, 1340]   # under-5 children in HR, zero KR rows
NIGERIA_ZERO_ELIGIBLE_CLUSTERS = [715, 1350]      # hv014=0, consistent w/ "no eligible children"


if __name__ == "__main__":
    # Read-only structural check: confirms configured paths exist.
    # Does NOT open, read, or modify any DHS data file.
    for country, info in COUNTRIES.items():
        for key in ("kr_path", "hr_path", "ir_path", "ge_path"):
            p = info[key]
            status = "OK" if p.exists() else "MISSING"
            print(f"{country:10s} {key:10s} {status:8s} {p}")
