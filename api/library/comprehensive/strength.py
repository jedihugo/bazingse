# =============================================================================
# DAY MASTER STRENGTH ASSESSMENT ENGINE
# =============================================================================
# DM strength = DM's element percentage of total chart elements.
# ~20% = balanced (100% / 5 elements).
# Branch interactions adjust element weights before computing percentages.
# =============================================================================

from typing import List, Dict, Tuple, Optional
from ..core import STEMS, BRANCHES
from ..derived import (
    ELEMENT_CYCLES, get_all_branch_qi, get_ten_god,
    STEM_ORDER, BRANCH_ORDER
)
from ..seasonal import SEASONAL_ADJUSTMENT
from .models import StrengthAssessment, BranchInteraction, ChartData


# =============================================================================
# ELEMENT ROLE CLASSIFICATION
# =============================================================================

def _element_role(dm_element: str, target_element: str) -> str:
    """
    Classify an element's role relative to the Day Master's element.
    Returns: "support", "drain", or "neutral" (same=support via companion)
    """
    if target_element == dm_element:
        return "support"  # Same element = companions
    if ELEMENT_CYCLES["generated_by"].get(dm_element) == target_element:
        return "support"  # Resource (generates me)
    # Everything else drains: output, wealth, officer
    return "drain"


# =============================================================================
# SEASONAL QI STATE
# =============================================================================

def get_seasonal_state(chart: ChartData) -> str:
    """Get the Day Master's seasonal state based on month branch."""
    month_branch = chart.pillars["month"].branch
    dm_element = chart.dm_element
    states = BRANCHES[month_branch]["element_states"]
    return states.get(dm_element, "Resting")


def get_seasonal_multiplier(state: str) -> float:
    """Convert seasonal state to multiplier."""
    return SEASONAL_ADJUSTMENT.get(state.lower(), 1.0)


# =============================================================================
# ROOTING ANALYSIS
# =============================================================================

def check_rooting(chart: ChartData) -> dict:
    """
    Check if the Day Master has roots in the earthly branches.
    A root = the DM's element appearing in a branch's qi.
    Stronger roots = higher qi scores.
    """
    dm = chart.day_master
    dm_element = chart.dm_element
    roots = []

    for pos in ["year", "month", "day", "hour"]:
        branch = chart.pillars[pos].branch
        branch_qi = get_all_branch_qi(branch)
        for stem, score in branch_qi:
            if STEMS[stem]["element"] == dm_element:
                roots.append({
                    "position": pos,
                    "branch": branch,
                    "stem": stem,
                    "qi_score": score,
                    "is_exact": stem == dm,
                })

    total_root_score = sum(r["qi_score"] for r in roots)
    has_root = len(roots) > 0
    has_strong_root = any(r["qi_score"] >= 50 for r in roots)

    return {
        "roots": roots,
        "root_count": len(roots),
        "total_root_score": total_root_score,
        "has_root": has_root,
        "has_strong_root": has_strong_root,
    }


# =============================================================================
# ELEMENT COUNTING
# =============================================================================

def count_elements(chart: ChartData) -> Dict[str, float]:
    """
    Count all element weights in the natal chart.
    Visible stems count full weight (1.0).
    Hidden stems count proportionally based on qi score (score/100).
    """
    element_counts = {"Wood": 0.0, "Fire": 0.0, "Earth": 0.0, "Metal": 0.0, "Water": 0.0}

    for pos in ["year", "month", "day", "hour"]:
        pillar = chart.pillars[pos]

        # Heavenly stem = full weight
        stem_element = STEMS[pillar.stem]["element"]
        element_counts[stem_element] += 1.0

        # Branch qi = weighted by score
        branch_qi = get_all_branch_qi(pillar.branch)
        for stem, score in branch_qi:
            elem = STEMS[stem]["element"]
            element_counts[elem] += score / 100.0

    return element_counts


