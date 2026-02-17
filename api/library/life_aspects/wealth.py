# * =========================
# * LIFE ASPECTS - WEALTH MODULE
# * =========================
# Financial opportunity and risk analysis based on BaZi.
#
# Analyzes:
# 1. Wealth Ten Gods (DW, IW) presence and strength
# 2. Wealth storage (財庫) activation status
# 3. Competition elements (RW) threatening wealth
# 4. Pillar position context (inherited vs earned vs late-life wealth)

from typing import Dict, List, Optional

# Import base utilities
from .base import (
    NODE_RELATIONSHIPS,
    PILLAR_LIFE_PERIODS,
    TEN_GOD_ASPECT_MAPPING,
    ELEMENT_CONTROLS,
    STEM_TO_ELEMENT,
    stems_to_element_totals,
    get_node_relationship_context,
)

# * -------------------------
# * OPPORTUNITY & RISK WEIGHTS
# * -------------------------
# Weighted scoring for outlook calculation (replaces simple count-based scoring)

OPPORTUNITY_WEIGHTS = {
    "storage_maximum": 40,      # Storage at maximum = exceptional
    "storage_activated": 25,    # Storage activated (filled OR opened)
    "property_indicator": 35,   # Earth storages = property timing
    "wealth_increase": 20,      # Significant wealth increase
    "seasonal_favorable": 15,   # Prosperous/Strengthening state
}

RISK_WEIGHTS = {
    "weak_daymaster": 25,       # DM too weak to hold wealth
    "wealth_decrease": 20,      # Wealth element weakened
    "seasonal_unfavorable": 15, # Dead/Trapped state
}

# * -------------------------
# * PROPERTY INDICATORS
# * -------------------------
# All storage branches (Chen, Chou, Wei, Xu) are Earth branches.
# In BaZi, Earth = property/land. Storage activation = property timing signal.

PROPERTY_STORAGE_BRANCHES = ["Chen", "Chou", "Wei", "Xu"]

PROPERTY_INDICATORS = {
    "year": {"positive": "Ancestral land, inherited property", "positive_id": "Tanah warisan"},
    "month": {"positive": "Career-related property", "positive_id": "Properti karier"},
    "day": {"positive": "Marital home, joint property", "positive_id": "Rumah tangga"},
    "hour": {"positive": "Late-life property", "positive_id": "Properti masa tua"},
    "10yr_luck": {"positive": "Decade favorable for property", "positive_id": "Dekade baik untuk properti"},
    "annual": {"positive": "Year favorable for property", "positive_id": "Tahun baik untuk properti"},
    "monthly": {"positive": "Month favorable for property (60-120 day window)", "positive_id": "Bulan baik untuk properti"},
}

# * -------------------------
# * WEALTH TEN GODS
# * -------------------------

WEALTH_TEN_GODS = {
    "DW": {
        "chinese": "正財",
        "type": "earned",
        "description": "Steady income, salary, earned wealth",
        "description_chinese": "穩定收入、薪資、正當財富",
        "favorable_when": "Day Master strong enough to handle responsibility",
    },
    "IW": {
        "chinese": "偏財",
        "type": "windfall",
        "description": "Investments, windfall, unexpected gains, business income",
        "description_chinese": "投資、意外之財、生意收入",
        "favorable_when": "Day Master strong and can manage risk",
    },
    "RW": {
        "chinese": "劫財",
        "type": "competitor",
        "description": "Competition for resources, potential loss",
        "description_chinese": "競爭、破財風險",
        "favorable_when": "Never - this is a wealth drain",
    },
}

# * -------------------------
# * WEALTH INDICATORS BY PILLAR
# * -------------------------
# Same wealth element in different pillars has different meanings

WEALTH_INDICATORS = {
    "year": {
        "positive": "Inherited wealth, family fortune, ancestral blessings",
        "positive_chinese": "祖業、家族財富",
        "negative": "Family financial burden, ancestral debt",
        "negative_chinese": "祖上債務、家族負擔",
    },
    "month": {
        "positive": "Career income, salary, professional earnings",
        "positive_chinese": "事業收入、薪資",
        "negative": "Career financial instability, job-related losses",
        "negative_chinese": "事業財務不穩、工作損失",
    },
    "day": {
        "positive": "Personal wealth, savings, material assets",
        "positive_chinese": "個人財富、儲蓄、物質資產",
        "negative": "Personal financial drain, asset losses",
        "negative_chinese": "個人財務消耗、資產損失",
    },
    "hour": {
        "positive": "Late-life wealth, children's support, retirement security",
        "positive_chinese": "晚年財富、子女供養",
        "negative": "Late-life financial worries, children's financial burden",
        "negative_chinese": "晚年財務憂慮、子女負擔",
    },
    # Luck pillars
    "10yr_luck": {
        "positive": "Decade of financial opportunity",
        "positive_chinese": "十年財運興旺",
        "negative": "Decade of financial challenges",
        "negative_chinese": "十年財運困難",
    },
    "annual": {
        "positive": "Year of financial opportunity",
        "positive_chinese": "年度財運良好",
        "negative": "Year of financial caution",
        "negative_chinese": "年度財運需謹慎",
    },
    "monthly": {
        "positive": "Month of financial opportunity",
        "positive_chinese": "月度財運良好",
        "negative": "Month of financial caution",
        "negative_chinese": "月度財運需謹慎",
    },
}

