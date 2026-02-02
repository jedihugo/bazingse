# * =========================
# * LOCALIZATION UTILITIES
# * =========================
# Dual-language text builders for narrative generation.
# Supports English (en) and Chinese (zh).

from typing import Dict, Any, Optional, List

# Supported locales
SUPPORTED_LOCALES = ["en", "zh"]

# =============================================================================
# ELEMENT NAME MAPPINGS
# =============================================================================

ELEMENT_NAMES = {
    "Wood": {"en": "Wood", "zh": "木"},
    "Fire": {"en": "Fire", "zh": "火"},
    "Earth": {"en": "Earth", "zh": "土"},
    "Metal": {"en": "Metal", "zh": "金"},
    "Water": {"en": "Water", "zh": "水"},
}

# =============================================================================
# STEM NAME MAPPINGS
# =============================================================================

STEM_NAMES = {
    "Jia": {"en": "Jia", "zh": "甲", "element": "Wood", "polarity": "Yang"},
    "Yi": {"en": "Yi", "zh": "乙", "element": "Wood", "polarity": "Yin"},
    "Bing": {"en": "Bing", "zh": "丙", "element": "Fire", "polarity": "Yang"},
    "Ding": {"en": "Ding", "zh": "丁", "element": "Fire", "polarity": "Yin"},
    "Wu": {"en": "Wu", "zh": "戊", "element": "Earth", "polarity": "Yang"},
    "Ji": {"en": "Ji", "zh": "己", "element": "Earth", "polarity": "Yin"},
    "Geng": {"en": "Geng", "zh": "庚", "element": "Metal", "polarity": "Yang"},
    "Xin": {"en": "Xin", "zh": "辛", "element": "Metal", "polarity": "Yin"},
    "Ren": {"en": "Ren", "zh": "壬", "element": "Water", "polarity": "Yang"},
    "Gui": {"en": "Gui", "zh": "癸", "element": "Water", "polarity": "Yin"},
}

# =============================================================================
# BRANCH NAME MAPPINGS
# =============================================================================

BRANCH_NAMES = {
    "Zi": {"en": "Zi", "zh": "子", "animal": "Rat", "animal_zh": "鼠", "element": "Water"},
    "Chou": {"en": "Chou", "zh": "丑", "animal": "Ox", "animal_zh": "牛", "element": "Earth"},
    "Yin": {"en": "Yin", "zh": "寅", "animal": "Tiger", "animal_zh": "虎", "element": "Wood"},
    "Mao": {"en": "Mao", "zh": "卯", "animal": "Rabbit", "animal_zh": "兔", "element": "Wood"},
    "Chen": {"en": "Chen", "zh": "辰", "animal": "Dragon", "animal_zh": "龙", "element": "Earth"},
    "Si": {"en": "Si", "zh": "巳", "animal": "Snake", "animal_zh": "蛇", "element": "Fire"},
    "Wu": {"en": "Wu", "zh": "午", "animal": "Horse", "animal_zh": "马", "element": "Fire"},
    "Wei": {"en": "Wei", "zh": "未", "animal": "Goat", "animal_zh": "羊", "element": "Earth"},
    "Shen": {"en": "Shen", "zh": "申", "animal": "Monkey", "animal_zh": "猴", "element": "Metal"},
    "You": {"en": "You", "zh": "酉", "animal": "Rooster", "animal_zh": "鸡", "element": "Metal"},
    "Xu": {"en": "Xu", "zh": "戌", "animal": "Dog", "animal_zh": "狗", "element": "Earth"},
    "Hai": {"en": "Hai", "zh": "亥", "animal": "Pig", "animal_zh": "猪", "element": "Water"},
}

# =============================================================================
# SEASONAL STATE MAPPINGS
# =============================================================================

SEASONAL_STATES = {
    "Prosperous": {"en": "Prosperous", "zh": "旺"},
    "Strengthening": {"en": "Strengthening", "zh": "相"},
    "Resting": {"en": "Resting", "zh": "休"},
    "Trapped": {"en": "Trapped", "zh": "囚"},
    "Dead": {"en": "Dead", "zh": "死"},
}

# =============================================================================
# PUNISHMENT TYPE MAPPINGS
# =============================================================================

