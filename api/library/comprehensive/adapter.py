# =============================================================================
# ADAPTER: Comprehensive Engine → Frontend JSON
# =============================================================================
# Translates the comprehensive engine's Python dataclasses into the exact JSON
# shape the frontend expects from /api/analyze_bazi.
# =============================================================================

from typing import List, Dict, Optional, Any, Tuple
from ..core import STEMS, BRANCHES
from ..derived import (
    get_ten_god, get_all_branch_qi, TEN_GODS, TEN_GOD_NOTES,
    ELEMENT_CYCLES, STEM_ORDER, BRANCH_ORDER,
)
from ..qi_phase import get_qi_phase_for_pillar
from .models import (
    ChartData, Pillar, StrengthAssessment, BranchInteraction,
    ShenShaResult, TenGodEntry, RedFlag, EventPrediction,
    EnvironmentAssessment, LuckPillarInfo,
)
from .ten_gods import (
    TEN_GOD_INFO, TEN_GOD_LIFE_MEANING,
    classify_ten_god_strength, analyze_ten_god_patterns,
    check_spouse_star, check_children_star,
)
from .strength import count_elements


# =============================================================================
# NODE KEY MAPPING
# =============================================================================
# Maps pillar position → node key prefixes for HS and EB
POSITION_TO_NODE = {
    "year":        ("hs_y",    "eb_y"),
    "month":       ("hs_m",    "eb_m"),
    "day":         ("hs_d",    "eb_d"),
    "hour":        ("hs_h",    "eb_h"),
    "luck_pillar": ("hs_10yl", "eb_10yl"),
}


# =============================================================================
# BUILD STEM (HS) NODE
# =============================================================================

def build_stem_node(pillar: Pillar, chart: ChartData) -> dict:
    """Build a Heavenly Stem node dict matching frontend shape."""
    stem = pillar.stem
    stem_data = STEMS[stem]
    qi = {stem: 100.0}

    # Ten God
    tg = get_ten_god(chart.day_master, stem)
    ten_god_abbr = tg[0] if tg else ("DM" if stem == chart.day_master else "")

    # Qi phase
    qi_phase = None
    try:
        qi_phase = get_qi_phase_for_pillar(stem, pillar.branch)
    except Exception:
        pass

    return {
        "id": stem,
        "base": {"id": stem, "qi": dict(qi)},
        "post": {"id": stem, "qi": dict(qi)},
        "badges": [],
        "base_qi": dict(qi),
        "qi_phase": qi_phase,
        "ten_god": ten_god_abbr,
        "interaction_ids": [],
    }


# =============================================================================
# BUILD BRANCH (EB) NODE
# =============================================================================

def build_branch_node(pillar: Pillar, chart: ChartData) -> dict:
    """Build an Earthly Branch node dict matching frontend shape."""
    branch = pillar.branch
    branch_data = BRANCHES[branch]

    # Build qi dict from branch hidden stems
    qi = {}
    for stem_id, score in branch_data.get("qi", []):
        qi[stem_id] = float(score)

    # Ten God for primary qi
    primary_qi = branch_data["qi"][0] if branch_data.get("qi") else None
    tg = None
    if primary_qi:
        tg = get_ten_god(chart.day_master, primary_qi[0])
    ten_god_abbr = tg[0] if tg else ""

    return {
        "id": branch,
        "base": {"id": branch, "qi": dict(qi)},
        "post": {"id": branch, "qi": dict(qi)},
        "badges": [],
        "base_qi": dict(qi),
        "ten_god": ten_god_abbr,
        "interaction_ids": [],
    }


# =============================================================================
# BUILD ALL NODES
# =============================================================================

def build_all_nodes(chart: ChartData) -> dict:
    """Build all hs_y/eb_y through hs_h/eb_h + luck pillar nodes."""
    nodes = {}

    for pos, pillar in chart.pillars.items():
        if pos not in POSITION_TO_NODE:
            continue
        hs_key, eb_key = POSITION_TO_NODE[pos]
        nodes[hs_key] = build_stem_node(pillar, chart)
        nodes[eb_key] = build_branch_node(pillar, chart)

    # Luck pillar
    if chart.luck_pillar:
        hs_key, eb_key = POSITION_TO_NODE["luck_pillar"]
        nodes[hs_key] = build_stem_node(chart.luck_pillar, chart)
        nodes[eb_key] = build_branch_node(chart.luck_pillar, chart)

    return nodes


