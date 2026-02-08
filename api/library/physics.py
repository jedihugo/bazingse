# =============================================================================
# PHYSICS SCHOOL - Stem Imagery & Element State Engine
# =============================================================================
# The "physics" school considers the NATURE of each stem (ocean vs dew),
# the QUANTITY in the chart, and ELEMENT STATES (e.g., Wet Wood can't fuel Fire).
#
# This module runs as a POST-PROCESSING MODIFIER LAYER on top of the classic
# Wu Xing combat engine. It does NOT replace unity.py — it modifies results.
#
# Architecture:
#   1. Classic combat runs as normal → base source_loss and target_change
#   2. Physics layer looks up STEM_IMAGERY for the specific stem pair
#   3. Physics layer checks active ELEMENT_STATES for blocked production/control
#   4. Modifies the base result (e.g., Wet Wood → Fire production reduced to 10%)
#   5. Logs physics-specific narrative
# =============================================================================

from typing import Dict, List, Optional, Tuple

# =============================================================================
# STEM IMAGERY MATRIX (10 × 10 = 100 pairs, 40 priority pairs for MVP)
# =============================================================================
# Every stem pair gets an interaction profile instead of relying solely on
# generic element cycles. The key is (source_stem, target_stem).
#
# 7 outcome categories:
#   harmonious     — balanced, beneficial interaction
#   overwhelming   — source overpowers target
#   insufficient   — source too weak to affect target
#   destructive    — both sides damaged beyond normal
#   reversed       — expected direction flips
#   transformative — interaction creates something new
#   stalemate      — neither side can affect the other
#
# source_modifier: applied to source's loss (negative = source loses MORE)
# target_modifier: applied to target's change (negative = target loses MORE, positive = gains MORE)
# These are MULTIPLIERS on top of the classic result, where 0.0 = no change, 1.0 = double.

