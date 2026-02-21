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
from ..wealth_storage import (
    DM_WEALTH_STORAGE, STORAGE_OPENER, LARGE_WEALTH_STORAGE, WEALTH_ELEMENT_STEMS,
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
from .strength import count_elements, count_all_elements, adjust_elements_for_interactions, apply_seasonal_scaling
from .qi_phase_analysis import analyze_qi_phases
from .spiritual_sensitivity import assess_spiritual_sensitivity


# =============================================================================
# WEALTH STORAGE COMPUTATION (財庫)
# =============================================================================

def _compute_wealth_storage(chart: ChartData) -> dict:
    """
    Compute wealth storage (財庫) from ChartData for frontend display.
    Uses the same theory as bazingse.py's detect_wealth_storage() but
    operates on ChartData instead of the nodes dict.
    """
    dm_stem = chart.day_master
    dm_element = chart.dm_element
    wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    wealth_stems = WEALTH_ELEMENT_STEMS.get(wealth_element, [])
    storage_branch = DM_WEALTH_STORAGE.get(dm_element)
    opener_branch = STORAGE_OPENER.get(storage_branch) if storage_branch else None

    if not storage_branch:
        return {
            "daymaster_element": dm_element, "daymaster_stem": dm_stem,
            "wealth_element": wealth_element, "wealth_stems": wealth_stems,
            "wealth_storage_branch": None, "opener_branch": None,
            "storages": [], "all_storages": [], "summary": f"No storage mapping for {dm_element} DM",
        }

    # Collect all pillars (natal + luck + time period)
    all_pillars: List[Tuple[str, Pillar]] = []
    for pos in ["year", "month", "day", "hour"]:
        if pos in chart.pillars:
            all_pillars.append((pos, chart.pillars[pos]))
    if chart.luck_pillar:
        all_pillars.append(("luck_pillar", chart.luck_pillar))
    for pos, p in chart.time_period_pillars.items():
        all_pillars.append((pos, p))

    storages = []

    for pos, pillar in all_pillars:
        if pillar.branch != storage_branch:
            continue

        # Check Large Wealth Storage (DM stem on own storage branch)
        pillar_key = f"{pillar.stem}-{pillar.branch}"
        is_large = pillar_key in LARGE_WEALTH_STORAGE

        # Check FILLER: wealth stems in OTHER positions
        filler_positions = []
        for other_pos, other_p in all_pillars:
            if other_pos == pos:
                continue
            if other_p.stem in wealth_stems:
                filler_positions.append(f"{other_pos}(HS)")
            # Check primary qi of branch
            if other_p.hidden_stems:
                primary_stem = other_p.hidden_stems[0][0]
                if primary_stem in wealth_stems:
                    filler_positions.append(f"{other_pos}(EB)")
        is_filled = len(filler_positions) > 0

        # Check OPENER: clash branch in OTHER positions
        opener_positions = [other_pos for other_pos, other_p in all_pillars
                           if other_pos != pos and other_p.branch == opener_branch]
        is_opened = len(opener_positions) > 0

        # Activation level
        if is_filled and is_opened:
            activation = "maximum"
        elif is_filled or is_opened:
            activation = "activated"
        else:
            activation = "latent"

        branch_chinese = BRANCHES.get(storage_branch, {}).get("chinese", storage_branch)
        stem_chinese = STEMS.get(pillar.stem, {}).get("chinese", pillar.stem)

        storages.append({
            "position": pos,
            "branch": storage_branch,
            "branch_chinese": branch_chinese,
            "pillar": pillar_key,
            "pillar_chinese": f"{stem_chinese}{branch_chinese}",
            "is_large": is_large,
            "storage_type": "wealth",
            "stored_element": wealth_element,
            "wealth_element": wealth_element,
            "filler_stems": wealth_stems,
            "is_filled": is_filled,
            "filler_positions": filler_positions,
            "opener_branch": opener_branch,
            "is_opened": is_opened,
            "opener_positions": opener_positions,
            "activation_level": activation,
        })

    # Summary
    total = len(storages)
    maximum = sum(1 for s in storages if s["activation_level"] == "maximum")
    activated = sum(1 for s in storages if s["activation_level"] != "latent")
    large_count = sum(1 for s in storages if s["is_large"])
    branch_chinese = BRANCHES.get(storage_branch, {}).get("chinese", storage_branch)

    if total == 0:
        summary = (f"No wealth storage (财库) found for {dm_element} DM. "
                   f"Storage branch {storage_branch} ({branch_chinese}) not in chart.")
    else:
        parts = []
        if large_count:
            parts.append(f"{large_count} Large (大财库)")
        if total - large_count:
            parts.append(f"{total - large_count} Standard (财库)")
        summary = f"Found {', '.join(parts)} for {dm_element} DM. "
        if maximum:
            summary += f"{maximum} at MAXIMUM activation (filled + opened). "
        elif activated:
            summary += f"{activated}/{total} activated. "
        else:
            summary += f"All {total} latent (locked). "

    return {
        "daymaster_element": dm_element, "daymaster_stem": dm_stem,
        "wealth_element": wealth_element, "wealth_stems": wealth_stems,
        "wealth_storage_branch": storage_branch, "opener_branch": opener_branch,
        "storages": storages, "all_storages": storages,
        "summary": summary,
    }


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
    "annual":      ("hs_yl",   "eb_yl"),
    "monthly":     ("hs_ml",   "eb_ml"),
    "daily":       ("hs_dl",   "eb_dl"),
    "hourly":      ("hs_hl",   "eb_hl"),
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

    # Time-period pillars
    for tp_pos, tp_pillar in chart.time_period_pillars.items():
        if tp_pos in POSITION_TO_NODE:
            hs_key, eb_key = POSITION_TO_NODE[tp_pos]
            nodes[hs_key] = build_stem_node(tp_pillar, chart)
            nodes[eb_key] = build_branch_node(tp_pillar, chart)

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
    for pos, pillar in chart.time_period_pillars.items():
        if pillar.branch == branch and pos in POSITION_TO_NODE:
            return POSITION_TO_NODE[pos][1]
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

def build_element_scores(chart: ChartData,
                         interactions: list = None) -> Tuple[dict, dict, dict]:
    """
    2-tier element scores: natal (4 pillars) vs full (natal + LP + time-period).
    Interaction-adjusted so element bars match DM strength percentage.
    Returns (base_element_score, natal_element_score, post_element_score)
    as {stem_name: float} dicts.
    """
    natal_counts = count_elements(chart)      # Natal 4 pillars only
    full_counts = count_all_elements(chart)    # Everything

    # Adjust for branch interactions (combinations/clashes)
    if interactions:
        natal_counts = adjust_elements_for_interactions(natal_counts, interactions, chart)
        full_counts = adjust_elements_for_interactions(full_counts, interactions, chart)

    # Apply seasonal scaling (旺相休囚死) — the most important factor
    month_branch = chart.pillars["month"].branch
    natal_counts = apply_seasonal_scaling(natal_counts, month_branch)
    full_counts = apply_seasonal_scaling(full_counts, month_branch)

    def _to_stem_scores(elem_counts):
        scores = {}
        for stem_id in STEMS:
            stem_elem = STEMS[stem_id]["element"]
            scores[stem_id] = round(elem_counts.get(stem_elem, 0) * 50, 1)
        return scores

    natal_scores = _to_stem_scores(natal_counts)
    full_scores = _to_stem_scores(full_counts)

    # base = natal, natal = natal, post = full (includes LP + time periods)
    return natal_scores, dict(natal_scores), full_scores


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

def _build_ten_gods_warnings(tg_entries: List[TenGodEntry],
                              tg_classification: Dict[str, dict],
                              chart: ChartData) -> list:
    """Build per-pillar ten gods warnings in the exact shape the frontend expects."""
    warnings = []
    # Risk ten gods that warrant a warning when visible
    RISK_TEN_GODS = {
        "7K": {
            "en": "Seven Killings prominent — aggressive energy, risk of conflicts",
            "zh": "七殺旺 — 攻擊性強，易有衝突",
            "id": "Tujuh Pembunuh menonjol — energi agresif, risiko konflik",
        },
        "HO": {
            "en": "Hurting Officer prominent — rebellious, challenges authority",
            "zh": "傷官旺 — 叛逆，挑戰權威",
            "id": "Hurting Officer menonjol — pemberontak, menantang otoritas",
        },
        "RW": {
            "en": "Rob Wealth present — wealth drained through others, competition",
            "zh": "劫財現 — 財被他人所奪，競爭激烈",
            "id": "Rob Wealth hadir — kekayaan terkuras oleh orang lain, persaingan",
        },
    }

    seen = set()  # Avoid duplicate warnings per (ten_god, position)
    for entry in tg_entries:
        if not entry.visible:
            continue
        if entry.abbreviation not in RISK_TEN_GODS:
            continue
        key = (entry.abbreviation, entry.position)
        if key in seen:
            continue
        seen.add(key)
        msgs = RISK_TEN_GODS[entry.abbreviation]
        info = TEN_GOD_INFO.get(entry.abbreviation, {})
        warnings.append({
            "ten_god": entry.abbreviation,
            "ten_god_chinese": info.get("chinese", entry.chinese),
            "ten_god_english": info.get("english", entry.english),
            "pillar": entry.position,
            "message": msgs["en"],
            "message_chinese": msgs["zh"],
            "message_id": msgs["id"],
        })

    # Absent spouse star warning on day pillar
    spouse = check_spouse_star(chart, tg_classification)
    if spouse["is_critical_absent"]:
        star_abbr = spouse["star"]
        info = TEN_GOD_INFO.get(star_abbr, {})
        warnings.append({
            "ten_god": star_abbr,
            "ten_god_chinese": info.get("chinese", ""),
            "ten_god_english": info.get("english", ""),
            "pillar": "day",
            "message": f"{info.get('english', star_abbr)} (spouse star) absent from chart",
            "message_chinese": f"{info.get('chinese', '')}（配偶星）不見於命盤",
            "message_id": f"{info.get('english', star_abbr)} (bintang pasangan) tidak ada dalam bagan",
        })

    # Absent children star warning on hour pillar
    children = check_children_star(chart, tg_classification)
    if not children["any_present"]:
        star_abbr = children["primary_star"]
        info = TEN_GOD_INFO.get(star_abbr, {})
        warnings.append({
            "ten_god": star_abbr,
            "ten_god_chinese": info.get("chinese", ""),
            "ten_god_english": info.get("english", ""),
            "pillar": "hour",
            "message": "Children stars absent from chart",
            "message_chinese": "子女星不見於命盤",
            "message_id": "Bintang anak tidak ada dalam bagan",
        })

    # Chart-level pattern warnings mapped to representative pillar/ten god
    patterns = analyze_ten_god_patterns(chart, tg_classification)
    PATTERN_TO_TG = {
        "companion_heavy": "RW",
        "output_heavy": "HO",
        "ho_prominent": "HO",
        "7k_prominent": "7K",
        "rw_present": "RW",
        "no_wealth": "DW",
        "no_officer": "DO",
        "no_resource": "DR",
    }
    PATTERN_TO_PILLAR = {
        "no_wealth": "day",
        "no_officer": "month",
        "no_resource": "month",
    }
    for p in patterns:
        tg_abbr = PATTERN_TO_TG.get(p["pattern"])
        if not tg_abbr:
            continue
        # Skip if we already have a per-entry warning for this ten god
        pillar = PATTERN_TO_PILLAR.get(p["pattern"], "day")
        if (tg_abbr, pillar) in seen:
            continue
        seen.add((tg_abbr, pillar))
        info = TEN_GOD_INFO.get(tg_abbr, {})
        warnings.append({
            "ten_god": tg_abbr,
            "ten_god_chinese": info.get("chinese", ""),
            "ten_god_english": info.get("english", ""),
            "pillar": pillar,
            "message": p["description"],
            "message_chinese": p["description"],
            "message_id": p["description"],
        })

    return warnings


def build_ten_gods_detail(tg_entries: List[TenGodEntry],
                           tg_classification: Dict[str, dict],
                           chart: ChartData) -> dict:
    """Build ten_gods_detail matching frontend shape."""
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

    # Warnings in frontend-expected shape
    warnings = _build_ten_gods_warnings(tg_entries, tg_classification, chart)

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
        "annual": ("YL", "hs", "annual"),
        "monthly": ("ML", "hs", "monthly"),
        "daily": ("DL", "hs", "daily"),
        "hourly": ("HL", "hs", "hourly"),
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
# CLIENT SUMMARY (structured JSON for non-technical frontend)
# =============================================================================

def _summary_chart_overview(chart: ChartData) -> dict:
    """Section: chart overview with DM nature."""
    from .templates import DM_NATURE, _pick
    dm_info = STEMS[chart.day_master]
    key = (dm_info["element"], dm_info["polarity"].capitalize())
    nature = DM_NATURE.get(key, {})
    items = [
        {"label": "Day Master", "value": f"{nature.get('name', chart.day_master)} ({nature.get('chinese', dm_info['chinese'])}) — {_pick(nature.get('nature', ['']))}"},
        {"label": "Personality", "value": nature.get("personality", "")},
    ]
    return {
        "id": "chart_overview",
        "title": "Your Chart",
        "title_zh": "命盤概覽",
        "items": items,
    }


def _summary_strength(strength: StrengthAssessment, chart: ChartData) -> dict:
    """Section: DM strength assessment with WHY-reasoning for favorable/unfavorable."""
    from .templates import STRENGTH_VERDICTS, STRENGTH_EXPLANATION, _pick

    text = _pick(STRENGTH_VERDICTS.get(strength.verdict, ["No assessment available."]))

    dm_element = chart.dm_element
    dm_name = f"{chart.day_master} {dm_element}"
    resource = ELEMENT_CYCLES["generated_by"].get(dm_element, "")
    output = ELEMENT_CYCLES["generating"].get(dm_element, "")
    wealth = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    officer = ELEMENT_CYCLES["controlled_by"].get(dm_element, "")

    # Role labels for each element relative to DM
    if strength.verdict in ("weak", "extremely_weak"):
        role_map = {
            dm_element: "companion — strengthens you",
            resource: "resource — generates your " + dm_element,
            output: "output — exhausts your weak " + dm_element,
            wealth: "wealth — drains your weak " + dm_element,
            officer: "officer — attacks/controls " + dm_element,
        }
    elif strength.verdict in ("strong", "extremely_strong"):
        role_map = {
            dm_element: "companion — overloads the chart",
            resource: "resource — fuels already excessive " + dm_element,
            output: "output — channels excess energy",
            wealth: "wealth — absorbs your strength",
            officer: "officer — disciplines your energy",
        }
    else:
        role_map = {
            dm_element: "companion",
            resource: "resource — generates " + dm_element,
            output: "output — channels energy",
            wealth: "wealth — productive use of strength",
            officer: "officer — can tip balance",
        }

    items = [
        {"label": "Score", "value": f"{strength.score}% (20% = balanced)"},
    ]

    # Useful God with simulation-based reason
    ug = strength.useful_god
    ug_pct = strength.element_percentages.get(ug, 0)
    ug_reason = f"most deficient at {ug_pct}% — adding it brings the chart closest to balance"
    items.append({"label": "Useful God", "value": f"{ug} — {ug_reason}"})

    # Favorable with role explanation
    fav_explained = []
    for elem in strength.favorable_elements:
        role = role_map.get(elem, "")
        fav_explained.append(f"{elem} ({role})" if role else elem)
    items.append({"label": "Favorable", "value": ", ".join(fav_explained)})

    # Unfavorable with role explanation
    unfav_explained = []
    for elem in strength.unfavorable_elements:
        role = role_map.get(elem, "")
        unfav_explained.append(f"{elem} ({role})" if role else elem)
    items.append({"label": "Unfavorable", "value": ", ".join(unfav_explained)})

    # Best element pairs (luck pillar combos)
    if strength.best_element_pairs:
        pair_parts = []
        for p in strength.best_element_pairs[:3]:
            elems = "+".join(p["elements"])
            pair_parts.append(elems)
        items.append({"label": "Best Luck Combos", "value": ", ".join(pair_parts)})

    # Explanation paragraph
    verdict_key = strength.verdict if strength.verdict in STRENGTH_EXPLANATION else "neutral"
    explanation = STRENGTH_EXPLANATION[verdict_key].format(
        dm_name=dm_name, dm_element=dm_element, score=strength.score,
        resource=resource, output=output, wealth=wealth, officer=officer,
        useful_god=strength.useful_god,
        unfav_list=", ".join(strength.unfavorable_elements),
    )
    items.append({"label": "Why?", "value": explanation})

    severity = ("strong" if strength.verdict in ("strong", "extremely_strong")
                else "weak" if strength.verdict in ("weak", "extremely_weak")
                else "neutral")

    return {
        "id": "strength",
        "title": "Strength Assessment",
        "title_zh": "日主強弱",
        "severity": severity,
        "text": text,
        "items": items,
    }


def _summary_ten_gods(chart: ChartData, tg_classification: Dict[str, dict]) -> dict:
    """Section: ten gods profile."""
    from .templates import TEN_GOD_INTERPRETATIONS, _pick
    items = []
    dominant = []
    for abbr, info in tg_classification.items():
        strength_level = info.get("strength", "ABSENT")
        templates = TEN_GOD_INTERPRETATIONS.get(abbr, {})
        text = _pick(templates.get(strength_level, templates.get("PRESENT", [""])))
        if not text:
            text = f"{info.get('english', abbr)} ({info.get('chinese', '')}) is {strength_level}"
        severity = "warning" if strength_level == "PROMINENT" and abbr in ("7K", "HO", "RW") else "info" if strength_level == "PROMINENT" else "alert" if strength_level == "ABSENT" and abbr in ("DW", "DO") else None
        items.append({
            "label": f"{abbr} ({info.get('chinese', '')})",
            "value": text,
            **({"severity": severity} if severity else {}),
        })
        if strength_level == "PROMINENT":
            dominant.append(info.get("english", abbr))
    text = f"Dominant: {', '.join(dominant)}" if dominant else "No dominant ten gods"
    return {
        "id": "ten_gods",
        "title": "Ten Gods Profile",
        "title_zh": "十神分析",
        "text": text,
        "items": items,
    }


def _summary_interactions(interactions: List[BranchInteraction]) -> dict:
    """Section: branch interactions summary."""
    positive_types = {"harmony", "three_harmony", "half_three_harmony", "directional_combo"}
    pos_count = sum(1 for i in interactions if i.interaction_type in positive_types)
    neg_count = len(interactions) - pos_count
    items = []
    for inter in interactions[:8]:
        polarity = "positive" if inter.interaction_type in positive_types else "negative"
        severity = "positive" if polarity == "positive" else inter.severity
        palaces_str = " vs ".join(inter.palaces) if inter.palaces else ""
        items.append({
            "label": f"{inter.chinese_name} {inter.interaction_type.replace('_', ' ').title()}",
            "value": f"{palaces_str} — {inter.description}" if palaces_str else inter.description,
            "severity": severity,
        })
    return {
        "id": "interactions",
        "title": "Branch Interactions",
        "title_zh": "地支關係",
        "text": f"{pos_count} positive, {neg_count} negative interactions found",
        "items": items,
    }


def _summary_shen_sha(shen_sha: List[ShenShaResult]) -> dict:
    """Section: special stars."""
    from .templates import SHEN_SHA_IMPACTS, _pick
    items = []
    for s in shen_sha:
        if not s.present:
            continue
        templates = SHEN_SHA_IMPACTS.get(s.name_chinese, {})
        text = _pick(templates.get("present", [f"{s.name_english} present"]))
        severity = "positive" if s.nature == "auspicious" else "negative" if s.nature == "inauspicious" else "info"
        items.append({
            "label": f"{s.name_chinese} {s.name_english}",
            "value": text,
            "severity": severity,
        })
    return {
        "id": "shen_sha",
        "title": "Special Stars",
        "title_zh": "神煞",
        "items": items,
    }


def _summary_red_flags(flags: Dict[str, List[RedFlag]]) -> dict:
    """Section: red flags grouped by life area."""
    items = []
    for area, area_flags in flags.items():
        for f in area_flags:
            items.append({
                "label": area.capitalize(),
                "value": f"{f.indicator_name} — {f.description}",
                "severity": f.severity,
            })
    return {
        "id": "red_flags",
        "title": "Red Flags",
        "title_zh": "警示",
        "items": items,
    }


def _summary_luck_pillar(chart: ChartData, strength: StrengthAssessment) -> Optional[dict]:
    """Section: current luck pillar (full tier only)."""
    if not chart.luck_pillar:
        return None
    lp = chart.luck_pillar
    lp_stem_info = STEMS[lp.stem]
    from ..derived import get_ten_god
    tg = get_ten_god(chart.day_master, lp.stem)
    tg_label = f"{tg[1]} ({tg[2]})" if tg else ""
    text = f"{lp.stem_chinese}{lp.branch_chinese} ({lp.stem} {lp.branch}) — {tg_label} decade"
    return {
        "id": "luck_pillar",
        "title": "Current Luck Pillar",
        "title_zh": "大運分析",
        "text": text,
    }


def _summary_health(chart: ChartData, strength: StrengthAssessment) -> dict:
    """Section: health based on element balance + seasonal states + control cycle.

    Three layers of analysis:
    1. Element balance: deficient/excess elements -> organ vulnerability
    2. Seasonal state: elements in Dead/Trapped state -> heightened risk
    3. Control cycle: weak controller -> uncontrolled target organ
    """
    from .templates import HEALTH_ELEMENT_MAP, CONTROL_CYCLE_EXPLANATIONS

    elem_counts = count_elements(chart)
    total = sum(elem_counts.values())
    avg = total / 5 if total > 0 else 1.0

    # Get seasonal states for all elements from month branch
    month_branch = chart.pillars["month"].branch
    seasonal_states = BRANCHES[month_branch].get("element_states", {})

    # Detect control cycle imbalances
    ELEMENT_CONTROLS_MAP = {
        "Wood": "Earth", "Fire": "Metal", "Earth": "Water",
        "Metal": "Wood", "Water": "Fire",
    }
    control_imbalances = {}  # controlled_element -> controller info
    for controller, controlled in ELEMENT_CONTROLS_MAP.items():
        controller_state = seasonal_states.get(controller, "Resting")
        controller_count = elem_counts.get(controller, 0)
        # Weak controller: Dead/Trapped state OR very low count
        if controller_state in ("Dead", "Trapped") or controller_count < avg * 0.3:
            control_imbalances[controlled] = {
                "controller": controller,
                "controller_state": controller_state,
                "controller_count": controller_count,
            }

    items = []
    SEASONAL_WEIGHT = {"Dead": 2.0, "Trapped": 1.5, "Resting": 1.0, "Strengthening": 0.7, "Prosperous": 0.5}

    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        pct = (count / total * 100) if total > 0 else 20
        organ_info = HEALTH_ELEMENT_MAP.get(elem, {})
        yin_organ = organ_info.get("yin_organ", elem)
        body_parts = organ_info.get("body_parts", "")
        seasonal_state = seasonal_states.get(elem, "Resting")

        reasons = []
        severity = None

        # Layer 1: Element balance
        if count < avg * 0.5:
            reasons.append(f"{elem} severely deficient ({pct:.0f}%). {organ_info.get('deficiency', 'vulnerability')}")
            severity = "warning"
        elif count < avg * 0.75:
            reasons.append(f"{elem} below average ({pct:.0f}%). Mild {yin_organ.split('(')[0].strip().lower()} vulnerability")
            severity = "mild"
        elif count > avg * 1.8:
            reasons.append(f"{elem} in excess ({pct:.0f}%). {organ_info.get('excess', 'overactive')}")
            severity = "warning"
        elif count > avg * 1.4:
            reasons.append(f"{elem} above average ({pct:.0f}%). Watch for: {organ_info.get('excess', 'overactivity')}")
            severity = "mild"

        # Layer 2: Seasonal vulnerability
        if seasonal_state in ("Dead", "Trapped"):
            state_label = "Dead (死)" if seasonal_state == "Dead" else "Trapped (囚)"
            reasons.append(f"{elem} in {state_label} seasonal state — heightened {yin_organ.split('(')[0].strip().lower()} vulnerability")
            if severity is None:
                severity = "mild"
            elif severity == "mild":
                severity = "warning"

        # Layer 3: Control cycle imbalance
        if elem in control_imbalances:
            imb = control_imbalances[elem]
            ctrl = imb["controller"]
            explanation = CONTROL_CYCLE_EXPLANATIONS.get((ctrl, elem), "")
            if explanation:
                reasons.append(explanation)
            else:
                reasons.append(f"{ctrl} is too weak to control {elem} — {yin_organ.split('(')[0].strip().lower()} system unregulated")
            if severity is None:
                severity = "mild"
            elif severity == "mild":
                severity = "warning"

        # Only include elements with issues
        if reasons:
            items.append({
                "label": f"{yin_organ} ({elem})",
                "value": ". ".join(reasons) + f". Body parts: {body_parts}.",
                "severity": severity or "info",
            })

    # If no issues found, show balanced message
    if not items:
        items.append({
            "label": "Overall",
            "value": "Element balance is healthy. No significant organ system vulnerabilities detected.",
            "severity": "positive",
        })

    return {
        "id": "health",
        "title": "Health",
        "title_zh": "健康",
        "items": items,
    }


def _summary_remedies(strength: StrengthAssessment, chart: ChartData) -> dict:
    """Section: remedies with health cross-linking."""
    from .templates import ELEMENT_REMEDIES, HEALTH_ELEMENT_MAP, HEALTH_BEHAVIORAL_REMEDIES

    useful = strength.useful_god
    remedies = ELEMENT_REMEDIES.get(useful, {})
    items = []

    if remedies:
        colors = ", ".join(remedies.get("colors", []))
        items.append({"label": "Colors", "value": f"Wear {colors} ({useful} element)"})
        items.append({"label": "Direction", "value": remedies.get("direction", "")})
        industries = ", ".join(remedies.get("industries", [])[:5])
        items.append({"label": "Industries", "value": industries})
        avoid = ", ".join(remedies.get("avoid_colors", []))
        if avoid:
            items.append({"label": "Avoid Colors", "value": avoid})

    # Health-aware remedies: check for deficient elements
    elem_counts = count_elements(chart)
    total = sum(elem_counts.values())
    avg = total / 5 if total > 0 else 1.0

    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        if count < avg * 0.5:
            elem_remedies = ELEMENT_REMEDIES.get(elem, {})
            organ = HEALTH_ELEMENT_MAP.get(elem, {}).get("yin_organ", elem).split("(")[0].strip()
            behavioral = HEALTH_BEHAVIORAL_REMEDIES.get(elem, "")

            if elem == useful:
                # Synergy: useful god already covers this element
                items.append({
                    "label": f"Health + Useful God synergy ({elem})",
                    "value": f"Your useful god ({useful}) also addresses your {organ.lower()} health. {behavioral}",
                    "severity": "positive",
                })
            else:
                # Secondary element remedy
                elem_colors = ", ".join(elem_remedies.get("colors", [])[:2])
                items.append({
                    "label": f"Health: {organ} ({elem})",
                    "value": f"Low {elem} weakens {organ.lower()}. Secondary remedy: add {elem_colors} accessories. {behavioral}",
                    "severity": "info",
                })

    # Excess element warnings
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        if count > avg * 1.8:
            organ = HEALTH_ELEMENT_MAP.get(elem, {}).get("yin_organ", elem).split("(")[0].strip()
            behavioral = HEALTH_BEHAVIORAL_REMEDIES.get(elem, "")
            items.append({
                "label": f"Health: {organ} excess ({elem})",
                "value": f"High {elem} overloads {organ.lower()}. Reduce {elem} element exposure. {behavioral}",
                "severity": "warning",
            })

    return {
        "id": "remedies",
        "title": "Remedies",
        "title_zh": "化解建議",
        "items": items,
    }


def _summary_predictions_timeline(predictions: Dict[str, list]) -> Optional[dict]:
    """Section: year-specific prediction highlights (full/timeline tier only)."""
    items = []
    for event_type, events in predictions.items():
        for ev in events[:2]:
            factors_str = "; ".join(ev.factors[:2]) if ev.factors else ""
            items.append({
                "label": event_type.replace("_", " ").title(),
                "value": f"Year {ev.year} (age {ev.age}) — score {ev.score:.0f}. {factors_str}",
            })
    if not items:
        return None
    return {
        "id": "predictions",
        "title": "Year Predictions",
        "title_zh": "流年預測",
        "items": items[:8],
    }


def _summary_natal_predictions(chart: ChartData,
                                tg_classification: Dict[str, dict],
                                strength: StrengthAssessment,
                                predictions: Dict[str, list],
                                flags: Dict[str, List[RedFlag]]) -> dict:
    """Section: life predictions from natal chart structure.
    Marriage, divorce risk, children, wealth potential — with reasons.
    """
    from .ten_gods import check_spouse_star, check_children_star
    items = []

    # --- MARRIAGE ---
    spouse = check_spouse_star(chart, tg_classification)
    spouse_star = spouse["star"]
    spouse_label = spouse["label"]
    spouse_strength = spouse["strength"]

    # Peach Blossom / romance indicators
    rw_strength = tg_classification.get("RW", {}).get("strength", "ABSENT")
    ho_strength = tg_classification.get("HO", {}).get("strength", "ABSENT")

    marriage_reasons = []
    if spouse_strength == "ABSENT":
        marriage_outlook = "DIFFICULT"
        marriage_reasons.append(f"{spouse_label} completely absent from natal chart")
        severity = "severe"
    elif spouse_strength == "HIDDEN_ONLY":
        marriage_outlook = "LATE"
        marriage_reasons.append(f"{spouse_label} only in hidden stems — marriage comes late or needs effort")
        severity = "warning"
    elif spouse_strength == "PROMINENT":
        marriage_outlook = "STRONG"
        marriage_reasons.append(f"{spouse_label} is prominent — strong marriage affinity")
        severity = "positive"
    else:
        marriage_outlook = "NORMAL"
        marriage_reasons.append(f"{spouse_label} is present — marriage attainable")
        severity = "info"

    # Check for marriage-damaging patterns
    if ho_strength == "PROMINENT" and chart.gender == "female":
        marriage_reasons.append("Hurting Officer prominent — conflicts with husband star")
        if marriage_outlook != "DIFFICULT":
            marriage_outlook = "CHALLENGING"
            severity = "warning"
    if rw_strength == "PROMINENT":
        marriage_reasons.append("Rob Wealth prominent — competition/interference in relationships")
        if marriage_outlook in ("NORMAL", "STRONG"):
            marriage_outlook = "CHALLENGING"
            severity = "warning"

    # Marriage flags
    marriage_flags = flags.get("marriage", [])
    for mf in marriage_flags[:2]:
        marriage_reasons.append(mf.description)

    # Top marriage years
    marriage_preds = predictions.get("marriage", [])
    if marriage_preds:
        top = marriage_preds[0]
        top_reasons = "; ".join(top.factors[:2])
        marriage_reasons.append(f"Best year: {top.year} (age {top.age}, score {top.score:.0f}) — {top_reasons}")

    items.append({
        "label": f"Marriage: {marriage_outlook}",
        "value": " | ".join(marriage_reasons),
        "severity": severity,
    })

    # --- DIVORCE RISK ---
    divorce_preds = predictions.get("divorce", [])
    divorce_reasons = []

    # Check natal chart indicators
    day_branch_clashed = False
    for inter_flag in flags.get("marriage", []):
        if "clash" in inter_flag.indicator_name.lower() or "冲" in inter_flag.indicator_name:
            day_branch_clashed = True
            break

    if spouse_strength == "ABSENT" and rw_strength in ("PROMINENT", "PRESENT"):
        divorce_risk = "HIGH"
        divorce_reasons.append("No spouse star + Rob Wealth present = partner drained away")
        severity = "severe"
    elif day_branch_clashed and ho_strength in ("PROMINENT", "PRESENT"):
        divorce_risk = "ELEVATED"
        divorce_reasons.append("Spouse palace clashed + Hurting Officer = marriage instability")
        severity = "warning"
    elif day_branch_clashed:
        divorce_risk = "MODERATE"
        divorce_reasons.append("Spouse palace has clash — periodic marriage tension")
        severity = "warning"
    elif ho_strength == "PROMINENT":
        divorce_risk = "MODERATE"
        divorce_reasons.append("Prominent Hurting Officer — sharp tongue damages relationships")
        severity = "warning"
    else:
        divorce_risk = "LOW"
        divorce_reasons.append("No major divorce indicators in natal chart")
        severity = "positive"

    if divorce_preds:
        top = divorce_preds[0]
        if top.score >= 40:
            top_reasons = "; ".join(top.factors[:2])
            divorce_reasons.append(f"Highest risk year: {top.year} (age {top.age}, score {top.score:.0f}) — {top_reasons}")

    items.append({
        "label": f"Divorce Risk: {divorce_risk}",
        "value": " | ".join(divorce_reasons),
        "severity": severity,
    })

    # --- CHILDREN ---
    children = check_children_star(chart, tg_classification)
    child_reasons = []

    primary_star = children["primary_star"]
    secondary_star = children["secondary_star"]
    p_strength = children["primary_strength"]
    s_strength = children["secondary_strength"]

    # Estimate children count based on star visibility
    child_count_est = 0
    if chart.gender == "male":
        sons_label, daughters_label = f"7K ({tg_classification.get('7K',{}).get('chinese','七殺')})", f"DO ({tg_classification.get('DO',{}).get('chinese','正官')})"
    else:
        sons_label, daughters_label = f"HO ({tg_classification.get('HO',{}).get('chinese','傷官')})", f"EG ({tg_classification.get('EG',{}).get('chinese','食神')})"

    p_count = tg_classification.get(primary_star, {}).get("total_count", 0)
    s_count = tg_classification.get(secondary_star, {}).get("total_count", 0)

    if p_strength == "PROMINENT":
        child_reasons.append(f"{sons_label} is prominent — likely multiple sons")
        child_count_est += 2
    elif p_strength in ("PRESENT", "HIDDEN_ONLY"):
        child_reasons.append(f"{sons_label} present — sons likely")
        child_count_est += 1
    else:
        child_reasons.append(f"{sons_label} absent — sons less likely naturally")

    if s_strength == "PROMINENT":
        child_reasons.append(f"{daughters_label} is prominent — likely multiple daughters")
        child_count_est += 2
    elif s_strength in ("PRESENT", "HIDDEN_ONLY"):
        child_reasons.append(f"{daughters_label} present — daughters likely")
        child_count_est += 1
    else:
        child_reasons.append(f"{daughters_label} absent — daughters less likely naturally")

    # Hour pillar (children palace) strength
    hour_branch = chart.pillars["hour"].branch
    hour_qi = get_all_branch_qi(hour_branch)
    hour_has_child_star = False
    for hs, score in hour_qi:
        tg = get_ten_god(chart.day_master, hs)
        if tg and tg[0] in (primary_star, secondary_star):
            hour_has_child_star = True
            break
    if hour_has_child_star:
        child_reasons.append("Children star in hour pillar (children palace) — strong fertility indicator")
    else:
        child_reasons.append("No children star in hour pillar — may need more effort")

    est_label = f"{child_count_est}+" if child_count_est > 0 else "uncertain"
    severity = "positive" if child_count_est >= 2 else "info" if child_count_est == 1 else "warning"

    # Top children years
    child_preds = predictions.get("children", [])
    if child_preds:
        top = child_preds[0]
        child_reasons.append(f"Best year: {top.year} (age {top.age})")

    items.append({
        "label": f"Children: est. {est_label}",
        "value": " | ".join(child_reasons),
        "severity": severity,
    })

    # --- WEALTH POTENTIAL ---
    dw_strength = tg_classification.get("DW", {}).get("strength", "ABSENT")
    iw_strength = tg_classification.get("IW", {}).get("strength", "ABSENT")
    eg_strength = tg_classification.get("EG", {}).get("strength", "ABSENT")
    do_strength = tg_classification.get("DO", {}).get("strength", "ABSENT")

    wealth_reasons = []
    dm_element = chart.dm_element
    wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element, "")

    # Wealth star assessment
    has_direct_wealth = dw_strength not in ("ABSENT",)
    has_indirect_wealth = iw_strength not in ("ABSENT",)

    # DM strength vs wealth capacity
    can_handle = strength.verdict not in ("extremely_weak",)
    is_strong_dm = strength.verdict in ("strong", "extremely_strong")

    # Wealth tier estimation
    wealth_score = 0

    if has_direct_wealth:
        wealth_score += 2
        wealth_reasons.append(f"Direct Wealth present — steady income capacity")
    if has_indirect_wealth:
        wealth_score += 2
        wealth_reasons.append(f"Indirect Wealth present — windfall/investment capacity")
    if iw_strength == "PROMINENT":
        wealth_score += 2
        wealth_reasons.append("Prominent Indirect Wealth — strong speculative/business luck")
    if dw_strength == "PROMINENT":
        wealth_score += 1
        wealth_reasons.append("Prominent Direct Wealth — strong salary/stable income")
    if is_strong_dm and (has_direct_wealth or has_indirect_wealth):
        wealth_score += 2
        wealth_reasons.append("Strong DM can hold wealth — good earning capacity")
    elif not can_handle:
        wealth_score -= 2
        wealth_reasons.append("Extremely weak DM — struggles to hold onto wealth")
    if eg_strength == "PROMINENT":
        wealth_score += 1
        wealth_reasons.append("Eating God prominent — wealth through creativity/talent")
    if rw_strength == "PROMINENT":
        wealth_score -= 2
        wealth_reasons.append("Rob Wealth prominent — money drains through competition/others")

    # Wealth flags
    wealth_flags = flags.get("wealth", [])
    for wf in wealth_flags[:2]:
        wealth_reasons.append(f"Warning: {wf.description}")
        wealth_score -= 1

    # Map score to tier
    if wealth_score >= 6:
        wealth_tier = "8-9 figures possible"
        tier_detail = "Strong wealth indicators — 8-figure potential with right timing. 9-figure if Indirect Wealth is prominent + strong DM."
        severity = "positive"
    elif wealth_score >= 4:
        wealth_tier = "7-8 figures possible"
        tier_detail = "Good wealth capacity — 7-figure achievable. 8-figure possible in favorable luck decades."
        severity = "positive"
    elif wealth_score >= 2:
        wealth_tier = "7 figures possible"
        tier_detail = "Moderate wealth indicators — comfortable living, 7-figure achievable with effort."
        severity = "info"
    elif wealth_score >= 0:
        wealth_tier = "6-7 figures"
        tier_detail = "Average wealth capacity — steady income but unlikely to break into high wealth without favorable luck."
        severity = "info"
    else:
        wealth_tier = "Wealth challenged"
        tier_detail = "Wealth stars weak or drained — financial stability requires careful management and favorable timing."
        severity = "warning"

    wealth_reasons.append(tier_detail)

    # Top career years
    career_preds = predictions.get("career", [])
    if career_preds:
        top = career_preds[0]
        wealth_reasons.append(f"Best career year: {top.year} (age {top.age})")

    items.append({
        "label": f"Wealth: {wealth_tier}",
        "value": " | ".join(wealth_reasons),
        "severity": severity,
    })

    return {
        "id": "natal_predictions",
        "title": "Life Predictions",
        "title_zh": "命理預測",
        "text": "Based on natal chart structure — what your birth chart says about marriage, children, and wealth potential",
        "items": items,
    }