# =============================================================================
# BADGE MAPPING
# =============================================================================
# Maps comprehensive interaction types → frontend badge types
INTERACTION_TO_BADGE = {
    "clash": "conflict",
    "harmony": "combination",
    "three_harmony": "combination",
    "half_three_harmony": "combination",
    "directional_combo": "combination",
    "punishment": "conflict",
    "self_punishment": "conflict",
    "harm": "conflict",
    "destruction": "conflict",
}


def _branch_to_node_key(branch: str, chart: ChartData) -> Optional[str]:
    """Find the eb_* node key for a given branch ID."""
    for pos, pillar in chart.pillars.items():
        if pillar.branch == branch and pos in POSITION_TO_NODE:
            return POSITION_TO_NODE[pos][1]
    if chart.luck_pillar and chart.luck_pillar.branch == branch:
        return POSITION_TO_NODE["luck_pillar"][1]
    return None


def map_interactions_to_badges(interactions: List[BranchInteraction],
                                chart: ChartData,
                                nodes: dict) -> None:
    """Add badge dicts to the correct EB nodes in-place."""
    for idx, inter in enumerate(interactions):
        badge_type = INTERACTION_TO_BADGE.get(inter.interaction_type, "conflict")
        interaction_id = f"INT_{idx}_{inter.interaction_type}"

        for branch in inter.branches:
            node_key = _branch_to_node_key(branch, chart)
            if node_key and node_key in nodes:
                nodes[node_key]["badges"].append({
                    "type": badge_type,
                    "interaction_id": interaction_id,
                    "chinese_name": inter.chinese_name,
                    "description": inter.description,
                })
                if interaction_id not in nodes[node_key]["interaction_ids"]:
                    nodes[node_key]["interaction_ids"].append(interaction_id)


# =============================================================================
# INTERACTIONS → DICT
# =============================================================================

def build_interaction_dict(interactions: List[BranchInteraction]) -> dict:
    """Convert BranchInteraction list → {id: interaction_obj} dict for frontend."""
    result = {}
    for idx, inter in enumerate(interactions):
        int_id = f"INT_{idx}_{inter.interaction_type}"
        branch_chinese = "".join(BRANCHES[b]["chinese"] for b in inter.branches)
        result[int_id] = {
            "id": int_id,
            "type": inter.interaction_type.upper(),
            "chinese_name": inter.chinese_name,
            "branches": inter.branches,
            "palaces": inter.palaces,
            "description": inter.description,
            "branch_chinese": branch_chinese,
            "severity": inter.severity,
            "activated_by_lp": inter.activated_by_lp,
        }
    return result


# =============================================================================
# DAYMASTER ANALYSIS
# =============================================================================

def build_daymaster_analysis(strength: StrengthAssessment,
                              chart: ChartData) -> dict:
    """Convert StrengthAssessment → frontend daymaster_analysis dict."""
    dm = chart.day_master
    dm_info = STEMS[dm]

    # Map verdict to frontend strength string
    verdict_map = {
        "extremely_strong": "Extremely Strong",
        "strong": "Strong",
        "neutral": "Balanced",
        "weak": "Weak",
        "extremely_weak": "Extremely Weak",
    }

    # Chart type
    if strength.is_following_chart:
        chart_type = f"Following ({strength.following_type})"
    elif strength.verdict in ("strong", "extremely_strong"):
        chart_type = "Strong"
    elif strength.verdict in ("weak", "extremely_weak"):
        chart_type = "Weak"
    else:
        chart_type = "Balanced"

    total = strength.support_count + strength.drain_count
    support_pct = round((strength.support_count / total * 100) if total > 0 else 50, 1)

    return {
        "daymaster": dm,
        "daymaster_chinese": dm_info["chinese"],
        "daymaster_element": dm_info["element"],
        "daymaster_polarity": dm_info["polarity"],
        "chart_type": chart_type,
        "daymaster_percentage": strength.score,
        "strength": verdict_map.get(strength.verdict, "Balanced"),
        "support_percentage": support_pct,
        "seasonal_state": strength.seasonal_state,
        "useful_god": strength.useful_god,
        "favorable_elements": strength.favorable_elements,
        "unfavorable_elements": strength.unfavorable_elements,
        "is_following_chart": strength.is_following_chart,
        "following_type": strength.following_type,
    }


# =============================================================================
# ELEMENT SCORES (3-tier: base → natal → post)
# =============================================================================

