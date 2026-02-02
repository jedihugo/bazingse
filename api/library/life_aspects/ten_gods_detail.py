# * =========================
# * LIFE ASPECTS - TEN GODS DETAIL MODULE
# * =========================
# Detailed Ten Gods analysis with pillar position context.
#
# Provides:
# 1. Ten God identification for each node
# 2. Pillar position meaning (relationship, life period)
# 3. Conflict/combination impact on each Ten God
# 4. Life aspect implications

from typing import Dict, List, Optional, Any

# Import base utilities
from .base import (
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    TEN_GOD_ASPECT_MAPPING,
    ELEMENT_CONTROLS,
    ELEMENT_GENERATES,
    STEM_TO_ELEMENT,
    get_node_relationship_context,
)

# Import from parent library
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import STEMS, BRANCHES

# * -------------------------
# * TEN GOD CALCULATION
# * -------------------------

def get_ten_god_for_stem(day_master_stem: str, target_stem: str) -> Dict:
    """
    Calculate Ten God relationship between Day Master and target stem.

    Args:
        day_master_stem: The Day Master's stem (e.g., "Ding")
        target_stem: The target stem to evaluate (e.g., "Bing")

    Returns:
        Dict with ten_god info: id, chinese, english, aspect, meaning
    """
    unknown_result = {"id": "?", "chinese": "?", "english": "Unknown", "aspect": "", "sub_aspect": ""}

    if not day_master_stem or not target_stem:
        return unknown_result

    dm_info = STEMS.get(day_master_stem, {})
    target_info = STEMS.get(target_stem, {})

    if not dm_info or not target_info:
        return unknown_result

    dm_element = dm_info.get("element", "")
    dm_polarity = dm_info.get("polarity", "")
    target_element = target_info.get("element", "")
    target_polarity = target_info.get("polarity", "")

    same_polarity = (dm_polarity == target_polarity)

    # Determine Ten God based on element relationship
    if dm_element == target_element:
        # Same element
        if same_polarity:
            ten_god = {"id": "F", "chinese": "比肩", "english": "Friend"}
        else:
            ten_god = {"id": "RW", "chinese": "劫財", "english": "Rob Wealth"}

    elif ELEMENT_GENERATES.get(dm_element) == target_element:
        # DM generates target (Output)
        if same_polarity:
            ten_god = {"id": "EG", "chinese": "食神", "english": "Eating God"}
        else:
            ten_god = {"id": "HO", "chinese": "傷官", "english": "Hurting Officer"}

    elif ELEMENT_CONTROLS.get(dm_element) == target_element:
        # DM controls target (Wealth)
        if same_polarity:
            ten_god = {"id": "IW", "chinese": "偏財", "english": "Indirect Wealth"}
        else:
            ten_god = {"id": "DW", "chinese": "正財", "english": "Direct Wealth"}

    elif ELEMENT_CONTROLS.get(target_element) == dm_element:
        # Target controls DM (Officer/Killer)
        if same_polarity:
            ten_god = {"id": "7K", "chinese": "七殺", "english": "Seven Killings"}
        else:
            ten_god = {"id": "DO", "chinese": "正官", "english": "Direct Officer"}

    elif ELEMENT_GENERATES.get(target_element) == dm_element:
        # Target generates DM (Resource)
        if same_polarity:
            ten_god = {"id": "IR", "chinese": "偏印", "english": "Indirect Resource"}
        else:
            ten_god = {"id": "DR", "chinese": "正印", "english": "Direct Resource"}

    else:
        return unknown_result

    # Add aspect mapping
    aspect_info = TEN_GOD_ASPECT_MAPPING.get(ten_god["id"], {})
    ten_god["aspect"] = aspect_info.get("aspect", "")
    ten_god["sub_aspect"] = aspect_info.get("sub_aspect", "")

    return ten_god


# * -------------------------
# * TEN GOD IN PILLAR MEANINGS
# * -------------------------

