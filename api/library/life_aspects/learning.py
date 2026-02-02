# * =========================
# * LIFE ASPECTS - LEARNING MODULE
# * =========================
# Education and skill development analysis based on BaZi.
#
# Analyzes:
# 1. Resource Ten Gods (DR, IR) - ability to learn
# 2. Output Ten Gods (EG, HO) - ability to express/apply knowledge
# 3. Day Master capacity - strength to absorb learning
# 4. Pillar position context (formal education vs self-taught vs mentoring)

from typing import Dict, List, Optional

# Import base utilities
from .base import (
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    TEN_GOD_ASPECT_MAPPING,
    ELEMENT_GENERATES,
    STEM_TO_ELEMENT,
    stems_to_element_totals,
    get_node_relationship_context,
    # Centralized translations
    ELEMENT_NAMES,
    SEASONAL_STATES,
    OUTLOOK_LABELS,
    get_element_name,
    get_seasonal_state,
)

# * -------------------------
# * LEARNING TEN GODS
# * -------------------------

LEARNING_TEN_GODS = {
    # Resource stars (generates Day Master)
    "DR": {
        "chinese": "正印",
        "type": "formal_learning",
        "description": "Formal education, traditional knowledge, mentorship, certifications",
        "description_chinese": "正規教育、傳統知識、師承、證書",
        "represents": "Traditional teachers, formal institutions, structured learning",
    },
    "IR": {
        "chinese": "偏印",
        "type": "unconventional_learning",
        "description": "Self-taught skills, intuition, unconventional methods, lateral thinking",
        "description_chinese": "自學技能、直覺、非傳統方法",
        "represents": "Self-learning, unique perspectives, alternative knowledge",
    },
    # Output stars (Day Master generates)
    "EG": {
        "chinese": "食神",
        "type": "gentle_expression",
        "description": "Teaching others, creative output, gentle communication",
        "description_chinese": "教導他人、創意輸出、溫和表達",
        "represents": "Ability to share knowledge, artistic expression",
    },
    "HO": {
        "chinese": "傷官",
        "type": "innovative_expression",
        "description": "Innovation, challenging norms, rebellious creativity, disruption",
        "description_chinese": "創新、挑戰常規、顛覆性創意",
        "represents": "Revolutionary ideas, breaking conventions, strong opinions",
    },
}

# * -------------------------
# * LEARNING INDICATORS BY PILLAR
# * -------------------------

LEARNING_INDICATORS = {
    "year": {
        "positive": "Strong educational foundation, family values learning",
        "positive_chinese": "良好教育基礎、家族重視學習",
        "negative": "Disrupted early education, family learning obstacles",
        "negative_chinese": "早年教育中斷、家庭學習障礙",
    },
    "month": {
        "positive": "Formal education success, professional skill development",
        "positive_chinese": "正規教育順利、專業技能發展",
        "negative": "Academic challenges, professional training difficulties",
        "negative_chinese": "學業挑戰、專業培訓困難",
    },
    "day": {
        "positive": "Strong self-learning ability, spouse supports learning",
        "positive_chinese": "自學能力強、配偶支持學習",
        "negative": "Self-doubt in learning, spouse indifferent to education",
        "negative_chinese": "學習自我懷疑、配偶不重視教育",
    },
    "hour": {
        "positive": "Lifelong learner, mentors others, wise in later years",
        "positive_chinese": "終身學習者、指導後輩、晚年智慧",
        "negative": "Late-life learning difficulties, children don't value education",
        "negative_chinese": "晚年學習困難、子女不重視教育",
    },
    # Luck pillars
    "10yr_luck": {
        "positive": "Decade of learning breakthroughs",
        "positive_chinese": "十年學習突破期",
        "negative": "Decade of learning stagnation",
        "negative_chinese": "十年學習停滯期",
    },
    "annual": {
        "positive": "Year favorable for learning new skills",
        "positive_chinese": "年度適合學習新技能",
        "negative": "Year of learning challenges",
        "negative_chinese": "年度學習挑戰",
    },
    "monthly": {
        "positive": "Month favorable for study and training",
        "positive_chinese": "月度適合學習培訓",
        "negative": "Month difficult for concentration",
        "negative_chinese": "月度難以集中精力",
    },
}

# * -------------------------
# * RESOURCE ELEMENT BY DAYMASTER
# * -------------------------
# Element that generates Day Master = Resource

DM_RESOURCE_ELEMENT = {
    "Wood": "Water",   # Water generates Wood
    "Fire": "Wood",    # Wood generates Fire
    "Earth": "Fire",   # Fire generates Earth
    "Metal": "Earth",  # Earth generates Metal
    "Water": "Metal",  # Metal generates Water
}

# Output element (what Day Master generates)
DM_OUTPUT_ELEMENT = {
    "Wood": "Fire",    # Wood generates Fire
    "Fire": "Earth",   # Fire generates Earth
    "Earth": "Metal",  # Earth generates Metal
    "Metal": "Water",  # Metal generates Water
    "Water": "Wood",   # Water generates Wood
}