STEM_IMAGERY: Dict[Tuple[str, str], dict] = {
    # =====================================================
    # PRODUCTION CYCLE (生) — 20 pairs (5 elements × 2 polarities × 2 target polarities)
    # Wood generates Fire
    # =====================================================
    ("Jia", "Bing"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,      # Normal exhaustion
        "target_modifier": 0.2,      # Big tree burns well → +20% Fire gain
        "imagery": "forest_fuels_sun",
        "zh": "甲木参天助丙火",
        "en": "Towering forest fuels the blazing sun",
    },
    ("Jia", "Ding"): {
        "outcome": "overwhelming",
        "wuxing_relation": "generation",
        "source_modifier": 0.1,      # Big tree barely affected
        "target_modifier": -0.3,     # Candle smothered by too much wood
        "imagery": "log_smothers_candle",
        "zh": "甲木粗大压丁火",
        "en": "Massive log smothers the candle flame",
    },
    ("Yi", "Bing"): {
        "outcome": "insufficient",
        "wuxing_relation": "generation",
        "source_modifier": -0.2,     # Vine exhausts faster
        "target_modifier": -0.4,     # Sun barely notices small kindling
        "imagery": "vine_too_small_for_sun",
        "zh": "乙木柔弱难助丙火",
        "en": "Delicate vine too small to fuel the blazing sun",
    },
    ("Yi", "Ding"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,      # Normal exhaustion
        "target_modifier": 0.3,      # Perfect match: small wood + candle
        "imagery": "kindling_lights_candle",
        "zh": "乙木轻柴点丁火",
        "en": "Dry kindling perfectly lights the candle",
    },

    # Fire generates Earth
    ("Bing", "Wu"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.2,      # Sun warms mountain → good nourishment
        "imagery": "sun_warms_mountain",
        "zh": "丙火暖戊土山",
        "en": "Blazing sun warms the great mountain",
    },
    ("Bing", "Ji"): {
        "outcome": "overwhelming",
        "wuxing_relation": "generation",
        "source_modifier": 0.1,
        "target_modifier": -0.3,     # Sun scorches garden soil → dries it out
        "imagery": "sun_scorches_garden",
        "zh": "丙火烈炎燥己土",
        "en": "Scorching sun dries out the garden soil",
    },
    ("Ding", "Wu"): {
        "outcome": "insufficient",
        "wuxing_relation": "generation",
        "source_modifier": -0.2,
        "target_modifier": -0.4,     # Candle can't warm a mountain
        "imagery": "candle_cant_warm_mountain",
        "zh": "丁火微弱难暖戊山",
        "en": "Candle flame cannot warm the great mountain",
    },
    ("Ding", "Ji"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.3,      # Candle warms garden → gentle nourishment
        "imagery": "hearth_warms_garden",
        "zh": "丁火温暖己土园",
        "en": "Warm hearth gently nourishes the garden",
    },

    # Earth generates Metal
    ("Wu", "Geng"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.2,      # Mountain contains ore → good resource
        "imagery": "mountain_bears_ore",
        "zh": "戊土高山藏庚金",
        "en": "Great mountain bears rich ore within",
    },
    ("Wu", "Xin"): {
        "outcome": "overwhelming",
        "wuxing_relation": "generation",
        "source_modifier": 0.1,
        "target_modifier": -0.3,     # Mountain buries jewelry → too heavy
        "imagery": "mountain_buries_jewel",
        "zh": "戊土厚重埋辛金",
        "en": "Heavy mountain buries the delicate jewel",
    },
    ("Ji", "Geng"): {
        "outcome": "insufficient",
        "wuxing_relation": "generation",
        "source_modifier": -0.2,
        "target_modifier": -0.4,     # Garden soil too thin to hold ore
        "imagery": "soil_too_thin_for_ore",
        "zh": "己土薄弱难育庚金",
        "en": "Thin garden soil cannot nurture heavy ore",
    },
    ("Ji", "Xin"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.3,      # Garden soil polishes gems
        "imagery": "soil_polishes_gem",
        "zh": "己土柔润养辛金",
        "en": "Rich garden soil polishes the precious gem",
    },

    # Metal generates Water
    ("Geng", "Ren"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.2,      # Axe cuts channel for river
        "imagery": "axe_opens_riverbed",
        "zh": "庚金劈山引壬水",
        "en": "Great axe carves the mountain for the river",
    },
    ("Geng", "Gui"): {
        "outcome": "overwhelming",
        "wuxing_relation": "generation",
        "source_modifier": 0.1,
        "target_modifier": -0.3,     # Axe shatters dewdrop
        "imagery": "axe_shatters_dew",
        "zh": "庚金粗砺碎癸水",
        "en": "Heavy axe shatters the delicate dewdrop",
    },
    ("Xin", "Ren"): {
        "outcome": "insufficient",
        "wuxing_relation": "generation",
        "source_modifier": -0.2,
        "target_modifier": -0.4,     # Jewelry too small to feed ocean
        "imagery": "jewel_lost_in_ocean",
        "zh": "辛金微小投壬洋",
        "en": "Tiny jewel dissolves in the vast ocean",
    },
    ("Xin", "Gui"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.3,      # Jewelry condenses dew — elegant match
        "imagery": "jewel_condenses_dew",
        "zh": "辛金凝露生癸水",
        "en": "Cool jewel condenses morning dew perfectly",
    },

    # Water generates Wood
    ("Ren", "Jia"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.2,      # River irrigates forest
        "imagery": "river_nourishes_forest",
        "zh": "壬水江河润甲木",
        "en": "Great river nourishes the towering forest",
    },
    ("Ren", "Yi"): {
        "outcome": "overwhelming",
        "wuxing_relation": "generation",
        "source_modifier": 0.1,      # Ocean barely affected
        "target_modifier": -0.8,     # Ocean drowns the vine — devastating
        "imagery": "ocean_drowns_vine",
        "zh": "壬水汪洋淹乙木",
        "en": "Vast ocean drowns the delicate vine",
    },
    ("Gui", "Jia"): {
        "outcome": "insufficient",
        "wuxing_relation": "generation",
        "source_modifier": -0.2,
        "target_modifier": -0.4,     # Dewdrop can't water a forest
        "imagery": "dew_cant_water_forest",
        "zh": "癸水微弱难润甲林",
        "en": "Tiny dewdrop cannot water the vast forest",
    },
    ("Gui", "Yi"): {
        "outcome": "harmonious",
        "wuxing_relation": "generation",
        "source_modifier": 0.0,
        "target_modifier": 0.3,      # Dew nurtures vine — perfect match
        "imagery": "dew_nurtures_vine",
        "zh": "癸水甘露养乙草",
        "en": "Sweet dew gently nurtures the tender vine",
    },

    # =====================================================
    # CONTROL CYCLE (克) — 20 pairs (5 elements × 2 polarities × 2 target polarities)
    # Wood controls Earth
    # =====================================================
    ("Jia", "Wu"): {
        "outcome": "stalemate",
        "wuxing_relation": "control",
        "source_modifier": -0.3,     # Tree roots crack but mountain endures
        "target_modifier": 0.3,      # Mountain barely scratched
        "imagery": "tree_vs_mountain",
        "zh": "甲木克戊土如撼山",
        "en": "Tree roots crack against the immovable mountain",
    },
    ("Jia", "Ji"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Tree plows garden — normal control
        "imagery": "tree_plows_garden",
        "zh": "甲木根植己土田",
        "en": "Tree roots break apart the garden soil",
    },
    ("Yi", "Wu"): {
        "outcome": "reversed",
        "wuxing_relation": "control",
        "source_modifier": -0.5,     # Vine breaks on mountain — reversal
        "target_modifier": 0.5,      # Mountain unaffected
        "imagery": "vine_breaks_on_mountain",
        "zh": "乙木柔弱攀戊山反折",
        "en": "Delicate vine snaps climbing the great mountain",
    },
    ("Yi", "Ji"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Vine spreads through garden — normal
        "imagery": "vine_spreads_garden",
        "zh": "乙木蔓延克己田",
        "en": "Vine spreads through the garden soil",
    },

    # Fire controls Metal
    ("Bing", "Geng"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Sun melts ore — proper forging
        "imagery": "sun_forges_metal",
        "zh": "丙火熔炼庚金矿",
        "en": "Blazing sun forges the raw ore into steel",
    },
    ("Bing", "Xin"): {
        "outcome": "destructive",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": -0.4,     # Sun vaporizes jewelry — excessive
        "imagery": "sun_vaporizes_jewel",
        "zh": "丙火烈焰毁辛金宝",
        "en": "Blazing sun vaporizes the precious jewel",
    },
    ("Ding", "Geng"): {
        "outcome": "insufficient",
        "wuxing_relation": "control",
        "source_modifier": -0.3,     # Candle can't melt an axe
        "target_modifier": 0.4,      # Axe barely warm
        "imagery": "candle_cant_melt_axe",
        "zh": "丁火微弱难熔庚斧",
        "en": "Candle flame cannot melt the heavy axe",
    },
    ("Ding", "Xin"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Candle refines jewelry — craftsmanship
        "imagery": "candle_refines_jewel",
        "zh": "丁火精炼辛金器",
        "en": "Skilled flame refines the precious jewel",
    },

    # Earth controls Water
    ("Wu", "Ren"): {
        "outcome": "stalemate",
        "wuxing_relation": "control",
        "source_modifier": -0.3,     # Mountain erodes trying to dam river
        "target_modifier": 0.3,      # River finds a way around
        "imagery": "mountain_dams_river",
        "zh": "戊土筑坝挡壬江难全",
        "en": "Mountain dam holds but river slowly erodes it",
    },
    ("Wu", "Gui"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Mountain absorbs dew — easy
        "imagery": "mountain_absorbs_dew",
        "zh": "戊土高山化癸露",
        "en": "Great mountain easily absorbs the morning dew",
    },
    ("Ji", "Ren"): {
        "outcome": "reversed",
        "wuxing_relation": "control",
        "source_modifier": -0.5,     # Garden soil washed away by river
        "target_modifier": 0.5,      # River strengthened by mud
        "imagery": "river_washes_garden",
        "zh": "壬水冲己田反强",
        "en": "Raging river washes away the garden soil",
    },
    ("Ji", "Gui"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Garden soil absorbs dew — natural
        "imagery": "garden_absorbs_dew",
        "zh": "己土田园纳癸露",
        "en": "Garden soil naturally absorbs the dew",
    },

    # Metal controls Wood
    ("Geng", "Jia"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Axe chops tree — classic control
        "imagery": "axe_chops_tree",
        "zh": "庚金利斧伐甲木",
        "en": "Sharp axe chops the tall tree",
    },
    ("Geng", "Yi"): {
        "outcome": "destructive",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": -0.4,     # Axe overkill on vine
        "imagery": "axe_obliterates_vine",
        "zh": "庚金重斧劈乙草",
        "en": "Heavy axe obliterates the tender vine",
    },
    ("Xin", "Jia"): {
        "outcome": "insufficient",
        "wuxing_relation": "control",
        "source_modifier": -0.3,     # Jewelry dull against tree
        "target_modifier": 0.4,      # Tree barely scratched
        "imagery": "jewel_cant_cut_tree",
        "zh": "辛金柔弱难伐甲林",
        "en": "Delicate jewel cannot cut the mighty tree",
    },
    ("Xin", "Yi"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Scissors trim vine — proper pruning
        "imagery": "scissors_trim_vine",
        "zh": "辛金剪刀修乙藤",
        "en": "Precise scissors trim the growing vine",
    },

    # Water controls Fire
    ("Ren", "Bing"): {
        "outcome": "stalemate",
        "wuxing_relation": "control",
        "source_modifier": -0.2,     # Ocean evaporates fighting sun
        "target_modifier": 0.2,      # Sun creates steam but holds
        "imagery": "ocean_vs_sun",
        "zh": "壬水汪洋对丙日难灭",
        "en": "Vast ocean steams but cannot extinguish the sun",
    },
    ("Ren", "Ding"): {
        "outcome": "destructive",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": -0.5,     # Ocean crushes candle instantly
        "imagery": "ocean_drowns_candle",
        "zh": "壬水汪洋灭丁烛",
        "en": "Vast ocean instantly drowns the candle",
    },
    ("Gui", "Bing"): {
        "outcome": "reversed",
        "wuxing_relation": "control",
        "source_modifier": -0.5,     # Dew evaporated by sun
        "target_modifier": 0.5,      # Sun strengthened
        "imagery": "sun_evaporates_dew",
        "zh": "丙火蒸癸露反强",
        "en": "Blazing sun evaporates the dew and grows stronger",
    },
    ("Gui", "Ding"): {
        "outcome": "harmonious",
        "wuxing_relation": "control",
        "source_modifier": 0.0,
        "target_modifier": 0.0,      # Dew quenches candle — normal control
        "imagery": "dew_quenches_candle",
        "zh": "癸水甘露熄丁烛",
        "en": "Morning dew gently quenches the candle",
    },
}