TEN_GOD_PILLAR_MEANINGS = {
    # Wealth Stars (財星)
    "DW": {
        "year": {
            "meaning": "Ancestral wealth, family financial foundation",
            "meaning_chinese": "祖業財富、家族經濟基礎",
            "positive": "Born into prosperity",
            "negative": "Family financial burden inherited",
        },
        "month": {
            "meaning": "Career income, salary, professional earnings",
            "meaning_chinese": "事業收入、薪資、專業收益",
            "positive": "Stable career income",
            "negative": "Work income unstable",
        },
        "day": {
            "meaning": "Spouse's wealth, marriage finances",
            "meaning_chinese": "配偶財富、婚姻財務",
            "positive": "Spouse brings wealth",
            "negative": "Spouse financial issues",
        },
        "hour": {
            "meaning": "Late-life wealth, children's support",
            "meaning_chinese": "晚年財富、子女供養",
            "positive": "Comfortable retirement",
            "negative": "Late-life financial worry",
        },
    },
    "IW": {
        "year": {
            "meaning": "Unexpected ancestral gains, inheritance",
            "meaning_chinese": "意外祖產、遺產",
            "positive": "Windfall from ancestry",
            "negative": "Unstable family wealth",
        },
        "month": {
            "meaning": "Business income, investment returns",
            "meaning_chinese": "生意收入、投資回報",
            "positive": "Good business luck",
            "negative": "Business risks",
        },
        "day": {
            "meaning": "Spouse's business, side income through partner",
            "meaning_chinese": "配偶生意、通過伴侶的副業",
            "positive": "Partner brings opportunities",
            "negative": "Partner's risky ventures",
        },
        "hour": {
            "meaning": "Children's business success, late-life investments",
            "meaning_chinese": "子女事業成功、晚年投資",
            "positive": "Children prosper",
            "negative": "Children's financial burden",
        },
    },
    # Resource Stars (印星)
    "DR": {
        "year": {
            "meaning": "Family education values, ancestral wisdom",
            "meaning_chinese": "家族教育觀念、祖傳智慧",
            "positive": "Strong educational foundation",
            "negative": "Limited early education",
        },
        "month": {
            "meaning": "Formal education, professional training",
            "meaning_chinese": "正規教育、專業培訓",
            "positive": "Academic achievement",
            "negative": "Educational struggles",
        },
        "day": {
            "meaning": "Self-development, spouse's wisdom",
            "meaning_chinese": "自我提升、配偶智慧",
            "positive": "Continuous self-improvement",
            "negative": "Learning obstacles",
        },
        "hour": {
            "meaning": "Mentoring others, late-life wisdom",
            "meaning_chinese": "指導他人、晚年智慧",
            "positive": "Respected teacher/mentor",
            "negative": "Knowledge not passed on",
        },
    },
    "IR": {
        "year": {
            "meaning": "Unconventional family knowledge, unique upbringing",
            "meaning_chinese": "非傳統家庭知識、獨特成長環境",
            "positive": "Creative family influence",
            "negative": "Disrupted early learning",
        },
        "month": {
            "meaning": "Self-taught skills, alternative methods",
            "meaning_chinese": "自學技能、另類方法",
            "positive": "Innovative learning style",
            "negative": "Difficulty with formal systems",
        },
        "day": {
            "meaning": "Intuitive knowledge, spouse's unique skills",
            "meaning_chinese": "直覺知識、配偶獨特技能",
            "positive": "Strong intuition",
            "negative": "Overthinking, anxiety",
        },
        "hour": {
            "meaning": "Unconventional wisdom, children's creativity",
            "meaning_chinese": "非傳統智慧、子女創造力",
            "positive": "Creative legacy",
            "negative": "Ideas not understood",
        },
    },
    # Output Stars (食傷)
    "EG": {
        "year": {
            "meaning": "Family creativity, ancestral talents",
            "meaning_chinese": "家族創意、祖傳才華",
            "positive": "Inherited talents",
            "negative": "Suppressed creativity early",
        },
        "month": {
            "meaning": "Professional creativity, work expression",
            "meaning_chinese": "專業創意、工作表達",
            "positive": "Creative career success",
            "negative": "Creativity not valued at work",
        },
        "day": {
            "meaning": "Personal expression, spouse supports creativity",
            "meaning_chinese": "個人表達、配偶支持創意",
            "positive": "Free self-expression",
            "negative": "Spouse stifles creativity",
        },
        "hour": {
            "meaning": "Teaching children, late-life creativity",
            "meaning_chinese": "教導子女、晚年創作",
            "positive": "Creative legacy to children",
            "negative": "Ideas not passed on",
        },
    },
    "HO": {
        "year": {
            "meaning": "Family rebellion, breaking ancestral norms",
            "meaning_chinese": "家族叛逆、打破祖傳規範",
            "positive": "Family innovator",
            "negative": "Conflict with traditions",
        },
        "month": {
            "meaning": "Career disruption, challenging authority",
            "meaning_chinese": "事業顛覆、挑戰權威",
            "positive": "Industry disruptor",
            "negative": "Trouble with superiors",
        },
        "day": {
            "meaning": "Personal rebellion, spouse conflicts",
            "meaning_chinese": "個人叛逆、配偶衝突",
            "positive": "Strong individuality",
            "negative": "Marriage conflicts",
        },
        "hour": {
            "meaning": "Children's rebellion, unconventional legacy",
            "meaning_chinese": "子女叛逆、非傳統遺產",
            "positive": "Innovative children",
            "negative": "Children rebel against you",
        },
    },
    # Officer Stars (官殺)
    "DO": {
        "year": {
            "meaning": "Family status, ancestral reputation",
            "meaning_chinese": "家族地位、祖傳聲望",
            "positive": "Noble family background",
            "negative": "Family status pressure",
        },
        "month": {
            "meaning": "Career authority, professional status",
            "meaning_chinese": "事業權威、專業地位",
            "positive": "High career position",
            "negative": "Work pressure, demanding job",
        },
        "day": {
            "meaning": "Personal authority, spouse's status (for women: husband)",
            "meaning_chinese": "個人權威、配偶地位（女命代表丈夫）",
            "positive": "Respected position",
            "negative": "Controlled by others",
        },
        "hour": {
            "meaning": "Children's achievements, late-life status",
            "meaning_chinese": "子女成就、晚年地位",
            "positive": "Children achieve status",
            "negative": "Children pressure you",
        },
    },
    "7K": {
        "year": {
            "meaning": "Family pressure, ancestral challenges",
            "meaning_chinese": "家族壓力、祖傳挑戰",
            "positive": "Overcame family hardship",
            "negative": "Harsh early environment",
        },
        "month": {
            "meaning": "Career competition, intense work pressure",
            "meaning_chinese": "事業競爭、高強度工作壓力",
            "positive": "Thrives under pressure",
            "negative": "Burnout, work enemies",
        },
        "day": {
            "meaning": "Personal challenges, spouse intensity (for women: difficult husband)",
            "meaning_chinese": "個人挑戰、配偶強勢（女命代表難搞丈夫）",
            "positive": "Strong resilience",
            "negative": "Difficult relationships",
        },
        "hour": {
            "meaning": "Children's challenges, intense late-life",
            "meaning_chinese": "子女挑戰、晚年高壓",
            "positive": "Children are fighters",
            "negative": "Children bring pressure",
        },
    },
    # Companion Stars (比劫)
    "F": {
        "year": {
            "meaning": "Siblings, family peers",
            "meaning_chinese": "兄弟姐妹、家族同輩",
            "positive": "Supportive siblings",
            "negative": "Sibling competition for resources",
        },
        "month": {
            "meaning": "Colleagues, work peers",
            "meaning_chinese": "同事、工作同輩",
            "positive": "Good teamwork",
            "negative": "Workplace competition",
        },
        "day": {
            "meaning": "Self-reliance, spouse is peer-like",
            "meaning_chinese": "自立、配偶像朋友",
            "positive": "Independent, equal partnership",
            "negative": "Too independent, distant",
        },
        "hour": {
            "meaning": "Children as peers, late-life friends",
            "meaning_chinese": "子女如朋友、晚年友誼",
            "positive": "Friend-like with children",
            "negative": "Children don't respect authority",
        },
    },
    "RW": {
        "year": {
            "meaning": "Competing siblings, family resource drain",
            "meaning_chinese": "競爭的兄弟姐妹、家族資源流失",
            "positive": "Learned to compete early",
            "negative": "Lost inheritance to siblings",
        },
        "month": {
            "meaning": "Work rivals, competitive colleagues",
            "meaning_chinese": "工作對手、競爭同事",
            "positive": "Motivated by competition",
            "negative": "Colleagues steal credit",
        },
        "day": {
            "meaning": "Self-competition, spouse competes with you",
            "meaning_chinese": "自我競爭、配偶與你競爭",
            "positive": "Drives self-improvement",
            "negative": "Spouse drains resources",
        },
        "hour": {
            "meaning": "Children compete for resources, late-life drain",
            "meaning_chinese": "子女競爭資源、晚年消耗",
            "positive": "Children are ambitious",
            "negative": "Children drain your wealth",
        },
    },
}


