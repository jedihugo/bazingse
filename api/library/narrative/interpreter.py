# * =========================
# * NARRATIVE INTERPRETER ENGINE
# * =========================
# Core engine that generates human-readable narrative interpretations
# from BaZi chart analysis data. No AI - pure template-based generation.

from typing import Dict, Any, List, Optional

from .templates import NARRATIVE_TEMPLATES, ELEMENT_MANIFESTATIONS, PILLAR_CONTEXT
from .priority import calculate_priority_score, prioritize_narratives, group_narratives_by_category
from .modifiers import get_element_balance_context, apply_element_modifiers, apply_shen_sha_modifiers
from .remedies import generate_remedies, get_quick_remedies
from .localization import (
    build_narrative_text,
    format_pillar_reference,
    format_branches_display,
    format_stems_display,
    ELEMENT_NAMES,
    STEM_NAMES,
    BRANCH_NAMES,
)
from .chain_engine import enrich_clash_with_chain_analysis, analyze_node_chain
from .qi_phase import get_qi_phase_for_stem, get_storage_info


def _build_shen_sha_by_node(special_stars: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Build a mapping of node_id -> list of Shen Sha present at that node.

    Args:
        special_stars: List of special star dicts from pattern engine

    Returns:
        Dict mapping node_id to list of Shen Sha IDs (e.g., {"eb_d": ["GU_CHEN", "HUA_GAI"]})
    """
    shen_sha_by_node = {}

    for star in special_stars:
        # Each special star has triggers (node_ids where it manifests)
        triggers = star.get("triggers", [])
        star_id = star.get("pattern_id", star.get("id", ""))

        # Normalize pattern_id (e.g., "GU_CHEN_Yin" -> "GU_CHEN")
        # Pattern IDs often have branch suffix
        base_star_id = star_id.split("_")[0] + ("_" + star_id.split("_")[1] if len(star_id.split("_")) > 1 and star_id.split("_")[1] in ["CHEN", "SU", "GAI"] else "")

        # Handle common Shen Sha types
        if "GU_CHEN" in star_id.upper():
            base_star_id = "GU_CHEN"
        elif "GUA_SU" in star_id.upper():
            base_star_id = "GUA_SU"
        elif "HUA_GAI" in star_id.upper():
            base_star_id = "HUA_GAI"
        elif "TIAN_YI" in star_id.upper():
            base_star_id = "TIAN_YI"
        elif "TAO_HUA" in star_id.upper():
            base_star_id = "TAO_HUA"
        elif "YANG_REN" in star_id.upper():
            base_star_id = "YANG_REN"

        for trigger in triggers:
            node_id = trigger.get("node_id", "")
            if node_id:
                if node_id not in shen_sha_by_node:
                    shen_sha_by_node[node_id] = []
                if base_star_id and base_star_id not in shen_sha_by_node[node_id]:
                    shen_sha_by_node[node_id].append(base_star_id)

    return shen_sha_by_node


def generate_narrative(
    interactions: Dict[str, Any],
    post_element_score: Dict[str, float],
    natal_element_score: Dict[str, float],
    daymaster_analysis: Dict[str, Any],
    wealth_storage_analysis: Optional[Dict[str, Any]] = None,
    special_stars: Optional[List[Dict[str, Any]]] = None,
    ten_gods_detail: Optional[Dict[str, Any]] = None,
    nodes: Optional[Dict[str, Any]] = None,
    interaction_log: Optional[List[Dict[str, Any]]] = None,
    locale: str = "en",
    max_narratives: int = 15,
) -> Dict[str, Any]:
    """
    Generate comprehensive narrative interpretation from BaZi analysis data.

    This is the main entry point for the narrative system.

    Args:
        interactions: Interaction log from bazingse.py analysis
        post_element_score: Post-interaction element scores (stem -> qi)
        natal_element_score: Natal element scores (stem -> qi)
        daymaster_analysis: Daymaster analysis dict
        wealth_storage_analysis: Optional wealth storage analysis
        special_stars: Optional list of special stars from pattern engine
        ten_gods_detail: Optional Ten Gods analysis for richer narratives
        nodes: Optional full API response for pillar analysis
        locale: Language locale ("en" or "zh")
        max_narratives: Maximum number of narratives to return

    Returns:
        Dict containing:
            - narratives: List of prioritized narrative dicts
            - narratives_by_category: Grouped narratives
            - element_context: Element balance analysis
            - remedies: Remedy recommendations
            - quick_remedies: Quick remedy summary
            - daymaster_narrative: Daymaster-specific narrative
            - summary: Overall chart summary
    """
    # Get daymaster element
    daymaster = daymaster_analysis.get("daymaster", "")
    daymaster_element = _extract_element(daymaster)

    # Analyze element balance - pass full daymaster_analysis for correct favorability
    element_context = get_element_balance_context(
        post_element_score,
        daymaster_element,
        daymaster_analysis  # Pass full analysis for favorable/unfavorable elements
    )

    # Build Shen Sha by node mapping for chain analysis
    shen_sha_by_node = {}
    if special_stars:
        shen_sha_by_node = _build_shen_sha_by_node(special_stars)

    # Generate narratives from interactions
    raw_narratives = []

    # Process interaction log
    # The interactions dict is keyed by interaction ID, with each value being the interaction details
    if isinstance(interactions, dict):
        # Convert dict values to list, filtering for significant interaction types
        interaction_list = [
            v for k, v in interactions.items()
            if isinstance(v, dict) and v.get("type") in NARRATIVE_TEMPLATES
        ]
    elif isinstance(interactions, list):
        interaction_list = interactions
    else:
        interaction_list = []

    for interaction in interaction_list:
        narrative = _process_interaction(interaction, locale)
        if narrative:
            # Apply modifiers
            narrative = apply_element_modifiers(narrative, element_context)
            if special_stars:
                narrative = apply_shen_sha_modifiers(narrative, special_stars)
            # Add pillar context for conflicts (clashes, harms, etc.)
            # Include daymaster element, nodes, element_context, and shen_sha for complete chain analysis
            narrative = _add_pillar_context(
                narrative, locale,
                daymaster_element=daymaster_element,
                nodes_data=nodes,
                element_context=element_context,
                shen_sha_by_node=shen_sha_by_node
            )
            raw_narratives.append(narrative)

    # Add element balance narratives
    balance_narratives = _generate_element_balance_narratives(element_context, locale)
    raw_narratives.extend(balance_narratives)

    # Add daymaster narrative
    daymaster_narrative = _generate_daymaster_narrative(daymaster_analysis, locale)
    if daymaster_narrative:
        raw_narratives.append(daymaster_narrative)

    # Add wealth storage narrative
    if wealth_storage_analysis:
        wealth_narratives = _generate_wealth_storage_narratives(wealth_storage_analysis, locale)
        raw_narratives.extend(wealth_narratives)

    # Add Ten Gods warnings as narratives
    if ten_gods_detail:
        ten_gods_narratives = _generate_ten_gods_narratives(ten_gods_detail, locale)
        raw_narratives.extend(ten_gods_narratives)

    # Add pillar analysis narratives (natal pillars interpretation)
    if nodes:
        pillar_narratives = _generate_pillar_narratives(nodes, daymaster_analysis, locale)
        raw_narratives.extend(pillar_narratives)

    # Prioritize and limit narratives
    prioritized = prioritize_narratives(raw_narratives, max_count=max_narratives)

    # Group by category
    grouped = group_narratives_by_category(prioritized)

    # Generate remedies
    remedies = generate_remedies(element_context, daymaster_element, locale)
    quick = get_quick_remedies(element_context.get("favorable_elements", []), locale)

    # Generate overall summary
    summary = _generate_summary(
        element_context=element_context,
        daymaster_analysis=daymaster_analysis,
        prioritized_narratives=prioritized,
        locale=locale
    )

    # Build chronological list from raw interaction_log (preserves engine processing order)
    all_chronological = _build_all_chronological(interaction_log or [], locale)

    return {
        "narratives": prioritized,
        "narratives_by_category": grouped,
        "all_chronological": all_chronological,
        "element_context": element_context,
        "remedies": remedies,
        "quick_remedies": quick,
        "daymaster_narrative": daymaster_narrative,
        "summary": summary,
        "locale": locale,
    }


def _process_interaction(interaction: Dict[str, Any], locale: str) -> Optional[Dict[str, Any]]:
    """
    Process a single interaction into a narrative dict.

    Args:
        interaction: Raw interaction dict from interaction log
        locale: Target locale

    Returns:
        Narrative dict or None if interaction type not supported
    """
    interaction_type = interaction.get("type", "")

    if interaction_type not in NARRATIVE_TEMPLATES:
        return None

    template = NARRATIVE_TEMPLATES[interaction_type]

    # Build variables for template substitution
    variables = _extract_interaction_variables(interaction)

    # Build localized text
    text = build_narrative_text(interaction_type, NARRATIVE_TEMPLATES, variables, locale)

    # Determine which detail text to use (transformed vs partial)
    if interaction.get("transformed", False):
        if "transformed" in text:
            text["status_detail"] = text["transformed"]
    else:
        if "partial" in text:
            text["status_detail"] = text["partial"]

    # Get element - derive from pattern/branches if not directly provided
    element = interaction.get("element", "")
    if not element:
        element = _derive_element_from_interaction(interaction)

    # Build narrative dict
    narrative = {
        "id": f"{interaction_type}_{hash(str(interaction.get('nodes', [])))}"[:32],
        "type": interaction_type,
        "category": template.get("category", "energy"),
        "polarity": template.get("polarity", "neutral"),
        "icon": template.get("icon", ""),
        "color_key": template.get("color_key", "neutral"),
        # Text content
        "title": text.get("title", interaction_type),
        "summary": text.get("summary", ""),
        "detail": text.get("detail", ""),
        "meaning": text.get("meaning", ""),
        "advice": text.get("advice", ""),
        "status_detail": text.get("status_detail", ""),
        # Data from interaction
        "nodes": interaction.get("nodes", []),
        "positions": interaction.get("positions", []),
        "element": element,
        "transformed": interaction.get("transformed", False),
        "points": interaction.get("points", ""),
        "distance": interaction.get("distance", ""),
        # Pillar references for UI
        "pillar_refs": [
            format_pillar_reference(node, locale)
            for node in interaction.get("nodes", [])
        ],
    }

    # Add branches/stems display
    if "branches" in interaction:
        narrative["branches_display"] = format_branches_display(interaction["branches"], locale)

    return narrative


# =============================================================================
# CHRONOLOGICAL INTERACTION LIST
# =============================================================================

# Chinese names for interaction types (used in formula display)
_TYPE_CHINESE = {
    "THREE_MEETINGS": "三会",
    "THREE_COMBINATIONS": "三合",
    "SIX_HARMONIES": "六合",
    "HALF_MEETINGS": "半会",
    "HALF_MEETING": "半会",
    "HALF_COMBINATIONS": "半合",
    "HALF_COMBINATION": "半合",
    "ARCHED_COMBINATIONS": "拱合",
    "ARCHED_COMBINATION": "拱合",
    "STEM_COMBINATIONS": "干合",
    "STEM_COMBINATION": "干合",
    "CLASHES": "冲",
    "CLASH": "冲",
    "PUNISHMENTS": "刑",
    "HARMS": "害",
    "HARM": "害",
    "DESTRUCTION": "破",
    "STEM_CONFLICTS": "干克",
    "STEM_CONFLICT": "干克",
    "CROSS_PILLAR_WUXING": "五行",
    "PILLAR_WUXING": "干支五行",
    "SEASONAL_ADJUSTMENT": "旺相休囚死",
    "ENERGY_FLOW": "流通",
}

# Polarity inference for types without templates
_TYPE_POLARITY = {
    "THREE_MEETINGS": "positive",
    "THREE_COMBINATIONS": "positive",
    "SIX_HARMONIES": "positive",
    "HALF_MEETINGS": "positive",
    "HALF_MEETING": "positive",
    "HALF_COMBINATIONS": "positive",
    "HALF_COMBINATION": "positive",
    "ARCHED_COMBINATIONS": "positive",
    "ARCHED_COMBINATION": "positive",
    "STEM_COMBINATIONS": "positive",
    "STEM_COMBINATION": "positive",
    "ENERGY_FLOW": "positive",
    "CLASHES": "negative",
    "CLASH": "negative",
    "PUNISHMENTS": "negative",
    "HARMS": "negative",
    "HARM": "negative",
    "DESTRUCTION": "negative",
    "STEM_CONFLICTS": "negative",
    "STEM_CONFLICT": "negative",
    "CROSS_PILLAR_WUXING": "neutral",
    "PILLAR_WUXING": "neutral",
    "SEASONAL_ADJUSTMENT": "neutral",
}


def _build_formula_string(interaction: Dict[str, Any]) -> str:
    """
    Build a formula string like "Mao + Xu → Fire 六合" from interaction data.
    """
    itype = interaction.get("type", "")
    chinese = _TYPE_CHINESE.get(itype, "")

    # Get branches or stems involved
    branches = interaction.get("branches", [])
    stems = interaction.get("stems", [])
    pattern = interaction.get("pattern", "")

    # Parse pattern if no branches/stems
    if not branches and not stems and pattern and "-" in pattern:
        parts = pattern.split("-")
        if all(p in STEM_NAMES for p in parts):
            stems = parts
        else:
            branches = parts

    element = interaction.get("element", "")
    arrow_target = f" {element}" if element else ""

    if branches:
        formula = " + ".join(branches) + f" →{arrow_target} {chinese}" if chinese else " + ".join(branches) + f" →{arrow_target}"
    elif stems:
        formula = " + ".join(stems) + f" →{arrow_target} {chinese}" if chinese else " + ".join(stems) + f" →{arrow_target}"
    elif pattern:
        formula = f"{pattern} →{arrow_target} {chinese}" if chinese else f"{pattern} →{arrow_target}"
    else:
        # Fallback: just type name + chinese
        human_type = itype.replace("_", " ").title()
        formula = f"{human_type} {chinese}".strip()

    return formula


def _build_match_string(interaction: Dict[str, Any], locale: str) -> str:
    """
    Build a match string like "Month EB + Hour EB" from node IDs.
    """
    node_ids = interaction.get("nodes", [])
    if not node_ids:
        return ""

    refs = []
    for node_id in node_ids:
        ref = format_pillar_reference(node_id, locale)
        refs.append(ref.get("abbrev", node_id))

    return " + ".join(refs)


def _build_qi_changes(interaction: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build before→after qi change entries for display.
    Returns list of {stem, before, after} dicts.
    """
    itype = interaction.get("type", "")
    changes = []

    if itype == "PILLAR_WUXING":
        hs_stem = interaction.get("hs_stem", "")
        eb_stem = interaction.get("eb_stem", "")
        hs_before = interaction.get("hs_qi_before")
        hs_after = interaction.get("hs_qi_after")
        eb_before = interaction.get("eb_qi_before")
        eb_after = interaction.get("eb_qi_after")
        # Use the actual qi stem name for EB (hidden stem or primary qi)
        eb_qi_stem = interaction.get("eb_qi_stem", eb_stem)

        if hs_before is not None and hs_after is not None:
            changes.append({
                "stem": hs_stem,
                "before": hs_before,
                "after": hs_after,
            })
        if eb_before is not None and eb_after is not None:
            changes.append({
                "stem": eb_qi_stem,
                "before": eb_before,
                "after": eb_after,
            })

    elif itype == "SAME_ELEMENT":
        hs_stem = interaction.get("hs_stem", "")
        eb_qi_stem = interaction.get("eb_qi_stem", "")
        hs_qi = interaction.get("hs_qi")
        eb_qi = interaction.get("eb_qi")
        strength = interaction.get("strength", "")
        qi_type = interaction.get("qi_type", "")

        if hs_qi is not None:
            changes.append({
                "stem": hs_stem,
                "before": hs_qi,
                "after": hs_qi,  # No change for same element
                "note": f"{'strong ' if strength == 'strong' else ''}rooting",
            })
        if eb_qi is not None:
            changes.append({
                "stem": eb_qi_stem,
                "before": eb_qi,
                "after": eb_qi,  # No change for same element
                "note": "Primary Qi" if qi_type == "PRIMARY_QI" else "Hidden Stem",
            })

    return changes


def _build_chronological_entry(interaction: Dict[str, Any], seq: int, locale: str) -> Dict[str, Any]:
    """
    Process one raw interaction into a chronological display entry.
    Uses existing template if available, otherwise creates fallback.
    """
    itype = interaction.get("type", "")
    template = NARRATIVE_TEMPLATES.get(itype, None)

    # Title: from template or humanized type name
    if template:
        locale_text = template.get(locale, template.get("en", {}))
        title = locale_text.get("title", itype.replace("_", " ").title())
        category = template.get("category", "energy")
        polarity = template.get("polarity", "neutral")
        icon = template.get("icon", "")
    else:
        title = itype.replace("_", " ").title()
        category = "energy"
        polarity = _TYPE_POLARITY.get(itype, "neutral")
        icon = ""

    # Element
    element = interaction.get("element", "")
    if not element:
        element = _derive_element_from_interaction(interaction)

    # Formula and match
    formula = _build_formula_string(interaction)
    match = _build_match_string(interaction, locale)

    # Points
    points = interaction.get("points", "")

    # Math formula (scoring breakdown)
    math_formula = interaction.get("math_formula", "")

    # Pillar references
    pillar_refs = [
        format_pillar_reference(node, locale)
        for node in interaction.get("nodes", [])
    ]

    # Build before→after qi display for PILLAR_WUXING and SAME_ELEMENT
    qi_changes = _build_qi_changes(interaction)

    entry = {
        "seq": seq,
        "type": itype,
        "category": category,
        "polarity": polarity,
        "icon": icon,
        "title": title,
        "element": element,
        "points": str(points) if points else "",
        "formula": formula,
        "match": match,
        "math_formula": str(math_formula) if math_formula else "",
        "qi_changes": qi_changes,
        "pillar_refs": pillar_refs,
        "nodes": interaction.get("nodes", []),
        "transformed": interaction.get("transformed", False),
        "distance": interaction.get("distance", ""),
    }

    return entry


def _build_all_chronological(interaction_log: List[Dict[str, Any]], locale: str) -> List[Dict[str, Any]]:
    """
    Build a flat chronological list of ALL interactions in engine-processing order.
    No filtering, no priority sorting - raw sequence.
    """
    entries = []
    for idx, interaction in enumerate(interaction_log):
        entry = _build_chronological_entry(interaction, seq=idx + 1, locale=locale)
        entries.append(entry)
    return entries


def _derive_element_from_interaction(interaction: Dict[str, Any]) -> str:
    """
    Derive the element involved in an interaction from its pattern or branches.

    For CLASH, HARM, etc., the element is the common element of the branches involved.
    E.g., Chou-Wei clash: both are Earth branches, so element = Earth.
    """
    pattern = interaction.get("pattern", "")
    interaction_type = interaction.get("type", "")

    # Parse branches from pattern (e.g., "Chou-Wei" -> ["Chou", "Wei"])
    if "-" in pattern:
        branches = pattern.split("-")
        elements = []
        for branch in branches:
            branch_info = BRANCH_NAMES.get(branch, {})
            elem = branch_info.get("element", "")
            if elem:
                elements.append(elem)

        # For clashes and harms, branches usually have the same element
        # Return the most common element
        if elements:
            from collections import Counter
            element_counts = Counter(elements)
            most_common = element_counts.most_common(1)
            if most_common:
                return most_common[0][0]

    return ""


def _extract_interaction_variables(interaction: Dict[str, Any]) -> Dict[str, Any]:
    """Extract variables from interaction for template substitution."""
    variables = {
        "element": interaction.get("element", ""),
        "points": interaction.get("points", ""),
        "distance": interaction.get("distance", ""),
    }

    # Extract branches - first try direct field, then parse from pattern
    branches = interaction.get("branches", [])
    if not branches:
        # Parse from pattern (e.g., "Chou-Wei" -> ["Chou", "Wei"])
        pattern = interaction.get("pattern", "")
        if "-" in pattern:
            branches = pattern.split("-")

    if branches:
        variables["branches"] = ", ".join(branches)
        if len(branches) >= 1:
            variables["branch1"] = branches[0]
        if len(branches) >= 2:
            variables["branch2"] = branches[1]
        if len(branches) >= 3:
            variables["branch3"] = branches[2]

    # Extract stems for stem combinations - first try direct field, then parse from pattern
    stems = interaction.get("stems", [])
    if not stems:
        pattern = interaction.get("pattern", "")
        if "-" in pattern:
            # Check if pattern contains stems (e.g., "Jia-Ji")
            parts = pattern.split("-")
            if all(part in STEM_NAMES for part in parts):
                stems = parts

    if stems:
        if len(stems) >= 1:
            variables["stem1"] = stems[0]
        if len(stems) >= 2:
            variables["stem2"] = stems[1]

    # Extract pattern info
    if "pattern" in interaction:
        variables["pattern"] = interaction["pattern"]

    # Extract punishment type
    if "punishment_type" in interaction:
        variables["punishment_type"] = interaction["punishment_type"]

    # Extract seasonal info
    if "state" in interaction:
        variables["state"] = interaction["state"]
    if "season" in interaction:
        variables["season"] = interaction["season"]
    if "multiplier" in interaction:
        variables["multiplier"] = interaction["multiplier"]

    return variables


def _generate_element_balance_narratives(
    element_context: Dict[str, Any],
    locale: str
) -> List[Dict[str, Any]]:
    """Generate narratives for element imbalances."""
    narratives = []

    # Excess element narratives
    for excess in element_context.get("excess_elements", []):
        element = excess["element"]
        pct = excess["percentage"]

        manifestations = ELEMENT_MANIFESTATIONS.get(element, {}).get("excess", {})
        manifest_text = manifestations.get("en" if locale == "en" else "zh", "")

        variables = {
            "element": element,
            "percentage": round(pct, 1),
            "manifestations": manifest_text,
            "controller": excess.get("controller", ""),
        }

        text = build_narrative_text("ELEMENT_EXCESS", NARRATIVE_TEMPLATES, variables, locale)

        narratives.append({
            "id": f"excess_{element}",
            "type": "ELEMENT_EXCESS",
            "category": "balance",
            "polarity": "negative",
            "icon": "excess",
            "color_key": "warning",
            "title": text.get("title", f"{element} Excess"),
            "summary": text.get("summary", ""),
            "detail": text.get("detail", ""),
            "meaning": text.get("meaning", ""),
            "element": element,
            "percentage": pct,
            "severity": excess["severity"],
        })

    # Deficient element narratives
    for deficient in element_context.get("deficient_elements", []):
        element = deficient["element"]
        pct = deficient["percentage"]

        manifestations = ELEMENT_MANIFESTATIONS.get(element, {}).get("deficiency", {})
        manifest_text = manifestations.get("en" if locale == "en" else "zh", "")

        variables = {
            "element": element,
            "percentage": round(pct, 1),
            "manifestations": manifest_text,
            "producer": deficient.get("producer", ""),
        }

        text = build_narrative_text("ELEMENT_DEFICIENCY", NARRATIVE_TEMPLATES, variables, locale)

        narratives.append({
            "id": f"deficient_{element}",
            "type": "ELEMENT_DEFICIENCY",
            "category": "balance",
            "polarity": "negative",
            "icon": "deficiency",
            "color_key": "warning",
            "title": text.get("title", f"{element} Deficiency"),
            "summary": text.get("summary", ""),
            "detail": text.get("detail", ""),
            "meaning": text.get("meaning", ""),
            "element": element,
            "percentage": pct,
            "severity": deficient["severity"],
        })

    return narratives


def _generate_daymaster_narrative(
    daymaster_analysis: Dict[str, Any],
    locale: str
) -> Optional[Dict[str, Any]]:
    """Generate narrative for daymaster strength.

    Uses daymaster_strength field which has values:
    - "Very Strong" (60%+)
    - "Strong" (45-60%)
    - "Balanced" (35-45%)
    - "Weak" (20-35%)
    - "Very Weak" (<20%)
    """
    if not daymaster_analysis:
        return None

    daymaster = daymaster_analysis.get("daymaster", "")
    # CRITICAL FIX: Use daymaster_strength, NOT chart_type
    # chart_type is "Normal"/"Vibrant"/"Follower" (chart classification)
    # daymaster_strength is "Very Strong"/"Strong"/"Balanced"/"Weak"/"Very Weak" (actual strength)
    strength = daymaster_analysis.get("daymaster_strength", "Balanced")
    support_pct = daymaster_analysis.get("support_percentage", 50)

    # Map strength to template
    if strength in ["Very Strong", "Strong"]:
        template_key = "DAYMASTER_STRONG"
        polarity = "positive"
        icon = "strong"
        color_key = "positive"
    elif strength == "Balanced":
        template_key = "DAYMASTER_BALANCED"
        polarity = "neutral"
        icon = "balanced"
        color_key = "neutral"
    else:  # "Weak" or "Very Weak"
        template_key = "DAYMASTER_WEAK"
        polarity = "neutral"
        icon = "weak"
        color_key = "warning"

    variables = {
        "daymaster": daymaster,
        "percentage": round(support_pct, 1),
        "strength": strength,
    }

    text = build_narrative_text(template_key, NARRATIVE_TEMPLATES, variables, locale)

    # Get favorable/unfavorable elements for context
    favorable = daymaster_analysis.get("favorable_elements", [])
    unfavorable = daymaster_analysis.get("unfavorable_elements", [])

    return {
        "id": f"daymaster_{strength.lower().replace(' ', '_')}",
        "type": template_key,
        "category": "daymaster",
        "polarity": polarity,
        "icon": icon,
        "color_key": color_key,
        "title": text.get("title", f"{strength} Daymaster"),
        "summary": text.get("summary", ""),
        "detail": text.get("detail", ""),
        "meaning": text.get("meaning", ""),
        "daymaster": daymaster,
        "daymaster_strength": strength,
        "support_percentage": support_pct,
        "favorable_elements": favorable,
        "unfavorable_elements": unfavorable,
    }


def _generate_wealth_storage_narratives(
    wealth_storage_analysis: Dict[str, Any],
    locale: str
) -> List[Dict[str, Any]]:
    """Generate narratives for wealth storage."""
    narratives = []

    if not wealth_storage_analysis:
        return narratives

    # Check for opened wealth storages
    opened = wealth_storage_analysis.get("opened_storages", [])
    for storage in opened:
        variables = {
            "storage_branch": storage.get("branch", ""),
            "stored_element": storage.get("stored_element", ""),
            "opener": storage.get("opener", ""),
        }

        text = build_narrative_text("WEALTH_STORAGE_OPENED", NARRATIVE_TEMPLATES, variables, locale)

        narratives.append({
            "id": f"wealth_open_{storage.get('branch', '')}",
            "type": "WEALTH_STORAGE_OPENED",
            "category": "wealth",
            "polarity": "positive",
            "icon": "wealth_open",
            "color_key": "wealth",
            "title": text.get("title", "Wealth Storage Opened"),
            "summary": text.get("summary", ""),
            "detail": text.get("detail", ""),
            "meaning": text.get("meaning", ""),
            **storage,
        })

    # Check for closed wealth storages
    closed = wealth_storage_analysis.get("closed_storages", [])
    for storage in closed:
        variables = {
            "storage_branch": storage.get("branch", ""),
            "stored_element": storage.get("stored_element", ""),
            "opener": storage.get("needed_opener", ""),
        }

        text = build_narrative_text("WEALTH_STORAGE_CLOSED", NARRATIVE_TEMPLATES, variables, locale)

        narratives.append({
            "id": f"wealth_closed_{storage.get('branch', '')}",
            "type": "WEALTH_STORAGE_CLOSED",
            "category": "wealth",
            "polarity": "neutral",
            "icon": "wealth_closed",
            "color_key": "neutral",
            "title": text.get("title", "Wealth Storage Present"),
            "summary": text.get("summary", ""),
            "detail": text.get("detail", ""),
            "meaning": text.get("meaning", ""),
            **storage,
        })

    return narratives


def _generate_summary(
    element_context: Dict[str, Any],
    daymaster_analysis: Dict[str, Any],
    prioritized_narratives: List[Dict[str, Any]],
    locale: str
) -> Dict[str, str]:
    """Generate an overall chart summary."""
    daymaster = daymaster_analysis.get("daymaster", "Unknown")
    chart_type = daymaster_analysis.get("chart_type", "Balanced")
    balance = element_context.get("balance_assessment", "unknown")

    # Count positive vs negative interactions
    positive_count = sum(1 for n in prioritized_narratives if n.get("polarity") == "positive")
    negative_count = sum(1 for n in prioritized_narratives if n.get("polarity") == "negative")

    # Get favorable elements
    favorable = element_context.get("favorable_elements", [])
    favorable_str = ", ".join(favorable[:2]) if favorable else "balanced elements"

    if locale == "zh":
        summary = f"您的{daymaster}日主{('身强' if chart_type == 'Strong' else '身弱')}。"
        if balance == "balanced":
            summary += "五行整体平衡。"
        elif balance == "severely_imbalanced":
            summary += "五行存在明显失衡。"
        else:
            summary += "五行略有失衡。"

        if favorable:
            summary += f"有利五行：{', '.join([ELEMENT_NAMES.get(e, {}).get('zh', e) for e in favorable[:2]])}。"

        if positive_count > negative_count:
            outlook = "当前运势以吉利组合为主，整体向好。"
        elif negative_count > positive_count:
            outlook = "当前运势存在挑战，建议谨慎行事。"
        else:
            outlook = "当前运势平稳，适合稳中求进。"
    else:
        summary = f"Your {daymaster} daymaster is {chart_type.lower()}. "
        if balance == "balanced":
            summary += "Elements are well-balanced overall. "
        elif balance == "severely_imbalanced":
            summary += "There are significant elemental imbalances. "
        else:
            summary += "There are minor elemental imbalances. "

        if favorable:
            summary += f"Favorable elements: {favorable_str}. "

        if positive_count > negative_count:
            outlook = "Current influences favor positive combinations - an auspicious period overall."
        elif negative_count > positive_count:
            outlook = "Current influences present some challenges - proceed with awareness."
        else:
            outlook = "Current influences are balanced - a stable period for steady progress."

    return {
        "text": summary,
        "outlook": outlook,
        "daymaster": daymaster,
        "chart_type": chart_type,
        "balance": balance,
        "favorable_elements": favorable,
        "positive_interactions": positive_count,
        "negative_interactions": negative_count,
    }


def _extract_element(daymaster_str: str) -> str:
    """Extract element from daymaster string like 'Yang Wood' or 'Jia'."""
    if not daymaster_str:
        return ""

    # Check if it's a stem name
    if daymaster_str in STEM_NAMES:
        return STEM_NAMES[daymaster_str].get("element", "")

    # Check if it's a "Polarity Element" format
    elements = ["Wood", "Fire", "Earth", "Metal", "Water"]
    for element in elements:
        if element in daymaster_str:
            return element

    return ""


# =============================================================================
# PILLAR CONTEXT FOR CONFLICTS
# =============================================================================

# Node ID to pillar mapping
NODE_TO_PILLAR = {
    "hs_h": "hour", "eb_h": "hour",
    "hs_d": "day", "eb_d": "day",
    "hs_m": "month", "eb_m": "month",
    "hs_y": "year", "eb_y": "year",
    "hs_10yl": "luck_10y", "eb_10yl": "luck_10y",
    "hs_yl": "annual", "eb_yl": "annual",
    "hs_ml": "monthly", "eb_ml": "monthly",
    "hs_dl": "daily", "eb_dl": "daily",
}

# What each pillar represents
PILLAR_LIFE_AREAS = {
    "hour": {
        "en": {"name": "Hour Pillar", "represents": "children, subordinates, future, late life"},
        "zh": {"name": "时柱", "represents": "子女、下属、未来、晚年"},
    },
    "day": {
        "en": {"name": "Day Pillar", "represents": "self, spouse, marriage, core identity"},
        "zh": {"name": "日柱", "represents": "自己、配偶、婚姻、核心身份"},
    },
    "month": {
        "en": {"name": "Month Pillar", "represents": "parents, career, social status"},
        "zh": {"name": "月柱", "represents": "父母、事业、社会地位"},
    },
    "year": {
        "en": {"name": "Year Pillar", "represents": "ancestors, foundation, early life"},
        "zh": {"name": "年柱", "represents": "祖先、根基、童年"},
    },
    "luck_10y": {
        "en": {"name": "10-Year Luck", "represents": "major life phase, decade themes"},
        "zh": {"name": "大运", "represents": "人生阶段、十年主题"},
    },
    "annual": {
        "en": {"name": "Annual Luck", "represents": "this year's energy and themes"},
        "zh": {"name": "流年", "represents": "年度能量和主题"},
    },
}


def _add_pillar_context(
    narrative: Dict[str, Any],
    locale: str,
    daymaster_element: str = "",
    nodes_data: Optional[Dict[str, Any]] = None,
    element_context: Optional[Dict[str, Any]] = None,
    shen_sha_by_node: Optional[Dict[str, List[str]]] = None
) -> Dict[str, Any]:
    """
    Add pillar context to interaction narratives, especially conflicts.

    This explains the CHAIN of interconnected factors:
    1. WHICH life areas are affected by clashes, harms, etc.
    2. The Daymaster-to-Spouse-Palace relationship (when Day EB is involved)
    3. Spouse Star (DW/IW) strength analysis
    4. Shen Sha + Qi Phase + Storage chain analysis
    5. Combined chain interpretation

    E.g., "Day-Hour clash affects spouse and children relationship"
    E.g., "Fire DM produces Earth Spouse Palace - you give energy to marriage, draining yourself"
    E.g., "Spouse Star (Metal) is severely weak - hard to find spouse"
    E.g., "CHAIN: Longs for marriage + can't find spouse = painful pattern"
    E.g., "Gu Chen in Spouse Palace with Earth excess EG - isolation from perfectionism"
    """
    narrative = dict(narrative)  # Don't modify original
    if shen_sha_by_node is None:
        shen_sha_by_node = {}

    nodes = narrative.get("nodes", [])
    if not nodes:
        return narrative

    # Identify pillars involved
    pillars_involved = []
    for node in nodes:
        pillar = NODE_TO_PILLAR.get(node, "")
        if pillar and pillar not in pillars_involved:
            pillars_involved.append(pillar)

    if not pillars_involved:
        return narrative

    # Build pillar context
    pillar_info = []
    for pillar in pillars_involved:
        info = PILLAR_LIFE_AREAS.get(pillar, {}).get("en" if locale == "en" else "zh", {})
        if info:
            pillar_info.append(info)

    narrative["pillars_involved"] = pillars_involved
    narrative["pillar_info"] = pillar_info

    # For conflicts, add specific life area impact
    if narrative.get("category") == "conflict" and len(pillars_involved) >= 2:
        areas = []
        for info in pillar_info:
            areas.append(info.get("represents", ""))

        if locale == "zh":
            narrative["life_area_impact"] = f"此冲突影响：{' 与 '.join([info.get('name', '') for info in pillar_info])}，涉及{'; '.join(areas)}"
        else:
            narrative["life_area_impact"] = f"This conflict affects: {' and '.join([info.get('name', '') for info in pillar_info])}, involving {'; '.join(areas)}"

    # Check for Daymaster-to-Spouse-Palace relationship chain
    # Day EB = Spouse Palace. If this is involved, analyze complete chain:
    # DM→Spouse Palace + Spouse Star strength + Combined interpretation
    if "day" in pillars_involved and daymaster_element and nodes_data:
        dm_spouse_context = _analyze_daymaster_spouse_relationship(
            daymaster_element, nodes_data, locale, element_context
        )
        if dm_spouse_context:
            narrative["dm_spouse_relationship"] = dm_spouse_context

    # ==========================================================================
    # FULL CHAIN ANALYSIS for CLASH/HARM/PUNISHMENT interactions
    # Uses chain_engine to link: Element → Ten God → Shen Sha → Qi Phase → Storage
    # ==========================================================================
    interaction_type = narrative.get("type", "")
    if interaction_type in ["CLASH", "HARM", "PUNISHMENT", "DESTRUCTION"] and nodes_data and element_context:
        # Use the chain engine to enrich with full analysis
        enriched = enrich_clash_with_chain_analysis(
            clash_narrative=narrative,
            nodes_data=nodes_data,
            daymaster_element=daymaster_element,
            element_context=element_context,
            shen_sha_by_node=shen_sha_by_node,
            locale=locale
        )
        # Merge enriched data back into narrative
        narrative["branch_chain_analyses"] = enriched.get("branch_chain_analyses", [])
        narrative["master_chain_narrative"] = enriched.get("master_chain_narrative", "")

    return narrative


def _analyze_daymaster_spouse_relationship(
    daymaster_element: str,
    nodes_data: Dict[str, Any],
    locale: str,
    element_context: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Analyze the COMPLETE chain for Spouse Palace interactions:

    1. DM-to-Spouse Palace relationship (how person relates to marriage)
    2. Spouse Star strength (DW/IW = Wealth element for DM)
    3. Combined interpretation

    This creates the interconnected, chain-reaction analysis:
    - DM produces Spouse Palace → longs for marriage, drains self
    - Spouse Star weak → hard to find/attract spouse
    - Combined: Tragic irony of wanting something you can't easily get

    Returns dict with complete relationship chain or None.
    """
    # Get Day EB data
    eb_d = nodes_data.get("eb_d", {})
    if not eb_d:
        return None

    # Get Day EB element from branch name
    branch_name = eb_d.get("id", "")
    spouse_palace_element = BRANCH_NAMES.get(branch_name, {}).get("element", "")

    if not spouse_palace_element or not daymaster_element:
        return None

    # WuXing relationships
    generates = {
        "Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
        "Metal": "Water", "Water": "Wood"
    }
    controls = {
        "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
        "Water": "Fire", "Metal": "Wood"
    }

    # =========================================================================
    # PART 1: DM-to-Spouse Palace relationship
    # =========================================================================
    dm_spouse_relationship = None
    dm_spouse_meaning_en = ""
    dm_spouse_meaning_zh = ""

    if generates.get(daymaster_element) == spouse_palace_element:
        dm_spouse_relationship = "produces"
        dm_spouse_meaning_en = (
            f"Your {daymaster_element} Daymaster produces {spouse_palace_element} (Spouse Palace). "
            f"You give energy to marriage - it's your aspiration, you long for it. "
            f"This drains and weakens you."
        )
        dm_spouse_meaning_zh = (
            f"您的{_element_to_chinese(daymaster_element)}日主生{_element_to_chinese(spouse_palace_element)}（配偶宫）。"
            f"您将精力投入婚姻——这是您的渴望。这会消耗您。"
        )
    elif controls.get(daymaster_element) == spouse_palace_element:
        dm_spouse_relationship = "controls"
        dm_spouse_meaning_en = (
            f"Your {daymaster_element} Daymaster controls {spouse_palace_element} (Spouse Palace). "
            f"Tendency to dominate or control in relationships."
        )
        dm_spouse_meaning_zh = (
            f"您的{_element_to_chinese(daymaster_element)}日主克{_element_to_chinese(spouse_palace_element)}（配偶宫）。"
            f"在感情中有支配或控制的倾向。"
        )
    elif generates.get(spouse_palace_element) == daymaster_element:
        dm_spouse_relationship = "supported_by"
        dm_spouse_meaning_en = (
            f"Spouse Palace ({spouse_palace_element}) produces your {daymaster_element} Daymaster. "
            f"Marriage supports you - spouse is a source of strength."
        )
        dm_spouse_meaning_zh = (
            f"配偶宫（{_element_to_chinese(spouse_palace_element)}）生您的{_element_to_chinese(daymaster_element)}日主。"
            f"婚姻支持您——配偶是您的力量来源。"
        )
    elif controls.get(spouse_palace_element) == daymaster_element:
        dm_spouse_relationship = "controlled_by"
        dm_spouse_meaning_en = (
            f"Spouse Palace ({spouse_palace_element}) controls your {daymaster_element} Daymaster. "
            f"Marriage may feel pressuring - spouse has authority over you."
        )
        dm_spouse_meaning_zh = (
            f"配偶宫（{_element_to_chinese(spouse_palace_element)}）克您的{_element_to_chinese(daymaster_element)}日主。"
            f"婚姻可能让您感到压力——配偶对您有支配力。"
        )
    elif daymaster_element == spouse_palace_element:
        dm_spouse_relationship = "same"
        dm_spouse_meaning_en = (
            f"Daymaster and Spouse Palace share {daymaster_element}. "
            f"Natural compatibility with spouse."
        )
        dm_spouse_meaning_zh = (
            f"日主和配偶宫同为{_element_to_chinese(daymaster_element)}。"
            f"与配偶有天然的契合。"
        )

    # =========================================================================
    # PART 2: Spouse Star (DW/IW) strength analysis
    # For males: Wealth element = Spouse Star (正财/偏财)
    # For females: Officer element = Spouse Star (正官/七杀)
    # =========================================================================
    spouse_star_element = controls.get(daymaster_element, "")  # DM controls = Wealth = Spouse Star (male)
    spouse_star_strength = "unknown"
    spouse_star_percentage = 0.0
    spouse_star_meaning_en = ""
    spouse_star_meaning_zh = ""

    if element_context and spouse_star_element:
        percentages = element_context.get("element_percentages", {})
        spouse_star_percentage = percentages.get(spouse_star_element, 0)

        # Determine strength based on percentage
        if spouse_star_percentage <= 5:
            spouse_star_strength = "severely_weak"
            spouse_star_meaning_en = (
                f"Your Spouse Star ({spouse_star_element}/Wealth) is severely weak at {spouse_star_percentage:.1f}%. "
                f"This indicates difficulty attracting or finding a spouse. "
                f"Marriage opportunities are scarce."
            )
            spouse_star_meaning_zh = (
                f"您的配偶星（{_element_to_chinese(spouse_star_element)}/财）严重不足，仅{spouse_star_percentage:.1f}%。"
                f"这表示难以吸引或找到配偶。婚姻机会稀少。"
            )
        elif spouse_star_percentage <= 12:
            spouse_star_strength = "weak"
            spouse_star_meaning_en = (
                f"Your Spouse Star ({spouse_star_element}/Wealth) is weak at {spouse_star_percentage:.1f}%. "
                f"Marriage may come later or require more effort."
            )
            spouse_star_meaning_zh = (
                f"您的配偶星（{_element_to_chinese(spouse_star_element)}/财）较弱，{spouse_star_percentage:.1f}%。"
                f"婚姻可能来得较晚或需要更多努力。"
            )
        elif spouse_star_percentage <= 24:
            spouse_star_strength = "balanced"
            spouse_star_meaning_en = (
                f"Your Spouse Star ({spouse_star_element}/Wealth) is balanced at {spouse_star_percentage:.1f}%."
            )
            spouse_star_meaning_zh = (
                f"您的配偶星（{_element_to_chinese(spouse_star_element)}/财）平衡，{spouse_star_percentage:.1f}%。"
            )
        elif spouse_star_percentage <= 35:
            spouse_star_strength = "strong"
            spouse_star_meaning_en = (
                f"Your Spouse Star ({spouse_star_element}/Wealth) is strong at {spouse_star_percentage:.1f}%. "
                f"Good marriage potential, attractive to partners."
            )
            spouse_star_meaning_zh = (
                f"您的配偶星（{_element_to_chinese(spouse_star_element)}/财）较强，{spouse_star_percentage:.1f}%。"
                f"婚姻潜力好，对伴侣有吸引力。"
            )
        else:
            spouse_star_strength = "excessive"
            spouse_star_meaning_en = (
                f"Your Spouse Star ({spouse_star_element}/Wealth) is excessive at {spouse_star_percentage:.1f}%. "
                f"May attract many partners but struggle with commitment."
            )
            spouse_star_meaning_zh = (
                f"您的配偶星（{_element_to_chinese(spouse_star_element)}/财）过旺，{spouse_star_percentage:.1f}%。"
                f"可能吸引很多伴侣但难以承诺。"
            )

    # =========================================================================
    # PART 3: Combined chain interpretation
    # =========================================================================
    chain_interpretation_en = ""
    chain_interpretation_zh = ""

    if dm_spouse_relationship == "produces" and spouse_star_strength in ["severely_weak", "weak"]:
        # Tragic combination: longs for marriage but can't find spouse
        chain_interpretation_en = (
            f"CHAIN ANALYSIS: You long for marriage (DM produces Spouse Palace), "
            f"but your Spouse Star is {spouse_star_strength.replace('_', ' ')} ({spouse_star_percentage:.1f}%). "
            f"This creates a painful pattern: giving energy to something that's hard to attain. "
            f"You drain yourself pursuing marriage while opportunities remain scarce."
        )
        chain_interpretation_zh = (
            f"链式分析：您渴望婚姻（日主生配偶宫），"
            f"但配偶星很弱（{spouse_star_percentage:.1f}%）。"
            f"这形成痛苦的模式：为难以得到的东西付出精力。"
            f"您在追求婚姻时消耗自己，而机会却很少。"
        )
    elif dm_spouse_relationship == "controls" and spouse_star_strength in ["severely_weak", "weak"]:
        chain_interpretation_en = (
            f"CHAIN ANALYSIS: You seek to control in relationships (DM controls Spouse Palace), "
            f"but your Spouse Star is weak ({spouse_star_percentage:.1f}%). "
            f"Controlling tendency with few opportunities creates frustration."
        )
        chain_interpretation_zh = (
            f"链式分析：您在感情中寻求控制（日主克配偶宫），"
            f"但配偶星很弱（{spouse_star_percentage:.1f}%）。"
            f"控制倾向加上机会少会造成挫折。"
        )

    # Build result
    result = {
        "dm_spouse_relationship": dm_spouse_relationship,
        "daymaster_element": daymaster_element,
        "spouse_palace_element": spouse_palace_element,
        "dm_spouse_meaning": dm_spouse_meaning_en if locale == "en" else dm_spouse_meaning_zh,
        "dm_spouse_meaning_en": dm_spouse_meaning_en,
        "dm_spouse_meaning_zh": dm_spouse_meaning_zh,
    }

    if spouse_star_element:
        result["spouse_star_element"] = spouse_star_element
        result["spouse_star_strength"] = spouse_star_strength
        result["spouse_star_percentage"] = spouse_star_percentage
        result["spouse_star_meaning"] = spouse_star_meaning_en if locale == "en" else spouse_star_meaning_zh
        result["spouse_star_meaning_en"] = spouse_star_meaning_en
        result["spouse_star_meaning_zh"] = spouse_star_meaning_zh

    if chain_interpretation_en:
        result["chain_interpretation"] = chain_interpretation_en if locale == "en" else chain_interpretation_zh
        result["chain_interpretation_en"] = chain_interpretation_en
        result["chain_interpretation_zh"] = chain_interpretation_zh

    return result


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


def _generate_ten_gods_narratives(
    ten_gods_detail: Dict[str, Any],
    locale: str
) -> List[Dict[str, Any]]:
    """
    Generate narratives from Ten Gods warnings and opportunities.

    The Ten Gods provide relationship context (what role each element plays
    relative to the daymaster).
    """
    narratives = []

    if not ten_gods_detail:
        return narratives

    # Process warnings
    warnings = ten_gods_detail.get("warnings", [])
    for warning in warnings:
        ten_god = warning.get("ten_god", "")
        ten_god_english = warning.get("ten_god_english", ten_god)
        ten_god_chinese = warning.get("ten_god_chinese", ten_god)
        pillar = warning.get("pillar", "")
        message = warning.get("message", "")
        message_zh = warning.get("message_chinese", message)

        # Get pillar context
        pillar_info = PILLAR_LIFE_AREAS.get(pillar, {})
        pillar_name_en = pillar_info.get("en", {}).get("name", pillar.title())
        pillar_name_zh = pillar_info.get("zh", {}).get("name", pillar)

        if locale == "zh":
            title = f"{ten_god_chinese}受影响"
            summary = f"{pillar_name_zh}的{ten_god_chinese}：{message_zh}"
        else:
            title = f"{ten_god_english} Affected"
            summary = f"{pillar_name_en} {ten_god_english}: {message}"

        narratives.append({
            "id": f"ten_god_warning_{warning.get('node_id', '')}",
            "type": "TEN_GOD_WARNING",
            "category": "ten_gods",
            "polarity": "negative",
            "icon": "warning",
            "color_key": "warning",
            "title": title,
            "summary": summary,
            "ten_god": ten_god,
            "ten_god_english": ten_god_english,
            "ten_god_chinese": ten_god_chinese,
            "pillar": pillar,
            "node_id": warning.get("node_id", ""),
        })

    # Process opportunities
    opportunities = ten_gods_detail.get("opportunities", [])
    for opp in opportunities:
        ten_god = opp.get("ten_god", "")
        ten_god_english = opp.get("ten_god_english", ten_god)
        ten_god_chinese = opp.get("ten_god_chinese", ten_god)
        pillar = opp.get("pillar", "")
        message = opp.get("message", "")
        message_zh = opp.get("message_chinese", message)

        pillar_info = PILLAR_LIFE_AREAS.get(pillar, {})
        pillar_name_en = pillar_info.get("en", {}).get("name", pillar.title())
        pillar_name_zh = pillar_info.get("zh", {}).get("name", pillar)

        if locale == "zh":
            title = f"{ten_god_chinese}机遇"
            summary = f"{pillar_name_zh}的{ten_god_chinese}：{message_zh}"
        else:
            title = f"{ten_god_english} Opportunity"
            summary = f"{pillar_name_en} {ten_god_english}: {message}"

        narratives.append({
            "id": f"ten_god_opp_{opp.get('node_id', '')}",
            "type": "TEN_GOD_OPPORTUNITY",
            "category": "ten_gods",
            "polarity": "positive",
            "icon": "opportunity",
            "color_key": "positive",
            "title": title,
            "summary": summary,
            "ten_god": ten_god,
            "ten_god_english": ten_god_english,
            "ten_god_chinese": ten_god_chinese,
            "pillar": pillar,
            "node_id": opp.get("node_id", ""),
        })

    return narratives


def _generate_pillar_narratives(
    nodes: Dict[str, Any],
    daymaster_analysis: Dict[str, Any],
    locale: str
) -> List[Dict[str, Any]]:
    """
    Generate pillar-by-pillar analysis narratives.

    This provides interpretation of each natal pillar (Year, Month, Day, Hour).
    """
    narratives = []

    # Only generate for natal pillars (not luck pillars)
    pillar_keys = [
        ("hs_y", "eb_y", "year"),
        ("hs_m", "eb_m", "month"),
        ("hs_d", "eb_d", "day"),
        ("hs_h", "eb_h", "hour"),
    ]

    daymaster = daymaster_analysis.get("daymaster", "")

    for hs_key, eb_key, pillar_name in pillar_keys:
        hs_data = nodes.get(hs_key, {})
        eb_data = nodes.get(eb_key, {})

        if not hs_data or not eb_data:
            continue

        # Node structure uses 'id' for stem/branch name
        stem = hs_data.get("id", "")
        branch = eb_data.get("id", "")

        # Get element from stem name using STEM_NAMES mapping
        stem_element = STEM_NAMES.get(stem, {}).get("element", "")
        branch_element = BRANCH_NAMES.get(branch, {}).get("element", "")

        # Get Chinese characters
        stem_chinese = STEM_NAMES.get(stem, {}).get("zh", stem)
        branch_chinese = BRANCH_NAMES.get(branch, {}).get("zh", branch)

        # Get Ten God if available
        ten_god = hs_data.get("ten_god", {})
        ten_god_abbr = ten_god.get("abbreviation", "") if isinstance(ten_god, dict) else ""
        ten_god_name = ten_god.get("name", "") if isinstance(ten_god, dict) else ""

        # Get pillar context
        pillar_info = PILLAR_LIFE_AREAS.get(pillar_name, {})
        pillar_context_en = pillar_info.get("en", {})
        pillar_context_zh = pillar_info.get("zh", {})

        # Only create narrative if we have meaningful data
        if not stem or not branch:
            continue

        # Build narrative text
        if locale == "zh":
            title = f"{pillar_context_zh.get('name', pillar_name)} 分析"
            summary = f"{stem_chinese}{branch_chinese}：天干{stem_element}，地支{branch_element}"
            if ten_god_name:
                summary += f"，{ten_god_name}"
            detail = f"此柱代表：{pillar_context_zh.get('represents', '')}"
        else:
            title = f"{pillar_context_en.get('name', pillar_name.title())} Analysis"
            summary = f"{stem} {branch}: Heavenly Stem {stem_element}, Earthly Branch {branch_element}"
            if ten_god_name:
                summary += f" ({ten_god_name})"
            detail = f"This pillar represents: {pillar_context_en.get('represents', '')}"

        narratives.append({
            "id": f"pillar_{pillar_name}",
            "type": "PILLAR_ANALYSIS",
            "category": "pillar",
            "polarity": "neutral",
            "icon": "pillar",
            "color_key": "neutral",
            "title": title,
            "summary": summary,
            "detail": detail,
            "pillar": pillar_name,
            "stem": stem,
            "branch": branch,
            "stem_element": stem_element,
            "branch_element": branch_element,
            "ten_god": ten_god_abbr,
            "ten_god_name": ten_god_name,
        })

    return narratives
