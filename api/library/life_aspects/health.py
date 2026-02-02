# * =========================
# * LIFE ASPECTS - HEALTH MODULE
# * =========================
# TCM (Traditional Chinese Medicine) organ-element correlations
# for BaZi health vulnerability analysis.
#
# Analyzes:
# 1. Direct conflicts (clashes, punishments, harms) → immediate stress
# 2. Control cycle imbalances (weak controller → imbalanced controlled)
# 3. Seasonal vulnerability (Dead/Trapped states)
# 4. Pillar position context (which relationship, which life period)

from typing import Dict, List, Optional

# Import base utilities
from .base import (
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    ELEMENT_CONTROLS,
    STEM_TO_ELEMENT,
    stems_to_element_totals,
    get_node_relationship_context,
    detect_control_imbalances,
    calculate_aspect_severity,
    # Centralized translations
    ELEMENT_NAMES,
    SEASONAL_STATES,
    ORGAN_SYSTEMS,
    get_element_name,
    get_seasonal_state,
    get_organ_system,
    get_body_parts,
)

# Import from parent library
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import STEMS, BRANCHES

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
        "system_chinese": "肝膽系統",
        "body_parts": ["eyes", "tendons", "nails"],
        "body_parts_chinese": ["眼", "筋", "指甲"],
        "emotion": "anger",
        "emotion_chinese": "怒",
    },
    "Fire": {
        "zang": "Heart",
        "fu": "Small Intestine",
        "chinese_zang": "心",
        "chinese_fu": "小腸",
        "system": "Cardiovascular",
        "system_chinese": "心血管系統",
        "body_parts": ["tongue", "blood vessels", "complexion"],
        "body_parts_chinese": ["舌", "血管", "面色"],
        "emotion": "joy/anxiety",
        "emotion_chinese": "喜/焦慮",
    },
    "Earth": {
        "zang": "Spleen",
        "fu": "Stomach",
        "chinese_zang": "脾",
        "chinese_fu": "胃",
        "system": "Digestive",
        "system_chinese": "消化系統",
        "body_parts": ["muscles", "mouth", "lips"],
        "body_parts_chinese": ["肌肉", "口", "唇"],
        "emotion": "worry",
        "emotion_chinese": "思/憂",
    },
    "Metal": {
        "zang": "Lungs",
        "fu": "Large Intestine",
        "chinese_zang": "肺",
        "chinese_fu": "大腸",
        "system": "Respiratory",
        "system_chinese": "呼吸系統",
        "body_parts": ["skin", "nose", "body hair"],
        "body_parts_chinese": ["皮膚", "鼻", "體毛"],
        "emotion": "grief",
        "emotion_chinese": "悲",
    },
    "Water": {
        "zang": "Kidneys",
        "fu": "Bladder",
        "chinese_zang": "腎",
        "chinese_fu": "膀胱",
        "system": "Urinary/Reproductive",
        "system_chinese": "泌尿生殖系統",
        "body_parts": ["bones", "ears", "hair"],
        "body_parts_chinese": ["骨", "耳", "頭髮"],
        "emotion": "fear",
        "emotion_chinese": "恐",
    },
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
        if len(parts) < 3:
            continue

        # Extract the item names (e.g., "Wu-Zi" or "Geng-Jia")
        items_part = parts[1]
        items = items_part.split("-")

        # Extract node IDs (e.g., "eb_y-eb_d")
        nodes_part = parts[2]
        nodes = nodes_part.split("-")

        for i, item in enumerate(items):
            # Get node context if available
            node_id = nodes[i] if i < len(nodes) else None
            node_context = get_node_relationship_context(node_id) if node_id else {}

            # Try to get element from stem or branch
            if item in STEMS:
                elem = STEMS[item].get("element", "")
                if elem in element_conflicts:
                    element_conflicts[elem].append({
                        "type": int_type,
                        "id": int_id,
                        "participant": item,
                        "participant_type": "stem",
                        "node_id": node_id,
                        "pillar": node_context.get("pillar", ""),
                        "represents": node_context.get("represents", ""),
                        "life_domain": node_context.get("life_domain", ""),
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
                                "participant_type": "branch",
                                "node_id": node_id,
                                "pillar": node_context.get("pillar", ""),
                                "represents": node_context.get("represents", ""),
                                "life_domain": node_context.get("life_domain", ""),
                            })

    return element_conflicts


