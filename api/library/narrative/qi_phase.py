# * =========================
# * QI PHASE CALCULATION (十二长生)
# * =========================
# The 12 Life Phases that each element goes through based on earthly branches.
# This is crucial for understanding the strength and state of elements.
#
# The 12 phases in order:
# 长生 → 沐浴 → 冠带 → 临官 → 帝旺 → 衰 → 病 → 死 → 墓 → 绝 → 胎 → 养
# Birth → Bath → Cap → Official → Emperor → Decline → Illness → Death → Tomb → Extinct → Embryo → Nurture

from typing import Dict, List, Tuple, Optional

# =============================================================================
# QI PHASE DEFINITIONS
# =============================================================================

QI_PHASE_ORDER = [
    "CHANG_SHENG",  # 长生 - Birth/Long Life
    "MU_YU",        # 沐浴 - Bathing
    "GUAN_DAI",     # 冠带 - Capping
    "LIN_GUAN",     # 临官 - Official
    "DI_WANG",      # 帝旺 - Emperor
    "SHUAI",        # 衰 - Decline
    "BING",         # 病 - Illness
    "SI",           # 死 - Death
    "MU",           # 墓 - Tomb (STORAGE)
    "JUE",          # 绝 - Extinction
    "TAI",          # 胎 - Embryo
    "YANG",         # 养 - Nurturing
]

BRANCH_ORDER = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]

# Starting branch for each element's Chang Sheng (Birth) phase
# Yang elements go forward, Yin elements go backward
ELEMENT_BIRTH_BRANCH = {
    # Yang elements - forward cycle
    "Yang Wood": "Hai",    # 甲木长生在亥
    "Yang Fire": "Yin",    # 丙火长生在寅
    "Yang Earth": "Yin",   # 戊土长生在寅 (follows Fire)
    "Yang Metal": "Si",    # 庚金长生在巳
    "Yang Water": "Shen",  # 壬水长生在申
    # Yin elements - backward cycle
    "Yin Wood": "Wu",      # 乙木长生在午
    "Yin Fire": "You",     # 丁火长生在酉
    "Yin Earth": "You",    # 己土长生在酉 (follows Fire)
    "Yin Metal": "Zi",     # 辛金长生在子
    "Yin Water": "Mao",    # 癸水长生在卯
}

