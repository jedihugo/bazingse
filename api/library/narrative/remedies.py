# * =========================
# * REMEDY RECOMMENDATIONS
# * =========================
# Generates remedy suggestions based on chart analysis.
# Remedies are suggestions for balancing element energies through
# colors, activities, directions, seasons, etc.

from typing import Dict, Any, List

# =============================================================================
# ELEMENT REMEDY MAPPINGS
# =============================================================================

ELEMENT_REMEDIES = {
    "Wood": {
        "colors": {
            "primary": ["green", "teal"],
            "secondary": ["black", "blue"],  # Water produces Wood
            "avoid": ["white", "silver"],    # Metal controls Wood
        },
        "colors_zh": {
            "primary": ["绿色", "青色"],
            "secondary": ["黑色", "蓝色"],
            "avoid": ["白色", "银色"],
        },
        "directions": {
            "favorable": ["East", "Southeast"],
            "unfavorable": ["West", "Northwest"],
        },
        "directions_zh": {
            "favorable": ["东", "东南"],
            "unfavorable": ["西", "西北"],
        },
        "activities": {
            "en": [
                "Spending time in nature, forests, parks",
                "Gardening and caring for plants",
                "Creative pursuits and new beginnings",
                "Morning activities (Wood time: 5-9 AM)",
                "Stretching and flexibility exercises",
            ],
            "zh": [
                "在大自然、森林、公园中度过时光",
                "园艺和照料植物",
                "创意追求和新开始",
                "早晨活动（木时：5-9点）",
                "伸展和柔韧性练习",
            ],
        },
        "foods": {
            "en": ["leafy greens", "sprouts", "sour foods", "herbs"],
            "zh": ["绿叶蔬菜", "豆芽", "酸味食物", "草药"],
        },
        "materials": {
            "en": ["wood", "bamboo", "paper", "cotton"],
            "zh": ["木头", "竹子", "纸", "棉花"],
        },
        "numbers": [3, 8],
        "seasons": {
            "favorable": "Spring",
            "favorable_zh": "春季",
        },
    },

    "Fire": {
        "colors": {
            "primary": ["red", "orange", "pink"],
            "secondary": ["green"],  # Wood produces Fire
            "avoid": ["black", "blue"],  # Water controls Fire
        },
        "colors_zh": {
            "primary": ["红色", "橙色", "粉色"],
            "secondary": ["绿色"],
            "avoid": ["黑色", "蓝色"],
        },
        "directions": {
            "favorable": ["South"],
            "unfavorable": ["North"],
        },
        "directions_zh": {
            "favorable": ["南"],
            "unfavorable": ["北"],
        },
        "activities": {
            "en": [
                "Social gatherings and celebrations",
                "Public speaking and performances",
                "Midday activities (Fire time: 9 AM - 1 PM)",
                "Cardio and high-energy exercise",
                "Networking and building connections",
            ],
            "zh": [
                "社交聚会和庆祝活动",
                "公开演讲和表演",
                "中午活动（火时：9-13点）",
                "有氧和高能量运动",
                "社交网络和建立联系",
            ],
        },
        "foods": {
            "en": ["red foods", "bitter foods", "peppers", "tomatoes"],
            "zh": ["红色食物", "苦味食物", "辣椒", "番茄"],
        },
        "materials": {
            "en": ["candles", "lights", "electronics", "leather"],
            "zh": ["蜡烛", "灯光", "电子产品", "皮革"],
        },
        "numbers": [2, 7],
        "seasons": {
            "favorable": "Summer",
            "favorable_zh": "夏季",
        },
    },

    "Earth": {
        "colors": {
            "primary": ["yellow", "brown", "beige", "terracotta"],
            "secondary": ["red", "orange"],  # Fire produces Earth
            "avoid": ["green"],  # Wood controls Earth
        },
        "colors_zh": {
            "primary": ["黄色", "棕色", "米色", "赭石色"],
            "secondary": ["红色", "橙色"],
            "avoid": ["绿色"],
        },
        "directions": {
            "favorable": ["Center", "Northeast", "Southwest"],
            "unfavorable": ["East", "Southeast"],
        },
        "directions_zh": {
            "favorable": ["中", "东北", "西南"],
            "unfavorable": ["东", "东南"],
        },
        "activities": {
            "en": [
                "Grounding practices and meditation",
                "Cooking and nurturing others",
                "Stability-focused activities",
                "Late afternoon activities (Earth times)",
                "Organizing and creating structure",
            ],
            "zh": [
                "接地练习和冥想",
                "烹饪和照顾他人",
                "注重稳定的活动",
                "下午晚些时候的活动（土时）",
                "整理和创建结构",
            ],
        },
        "foods": {
            "en": ["root vegetables", "grains", "sweet foods", "squash"],
            "zh": ["根茎蔬菜", "谷物", "甜味食物", "南瓜"],
        },
        "materials": {
            "en": ["ceramic", "clay", "stone", "brick"],
            "zh": ["陶瓷", "粘土", "石头", "砖块"],
        },
        "numbers": [5, 10],
        "seasons": {
            "favorable": "Late Summer / Season transitions",
            "favorable_zh": "长夏 / 季节转换期",
        },
    },

    "Metal": {
        "colors": {
            "primary": ["white", "silver", "gold", "metallic"],
            "secondary": ["yellow", "brown"],  # Earth produces Metal
            "avoid": ["red", "orange"],  # Fire controls Metal
        },
        "colors_zh": {
            "primary": ["白色", "银色", "金色", "金属色"],
            "secondary": ["黄色", "棕色"],
            "avoid": ["红色", "橙色"],
        },
        "directions": {
            "favorable": ["West", "Northwest"],
            "unfavorable": ["South"],
        },
        "directions_zh": {
            "favorable": ["西", "西北"],
            "unfavorable": ["南"],
        },
        "activities": {
            "en": [
                "Organizing and decluttering",
                "Setting boundaries and structure",
                "Evening activities (Metal time: 3-7 PM)",
                "Breathing exercises and respiratory health",
                "Precision work and detail-oriented tasks",
            ],
            "zh": [
                "整理和清理",
                "设定边界和结构",
                "傍晚活动（金时：15-19点）",
                "呼吸练习和呼吸系统健康",
                "精密工作和注重细节的任务",
            ],
        },
        "foods": {
            "en": ["white foods", "pungent foods", "onions", "garlic"],
            "zh": ["白色食物", "辛味食物", "洋葱", "大蒜"],
        },
        "materials": {
            "en": ["metal", "gold", "silver", "copper"],
            "zh": ["金属", "黄金", "白银", "铜"],
        },
        "numbers": [4, 9],
        "seasons": {
            "favorable": "Autumn",
            "favorable_zh": "秋季",
        },
    },

    "Water": {
        "colors": {
            "primary": ["black", "blue", "navy"],
            "secondary": ["white", "silver"],  # Metal produces Water
            "avoid": ["yellow", "brown"],  # Earth controls Water
        },
        "colors_zh": {
            "primary": ["黑色", "蓝色", "藏青色"],
            "secondary": ["白色", "银色"],
            "avoid": ["黄色", "棕色"],
        },
        "directions": {
            "favorable": ["North"],
            "unfavorable": ["Center", "Northeast", "Southwest"],
        },
        "directions_zh": {
            "favorable": ["北"],
            "unfavorable": ["中", "东北", "西南"],
        },
        "activities": {
            "en": [
                "Swimming and water-based activities",
                "Rest and introspection",
                "Night activities (Water time: 9 PM - 1 AM)",
                "Learning and study",
                "Travel and adaptability practices",
            ],
            "zh": [
                "游泳和水上活动",
                "休息和内省",
                "夜间活动（水时：21-1点）",
                "学习和研究",
                "旅行和适应性练习",
            ],
        },
        "foods": {
            "en": ["seafood", "salty foods", "dark foods", "seaweed"],
            "zh": ["海鲜", "咸味食物", "深色食物", "海藻"],
        },
        "materials": {
            "en": ["water features", "glass", "mirrors", "flowing fabrics"],
            "zh": ["水景", "玻璃", "镜子", "流动的织物"],
        },
        "numbers": [1, 6],
        "seasons": {
            "favorable": "Winter",
            "favorable_zh": "冬季",
        },
    },
}