def detect_vulnerable_elements(
    interactions: Dict,
    post_scores: Dict[str, float],
    natal_scores: Dict[str, float],
    seasonal_states: Dict[str, str]
) -> List[dict]:
    """
    Identify elements under significant stress.

    Returns list of vulnerable element info sorted by severity.
    Uses conflict count, seasonal state, and control imbalances.
    """
    vulnerabilities = []
    element_conflicts = aggregate_conflicts_by_element(interactions)

    # Convert stem scores to element totals
    post_element_totals = stems_to_element_totals(post_scores)
    natal_element_totals = stems_to_element_totals(natal_scores)

    # Get control imbalances
    control_imbalances = detect_control_imbalances(seasonal_states, post_element_totals)

    # Create a set of elements affected by control imbalances
    imbalanced_elements = {im["uncontrolled_element"] for im in control_imbalances}

    for element, conflicts in element_conflicts.items():
        # Get seasonal state
        seasonal_state = seasonal_states.get(element, "Resting")
        seasonal_mod = SEASONAL_HEALTH_MODIFIER.get(seasonal_state, 1.0)

        # Calculate weighted score based on conflict count and type
        base_score = 0
        pillar_contexts = []
        for conflict in conflicts:
            int_type = conflict.get("type", "")
            weight = 0.5
            for neg_type, w in CONFLICT_HEALTH_WEIGHTS.items():
                if neg_type in int_type:
                    weight = w
                    break
            base_score += weight * 10

            # Collect pillar context
            if conflict.get("pillar") and conflict.get("represents"):
                pillar_contexts.append({
                    "pillar": conflict["pillar"],
                    "represents": conflict["represents"],
                    "conflict_type": int_type,
                })

        # Apply seasonal modifier
        adjusted_score = base_score * seasonal_mod

        # Check for control imbalances affecting this element
        relevant_imbalances = [im for im in control_imbalances if im["uncontrolled_element"] == element]

        # Add imbalance impact to score
        for imbalance in relevant_imbalances:
            if imbalance["severity"] == "elevated":
                adjusted_score += 20
            else:
                adjusted_score += 12

        # Determine severity
        conflict_count = len(conflicts)
        has_imbalance = element in imbalanced_elements

        if adjusted_score > 30 or (conflict_count >= 3 and seasonal_state in ["Trapped", "Dead"]) or (has_imbalance and seasonal_state == "Dead"):
            severity = "severe"
        elif adjusted_score > 15 or conflict_count >= 2 or has_imbalance:
            severity = "moderate"
        elif adjusted_score > 0:
            severity = "mild"
        else:
            continue  # Skip if no issues

        # Only include if at least mild or has imbalance or trapped/dead
        if severity in ["moderate", "severe"] or has_imbalance or seasonal_state in ["Trapped", "Dead"]:
            organ_info = ELEMENT_ORGANS.get(element, {})

            # Calculate element score change
            post_total = post_element_totals.get(element, 0)
            natal_total = natal_element_totals.get(element, 0)
            score_change = post_total - natal_total

            vulnerabilities.append({
                "element": element,
                "element_chinese": {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}.get(element, ""),
                "organ_system": organ_info.get("system", ""),
                "organ_system_chinese": organ_info.get("system_chinese", ""),
                "zang_organ": organ_info.get("zang", ""),
                "fu_organ": organ_info.get("fu", ""),
                "chinese_zang": organ_info.get("chinese_zang", ""),
                "chinese_fu": organ_info.get("chinese_fu", ""),
                "body_parts": organ_info.get("body_parts", []),
                "body_parts_chinese": organ_info.get("body_parts_chinese", []),
                "severity": severity,
                "conflict_count": conflict_count,
                "weighted_score": round(adjusted_score, 1),
                "seasonal_state": seasonal_state,
                "seasonal_modifier": seasonal_mod,
                "element_score": post_total,
                "score_change": round(score_change, 1),
                "contributing_conflicts": [c.get("type", "") for c in conflicts[:5]],
                "pillar_contexts": pillar_contexts[:3],  # Top 3 pillar contexts
                "control_imbalances": relevant_imbalances,
                "has_control_imbalance": has_imbalance,
            })

    # Sort by severity (severe > moderate > mild), then by weighted_score descending
    severity_order = {"severe": 0, "moderate": 1, "mild": 2}
    vulnerabilities.sort(key=lambda x: (severity_order.get(x["severity"], 3), -x["weighted_score"]))

    return vulnerabilities