def build_element_scores(chart: ChartData) -> Tuple[dict, dict, dict]:
    """
    Compute 3-tier element scores from pillar data.
    Since the new engine doesn't mutate qi, all 3 tiers use the same values.
    Returns (base_element_score, natal_element_score, post_element_score)
    as {stem_name: float} dicts.
    """
    # Count raw elements in the chart
    elem_counts = count_elements(chart)

    # Convert to stem-based scores (each stem gets proportional share)
    stem_scores = {}
    for stem_id in STEMS:
        stem_elem = STEMS[stem_id]["element"]
        # Give each stem a score proportional to its element's count
        # Distribute among the 2 stems of each element
        stem_scores[stem_id] = round(elem_counts.get(stem_elem, 0) * 50, 1)

    return stem_scores, dict(stem_scores), dict(stem_scores)


# =============================================================================
# SPECIAL STARS (SHEN SHA)
# =============================================================================

def build_special_stars(shen_sha: List[ShenShaResult]) -> list:
    """Convert present ShenShaResult list → frontend special_stars format."""
    stars = []
    for s in shen_sha:
        if not s.present:
            continue
        stars.append({
            "chinese_name": s.name_chinese,
            "english_name": s.name_english,
            "target_branch": s.location or "",
            "palace": s.palace or "",
            "nature": s.nature,
            "impact": s.impact,
            "severity": s.severity,
            "is_void": s.is_void,
            "derivation": s.derivation,
            "life_areas": s.life_areas,
        })
    return stars


# =============================================================================
# HEALTH / WEALTH / LEARNING ANALYSIS
# =============================================================================

def _collect_red_flags(chart: ChartData,
                       strength: StrengthAssessment,
                       tg_classification: Dict[str, dict],
                       interactions: List[BranchInteraction],
                       shen_sha: List[ShenShaResult]) -> Dict[str, List[RedFlag]]:
    """Collect all red flags by life area (replicates report.py section_red_flags logic)."""
    flags: Dict[str, List[RedFlag]] = {
        "wealth": [], "marriage": [], "career": [],
        "health": [], "character": [],
    }

    # From Ten God patterns
    patterns = analyze_ten_god_patterns(chart, tg_classification)
    for p in patterns:
        areas = p.get("life_areas", [])
        target = areas[0] if areas else "character"
        if target not in flags:
            target = "character"
        flags[target].append(RedFlag(
            life_area=target,
            indicator_type="ten_god",
            indicator_name=p["pattern"],
            description=p["description"],
            severity=p["severity"],
        ))

    # Spouse star check
    spouse = check_spouse_star(chart, tg_classification)
    if spouse["is_critical_absent"]:
        flags["marriage"].append(RedFlag(
            life_area="marriage",
            indicator_type="ten_god",
            indicator_name=f"{spouse['star']} absent",
            description=f"{spouse['label']} is completely ABSENT from the natal chart.",
            severity="severe",
        ))

    # From branch interactions
    for inter in interactions:
        if inter.interaction_type in ("clash", "punishment", "self_punishment", "harm"):
            for palace in inter.palaces:
                if "Spouse" in palace:
                    target = "marriage"
                elif "Career" in palace:
                    target = "career"
                elif "Children" in palace:
                    target = "marriage"
                elif "Parents" in palace:
                    target = "character"
                else:
                    continue
                flags[target].append(RedFlag(
                    life_area=target,
                    indicator_type="branch_interaction",
                    indicator_name=inter.chinese_name,
                    description=inter.description,
                    severity=inter.severity,
                ))

    # From Shen Sha
    for s in shen_sha:
        if not s.present or s.nature != "inauspicious":
            continue
        areas = s.life_areas
        target = areas[0] if areas else "character"
        if target not in flags:
            target = "character"
        flags[target].append(RedFlag(
            life_area=target,
            indicator_type="shen_sha",
            indicator_name=s.name_chinese,
            description=f"{s.name_english} ({s.name_chinese}) in {s.palace or 'chart'}",
            severity=s.severity,
        ))

    return flags


def _severity_category(flags: List[RedFlag]) -> str:
    """Determine severity category from a list of red flags."""
    if not flags:
        return "balanced"
    severities = [f.severity for f in flags]
    if "critical" in severities or "severe" in severities:
        return "warning"
    if "moderate" in severities:
        return "caution"
    return "mild"


def _build_pattern_engine_stub(flags: List[RedFlag]) -> dict:
    """Build a pattern_engine sub-dict from red flags (replaces old pattern_engine)."""
    return {
        "pattern_count": len(flags),
        "compound_severity": len(flags) * 10,
        "severity_level": _severity_category(flags),
        "top_patterns": [
            {
                "chinese_name": f.indicator_name,
                "severity": 0.5 if f.severity == "mild" else 0.7 if f.severity == "moderate" else 0.9,
                "level": f.severity,
            }
            for f in flags[:5]
        ],
        "recommendations": [],
    }


