# * =========================
# * CHAIN ANALYSIS ENGINE
# * =========================
# Comprehensive node analysis that chains together ALL factors:
# - Element & Favorability
# - Ten God relationship
# - Shen Sha (Auxiliary Stars)
# - Qi Phase (十二长生)
# - Storage status (Wealth/Officer storage)
# - Opener status
#
# All deterministic, all template-based, all interconnected.

from typing import Dict, Any, List, Optional, Tuple

# =============================================================================
# SHEN SHA (AUXILIARY STARS) MEANINGS
# =============================================================================
# Each Shen Sha has base meaning + contextual meanings based on other factors

SHEN_SHA_MEANINGS = {
    "GU_CHEN": {  # 孤辰 - Lonely Star (male)
        "chinese": "孤辰",
        "english": "Lonely Star",
        "base": {
            "en": "tendency toward isolation and independence",
            "zh": "孤独和独立的倾向",
        },
        "with_unfavorable_element": {
            "en": "isolation amplified by elemental imbalance - loneliness feels heavier",
            "zh": "五行失衡加剧孤独感——孤独感更重",
        },
        "with_eating_god_excess": {
            "en": "isolation from being too picky and perfectionist - standards too high to connect",
            "zh": "因过于挑剔和完美主义而孤立——标准太高难以建立联系",
        },
        "in_spouse_palace": {
            "en": "loneliness specifically in marriage - difficulty finding or keeping partner",
            "zh": "婚姻中的孤独——难以找到或留住伴侣",
        },
        "in_spouse_palace_with_clash": {
            "en": "marriage blocked by isolation energy - destined pattern of loneliness in relationships",
            "zh": "孤独能量阻碍婚姻——感情中注定的孤独模式",
        },
    },
    "GUA_SU": {  # 寡宿 - Widow Star (female)
        "chinese": "寡宿",
        "english": "Widow Star",
        "base": {
            "en": "tendency toward solitude and self-reliance",
            "zh": "独处和自力更生的倾向",
        },
        "with_unfavorable_element": {
            "en": "solitude deepened by elemental imbalance",
            "zh": "五行失衡加深独处倾向",
        },
        "with_eating_god_excess": {
            "en": "solitude from overthinking and excessive standards",
            "zh": "因过度思虑和标准过高而独处",
        },
        "in_spouse_palace": {
            "en": "widow energy in marriage palace - late marriage or loss of spouse",
            "zh": "婚姻宫有寡宿——晚婚或失去配偶",
        },
        "in_spouse_palace_with_clash": {
            "en": "widow star clashed - marriage difficulties compounded",
            "zh": "寡宿被冲——婚姻困难加剧",
        },
    },
    "HUA_GAI": {  # 华盖 - Imperial Canopy
        "chinese": "华盖",
        "english": "Imperial Canopy",
        "base": {
            "en": "artistic talent, spiritual inclination, but also isolation from being 'above' others",
            "zh": "艺术天赋、灵性倾向，但也因'高人一等'而孤立",
        },
        "with_favorable_element": {
            "en": "artistic talents supported - can achieve recognition and success",
            "zh": "艺术天赋得到支持——可以获得认可和成功",
        },
        "with_unfavorable_element": {
            "en": "talents blocked by imbalance - artistic isolation without recognition",
            "zh": "才华被失衡阻碍——艺术上的孤立而无认可",
        },
        "with_eating_god_excess": {
            "en": "extreme perfectionism in art/spirituality - never satisfied with own work",
            "zh": "艺术/灵性上的极端完美主义——永远不满意自己的作品",
        },
        "in_spouse_palace": {
            "en": "spiritual/artistic nature affects marriage - partner must understand unique nature",
            "zh": "灵性/艺术气质影响婚姻——伴侣必须理解独特性格",
        },
        "with_tomb_phase": {
            "en": "talents hidden/buried - potential not yet realized, needs unlocking",
            "zh": "才华被隐藏/埋没——潜力尚未实现，需要开启",
        },
    },
    "TIAN_YI": {  # 天乙贵人 - Heavenly Noble
        "chinese": "天乙贵人",
        "english": "Heavenly Noble",
        "base": {
            "en": "attracts help from benefactors and noble people",
            "zh": "吸引贵人相助",
        },
        "with_favorable_element": {
            "en": "strong benefactor support - help comes easily when needed",
            "zh": "贵人支持强——需要时帮助容易获得",
        },
        "with_unfavorable_element": {
            "en": "benefactor energy weakened by imbalance - help available but harder to access",
            "zh": "贵人能量被失衡削弱——帮助存在但较难获得",
        },
        "in_spouse_palace": {
            "en": "spouse is a noble person - marriage brings elevation and support",
            "zh": "配偶是贵人——婚姻带来提升和支持",
        },
    },
    "TAO_HUA": {  # 桃花 - Peach Blossom
        "chinese": "桃花",
        "english": "Peach Blossom",
        "base": {
            "en": "romantic charm and attractiveness",
            "zh": "浪漫魅力和吸引力",
        },
        "with_favorable_element": {
            "en": "charm supported - attracts good romantic opportunities",
            "zh": "魅力得到支持——吸引好的浪漫机会",
        },
        "with_unfavorable_element": {
            "en": "charm creates complications - attracts but can't maintain",
            "zh": "魅力带来复杂——能吸引但难以维持",
        },
        "in_spouse_palace": {
            "en": "romantic nature in marriage - passionate but potentially unstable",
            "zh": "婚姻中的浪漫本性——热情但可能不稳定",
        },
        "in_spouse_palace_with_clash": {
            "en": "romance clashed - passionate attractions lead to conflict",
            "zh": "浪漫被冲——热情吸引导致冲突",
        },
    },
    "YANG_REN": {  # 羊刃 - Blade
        "chinese": "羊刃",
        "english": "Blade",
        "base": {
            "en": "aggressive energy, competitiveness, sharp personality",
            "zh": "攻击性能量、竞争性、尖锐性格",
        },
        "with_favorable_element": {
            "en": "competitive edge serves you well - can cut through obstacles",
            "zh": "竞争优势对你有利——可以克服障碍",
        },
        "with_unfavorable_element": {
            "en": "aggression backfires - sharp energy cuts self and others",
            "zh": "攻击性反噬——尖锐能量伤害自己和他人",
        },
        "in_spouse_palace": {
            "en": "blade in marriage - sharp conflicts with spouse, potential for separation",
            "zh": "婚姻中的羊刃——与配偶的尖锐冲突，有分离可能",
        },
    },
}

