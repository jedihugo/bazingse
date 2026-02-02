# * =========================
# * PILLAR-BASED STORY GENERATOR
# * =========================
# Tells the BaZi story node-by-node, starting from Daymaster.
#
# Order: DM (Day HS) → Year HS → Year EB → Month HS → Month EB → Day EB → Hour HS → Hour EB
#
# Each node gets a complete analysis:
# - Element & Ten God relationship
# - Shen Sha present
# - Qi Phase (for EBs)
# - Storage status (for EBs)
# - Interactions with other nodes

from typing import Dict, List, Any, Optional
from .qi_phase import get_qi_phase_for_stem, get_storage_info
from .chain_engine import SHEN_SHA_MEANINGS, QI_PHASE_MEANINGS, DM_TO_WEALTH_STORAGE
from .modifiers import TEN_GODS_FOR_ELEMENT, TEN_GODS_EXCESS_MEANING

# Node analysis order (story flow)
NODE_ORDER = [
    "hs_d",  # Daymaster - the self
    "hs_y",  # Year HS - ancestors, early influence
    "eb_y",  # Year EB - ancestral foundation
    "hs_m",  # Month HS - parents, career stem
    "eb_m",  # Month EB - parents, career root
    "eb_d",  # Day EB - spouse palace (IMPORTANT)
    "hs_h",  # Hour HS - children, output
    "eb_h",  # Hour EB - children, future
]

# Node meanings for context
NODE_MEANINGS = {
    "hs_d": {
        "en": {"name": "Daymaster", "role": "Self", "represents": "Your core identity, personality, and life force"},
        "zh": {"name": "日主", "role": "自我", "represents": "核心身份、性格、生命力"},
    },
    "hs_y": {
        "en": {"name": "Year Stem", "role": "Ancestors", "represents": "Ancestral influence, early childhood, social image"},
        "zh": {"name": "年干", "role": "祖先", "represents": "祖先影响、童年早期、社会形象"},
    },
    "eb_y": {
        "en": {"name": "Year Branch", "role": "Root", "represents": "Ancestral foundation, family karma, ages 1-16"},
        "zh": {"name": "年支", "role": "根基", "represents": "祖先根基、家族业力、1-16岁"},
    },
    "hs_m": {
        "en": {"name": "Month Stem", "role": "Parents/Career", "represents": "Parents' influence, career approach, ages 17-32"},
        "zh": {"name": "月干", "role": "父母/事业", "represents": "父母影响、事业方式、17-32岁"},
    },
    "eb_m": {
        "en": {"name": "Month Branch", "role": "Career Root", "represents": "Career foundation, social circle, seasonal strength"},
        "zh": {"name": "月支", "role": "事业根基", "represents": "事业根基、社交圈、季节力量"},
    },
    "eb_d": {
        "en": {"name": "Day Branch", "role": "Spouse Palace", "represents": "Marriage, partnership, inner self, ages 33-48"},
        "zh": {"name": "日支", "role": "配偶宫", "represents": "婚姻、伴侣、内在自我、33-48岁"},
    },
    "hs_h": {
        "en": {"name": "Hour Stem", "role": "Children/Output", "represents": "Children, creative output, legacy"},
        "zh": {"name": "时干", "role": "子女/产出", "represents": "子女、创造产出、传承"},
    },
    "eb_h": {
        "en": {"name": "Hour Branch", "role": "Future", "represents": "Children's foundation, late life, ages 49+"},
        "zh": {"name": "时支", "role": "未来", "represents": "子女根基、晚年、49岁以后"},
    },
}

# Ten God descriptions
TEN_GOD_INFO = {
    "resource": {
        "en": {"name": "Resource/Seal", "meaning": "support, nurturing, protection, learning, mother figure"},
        "zh": {"name": "印星", "meaning": "支持、滋养、保护、学习、母亲形象"},
    },
    "companion": {
        "en": {"name": "Companion/Rob", "meaning": "siblings, friends, competition, self-reliance"},
        "zh": {"name": "比劫", "meaning": "兄弟姐妹、朋友、竞争、自立"},
    },
    "output": {
        "en": {"name": "Output/Food God", "meaning": "expression, creativity, ideas, children (for women)"},
        "zh": {"name": "食伤", "meaning": "表达、创造力、想法、子女(女性)"},
    },
    "wealth": {
        "en": {"name": "Wealth", "meaning": "money, assets, father figure, spouse (for men)"},
        "zh": {"name": "财星", "meaning": "金钱、资产、父亲形象、配偶(男性)"},
    },
    "officer": {
        "en": {"name": "Officer/Power", "meaning": "authority, discipline, career, spouse (for women)"},
        "zh": {"name": "官杀", "meaning": "权威、纪律、事业、配偶(女性)"},
    },
}