def build_health_analysis(flags: Dict[str, List[RedFlag]],
                           strength: StrengthAssessment,
                           chart: ChartData) -> dict:
    """Build health_analysis matching old shape."""
    health_flags = flags.get("health", [])
    dm_element = chart.dm_element

    # Build warnings from element vulnerability
    elem_counts = count_elements(chart)
    from .templates import HEALTH_ELEMENT_MAP
    warnings = []
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        if elem_counts.get(elem, 0) < 1.0:
            organ_info = HEALTH_ELEMENT_MAP.get(elem, {})
            warnings.append({
                "element": elem,
                "organ_system": organ_info.get("yin_organ", "").split("(")[0].strip(),
                "zang_organ": organ_info.get("yin_organ", ""),
                "fu_organ": organ_info.get("yang_organ", ""),
                "severity": "moderate",
                "conflict_count": 0,
                "weighted_score": round((1.0 - elem_counts.get(elem, 0)) * 30, 1),
                "seasonal_state": strength.seasonal_state,
            })

    # Analysis text
    if warnings:
        primary = warnings[0]
        analysis_text = (
            f"Monitor {primary['organ_system']} system ({primary['element']} element). "
            f"Element count is low, indicating potential vulnerability."
        )
    elif health_flags:
        analysis_text = f"Health concern flagged: {health_flags[0].description}"
    else:
        analysis_text = "Overall health picture is balanced with no significant vulnerabilities detected."

    severity_score = min(100, len(health_flags) * 15 + len(warnings) * 10)

    # Determine severity_category for frontend color coding
    if severity_score >= 70:
        severity_category = "severe"
    elif severity_score >= 40:
        severity_category = "moderate"
    elif severity_score > 0:
        severity_category = "mild"
    else:
        severity_category = "balanced"

    result = {
        "health_warnings": warnings,
        "conflict_severity_score": round(severity_score, 1),
        "severity_category": severity_category,
        "most_vulnerable_element": warnings[0]["element"] if warnings else None,
        "seasonal_vulnerability": {},
        "analysis_text": analysis_text,
    }

    # Add pattern_engine sub-dict
    result["pattern_engine"] = _build_pattern_engine_stub(health_flags)

    return result


def build_wealth_analysis(flags: Dict[str, List[RedFlag]],
                           strength: StrengthAssessment,
                           tg_classification: Dict[str, dict],
                           chart: ChartData) -> dict:
    """Build wealth_analysis matching old shape."""
    wealth_flags = flags.get("wealth", [])
    dm_element = chart.dm_element
    wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element, "")

    # Check wealth star presence
    dw_info = tg_classification.get("DW", {})
    iw_info = tg_classification.get("IW", {})
    has_wealth = dw_info.get("strength", "ABSENT") != "ABSENT" or iw_info.get("strength", "ABSENT") != "ABSENT"

    outlook = "favorable" if has_wealth and not wealth_flags else ("challenging" if wealth_flags else "neutral")

    analysis_text = ""
    if outlook == "favorable":
        analysis_text = f"Wealth element ({wealth_element}) is present. Financial opportunities are accessible."
    elif outlook == "challenging":
        analysis_text = f"Wealth element ({wealth_element}) faces challenges. {wealth_flags[0].description if wealth_flags else ''}"
    else:
        analysis_text = f"Wealth outlook is neutral. Steady financial management recommended."

    result = {
        "wealth_element": wealth_element,
        "wealth_score": 50.0,
        "wealth_change": 0.0,
        "wealth_seasonal_state": strength.seasonal_state,
        "daymaster_can_handle": strength.verdict not in ("extremely_weak",),
        "storage_status": "unknown",
        "opportunities": [],
        "risks": [f.description for f in wealth_flags],
        "outlook": outlook,
        "analysis_text": analysis_text,
        "opportunity_score": 50 if has_wealth else 20,
        "risk_score": len(wealth_flags) * 20,
        "has_exceptional_opportunity": False,
    }

    result["pattern_engine"] = _build_pattern_engine_stub(wealth_flags)
    return result


