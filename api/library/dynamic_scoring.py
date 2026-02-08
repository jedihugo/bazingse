# * =========================
# * DYNAMIC SCORING SYSTEM (動態計分系統)
# * =========================
# Core dynamic calculation system for BaZi combinations and conflicts.
# Points are NO LONGER static - calculated based on current qi of interacting nodes.
#
# User-Specified Multipliers (untransformed / combined only):
# - Three Meetings (三會): 0.382
# - Three Combinations (三合): 0.238
# - HS Stem Combinations: 0.238
# - Half Meetings (半會): 0.382
# - Six Harmonies (六合): 0.238
# - Arched Combinations (拱合): 0.146
# - Transformation Bonus: 2.0

from .core import BRANCHES, STEMS
from .unity import WUXING_COMBAT, get_distance_multiplier

# =========================
# COMBINATION MULTIPLIERS
# =========================
COMBINATION_MULTIPLIERS = {
    "THREE_MEETINGS": 0.382,
    "THREE_COMBINATIONS": 0.238,
    "STEM_COMBINATIONS": 0.238,
    "HALF_MEETINGS": 0.382,
    "SIX_HARMONIES": 0.238,
    "ARCHED_COMBINATIONS": 0.146,
}

# Transformation Bonus (successful transformation multiplier)
TRANSFORMATION_BONUS = 2.0


def get_primary_qi_info(branch_value):
    """
    Get the PRIMARY QI (本氣) info for a branch.

    PRIMARY QI is the main energy of the Earthly Branch at index 0.
    This is NOT a hidden stem - it's the dominant, visible energy.

    Hidden Stems (藏干) are at index 1+ and are separate.

    Args:
        branch_value: Branch ID (e.g., "Yin", "Hai")

    Returns:
        tuple: (stem_id, base_qi) - e.g., ("Jia", 60) for Yin Tiger
               Returns (None, 0) if branch not found
    """
    if branch_value not in BRANCHES:
        return (None, 0)

    qi_list = BRANCHES[branch_value].get("qi", [])
    if not qi_list:
        return (None, 0)

    # Primary Qi is index 0 (NOT a hidden stem!)
    primary_stem = qi_list[0][0]  # e.g., "Jia" for Yin
    base_qi = qi_list[0][1]  # e.g., 60 for Yin

    return (primary_stem, base_qi)


# Backward compatibility alias
get_primary_hidden_stem_info = get_primary_qi_info


def get_current_qi_for_stem(node, stem_id):
    """
    Get the current qi value for a specific stem from a node.

    Args:
        node: ElementNode object
        stem_id: Stem ID (e.g., "Jia", "Bing")

    Returns:
        float: Current qi value for the stem's element+polarity
    """
    if stem_id not in STEMS:
        return 0

    elem = STEMS[stem_id]["element"]
    pol = STEMS[stem_id]["polarity"]
    element_key = f"{pol} {elem}"

    return node.elements.get(element_key, {}).get("score", 0)


