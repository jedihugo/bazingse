# * =========================
# * LIFE ASPECTS - BASE MODULE
# * =========================
# Shared utilities and constants for all life aspect analyses.
# This module provides the foundation for health, wealth, and learning analysis.

from typing import Dict, List, Optional, Tuple

# Import from parent library
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import STEMS, BRANCHES

# * -------------------------
# * PILLAR POSITION MAPPINGS (宮位)
# * -------------------------
# Each pillar position represents relationships and life periods.
# Reference: Traditional BaZi 六親宮位 theory

NODE_RELATIONSHIPS = {
    # === NATAL PILLARS (命局) ===
    # Year Pillar (年柱) - Ancestors, early life
    "hs_y": {
        "pillar": "year",
        "pillar_chinese": "年柱",
        "type": "stem",
        "represents": "grandfather/ancestors",
        "represents_chinese": "祖父/祖上",
        "life_domain": "ancestry",
    },
    "eb_y": {
        "pillar": "year",
        "pillar_chinese": "年柱",
        "type": "branch",
        "represents": "grandmother/origins",
        "represents_chinese": "祖母/出身",
        "life_domain": "ancestry",
    },
    # Month Pillar (月柱) - Parents, youth
    "hs_m": {
        "pillar": "month",
        "pillar_chinese": "月柱",
        "type": "stem",
        "represents": "father",
        "represents_chinese": "父親",
        "life_domain": "parents",
    },
    "eb_m": {
        "pillar": "month",
        "pillar_chinese": "月柱",
        "type": "branch",
        "represents": "mother",
        "represents_chinese": "母親",
        "life_domain": "parents",
    },
    # Day Pillar (日柱) - Self and spouse
    "hs_d": {
        "pillar": "day",
        "pillar_chinese": "日柱",
        "type": "stem",
        "represents": "self (day master)",
        "represents_chinese": "自己/日主",
        "life_domain": "self",
    },
    "eb_d": {
        "pillar": "day",
        "pillar_chinese": "日柱",
        "type": "branch",
        "represents": "spouse",
        "represents_chinese": "配偶",
        "life_domain": "spouse",
    },
    # Hour Pillar (時柱) - Children, late life
    "hs_h": {
        "pillar": "hour",
        "pillar_chinese": "時柱",
        "type": "stem",
        "represents": "children",
        "represents_chinese": "子女",
        "life_domain": "children",
    },
    "eb_h": {
        "pillar": "hour",
        "pillar_chinese": "時柱",
        "type": "branch",
        "represents": "descendants/subordinates",
        "represents_chinese": "後代/下屬",
        "life_domain": "children",
    },

    # === LUCK PILLARS (運限) - Temporal overlays ===
    # 10-Year Luck (大運)
    "hs_10yl": {
        "pillar": "10yr_luck",
        "pillar_chinese": "大運",
        "type": "stem",
        "represents": "decade theme",
        "represents_chinese": "十年運勢主題",
        "life_domain": "luck",
    },
    "eb_10yl": {
        "pillar": "10yr_luck",
        "pillar_chinese": "大運",
        "type": "branch",
        "represents": "decade environment",
        "represents_chinese": "十年運勢環境",
        "life_domain": "luck",
    },
    # Annual Luck (流年)
    "hs_yl": {
        "pillar": "annual",
        "pillar_chinese": "流年",
        "type": "stem",
        "represents": "year theme",
        "represents_chinese": "年度主題",
        "life_domain": "luck",
    },
    "eb_yl": {
        "pillar": "annual",
        "pillar_chinese": "流年",
        "type": "branch",
        "represents": "year environment",
        "represents_chinese": "年度環境",
        "life_domain": "luck",
    },
    # Monthly Luck (流月)
    "hs_ml": {
        "pillar": "monthly",
        "pillar_chinese": "流月",
        "type": "stem",
        "represents": "month theme",
        "represents_chinese": "月度主題",
        "life_domain": "luck",
    },
    "eb_ml": {
        "pillar": "monthly",
        "pillar_chinese": "流月",
        "type": "branch",
        "represents": "month environment",
        "represents_chinese": "月度環境",
        "life_domain": "luck",
    },
    # Daily Luck (流日)
    "hs_dl": {
        "pillar": "daily",
        "pillar_chinese": "流日",
        "type": "stem",
        "represents": "day theme",
        "represents_chinese": "日主題",
        "life_domain": "luck",
    },
    "eb_dl": {
        "pillar": "daily",
        "pillar_chinese": "流日",
        "type": "branch",
        "represents": "day environment",
        "represents_chinese": "日環境",
        "life_domain": "luck",
    },
    # Hourly Luck (流時)
    "hs_hl": {
        "pillar": "hourly",
        "pillar_chinese": "流時",
        "type": "stem",
        "represents": "hour theme",
        "represents_chinese": "時主題",
        "life_domain": "luck",
    },
    "eb_hl": {
        "pillar": "hourly",
        "pillar_chinese": "流時",
        "type": "branch",
        "represents": "hour environment",
        "represents_chinese": "時環境",
        "life_domain": "luck",
    },
}