def generate_analysis_text(
    warnings: List[dict],
    control_imbalances: List[dict],
    severity_score: float,
    daymaster_element: str
) -> Dict[str, str]:
    """Generate 2-3 sentence natural language summary in all 3 languages.

    Returns:
        Dict with keys 'en', 'zh', 'id' containing analysis text in each language.
    """
    # Balanced state messages
    if not warnings and not control_imbalances:
        return {
            "en": "Overall health picture is balanced with no significant organ system vulnerabilities detected in this period.",
            "zh": "整體健康狀況良好，此期間無明顯器官系統弱點。",
            "id": "Gambaran kesehatan secara keseluruhan seimbang, tidak ada kerentanan sistem organ yang signifikan terdeteksi pada periode ini.",
        }

    parts_en = []
    parts_zh = []
    parts_id = []

    # Check for control imbalances first (more important insight)
    if control_imbalances:
        primary_imbalance = control_imbalances[0]
        weak = primary_imbalance["weak_controller"]
        uncontrolled = primary_imbalance["uncontrolled_element"]
        organ_info = ELEMENT_ORGANS.get(uncontrolled, {})
        system = organ_info.get("system", uncontrolled)
        body_parts_en = organ_info.get("body_parts", [])

        # English
        bp_str = f" ({', '.join(body_parts_en[:2])})" if body_parts_en else ""
        parts_en.append(f"{weak} element is too weak to control {uncontrolled}, potentially affecting {get_organ_system(system, 'en')} system{bp_str}.")

        # Chinese
        weak_zh = get_element_name(weak, 'zh')
        uncontrolled_zh = get_element_name(uncontrolled, 'zh')
        system_zh = get_organ_system(system, 'zh')
        bp_zh = get_body_parts(uncontrolled, 'zh')
        bp_str_zh = f"（{', '.join(bp_zh[:2])}）" if bp_zh else ""
        parts_zh.append(f"{weak_zh}元素太弱無法控制{uncontrolled_zh}，可能影響{system_zh}{bp_str_zh}。")

        # Indonesian
        weak_id = get_element_name(weak, 'id')
        uncontrolled_id = get_element_name(uncontrolled, 'id')
        system_id = get_organ_system(system, 'id')
        bp_id = get_body_parts(uncontrolled, 'id')
        bp_str_id = f" ({', '.join(bp_id[:2])})" if bp_id else ""
        parts_id.append(f"Elemen {weak_id} terlalu lemah untuk mengendalikan {uncontrolled_id}, berpotensi mempengaruhi sistem {system_id}{bp_str_id}.")

    # Add direct conflict warnings
    if warnings:
        primary = warnings[0]
        element = primary["element"]
        system = primary["organ_system"]
        severity = primary["severity"]
        seasonal = primary["seasonal_state"]

        # Only add if not already covered by control imbalance
        if not control_imbalances or primary["element"] != control_imbalances[0]["uncontrolled_element"]:
            if severity == "severe":
                parts_en.append(f"Significant stress on {get_organ_system(system, 'en')} system ({element}).")
                parts_zh.append(f"{get_organ_system(system, 'zh')}承受重大壓力（{get_element_name(element, 'zh')}）。")
                parts_id.append(f"Tekanan signifikan pada sistem {get_organ_system(system, 'id')} ({get_element_name(element, 'id')}).")
            elif severity == "moderate":
                parts_en.append(f"Moderate pressure on {get_organ_system(system, 'en')} system.")
                parts_zh.append(f"{get_organ_system(system, 'zh')}承受中等壓力。")
                parts_id.append(f"Tekanan sedang pada sistem {get_organ_system(system, 'id')}.")

        # Add seasonal context if trapped/dead
        weak_controllers = [im["weak_controller"] for im in control_imbalances] if control_imbalances else []
        if seasonal in ["Trapped", "Dead"] and element not in weak_controllers:
            parts_en.append(f"{element} in '{seasonal}' state increases vulnerability.")
            parts_zh.append(f"{get_element_name(element, 'zh')}處於「{get_seasonal_state(seasonal, 'zh')}」狀態，增加脆弱性。")
            parts_id.append(f"{get_element_name(element, 'id')} dalam kondisi '{get_seasonal_state(seasonal, 'id')}' meningkatkan kerentanan.")

    # Add day master context if relevant
    if daymaster_element:
        affected_elements = [w["element"] for w in warnings]
        if daymaster_element in affected_elements:
            parts_en.append("As this affects your Day Master element, self-care is especially important.")
            parts_zh.append("由於這影響您的日主元素，自我保健尤為重要。")
            parts_id.append("Karena ini mempengaruhi elemen Day Master Anda, perawatan diri sangat penting.")

        # Check if daymaster is the weak controller
        for im in control_imbalances:
            if im["weak_controller"] == daymaster_element:
                parts_en.append("Your Day Master element being weak requires attention to the areas it governs.")
                parts_zh.append("您的日主元素較弱，需要關注其所管轄的領域。")
                parts_id.append("Elemen Day Master Anda yang lemah memerlukan perhatian pada area yang diaturnya.")
                break

    return {
        "en": " ".join(parts_en[:4]),
        "zh": " ".join(parts_zh[:4]),
        "id": " ".join(parts_id[:4]),
    }