def calculate_dynamic_combination_score(
    nodes,
    combination_type,
    is_transformed=False,
    distance_multiplier=1.0
):
    """
    Calculate dynamic score for a combination based on current node qi.

    Formula:
        1. Get Primary Qi qi for each branch node (or total qi for HS)
        2. Calculate average of qi values
        3. Apply combination-specific multiplier
        4. Apply transformation bonus if applicable
        5. Apply distance multiplier

    Args:
        nodes: List of ElementNode objects participating in combination
        combination_type: "THREE_MEETINGS", "SIX_HARMONIES", etc.
        is_transformed: Whether the combination successfully transformed
        distance_multiplier: Distance decay factor (1.0 for adjacent)

    Returns:
        tuple: (score, math_formula, qi_details, calculation_details)
            - score: Final calculated score
            - math_formula: Display string for timeline
            - qi_details: List of (stem, qi) tuples for narrative
            - calculation_details: Detailed step-by-step breakdown dict

    Example for Yin-Hai Six Harmony:
        Yin primary qi (Jia): 72.5
        Hai primary qi (Ren): 85.2
        avg(72.5, 85.2) = 78.85
        78.85 * 0.382 = 30.12
        If transformed: 30.12 * 1.618 = 48.73
    """
    qi_values = []
    qi_details = []  # For formula display: [(stem, qi), ...]
    qi_strings = []  # For formula: ["72.5", "85.2"]
    node_qi_info = []  # Detailed per-node info for calculation_details

    for node in nodes:
        if node.node_type == "branch":
            # Get Primary Qi
            stem_id, base_qi = get_primary_qi_info(node.value)
            if stem_id:
                qi = get_current_qi_for_stem(node, stem_id)
                qi_values.append(qi)
                qi_details.append((stem_id, qi, node.node_id))
                qi_strings.append(f"{qi:.1f}")
                # Detailed info including stem element and base qi
                stem_data = STEMS.get(stem_id, {})
                node_qi_info.append({
                    "node_id": node.node_id,
                    "branch": node.value,
                    "primary_qi_stem": stem_id,
                    "primary_qi_stem_chinese": stem_data.get("chinese", "?"),
                    "primary_qi_element": stem_data.get("element", "?"),
                    "base_qi": base_qi,
                    "current_qi": round(qi, 2)
                })
        elif node.node_type == "stem":
            # Stems use their direct qi value
            qi = node.get_total_score()
            qi_values.append(qi)
            qi_details.append((node.value, qi, node.node_id))
            qi_strings.append(f"{qi:.1f}")
            stem_data = STEMS.get(node.value, {})
            node_qi_info.append({
                "node_id": node.node_id,
                "stem": node.value,
                "stem_chinese": stem_data.get("chinese", "?"),
                "element": stem_data.get("element", "?"),
                "current_qi": round(qi, 2)
            })

    if not qi_values:
        return (0, "No qi values", [], {})

    # Calculate average qi
    avg_qi = sum(qi_values) / len(qi_values)

    # Get combination multiplier
    combo_mult = COMBINATION_MULTIPLIERS.get(combination_type, 0.5)

    # Calculate intermediate score (after combo multiplier, before distance/transform)
    after_combo_mult = avg_qi * combo_mult

    # Apply distance multiplier
    after_distance = after_combo_mult * distance_multiplier

    # Build calculation steps for detailed breakdown
    calculation_steps = []

    # Step 1: Qi values from each node
    calculation_steps.append({
        "step": 1,
        "operation": "Get Primary Qi from each node",
        "description": f"Extract the primary qi (本氣) from each participating Earthly Branch",
        "values": node_qi_info,
        "result": [round(q, 2) for q in qi_values]
    })

    # Step 2: Calculate average
    calculation_steps.append({
        "step": 2,
        "operation": "Calculate Average",
        "formula": f"({' + '.join(qi_strings)}) ÷ {len(qi_values)}",
        "description": f"Average of all primary qi values",
        "result": round(avg_qi, 2)
    })

    # Step 3: Apply combination multiplier
    combo_mult_explanation = {
        "THREE_MEETINGS": "三會 (Three Meetings) - Strongest seasonal combination: 0.618 (Golden Ratio)",
        "THREE_COMBINATIONS": "三合 (Three Combinations) - Triangular harmony: 0.5",
        "SIX_HARMONIES": "六合 (Six Harmonies) - Pair harmony: 0.382 (φ⁻²)",
        "HALF_MEETINGS": "半會 (Half Meetings) - Partial seasonal: 0.382 (φ⁻²)",
        "ARCHED_COMBINATIONS": "拱合 (Arched Combinations) - 2/3 of Three Combinations: 0.238",
        "STEM_COMBINATIONS": "天干五合 (Stem Combinations) - Heavenly Stem pairs: 0.5"
    }.get(combination_type, f"{combination_type}: {combo_mult}")

    calculation_steps.append({
        "step": 3,
        "operation": "Apply Combination Multiplier",
        "formula": f"{avg_qi:.2f} × {combo_mult}",
        "multiplier": combo_mult,
        "multiplier_type": combination_type,
        "explanation": combo_mult_explanation,
        "result": round(after_combo_mult, 2)
    })

    # Step 4: Apply distance multiplier (if not 1.0)
    if distance_multiplier != 1.0:
        calculation_steps.append({
            "step": 4,
            "operation": "Apply Distance Decay",
            "formula": f"{after_combo_mult:.2f} × {distance_multiplier}",
            "multiplier": distance_multiplier,
            "explanation": f"Distance decay: farther nodes = weaker effect. Multiplier: {distance_multiplier}",
            "result": round(after_distance, 2)
        })

    # Build formula string and final score
    qi_str = ", ".join(qi_strings)

    if is_transformed:
        final_score = after_distance * TRANSFORMATION_BONUS

        # Step 5: Apply transformation bonus
        calculation_steps.append({
            "step": len(calculation_steps) + 1,
            "operation": "Apply Transformation Bonus",
            "formula": f"{after_distance:.2f} × {TRANSFORMATION_BONUS:.3f}",
            "multiplier": TRANSFORMATION_BONUS,
            "explanation": f"Transformation bonus (φ = Golden Ratio 1.618) - Heavenly Stem supports the transformed element",
            "result": round(final_score, 2)
        })

        # Formula with transformation
        if distance_multiplier != 1.0:
            formula = f"avg({qi_str}) × {combo_mult} × {distance_multiplier} × {TRANSFORMATION_BONUS:.3f} = {final_score:.1f}"
        else:
            formula = f"avg({qi_str}) × {combo_mult} × {TRANSFORMATION_BONUS:.3f} = {final_score:.1f}"
        formula += f" → +{final_score:.1f} (transformed!)"
    else:
        final_score = after_distance

        # Formula without transformation
        if distance_multiplier != 1.0:
            formula = f"avg({qi_str}) × {combo_mult} × {distance_multiplier} = {final_score:.1f}"
        else:
            formula = f"avg({qi_str}) × {combo_mult} = {final_score:.1f}"
        formula += f" → +{final_score:.1f} (combined)"

    # Build complete calculation_details
    calculation_details = {
        "combination_type": combination_type,
        "combination_type_chinese": {
            "THREE_MEETINGS": "三會",
            "THREE_COMBINATIONS": "三合",
            "SIX_HARMONIES": "六合",
            "HALF_MEETINGS": "半會",
            "ARCHED_COMBINATIONS": "拱合",
            "STEM_COMBINATIONS": "天干五合"
        }.get(combination_type, combination_type),
        "is_transformed": is_transformed,
        "transformation_reason": "Heavenly Stem element matches transformed element" if is_transformed else "No matching Heavenly Stem element for full transformation",
        "base_multiplier": combo_mult,
        "distance_multiplier": distance_multiplier,
        "transformation_bonus": TRANSFORMATION_BONUS if is_transformed else None,
        "participating_nodes": node_qi_info,
        "average_qi": round(avg_qi, 2),
        "final_score": round(final_score, 2),
        "steps": calculation_steps,
        "formula_summary": formula
    }

    return (round(final_score, 2), formula, qi_details, calculation_details)