# =============================================================================
# QI PHASE (十二长生) MEANINGS
# =============================================================================

QI_PHASE_MEANINGS = {
    "CHANG_SHENG": {  # 长生 - Birth/Long Life
        "chinese": "长生",
        "english": "Birth",
        "base": {
            "en": "new beginnings, vitality, growth potential",
            "zh": "新的开始、活力、成长潜力",
        },
        "element_context": {
            "en": "element energy is being born - fresh and growing",
            "zh": "五行能量正在诞生——新鲜且成长中",
        },
    },
    "MU_YU": {  # 沐浴 - Bathing
        "chinese": "沐浴",
        "english": "Bathing",
        "base": {
            "en": "vulnerability, exposure, romantic encounters",
            "zh": "脆弱、暴露、浪漫邂逅",
        },
        "in_spouse_palace": {
            "en": "bathing phase in spouse palace - romantic but vulnerable in marriage",
            "zh": "配偶宫沐浴——婚姻中浪漫但脆弱",
        },
    },
    "GUAN_DAI": {  # 冠带 - Capping
        "chinese": "冠带",
        "english": "Capping",
        "base": {
            "en": "coming of age, taking responsibility, gaining recognition",
            "zh": "成年、承担责任、获得认可",
        },
    },
    "LIN_GUAN": {  # 临官 - Official
        "chinese": "临官",
        "english": "Official",
        "base": {
            "en": "career advancement, authority, peak performance",
            "zh": "事业发展、权威、巅峰表现",
        },
    },
    "DI_WANG": {  # 帝旺 - Emperor
        "chinese": "帝旺",
        "english": "Emperor",
        "base": {
            "en": "peak power, maximum strength, but also nowhere to go but down",
            "zh": "权力巅峰、最大力量，但也盛极而衰",
        },
    },
    "SHUAI": {  # 衰 - Decline
        "chinese": "衰",
        "english": "Decline",
        "base": {
            "en": "weakening, reduction, need for conservation",
            "zh": "衰弱、减少、需要保守",
        },
    },
    "BING": {  # 病 - Illness
        "chinese": "病",
        "english": "Illness",
        "base": {
            "en": "vulnerability, need for healing, potential health issues",
            "zh": "脆弱、需要疗愈、潜在健康问题",
        },
    },
    "SI": {  # 死 - Death
        "chinese": "死",
        "english": "Death",
        "base": {
            "en": "ending, transformation, release of old patterns",
            "zh": "结束、转化、释放旧模式",
        },
    },
    "MU": {  # 墓 - Tomb/Storage
        "chinese": "墓",
        "english": "Tomb",
        "base": {
            "en": "hidden storage, buried potential, things waiting to be unlocked",
            "zh": "隐藏储存、埋藏潜力、等待开启的事物",
        },
        "is_storage": True,
        "storage_meaning": {
            "en": "This branch acts as a STORAGE - containing hidden resources that need an opener to access",
            "zh": "此支是库——包含需要开启者才能获取的隐藏资源",
        },
        "with_no_opener": {
            "en": "storage locked - potential remains buried and inaccessible",
            "zh": "库未开——潜力仍被埋藏无法获取",
        },
        "with_opener": {
            "en": "storage opened - hidden resources become accessible",
            "zh": "库已开——隐藏资源变得可获取",
        },
        "with_clash": {
            "en": "storage clashed open - resources released suddenly, possibly chaotically",
            "zh": "库被冲开——资源突然释放，可能混乱",
        },
    },
    "JUE": {  # 绝 - Extinction
        "chinese": "绝",
        "english": "Extinction",
        "base": {
            "en": "complete ending, void, but also seed of new beginning",
            "zh": "完全结束、虚空，但也是新开始的种子",
        },
    },
    "TAI": {  # 胎 - Embryo
        "chinese": "胎",
        "english": "Embryo",
        "base": {
            "en": "conception, planning, potential not yet manifested",
            "zh": "孕育、规划、尚未显现的潜力",
        },
    },
    "YANG": {  # 养 - Nurturing
        "chinese": "养",
        "english": "Nurturing",
        "base": {
            "en": "preparation, nurturing, building foundation",
            "zh": "准备、滋养、打基础",
        },
    },
}

