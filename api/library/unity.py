# * =========================
# * WU XING COMBAT ENGINE (五行戰鬥引擎)
# * =========================
# Core combat system for ALL Wu Xing element interactions.
# This is the foundation for:
# - Pillar Unity: HS↔EB within same pillar (distance=1.0, amplifier=1.0)
# - Cross-pillar interactions (with distance modifier)
# - Combinations/Transformations (生 generation cycle)
# - Clashes/Harms (克 control cycle, amplifier=1.618)
# - Punishments (amplifier varies by severity)

WUXING_COMBAT = {
    # Base interaction formula
    "ENGAGEMENT_RATE": 0.382,    # φ² - interaction_point = min(qi) × 0.382
    "SOURCE_RATIO": 0.618,       # Golden ratio φ - source loses 0.618 of interaction
    "TARGET_RATIO": 1.0,         # Target loses/gains 1.0 of interaction

    # Amplifiers for special interactions
    "AMPLIFIER_CLASH": 1.618,    # Golden ratio φ for clashes (沖)
    "AMPLIFIER_HARM": 1.618,     # Golden ratio φ for harms (害)
    "AMPLIFIER_NORMAL": 1.0,     # Normal interactions

    # Distance multipliers for qi interactions (Primary Qi + Hidden Stems)
    # Distance includes penalty: +1 for Hidden Stems (index 1+)
    "DISTANCE_MULTIPLIERS": {
        1: 1.0,      # Distance 1: HS ↔ Primary Qi (base pillar unity)
        2: 0.618,    # Distance 2: HS ↔ Hidden Stem (golden ratio φ)
        3: 0.5,      # Distance 3
        4: 0.382,    # Distance 4 (φ²)
        5: 0.236,    # Distance 5 (φ³)
        # Distance > 5: No interaction (returns 0.0)
    }
}


def get_distance_multiplier(distance):
    """
    Get the distance multiplier for Wu Xing interactions.

    Distance includes qi type penalty:
    - HS ↔ Primary Qi: distance 1 (no penalty)
    - HS ↔ Hidden Stem: distance 2 (+1 penalty for being hidden)
    - Hidden Stem ↔ Hidden Stem: distance base + 2

    Args:
        distance: Integer distance (1-5, or > 5 for no interaction)

    Returns:
        float: Multiplier (1.0 for distance 1, decays with distance)
        Returns 0.0 for distance > 5 (no interaction)
    """
    multipliers = WUXING_COMBAT["DISTANCE_MULTIPLIERS"]
    if distance in multipliers:
        return multipliers[distance]
    # For distances beyond 5, no interaction
    return 0.0


def get_qi_type(stem_index):
    """
    Determine if a qi value is Primary Qi or Hidden Stem based on index.

    BaZi Terminology:
    - PRIMARY_QI (本氣): Index 0 - main energy of the branch, NOT hidden
    - HIDDEN_STEM (藏干): Index 1+ - secondary/tertiary energies, actually hidden

    Args:
        stem_index: Position in the branch's qi list (0, 1, or 2)

    Returns:
        str: "PRIMARY_QI" if index 0, "HIDDEN_STEM" if index 1+
    """
    return "PRIMARY_QI" if stem_index == 0 else "HIDDEN_STEM"


# Backward compatibility alias
get_hidden_stem_priority = get_qi_type