# * -------------------------
# * CONFLICT IMPACT ON TEN GODS
# * -------------------------

def analyze_interaction_impact(
    ten_god_id: str,
    interaction_type: str,
    pillar: str
) -> Dict:
    """
    Analyze the impact of an interaction on a Ten God in a specific pillar.

    Returns dict with impact assessment.
    """
    # Interaction type impacts
    negative_types = ["CLASH", "PUNISHMENT", "HARM", "DESTRUCTION", "STEM_CONFLICT"]
    positive_types = ["THREE_MEETINGS", "THREE_COMBINATIONS", "SIX_HARMONIES", "STEM_COMBINATION"]

    is_negative = any(neg in interaction_type for neg in negative_types)
    is_positive = any(pos in interaction_type for pos in positive_types)

    pillar_meanings = TEN_GOD_PILLAR_MEANINGS.get(ten_god_id, {}).get(pillar, {})

    if is_negative:
        return {
            "impact_type": "negative",
            "impact_chinese": "負面",
            "interpretation": pillar_meanings.get("negative", f"{ten_god_id} under stress"),
            "severity": "warning" if "CLASH" in interaction_type or "PUNISHMENT" in interaction_type else "caution",
        }
    elif is_positive:
        return {
            "impact_type": "positive",
            "impact_chinese": "正面",
            "interpretation": pillar_meanings.get("positive", f"{ten_god_id} enhanced"),
            "severity": "favorable",
        }
    else:
        return {
            "impact_type": "neutral",
            "impact_chinese": "中性",
            "interpretation": pillar_meanings.get("meaning", f"{ten_god_id} present"),
            "severity": "neutral",
        }