def _summary_predictions_timeline(predictions: Dict[str, list]) -> Optional[dict]:
    """Section: year-specific prediction highlights (full/timeline tier only)."""
    items = []
    for event_type, events in predictions.items():
        for ev in events[:2]:
            factors_str = "; ".join(ev.factors[:2]) if ev.factors else ""
            items.append({
                "label": event_type.replace("_", " ").title(),
                "value": f"Year {ev.year} (age {ev.age}) — score {ev.score:.0f}. {factors_str}",
            })
    if not items:
        return None
    return {
        "id": "predictions",
        "title": "Year Predictions",
        "title_zh": "流年預測",
        "items": items[:8],
    }


def _summary_honest(chart: ChartData, strength: StrengthAssessment,
                     tg_classification: Dict[str, dict],
                     flags: Dict[str, List[RedFlag]]) -> dict:
    """Section: comprehensive honest life summary with WHY-reasoning."""
    from .templates import LIFE_LESSON_TEMPLATES, DM_NATURE, HEALTH_ELEMENT_MAP, _pick
    from .ten_gods import check_spouse_star

    dm_element = chart.dm_element
    dm_info = STEMS[chart.day_master]
    dm_key = (dm_info["element"], dm_info["polarity"].capitalize())
    nature = DM_NATURE.get(dm_key, {})

    resource = ELEMENT_CYCLES["generated_by"].get(dm_element, "")
    output = ELEMENT_CYCLES["generating"].get(dm_element, "")
    wealth = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    officer = ELEMENT_CYCLES["controlled_by"].get(dm_element, "")

    # Life lesson
    if strength.is_following_chart:
        key = "following"
    elif strength.verdict in ("weak", "extremely_weak"):
        key = f"weak_{dm_element.lower()}"
    else:
        key = "strong_general"
    templates = LIFE_LESSON_TEMPLATES.get(key, LIFE_LESSON_TEMPLATES.get("strong_general", [""]))
    life_lesson = _pick(templates)

    parts = []

    # Who you are
    parts.append(f"You are {nature.get('name', chart.day_master)} ({nature.get('chinese', dm_info['chinese'])}). "
                 f"Personality: {nature.get('personality', 'unknown')}.")

    # Strength reality (score = element %, 20% = balanced)
    score = strength.score
    if score < 10:
        parts.append(f"Your Day Master is extremely weak ({score:.0f}% element presence, 20% = balanced). "
                     "You are easily overwhelmed by life's demands. "
                     "Your biggest challenge is finding support systems and environments that sustain you.")
    elif score < 16:
        parts.append(f"Your Day Master is weak ({score:.0f}% element presence, 20% = balanced). "
                     "You need more support than most people. "
                     "Resource and companion elements are your lifeline.")
    elif score < 24:
        parts.append(f"Your Day Master is balanced ({score:.0f}% element presence, 20% = balanced). "
                     "You have a flexible chart — small shifts in luck pillars have outsized effects on your life.")
    elif score < 30:
        parts.append(f"Your Day Master is strong ({score:.0f}% element presence, 20% = balanced). "
                     "You have abundant energy but need productive outlets. "
                     "Without channels for your strength, you become restless and domineering.")
    else:
        parts.append(f"Your Day Master is extremely strong ({score:.0f}% element presence, 20% = balanced). "
                     "You have overwhelming energy. The risk is stagnation and bulldozing over others.")

    # Marriage reality — GENDER-AWARE
    spouse = check_spouse_star(chart, tg_classification)
    marriage_flags = flags.get("marriage", [])

    if chart.gender == "female":
        # For females: DO (Direct Officer) = husband star
        do_strength = tg_classification.get("DO", {}).get("strength", "ABSENT")
        if do_strength == "ABSENT":
            parts.append("Marriage: Your husband star (正官 Direct Officer) is ABSENT. "
                         "This is the hardest marriage indicator for a woman — partnership comes very late, "
                         "with great difficulty, or through unconventional paths. "
                         "The right luck decade is critical.")
        elif marriage_flags:
            severe_count = sum(1 for f in marriage_flags if f.severity in ("severe", "critical"))
            if severe_count >= 2:
                parts.append("Marriage: Multiple severe marriage indicators. "
                             "Relationships are a major life challenge requiring active management.")
            elif severe_count == 1:
                parts.append("Marriage: One significant marriage challenge exists. "
                             "Awareness and timing can mitigate it.")
            else:
                parts.append("Marriage: Some marriage challenges flagged, but manageable with awareness.")
        else:
            parts.append("Marriage: No major obstacles in the natal chart. "
                         "Timing and luck pillar alignment will determine when.")
    else:
        # Male path
        if spouse["is_critical_absent"]:
            parts.append(f"Marriage: Your {spouse['label']} is ABSENT. "
                         "This is the single hardest indicator — marriage comes very late, "
                         "with great difficulty, or through unconventional paths. This is not a death sentence, "
                         "but it requires conscious effort and the right luck decade.")
        elif marriage_flags:
            severe_count = sum(1 for f in marriage_flags if f.severity in ("severe", "critical"))
            if severe_count >= 2:
                parts.append("Marriage: Multiple severe marriage indicators. "
                             "Relationships are a major life challenge requiring active management.")
            elif severe_count == 1:
                parts.append("Marriage: One significant marriage challenge exists. "
                             "Awareness and timing can mitigate it.")
            else:
                parts.append("Marriage: Some marriage challenges flagged, but manageable with awareness.")
        else:
            parts.append("Marriage: No major obstacles in the natal chart. "
                         "Timing and luck pillar alignment will determine when.")

    # Wealth reality (keep existing logic)
    dw = tg_classification.get("DW", {}).get("strength", "ABSENT")
    iw = tg_classification.get("IW", {}).get("strength", "ABSENT")
    rw = tg_classification.get("RW", {}).get("strength", "ABSENT")
    if dw == "ABSENT" and iw == "ABSENT":
        parts.append("Wealth: Both wealth stars absent. "
                     "Money doesn't come naturally — must be actively pursued through favorable elements and timing.")
    elif rw == "PROMINENT":
        parts.append("Wealth: Rob Wealth is prominent — money comes but also leaves through others. "
                     "Avoid partnerships and lending. Protect what you earn.")
    elif iw == "PROMINENT":
        parts.append("Wealth: Strong Indirect Wealth — windfall potential through speculation, business, or investments. "
                     "Risk tolerance is high, but so is the upside.")

    # NEW: Health cross-reference
    elem_counts = count_elements(chart)
    total_count = sum(elem_counts.values())
    avg_count = total_count / 5 if total_count > 0 else 1.0
    deficient_elements = [e for e in ["Wood", "Fire", "Earth", "Metal", "Water"]
                          if elem_counts.get(e, 0) < avg_count * 0.5]
    if deficient_elements:
        organs = []
        for e in deficient_elements:
            organ = HEALTH_ELEMENT_MAP.get(e, {}).get("yin_organ", e).split("(")[0].strip()
            organs.append(f"{organ} ({e})")
        parts.append(f"Health: Watch {', '.join(organs)} — these elements are deficient in your chart.")

    # The life lesson
    parts.append(f"Life lesson: {life_lesson}")

    # Useful God with simulation-based reasoning
    ug = strength.useful_god
    ug_pct = strength.element_percentages.get(ug, 0)
    parts.append(
        f"Your useful god is {ug} (currently at {ug_pct}% — most deficient). "
        f"Adding {ug} brings the chart closest to 20% equilibrium across all five elements. "
        f"Favorable: {', '.join(strength.favorable_elements)}. "
        f"Unfavorable: {', '.join(strength.unfavorable_elements)} (already excessive). "
        f"Everything in your life improves when you increase {ug} element exposure."
    )

    return {
        "id": "summary",
        "title": "Honest Summary",
        "title_zh": "總結",
        "text": " ".join(parts),
    }