# * -------------------------
# * WEALTH ELEMENT BY DAYMASTER
# * -------------------------
# Day Master controls Wealth element

DM_WEALTH_ELEMENT = {
    "Wood": "Earth",   # Wood controls Earth
    "Fire": "Metal",   # Fire controls Metal
    "Earth": "Water",  # Earth controls Water
    "Metal": "Wood",   # Metal controls Wood
    "Water": "Fire",   # Water controls Fire
}

# * -------------------------
# * MAIN ANALYSIS FUNCTION
# * -------------------------

def generate_wealth_analysis(
    interactions: Dict,
    post_element_score: Dict[str, float],
    natal_element_score: Dict[str, float],
    seasonal_states: Dict[str, str],
    daymaster_element: str,
    daymaster_strength: str,
    wealth_storage_analysis: Optional[Dict] = None
) -> dict:
    """
    Analyze chart for wealth opportunities and risks.

    Good wealth period indicators:
    - DW/IW present in luck pillars
    - Wealth element strong (score > threshold)
    - Wealth element in Prosperous/Strengthening state
    - Storage activated (opened + filled)
    - Day Master strong enough to handle wealth

    Bad wealth period indicators:
    - RW (Rob Wealth) strong
    - Wealth element under clash/harm
    - Wealth element in Dead/Trapped state
    - Storage unopened or blocked
    - Day Master too weak to hold wealth

    Args:
        interactions: All chart interactions
        post_element_score: 10-stem scores after interactions
        natal_element_score: 10-stem scores natal only
        seasonal_states: Element seasonal states
        daymaster_element: Day Master's element
        daymaster_strength: "Strong", "Balanced", "Weak", etc.
        wealth_storage_analysis: Optional existing wealth storage data

    Returns:
        Dict with wealth analysis results
    """
    # Get wealth element for this Day Master
    wealth_element = DM_WEALTH_ELEMENT.get(daymaster_element, "")

    # Convert to element totals
    post_totals = stems_to_element_totals(post_element_score)
    natal_totals = stems_to_element_totals(natal_element_score)

    # Get wealth element scores
    wealth_score_post = post_totals.get(wealth_element, 0)
    wealth_score_natal = natal_totals.get(wealth_element, 0)
    wealth_change = wealth_score_post - wealth_score_natal

    # Get seasonal state for wealth element
    wealth_seasonal = seasonal_states.get(wealth_element, "Resting")

    # Determine if this is a good wealth period
    opportunities = []
    risks = []

    # Element translations for Indonesian
    element_id = {"Wood": "Kayu", "Fire": "Api", "Earth": "Tanah", "Metal": "Logam", "Water": "Air"}.get(wealth_element, wealth_element)

    # Seasonal state translations
    seasonal_chinese = {"Prosperous": "旺", "Strengthening": "相", "Resting": "休", "Trapped": "囚", "Dead": "死"}.get(wealth_seasonal, wealth_seasonal)
    seasonal_id = {"Prosperous": "Makmur", "Strengthening": "Menguat", "Resting": "Istirahat", "Trapped": "Terjebak", "Dead": "Mati"}.get(wealth_seasonal, wealth_seasonal)

    # Check wealth element strength
    if wealth_change > 50:
        opportunities.append({
            "type": "wealth_increase",
            "description": f"Wealth element ({wealth_element}) significantly strengthened",
            "description_chinese": f"財元素({wealth_element})顯著增強",
            "description_id": f"Elemen kekayaan ({element_id}) meningkat signifikan",
            "impact": "positive",
        })
    elif wealth_change < -30:
        risks.append({
            "type": "wealth_decrease",
            "description": f"Wealth element ({wealth_element}) weakened",
            "description_chinese": f"財元素({wealth_element})減弱",
            "description_id": f"Elemen kekayaan ({element_id}) melemah",
            "impact": "negative",
        })

    # Check seasonal state
    if wealth_seasonal in ["Prosperous", "Strengthening"]:
        opportunities.append({
            "type": "seasonal_favorable",
            "description": f"Wealth element in {wealth_seasonal} state",
            "description_chinese": f"財元素處於{seasonal_chinese}狀態",
            "description_id": f"Elemen kekayaan dalam kondisi {seasonal_id}",
            "impact": "positive",
        })
    elif wealth_seasonal in ["Dead", "Trapped"]:
        risks.append({
            "type": "seasonal_unfavorable",
            "description": f"Wealth element in {wealth_seasonal} state",
            "description_chinese": f"財元素處於{seasonal_chinese}狀態",
            "description_id": f"Elemen kekayaan dalam kondisi {seasonal_id}",
            "impact": "negative",
        })

    # Check Day Master capacity
    dm_can_handle = daymaster_strength in ["Strong", "Very Strong", "Balanced"]
    if not dm_can_handle:
        risks.append({
            "type": "weak_daymaster",
            "description": "Day Master may be too weak to handle wealth opportunities",
            "description_chinese": "日主較弱，可能難以把握財運",
            "description_id": "Day Master mungkin terlalu lemah untuk menangani peluang keuangan",
            "impact": "warning",
        })

    # Add wealth storage info if available
    # Enhanced: Track severity (maximum vs activated) and property opportunity
    storage_status = "unknown"
    maximum_count = 0
    activated_count = 0
    property_opportunity = False

    if wealth_storage_analysis:
        storages = wealth_storage_analysis.get("all_storages", [])
        total_count = len(storages)

        for s in storages:
            level = s.get("activation_level", "latent")
            if level == "maximum":
                maximum_count += 1
            elif level == "activated":
                activated_count += 1

        # Property detection: any activated storage = Earth branch active
        # All storage branches (Chen, Chou, Wei, Xu) are Earth = property/land
        total_activated = maximum_count + activated_count
        if total_activated > 0:
            property_opportunity = True

            # Add property-specific opportunity with severity-based weight
            if maximum_count >= 2:
                severity = "exceptional"
                desc = f"EXCEPTIONAL: {maximum_count} wealth storage(s) at MAXIMUM - prime property timing"
                desc_id = f"LUAR BIASA: {maximum_count} gudang kekayaan MAKSIMUM - waktu tepat untuk properti"
                desc_chinese = f"極佳：{maximum_count}個財庫達到最大值 - 置產良機"
            elif maximum_count >= 1:
                severity = "strong"
                desc = f"Strong property timing: {total_activated}/{total_count} storage(s) activated"
                desc_id = f"Waktu properti kuat: {total_activated}/{total_count} gudang aktif"
                desc_chinese = f"強勢：{total_activated}/{total_count}個財庫已啟動"
            else:
                severity = "moderate"
                desc = f"Property opportunity: {activated_count}/{total_count} storage(s) activated"
                desc_id = f"Peluang properti: {activated_count}/{total_count} gudang aktif"
                desc_chinese = f"適中：{activated_count}/{total_count}個財庫已啟動"

            opportunities.append({
                "type": "storage_activated",
                "description": desc,
                "description_id": desc_id,
                "description_chinese": desc_chinese,
                "impact": "positive",
                "severity": severity,
                "weight": (OPPORTUNITY_WEIGHTS["storage_maximum"] * maximum_count +
                          OPPORTUNITY_WEIGHTS["storage_activated"] * activated_count),
            })

            storage_status = "maximum" if maximum_count > 0 else "activated"
        elif total_count > 0:
            storage_status = "latent"

    # Calculate overall wealth outlook using weighted scoring
    def get_item_weight(item, default_weight=10):
        """Get weight from item or lookup by type."""
        if "weight" in item:
            return item["weight"]
        item_type = item.get("type", "")
        return OPPORTUNITY_WEIGHTS.get(item_type, RISK_WEIGHTS.get(item_type, default_weight))

    opportunity_score = sum(get_item_weight(o, 20) for o in opportunities)
    risk_score = sum(get_item_weight(r, 15) for r in risks)

    score_diff = opportunity_score - risk_score
    if score_diff > 30:
        outlook = "favorable"
        outlook_chinese = "有利"
    elif score_diff < -20:
        outlook = "challenging"
        outlook_chinese = "挑戰"
    else:
        outlook = "neutral"
        outlook_chinese = "中性"

    # Generate analysis text aligned with calculated outlook (multilingual)
    # Sort opportunities/risks by weight for priority
    sorted_opps = sorted(opportunities, key=lambda x: x.get("weight", 10), reverse=True)
    sorted_risks = sorted(risks, key=lambda x: x.get("weight", 10), reverse=True)

    has_exceptional = any(o.get("severity") == "exceptional" for o in opportunities)

    # Helper to get description in specific language
    def get_desc(item, lang_suffix=""):
        """Get description in specified language, fallback to English."""
        if lang_suffix:
            key = f"description_{lang_suffix}"
            if key in item:
                return item[key]
        return item.get("description", "")

    # Generate analysis text in all three languages
    analysis_text = ""
    analysis_text_chinese = ""
    analysis_text_id = ""

    if outlook == "favorable":
        if has_exceptional:
            analysis_text = f"Excellent wealth/property timing. {get_desc(sorted_opps[0])}."
            analysis_text_chinese = f"極佳的財運/置產時機。{get_desc(sorted_opps[0], 'chinese')}。"
            analysis_text_id = f"Waktu keuangan/properti yang sangat baik. {get_desc(sorted_opps[0], 'id')}."
        elif property_opportunity:
            analysis_text = f"Favorable period for wealth and property. {get_desc(sorted_opps[0])}."
            analysis_text_chinese = f"財運和置產的有利時期。{get_desc(sorted_opps[0], 'chinese')}。"
            analysis_text_id = f"Periode yang menguntungkan untuk keuangan dan properti. {get_desc(sorted_opps[0], 'id')}."
        else:
            analysis_text = f"Favorable wealth period. {get_desc(sorted_opps[0])}."
            analysis_text_chinese = f"財運有利時期。{get_desc(sorted_opps[0], 'chinese')}。"
            analysis_text_id = f"Periode keuangan yang menguntungkan. {get_desc(sorted_opps[0], 'id')}."

        # Add minor risk note if exists (doesn't change favorable outlook)
        if sorted_risks and sorted_risks[0].get("weight", 15) < 20:
            analysis_text += f" Minor caution: {get_desc(sorted_risks[0]).lower()}."
            analysis_text_chinese += f" 小提醒：{get_desc(sorted_risks[0], 'chinese')}。"
            analysis_text_id += f" Peringatan kecil: {get_desc(sorted_risks[0], 'id').lower()}."

    elif outlook == "challenging":
        analysis_text = f"Exercise financial caution. {get_desc(sorted_risks[0])}."
        analysis_text_chinese = f"財務上需謹慎。{get_desc(sorted_risks[0], 'chinese')}。"
        analysis_text_id = f"Berhati-hatilah dengan keuangan. {get_desc(sorted_risks[0], 'id')}."

    else:  # neutral
        if opportunities and risks:
            analysis_text = f"Mixed wealth signals. {get_desc(sorted_opps[0])}, but {get_desc(sorted_risks[0]).lower()}."
            analysis_text_chinese = f"財運信號參半。{get_desc(sorted_opps[0], 'chinese')}，但{get_desc(sorted_risks[0], 'chinese')}。"
            analysis_text_id = f"Sinyal keuangan campuran. {get_desc(sorted_opps[0], 'id')}, tetapi {get_desc(sorted_risks[0], 'id').lower()}."
        elif opportunities:
            analysis_text = f"Modest wealth opportunity. {get_desc(sorted_opps[0])}."
            analysis_text_chinese = f"適度的財運機會。{get_desc(sorted_opps[0], 'chinese')}。"
            analysis_text_id = f"Peluang keuangan yang sedang. {get_desc(sorted_opps[0], 'id')}."
        else:
            analysis_text = "Neutral wealth period with no significant indicators."
            analysis_text_chinese = "財運中性，無明顯指標。"
            analysis_text_id = "Periode keuangan netral tanpa indikator signifikan."

    # Add Indonesian outlook translation
    outlook_id = {"favorable": "menguntungkan", "challenging": "menantang", "neutral": "netral"}.get(outlook, "netral")

    return {
        "wealth_element": wealth_element,
        "wealth_element_chinese": {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}.get(wealth_element, ""),
        "wealth_element_id": {"Wood": "Kayu", "Fire": "Api", "Earth": "Tanah", "Metal": "Logam", "Water": "Air"}.get(wealth_element, ""),
        "wealth_score": round(wealth_score_post, 1),
        "wealth_change": round(wealth_change, 1),
        "wealth_seasonal_state": wealth_seasonal,
        "daymaster_can_handle": dm_can_handle,
        "storage_status": storage_status,
        "opportunities": opportunities,
        "risks": risks,
        "outlook": outlook,
        "outlook_chinese": outlook_chinese,
        "outlook_id": outlook_id,
        "analysis_text": analysis_text,
        "analysis_text_chinese": analysis_text_chinese,
        "analysis_text_id": analysis_text_id,
        # New fields for frontend flexibility
        "opportunity_score": opportunity_score,
        "risk_score": risk_score,
        "has_exceptional_opportunity": has_exceptional,
        "property_opportunity": property_opportunity,
        "maximum_storage_count": maximum_count if wealth_storage_analysis else 0,
    }
