# * =========================
# * NARRATIVE MODIFIERS
# * =========================
# Applies contextual modifiers to narratives based on:
# - Element balance (excess/deficiency)
# - Shen Sha (special stars) presence
# - Daymaster strength
# - Seasonal timing
# - Ten Gods relationships and their meanings

from typing import Dict, Any, List, Optional, Tuple

# =============================================================================
# ELEMENT BALANCE THRESHOLDS
# =============================================================================
# Used to determine if an element is in excess or deficient

BALANCE_THRESHOLDS = {
    "severe_excess": 35.0,    # >35% of total qi
    "moderate_excess": 28.0,  # >28% of total qi
    "balanced_upper": 24.0,   # Upper bound of balance
    "balanced_lower": 16.0,   # Lower bound of balance
    "moderate_deficiency": 12.0,  # <12% of total qi
    "severe_deficiency": 8.0,     # <8% of total qi
}

# =============================================================================
# TEN GODS RELATIONSHIPS (十神)
# =============================================================================
# Maps daymaster element to its Ten Gods relationships

TEN_GODS_FOR_ELEMENT = {
    # For Fire daymaster
    "Fire": {
        "Wood": "resource",      # 印/枭 - Resource/Indirect Resource
        "Fire": "companion",     # 比/劫 - Friend/Rob Wealth
        "Earth": "output",       # 食/伤 - Eating God/Hurting Officer
        "Metal": "wealth",       # 财 - Direct/Indirect Wealth
        "Water": "officer",      # 官/杀 - Direct Officer/Seven Killings
    },
    "Wood": {
        "Water": "resource",
        "Wood": "companion",
        "Fire": "output",
        "Earth": "wealth",
        "Metal": "officer",
    },
    "Earth": {
        "Fire": "resource",
        "Earth": "companion",
        "Metal": "output",
        "Water": "wealth",
        "Wood": "officer",
    },
    "Metal": {
        "Earth": "resource",
        "Metal": "companion",
        "Water": "output",
        "Wood": "wealth",
        "Fire": "officer",
    },
    "Water": {
        "Metal": "resource",
        "Water": "companion",
        "Wood": "output",
        "Fire": "wealth",
        "Earth": "officer",
    },
}

# Ten Gods excess meanings - what happens when a Ten God is too strong
TEN_GODS_EXCESS_MEANING = {
    "output": {  # Eating God/Hurting Officer (食伤)
        "en": "overthinking, perfectionism, pickiness, slow to decide/act, hard to settle",
        "zh": "过度思虑、完美主义、挑剔、行动迟缓、难以安定",
        "traits": ["perfectionist", "overthinking", "picky", "slow to act"],
    },
    "resource": {  # Resource/Seal (印)
        "en": "over-dependence, passivity, laziness, expecting others to help",
        "zh": "过度依赖、被动、懒惰、期待他人帮助",
        "traits": ["dependent", "passive", "lazy"],
    },
    "companion": {  # Friend/Rob Wealth (比劫)
        "en": "stubbornness, competition, jealousy, difficulty with sharing",
        "zh": "固执、争强好胜、嫉妒、不善分享",
        "traits": ["stubborn", "competitive", "jealous"],
    },
    "wealth": {  # Wealth (财)
        "en": "materialism, greed, overwork for money, neglecting relationships",
        "zh": "物质主义、贪婪、为钱过度工作、忽视感情",
        "traits": ["materialistic", "greedy", "workaholic"],
    },
    "officer": {  # Officer/Seven Killings (官杀)
        "en": "pressure, stress, feeling controlled, authority conflicts",
        "zh": "压力、紧张、被控制感、权威冲突",
        "traits": ["stressed", "pressured", "controlled"],
    },
}

# =============================================================================
# ELEMENT GENERATION/CONTROL CYCLES
# =============================================================================

ELEMENT_GENERATES = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood",
}

ELEMENT_CONTROLS = {
    "Wood": "Earth",
    "Fire": "Metal",
    "Earth": "Water",
    "Metal": "Wood",
    "Water": "Fire",
}

ELEMENT_GENERATED_BY = {v: k for k, v in ELEMENT_GENERATES.items()}
ELEMENT_CONTROLLED_BY = {v: k for k, v in ELEMENT_CONTROLS.items()}


