# api/library/comprehensive/spiritual_sensitivity.py
"""
Spiritual Sensitivity Assessment (灵性敏感度评估)
Combines Shen Sha, Ten Gods, qi phase combos, and DM traits
to score a person's sensitivity to the spiritual/unseen realm.
"""

from typing import List, Dict, Tuple
from ..core import STEMS
from ..derived import get_ten_god
from .models import ChartData, ShenShaResult


# =============================================================================
# SENSITIVITY LEVELS
# =============================================================================

SENSITIVITY_LEVELS = [
    {
        "min": 0, "max": 20,
        "level": "normal",
        "label_en": "Normal",
        "label_zh": "正常",
        "description_en": "Grounded, practical, not particularly spiritual. Trusts what can be seen and touched.",
        "description_zh": "脚踏实地、务实，没有特别的灵性倾向。相信眼见为实。",
    },
    {
        "min": 21, "max": 40,
        "level": "mild",
        "label_en": "Mild Awareness",
        "label_zh": "轻度感知",
        "description_en": "Gets 'gut feelings' that turn out correct. Intuitive but dismisses it as coincidence.",
        "description_zh": '经常有准确的"直觉"，但自己把它当作巧合。',
    },
    {
        "min": 41, "max": 60,
        "level": "moderate",
        "label_en": "Moderate Sensitivity",
        "label_zh": "中度敏感",
        "description_en": "Vivid dreams that sometimes come true. Senses presence of spirits. Drawn to temples/churches. Feels energy of places.",
        "description_zh": "梦境清晰，有时会成真。能感应到灵体的存在。被寺庙/教堂吸引。能感受到场所的能量。",
    },
    {
        "min": 61, "max": 80,
        "level": "strong",
        "label_en": "Strong Sensitivity",
        "label_zh": "高度敏感",
        "description_en": "Can perceive spirits or energies. Attracted to mystical/occult knowledge. May have experienced unexplainable events. Should develop this ability rather than suppress it.",
        "description_zh": "能感知灵体或能量。被神秘/玄学知识吸引。可能经历过无法解释的事件。应该发展这种能力，而不是压制它。",
    },
    {
        "min": 81, "max": 100,
        "level": "extreme",
        "label_en": "Extremely Sensitive",
        "label_zh": "极度敏感",
        "description_en": "'Third eye' naturally open. Sees/senses other dimensions. Prophetic dreams are common. Has been told they're 'different' since childhood. Needs grounding practices to stay balanced.",
        "description_zh": '"天眼"自然开启。能看到/感知另一个维度。预知梦很常见。从小就被认为"与众不同"。需要接地练习来保持平衡。',
    },
]


def _get_level(score: int) -> dict:
    """Get the sensitivity level for a given score."""
    clamped = max(0, min(100, score))
    for level in SENSITIVITY_LEVELS:
        if level["min"] <= clamped <= level["max"]:
            return level
    return SENSITIVITY_LEVELS[0]


