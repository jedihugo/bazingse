# =============================================================================
# TEN GODS (十神) COMPREHENSIVE MAPPING ENGINE
# =============================================================================
# Maps all Ten Gods across every visible stem and hidden stem in all pillars.
# Classifies each Ten God's strength in the chart.
# =============================================================================

from typing import List, Dict, Tuple, Optional
from ..core import STEMS, BRANCHES
from ..derived import get_ten_god, get_all_branch_qi, ELEMENT_CYCLES
from .models import TenGodEntry, ChartData


# Ten God display info
TEN_GOD_INFO = {
    "F":  {"english": "Friend",           "chinese": "比肩", "category": "companion", "element_role": "same"},
    "RW": {"english": "Rob Wealth",       "chinese": "劫財", "category": "companion", "element_role": "same"},
    "EG": {"english": "Eating God",       "chinese": "食神", "category": "output",    "element_role": "output"},
    "HO": {"english": "Hurting Officer",  "chinese": "傷官", "category": "output",    "element_role": "output"},
    "IW": {"english": "Indirect Wealth",  "chinese": "偏財", "category": "wealth",    "element_role": "wealth"},
    "DW": {"english": "Direct Wealth",    "chinese": "正財", "category": "wealth",    "element_role": "wealth"},
    "7K": {"english": "Seven Killings",   "chinese": "七殺", "category": "officer",   "element_role": "officer"},
    "DO": {"english": "Direct Officer",   "chinese": "正官", "category": "officer",   "element_role": "officer"},
    "IR": {"english": "Indirect Resource","chinese": "偏印", "category": "resource",  "element_role": "resource"},
    "DR": {"english": "Direct Resource",  "chinese": "正印", "category": "resource",  "element_role": "resource"},
}

# Male and female specific meanings for Ten Gods
TEN_GOD_LIFE_MEANING = {
    "male": {
        "DW": "wife star",
        "IW": "mistress/father star",
        "DO": "children (daughters) star",
        "7K": "children (sons) / authority star",
        "DR": "mother star",
        "IR": "stepmother / unusual knowledge star",
        "F":  "siblings (same gender) / competitors",
        "RW": "siblings (opposite gender) / rivals",
        "EG": "subordinates / talent star",
        "HO": "creativity / rebellion star",
    },
    "female": {
        "DO": "husband star",
        "7K": "boyfriend / lover / authority star",
        "EG": "children (daughters) star",
        "HO": "children (sons) / creativity star",
        "DW": "father star",
        "IW": "father figure star",
        "DR": "mother star",
        "IR": "stepmother / unusual knowledge star",
        "F":  "siblings (same gender) / competitors",
        "RW": "siblings (opposite gender) / rivals",
    },
}


def map_all_ten_gods(chart: ChartData) -> List[TenGodEntry]:
    """Map Ten Gods for every stem in the chart (visible + hidden)."""
    dm = chart.day_master
    entries = []

    for pos in ["year", "month", "day", "hour"]:
        pillar = chart.pillars[pos]

        # Visible stem (skip Day Master itself for the mapping)
        stem = pillar.stem
        tg = get_ten_god(dm, stem)
        if tg:
            entries.append(TenGodEntry(
                stem=stem,
                abbreviation=tg[0],
                english=tg[1],
                chinese=tg[2],
                location=f"{pos}_stem",
                position=pos,
                visible=True,
            ))

        # Hidden stems in branch
        branch_qi = get_all_branch_qi(pillar.branch)
        for idx, (hs, score) in enumerate(branch_qi):
            tg = get_ten_god(dm, hs)
            if tg:
                label = "primary_qi" if idx == 0 else f"hidden_{idx}"
                entries.append(TenGodEntry(
                    stem=hs,
                    abbreviation=tg[0],
                    english=tg[1],
                    chinese=tg[2],
                    location=f"{pos}_branch_{label}",
                    position=pos,
                    visible=False,
                ))

    # Luck pillar if present
    if chart.luck_pillar:
        lp = chart.luck_pillar
        tg = get_ten_god(dm, lp.stem)
        if tg:
            entries.append(TenGodEntry(
                stem=lp.stem,
                abbreviation=tg[0],
                english=tg[1],
                chinese=tg[2],
                location="luck_pillar_stem",
                position="luck_pillar",
                visible=True,
            ))
        branch_qi = get_all_branch_qi(lp.branch)
        for idx, (hs, score) in enumerate(branch_qi):
            tg = get_ten_god(dm, hs)
            if tg:
                label = "primary_qi" if idx == 0 else f"hidden_{idx}"
                entries.append(TenGodEntry(
                    stem=hs,
                    abbreviation=tg[0],
                    english=tg[1],
                    chinese=tg[2],
                    location=f"luck_pillar_branch_{label}",
                    position="luck_pillar",
                    visible=False,
                ))

    return entries