# WuXing relationships
WUXING_RELATIONSHIPS = {
    "Wood": {"resource": "Water", "companion": "Wood", "output": "Fire", "wealth": "Earth", "officer": "Metal"},
    "Fire": {"resource": "Wood", "companion": "Fire", "output": "Earth", "wealth": "Metal", "officer": "Water"},
    "Earth": {"resource": "Fire", "companion": "Earth", "output": "Metal", "wealth": "Water", "officer": "Wood"},
    "Metal": {"resource": "Earth", "companion": "Metal", "output": "Water", "wealth": "Wood", "officer": "Fire"},
    "Water": {"resource": "Metal", "companion": "Water", "output": "Wood", "wealth": "Fire", "officer": "Earth"},
}

# Stem to element mapping
STEM_ELEMENTS = {
    "Jia": "Wood", "Yi": "Wood",
    "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth",
    "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water",
}

# Branch to element mapping
BRANCH_ELEMENTS = {
    "Zi": "Water", "Chou": "Earth", "Yin": "Wood", "Mao": "Wood",
    "Chen": "Earth", "Si": "Fire", "Wu": "Fire", "Wei": "Earth",
    "Shen": "Metal", "You": "Metal", "Xu": "Earth", "Hai": "Water",
}


def get_ten_god_relationship(dm_element: str, target_element: str) -> str:
    """Get the Ten God relationship between daymaster and target element."""
    if dm_element not in WUXING_RELATIONSHIPS:
        return "unknown"

    relationships = WUXING_RELATIONSHIPS[dm_element]
    for role, element in relationships.items():
        if element == target_element:
            return role
    return "unknown"


def generate_pillar_stories(
    nodes_data: Dict[str, Any],
    daymaster_analysis: Dict[str, Any],
    element_context: Dict[str, Any],
    special_stars: List[Dict[str, Any]],
    interactions: Dict[str, Any],
    locale: str = "en"
) -> Dict[str, Any]:
    """
    Generate node-by-node stories for the natal chart.

    Returns:
        Dict with:
        - pillar_stories: List of node analyses in story order
        - minimap: Data for rendering the chart minimap with highlights
    """
    stories = []

    # Get daymaster info
    daymaster = daymaster_analysis.get("daymaster", "")
    dm_parts = daymaster.split(" ") if daymaster else []
    dm_polarity = dm_parts[0] if len(dm_parts) > 1 else ""
    dm_element = dm_parts[1] if len(dm_parts) > 1 else ""

    # Get daymaster stem
    dm_stem = nodes_data.get("hs_d", {}).get("id", "")

    # Build Shen Sha by node mapping
    shen_sha_by_node = _build_shen_sha_by_node(special_stars)

    # Get element percentages
    element_percentages = element_context.get("element_percentages", {})
    favorable_elements = element_context.get("favorable_elements", [])

    # Build interaction map (which nodes interact with which)
    interaction_map = _build_interaction_map(interactions)

    # Generate story for each node
    for node_id in NODE_ORDER:
        node_data = nodes_data.get(node_id, {})
        if not node_data:
            continue

        story = _analyze_node(
            node_id=node_id,
            node_data=node_data,
            dm_element=dm_element,
            dm_stem=dm_stem,
            element_percentages=element_percentages,
            favorable_elements=favorable_elements,
            shen_sha_by_node=shen_sha_by_node,
            interaction_map=interaction_map,
            interactions=interactions,
            locale=locale
        )

        if story:
            stories.append(story)

    # Build minimap data
    minimap = _build_minimap(nodes_data, dm_element, locale)

    return {
        "pillar_stories": stories,
        "minimap": minimap,
        "story_order": NODE_ORDER,
    }