# =============================================================================
# STORAGE BRANCH MAPPINGS
# =============================================================================

# Which branches are Storage (库) for which elements
STORAGE_BRANCHES = {
    "Chen": {"stores": "Water", "opener": "Xu"},   # 辰 stores Water, opened by Xu
    "Xu": {"stores": "Fire", "opener": "Chen"},    # 戌 stores Fire, opened by Chen
    "Chou": {"stores": "Metal", "opener": "Wei"},  # 丑 stores Metal, opened by Wei
    "Wei": {"stores": "Wood", "opener": "Chou"},   # 未 stores Wood, opened by Chou
}

# Day Master to Wealth Storage mapping
DM_TO_WEALTH_STORAGE = {
    "Wood": "Chen",   # Wood DM wealth (Earth) → but Earth has no dedicated storage, assigned Chen
    "Fire": "Chou",   # Fire DM wealth (Metal) → Chou stores Metal
    "Earth": "Chen",  # Earth DM wealth (Water) → Chen stores Water
    "Metal": "Wei",   # Metal DM wealth (Wood) → Wei stores Wood
    "Water": "Xu",    # Water DM wealth (Fire) → Xu stores Fire
}

# =============================================================================
# TEN GODS CONTEXT
# =============================================================================

TEN_GOD_NAMES = {
    "output": {"en": "Eating God/Hurting Officer", "zh": "食伤", "abbrev": "EG/HO"},
    "resource": {"en": "Resource/Seal", "zh": "印", "abbrev": "R"},
    "companion": {"en": "Friend/Rob Wealth", "zh": "比劫", "abbrev": "F/RW"},
    "wealth": {"en": "Direct/Indirect Wealth", "zh": "财", "abbrev": "DW/IW"},
    "officer": {"en": "Direct Officer/Seven Killings", "zh": "官杀", "abbrev": "DO/7K"},
}