def get_element_balance_context(
    post_element_score: Dict[str, float],
    daymaster_element: str,
    daymaster_analysis: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze element balance and return context for narrative generation.

    CRITICAL: Element excess OVERRIDES theoretical favorability.
    If an element is already excessive (>28%), it becomes UNFAVORABLE
    regardless of what daymaster strength suggests.

    Args:
        post_element_score: Dict of stem -> qi score (e.g., {"Jia": 150.5, "Yi": 80.2, ...})
        daymaster_element: The daymaster's element (e.g., "Wood")
        daymaster_analysis: Full daymaster analysis from bazingse.py (contains correct favorable/unfavorable)

    Returns:
        Dict containing:
            - element_percentages: Dict of element -> percentage
            - excess_elements: List of elements in excess with severity
            - deficient_elements: List of elements deficient with severity
            - balance_assessment: Overall balance assessment
            - favorable_elements: Elements that help balance (ADJUSTED for excess)
            - unfavorable_elements: Elements that worsen imbalance (ADJUSTED for excess)
            - daymaster_strength: Strength level from daymaster_analysis
            - ten_god_context: Ten God relationships for interpretation
    """
    # Convert stem scores to element totals
    element_totals = _stems_to_elements(post_element_score)

    # Calculate total and percentages
    total_qi = sum(element_totals.values())
    if total_qi == 0:
        return {
            "element_percentages": {},
            "excess_elements": [],
            "deficient_elements": [],
            "balance_assessment": "unknown",
            "favorable_elements": [],
            "unfavorable_elements": [],
            "daymaster_strength": "Unknown",
            "ten_god_context": {},
        }

    percentages = {
        element: (qi / total_qi) * 100
        for element, qi in element_totals.items()
    }

    # Identify excess and deficient elements
    excess_elements = []
    deficient_elements = []
    excess_element_names = set()  # Track for favorability override

    for element, pct in percentages.items():
        # Get Ten God relationship for this element
        ten_god = TEN_GODS_FOR_ELEMENT.get(daymaster_element, {}).get(element, "")
        ten_god_meaning = TEN_GODS_EXCESS_MEANING.get(ten_god, {})

        if pct >= BALANCE_THRESHOLDS["severe_excess"]:
            excess_elements.append({
                "element": element,
                "percentage": round(pct, 1),
                "severity": "severe",
                "controller": ELEMENT_CONTROLLED_BY.get(element, ""),
                "ten_god": ten_god,
                "ten_god_excess_meaning": ten_god_meaning.get("en", ""),
                "ten_god_excess_meaning_zh": ten_god_meaning.get("zh", ""),
            })
            excess_element_names.add(element)
        elif pct >= BALANCE_THRESHOLDS["moderate_excess"]:
            excess_elements.append({
                "element": element,
                "percentage": round(pct, 1),
                "severity": "moderate",
                "controller": ELEMENT_CONTROLLED_BY.get(element, ""),
                "ten_god": ten_god,
                "ten_god_excess_meaning": ten_god_meaning.get("en", ""),
                "ten_god_excess_meaning_zh": ten_god_meaning.get("zh", ""),
            })
            excess_element_names.add(element)

        if pct <= BALANCE_THRESHOLDS["severe_deficiency"]:
            deficient_elements.append({
                "element": element,
                "percentage": round(pct, 1),
                "severity": "severe",
                "producer": ELEMENT_GENERATED_BY.get(element, ""),
            })
        elif pct <= BALANCE_THRESHOLDS["moderate_deficiency"]:
            deficient_elements.append({
                "element": element,
                "percentage": round(pct, 1),
                "severity": "moderate",
                "producer": ELEMENT_GENERATED_BY.get(element, ""),
            })

    # Determine overall balance assessment
    if len(excess_elements) == 0 and len(deficient_elements) == 0:
        balance_assessment = "balanced"
    elif any(e["severity"] == "severe" for e in excess_elements + deficient_elements):
        balance_assessment = "severely_imbalanced"
    else:
        balance_assessment = "moderately_imbalanced"

    # Get base favorable/unfavorable from daymaster_analysis
    if daymaster_analysis:
        base_favorable = list(daymaster_analysis.get("favorable_elements", []))
        base_unfavorable = list(daymaster_analysis.get("unfavorable_elements", []))
        daymaster_strength = daymaster_analysis.get("daymaster_strength", "Balanced")
    else:
        base_favorable, base_unfavorable = _determine_favorable_elements(
            daymaster_element,
            excess_elements,
            deficient_elements,
            percentages
        )
        daymaster_strength = "Unknown"

    # CRITICAL: Override favorability based on actual element excess
    # If an element is already excessive, it CANNOT be favorable
    # because adding more of it will only worsen the imbalance
    favorable = []
    unfavorable = list(base_unfavorable)

    for elem in base_favorable:
        if elem in excess_element_names:
            # Element is excessive - move to unfavorable
            if elem not in unfavorable:
                unfavorable.append(elem)
        else:
            favorable.append(elem)

    # Also add all excess elements to unfavorable if not already there
    for elem in excess_element_names:
        if elem not in unfavorable:
            unfavorable.append(elem)

    # Build Ten God context for interpretation
    ten_god_context = {}
    if daymaster_element in TEN_GODS_FOR_ELEMENT:
        for elem, ten_god in TEN_GODS_FOR_ELEMENT[daymaster_element].items():
            ten_god_context[elem] = {
                "ten_god": ten_god,
                "is_excess": elem in excess_element_names,
                "percentage": round(percentages.get(elem, 0), 1),
            }
            if elem in excess_element_names:
                meaning = TEN_GODS_EXCESS_MEANING.get(ten_god, {})
                ten_god_context[elem]["excess_meaning"] = meaning.get("en", "")
                ten_god_context[elem]["excess_meaning_zh"] = meaning.get("zh", "")
                ten_god_context[elem]["traits"] = meaning.get("traits", [])

    return {
        "element_percentages": {k: round(v, 1) for k, v in percentages.items()},
        "excess_elements": excess_elements,
        "deficient_elements": deficient_elements,
        "balance_assessment": balance_assessment,
        "favorable_elements": favorable,
        "unfavorable_elements": unfavorable,
        "daymaster_strength": daymaster_strength,
        "ten_god_context": ten_god_context,
    }


def apply_element_modifiers(
    narrative: Dict[str, Any],
    element_context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply element balance modifiers to a narrative.

    This is CRITICAL for providing accurate interpretations:
    - A "positive" combination can be BAD if it generates an unfavorable/excessive element
    - A "negative" conflict involving excessive elements tells a specific story via Ten Gods
    - Element excess overrides theoretical favorability

    Args:
        narrative: The narrative dict to modify
        element_context: Element balance context from get_element_balance_context()

    Returns:
        Modified narrative with additional context including Ten God interpretation
    """
    narrative = dict(narrative)  # Don't modify original

    # Get the element involved in this interaction
    interaction_element = narrative.get("element", "")
    favorable_elements = element_context.get("favorable_elements", [])
    unfavorable_elements = element_context.get("unfavorable_elements", [])
    daymaster_strength = element_context.get("daymaster_strength", "Unknown")
    ten_god_context = element_context.get("ten_god_context", {})

    if not interaction_element:
        return narrative

    # Check if this element is in excess or deficient
    excess_info = next(
        (e for e in element_context.get("excess_elements", [])
         if e["element"] == interaction_element),
        None
    )
    deficient_info = next(
        (e for e in element_context.get("deficient_elements", [])
         if e["element"] == interaction_element),
        None
    )

    # Get Ten God info for this element
    ten_god_info = ten_god_context.get(interaction_element, {})
    ten_god_name = ten_god_info.get("ten_god", "")

    # Determine favorability (already adjusted for excess in get_element_balance_context)
    is_favorable = interaction_element in favorable_elements
    is_unfavorable = interaction_element in unfavorable_elements

    # Add Ten God context to narrative
    if ten_god_name:
        narrative["ten_god"] = ten_god_name
        narrative["ten_god_display"] = _ten_god_to_display(ten_god_name)

    # Add favorability context with Ten God interpretation
    if is_favorable:
        narrative["favorability"] = "favorable"
        narrative["favorability_note"] = f"{interaction_element} is favorable for your chart - this combination benefits you."
        narrative["favorability_note_zh"] = f"{_element_to_chinese(interaction_element)}对您的命盘有利 - 此组合对您有益。"
    elif is_unfavorable:
        narrative["favorability"] = "unfavorable"

        # Build comprehensive unfavorability explanation with Ten God context
        if excess_info:
            # Element is EXCESSIVE - this is the key insight
            pct = excess_info["percentage"]
            ten_god_meaning = excess_info.get("ten_god_excess_meaning", "")
            ten_god_meaning_zh = excess_info.get("ten_god_excess_meaning_zh", "")
            ten_god_display = _ten_god_to_display(ten_god_name)
            ten_god_display_zh = _ten_god_to_display_zh(ten_god_name)

            if ten_god_meaning:
                # Tell the complete story: element excess + Ten God meaning
                narrative["favorability_note"] = (
                    f"{interaction_element} is excessive ({pct}%) in your chart. "
                    f"As your {ten_god_display}, excessive {interaction_element} means: {ten_god_meaning}. "
                    f"This interaction amplifies the imbalance."
                )
                narrative["favorability_note_zh"] = (
                    f"{_element_to_chinese(interaction_element)}在您的命盘中过旺（{pct}%）。"
                    f"作为您的{ten_god_display_zh}，过多的{_element_to_chinese(interaction_element)}意味着：{ten_god_meaning_zh}。"
                    f"此互动加剧了失衡。"
                )
                # Store traits for UI use
                narrative["excess_traits"] = ten_god_info.get("traits", [])
            else:
                narrative["favorability_note"] = (
                    f"{interaction_element} is excessive ({pct}%) - adding more worsens the imbalance."
                )
                narrative["favorability_note_zh"] = (
                    f"{_element_to_chinese(interaction_element)}已过旺（{pct}%）- 增加更多会加剧失衡。"
                )
        else:
            # Not excess, but still unfavorable based on daymaster strength
            if daymaster_strength in ["Very Strong", "Strong"]:
                narrative["favorability_note"] = (
                    f"{interaction_element} is unfavorable - it strengthens an already strong daymaster."
                )
                narrative["favorability_note_zh"] = (
                    f"{_element_to_chinese(interaction_element)}不利 - 它增强了已经很强的日主。"
                )
            elif daymaster_strength in ["Weak", "Very Weak"]:
                narrative["favorability_note"] = (
                    f"{interaction_element} is unfavorable - it drains a weak daymaster."
                )
                narrative["favorability_note_zh"] = (
                    f"{_element_to_chinese(interaction_element)}不利 - 它消耗了虚弱的日主。"
                )
            else:
                narrative["favorability_note"] = (
                    f"{interaction_element} is unfavorable for your current chart balance."
                )
                narrative["favorability_note_zh"] = (
                    f"{_element_to_chinese(interaction_element)}对您当前的命盘平衡不利。"
                )

        # Override polarity for "positive" combinations that generate unfavorable elements
        if narrative.get("polarity") == "positive":
            narrative["effective_polarity"] = "negative"
            narrative["polarity_override_reason"] = "generates unfavorable/excessive element"
    else:
        narrative["favorability"] = "neutral"

    # Add element status context
    if excess_info:
        narrative["element_status"] = "excess"
        narrative["element_status_severity"] = excess_info["severity"]
        narrative["element_percentage"] = excess_info["percentage"]
    elif deficient_info:
        narrative["element_status"] = "deficient"
        narrative["element_status_severity"] = deficient_info["severity"]
        narrative["element_percentage"] = deficient_info["percentage"]
    else:
        narrative["element_status"] = "balanced"

    return narrative


def _ten_god_to_display(ten_god: str) -> str:
    """Convert ten god key to display name."""
    mapping = {
        "output": "Eating God (食伤)",
        "resource": "Resource (印)",
        "companion": "Friend/Rob Wealth (比劫)",
        "wealth": "Wealth (财)",
        "officer": "Officer (官杀)",
    }
    return mapping.get(ten_god, ten_god)


def _ten_god_to_display_zh(ten_god: str) -> str:
    """Convert ten god key to Chinese display name."""
    mapping = {
        "output": "食伤",
        "resource": "印",
        "companion": "比劫",
        "wealth": "财",
        "officer": "官杀",
    }
    return mapping.get(ten_god, ten_god)


def apply_shen_sha_modifiers(
    narrative: Dict[str, Any],
    special_stars: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Apply Shen Sha (special stars) modifiers to a narrative.

    Args:
        narrative: The narrative dict to modify
        special_stars: List of special stars from pattern_engine

    Returns:
        Modified narrative with Shen Sha context
    """
    narrative = dict(narrative)  # Don't modify original

    # Get nodes involved in this interaction
    interaction_nodes = narrative.get("nodes", [])

    if not interaction_nodes or not special_stars:
        return narrative

    # Find relevant stars (those affecting the same nodes)
    relevant_stars = []
    for star in special_stars:
        star_node = star.get("node", "")
        if star_node in interaction_nodes:
            relevant_stars.append({
                "name": star.get("name", ""),
                "chinese_name": star.get("chinese_name", ""),
                "effect": star.get("effect", ""),
                "polarity": star.get("polarity", "neutral"),
            })

    if relevant_stars:
        narrative["shen_sha"] = relevant_stars
        # Add summary note
        positive_stars = [s for s in relevant_stars if s["polarity"] == "positive"]
        negative_stars = [s for s in relevant_stars if s["polarity"] == "negative"]

        if positive_stars and not negative_stars:
            narrative["shen_sha_note"] = "Auspicious stars enhance this interaction"
            narrative["shen_sha_note_zh"] = "吉星增强此互动"
        elif negative_stars and not positive_stars:
            narrative["shen_sha_note"] = "Challenging stars complicate this interaction"
            narrative["shen_sha_note_zh"] = "凶星使此互动复杂化"
        elif positive_stars and negative_stars:
            narrative["shen_sha_note"] = "Mixed star influences present"
            narrative["shen_sha_note_zh"] = "吉凶星混合影响"

    return narrative


def _stems_to_elements(stem_scores: Dict[str, float]) -> Dict[str, float]:
    """Convert stem-based scores to element totals."""
    stem_to_element = {
        "Jia": "Wood", "Yi": "Wood",
        "Bing": "Fire", "Ding": "Fire",
        "Wu": "Earth", "Ji": "Earth",
        "Geng": "Metal", "Xin": "Metal",
        "Ren": "Water", "Gui": "Water",
    }

    element_totals = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}

    for stem, score in stem_scores.items():
        element = stem_to_element.get(stem, "")
        if element:
            element_totals[element] += score

    return element_totals


def _determine_favorable_elements(
    daymaster_element: str,
    excess_elements: List[Dict],
    deficient_elements: List[Dict],
    percentages: Dict[str, float]
) -> Tuple[List[str], List[str]]:
    """
    Determine which elements are favorable vs unfavorable for the chart.

    General principles:
    - If daymaster element is strong: favor output/wealth elements
    - If daymaster element is weak: favor resource/friend elements
    - Elements that control excess are favorable
    - Elements that produce deficient are favorable
    """
    favorable = []
    unfavorable = []

    # Get daymaster percentage
    dm_pct = percentages.get(daymaster_element, 20.0)

    # Determine daymaster strength
    dm_strong = dm_pct >= BALANCE_THRESHOLDS["balanced_upper"]

    if dm_strong:
        # Strong daymaster benefits from output/wealth
        output_element = ELEMENT_GENERATES.get(daymaster_element, "")
        wealth_element = ELEMENT_CONTROLS.get(daymaster_element, "")
        if output_element:
            favorable.append(output_element)
        if wealth_element:
            favorable.append(wealth_element)

        # More resource/friend could worsen excess
        resource_element = ELEMENT_GENERATED_BY.get(daymaster_element, "")
        if resource_element:
            unfavorable.append(resource_element)
        unfavorable.append(daymaster_element)  # More of same
    else:
        # Weak daymaster benefits from resource/friend
        resource_element = ELEMENT_GENERATED_BY.get(daymaster_element, "")
        if resource_element:
            favorable.append(resource_element)
        favorable.append(daymaster_element)  # More of same strengthens

        # Output/wealth drains weak daymaster
        output_element = ELEMENT_GENERATES.get(daymaster_element, "")
        wealth_element = ELEMENT_CONTROLS.get(daymaster_element, "")
        if output_element:
            unfavorable.append(output_element)
        if wealth_element:
            unfavorable.append(wealth_element)

    # Also consider excess/deficient elements
    for excess in excess_elements:
        controller = excess.get("controller", "")
        if controller and controller not in favorable:
            favorable.append(controller)

    for deficient in deficient_elements:
        producer = deficient.get("producer", "")
        if producer and producer not in favorable:
            favorable.append(producer)

    # Remove duplicates while preserving order
    favorable = list(dict.fromkeys(favorable))
    unfavorable = list(dict.fromkeys(unfavorable))

    # Remove any overlap (if something is in both, remove from unfavorable)
    unfavorable = [e for e in unfavorable if e not in favorable]

    return favorable, unfavorable


def _element_to_chinese(element: str) -> str:
    """Convert element name to Chinese."""
    mapping = {
        "Wood": "木",
        "Fire": "火",
        "Earth": "土",
        "Metal": "金",
        "Water": "水",
    }
    return mapping.get(element, element)