def _diff_ten_gods_arriving(tg_entries: List[TenGodEntry],
                             tg_classification: Dict[str, dict],
                             chart: ChartData) -> Optional[dict]:
    """Section: ten gods arriving via LP/time-period (diff from natal)."""
    from .templates import TEN_GOD_INTERPRETATIONS, _pick
    natal_positions = {"year", "month", "day", "hour"}
    # Find ten gods in LP/time-period pillars
    arriving = {}  # abbr -> list of (position, visible)
    for entry in tg_entries:
        if entry.position in natal_positions:
            continue
        if entry.abbreviation == "DM":
            continue
        arriving.setdefault(entry.abbreviation, []).append(
            (entry.position, entry.visible))

    if not arriving:
        return None

    items = []
    for abbr, appearances in arriving.items():
        natal_strength = tg_classification.get(abbr, {}).get("strength", "ABSENT")
        info = TEN_GOD_INFO.get(abbr, {})
        english = info.get("english", abbr)
        chinese = info.get("chinese", "")
        # Life meaning for this person's gender
        life_meaning = TEN_GOD_LIFE_MEANING.get(chart.gender, {}).get(abbr, "")

        # Visible arrivals are more significant
        visible_arrivals = [pos for pos, vis in appearances if vis]
        hidden_arrivals = [pos for pos, vis in appearances if not vis]
        pos_labels = visible_arrivals + [f"({p} hidden)" for p in hidden_arrivals]
        sources = ", ".join(pos_labels)

        if natal_strength == "ABSENT":
            label_prefix = "NEW"
            severity = "warning"
            templates = TEN_GOD_INTERPRETATIONS.get(abbr, {})
            meaning = _pick(templates.get("PRESENT", [f"{english} arrives"]))
        elif natal_strength in ("HIDDEN_ONLY", "WEAK"):
            label_prefix = "BOOSTED"
            severity = "info"
            meaning = f"{english} was weak natally, now reinforced"
        elif natal_strength == "PROMINENT":
            label_prefix = "AMPLIFIED"
            severity = "warning" if abbr in ("7K", "HO", "RW") else "info"
            meaning = f"{english} already dominant — further amplified"
        else:
            label_prefix = "REINFORCED"
            severity = "info"
            meaning = f"{english} gains additional support"

        if life_meaning:
            meaning += f" ({life_meaning})"

        items.append({
            "label": f"{label_prefix}: {abbr} ({chinese})",
            "value": f"via {sources} — {meaning}",
            "severity": severity,
        })

    return {
        "id": "ten_gods_diff",
        "title": "Ten Gods Arriving",
        "title_zh": "十神變化",
        "text": f"{len(arriving)} ten god(s) enter from luck/time pillars",
        "items": items,
    }


