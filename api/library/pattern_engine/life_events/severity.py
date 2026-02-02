# * =============================================================================
# * SEVERITY CALCULATION ENGINE
# * =============================================================================
# * Calculates life event severity from pattern matches, seasonal states,
# * pillar positions, and Day Master relevance.
# * =============================================================================

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from enum import Enum

from .taxonomy import (
    LifeDomain,
    Sentiment,
    Severity as SeverityLevel,
    EventType,
    ALL_EVENT_TYPES,
    TCM_ORGANS,
)


# =============================================================================
# SEVERITY MULTIPLIERS
# =============================================================================

# Distance multipliers (closer interactions are stronger)
DISTANCE_MULTIPLIERS = {
    0: 1.0,    # Adjacent
    1: 0.85,   # One apart
    2: 0.70,   # Two apart
    3: 0.55,   # Three apart
    4: 0.45,   # Four apart (luck pillars)
}

# Seasonal state multipliers (vulnerability increases in trapped/dead states)
SEASONAL_STATE_MULTIPLIERS = {
    "Prosperous": 0.6,    # 旺 - Element is strong, less vulnerable
    "Strengthening": 0.8,  # 相 - Growing strength
    "Resting": 1.0,        # 休 - Baseline
    "Trapped": 1.4,        # 囚 - Weakened, more vulnerable
    "Dead": 1.8,           # 死 - Weakest, highly vulnerable
}

# Pillar position multipliers (Day pillar is most personal)
PILLAR_POSITION_MULTIPLIERS = {
    "year": 1.0,    # Ancestral, external
    "month": 1.2,   # Career, parents
    "day": 1.5,     # Self, spouse
    "hour": 1.0,    # Children, legacy
}

# Pillar position names from position codes
POSITION_TO_PILLAR = {
    0: "hour",
    1: "day",
    2: "month",
    3: "year",
    4: "10yl",   # 10-year luck
    5: "annual",
    6: "monthly",
    7: "daily",
    8: "hourly",
}

# Pattern category severity weights
PATTERN_CATEGORY_WEIGHTS = {
    "punishment": 1.0,        # Most severe negative
    "clash": 0.9,
    "harm": 0.7,
    "destruction": 0.5,
    "stem_conflict": 0.6,
    "three_meetings": 1.0,    # Most powerful positive
    "three_combinations": 0.9,
    "six_harmonies": 0.7,
    "half_meetings": 0.5,
    "half_combinations": 0.4,
    "arched_combinations": 0.3,
    "stem_combination": 0.8,
}


# =============================================================================
# SEVERITY CALCULATION
# =============================================================================

@dataclass
class SeverityResult:
    """Result of severity calculation."""
    raw_score: float           # Base score before normalization
    normalized_score: float    # 0-100 scale
    severity_level: SeverityLevel
    contributing_factors: Dict[str, float]
    explanation: str


def calculate_pattern_severity(
    pattern_id: str,
    pattern_category: str,
    distance: int,
    seasonal_state: str,
    pillar_position: int,
    daymaster_element: str,
    pattern_element: Optional[str] = None,
    is_transformed: bool = False,
) -> SeverityResult:
    """
    Calculate severity of a single pattern match.

    Formula:
    severity = base_weight
             × distance_multiplier
             × seasonal_multiplier
             × pillar_multiplier
             × daymaster_relevance
             × transformation_bonus
    """

    factors = {}

    # Base weight from pattern category
    category_key = pattern_category.lower()
    base_weight = PATTERN_CATEGORY_WEIGHTS.get(category_key, 0.5)
    factors["base_weight"] = base_weight

    # Distance multiplier
    distance_mult = DISTANCE_MULTIPLIERS.get(distance, 0.4)
    factors["distance_mult"] = distance_mult

    # Seasonal state multiplier
    seasonal_mult = SEASONAL_STATE_MULTIPLIERS.get(seasonal_state, 1.0)
    factors["seasonal_mult"] = seasonal_mult

    # Pillar position multiplier
    pillar_name = POSITION_TO_PILLAR.get(pillar_position, "year")
    pillar_mult = PILLAR_POSITION_MULTIPLIERS.get(pillar_name, 1.0)
    factors["pillar_mult"] = pillar_mult

    # Day Master relevance
    dm_mult = 1.0
    if pattern_element:
        if pattern_element == daymaster_element:
            dm_mult = 1.5  # Directly affects Day Master
        elif _elements_related(pattern_element, daymaster_element):
            dm_mult = 1.2  # Related element
    factors["dm_relevance"] = dm_mult

    # Transformation bonus
    transform_bonus = 1.3 if is_transformed else 1.0
    factors["transform_bonus"] = transform_bonus

    # Calculate raw score
    raw_score = (
        base_weight *
        distance_mult *
        seasonal_mult *
        pillar_mult *
        dm_mult *
        transform_bonus *
        10  # Scale factor
    )

    # Normalize to 0-100 (typical range is 0-30)
    normalized = min(100, (raw_score / 30) * 100)

    # Determine severity level
    if normalized >= 70:
        level = SeverityLevel.CRITICAL
    elif normalized >= 50:
        level = SeverityLevel.MAJOR
    elif normalized >= 30:
        level = SeverityLevel.MODERATE
    else:
        level = SeverityLevel.MINOR

    # Generate explanation
    explanation = _generate_severity_explanation(
        pattern_id, level, factors, seasonal_state, pillar_name
    )

    return SeverityResult(
        raw_score=round(raw_score, 2),
        normalized_score=round(normalized, 1),
        severity_level=level,
        contributing_factors=factors,
        explanation=explanation,
    )