# =============================================================================
# ELEMENT STATES — Modified states triggered by quantity imbalance
# =============================================================================
# When one element overwhelms another by quantity (qi ratio ≥ threshold),
# the base element enters a modified state that BLOCKS certain actions.
#
# threshold_ratio: trigger_element_total / base_element_total must be >= this
# blocked_action: what the base element can no longer do while in this state
# production_factor: multiplier on production output (1.0 = normal, 0.1 = 90% blocked)

ELEMENT_STATES: Dict[str, dict] = {
    "wet_wood": {
        "name_en": "Wet Wood",
        "name_zh": "濕木",
        "name_id": "Kayu Basah",
        "base_element": "Wood",
        "trigger_element": "Water",
        "threshold_ratio": 2.0,
        "blocked_action": "produce_fire",
        "production_factor": 0.1,   # Wood can only produce 10% of normal Fire
        "description_en": "Too much Water saturates Wood — soggy wood cannot burn",
        "description_zh": "水多木浮 — 湿木不能生火",
        "description_id": "Terlalu banyak Air membuat Kayu basah — tidak bisa menyala",
    },
    "molten_metal": {
        "name_en": "Molten Metal",
        "name_zh": "熔金",
        "name_id": "Logam Cair",
        "base_element": "Metal",
        "trigger_element": "Fire",
        "threshold_ratio": 2.0,
        "blocked_action": "control_wood",
        "production_factor": 0.1,   # Metal can only control 10% of normal Wood
        "description_en": "Too much Fire melts Metal — liquid metal cannot chop Wood",
        "description_zh": "火多金熔 — 熔金不能克木",
        "description_id": "Terlalu banyak Api melelehkan Logam — tidak bisa memotong Kayu",
    },
    "mud": {
        "name_en": "Mud",
        "name_zh": "泥土",
        "name_id": "Lumpur",
        "base_element": "Earth",
        "trigger_element": "Water",
        "threshold_ratio": 2.0,
        "blocked_action": "control_water",
        "production_factor": 0.1,   # Earth can only control 10% of normal Water
        "description_en": "Too much Water turns Earth to mud — mud cannot dam Water",
        "description_zh": "水多土流 — 泥土不能制水",
        "description_id": "Terlalu banyak Air mengubah Tanah jadi lumpur — tidak bisa membendung Air",
    },
    "smothered_fire": {
        "name_en": "Smothered Fire",
        "name_zh": "埋火",
        "name_id": "Api Tertimbun",
        "base_element": "Fire",
        "trigger_element": "Earth",
        "threshold_ratio": 2.0,
        "blocked_action": "control_metal",
        "production_factor": 0.1,   # Fire can only control 10% of normal Metal
        "description_en": "Too much Earth smothers Fire — buried flame cannot forge Metal",
        "description_zh": "土多火埋 — 埋火不能克金",
        "description_id": "Terlalu banyak Tanah menimbun Api — tidak bisa melebur Logam",
    },
    "frozen_water": {
        "name_en": "Frozen Water",
        "name_zh": "冰水",
        "name_id": "Air Beku",
        "base_element": "Water",
        "trigger_element": "Metal",
        "threshold_ratio": 2.0,
        "blocked_action": "produce_wood",
        "production_factor": 0.1,   # Water can only produce 10% of normal Wood
        "description_en": "Too much Metal freezes Water — ice cannot nourish Wood",
        "description_zh": "金多水寒 — 冰水不能生木",
        "description_id": "Terlalu banyak Logam membekukan Air — tidak bisa menumbuhkan Kayu",
    },
}