def _diff_interactions(interactions: List[BranchInteraction]) -> Optional[dict]:
    """Section: NEW interactions activated by LP/time-period (not natal-only)."""
    positive_types = {"harmony", "three_harmony", "half_three_harmony", "directional_combo"}
    new_interactions = [i for i in interactions if i.activated_by_lp]
    if not new_interactions:
        return None

    pos_count = sum(1 for i in new_interactions if i.interaction_type in positive_types)
    neg_count = len(new_interactions) - pos_count

    items = []
    for inter in new_interactions[:8]:
        polarity = "positive" if inter.interaction_type in positive_types else "negative"
        severity = "positive" if polarity == "positive" else inter.severity
        palaces_str = " vs ".join(inter.palaces) if inter.palaces else ""
        items.append({
            "label": f"{inter.chinese_name} {inter.interaction_type.replace('_', ' ').title()}",
            "value": f"{palaces_str} — {inter.description}" if palaces_str else inter.description,
            "severity": severity,
        })
    return {
        "id": "interactions_diff",
        "title": "New Interactions",
        "title_zh": "新增地支關係",
        "text": f"{pos_count} positive, {neg_count} negative NEW interactions from luck/time pillars",
        "items": items,
    }


def _diff_shen_sha(shen_sha: List[ShenShaResult]) -> Optional[dict]:
    """Section: shen sha activated by LP/time-period."""
    from .templates import SHEN_SHA_IMPACTS, _pick
    new_stars = [s for s in shen_sha if s.present and s.activated_by is not None]
    if not new_stars:
        return None

    items = []
    for s in new_stars:
        templates = SHEN_SHA_IMPACTS.get(s.name_chinese, {})
        text = _pick(templates.get("present", [f"{s.name_english} activated"]))
        severity = "positive" if s.nature == "auspicious" else "negative" if s.nature == "inauspicious" else "info"
        items.append({
            "label": f"{s.name_chinese} {s.name_english}",
            "value": f"via {s.activated_by} — {text}",
            "severity": severity,
        })
    return {
        "id": "shen_sha_diff",
        "title": "Stars Activated",
        "title_zh": "新增神煞",
        "text": f"{len(new_stars)} star(s) activated by luck/time pillars",
        "items": items,
    }