def calculate_dynamic_conflict_score(
    controller_node,
    victim_node,
    conflict_type="CONFLICT",
    distance=1,
    severity_multiplier=1.0,
    amplifier=1.0
):
    """
    Calculate dynamic score for conflicts using Wu Xing Combat Engine.

    Formula:
        min(controller_qi, victim_qi) x 0.5 x distance_mult x severity_mult x amplifier
        controller_damage = result x 0.618
        victim_damage = result x 1.0

    Args:
        controller_node: ElementNode (controller/aggressor)
        victim_node: ElementNode (controlled/victim)
        conflict_type: "PUNISHMENT", "DESTRUCTION", "STEM_CONFLICT", etc.
        distance: Distance between nodes (1-5)
        severity_multiplier: For punishments (severe=1.0, moderate=0.85, light=0.70, self=0.60)
        amplifier: Additional multiplier (1.618 for clash/harm, 1.0 for normal)

    Returns:
        tuple: (controller_damage, victim_damage, math_formula, qi_details)
    """
    # Get qi values
    if controller_node.node_type == "branch":
        stem_id, _ = get_primary_qi_info(controller_node.value)
        controller_qi = get_current_qi_for_stem(controller_node, stem_id) if stem_id else 0
        controller_stem = stem_id
    else:
        controller_qi = controller_node.get_total_score()
        controller_stem = controller_node.value

    if victim_node.node_type == "branch":
        stem_id, _ = get_primary_qi_info(victim_node.value)
        victim_qi = get_current_qi_for_stem(victim_node, stem_id) if stem_id else 0
        victim_stem = stem_id
    else:
        victim_qi = victim_node.get_total_score()
        victim_stem = victim_node.value

    qi_details = [
        (controller_stem, controller_qi, controller_node.node_id),
        (victim_stem, victim_qi, victim_node.node_id)
    ]

    # Calculate using Wu Xing Combat Engine formula
    min_qi = min(controller_qi, victim_qi)
    distance_mult = get_distance_multiplier(distance) if distance > 0 else 1.0

    # Base interaction
    interaction_point = min_qi * WUXING_COMBAT["ENGAGEMENT_RATE"]  # 0.5
    effective = interaction_point * distance_mult * severity_multiplier * amplifier

    # Asymmetric damage (controller 0.618, victim 1.0)
    controller_damage = effective * WUXING_COMBAT["SOURCE_RATIO"]  # 0.618
    victim_damage = effective * WUXING_COMBAT["TARGET_RATIO"]  # 1.0

    # Build formula
    formula = f"min({controller_qi:.1f}, {victim_qi:.1f}) x 0.5"
    if distance_mult != 1.0:
        formula += f" x {distance_mult}"
    if severity_multiplier != 1.0:
        formula += f" x {severity_multiplier:.2f}"
    if amplifier != 1.0:
        formula += f" x {amplifier:.3f}"
    formula += f" = {effective:.1f} -> -{controller_damage:.1f}, -{victim_damage:.1f}"

    return (
        round(controller_damage, 2),
        round(victim_damage, 2),
        formula,
        qi_details
    )


