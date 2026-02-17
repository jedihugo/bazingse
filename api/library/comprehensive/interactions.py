# =============================================================================
# BRANCH INTERACTIONS ENGINE
# =============================================================================
# Detects ALL branch interactions between natal pillars and with luck pillar:
#   - Six Clashes (六冲)
#   - Six Harmonies (六合)
#   - Three Harmony Frames (三合局)
#   - Directional Combinations (三会局)
#   - Three Punishments (三刑)
#   - Six Harms (六害)
#   - Destructions (破)
# =============================================================================

from typing import List, Dict, Set, Tuple, Optional
from ..core import STEMS, BRANCHES
from ..derived import ELEMENT_CYCLES
from .models import BranchInteraction, ChartData

# Palace names for human-readable output
PALACE_NAMES = {
    "year": "Year (Parents/Ancestry)",
    "month": "Month (Career/Social)",
    "day": "Day (Self/Spouse)",
    "hour": "Hour (Children/Legacy)",
    "luck_pillar": "Current Luck Pillar",
}


def _get_all_branches(chart: ChartData, include_lp: bool = True) -> List[Tuple[str, str]]:
    """Get all (position, branch) pairs from chart."""
    pairs = []
    for pos in ["year", "month", "day", "hour"]:
        pairs.append((pos, chart.pillars[pos].branch))
    if include_lp and chart.luck_pillar:
        pairs.append(("luck_pillar", chart.luck_pillar.branch))
    return pairs


# =============================================================================
# SIX CLASHES (六冲)
# =============================================================================

CLASH_PAIRS = {
    frozenset({"Zi", "Wu"}), frozenset({"Chou", "Wei"}),
    frozenset({"Yin", "Shen"}), frozenset({"Mao", "You"}),
    frozenset({"Chen", "Xu"}), frozenset({"Si", "Hai"}),
}