def count_all_elements(chart: ChartData) -> Dict[str, float]:
    """Count element weights across ALL pillars (natal + luck + time-period)."""
    element_counts = count_elements(chart)  # Start with natal

    # Add luck pillar
    if chart.luck_pillar:
        stem_element = STEMS[chart.luck_pillar.stem]["element"]
        element_counts[stem_element] += 1.0
        for stem, score in get_all_branch_qi(chart.luck_pillar.branch):
            element_counts[STEMS[stem]["element"]] += score / 100.0

    # Add time-period pillars
    for pos, pillar in chart.time_period_pillars.items():
        stem_element = STEMS[pillar.stem]["element"]
        element_counts[stem_element] += 1.0
        for stem, score in get_all_branch_qi(pillar.branch):
            element_counts[STEMS[stem]["element"]] += score / 100.0

    return element_counts


def count_support_vs_drain(chart: ChartData) -> Tuple[float, float]:
    """
    Count supporting vs draining element weights.
    Support = same element + resource element
    Drain = output + wealth + officer elements
    """
    dm_element = chart.dm_element
    resource_element = ELEMENT_CYCLES["generated_by"].get(dm_element)

    support = 0.0
    drain = 0.0

    for pos in ["year", "month", "day", "hour"]:
        pillar = chart.pillars[pos]

        # Heavenly stem
        stem_elem = STEMS[pillar.stem]["element"]
        if stem_elem == dm_element or stem_elem == resource_element:
            support += 1.0
        else:
            drain += 1.0

        # Branch qi
        branch_qi = get_all_branch_qi(pillar.branch)
        for stem, score in branch_qi:
            elem = STEMS[stem]["element"]
            weight = score / 100.0
            if elem == dm_element or elem == resource_element:
                support += weight
            else:
                drain += weight

    return support, drain


# =============================================================================
# INTERACTION-ADJUSTED ELEMENT COUNTING
# =============================================================================

# Bonuses for combinations that generate elements.
# Transformed = resulting element present as visible Heavenly Stem.
INTERACTION_BONUSES = {
    "directional_combo": {"transformed": 2.0, "combined": 0.8},
    "three_harmony":     {"transformed": 1.5, "combined": 0.6},
    "half_three_harmony": {"transformed": 0.3, "combined": 0.2},
    "harmony":           {"transformed": 0.5, "combined": 0.2},
}

CLASH_PENALTY = 0.3


def _get_resulting_element(interaction: BranchInteraction) -> Optional[str]:
    """Look up the resulting element for a combination interaction."""
    from .interactions import HARMONY_PAIRS, THREE_HARMONY_FRAMES, DIRECTIONAL_COMBOS

    itype = interaction.interaction_type
    branches_set = frozenset(interaction.branches)

    if itype == "directional_combo":
        info = DIRECTIONAL_COMBOS.get(branches_set)
        return info[0] if info else None
    elif itype == "three_harmony":
        return THREE_HARMONY_FRAMES.get(branches_set)
    elif itype == "half_three_harmony":
        for frame_set, elem in THREE_HARMONY_FRAMES.items():
            if branches_set.issubset(frame_set):
                return elem
        return None
    elif itype == "harmony":
        return HARMONY_PAIRS.get(branches_set)
    return None


def adjust_elements_for_interactions(
    element_counts: Dict[str, float],
    interactions: List[BranchInteraction],
    chart: ChartData,
) -> Dict[str, float]:
    """
    Adjust element counts based on branch interactions.
    Positive combinations add weight to the resulting element.
    Transformed (resulting element present as HS) = larger bonus.
    Clashes reduce both elements slightly.
    """
    adjusted = dict(element_counts)

    # Collect visible Heavenly Stem elements
    hs_elements = set()
    for pos in ["year", "month", "day", "hour"]:
        hs_elements.add(chart.pillars[pos].stem_element)

    for interaction in interactions:
        itype = interaction.interaction_type

        if itype in INTERACTION_BONUSES:
            resulting_element = _get_resulting_element(interaction)
            if resulting_element:
                transformed = resulting_element in hs_elements
                key = "transformed" if transformed else "combined"
                bonus = INTERACTION_BONUSES[itype][key]
                adjusted[resulting_element] = adjusted.get(resulting_element, 0) + bonus

        elif itype == "clash":
            for br in interaction.branches:
                elem = BRANCHES[br]["element"]
                adjusted[elem] = max(0, adjusted.get(elem, 0) - CLASH_PENALTY)

    return adjusted