# * -------------------------
# * LIFE PERIOD MAPPINGS (限運)
# * -------------------------
# Traditional BaZi assigns life periods to each pillar

PILLAR_LIFE_PERIODS = {
    "year": {
        "start_age": 0,
        "end_age": 16,
        "chinese": "早年",
        "english": "early life",
        "description": "Childhood and adolescence",
    },
    "month": {
        "start_age": 16,
        "end_age": 32,
        "chinese": "青年",
        "english": "youth",
        "description": "Young adulthood and career building",
    },
    "day": {
        "start_age": 32,
        "end_age": 48,
        "chinese": "中年",
        "english": "middle age",
        "description": "Prime years, self and family",
    },
    "hour": {
        "start_age": 48,
        "end_age": 100,
        "chinese": "晚年",
        "english": "later life",
        "description": "Maturity and legacy",
    },
    # Luck pillars don't have fixed periods - they're temporal overlays
    "10yr_luck": {"chinese": "大運", "english": "10-year luck"},
    "annual": {"chinese": "流年", "english": "annual luck"},
    "monthly": {"chinese": "流月", "english": "monthly luck"},
    "daily": {"chinese": "流日", "english": "daily luck"},
    "hourly": {"chinese": "流時", "english": "hourly luck"},
}

# * -------------------------
# * TEN GODS ASPECT MAPPING (十神與生活層面)
# * -------------------------
# Maps Ten Gods to life aspects they represent

TEN_GOD_ASPECT_MAPPING = {
    # Resource stars (印星) - Learning, mentorship
    "DR": {
        "chinese": "正印",
        "aspect": "learning",
        "sub_aspect": "formal_education",
        "description": "Formal education, traditional knowledge, mentorship",
    },
    "IR": {
        "chinese": "偏印",
        "aspect": "learning",
        "sub_aspect": "unconventional_learning",
        "description": "Self-taught skills, intuition, unconventional methods",
    },
    # Wealth stars (財星) - Financial
    "DW": {
        "chinese": "正財",
        "aspect": "wealth",
        "sub_aspect": "earned_income",
        "description": "Steady income, salary, earned wealth",
    },
    "IW": {
        "chinese": "偏財",
        "aspect": "wealth",
        "sub_aspect": "windfall",
        "description": "Investments, windfall, unexpected gains",
    },
    # Output stars (食傷) - Expression, creativity
    "EG": {
        "chinese": "食神",
        "aspect": "learning",
        "sub_aspect": "creative_expression",
        "description": "Creative output, teaching others, gentle expression",
    },
    "HO": {
        "chinese": "傷官",
        "aspect": "learning",
        "sub_aspect": "innovation",
        "description": "Innovation, challenging norms, rebellious creativity",
    },
    # Officer stars (官殺) - Career, authority
    "DO": {
        "chinese": "正官",
        "aspect": "career",
        "sub_aspect": "formal_authority",
        "description": "Official position, respect, structured career",
    },
    "7K": {
        "chinese": "七殺",
        "aspect": "career",
        "sub_aspect": "competitive_pressure",
        "description": "Pressure, competition, martial energy",
    },
    # Companion stars (比劫) - Relationships
    "F": {
        "chinese": "比肩",
        "aspect": "relationships",
        "sub_aspect": "peer_support",
        "description": "Friends, peers, collaboration",
    },
    "RW": {
        "chinese": "劫財",
        "aspect": "wealth",
        "sub_aspect": "competition",
        "description": "Competition for resources, potential loss",
    },
    # Day Master
    "DM": {
        "chinese": "日主",
        "aspect": "self",
        "sub_aspect": "core_identity",
        "description": "The self, core identity",
    },
}

