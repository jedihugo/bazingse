# =============================================================================
# COMPREHENSIVE REPORT GENERATOR
# =============================================================================
# Assembles all analysis sections into a complete markdown report.
# Pure Python, zero LLM dependency, fully deterministic.
# =============================================================================

import random
from typing import List, Dict, Optional, Tuple
from ..core import STEMS, BRANCHES
from ..derived import ELEMENT_CYCLES, get_ten_god, get_all_branch_qi, ELEMENT_CHINESE
from .models import (
    ChartData, Pillar, ShenShaResult, BranchInteraction,
    StrengthAssessment, RedFlag, EventPrediction, LuckPillarInfo,
    EnvironmentAssessment, TenGodEntry,
)
from .ten_gods import (
    map_all_ten_gods, classify_ten_god_strength, check_spouse_star,
    check_children_star, analyze_ten_god_patterns, TEN_GOD_INFO,
    get_ten_god_element_counts,
)
from .strength import assess_day_master_strength, count_elements
from .interactions import detect_all_interactions, get_negative_interactions
from .shen_sha import run_all_shen_sha, get_void_branches
from .predictions import run_all_predictions, get_annual_pillar
from .environment import assess_environment
from .templates import (
    DM_NATURE, STRENGTH_VERDICTS, TEN_GOD_INTERPRETATIONS,
    SHEN_SHA_IMPACTS, INTERACTION_IMPACTS, SEVERITY_LANGUAGE,
    HEALTH_ELEMENT_MAP, ELEMENT_REMEDIES, LIFE_LESSON_TEMPLATES, _pick,
)


# =============================================================================
# SECTION 1: CHART SETUP
# =============================================================================

def section_chart_setup(chart: ChartData, tg_entries: List[TenGodEntry]) -> str:
    lines = []
    lines.append("## SECTION 1: CHART SETUP\n")

    # Four Pillars table
    lines.append("### Four Pillars (四柱)\n")
    lines.append("| | Year (年柱) | Month (月柱) | Day (日柱) | Hour (时柱) |")
    lines.append("|---|---|---|---|---|")

    # Palace
    lines.append(f"| **Palace** | Parents/Ancestry | Career/Social | Self/Spouse | Children/Legacy |")

    # Heavenly Stems
    stems = []
    for pos in ["year", "month", "day", "hour"]:
        p = chart.pillars[pos]
        s = STEMS[p.stem]
        stems.append(f"{s['chinese']} ({p.stem}) {s['element']}")
    lines.append(f"| **Heavenly Stem** | {' | '.join(stems)} |")

    # Earthly Branches
    branches = []
    for pos in ["year", "month", "day", "hour"]:
        p = chart.pillars[pos]
        b = BRANCHES[p.branch]
        branches.append(f"{b['chinese']} ({p.branch}) {b['element']}")
    lines.append(f"| **Earthly Branch** | {' | '.join(branches)} |")

    # Hidden Stems
    hidden = []
    for pos in ["year", "month", "day", "hour"]:
        p = chart.pillars[pos]
        qi = get_all_branch_qi(p.branch)
        hs_str = ", ".join(f"{STEMS[s]['chinese']}({score})" for s, score in qi)
        hidden.append(hs_str)
    lines.append(f"| **Hidden Stems** | {' | '.join(hidden)} |")

    lines.append("")

    # Day Master info
    dm = chart.day_master
    dm_info = STEMS[dm]
    nature_key = (dm_info["element"], dm_info["polarity"])
    nature = DM_NATURE.get(nature_key, {})

    lines.append("### Day Master (日主)\n")
    lines.append(f"**{dm_info['chinese']} ({dm}) — {dm_info['element']} {dm_info['polarity']}**\n")
    if nature:
        nature_texts = nature.get("nature", [])
        lines.append(f"*{_pick(nature_texts)}*\n")
        lines.append(f"Personality: {nature.get('personality', '')}\n")

    # Ten Gods reference table
    lines.append("### Ten Gods Map (十神)\n")
    lines.append("| Location | Stem | Ten God | Chinese |")
    lines.append("|---|---|---|---|")
    for entry in tg_entries:
        if entry.position != "luck_pillar":
            vis = "" if entry.visible else " (hidden)"
            lines.append(f"| {entry.location}{vis} | {STEMS[entry.stem]['chinese']} ({entry.stem}) "
                        f"| {entry.english} ({entry.abbreviation}) | {entry.chinese} |")

    # Luck pillar info if present
    if chart.luck_pillar:
        lp = chart.luck_pillar
        lines.append(f"\n### Current Luck Pillar (大运)\n")
        lines.append(f"**{STEMS[lp.stem]['chinese']}{BRANCHES[lp.branch]['chinese']} "
                     f"({lp.stem} {lp.branch})**\n")

    return "\n".join(lines)