TEN_GOD_EXCESS_TRAITS = {
    "output": ["perfectionist", "overthinking", "picky", "slow to act", "hard to settle"],
    "resource": ["dependent", "passive", "lazy", "expects help"],
    "companion": ["stubborn", "competitive", "jealous", "selfish"],
    "wealth": ["materialistic", "greedy", "workaholic", "neglects relationships"],
    "officer": ["stressed", "pressured", "controlled", "authority conflicts"],
}


# =============================================================================
# CHAIN ANALYSIS ENGINE
# =============================================================================

def analyze_node_chain(
    branch: str,
    element: str,
    is_favorable: bool,
    ten_god: str,
    shen_sha_list: List[str],
    qi_phase: str,
    pillar_type: str,  # "day", "hour", "month", "year"
    daymaster_element: str,
    element_percentages: Dict[str, float],
    has_clash: bool = False,
    clash_with: str = "",
    locale: str = "en"
) -> Dict[str, Any]:
    """
    Comprehensive chain analysis for a single node/branch.

    Links together ALL factors into interconnected narrative:
    1. Element & Favorability context
    2. Ten God relationship and excess meaning
    3. Shen Sha meanings (contextual)
    4. Qi Phase meaning
    5. Storage status and opener
    6. Combined chain interpretation

    Returns complete analysis dict with all chains linked.
    """
    result = {
        "branch": branch,
        "element": element,
        "is_favorable": is_favorable,
        "ten_god": ten_god,
        "pillar_type": pillar_type,
        "chains": [],
        "combined_narrative": "",
    }

    # =========================================================================
    # CHAIN 1: Element & Favorability
    # =========================================================================
    element_pct = element_percentages.get(element, 0)
    element_chain = {
        "type": "element",
        "element": element,
        "percentage": element_pct,
        "favorable": is_favorable,
    }

    if is_favorable:
        element_chain["meaning"] = f"{element} ({element_pct:.1f}%) is favorable for your chart"
        element_chain["meaning_zh"] = f"{_element_zh(element)}（{element_pct:.1f}%）对您的命盘有利"
    else:
        if element_pct > 28:
            element_chain["meaning"] = f"{element} ({element_pct:.1f}%) is excessive and unfavorable"
            element_chain["meaning_zh"] = f"{_element_zh(element)}（{element_pct:.1f}%）过旺且不利"
        else:
            element_chain["meaning"] = f"{element} ({element_pct:.1f}%) is unfavorable for your chart balance"
            element_chain["meaning_zh"] = f"{_element_zh(element)}（{element_pct:.1f}%）对命盘平衡不利"

    result["chains"].append(element_chain)

    # =========================================================================
    # CHAIN 2: Ten God
    # =========================================================================
    if ten_god:
        ten_god_info = TEN_GOD_NAMES.get(ten_god, {})
        ten_god_chain = {
            "type": "ten_god",
            "ten_god": ten_god,
            "name_en": ten_god_info.get("en", ten_god),
            "name_zh": ten_god_info.get("zh", ten_god),
        }

        # Check if this Ten God is in excess
        is_excess = element_pct > 28
        if is_excess:
            traits = TEN_GOD_EXCESS_TRAITS.get(ten_god, [])
            ten_god_chain["is_excess"] = True
            ten_god_chain["excess_traits"] = traits
            ten_god_chain["meaning"] = f"Excessive {ten_god_info.get('en', ten_god)}: {', '.join(traits)}"
            ten_god_chain["meaning_zh"] = f"过旺的{ten_god_info.get('zh', ten_god)}：{_traits_zh(traits)}"
        else:
            ten_god_chain["is_excess"] = False
            ten_god_chain["meaning"] = f"{ten_god_info.get('en', ten_god)} relationship"
            ten_god_chain["meaning_zh"] = f"{ten_god_info.get('zh', ten_god)}关系"

        result["chains"].append(ten_god_chain)

    # =========================================================================
    # CHAIN 3: Shen Sha (Auxiliary Stars)
    # =========================================================================
    for shen_sha in shen_sha_list:
        shen_sha_data = SHEN_SHA_MEANINGS.get(shen_sha, {})
        if not shen_sha_data:
            continue

        shen_sha_chain = {
            "type": "shen_sha",
            "shen_sha": shen_sha,
            "chinese": shen_sha_data.get("chinese", ""),
            "english": shen_sha_data.get("english", ""),
            "base_meaning": shen_sha_data.get("base", {}).get(locale, ""),
        }

        # Build contextual meaning based on other factors
        contextual_meanings = []

        # Context: Favorable/Unfavorable element
        if is_favorable and "with_favorable_element" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["with_favorable_element"].get(locale, ""))
        elif not is_favorable and "with_unfavorable_element" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["with_unfavorable_element"].get(locale, ""))

        # Context: Ten God excess
        if ten_god == "output" and element_pct > 28 and "with_eating_god_excess" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["with_eating_god_excess"].get(locale, ""))

        # Context: Spouse Palace
        if pillar_type == "day" and "in_spouse_palace" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["in_spouse_palace"].get(locale, ""))

        # Context: Spouse Palace with Clash
        if pillar_type == "day" and has_clash and "in_spouse_palace_with_clash" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["in_spouse_palace_with_clash"].get(locale, ""))

        # Context: Tomb phase
        if qi_phase == "MU" and "with_tomb_phase" in shen_sha_data:
            contextual_meanings.append(shen_sha_data["with_tomb_phase"].get(locale, ""))

        shen_sha_chain["contextual_meanings"] = contextual_meanings
        shen_sha_chain["combined_meaning"] = " → ".join([shen_sha_chain["base_meaning"]] + contextual_meanings)

        result["chains"].append(shen_sha_chain)

    # =========================================================================
    # CHAIN 4: Qi Phase
    # =========================================================================
    if qi_phase:
        qi_phase_data = QI_PHASE_MEANINGS.get(qi_phase, {})
        qi_phase_chain = {
            "type": "qi_phase",
            "phase": qi_phase,
            "chinese": qi_phase_data.get("chinese", ""),
            "english": qi_phase_data.get("english", ""),
            "base_meaning": qi_phase_data.get("base", {}).get(locale, ""),
        }

        # Special handling for Tomb (Storage)
        if qi_phase == "MU" and qi_phase_data.get("is_storage"):
            qi_phase_chain["is_storage"] = True
            qi_phase_chain["storage_meaning"] = qi_phase_data.get("storage_meaning", {}).get(locale, "")

        result["chains"].append(qi_phase_chain)

    # =========================================================================
    # CHAIN 5: Storage Analysis
    # =========================================================================
    storage_info = STORAGE_BRANCHES.get(branch)
    if storage_info:
        storage_chain = {
            "type": "storage",
            "branch": branch,
            "stores": storage_info["stores"],
            "opener": storage_info["opener"],
        }

        # Check if this is Wealth Storage for the daymaster
        wealth_storage_branch = DM_TO_WEALTH_STORAGE.get(daymaster_element)
        if branch == wealth_storage_branch:
            storage_chain["is_wealth_storage"] = True
            storage_chain["wealth_element"] = storage_info["stores"]

            # Check wealth element strength in chart
            wealth_pct = element_percentages.get(storage_info["stores"], 0)
            storage_chain["wealth_percentage"] = wealth_pct

            if wealth_pct <= 5:
                storage_chain["wealth_strength"] = "severely_weak"
                storage_chain["wealth_meaning"] = f"Wealth ({storage_info['stores']}) is severely weak at {wealth_pct:.1f}% - wealth storage contains little"
            elif wealth_pct <= 12:
                storage_chain["wealth_strength"] = "weak"
                storage_chain["wealth_meaning"] = f"Wealth ({storage_info['stores']}) is weak at {wealth_pct:.1f}%"
            else:
                storage_chain["wealth_strength"] = "adequate"
                storage_chain["wealth_meaning"] = f"Wealth ({storage_info['stores']}) at {wealth_pct:.1f}%"

        # Check opener status
        if has_clash and clash_with == storage_info["opener"]:
            storage_chain["opener_present"] = True
            storage_chain["opened_by_clash"] = True
            storage_chain["opener_meaning"] = f"Storage clashed open by {storage_info['opener']} - resources released, possibly chaotically"
        else:
            # Would need to check if opener exists elsewhere in chart
            storage_chain["opener_present"] = False
            storage_chain["opener_meaning"] = f"Storage locked - needs {storage_info['opener']} to open"

        result["chains"].append(storage_chain)

    # =========================================================================
    # COMBINED NARRATIVE
    # =========================================================================
    result["combined_narrative"] = _build_combined_narrative(result["chains"], locale)

    return result


