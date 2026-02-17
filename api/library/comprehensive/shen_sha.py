# =============================================================================
# COMPLETE SHEN SHA (神煞) ENGINE — All 37+ Stars
# =============================================================================
# Every star has:
#   1. A lookup table for derivation
#   2. A check function that returns ShenShaResult
#   3. Full derivation logic shown in the result
#
# CORRECTED: Kong Wang uses full Day Pillar (stem+branch), not just stem.
# =============================================================================

from typing import List, Dict, Set, Optional, Tuple
from ..core import STEMS, BRANCHES
from ..derived import STEM_ORDER, BRANCH_ORDER, get_ten_god
from .models import ShenShaResult, ChartData

# =============================================================================
# UTILITY: 60 Jiazi cycle
# =============================================================================

def _jiazi_number(stem: str, branch: str) -> int:
    """Calculate the 60 Jiazi pillar number (0-59) from stem and branch."""
    si = STEMS[stem]["index"]
    bi = BRANCHES[branch]["index"]
    # Stem and branch must share parity (both even or both odd index)
    # Formula: find N where N%10==si and N%12==bi, 0 <= N < 60
    for n in range(60):
        if n % 10 == si and n % 12 == bi:
            return n
    return -1  # Invalid combination


def _xun_void_branches(stem: str, branch: str) -> Tuple[str, str]:
    """
    Calculate the two Void (空亡) branches for a given pillar.
    Uses the full stem+branch to determine the 旬 (decade).
    """
    n = _jiazi_number(stem, branch)
    if n < 0:
        return ("", "")
    xun_start = (n // 10) * 10  # First pillar in this 旬
    # The 10 branches used in this 旬
    used_branches = set()
    for i in range(10):
        bi = (xun_start + i) % 12
        used_branches.add(bi)
    # The 2 missing branches are the void ones
    all_branches = set(range(12))
    void_indices = sorted(all_branches - used_branches)
    return (BRANCH_ORDER[void_indices[0]], BRANCH_ORDER[void_indices[1]])


# =============================================================================
# HELPER: Check if a branch is in the chart
# =============================================================================

def _find_branch(chart: ChartData, target_branch: str,
                 include_lp: bool = True) -> List[dict]:
    """Find all locations of a branch in the chart. Returns list of {palace, activated_by}."""
    results = []
    for pos in ["year", "month", "day", "hour"]:
        if chart.pillars[pos].branch == target_branch:
            results.append({"palace": pos, "activated_by": None})
    if include_lp and chart.luck_pillar and chart.luck_pillar.branch == target_branch:
        results.append({"palace": "luck_pillar", "activated_by": "luck_pillar"})
    for pos, pillar in chart.time_period_pillars.items():
        if pillar.branch == target_branch:
            results.append({"palace": pos, "activated_by": pos})
    return results


def _branch_in_chart(chart: ChartData, target_branch: str,
                     include_lp: bool = True) -> bool:
    return len(_find_branch(chart, target_branch, include_lp)) > 0


# =============================================================================
# 1. 天乙贵人 (Tian Yi Gui Ren / Heavenly Noble)
# =============================================================================

TIAN_YI_LOOKUP: Dict[str, Tuple[str, str]] = {
    "Jia": ("Chou", "Wei"),
    "Yi":  ("Zi", "Shen"),
    "Bing": ("Hai", "You"),
    "Ding": ("Hai", "You"),
    "Wu":  ("Chou", "Wei"),
    "Ji":  ("Zi", "Shen"),
    "Geng": ("Chou", "Wei"),
    "Xin": ("Yin", "Wu"),
    "Ren": ("Mao", "Si"),
    "Gui": ("Mao", "Si"),
}


def check_tian_yi(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    targets = TIAN_YI_LOOKUP.get(dm, ())
    results = []
    for t in targets:
        locs = _find_branch(chart, t)
        if locs:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Heavenly Noble",
                    name_chinese="天乙贵人",
                    present=True,
                    location=t,
                    palace=loc["palace"],
                    activated_by=loc["activated_by"],
                    derivation=f"For {dm} DM: Tian Yi at {BRANCHES[t]['chinese']} ({t}). "
                               f"Found in {loc['palace'].replace('_', ' ')} palace.",
                    nature="auspicious",
                    life_areas=["career", "relationship", "wealth"],
                    severity="mild",
                ))
        else:
            results.append(ShenShaResult(
                name_english="Heavenly Noble",
                name_chinese="天乙贵人",
                present=False,
                location=t,
                derivation=f"For {dm} DM: Tian Yi at {BRANCHES[t]['chinese']} ({t}). Not in chart.",
            ))
    return results


# =============================================================================
# 2. 太极贵人 (Tai Ji Gui Ren / Tai Ji Noble)
# =============================================================================

TAI_JI_LOOKUP: Dict[str, Tuple[str, str]] = {
    "Jia": ("Zi", "Wu"),   "Yi":  ("Zi", "Wu"),
    "Bing": ("Mao", "You"), "Ding": ("Mao", "You"),
    "Wu":  ("Mao", "You"), "Ji":  ("Mao", "You"),
    "Geng": ("Chou", "Wei"), "Xin": ("Chou", "Wei"),
    "Ren": ("Zi", "Wu"),   "Gui": ("Zi", "Wu"),
}


def check_tai_ji(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    targets = TAI_JI_LOOKUP.get(dm, ())
    results = []
    for t in targets:
        locs = _find_branch(chart, t)
        if locs:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Tai Ji Noble",
                    name_chinese="太极贵人",
                    present=True, location=t, palace=loc["palace"],
                    activated_by=loc["activated_by"],
                    derivation=f"For {dm} DM: Tai Ji at {BRANCHES[t]['chinese']}. In {loc['palace']}.",
                    nature="auspicious",
                    life_areas=["career", "education"],
                ))
    if not any(r.present for r in results):
        results.append(ShenShaResult(
            name_english="Tai Ji Noble", name_chinese="太极贵人", present=False,
            derivation=f"For {dm} DM: Tai Ji at {', '.join(BRANCHES[t]['chinese'] for t in targets)}. Not in chart.",
        ))
    return results


