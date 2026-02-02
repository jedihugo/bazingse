# * =========================
# * HEALTH ANALYSIS MODULE
# * =========================
# TCM (Traditional Chinese Medicine) organ-element correlations
# for BaZi health vulnerability analysis

from typing import Dict, List, Optional
from .core import BRANCHES, STEMS

# * -------------------------
# * TCM ELEMENT-ORGAN MAPPING
# * -------------------------
# Each element governs specific organ pairs (Zang-Fu theory)

ELEMENT_ORGANS = {
    "Wood": {
        "zang": "Liver",
        "fu": "Gallbladder",
        "chinese_zang": "肝",
        "chinese_fu": "膽",
        "system": "Hepatobiliary",
        "body_parts": ["eyes", "tendons", "nails"],
        "emotion": "anger"
    },
    "Fire": {
        "zang": "Heart",
        "fu": "Small Intestine",
        "chinese_zang": "心",
        "chinese_fu": "小腸",
        "system": "Cardiovascular",
        "body_parts": ["tongue", "blood vessels", "complexion"],
        "emotion": "joy/anxiety"
    },
    "Earth": {
        "zang": "Spleen",
        "fu": "Stomach",
        "chinese_zang": "脾",
        "chinese_fu": "胃",
        "system": "Digestive",
        "body_parts": ["muscles", "mouth", "lips"],
        "emotion": "worry"
    },
    "Metal": {
        "zang": "Lungs",
        "fu": "Large Intestine",
        "chinese_zang": "肺",
        "chinese_fu": "大腸",
        "system": "Respiratory",
        "body_parts": ["skin", "nose", "body hair"],
        "emotion": "grief"
    },
    "Water": {
        "zang": "Kidneys",
        "fu": "Bladder",
        "chinese_zang": "腎",
        "chinese_fu": "膀胱",
        "system": "Urinary/Reproductive",
        "body_parts": ["bones", "ears", "hair"],
        "emotion": "fear"
    }
}

# * -------------------------
# * CONFLICT SEVERITY WEIGHTS
# * -------------------------

CONFLICT_HEALTH_WEIGHTS = {
    "CLASH": 1.0,
    "PUNISHMENT": 0.85,
    "HARM": 0.70,
    "DESTRUCTION": 0.50,
    "STEM_CONFLICT": 0.60,
}

# * -------------------------
# * SEASONAL HEALTH MODIFIERS
# * -------------------------
# Elements in "Trapped" or "Dead" state are more vulnerable

SEASONAL_HEALTH_MODIFIER = {
    "Prosperous": 0.5,
    "Strengthening": 0.7,
    "Resting": 1.0,
    "Trapped": 1.5,
    "Dead": 2.0,
}


def get_element_seasonal_states(month_branch: str) -> Dict[str, str]:
    """Get seasonal state for each element based on month branch."""
    if not month_branch or month_branch not in BRANCHES:
        return {elem: "Resting" for elem in ELEMENT_ORGANS.keys()}

    return BRANCHES[month_branch].get("element_states", {})


def get_stem_element(stem_id: str) -> str:
    """Get element from stem ID."""
    if stem_id in STEMS:
        return STEMS[stem_id].get("element", "")
    return ""