def classify_ten_god_strength(entries: List[TenGodEntry]) -> Dict[str, dict]:
    """
    Classify each Ten God's strength in the chart.

    Returns dict keyed by abbreviation with:
      - strength: "PROMINENT", "PRESENT", "WEAK", "HIDDEN_ONLY", "ABSENT"
      - visible_count: number of visible (heavenly stem) appearances
      - hidden_count: number of hidden stem appearances
      - total_count: visible + hidden
      - locations: list of location strings
    """
    # Only count natal chart entries (not luck pillar)
    tg_counts: Dict[str, dict] = {}
    for abbr in TEN_GOD_INFO:
        tg_counts[abbr] = {
            "abbreviation": abbr,
            "english": TEN_GOD_INFO[abbr]["english"],
            "chinese": TEN_GOD_INFO[abbr]["chinese"],
            "category": TEN_GOD_INFO[abbr]["category"],
            "visible_count": 0,
            "hidden_count": 0,
            "total_count": 0,
            "locations": [],
            "strength": "ABSENT",
        }

    for entry in entries:
        if entry.position == "luck_pillar":
            continue
        info = tg_counts.get(entry.abbreviation)
        if not info:
            continue
        if entry.visible:
            info["visible_count"] += 1
        else:
            info["hidden_count"] += 1
        info["total_count"] += 1
        info["locations"].append(entry.location)

    for abbr, info in tg_counts.items():
        vc = info["visible_count"]
        hc = info["hidden_count"]
        total = info["total_count"]

        if total == 0:
            info["strength"] = "ABSENT"
        elif vc >= 2:
            info["strength"] = "PROMINENT"
        elif vc == 1 and hc >= 1:
            info["strength"] = "PROMINENT"
        elif vc == 1:
            info["strength"] = "PRESENT"
        elif hc >= 2:
            info["strength"] = "PRESENT"
        elif hc == 1:
            info["strength"] = "HIDDEN_ONLY"
        else:
            info["strength"] = "WEAK"

    return tg_counts


def get_dominant_ten_gods(classification: Dict[str, dict]) -> List[str]:
    """Return Ten God abbreviations that are PROMINENT."""
    return [abbr for abbr, info in classification.items()
            if info["strength"] == "PROMINENT"]


def get_absent_ten_gods(classification: Dict[str, dict]) -> List[str]:
    """Return Ten God abbreviations that are ABSENT."""
    return [abbr for abbr, info in classification.items()
            if info["strength"] == "ABSENT"]


def check_spouse_star(chart: ChartData, classification: Dict[str, dict]) -> dict:
    """
    Check the spouse star status for this chart.
    Male: DW (Direct Wealth) = wife star
    Female: DO (Direct Officer) = husband star
    """
    if chart.gender == "male":
        star = "DW"
        label = "wife star (正財)"
    else:
        star = "DO"
        label = "husband star (正官)"

    info = classification.get(star, {})
    strength = info.get("strength", "ABSENT")

    return {
        "star": star,
        "label": label,
        "strength": strength,
        "present": strength not in ("ABSENT",),
        "locations": info.get("locations", []),
        "is_critical_absent": strength == "ABSENT",
    }


def check_children_star(chart: ChartData, classification: Dict[str, dict]) -> dict:
    """
    Check children star status.
    Male: 7K (sons), DO (daughters)
    Female: EG (daughters), HO (sons)
    """
    if chart.gender == "male":
        primary = "7K"
        secondary = "DO"
    else:
        primary = "HO"
        secondary = "EG"

    p_info = classification.get(primary, {})
    s_info = classification.get(secondary, {})

    return {
        "primary_star": primary,
        "secondary_star": secondary,
        "primary_strength": p_info.get("strength", "ABSENT"),
        "secondary_strength": s_info.get("strength", "ABSENT"),
        "any_present": (p_info.get("strength", "ABSENT") != "ABSENT" or
                       s_info.get("strength", "ABSENT") != "ABSENT"),
    }


