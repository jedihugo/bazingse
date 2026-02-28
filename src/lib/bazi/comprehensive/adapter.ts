
// =============================================================================
// ADAPTER: Comprehensive Engine -> Frontend JSON
// =============================================================================
// Translates the comprehensive engine's TypeScript objects into the exact JSON
// shape the frontend expects from /api/analyze_bazi.
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName, type Element } from '../core';
import {
  getTenGod, getAllBranchQi, TEN_GODS, TEN_GOD_NOTES,
  ELEMENT_CYCLES, STEM_ORDER, BRANCH_ORDER, ELEMENT_CHINESE,
} from '../derived';
import {
  DM_WEALTH_STORAGE, STORAGE_OPENER, LARGE_WEALTH_STORAGE, WEALTH_ELEMENT_STEMS,
} from '../wealth-storage';
import { calculateWuxing, wuxingToElementCounts, type WuxingResult, type InteractionLog } from '../wuxing/calculator';
import { calculateDmLens } from '../wuxing/dm-lens';
import { chartToWuxingInput } from './wuxing-bridge';
import { getQiPhaseForPillar } from '../qi-phase';
import type {
  ChartData, Pillar, StrengthAssessment, BranchInteraction,
  ShenShaResult, TenGodEntry, RedFlag, EventPrediction,
  EnvironmentAssessment, LuckPillarInfo,
} from './models';
import {
  TEN_GOD_INFO, TEN_GOD_LIFE_MEANING,
  classifyTenGodStrength, analyzeTenGodPatterns,
  checkSpouseStar, checkChildrenStar,
} from './ten-gods';
import { countAllElements, adjustElementsForInteractions, applySeasonalScaling } from './strength';
import { analyzeQiPhases } from './qi-phase-analysis';
import { assessSpiritualSensitivity } from './spiritual-sensitivity';
import {
  DM_NATURE, STRENGTH_VERDICTS, TEN_GOD_INTERPRETATIONS,
  SHEN_SHA_IMPACTS, ELEMENT_REMEDIES, LIFE_LESSON_TEMPLATES,
  HEALTH_ELEMENT_MAP, HEALTH_BEHAVIORAL_REMEDIES,
  STRENGTH_EXPLANATION, CONTROL_CYCLE_EXPLANATIONS,
  _pick,
} from './templates';


// =============================================================================
// WEALTH STORAGE COMPUTATION (財庫)
// =============================================================================

function _computeWealthStorage(chart: ChartData): Record<string, unknown> {
  /**
   * Compute wealth storage (財庫) from ChartData for frontend display.
   */
  const dmStem = chart.day_master;
  const dmElement = chart.dm_element;
  const wealthElement = ELEMENT_CYCLES.controlling[dmElement] ?? "";
  const wealthStems = WEALTH_ELEMENT_STEMS[wealthElement as Element] ?? [];
  const storageBranch = DM_WEALTH_STORAGE[dmElement] ?? null;
  const openerBranch = storageBranch ? (STORAGE_OPENER[storageBranch] ?? null) : null;

  if (!storageBranch) {
    return {
      daymaster_element: dmElement, daymaster_stem: dmStem,
      wealth_element: wealthElement, wealth_stems: wealthStems,
      wealth_storage_branch: null, opener_branch: null,
      storages: [], all_storages: [], summary: `No storage mapping for ${dmElement} DM`,
    };
  }

  // Collect all pillars (natal + luck + time period)
  const allPillars: Array<[string, Pillar]> = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    if (chart.pillars[pos]) {
      allPillars.push([pos, chart.pillars[pos]]);
    }
  }
  if (chart.luck_pillar) {
    allPillars.push(["luck_pillar", chart.luck_pillar]);
  }
  for (const [pos, p] of Object.entries(chart.time_period_pillars)) {
    allPillars.push([pos, p]);
  }

  const storages: Array<Record<string, unknown>> = [];

  for (const [pos, pillar] of allPillars) {
    if (pillar.branch !== storageBranch) continue;

    // Check Large Wealth Storage
    const pillarKey = `${pillar.stem}-${pillar.branch}`;
    const isLarge = pillarKey in LARGE_WEALTH_STORAGE;

    // Check FILLER: wealth stems in OTHER positions
    const fillerPositions: string[] = [];
    for (const [otherPos, otherP] of allPillars) {
      if (otherPos === pos) continue;
      if (wealthStems.includes(otherP.stem as never)) {
        fillerPositions.push(`${otherPos}(HS)`);
      }
      // Check primary qi of branch
      if (otherP.hidden_stems && otherP.hidden_stems.length > 0) {
        const primaryStem = otherP.hidden_stems[0][0];
        if (wealthStems.includes(primaryStem as never)) {
          fillerPositions.push(`${otherPos}(EB)`);
        }
      }
    }
    const isFilled = fillerPositions.length > 0;

    // Check OPENER: clash branch in OTHER positions
    const openerPositions = allPillars
      .filter(([otherPos, otherP]) => otherPos !== pos && otherP.branch === openerBranch)
      .map(([otherPos]) => otherPos);
    const isOpened = openerPositions.length > 0;

    // Activation level
    let activation: string;
    if (isFilled && isOpened) {
      activation = "maximum";
    } else if (isFilled || isOpened) {
      activation = "activated";
    } else {
      activation = "latent";
    }

    const branchChinese = BRANCHES[storageBranch as BranchName]?.chinese ?? storageBranch;
    const stemChinese = STEMS[pillar.stem]?.chinese ?? pillar.stem;

    storages.push({
      position: pos,
      branch: storageBranch,
      branch_chinese: branchChinese,
      pillar: pillarKey,
      pillar_chinese: `${stemChinese}${branchChinese}`,
      is_large: isLarge,
      storage_type: "wealth",
      stored_element: wealthElement,
      wealth_element: wealthElement,
      filler_stems: [...wealthStems],
      is_filled: isFilled,
      filler_positions: fillerPositions,
      opener_branch: openerBranch,
      is_opened: isOpened,
      opener_positions: openerPositions,
      activation_level: activation,
    });
  }

  // Summary
  const total = storages.length;
  const maximum = storages.filter(s => s.activation_level === "maximum").length;
  const activated = storages.filter(s => s.activation_level !== "latent").length;
  const largeCount = storages.filter(s => s.is_large).length;
  const branchChineseLabel = BRANCHES[storageBranch as BranchName]?.chinese ?? storageBranch;

  let summary: string;
  if (total === 0) {
    summary = `No wealth storage (财库) found for ${dmElement} DM. Storage branch ${storageBranch} (${branchChineseLabel}) not in chart.`;
  } else {
    const parts: string[] = [];
    if (largeCount) parts.push(`${largeCount} Large (大财库)`);
    if (total - largeCount) parts.push(`${total - largeCount} Standard (财库)`);
    summary = `Found ${parts.join(", ")} for ${dmElement} DM. `;
    if (maximum) {
      summary += `${maximum} at MAXIMUM activation (filled + opened). `;
    } else if (activated) {
      summary += `${activated}/${total} activated. `;
    } else {
      summary += `All ${total} latent (locked). `;
    }
  }

  return {
    daymaster_element: dmElement, daymaster_stem: dmStem,
    wealth_element: wealthElement, wealth_stems: [...wealthStems],
    wealth_storage_branch: storageBranch, opener_branch: openerBranch,
    storages, all_storages: storages,
    summary,
  };
}


// =============================================================================
// NODE KEY MAPPING
// =============================================================================

const POSITION_TO_NODE: Record<string, [string, string]> = {
  year:        ["hs_y",    "eb_y"],
  month:       ["hs_m",    "eb_m"],
  day:         ["hs_d",    "eb_d"],
  hour:        ["hs_h",    "eb_h"],
  luck_pillar: ["hs_10yl", "eb_10yl"],
  annual:      ["hs_yl",   "eb_yl"],
  monthly:     ["hs_ml",   "eb_ml"],
  daily:       ["hs_dl",   "eb_dl"],
  hourly:      ["hs_hl",   "eb_hl"],
};


// =============================================================================
// BUILD STEM (HS) NODE
// =============================================================================

function buildStemNode(pillar: Pillar, chart: ChartData): Record<string, unknown> {
  const stem = pillar.stem;
  const qi: Record<string, number> = { [stem]: 100.0 };

  // Ten God
  const tg = getTenGod(chart.day_master, stem);
  const tenGodAbbr = tg ? tg[0] : (stem === chart.day_master ? "DM" : "");

  // Qi phase
  let qiPhase: string | null = null;
  try {
    const phase = getQiPhaseForPillar(stem, pillar.branch);
    qiPhase = phase ? phase.id : null;
  } catch {
    // ignore
  }

  return {
    id: stem,
    base: { id: stem, qi: { ...qi } },
    post: { id: stem, qi: { ...qi } },
    badges: [],
    base_qi: { ...qi },
    qi_phase: qiPhase,
    ten_god: tenGodAbbr,
    interaction_ids: [],
  };
}


// =============================================================================
// BUILD BRANCH (EB) NODE
// =============================================================================

function buildBranchNode(pillar: Pillar, chart: ChartData): Record<string, unknown> {
  const branch = pillar.branch;
  const branchData = BRANCHES[branch];

  // Build qi dict from branch hidden stems
  const qi: Record<string, number> = {};
  for (const [stemId, score] of branchData.qi) {
    qi[stemId] = score;
  }

  // Ten God for primary qi
  const primaryQi = branchData.qi[0];
  let tg: readonly [string, string, string] | null = null;
  if (primaryQi) {
    tg = getTenGod(chart.day_master, primaryQi[0]);
  }
  const tenGodAbbr = tg ? tg[0] : "";

  return {
    id: branch,
    base: { id: branch, qi: { ...qi } },
    post: { id: branch, qi: { ...qi } },
    badges: [],
    base_qi: { ...qi },
    ten_god: tenGodAbbr,
    interaction_ids: [],
  };
}


// =============================================================================
// BUILD ALL NODES
// =============================================================================

function buildAllNodes(chart: ChartData): Record<string, Record<string, unknown>> {
  const nodes: Record<string, Record<string, unknown>> = {};

  for (const [pos, pillar] of Object.entries(chart.pillars)) {
    if (!(pos in POSITION_TO_NODE)) continue;
    const [hsKey, ebKey] = POSITION_TO_NODE[pos];
    nodes[hsKey] = buildStemNode(pillar, chart);
    nodes[ebKey] = buildBranchNode(pillar, chart);
  }

  // Luck pillar
  if (chart.luck_pillar) {
    const [hsKey, ebKey] = POSITION_TO_NODE.luck_pillar;
    nodes[hsKey] = buildStemNode(chart.luck_pillar, chart);
    nodes[ebKey] = buildBranchNode(chart.luck_pillar, chart);
  }

  // Time-period pillars
  for (const [tpPos, tpPillar] of Object.entries(chart.time_period_pillars)) {
    if (tpPos in POSITION_TO_NODE) {
      const [hsKey, ebKey] = POSITION_TO_NODE[tpPos];
      nodes[hsKey] = buildStemNode(tpPillar, chart);
      nodes[ebKey] = buildBranchNode(tpPillar, chart);
    }
  }

  return nodes;
}


// =============================================================================
// BADGE MAPPING
// =============================================================================

const INTERACTION_TO_BADGE: Record<string, string> = {
  clash: "conflict",
  harmony: "combination",
  three_harmony: "combination",
  half_three_harmony: "combination",
  directional_combo: "combination",
  punishment: "conflict",
  self_punishment: "conflict",
  harm: "conflict",
  destruction: "conflict",
};

function _branchToNodeKey(branch: string, chart: ChartData): string | null {
  for (const [pos, pillar] of Object.entries(chart.pillars)) {
    if (pillar.branch === branch && pos in POSITION_TO_NODE) {
      return POSITION_TO_NODE[pos][1];
    }
  }
  if (chart.luck_pillar && chart.luck_pillar.branch === branch) {
    return POSITION_TO_NODE.luck_pillar[1];
  }
  for (const [pos, pillar] of Object.entries(chart.time_period_pillars)) {
    if (pillar.branch === branch && pos in POSITION_TO_NODE) {
      return POSITION_TO_NODE[pos][1];
    }
  }
  return null;
}