def calculate_hidden_penalty(source_is_hs, source_priority, target_is_hs, target_priority):
    """
    Calculate the penalty for qi interactions based on visibility.

    BaZi Terminology:
    - PRIMARY_QI (本氣): Main energy at index 0 - visible, no penalty
    - HIDDEN_STEM (藏干): Secondary/tertiary at index 1+ - hidden, adds penalty

    Rules:
    - HS ↔ Primary Qi: penalty = 0 (both visible)
    - HS ↔ Hidden Stem: penalty = 1 (target is hidden)
    - Primary Qi ↔ Hidden Stem: penalty = 1
    - Hidden Stem ↔ Hidden Stem: penalty = 2 (both hidden)

    Args:
        source_is_hs: True if source is a Heavenly Stem
        source_priority: "PRIMARY" (Primary Qi) or "SECONDARY" (Hidden Stem)
        target_is_hs: True if target is a Heavenly Stem
        target_priority: "PRIMARY" (Primary Qi) or "SECONDARY" (Hidden Stem)

    Returns:
        int: Visibility penalty (0, 1, or 2)
    """
    # HS (Heavenly Stem) interacting with EB qi
    if source_is_hs:
        # HS ↔ Primary Qi: no penalty (both visible)
        if target_priority == "PRIMARY":
            return 0
        # HS ↔ Hidden Stem: +1 penalty
        return 1

    if target_is_hs:
        # Primary Qi ↔ HS: no penalty
        if source_priority == "PRIMARY":
            return 0
        # Hidden Stem ↔ HS: +1 penalty
        return 1

    # Both are EB qi values
    if source_priority == "PRIMARY" and target_priority == "PRIMARY":
        return 0  # Both Primary Qi - visible
    elif source_priority == "SECONDARY" and target_priority == "SECONDARY":
        return 2  # Both Hidden Stems - both hidden
    else:
        # Primary Qi ↔ Hidden Stem
        return 1


def format_interaction_math(source_qi, target_qi, distance_multiplier, source_loss, target_change, is_control=True):
    """
    Generate a 1-liner math formula for UI display.

    Format: "min(100,60)×0.5×0.618 = 18.5 → -11.4, -18.5" (control)
            "min(100,60)×0.5×0.618 = 18.5 → -11.4, +18.5" (generation)

    Args:
        source_qi: Source qi value before interaction
        target_qi: Target qi value before interaction
        distance_multiplier: Distance multiplier applied
        source_loss: Calculated source loss (positive value)
        target_change: Calculated target change (positive value, sign added based on is_control)
        is_control: True for control (target loses), False for generation (target gains)

    Returns:
        str: Formatted math string
    """
    min_qi = min(source_qi, target_qi)
    interaction_base = min_qi * 0.5

    # Build formula
    if distance_multiplier == 1.0:
        # Omit ×1.0 for cleaner display
        formula = f"min({source_qi:.0f},{target_qi:.0f})×0.5"
        result = interaction_base
    else:
        formula = f"min({source_qi:.0f},{target_qi:.0f})×0.5×{distance_multiplier}"
        result = interaction_base * distance_multiplier

    # Format result with sign indicators
    target_sign = "-" if is_control else "+"

    return f"{formula} = {result:.1f} → -{source_loss:.1f}, {target_sign}{abs(target_change):.1f}"


def apply_wuxing_interaction(source_qi, target_qi, distance_modifier=1.0, amplifier=1.0):
    """
    Core Wu Xing combat engine. Calculates qi changes when elements interact.

    Formula:
        interaction_point = min(source_qi, target_qi) × 0.5
        effective_interaction = interaction_point × distance_modifier × amplifier
        source_change = effective_interaction × 0.618
        target_change = effective_interaction × 1.0

    Args:
        source_qi: Current qi of the source element (controller or producer)
        target_qi: Current qi of the target element (controlled or receiver)
        distance_modifier: 1.0 for same pillar, decays with distance
        amplifier: 1.0 normal, 1.618 for clash/harm

    Returns:
        tuple: (source_loss, target_change)

    Example - Control (克) with clash amplifier:
        Water 100 controls Fire 70 (clash, distance=2):
        - interaction_point = min(100, 70) × 0.5 = 35
        - effective = 35 × 0.618 × 1.618 = 35.00
        - source_loss = 35 × 0.618 = 21.63
        - target_loss = 35 × 1.0 = 35
        - Returns: (21.63, 35)

    Example - Generation (生):
        Wood 60 produces Fire 100:
        - interaction_point = min(60, 100) × 0.5 = 30
        - source_loss = 30 × 0.618 = 18.54
        - target_gain = 30 × 1.0 = 30
        - Returns: (18.54, 30)
    """
    interaction_point = min(source_qi, target_qi) * WUXING_COMBAT["ENGAGEMENT_RATE"]
    effective = interaction_point * distance_modifier * amplifier
    source_loss = effective * WUXING_COMBAT["SOURCE_RATIO"]
    target_change = effective * WUXING_COMBAT["TARGET_RATIO"]
    return (source_loss, target_change)


