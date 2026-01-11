# * =========================
# * POSITIVE COMBINATION PATTERNS (DERIVED FROM CORE)
# * =========================
# All positive/supportive branch and stem interactions
# Patterns are DERIVED from the core.py STEMS and BRANCHES.

from .core import STEMS, BRANCHES
from .derived import ELEMENT_POLARITY_TO_STEM
from .scoring import (
    BASE_SCORES,
    DISTANCE_MULTIPLIERS,
    generate_scoring,
)

# * -------------------------
# * THREE MEETINGS (三會 - Seasonal Directional Combos)
# * -------------------------

_THREE_MEETINGS_SCORING = generate_scoring(
    BASE_SCORES["THREE_MEETINGS"]["combined"],
    BASE_SCORES["THREE_MEETINGS"]["transformed"],
    "three_branch"
)

_season_combos_seen = set()
THREE_MEETINGS = {}
for branch_id, branch in BRANCHES.items():
    season_combo = branch.get("season_combo")
    if season_combo:
        key = "-".join(season_combo[:3])
        if key not in _season_combos_seen:
            _season_combos_seen.add(key)
            THREE_MEETINGS[key] = {
                "branches": list(season_combo[:3]),
                "element": season_combo[3],
                "scoring": _THREE_MEETINGS_SCORING
            }

# * -------------------------
# * THREE COMBINATIONS (三合 - Triangular Combos)
# * -------------------------

_THREE_COMBINATIONS_SCORING = generate_scoring(
    BASE_SCORES["THREE_COMBINATIONS"]["combined"],
    BASE_SCORES["THREE_COMBINATIONS"]["transformed"],
    "three_branch"
)

_three_combos_seen = set()
THREE_COMBINATIONS = {}
for branch_id, branch in BRANCHES.items():
    three_combo = branch.get("three_combo")
    if three_combo:
        key = "-".join(three_combo[:3])
        if key not in _three_combos_seen:
            _three_combos_seen.add(key)
            THREE_COMBINATIONS[key] = {
                "branches": list(three_combo[:3]),
                "element": three_combo[3],
                "scoring": _THREE_COMBINATIONS_SCORING
            }

# * -------------------------
# * HALF MEETINGS (半會) - Requires Earth (storage) branch to be present
# * -------------------------
# Rules:
# 1. Must include the Earth storage branch (Chou, Chen, Wei, Xu)
# 2. Excludes pairs that are already SIX_HARMONIES (Zi-Chou, Wu-Wei)
#
# Valid patterns:
# - Winter/Water (Hai-Zi-Chou): Hai-Chou only (Zi-Chou is SIX_HARMONIES)
# - Spring/Wood (Yin-Mao-Chen): Yin-Chen, Mao-Chen
# - Summer/Fire (Si-Wu-Wei): Si-Wei only (Wu-Wei is SIX_HARMONIES)
# - Autumn/Metal (Shen-You-Xu): Shen-Xu, You-Xu

_HALF_MEETINGS_SCORING = generate_scoring(
    BASE_SCORES["HALF_MEETINGS"]["combined"],
    BASE_SCORES["HALF_MEETINGS"]["transformed"],
    "two_branch"
)