# Lookup: which element state applies for a given (base_element, action) pair
# action is "produce_X" or "control_X"
_STATE_BY_BLOCKED_ACTION: Dict[str, str] = {
    state["blocked_action"]: state_id
    for state_id, state in ELEMENT_STATES.items()
}

# Lookup: base_element → list of possible states
_STATES_BY_BASE_ELEMENT: Dict[str, List[str]] = {}
for _sid, _sdata in ELEMENT_STATES.items():
    _base = _sdata["base_element"]
    if _base not in _STATES_BY_BASE_ELEMENT:
        _STATES_BY_BASE_ELEMENT[_base] = []
    _STATES_BY_BASE_ELEMENT[_base].append(_sid)

# Chain reaction map: if state X is active, what downstream effects occur?
# E.g., wet_wood blocks Fire production → Fire weakened → Fire controls Metal less
CHAIN_REACTION_MAP: Dict[str, dict] = {
    "wet_wood": {
        "blocked_production": ("Wood", "Fire"),
        "downstream": "Fire weakened → Metal less controlled",
        "downstream_element": "Fire",
        "downstream_effect": "weaken",
        "downstream_factor": 0.7,  # Fire effectiveness reduced to 70%
    },
    "molten_metal": {
        "blocked_production": ("Metal", "Wood"),
        "downstream": "Wood grows unchecked → Earth more controlled",
        "downstream_element": "Wood",
        "downstream_effect": "strengthen",
        "downstream_factor": 1.3,  # Wood effectiveness increased to 130%
    },
    "mud": {
        "blocked_production": ("Earth", "Water"),
        "downstream": "Water flows unchecked → Fire more controlled",
        "downstream_element": "Water",
        "downstream_effect": "strengthen",
        "downstream_factor": 1.3,
    },
    "smothered_fire": {
        "blocked_production": ("Fire", "Metal"),
        "downstream": "Metal uncontrolled → Wood more controlled",
        "downstream_element": "Metal",
        "downstream_effect": "strengthen",
        "downstream_factor": 1.3,
    },
    "frozen_water": {
        "blocked_production": ("Water", "Wood"),
        "downstream": "Wood weakened → Earth less controlled",
        "downstream_element": "Wood",
        "downstream_effect": "weaken",
        "downstream_factor": 0.7,
    },
}