def calculate_symmetric_conflict_score(
    node1,
    node2,
    conflict_type="CONFLICT",
    distance=1,
    severity_multiplier=1.0
):
    """
    Calculate symmetric damage for conflicts where both sides take equal damage.
    Used for self-punishments, same-element clashes, etc.

    Formula:
        min(node1_qi, node2_qi) x 0.5 x distance_mult x severity_mult
        damage = result (same for both nodes)

    Args:
        node1: First ElementNode
        node2: Second ElementNode
        conflict_type: Type of conflict
        distance: Distance between nodes
        severity_multiplier: For punishments

    Returns:
        tuple: (damage, math_formula, qi_details)
    """
    # Get qi values
    if node1.node_type == "branch":
        stem_id, _ = get_primary_qi_info(node1.value)
        node1_qi = get_current_qi_for_stem(node1, stem_id) if stem_id else 0
        node1_stem = stem_id
    else:
        node1_qi = node1.get_total_score()
        node1_stem = node1.value

    if node2.node_type == "branch":
        stem_id, _ = get_primary_qi_info(node2.value)
        node2_qi = get_current_qi_for_stem(node2, stem_id) if stem_id else 0
        node2_stem = stem_id
    else:
        node2_qi = node2.get_total_score()
        node2_stem = node2.value

    qi_details = [
        (node1_stem, node1_qi, node1.node_id),
        (node2_stem, node2_qi, node2.node_id)
    ]

    # Calculate
    min_qi = min(node1_qi, node2_qi)
    distance_mult = get_distance_multiplier(distance) if distance > 0 else 1.0

    # Symmetric damage
    interaction_point = min_qi * WUXING_COMBAT["ENGAGEMENT_RATE"]  # 0.5
    damage = interaction_point * distance_mult * severity_multiplier

    # Build formula
    formula = f"min({node1_qi:.1f}, {node2_qi:.1f}) x 0.5"
    if distance_mult != 1.0:
        formula += f" x {distance_mult}"
    if severity_multiplier != 1.0:
        formula += f" x {severity_multiplier:.2f}"
    formula += f" = {damage:.1f} -> -{damage:.1f} (each)"

    return (round(damage, 2), formula, qi_details)