def build_learning_analysis(flags: Dict[str, List[RedFlag]],
                             strength: StrengthAssessment,
                             tg_classification: Dict[str, dict],
                             chart: ChartData) -> dict:
    """Build learning_analysis matching old shape."""
    dm_element = chart.dm_element
    resource_element = ELEMENT_CYCLES["generated_by"].get(dm_element, "")
    output_element = ELEMENT_CYCLES["generating"].get(dm_element, "")

    # Check resource star
    dr_info = tg_classification.get("DR", {})
    ir_info = tg_classification.get("IR", {})
    has_resource = dr_info.get("strength", "ABSENT") != "ABSENT" or ir_info.get("strength", "ABSENT") != "ABSENT"

    outlook = "favorable" if has_resource else "neutral"
    analysis_text = (
        f"Resource element ({resource_element}) is {'present' if has_resource else 'weak'}. "
        f"Learning capacity is {'good' if has_resource else 'average'}."
    )

    result = {
        "resource_element": resource_element,
        "output_element": output_element,
        "resource_score": 50.0,
        "resource_change": 0.0,
        "resource_seasonal_state": strength.seasonal_state,
        "output_score": 50.0,
        "output_change": 0.0,
        "output_seasonal_state": strength.seasonal_state,
        "daymaster_can_focus": strength.verdict not in ("extremely_weak",),
        "daymaster_can_absorb": True,
        "opportunities": [],
        "blocks": [],
        "outlook": outlook,
        "breakthrough_likely": False,
        "analysis_text": analysis_text,
    }

    result["pattern_engine"] = _build_pattern_engine_stub([])
    return result


# =============================================================================
# TEN GODS DETAIL
# =============================================================================

def build_ten_gods_detail(tg_entries: List[TenGodEntry],
                           tg_classification: Dict[str, dict],
                           chart: ChartData) -> dict:
    """Build ten_gods_detail matching old shape."""
    dm = chart.day_master
    dm_element = STEMS[dm]["element"]

    # Build per-node analysis
    nodes_analysis = {}
    for entry in tg_entries:
        node_key = entry.location
        nodes_analysis[node_key] = {
            "stem": entry.stem,
            "ten_god": entry.abbreviation,
            "ten_god_english": entry.english,
            "ten_god_chinese": entry.chinese,
            "visible": entry.visible,
            "position": entry.position,
        }

    # Warnings from patterns
    patterns = analyze_ten_god_patterns(chart, tg_classification)
    warnings = []
    for p in patterns:
        warnings.append({
            "pattern": p["pattern"],
            "description": p["description"],
            "severity": p["severity"],
            "life_areas": p["life_areas"],
        })

    # Summary by category
    summary = {
        "wealth_nodes": [], "resource_nodes": [], "output_nodes": [],
        "officer_nodes": [], "companion_nodes": [],
    }
    for entry in tg_entries:
        info = TEN_GOD_INFO.get(entry.abbreviation, {})
        cat = info.get("category", "")
        key = f"{cat}_nodes"
        if key in summary:
            summary[key].append(entry.location)

    return {
        "day_master": dm,
        "day_master_element": dm_element,
        "nodes": nodes_analysis,
        "summary": summary,
        "warnings": warnings,
        "opportunities": [],
    }


# =============================================================================
# RECOMMENDATIONS
# =============================================================================

def build_recommendations(predictions: Dict[str, list],
                           flags: Dict[str, List[RedFlag]],
                           strength: StrengthAssessment,
                           env: EnvironmentAssessment) -> list:
    """Build unified recommendations list."""
    recs = []
    order = 0

    # Element remedy
    if strength.useful_god:
        from .templates import ELEMENT_REMEDIES
        remedies = ELEMENT_REMEDIES.get(strength.useful_god, {})
        colors = ", ".join(remedies.get("colors", [])[:3])
        direction = remedies.get("direction", "")
        order += 1
        recs.append({
            "priority": "high",
            "order": order,
            "domain": "general",
            "title": f"Strengthen {strength.useful_god} Element",
            "description": (
                f"Your useful god is {strength.useful_god}. "
                f"Favorable elements: {', '.join(strength.favorable_elements)}. "
                f"Wear colors: {colors}. Direction: {direction}."
            ),
        })

    # Environment recommendation
    if env.crosses_water_benefit:
        order += 1
        recs.append({
            "priority": "medium",
            "order": order,
            "domain": "environment",
            "title": "Consider Relocation Near Water",
            "description": env.crosses_water_reason,
        })

    # From red flags
    for area, area_flags in flags.items():
        if area_flags:
            most_severe = max(area_flags, key=lambda f: {"mild": 0, "moderate": 1, "severe": 2, "critical": 3}.get(f.severity, 0))
            sev = most_severe.severity
            priority_str = "high" if sev in ("severe", "critical") else "medium" if sev == "moderate" else "low"
            order += 1
            recs.append({
                "priority": priority_str,
                "order": order,
                "domain": area,
                "title": f"Address {area.capitalize()} Concerns",
                "description": most_severe.description,
            })

    return recs