# =============================================================================
# 3. 天德贵人 (Tian De Gui Ren / Heavenly Virtue)
# =============================================================================

TIAN_DE_LOOKUP: Dict[str, str] = {
    # Month Branch -> Tian De Stem/Branch
    "Yin": "Ding", "Mao": "Shen", "Chen": "Ren", "Si": "Xin",
    "Wu": "Hai", "Wei": "Jia", "Shen": "Gui", "You": "Yin",
    "Xu": "Bing", "Hai": "Yi", "Zi": "Si", "Chou": "Geng",
}


def check_tian_de(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    target = TIAN_DE_LOOKUP.get(month_branch)
    if not target:
        return [ShenShaResult(name_english="Heavenly Virtue", name_chinese="天德贵人",
                              present=False, derivation="Could not determine month branch.")]

    # Target can be a stem or a branch
    found = False
    palace = None
    activated_by = None

    # Check if target is a stem (appears as heavenly stem in chart)
    if target in STEMS:
        for pos in ["year", "month", "day", "hour"]:
            if chart.pillars[pos].stem == target:
                found = True
                palace = pos
                break

    # Check if target is a branch
    if target in BRANCHES:
        locs = _find_branch(chart, target)
        if locs:
            found = True
            palace = locs[0]["palace"]
            activated_by = locs[0]["activated_by"]

    return [ShenShaResult(
        name_english="Heavenly Virtue", name_chinese="天德贵人",
        present=found, location=target, palace=palace, activated_by=activated_by,
        derivation=f"For {BRANCHES[month_branch]['chinese']} month: Tian De = {target}. "
                   f"{'PRESENT' if found else 'ABSENT'}.",
        nature="auspicious" if found else "neutral",
        life_areas=["general", "health"],
    )]


# =============================================================================
# 4. 月德贵人 (Yue De Gui Ren / Monthly Virtue)
# =============================================================================

YUE_DE_LOOKUP: Dict[str, str] = {
    # Month branch group -> Yue De stem
    "Yin": "Bing", "Wu": "Bing", "Xu": "Bing",       # 寅午戌月 → 丙
    "Shen": "Ren", "Zi": "Ren", "Chen": "Ren",       # 申子辰月 → 壬
    "Si": "Geng", "You": "Geng", "Chou": "Geng",     # 巳酉丑月 → 庚
    "Hai": "Jia", "Mao": "Jia", "Wei": "Jia",        # 亥卯未月 → 甲
}


def check_yue_de(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    target_stem = YUE_DE_LOOKUP.get(month_branch)
    if not target_stem:
        return [ShenShaResult(name_english="Monthly Virtue", name_chinese="月德贵人",
                              present=False, derivation="Could not determine.")]

    found = False
    palace = None
    for pos in ["year", "month", "day", "hour"]:
        if chart.pillars[pos].stem == target_stem:
            found = True
            palace = pos
            break
    # Also check hidden stems
    if not found:
        for pos in ["year", "month", "day", "hour"]:
            for hs, _ in chart.pillars[pos].hidden_stems:
                if hs == target_stem:
                    found = True
                    palace = pos
                    break

    return [ShenShaResult(
        name_english="Monthly Virtue", name_chinese="月德贵人",
        present=found, location=target_stem, palace=palace,
        derivation=f"For {BRANCHES[month_branch]['chinese']} month: Yue De = {STEMS[target_stem]['chinese']}. "
                   f"{'PRESENT' if found else 'ABSENT'}.",
        nature="auspicious" if found else "neutral",
        life_areas=["general", "health"],
    )]


# =============================================================================
# 5. 文昌贵人 (Wen Chang / Academic Star)
# =============================================================================

WEN_CHANG_LOOKUP: Dict[str, str] = {
    "Jia": "Si", "Yi": "Wu", "Bing": "Shen", "Ding": "You",
    "Wu": "Shen", "Ji": "You", "Geng": "Hai", "Xin": "Zi",
    "Ren": "Yin", "Gui": "Mao",
}


def check_wen_chang(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = WEN_CHANG_LOOKUP.get(dm, "")
    if not target:
        return []
    locs = _find_branch(chart, target)
    if locs:
        loc = locs[0]
        return [ShenShaResult(
            name_english="Academic Star", name_chinese="文昌贵人",
            present=True, location=target, palace=loc["palace"],
            activated_by=loc["activated_by"],
            derivation=f"For {dm} DM: Wen Chang at {BRANCHES[target]['chinese']}. In {loc['palace']}.",
            nature="auspicious", life_areas=["education", "career"],
        )]
    return [ShenShaResult(
        name_english="Academic Star", name_chinese="文昌贵人",
        present=False, location=target,
        derivation=f"For {dm} DM: Wen Chang at {BRANCHES[target]['chinese']}. Not in chart.",
    )]


# =============================================================================
# 6. 金舆 (Jin Yu / Golden Carriage)
# =============================================================================

JIN_YU_LOOKUP: Dict[str, str] = {
    "Jia": "Chen", "Yi": "Si", "Bing": "Wei", "Ding": "Shen",
    "Wu": "Wei", "Ji": "Shen", "Geng": "Xu", "Xin": "Hai",
    "Ren": "Zi", "Gui": "Chou",
}


def check_jin_yu(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = JIN_YU_LOOKUP.get(dm, "")
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Golden Carriage", name_chinese="金舆",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {dm} DM: Jin Yu at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT in ' + locs[0]['palace'] if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["wealth", "status"],
    )]


# =============================================================================
# 7. 天厨贵人 (Tian Chu / Heavenly Kitchen)
# =============================================================================

TIAN_CHU_LOOKUP: Dict[str, str] = {
    "Jia": "Si", "Yi": "Wu", "Bing": "Si", "Ding": "Wu",
    "Wu": "Si", "Ji": "Wu", "Geng": "Shen", "Xin": "You",
    "Ren": "Shen", "Gui": "You",
}


def check_tian_chu(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = TIAN_CHU_LOOKUP.get(dm, "")
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Heavenly Kitchen", name_chinese="天厨贵人",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {dm} DM: Tian Chu at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["wealth", "food"],
    )]


# =============================================================================
# 8. 禄神 (Lu Shen / Prosperity Star)
# =============================================================================

LU_SHEN_LOOKUP: Dict[str, str] = {
    "Jia": "Yin", "Yi": "Mao", "Bing": "Si", "Ding": "Wu",
    "Wu": "Si", "Ji": "Wu", "Geng": "Shen", "Xin": "You",
    "Ren": "Hai", "Gui": "Zi",
}


def check_lu_shen(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = LU_SHEN_LOOKUP.get(dm, "")
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Prosperity Star", name_chinese="禄神",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {dm} DM: Lu Shen at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["wealth", "career"],
    )]