# QI Phase info with Chinese names and meanings
QI_PHASE_INFO = {
    "CHANG_SHENG": {
        "chinese": "长生",
        "english": "Birth",
        "meaning_en": "New beginnings, vitality, growth potential, starting phase",
        "meaning_zh": "新的开始、活力、成长潜力、起步阶段",
        "strength": "growing",
        "is_storage": False,
    },
    "MU_YU": {
        "chinese": "沐浴",
        "english": "Bathing",
        "meaning_en": "Vulnerability, exposure, cleansing, romantic encounters, instability",
        "meaning_zh": "脆弱、暴露、洁净、浪漫邂逅、不稳定",
        "strength": "unstable",
        "is_storage": False,
        "special_note_en": "Also called 'Peach Blossom Ground' - indicates romantic but unstable energy",
        "special_note_zh": "也叫'桃花地'——表示浪漫但不稳定的能量",
    },
    "GUAN_DAI": {
        "chinese": "冠带",
        "english": "Capping",
        "meaning_en": "Coming of age, taking responsibility, gaining recognition",
        "meaning_zh": "成年、承担责任、获得认可",
        "strength": "strengthening",
        "is_storage": False,
    },
    "LIN_GUAN": {
        "chinese": "临官",
        "english": "Official",
        "meaning_en": "Career advancement, authority, professional peak, taking office",
        "meaning_zh": "事业发展、权威、职业巅峰、走马上任",
        "strength": "strong",
        "is_storage": False,
    },
    "DI_WANG": {
        "chinese": "帝旺",
        "english": "Emperor",
        "meaning_en": "Peak power, maximum strength, full bloom, but also at turning point",
        "meaning_zh": "权力巅峰、最大力量、全盛期，但也是转折点",
        "strength": "peak",
        "is_storage": False,
        "special_note_en": "At the very peak - nowhere to go but down. Yang energy at maximum.",
        "special_note_zh": "处于顶峰——盛极而衰。阳气达到最大。",
    },
    "SHUAI": {
        "chinese": "衰",
        "english": "Decline",
        "meaning_en": "Weakening, reduction, need for conservation, past prime",
        "meaning_zh": "衰弱、减少、需要保守、过了巅峰",
        "strength": "weakening",
        "is_storage": False,
    },
    "BING": {
        "chinese": "病",
        "english": "Illness",
        "meaning_en": "Vulnerability, need for healing, potential health issues, weakness",
        "meaning_zh": "脆弱、需要疗愈、潜在健康问题、虚弱",
        "strength": "weak",
        "is_storage": False,
    },
    "SI": {
        "chinese": "死",
        "english": "Death",
        "meaning_en": "Ending, transformation, release of old patterns, stillness",
        "meaning_zh": "结束、转化、释放旧模式、静止",
        "strength": "dead",
        "is_storage": False,
    },
    "MU": {
        "chinese": "墓",
        "english": "Tomb",
        "meaning_en": "Hidden storage, buried potential, things waiting to be unlocked",
        "meaning_zh": "隐藏储存、埋藏潜力、等待开启的事物",
        "strength": "stored",
        "is_storage": True,
        "special_note_en": "STORAGE phase - contains hidden resources. Needs opener (clash) to release.",
        "special_note_zh": "库的阶段——包含隐藏资源。需要开启者（冲）来释放。",
    },
    "JUE": {
        "chinese": "绝",
        "english": "Extinction",
        "meaning_en": "Complete ending, void, emptiness, but also seed of new beginning",
        "meaning_zh": "完全结束、虚空、空虚，但也是新开始的种子",
        "strength": "extinct",
        "is_storage": False,
    },
    "TAI": {
        "chinese": "胎",
        "english": "Embryo",
        "meaning_en": "Conception, planning, potential not yet manifested, hidden growth",
        "meaning_zh": "孕育、规划、尚未显现的潜力、隐藏的成长",
        "strength": "forming",
        "is_storage": False,
    },
    "YANG": {
        "chinese": "养",
        "english": "Nurturing",
        "meaning_en": "Preparation, nurturing, building foundation, gathering strength",
        "meaning_zh": "准备、滋养、打基础、积蓄力量",
        "strength": "nurturing",
        "is_storage": False,
    },
}


# =============================================================================
# CALCULATION FUNCTIONS
# =============================================================================

def get_qi_phase(element: str, polarity: str, branch: str) -> Dict[str, any]:
    """
    Calculate the Qi Phase for an element in a given branch.

    Args:
        element: Element name (Wood, Fire, Earth, Metal, Water)
        polarity: "Yang" or "Yin"
        branch: Earthly branch (Zi, Chou, Yin, etc.)

    Returns:
        Dict with phase info including:
        - phase: Phase key (e.g., "MU" for Tomb)
        - chinese: Chinese name
        - english: English name
        - meaning: Full meaning
        - is_storage: Whether this is a storage phase
    """
    polarity_element = f"{polarity} {element}"

    if polarity_element not in ELEMENT_BIRTH_BRANCH:
        return {"phase": "UNKNOWN", "chinese": "未知", "english": "Unknown"}

    birth_branch = ELEMENT_BIRTH_BRANCH[polarity_element]
    birth_index = BRANCH_ORDER.index(birth_branch)
    branch_index = BRANCH_ORDER.index(branch)

    # Calculate phase offset
    if polarity == "Yang":
        # Yang goes forward (clockwise)
        offset = (branch_index - birth_index) % 12
    else:
        # Yin goes backward (counter-clockwise)
        offset = (birth_index - branch_index) % 12

    phase_key = QI_PHASE_ORDER[offset]
    phase_info = QI_PHASE_INFO[phase_key]

    return {
        "phase": phase_key,
        "chinese": phase_info["chinese"],
        "english": phase_info["english"],
        "meaning_en": phase_info["meaning_en"],
        "meaning_zh": phase_info["meaning_zh"],
        "strength": phase_info["strength"],
        "is_storage": phase_info["is_storage"],
        "special_note_en": phase_info.get("special_note_en", ""),
        "special_note_zh": phase_info.get("special_note_zh", ""),
    }


