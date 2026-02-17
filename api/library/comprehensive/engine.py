# =============================================================================
# COMPREHENSIVE BAZI ENGINE — Main Entry Point
# =============================================================================
# Provides the primary interface for constructing ChartData from pillar inputs
# and generating complete reports.
# =============================================================================

from typing import List, Dict, Optional, Tuple
from ..core import STEMS, BRANCHES
from ..derived import get_all_branch_qi, STEM_ORDER, BRANCH_ORDER
from .models import ChartData, Pillar, LuckPillarInfo
from .report import generate_comprehensive_report


def build_chart(
    gender: str,
    birth_year: int,
    year_stem: str, year_branch: str,
    month_stem: str, month_branch: str,
    day_stem: str, day_branch: str,
    hour_stem: str, hour_branch: str,
    luck_pillar_stem: str = "",
    luck_pillar_branch: str = "",
    luck_pillars: Optional[List[dict]] = None,
    current_year: int = 0,
    annual_stem: str = "", annual_branch: str = "",
    monthly_stem: str = "", monthly_branch: str = "",
    daily_stem: str = "", daily_branch: str = "",
    hourly_stem: str = "", hourly_branch: str = "",
) -> ChartData:
    """
    Build a ChartData object from raw pillar inputs.

    Args:
        gender: "male" or "female"
        birth_year: Gregorian birth year
        year/month/day/hour_stem: Pinyin stem IDs (e.g., "Jia", "Yi")
        year/month/day/hour_branch: Pinyin branch IDs (e.g., "Zi", "Chou")
        luck_pillar_stem/branch: Current luck pillar (optional)
        luck_pillars: List of dicts with keys: stem, branch, start_age, end_age, start_year, end_year
        current_year: Override current year (0 = auto-detect)
    """
    from datetime import datetime
    if current_year == 0:
        current_year = datetime.now().year

    age = current_year - birth_year

    # Build pillar objects
    pillars = {}
    for pos, stem, branch in [
        ("year", year_stem, year_branch),
        ("month", month_stem, month_branch),
        ("day", day_stem, day_branch),
        ("hour", hour_stem, hour_branch),
    ]:
        qi = get_all_branch_qi(branch)
        pillars[pos] = Pillar(
            position=pos,
            stem=stem,
            branch=branch,
            stem_chinese=STEMS[stem]["chinese"],
            branch_chinese=BRANCHES[branch]["chinese"],
            stem_element=STEMS[stem]["element"],
            stem_polarity=STEMS[stem]["polarity"],
            branch_element=BRANCHES[branch]["element"],
            branch_polarity=BRANCHES[branch]["polarity"],
            hidden_stems=qi,
        )

    # Build luck pillar
    lp = None
    if luck_pillar_stem and luck_pillar_branch:
        lp_qi = get_all_branch_qi(luck_pillar_branch)
        lp = Pillar(
            position="luck_pillar",
            stem=luck_pillar_stem,
            branch=luck_pillar_branch,
            stem_chinese=STEMS[luck_pillar_stem]["chinese"],
            branch_chinese=BRANCHES[luck_pillar_branch]["chinese"],
            stem_element=STEMS[luck_pillar_stem]["element"],
            stem_polarity=STEMS[luck_pillar_stem]["polarity"],
            branch_element=BRANCHES[luck_pillar_branch]["element"],
            branch_polarity=BRANCHES[luck_pillar_branch]["polarity"],
            hidden_stems=lp_qi,
        )

    # Build luck pillars list
    lp_list = []
    if luck_pillars:
        for lp_data in luck_pillars:
            from ..derived import get_ten_god
            stem = lp_data["stem"]
            branch = lp_data["branch"]
            tg = get_ten_god(day_stem, stem)
            lp_info = LuckPillarInfo(
                stem=stem,
                branch=branch,
                stem_chinese=STEMS[stem]["chinese"],
                branch_chinese=BRANCHES[branch]["chinese"],
                start_age=lp_data.get("start_age", 0),
                end_age=lp_data.get("end_age", 0),
                start_year=lp_data.get("start_year", 0),
                end_year=lp_data.get("end_year", 0),
                stem_ten_god=tg[0] if tg else "",
                stem_ten_god_chinese=tg[2] if tg else "",
                is_current=(luck_pillar_stem == stem and luck_pillar_branch == branch),
                hidden_stems=get_all_branch_qi(branch),
            )
            lp_list.append(lp_info)

    # Build time-period pillars
    tp_pillars = {}
    for tp_pos, tp_stem, tp_branch in [
        ("annual", annual_stem, annual_branch),
        ("monthly", monthly_stem, monthly_branch),
        ("daily", daily_stem, daily_branch),
        ("hourly", hourly_stem, hourly_branch),
    ]:
        if tp_stem and tp_branch:
            tp_qi = get_all_branch_qi(tp_branch)
            tp_pillars[tp_pos] = Pillar(
                position=tp_pos,
                stem=tp_stem,
                branch=tp_branch,
                stem_chinese=STEMS[tp_stem]["chinese"],
                branch_chinese=BRANCHES[tp_branch]["chinese"],
                stem_element=STEMS[tp_stem]["element"],
                stem_polarity=STEMS[tp_stem]["polarity"],
                branch_element=BRANCHES[tp_branch]["element"],
                branch_polarity=BRANCHES[tp_branch]["polarity"],
                hidden_stems=tp_qi,
            )

    # Day Master info
    dm = day_stem
    dm_info = STEMS[dm]

    # Current year stems
    cy_stem_idx = (current_year - 4) % 10
    cy_branch_idx = (current_year - 4) % 12

    chart = ChartData(
        gender=gender.lower(),
        birth_year=birth_year,
        age=age,
        pillars=pillars,
        day_master=dm,
        dm_element=dm_info["element"],
        dm_polarity=dm_info["polarity"],
        dm_chinese=dm_info["chinese"],
        luck_pillar=lp,
        luck_pillars=lp_list,
        time_period_pillars=tp_pillars,
        current_year_stem=STEM_ORDER[cy_stem_idx],
        current_year_branch=BRANCH_ORDER[cy_branch_idx],
    )

    return chart