# =============================================================================
# 9. 将星 (Jiang Xing / General Star)
# =============================================================================

JIANG_XING_LOOKUP: Dict[str, str] = {
    # Year/Day Branch -> General Star (the 'emperor' of the Three Harmony frame)
    "Yin": "Wu", "Wu": "Wu", "Xu": "Wu",
    "Shen": "Zi", "Zi": "Zi", "Chen": "Zi",
    "Si": "You", "You": "You", "Chou": "You",
    "Hai": "Mao", "Mao": "Mao", "Wei": "Mao",
}


def check_jiang_xing(chart: ChartData) -> List[ShenShaResult]:
    results = []
    for base_pos in ["year", "day"]:
        base_branch = chart.pillars[base_pos].branch
        target = JIANG_XING_LOOKUP.get(base_branch)
        if not target:
            continue
        locs = _find_branch(chart, target, include_lp=True)
        if locs:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="General Star", name_chinese="将星",
                    present=True, location=target, palace=loc["palace"],
                    activated_by=loc["activated_by"],
                    derivation=f"For {base_pos} branch {BRANCHES[base_branch]['chinese']}: "
                               f"Jiang Xing at {BRANCHES[target]['chinese']}. In {loc['palace']}.",
                    nature="auspicious", life_areas=["career", "authority"],
                ))
    if not results:
        year_branch = chart.pillars["year"].branch
        target = JIANG_XING_LOOKUP.get(year_branch, "?")
        results.append(ShenShaResult(
            name_english="General Star", name_chinese="将星",
            present=False, location=target if target != "?" else None,
            derivation=f"Jiang Xing at {BRANCHES.get(target, {}).get('chinese', '?')}. ABSENT.",
        ))
    return results


# =============================================================================
# 10. 天医 (Tian Yi / Heavenly Doctor)
# =============================================================================

TIAN_YI_DOCTOR_LOOKUP: Dict[str, str] = {
    # Month Branch -> Tian Yi Doctor branch (one position behind in the 12 branches)
    "Yin": "Chou", "Mao": "Yin", "Chen": "Mao", "Si": "Chen",
    "Wu": "Si", "Wei": "Wu", "Shen": "Wei", "You": "Shen",
    "Xu": "You", "Hai": "Xu", "Zi": "Hai", "Chou": "Zi",
}


def check_tian_yi_doctor(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    target = TIAN_YI_DOCTOR_LOOKUP.get(month_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Heavenly Doctor", name_chinese="天医",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {BRANCHES[month_branch]['chinese']} month: Tian Yi Doctor at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["health"],
    )]


# =============================================================================
# 11. 天赦 (Tian She / Heavenly Pardon)
# =============================================================================

TIAN_SHE_LOOKUP: Dict[str, str] = {
    # Season -> required Day Pillar (stem+branch combined key)
    "Spring": "Wu-Yin",    # 戊寅日
    "Summer": "Jia-Wu",    # 甲午日
    "Autumn": "Wu-Shen",   # 戊申日
    "Winter": "Jia-Zi",    # 甲子日
}


def check_tian_she(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    season = BRANCHES[month_branch]["season"]
    required = TIAN_SHE_LOOKUP.get(season)
    if not required:
        return []
    day_key = f"{chart.pillars['day'].stem}-{chart.pillars['day'].branch}"
    present = day_key == required
    return [ShenShaResult(
        name_english="Heavenly Pardon", name_chinese="天赦",
        present=present,
        derivation=f"Born in {season} ({BRANCHES[month_branch]['chinese']} month): "
                   f"Tian She requires {required} day. Day is {day_key}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["legal", "general"],
    )]


# =============================================================================
# 12. 红鸾 (Hong Luan / Red Phoenix)
# =============================================================================

HONG_LUAN_LOOKUP: Dict[str, str] = {
    "Zi": "Mao", "Chou": "Yin", "Yin": "Chou", "Mao": "Zi",
    "Chen": "Hai", "Si": "Xu", "Wu": "You", "Wei": "Shen",
    "Shen": "Wei", "You": "Wu", "Xu": "Si", "Hai": "Chen",
}


def check_hong_luan(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = HONG_LUAN_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Red Phoenix", name_chinese="红鸾",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Hong Luan at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["marriage", "relationship"],
    )]


# =============================================================================
# 13. 天喜 (Tian Xi / Heavenly Happiness) — opposite of Hong Luan
# =============================================================================

TIAN_XI_LOOKUP: Dict[str, str] = {
    "Zi": "You", "Chou": "Shen", "Yin": "Wei", "Mao": "Wu",
    "Chen": "Si", "Si": "Chen", "Wu": "Mao", "Wei": "Yin",
    "Shen": "Chou", "You": "Zi", "Xu": "Hai", "Hai": "Xu",
}


def check_tian_xi(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = TIAN_XI_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Heavenly Happiness", name_chinese="天喜",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Tian Xi at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["marriage", "celebration"],
    )]


# =============================================================================
# 14. 福星贵人 (Fu Xing / Fortune Star)
# =============================================================================