# * -------------------------
# * MAIN ANALYSIS FUNCTION
# * -------------------------

def generate_learning_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    natal_element_score: Dict[str, float],
    seasonal_states: Dict[str, str],
    daymaster_element: str,
    daymaster_strength: str,
    support_percentage: float = 50.0
) -> dict:
    """
    Analyze chart for learning opportunities and blocks.

    Good learning period indicators:
    - DR/IR present in luck pillars (resource element strong)
    - Resource element in Prosperous/Strengthening state
    - Day Master has capacity to absorb (not too weak)
    - Output channels open (EG/HO not blocked)

    Bad learning period indicators:
    - Resource element weak or Dead
    - Resource under heavy conflict
    - Day Master too weak (< 20% support) - can't focus
    - Output channels blocked (EG/HO damaged)

    Args:
        interactions: All chart interactions
        post_element_score: 10-stem scores after interactions
        natal_element_score: 10-stem scores natal only
        seasonal_states: Element seasonal states
        daymaster_element: Day Master's element
        daymaster_strength: "Strong", "Balanced", "Weak", etc.
        support_percentage: Day Master support % from daymaster_analysis

    Returns:
        Dict with learning analysis results
    """
    # Get resource and output elements for this Day Master
    resource_element = DM_RESOURCE_ELEMENT.get(daymaster_element, "")
    output_element = DM_OUTPUT_ELEMENT.get(daymaster_element, "")

    # Convert to element totals
    post_totals = stems_to_element_totals(post_element_score)
    natal_totals = stems_to_element_totals(natal_element_score)

    # Get resource element scores
    resource_score_post = post_totals.get(resource_element, 0)
    resource_score_natal = natal_totals.get(resource_element, 0)
    resource_change = resource_score_post - resource_score_natal

    # Get output element scores
    output_score_post = post_totals.get(output_element, 0)
    output_score_natal = natal_totals.get(output_element, 0)
    output_change = output_score_post - output_score_natal

    # Get seasonal states
    resource_seasonal = seasonal_states.get(resource_element, "Resting")
    output_seasonal = seasonal_states.get(output_element, "Resting")

    # Determine learning opportunities and blocks
    opportunities = []
    blocks = []

    # Get element names in all languages for interpolation
    resource_en = get_element_name(resource_element, 'en')
    resource_zh = get_element_name(resource_element, 'zh')
    resource_id = get_element_name(resource_element, 'id')

    # Check resource element strength
    if resource_change > 30:
        opportunities.append({
            "type": "resource_increase",
            "description": f"Resource element ({resource_en}) strengthened - learning capacity enhanced",
            "description_chinese": f"印星元素（{resource_zh}）增強 - 學習能力提升",
            "description_id": f"Elemen sumber ({resource_id}) menguat - kapasitas belajar meningkat",
            "impact": "positive",
        })
    elif resource_change < -20:
        blocks.append({
            "type": "resource_decrease",
            "description": f"Resource element ({resource_en}) weakened - learning may be challenging",
            "description_chinese": f"印星元素（{resource_zh}）減弱 - 學習可能有挑戰",
            "description_id": f"Elemen sumber ({resource_id}) melemah - belajar mungkin lebih menantang",
            "impact": "negative",
        })

    # Check resource seasonal state
    resource_seasonal_zh = get_seasonal_state(resource_seasonal, 'zh')
    resource_seasonal_id = get_seasonal_state(resource_seasonal, 'id')

    if resource_seasonal in ["Prosperous", "Strengthening"]:
        opportunities.append({
            "type": "resource_seasonal_favorable",
            "description": f"Resource element in {resource_seasonal} state - knowledge absorption enhanced",
            "description_chinese": f"印星處於{resource_seasonal_zh}狀態 - 知識吸收增強",
            "description_id": f"Elemen sumber dalam kondisi {resource_seasonal_id} - penyerapan pengetahuan meningkat",
            "impact": "positive",
        })
    elif resource_seasonal in ["Dead", "Trapped"]:
        blocks.append({
            "type": "resource_seasonal_unfavorable",
            "description": f"Resource element in {resource_seasonal} state - learning requires more effort",
            "description_chinese": f"印星處於{resource_seasonal_zh}狀態 - 學習需要更多努力",
            "description_id": f"Elemen sumber dalam kondisi {resource_seasonal_id} - belajar memerlukan usaha lebih",
            "impact": "negative",
        })

    # Check output channels
    output_seasonal_zh = get_seasonal_state(output_seasonal, 'zh')
    output_seasonal_id = get_seasonal_state(output_seasonal, 'id')

    if output_seasonal in ["Prosperous", "Strengthening"]:
        opportunities.append({
            "type": "output_favorable",
            "description": "Expression channels open - good for teaching and applying knowledge",
            "description_chinese": "表達管道暢通 - 適合教學和應用知識",
            "description_id": "Saluran ekspresi terbuka - baik untuk mengajar dan menerapkan pengetahuan",
            "impact": "positive",
        })
    elif output_seasonal == "Dead":
        blocks.append({
            "type": "output_blocked",
            "description": "Expression channels restricted - focus on input over output",
            "description_chinese": "表達管道受限 - 專注吸收而非輸出",
            "description_id": "Saluran ekspresi terbatas - fokus pada menyerap daripada mengekspresikan",
            "impact": "warning",
        })

    # Check Day Master capacity
    dm_can_focus = support_percentage >= 20  # Minimum to focus
    dm_can_absorb = support_percentage <= 70  # Too strong = doesn't need to learn

    if not dm_can_focus:
        blocks.append({
            "type": "weak_daymaster",
            "description": "Day Master support low - may have difficulty concentrating",
            "description_chinese": "日主支持度低 - 可能難以集中注意力",
            "description_id": "Dukungan Day Master rendah - mungkin sulit berkonsentrasi",
            "impact": "negative",
        })

    if support_percentage > 70:
        blocks.append({
            "type": "overly_strong_daymaster",
            "description": "Day Master very strong - may resist new learning",
            "description_chinese": "日主過強 - 可能抗拒新學習",
            "description_id": "Day Master sangat kuat - mungkin menolak pembelajaran baru",
            "impact": "warning",
        })

    # Calculate overall learning outlook
    opportunity_score = len(opportunities) * 20
    block_score = len(blocks) * 15

    if opportunity_score > block_score + 20:
        outlook = "favorable"
        outlook_chinese = "有利"
        outlook_id = "menguntungkan"
        breakthrough_likely = True
    elif block_score > opportunity_score + 20:
        outlook = "challenging"
        outlook_chinese = "挑戰"
        outlook_id = "menantang"
        breakthrough_likely = False
    else:
        outlook = "neutral"
        outlook_chinese = "中性"
        outlook_id = "netral"
        breakthrough_likely = False

    # Helper to get description in specific language
    def get_desc(item, lang="en"):
        if lang == "zh":
            return item.get("description_chinese", item.get("description", ""))
        elif lang == "id":
            return item.get("description_id", item.get("description", ""))
        return item.get("description", "")

    # Generate multilingual analysis text
    if opportunities and not blocks:
        analysis_text = f"Favorable period for learning and skill development. {get_desc(opportunities[0], 'en')}."
        analysis_text_chinese = f"學習和技能發展的有利時期。{get_desc(opportunities[0], 'zh')}。"
        analysis_text_id = f"Periode yang menguntungkan untuk belajar dan pengembangan keterampilan. {get_desc(opportunities[0], 'id')}."
    elif blocks and not opportunities:
        analysis_text = f"Learning may require extra effort this period. {get_desc(blocks[0], 'en')}."
        analysis_text_chinese = f"此期間學習可能需要額外努力。{get_desc(blocks[0], 'zh')}。"
        analysis_text_id = f"Belajar mungkin memerlukan usaha ekstra pada periode ini. {get_desc(blocks[0], 'id')}."
    elif opportunities and blocks:
        analysis_text = f"Mixed signals for learning. {get_desc(opportunities[0], 'en')}, but {get_desc(blocks[0], 'en').lower()}."
        analysis_text_chinese = f"學習信號參半。{get_desc(opportunities[0], 'zh')}，但{get_desc(blocks[0], 'zh')}。"
        analysis_text_id = f"Sinyal pembelajaran campuran. {get_desc(opportunities[0], 'id')}, tetapi {get_desc(blocks[0], 'id').lower()}."
    else:
        analysis_text = "Neutral learning period with steady progress possible."
        analysis_text_chinese = "中性學習期，可能穩定進展。"
        analysis_text_id = "Periode pembelajaran netral dengan kemungkinan kemajuan yang stabil."

    return {
        "resource_element": resource_element,
        "resource_element_chinese": get_element_name(resource_element, 'zh'),
        "resource_element_id": get_element_name(resource_element, 'id'),
        "output_element": output_element,
        "output_element_chinese": get_element_name(output_element, 'zh'),
        "output_element_id": get_element_name(output_element, 'id'),
        "resource_score": round(resource_score_post, 1),
        "resource_change": round(resource_change, 1),
        "resource_seasonal_state": resource_seasonal,
        "output_score": round(output_score_post, 1),
        "output_change": round(output_change, 1),
        "output_seasonal_state": output_seasonal,
        "daymaster_can_focus": dm_can_focus,
        "daymaster_can_absorb": dm_can_absorb,
        "opportunities": opportunities,
        "blocks": blocks,
        "outlook": outlook,
        "outlook_chinese": outlook_chinese,
        "outlook_id": outlook_id,
        "breakthrough_likely": breakthrough_likely,
        # Multilingual analysis text
        "analysis_text": analysis_text,
        "analysis_text_chinese": analysis_text_chinese,
        "analysis_text_id": analysis_text_id,
    }