# =============================================================================
# REMEDY TEMPLATES
# =============================================================================

REMEDY_TEMPLATES = {
    "strengthen": {
        "en": {
            "title": "To strengthen {element}:",
            "intro": "Your chart would benefit from more {element} energy. Consider:",
        },
        "zh": {
            "title": "增强{element_zh}：",
            "intro": "您的命盘需要更多{element_zh}能量。考虑：",
        },
    },
    "reduce": {
        "en": {
            "title": "To balance excess {element}:",
            "intro": "{element} is overactive in your chart. To balance:",
        },
        "zh": {
            "title": "平衡过旺的{element_zh}：",
            "intro": "{element_zh}在您的命盘中过于活跃。为平衡：",
        },
    },
    "maintain": {
        "en": {
            "title": "To maintain {element} balance:",
            "intro": "{element} is well-balanced. To maintain this harmony:",
        },
        "zh": {
            "title": "保持{element_zh}平衡：",
            "intro": "{element_zh}保持良好平衡。为维持这种和谐：",
        },
    },
}


def generate_remedies(
    element_context: Dict[str, Any],
    daymaster_element: str,
    locale: str = "en"
) -> List[Dict[str, Any]]:
    """
    Generate remedy recommendations based on element balance analysis.

    Args:
        element_context: Element balance context from get_element_balance_context()
        daymaster_element: The daymaster's element
        locale: Language locale ("en" or "zh")

    Returns:
        List of remedy recommendation dicts
    """
    remedies = []

    favorable_elements = element_context.get("favorable_elements", [])
    unfavorable_elements = element_context.get("unfavorable_elements", [])
    deficient_elements = element_context.get("deficient_elements", [])
    excess_elements = element_context.get("excess_elements", [])

    # Generate strengthening remedies for deficient/favorable elements
    for deficient in deficient_elements:
        element = deficient["element"]
        if element in ELEMENT_REMEDIES:
            remedy = _build_remedy(
                element=element,
                remedy_type="strengthen",
                severity=deficient["severity"],
                locale=locale
            )
            remedies.append(remedy)

    # Generate balancing remedies for excess elements
    for excess in excess_elements:
        element = excess["element"]
        controller = excess.get("controller", "")
        if controller in ELEMENT_REMEDIES:
            remedy = _build_remedy(
                element=controller,
                remedy_type="reduce",
                target_element=element,
                severity=excess["severity"],
                locale=locale
            )
            remedies.append(remedy)

    # If no specific imbalances, suggest maintaining balance for daymaster
    if not remedies and daymaster_element in ELEMENT_REMEDIES:
        remedy = _build_remedy(
            element=daymaster_element,
            remedy_type="maintain",
            locale=locale
        )
        remedies.append(remedy)

    return remedies