# Manually define valid HALF_MEETINGS (Earth branch must be present, no SIX_HARMONIES overlap)
HALF_MEETINGS = {
    # Winter/Water - Hai-Zi-Chou, Earth=Chou
    "Hai-Chou": {
        "branches": ["Hai", "Chou"],
        "element": "Water",
        "missing": "Zi",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Spring/Wood - Yin-Mao-Chen, Earth=Chen
    "Yin-Chen": {
        "branches": ["Yin", "Chen"],
        "element": "Wood",
        "missing": "Mao",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
    "Mao-Chen": {
        "branches": ["Mao", "Chen"],
        "element": "Wood",
        "missing": "Yin",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Summer/Fire - Si-Wu-Wei, Earth=Wei
    "Si-Wei": {
        "branches": ["Si", "Wei"],
        "element": "Fire",
        "missing": "Wu",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
    # Autumn/Metal - Shen-You-Xu, Earth=Xu
    "Shen-Xu": {
        "branches": ["Shen", "Xu"],
        "element": "Metal",
        "missing": "You",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
    "You-Xu": {
        "branches": ["You", "Xu"],
        "element": "Metal",
        "missing": "Shen",
        "blocked_by": [],
        "scoring": _HALF_MEETINGS_SCORING
    },
}

# * -------------------------
# * SIX HARMONIES (六合 - Pair Combinations)
# * -------------------------

_SIX_HARMONIES_SCORING = generate_scoring(
    BASE_SCORES["SIX_HARMONIES"]["combined"],
    BASE_SCORES["SIX_HARMONIES"]["transformed"],
    "two_branch"
)

_harmonies_seen = set()
SIX_HARMONIES = {}
for branch_id, branch in BRANCHES.items():
    partner = branch.get("harmonizes")
    harmony_element = branch.get("harmony_element")
    if partner and harmony_element:
        pair = tuple(sorted([branch_id, partner]))
        if pair not in _harmonies_seen:
            _harmonies_seen.add(pair)
            key = f"{pair[0]}-{pair[1]}"
            SIX_HARMONIES[key] = {
                "branches": list(pair),
                "element": harmony_element,
                "scoring": _SIX_HARMONIES_SCORING
            }

# * -------------------------
# * ARCHED COMBINATIONS (拱合) - Any 2 of 3 branches from THREE_COMBINATIONS
# * -------------------------

_ARCHED_COMBINATIONS_SCORING = {
    "detected": {
        "1": BASE_SCORES["ARCHED_COMBINATIONS"]["combined"],
        "2": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["2"]),
        "3": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["3"]),
        "4": round(BASE_SCORES["ARCHED_COMBINATIONS"]["combined"] * DISTANCE_MULTIPLIERS["two_branch"]["4"])
    }
}

ARCHED_COMBINATIONS = {}
for combo_key, combo in THREE_COMBINATIONS.items():
    branches = combo["branches"]
    element = combo["element"]
    first, middle, third = branches[0], branches[1], branches[2]
    # Generate all 3 possible pairs (any 2 of 3 branches)
    pairs = [
        ([first, middle], third),   # first + middle, missing third
        ([middle, third], first),   # middle + third, missing first
        ([first, third], middle),   # first + third, missing middle
    ]
    for pair_branches, missing in pairs:
        arch_key = f"{pair_branches[0]}-{pair_branches[1]}"
        if arch_key not in ARCHED_COMBINATIONS:
            ARCHED_COMBINATIONS[arch_key] = {
                "branches": pair_branches,
                "element": element,
                "missing": missing,
                "scoring": _ARCHED_COMBINATIONS_SCORING
            }

# * -------------------------
# * STEM COMBINATIONS (天干五合)
# * -------------------------

_STEM_COMBINATIONS_SCORING = generate_scoring(
    BASE_SCORES["STEM_COMBINATIONS"]["combined"],
    BASE_SCORES["STEM_COMBINATIONS"]["transformed"],
    "two_branch"
)

_stem_combos_seen = set()
STEM_COMBINATIONS = {}
for stem_id, stem in STEMS.items():
    partner = stem.get("combines_with")
    combo_element = stem.get("combination_element")
    if partner and combo_element:
        pair = tuple(sorted([stem_id, partner]))
        if pair not in _stem_combos_seen:
            _stem_combos_seen.add(pair)
            key = f"{pair[0]}-{pair[1]}"
            transform_to = ELEMENT_POLARITY_TO_STEM.get((combo_element, "Yang"))
            STEM_COMBINATIONS[key] = {
                "interaction_type": "HS_COMBINATIONS",
                "transform_to": transform_to,
                "transform_element": combo_element,
                "transformation_requirement": {
                    "element": combo_element,
                    "location": "eb",
                },
                "scoring": _STEM_COMBINATIONS_SCORING,
                "meaning": {}
            }

# * -------------------------
# * TRANSFORMATION STRENGTH TIERS
# * -------------------------

TRANSFORMATION_STRENGTH = {
    "THREE_MEETINGS": "strong",
    "THREE_COMBINATIONS": "normal",
    "ARCHED_COMBINATIONS": "normal",
    "SIX_HARMONIES": "weak",
}

STRENGTH_ORDER = {
    "ultra_strong": 0,
    "strong": 1,
    "normal": 2,
    "weak": 3
}
