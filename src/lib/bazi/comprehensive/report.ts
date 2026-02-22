import 'server-only';

// =============================================================================
// COMPREHENSIVE REPORT GENERATOR
// =============================================================================
// Assembles all analysis sections into a complete markdown report.
// Pure TypeScript, zero LLM dependency, fully deterministic.
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName } from '../core';
import { ELEMENT_CYCLES, getTenGod, getAllBranchQi, ELEMENT_CHINESE } from '../derived';
import type {
  ChartData, ShenShaResult, BranchInteraction,
  StrengthAssessment, RedFlag, EventPrediction,
  EnvironmentAssessment, TenGodEntry,
} from './models';
import {
  mapAllTenGods, classifyTenGodStrength, checkSpouseStar,
  checkChildrenStar, analyzeTenGodPatterns, TEN_GOD_INFO,
} from './ten-gods';
import { countSupportVsDrain, getSeasonalState } from './strength';
import { detectAllInteractions } from './interactions';
import { runAllShenSha } from './shen-sha';
import { runAllPredictions, getAnnualPillar } from './predictions';
import { assessEnvironment } from './environment';
import {
  DM_NATURE, STRENGTH_VERDICTS, TEN_GOD_INTERPRETATIONS,
  SHEN_SHA_IMPACTS, SEVERITY_LANGUAGE,
  HEALTH_ELEMENT_MAP, ELEMENT_REMEDIES, LIFE_LESSON_TEMPLATES, _pick,
} from './templates';
import { calculateWuxing, wuxingToElementCounts, type WuxingResult } from '../wuxing/calculator';
import { chartToWuxingInput } from './wuxing-bridge';


// =============================================================================
// SECTION 1: CHART SETUP
// =============================================================================