def aggregate_conflicts_by_element(interactions: Dict) -> Dict[str, List[dict]]:
    """
    Group negative interactions by the element they damage.

    Returns: {element: [list of conflict info]}

    Interaction ID format: TYPE~ITEM1-ITEM2~node1-node2
    Examples:
    - CLASH~Wu-Zi~eb_y-eb_d (branch clash: Wu vs Zi)
    - STEM_CONFLICT~Geng-Jia~hs_d-hs_ml (stem conflict: Geng vs Jia)
    """
    element_conflicts = {elem: [] for elem in ELEMENT_ORGANS.keys()}

    for int_id, interaction in interactions.items():
        if isinstance(interaction, str):
            continue

        int_type = interaction.get("type", "")

        # Only process negative interactions
        negative_types = ["CLASH", "PUNISHMENT", "HARM", "DESTRUCTION", "STEM_CONFLICT"]
        is_negative = any(neg in int_type for neg in negative_types)

        if not is_negative:
            continue

        # Parse stem/branch IDs from interaction ID (e.g., "CLASH~Wu-Zi~eb_y-eb_d")
        parts = int_id.split("~")
        if len(parts) < 2:
            continue

        # Extract the item names (e.g., "Wu-Zi" or "Geng-Jia")
        items_part = parts[1]
        items = items_part.split("-")

        for item in items:
            # Try to get element from stem or branch
            if item in STEMS:
                elem = STEMS[item].get("element", "")
                if elem in element_conflicts:
                    element_conflicts[elem].append({
                        "type": int_type,
                        "id": int_id,
                        "participant": item,
                        "damage": interaction.get("damage", interaction.get("reduction", 0))
                    })
            elif item in BRANCHES:
                # Use primary qi element
                hidden_qi = BRANCHES[item].get("hidden_qi", [])
                if hidden_qi:
                    primary_stem = hidden_qi[0].get("stem", "")
                    if primary_stem in STEMS:
                        elem = STEMS[primary_stem].get("element", "")
                        if elem in element_conflicts:
                            element_conflicts[elem].append({
                                "type": int_type,
                                "id": int_id,
                                "participant": item,
                                "damage": interaction.get("damage", interaction.get("reduction", 0))
                            })

    return element_conflicts


def calculate_conflict_severity(
    interactions: Dict,
    seasonal_states: Dict[str, str]
) -> float:
    """Calculate overall conflict severity score (0-100).

    Uses conflict count and type weights since damage values
    may not be available in all interaction formats.
    """
    total_weighted_score = 0

    element_conflicts = aggregate_conflicts_by_element(interactions)

    for element, conflicts in element_conflicts.items():
        seasonal_state = seasonal_states.get(element, "Resting")
        seasonal_mod = SEASONAL_HEALTH_MODIFIER.get(seasonal_state, 1.0)

        for conflict in conflicts:
            int_type = conflict.get("type", "")

            # Get base weight for conflict type
            base_weight = 0.5
            for neg_type, weight in CONFLICT_HEALTH_WEIGHTS.items():
                if neg_type in int_type:
                    base_weight = weight
                    break

            # Use base score of 10 per conflict (since damage values may not be available)
            base_score = 10
            total_weighted_score += base_weight * base_score * seasonal_mod

    # Normalize to 0-100 (calibrated for typical charts with ~10-20 conflicts)
    max_expected = 100
    return min(100, (total_weighted_score / max_expected) * 100)


def detect_vulnerable_elements(
    interactions: Dict,
    post_scores: Dict[str, float],
    natal_scores: Dict[str, float],
    seasonal_states: Dict[str, str]
) -> List[dict]:
    """
    Identify elements under significant stress.

    Returns list of vulnerable element info sorted by severity.
    Uses conflict count and seasonal state to determine severity.
    """
    vulnerabilities = []
    element_conflicts = aggregate_conflicts_by_element(interactions)

    for element, conflicts in element_conflicts.items():
        if len(conflicts) < 1:
            continue

        conflict_count = len(conflicts)

        # Get seasonal state
        seasonal_state = seasonal_states.get(element, "Resting")
        seasonal_mod = SEASONAL_HEALTH_MODIFIER.get(seasonal_state, 1.0)

        # Calculate weighted score based on conflict count and type
        base_score = 0
        for conflict in conflicts:
            int_type = conflict.get("type", "")
            weight = 0.5
            for neg_type, w in CONFLICT_HEALTH_WEIGHTS.items():
                if neg_type in int_type:
                    weight = w
                    break
            base_score += weight * 10  # Base 10 points per conflict

        # Apply seasonal modifier
        adjusted_score = base_score * seasonal_mod

        # Determine severity based on adjusted score and seasonal state
        if adjusted_score > 30 or (conflict_count >= 3 and seasonal_state in ["Trapped", "Dead"]):
            severity = "severe"
        elif adjusted_score > 15 or conflict_count >= 2:
            severity = "moderate"
        else:
            severity = "mild"

        # Only include if at least moderate or trapped/dead
        if severity in ["moderate", "severe"] or seasonal_state in ["Trapped", "Dead"]:
            organ_info = ELEMENT_ORGANS.get(element, {})
            vulnerabilities.append({
                "element": element,
                "organ_system": organ_info.get("system", ""),
                "zang_organ": organ_info.get("zang", ""),
                "fu_organ": organ_info.get("fu", ""),
                "chinese_zang": organ_info.get("chinese_zang", ""),
                "chinese_fu": organ_info.get("chinese_fu", ""),
                "severity": severity,
                "conflict_count": conflict_count,
                "weighted_score": round(adjusted_score, 1),
                "seasonal_state": seasonal_state,
                "seasonal_modifier": seasonal_mod,
                "contributing_conflicts": [c.get("type", "") for c in conflicts[:5]]
            })

    # Sort by severity (severe > moderate > mild), then by weighted_score descending
    severity_order = {"severe": 0, "moderate": 1, "mild": 2}
    vulnerabilities.sort(key=lambda x: (severity_order.get(x["severity"], 3), -x["weighted_score"]))

    return vulnerabilities