def assess_spiritual_sensitivity(
    chart: ChartData,
    shen_sha_results: List[ShenShaResult],
    qi_phase_spiritual_bonus: int = 0,
) -> Dict:
    """
    Assess spiritual sensitivity based on Shen Sha, Ten Gods, DM traits,
    and qi phase tandem bonuses.

    Returns:
        {
            "score": int (0-100),
            "level": str,
            "label_en": str,
            "label_zh": str,
            "description_en": str,
            "description_zh": str,
            "indicators": [{"name", "name_zh", "weight", "reason"}, ...],
            "guidance_en": str,
            "guidance_zh": str,
        }
    """
    indicators: List[Dict] = []
    score = 0

    present_shen_sha: Dict[str, ShenShaResult] = {}
    for r in shen_sha_results:
        if r.present:
            present_shen_sha[r.name_chinese] = r

    # --- PRIMARY INDICATORS ---

    # 华盖 (Canopy Star) -- #1 spiritual marker
    if "华盖" in present_shen_sha:
        w = 25
        score += w
        indicators.append({
            "name": "Canopy Star (Hua Gai)",
            "name_zh": "华盖",
            "weight": w,
            "reason": "THE classical spiritual marker — solitary, introspective, drawn to metaphysics",
        })

    # 童子 (Child Star) -- spirit child
    if "童子" in present_shen_sha:
        w = 20
        score += w
        indicators.append({
            "name": "Child Star (Tong Zi)",
            "name_zh": "童子",
            "weight": w,
            "reason": "Spirit child sent from heaven — soul not fully of this world",
        })

    # 太极贵人 (Tai Ji Noble)
    if "太极贵人" in present_shen_sha:
        w = 15
        score += w
        indicators.append({
            "name": "Tai Ji Noble",
            "name_zh": "太极贵人",
            "weight": w,
            "reason": "Metaphysical intelligence — natural affinity for yin-yang and the unseen",
        })

    # 空亡 (Void) on day or hour pillar
    for r in shen_sha_results:
        if r.name_chinese == "空亡" and r.present and r.palace in ("day", "hour"):
            palace_zh = {"day": "日柱", "hour": "时柱"}[r.palace]
            w = 15
            score += w
            indicators.append({
                "name": f"Void (Kong Wang) in {r.palace} pillar",
                "name_zh": f"空亡在{palace_zh}",
                "weight": w,
                "reason": f"Empty space in {r.palace} palace = thin barrier between worlds",
            })
            break  # Only count once

    # 偏印 (Indirect Resource) prominence
    # get_ten_god() returns a tuple: (abbreviation, english, chinese) or None
    dm = chart.day_master
    ir_count = 0
    # Check visible stems
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg[0] == "IR":
                ir_count += 1
    # Check hidden stems -- List[Tuple[str, int]]
    for pos in ["year", "month", "day", "hour"]:
        for hs, _weight in chart.pillars[pos].hidden_stems:
            if hs != dm:
                tg = get_ten_god(dm, hs)
                if tg and tg[0] == "IR":
                    ir_count += 1

    if ir_count >= 2:
        w = 15
        score += w
        indicators.append({
            "name": "Indirect Resource (Pian Yin) Prominent",
            "name_zh": "偏印突出",
            "weight": w,
            "reason": f"Unconventional perception — {ir_count} Indirect Resource stems found. Channel for non-physical knowledge",
        })
    elif ir_count == 1:
        w = 8
        score += w
        indicators.append({
            "name": "Indirect Resource (Pian Yin) Present",
            "name_zh": "偏印存在",
            "weight": w,
            "reason": "Some unconventional thinking — Indirect Resource present but not dominant",
        })

    # --- SECONDARY INDICATORS ---

    # 亡神 (Lost Spirit)
    if "亡神" in present_shen_sha:
        w = 10
        score += w
        indicators.append({
            "name": "Lost Spirit (Wang Shen)",
            "name_zh": "亡神",
            "weight": w,
            "reason": "Spirit energy scattered — porous boundary with spirit realm",
        })

    # Day Master 壬 or 癸 (Water)
    if dm in ("Ren", "Gui"):
        w = 5
        score += w
        indicators.append({
            "name": f"Water Day Master ({STEMS[dm]['chinese']})",
            "name_zh": f"日主{STEMS[dm]['chinese']}水",
            "weight": w,
            "reason": "Water element is naturally intuitive, reflective, and psychically receptive",
        })

    # Multiple Yin stems (3+)
    yin_count = sum(
        1 for pos in ["year", "month", "day", "hour"]
        if STEMS[chart.pillars[pos].stem]["polarity"] == "Yin"
    )
    if yin_count >= 3:
        w = 5
        score += w
        indicators.append({
            "name": f"Multiple Yin Stems ({yin_count}/4)",
            "name_zh": f"多阴干({yin_count}/4)",
            "weight": w,
            "reason": "Yin energy is more receptive to the spiritual/invisible realm",
        })

    # --- QI PHASE TANDEM BONUS ---
    if qi_phase_spiritual_bonus > 0:
        score += qi_phase_spiritual_bonus
        indicators.append({
            "name": "Qi Phase + Shen Sha Tandem Effects",
            "name_zh": "十二长生+神煞联动效应",
            "weight": qi_phase_spiritual_bonus,
            "reason": "Qi phase combinations amplify spiritual sensitivity (see qi phase analysis)",
        })

    # --- DAMPENING INDICATORS ---

    # 正印 (Direct Resource) dominant over 偏印
    dr_count = 0
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg[0] == "DR":
                dr_count += 1
    if dr_count > ir_count and dr_count >= 2:
        w = -10
        score += w
        indicators.append({
            "name": "Direct Resource Dominant",
            "name_zh": "正印压制偏印",
            "weight": w,
            "reason": "Orthodox thinking overrides intuition — conventional mind suppresses psychic channel",
        })

    # 正官 (Direct Officer) very prominent
    do_count = 0
    for pos in ["year", "month", "day", "hour"]:
        stem = chart.pillars[pos].stem
        if stem != dm:
            tg = get_ten_god(dm, stem)
            if tg and tg[0] == "DO":
                do_count += 1
    if do_count >= 2:
        w = -5
        score += w
        indicators.append({
            "name": "Direct Officer Very Prominent",
            "name_zh": "正官太旺",
            "weight": w,
            "reason": "Rigid structure and rules suppress spiritual sensitivity",
        })

    # Clamp score
    score = max(0, min(100, score))

    # Get level
    level_info = _get_level(score)

    # Generate guidance
    guidance_en, guidance_zh = _generate_guidance(score, indicators, present_shen_sha)

    return {
        "score": score,
        "level": level_info["level"],
        "label_en": level_info["label_en"],
        "label_zh": level_info["label_zh"],
        "description_en": level_info["description_en"],
        "description_zh": level_info["description_zh"],
        "indicators": indicators,
        "guidance_en": guidance_en,
        "guidance_zh": guidance_zh,
    }