# * -------------------------
# * INDONESIAN TRANSLATIONS
# * -------------------------

# Mapping for common BaZi pillar meanings to Indonesian
MEANING_TRANSLATIONS_ID = {
    # Wealth
    "Ancestral wealth, family financial foundation": "Kekayaan leluhur, fondasi keuangan keluarga",
    "Career income, salary, professional earnings": "Pendapatan karier, gaji, penghasilan profesional",
    "Spouse's wealth, marriage finances": "Kekayaan pasangan, keuangan pernikahan",
    "Late-life wealth, children's support": "Kekayaan masa tua, dukungan anak",
    "Unexpected ancestral gains, inheritance": "Keuntungan leluhur tak terduga, warisan",
    "Business income, investment returns": "Pendapatan bisnis, hasil investasi",
    "Spouse's business, side income through partner": "Bisnis pasangan, pendapatan tambahan melalui partner",
    "Children's business success, late-life investments": "Kesuksesan bisnis anak, investasi masa tua",
    # Resource
    "Family education values, ancestral wisdom": "Nilai pendidikan keluarga, kebijaksanaan leluhur",
    "Formal education, professional training": "Pendidikan formal, pelatihan profesional",
    "Self-development, spouse's wisdom": "Pengembangan diri, kebijaksanaan pasangan",
    "Mentoring others, late-life wisdom": "Membimbing orang lain, kebijaksanaan masa tua",
    "Unconventional family knowledge, unique upbringing": "Pengetahuan keluarga non-konvensional, didikan unik",
    "Self-taught skills, alternative methods": "Keterampilan otodidak, metode alternatif",
    "Intuitive knowledge, spouse's unique skills": "Pengetahuan intuitif, keterampilan unik pasangan",
    "Unconventional wisdom, children's creativity": "Kebijaksanaan non-konvensional, kreativitas anak",
    # Output
    "Family creativity, ancestral talents": "Kreativitas keluarga, bakat leluhur",
    "Professional creativity, work expression": "Kreativitas profesional, ekspresi kerja",
    "Personal expression, spouse supports creativity": "Ekspresi pribadi, pasangan mendukung kreativitas",
    "Teaching children, late-life creativity": "Mengajar anak, kreativitas masa tua",
    "Family rebellion, breaking ancestral norms": "Pemberontakan keluarga, melanggar norma leluhur",
    "Career disruption, challenging authority": "Gangguan karier, menantang otoritas",
    "Personal rebellion, spouse conflicts": "Pemberontakan pribadi, konflik dengan pasangan",
    "Children's rebellion, unconventional legacy": "Pemberontakan anak, warisan non-konvensional",
    # Officer
    "Family status, ancestral reputation": "Status keluarga, reputasi leluhur",
    "Career authority, professional status": "Otoritas karier, status profesional",
    "Personal authority, spouse's status (for women: husband)": "Otoritas pribadi, status pasangan (untuk wanita: suami)",
    "Children's achievements, late-life status": "Pencapaian anak, status masa tua",
    "Family pressure, ancestral challenges": "Tekanan keluarga, tantangan leluhur",
    "Career competition, intense work pressure": "Persaingan karier, tekanan kerja tinggi",
    "Personal challenges, spouse intensity (for women: difficult husband)": "Tantangan pribadi, intensitas pasangan (untuk wanita: suami sulit)",
    "Children's challenges, intense late-life": "Tantangan anak, masa tua intens",
    # Companion
    "Siblings, family peers": "Saudara kandung, sepupu keluarga",
    "Colleagues, work peers": "Rekan kerja, teman sejawat",
    "Self-reliance, spouse is peer-like": "Kemandirian, pasangan seperti teman",
    "Children as peers, late-life friends": "Anak seperti teman, sahabat masa tua",
    "Competing siblings, family resource drain": "Persaingan saudara, pengurasan sumber daya keluarga",
    "Work rivals, competitive colleagues": "Saingan kerja, rekan kompetitif",
    "Self-competition, spouse competes with you": "Kompetisi diri, pasangan bersaing dengan Anda",
    "Children compete for resources, late-life drain": "Anak bersaing untuk sumber daya, pengurasan masa tua",
}