# =============================================================================
# NARRATIVE ANALYSIS
# =============================================================================

def _interaction_icon(itype: str) -> str:
    """Map interaction type to NarrativeCard icon key."""
    return {
        "clash": "clash",
        "harmony": "harmony",
        "three_harmony": "triangle",
        "half_three_harmony": "half_combo",
        "directional_combo": "meeting",
        "punishment": "punishment",
        "self_punishment": "punishment",
        "harm": "harm",
        "destruction": "destruction",
    }.get(itype, itype)


def _palace_to_pillar_ref(palace: str) -> dict:
    """Convert a palace string like 'Year (Parents/Ancestry)' to a pillar_ref."""
    pos_map = {
        "year": ("HS-Y", "hs", "year"),
        "month": ("HS-M", "hs", "month"),
        "day": ("HS-D", "hs", "day"),
        "hour": ("HS-H", "hs", "hour"),
        "luck": ("LP", "hs", "luck"),
    }
    p_lower = palace.lower()
    for key, (abbrev, node_type, position) in pos_map.items():
        if key in p_lower:
            return {"abbrev": abbrev, "node_type": node_type, "position": position}
    return {"abbrev": palace[:4], "node_type": "hs", "position": "unknown"}


def _interaction_title(inter) -> str:
    """Generate a title for an interaction card."""
    type_names = {
        "clash": "六冲 Clash",
        "harmony": "六合 Harmony",
        "three_harmony": "三合 Three Harmony",
        "half_three_harmony": "半三合 Half Harmony",
        "directional_combo": "三会 Directional",
        "punishment": "刑 Punishment",
        "self_punishment": "自刑 Self-Punishment",
        "harm": "害 Harm",
        "destruction": "破 Destruction",
    }
    return type_names.get(inter.interaction_type, inter.interaction_type.replace("_", " ").title())


def build_narrative_analysis(interactions: List[BranchInteraction],
                              shen_sha: List[ShenShaResult],
                              tg_entries: List[TenGodEntry],
                              strength: StrengthAssessment,
                              chart: ChartData) -> dict:
    """Build narrative_analysis matching NarrativeCard.tsx expected fields."""
    cards = []
    seq = 0

    # Cards from branch interactions
    for inter in interactions:
        seq += 1
        polarity = "negative" if inter.interaction_type in ("clash", "punishment", "self_punishment", "harm", "destruction") else "positive"
        # Build formula from branches involved
        branches_cn = []
        for p in inter.palaces:
            p_lower = p.lower()
            if "year" in p_lower:
                branches_cn.append(chart.pillars["year"].branch_chinese)
            elif "month" in p_lower:
                branches_cn.append(chart.pillars["month"].branch_chinese)
            elif "day" in p_lower:
                branches_cn.append(chart.pillars["day"].branch_chinese)
            elif "hour" in p_lower:
                branches_cn.append(chart.pillars["hour"].branch_chinese)
            elif "luck" in p_lower and chart.luck_pillar:
                branches_cn.append(chart.luck_pillar.branch_chinese)

        # Extract element from description (e.g., "→ Fire" or "Fire局")
        element = None
        desc = inter.description
        for el in ("Wood", "Fire", "Earth", "Metal", "Water"):
            if el in desc:
                element = el
                break

        cards.append({
            "seq": seq,
            "id": f"narrative_{seq}",
            "category": "interaction",
            "type": inter.interaction_type,
            "icon": _interaction_icon(inter.interaction_type),
            "title": _interaction_title(inter),
            "chinese_name": inter.chinese_name,
            "polarity": polarity,
            "element": element,
            "formula": inter.description,
            "match": " + ".join(branches_cn) if branches_cn else None,
            "description": inter.description,
            "palaces": inter.palaces,
            "pillar_refs": [_palace_to_pillar_ref(p) for p in inter.palaces],
            "severity": inter.severity,
            "priority": 3 if inter.severity == "severe" else 2 if inter.severity == "moderate" else 1,
        })

    # Cards from present Shen Sha
    for s in shen_sha:
        if not s.present:
            continue
        seq += 1
        polarity = "positive" if s.nature == "auspicious" else "negative" if s.nature == "inauspicious" else "neutral"
        cards.append({
            "seq": seq,
            "id": f"narrative_{seq}",
            "category": "shen_sha",
            "type": s.name_english.lower().replace(" ", "_") if s.name_english else "star",
            "icon": "flow",  # Default icon for shen sha
            "title": f"{s.name_chinese} {s.name_english}",
            "chinese_name": s.name_chinese,
            "polarity": polarity,
            "element": None,
            "formula": s.derivation or None,
            "match": s.palace if s.palace else None,
            "description": s.impact or f"{s.name_english} present in {s.palace or 'chart'}",
            "palaces": [s.palace] if s.palace else [],
            "pillar_refs": [_palace_to_pillar_ref(s.palace)] if s.palace else [],
            "severity": s.severity,
            "priority": 2 if s.nature in ("auspicious", "inauspicious") else 1,
        })

    # Sort by priority desc, then seq asc
    cards.sort(key=lambda c: (-c["priority"], c["seq"]))

    # Re-assign seq after sorting for display order
    for i, card in enumerate(cards):
        card["seq"] = i + 1

    return {
        "all_chronological": cards,
        "narratives": cards[:15],
        "narratives_by_category": {
            "interaction": [c for c in cards if c["category"] == "interaction"],
            "shen_sha": [c for c in cards if c["category"] == "shen_sha"],
        },
        "element_context": {
            "daymaster": chart.day_master,
            "daymaster_element": chart.dm_element,
            "strength": strength.verdict,
        },
        "remedies": [],
        "quick_remedies": [],
    }