# * -------------------------
# * ELEMENT CYCLE CONSTANTS (五行生剋)
# * -------------------------
# Wu Xing control and generation cycles

ELEMENT_CONTROLS = {
    "Wood": "Earth",   # 木剋土 Wood breaks Earth
    "Fire": "Metal",   # 火剋金 Fire melts Metal
    "Earth": "Water",  # 土剋水 Earth blocks Water
    "Metal": "Wood",   # 金剋木 Metal cuts Wood
    "Water": "Fire",   # 水剋火 Water extinguishes Fire
}

ELEMENT_GENERATES = {
    "Wood": "Fire",    # 木生火 Wood feeds Fire
    "Fire": "Earth",   # 火生土 Fire creates Earth
    "Earth": "Metal",  # 土生金 Earth bears Metal
    "Metal": "Water",  # 金生水 Metal carries Water
    "Water": "Wood",   # 水生木 Water nourishes Wood
}

# Reverse lookups
ELEMENT_CONTROLLED_BY = {v: k for k, v in ELEMENT_CONTROLS.items()}
ELEMENT_GENERATED_BY = {v: k for k, v in ELEMENT_GENERATES.items()}

# * -------------------------
# * STEM TO ELEMENT MAPPING
# * -------------------------

STEM_TO_ELEMENT = {
    "Jia": "Wood", "Yi": "Wood",
    "Bing": "Fire", "Ding": "Fire",
    "Wu": "Earth", "Ji": "Earth",
    "Geng": "Metal", "Xin": "Metal",
    "Ren": "Water", "Gui": "Water",
}

# * -------------------------
# * CENTRALIZED TRANSLATIONS
# * -------------------------
# Single source of truth for all multilingual strings

ELEMENT_NAMES = {
    "Wood": {"en": "Wood", "zh": "木", "id": "Kayu"},
    "Fire": {"en": "Fire", "zh": "火", "id": "Api"},
    "Earth": {"en": "Earth", "zh": "土", "id": "Tanah"},
    "Metal": {"en": "Metal", "zh": "金", "id": "Logam"},
    "Water": {"en": "Water", "zh": "水", "id": "Air"},
}

SEASONAL_STATES = {
    "Prosperous": {"en": "Prosperous", "zh": "旺", "id": "Makmur"},
    "Strengthening": {"en": "Strengthening", "zh": "相", "id": "Menguat"},
    "Resting": {"en": "Resting", "zh": "休", "id": "Istirahat"},
    "Trapped": {"en": "Trapped", "zh": "囚", "id": "Terjebak"},
    "Dead": {"en": "Dead", "zh": "死", "id": "Mati"},
}

SEVERITY_LABELS = {
    "severe": {"en": "Severe", "zh": "嚴重", "id": "Parah"},
    "moderate": {"en": "Moderate", "zh": "中等", "id": "Sedang"},
    "mild": {"en": "Mild", "zh": "輕微", "id": "Ringan"},
    "balanced": {"en": "Balanced", "zh": "平衡", "id": "Seimbang"},
}

OUTLOOK_LABELS = {
    "favorable": {"en": "Favorable", "zh": "有利", "id": "Menguntungkan"},
    "neutral": {"en": "Neutral", "zh": "中性", "id": "Netral"},
    "challenging": {"en": "Challenging", "zh": "挑戰", "id": "Menantang"},
}

# TCM organ system translations
ORGAN_SYSTEMS = {
    "Hepatobiliary": {"en": "Hepatobiliary", "zh": "肝膽系統", "id": "Hepatobilier"},
    "Cardiovascular": {"en": "Cardiovascular", "zh": "心血管系統", "id": "Kardiovaskular"},
    "Digestive": {"en": "Digestive", "zh": "消化系統", "id": "Pencernaan"},
    "Respiratory": {"en": "Respiratory", "zh": "呼吸系統", "id": "Pernapasan"},
    "Urinary/Reproductive": {"en": "Urinary/Reproductive", "zh": "泌尿生殖系統", "id": "Kemih/Reproduksi"},
}

