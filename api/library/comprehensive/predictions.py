# =============================================================================
# EVENT PREDICTION ENGINE
# =============================================================================
# Year-by-year scoring for major life events:
#   - Marriage timing
#   - Divorce risk
#   - Children arrival
#   - Career peaks/changes
# Uses natal chart, luck pillars, and annual pillar interactions.
# =============================================================================

from typing import List, Dict, Tuple, Optional
from ..core import STEMS, BRANCHES
from ..derived import (
    ELEMENT_CYCLES, get_ten_god, get_all_branch_qi,
    STEM_ORDER, BRANCH_ORDER
)
from .models import EventPrediction, ChartData, LuckPillarInfo
from .shen_sha import HONG_LUAN_LOOKUP, TIAN_XI_LOOKUP, TAO_HUA_LOOKUP, _xun_void_branches


# =============================================================================
# ANNUAL PILLAR CALCULATOR
# =============================================================================

def get_annual_pillar(year: int) -> Tuple[str, str]:
    """Calculate the Heavenly Stem and Earthly Branch for a given year."""
    stem_idx = (year - 4) % 10
    branch_idx = (year - 4) % 12
    return STEM_ORDER[stem_idx], BRANCH_ORDER[branch_idx]


# =============================================================================
# CLASH DETECTION HELPERS
# =============================================================================

CLASH_MAP = {b: BRANCHES[b]["clashes"] for b in BRANCHES}
HARMONY_MAP = {b: BRANCHES[b]["harmonizes"] for b in BRANCHES}


def _branches_clash(b1: str, b2: str) -> bool:
    return CLASH_MAP.get(b1) == b2


def _branches_harmonize(b1: str, b2: str) -> bool:
    return HARMONY_MAP.get(b1) == b2


# =============================================================================
# MARRIAGE TIMING PREDICTOR
# =============================================================================