def _build_combined_narrative(chains: List[Dict[str, Any]], locale: str) -> str:
    """Build a combined narrative from all chains."""
    parts = []

    for chain in chains:
        chain_type = chain.get("type", "")

        if chain_type == "element":
            parts.append(chain.get("meaning" if locale == "en" else "meaning_zh", ""))

        elif chain_type == "ten_god":
            if chain.get("is_excess"):
                parts.append(chain.get("meaning" if locale == "en" else "meaning_zh", ""))

        elif chain_type == "shen_sha":
            combined = chain.get("combined_meaning", "")
            if combined:
                name = chain.get("english" if locale == "en" else "chinese", "")
                parts.append(f"{name}: {combined}")

        elif chain_type == "qi_phase":
            if chain.get("is_storage"):
                parts.append(chain.get("storage_meaning", ""))
            else:
                parts.append(f"Qi Phase {chain.get('english', '')}: {chain.get('base_meaning', '')}")

        elif chain_type == "storage":
            if chain.get("is_wealth_storage"):
                parts.append(chain.get("wealth_meaning", ""))
            parts.append(chain.get("opener_meaning", ""))

    return " | ".join(parts)


def _element_zh(element: str) -> str:
    """Convert element to Chinese."""
    mapping = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}
    return mapping.get(element, element)