def _analyze_node(
    node_id: str,
    node_data: Dict[str, Any],
    dm_element: str,
    dm_stem: str,
    element_percentages: Dict[str, float],
    favorable_elements: List[str],
    shen_sha_by_node: Dict[str, List[str]],
    interaction_map: Dict[str, List[str]],
    interactions: Dict[str, Any],
    locale: str
) -> Optional[Dict[str, Any]]:
    """Analyze a single node and generate its story."""

    node_value = node_data.get("id", "")
    if not node_value:
        return None

    # Determine if HS or EB
    is_stem = node_id.startswith("hs_")

    # Get element
    if is_stem:
        element = STEM_ELEMENTS.get(node_value, "")
    else:
        element = BRANCH_ELEMENTS.get(node_value, "")

    if not element:
        return None

    # Get node meaning
    node_meaning = NODE_MEANINGS.get(node_id, {}).get(locale, {})

    # Get Ten God relationship
    ten_god_role = get_ten_god_relationship(dm_element, element)
    ten_god_info = TEN_GOD_INFO.get(ten_god_role, {}).get(locale, {})

    # Check element favorability
    element_pct = element_percentages.get(element, 0)
    is_favorable = element in favorable_elements
    is_excessive = element_pct > 28  # Excess threshold

    # Build base story
    story = {
        "node_id": node_id,
        "node_value": node_value,
        "element": element,
        "element_percentage": element_pct,
        "is_favorable": is_favorable,
        "is_excessive": is_excessive,
        "node_name": node_meaning.get("name", node_id),
        "node_role": node_meaning.get("role", ""),
        "node_represents": node_meaning.get("represents", ""),
        "ten_god_role": ten_god_role,
        "ten_god_name": ten_god_info.get("name", ""),
        "ten_god_meaning": ten_god_info.get("meaning", ""),
        "is_daymaster": node_id == "hs_d",
    }

    # Add excess meaning if applicable
    if is_excessive and ten_god_role in TEN_GODS_EXCESS_MEANING:
        excess_info = TEN_GODS_EXCESS_MEANING[ten_god_role]
        story["excess_meaning"] = excess_info.get(locale, excess_info.get("en", ""))
        story["excess_traits"] = excess_info.get("traits", [])

    # For Earthly Branches, add Qi Phase and Storage info
    if not is_stem:
        # Qi Phase
        if dm_stem:
            qi_phase = get_qi_phase_for_stem(dm_stem, node_value)
            story["qi_phase"] = {
                "phase": qi_phase.get("phase", ""),
                "chinese": qi_phase.get("chinese", ""),
                "english": qi_phase.get("english", ""),
                "meaning": qi_phase.get("meaning_en" if locale == "en" else "meaning_zh", ""),
                "strength": qi_phase.get("strength", ""),
                "is_storage_phase": qi_phase.get("is_storage", False),
            }

        # Storage info
        storage = get_storage_info(node_value)
        if storage:
            story["storage"] = {
                "stores": storage.get("stores", ""),
                "opener": storage.get("opener", ""),
                "is_wealth_storage": node_value == DM_TO_WEALTH_STORAGE.get(dm_element, ""),
            }

    # Add Shen Sha
    shen_sha_list = shen_sha_by_node.get(node_id, [])
    if shen_sha_list:
        story["shen_sha"] = []
        for ss_id in shen_sha_list:
            ss_info = SHEN_SHA_MEANINGS.get(ss_id, {})
            story["shen_sha"].append({
                "id": ss_id,
                "chinese": ss_info.get("chinese", ss_id),
                "english": ss_info.get("english", ss_id),
                "base_meaning": ss_info.get("base_meaning", {}).get(locale, ""),
            })

    # Add interactions this node is involved in
    node_interactions = interaction_map.get(node_id, [])
    if node_interactions:
        story["interactions"] = []
        for int_id in node_interactions[:5]:  # Limit to top 5
            int_data = interactions.get(int_id, {})
            if int_data:
                story["interactions"].append({
                    "id": int_id,
                    "type": int_data.get("type", ""),
                    "with_nodes": [n for n in int_data.get("nodes", []) if n != node_id],
                })

    # Generate narrative text
    story["narrative"] = _generate_node_narrative(story, locale)

    return story


def _generate_node_narrative(story: Dict[str, Any], locale: str) -> str:
    """Generate human-readable narrative for a node."""
    parts = []

    node_name = story.get("node_name", "")
    element = story.get("element", "")
    ten_god_name = story.get("ten_god_name", "")
    element_pct = story.get("element_percentage", 0)
    is_favorable = story.get("is_favorable", False)
    is_excessive = story.get("is_excessive", False)

    # Daymaster intro
    if story.get("is_daymaster"):
        if locale == "zh":
            parts.append(f"你是{element}命，{story.get('node_represents', '')}")
        else:
            parts.append(f"You are {element} Daymaster - {story.get('node_represents', '')}")
    else:
        # Regular node intro
        if locale == "zh":
            parts.append(f"{node_name}是{element}（{ten_god_name}）")
        else:
            parts.append(f"{node_name} is {element} ({ten_god_name})")

    # Element status
    if is_excessive:
        if locale == "zh":
            parts.append(f"{element}过旺（{element_pct:.1f}%），不利")
        else:
            parts.append(f"{element} is excessive ({element_pct:.1f}%) - unfavorable")

        # Add excess traits
        if story.get("excess_meaning"):
            parts.append(story["excess_meaning"])
    elif not is_favorable:
        if locale == "zh":
            parts.append(f"{element}（{element_pct:.1f}%）对你不利")
        else:
            parts.append(f"{element} ({element_pct:.1f}%) is unfavorable for you")
    else:
        if locale == "zh":
            parts.append(f"{element}（{element_pct:.1f}%）对你有利")
        else:
            parts.append(f"{element} ({element_pct:.1f}%) is favorable for you")

    # Qi Phase for branches
    qi_phase = story.get("qi_phase")
    if qi_phase:
        phase_name = qi_phase.get("chinese" if locale == "zh" else "english", "")
        if phase_name:
            if locale == "zh":
                parts.append(f"气相：{phase_name} - {qi_phase.get('meaning', '')}")
            else:
                parts.append(f"Qi Phase: {phase_name} - {qi_phase.get('meaning', '')}")

    # Storage
    storage = story.get("storage")
    if storage:
        stores = storage.get("stores", "")
        opener = storage.get("opener", "")
        is_wealth = storage.get("is_wealth_storage", False)

        if locale == "zh":
            storage_text = f"此支为{stores}库"
            if is_wealth:
                storage_text += "（财库！）"
            storage_text += f"，{opener}冲开"
            parts.append(storage_text)
        else:
            storage_text = f"This branch stores {stores}"
            if is_wealth:
                storage_text += " (Wealth Storage!)"
            storage_text += f", opened by {opener}"
            parts.append(storage_text)

    # Shen Sha
    shen_sha = story.get("shen_sha", [])
    if shen_sha:
        ss_names = [ss.get("chinese" if locale == "zh" else "english", "") for ss in shen_sha]
        if locale == "zh":
            parts.append(f"神煞：{', '.join(ss_names)}")
        else:
            parts.append(f"Special Stars: {', '.join(ss_names)}")

    # Key interactions
    interactions = story.get("interactions", [])
    if interactions:
        int_types = [i.get("type", "") for i in interactions[:3]]
        if locale == "zh":
            parts.append(f"参与：{', '.join(int_types)}")
        else:
            parts.append(f"Involved in: {', '.join(int_types)}")

    return " | ".join(parts)


