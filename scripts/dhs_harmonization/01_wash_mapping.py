"""
01_wash_mapping.py
====================
Finalized, externally-verified WASH (v113 water / v116 sanitation)
harmonization mapping, per the approved Final Analysis Specification.

Pure mapping definitions and documentation only - no data is loaded and
no mapping is applied to any dataset in this module.
"""

# ----------------------------------------------------------------------
# v113 - Drinking water source -> harmonized category
# ----------------------------------------------------------------------
WATER_CATEGORY_MAP = {
    11: "Improved",                  # piped into dwelling
    12: "Improved",                  # piped to yard/plot
    13: "Improved",                  # piped to neighbor
    14: "Improved",                  # public tap/standpipe
    21: "Improved",                  # tube well or borehole
    31: "Improved",                  # protected well
    32: "Unimproved",                # unprotected well
    41: "Improved",                  # protected spring
    42: "Unimproved",                # unprotected spring
    43: "SurfaceWater",              # river/dam/lake/ponds/stream/canal/irrigation channel
    51: "Improved",                  # rainwater
    61: "Improved",                  # tanker truck (delivered water)
    62: "Improved",                  # cart with small tank (delivered water)
    71: "Improved",                  # bottled water (packaged water)
    72: "Improved",                  # packaged water - country-specific label, see below
    96: "Unknown",                   # other -> not classifiable
    97: "StructuralNotApplicable",   # not a de jure resident
}

# Documentation only: country-specific label text for code 72, preserved
# for reporting even though the harmonized category is Improved for all.
WATER_CODE72_LABELS_BY_COUNTRY = {
    "ethiopia": "large bottle",
    "ghana": "sachet water",
    "kenya": None,      # code 72 not observed in Kenya's questionnaire
    "nigeria": "sachet water",
}

# ----------------------------------------------------------------------
# v116 - Sanitation facility -> harmonized category (CORE specification)
# ----------------------------------------------------------------------
SANITATION_CATEGORY_MAP_CORE = {
    11: "Improved",                  # flush to piped sewer system
    12: "Improved",                  # flush to septic tank
    13: "Improved",                  # flush to pit latrine
    14: "Unimproved",                # flush to somewhere else
    15: "Unimproved",                # flush, don't know where
    16: "UnclassifiedBioDigester",   # Ghana-only bio-digester - UNCLASSIFIED (core), see below
    21: "Improved",                  # ventilated improved pit latrine (VIP)
    22: "Improved",                  # pit latrine with slab
    23: "Unimproved",                # pit latrine without slab/open pit
    31: "OpenDefecation",            # no facility/bush/field
    41: "Improved",                  # composting toilet
    42: "Unimproved",                # bucket toilet
    43: "Unimproved",                # hanging toilet/latrine
    96: "Unknown",                   # other -> not classifiable
    97: "StructuralNotApplicable",   # not a de jure resident
}

# Robustness variant: Ghana code 16 reclassified as Improved. Built as a
# copy + override so the core map above is never mutated.
SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER = {
    **SANITATION_CATEGORY_MAP_CORE,
    16: "Improved",
}

# Documentation: Ghana-only facility type, explicitly flagged unresolved.
SANITATION_CODE16_LABEL = "flush, bio-digester (biofil)"
SANITATION_CODE16_COUNTRY = "ghana"
SANITATION_CODE16_STATUS_CORE = "UNCLASSIFIED - no authoritative JMP source found"

# ----------------------------------------------------------------------
# v160 service-level refinement - defined as a pure function here.
# NOT called anywhere in this module; only used by 03_build_indicators.py
# once approved and executed.
# ----------------------------------------------------------------------
def classify_sanitation_service(v116_category, v160_value):
    """
    v116_category: output of a SANITATION_CATEGORY_MAP_* lookup
    v160_value: raw v160 code (0=not shared, 1=shared, 7=structural, NaN=structural-missing)
    Returns: "Basic" | "Limited" | "StructuralNotApplicable" | "Unimproved" |
             "OpenDefecation" | "Unknown" | "UnclassifiedBioDigester" | None

    Explicit WASH states (Unimproved, OpenDefecation, Unknown,
    StructuralNotApplicable, UnclassifiedBioDigester) propagate through
    UNCHANGED - v160 is never consulted for these, per the approved
    specification. Only "Improved" rows are ever resolved using v160.
    """
    if v116_category == "Improved":
        if v160_value == 0:
            return "Basic"
        if v160_value == 1:
            return "Limited"
        if v160_value == 7:
            return "StructuralNotApplicable"
        return None  # unexpected value or missing/NaN under Improved - do not guess

    # Identity propagation - v160 is NOT consulted for any of these:
    if v116_category in ("Unimproved", "OpenDefecation", "Unknown",
                          "StructuralNotApplicable", "UnclassifiedBioDigester"):
        return v116_category

    return None  # any other unexpected category input - do not guess

# ----------------------------------------------------------------------
# Robustness collapse: Basic/Limited/Unimproved/OpenDefecation ->
# simple Improved/Non-improved. Defined, not applied here.
# ----------------------------------------------------------------------
SANITATION_SERVICE_COLLAPSE_MAP = {
    "Basic": "Improved",
    "Limited": "Improved",
    "Unimproved": "NonImproved",
    "OpenDefecation": "NonImproved",
    "Unknown": "Unknown",
    "StructuralNotApplicable": "StructuralNotApplicable",
    "UnclassifiedBioDigester": "UnclassifiedBioDigester",
}


if __name__ == "__main__":
    # Prints the mapping tables for manual review only. Touches no data.
    print("WATER_CATEGORY_MAP:", WATER_CATEGORY_MAP)
    print("WATER_CODE72_LABELS_BY_COUNTRY:", WATER_CODE72_LABELS_BY_COUNTRY)
    print("SANITATION_CATEGORY_MAP_CORE:", SANITATION_CATEGORY_MAP_CORE)
    print("SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER:",
          SANITATION_CATEGORY_MAP_ROBUSTNESS_BIODIGESTER)
