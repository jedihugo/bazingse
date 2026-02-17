# =============================================================================
# ENVIRONMENTAL QI & RELOCATION ASSESSMENT (过江龙)
# =============================================================================
# Analyzes whether relocation benefits the chart based on:
#   - Water element need (crossing water theory)
#   - Directional element alignment
#   - Void disruption potential
#   - Overall element balance
# =============================================================================

from typing import List, Dict, Optional
from ..core import STEMS, BRANCHES
from ..derived import ELEMENT_CYCLES, ELEMENT_CHINESE
from .models import EnvironmentAssessment, ChartData, StrengthAssessment


# =============================================================================
# DIRECTIONAL ELEMENTS
# =============================================================================

DIRECTION_ELEMENTS = {
    "East": "Wood",
    "South": "Fire",
    "West": "Metal",
    "North": "Water",
    "Center": "Earth",
    "Southeast": "Wood",
    "Southwest": "Earth",
    "Northeast": "Earth",
    "Northwest": "Metal",
}

ELEMENT_DIRECTIONS = {
    "Wood": ["East", "Southeast"],
    "Fire": ["South"],
    "Earth": ["Center", "Southwest", "Northeast"],
    "Metal": ["West", "Northwest"],
    "Water": ["North"],
}

ELEMENT_CLIMATES = {
    "Wood": "warm and humid, with abundant vegetation",
    "Fire": "hot, tropical, sunny climate",
    "Earth": "moderate, stable climate with good agriculture",
    "Metal": "cool, dry, crisp air climate",
    "Water": "cold, coastal, or near bodies of water",
}

ELEMENT_GEOGRAPHY = {
    "Wood": "forested areas, near parks and greenery",
    "Fire": "tropical regions, elevated or volcanic areas",
    "Earth": "flat plains, agricultural regions, central locations",
    "Metal": "mountainous regions, mineral-rich areas, western areas",
    "Water": "coastal cities, river valleys, island nations, lakeside",
}


# =============================================================================
# CROSSING WATER (过江龙) ASSESSMENT
# =============================================================================

def assess_crossing_water(chart: ChartData, strength: StrengthAssessment) -> dict:
    """
    Assess the 过江龙 (Dragon Crossing River) theory:
    Does this person benefit from crossing water / living abroad?

    Scoring (0-5 scale):
    +1 if DM is weak Water or needs Water as useful god
    +1 if Water element is depleted in natal chart
    +1 if natal chart has Fire/Earth dominance (Water is needed to balance)
    +1 if Yi Ma (Traveling Horse) is present in natal chart
    +1 if chart has significant void issues that relocation could disrupt
    """
    score = 0
    factors = []
    dm_element = chart.dm_element

    # 1. DM needs Water
    needs_water = ("Water" in strength.favorable_elements)
    if needs_water:
        score += 1
        factors.append("Water is a favorable element for this chart")

    # DM IS Water and weak
    if dm_element == "Water" and strength.verdict in ("weak", "extremely_weak"):
        score += 1
        factors.append("Weak Water DM directly benefits from Water environment")

    # 2. Water depleted in natal chart
    from .strength import count_elements
    elem_counts = count_elements(chart)
    water_count = elem_counts.get("Water", 0)
    fire_count = elem_counts.get("Fire", 0)
    earth_count = elem_counts.get("Earth", 0)

    if water_count < 1.0:
        score += 1
        factors.append(f"Water element severely depleted (count: {water_count:.1f})")
    elif water_count < 2.0:
        factors.append(f"Water element below average (count: {water_count:.1f})")

    # 3. Fire/Earth dominance
    if fire_count + earth_count > 5.0:
        score += 1
        factors.append(f"Fire+Earth dominance ({fire_count:.1f}+{earth_count:.1f}) "
                      "needs Water to balance")

    # 4. Yi Ma presence (travel star)
    from .shen_sha import YI_MA_LOOKUP
    has_yi_ma = False
    for base_pos in ["year", "day"]:
        base_br = chart.pillars[base_pos].branch
        target = YI_MA_LOOKUP.get(base_br)
        if target:
            natal_branches = {chart.pillars[p].branch for p in ["year", "month", "day", "hour"]}
            if target in natal_branches:
                has_yi_ma = True
                break

    if has_yi_ma:
        score += 1
        factors.append("Traveling Horse (驿马) present = natural traveler")

    # Verdict
    if score >= 4:
        verdict = "strong"
        benefit = True
        reason = ("This chart strongly benefits from crossing water. "
                 "Relocation abroad or near major bodies of water is a PRIMARY life remedy.")
    elif score >= 2:
        verdict = "moderate"
        benefit = True
        reason = ("This chart moderately benefits from crossing water. "
                 "Living near water or abroad will significantly help.")
    else:
        verdict = "not_applicable"
        benefit = False
        reason = ("Crossing water is neutral for this chart. "
                 "Relocation is not a significant remedy.")

    return {
        "score": score,
        "verdict": verdict,
        "benefit": benefit,
        "reason": reason,
        "factors": factors,
    }