# =============================================================================
# SECTION 2: DM STRENGTH
# =============================================================================

def section_strength(chart: ChartData, strength: StrengthAssessment) -> str:
    lines = []
    lines.append("## SECTION 2: DAY MASTER STRENGTH ASSESSMENT\n")

    lines.append(f"**Score: {strength.score}/100** (50 = perfectly balanced)\n")
    lines.append(f"- Support count: {strength.support_count}")
    lines.append(f"- Drain count: {strength.drain_count}")
    lines.append(f"- Seasonal state: {strength.seasonal_state}")
    lines.append(f"- Verdict: **{strength.verdict.upper().replace('_', ' ')}**\n")

    # Verdict interpretation
    verdict_text = _pick(STRENGTH_VERDICTS.get(strength.verdict, [""]))
    lines.append(f"*{verdict_text}*\n")

    # Following chart
    if strength.is_following_chart:
        lines.append(f"**FOLLOWING CHART (从格) DETECTED** — Type: {strength.following_type}")
        lines.append("This chart is so weak that it 'follows' the dominant force instead of fighting it.\n")

    # Useful God
    lines.append(f"### Useful God (用神): **{strength.useful_god}** ({ELEMENT_CHINESE.get(strength.useful_god, '')})\n")
    fav_strs = [f"{e} ({ELEMENT_CHINESE.get(e, '')})" for e in strength.favorable_elements]
    unfav_strs = [f"{e} ({ELEMENT_CHINESE.get(e, '')})" for e in strength.unfavorable_elements]
    lines.append(f"- Favorable elements: {', '.join(fav_strs)}")
    lines.append(f"- Unfavorable elements: {', '.join(unfav_strs)}")

    return "\n".join(lines)


# =============================================================================
# SECTION 3: TEN GODS DEEP ANALYSIS
# =============================================================================