# Wu Xing cycle lookups
_PRODUCES: Dict[str, str] = {
    "Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
    "Metal": "Water", "Water": "Wood",
}
_CONTROLS: Dict[str, str] = {
    "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
    "Metal": "Wood", "Water": "Fire",
}


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def get_stem_interaction(source_stem: str, target_stem: str) -> Optional[dict]:
    """Look up the stem imagery interaction profile for a specific pair.

    Returns None if the pair is not in the priority matrix (falls back to classic).
    """
    return STEM_IMAGERY.get((source_stem, target_stem))


def _aggregate_element_scores(element_scores: dict) -> Dict[str, float]:
    """Aggregate stem-level scores (e.g., 'Yang Wood': 100) into element totals.

    Input format: {"Yang Wood": 80, "Yin Wood": 40, "Yang Fire": 60, ...}
    Output format: {"Wood": 120, "Fire": 60, ...}
    """
    # Map stem names to elements
    stem_to_element = {
        "Jia": "Wood", "Yi": "Wood",
        "Bing": "Fire", "Ding": "Fire",
        "Wu": "Earth", "Ji": "Earth",
        "Geng": "Metal", "Xin": "Metal",
        "Ren": "Water", "Gui": "Water",
    }
    polarity_stem_to_element = {
        "Yang Wood": "Wood", "Yin Wood": "Wood",
        "Yang Fire": "Fire", "Yin Fire": "Fire",
        "Yang Earth": "Earth", "Yin Earth": "Earth",
        "Yang Metal": "Metal", "Yin Metal": "Metal",
        "Yang Water": "Water", "Yin Water": "Water",
    }

    totals: Dict[str, float] = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}

    for key, score in element_scores.items():
        # Try polarity+element format first ("Yang Wood")
        element = polarity_stem_to_element.get(key)
        if element is None:
            # Try stem name format ("Jia")
            element = stem_to_element.get(key)
        if element:
            totals[element] += score

    return totals


