# * =========================
# * NARRATIVE PRIORITY SCORING
# * =========================
# Determines which narratives are most important to display.
# Uses a weighted scoring system based on interaction strength, type, and context.

from typing import List, Dict, Any

# =============================================================================
# PRIORITY WEIGHTS
# =============================================================================
# Base priority scores by interaction type

TYPE_PRIORITY = {
    # High priority - Full transformations and major conflicts
    "THREE_MEETINGS": 100,
    "THREE_COMBINATIONS": 95,
    "CLASHES": 90,
    "PUNISHMENTS": 85,

    # Medium-high priority - Partial combinations and significant interactions
    "SIX_HARMONIES": 75,
    "STEM_COMBINATIONS": 70,
    "STEM_CONFLICTS": 65,
    "HARMS": 60,

    # Medium priority - Partial patterns
    "HALF_MEETINGS": 55,
    "HALF_COMBINATIONS": 50,
    "DESTRUCTION": 45,
    "ARCHED_COMBINATIONS": 40,

    # Lower priority - Background interactions
    "SEASONAL_ADJUSTMENT": 30,
    "ENERGY_FLOW": 25,

    # Special narratives - Element balance and daymaster
    "ELEMENT_EXCESS": 80,
    "ELEMENT_DEFICIENCY": 75,
    "DAYMASTER_STRONG": 70,
    "DAYMASTER_BALANCED": 65,
    "DAYMASTER_WEAK": 70,
    "WEALTH_STORAGE_OPENED": 85,
    "WEALTH_STORAGE_CLOSED": 50,

    # Ten Gods narratives - Important for understanding relationships
    "TEN_GOD_WARNING": 72,
    "TEN_GOD_OPPORTUNITY": 68,

    # Pillar analysis - Lower priority (contextual info)
    "PILLAR_ANALYSIS": 35,

    # Alternate key names (backward compatibility)
    "CLASH": 90,
    "HARM": 60,
    "HALF_MEETING": 55,
    "HALF_COMBINATION": 50,
    "ARCHED_COMBINATION": 40,
    "STEM_COMBINATION": 70,
    "STEM_CONFLICT": 65,
    "CROSS_PILLAR_WUXING": 30,
}

# Multipliers based on transformation status
TRANSFORMATION_MULTIPLIER = {
    True: 1.5,   # Full transformation - more significant
    False: 1.0,  # Partial/no transformation
}

# Multipliers based on pillar involvement
PILLAR_MULTIPLIER = {
    "day": 1.3,      # Day pillar interactions are most personal
    "month": 1.2,    # Month pillar affects career/status
    "hour": 1.1,     # Hour pillar affects children/late life
    "year": 1.0,     # Year pillar is foundational
    "luck_10y": 1.4, # Current luck cycle is very relevant
    "annual": 1.3,   # Annual luck is timely
    "monthly": 1.2,  # Monthly luck for short-term
    "daily": 1.1,    # Daily luck for specific timing
    "talisman": 0.8, # Talisman interactions are supplementary
}

# Distance affects significance (adjacent = more impactful)
DISTANCE_MULTIPLIER = {
    "adjacent": 1.3,
    "nearby": 1.1,
    "far": 0.9,
}