def calculate_wuxing_control(controller_qi, controlled_qi, distance=0, is_clash=False, is_harm=False):
    """
    Calculate Wu Xing control interaction (克).
    Both controller and controlled lose qi.

    Args:
        controller_qi: Qi of the controlling element
        controlled_qi: Qi of the controlled element
        distance: Distance between nodes (0 = same pillar)
        is_clash: If True, apply 1.618 amplifier
        is_harm: If True, apply 1.618 amplifier

    Returns:
        dict: {
            'controller_loss': float,
            'controlled_loss': float,
            'interaction_point': float,
            'effective': float
        }
    """
    distance_mod = get_distance_multiplier(distance)
    amplifier = WUXING_COMBAT["AMPLIFIER_NORMAL"]
    if is_clash or is_harm:
        amplifier = WUXING_COMBAT["AMPLIFIER_CLASH"]

    controller_loss, controlled_loss = apply_wuxing_interaction(
        controller_qi, controlled_qi, distance_mod, amplifier
    )

    return {
        'controller_loss': controller_loss,
        'controlled_loss': controlled_loss,
        'interaction_point': min(controller_qi, controlled_qi) * WUXING_COMBAT["ENGAGEMENT_RATE"],
        'effective': min(controller_qi, controlled_qi) * WUXING_COMBAT["ENGAGEMENT_RATE"] * distance_mod * amplifier,
        'distance_modifier': distance_mod,
        'amplifier': amplifier
    }


def calculate_wuxing_generation(producer_qi, receiver_qi, distance=0):
    """
    Calculate Wu Xing generation interaction (生).
    Producer loses qi, receiver gains qi.

    Args:
        producer_qi: Qi of the producing element
        receiver_qi: Qi of the receiving element
        distance: Distance between nodes (0 = same pillar)

    Returns:
        dict: {
            'producer_loss': float,
            'receiver_gain': float,
            'interaction_point': float,
            'effective': float
        }
    """
    distance_mod = get_distance_multiplier(distance)
    amplifier = WUXING_COMBAT["AMPLIFIER_NORMAL"]

    producer_loss, receiver_gain = apply_wuxing_interaction(
        producer_qi, receiver_qi, distance_mod, amplifier
    )

    return {
        'producer_loss': producer_loss,
        'receiver_gain': receiver_gain,
        'interaction_point': min(producer_qi, receiver_qi) * WUXING_COMBAT["ENGAGEMENT_RATE"],
        'effective': min(producer_qi, receiver_qi) * WUXING_COMBAT["ENGAGEMENT_RATE"] * distance_mod * amplifier,
        'distance_modifier': distance_mod,
        'amplifier': amplifier
    }

# * =========================
# * HIDDEN QI INTERACTIONS (藏干相剋)
# * =========================
# Classical BaZi principle: Primary and secondary qi always interact,
# tertiary/residual qi (余氣) can engage during seasonal transitions

HIDDEN_QI_INTERACTIONS = {
    "PRIMARY_PRIMARY": 1.0,      # Full interaction between primary Qi
    "PRIMARY_SECONDARY": 0.5,    # Half interaction with secondary Qi
    "SECONDARY_SECONDARY": 0.25, # Quarter interaction between secondary Qi
    "PRIMARY_TERTIARY": 0.30,    # Tertiary qi (余氣) interaction - weaker but present
    "SECONDARY_TERTIARY": 0.15,  # Secondary-tertiary cross interaction
    "TERTIARY_TERTIARY": 0.10,   # Rare - both nodes have tertiary qi conflict
    "damage": {
        "damage_factor": 0.15,           # For negative interactions on hidden qi
        "tertiary_damage_factor": 0.05   # Reduced damage for tertiary qi interactions
    }
}