# =============================================================================
# MAPPINGS (static reference data for frontend)
# =============================================================================

def build_mappings() -> dict:
    """Build the mappings dict reusing STEMS/BRANCHES constants."""
    return {
        "heavenly_stems": {
            stem_id: {
                "id": stem_id,
                "pinyin": stem_id,
                "chinese": stem_data["chinese"],
                "english": stem_id,
                "hex_color": stem_data["color"],
            }
            for stem_id, stem_data in STEMS.items()
        },
        "earthly_branches": {
            branch_id: {
                "id": branch_id,
                "chinese": branch_data["chinese"],
                "animal": branch_data["animal"],
                "hex_color": branch_data["color"],
                "qi": [
                    {
                        "stem": qi_tuple[0],
                        "score": qi_tuple[1],
                        "stem_chinese": STEMS.get(qi_tuple[0], {}).get("chinese", "?"),
                        "element": STEMS.get(qi_tuple[0], {}).get("element", "?"),
                        "polarity": STEMS.get(qi_tuple[0], {}).get("polarity", "?"),
                        "hex_color": STEMS.get(qi_tuple[0], {}).get("color", "#ccc"),
                    }
                    for qi_tuple in branch_data.get("qi", [])
                ],
            }
            for branch_id, branch_data in BRANCHES.items()
        },
        "ten_gods": TEN_GODS,
        "event_types": {
            "registration": {"hex_color": "#60a5fa", "icon": "", "label": "Registration"},
            "seasonal": {"hex_color": "#fbbf24", "icon": "", "label": "Seasonal"},
            "controlling": {"hex_color": "#f87171", "icon": "", "label": "Controlling"},
            "controlled": {"hex_color": "#f87171", "icon": "", "label": "Controlled"},
            "control": {"hex_color": "#f87171", "icon": "", "label": "Control"},
            "producing": {"hex_color": "#4ade80", "icon": "", "label": "Producing"},
            "produced": {"hex_color": "#4ade80", "icon": "", "label": "Produced"},
            "generation": {"hex_color": "#4ade80", "icon": "", "label": "Generation"},
            "combination": {"hex_color": "#c084fc", "icon": "", "label": "Combination"},
            "conflict": {"hex_color": "#fb923c", "icon": "", "label": "Conflict"},
            "conflict_aggressor": {"hex_color": "#fb923c", "icon": "", "label": "Conflict"},
            "conflict_victim": {"hex_color": "#fb923c", "icon": "", "label": "Conflict"},
            "same_element": {"hex_color": "#2dd4bf", "icon": "", "label": "Same Element"},
        },
        "ten_gods_styling": {
            "DM": {"hex_color": "#9333ea", "bg_hex": "#f3e8ff", "label": "Day Master"},
            "F": {"hex_color": "#2563eb", "bg_hex": "#dbeafe", "label": "Friend"},
            "RW": {"hex_color": "#3b82f6", "bg_hex": "#eff6ff", "label": "Rob Wealth"},
            "EG": {"hex_color": "#16a34a", "bg_hex": "#dcfce7", "label": "Eating God"},
            "HO": {"hex_color": "#22c55e", "bg_hex": "#f0fdf4", "label": "Hurting Officer"},
            "IW": {"hex_color": "#ca8a04", "bg_hex": "#fef9c3", "label": "Indirect Wealth"},
            "DW": {"hex_color": "#eab308", "bg_hex": "#fefce8", "label": "Direct Wealth"},
            "7K": {"hex_color": "#dc2626", "bg_hex": "#fee2e2", "label": "Seven Killings"},
            "DO": {"hex_color": "#ef4444", "bg_hex": "#fef2f2", "label": "Direct Officer"},
            "IR": {"hex_color": "#4b5563", "bg_hex": "#f3f4f6", "label": "Indirect Resource"},
            "DR": {"hex_color": "#6b7280", "bg_hex": "#f9fafb", "label": "Direct Resource"},
        },
        "elements": {
            "Wood": {"hex_color": "#22c55e", "hex_color_yang": "#16a34a", "hex_color_yin": "#4ade80"},
            "Fire": {"hex_color": "#ef4444", "hex_color_yang": "#dc2626", "hex_color_yin": "#f87171"},
            "Earth": {"hex_color": "#ca8a04", "hex_color_yang": "#a16207", "hex_color_yin": "#eab308"},
            "Metal": {"hex_color": "#6b7280", "hex_color_yang": "#4b5563", "hex_color_yin": "#9ca3af"},
            "Water": {"hex_color": "#3b82f6", "hex_color_yang": "#2563eb", "hex_color_yin": "#60a5fa"},
        },
    }