FU_XING_LOOKUP: Dict[str, str] = {
    "Jia": "Yin", "Yi": "Mao", "Bing": "Si", "Ding": "Wu",
    "Wu": "Si", "Ji": "Wu", "Geng": "Shen", "Xin": "You",
    "Ren": "Hai", "Gui": "Zi",
}


def check_fu_xing(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = FU_XING_LOOKUP.get(dm, "")
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Fortune Star", name_chinese="福星贵人",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {dm} DM: Fu Xing at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="auspicious" if present else "neutral",
        life_areas=["wealth", "luck"],
    )]


# =============================================================================
# 15. 三奇贵人 (San Qi / Three Wonders Noble)
# =============================================================================

def check_san_qi(chart: ChartData) -> List[ShenShaResult]:
    stems = [chart.pillars[p].stem for p in ["year", "month", "day", "hour"]]

    # Heavenly Three Wonders: 甲戊庚 in sequence
    heaven = ["Jia", "Wu", "Geng"]
    # Earthly Three Wonders: 乙丙丁 in sequence
    earth = ["Yi", "Bing", "Ding"]
    # Human Three Wonders: 壬癸辛 in sequence
    human = ["Ren", "Gui", "Xin"]

    def check_sequence(seq, name):
        for i in range(len(stems) - 2):
            if stems[i:i+3] == seq:
                return True
        return False

    results = []
    for seq, label, cn in [(heaven, "Heavenly", "天上三奇"),
                            (earth, "Earthly", "地上三奇"),
                            (human, "Human", "人中三奇")]:
        found = check_sequence(seq, label)
        if found:
            results.append(ShenShaResult(
                name_english=f"Three Wonders ({label})",
                name_chinese=cn,
                present=True,
                derivation=f"Stems sequence {' → '.join(STEMS[s]['chinese'] for s in seq)} found in pillars.",
                nature="auspicious",
                life_areas=["intelligence", "career"],
            ))

    if not results:
        results.append(ShenShaResult(
            name_english="Three Wonders Noble", name_chinese="三奇贵人",
            present=False,
            derivation="No Three Wonders sequence (甲戊庚, 乙丙丁, 壬癸辛) found in stem order.",
        ))
    return results


# =============================================================================
# 16. 羊刃 (Yang Ren / Sheep Blade) — extended for all DMs
# =============================================================================

YANG_REN_LOOKUP: Dict[str, str] = {
    # Classical: Yang stems only
    "Jia": "Mao", "Bing": "Wu", "Wu": "Wu", "Geng": "You", "Ren": "Zi",
    # Extended for Yin stems (one past Lu)
    "Yi": "Chen", "Ding": "Wei", "Ji": "Wei", "Xin": "Xu", "Gui": "Chou",
}


def check_yang_ren(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = YANG_REN_LOOKUP.get(dm)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    is_yang = STEMS[dm]["polarity"] == "Yang"
    return [ShenShaResult(
        name_english="Sheep Blade", name_chinese="羊刃",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {dm} DM ({'Yang' if is_yang else 'Yin, extended'}): "
                   f"Yang Ren at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "career", "legal"],
        severity="moderate" if present else "mild",
    )]


# =============================================================================
# 17. 空亡 (Kong Wang / Void) — CORRECTED: uses full Day Pillar
# =============================================================================

def check_kong_wang(chart: ChartData) -> List[ShenShaResult]:
    day_stem = chart.pillars["day"].stem
    day_branch = chart.pillars["day"].branch
    void_b1, void_b2 = _xun_void_branches(day_stem, day_branch)

    results = []
    for vb in [void_b1, void_b2]:
        if not vb:
            continue
        locs = _find_branch(chart, vb, include_lp=False)  # Only natal
        if locs:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Void Star", name_chinese="空亡",
                    present=True, location=vb, palace=loc["palace"],
                    derivation=f"Day Pillar {STEMS[day_stem]['chinese']}{BRANCHES[day_branch]['chinese']} "
                               f"is in {_get_xun_name(day_stem, day_branch)}. "
                               f"Void at {BRANCHES[vb]['chinese']}. Found in {loc['palace']}.",
                    nature="inauspicious",
                    life_areas=["career", "relationship", "children"],
                    severity="moderate",
                ))
        else:
            results.append(ShenShaResult(
                name_english="Void Star", name_chinese="空亡",
                present=False, location=vb,
                derivation=f"Void at {BRANCHES[vb]['chinese']}. Not in natal branches.",
            ))
    return results


def _get_xun_name(stem: str, branch: str) -> str:
    n = _jiazi_number(stem, branch)
    xun_start = (n // 10) * 10
    s_idx = xun_start % 10
    b_idx = xun_start % 12
    return f"{STEMS[STEM_ORDER[s_idx]]['chinese']}{BRANCHES[BRANCH_ORDER[b_idx]]['chinese']}旬"


def get_void_branches(chart: ChartData) -> Set[str]:
    """Get the set of Void branch IDs for this chart."""
    day_stem = chart.pillars["day"].stem
    day_branch = chart.pillars["day"].branch
    vb1, vb2 = _xun_void_branches(day_stem, day_branch)
    return {vb1, vb2} - {""}


# =============================================================================
# 18. 桃花 (Tao Hua / Peach Blossom)
# =============================================================================

TAO_HUA_LOOKUP: Dict[str, str] = {
    "Yin": "Mao", "Wu": "Mao", "Xu": "Mao",
    "Shen": "You", "Zi": "You", "Chen": "You",
    "Si": "Wu", "You": "Wu", "Chou": "Wu",
    "Hai": "Zi", "Mao": "Zi", "Wei": "Zi",
}


def check_tao_hua(chart: ChartData) -> List[ShenShaResult]:
    results = []
    seen = set()
    for base_pos in ["year", "day"]:
        base_branch = chart.pillars[base_pos].branch
        target = TAO_HUA_LOOKUP.get(base_branch)
        if not target or target in seen:
            continue
        seen.add(target)
        locs = _find_branch(chart, target)
        present = len(locs) > 0
        if present:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Peach Blossom", name_chinese="桃花",
                    present=True, location=target, palace=loc["palace"],
                    activated_by=loc["activated_by"],
                    derivation=f"For {base_pos} branch {BRANCHES[base_branch]['chinese']}: "
                               f"Peach Blossom at {BRANCHES[target]['chinese']}. In {loc['palace']}.",
                    nature="mixed",
                    life_areas=["relationship", "career"],
                ))
    if not any(r.present for r in results):
        year_branch = chart.pillars["year"].branch
        target = TAO_HUA_LOOKUP.get(year_branch, "?")
        results.append(ShenShaResult(
            name_english="Peach Blossom", name_chinese="桃花",
            present=False, location=target if target != "?" else None,
            derivation=f"Peach Blossom at {BRANCHES.get(target, {}).get('chinese', '?')}. ABSENT.",
        ))
    return results