def calculate_priority_score(interaction: Dict[str, Any]) -> float:
    """
    Calculate the priority score for a single narrative/interaction.
    Higher score = more important to show.

    Args:
        interaction: Dict containing interaction data with keys like:
            - type: Interaction type (e.g., "THREE_MEETINGS")
            - transformed: Boolean for transformation status
            - positions: List of position indices
            - distance: Distance key (e.g., "adjacent")
            - points: Qi impact (can parse from string like "+15.5 points")

    Returns:
        Float priority score
    """
    interaction_type = interaction.get("type", "")

    # Base priority from type
    base_score = TYPE_PRIORITY.get(interaction_type, 20)

    # Transformation multiplier
    transformed = interaction.get("transformed", False)
    trans_mult = TRANSFORMATION_MULTIPLIER.get(transformed, 1.0)

    # Pillar involvement multiplier (take the highest)
    positions = interaction.get("positions", [])
    pillar_mult = 1.0
    for pos in positions:
        pillar_type = _position_to_pillar_type(pos)
        mult = PILLAR_MULTIPLIER.get(pillar_type, 1.0)
        pillar_mult = max(pillar_mult, mult)

    # Distance multiplier
    distance = interaction.get("distance", "")
    dist_mult = 1.0
    if "adjacent" in str(distance).lower():
        dist_mult = DISTANCE_MULTIPLIER["adjacent"]
    elif "nearby" in str(distance).lower():
        dist_mult = DISTANCE_MULTIPLIER["nearby"]
    elif "far" in str(distance).lower():
        dist_mult = DISTANCE_MULTIPLIER["far"]

    # Qi impact bonus (normalize points to a multiplier)
    points_str = interaction.get("points", "0")
    qi_bonus = _parse_points_bonus(points_str)

    # Calculate final score
    final_score = base_score * trans_mult * pillar_mult * dist_mult + qi_bonus

    return final_score


def prioritize_narratives(
    narratives: List[Dict[str, Any]],
    max_count: int = 10,
    min_score: float = 30.0
) -> List[Dict[str, Any]]:
    """
    Sort and filter narratives by priority, returning the most important ones.

    Args:
        narratives: List of narrative dicts
        max_count: Maximum number of narratives to return
        min_score: Minimum priority score to include

    Returns:
        Sorted list of top narratives with priority_score added
    """
    # Calculate scores for all narratives
    scored = []
    for narrative in narratives:
        score = calculate_priority_score(narrative)
        if score >= min_score:
            narrative_with_score = dict(narrative)
            narrative_with_score["priority_score"] = round(score, 1)
            scored.append(narrative_with_score)

    # Sort by score descending
    scored.sort(key=lambda x: x["priority_score"], reverse=True)

    # Return top N
    return scored[:max_count]


def _position_to_pillar_type(position: int) -> str:
    """
    Convert position index to pillar type name.

    Position mapping (from AGENTS.md):
    0=Hour | 1=Day | 2=Month | 3=Year | 4=10YL | 5=Annual | 6=Monthly | 7=Daily | 8=Hourly
    Talisman positions: 9-12 for year/month/day/hour talismans
    """
    position_map = {
        0: "hour",
        1: "day",
        2: "month",
        3: "year",
        4: "luck_10y",
        5: "annual",
        6: "monthly",
        7: "daily",
        8: "hourly",
        # Talisman positions
        9: "talisman",
        10: "talisman",
        11: "talisman",
        12: "talisman",
    }
    return position_map.get(position, "unknown")


def _parse_points_bonus(points_str: str) -> float:
    """
    Parse a points string like "+15.5 points" or "-8.2 points" and return a bonus.
    Higher absolute value = more significant interaction.
    """
    try:
        # Extract numeric value
        import re
        match = re.search(r'[+-]?[\d.]+', str(points_str))
        if match:
            value = abs(float(match.group()))
            # Scale to a reasonable bonus (0-20 range)
            return min(value / 5.0, 20.0)
    except (ValueError, AttributeError):
        pass
    return 0.0


def group_narratives_by_category(
    narratives: List[Dict[str, Any]]
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group narratives by their category for organized display.

    Categories:
    - combination: Positive combinations
    - conflict: Negative conflicts
    - balance: Element balance issues
    - daymaster: Daymaster analysis
    - wealth: Wealth storage
    - ten_gods: Ten Gods relationships
    - pillar: Pillar analysis
    - seasonal: Seasonal influences
    - energy: Energy flow
    """
    grouped = {
        "combination": [],
        "conflict": [],
        "balance": [],
        "daymaster": [],
        "wealth": [],
        "ten_gods": [],
        "pillar": [],
        "seasonal": [],
        "energy": [],
    }

    for narrative in narratives:
        category = narrative.get("category", "")
        if category in grouped:
            grouped[category].append(narrative)
        else:
            # Default to energy for unknown categories
            grouped["energy"].append(narrative)

    return grouped