# Body parts translations (per element)
BODY_PARTS = {
    "Wood": {
        "parts": ["eyes", "tendons", "nails"],
        "zh": ["眼", "筋", "指甲"],
        "id": ["mata", "tendon", "kuku"],
    },
    "Fire": {
        "parts": ["tongue", "blood vessels", "complexion"],
        "zh": ["舌", "血管", "面色"],
        "id": ["lidah", "pembuluh darah", "kulit wajah"],
    },
    "Earth": {
        "parts": ["muscles", "mouth", "lips"],
        "zh": ["肌肉", "口", "唇"],
        "id": ["otot", "mulut", "bibir"],
    },
    "Metal": {
        "parts": ["skin", "nose", "body hair"],
        "zh": ["皮膚", "鼻", "體毛"],
        "id": ["kulit", "hidung", "bulu badan"],
    },
    "Water": {
        "parts": ["bones", "ears", "hair"],
        "zh": ["骨", "耳", "頭髮"],
        "id": ["tulang", "telinga", "rambut"],
    },
}


def get_element_name(element: str, lang: str = "en") -> str:
    """Get element name in specified language."""
    return ELEMENT_NAMES.get(element, {}).get(lang, element)


def get_seasonal_state(state: str, lang: str = "en") -> str:
    """Get seasonal state name in specified language."""
    return SEASONAL_STATES.get(state, {}).get(lang, state)


def get_organ_system(system: str, lang: str = "en") -> str:
    """Get organ system name in specified language."""
    return ORGAN_SYSTEMS.get(system, {}).get(lang, system)


def get_body_parts(element: str, lang: str = "en") -> List[str]:
    """Get body parts for an element in specified language."""
    parts_data = BODY_PARTS.get(element, {})
    if lang == "en":
        return parts_data.get("parts", [])
    return parts_data.get(lang, parts_data.get("parts", []))


# * -------------------------
# * UTILITY FUNCTIONS
# * -------------------------

def stems_to_element_totals(stem_scores: Dict[str, float]) -> Dict[str, float]:
    """
    Convert 10-stem scores to 5-element totals.

    Args:
        stem_scores: Dict mapping stem IDs to scores
                    e.g., {"Jia": 93, "Yi": 313, "Bing": 119, ...}

    Returns:
        Dict mapping elements to totals
        e.g., {"Wood": 406, "Fire": 226, "Earth": 310, "Metal": 68, "Water": 526}
    """
    element_totals = {"Wood": 0.0, "Fire": 0.0, "Earth": 0.0, "Metal": 0.0, "Water": 0.0}

    for stem, score in stem_scores.items():
        element = STEM_TO_ELEMENT.get(stem)
        if element:
            element_totals[element] += score

    return element_totals


def get_node_relationship_context(node_id: str) -> Dict:
    """
    Get the relationship context for a node ID.

    Args:
        node_id: Node identifier (e.g., "hs_y", "eb_d", "hs_10yl")

    Returns:
        Dict with pillar, represents, life_domain, etc.
        Returns empty dict if node_id not found.
    """
    return NODE_RELATIONSHIPS.get(node_id, {})


def get_life_period_for_pillar(pillar: str) -> Dict:
    """
    Get the life period information for a pillar.

    Args:
        pillar: Pillar name (e.g., "year", "month", "day", "hour")

    Returns:
        Dict with start_age, end_age, chinese, english, description
    """
    return PILLAR_LIFE_PERIODS.get(pillar, {})