def analyze_for_api(chart: ChartData) -> dict:
    """
    Run full analysis and return all intermediate results (not just markdown).
    Used by the /api/analyze_bazi adapter.
    """
    from .ten_gods import map_all_ten_gods, classify_ten_god_strength
    from .strength import assess_day_master_strength
    from .interactions import detect_all_interactions
    from .shen_sha import run_all_shen_sha
    from .predictions import run_all_predictions
    from .environment import assess_environment

    strength = assess_day_master_strength(chart)
    tg_entries = map_all_ten_gods(chart)
    tg_classification = classify_ten_god_strength(tg_entries)
    interactions = detect_all_interactions(chart)
    shen_sha = run_all_shen_sha(chart)
    predictions = run_all_predictions(chart)
    env = assess_environment(chart, strength)
    comprehensive_report = generate_comprehensive_report(chart)

    return {
        "strength": strength,
        "ten_god_entries": tg_entries,
        "ten_god_classification": tg_classification,
        "interactions": interactions,
        "shen_sha": shen_sha,
        "predictions": predictions,
        "environment": env,
        "comprehensive_report": comprehensive_report,
    }


def analyze(
    gender: str,
    birth_year: int,
    year_stem: str, year_branch: str,
    month_stem: str, month_branch: str,
    day_stem: str, day_branch: str,
    hour_stem: str, hour_branch: str,
    luck_pillar_stem: str = "",
    luck_pillar_branch: str = "",
    luck_pillars: Optional[List[dict]] = None,
    current_year: int = 0,
) -> str:
    """
    One-call comprehensive BaZi analysis.
    Returns complete markdown report.
    """
    chart = build_chart(
        gender=gender,
        birth_year=birth_year,
        year_stem=year_stem, year_branch=year_branch,
        month_stem=month_stem, month_branch=month_branch,
        day_stem=day_stem, day_branch=day_branch,
        hour_stem=hour_stem, hour_branch=hour_branch,
        luck_pillar_stem=luck_pillar_stem,
        luck_pillar_branch=luck_pillar_branch,
        luck_pillars=luck_pillars,
        current_year=current_year,
    )
    return generate_comprehensive_report(chart)