function sectionChartSetup(chart: ChartData, tgEntries: TenGodEntry[]): string {
  const lines: string[] = [];
  lines.push("## SECTION 1: CHART SETUP\n");

  // Four Pillars table
  lines.push("### Four Pillars (四柱)\n");
  lines.push("| | Year (年柱) | Month (月柱) | Day (日柱) | Hour (时柱) |");
  lines.push("|---|---|---|---|---|");

  // Palace
  lines.push("| **Palace** | Parents/Ancestry | Career/Social | Self/Spouse | Children/Legacy |");

  // Heavenly Stems
  const stems: string[] = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    const p = chart.pillars[pos];
    const s = STEMS[p.stem];
    stems.push(`${s.chinese} (${p.stem}) ${s.element}`);
  }
  lines.push(`| **Heavenly Stem** | ${stems.join(" | ")} |`);

  // Earthly Branches
  const branches: string[] = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    const p = chart.pillars[pos];
    const b = BRANCHES[p.branch];
    branches.push(`${b.chinese} (${p.branch}) ${b.element}`);
  }
  lines.push(`| **Earthly Branch** | ${branches.join(" | ")} |`);

  // Hidden Stems
  const hidden: string[] = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    const p = chart.pillars[pos];
    const qi = getAllBranchQi(p.branch);
    const hsStr = qi.map(([s, score]) => `${STEMS[s as StemName].chinese}(${score})`).join(", ");
    hidden.push(hsStr);
  }
  lines.push(`| **Hidden Stems** | ${hidden.join(" | ")} |`);

  lines.push("");

  // Day Master info
  const dm = chart.day_master;
  const dmInfo = STEMS[dm];
  const natureKey = `${dmInfo.element}|${dmInfo.polarity}`;
  const nature = DM_NATURE[natureKey];

  lines.push("### Day Master (日主)\n");
  lines.push(`**${dmInfo.chinese} (${dm}) — ${dmInfo.element} ${dmInfo.polarity}**\n`);
  if (nature) {
    const natureTexts = nature.nature;
    lines.push(`*${_pick(natureTexts)}*\n`);
    lines.push(`Personality: ${nature.personality}\n`);
  }

  // Ten Gods reference table
  lines.push("### Ten Gods Map (十神)\n");
  lines.push("| Location | Stem | Ten God | Chinese |");
  lines.push("|---|---|---|---|");
  for (const entry of tgEntries) {
    if (entry.position !== "luck_pillar") {
      const vis = entry.visible ? "" : " (hidden)";
      lines.push(
        `| ${entry.location}${vis} | ${STEMS[entry.stem].chinese} (${entry.stem}) `
        + `| ${entry.english} (${entry.abbreviation}) | ${entry.chinese} |`
      );
    }
  }

  // Luck pillar info if present
  if (chart.luck_pillar) {
    const lp = chart.luck_pillar;
    lines.push(`\n### Current Luck Pillar (大运)\n`);
    lines.push(
      `**${STEMS[lp.stem].chinese}${BRANCHES[lp.branch].chinese} `
      + `(${lp.stem} ${lp.branch})**\n`
    );
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 2: DM STRENGTH
// =============================================================================

function sectionStrength(chart: ChartData, strength: StrengthAssessment): string {
  const lines: string[] = [];
  lines.push("## SECTION 2: DAY MASTER STRENGTH ASSESSMENT\n");

  lines.push(`**Score: ${strength.score}/100** (50 = perfectly balanced)\n`);
  lines.push(`- Support count: ${strength.support_count}`);
  lines.push(`- Drain count: ${strength.drain_count}`);
  lines.push(`- Seasonal state: ${strength.seasonal_state}`);
  lines.push(`- Verdict: **${strength.verdict.toUpperCase().replace(/_/g, " ")}**\n`);

  // Verdict interpretation
  const verdictText = _pick(STRENGTH_VERDICTS[strength.verdict] ?? [""]);
  lines.push(`*${verdictText}*\n`);

  // Following chart
  if (strength.is_following_chart) {
    lines.push(`**FOLLOWING CHART (从格) DETECTED** — Type: ${strength.following_type}`);
    lines.push("This chart is so weak that it 'follows' the dominant force instead of fighting it.\n");
  }

  // Useful God
  lines.push(`### Useful God (用神): **${strength.useful_god}** (${ELEMENT_CHINESE[strength.useful_god as keyof typeof ELEMENT_CHINESE] ?? ""})\n`);
  const favStrs = strength.favorable_elements.map(e => `${e} (${ELEMENT_CHINESE[e as keyof typeof ELEMENT_CHINESE] ?? ""})`);
  const unfavStrs = strength.unfavorable_elements.map(e => `${e} (${ELEMENT_CHINESE[e as keyof typeof ELEMENT_CHINESE] ?? ""})`);
  lines.push(`- Favorable elements: ${favStrs.join(", ")}`);
  lines.push(`- Unfavorable elements: ${unfavStrs.join(", ")}`);

  return lines.join("\n");
}


// =============================================================================
// SECTION 3: TEN GODS DEEP ANALYSIS
// =============================================================================

function sectionTenGods(
  chart: ChartData,
  classification: Record<string, Record<string, unknown>>,
  tgEntries: TenGodEntry[],
): string {
  const lines: string[] = [];
  lines.push("## SECTION 3: TEN GODS DEEP ANALYSIS (十神)\n");

  // Classification table
  lines.push("| Ten God | Chinese | Strength | Visible | Hidden | Locations |");
  lines.push("|---|---|---|---|---|---|");
  for (const abbr of ["F", "RW", "EG", "HO", "IW", "DW", "7K", "DO", "IR", "DR"]) {
    const info = classification[abbr];
    lines.push(
      `| ${info.english} (${abbr}) | ${info.chinese} | `
      + `**${info.strength}** | ${info.visible_count} | `
      + `${info.hidden_count} | ${(info.locations as string[]).join(", ")} |`
    );
  }

  lines.push("");

  // Detailed interpretation for each
  for (const abbr of ["F", "RW", "EG", "HO", "IW", "DW", "7K", "DO", "IR", "DR"]) {
    const info = classification[abbr];
    const strengthLevel = info.strength as string;
    const templates = TEN_GOD_INTERPRETATIONS[abbr] ?? {};

    if (strengthLevel === "PROMINENT" && templates["PROMINENT"]) {
      lines.push(`**${info.english} (${info.chinese})**: ${_pick(templates["PROMINENT"])}\n`);
    } else if ((strengthLevel === "PRESENT" || strengthLevel === "HIDDEN_ONLY") && templates["PRESENT"]) {
      lines.push(`**${info.english} (${info.chinese})**: ${_pick(templates["PRESENT"])}\n`);
    } else if (strengthLevel === "ABSENT" && templates["ABSENT"]) {
      lines.push(`**${info.english} (${info.chinese})**: ${_pick(templates["ABSENT"])}\n`);
    }
  }

  // Spouse star check
  const spouse = checkSpouseStar(chart, classification);
  lines.push(`### Spouse Star: ${spouse.label}\n`);
  if (spouse.is_critical_absent) {
    lines.push(
      `**WARNING: ${spouse.label} is ABSENT.** `
      + `This is a critical indicator for marriage difficulty.\n`
    );
  } else {
    lines.push(`Status: ${spouse.strength}. Locations: ${(spouse.locations as string[]).join(", ")}\n`);
  }

  // Children star check
  const children = checkChildrenStar(chart, classification);
  lines.push(`### Children Stars: ${children.primary_star} / ${children.secondary_star}\n`);
  if (!children.any_present) {
    lines.push("**Both children stars are ABSENT.** Children may come late or with difficulty.\n");
  }

  // Patterns
  const patterns = analyzeTenGodPatterns(chart, classification);
  if (patterns.length > 0) {
    lines.push("### Notable Patterns\n");
    for (const p of patterns) {
      lines.push(`- **${p.pattern}**: ${p.description}`);
    }
    lines.push("");
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 4: BRANCH INTERACTIONS
// =============================================================================

function sectionInteractions(chart: ChartData, interactions: BranchInteraction[]): string {
  const lines: string[] = [];
  lines.push("## SECTION 4: BRANCH INTERACTIONS (地支关系)\n");

  if (interactions.length === 0) {
    lines.push("No significant branch interactions detected.\n");
    return lines.join("\n");
  }

  // Group by type
  const byType: Record<string, BranchInteraction[]> = {};
  for (const inter of interactions) {
    if (!byType[inter.interaction_type]) {
      byType[inter.interaction_type] = [];
    }
    byType[inter.interaction_type].push(inter);
  }

  const typeOrder = [
    "clash", "harmony", "three_harmony", "half_three_harmony",
    "directional_combo", "punishment", "self_punishment", "harm", "destruction",
  ];

  const typeLabels: Record<string, string> = {
    clash: "Six Clashes (六冲)",
    harmony: "Six Harmonies (六合)",
    three_harmony: "Three Harmony Frames (三合局)",
    half_three_harmony: "Half Three Harmony (半三合)",
    directional_combo: "Directional Combinations (三会局)",
    punishment: "Punishments (三刑)",
    self_punishment: "Self-Punishments (自刑)",
    harm: "Six Harms (六害)",
    destruction: "Destructions (破)",
  };

  for (const itype of typeOrder) {
    if (!byType[itype]) continue;
    const items = byType[itype];
    lines.push(`### ${typeLabels[itype] ?? itype}\n`);
    for (const item of items) {
      const lpTag = item.activated_by_lp ? " **[ACTIVATED BY LUCK PILLAR]**" : "";
      lines.push(`- **${item.description}**${lpTag}`);
      lines.push(`  - Palaces: ${item.palaces.join(", ")}`);
      lines.push(`  - Severity: ${item.severity}`);
    }
    lines.push("");
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 5: SHEN SHA AUDIT
// =============================================================================

function sectionShenSha(chart: ChartData, shenSha: ShenShaResult[]): string {
  const lines: string[] = [];
  lines.push("## SECTION 5: SHEN SHA FULL AUDIT (神煞)\n");

  const present = shenSha.filter(s => s.present);
  const absent = shenSha.filter(s => !s.present);

  lines.push("### Present Stars\n");
  if (present.length > 0) {
    lines.push("| Star | Chinese | Location | Palace | Nature | Severity | Void? |");
    lines.push("|---|---|---|---|---|---|---|");
    for (const s of present) {
      const voidTag = s.is_void ? "VOID" : "";
      const palace = s.palace ?? "";
      const activated = s.activated_by ? ` (via ${s.activated_by})` : "";
      lines.push(
        `| ${s.name_english} | ${s.name_chinese} | ${s.location ?? ""} `
        + `| ${palace}${activated} | ${s.nature} | ${s.severity} | ${voidTag} |`
      );
    }
  } else {
    lines.push("No stars detected.\n");
  }

  lines.push("");

  // Derivation details
  lines.push("### Derivation Details\n");
  for (const s of present) {
    lines.push(`- **${s.name_chinese} (${s.name_english})**: ${s.derivation}`);

    // Impact template
    const impacts = SHEN_SHA_IMPACTS[s.name_chinese];
    if (impacts && impacts.present) {
      lines.push(`  - *${_pick(impacts.present)}*`);
    }

    if (s.is_void) {
      lines.push(
        `  - **NOTE: This star sits on a VOID branch. `
        + `Its effect is weakened or unreliable.**`
      );
    }
  }
  lines.push("");

  // Notable absences
  const criticalAbsent = new Set(["天乙贵人", "禄神", "天医", "天德贵人", "文昌贵人", "将星", "红鸾"]);
  const notableAbsent = absent.filter(s => criticalAbsent.has(s.name_chinese));
  if (notableAbsent.length > 0) {
    lines.push("### Notable Absences\n");
    for (const s of notableAbsent) {
      const impacts = SHEN_SHA_IMPACTS[s.name_chinese];
      if (impacts && impacts.absent) {
        lines.push(`- **${s.name_chinese} (${s.name_english})**: ${_pick(impacts.absent)}`);
      }
    }
    lines.push("");
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 6: RED FLAGS
// =============================================================================

function sectionRedFlags(
  chart: ChartData,
  strength: StrengthAssessment,
  classification: Record<string, Record<string, unknown>>,
  interactions: BranchInteraction[],
  shenSha: ShenShaResult[],
): string {
  const lines: string[] = [];
  lines.push("## SECTION 6: RED FLAGS — DIRECT AND UNFILTERED\n");

  // Collect all red flags by life area
  const flags: Record<string, RedFlag[]> = {
    wealth: [], marriage: [], career: [], health: [], character: [],
  };

  // From Ten Gods
  const patterns = analyzeTenGodPatterns(chart, classification);
  for (const p of patterns) {
    const areas = (p.life_areas as string[]) ?? [];
    let target = areas[0] ?? "character";
    if (target === "relationship") target = "marriage";
    if (!(target in flags)) target = "character";
    flags[target].push({
      life_area: target,
      indicator_type: "ten_god",
      indicator_name: p.pattern as string,
      description: p.description as string,
      severity: p.severity as string,
    });
  }

  // Spouse star absent
  const spouse = checkSpouseStar(chart, classification);
  if (spouse.is_critical_absent) {
    flags.marriage.push({
      life_area: "marriage",
      indicator_type: "ten_god",
      indicator_name: `${spouse.star} absent`,
      description: `${spouse.label} is completely ABSENT from the natal chart.`,
      severity: "severe",
    });
  }

  // From branch interactions (negative ones)
  for (const inter of interactions) {
    if (["clash", "punishment", "self_punishment", "harm"].includes(inter.interaction_type)) {
      for (const palace of inter.palaces) {
        let target: string | null = null;
        if (palace.includes("Spouse")) target = "marriage";
        else if (palace.includes("Career")) target = "career";
        else if (palace.includes("Children")) target = "marriage";
        else if (palace.includes("Parents")) target = "character";
        if (target) {
          flags[target].push({
            life_area: target,
            indicator_type: "branch_interaction",
            indicator_name: inter.chinese_name,
            description: inter.description,
            severity: inter.severity,
          });
        }
      }
    }
  }

  // From Shen Sha
  const presentInauspicious = shenSha.filter(s => s.present && s.nature === "inauspicious");
  for (const s of presentInauspicious) {
    const areas = s.life_areas;
    let target = areas[0] ?? "character";
    if (target === "relationship") target = "marriage";
    if (!(target in flags)) target = "character";
    flags[target].push({
      life_area: target,
      indicator_type: "shen_sha",
      indicator_name: s.name_chinese,
      description: `${s.name_english} (${s.name_chinese}) in ${s.palace ?? "chart"}`,
      severity: s.severity,
    });
  }

  // Output by life area
  const severityOrder: Record<string, number> = { critical: 0, severe: 1, moderate: 2, mild: 3 };

  const areaLabels: Array<[string, string]> = [
    ["marriage", "Marriage & Relationships"],
    ["wealth", "Wealth & Finances"],
    ["career", "Career & Authority"],
    ["health", "Health"],
    ["character", "Character & Behavior"],
  ];

  let sev = "";
  for (const [area, label] of areaLabels) {
    const areaFlags = flags[area] ?? [];
    if (areaFlags.length === 0) {
      lines.push(`### ${label}\n`);
      lines.push("No significant red flags in this area.\n");
      continue;
    }

    areaFlags.sort((a, b) => (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3));
    lines.push(`### ${label} (${areaFlags.length} indicators)\n`);

    for (const f of areaFlags) {
      sev = _pick(SEVERITY_LANGUAGE[f.severity] ?? [f.severity]);
      lines.push(
        `- **[${f.severity.toUpperCase()}] ${f.indicator_name}** (${f.indicator_type}): `
        + `${f.description}`
      );
    }
    lines.push(
      `\n*${areaFlags.length} separate indicators affect ${label.toLowerCase()}.* `
      + `${sev}\n`
    );
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 7: CURRENT LUCK PILLAR
// =============================================================================

function sectionLuckPillar(chart: ChartData, strength: StrengthAssessment): string {
  const lines: string[] = [];
  lines.push("## SECTION 7: CURRENT LUCK PILLAR ANALYSIS (大运)\n");

  if (!chart.luck_pillar) {
    lines.push("No luck pillar provided.\n");
    return lines.join("\n");
  }

  const lp = chart.luck_pillar;
  const dm = chart.day_master;

  // LP stem ten god
  const tg = getTenGod(dm, lp.stem);
  const tgStr = tg ? `${tg[1]} (${tg[0]} / ${tg[2]})` : "Unknown";

  lines.push(
    `**Luck Pillar: ${STEMS[lp.stem].chinese}${BRANCHES[lp.branch].chinese} `
    + `(${lp.stem} ${lp.branch})**\n`
  );
  lines.push(`- Stem Ten God: ${tgStr}`);
  lines.push(`- Stem Element: ${STEMS[lp.stem].element}`);
  lines.push(`- Branch Element: ${BRANCHES[lp.branch].element}`);

  // Hidden stems in LP branch
  const lpQi = getAllBranchQi(lp.branch);
  const lpQiStrs = lpQi.map(([s, sc]) => `${STEMS[s as StemName].chinese}(${sc})`);
  lines.push(`- Branch Hidden Stems: ${lpQiStrs.join(", ")}`);

  // Is LP element favorable?
  const lpStemElem = STEMS[lp.stem].element;
  const lpBranchElem = BRANCHES[lp.branch].element;
  const fav = strength.favorable_elements;
  const unfav = strength.unfavorable_elements;

  const stemVerdict = fav.includes(lpStemElem) ? "FAVORABLE" : (unfav.includes(lpStemElem) ? "UNFAVORABLE" : "NEUTRAL");
  const branchVerdict = fav.includes(lpBranchElem) ? "FAVORABLE" : (unfav.includes(lpBranchElem) ? "UNFAVORABLE" : "NEUTRAL");

  lines.push(`\n- LP Stem (${lpStemElem}): **${stemVerdict}**`);
  lines.push(`- LP Branch (${lpBranchElem}): **${branchVerdict}**\n`);

  // Current year analysis
  const currentYear = new Date().getFullYear();
  const [annualStem, annualBranch] = getAnnualPillar(currentYear);
  const annualTg = getTenGod(dm, annualStem);
  const annualTgStr = annualTg ? `${annualTg[1]} (${annualTg[0]} / ${annualTg[2]})` : "Unknown";

  lines.push(
    `### Current Year ${currentYear}: `
    + `${STEMS[annualStem].chinese}${BRANCHES[annualBranch].chinese} `
    + `(${annualStem} ${annualBranch})\n`
  );
  lines.push(`- Annual Stem Ten God: ${annualTgStr}`);

  const annualStemElem = STEMS[annualStem].element;
  const annualVerdict = fav.includes(annualStemElem) ? "FAVORABLE" : (unfav.includes(annualStemElem) ? "UNFAVORABLE" : "NEUTRAL");
  lines.push(`- Annual Element (${annualStemElem}): **${annualVerdict}**\n`);

  return lines.join("\n");
}


// =============================================================================
// SECTION 8: HEALTH ANALYSIS
// =============================================================================

function sectionHealth(
  chart: ChartData,
  strength: StrengthAssessment,
  shenSha: ShenShaResult[],
  elemCounts: Record<string, number>,
): string {
  const lines: string[] = [];
  lines.push("## SECTION 8: HEALTH ANALYSIS (健康)\n");

  // Element balance table
  lines.push("### Element Balance\n");
  lines.push("| Element | Count | Status | Organs at Risk |");
  lines.push("|---|---|---|---|");

  const avg = Object.values(elemCounts).reduce((a, b) => a + b, 0) / 5;
  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const count = elemCounts[elem] ?? 0;
    const health = HEALTH_ELEMENT_MAP[elem];
    let status: string;
    let risk: string;
    if (count > avg * 1.5) {
      status = "EXCESS";
      risk = health.excess;
    } else if (count < avg * 0.5) {
      status = "DEFICIENT";
      risk = health.deficiency;
    } else {
      status = "Balanced";
      risk = "\u2014";
    }
    lines.push(
      `| ${elem} (${ELEMENT_CHINESE[elem as keyof typeof ELEMENT_CHINESE]}) | ${count.toFixed(1)} | ${status} `
      + `| ${risk} |`
    );
  }

  lines.push("");

  // TCM mapping
  lines.push("### Organ Systems at Risk\n");
  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const count = elemCounts[elem] ?? 0;
    const health = HEALTH_ELEMENT_MAP[elem];
    if (count > avg * 1.5) {
      lines.push(
        `- **${elem} EXCESS**: ${health.yin_organ} and ${health.yang_organ} overloaded. `
        + `Watch for: ${health.excess}. Body parts affected: ${health.body_parts}.`
      );
    } else if (count < avg * 0.5) {
      lines.push(
        `- **${elem} DEFICIENT**: ${health.yin_organ} and ${health.yang_organ} weakened. `
        + `Watch for: ${health.deficiency}. Body parts affected: ${health.body_parts}.`
      );
    }
  }

  // Health-related Shen Sha
  const healthStars = shenSha.filter(s => s.present && s.life_areas.includes("health"));
  if (healthStars.length > 0) {
    lines.push("\n### Health-Related Stars\n");
    for (const s of healthStars) {
      const impacts = SHEN_SHA_IMPACTS[s.name_chinese];
      const impactText = impacts?.present?.[0] ?? s.derivation;
      lines.push(`- **${s.name_chinese} (${s.name_english})**: ${impactText}`);
    }
  }

  lines.push("");
  return lines.join("\n");
}


// =============================================================================
// SECTION 9: REMEDIES
// =============================================================================

function sectionRemedies(
  chart: ChartData,
  strength: StrengthAssessment,
  env: EnvironmentAssessment,
): string {
  const lines: string[] = [];
  lines.push("## SECTION 9: REMEDIES & WHAT MUST CHANGE\n");

  const useful = strength.useful_god;
  const remedies = ELEMENT_REMEDIES[useful] ?? { colors: [], avoid_colors: [], industries: [], environment: [], direction: "" };

  // 9a Elemental
  lines.push("### 9a. Elemental Remedies\n");
  lines.push(`**Useful God Element: ${useful} (${ELEMENT_CHINESE[useful as keyof typeof ELEMENT_CHINESE] ?? ""})**\n`);
  lines.push(`- **Colors to wear**: ${remedies.colors.join(", ")}`);
  lines.push(`- **Colors to avoid**: ${remedies.avoid_colors.join(", ")}`);
  lines.push(`- **Favorable directions**: ${env.favorable_directions.join(", ")}`);
  lines.push(`- **Industries**: ${remedies.industries.join(", ")}`);
  lines.push(`- **Environment**: ${remedies.environment.join(", ")}\n`);

  // 9b Behavioral
  lines.push("### 9b. Behavioral Changes\n");
  if (strength.verdict === "weak" || strength.verdict === "extremely_weak") {
    lines.push("- Build support systems. You cannot do everything alone.");
    lines.push("- Avoid overcommitting. Your energy is limited — protect it.");
    lines.push("- Seek mentors and allies actively. They are your lifeline.");
  } else if (strength.verdict === "strong" || strength.verdict === "extremely_strong") {
    lines.push("- Channel excess energy into productive output (creative work, exercise).");
    lines.push("- Practice patience and listening. Your strength can bulldoze others.");
    lines.push("- Give more than you take. Generosity balances your chart.");
  }
  lines.push("");

  // 9c Relationship
  lines.push("### 9c. Relationship Guidance\n");
  const dmElement = chart.dm_element;
  const spouseElement = ELEMENT_CYCLES.controlling[dmElement] ?? "";
  lines.push(
    `- Best partner element alignment: ${spouseElement} `
    + `(${ELEMENT_CHINESE[spouseElement as keyof typeof ELEMENT_CHINESE] ?? ""})`
  );
  lines.push(
    `- Your spouse palace (Day Branch): `
    + `${BRANCHES[chart.pillars["day"].branch].chinese} `
    + `(${chart.pillars["day"].branch})\n`
  );

  // 9d Financial
  lines.push("### 9d. Financial Strategy\n");
  const wealthElement = ELEMENT_CYCLES.controlling[dmElement] ?? "";
  if (strength.verdict === "weak" || strength.verdict === "extremely_weak") {
    lines.push(
      `- Wealth element (${wealthElement}) is too heavy for a weak DM. `
      + "Focus on stable, low-risk income streams."
    );
    lines.push("- Avoid partnerships where you contribute capital. You'll lose it.");
  } else {
    lines.push(
      `- Wealth element (${wealthElement}) can be handled. `
      + "Take calculated risks in favorable years."
    );
  }
  lines.push("");

  // 9e Environmental
  lines.push("### 9e. Relocation & Environment\n");
  lines.push(
    `- Crossing Water benefit: **${env.guo_jiang_long_verdict.toUpperCase()}** `
    + `(score: ${env.guo_jiang_long_score}/5)`
  );
  for (const factor of env.guo_jiang_long_factors) {
    lines.push(`  - ${factor}`);
  }
  lines.push(`- Ideal climate: ${env.ideal_climate}`);
  lines.push(`- Ideal geography: ${env.ideal_geography}`);
  if (env.crosses_water_benefit) {
    lines.push(`\n**${env.crosses_water_reason}**`);
  }
  lines.push("");

  return lines.join("\n");
}


// =============================================================================
// SECTION 10: EVENT PREDICTIONS
// =============================================================================

function sectionPredictions(chart: ChartData, predictions: Record<string, EventPrediction[]>): string {
  const lines: string[] = [];
  lines.push("## SECTION 10: LIFE EVENT PREDICTIONS\n");

  const eventTypes: Array<[string, string]> = [
    ["marriage", "Marriage Timing"],
    ["divorce", "Divorce/Separation Risk"],
    ["children", "Children Arrival"],
    ["career", "Career Peaks"],
  ];

  for (const [eventType, label] of eventTypes) {
    const events = predictions[eventType] ?? [];
    lines.push(`### ${label}\n`);
    if (events.length === 0) {
      lines.push("No high-probability years detected.\n");
      continue;
    }

    lines.push("| Year | Age | Score | Key Factors |");
    lines.push("|---|---|---|---|");
    for (const e of events.slice(0, 5)) {
      const factorsStr = e.factors.slice(0, 3).join("; ");
      lines.push(`| ${e.year} | ${e.age} | ${e.score} | ${factorsStr} |`);
    }
    lines.push("");
  }

  return lines.join("\n");
}


// =============================================================================
// SECTION 11: HONEST SUMMARY
// =============================================================================

function sectionSummary(
  chart: ChartData,
  strength: StrengthAssessment,
  classification: Record<string, Record<string, unknown>>,
): string {
  const lines: string[] = [];
  lines.push("## SECTION 11: HONEST SUMMARY\n");

  const dmElement = chart.dm_element;
  const verdict = strength.verdict;

  // Life lesson
  let lesson: string;
  if (strength.is_following_chart) {
    lesson = _pick(LIFE_LESSON_TEMPLATES.following ?? [""]);
  } else if (verdict === "weak" || verdict === "extremely_weak") {
    const key = `weak_${dmElement.toLowerCase()}`;
    lesson = _pick(LIFE_LESSON_TEMPLATES[key] ?? LIFE_LESSON_TEMPLATES.weak_water ?? [""]);
  } else {
    lesson = _pick(LIFE_LESSON_TEMPLATES.strong_general ?? [""]);
  }

  lines.push("### Core Life Lesson\n");
  lines.push(`*${lesson}*\n`);

  // What designed for vs fighting
  const natureKey = `${dmElement}|${STEMS[chart.day_master].polarity}`;
  const nature = DM_NATURE[natureKey];

  lines.push("### Designed For vs. Fighting Against\n");
  const useful = strength.useful_god;
  const usefulRemedies = ELEMENT_REMEDIES[useful];
  lines.push(
    `This chart is designed to thrive with **${useful}** energy — `
    + `${usefulRemedies?.industries?.[0] ?? "versatile work"} `
    + `type environments.`
  );

  const unfavElements = strength.unfavorable_elements;
  if (unfavElements.length > 0) {
    const verb = (verdict === "weak" || verdict === "extremely_weak") ? "crushes" : "stagnates";
    lines.push(
      `\nThe biggest fight is against excessive **${unfavElements[0]}** energy, which `
      + `${verb} this chart.\n`
    );
  }

  // Single most important thing
  lines.push("### The Single Most Important Thing\n");

  const spouse = checkSpouseStar(chart, classification);
  if (spouse.is_critical_absent && chart.gender === "male") {
    lines.push(
      "**Your wife star is missing.** Marriage is your biggest life challenge. "
      + "Without conscious effort and the right timing (favorable luck pillars), "
      + "marriage will either not happen, happen late, or not last. "
      + "This is not a maybe — it's the chart's clearest signal.\n"
    );
  } else if (verdict === "extremely_weak") {
    lines.push(
      `**You are running on empty.** Your ${dmElement} energy is critically depleted. `
      + `Everything — health, relationships, career — depends on getting more `
      + `${strength.useful_god} into your life. Environment, colors, direction, `
      + `career choice — all must align. This is not optional.\n`
    );
  } else if (strength.is_following_chart) {
    lines.push(
      "**Stop fighting the current.** Your chart follows the dominant force. "
      + "The worst thing you can do is resist. Go where the energy flows — "
      + "the right career, the right location, the right people. "
      + "Surrender is your strength.\n"
    );
  } else {
    lines.push(
      `**Balance is everything.** Your chart has real strengths but also real `
      + `vulnerabilities. The useful god (${useful}) must be consistently `
      + `present in your environment, career, and relationships. `
      + `When it is, everything flows. When it isn't, problems compound.\n`
    );
  }

  return lines.join("\n");
}


// =============================================================================
// MASTER REPORT GENERATOR
// =============================================================================

export function generateComprehensiveReport(chart: ChartData, wuxingResult?: WuxingResult): string {
  /**
   * Generate the complete 11-section BaZi analysis report.
   * Pure TypeScript, zero LLM, fully deterministic (except random template selection).
   */
  // Compute wuxing result if not provided
  if (!wuxingResult) {
    wuxingResult = calculateWuxing(chartToWuxingInput(chart));
  }

  // Map wuxing strength label to legacy verdict
  const STRENGTH_TO_VERDICT: Record<string, string> = {
    dominant: 'extremely_strong',
    strong: 'strong',
    balanced: 'neutral',
    weak: 'weak',
    very_weak: 'extremely_weak',
  };

  // Build element percentages from wuxing
  const wuxingPercentages: Record<string, number> = {};
  for (const elem of ['Wood', 'Fire', 'Earth', 'Metal', 'Water'] as const) {
    wuxingPercentages[elem] = wuxingResult.elements[elem].percent;
  }

  // Build backward-compatible StrengthAssessment from wuxing
  const [support, drain] = countSupportVsDrain(chart);
  const seasonalState = getSeasonalState(chart);

  const strength: StrengthAssessment = {
    score: wuxingResult.dayMaster.percent,
    verdict: STRENGTH_TO_VERDICT[wuxingResult.dayMaster.strength] ?? 'neutral',
    useful_god: wuxingResult.gods.useful,
    element_percentages: wuxingPercentages,
    favorable_elements: [wuxingResult.gods.useful, wuxingResult.gods.favorable],
    unfavorable_elements: [wuxingResult.gods.unfavorable, wuxingResult.gods.enemy],
    support_count: Math.round(support * 100) / 100,
    drain_count: Math.round(drain * 100) / 100,
    seasonal_state: seasonalState,
    is_following_chart: false,
    following_type: null,
    best_element_pairs: [],
  };

  // Element counts from wuxing (percentage-based)
  const elemCounts = wuxingToElementCounts(wuxingResult);

  // Run all analyses
  const tgEntries = mapAllTenGods(chart);
  const tgClassification = classifyTenGodStrength(tgEntries);
  const interactions = detectAllInteractions(chart);
  const shenSha = runAllShenSha(chart);
  const predictions = runAllPredictions(chart);
  const env = assessEnvironment(chart, strength, wuxingResult);

  // Build report
  const sections = [
    `# Comprehensive BaZi Analysis Report\n`,
    `**Gender**: ${chart.gender.charAt(0).toUpperCase() + chart.gender.slice(1)} | **Age**: ${chart.age} | `
    + `**Birth Year**: ${chart.birth_year}\n`,
    `---\n`,
    sectionChartSetup(chart, tgEntries),
    "\n---\n",
    sectionStrength(chart, strength),
    "\n---\n",
    sectionTenGods(chart, tgClassification, tgEntries),
    "\n---\n",
    sectionInteractions(chart, interactions),
    "\n---\n",
    sectionShenSha(chart, shenSha),
    "\n---\n",
    sectionRedFlags(chart, strength, tgClassification, interactions, shenSha),
    "\n---\n",
    sectionLuckPillar(chart, strength),
    "\n---\n",
    sectionHealth(chart, strength, shenSha, elemCounts),
    "\n---\n",
    sectionRemedies(chart, strength, env),
    "\n---\n",
    sectionPredictions(chart, predictions),
    "\n---\n",
    sectionSummary(chart, strength, tgClassification),
  ];

  return sections.join("\n");
}