def _get_meaning_indonesian(pillar_meaning: Dict, fallback: str) -> str:
    """Get Indonesian translation of pillar meaning."""
    meaning_en = pillar_meaning.get("meaning", fallback) or fallback
    return MEANING_TRANSLATIONS_ID.get(meaning_en, meaning_en)


# * -------------------------
# * MAIN ANALYSIS FUNCTION
# * -------------------------

def generate_ten_gods_detail(
    nodes: Dict[str, Any],
    day_master_stem: str,
    interactions: Dict[str, Any],
) -> Dict:
    """
    Generate detailed Ten Gods analysis for each node.

    Args:
        nodes: Dict of node data from API response
        day_master_stem: The Day Master's stem (e.g., "Ding")
        interactions: All interactions from the chart

    Returns:
        Dict with detailed Ten Gods analysis per node
    """
    analysis = {
        "day_master": day_master_stem,
        "day_master_element": STEMS.get(day_master_stem, {}).get("element", ""),
        "nodes": {},
        "summary": {
            "wealth_nodes": [],
            "resource_nodes": [],
            "output_nodes": [],
            "officer_nodes": [],
            "companion_nodes": [],
        },
        "warnings": [],
        "opportunities": [],
    }

    # Analyze each node
    node_ids = [
        "hs_y", "hs_m", "hs_d", "hs_h",  # Natal stems
        "eb_y", "eb_m", "eb_d", "eb_h",  # Natal branches
        "hs_10yl", "eb_10yl",  # 10-year luck
        "hs_yl", "eb_yl",  # Annual luck
        "hs_ml", "eb_ml",  # Monthly luck
        "hs_dl", "eb_dl",  # Daily luck
        "hs_hl", "eb_hl",  # Hourly luck
    ]

    for node_id in node_ids:
        node_data = nodes.get(node_id)
        if not node_data:
            continue

        # Get node context
        node_context = get_node_relationship_context(node_id)
        pillar = node_context.get("pillar", "")
        represents = node_context.get("represents", "")
        represents_chinese = node_context.get("represents_chinese", "")
        life_domain = node_context.get("life_domain", "")

        # Get stem ID (for HS nodes, it's direct; for EB nodes, use primary qi)
        stem_id = node_data.get("id", "")

        # For EB nodes, get primary qi stem
        is_branch = node_id.startswith("eb_")
        primary_qi_stem = None
        if is_branch and stem_id in BRANCHES:
            # qi is a list of tuples: [(stem, percentage), ...]
            qi_list = BRANCHES[stem_id].get("qi", [])
            if qi_list and len(qi_list) > 0:
                # First item is primary qi - it's a tuple (stem, percentage)
                primary_qi_stem = qi_list[0][0] if isinstance(qi_list[0], tuple) else qi_list[0]

        # Calculate Ten God
        if is_branch:
            ten_god = get_ten_god_for_stem(day_master_stem, primary_qi_stem) if primary_qi_stem else {"id": "?"}
        else:
            ten_god = get_ten_god_for_stem(day_master_stem, stem_id)

        # Get pillar meaning for this Ten God
        pillar_meaning = TEN_GOD_PILLAR_MEANINGS.get(ten_god["id"], {}).get(pillar, {})

        # Analyze interactions affecting this node
        interaction_ids = node_data.get("interaction_ids", [])
        impacts = []
        has_negative = False
        has_positive = False

        for int_id in interaction_ids:
            impact = analyze_interaction_impact(ten_god["id"], int_id, pillar)
            impacts.append({
                "interaction_id": int_id,
                **impact
            })
            if impact["impact_type"] == "negative":
                has_negative = True
            elif impact["impact_type"] == "positive":
                has_positive = True

        # Build node analysis
        node_analysis = {
            "node_id": node_id,
            "stem_or_branch": stem_id,
            "is_branch": is_branch,
            "primary_qi_stem": primary_qi_stem,
            "ten_god": ten_god,
            "pillar": pillar,
            "pillar_chinese": node_context.get("pillar_chinese", ""),
            "represents": represents,
            "represents_chinese": represents_chinese,
            "life_domain": life_domain,
            "pillar_meaning": pillar_meaning,
            "interaction_count": len(interaction_ids),
            "impacts": impacts,
            "has_negative_impact": has_negative,
            "has_positive_impact": has_positive,
            "badges": node_data.get("badges", []),
        }

        analysis["nodes"][node_id] = node_analysis

        # Categorize by aspect
        aspect = ten_god.get("aspect", "")
        if aspect == "wealth":
            analysis["summary"]["wealth_nodes"].append(node_id)
        elif aspect == "learning":
            analysis["summary"]["resource_nodes"].append(node_id)
        elif aspect == "career":
            analysis["summary"]["officer_nodes"].append(node_id)
        elif aspect == "relationships":
            analysis["summary"]["companion_nodes"].append(node_id)

        # Generate warnings for negative impacts on important nodes
        if has_negative and pillar in ["day", "month"] and ten_god.get("id") != "?":
            # Messages should be clean descriptions - frontend adds "{ten_god} @ {pillar}:" prefix
            # English message: describe what aspect is affected
            meaning_en = pillar_meaning.get("meaning", represents) or represents
            warning_text_en = f"{meaning_en} under conflict"
            # Chinese message
            meaning_zh = pillar_meaning.get("meaning_chinese", represents_chinese) or represents_chinese
            warning_text_zh = f"{meaning_zh}受沖"
            # Indonesian message
            meaning_id = _get_meaning_indonesian(pillar_meaning, represents)
            warning_text_id = f"{meaning_id} terkena konflik"

            analysis["warnings"].append({
                "node_id": node_id,
                "ten_god": ten_god.get("id", "?"),
                "ten_god_chinese": ten_god.get("chinese", "?"),
                "ten_god_english": ten_god.get("english", "?"),
                "pillar": pillar,
                "message": warning_text_en,
                "message_chinese": warning_text_zh,
                "message_id": warning_text_id,
            })

        # Generate opportunities for positive impacts
        if has_positive and not has_negative and ten_god.get("id") != "?":
            # Messages should be clean descriptions - frontend adds "{ten_god} @ {pillar}:" prefix
            # English message
            meaning_en = pillar_meaning.get("meaning", represents) or represents
            opp_text_en = f"{meaning_en} strengthened"
            # Chinese message
            meaning_zh = pillar_meaning.get("meaning_chinese", represents_chinese) or represents_chinese
            opp_text_zh = f"{meaning_zh}得助"
            # Indonesian message
            meaning_id = _get_meaning_indonesian(pillar_meaning, represents)
            opp_text_id = f"{meaning_id} diperkuat"

            analysis["opportunities"].append({
                "node_id": node_id,
                "ten_god": ten_god.get("id", "?"),
                "ten_god_chinese": ten_god.get("chinese", "?"),
                "ten_god_english": ten_god.get("english", "?"),
                "pillar": pillar,
                "message": opp_text_en,
                "message_chinese": opp_text_zh,
                "message_id": opp_text_id,
            })

    # Generate multilingual summary text
    summary_texts = _generate_summary_text(analysis)
    analysis["summary_text"] = summary_texts["en"]
    analysis["summary_text_chinese"] = summary_texts["zh"]
    analysis["summary_text_id"] = summary_texts["id"]

    return analysis