def generate_health_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    natal_element_score: Dict[str, float],
    month_branch: str,
    daymaster_element: str
) -> dict:
    """
    Main function: Analyze chart interactions for health impact.

    Analyzes three dimensions:
    1. Direct conflicts (clashes, punishments, harms)
    2. Control cycle imbalances (weak Fire → Metal issues)
    3. Seasonal vulnerability (Dead/Trapped states)

    Returns dict with:
    - health_warnings: List of vulnerable elements with organ info
    - control_imbalances: List of Wu Xing control cycle issues
    - conflict_severity_score: 0-100 severity score
    - most_vulnerable_element: Primary element of concern
    - seasonal_vulnerability: Element seasonal states
    - analysis_text: Natural language summary
    """
    # Get seasonal states
    seasonal_states = get_element_seasonal_states(month_branch)

    # Convert stem scores to element totals
    post_element_totals = stems_to_element_totals(post_element_score)

    # Detect control cycle imbalances (THE KEY FIX)
    control_imbalances = detect_control_imbalances(seasonal_states, post_element_totals)

    # Detect vulnerable elements (includes both conflicts and imbalances)
    warnings = detect_vulnerable_elements(
        interactions,
        post_element_score,
        natal_element_score,
        seasonal_states
    )

    # Calculate overall severity
    total_conflicts = sum(len(aggregate_conflicts_by_element(interactions)[e]) for e in ELEMENT_ORGANS.keys())
    dm_seasonal = seasonal_states.get(daymaster_element, "Resting")
    severity_score, severity_category = calculate_aspect_severity(
        total_conflicts,
        dm_seasonal,
        control_imbalances
    )

    # Find most vulnerable - prioritize control imbalances
    if control_imbalances:
        most_vulnerable = control_imbalances[0]["uncontrolled_element"]
    elif warnings:
        most_vulnerable = warnings[0]["element"]
    else:
        most_vulnerable = None

    # Generate multilingual text
    analysis_texts = generate_analysis_text(warnings, control_imbalances, severity_score, daymaster_element)

    return {
        "health_warnings": warnings,
        "control_imbalances": control_imbalances,
        "conflict_severity_score": round(severity_score, 1),
        "severity_category": severity_category,
        "most_vulnerable_element": most_vulnerable,
        "seasonal_vulnerability": seasonal_states,
        "element_totals": post_element_totals,
        # Multilingual analysis text
        "analysis_text": analysis_texts["en"],
        "analysis_text_chinese": analysis_texts["zh"],
        "analysis_text_id": analysis_texts["id"],
    }