def _build_remedy(
    element: str,
    remedy_type: str,
    target_element: str = None,
    severity: str = "moderate",
    locale: str = "en"
) -> Dict[str, Any]:
    """
    Build a single remedy recommendation.

    Args:
        element: The element to strengthen/use
        remedy_type: "strengthen", "reduce", or "maintain"
        target_element: For "reduce" type, the element being reduced
        severity: "moderate" or "severe"
        locale: Language locale

    Returns:
        Remedy dict with recommendations
    """
    element_data = ELEMENT_REMEDIES.get(element, {})
    template = REMEDY_TEMPLATES.get(remedy_type, REMEDY_TEMPLATES["strengthen"])

    element_zh = _element_to_chinese(element)
    target_zh = _element_to_chinese(target_element) if target_element else ""

    # Build title and intro
    if locale == "zh":
        title = template["zh"]["title"].format(element_zh=element_zh)
        if target_element:
            intro = template["zh"]["intro"].format(element_zh=target_zh)
        else:
            intro = template["zh"]["intro"].format(element_zh=element_zh)
    else:
        title = template["en"]["title"].format(element=element)
        if target_element:
            intro = template["en"]["intro"].format(element=target_element)
        else:
            intro = template["en"]["intro"].format(element=element)

    # Get locale-specific data
    colors_key = "colors_zh" if locale == "zh" else "colors"
    directions_key = "directions_zh" if locale == "zh" else "directions"
    activities_key = locale

    colors = element_data.get(colors_key, element_data.get("colors", {}))
    directions = element_data.get(directions_key, element_data.get("directions", {}))
    activities = element_data.get("activities", {}).get(locale, [])
    foods = element_data.get("foods", {}).get(locale, [])
    materials = element_data.get("materials", {}).get(locale, [])
    numbers = element_data.get("numbers", [])
    seasons = element_data.get("seasons", {})

    remedy = {
        "element": element,
        "element_zh": element_zh,
        "type": remedy_type,
        "severity": severity,
        "title": title,
        "intro": intro,
        "recommendations": {
            "colors": {
                "use": colors.get("primary", []),
                "support": colors.get("secondary", []),
                "avoid": colors.get("avoid", []),
            },
            "directions": directions,
            "activities": activities[:3] if len(activities) > 3 else activities,  # Limit to 3
            "foods": foods,
            "materials": materials,
            "lucky_numbers": numbers,
            "favorable_season": seasons.get("favorable_zh" if locale == "zh" else "favorable", ""),
        },
    }

    # Add target element info for "reduce" type
    if target_element:
        remedy["target_element"] = target_element
        remedy["target_element_zh"] = target_zh

    return remedy


def get_quick_remedies(
    favorable_elements: List[str],
    locale: str = "en"
) -> Dict[str, Any]:
    """
    Get quick remedy suggestions for favorable elements.
    Returns a simplified dict suitable for compact display.

    Args:
        favorable_elements: List of favorable element names
        locale: Language locale

    Returns:
        Dict with quick remedy info
    """
    if not favorable_elements:
        return {}

    primary_element = favorable_elements[0]
    element_data = ELEMENT_REMEDIES.get(primary_element, {})

    colors_key = "colors_zh" if locale == "zh" else "colors"
    colors = element_data.get(colors_key, element_data.get("colors", {}))

    return {
        "favorable_element": primary_element,
        "favorable_element_zh": _element_to_chinese(primary_element),
        "lucky_colors": colors.get("primary", [])[:2],
        "lucky_numbers": element_data.get("numbers", []),
        "favorable_direction": element_data.get(
            "directions_zh" if locale == "zh" else "directions", {}
        ).get("favorable", [""])[0],
    }


def _element_to_chinese(element: str) -> str:
    """Convert element name to Chinese."""
    mapping = {
        "Wood": "木",
        "Fire": "火",
        "Earth": "土",
        "Metal": "金",
        "Water": "水",
    }
    return mapping.get(element, element) if element else ""