# =============================================================================
# 19. 华盖 (Hua Gai / Canopy Star)
# =============================================================================

HUA_GAI_LOOKUP: Dict[str, str] = {
    "Yin": "Xu", "Wu": "Xu", "Xu": "Xu",
    "Shen": "Chen", "Zi": "Chen", "Chen": "Chen",
    "Si": "Chou", "You": "Chou", "Chou": "Chou",
    "Hai": "Wei", "Mao": "Wei", "Wei": "Wei",
}


def check_hua_gai(chart: ChartData) -> List[ShenShaResult]:
    results = []
    seen = set()
    for base_pos in ["year", "day"]:
        base_branch = chart.pillars[base_pos].branch
        target = HUA_GAI_LOOKUP.get(base_branch)
        if not target or target in seen:
            continue
        seen.add(target)
        locs = _find_branch(chart, target)
        present = len(locs) > 0
        if present:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Canopy Star", name_chinese="华盖",
                    present=True, location=target, palace=loc["palace"],
                    derivation=f"For {base_pos} branch {BRANCHES[base_branch]['chinese']}: "
                               f"Hua Gai at {BRANCHES[target]['chinese']}. In {loc['palace']}.",
                    nature="mixed", life_areas=["spirituality", "education"],
                ))
    if not any(r.present for r in results if r.present):
        year_branch = chart.pillars["year"].branch
        target = HUA_GAI_LOOKUP.get(year_branch, "?")
        results.append(ShenShaResult(
            name_english="Canopy Star", name_chinese="华盖",
            present=False,
            derivation=f"Hua Gai at {BRANCHES.get(target, {}).get('chinese', '?')}. ABSENT.",
        ))
    return results


# =============================================================================
# 20. 驿马 (Yi Ma / Traveling Horse)
# =============================================================================

YI_MA_LOOKUP: Dict[str, str] = {
    "Yin": "Shen", "Wu": "Shen", "Xu": "Shen",
    "Shen": "Yin", "Zi": "Yin", "Chen": "Yin",
    "Si": "Hai", "You": "Hai", "Chou": "Hai",
    "Hai": "Si", "Mao": "Si", "Wei": "Si",
}


def check_yi_ma(chart: ChartData) -> List[ShenShaResult]:
    results = []
    seen = set()
    for base_pos in ["year", "day"]:
        base_branch = chart.pillars[base_pos].branch
        target = YI_MA_LOOKUP.get(base_branch)
        if not target or target in seen:
            continue
        seen.add(target)
        locs = _find_branch(chart, target)
        present = len(locs) > 0
        if present:
            for loc in locs:
                results.append(ShenShaResult(
                    name_english="Traveling Horse", name_chinese="驿马",
                    present=True, location=target, palace=loc["palace"],
                    activated_by=loc["activated_by"],
                    derivation=f"For {base_pos} branch {BRANCHES[base_branch]['chinese']}: "
                               f"Yi Ma at {BRANCHES[target]['chinese']}. In {loc['palace']}.",
                    nature="mixed", life_areas=["travel", "career"],
                ))
    if not results:
        year_branch = chart.pillars["year"].branch
        target = YI_MA_LOOKUP.get(year_branch, "?")
        results.append(ShenShaResult(
            name_english="Traveling Horse", name_chinese="驿马",
            present=False, location=target if target != "?" else None,
            derivation=f"Yi Ma at {BRANCHES.get(target, {}).get('chinese', '?')}. ABSENT.",
        ))
    return results


# =============================================================================
# 21. 劫煞 (Jie Sha / Robbery Star)
# =============================================================================

JIE_SHA_LOOKUP: Dict[str, str] = {
    "Yin": "Hai", "Wu": "Hai", "Xu": "Hai",
    "Shen": "Si", "Zi": "Si", "Chen": "Si",
    "Si": "Yin", "You": "Yin", "Chou": "Yin",
    "Hai": "Shen", "Mao": "Shen", "Wei": "Shen",
}