# =============================================================================
# FOLLOWING CHART (从格) DETECTION
# =============================================================================

def detect_following_chart(chart: ChartData, support: float, drain: float,
                           seasonal_state: str, root_info: dict) -> Tuple[bool, Optional[str]]:
    """
    Detect if this is a Following Chart (从格).
    Conditions:
    - DM is extremely weak (very low support, no strong root)
    - No resource or companion stems in visible positions
    - Seasonal state is Trapped or Dead
    """
    dm = chart.day_master
    dm_element = chart.dm_element
    resource_element = ELEMENT_CYCLES["generated_by"].get(dm_element)

    # Check if DM has any visible support
    visible_support = 0
    for pos in ["year", "month", "hour"]:  # Skip day stem (that's the DM itself)
        stem_elem = STEMS[chart.pillars[pos].stem]["element"]
        if stem_elem == dm_element or stem_elem == resource_element:
            visible_support += 1

    # Following chart conditions
    if (visible_support == 0 and
        not root_info["has_strong_root"] and
        seasonal_state in ("Trapped", "Dead") and
        drain > support * 3):

        # Determine following type based on dominant drain
        element_counts = count_elements(chart)
        # Remove DM's own element count to see what dominates
        drain_elements = {}
        for elem, count in element_counts.items():
            if elem != dm_element and elem != resource_element:
                drain_elements[elem] = count

        if drain_elements:
            dominant = max(drain_elements, key=drain_elements.get)
            output_element = ELEMENT_CYCLES["generating"].get(dm_element)
            wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element)
            officer_element = ELEMENT_CYCLES["controlled_by"].get(dm_element)

            if dominant == output_element:
                return True, "output"
            elif dominant == wealth_element:
                return True, "wealth"
            elif dominant == officer_element:
                return True, "officer"
            return True, "mixed"

    return False, None


# =============================================================================
# USEFUL GOD (用神) DETERMINATION
# =============================================================================

def determine_useful_god(chart: ChartData, verdict: str,
                         is_following: bool, following_type: Optional[str]) -> dict:
    """
    Determine the Useful God (用神) and favorable/unfavorable elements.
    """
    dm_element = chart.dm_element
    resource_element = ELEMENT_CYCLES["generated_by"].get(dm_element)
    output_element = ELEMENT_CYCLES["generating"].get(dm_element)
    wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element)
    officer_element = ELEMENT_CYCLES["controlled_by"].get(dm_element)

    if is_following:
        # Following chart: go WITH the dominant force
        if following_type == "wealth":
            return {
                "useful_god": wealth_element,
                "favorable": [wealth_element, output_element, officer_element],
                "unfavorable": [dm_element, resource_element],
            }
        elif following_type == "officer":
            return {
                "useful_god": officer_element,
                "favorable": [officer_element, wealth_element, output_element],
                "unfavorable": [dm_element, resource_element],
            }
        elif following_type == "output":
            return {
                "useful_god": output_element,
                "favorable": [output_element, wealth_element],
                "unfavorable": [dm_element, resource_element, officer_element],
            }
        else:
            return {
                "useful_god": wealth_element,
                "favorable": [wealth_element, output_element],
                "unfavorable": [dm_element, resource_element],
            }

    if verdict in ("extremely_weak", "weak"):
        # Weak DM needs support: resource + companion
        return {
            "useful_god": resource_element,
            "favorable": [resource_element, dm_element],
            "unfavorable": [wealth_element, officer_element, output_element],
        }
    elif verdict in ("extremely_strong", "strong"):
        # Strong DM needs draining: output + wealth
        return {
            "useful_god": output_element,
            "favorable": [output_element, wealth_element, officer_element],
            "unfavorable": [dm_element, resource_element],
        }
    else:
        # Neutral: balanced, slight preference for balance
        return {
            "useful_god": output_element,
            "favorable": [output_element, wealth_element],
            "unfavorable": [officer_element],
        }