def _diff_element_shift(chart: ChartData) -> Optional[dict]:
    """Section: how element balance shifted from natal to full."""
    natal_counts = count_elements(chart)
    full_counts = count_all_elements(chart)

    # Check if there's any actual difference
    if natal_counts == full_counts:
        return None

    natal_total = sum(natal_counts.values())
    full_total = sum(full_counts.values())

    ELEMENT_CHINESE = {"Wood": "木", "Fire": "火", "Earth": "土", "Metal": "金", "Water": "水"}
    items = []
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        natal_pct = (natal_counts[elem] / natal_total * 100) if natal_total > 0 else 0
        full_pct = (full_counts[elem] / full_total * 100) if full_total > 0 else 0
        change = full_pct - natal_pct
        if abs(change) < 1.0:
            continue
        arrow = "+" if change > 0 else ""
        severity = "positive" if change > 3 else "negative" if change < -3 else "info"
        items.append({
            "label": f"{ELEMENT_CHINESE[elem]} {elem}",
            "value": f"{natal_pct:.0f}% -> {full_pct:.0f}% ({arrow}{change:.0f}%)",
            "severity": severity,
        })

    if not items:
        return None

    return {
        "id": "element_shift",
        "title": "Element Balance Shift",
        "title_zh": "五行變化",
        "text": "How luck/time pillars shift your element balance",
        "items": items,
    }