def check_jie_sha(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = JIE_SHA_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Robbery Star", name_chinese="劫煞",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Jie Sha at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["wealth", "safety"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 22. 亡神 (Wang Shen / Lost Spirit)
# =============================================================================

WANG_SHEN_LOOKUP: Dict[str, str] = {
    "Yin": "Si", "Wu": "Si", "Xu": "Si",
    "Shen": "Hai", "Zi": "Hai", "Chen": "Hai",
    "Si": "Shen", "You": "Shen", "Chou": "Shen",
    "Hai": "Yin", "Mao": "Yin", "Wei": "Yin",
}


def check_wang_shen(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = WANG_SHEN_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Lost Spirit", name_chinese="亡神",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Wang Shen at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "spirit"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 23. 灾煞 (Zai Sha / Disaster Star)
# =============================================================================

ZAI_SHA_LOOKUP: Dict[str, str] = {
    "Yin": "Zi", "Wu": "Zi", "Xu": "Zi",
    "Shen": "Wu", "Zi": "Wu", "Chen": "Wu",
    "Si": "Mao", "You": "Mao", "Chou": "Mao",  # Fixed: 巳酉丑 → 午 is wrong for Zai Sha
    "Hai": "You", "Mao": "You", "Wei": "You",
}
# Correction: Zai Sha standard: 寅午戌→子, 巳酉丑→午, 申子辰→卯, 亥卯未→酉
# Fixing:
ZAI_SHA_LOOKUP = {
    "Yin": "Zi", "Wu": "Zi", "Xu": "Zi",
    "Si": "Wu", "You": "Wu", "Chou": "Wu",
    "Shen": "Mao", "Zi": "Mao", "Chen": "Mao",
    "Hai": "You", "Mao": "You", "Wei": "You",
}


def check_zai_sha(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = ZAI_SHA_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Disaster Star", name_chinese="灾煞",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Zai Sha at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "safety"], severity="severe" if present else "mild",
    )]


# =============================================================================
# 24. 天罗地网 (Tian Luo Di Wang / Heaven's Net and Earth's Snare)
# =============================================================================

def check_tian_luo_di_wang(chart: ChartData) -> List[ShenShaResult]:
    results = []
    natal_branches = [chart.pillars[p].branch for p in ["year", "month", "day", "hour"]]

    # 天罗 at 戌/亥, 地网 at 辰/巳
    tian_luo = {"Xu", "Hai"}
    di_wang = {"Chen", "Si"}

    for br in natal_branches:
        if br in tian_luo:
            pos = [p for p in ["year", "month", "day", "hour"]
                   if chart.pillars[p].branch == br][0]
            results.append(ShenShaResult(
                name_english="Heaven's Net", name_chinese="天罗",
                present=True, location=br, palace=pos,
                derivation=f"{BRANCHES[br]['chinese']} in {pos} palace = Heaven's Net (天罗).",
                nature="inauspicious", life_areas=["legal", "relationship"],
                severity="moderate",
            ))
        if br in di_wang:
            pos = [p for p in ["year", "month", "day", "hour"]
                   if chart.pillars[p].branch == br][0]
            results.append(ShenShaResult(
                name_english="Earth's Snare", name_chinese="地网",
                present=True, location=br, palace=pos,
                derivation=f"{BRANCHES[br]['chinese']} in {pos} palace = Earth's Snare (地网).",
                nature="inauspicious", life_areas=["legal", "relationship"],
                severity="moderate",
            ))

    if not results:
        results.append(ShenShaResult(
            name_english="Heaven's Net / Earth's Snare", name_chinese="天罗地网",
            present=False,
            derivation="No 辰巳 (Earth's Snare) or 戌亥 (Heaven's Net) in natal branches.",
        ))
    return results


# =============================================================================
# 25. 阴差阳错 (Yin Cha Yang Cuo / Yin-Yang Disharmony Day)
# =============================================================================

YIN_CHA_YANG_CUO_DAYS = {
    ("Bing", "Zi"), ("Bing", "Wu"), ("Ding", "Chou"), ("Ding", "Wei"),
    ("Wu", "Yin"), ("Wu", "Shen"), ("Xin", "Mao"), ("Xin", "You"),
    ("Ren", "Chen"), ("Ren", "Xu"), ("Gui", "Si"), ("Gui", "Hai"),
}


def check_yin_cha_yang_cuo(chart: ChartData) -> List[ShenShaResult]:
    day_stem = chart.pillars["day"].stem
    day_branch = chart.pillars["day"].branch
    present = (day_stem, day_branch) in YIN_CHA_YANG_CUO_DAYS
    return [ShenShaResult(
        name_english="Yin-Yang Disharmony Day", name_chinese="阴差阳错",
        present=present,
        derivation=f"Day Pillar {STEMS[day_stem]['chinese']}{BRANCHES[day_branch]['chinese']}: "
                   f"{'IS' if present else 'is NOT'} a Yin-Yang Disharmony day.",
        nature="inauspicious" if present else "neutral",
        life_areas=["marriage", "relationship"],
        severity="critical" if present else "mild",
    )]


# =============================================================================
# 26. 孤辰 (Gu Chen / Lonely Star)
# =============================================================================

GU_CHEN_LOOKUP: Dict[str, str] = {
    "Zi": "Yin", "Chou": "Yin", "Hai": "Yin",
    "Yin": "Si", "Mao": "Si", "Chen": "Si",
    "Si": "Shen", "Wu": "Shen", "Wei": "Shen",
    "Shen": "Hai", "You": "Hai", "Xu": "Hai",
}


def check_gu_chen(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = GU_CHEN_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Lonely Star", name_chinese="孤辰",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        activated_by=locs[0]["activated_by"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Gu Chen at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["relationship", "family"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 27. 寡宿 (Gua Su / Widow Star)
# =============================================================================

GUA_SU_LOOKUP: Dict[str, str] = {
    "Zi": "Xu", "Chou": "Xu", "Hai": "Xu",
    "Yin": "Chou", "Mao": "Chou", "Chen": "Chou",
    "Si": "Chen", "Wu": "Chen", "Wei": "Chen",
    "Shen": "Wei", "You": "Wei", "Xu": "Wei",
}


def check_gua_su(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = GUA_SU_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Widow Star", name_chinese="寡宿",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Gua Su at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["relationship"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 28. 四废 (Si Fei / Four Wastes)
# =============================================================================

SI_FEI_DAYS: Dict[str, set] = {
    "Spring": {("Geng", "Shen"), ("Xin", "You")},     # Metal dead in Spring
    "Summer": {("Ren", "Zi"), ("Gui", "Hai")},         # Water dead in Summer
    "Autumn": {("Jia", "Yin"), ("Yi", "Mao")},         # Wood dead in Autumn
    "Winter": {("Bing", "Wu"), ("Ding", "Si")},        # Fire dead in Winter
}


def check_si_fei(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    season = BRANCHES[month_branch]["season"]
    day_pair = (chart.pillars["day"].stem, chart.pillars["day"].branch)
    waste_days = SI_FEI_DAYS.get(season, set())
    present = day_pair in waste_days
    return [ShenShaResult(
        name_english="Four Wastes", name_chinese="四废",
        present=present,
        derivation=f"Born in {season} ({BRANCHES[month_branch]['chinese']} month). "
                   f"Day Pillar {STEMS[day_pair[0]]['chinese']}{BRANCHES[day_pair[1]]['chinese']}: "
                   f"{'IS' if present else 'is NOT'} a Four Wastes day.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "general"], severity="severe" if present else "mild",
    )]


# =============================================================================
# 29. 十恶大败 (Shi E Da Bai / Ten Evils Great Defeat)
# =============================================================================

SHI_E_DA_BAI_DAYS = {
    ("Jia", "Chen"), ("Yi", "Si"), ("Bing", "Shen"), ("Ding", "Hai"),
    ("Wu", "Xu"), ("Ji", "Chou"), ("Geng", "Chen"), ("Xin", "Si"),
    ("Ren", "Shen"), ("Gui", "Hai"),
}


def check_shi_e_da_bai(chart: ChartData) -> List[ShenShaResult]:
    day_pair = (chart.pillars["day"].stem, chart.pillars["day"].branch)
    present = day_pair in SHI_E_DA_BAI_DAYS
    return [ShenShaResult(
        name_english="Ten Evils Great Defeat", name_chinese="十恶大败",
        present=present,
        derivation=f"Day Pillar {STEMS[day_pair[0]]['chinese']}{BRANCHES[day_pair[1]]['chinese']}: "
                   f"{'IS' if present else 'is NOT'} a Ten Evils day.",
        nature="inauspicious" if present else "neutral",
        life_areas=["wealth", "general"], severity="severe" if present else "mild",
    )]


# =============================================================================
# 30. 魁罡 (Kui Gang)
# =============================================================================

KUI_GANG_DAYS = {
    ("Ren", "Chen"), ("Geng", "Chen"), ("Geng", "Xu"), ("Wu", "Xu"),
}


def check_kui_gang(chart: ChartData) -> List[ShenShaResult]:
    day_pair = (chart.pillars["day"].stem, chart.pillars["day"].branch)
    present = day_pair in KUI_GANG_DAYS
    return [ShenShaResult(
        name_english="Kui Gang", name_chinese="魁罡",
        present=present,
        derivation=f"Day Pillar {STEMS[day_pair[0]]['chinese']}{BRANCHES[day_pair[1]]['chinese']}: "
                   f"{'IS' if present else 'is NOT'} a Kui Gang day.",
        nature="mixed" if present else "neutral",
        life_areas=["career", "authority", "marriage"],
        severity="moderate" if present else "mild",
    )]


# =============================================================================
# 31. 血刃 (Xue Ren / Blood Blade)
# =============================================================================

XUE_REN_LOOKUP: Dict[str, str] = {
    "Jia": "Mao", "Yi": "Chen", "Bing": "Wu", "Ding": "Wei",
    "Wu": "Wu", "Ji": "Wei", "Geng": "You", "Xin": "Xu",
    "Ren": "Zi", "Gui": "Chou",
}


def check_xue_ren(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = XUE_REN_LOOKUP.get(dm)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Blood Blade", name_chinese="血刃",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {dm} DM: Blood Blade at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 32. 勾绞 (Gou Jiao / Hook and Strangle)
# =============================================================================

def check_gou_jiao(chart: ChartData) -> List[ShenShaResult]:
    year_idx = BRANCHES[chart.pillars["year"].branch]["index"]
    gou_idx = (year_idx + 1) % 12  # Hook = year + 1
    jiao_idx = (year_idx - 1) % 12  # Strangle = year - 1
    gou_branch = BRANCH_ORDER[gou_idx]
    jiao_branch = BRANCH_ORDER[jiao_idx]

    results = []
    for target, label, cn in [(gou_branch, "Hook", "勾"),
                               (jiao_branch, "Strangle", "绞")]:
        locs = _find_branch(chart, target)
        present = len(locs) > 0
        if present:
            results.append(ShenShaResult(
                name_english=f"{label} Star", name_chinese=cn,
                present=True, location=target, palace=locs[0]["palace"],
                activated_by=locs[0]["activated_by"],
                derivation=f"Year {chart.pillars['year'].branch_chinese}: "
                           f"{label} at {BRANCHES[target]['chinese']}. PRESENT.",
                nature="inauspicious", life_areas=["legal", "disputes"],
                severity="moderate",
            ))
    if not results:
        results.append(ShenShaResult(
            name_english="Hook and Strangle", name_chinese="勾绞",
            present=False,
            derivation=f"Hook at {BRANCHES[gou_branch]['chinese']}, "
                       f"Strangle at {BRANCHES[jiao_branch]['chinese']}. Both ABSENT.",
        ))
    return results


# =============================================================================
# 33. 丧门 (Sang Men / Funeral Door)
# =============================================================================

def check_sang_men(chart: ChartData) -> List[ShenShaResult]:
    year_idx = BRANCHES[chart.pillars["year"].branch]["index"]
    target_idx = (year_idx + 2) % 12
    target = BRANCH_ORDER[target_idx]
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Funeral Door", name_chinese="丧门",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"Year + 2 positions = {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "family"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 34. 吊客 (Diao Ke / Hanging Guest)
# =============================================================================

def check_diao_ke(chart: ChartData) -> List[ShenShaResult]:
    year_idx = BRANCHES[chart.pillars["year"].branch]["index"]
    target_idx = (year_idx - 2) % 12
    target = BRANCH_ORDER[target_idx]
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Hanging Guest", name_chinese="吊客",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"Year - 2 positions = {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "family"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 35. 咸池 (Xian Chi / Salty Pool)
# =============================================================================

XIAN_CHI_LOOKUP: Dict[str, str] = {
    "Jia": "You", "Yi": "You", "Bing": "Zi", "Ding": "Zi",
    "Wu": "Zi", "Ji": "Zi", "Geng": "Mao", "Xin": "Mao",
    "Ren": "Wu", "Gui": "Wu",
}


def check_xian_chi(chart: ChartData) -> List[ShenShaResult]:
    dm = chart.day_master
    target = XIAN_CHI_LOOKUP.get(dm)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="Salty Pool", name_chinese="咸池",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {dm} DM: Xian Chi at {BRANCHES[target]['chinese']}. "
                   f"{'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["relationship"], severity="moderate" if present else "mild",
    )]


# =============================================================================
# 36. 白虎 (Bai Hu / White Tiger)
# =============================================================================

BAI_HU_LOOKUP: Dict[str, str] = {
    "Zi": "Wu", "Chou": "Wei", "Yin": "Shen", "Mao": "You",
    "Chen": "Xu", "Si": "Hai", "Wu": "Zi", "Wei": "Chou",
    "Shen": "Yin", "You": "Mao", "Xu": "Chen", "Hai": "Si",
}


def check_bai_hu(chart: ChartData) -> List[ShenShaResult]:
    year_branch = chart.pillars["year"].branch
    target = BAI_HU_LOOKUP.get(year_branch)
    if not target:
        return []
    locs = _find_branch(chart, target)
    present = len(locs) > 0
    return [ShenShaResult(
        name_english="White Tiger", name_chinese="白虎",
        present=present, location=target,
        palace=locs[0]["palace"] if present else None,
        derivation=f"For {BRANCHES[year_branch]['chinese']} year: Bai Hu at "
                   f"{BRANCHES[target]['chinese']}. {'PRESENT' if present else 'ABSENT'}.",
        nature="inauspicious" if present else "neutral",
        life_areas=["health", "safety"], severity="severe" if present else "mild",
    )]


# =============================================================================
# 37. 童子 (Tong Zi / Child Star)
# =============================================================================

TONG_ZI_SEASON_LOOKUP: Dict[str, Tuple[str, str]] = {
    "Spring": ("Yin", "Zi"),
    "Summer": ("Mao", "Wei"),
    "Autumn": ("Yin", "Zi"),
    "Winter": ("Mao", "Wei"),
}

TONG_ZI_ELEMENT_LOOKUP: Dict[str, Tuple[str, str]] = {
    "Metal": ("Wu", "Mao"),
    "Wood": ("Wu", "Mao"),
    "Water": ("You", "Xu"),
    "Fire": ("You", "Xu"),
    "Earth": ("Chen", "Si"),
}


def check_tong_zi(chart: ChartData) -> List[ShenShaResult]:
    month_branch = chart.pillars["month"].branch
    season = BRANCHES[month_branch]["season"]
    dm_element = chart.dm_element

    natal_branches = {chart.pillars[p].branch for p in ["year", "month", "day", "hour"]}

    # Check by season
    season_targets = TONG_ZI_SEASON_LOOKUP.get(season, ())
    # Check by DM element
    element_targets = TONG_ZI_ELEMENT_LOOKUP.get(dm_element, ())

    all_targets = set(season_targets) | set(element_targets)
    found_in = all_targets & natal_branches

    if found_in:
        target = list(found_in)[0]
        pos = [p for p in ["year", "month", "day", "hour"]
               if chart.pillars[p].branch == target][0]
        return [ShenShaResult(
            name_english="Child Star", name_chinese="童子",
            present=True, location=target, palace=pos,
            derivation=f"Born in {season}, DM element {dm_element}. "
                       f"Check for {', '.join(BRANCHES[t]['chinese'] for t in all_targets)}. "
                       f"{BRANCHES[target]['chinese']} found in {pos}.",
            nature="inauspicious",
            life_areas=["marriage", "health", "children"],
            severity="moderate",
        )]
    return [ShenShaResult(
        name_english="Child Star", name_chinese="童子",
        present=False,
        derivation=f"Born in {season}, DM element {dm_element}. "
                   f"Check for {', '.join(BRANCHES[t]['chinese'] for t in all_targets)}. None found.",
    )]


# =============================================================================
# MASTER FUNCTION: Run All Shen Sha Checks
# =============================================================================

ALL_CHECKS = [
    check_tian_yi,
    check_tai_ji,
    check_tian_de,
    check_yue_de,
    check_wen_chang,
    check_jin_yu,
    check_tian_chu,
    check_lu_shen,
    check_jiang_xing,
    check_tian_yi_doctor,
    check_tian_she,
    check_hong_luan,
    check_tian_xi,
    check_fu_xing,
    check_san_qi,
    check_yang_ren,
    check_kong_wang,
    check_tao_hua,
    check_hua_gai,
    check_yi_ma,
    check_jie_sha,
    check_wang_shen,
    check_zai_sha,
    check_tian_luo_di_wang,
    check_yin_cha_yang_cuo,
    check_gu_chen,
    check_gua_su,
    check_si_fei,
    check_shi_e_da_bai,
    check_kui_gang,
    check_xue_ren,
    check_gou_jiao,
    check_sang_men,
    check_diao_ke,
    check_xian_chi,
    check_bai_hu,
    check_tong_zi,
]


def run_all_shen_sha(chart: ChartData) -> List[ShenShaResult]:
    """Run all 37 Shen Sha checks and return combined results."""
    results = []
    void_branches = get_void_branches(chart)

    for check_fn in ALL_CHECKS:
        star_results = check_fn(chart)
        # Mark void status
        for r in star_results:
            if r.present and r.location and r.location in void_branches:
                r.is_void = True
        results.extend(star_results)
    return results


def get_present_shen_sha(chart: ChartData) -> List[ShenShaResult]:
    """Return only present/activated Shen Sha stars."""
    return [r for r in run_all_shen_sha(chart) if r.present]


def get_absent_critical_shen_sha(chart: ChartData) -> List[ShenShaResult]:
    """Return absent Shen Sha that would have been important for this chart."""
    all_results = run_all_shen_sha(chart)
    # Stars whose absence is notable
    critical_names = {"禄神", "天医", "天德贵人", "天赦", "将星", "文昌贵人", "福星贵人"}
    return [r for r in all_results
            if not r.present and r.name_chinese in critical_names]