function mapInteractionsToBadges(
  interactions: BranchInteraction[],
  chart: ChartData,
  nodes: Record<string, Record<string, unknown>>,
): void {
  for (let idx = 0; idx < interactions.length; idx++) {
    const inter = interactions[idx];
    const badgeType = INTERACTION_TO_BADGE[inter.interaction_type] ?? "conflict";
    const interactionId = `INT_${idx}_${inter.interaction_type}`;

    for (const branch of inter.branches) {
      const nodeKey = _branchToNodeKey(branch, chart);
      if (nodeKey && nodes[nodeKey]) {
        (nodes[nodeKey].badges as Array<Record<string, unknown>>).push({
          type: badgeType,
          interaction_id: interactionId,
          chinese_name: inter.chinese_name,
          description: inter.description,
        });
        const ids = nodes[nodeKey].interaction_ids as string[];
        if (!ids.includes(interactionId)) {
          ids.push(interactionId);
        }
      }
    }
  }
}


// =============================================================================
// INTERACTIONS -> DICT
// =============================================================================

function buildInteractionDict(interactions: BranchInteraction[]): Record<string, Record<string, unknown>> {
  const result: Record<string, Record<string, unknown>> = {};
  for (let idx = 0; idx < interactions.length; idx++) {
    const inter = interactions[idx];
    const intId = `INT_${idx}_${inter.interaction_type}`;
    const branchChinese = inter.branches.map(b => {
      if (b in STEMS) return STEMS[b as StemName].chinese;
      if (b in BRANCHES) return BRANCHES[b as BranchName].chinese;
      return b;
    }).join("");
    result[intId] = {
      id: intId,
      type: inter.interaction_type.toUpperCase(),
      chinese_name: inter.chinese_name,
      branches: inter.branches,
      palaces: inter.palaces,
      description: inter.description,
      branch_chinese: branchChinese,
      severity: inter.severity,
      activated_by_lp: inter.activated_by_lp,
    };
  }
  return result;
}


// =============================================================================
// DAYMASTER ANALYSIS
// =============================================================================

function buildDaymasterAnalysis(strength: StrengthAssessment, chart: ChartData): Record<string, unknown> {
  const dm = chart.day_master;
  const dmInfo = STEMS[dm];

  const verdictMap: Record<string, string> = {
    extremely_strong: "Extremely Strong",
    strong: "Strong",
    neutral: "Balanced",
    weak: "Weak",
    extremely_weak: "Extremely Weak",
  };

  let chartType: string;
  if (strength.is_following_chart) {
    chartType = `Following (${strength.following_type})`;
  } else if (strength.verdict === "strong" || strength.verdict === "extremely_strong") {
    chartType = "Strong";
  } else if (strength.verdict === "weak" || strength.verdict === "extremely_weak") {
    chartType = "Weak";
  } else {
    chartType = "Balanced";
  }

  const total = strength.support_count + strength.drain_count;
  const supportPct = total > 0 ? Math.round(strength.support_count / total * 1000) / 10 : 50;

  return {
    daymaster: dm,
    daymaster_chinese: dmInfo.chinese,
    daymaster_element: dmInfo.element,
    daymaster_polarity: dmInfo.polarity,
    chart_type: chartType,
    daymaster_percentage: strength.score,
    strength: verdictMap[strength.verdict] ?? "Balanced",
    support_percentage: supportPct,
    seasonal_state: strength.seasonal_state,
    useful_god: strength.useful_god,
    favorable_elements: strength.favorable_elements,
    unfavorable_elements: strength.unfavorable_elements,
    is_following_chart: strength.is_following_chart,
    following_type: strength.following_type,
  };
}


// =============================================================================
// ELEMENT SCORES (3-tier: base -> natal -> post)
// =============================================================================

function buildElementScores(
  chart: ChartData,
  interactions?: BranchInteraction[],
  wuxingResult?: WuxingResult,
): [Record<string, number>, Record<string, number>, Record<string, number>] {
  function _toStemScores(elemCounts: Record<string, number>): Record<string, number> {
    const scores: Record<string, number> = {};
    for (const stemId of Object.keys(STEMS)) {
      const stemElem = STEMS[stemId as StemName].element;
      scores[stemId] = Math.round((elemCounts[stemElem] ?? 0) * 50 * 10) / 10;
    }
    return scores;
  }

  // Compute wuxing result if not provided
  if (!wuxingResult) {
    wuxingResult = calculateWuxing(chartToWuxingInput(chart));
  }

  // Use wuxing element percentages for natal scores (base + natal)
  // For stem scores, use percentage-based approach: each stem gets its element's percentage
  // This keeps the bar chart proportions identical to the wuxing percentages
  const natalPctCounts: Record<string, number> = {};
  for (const elem of ['Wood', 'Fire', 'Earth', 'Metal', 'Water']) {
    // Convert percentage (0-100) to a "count" that, when multiplied by 50,
    // gives a score proportional to the element's presence
    natalPctCounts[elem] = wuxingResult.elements[elem as keyof typeof wuxingResult.elements].percent / 100 * 10;
  }

  const natalScores = _toStemScores(natalPctCounts);

  // Post scores: only differ from natal when luck/time pillars are present.
  // Without them, post === natal (no arrows in the UI).
  const hasExtraPillars = !!chart.luck_pillar || Object.keys(chart.time_period_pillars).length > 0;

  if (!hasExtraPillars) {
    return [natalScores, { ...natalScores }, { ...natalScores }];
  }

  // With luck/time pillars, use old pipeline for "full chart" scores
  // (wuxing calculator doesn't include luck/time pillars yet)
  let fullCounts = countAllElements(chart);
  if (interactions && interactions.length > 0) {
    fullCounts = adjustElementsForInteractions(fullCounts, interactions, chart);
  }
  const monthBranch = chart.pillars["month"].branch;
  fullCounts = applySeasonalScaling(fullCounts, monthBranch);
  const fullScores = _toStemScores(fullCounts);

  return [natalScores, { ...natalScores }, fullScores];
}


// =============================================================================
// SPECIAL STARS (SHEN SHA)
// =============================================================================

function buildSpecialStars(shenSha: ShenShaResult[]): Array<Record<string, unknown>> {
  const stars: Array<Record<string, unknown>> = [];
  for (const s of shenSha) {
    if (!s.present) continue;
    stars.push({
      chinese_name: s.name_chinese,
      english_name: s.name_english,
      target_branch: s.location ?? "",
      palace: s.palace ?? "",
      nature: s.nature,
      impact: s.impact,
      severity: s.severity,
      is_void: s.is_void,
      derivation: s.derivation,
      life_areas: s.life_areas,
    });
  }
  return stars;
}


// =============================================================================
// RED FLAGS COLLECTOR
// =============================================================================

function _collectRedFlags(
  chart: ChartData,
  strength: StrengthAssessment,
  tgClassification: Record<string, Record<string, unknown>>,
  interactions: BranchInteraction[],
  shenSha: ShenShaResult[],
): Record<string, RedFlag[]> {
  const flags: Record<string, RedFlag[]> = {
    wealth: [], marriage: [], career: [],
    health: [], character: [],
  };

  // From Ten God patterns
  const patterns = analyzeTenGodPatterns(chart, tgClassification);
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

  // Spouse star check
  const spouse = checkSpouseStar(chart, tgClassification);
  if (spouse.is_critical_absent) {
    flags.marriage.push({
      life_area: "marriage",
      indicator_type: "ten_god",
      indicator_name: `${spouse.star} absent`,
      description: `${spouse.label} is completely ABSENT from the natal chart.`,
      severity: "severe",
    });
  }

  // From branch interactions
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
  for (const s of shenSha) {
    if (!s.present || s.nature !== "inauspicious") continue;
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

  return flags;
}


function _severityCategory(flags: RedFlag[]): string {
  if (flags.length === 0) return "balanced";
  const severities = flags.map(f => f.severity);
  if (severities.includes("critical") || severities.includes("severe")) return "warning";
  if (severities.includes("moderate")) return "caution";
  return "mild";
}


function _buildPatternEngineStub(flags: RedFlag[]): Record<string, unknown> {
  return {
    pattern_count: flags.length,
    compound_severity: flags.length * 10,
    severity_level: _severityCategory(flags),
    top_patterns: flags.slice(0, 5).map(f => ({
      chinese_name: f.indicator_name,
      severity: f.severity === "mild" ? 0.5 : f.severity === "moderate" ? 0.7 : 0.9,
      level: f.severity,
    })),
    recommendations: [],
  };
}


// =============================================================================
// HEALTH / WEALTH / LEARNING ANALYSIS
// =============================================================================

function buildHealthAnalysis(
  flags: Record<string, RedFlag[]>,
  strength: StrengthAssessment,
  chart: ChartData,
  elemCounts?: Record<string, number>,
): Record<string, unknown> {
  const healthFlags = flags.health ?? [];
  // Use wuxing-based element percentages if provided, otherwise compute
  if (!elemCounts) {
    const wr = calculateWuxing(chartToWuxingInput(chart));
    elemCounts = wuxingToElementCounts(wr);
  }
  const warnings: Array<Record<string, unknown>> = [];

  // With percentage-based counts (avg=20), < 12% is deficient
  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    if ((elemCounts[elem] ?? 0) < 12) {
      const organInfo = HEALTH_ELEMENT_MAP[elem];
      warnings.push({
        element: elem,
        organ_system: organInfo.yin_organ.split("(")[0].trim(),
        zang_organ: organInfo.yin_organ,
        fu_organ: organInfo.yang_organ,
        severity: "moderate",
        conflict_count: 0,
        weighted_score: Math.round((20 - (elemCounts[elem] ?? 0)) * 5) / 10,
        seasonal_state: strength.seasonal_state,
      });
    }
  }

  let analysisText: string;
  if (warnings.length > 0) {
    const primary = warnings[0];
    analysisText = `Monitor ${primary.organ_system} system (${primary.element} element). Element count is low, indicating potential vulnerability.`;
  } else if (healthFlags.length > 0) {
    analysisText = `Health concern flagged: ${healthFlags[0].description}`;
  } else {
    analysisText = "Overall health picture is balanced with no significant vulnerabilities detected.";
  }

  const severityScore = Math.min(100, healthFlags.length * 15 + warnings.length * 10);
  let severityCat: string;
  if (severityScore >= 70) severityCat = "severe";
  else if (severityScore >= 40) severityCat = "moderate";
  else if (severityScore > 0) severityCat = "mild";
  else severityCat = "balanced";

  return {
    health_warnings: warnings,
    conflict_severity_score: Math.round(severityScore * 10) / 10,
    severity_category: severityCat,
    most_vulnerable_element: warnings.length > 0 ? warnings[0].element : null,
    seasonal_vulnerability: {},
    analysis_text: analysisText,
    pattern_engine: _buildPatternEngineStub(healthFlags),
  };
}


function buildWealthAnalysis(
  flags: Record<string, RedFlag[]>,
  strength: StrengthAssessment,
  tgClassification: Record<string, Record<string, unknown>>,
  chart: ChartData,
): Record<string, unknown> {
  const wealthFlags = flags.wealth ?? [];
  const dmElement = chart.dm_element;
  const wealthElement = ELEMENT_CYCLES.controlling[dmElement] ?? "";

  const dwInfo = tgClassification.DW ?? {};
  const iwInfo = tgClassification.IW ?? {};
  const hasWealth = (dwInfo.strength ?? "ABSENT") !== "ABSENT" || (iwInfo.strength ?? "ABSENT") !== "ABSENT";

  const outlook = hasWealth && wealthFlags.length === 0
    ? "favorable"
    : (wealthFlags.length > 0 ? "challenging" : "neutral");

  let analysisText: string;
  if (outlook === "favorable") {
    analysisText = `Wealth element (${wealthElement}) is present. Financial opportunities are accessible.`;
  } else if (outlook === "challenging") {
    analysisText = `Wealth element (${wealthElement}) faces challenges. ${wealthFlags[0]?.description ?? ""}`;
  } else {
    analysisText = "Wealth outlook is neutral. Steady financial management recommended.";
  }

  return {
    wealth_element: wealthElement,
    wealth_score: 50.0,
    wealth_change: 0.0,
    wealth_seasonal_state: strength.seasonal_state,
    daymaster_can_handle: strength.verdict !== "extremely_weak",
    storage_status: "unknown",
    opportunities: [],
    risks: wealthFlags.map(f => f.description),
    outlook,
    analysis_text: analysisText,
    opportunity_score: hasWealth ? 50 : 20,
    risk_score: wealthFlags.length * 20,
    has_exceptional_opportunity: false,
    pattern_engine: _buildPatternEngineStub(wealthFlags),
  };
}