# =============================================================================
# MASTER ADAPTER FUNCTION
# =============================================================================

def adapt_to_frontend(chart: ChartData, results: dict) -> dict:
    """
    Master adapter: translates comprehensive engine results into the exact
    JSON shape the frontend expects from /api/analyze_bazi.

    Args:
        chart: The ChartData object
        results: Dict from analyze_for_api() containing all analysis results

    Returns:
        Dict with all frontend-expected keys (nodes, scores, analyses, etc.)
    """
    strength = results["strength"]
    tg_entries = results["ten_god_entries"]
    tg_classification = results["ten_god_classification"]
    interactions = results["interactions"]
    shen_sha = results["shen_sha"]
    predictions = results["predictions"]
    env = results["environment"]
    comprehensive_report = results.get("comprehensive_report", "")

    # 1. Build all nodes
    nodes = build_all_nodes(chart)

    # 2. Map interaction badges onto nodes
    map_interactions_to_badges(interactions, chart, nodes)

    # 3. Collect red flags
    flags = _collect_red_flags(chart, strength, tg_classification, interactions, shen_sha)

    # 4. Build element scores
    base_score, natal_score, post_score = build_element_scores(chart)

    # 5. Assemble response
    response = {}

    # Nodes
    response.update(nodes)

    # Scores
    response["base_element_score"] = base_score
    response["natal_element_score"] = natal_score
    response["post_element_score"] = post_score

    # Interactions
    response["interactions"] = build_interaction_dict(interactions)

    # Daymaster analysis
    response["daymaster_analysis"] = build_daymaster_analysis(strength, chart)

    # Life aspects
    response["health_analysis"] = build_health_analysis(flags, strength, chart)
    response["wealth_analysis"] = build_wealth_analysis(flags, strength, tg_classification, chart)
    response["learning_analysis"] = build_learning_analysis(flags, strength, tg_classification, chart)

    # Ten Gods detail
    response["ten_gods_detail"] = build_ten_gods_detail(tg_entries, tg_classification, chart)

    # Special stars
    response["special_stars"] = build_special_stars(shen_sha)

    # Recommendations
    response["recommendations"] = build_recommendations(predictions, flags, strength, env)

    # Narrative
    response["narrative_analysis"] = build_narrative_analysis(
        interactions, shen_sha, tg_entries, strength, chart)

    # Pattern engine analysis (stub for backward compatibility)
    response["pattern_engine_analysis"] = {
        "enhanced_patterns": [],
        "domain_analysis": {},
        "recommendations": response["recommendations"],
        "special_stars": response["special_stars"],
    }

    # Wealth storage (stub)
    response["wealth_storage_analysis"] = {}

    # Unit tracker (stub)
    response["unit_tracker"] = None

    # Mappings
    response["mappings"] = build_mappings()

    # Comprehensive report (new field)
    response["comprehensive_report"] = comprehensive_report

    return response