def detect_control_imbalances(
    seasonal_states: Dict[str, str],
    element_totals: Optional[Dict[str, float]] = None
) -> List[dict]:
    """
    Detect when a weak controller element cannot properly control its target.

    TCM principle: 相侮 (xiāng wǔ) - "Reverse Control"
    When Fire is "Dead"/"Trapped", it cannot properly control Metal.
    Metal becomes uncontrolled and may cause health issues (skin, lungs).

    Args:
        seasonal_states: Dict mapping elements to seasonal states
                        e.g., {"Wood": "Strengthening", "Fire": "Dead", ...}
        element_totals: Optional element score totals for additional analysis

    Returns:
        List of control imbalance dicts with:
        - weak_controller: The element that's too weak
        - controller_state: Its seasonal state (Dead/Trapped)
        - uncontrolled_element: The element that's now imbalanced
        - severity: "elevated" for Dead, "moderate" for Trapped
        - explanation: Human-readable explanation
    """
    imbalances = []

    for controller, controlled in ELEMENT_CONTROLS.items():
        controller_state = seasonal_states.get(controller, "Resting")

        if controller_state in ["Dead", "Trapped"]:
            # Determine severity based on seasonal state
            if controller_state == "Dead":
                severity = "elevated"
                severity_chinese = "較高"
            else:  # Trapped
                severity = "moderate"
                severity_chinese = "中等"

            imbalance = {
                "type": "control_imbalance",
                "weak_controller": controller,
                "weak_controller_chinese": {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}.get(controller, ""),
                "controller_state": controller_state,
                "controller_state_chinese": {"Dead": "死", "Trapped": "囚"}.get(controller_state, ""),
                "uncontrolled_element": controlled,
                "uncontrolled_element_chinese": {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}.get(controlled, ""),
                "severity": severity,
                "severity_chinese": severity_chinese,
                "explanation": f"{controller} ({controller_state}) cannot properly control {controlled}",
                "explanation_chinese": f"{controller}({controller_state})無法有效控制{controlled}",
            }

            # Add element score context if available
            if element_totals:
                controller_score = element_totals.get(controller, 0)
                controlled_score = element_totals.get(controlled, 0)
                imbalance["controller_score"] = controller_score
                imbalance["controlled_score"] = controlled_score

                # Additional severity check: if controlled is much stronger
                if controlled_score > controller_score * 1.5:
                    imbalance["score_imbalance"] = True
                    imbalance["explanation"] += f" (score imbalance: {controlled} {controlled_score:.0f} >> {controller} {controller_score:.0f})"

            imbalances.append(imbalance)

    return imbalances


def calculate_aspect_severity(
    conflict_count: int,
    seasonal_state: str,
    control_imbalances: List[dict],
    base_weight: float = 10.0
) -> Tuple[float, str]:
    """
    Calculate overall severity score for a life aspect.

    Args:
        conflict_count: Number of direct conflicts affecting this aspect
        seasonal_state: Seasonal state of the primary element (Prosperous/Dead/etc.)
        control_imbalances: List of control imbalance dicts
        base_weight: Base points per conflict (default 10)

    Returns:
        Tuple of (severity_score, severity_category)
        - severity_score: 0-100 numeric score
        - severity_category: "severe", "moderate", "mild", or "balanced"
    """
    # Seasonal modifiers
    SEASONAL_MOD = {
        "Prosperous": 0.5,
        "Strengthening": 0.7,
        "Resting": 1.0,
        "Trapped": 1.5,
        "Dead": 2.0,
    }

    seasonal_mod = SEASONAL_MOD.get(seasonal_state, 1.0)

    # Base score from conflicts
    conflict_score = conflict_count * base_weight * seasonal_mod

    # Add control imbalance impact
    imbalance_score = 0
    for imbalance in control_imbalances:
        if imbalance.get("severity") == "elevated":
            imbalance_score += 15 * seasonal_mod
        else:  # moderate
            imbalance_score += 10 * seasonal_mod

    total_score = conflict_score + imbalance_score

    # Normalize to 0-100
    normalized = min(100, (total_score / 100) * 100)

    # Determine category
    if normalized > 60 or (control_imbalances and seasonal_state in ["Dead", "Trapped"]):
        category = "severe"
    elif normalized > 30 or control_imbalances:
        category = "moderate"
    elif normalized > 10:
        category = "mild"
    else:
        category = "balanced"

    return round(normalized, 1), category


def get_ten_god_aspect(ten_god_id: str) -> Dict:
    """
    Get the life aspect mapping for a Ten God.

    Args:
        ten_god_id: Ten God abbreviation (e.g., "DW", "IR", "HO")

    Returns:
        Dict with aspect, sub_aspect, description, chinese
    """
    return TEN_GOD_ASPECT_MAPPING.get(ten_god_id, {})