function buildLearningAnalysis(
  flags: Record<string, RedFlag[]>,
  strength: StrengthAssessment,
  tgClassification: Record<string, Record<string, unknown>>,
  chart: ChartData,
): Record<string, unknown> {
  const dmElement = chart.dm_element;
  const resourceElement = ELEMENT_CYCLES.generated_by[dmElement] ?? "";
  const outputElement = ELEMENT_CYCLES.generating[dmElement] ?? "";

  const drInfo = tgClassification.DR ?? {};
  const irInfo = tgClassification.IR ?? {};
  const hasResource = (drInfo.strength ?? "ABSENT") !== "ABSENT" || (irInfo.strength ?? "ABSENT") !== "ABSENT";

  const outlook = hasResource ? "favorable" : "neutral";
  const analysisText =
    `Resource element (${resourceElement}) is ${hasResource ? "present" : "weak"}. `
    + `Learning capacity is ${hasResource ? "good" : "average"}.`;

  return {
    resource_element: resourceElement,
    output_element: outputElement,
    resource_score: 50.0,
    resource_change: 0.0,
    resource_seasonal_state: strength.seasonal_state,
    output_score: 50.0,
    output_change: 0.0,
    output_seasonal_state: strength.seasonal_state,
    daymaster_can_focus: strength.verdict !== "extremely_weak",
    daymaster_can_absorb: true,
    opportunities: [],
    blocks: [],
    outlook,
    breakthrough_likely: false,
    analysis_text: analysisText,
    pattern_engine: _buildPatternEngineStub([]),
  };
}


// =============================================================================
// TEN GODS DETAIL
// =============================================================================