def build_client_summary(chart: ChartData, results: dict,
                          flags: Dict[str, List[RedFlag]]) -> dict:
    """Build structured client summary for non-technical frontend display.
    Natal tier: static analysis of birth chart.
    Full tier: diff-focused — what changed from natal due to LP/time pillars.
    """
    strength = results["strength"]
    tg_entries = results["ten_god_entries"]
    tg_classification = results["ten_god_classification"]
    interactions = results["interactions"]
    shen_sha = results["shen_sha"]
    predictions = results["predictions"]

    has_luck = chart.luck_pillar is not None
    has_time_period = len(chart.time_period_pillars) > 0
    is_full = has_luck or has_time_period
    tier = "full" if is_full else "natal"

    if not is_full:
        # NATAL tier: static analysis of birth chart
        sections = [
            _summary_chart_overview(chart),
            _summary_strength(strength, chart),
            _summary_ten_gods(chart, tg_classification),
            _summary_interactions(interactions),
            _summary_shen_sha(shen_sha),
            _summary_red_flags(flags),
            _summary_natal_predictions(chart, tg_classification, strength, predictions, flags),
            _summary_health(chart, strength),
            _summary_remedies(strength, chart),
            _summary_honest(chart, strength, tg_classification, flags),
        ]
    else:
        # FULL tier: diff-focused — what changed from natal
        sections = []

        # Luck pillar context
        lp_section = _summary_luck_pillar(chart, strength)
        if lp_section:
            sections.append(lp_section)

        # Element balance shift
        elem_diff = _diff_element_shift(chart)
        if elem_diff:
            sections.append(elem_diff)

        # Ten gods arriving
        tg_diff = _diff_ten_gods_arriving(tg_entries, tg_classification, chart)
        if tg_diff:
            sections.append(tg_diff)

        # New interactions from LP/time pillars
        inter_diff = _diff_interactions(interactions)
        if inter_diff:
            sections.append(inter_diff)

        # Stars activated by LP/time pillars
        sha_diff = _diff_shen_sha(shen_sha)
        if sha_diff:
            sections.append(sha_diff)

        # Red flags still relevant
        rf = _summary_red_flags(flags)
        if rf.get("items"):
            sections.append(rf)

        # Year predictions — only for year-level analysis
        is_year_only = "monthly" not in chart.time_period_pillars and "daily" not in chart.time_period_pillars
        if is_year_only:
            pred_section = _summary_predictions_timeline(predictions)
            if pred_section:
                sections.append(pred_section)

        # Remedies always useful
        sections.append(_summary_remedies(strength, chart))

    return {
        "tier": tier,
        "sections": sections,
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

    # 4. Build element scores (interaction-adjusted to match DM strength %)
    base_score, natal_score, post_score = build_element_scores(chart, interactions)

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

    # Wealth storage (財庫)
    response["wealth_storage_analysis"] = _compute_wealth_storage(chart)

    # Unit tracker (stub)
    response["unit_tracker"] = None

    # Mappings
    response["mappings"] = build_mappings()

    # Comprehensive report (new field)
    response["comprehensive_report"] = comprehensive_report

    # Qi Phase contextual analysis (十二长生深度分析) + Spiritual Sensitivity (灵性敏感度)
    try:
        qi_phase_result = analyze_qi_phases(chart, shen_sha)
        response["qi_phase_analysis"] = qi_phase_result

        spiritual_bonus = qi_phase_result.get("spiritual_bonus", 0)
        response["spiritual_sensitivity"] = assess_spiritual_sensitivity(
            chart, shen_sha, qi_phase_spiritual_bonus=spiritual_bonus
        )
    except Exception:
        response["qi_phase_analysis"] = None
        response["spiritual_sensitivity"] = None

    # Client summary (structured JSON for frontend)
    response["client_summary"] = build_client_summary(chart, results, flags)

    return response