def _build_shen_sha_by_node(special_stars: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Build mapping of node_id -> list of Shen Sha IDs."""
    result = {}

    for star in special_stars:
        pattern_id = star.get("pattern_id", "")

        # Normalize to base ID
        base_id = ""
        if "GU_CHEN" in pattern_id.upper():
            base_id = "GU_CHEN"
        elif "GUA_SU" in pattern_id.upper():
            base_id = "GUA_SU"
        elif "HUA_GAI" in pattern_id.upper():
            base_id = "HUA_GAI"
        elif "TAO_HUA" in pattern_id.upper():
            base_id = "TAO_HUA"
        elif "YANG_REN" in pattern_id.upper():
            base_id = "YANG_REN"
        elif "GUI_REN" in pattern_id.upper():
            base_id = "GUI_REN"
        elif "KONG_WANG" in pattern_id.upper():
            base_id = "KONG_WANG"
        elif "YI_MA" in pattern_id.upper():
            base_id = "YI_MA"
        elif "LU_SHEN" in pattern_id.upper():
            base_id = "LU_SHEN"

        if not base_id:
            continue

        triggers = star.get("triggers", [])
        for trigger in triggers:
            node_id = trigger.get("node_id", "")
            if node_id:
                if node_id not in result:
                    result[node_id] = []
                if base_id not in result[node_id]:
                    result[node_id].append(base_id)

    return result


def _build_interaction_map(interactions: Dict[str, Any]) -> Dict[str, List[str]]:
    """Build mapping of node_id -> list of interaction IDs it's involved in."""
    result = {}

    for int_id, int_data in interactions.items():
        if not isinstance(int_data, dict):
            continue

        nodes = int_data.get("nodes", [])
        for node_id in nodes:
            if node_id not in result:
                result[node_id] = []
            result[node_id].append(int_id)

    return result


def _build_minimap(nodes_data: Dict[str, Any], dm_element: str, locale: str) -> Dict[str, Any]:
    """Build minimap data for visual display."""
    pillars = []

    pillar_order = [
        ("hour", "hs_h", "eb_h"),
        ("day", "hs_d", "eb_d"),
        ("month", "hs_m", "eb_m"),
        ("year", "hs_y", "eb_y"),
    ]

    for pillar_name, hs_id, eb_id in pillar_order:
        hs_data = nodes_data.get(hs_id, {})
        eb_data = nodes_data.get(eb_id, {})

        hs_value = hs_data.get("id", "")
        eb_value = eb_data.get("id", "")

        hs_element = STEM_ELEMENTS.get(hs_value, "")
        eb_element = BRANCH_ELEMENTS.get(eb_value, "")

        pillars.append({
            "pillar": pillar_name,
            "hs": {
                "node_id": hs_id,
                "value": hs_value,
                "element": hs_element,
                "ten_god": get_ten_god_relationship(dm_element, hs_element) if hs_element else "",
            },
            "eb": {
                "node_id": eb_id,
                "value": eb_value,
                "element": eb_element,
                "ten_god": get_ten_god_relationship(dm_element, eb_element) if eb_element else "",
            },
        })

    return {
        "pillars": pillars,
        "dm_element": dm_element,
    }