function _buildTenGodsWarnings(
  tgEntries: TenGodEntry[],
  tgClassification: Record<string, Record<string, unknown>>,
  chart: ChartData,
): Array<Record<string, unknown>> {
  const warnings: Array<Record<string, unknown>> = [];

  const RISK_TEN_GODS: Record<string, Record<string, string>> = {
    "7K": {
      en: "Seven Killings prominent — aggressive energy, risk of conflicts",
      zh: "七殺旺 — 攻擊性強，易有衝突",
      id: "Tujuh Pembunuh menonjol — energi agresif, risiko konflik",
    },
    HO: {
      en: "Hurting Officer prominent — rebellious, challenges authority",
      zh: "傷官旺 — 叛逆，挑戰權威",
      id: "Hurting Officer menonjol — pemberontak, menantang otoritas",
    },
    RW: {
      en: "Rob Wealth present — wealth drained through others, competition",
      zh: "劫財現 — 財被他人所奪，競爭激烈",
      id: "Rob Wealth hadir — kekayaan terkuras oleh orang lain, persaingan",
    },
  };

  const seen = new Set<string>();
  for (const entry of tgEntries) {
    if (!entry.visible) continue;
    if (!(entry.abbreviation in RISK_TEN_GODS)) continue;
    const key = `${entry.abbreviation}|${entry.position}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const msgs = RISK_TEN_GODS[entry.abbreviation];
    const info = TEN_GOD_INFO[entry.abbreviation] ?? {};
    warnings.push({
      ten_god: entry.abbreviation,
      ten_god_chinese: info.chinese ?? entry.chinese,
      ten_god_english: info.english ?? entry.english,
      pillar: entry.position,
      message: msgs.en,
      message_chinese: msgs.zh,
      message_id: msgs.id,
    });
  }

  // Absent spouse star warning
  const spouse = checkSpouseStar(chart, tgClassification);
  if (spouse.is_critical_absent) {
    const starAbbr = spouse.star as string;
    const info = TEN_GOD_INFO[starAbbr] ?? {};
    warnings.push({
      ten_god: starAbbr,
      ten_god_chinese: info.chinese ?? "",
      ten_god_english: info.english ?? "",
      pillar: "day",
      message: `${info.english ?? starAbbr} (spouse star) absent from chart`,
      message_chinese: `${info.chinese ?? ""}（配偶星）不見於命盤`,
      message_id: `${info.english ?? starAbbr} (bintang pasangan) tidak ada dalam bagan`,
    });
  }

  // Absent children star warning
  const children = checkChildrenStar(chart, tgClassification);
  if (!children.any_present) {
    const starAbbr = children.primary_star as string;
    const info = TEN_GOD_INFO[starAbbr] ?? {};
    warnings.push({
      ten_god: starAbbr,
      ten_god_chinese: info.chinese ?? "",
      ten_god_english: info.english ?? "",
      pillar: "hour",
      message: "Children stars absent from chart",
      message_chinese: "子女星不見於命盤",
      message_id: "Bintang anak tidak ada dalam bagan",
    });
  }

  // Chart-level pattern warnings
  const patterns = analyzeTenGodPatterns(chart, tgClassification);
  const PATTERN_TO_TG: Record<string, string> = {
    companion_heavy: "RW",
    output_heavy: "HO",
    ho_prominent: "HO",
    "7k_prominent": "7K",
    rw_present: "RW",
    no_wealth: "DW",
    no_officer: "DO",
    no_resource: "DR",
  };
  const PATTERN_TO_PILLAR: Record<string, string> = {
    no_wealth: "day",
    no_officer: "month",
    no_resource: "month",
  };
  for (const p of patterns) {
    const tgAbbr = PATTERN_TO_TG[p.pattern as string];
    if (!tgAbbr) continue;
    const pillar = PATTERN_TO_PILLAR[p.pattern as string] ?? "day";
    const seenKey = `${tgAbbr}|${pillar}`;
    if (seen.has(seenKey)) continue;
    seen.add(seenKey);
    const info = TEN_GOD_INFO[tgAbbr] ?? {};
    warnings.push({
      ten_god: tgAbbr,
      ten_god_chinese: info.chinese ?? "",
      ten_god_english: info.english ?? "",
      pillar,
      message: p.description as string,
      message_chinese: p.description as string,
      message_id: p.description as string,
    });
  }

  return warnings;
}


function buildTenGodsDetail(
  tgEntries: TenGodEntry[],
  tgClassification: Record<string, Record<string, unknown>>,
  chart: ChartData,
): Record<string, unknown> {
  const dm = chart.day_master;
  const dmElement = STEMS[dm].element;

  const nodesAnalysis: Record<string, Record<string, unknown>> = {};
  for (const entry of tgEntries) {
    nodesAnalysis[entry.location] = {
      stem: entry.stem,
      ten_god: entry.abbreviation,
      ten_god_english: entry.english,
      ten_god_chinese: entry.chinese,
      visible: entry.visible,
      position: entry.position,
    };
  }

  const warnings = _buildTenGodsWarnings(tgEntries, tgClassification, chart);

  const summary: Record<string, string[]> = {
    wealth_nodes: [], resource_nodes: [], output_nodes: [],
    officer_nodes: [], companion_nodes: [],
  };
  for (const entry of tgEntries) {
    const info = TEN_GOD_INFO[entry.abbreviation];
    if (info) {
      const key = `${info.category}_nodes`;
      if (summary[key]) {
        summary[key].push(entry.location);
      }
    }
  }

  return {
    day_master: dm,
    day_master_element: dmElement,
    nodes: nodesAnalysis,
    summary,
    warnings,
    opportunities: [],
  };
}


// =============================================================================
// RECOMMENDATIONS
// =============================================================================

function buildRecommendations(
  predictions: Record<string, EventPrediction[]>,
  flags: Record<string, RedFlag[]>,
  strength: StrengthAssessment,
  env: EnvironmentAssessment,
): Array<Record<string, unknown>> {
  const recs: Array<Record<string, unknown>> = [];
  let order = 0;

  if (strength.useful_god) {
    const remedies = ELEMENT_REMEDIES[strength.useful_god] ?? { colors: [], direction: "" };
    const colors = remedies.colors.slice(0, 3).join(", ");
    const direction = remedies.direction ?? "";
    order += 1;
    recs.push({
      priority: "high",
      order,
      domain: "general",
      title: `Strengthen ${strength.useful_god} Element`,
      description:
        `Your useful god is ${strength.useful_god}. `
        + `Favorable elements: ${strength.favorable_elements.join(", ")}. `
        + `Wear colors: ${colors}. Direction: ${direction}.`,
    });
  }

  if (env.crosses_water_benefit) {
    order += 1;
    recs.push({
      priority: "medium",
      order,
      domain: "environment",
      title: "Consider Relocation Near Water",
      description: env.crosses_water_reason,
    });
  }

  for (const [area, areaFlags] of Object.entries(flags)) {
    if (areaFlags.length > 0) {
      const sevOrder: Record<string, number> = { mild: 0, moderate: 1, severe: 2, critical: 3 };
      const mostSevere = areaFlags.reduce((a, b) => (sevOrder[a.severity] ?? 0) >= (sevOrder[b.severity] ?? 0) ? a : b);
      const sev = mostSevere.severity;
      const priorityStr = (sev === "severe" || sev === "critical") ? "high" : sev === "moderate" ? "medium" : "low";
      order += 1;
      recs.push({
        priority: priorityStr,
        order,
        domain: area,
        title: `Address ${area.charAt(0).toUpperCase() + area.slice(1)} Concerns`,
        description: mostSevere.description,
      });
    }
  }

  return recs;
}


// =============================================================================
// NARRATIVE ANALYSIS (from WuxingResult.interactions)
// =============================================================================

/** Chinese names for wuxing interaction types */
const WUXING_CHINESE_NAMES: Record<string, string> = {
  PILLAR_PAIR: "柱内互动",
  THREE_MEETINGS: "三会",
  THREE_COMBOS: "三合",
  SIX_HARMONIES: "六合",
  HALF_MEETINGS: "半三会",
  ARCHED_COMBOS: "拱合",
  STEM_COMBOS: "天干五合",
  SIX_CLASH: "六冲",
  PUNISHMENT_SHI: "势刑",
  PUNISHMENT_EN: "恩刑",
  PUNISHMENT_SELF: "自刑",
  PUNISHMENT_WU_LI: "无礼刑",
  SIX_HARM: "六害",
  DESTRUCTION: "破",
  STEM_CLASH: "天干四冲",
  NATURAL_FLOW: "自然流转",
  SEASONAL: "令调",
};

/** English labels for wuxing interaction types */
const WUXING_ENGLISH_NAMES: Record<string, string> = {
  PILLAR_PAIR: "Pillar Pair",
  THREE_MEETINGS: "Three Meetings",
  THREE_COMBOS: "Three Combo",
  SIX_HARMONIES: "Six Harmony",
  HALF_MEETINGS: "Half Meeting",
  ARCHED_COMBOS: "Arched Combo",
  STEM_COMBOS: "Stem Combo",
  SIX_CLASH: "Six Clash",
  PUNISHMENT_SHI: "Punishment",
  PUNISHMENT_EN: "Punishment",
  PUNISHMENT_SELF: "Self Punishment",
  PUNISHMENT_WU_LI: "Punishment",
  SIX_HARM: "Six Harm",
  DESTRUCTION: "Destruction",
  STEM_CLASH: "Stem Clash",
  NATURAL_FLOW: "Natural Flow",
  SEASONAL: "Seasonal Adjustment",
};

/** Icon keys matching NarrativeCard's ICON_MAP */
const WUXING_ICON_MAP: Record<string, string> = {
  PILLAR_PAIR: "cross_pillar",
  THREE_MEETINGS: "meeting",
  THREE_COMBOS: "triangle",
  SIX_HARMONIES: "harmony",
  HALF_MEETINGS: "half_meeting",
  ARCHED_COMBOS: "arch",
  STEM_COMBOS: "stem_combo",
  SIX_CLASH: "clash",
  PUNISHMENT_SHI: "punishment",
  PUNISHMENT_EN: "punishment",
  PUNISHMENT_SELF: "punishment",
  PUNISHMENT_WU_LI: "punishment",
  SIX_HARM: "harm",
  DESTRUCTION: "destruction",
  STEM_CLASH: "stem_conflict",
  NATURAL_FLOW: "flow",
  SEASONAL: "season",
};

/** Determine polarity from step number */
function _wuxingPolarity(step: number): "positive" | "negative" | "neutral" {
  if (step <= 3) return "positive";
  if (step <= 5) return "negative";
  return "neutral";
}

/** Parse node ID like "YP.HS" or "MP.EB" into a pillar ref */
function _nodeIdToPillarRef(nodeId: string): Record<string, string> {
  const positionMap: Record<string, string> = {
    YP: "year",
    MP: "month",
    DP: "day",
    HP: "hour",
    LP: "luck",
  };
  const nodeTypeMap: Record<string, string> = {
    HS: "stem",
    EB: "branch",
  };

  const parts = nodeId.split(".");
  const pillarAbbrev = parts[0] ?? "";
  const nodeKind = parts[1] ?? "";

  const position = positionMap[pillarAbbrev] ?? "unknown";
  const nodeType = nodeTypeMap[nodeKind] ?? "hs";

  return {
    abbrev: nodeId,
    node_type: nodeType,
    position,
  };
}

/** Build pillar refs from an InteractionLog entry */
function _buildPillarRefs(log: InteractionLog): Array<Record<string, string>> {
  const refs: Array<Record<string, string>> = [];
  const seen = new Set<string>();

  const addRef = (nodeId: string) => {
    if (!seen.has(nodeId)) {
      seen.add(nodeId);
      refs.push(_nodeIdToPillarRef(nodeId));
    }
  };

  if (log.nodeA) addRef(log.nodeA);
  if (log.nodeB) addRef(log.nodeB);
  if (log.nodes) {
    for (const n of log.nodes) addRef(n);
  }

  return refs;
}

/** Build title string for a wuxing interaction log entry */
function _wuxingTitle(log: InteractionLog): string {
  const cn = WUXING_CHINESE_NAMES[log.type] ?? "";
  const en = WUXING_ENGLISH_NAMES[log.type] ?? log.type.replace(/_/g, " ");

  // For pillar pairs, include the relationship (盖头/截脚/生)
  if (log.type === "PILLAR_PAIR" && log.relationship) {
    return `${cn} ${log.relationship}`;
  }

  return `${cn} ${en}`;
}

/** Build the match string (branch names joined) */
function _wuxingMatch(log: InteractionLog): string | null {
  if (log.branches && log.branches.length > 0) {
    return log.branches.join(" + ");
  }
  return null;
}

/** Build math_formula showing gap multiplier if < 1 */
function _wuxingMathFormula(log: InteractionLog): string | null {
  const parts: string[] = [];
  if (log.gapMultiplier != null && log.gapMultiplier < 1) {
    parts.push(`gap\u00D7${log.gapMultiplier}`);
  }
  if (log.transformed) {
    parts.push("transformed \u00D72.5");
  }
  return parts.length > 0 ? parts.join(", ") : null;
}

function _palaceToPillarRef(palace: string): Record<string, string> {
  const posMap: Record<string, [string, string, string]> = {
    year: ["HS-Y", "hs", "year"],
    month: ["HS-M", "hs", "month"],
    day: ["HS-D", "hs", "day"],
    hour: ["HS-H", "hs", "hour"],
    luck: ["LP", "hs", "luck"],
    annual: ["YL", "hs", "annual"],
    monthly: ["ML", "hs", "monthly"],
    daily: ["DL", "hs", "daily"],
    hourly: ["HL", "hs", "hourly"],
  };
  const pLower = palace.toLowerCase();
  for (const [key, [abbrev, nodeType, position]] of Object.entries(posMap)) {
    if (pLower.includes(key)) {
      return { abbrev, node_type: nodeType, position };
    }
  }
  return { abbrev: palace.slice(0, 4), node_type: "hs", position: "unknown" };
}

function buildNarrativeAnalysis(
  interactions: BranchInteraction[],
  shenSha: ShenShaResult[],
  _tgEntries: TenGodEntry[],
  strength: StrengthAssessment,
  chart: ChartData,
  wuxingResult?: WuxingResult,
): Record<string, unknown> {
  const cards: Array<Record<string, unknown>> = [];
  let seq = 0;

  // --- Wuxing interaction log cards (preferred, chronological) ---
  if (wuxingResult && wuxingResult.interactions.length > 0) {
    // Sort by step first, then by original array order within each step
    const sorted = [...wuxingResult.interactions].sort((a, b) => a.step - b.step);

    for (const log of sorted) {
      // Skip Step 0 (initial assignment) — not a visible interaction
      if (log.step === 0) continue;

      // Skip logOnly entries (same-element clashes/destructions that don't change points)
      if (log.logOnly) continue;

      seq += 1;

      cards.push({
        seq,
        id: `wuxing_${seq}`,
        category: "wuxing",
        type: log.type.toLowerCase(),
        icon: WUXING_ICON_MAP[log.type] ?? "flow",
        title: _wuxingTitle(log),
        chinese_name: WUXING_CHINESE_NAMES[log.type] ?? log.type,
        polarity: _wuxingPolarity(log.step),
        element: log.resultElement ?? null,
        formula: log.details ?? null,
        match: _wuxingMatch(log),
        pillar_refs: _buildPillarRefs(log),
        points: log.basis != null ? `basis=${log.basis.toFixed(1)}` : null,
        math_formula: _wuxingMathFormula(log),
        severity: "moderate",
        priority: log.step,
      });
    }
  } else {
    // Fallback: build cards from old BranchInteraction[] if no wuxing result
    for (const inter of interactions) {
      seq += 1;
      const polarity = ["clash", "punishment", "self_punishment", "harm", "destruction"].includes(inter.interaction_type) ? "negative" : "positive";

      const branchesCn: string[] = [];
      for (const p of inter.palaces) {
        const pLower = p.toLowerCase();
        if (pLower.includes("year")) branchesCn.push(chart.pillars["year"].branch_chinese);
        else if (pLower.includes("month")) branchesCn.push(chart.pillars["month"].branch_chinese);
        else if (pLower.includes("day")) branchesCn.push(chart.pillars["day"].branch_chinese);
        else if (pLower.includes("hour")) branchesCn.push(chart.pillars["hour"].branch_chinese);
        else if (pLower.includes("luck") && chart.luck_pillar) branchesCn.push(chart.luck_pillar.branch_chinese);
      }

      let element: string | null = null;
      for (const el of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
        if (inter.description.includes(el)) {
          element = el;
          break;
        }
      }

      cards.push({
        seq,
        id: `narrative_${seq}`,
        category: "interaction",
        type: inter.interaction_type,
        icon: inter.interaction_type,
        title: inter.chinese_name || inter.interaction_type,
        chinese_name: inter.chinese_name,
        polarity,
        element,
        formula: inter.description,
        match: branchesCn.length > 0 ? branchesCn.join(" + ") : null,
        description: inter.description,
        palaces: inter.palaces,
        pillar_refs: inter.palaces.map(p => _palaceToPillarRef(p)),
        severity: inter.severity,
        priority: inter.severity === "severe" ? 3 : inter.severity === "moderate" ? 2 : 1,
      });
    }
  }

  // --- Shen Sha cards (SEPARATE from wuxing interactions) ---
  const shenShaCards: Array<Record<string, unknown>> = [];
  let shenSeq = 0;
  for (const s of shenSha) {
    if (!s.present) continue;
    shenSeq += 1;
    const polarity = s.nature === "auspicious" ? "positive" : s.nature === "inauspicious" ? "negative" : "neutral";
    shenShaCards.push({
      seq: shenSeq,
      id: `shensha_${shenSeq}`,
      category: "shen_sha",
      type: s.name_english ? s.name_english.toLowerCase().replace(/ /g, "_") : "star",
      icon: "flow",
      title: `${s.name_chinese} ${s.name_english}`,
      chinese_name: s.name_chinese,
      polarity,
      element: null,
      formula: s.derivation ?? null,
      match: s.palace ?? null,
      description: s.impact || `${s.name_english} present in ${s.palace ?? "chart"}`,
      palaces: s.palace ? [s.palace] : [],
      pillar_refs: s.palace ? [_palaceToPillarRef(s.palace)] : [],
      severity: s.severity,
      priority: 1,
    });
  }

  // Chronological order: by step (priority field), then by seq within step
  cards.sort((a, b) => {
    const pDiff = (a.priority as number) - (b.priority as number);
    if (pDiff !== 0) return pDiff;
    return (a.seq as number) - (b.seq as number);
  });

  // Re-assign seq after sorting
  for (let i = 0; i < cards.length; i++) {
    cards[i].seq = i + 1;
  }

  return {
    all_chronological: cards,  // wuxing only (no shen sha)
    shen_sha_cards: shenShaCards,  // separate section
    narratives: cards.slice(0, 15),
    narratives_by_category: {
      wuxing: cards.filter(c => c.category === "wuxing"),
      interaction: cards.filter(c => c.category === "interaction"),
      shen_sha: shenShaCards,
    },
    element_context: {
      daymaster: chart.day_master,
      daymaster_element: chart.dm_element,
      strength: strength.verdict,
    },
    remedies: [],
    quick_remedies: [],
  };
}


// =============================================================================
// MAPPINGS (static reference data for frontend)
// =============================================================================

function buildMappings(): Record<string, unknown> {
  const heavenlyStems: Record<string, Record<string, unknown>> = {};
  for (const [stemId, stemData] of Object.entries(STEMS)) {
    heavenlyStems[stemId] = {
      id: stemId,
      pinyin: stemId,
      chinese: stemData.chinese,
      english: stemId,
      hex_color: stemData.color,
    };
  }

  const earthlyBranches: Record<string, Record<string, unknown>> = {};
  for (const [branchId, branchData] of Object.entries(BRANCHES)) {
    earthlyBranches[branchId] = {
      id: branchId,
      chinese: branchData.chinese,
      animal: branchData.animal,
      hex_color: branchData.color,
      qi: branchData.qi.map(([qiStem, qiScore]) => ({
        stem: qiStem,
        score: qiScore,
        stem_chinese: STEMS[qiStem]?.chinese ?? "?",
        element: STEMS[qiStem]?.element ?? "?",
        polarity: STEMS[qiStem]?.polarity ?? "?",
        hex_color: STEMS[qiStem]?.color ?? "#ccc",
      })),
    };
  }

  return {
    heavenly_stems: heavenlyStems,
    earthly_branches: earthlyBranches,
    ten_gods: TEN_GODS,
    event_types: {
      registration: { hex_color: "#60a5fa", icon: "", label: "Registration" },
      seasonal: { hex_color: "#fbbf24", icon: "", label: "Seasonal" },
      controlling: { hex_color: "#f87171", icon: "", label: "Controlling" },
      controlled: { hex_color: "#f87171", icon: "", label: "Controlled" },
      control: { hex_color: "#f87171", icon: "", label: "Control" },
      producing: { hex_color: "#4ade80", icon: "", label: "Producing" },
      produced: { hex_color: "#4ade80", icon: "", label: "Produced" },
      generation: { hex_color: "#4ade80", icon: "", label: "Generation" },
      combination: { hex_color: "#c084fc", icon: "", label: "Combination" },
      conflict: { hex_color: "#fb923c", icon: "", label: "Conflict" },
      conflict_aggressor: { hex_color: "#fb923c", icon: "", label: "Conflict" },
      conflict_victim: { hex_color: "#fb923c", icon: "", label: "Conflict" },
      same_element: { hex_color: "#2dd4bf", icon: "", label: "Same Element" },
    },
    ten_gods_styling: {
      DM: { hex_color: "#9333ea", bg_hex: "#f3e8ff", label: "Day Master" },
      F: { hex_color: "#2563eb", bg_hex: "#dbeafe", label: "Friend" },
      RW: { hex_color: "#3b82f6", bg_hex: "#eff6ff", label: "Rob Wealth" },
      EG: { hex_color: "#16a34a", bg_hex: "#dcfce7", label: "Eating God" },
      HO: { hex_color: "#22c55e", bg_hex: "#f0fdf4", label: "Hurting Officer" },
      IW: { hex_color: "#ca8a04", bg_hex: "#fef9c3", label: "Indirect Wealth" },
      DW: { hex_color: "#eab308", bg_hex: "#fefce8", label: "Direct Wealth" },
      "7K": { hex_color: "#dc2626", bg_hex: "#fee2e2", label: "Seven Killings" },
      DO: { hex_color: "#ef4444", bg_hex: "#fef2f2", label: "Direct Officer" },
      IR: { hex_color: "#4b5563", bg_hex: "#f3f4f6", label: "Indirect Resource" },
      DR: { hex_color: "#6b7280", bg_hex: "#f9fafb", label: "Direct Resource" },
    },
    elements: {
      Wood: { hex_color: "#22c55e", hex_color_yang: "#16a34a", hex_color_yin: "#4ade80" },
      Fire: { hex_color: "#ef4444", hex_color_yang: "#dc2626", hex_color_yin: "#f87171" },
      Earth: { hex_color: "#ca8a04", hex_color_yang: "#a16207", hex_color_yin: "#eab308" },
      Metal: { hex_color: "#6b7280", hex_color_yang: "#4b5563", hex_color_yin: "#9ca3af" },
      Water: { hex_color: "#3b82f6", hex_color_yang: "#2563eb", hex_color_yin: "#60a5fa" },
    },
  };
}


// =============================================================================
// CLIENT SUMMARY
// =============================================================================

function _summaryChartOverview(chart: ChartData): Record<string, unknown> {
  const dmInfo = STEMS[chart.day_master];
  const key = `${dmInfo.element}|${dmInfo.polarity}`;
  const nature = DM_NATURE[key];
  const items = [
    { label: "Day Master", value: `${nature?.name ?? chart.day_master} (${nature?.chinese ?? dmInfo.chinese}) — ${_pick(nature?.nature ?? [""])}` },
    { label: "Personality", value: nature?.personality ?? "" },
  ];
  return { id: "chart_overview", title: "Your Chart", title_zh: "命盤概覽", items };
}

function _summaryStrength(strength: StrengthAssessment, chart: ChartData): Record<string, unknown> {
  const text = _pick(STRENGTH_VERDICTS[strength.verdict] ?? ["No assessment available."]);
  const dmElement = chart.dm_element;
  const dmName = `${chart.day_master} ${dmElement}`;
  const resource = ELEMENT_CYCLES.generated_by[dmElement] ?? "";
  const output = ELEMENT_CYCLES.generating[dmElement] ?? "";
  const wealth = ELEMENT_CYCLES.controlling[dmElement] ?? "";
  const officer = ELEMENT_CYCLES.controlled_by[dmElement] ?? "";

  let roleMap: Record<string, string>;
  if (strength.verdict === "weak" || strength.verdict === "extremely_weak") {
    roleMap = {
      [dmElement]: "companion — strengthens you",
      [resource]: `resource — generates your ${dmElement}`,
      [output]: `output — exhausts your weak ${dmElement}`,
      [wealth]: `wealth — drains your weak ${dmElement}`,
      [officer]: `officer — attacks/controls ${dmElement}`,
    };
  } else if (strength.verdict === "strong" || strength.verdict === "extremely_strong") {
    roleMap = {
      [dmElement]: "companion — overloads the chart",
      [resource]: `resource — fuels already excessive ${dmElement}`,
      [output]: "output — channels excess energy",
      [wealth]: "wealth — absorbs your strength",
      [officer]: "officer — disciplines your energy",
    };
  } else {
    roleMap = {
      [dmElement]: "companion",
      [resource]: `resource — generates ${dmElement}`,
      [output]: "output — channels energy",
      [wealth]: "wealth — productive use of strength",
      [officer]: "officer — can tip balance",
    };
  }

  const items: Array<Record<string, unknown>> = [
    { label: "Score", value: `${strength.score}% (20% = balanced)` },
  ];

  const ug = strength.useful_god;
  const ugPct = strength.element_percentages[ug] ?? 0;
  items.push({ label: "Useful God", value: `${ug} — most deficient at ${ugPct}% — adding it brings the chart closest to balance` });

  const favExplained = strength.favorable_elements.map(elem => {
    const role = roleMap[elem] ?? "";
    return role ? `${elem} (${role})` : elem;
  });
  items.push({ label: "Favorable", value: favExplained.join(", ") });

  const unfavExplained = strength.unfavorable_elements.map(elem => {
    const role = roleMap[elem] ?? "";
    return role ? `${elem} (${role})` : elem;
  });
  items.push({ label: "Unfavorable", value: unfavExplained.join(", ") });

  if (strength.best_element_pairs && strength.best_element_pairs.length > 0) {
    const pairParts = strength.best_element_pairs.slice(0, 3).map(p => (p.elements as string[]).join("+"));
    items.push({ label: "Best Luck Combos", value: pairParts.join(", ") });
  }

  const verdictKey = strength.verdict in STRENGTH_EXPLANATION ? strength.verdict : "neutral";
  const explanation = STRENGTH_EXPLANATION[verdictKey]
    .replace(/\{dm_name\}/g, dmName)
    .replace(/\{dm_element\}/g, dmElement)
    .replace(/\{score\}/g, String(strength.score))
    .replace(/\{resource\}/g, resource)
    .replace(/\{output\}/g, output)
    .replace(/\{wealth\}/g, wealth)
    .replace(/\{officer\}/g, officer)
    .replace(/\{useful_god\}/g, strength.useful_god)
    .replace(/\{unfav_list\}/g, strength.unfavorable_elements.join(", "));
  items.push({ label: "Why?", value: explanation });

  const severity = (strength.verdict === "strong" || strength.verdict === "extremely_strong")
    ? "strong"
    : (strength.verdict === "weak" || strength.verdict === "extremely_weak") ? "weak" : "neutral";

  return { id: "strength", title: "Strength Assessment", title_zh: "日主強弱", severity, text, items };
}

function _summaryTenGods(chart: ChartData, tgClassification: Record<string, Record<string, unknown>>): Record<string, unknown> {
  const items: Array<Record<string, unknown>> = [];
  const dominant: string[] = [];
  for (const [abbr, info] of Object.entries(tgClassification)) {
    const strengthLevel = (info.strength as string) ?? "ABSENT";
    const templates = TEN_GOD_INTERPRETATIONS[abbr] ?? {};
    let textVal = _pick(templates[strengthLevel] ?? templates.PRESENT ?? [""]);
    if (!textVal) textVal = `${info.english ?? abbr} (${info.chinese ?? ""}) is ${strengthLevel}`;
    let severity: string | undefined;
    if (strengthLevel === "PROMINENT" && ["7K", "HO", "RW"].includes(abbr)) severity = "warning";
    else if (strengthLevel === "PROMINENT") severity = "info";
    else if (strengthLevel === "ABSENT" && ["DW", "DO"].includes(abbr)) severity = "alert";
    const item: Record<string, unknown> = { label: `${abbr} (${info.chinese ?? ""})`, value: textVal };
    if (severity) item.severity = severity;
    items.push(item);
    if (strengthLevel === "PROMINENT") dominant.push((info.english as string) ?? abbr);
  }
  const text = dominant.length > 0 ? `Dominant: ${dominant.join(", ")}` : "No dominant ten gods";
  return { id: "ten_gods", title: "Ten Gods Profile", title_zh: "十神分析", text, items };
}

function _summaryInteractions(interactions: BranchInteraction[]): Record<string, unknown> {
  const positiveTypes = new Set(["harmony", "three_harmony", "half_three_harmony", "directional_combo"]);
  const posCount = interactions.filter(i => positiveTypes.has(i.interaction_type)).length;
  const negCount = interactions.length - posCount;
  const items: Array<Record<string, unknown>> = [];
  for (const inter of interactions.slice(0, 8)) {
    const polarity = positiveTypes.has(inter.interaction_type) ? "positive" : "negative";
    const severity = polarity === "positive" ? "positive" : inter.severity;
    const palacesStr = inter.palaces.join(" vs ");
    items.push({
      label: `${inter.chinese_name} ${inter.interaction_type.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}`,
      value: palacesStr ? `${palacesStr} — ${inter.description}` : inter.description,
      severity,
    });
  }
  return { id: "interactions", title: "Branch Interactions", title_zh: "地支關係", text: `${posCount} positive, ${negCount} negative interactions found`, items };
}

function _summaryShenSha(shenSha: ShenShaResult[]): Record<string, unknown> {
  const items: Array<Record<string, unknown>> = [];
  for (const s of shenSha) {
    if (!s.present) continue;
    const templates = SHEN_SHA_IMPACTS[s.name_chinese] ?? {};
    const text = _pick(templates.present ?? [`${s.name_english} present`]);
    const severity = s.nature === "auspicious" ? "positive" : s.nature === "inauspicious" ? "negative" : "info";
    items.push({ label: `${s.name_chinese} ${s.name_english}`, value: text, severity });
  }
  return { id: "shen_sha", title: "Special Stars", title_zh: "神煞", items };
}

function _summaryRedFlags(flags: Record<string, RedFlag[]>): Record<string, unknown> {
  const items: Array<Record<string, unknown>> = [];
  for (const [area, areaFlags] of Object.entries(flags)) {
    for (const f of areaFlags) {
      items.push({ label: area.charAt(0).toUpperCase() + area.slice(1), value: `${f.indicator_name} — ${f.description}`, severity: f.severity });
    }
  }
  return { id: "red_flags", title: "Red Flags", title_zh: "警示", items };
}

function _summaryLuckPillar(chart: ChartData, strength: StrengthAssessment): Record<string, unknown> | null {
  if (!chart.luck_pillar) return null;
  const lp = chart.luck_pillar;
  const tg = getTenGod(chart.day_master, lp.stem);
  const tgLabel = tg ? `${tg[1]} (${tg[2]})` : "";
  const text = `${lp.stem_chinese}${lp.branch_chinese} (${lp.stem} ${lp.branch}) — ${tgLabel} decade`;
  return { id: "luck_pillar", title: "Current Luck Pillar", title_zh: "大運分析", text };
}

function _summaryHealth(chart: ChartData, strength: StrengthAssessment, elemCounts?: Record<string, number>): Record<string, unknown> {
  // With wuxing percentages, values are already in percent (avg=20)
  if (!elemCounts) {
    const wr = calculateWuxing(chartToWuxingInput(chart));
    elemCounts = wuxingToElementCounts(wr);
  }
  const total = Object.values(elemCounts).reduce((a, b) => a + b, 0);
  const avg = total > 0 ? total / 5 : 20;

  const monthBranch = chart.pillars["month"].branch;
  const seasonalStates = (BRANCHES[monthBranch] as Record<string, unknown>).element_states as Record<string, string> ?? {};

  const ELEMENT_CONTROLS_MAP: Record<string, string> = {
    Wood: "Earth", Fire: "Metal", Earth: "Water", Metal: "Wood", Water: "Fire",
  };
  const controlImbalances: Record<string, Record<string, unknown>> = {};
  for (const [controller, controlled] of Object.entries(ELEMENT_CONTROLS_MAP)) {
    const controllerState = seasonalStates[controller] ?? "Resting";
    const controllerCount = elemCounts[controller] ?? 0;
    if (controllerState === "Dead" || controllerState === "Trapped" || controllerCount < avg * 0.3) {
      controlImbalances[controlled] = { controller, controller_state: controllerState, controller_count: controllerCount };
    }
  }

  const items: Array<Record<string, unknown>> = [];

  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const count = elemCounts[elem] ?? 0;
    const pct = count; // Already in percentage
    const organInfo = HEALTH_ELEMENT_MAP[elem];
    const yinOrgan = organInfo.yin_organ;
    const bodyParts = organInfo.body_parts;
    const seasonalState = seasonalStates[elem] ?? "Resting";

    const reasons: string[] = [];
    let severity: string | null = null;

    // Layer 1: Element balance
    if (count < avg * 0.5) {
      reasons.push(`${elem} severely deficient (${Math.round(pct)}%). ${organInfo.deficiency}`);
      severity = "warning";
    } else if (count < avg * 0.75) {
      reasons.push(`${elem} below average (${Math.round(pct)}%). Mild ${yinOrgan.split("(")[0].trim().toLowerCase()} vulnerability`);
      severity = "mild";
    } else if (count > avg * 1.8) {
      reasons.push(`${elem} in excess (${Math.round(pct)}%). ${organInfo.excess}`);
      severity = "warning";
    } else if (count > avg * 1.4) {
      reasons.push(`${elem} above average (${Math.round(pct)}%). Watch for: ${organInfo.excess}`);
      severity = "mild";
    }

    // Layer 2: Seasonal vulnerability
    if (seasonalState === "Dead" || seasonalState === "Trapped") {
      const stateLabel = seasonalState === "Dead" ? "Dead (死)" : "Trapped (囚)";
      reasons.push(`${elem} in ${stateLabel} seasonal state — heightened ${yinOrgan.split("(")[0].trim().toLowerCase()} vulnerability`);
      if (!severity) severity = "mild";
      else if (severity === "mild") severity = "warning";
    }

    // Layer 3: Control cycle imbalance
    if (elem in controlImbalances) {
      const imb = controlImbalances[elem];
      const ctrl = imb.controller as string;
      const explanation = CONTROL_CYCLE_EXPLANATIONS[`${ctrl}|${elem}`];
      if (explanation) {
        reasons.push(explanation);
      } else {
        reasons.push(`${ctrl} is too weak to control ${elem} — ${yinOrgan.split("(")[0].trim().toLowerCase()} system unregulated`);
      }
      if (!severity) severity = "mild";
      else if (severity === "mild") severity = "warning";
    }

    if (reasons.length > 0) {
      items.push({
        label: `${yinOrgan} (${elem})`,
        value: `${reasons.join(". ")}. Body parts: ${bodyParts}.`,
        severity: severity ?? "info",
      });
    }
  }

  if (items.length === 0) {
    items.push({ label: "Overall", value: "Element balance is healthy. No significant organ system vulnerabilities detected.", severity: "positive" });
  }

  return { id: "health", title: "Health", title_zh: "健康", items };
}

function _summaryRemedies(strength: StrengthAssessment, chart: ChartData, elemCounts?: Record<string, number>): Record<string, unknown> {
  const useful = strength.useful_god;
  const remedies = ELEMENT_REMEDIES[useful];
  const items: Array<Record<string, unknown>> = [];

  if (remedies) {
    items.push({ label: "Colors", value: `Wear ${remedies.colors.join(", ")} (${useful} element)` });
    items.push({ label: "Direction", value: remedies.direction });
    items.push({ label: "Industries", value: remedies.industries.slice(0, 5).join(", ") });
    const avoid = remedies.avoid_colors.join(", ");
    if (avoid) items.push({ label: "Avoid Colors", value: avoid });
  }

  // Use wuxing-based element percentages (avg=20)
  if (!elemCounts) {
    const wr = calculateWuxing(chartToWuxingInput(chart));
    elemCounts = wuxingToElementCounts(wr);
  }
  const avgCount = 20; // wuxing percentages average to 20

  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const count = elemCounts[elem] ?? 0;
    if (count < avgCount * 0.5) {
      const elemRemedies = ELEMENT_REMEDIES[elem];
      const organ = HEALTH_ELEMENT_MAP[elem].yin_organ.split("(")[0].trim();
      const behavioral = HEALTH_BEHAVIORAL_REMEDIES[elem] ?? "";
      if (elem === useful) {
        items.push({ label: `Health + Useful God synergy (${elem})`, value: `Your useful god (${useful}) also addresses your ${organ.toLowerCase()} health. ${behavioral}`, severity: "positive" });
      } else {
        const elemColors = elemRemedies ? elemRemedies.colors.slice(0, 2).join(", ") : "";
        items.push({ label: `Health: ${organ} (${elem})`, value: `Low ${elem} weakens ${organ.toLowerCase()}. Secondary remedy: add ${elemColors} accessories. ${behavioral}`, severity: "info" });
      }
    }
  }

  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const count = elemCounts[elem] ?? 0;
    if (count > avgCount * 1.8) {
      const organ = HEALTH_ELEMENT_MAP[elem].yin_organ.split("(")[0].trim();
      const behavioral = HEALTH_BEHAVIORAL_REMEDIES[elem] ?? "";
      items.push({ label: `Health: ${organ} excess (${elem})`, value: `High ${elem} overloads ${organ.toLowerCase()}. Reduce ${elem} element exposure. ${behavioral}`, severity: "warning" });
    }
  }

  return { id: "remedies", title: "Remedies", title_zh: "化解建議", items };
}

// The second (overriding) version of _summaryPredictionsTimeline
function _summaryPredictionsTimeline(predictions: Record<string, EventPrediction[]>): Record<string, unknown> | null {
  const items: Array<Record<string, unknown>> = [];
  for (const [eventType, events] of Object.entries(predictions)) {
    for (const ev of events.slice(0, 2)) {
      const factorsStr = ev.factors.slice(0, 2).join("; ");
      items.push({ label: eventType.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()), value: `Year ${ev.year} (age ${ev.age}) — score ${ev.score.toFixed(0)}. ${factorsStr}` });
    }
  }
  if (items.length === 0) return null;
  return { id: "predictions", title: "Year Predictions", title_zh: "流年預測", items: items.slice(0, 8) };
}

function _summaryNatalPredictions(
  chart: ChartData,
  tgClassification: Record<string, Record<string, unknown>>,
  strength: StrengthAssessment,
  predictions: Record<string, EventPrediction[]>,
  flags: Record<string, RedFlag[]>,
): Record<string, unknown> {
  const items: Array<Record<string, unknown>> = [];

  // --- MARRIAGE ---
  const spouse = checkSpouseStar(chart, tgClassification);
  const spouseStrength = spouse.strength as string;
  const spouseLabel = spouse.label as string;

  const rwStrength = (tgClassification.RW?.strength as string) ?? "ABSENT";
  const hoStrength = (tgClassification.HO?.strength as string) ?? "ABSENT";

  const marriageReasons: string[] = [];
  let marriageOutlook: string;
  let severity: string;

  if (spouseStrength === "ABSENT") {
    marriageOutlook = "DIFFICULT";
    marriageReasons.push(`${spouseLabel} completely absent from natal chart`);
    severity = "severe";
  } else if (spouseStrength === "HIDDEN_ONLY") {
    marriageOutlook = "LATE";
    marriageReasons.push(`${spouseLabel} only in hidden stems — marriage comes late or needs effort`);
    severity = "warning";
  } else if (spouseStrength === "PROMINENT") {
    marriageOutlook = "STRONG";
    marriageReasons.push(`${spouseLabel} is prominent — strong marriage affinity`);
    severity = "positive";
  } else {
    marriageOutlook = "NORMAL";
    marriageReasons.push(`${spouseLabel} is present — marriage attainable`);
    severity = "info";
  }

  if (hoStrength === "PROMINENT" && chart.gender === "female") {
    marriageReasons.push("Hurting Officer prominent — conflicts with husband star");
    if (marriageOutlook !== "DIFFICULT") { marriageOutlook = "CHALLENGING"; severity = "warning"; }
  }
  if (rwStrength === "PROMINENT") {
    marriageReasons.push("Rob Wealth prominent — competition/interference in relationships");
    if (marriageOutlook === "NORMAL" || marriageOutlook === "STRONG") { marriageOutlook = "CHALLENGING"; severity = "warning"; }
  }

  for (const mf of (flags.marriage ?? []).slice(0, 2)) {
    marriageReasons.push(mf.description);
  }

  const marriagePreds = predictions.marriage ?? [];
  if (marriagePreds.length > 0) {
    const top = marriagePreds[0];
    marriageReasons.push(`Best year: ${top.year} (age ${top.age}, score ${top.score.toFixed(0)}) — ${top.factors.slice(0, 2).join("; ")}`);
  }

  items.push({ label: `Marriage: ${marriageOutlook}`, value: marriageReasons.join(" | "), severity });

  // --- DIVORCE RISK ---
  const divorceReasons: string[] = [];
  let divorceRisk: string;

  let dayBranchClashed = false;
  for (const interFlag of (flags.marriage ?? [])) {
    if (interFlag.indicator_name.toLowerCase().includes("clash") || interFlag.indicator_name.includes("冲")) {
      dayBranchClashed = true;
      break;
    }
  }

  if (spouseStrength === "ABSENT" && (rwStrength === "PROMINENT" || rwStrength === "PRESENT")) {
    divorceRisk = "HIGH";
    divorceReasons.push("No spouse star + Rob Wealth present = partner drained away");
    severity = "severe";
  } else if (dayBranchClashed && (hoStrength === "PROMINENT" || hoStrength === "PRESENT")) {
    divorceRisk = "ELEVATED";
    divorceReasons.push("Spouse palace clashed + Hurting Officer = marriage instability");
    severity = "warning";
  } else if (dayBranchClashed) {
    divorceRisk = "MODERATE";
    divorceReasons.push("Spouse palace has clash — periodic marriage tension");
    severity = "warning";
  } else if (hoStrength === "PROMINENT") {
    divorceRisk = "MODERATE";
    divorceReasons.push("Prominent Hurting Officer — sharp tongue damages relationships");
    severity = "warning";
  } else {
    divorceRisk = "LOW";
    divorceReasons.push("No major divorce indicators in natal chart");
    severity = "positive";
  }

  const divorcePreds = predictions.divorce ?? [];
  if (divorcePreds.length > 0 && divorcePreds[0].score >= 40) {
    const top = divorcePreds[0];
    divorceReasons.push(`Highest risk year: ${top.year} (age ${top.age}, score ${top.score.toFixed(0)}) — ${top.factors.slice(0, 2).join("; ")}`);
  }

  items.push({ label: `Divorce Risk: ${divorceRisk}`, value: divorceReasons.join(" | "), severity });

  // --- CHILDREN ---
  const children = checkChildrenStar(chart, tgClassification);
  const childReasons: string[] = [];
  const primaryStar = children.primary_star as string;
  const secondaryStar = children.secondary_star as string;
  const pStrength = children.primary_strength as string;
  const sStrength = children.secondary_strength as string;

  let childCountEst = 0;
  let sonsLabel: string, daughtersLabel: string;
  if (chart.gender === "male") {
    sonsLabel = `7K (${tgClassification["7K"]?.chinese ?? "七殺"})`;
    daughtersLabel = `DO (${tgClassification.DO?.chinese ?? "正官"})`;
  } else {
    sonsLabel = `HO (${tgClassification.HO?.chinese ?? "傷官"})`;
    daughtersLabel = `EG (${tgClassification.EG?.chinese ?? "食神"})`;
  }

  if (pStrength === "PROMINENT") { childReasons.push(`${sonsLabel} is prominent — likely multiple sons`); childCountEst += 2; }
  else if (pStrength === "PRESENT" || pStrength === "HIDDEN_ONLY") { childReasons.push(`${sonsLabel} present — sons likely`); childCountEst += 1; }
  else childReasons.push(`${sonsLabel} absent — sons less likely naturally`);

  if (sStrength === "PROMINENT") { childReasons.push(`${daughtersLabel} is prominent — likely multiple daughters`); childCountEst += 2; }
  else if (sStrength === "PRESENT" || sStrength === "HIDDEN_ONLY") { childReasons.push(`${daughtersLabel} present — daughters likely`); childCountEst += 1; }
  else childReasons.push(`${daughtersLabel} absent — daughters less likely naturally`);

  const hourBranch = chart.pillars["hour"].branch;
  const hourQi = getAllBranchQi(hourBranch);
  let hourHasChildStar = false;
  for (const [hs] of hourQi) {
    const tg = getTenGod(chart.day_master, hs as StemName);
    if (tg && (tg[0] === primaryStar || tg[0] === secondaryStar)) { hourHasChildStar = true; break; }
  }
  childReasons.push(hourHasChildStar
    ? "Children star in hour pillar (children palace) — strong fertility indicator"
    : "No children star in hour pillar — may need more effort");

  const estLabel = childCountEst > 0 ? `${childCountEst}+` : "uncertain";
  severity = childCountEst >= 2 ? "positive" : childCountEst === 1 ? "info" : "warning";

  const childPreds = predictions.children ?? [];
  if (childPreds.length > 0) {
    childReasons.push(`Best year: ${childPreds[0].year} (age ${childPreds[0].age})`);
  }

  items.push({ label: `Children: est. ${estLabel}`, value: childReasons.join(" | "), severity });

  // --- WEALTH POTENTIAL ---
  const dwStrength = (tgClassification.DW?.strength as string) ?? "ABSENT";
  const iwStrength = (tgClassification.IW?.strength as string) ?? "ABSENT";
  const egStrength = (tgClassification.EG?.strength as string) ?? "ABSENT";

  const wealthReasons: string[] = [];
  const dmElement = chart.dm_element;
  const hasDW = dwStrength !== "ABSENT";
  const hasIW = iwStrength !== "ABSENT";
  const canHandle = strength.verdict !== "extremely_weak";
  const isStrongDm = strength.verdict === "strong" || strength.verdict === "extremely_strong";

  let wealthScore = 0;
  if (hasDW) { wealthScore += 2; wealthReasons.push("Direct Wealth present — steady income capacity"); }
  if (hasIW) { wealthScore += 2; wealthReasons.push("Indirect Wealth present — windfall/investment capacity"); }
  if (iwStrength === "PROMINENT") { wealthScore += 2; wealthReasons.push("Prominent Indirect Wealth — strong speculative/business luck"); }
  if (dwStrength === "PROMINENT") { wealthScore += 1; wealthReasons.push("Prominent Direct Wealth — strong salary/stable income"); }
  if (isStrongDm && (hasDW || hasIW)) { wealthScore += 2; wealthReasons.push("Strong DM can hold wealth — good earning capacity"); }
  else if (!canHandle) { wealthScore -= 2; wealthReasons.push("Extremely weak DM — struggles to hold onto wealth"); }
  if (egStrength === "PROMINENT") { wealthScore += 1; wealthReasons.push("Eating God prominent — wealth through creativity/talent"); }
  if (rwStrength === "PROMINENT") { wealthScore -= 2; wealthReasons.push("Rob Wealth prominent — money drains through competition/others"); }

  for (const wf of (flags.wealth ?? []).slice(0, 2)) {
    wealthReasons.push(`Warning: ${wf.description}`);
    wealthScore -= 1;
  }

  let wealthTier: string, tierDetail: string;
  if (wealthScore >= 6) {
    wealthTier = "8-9 figures possible"; tierDetail = "Strong wealth indicators — 8-figure potential with right timing. 9-figure if Indirect Wealth is prominent + strong DM."; severity = "positive";
  } else if (wealthScore >= 4) {
    wealthTier = "7-8 figures possible"; tierDetail = "Good wealth capacity — 7-figure achievable. 8-figure possible in favorable luck decades."; severity = "positive";
  } else if (wealthScore >= 2) {
    wealthTier = "7 figures possible"; tierDetail = "Moderate wealth indicators — comfortable living, 7-figure achievable with effort."; severity = "info";
  } else if (wealthScore >= 0) {
    wealthTier = "6-7 figures"; tierDetail = "Average wealth capacity — steady income but unlikely to break into high wealth without favorable luck."; severity = "info";
  } else {
    wealthTier = "Wealth challenged"; tierDetail = "Wealth stars weak or drained — financial stability requires careful management and favorable timing."; severity = "warning";
  }
  wealthReasons.push(tierDetail);

  const careerPreds = predictions.career ?? [];
  if (careerPreds.length > 0) wealthReasons.push(`Best career year: ${careerPreds[0].year} (age ${careerPreds[0].age})`);

  items.push({ label: `Wealth: ${wealthTier}`, value: wealthReasons.join(" | "), severity });

  return {
    id: "natal_predictions", title: "Life Predictions", title_zh: "命理預測",
    text: "Based on natal chart structure — what your birth chart says about marriage, children, and wealth potential",
    items,
  };
}

function _summaryHonest(
  chart: ChartData, strength: StrengthAssessment,
  tgClassification: Record<string, Record<string, unknown>>,
  flags: Record<string, RedFlag[]>,
  elemCounts?: Record<string, number>,
): Record<string, unknown> {
  const dmElement = chart.dm_element;
  const dmInfo = STEMS[chart.day_master];
  const dmKey = `${dmInfo.element}|${dmInfo.polarity}`;
  const nature = DM_NATURE[dmKey];

  let key: string;
  if (strength.is_following_chart) key = "following";
  else if (strength.verdict === "weak" || strength.verdict === "extremely_weak") key = `weak_${dmElement.toLowerCase()}`;
  else key = "strong_general";
  const lifeLesson = _pick(LIFE_LESSON_TEMPLATES[key] ?? LIFE_LESSON_TEMPLATES.strong_general ?? [""]);

  const parts: string[] = [];

  parts.push(`You are ${nature?.name ?? chart.day_master} (${nature?.chinese ?? dmInfo.chinese}). Personality: ${nature?.personality ?? "unknown"}.`);

  const score = strength.score;
  if (score < 10) parts.push(`Your Day Master is extremely weak (${score.toFixed(0)}% element presence, 20% = balanced). You are easily overwhelmed by life's demands. Your biggest challenge is finding support systems and environments that sustain you.`);
  else if (score < 16) parts.push(`Your Day Master is weak (${score.toFixed(0)}% element presence, 20% = balanced). You need more support than most people. Resource and companion elements are your lifeline.`);
  else if (score < 24) parts.push(`Your Day Master is balanced (${score.toFixed(0)}% element presence, 20% = balanced). You have a flexible chart — small shifts in luck pillars have outsized effects on your life.`);
  else if (score < 30) parts.push(`Your Day Master is strong (${score.toFixed(0)}% element presence, 20% = balanced). You have abundant energy but need productive outlets. Without channels for your strength, you become restless and domineering.`);
  else parts.push(`Your Day Master is extremely strong (${score.toFixed(0)}% element presence, 20% = balanced). You have overwhelming energy. The risk is stagnation and bulldozing over others.`);

  // Marriage
  const spouse = checkSpouseStar(chart, tgClassification);
  const marriageFlags = flags.marriage ?? [];

  if (chart.gender === "female") {
    const doStr = (tgClassification.DO?.strength as string) ?? "ABSENT";
    if (doStr === "ABSENT") parts.push("Marriage: Your husband star (正官 Direct Officer) is ABSENT. This is the hardest marriage indicator for a woman — partnership comes very late, with great difficulty, or through unconventional paths. The right luck decade is critical.");
    else if (marriageFlags.length > 0) {
      const severeCount = marriageFlags.filter(f => f.severity === "severe" || f.severity === "critical").length;
      if (severeCount >= 2) parts.push("Marriage: Multiple severe marriage indicators. Relationships are a major life challenge requiring active management.");
      else if (severeCount === 1) parts.push("Marriage: One significant marriage challenge exists. Awareness and timing can mitigate it.");
      else parts.push("Marriage: Some marriage challenges flagged, but manageable with awareness.");
    } else parts.push("Marriage: No major obstacles in the natal chart. Timing and luck pillar alignment will determine when.");
  } else {
    if (spouse.is_critical_absent) parts.push(`Marriage: Your ${spouse.label} is ABSENT. This is the single hardest indicator — marriage comes very late, with great difficulty, or through unconventional paths. This is not a death sentence, but it requires conscious effort and the right luck decade.`);
    else if (marriageFlags.length > 0) {
      const severeCount = marriageFlags.filter(f => f.severity === "severe" || f.severity === "critical").length;
      if (severeCount >= 2) parts.push("Marriage: Multiple severe marriage indicators. Relationships are a major life challenge requiring active management.");
      else if (severeCount === 1) parts.push("Marriage: One significant marriage challenge exists. Awareness and timing can mitigate it.");
      else parts.push("Marriage: Some marriage challenges flagged, but manageable with awareness.");
    } else parts.push("Marriage: No major obstacles in the natal chart. Timing and luck pillar alignment will determine when.");
  }

  // Wealth
  const dw = (tgClassification.DW?.strength as string) ?? "ABSENT";
  const iw = (tgClassification.IW?.strength as string) ?? "ABSENT";
  const rw = (tgClassification.RW?.strength as string) ?? "ABSENT";
  if (dw === "ABSENT" && iw === "ABSENT") parts.push("Wealth: Both wealth stars absent. Money doesn't come naturally — must be actively pursued through favorable elements and timing.");
  else if (rw === "PROMINENT") parts.push("Wealth: Rob Wealth is prominent — money comes but also leaves through others. Avoid partnerships and lending. Protect what you earn.");
  else if (iw === "PROMINENT") parts.push("Wealth: Strong Indirect Wealth — windfall potential through speculation, business, or investments. Risk tolerance is high, but so is the upside.");

  // Health — use wuxing percentages (avg=20)
  if (!elemCounts) {
    const wr = calculateWuxing(chartToWuxingInput(chart));
    elemCounts = wuxingToElementCounts(wr);
  }
  const avgCount = 20; // wuxing percentages average to 20
  const deficientElements = ["Wood", "Fire", "Earth", "Metal", "Water"].filter(e => (elemCounts![e] ?? 0) < avgCount * 0.5);
  if (deficientElements.length > 0) {
    const organs = deficientElements.map(e => `${HEALTH_ELEMENT_MAP[e].yin_organ.split("(")[0].trim()} (${e})`);
    parts.push(`Health: Watch ${organs.join(", ")} — these elements are deficient in your chart.`);
  }

  parts.push(`Life lesson: ${lifeLesson}`);

  const ug = strength.useful_god;
  const ugPct = strength.element_percentages[ug] ?? 0;
  parts.push(
    `Your useful god is ${ug} (currently at ${ugPct}% — most deficient). `
    + `Adding ${ug} brings the chart closest to 20% equilibrium across all five elements. `
    + `Favorable: ${strength.favorable_elements.join(", ")}. `
    + `Unfavorable: ${strength.unfavorable_elements.join(", ")} (already excessive). `
    + `Everything in your life improves when you increase ${ug} element exposure.`
  );

  return { id: "summary", title: "Honest Summary", title_zh: "總結", text: parts.join(" ") };
}

function _diffTenGodsArriving(
  tgEntries: TenGodEntry[],
  tgClassification: Record<string, Record<string, unknown>>,
  chart: ChartData,
): Record<string, unknown> | null {
  const natalPositions = new Set(["year", "month", "day", "hour"]);
  const arriving: Record<string, Array<[string, boolean]>> = {};
  for (const entry of tgEntries) {
    if (natalPositions.has(entry.position)) continue;
    if (entry.abbreviation === "DM") continue;
    if (!arriving[entry.abbreviation]) arriving[entry.abbreviation] = [];
    arriving[entry.abbreviation].push([entry.position, entry.visible]);
  }
  if (Object.keys(arriving).length === 0) return null;

  const items: Array<Record<string, unknown>> = [];
  for (const [abbr, appearances] of Object.entries(arriving)) {
    const natalStrength = (tgClassification[abbr]?.strength as string) ?? "ABSENT";
    const info = TEN_GOD_INFO[abbr] ?? {};
    const english = info.english ?? abbr;
    const chinese = info.chinese ?? "";
    const lifeMeaning = TEN_GOD_LIFE_MEANING[chart.gender]?.[abbr] ?? "";

    const visibleArrivals = appearances.filter(([, vis]) => vis).map(([pos]) => pos);
    const hiddenArrivals = appearances.filter(([, vis]) => !vis).map(([pos]) => `(${pos} hidden)`);
    const sources = [...visibleArrivals, ...hiddenArrivals].join(", ");

    let labelPrefix: string, severity: string, meaning: string;
    if (natalStrength === "ABSENT") {
      labelPrefix = "NEW"; severity = "warning";
      const templates = TEN_GOD_INTERPRETATIONS[abbr] ?? {};
      meaning = _pick(templates.PRESENT ?? [`${english} arrives`]);
    } else if (natalStrength === "HIDDEN_ONLY" || natalStrength === "WEAK") {
      labelPrefix = "BOOSTED"; severity = "info"; meaning = `${english} was weak natally, now reinforced`;
    } else if (natalStrength === "PROMINENT") {
      labelPrefix = "AMPLIFIED"; severity = ["7K", "HO", "RW"].includes(abbr) ? "warning" : "info"; meaning = `${english} already dominant — further amplified`;
    } else {
      labelPrefix = "REINFORCED"; severity = "info"; meaning = `${english} gains additional support`;
    }
    if (lifeMeaning) meaning += ` (${lifeMeaning})`;

    items.push({ label: `${labelPrefix}: ${abbr} (${chinese})`, value: `via ${sources} — ${meaning}`, severity });
  }

  return { id: "ten_gods_diff", title: "Ten Gods Arriving", title_zh: "十神變化", text: `${Object.keys(arriving).length} ten god(s) enter from luck/time pillars`, items };
}

function _diffInteractions(interactions: BranchInteraction[]): Record<string, unknown> | null {
  const positiveTypes = new Set(["harmony", "three_harmony", "half_three_harmony", "directional_combo"]);
  const newInteractions = interactions.filter(i => i.activated_by_lp);
  if (newInteractions.length === 0) return null;

  const posCount = newInteractions.filter(i => positiveTypes.has(i.interaction_type)).length;
  const negCount = newInteractions.length - posCount;

  const items: Array<Record<string, unknown>> = [];
  for (const inter of newInteractions.slice(0, 8)) {
    const polarity = positiveTypes.has(inter.interaction_type) ? "positive" : "negative";
    const severity = polarity === "positive" ? "positive" : inter.severity;
    const palacesStr = inter.palaces.join(" vs ");
    items.push({
      label: `${inter.chinese_name} ${inter.interaction_type.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}`,
      value: palacesStr ? `${palacesStr} — ${inter.description}` : inter.description,
      severity,
    });
  }
  return { id: "interactions_diff", title: "New Interactions", title_zh: "新增地支關係", text: `${posCount} positive, ${negCount} negative NEW interactions from luck/time pillars`, items };
}

function _diffShenSha(shenSha: ShenShaResult[]): Record<string, unknown> | null {
  const newStars = shenSha.filter(s => s.present && s.activated_by !== null);
  if (newStars.length === 0) return null;

  const items: Array<Record<string, unknown>> = [];
  for (const s of newStars) {
    const templates = SHEN_SHA_IMPACTS[s.name_chinese] ?? {};
    const text = _pick(templates.present ?? [`${s.name_english} activated`]);
    const severity = s.nature === "auspicious" ? "positive" : s.nature === "inauspicious" ? "negative" : "info";
    items.push({ label: `${s.name_chinese} ${s.name_english}`, value: `via ${s.activated_by} — ${text}`, severity });
  }
  return { id: "shen_sha_diff", title: "Stars Activated", title_zh: "新增神煞", text: `${newStars.length} star(s) activated by luck/time pillars`, items };
}

function _diffElementShift(chart: ChartData, natalElemCounts?: Record<string, number>): Record<string, unknown> | null {
  // Natal counts from wuxing (percentages, already summing to ~100)
  if (!natalElemCounts) {
    const wr = calculateWuxing(chartToWuxingInput(chart));
    natalElemCounts = wuxingToElementCounts(wr);
  }
  // Full counts (with luck/time pillars) still use old pipeline
  const fullCounts = countAllElements(chart);

  const fullTotal = Object.values(fullCounts).reduce((a, b) => a + b, 0);

  const EC: Record<string, string> = { Wood: "木", Fire: "火", Earth: "土", Metal: "金", Water: "水" };
  const items: Array<Record<string, unknown>> = [];
  let anyDifference = false;
  for (const elem of ["Wood", "Fire", "Earth", "Metal", "Water"]) {
    const natalPct = natalElemCounts[elem] ?? 0; // Already percentage
    const fullPct = fullTotal > 0 ? fullCounts[elem] / fullTotal * 100 : 0;
    const change = fullPct - natalPct;
    if (Math.abs(change) < 1.0) continue;
    const arrow = change > 0 ? "+" : "";
    const severity = change > 3 ? "positive" : change < -3 ? "negative" : "info";
    items.push({ label: `${EC[elem]} ${elem}`, value: `${Math.round(natalPct)}% -> ${Math.round(fullPct)}% (${arrow}${Math.round(change)}%)`, severity });
  }

  if (items.length === 0) return null;
  return { id: "element_shift", title: "Element Balance Shift", title_zh: "五行變化", text: "How luck/time pillars shift your element balance", items };
}

function buildClientSummary(
  chart: ChartData,
  results: Record<string, unknown>,
  flags: Record<string, RedFlag[]>,
): Record<string, unknown> {
  const strength = results.strength as StrengthAssessment;
  const tgEntries = results.ten_god_entries as TenGodEntry[];
  const tgClassification = results.ten_god_classification as Record<string, Record<string, unknown>>;
  const interactions = results.interactions as BranchInteraction[];
  const shenSha = results.shen_sha as ShenShaResult[];
  const predictions = results.predictions as Record<string, EventPrediction[]>;

  // Get wuxing element counts (percentages) from results
  const wr = results.wuxing_result as WuxingResult | undefined;
  const elemCounts = wr ? wuxingToElementCounts(wr) : undefined;

  const hasLuck = chart.luck_pillar !== null;
  const hasTimePeriod = Object.keys(chart.time_period_pillars).length > 0;
  const isFull = hasLuck || hasTimePeriod;
  const tier = isFull ? "full" : "natal";

  let sections: Array<Record<string, unknown>>;

  if (!isFull) {
    sections = [
      _summaryChartOverview(chart),
      _summaryStrength(strength, chart),
      _summaryTenGods(chart, tgClassification),
      _summaryInteractions(interactions),
      _summaryShenSha(shenSha),
      _summaryRedFlags(flags),
      _summaryNatalPredictions(chart, tgClassification, strength, predictions, flags),
      _summaryHealth(chart, strength, elemCounts),
      _summaryRemedies(strength, chart, elemCounts),
      _summaryHonest(chart, strength, tgClassification, flags, elemCounts),
    ];
  } else {
    sections = [];
    const lpSection = _summaryLuckPillar(chart, strength);
    if (lpSection) sections.push(lpSection);

    const elemDiff = _diffElementShift(chart, elemCounts);
    if (elemDiff) sections.push(elemDiff);

    const tgDiff = _diffTenGodsArriving(tgEntries, tgClassification, chart);
    if (tgDiff) sections.push(tgDiff);

    const interDiff = _diffInteractions(interactions);
    if (interDiff) sections.push(interDiff);

    const shaDiff = _diffShenSha(shenSha);
    if (shaDiff) sections.push(shaDiff);

    const rf = _summaryRedFlags(flags);
    if ((rf.items as unknown[])?.length > 0) sections.push(rf);

    const isYearOnly = !("monthly" in chart.time_period_pillars) && !("daily" in chart.time_period_pillars);
    if (isYearOnly) {
      const predSection = _summaryPredictionsTimeline(predictions);
      if (predSection) sections.push(predSection);
    }

    sections.push(_summaryRemedies(strength, chart, elemCounts));
  }

  return { tier, sections };
}


// =============================================================================
// MASTER ADAPTER FUNCTION
// =============================================================================

export function adaptToFrontend(chart: ChartData, results: Record<string, unknown>): Record<string, unknown> {
  /**
   * Master adapter: translates comprehensive engine results into the exact
   * JSON shape the frontend expects from /api/analyze_bazi.
   */
  const strength = results.strength as StrengthAssessment;
  const tgEntries = results.ten_god_entries as TenGodEntry[];
  const tgClassification = results.ten_god_classification as Record<string, Record<string, unknown>>;
  const interactions = results.interactions as BranchInteraction[];
  const shenSha = results.shen_sha as ShenShaResult[];
  const predictions = results.predictions as Record<string, EventPrediction[]>;
  const env = results.environment as EnvironmentAssessment;
  const comprehensiveReport = (results.comprehensive_report as string) ?? "";
  const wuxingResult = results.wuxing_result as WuxingResult | undefined;

  // 1. Build all nodes
  const nodes = buildAllNodes(chart);

  // 2. Map interaction badges onto nodes
  mapInteractionsToBadges(interactions, chart, nodes);

  // 3. Collect red flags
  const flags = _collectRedFlags(chart, strength, tgClassification, interactions, shenSha);

  // 4. Build element scores (use wuxing result if available)
  const [baseScore, natalScore, postScore] = buildElementScores(chart, interactions, wuxingResult);

  // 5. Get wuxing element counts for downstream functions
  const elemCounts = wuxingResult ? wuxingToElementCounts(wuxingResult) : undefined;

  // 6. Assemble response
  const response: Record<string, unknown> = {};

  // Nodes
  Object.assign(response, nodes);

  // Scores
  response.base_element_score = baseScore;
  response.natal_element_score = natalScore;
  response.post_element_score = postScore;

  // Interactions
  response.interactions = buildInteractionDict(interactions);

  // Daymaster analysis
  response.daymaster_analysis = buildDaymasterAnalysis(strength, chart);

  // DM Lens (Step 8b) — support-pressure narrative
  if (wuxingResult) {
    response.dm_lens = calculateDmLens(wuxingResult);
  }

  // Life aspects
  response.health_analysis = buildHealthAnalysis(flags, strength, chart, elemCounts);
  response.wealth_analysis = buildWealthAnalysis(flags, strength, tgClassification, chart);
  response.learning_analysis = buildLearningAnalysis(flags, strength, tgClassification, chart);

  // Ten Gods detail
  response.ten_gods_detail = buildTenGodsDetail(tgEntries, tgClassification, chart);

  // Special stars
  response.special_stars = buildSpecialStars(shenSha);

  // Recommendations
  response.recommendations = buildRecommendations(predictions, flags, strength, env);

  // Narrative
  response.narrative_analysis = buildNarrativeAnalysis(interactions, shenSha, tgEntries, strength, chart, wuxingResult);

  // Pattern engine (stub)
  response.pattern_engine_analysis = {
    enhanced_patterns: [],
    domain_analysis: {},
    recommendations: response.recommendations,
    special_stars: response.special_stars,
  };

  // Wealth storage
  response.wealth_storage_analysis = _computeWealthStorage(chart);

  // Unit tracker (stub)
  response.unit_tracker = null;

  // Mappings
  response.mappings = buildMappings();

  // Comprehensive report
  response.comprehensive_report = comprehensiveReport;

  // Qi Phase + Spiritual Sensitivity
  try {
    const qiPhaseResult = analyzeQiPhases(chart, shenSha);
    response.qi_phase_analysis = qiPhaseResult;

    const spiritualBonus = (qiPhaseResult as Record<string, unknown>).spiritual_bonus as number ?? 0;
    response.spiritual_sensitivity = assessSpiritualSensitivity(chart, shenSha, spiritualBonus);
  } catch {
    response.qi_phase_analysis = null;
    response.spiritual_sensitivity = null;
  }

  // Client summary
  response.client_summary = buildClientSummary(chart, results, flags);

  return response;
}