PUNISHMENT_TYPES = {
    "shi": {"en": "Power Punishment", "zh": "势刑"},
    "wu_li": {"en": "Rudeness Punishment", "zh": "无礼刑"},
    "en": {"en": "Ungrateful Punishment", "zh": "恩刑"},
    "zi": {"en": "Self-Punishment", "zh": "自刑"},
}


def get_localized_template(
    template: Dict[str, Any],
    locale: str = "en"
) -> Dict[str, str]:
    """
    Get locale-specific template strings.

    Args:
        template: Template dict with "en" and "zh" keys
        locale: Target locale

    Returns:
        Dict of template strings for the locale
    """
    if locale not in SUPPORTED_LOCALES:
        locale = "en"

    return template.get(locale, template.get("en", {}))


def build_narrative_text(
    template_key: str,
    templates: Dict[str, Any],
    variables: Dict[str, Any],
    locale: str = "en"
) -> Dict[str, str]:
    """
    Build narrative text from template and variables.

    Args:
        template_key: Key to look up in templates dict
        templates: Templates dict from templates.py
        variables: Variables to substitute into template
        locale: Target locale

    Returns:
        Dict with keys: title, summary, detail, meaning (as available)
    """
    template = templates.get(template_key, {})
    locale_template = get_localized_template(template, locale)

    if not locale_template:
        return {"title": template_key, "summary": "", "detail": "", "meaning": ""}

    # Prepare localized variable names
    localized_vars = _localize_variables(variables, locale)

    result = {}

    for key in ["title", "summary", "detail", "meaning", "advice", "transformed", "partial"]:
        if key in locale_template:
            try:
                result[key] = locale_template[key].format(**localized_vars)
            except KeyError as e:
                # If a variable is missing, leave placeholder visible
                result[key] = locale_template[key]

    return result


def _localize_variables(variables: Dict[str, Any], locale: str) -> Dict[str, Any]:
    """
    Add locale-specific versions of variables.

    For example, if variables has "element": "Wood",
    this adds "element_zh": "木" for Chinese locale.
    """
    localized = dict(variables)

    # Localize element names
    if "element" in variables:
        element = variables["element"]
        localized["element_zh"] = ELEMENT_NAMES.get(element, {}).get("zh", element)

    # Localize stem names
    for key in ["stem1", "stem2", "producer", "receiver"]:
        if key in variables:
            stem = variables[key]
            stem_info = STEM_NAMES.get(stem, {})
            localized[f"{key}_zh"] = stem_info.get("zh", stem)

    # Localize branch names
    for key in ["branch1", "branch2", "branch3"]:
        if key in variables:
            branch = variables[key]
            branch_info = BRANCH_NAMES.get(branch, {})
            localized[f"{key}_zh"] = branch_info.get("zh", branch)

    # Localize branches list
    if "branches" in variables:
        branches = variables["branches"]
        if isinstance(branches, list):
            localized["branches_zh"] = ", ".join(
                BRANCH_NAMES.get(b, {}).get("zh", b) for b in branches
            )
        elif isinstance(branches, str):
            # Parse comma-separated string
            branch_list = [b.strip() for b in branches.split(",")]
            localized["branches_zh"] = ", ".join(
                BRANCH_NAMES.get(b, {}).get("zh", b) for b in branch_list
            )

    # Localize seasonal state
    if "state" in variables:
        state = variables["state"]
        localized["state_zh"] = SEASONAL_STATES.get(state, {}).get("zh", state)

    # Localize punishment type
    if "punishment_type" in variables:
        ptype = variables["punishment_type"]
        localized["punishment_type_zh"] = PUNISHMENT_TYPES.get(ptype, {}).get("zh", ptype)

    # Localize controller/producer elements
    for key in ["controller", "producer"]:
        if key in variables:
            element = variables[key]
            localized[f"{key}_zh"] = ELEMENT_NAMES.get(element, {}).get("zh", element)

    # Localize daymaster
    if "daymaster" in variables:
        dm = variables["daymaster"]
        # Daymaster is usually like "Yang Wood" or "Jia"
        if dm in STEM_NAMES:
            localized["daymaster_zh"] = STEM_NAMES[dm].get("zh", dm)
        else:
            # Try to parse "Yang Element" format
            parts = dm.split()
            if len(parts) == 2:
                polarity, element = parts
                localized["daymaster_zh"] = f"{'阳' if polarity == 'Yang' else '阴'}{ELEMENT_NAMES.get(element, {}).get('zh', element)}"
            else:
                localized["daymaster_zh"] = dm

    return localized