def get_qi_phase_for_stem(stem: str, branch: str) -> Dict[str, any]:
    """
    Calculate Qi Phase for a Heavenly Stem in a given branch.

    Args:
        stem: Stem name (Jia, Yi, Bing, etc.)
        branch: Branch name (Zi, Chou, etc.)

    Returns:
        Qi Phase info dict
    """
    STEM_INFO = {
        "Jia": ("Wood", "Yang"),
        "Yi": ("Wood", "Yin"),
        "Bing": ("Fire", "Yang"),
        "Ding": ("Fire", "Yin"),
        "Wu": ("Earth", "Yang"),
        "Ji": ("Earth", "Yin"),
        "Geng": ("Metal", "Yang"),
        "Xin": ("Metal", "Yin"),
        "Ren": ("Water", "Yang"),
        "Gui": ("Water", "Yin"),
    }

    if stem not in STEM_INFO:
        return {"phase": "UNKNOWN", "chinese": "未知", "english": "Unknown"}

    element, polarity = STEM_INFO[stem]
    return get_qi_phase(element, polarity, branch)


def get_storage_info(branch: str) -> Optional[Dict[str, str]]:
    """
    Get storage information for a branch if it's a storage branch (库).

    The four storage branches are: Chen, Xu, Chou, Wei
    Each stores a specific element and has a specific opener (clash branch).

    Args:
        branch: Branch name

    Returns:
        Storage info dict or None if not a storage branch
    """
    STORAGE_BRANCHES = {
        "Chen": {"stores": "Water", "opener": "Xu", "chinese": "辰"},
        "Xu": {"stores": "Fire", "opener": "Chen", "chinese": "戌"},
        "Chou": {"stores": "Metal", "opener": "Wei", "chinese": "丑"},
        "Wei": {"stores": "Wood", "opener": "Chou", "chinese": "未"},
    }

    if branch in STORAGE_BRANCHES:
        info = STORAGE_BRANCHES[branch]
        return {
            "branch": branch,
            "branch_chinese": info["chinese"],
            "stores": info["stores"],
            "opener": info["opener"],
            "is_storage": True,
        }

    return None


def get_all_phases_for_branch(branch: str) -> Dict[str, Dict[str, any]]:
    """
    Get the Qi Phase of ALL elements in a given branch.

    Useful for comprehensive branch analysis.

    Args:
        branch: Branch name

    Returns:
        Dict mapping "Element Polarity" -> Qi Phase info
    """
    result = {}

    for polarity_element, _ in ELEMENT_BIRTH_BRANCH.items():
        polarity, element = polarity_element.split(" ")
        phase_info = get_qi_phase(element, polarity, branch)
        result[polarity_element] = phase_info

    return result


def find_phases_in_branch(branch: str, phase: str) -> List[str]:
    """
    Find which elements have a specific phase in a branch.

    E.g., "Which elements are in Tomb (MU) phase in Chou?"

    Args:
        branch: Branch name
        phase: Phase key (e.g., "MU" for Tomb)

    Returns:
        List of "Polarity Element" strings that have this phase
    """
    result = []

    all_phases = get_all_phases_for_branch(branch)
    for polarity_element, phase_info in all_phases.items():
        if phase_info["phase"] == phase:
            result.append(polarity_element)

    return result


# =============================================================================
# NARRATIVE INTEGRATION
# =============================================================================

def get_qi_phase_narrative_context(
    stem: str,
    branch: str,
    locale: str = "en"
) -> Dict[str, any]:
    """
    Get complete Qi Phase context for narrative generation.

    Includes:
    - Phase info
    - Storage status
    - What elements are stored (if storage)
    - Narrative meaning

    Args:
        stem: The stem to check phase for (usually daymaster stem)
        branch: The branch to check in
        locale: "en" or "zh"

    Returns:
        Complete context dict for narrative
    """
    phase_info = get_qi_phase_for_stem(stem, branch)
    storage_info = get_storage_info(branch)

    result = {
        "stem": stem,
        "branch": branch,
        "phase": phase_info["phase"],
        "phase_chinese": phase_info["chinese"],
        "phase_english": phase_info["english"],
        "phase_meaning": phase_info["meaning_en"] if locale == "en" else phase_info["meaning_zh"],
        "strength": phase_info["strength"],
        "is_storage_phase": phase_info["is_storage"],
    }

    if phase_info.get("special_note_en"):
        result["special_note"] = phase_info["special_note_en"] if locale == "en" else phase_info["special_note_zh"]

    if storage_info:
        result["is_storage_branch"] = True
        result["stored_element"] = storage_info["stores"]
        result["opener_branch"] = storage_info["opener"]
    else:
        result["is_storage_branch"] = False

    return result