def _generate_guidance(score: int, indicators: list, present_shen_sha: dict) -> Tuple[str, str]:
    """Generate guidance text based on score and indicators."""
    if score <= 20:
        return (
            "No special spiritual development needed. Focus on practical life goals.",
            "无需特别的灵性发展。专注于实际生活目标。",
        )
    elif score <= 40:
        return (
            "Trust your gut feelings more — they are often correct. Light meditation or mindfulness practice would sharpen this natural intuition.",
            "多相信自己的直觉——它们往往是正确的。轻度冥想或正念练习可以增强这种天生的直觉。",
        )
    elif score <= 60:
        en = "You have real spiritual sensitivity. Consider structured spiritual practice — meditation, qigong, or temple visits."
        zh = "你有真正的灵性敏感度。建议进行有结构的灵性修行——冥想、气功或寺庙参拜。"
        if "华盖" in present_shen_sha:
            en += " The Canopy Star in your chart means solitude helps you connect with the spiritual realm — don't fight the need for alone time."
            zh += " 你命中的华盖意味着独处有助于连接灵性世界——不要抗拒独处的需要。"
        return (en, zh)
    elif score <= 80:
        en = "Strong spiritual sensitivity — you likely already experience unexplainable phenomena. This ability should be DEVELOPED, not suppressed. Suppressing it causes anxiety, insomnia, and restlessness."
        zh = "灵性敏感度很强——你很可能已经经历过无法解释的现象。这种能力应该被发展，而不是压制。压制它会导致焦虑、失眠和不安。"
        if "童子" in present_shen_sha:
            en += " The Child Star suggests your soul carries memories from before this life. Classical remedy: 送替身 ritual to settle the spirit."
            zh += " 童子星暗示你的灵魂携带着前世的记忆。古典化解方法：送替身仪式来安定灵体。"
        en += " Seek a qualified spiritual teacher or mentor."
        zh += " 建议寻找合格的灵性导师。"
        return (en, zh)
    else:
        en = "Extremely high spiritual sensitivity — your 'third eye' is naturally open. You likely see, sense, or dream things others cannot. This is NOT a disorder — it is a genuine ability that needs proper management."
        zh = '极高的灵性敏感度——你的"天眼"自然开启。你很可能看到、感知到或梦到别人无法触及的事物。这不是病——这是真正的能力，需要正确管理。'
        en += " CRITICAL: Grounding practices are essential — physical exercise, Earth element remedies, structured daily routine. Without grounding, this sensitivity can become overwhelming."
        zh += " 重要：接地练习至关重要——体育锻炼、土元素化解、有规律的日常作息。没有接地，这种敏感度可能变得难以承受。"
        if "华盖" in present_shen_sha and "空亡" in present_shen_sha:
            en += " Canopy + Void combination: structured spiritual practice (Buddhism, Taoism) is better than unstructured exploration."
            zh += " 华盖+空亡组合：有结构的灵性修行（佛教、道教）比无序探索更好。"
        return (en, zh)
