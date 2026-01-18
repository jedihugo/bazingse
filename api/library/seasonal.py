# * =========================
# * SEASONAL STRENGTH & TRANSFORMATION RULES
# * =========================
# Season/element_states are now embedded in BRANCHES (core.py).
# This file derives seasonal lookups from that embedded data.

from .core import BRANCHES

# Build SEASONAL_STRENGTH from BRANCHES.element_states
# Format: Element -> {State -> [Branches]}
SEASONAL_STRENGTH = {"Wood": {}, "Fire": {}, "Earth": {}, "Metal": {}, "Water": {}}
for branch_id, branch in BRANCHES.items():
    for element, state in branch["element_states"].items():
        if state not in SEASONAL_STRENGTH[element]:
            SEASONAL_STRENGTH[element][state] = []
        SEASONAL_STRENGTH[element][state].append(branch_id)

SEASONAL_ADJUSTMENT = {
    # Balanced multipliers for seasonal effects (旺相休囚死)
    # Reduced impact for more subtle seasonal influence
    "prosperous": 1.236,     # 旺 Wang - Peak/thriving (strongest)
    "strengthening": 1.146,  # 相 Xiang - Growing phase
    "resting": 1.0,          # 休 Xiu - Baseline (no change)
    "trapped": 0.886,        # 囚 Qiu - Trapped/declining
    "dead": 0.786            # 死 Si - Dead/weakest
}

# Alias for backward compatibility
ELEMENT_SEASONAL_STATES = SEASONAL_STRENGTH

# * =========================
# * TRANSFORMATION SEASONAL REQUIREMENTS (化成條件)
# * =========================
# Classical BaZi principle: Some transformations only complete in specific seasons
# or receive bonuses when occurring in their native season

TRANSFORMATION_SEASONAL_RULES = {
    "Wood": {
        "favorable_seasons": ["Yin", "Mao", "Chen", "Hai", "Zi"],  # Spring + Winter
        "unfavorable_seasons": ["Shen", "You", "Xu"],  # Autumn (Metal controls Wood)
        "bonus_multiplier": 1.15,
        "penalty_multiplier": 0.85,
    },
    "Fire": {
        "favorable_seasons": ["Si", "Wu", "Wei", "Yin", "Mao"],  # Summer + Spring
        "unfavorable_seasons": ["Hai", "Zi", "Chou"],  # Winter (Water controls Fire)
        "bonus_multiplier": 1.15,
        "penalty_multiplier": 0.85,
    },
    "Earth": {
        "favorable_seasons": ["Chen", "Chou", "Wei", "Xu", "Si", "Wu"],  # Earth + Summer
        "unfavorable_seasons": ["Yin", "Mao"],  # Spring (Wood controls Earth)
        "bonus_multiplier": 1.12,
        "penalty_multiplier": 0.88,
    },
    "Metal": {
        "favorable_seasons": ["Shen", "You", "Xu", "Chen", "Chou", "Wei"],  # Autumn + Earth
        "unfavorable_seasons": ["Si", "Wu"],  # Summer (Fire controls Metal)
        "bonus_multiplier": 1.15,
        "penalty_multiplier": 0.85,
    },
    "Water": {
        "favorable_seasons": ["Hai", "Zi", "Chou", "Shen", "You"],  # Winter + Autumn
        "unfavorable_seasons": ["Chen", "Chou", "Wei", "Xu"],  # Earth months
        "bonus_multiplier": 1.15,
        "penalty_multiplier": 0.85,
    }
}

# Daymaster involvement multipliers
DAYMASTER_TRANSFORMATION_RULES = {
    "day_stem_involved": {
        "multiplier": 1.25,
        "description": "Day Master stem participates in transformation (日主干合)"
    },
    "day_branch_involved": {
        "multiplier": 1.20,
        "description": "Day Branch participates in transformation (日支合)"
    },
    "both_involved": {
        "multiplier": 1.35,
        "description": "Day Pillar fully engaged in transformation (日柱入局)"
    }
}