def detect_clashes(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pos1, br1 = pairs[i]
            pos2, br2 = pairs[j]
            if frozenset({br1, br2}) in CLASH_PAIRS:
                activated = pos1 == "luck_pillar" or pos2 == "luck_pillar"
                elem1 = BRANCHES[br1]["element"]
                elem2 = BRANCHES[br2]["element"]

                results.append(BranchInteraction(
                    interaction_type="clash",
                    chinese_name="六冲",
                    branches=[br1, br2],
                    palaces=[PALACE_NAMES[pos1], PALACE_NAMES[pos2]],
                    description=f"{BRANCHES[br1]['chinese']}{BRANCHES[br2]['chinese']}冲 "
                               f"({elem1} vs {elem2})",
                    activated_by_lp=activated,
                    severity="severe",
                ))
    return results


# =============================================================================
# SIX HARMONIES (六合)
# =============================================================================

HARMONY_PAIRS = {
    frozenset({"Zi", "Chou"}): "Earth",
    frozenset({"Yin", "Hai"}): "Wood",
    frozenset({"Mao", "Xu"}): "Fire",
    frozenset({"Chen", "You"}): "Metal",
    frozenset({"Si", "Shen"}): "Water",
    frozenset({"Wu", "Wei"}): "Fire",
}


def detect_harmonies(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pos1, br1 = pairs[i]
            pos2, br2 = pairs[j]
            key = frozenset({br1, br2})
            if key in HARMONY_PAIRS:
                element = HARMONY_PAIRS[key]
                activated = pos1 == "luck_pillar" or pos2 == "luck_pillar"

                results.append(BranchInteraction(
                    interaction_type="harmony",
                    chinese_name="六合",
                    branches=[br1, br2],
                    palaces=[PALACE_NAMES[pos1], PALACE_NAMES[pos2]],
                    description=f"{BRANCHES[br1]['chinese']}{BRANCHES[br2]['chinese']}合 "
                               f"→ {element}",
                    activated_by_lp=activated,
                    severity="mild",
                ))
    return results


# =============================================================================
# THREE HARMONY FRAMES (三合局)
# =============================================================================

THREE_HARMONY_FRAMES = {
    frozenset({"Shen", "Zi", "Chen"}): "Water",
    frozenset({"Hai", "Mao", "Wei"}): "Wood",
    frozenset({"Yin", "Wu", "Xu"}): "Fire",
    frozenset({"Si", "You", "Chou"}): "Metal",
}


def detect_three_harmony(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)
    all_branches = {br for _, br in pairs}

    for frame_set, element in THREE_HARMONY_FRAMES.items():
        present = frame_set & all_branches
        if len(present) == 3:
            # Full frame present
            positions = []
            for pos, br in pairs:
                if br in frame_set:
                    positions.append(PALACE_NAMES[pos])
            activated = any(pos == "luck_pillar" for pos, br in pairs if br in frame_set)

            branches_chinese = "".join(BRANCHES[b]["chinese"] for b in sorted(frame_set, key=lambda x: BRANCHES[x]["index"]))
            results.append(BranchInteraction(
                interaction_type="three_harmony",
                chinese_name="三合局",
                branches=sorted(list(frame_set), key=lambda x: BRANCHES[x]["index"]),
                palaces=positions,
                description=f"{branches_chinese}三合{element}局",
                activated_by_lp=activated,
                severity="mild",
            ))
        elif len(present) == 2:
            # Partial frame (half combination)
            branches_list = sorted(list(present), key=lambda x: BRANCHES[x]["index"])
            positions = []
            activated = False
            for pos, br in pairs:
                if br in present:
                    positions.append(PALACE_NAMES[pos])
                    if pos == "luck_pillar":
                        activated = True

            missing = list(frame_set - present)[0]
            branches_chinese = "".join(BRANCHES[b]["chinese"] for b in branches_list)
            results.append(BranchInteraction(
                interaction_type="half_three_harmony",
                chinese_name="半三合",
                branches=branches_list,
                palaces=positions,
                description=f"{branches_chinese}半合{element}局 "
                           f"(missing {BRANCHES[missing]['chinese']})",
                activated_by_lp=activated,
                severity="mild",
            ))

    return results


# =============================================================================
# DIRECTIONAL COMBINATIONS (三会局)
# =============================================================================

DIRECTIONAL_COMBOS = {
    frozenset({"Yin", "Mao", "Chen"}): ("Wood", "East"),
    frozenset({"Si", "Wu", "Wei"}): ("Fire", "South"),
    frozenset({"Shen", "You", "Xu"}): ("Metal", "West"),
    frozenset({"Hai", "Zi", "Chou"}): ("Water", "North"),
}


def detect_directional_combos(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)
    all_branches = {br for _, br in pairs}

    for combo_set, (element, direction) in DIRECTIONAL_COMBOS.items():
        present = combo_set & all_branches
        if len(present) >= 3:
            positions = []
            activated = False
            for pos, br in pairs:
                if br in combo_set:
                    positions.append(PALACE_NAMES[pos])
                    if pos == "luck_pillar":
                        activated = True

            branches_chinese = "".join(BRANCHES[b]["chinese"] for b in sorted(combo_set, key=lambda x: BRANCHES[x]["index"]))
            results.append(BranchInteraction(
                interaction_type="directional_combo",
                chinese_name="三会局",
                branches=sorted(list(combo_set), key=lambda x: BRANCHES[x]["index"]),
                palaces=positions,
                description=f"{branches_chinese}三会{element}局 ({direction})",
                activated_by_lp=activated,
                severity="mild",
            ))

    return results


# =============================================================================
# THREE PUNISHMENTS (三刑)
# =============================================================================

# Group punishments
PUNISHMENT_GROUPS = {
    "ungrateful": {
        "branches": frozenset({"Yin", "Si", "Shen"}),
        "chinese": "寅巳申 恃势之刑",
        "english": "Ungrateful/Power Punishment",
    },
    "bullying": {
        "branches": frozenset({"Chou", "Wei", "Xu"}),
        "chinese": "丑未戌 无礼之刑",
        "english": "Bullying/Rudeness Punishment",
    },
}

# Pair punishments
PUNISHMENT_PAIR = {
    frozenset({"Zi", "Mao"}): {
        "chinese": "子卯 无恩之刑",
        "english": "Rude/Graceless Punishment",
    },
}

# Self punishments
SELF_PUNISHMENT_BRANCHES = {"Chen", "Wu", "You", "Hai"}


def detect_punishments(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)
    all_branches_list = [br for _, br in pairs]
    all_branches_set = set(all_branches_list)

    # 3-branch group punishments
    for pun_type, info in PUNISHMENT_GROUPS.items():
        present = info["branches"] & all_branches_set
        if len(present) >= 2:
            positions = []
            activated = False
            for pos, br in pairs:
                if br in present:
                    positions.append(PALACE_NAMES[pos])
                    if pos == "luck_pillar":
                        activated = True

            full = len(present) == 3
            results.append(BranchInteraction(
                interaction_type="punishment",
                chinese_name="三刑" if full else "半刑",
                branches=sorted(list(present), key=lambda x: BRANCHES[x]["index"]),
                palaces=positions,
                description=f"{info['chinese']} ({'FULL' if full else 'PARTIAL'}) - {info['english']}",
                activated_by_lp=activated,
                severity="severe" if full else "moderate",
            ))

    # 2-branch pair punishments
    for pair_set, info in PUNISHMENT_PAIR.items():
        present = pair_set & all_branches_set
        if len(present) == 2:
            positions = []
            activated = False
            for pos, br in pairs:
                if br in pair_set:
                    positions.append(PALACE_NAMES[pos])
                    if pos == "luck_pillar":
                        activated = True

            results.append(BranchInteraction(
                interaction_type="punishment",
                chinese_name="二刑",
                branches=sorted(list(pair_set), key=lambda x: BRANCHES[x]["index"]),
                palaces=positions,
                description=f"{info['chinese']} - {info['english']}",
                activated_by_lp=activated,
                severity="moderate",
            ))

    # Self-punishments (same branch appearing twice)
    from collections import Counter
    branch_counts = Counter(all_branches_list)
    for br, count in branch_counts.items():
        if br in SELF_PUNISHMENT_BRANCHES and count >= 2:
            positions = [PALACE_NAMES[pos] for pos, b in pairs if b == br]
            activated = any(pos == "luck_pillar" for pos, b in pairs if b == br)

            results.append(BranchInteraction(
                interaction_type="self_punishment",
                chinese_name="自刑",
                branches=[br, br],
                palaces=positions,
                description=f"{BRANCHES[br]['chinese']}{BRANCHES[br]['chinese']}自刑 - "
                           f"{BRANCHES[br].get('self_punishment_nature', 'Self-conflict')}",
                activated_by_lp=activated,
                severity="moderate",
            ))

    return results


# =============================================================================
# SIX HARMS (六害)
# =============================================================================

HARM_PAIRS = {
    frozenset({"Zi", "Wei"}), frozenset({"Chou", "Wu"}),
    frozenset({"Yin", "Si"}), frozenset({"Mao", "Chen"}),
    frozenset({"Shen", "Hai"}), frozenset({"You", "Xu"}),
}


def detect_harms(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pos1, br1 = pairs[i]
            pos2, br2 = pairs[j]
            if frozenset({br1, br2}) in HARM_PAIRS:
                activated = pos1 == "luck_pillar" or pos2 == "luck_pillar"

                results.append(BranchInteraction(
                    interaction_type="harm",
                    chinese_name="六害",
                    branches=[br1, br2],
                    palaces=[PALACE_NAMES[pos1], PALACE_NAMES[pos2]],
                    description=f"{BRANCHES[br1]['chinese']}{BRANCHES[br2]['chinese']}害",
                    activated_by_lp=activated,
                    severity="moderate",
                ))
    return results


# =============================================================================
# DESTRUCTIONS (破)
# =============================================================================

DESTRUCTION_PAIRS = {
    frozenset({"Zi", "You"}), frozenset({"Chou", "Chen"}),
    frozenset({"Yin", "Hai"}), frozenset({"Mao", "Wu"}),
    frozenset({"Si", "Shen"}), frozenset({"Wei", "Xu"}),
}


def detect_destructions(chart: ChartData) -> List[BranchInteraction]:
    results = []
    pairs = _get_all_branches(chart)

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pos1, br1 = pairs[i]
            pos2, br2 = pairs[j]
            if frozenset({br1, br2}) in DESTRUCTION_PAIRS:
                activated = pos1 == "luck_pillar" or pos2 == "luck_pillar"

                results.append(BranchInteraction(
                    interaction_type="destruction",
                    chinese_name="破",
                    branches=[br1, br2],
                    palaces=[PALACE_NAMES[pos1], PALACE_NAMES[pos2]],
                    description=f"{BRANCHES[br1]['chinese']}{BRANCHES[br2]['chinese']}破",
                    activated_by_lp=activated,
                    severity="mild",
                ))
    return results


# =============================================================================
# MASTER FUNCTION: Detect All Interactions
# =============================================================================

def detect_all_interactions(chart: ChartData) -> List[BranchInteraction]:
    """Run all interaction checks and return combined results."""
    results = []
    results.extend(detect_clashes(chart))
    results.extend(detect_harmonies(chart))
    results.extend(detect_three_harmony(chart))
    results.extend(detect_directional_combos(chart))
    results.extend(detect_punishments(chart))
    results.extend(detect_harms(chart))
    results.extend(detect_destructions(chart))
    return results


def get_negative_interactions(chart: ChartData) -> List[BranchInteraction]:
    """Return only negative interactions (clashes, punishments, harms, destructions)."""
    negative_types = {"clash", "punishment", "self_punishment", "harm", "destruction"}
    return [i for i in detect_all_interactions(chart)
            if i.interaction_type in negative_types]


def get_positive_interactions(chart: ChartData) -> List[BranchInteraction]:
    """Return only positive interactions (harmonies, three harmony, directional)."""
    positive_types = {"harmony", "three_harmony", "half_three_harmony", "directional_combo"}
    return [i for i in detect_all_interactions(chart)
            if i.interaction_type in positive_types]