def _traits_zh(traits: List[str]) -> str:
    """Convert trait list to Chinese."""
    trait_map = {
        "perfectionist": "完美主义",
        "overthinking": "过度思虑",
        "picky": "挑剔",
        "slow to act": "行动迟缓",
        "hard to settle": "难以安定",
        "dependent": "依赖",
        "passive": "被动",
        "lazy": "懒惰",
        "expects help": "期待他人帮助",
        "stubborn": "固执",
        "competitive": "争强好胜",
        "jealous": "嫉妒",
        "selfish": "自私",
        "materialistic": "物质主义",
        "greedy": "贪婪",
        "workaholic": "工作狂",
        "neglects relationships": "忽视感情",
        "stressed": "压力大",
        "pressured": "被迫",
        "controlled": "被控制",
        "authority conflicts": "权威冲突",
    }
    return "、".join(trait_map.get(t, t) for t in traits)


# =============================================================================
# INTEGRATION WITH CLASH ANALYSIS
# =============================================================================

def enrich_clash_with_chain_analysis(
    clash_narrative: Dict[str, Any],
    nodes_data: Dict[str, Any],
    daymaster_element: str,
    element_context: Dict[str, Any],
    shen_sha_by_node: Dict[str, List[str]],
    locale: str = "en"
) -> Dict[str, Any]:
    """
    Enrich a clash narrative with full chain analysis for each branch involved.

    Args:
        clash_narrative: The basic clash narrative
        nodes_data: Full node data from API
        daymaster_element: e.g., "Fire"
        element_context: Element balance context
        shen_sha_by_node: Dict mapping node_id to list of Shen Sha present
        locale: "en" or "zh"

    Returns:
        Enriched narrative with chain analysis for each branch
    """
    from .qi_phase import get_qi_phase_for_stem

    enriched = dict(clash_narrative)

    nodes = clash_narrative.get("nodes", [])
    element_percentages = element_context.get("element_percentages", {})
    ten_god_context = element_context.get("ten_god_context", {})

    # Get daymaster stem from nodes_data for Qi Phase calculation
    daymaster_stem = ""
    hs_d_data = nodes_data.get("hs_d", {})
    if hs_d_data:
        daymaster_stem = hs_d_data.get("id", "")

    branch_analyses = []

    for node_id in nodes:
        # Get node data
        node_data = nodes_data.get(node_id, {})
        branch = node_data.get("id", "")

        if not branch:
            continue

        # Get branch element
        from .localization import BRANCH_NAMES
        branch_info = BRANCH_NAMES.get(branch, {})
        element = branch_info.get("element", "")

        # Determine pillar type
        pillar_type = "unknown"
        if "_d" in node_id:
            pillar_type = "day"
        elif "_h" in node_id:
            pillar_type = "hour"
        elif "_m" in node_id:
            pillar_type = "month"
        elif "_y" in node_id:
            pillar_type = "year"

        # Get favorability
        favorable_elements = element_context.get("favorable_elements", [])
        is_favorable = element in favorable_elements

        # Get Ten God
        ten_god_info = ten_god_context.get(element, {})
        ten_god = ten_god_info.get("ten_god", "")

        # Get Shen Sha for this node
        shen_sha_list = shen_sha_by_node.get(node_id, [])

        # Calculate Qi Phase for daymaster in this branch
        # This tells us the "life phase" of the daymaster's energy in this position
        qi_phase = ""
        if daymaster_stem and branch:
            qi_phase_info = get_qi_phase_for_stem(daymaster_stem, branch)
            qi_phase = qi_phase_info.get("phase", "")

        # Get clash partner
        other_nodes = [n for n in nodes if n != node_id]
        clash_with = ""
        if other_nodes:
            other_data = nodes_data.get(other_nodes[0], {})
            clash_with = other_data.get("id", "")

        # Run chain analysis
        chain_analysis = analyze_node_chain(
            branch=branch,
            element=element,
            is_favorable=is_favorable,
            ten_god=ten_god,
            shen_sha_list=shen_sha_list,
            qi_phase=qi_phase,
            pillar_type=pillar_type,
            daymaster_element=daymaster_element,
            element_percentages=element_percentages,
            has_clash=True,
            clash_with=clash_with,
            locale=locale
        )

        branch_analyses.append({
            "node_id": node_id,
            "branch": branch,
            "pillar_type": pillar_type,
            "analysis": chain_analysis,
        })

    enriched["branch_chain_analyses"] = branch_analyses

    # Build master narrative combining all chains
    master_parts = []
    for ba in branch_analyses:
        analysis = ba["analysis"]
        master_parts.append(f"[{ba['branch']} ({ba['pillar_type'].upper()})] {analysis['combined_narrative']}")

    enriched["master_chain_narrative"] = " ⟷ ".join(master_parts)

    return enriched