def calculate_compound_severity(
    pattern_results: List[SeverityResult],
    domain: LifeDomain,
) -> SeverityResult:
    """
    Calculate combined severity from multiple patterns.

    Compound patterns have multiplicative effects beyond simple addition.
    """
    if not pattern_results:
        return SeverityResult(
            raw_score=0,
            normalized_score=0,
            severity_level=SeverityLevel.MINOR,
            contributing_factors={},
            explanation="No patterns detected",
        )

    # Sum individual scores
    total_raw = sum(r.raw_score for r in pattern_results)

    # Apply compound bonus (more patterns = amplified effect)
    pattern_count = len(pattern_results)
    compound_mult = 1.0 + (pattern_count - 1) * 0.25  # +25% per additional pattern

    compounded_raw = total_raw * compound_mult

    # Normalize
    normalized = min(100, (compounded_raw / 50) * 100)

    # Determine level
    if normalized >= 70:
        level = SeverityLevel.CRITICAL
    elif normalized >= 50:
        level = SeverityLevel.MAJOR
    elif normalized >= 30:
        level = SeverityLevel.MODERATE
    else:
        level = SeverityLevel.MINOR

    factors = {
        "pattern_count": pattern_count,
        "compound_multiplier": compound_mult,
        "individual_scores": [r.raw_score for r in pattern_results],
    }

    explanation = (
        f"{pattern_count} patterns converge affecting {domain.value} domain. "
        f"Combined severity: {level.value}."
    )

    return SeverityResult(
        raw_score=round(compounded_raw, 2),
        normalized_score=round(normalized, 1),
        severity_level=level,
        contributing_factors=factors,
        explanation=explanation,
    )


# =============================================================================
# DOMAIN-SPECIFIC SEVERITY
# =============================================================================

def calculate_health_severity(
    pattern_results: List[SeverityResult],
    affected_elements: Set[str],
    seasonal_states: Dict[str, str],
    daymaster_element: str,
) -> Dict:
    """
    Calculate health-specific severity with TCM correlations.
    """
    base_result = calculate_compound_severity(pattern_results, LifeDomain.HEALTH)

    # Find affected organs
    affected_organs = []
    for element in affected_elements:
        if element in TCM_ORGANS:
            organ = TCM_ORGANS[element]
            organ_severity = seasonal_states.get(element, "Resting")
            affected_organs.append({
                "element": element,
                "zang": organ.zang_organ,
                "fu": organ.fu_organ,
                "chinese_zang": organ.chinese_zang,
                "chinese_fu": organ.chinese_fu,
                "body_parts": list(organ.body_parts),
                "emotion": organ.emotion,
                "seasonal_state": organ_severity,
                "vulnerability": SEASONAL_STATE_MULTIPLIERS.get(organ_severity, 1.0),
            })

    # Sort by vulnerability (higher = more at risk)
    affected_organs.sort(key=lambda x: x["vulnerability"], reverse=True)

    return {
        "severity_result": base_result,
        "affected_organs": affected_organs,
        "most_vulnerable": affected_organs[0] if affected_organs else None,
        "recommendation": _generate_health_recommendation(
            affected_organs, base_result.severity_level
        ),
    }