# =============================================================================
# FAVORABLE DIRECTIONS
# =============================================================================

def get_favorable_directions(strength: StrengthAssessment) -> Dict[str, List[str]]:
    """
    Determine favorable and unfavorable directions based on useful god.
    """
    favorable = []
    unfavorable = []

    for elem in strength.favorable_elements:
        dirs = ELEMENT_DIRECTIONS.get(elem, [])
        favorable.extend(dirs)

    for elem in strength.unfavorable_elements:
        dirs = ELEMENT_DIRECTIONS.get(elem, [])
        unfavorable.extend(dirs)

    return {
        "favorable": list(dict.fromkeys(favorable)),  # deduplicate preserving order
        "unfavorable": list(dict.fromkeys(unfavorable)),
    }


# =============================================================================
# IDEAL ENVIRONMENT
# =============================================================================

def get_ideal_environment(strength: StrengthAssessment) -> dict:
    """
    Determine ideal climate and geography based on useful god element.
    """
    useful = strength.useful_god
    return {
        "ideal_climate": ELEMENT_CLIMATES.get(useful, "moderate climate"),
        "ideal_geography": ELEMENT_GEOGRAPHY.get(useful, "balanced environment"),
        "useful_element": useful,
        "useful_element_chinese": ELEMENT_CHINESE.get(useful, ""),
    }


# =============================================================================
# VOID DISRUPTION ASSESSMENT
# =============================================================================

def assess_void_disruption(chart: ChartData) -> List[str]:
    """
    Check which palaces have branches that are void (空亡).
    Void branches are partially "nullified" — relocation can sometimes
    fill or disrupt the void.
    """
    from .shen_sha import get_void_branches

    void_brs = get_void_branches(chart)
    disrupted = []

    for pos in ["year", "month", "day", "hour"]:
        if chart.pillars[pos].branch in void_brs:
            disrupted.append(pos)

    return disrupted


# =============================================================================
# MASTER ENVIRONMENT ASSESSMENT
# =============================================================================

def assess_environment(chart: ChartData, strength: StrengthAssessment) -> EnvironmentAssessment:
    """
    Complete environmental qi and relocation assessment.
    """
    # Crossing water
    cw = assess_crossing_water(chart, strength)

    # Directions
    dirs = get_favorable_directions(strength)

    # Environment
    env = get_ideal_environment(strength)

    # Void disruption
    void_palaces = assess_void_disruption(chart)

    # Location recommendations
    if cw["benefit"]:
        location_recs = (
            f"Relocating abroad or near water is strongly recommended. "
            f"Best directions: {', '.join(dirs['favorable'])}. "
            f"Ideal environment: {env['ideal_climate']}. "
            f"Best geography: {env['ideal_geography']}."
        )
    else:
        location_recs = (
            f"Relocation is neutral. If moving, favor these directions: "
            f"{', '.join(dirs['favorable'])}. "
            f"Ideal climate: {env['ideal_climate']}."
        )

    return EnvironmentAssessment(
        crosses_water_benefit=cw["benefit"],
        crosses_water_reason=cw["reason"],
        favorable_directions=dirs["favorable"],
        unfavorable_directions=dirs["unfavorable"],
        ideal_climate=env["ideal_climate"],
        ideal_geography=env["ideal_geography"],
        guo_jiang_long_score=cw["score"],
        guo_jiang_long_verdict=cw["verdict"],
        guo_jiang_long_factors=cw["factors"],
        void_disruption_palaces=void_palaces,
        location_recommendations=location_recs,
    )