def _generate_summary_text(analysis: Dict) -> Dict[str, str]:
    """Generate natural language summary of Ten Gods analysis in all 3 languages.

    Returns:
        Dict with keys 'en', 'zh', 'id' containing summary text in each language.
    """
    warnings = analysis.get("warnings", [])
    opportunities = analysis.get("opportunities", [])

    parts_en = []
    parts_zh = []
    parts_id = []

    if warnings:
        primary_warning = warnings[0]
        parts_en.append(f"Watch {primary_warning.get('message', '')}.")
        parts_zh.append(f"注意：{primary_warning.get('message_chinese', '')}。")
        parts_id.append(f"Perhatikan: {primary_warning.get('message_id', '')}.")

    if opportunities:
        primary_opp = opportunities[0]
        parts_en.append(f"Favorable: {primary_opp.get('message', '')}.")
        parts_zh.append(f"有利：{primary_opp.get('message_chinese', '')}。")
        parts_id.append(f"Menguntungkan: {primary_opp.get('message_id', '')}.")

    if not warnings and not opportunities:
        parts_en.append("Ten Gods configuration is balanced with no significant conflicts.")
        parts_zh.append("十神配置平衡，無明顯衝突。")
        parts_id.append("Konfigurasi Sepuluh Dewa seimbang tanpa konflik signifikan.")

    return {
        "en": " ".join(parts_en[:3]),
        "zh": " ".join(parts_zh[:3]),
        "id": " ".join(parts_id[:3]),
    }