def get_ten_god_element_counts(entries: List[TenGodEntry]) -> Dict[str, float]:
    """
    Count element influence by Ten God category (companion, output, wealth, officer, resource).
    Visible stems count 1.0, hidden stems count proportionally less.
    Only counts natal chart entries.
    """
    HIDDEN_WEIGHT = 0.5
    counts = {"companion": 0.0, "output": 0.0, "wealth": 0.0,
              "officer": 0.0, "resource": 0.0}

    for entry in entries:
        if entry.position == "luck_pillar":
            continue
        cat = TEN_GOD_INFO.get(entry.abbreviation, {}).get("category")
        if cat:
            weight = 1.0 if entry.visible else HIDDEN_WEIGHT
            counts[cat] += weight

    return counts


def analyze_ten_god_patterns(chart: ChartData, classification: Dict[str, dict]) -> List[dict]:
    """
    Identify notable Ten God patterns in the chart.
    Returns list of pattern descriptions.
    """
    patterns = []

    # Check for too many companions (Friend + Rob Wealth)
    f_total = classification["F"]["total_count"] + classification["RW"]["total_count"]
    if f_total >= 3:
        patterns.append({
            "pattern": "companion_heavy",
            "description": "Too many companions (Friend + Rob Wealth) = competition problems, "
                          "wealth leakage, relationship interference",
            "severity": "moderate",
            "life_areas": ["wealth", "relationship"],
        })

    # Check for output overload (Eating God + Hurting Officer)
    eg_ho = classification["EG"]["total_count"] + classification["HO"]["total_count"]
    if eg_ho >= 3:
        patterns.append({
            "pattern": "output_heavy",
            "description": "Too much output energy (EG + HO) = energy drain, overwork, "
                          "weakened authority, undermined structure",
            "severity": "moderate",
            "life_areas": ["health", "career"],
        })

    # Hurting Officer prominent = trouble with authority
    if classification["HO"]["strength"] == "PROMINENT":
        patterns.append({
            "pattern": "ho_prominent",
            "description": "Prominent Hurting Officer = rebellious, conflicts with authority, "
                          "creative but destructive to structure and rules",
            "severity": "moderate",
            "life_areas": ["career", "relationship", "legal"],
        })

    # Seven Killings prominent without control
    if classification["7K"]["strength"] == "PROMINENT":
        has_eg = classification["EG"]["total_count"] > 0
        patterns.append({
            "pattern": "7k_prominent",
            "description": ("Seven Killings prominent" +
                          (" but controlled by Eating God" if has_eg else
                           " WITHOUT control = aggressive, ruthless, danger of conflicts")),
            "severity": "mild" if has_eg else "severe",
            "life_areas": ["career", "health", "legal"],
        })

    # Rob Wealth prominent = wealth problems
    if classification["RW"]["strength"] in ("PROMINENT", "PRESENT"):
        patterns.append({
            "pattern": "rw_present",
            "description": "Rob Wealth present = money lost through others, "
                          "partnerships can drain wealth, competitive spending",
            "severity": "moderate",
            "life_areas": ["wealth"],
        })

    # No wealth at all
    if (classification["DW"]["strength"] == "ABSENT" and
        classification["IW"]["strength"] == "ABSENT"):
        patterns.append({
            "pattern": "no_wealth",
            "description": "Both Direct and Indirect Wealth ABSENT = "
                          "difficulty accumulating wealth, needs element remedies",
            "severity": "severe",
            "life_areas": ["wealth"],
        })

    # No officer at all
    if (classification["DO"]["strength"] == "ABSENT" and
        classification["7K"]["strength"] == "ABSENT"):
        patterns.append({
            "pattern": "no_officer",
            "description": "Both Direct Officer and Seven Killings ABSENT = "
                          "lack of discipline, authority, and career structure",
            "severity": "moderate",
            "life_areas": ["career"],
        })

    # No resource at all
    if (classification["DR"]["strength"] == "ABSENT" and
        classification["IR"]["strength"] == "ABSENT"):
        patterns.append({
            "pattern": "no_resource",
            "description": "Both Direct and Indirect Resource ABSENT = "
                          "lack of support, mentors, education backing, mother issues",
            "severity": "moderate",
            "life_areas": ["education", "health", "family"],
        })

    return patterns