def format_combination_narrative(
    nodes,
    combination_type,
    pattern,
    element,
    qi_details,
    score,
    is_transformed
):
    """
    Generate detailed narrative for combination events.

    Args:
        nodes: List of node IDs (e.g., ["eb_y", "eb_m"])
        combination_type: Type of combination
        pattern: Pattern string (e.g., "Yin-Hai")
        element: Resulting element
        qi_details: List of (stem, qi, node_id) tuples
        score: Final score
        is_transformed: Whether transformation occurred

    Returns:
        str: Human-readable narrative
    """
    # Build node locations
    pillar_map = {"y": "Year", "m": "Month", "d": "Day", "h": "Hour"}
    node_names = []
    for node_id in nodes:
        suffix = node_id.split("_")[1] if "_" in node_id else ""
        pillar = pillar_map.get(suffix, suffix.upper())
        node_type = "HS" if node_id.startswith("hs_") else "EB"
        node_names.append(f"{pillar} {node_type}")

    # Build qi details string
    qi_parts = []
    for stem, qi, node_id in qi_details:
        if stem:
            chinese = STEMS[stem]["chinese"] if stem in STEMS else stem
            qi_parts.append(f"{stem}({chinese})={qi:.1f}")

    combo_name = combination_type.replace("_", " ").title()
    multiplier = COMBINATION_MULTIPLIERS.get(combination_type, 0.5)

    narrative = f"{' and '.join(node_names)} formed {combo_name} ({pattern}). "
    narrative += f"Primary qi: {', '.join(qi_parts)}. "
    narrative += f"Calculation: avg x {multiplier}"
    if is_transformed:
        narrative += f" x {TRANSFORMATION_BONUS:.3f} (transformed)"
    narrative += f" = {score:.1f}. "
    narrative += f"Result: +{score:.1f} {element} qi added"
    if is_transformed:
        narrative += " (fully transformed!)"
    else:
        narrative += " (combined)"
    narrative += "."

    return narrative


def format_conflict_narrative(
    controller_node_id,
    victim_node_id,
    conflict_type,
    pattern,
    qi_details,
    controller_damage,
    victim_damage,
    severity=""
):
    """
    Generate detailed narrative for conflict events.

    Args:
        controller_node_id: Controller node ID
        victim_node_id: Victim node ID
        conflict_type: Type of conflict
        pattern: Pattern string
        qi_details: List of (stem, qi, node_id) tuples
        controller_damage: Damage to controller
        victim_damage: Damage to victim
        severity: Severity level (for punishments)

    Returns:
        str: Human-readable narrative
    """
    pillar_map = {"y": "Year", "m": "Month", "d": "Day", "h": "Hour"}

    def get_node_name(node_id):
        suffix = node_id.split("_")[1] if "_" in node_id else ""
        pillar = pillar_map.get(suffix, suffix.upper())
        node_type = "HS" if node_id.startswith("hs_") else "EB"
        return f"{pillar} {node_type}"

    controller_name = get_node_name(controller_node_id)
    victim_name = get_node_name(victim_node_id)

    # Build qi details
    qi_parts = []
    for stem, qi, node_id in qi_details:
        if stem:
            chinese = STEMS[stem]["chinese"] if stem in STEMS else stem
            node_name = get_node_name(node_id)
            qi_parts.append(f"{stem}({chinese})@{node_name}={qi:.1f}")

    conflict_name = conflict_type.replace("_", " ").title()

    narrative = f"{controller_name} {conflict_name.lower()}s with {victim_name} ({pattern})"
    if severity:
        narrative += f" [{severity}]"
    narrative += ". "
    narrative += f"Primary qi: {', '.join(qi_parts)}. "
    narrative += f"Result: Controller lost {controller_damage:.1f}, Victim lost {victim_damage:.1f}."

    return narrative