def detect_element_states(element_scores: dict) -> List[dict]:
    """Scan post-interaction element totals and return active modified states.

    Args:
        element_scores: Dict of element scores (can be stem-level or element-level)

    Returns:
        List of active element state dicts with state_id, ratio, and full state info
    """
    totals = _aggregate_element_scores(element_scores)
    active_states = []

    for state_id, state in ELEMENT_STATES.items():
        base = state["base_element"]
        trigger = state["trigger_element"]

        base_total = totals.get(base, 0)
        trigger_total = totals.get(trigger, 0)

        if base_total <= 0:
            continue

        ratio = trigger_total / base_total

        if ratio >= state["threshold_ratio"]:
            active_states.append({
                "state_id": state_id,
                "base_element": base,
                "trigger_element": trigger,
                "ratio": round(ratio, 2),
                "threshold": state["threshold_ratio"],
                "name_en": state["name_en"],
                "name_zh": state["name_zh"],
                "name_id": state["name_id"],
                "blocked_action": state["blocked_action"],
                "production_factor": state["production_factor"],
                "description_en": state["description_en"],
                "description_zh": state["description_zh"],
                "description_id": state["description_id"],
            })

    return active_states


def detect_chain_reactions(active_states: List[dict], max_depth: int = 3) -> List[dict]:
    """Detect downstream chain reactions from active element states.

    E.g., wet_wood → Fire starved → Metal less controlled

    Args:
        active_states: List from detect_element_states()
        max_depth: Maximum chain depth (default 3)

    Returns:
        List of chain reaction dicts
    """
    chains = []
    active_state_ids = {s["state_id"] for s in active_states}

    for state in active_states:
        state_id = state["state_id"]
        chain_info = CHAIN_REACTION_MAP.get(state_id)
        if not chain_info:
            continue

        chain = {
            "trigger_state": state_id,
            "trigger_name_en": state["name_en"],
            "trigger_name_zh": state["name_zh"],
            "steps": [{
                "step": 1,
                "cause": f"{state['name_en']} blocks {state['blocked_action'].replace('_', ' ')}",
                "effect": chain_info["downstream"],
                "affected_element": chain_info["downstream_element"],
                "effect_type": chain_info["downstream_effect"],
                "factor": chain_info["downstream_factor"],
            }],
        }

        chains.append(chain)

    return chains