def section_ten_gods(chart: ChartData, classification: Dict[str, dict],
                     tg_entries: List[TenGodEntry]) -> str:
    lines = []
    lines.append("## SECTION 3: TEN GODS DEEP ANALYSIS (十神)\n")

    # Classification table
    lines.append("| Ten God | Chinese | Strength | Visible | Hidden | Locations |")
    lines.append("|---|---|---|---|---|---|")
    for abbr in ["F", "RW", "EG", "HO", "IW", "DW", "7K", "DO", "IR", "DR"]:
        info = classification[abbr]
        lines.append(f"| {info['english']} ({abbr}) | {info['chinese']} | "
                    f"**{info['strength']}** | {info['visible_count']} | "
                    f"{info['hidden_count']} | {', '.join(info['locations'])} |")

    lines.append("")

    # Detailed interpretation for each
    for abbr in ["F", "RW", "EG", "HO", "IW", "DW", "7K", "DO", "IR", "DR"]:
        info = classification[abbr]
        strength = info["strength"]
        templates = TEN_GOD_INTERPRETATIONS.get(abbr, {})

        if strength == "PROMINENT" and "PROMINENT" in templates:
            lines.append(f"**{info['english']} ({info['chinese']})**: {_pick(templates['PROMINENT'])}\n")
        elif strength in ("PRESENT", "HIDDEN_ONLY") and "PRESENT" in templates:
            lines.append(f"**{info['english']} ({info['chinese']})**: {_pick(templates['PRESENT'])}\n")
        elif strength == "ABSENT" and "ABSENT" in templates:
            lines.append(f"**{info['english']} ({info['chinese']})**: {_pick(templates['ABSENT'])}\n")

    # Spouse star check
    spouse = check_spouse_star(chart, classification)
    lines.append(f"### Spouse Star: {spouse['label']}\n")
    if spouse["is_critical_absent"]:
        lines.append(f"**WARNING: {spouse['label']} is ABSENT.** "
                    f"This is a critical indicator for marriage difficulty.\n")
    else:
        lines.append(f"Status: {spouse['strength']}. Locations: {', '.join(spouse['locations'])}\n")

    # Children star check
    children = check_children_star(chart, classification)
    lines.append(f"### Children Stars: {children['primary_star']} / {children['secondary_star']}\n")
    if not children["any_present"]:
        lines.append(f"**Both children stars are ABSENT.** Children may come late or with difficulty.\n")

    # Patterns
    patterns = analyze_ten_god_patterns(chart, classification)
    if patterns:
        lines.append("### Notable Patterns\n")
        for p in patterns:
            lines.append(f"- **{p['pattern']}**: {p['description']}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# SECTION 4: BRANCH INTERACTIONS
# =============================================================================

def section_interactions(chart: ChartData, interactions: List[BranchInteraction]) -> str:
    lines = []
    lines.append("## SECTION 4: BRANCH INTERACTIONS (地支关系)\n")

    if not interactions:
        lines.append("No significant branch interactions detected.\n")
        return "\n".join(lines)

    # Group by type
    by_type: Dict[str, List[BranchInteraction]] = {}
    for inter in interactions:
        by_type.setdefault(inter.interaction_type, []).append(inter)

    type_order = ["clash", "harmony", "three_harmony", "half_three_harmony",
                  "directional_combo", "punishment", "self_punishment", "harm", "destruction"]

    type_labels = {
        "clash": "Six Clashes (六冲)",
        "harmony": "Six Harmonies (六合)",
        "three_harmony": "Three Harmony Frames (三合局)",
        "half_three_harmony": "Half Three Harmony (半三合)",
        "directional_combo": "Directional Combinations (三会局)",
        "punishment": "Punishments (三刑)",
        "self_punishment": "Self-Punishments (自刑)",
        "harm": "Six Harms (六害)",
        "destruction": "Destructions (破)",
    }

    for itype in type_order:
        if itype not in by_type:
            continue
        items = by_type[itype]
        lines.append(f"### {type_labels.get(itype, itype)}\n")
        for item in items:
            lp_tag = " **[ACTIVATED BY LUCK PILLAR]**" if item.activated_by_lp else ""
            lines.append(f"- **{item.description}**{lp_tag}")
            lines.append(f"  - Palaces: {', '.join(item.palaces)}")
            lines.append(f"  - Severity: {item.severity}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# SECTION 5: SHEN SHA AUDIT
# =============================================================================

def section_shen_sha(chart: ChartData, shen_sha: List[ShenShaResult]) -> str:
    lines = []
    lines.append("## SECTION 5: SHEN SHA FULL AUDIT (神煞)\n")

    # Summary table of present stars
    present = [s for s in shen_sha if s.present]
    absent = [s for s in shen_sha if not s.present]

    lines.append("### Present Stars\n")
    if present:
        lines.append("| Star | Chinese | Location | Palace | Nature | Severity | Void? |")
        lines.append("|---|---|---|---|---|---|---|")
        for s in present:
            void_tag = "VOID" if s.is_void else ""
            palace = s.palace or ""
            activated = f" (via {s.activated_by})" if s.activated_by else ""
            lines.append(f"| {s.name_english} | {s.name_chinese} | {s.location or ''} "
                        f"| {palace}{activated} | {s.nature} | {s.severity} | {void_tag} |")
    else:
        lines.append("No stars detected.\n")

    lines.append("")

    # Derivation details
    lines.append("### Derivation Details\n")
    for s in present:
        lines.append(f"- **{s.name_chinese} ({s.name_english})**: {s.derivation}")

        # Impact template
        impacts = SHEN_SHA_IMPACTS.get(s.name_chinese, {})
        if "present" in impacts:
            lines.append(f"  - *{_pick(impacts['present'])}*")

        if s.is_void:
            lines.append(f"  - **NOTE: This star sits on a VOID branch. "
                        f"Its effect is weakened or unreliable.**")
    lines.append("")

    # Notable absences
    critical_absent = {"天乙贵人", "禄神", "天医", "天德贵人", "文昌贵人", "将星", "红鸾"}
    notable_absent = [s for s in absent if s.name_chinese in critical_absent]
    if notable_absent:
        lines.append("### Notable Absences\n")
        for s in notable_absent:
            impacts = SHEN_SHA_IMPACTS.get(s.name_chinese, {})
            if "absent" in impacts:
                lines.append(f"- **{s.name_chinese} ({s.name_english})**: {_pick(impacts['absent'])}")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# SECTION 6: RED FLAGS
# =============================================================================

def section_red_flags(chart: ChartData, strength: StrengthAssessment,
                      classification: Dict[str, dict],
                      interactions: List[BranchInteraction],
                      shen_sha: List[ShenShaResult]) -> str:
    lines = []
    lines.append("## SECTION 6: RED FLAGS — DIRECT AND UNFILTERED\n")

    # Collect all red flags by life area
    flags: Dict[str, List[RedFlag]] = {
        "wealth": [], "marriage": [], "career": [], "health": [], "character": [],
    }

    # From Ten Gods
    patterns = analyze_ten_god_patterns(chart, classification)
    for p in patterns:
        for area in p["life_areas"]:
            if area in ("wealth", "relationship"):
                target = "marriage" if area == "relationship" else area
            elif area in flags:
                target = area
            else:
                target = "character"
            flags[target].append(RedFlag(
                life_area=target,
                indicator_type="ten_god",
                indicator_name=p["pattern"],
                description=p["description"],
                severity=p["severity"],
            ))

    # Spouse star absent
    spouse = check_spouse_star(chart, classification)
    if spouse["is_critical_absent"]:
        flags["marriage"].append(RedFlag(
            life_area="marriage",
            indicator_type="ten_god",
            indicator_name=f"{spouse['star']} absent",
            description=f"{spouse['label']} is completely ABSENT from the natal chart.",
            severity="severe",
        ))

    # From branch interactions (negative ones)
    for inter in interactions:
        if inter.interaction_type in ("clash", "punishment", "self_punishment", "harm"):
            for palace in inter.palaces:
                if "Spouse" in palace:
                    flags["marriage"].append(RedFlag(
                        life_area="marriage",
                        indicator_type="branch_interaction",
                        indicator_name=inter.chinese_name,
                        description=inter.description,
                        severity=inter.severity,
                    ))
                elif "Career" in palace:
                    flags["career"].append(RedFlag(
                        life_area="career",
                        indicator_type="branch_interaction",
                        indicator_name=inter.chinese_name,
                        description=inter.description,
                        severity=inter.severity,
                    ))
                elif "Children" in palace:
                    flags["marriage"].append(RedFlag(
                        life_area="marriage",
                        indicator_type="branch_interaction",
                        indicator_name=inter.chinese_name,
                        description=inter.description,
                        severity=inter.severity,
                    ))
                elif "Parents" in palace:
                    flags["character"].append(RedFlag(
                        life_area="character",
                        indicator_type="branch_interaction",
                        indicator_name=inter.chinese_name,
                        description=inter.description,
                        severity=inter.severity,
                    ))

    # From Shen Sha
    present_shen_sha = [s for s in shen_sha if s.present and s.nature == "inauspicious"]
    for s in present_shen_sha:
        for area in s.life_areas:
            if area in ("relationship",):
                target = "marriage"
            elif area in flags:
                target = area
            else:
                target = "character"
            flags[target].append(RedFlag(
                life_area=target,
                indicator_type="shen_sha",
                indicator_name=s.name_chinese,
                description=f"{s.name_english} ({s.name_chinese}) in {s.palace or 'chart'}",
                severity=s.severity,
            ))

    # Output by life area
    severity_order = {"critical": 0, "severe": 1, "moderate": 2, "mild": 3}

    for area, label in [("marriage", "Marriage & Relationships"),
                        ("wealth", "Wealth & Finances"),
                        ("career", "Career & Authority"),
                        ("health", "Health"),
                        ("character", "Character & Behavior")]:
        area_flags = flags.get(area, [])
        if not area_flags:
            lines.append(f"### {label}\n")
            lines.append("No significant red flags in this area.\n")
            continue

        area_flags.sort(key=lambda f: severity_order.get(f.severity, 3))
        lines.append(f"### {label} ({len(area_flags)} indicators)\n")

        for f in area_flags:
            sev = _pick(SEVERITY_LANGUAGE.get(f.severity, [f.severity]))
            lines.append(f"- **[{f.severity.upper()}] {f.indicator_name}** ({f.indicator_type}): "
                        f"{f.description}")
        lines.append(f"\n*{len(area_flags)} separate indicators affect {label.lower()}.* "
                    f"{sev}\n")

    return "\n".join(lines)


# =============================================================================
# SECTION 7: CURRENT LUCK PILLAR
# =============================================================================

def section_luck_pillar(chart: ChartData, strength: StrengthAssessment) -> str:
    lines = []
    lines.append("## SECTION 7: CURRENT LUCK PILLAR ANALYSIS (大运)\n")

    if not chart.luck_pillar:
        lines.append("No luck pillar provided.\n")
        return "\n".join(lines)

    lp = chart.luck_pillar
    dm = chart.day_master

    # LP stem ten god
    tg = get_ten_god(dm, lp.stem)
    tg_str = f"{tg[1]} ({tg[0]} / {tg[2]})" if tg else "Unknown"

    lines.append(f"**Luck Pillar: {STEMS[lp.stem]['chinese']}{BRANCHES[lp.branch]['chinese']} "
                f"({lp.stem} {lp.branch})**\n")
    lines.append(f"- Stem Ten God: {tg_str}")
    lines.append(f"- Stem Element: {STEMS[lp.stem]['element']}")
    lines.append(f"- Branch Element: {BRANCHES[lp.branch]['element']}")

    # Hidden stems in LP branch
    lp_qi = get_all_branch_qi(lp.branch)
    lp_qi_strs = [f"{STEMS[s]['chinese']}({sc})" for s, sc in lp_qi]
    lines.append(f"- Branch Hidden Stems: {', '.join(lp_qi_strs)}")

    # Is LP element favorable?
    lp_stem_elem = STEMS[lp.stem]["element"]
    lp_branch_elem = BRANCHES[lp.branch]["element"]
    fav = strength.favorable_elements
    unfav = strength.unfavorable_elements

    stem_verdict = "FAVORABLE" if lp_stem_elem in fav else ("UNFAVORABLE" if lp_stem_elem in unfav else "NEUTRAL")
    branch_verdict = "FAVORABLE" if lp_branch_elem in fav else ("UNFAVORABLE" if lp_branch_elem in unfav else "NEUTRAL")

    lines.append(f"\n- LP Stem ({lp_stem_elem}): **{stem_verdict}**")
    lines.append(f"- LP Branch ({lp_branch_elem}): **{branch_verdict}**\n")

    # Current year analysis
    from datetime import datetime
    current_year = datetime.now().year
    annual_stem, annual_branch = get_annual_pillar(current_year)
    annual_tg = get_ten_god(dm, annual_stem)
    annual_tg_str = f"{annual_tg[1]} ({annual_tg[0]} / {annual_tg[2]})" if annual_tg else "Unknown"

    lines.append(f"### Current Year {current_year}: "
                f"{STEMS[annual_stem]['chinese']}{BRANCHES[annual_branch]['chinese']} "
                f"({annual_stem} {annual_branch})\n")
    lines.append(f"- Annual Stem Ten God: {annual_tg_str}")

    annual_stem_elem = STEMS[annual_stem]["element"]
    annual_verdict = "FAVORABLE" if annual_stem_elem in fav else ("UNFAVORABLE" if annual_stem_elem in unfav else "NEUTRAL")
    lines.append(f"- Annual Element ({annual_stem_elem}): **{annual_verdict}**\n")

    return "\n".join(lines)


# =============================================================================
# SECTION 8: HEALTH ANALYSIS
# =============================================================================

def section_health(chart: ChartData, strength: StrengthAssessment,
                   shen_sha: List[ShenShaResult]) -> str:
    lines = []
    lines.append("## SECTION 8: HEALTH ANALYSIS (健康)\n")

    elem_counts = count_elements(chart)

    # Element balance table
    lines.append("### Element Balance\n")
    lines.append("| Element | Count | Status | Organs at Risk |")
    lines.append("|---|---|---|---|")

    avg = sum(elem_counts.values()) / 5
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        health = HEALTH_ELEMENT_MAP[elem]
        if count > avg * 1.5:
            status = "EXCESS"
            risk = health["excess"]
        elif count < avg * 0.5:
            status = "DEFICIENT"
            risk = health["deficiency"]
        else:
            status = "Balanced"
            risk = "—"
        lines.append(f"| {elem} ({ELEMENT_CHINESE[elem]}) | {count:.1f} | {status} "
                    f"| {risk} |")

    lines.append("")

    # TCM mapping
    lines.append("### Organ Systems at Risk\n")
    for elem in ["Wood", "Fire", "Earth", "Metal", "Water"]:
        count = elem_counts.get(elem, 0)
        health = HEALTH_ELEMENT_MAP[elem]
        if count > avg * 1.5:
            lines.append(f"- **{elem} EXCESS**: {health['yin_organ']} and {health['yang_organ']} overloaded. "
                        f"Watch for: {health['excess']}. Body parts affected: {health['body_parts']}.")
        elif count < avg * 0.5:
            lines.append(f"- **{elem} DEFICIENT**: {health['yin_organ']} and {health['yang_organ']} weakened. "
                        f"Watch for: {health['deficiency']}. Body parts affected: {health['body_parts']}.")

    # Health-related Shen Sha
    health_stars = [s for s in shen_sha if s.present and "health" in s.life_areas]
    if health_stars:
        lines.append("\n### Health-Related Stars\n")
        for s in health_stars:
            lines.append(f"- **{s.name_chinese} ({s.name_english})**: "
                        f"{SHEN_SHA_IMPACTS.get(s.name_chinese, {}).get('present', [''])[0] if SHEN_SHA_IMPACTS.get(s.name_chinese, {}).get('present') else s.derivation}")

    lines.append("")
    return "\n".join(lines)


# =============================================================================
# SECTION 9: REMEDIES
# =============================================================================

def section_remedies(chart: ChartData, strength: StrengthAssessment,
                     env: EnvironmentAssessment) -> str:
    lines = []
    lines.append("## SECTION 9: REMEDIES & WHAT MUST CHANGE\n")

    useful = strength.useful_god
    remedies = ELEMENT_REMEDIES.get(useful, {})

    # 9a Elemental
    lines.append("### 9a. Elemental Remedies\n")
    lines.append(f"**Useful God Element: {useful} ({ELEMENT_CHINESE.get(useful, '')})**\n")
    lines.append(f"- **Colors to wear**: {', '.join(remedies.get('colors', []))}")
    lines.append(f"- **Colors to avoid**: {', '.join(remedies.get('avoid_colors', []))}")
    lines.append(f"- **Favorable directions**: {', '.join(env.favorable_directions)}")
    lines.append(f"- **Industries**: {', '.join(remedies.get('industries', []))}")
    lines.append(f"- **Environment**: {', '.join(remedies.get('environment', []))}\n")

    # 9b Behavioral
    lines.append("### 9b. Behavioral Changes\n")
    dm_element = chart.dm_element
    if strength.verdict in ("weak", "extremely_weak"):
        lines.append("- Build support systems. You cannot do everything alone.")
        lines.append("- Avoid overcommitting. Your energy is limited — protect it.")
        lines.append("- Seek mentors and allies actively. They are your lifeline.")
    elif strength.verdict in ("strong", "extremely_strong"):
        lines.append("- Channel excess energy into productive output (creative work, exercise).")
        lines.append("- Practice patience and listening. Your strength can bulldoze others.")
        lines.append("- Give more than you take. Generosity balances your chart.")
    lines.append("")

    # 9c Relationship
    lines.append("### 9c. Relationship Guidance\n")
    spouse_element = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    lines.append(f"- Best partner element alignment: {spouse_element} "
                f"({ELEMENT_CHINESE.get(spouse_element, '')})")
    lines.append(f"- Your spouse palace (Day Branch): "
                f"{BRANCHES[chart.pillars['day'].branch]['chinese']} "
                f"({chart.pillars['day'].branch})\n")

    # 9d Financial
    lines.append("### 9d. Financial Strategy\n")
    wealth_element = ELEMENT_CYCLES["controlling"].get(dm_element, "")
    if strength.verdict in ("weak", "extremely_weak"):
        lines.append(f"- Wealth element ({wealth_element}) is too heavy for a weak DM. "
                    "Focus on stable, low-risk income streams.")
        lines.append("- Avoid partnerships where you contribute capital. You'll lose it.")
    else:
        lines.append(f"- Wealth element ({wealth_element}) can be handled. "
                    "Take calculated risks in favorable years.")
    lines.append("")

    # 9f Environmental
    lines.append("### 9e. Relocation & Environment\n")
    lines.append(f"- Crossing Water benefit: **{env.guo_jiang_long_verdict.upper()}** "
                f"(score: {env.guo_jiang_long_score}/5)")
    for factor in env.guo_jiang_long_factors:
        lines.append(f"  - {factor}")
    lines.append(f"- Ideal climate: {env.ideal_climate}")
    lines.append(f"- Ideal geography: {env.ideal_geography}")
    if env.crosses_water_benefit:
        lines.append(f"\n**{env.crosses_water_reason}**")
    lines.append("")

    return "\n".join(lines)


# =============================================================================
# SECTION 10: EVENT PREDICTIONS
# =============================================================================

def section_predictions(chart: ChartData, predictions: Dict[str, List[EventPrediction]]) -> str:
    lines = []
    lines.append("## SECTION 10: LIFE EVENT PREDICTIONS\n")

    for event_type, label in [("marriage", "Marriage Timing"),
                               ("divorce", "Divorce/Separation Risk"),
                               ("children", "Children Arrival"),
                               ("career", "Career Peaks")]:
        events = predictions.get(event_type, [])
        lines.append(f"### {label}\n")
        if not events:
            lines.append("No high-probability years detected.\n")
            continue

        lines.append("| Year | Age | Score | Key Factors |")
        lines.append("|---|---|---|---|")
        for e in events[:5]:
            factors_str = "; ".join(e.factors[:3])
            lines.append(f"| {e.year} | {e.age} | {e.score} | {factors_str} |")
        lines.append("")

    return "\n".join(lines)


# =============================================================================
# SECTION 11: HONEST SUMMARY
# =============================================================================

def section_summary(chart: ChartData, strength: StrengthAssessment,
                    classification: Dict[str, dict]) -> str:
    lines = []
    lines.append("## SECTION 11: HONEST SUMMARY\n")

    dm_element = chart.dm_element
    verdict = strength.verdict

    # Life lesson
    if strength.is_following_chart:
        lesson = _pick(LIFE_LESSON_TEMPLATES.get("following", [""]))
    elif verdict in ("weak", "extremely_weak"):
        key = f"weak_{dm_element.lower()}"
        lesson = _pick(LIFE_LESSON_TEMPLATES.get(key, LIFE_LESSON_TEMPLATES.get("weak_water", [""])))
    else:
        lesson = _pick(LIFE_LESSON_TEMPLATES.get("strong_general", [""]))

    lines.append(f"### Core Life Lesson\n")
    lines.append(f"*{lesson}*\n")

    # What designed for vs fighting
    nature_key = (dm_element, STEMS[chart.day_master]["polarity"])
    nature = DM_NATURE.get(nature_key, {})

    lines.append("### Designed For vs. Fighting Against\n")
    useful = strength.useful_god
    lines.append(f"This chart is designed to thrive with **{useful}** energy — "
                f"{ELEMENT_REMEDIES.get(useful, {}).get('industries', ['versatile work'])[0]} "
                f"type environments.")

    unfav = strength.unfavorable_elements
    if unfav:
        lines.append(f"\nThe biggest fight is against excessive **{unfav[0]}** energy, which "
                    f"{'crushes' if verdict in ('weak', 'extremely_weak') else 'stagnates'} "
                    f"this chart.\n")

    # Single most important thing
    lines.append("### The Single Most Important Thing\n")

    # Determine what matters most
    spouse = check_spouse_star(chart, classification)
    if spouse["is_critical_absent"] and chart.gender == "male":
        lines.append("**Your wife star is missing.** Marriage is your biggest life challenge. "
                    "Without conscious effort and the right timing (favorable luck pillars), "
                    "marriage will either not happen, happen late, or not last. "
                    "This is not a maybe — it's the chart's clearest signal.\n")
    elif verdict == "extremely_weak":
        lines.append(f"**You are running on empty.** Your {dm_element} energy is critically depleted. "
                    f"Everything — health, relationships, career — depends on getting more "
                    f"{strength.useful_god} into your life. Environment, colors, direction, "
                    f"career choice — all must align. This is not optional.\n")
    elif strength.is_following_chart:
        lines.append("**Stop fighting the current.** Your chart follows the dominant force. "
                    "The worst thing you can do is resist. Go where the energy flows — "
                    "the right career, the right location, the right people. "
                    "Surrender is your strength.\n")
    else:
        lines.append(f"**Balance is everything.** Your chart has real strengths but also real "
                    f"vulnerabilities. The useful god ({useful}) must be consistently "
                    f"present in your environment, career, and relationships. "
                    f"When it is, everything flows. When it isn't, problems compound.\n")

    return "\n".join(lines)


# =============================================================================
# MASTER REPORT GENERATOR
# =============================================================================

def generate_comprehensive_report(chart: ChartData) -> str:
    """
    Generate the complete 11-section BaZi analysis report.
    Pure Python, zero LLM, fully deterministic (except random template selection).
    """
    # Run all analyses
    tg_entries = map_all_ten_gods(chart)
    tg_classification = classify_ten_god_strength(tg_entries)
    strength = assess_day_master_strength(chart)
    interactions = detect_all_interactions(chart)
    shen_sha = run_all_shen_sha(chart)
    predictions = run_all_predictions(chart)
    env = assess_environment(chart, strength)

    # Build report
    sections = [
        f"# Comprehensive BaZi Analysis Report\n",
        f"**Gender**: {chart.gender.capitalize()} | **Age**: {chart.age} | "
        f"**Birth Year**: {chart.birth_year}\n",
        f"---\n",
        section_chart_setup(chart, tg_entries),
        "\n---\n",
        section_strength(chart, strength),
        "\n---\n",
        section_ten_gods(chart, tg_classification, tg_entries),
        "\n---\n",
        section_interactions(chart, interactions),
        "\n---\n",
        section_shen_sha(chart, shen_sha),
        "\n---\n",
        section_red_flags(chart, strength, tg_classification, interactions, shen_sha),
        "\n---\n",
        section_luck_pillar(chart, strength),
        "\n---\n",
        section_health(chart, strength, shen_sha),
        "\n---\n",
        section_remedies(chart, strength, env),
        "\n---\n",
        section_predictions(chart, predictions),
        "\n---\n",
        section_summary(chart, strength, tg_classification),
    ]

    return "\n".join(sections)