def generate_analysis_text(
    warnings: List[dict],
    severity_score: float,
    daymaster_element: str
) -> str:
    """Generate 2-3 sentence natural language summary."""

    if not warnings:
        return "Overall health picture is balanced with no significant organ system vulnerabilities detected in this period."

    # Get most severe warning
    primary = warnings[0]
    element = primary["element"]
    system = primary["organ_system"]
    zang = primary["zang_organ"]
    fu = primary["fu_organ"]
    chinese = primary["chinese_zang"]
    severity = primary["severity"]
    seasonal = primary["seasonal_state"]
    count = primary["conflict_count"]

    # Build analysis text
    parts = []

    if severity == "severe":
        parts.append(f"This period shows significant stress on the {system} system ({element}/{chinese}).")
        parts.append(f"{count} conflicts converge on {zang} and {fu}.")
    elif severity == "moderate":
        parts.append(f"Moderate pressure detected on {system} system ({element} element).")
        parts.append(f"{zang}/{fu} function may need attention.")
    else:
        parts.append(f"Minor {element} element fluctuations noted affecting {system} system.")

    # Add seasonal context if trapped/dead
    if seasonal in ["Trapped", "Dead"]:
        parts.append(f"The seasonal '{seasonal}' state amplifies vulnerability.")

    # Add day master context if relevant
    if daymaster_element == element:
        parts.append("As this affects your Day Master element, self-care is especially important.")

    # Multiple warnings
    if len(warnings) > 1:
        other_systems = [w["organ_system"] for w in warnings[1:3]]
        if other_systems:
            parts.append(f"Also monitor: {', '.join(other_systems)}.")

    return " ".join(parts[:3])


def generate_health_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    natal_element_score: Dict[str, float],
    month_branch: str,
    daymaster_element: str
) -> dict:
    """
    Main function: Analyze chart interactions for health impact.

    Returns dict with health_warnings, conflict_severity_score, analysis_text
    """
    # Get seasonal states
    seasonal_states = get_element_seasonal_states(month_branch)

    # Calculate severity
    severity_score = calculate_conflict_severity(interactions, seasonal_states)

    # Detect vulnerable elements
    warnings = detect_vulnerable_elements(
        interactions,
        post_element_score,
        natal_element_score,
        seasonal_states
    )

    # Find most vulnerable
    most_vulnerable = warnings[0]["element"] if warnings else None

    # Generate text
    analysis_text = generate_analysis_text(warnings, severity_score, daymaster_element)

    return {
        "health_warnings": warnings,
        "conflict_severity_score": round(severity_score, 1),
        "most_vulnerable_element": most_vulnerable,
        "seasonal_vulnerability": seasonal_states,
        "analysis_text": analysis_text
    }