def get_physics_modifier_for_interaction(
    source_stem: str,
    target_stem: str,
    source_element: str,
    target_element: str,
    wuxing_relation: str,
    active_states: List[dict],
) -> dict:
    """Calculate the physics modifier for a single interaction.

    This is the main entry point called during interaction processing.
    It combines stem imagery modifiers with element state blocking.

    Args:
        source_stem: e.g., "Ren"
        target_stem: e.g., "Yi"
        source_element: e.g., "Water"
        target_element: e.g., "Wood"
        wuxing_relation: "generation" or "control"
        active_states: Current active element states

    Returns:
        Dict with source_modifier, target_modifier, imagery info, and state effects
    """
    result = {
        "has_physics_effect": False,
        "source_modifier": 0.0,
        "target_modifier": 0.0,
        "imagery": None,
        "outcome": None,
        "state_blocked": False,
        "state_production_factor": 1.0,
        "state_name": None,
    }

    # 1. Check stem imagery
    interaction = get_stem_interaction(source_stem, target_stem)
    if interaction:
        result["has_physics_effect"] = True
        result["source_modifier"] = interaction["source_modifier"]
        result["target_modifier"] = interaction["target_modifier"]
        result["imagery"] = interaction["imagery"]
        result["outcome"] = interaction["outcome"]
        result["en"] = interaction["en"]
        result["zh"] = interaction["zh"]

    # 2. Check element state blocking
    if wuxing_relation == "generation":
        action = f"produce_{target_element.lower()}"
    elif wuxing_relation == "control":
        action = f"control_{target_element.lower()}"
    else:
        action = None

    if action:
        for state in active_states:
            if state["blocked_action"] == action and state["base_element"] == source_element:
                result["has_physics_effect"] = True
                result["state_blocked"] = True
                result["state_production_factor"] = state["production_factor"]
                result["state_name"] = state["name_en"]
                result["state_name_zh"] = state["name_zh"]
                break

    return result


def apply_physics_to_classic_result(
    classic_source_loss: float,
    classic_target_change: float,
    physics_modifier: dict,
) -> Tuple[float, float]:
    """Apply physics modifiers on top of classic combat results.

    Args:
        classic_source_loss: Base source loss from unity.py
        classic_target_change: Base target change from unity.py (negative=loss, positive=gain)
        physics_modifier: Result from get_physics_modifier_for_interaction()

    Returns:
        (modified_source_loss, modified_target_change) tuple
    """
    if not physics_modifier["has_physics_effect"]:
        return classic_source_loss, classic_target_change

    source_loss = classic_source_loss
    target_change = classic_target_change

    # Apply stem imagery modifiers
    source_mod = physics_modifier["source_modifier"]
    target_mod = physics_modifier["target_modifier"]

    # source_modifier: positive = source loses LESS, negative = source loses MORE
    source_loss = source_loss * (1.0 - source_mod)

    # target_modifier: positive = target gains MORE (generation) or loses LESS (control)
    # negative = target gains LESS or loses MORE
    if target_change >= 0:
        # Generation: target is gaining
        target_change = target_change * (1.0 + target_mod)
    else:
        # Control: target is losing
        target_change = target_change * (1.0 - target_mod)

    # Apply element state blocking (further reduces effectiveness)
    if physics_modifier["state_blocked"]:
        factor = physics_modifier["state_production_factor"]
        # Reduce both source exhaustion and target effect
        source_loss = source_loss * factor
        if target_change >= 0:
            target_change = target_change * factor
        else:
            target_change = target_change * factor

    return round(source_loss, 2), round(target_change, 2)


def build_physics_analysis(
    element_scores: dict,
    interaction_log: list,
) -> dict:
    """Build the complete physics analysis response section.

    Called after all interactions are complete. Scans final element scores
    for active states and chain reactions, and collects stem imagery data
    from the interaction log.

    Args:
        element_scores: Final post-interaction element scores
        interaction_log: Complete interaction log with physics data

    Returns:
        Dict ready to be added to API response as "physics_analysis"
    """
    # Detect element states from final scores
    active_states = detect_element_states(element_scores)

    # Detect chain reactions
    chain_reactions = detect_chain_reactions(active_states)

    # Collect stem interactions from log
    stem_interactions = []
    for entry in interaction_log:
        physics_data = entry.get("physics")
        if physics_data and physics_data.get("has_physics_effect"):
            stem_interactions.append({
                "source": entry.get("source", ""),
                "target": entry.get("target", ""),
                "outcome": physics_data.get("outcome", ""),
                "imagery": physics_data.get("imagery", ""),
                "en": physics_data.get("en", ""),
                "zh": physics_data.get("zh", ""),
                "state_blocked": physics_data.get("state_blocked", False),
                "state_name": physics_data.get("state_name"),
            })

    return {
        "element_states": active_states,
        "chain_reactions": chain_reactions,
        "stem_interactions": stem_interactions,
        "total_physics_effects": len(stem_interactions),
        "total_states_active": len(active_states),
        "total_chain_reactions": len(chain_reactions),
    }