def predict_marriage_years(chart: ChartData, start_year: int = 0,
                           end_year: int = 0) -> List[EventPrediction]:
    """
    Score each year for marriage probability.
    Factors:
    1. Hong Luan (红鸾) or Tian Xi (天喜) activated by annual branch
    2. Peach Blossom activated by annual branch
    3. Spouse Palace (Day Branch) harmonized or clashed by annual branch
    4. Spouse star (DW for male, DO for female) appearing in annual stem
    5. Luck pillar alignment
    6. Cultural age window bonus
    """
    if start_year == 0:
        start_year = chart.birth_year + 18
    if end_year == 0:
        end_year = chart.birth_year + 55

    dm = chart.day_master
    day_branch = chart.pillars["day"].branch
    year_branch = chart.pillars["year"].branch

    # Spouse star for this gender
    spouse_star_abbr = "DW" if chart.gender == "male" else "DO"

    # Hong Luan and Tian Xi targets
    hl_target = HONG_LUAN_LOOKUP.get(year_branch)
    tx_target = TIAN_XI_LOOKUP.get(year_branch)

    # Peach Blossom targets
    pb_targets = set()
    for base in ["year", "day"]:
        base_br = chart.pillars[base].branch
        pb = TAO_HUA_LOOKUP.get(base_br)
        if pb:
            pb_targets.add(pb)

    results = []

    for year in range(start_year, end_year + 1):
        age = year - chart.birth_year
        score = 0.0
        factors = []

        annual_stem, annual_branch = get_annual_pillar(year)

        # 1. Hong Luan activated
        if annual_branch == hl_target:
            score += 25
            factors.append("Hong Luan (红鸾) activated")

        # 2. Tian Xi activated
        if annual_branch == tx_target:
            score += 20
            factors.append("Tian Xi (天喜) activated")

        # 3. Peach Blossom activated
        if annual_branch in pb_targets:
            score += 15
            factors.append("Peach Blossom (桃花) activated")

        # 4. Spouse palace (day branch) harmonized
        if _branches_harmonize(day_branch, annual_branch):
            score += 20
            factors.append("Spouse palace harmonized by annual branch")

        # 5. Spouse palace clashed (can trigger marriage OR separation)
        if _branches_clash(day_branch, annual_branch):
            score += 10
            factors.append("Spouse palace clashed (can trigger marriage event)")

        # 6. Spouse star in annual stem
        tg = get_ten_god(dm, annual_stem)
        if tg and tg[0] == spouse_star_abbr:
            score += 20
            factors.append(f"Spouse star ({spouse_star_abbr}) in annual stem")

        # 7. Spouse star in annual branch hidden stems
        for hs, qs in get_all_branch_qi(annual_branch):
            tg = get_ten_god(dm, hs)
            if tg and tg[0] == spouse_star_abbr:
                score += 10
                factors.append(f"Spouse star in annual branch hidden stem")
                break

        # 8. Cultural age window
        if chart.gender == "male":
            if 26 <= age <= 33:
                score += 10
                factors.append("Prime marriage age window (male 26-33)")
            elif 22 <= age <= 25:
                score += 5
        else:
            if 23 <= age <= 29:
                score += 10
                factors.append("Prime marriage age window (female 23-29)")
            elif 20 <= age <= 22:
                score += 5

        # 9. Check luck pillar alignment
        for lp in chart.luck_pillars:
            if lp.start_year <= year <= lp.end_year:
                lp_tg = get_ten_god(dm, lp.stem)
                if lp_tg and lp_tg[0] == spouse_star_abbr:
                    score += 10
                    factors.append(f"Luck pillar stem = spouse star")
                if _branches_harmonize(day_branch, lp.branch):
                    score += 5
                    factors.append(f"Luck pillar harmonizes spouse palace")
                break

        if score >= 20:
            results.append(EventPrediction(
                event_type="marriage",
                year=year,
                age=age,
                score=round(score, 1),
                factors=factors,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


# =============================================================================
# DIVORCE RISK PREDICTOR
# =============================================================================

def predict_divorce_years(chart: ChartData, start_year: int = 0,
                          end_year: int = 0) -> List[EventPrediction]:
    """
    Score each year for divorce/separation risk.
    Factors:
    1. Spouse palace clashed by annual branch
    2. Rob Wealth in annual stem (steals spouse)
    3. Hurting Officer in annual stem (female: destroys husband star)
    4. Punishment involving spouse palace
    5. Void on spouse palace activated
    """
    if start_year == 0:
        start_year = chart.birth_year + 20
    if end_year == 0:
        end_year = chart.birth_year + 60

    dm = chart.day_master
    day_branch = chart.pillars["day"].branch

    results = []

    for year in range(start_year, end_year + 1):
        age = year - chart.birth_year
        score = 0.0
        factors = []

        annual_stem, annual_branch = get_annual_pillar(year)

        # 1. Spouse palace clashed
        if _branches_clash(day_branch, annual_branch):
            score += 25
            factors.append("Spouse palace directly clashed")

        # 2. Rob Wealth in annual stem
        tg = get_ten_god(dm, annual_stem)
        if tg and tg[0] == "RW":
            score += 20
            factors.append("Rob Wealth appears (competitor for spouse)")

        # 3. Hurting Officer (especially bad for females)
        if tg and tg[0] == "HO":
            bonus = 20 if chart.gender == "female" else 10
            score += bonus
            factors.append("Hurting Officer appears (damages marriage structure)")

        # 4. Seven Killings for females (rival male)
        if chart.gender == "female" and tg and tg[0] == "7K":
            score += 10
            factors.append("Seven Killings appears (rival/affair indicator)")

        # 5. Check punishment patterns with annual branch
        natal_branches = [chart.pillars[p].branch for p in ["year", "month", "day", "hour"]]
        punishment_check = set(natal_branches) | {annual_branch}

        # Ungrateful punishment (Yin-Si-Shen)
        ungrateful = {"Yin", "Si", "Shen"}
        if len(ungrateful & punishment_check) >= 3 and annual_branch in ungrateful:
            score += 15
            factors.append("Ungrateful punishment activated")

        # Bullying punishment (Chou-Wei-Xu)
        bullying = {"Chou", "Wei", "Xu"}
        if len(bullying & punishment_check) >= 3 and annual_branch in bullying:
            score += 15
            factors.append("Bullying punishment activated")

        # 6. Luck pillar clash on spouse palace
        for lp in chart.luck_pillars:
            if lp.start_year <= year <= lp.end_year:
                if _branches_clash(day_branch, lp.branch):
                    score += 15
                    factors.append("Luck pillar also clashes spouse palace")
                break

        if score >= 20:
            results.append(EventPrediction(
                event_type="divorce",
                year=year,
                age=age,
                score=round(score, 1),
                factors=factors,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


# =============================================================================
# CHILDREN ARRIVAL PREDICTOR
# =============================================================================

def predict_children_years(chart: ChartData, start_year: int = 0,
                           end_year: int = 0) -> List[EventPrediction]:
    """
    Score each year for children arrival probability.
    Male: 7K = sons, DO = daughters
    Female: HO = sons, EG = daughters
    """
    if start_year == 0:
        start_year = chart.birth_year + 20
    if end_year == 0:
        end_year = chart.birth_year + 50

    dm = chart.day_master
    hour_branch = chart.pillars["hour"].branch

    # Children star mapping
    if chart.gender == "male":
        child_stars = {"7K", "DO"}
    else:
        child_stars = {"HO", "EG"}

    results = []

    for year in range(start_year, end_year + 1):
        age = year - chart.birth_year
        score = 0.0
        factors = []

        annual_stem, annual_branch = get_annual_pillar(year)

        # 1. Children star in annual stem
        tg = get_ten_god(dm, annual_stem)
        if tg and tg[0] in child_stars:
            score += 25
            factors.append(f"Children star ({tg[0]}) in annual stem")

        # 2. Children star in annual branch hidden stems
        for hs, qs in get_all_branch_qi(annual_branch):
            tg_h = get_ten_god(dm, hs)
            if tg_h and tg_h[0] in child_stars:
                score += 10
                factors.append(f"Children star in annual branch")
                break

        # 3. Hour palace (children palace) harmonized
        if _branches_harmonize(hour_branch, annual_branch):
            score += 15
            factors.append("Children palace harmonized")

        # 4. Cultural age window
        if chart.gender == "male":
            if 27 <= age <= 36:
                score += 8
        else:
            if 24 <= age <= 33:
                score += 8

        # 5. Luck pillar alignment
        for lp in chart.luck_pillars:
            if lp.start_year <= year <= lp.end_year:
                lp_tg = get_ten_god(dm, lp.stem)
                if lp_tg and lp_tg[0] in child_stars:
                    score += 10
                    factors.append("Luck pillar stem = children star")
                break

        if score >= 20:
            results.append(EventPrediction(
                event_type="child_birth",
                year=year,
                age=age,
                score=round(score, 1),
                factors=factors,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


# =============================================================================
# CAREER PEAK PREDICTOR
# =============================================================================

def predict_career_years(chart: ChartData, start_year: int = 0,
                         end_year: int = 0) -> List[EventPrediction]:
    """
    Score each year for career advancement probability.
    """
    if start_year == 0:
        start_year = chart.birth_year + 20
    if end_year == 0:
        end_year = chart.birth_year + 65

    dm = chart.day_master

    results = []

    for year in range(start_year, end_year + 1):
        age = year - chart.birth_year
        score = 0.0
        factors = []

        annual_stem, annual_branch = get_annual_pillar(year)
        tg = get_ten_god(dm, annual_stem)

        # 1. Direct Officer in annual stem (promotion, recognition)
        if tg and tg[0] == "DO":
            score += 20
            factors.append("Direct Officer year (recognition, promotion)")

        # 2. Seven Killings in annual stem (power, but risky)
        if tg and tg[0] == "7K":
            score += 15
            factors.append("Seven Killings year (power grab, risk)")

        # 3. Indirect Wealth in annual stem (windfall, business)
        if tg and tg[0] == "IW":
            score += 15
            factors.append("Indirect Wealth year (windfall, opportunity)")

        # 4. Month pillar (career palace) harmonized
        month_branch = chart.pillars["month"].branch
        if _branches_harmonize(month_branch, annual_branch):
            score += 15
            factors.append("Career palace harmonized")

        # 5. Career palace clashed (career upheaval - can be promotion or loss)
        if _branches_clash(month_branch, annual_branch):
            score += 10
            factors.append("Career palace clashed (career change event)")

        # 6. Luck pillar alignment
        for lp in chart.luck_pillars:
            if lp.start_year <= year <= lp.end_year:
                lp_tg = get_ten_god(dm, lp.stem)
                if lp_tg and lp_tg[0] in ("DO", "7K", "IW"):
                    score += 10
                    factors.append(f"Luck pillar = {lp_tg[0]} (career energy)")
                break

        if score >= 20:
            results.append(EventPrediction(
                event_type="career_peak",
                year=year,
                age=age,
                score=round(score, 1),
                factors=factors,
            ))

    results.sort(key=lambda x: x.score, reverse=True)
    return results


# =============================================================================
# MASTER PREDICTION FUNCTION
# =============================================================================

def run_all_predictions(chart: ChartData) -> Dict[str, List[EventPrediction]]:
    """Run all prediction algorithms and return top results for each category."""
    return {
        "marriage": predict_marriage_years(chart)[:5],
        "divorce": predict_divorce_years(chart)[:5],
        "children": predict_children_years(chart)[:5],
        "career": predict_career_years(chart)[:5],
    }