def format_pillar_reference(
    node_id: str,
    locale: str = "en"
) -> Dict[str, str]:
    """
    Format a node ID into a human-readable pillar reference.

    Args:
        node_id: Node ID like "hs_d" or "eb_y"
        locale: Target locale

    Returns:
        Dict with "text" and "abbrev" keys
    """
    # Parse node ID
    parts = node_id.split("_")
    if len(parts) < 2:
        return {"text": node_id, "abbrev": node_id}

    node_type = parts[0]  # "hs" or "eb"
    position = parts[1]   # "d", "y", "m", "h", "10yl", "yl", etc.

    type_names = {
        "hs": {"en": "Heavenly Stem", "zh": "天干"},
        "eb": {"en": "Earthly Branch", "zh": "地支"},
    }

    position_names = {
        "h": {"en": "Hour", "zh": "时", "abbrev_en": "Hr", "abbrev_zh": "时"},
        "d": {"en": "Day", "zh": "日", "abbrev_en": "Day", "abbrev_zh": "日"},
        "m": {"en": "Month", "zh": "月", "abbrev_en": "Mo", "abbrev_zh": "月"},
        "y": {"en": "Year", "zh": "年", "abbrev_en": "Yr", "abbrev_zh": "年"},
        "10yl": {"en": "10Y Luck", "zh": "大运", "abbrev_en": "10Y", "abbrev_zh": "运"},
        "yl": {"en": "Annual", "zh": "流年", "abbrev_en": "Ann", "abbrev_zh": "年"},
        "ml": {"en": "Monthly", "zh": "流月", "abbrev_en": "Mon", "abbrev_zh": "月"},
        "dl": {"en": "Daily", "zh": "流日", "abbrev_en": "Day", "abbrev_zh": "日"},
        "hl": {"en": "Hourly", "zh": "流时", "abbrev_en": "Hr", "abbrev_zh": "时"},
        "ty": {"en": "Talisman Year", "zh": "符年", "abbrev_en": "TY", "abbrev_zh": "符年"},
        "tm": {"en": "Talisman Month", "zh": "符月", "abbrev_en": "TM", "abbrev_zh": "符月"},
        "td": {"en": "Talisman Day", "zh": "符日", "abbrev_en": "TD", "abbrev_zh": "符日"},
        "th": {"en": "Talisman Hour", "zh": "符时", "abbrev_en": "TH", "abbrev_zh": "符时"},
    }

    type_info = type_names.get(node_type, {"en": node_type, "zh": node_type})
    pos_info = position_names.get(position, {"en": position, "zh": position, "abbrev_en": position, "abbrev_zh": position})

    if locale == "zh":
        text = f"{pos_info['zh']}{type_info['zh']}"
        abbrev = pos_info.get("abbrev_zh", position)
    else:
        text = f"{pos_info['en']} {type_info['en']}"
        abbrev = pos_info.get("abbrev_en", position)

    return {"text": text, "abbrev": abbrev, "node_type": node_type, "position": position}


def format_branches_display(
    branches: List[str],
    locale: str = "en"
) -> str:
    """
    Format a list of branches for display.

    Args:
        branches: List of branch names
        locale: Target locale

    Returns:
        Formatted string
    """
    if not branches:
        return ""

    if locale == "zh":
        branch_chars = [BRANCH_NAMES.get(b, {}).get("zh", b) for b in branches]
        return "".join(branch_chars)
    else:
        return ", ".join(branches)


def format_stems_display(
    stems: List[str],
    locale: str = "en"
) -> str:
    """
    Format a list of stems for display.

    Args:
        stems: List of stem names
        locale: Target locale

    Returns:
        Formatted string
    """
    if not stems:
        return ""

    if locale == "zh":
        stem_chars = [STEM_NAMES.get(s, {}).get("zh", s) for s in stems]
        return "".join(stem_chars)
    else:
        return ", ".join(stems)