def calculate_wealth_severity(
    pattern_results: List[SeverityResult],
    wealth_element: str,  # Typically the element DM controls
    seasonal_state: str,
) -> Dict:
    """
    Calculate wealth-specific severity.
    """
    base_result = calculate_compound_severity(pattern_results, LifeDomain.WEALTH)

    # Adjust based on wealth element's seasonal state
    wealth_vulnerability = SEASONAL_STATE_MULTIPLIERS.get(seasonal_state, 1.0)

    adjusted_score = base_result.normalized_score * wealth_vulnerability

    return {
        "severity_result": base_result,
        "wealth_element": wealth_element,
        "wealth_seasonal_state": seasonal_state,
        "adjusted_score": round(adjusted_score, 1),
        "recommendation": _generate_wealth_recommendation(
            base_result.severity_level, seasonal_state
        ),
    }


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _elements_related(elem1: str, elem2: str) -> bool:
    """Check if two elements are in producing/controlling relationship."""
    RELATIONS = {
        "Wood": {"Fire", "Earth"},      # Produces Fire, Controls Earth
        "Fire": {"Earth", "Metal"},     # Produces Earth, Controls Metal
        "Earth": {"Metal", "Water"},    # Produces Metal, Controls Water
        "Metal": {"Water", "Wood"},     # Produces Water, Controls Wood
        "Water": {"Wood", "Fire"},      # Produces Wood, Controls Fire
    }
    return elem2 in RELATIONS.get(elem1, set())


def _generate_severity_explanation(
    pattern_id: str,
    level: SeverityLevel,
    factors: Dict[str, float],
    seasonal_state: str,
    pillar_name: str,
) -> str:
    """Generate human-readable explanation of severity calculation."""
    parts = []

    # Pattern identification
    pattern_type = pattern_id.split("~")[0] if "~" in pattern_id else pattern_id
    parts.append(f"{pattern_type} pattern detected")

    # Severity level
    level_text = {
        SeverityLevel.MINOR: "minor impact",
        SeverityLevel.MODERATE: "moderate impact",
        SeverityLevel.MAJOR: "significant impact",
        SeverityLevel.CRITICAL: "critical impact",
    }
    parts.append(level_text.get(level, "some impact"))

    # Key factors
    if factors.get("seasonal_mult", 1.0) > 1.2:
        parts.append(f"amplified by {seasonal_state} seasonal state")

    if factors.get("dm_relevance", 1.0) > 1.2:
        parts.append("directly affecting Day Master")

    if pillar_name == "day":
        parts.append("in personal Day pillar")
    elif pillar_name == "month":
        parts.append("in career Month pillar")

    return ". ".join(parts) + "."


def _generate_health_recommendation(
    affected_organs: List[Dict],
    severity: SeverityLevel,
) -> str:
    """Generate health recommendation based on affected organs."""
    if not affected_organs:
        return "No specific organ vulnerability detected."

    primary = affected_organs[0]
    organ = primary["zang"]
    element = primary["element"]

    recommendations = {
        "Wood": f"Support {organ} through gentle exercise, avoid anger, eat green vegetables",
        "Fire": f"Protect {organ} through adequate rest, manage anxiety, avoid excessive heat",
        "Earth": f"Strengthen {organ} through regular meals, reduce worry, avoid dampness",
        "Metal": f"Support {organ} through breathing exercises, process grief, protect from cold",
        "Water": f"Nourish {organ} through adequate hydration, manage fear, get sufficient rest",
    }

    base_rec = recommendations.get(element, f"Support {organ} function")

    if severity in [SeverityLevel.MAJOR, SeverityLevel.CRITICAL]:
        return f"IMPORTANT: {base_rec}. Consider consulting a healthcare provider."

    return base_rec


def _generate_wealth_recommendation(
    severity: SeverityLevel,
    seasonal_state: str,
) -> str:
    """Generate wealth recommendation based on severity."""
    if severity == SeverityLevel.CRITICAL:
        return "High financial volatility expected. Avoid major investments. Preserve capital."
    elif severity == SeverityLevel.MAJOR:
        return "Financial caution advised. Review investments and reduce risk exposure."
    elif severity == SeverityLevel.MODERATE:
        return "Minor financial fluctuations possible. Maintain diversified portfolio."
    else:
        return "Financial outlook stable. Normal business operations can continue."


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Multipliers
    "DISTANCE_MULTIPLIERS",
    "SEASONAL_STATE_MULTIPLIERS",
    "PILLAR_POSITION_MULTIPLIERS",
    "PATTERN_CATEGORY_WEIGHTS",

    # Classes
    "SeverityResult",

    # Functions
    "calculate_pattern_severity",
    "calculate_compound_severity",
    "calculate_health_severity",
    "calculate_wealth_severity",
]