# =============================================================================
# MAIN STRENGTH ASSESSMENT
# =============================================================================

# Seasonal nudge on DM element percentage (small adjustments)
SEASONAL_NUDGE = {
    "Prosperous": 2.0,
    "Strengthening": 1.0,
    "Resting": 0.0,
    "Trapped": -1.0,
    "Dead": -2.0,
}

# Verdict thresholds (20% = balanced center)
VERDICT_THRESHOLDS = {
    "extremely_strong": 30.0,
    "strong": 24.0,
    "neutral_upper": 24.0,
    "neutral_lower": 16.0,
    "weak": 10.0,
}


def assess_day_master_strength(
    chart: ChartData,
    interactions: Optional[List[BranchInteraction]] = None,
) -> StrengthAssessment:
    """
    DM strength = DM's element percentage of total chart elements.
    ~20% = balanced. Branch interactions adjust element weights.
    """
    # 1. Count raw elements
    element_counts = count_elements(chart)

    # 2. Adjust for interactions (combinations add element weight, clashes reduce)
    if interactions:
        element_counts = adjust_elements_for_interactions(
            element_counts, interactions, chart)

    # 3. Calculate percentages
    total = sum(element_counts.values())
    if total > 0:
        percentages = {elem: (count / total) * 100 for elem, count in element_counts.items()}
    else:
        percentages = {elem: 20.0 for elem in element_counts}

    # 4. DM strength score = DM's element percentage (single source of truth)
    dm_element = chart.dm_element
    score = max(1.0, min(50.0, round(percentages[dm_element], 1)))

    # 5. Drain pressure: if drain elements individually exceed the DM,
    #    the DM is under pressure even at a "balanced" percentage.
    #    e.g., Wood 22% looks balanced, but Fire 40% + Earth 24% = heavy drain.
    output_elem = ELEMENT_CYCLES["generating"].get(dm_element, "")
    wealth_elem = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    officer_elem = ELEMENT_CYCLES["controlled_by"].get(dm_element, "")

    drain_pressure = 0.0
    for drain_elem in [output_elem, wealth_elem, officer_elem]:
        if drain_elem:
            excess = percentages.get(drain_elem, 0) - score
            if excess > 0:
                drain_pressure += excess

    # 6. Seasonal and root factors
    seasonal_state = get_seasonal_state(chart)
    root_info = check_rooting(chart)

    effective_pct = score + SEASONAL_NUDGE.get(seasonal_state, 0)
    if root_info["has_strong_root"]:
        effective_pct += 1.0
    elif not root_info["has_root"]:
        effective_pct -= 1.5

    # 7. Apply drain pressure — each point of excess reduces effective strength
    #    e.g., Fire 40% vs Wood 22% = 18 pts excess → heavy pressure on Wood
    effective_pct -= drain_pressure * 0.4

    # 8. Determine verdict using effective_pct (20% = balanced)
    if effective_pct >= 30.0:
        verdict = "extremely_strong"
    elif effective_pct >= 24.0:
        verdict = "strong"
    elif effective_pct >= 16.0:
        verdict = "neutral"
    elif effective_pct >= 10.0:
        verdict = "weak"
    else:
        verdict = "extremely_weak"

    # 9. Support/drain counts (kept for compatibility)
    support, drain = count_support_vs_drain(chart)

    # 10. Check for following chart
    is_following, following_type = detect_following_chart(
        chart, support, drain, seasonal_state, root_info)

    # 11. Determine useful god and elements
    god_info = determine_useful_god(chart, verdict, is_following, following_type)

    return StrengthAssessment(
        score=score,
        verdict=verdict,
        support_count=round(support, 2),
        drain_count=round(drain, 2),
        seasonal_state=seasonal_state,
        is_following_chart=is_following,
        following_type=following_type,
        useful_god=god_info["useful_god"],
        favorable_elements=god_info["favorable"],
        unfavorable_elements=god_info["unfavorable"],
        element_percentages={k: round(v, 1) for k, v in percentages.items()},
    )
