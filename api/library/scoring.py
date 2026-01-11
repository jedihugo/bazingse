# * -------------------------
# * SCORING SYSTEM - FORMULA-BASED
# * -------------------------
# Define multipliers for distance-based scoring

DISTANCE_MULTIPLIERS = {
    "three_branch": {  # For THREE_MEETINGS and THREE_COMBINATIONS
        "2": 1.0,      # Three consecutive nodes (best)
        "3": 0.786,
        "4": 0.618,
        "5": 0.500,
        "6": 0.382,
        "7": 0.236,
    },
    "two_branch": {  # For all other branch interactions
        "1": 1.0,      # Gap = 1 (adjacent pillars, luck-natal)
        "2": 0.618,    # Gap = 2
        "3": 0.382,    # Gap = 3
        "4": 0.236,    # Gap = 4 (cross-layer at gap=3)
    }
}

# Base scores for each interaction type
# POSITIVE: p = combined (detected), q = transformed (fully activated)
# NEGATIVE: p = impact (initial conflict), q = severity (intensified conflict)
BASE_SCORES = {
    # Positive Interactions (supportive, generative)
    "THREE_MEETINGS": {"combined": 35, "transformed": 61.8},
    "THREE_COMBINATIONS": {"combined": 25, "transformed": 45},
    "HALF_MEETINGS": {"combined": 20, "transformed": 40},
    "STEM_COMBINATIONS": {"combined": 19, "transformed": 38},
    "SIX_HARMONIES": {"combined": 18, "transformed": 35},
    "ARCHED_COMBINATIONS": {"combined": 12, "transformed": 25},

    # Negative Interactions (conflicting, destructive)
    "CLASHES_OPPOSITE": {"damage": 38},  # Opposite elements: asymmetric (victim 1.0, controller 0.618)
    "CLASHES_SAME": {"damage": 38},  # Same element: equal mutual damage
    "PUNISHMENTS_3NODE": {"damage": 38},  # 3-node: equal 1:1:1, ELEVATED severity
    "STEM_CONFLICTS": {"damage": 35},  # HS asymmetric (victim 1.0, controller 0.618)
    "HARMS": {"damage": 20},  # EB asymmetric (victim 1.0, controller 0.618)
    "DESTRUCTION_OPPOSITE": {"damage": 20},  # Opposite elements: asymmetric, distance 0 only
    "DESTRUCTION_SAME": {"damage": 20},  # Same element: equal mutual, distance 0 only
    "PUNISHMENTS_2NODE": {"damage": 16},  # 2-node: asymmetric 0.618:1 (less than HARMS)
}


def generate_scoring(base_1, base_2, pattern_type, state_1="combined", state_2="transformed"):
    """
    Generate scoring dictionary with distance multipliers applied.

    Formula: score = base_score * multiplier

    Args:
        base_1 (int): Base score for first state (e.g., combined/impact)
        base_2 (int): Base score for second state (e.g., transformed/severity)
        pattern_type (str): "three_branch" or "two_branch"
        state_1 (str): Name for first state (default: "combined")
        state_2 (str): Name for second state (default: "transformed")

    Returns:
        dict: Complete scoring dictionary with all distance levels calculated

    Examples:
        Positive: generate_scoring(19, 38, "two_branch")
        Negative: generate_scoring(22, 42, "two_branch", "impact", "severity")
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]

    scoring = {
        state_1: {},
        state_2: {}
    }

    for distance_key, multiplier in multipliers.items():
        scoring[state_1][distance_key] = round(base_1 * multiplier)
        scoring[state_2][distance_key] = round(base_2 * multiplier)

    return scoring


def generate_single_scoring(base, pattern_type):
    """
    Generate simple scoring with only distance decay (no states).
    Used for mutual/equal damage patterns like CLASHES.

    Formula: score = base * distance_multiplier

    Args:
        base (int): Base damage/score
        pattern_type (str): "three_branch" or "two_branch"

    Returns:
        dict: Flat scoring dictionary with distance levels

    Example:
        CLASHES: generate_single_scoring(38, "two_branch")
        -> {"1": 38, "2": 24, "3": 15, "4": 9}
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]
    scoring = {}

    for distance_key, multiplier in multipliers.items():
        scoring[distance_key] = round(base * multiplier)

    return scoring


def generate_asymmetric_scoring(base, pattern_type, ratio=0.618):
    """
    Generate asymmetric scoring for controller-victim relationships.
    Used for STEM_CONFLICTS where controller expends less energy than victim suffers.

    Formula:
        victim_score = base * distance_multiplier
        controller_score = base * ratio * distance_multiplier

    Args:
        base (int): Base damage (victim's full damage)
        pattern_type (str): "three_branch" or "two_branch"
        ratio (float): Controller-to-victim ratio (default: 0.618, golden ratio)

    Returns:
        dict: Scoring with separate controller and victim dictionaries

    Example:
        STEM_CONFLICTS: generate_asymmetric_scoring(35, "two_branch", 0.618)
        -> {
            "victim": {"1": 35, "2": 22, "3": 13, "4": 8},
            "controller": {"1": 22, "2": 14, "3": 8, "4": 5}
          }
    """
    multipliers = DISTANCE_MULTIPLIERS[pattern_type]

    scoring = {
        "victim": {},
        "controller": {}
    }

    for distance_key, multiplier in multipliers.items():
        scoring["victim"][distance_key] = round(base * multiplier)
        scoring["controller"][distance_key] = round(base * ratio * multiplier)

    return scoring
