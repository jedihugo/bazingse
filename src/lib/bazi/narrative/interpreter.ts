
// =============================================================================
// NARRATIVE INTERPRETER
// =============================================================================
// Main narrative generation entry point.
// Processes BaZi analysis data into human-readable narratives.
// Ported from api/library/narrative/interpreter.py
// =============================================================================

import type { Element, StemName, BranchName } from '../core';
import { STEMS } from '../core';
import { NARRATIVE_TEMPLATES, ELEMENT_MANIFESTATIONS, PILLAR_CONTEXT } from './templates';
import { calculatePriorityScore, prioritizeNarratives } from './priority';
import type { NarrativeEntry } from './priority';
import { ELEMENT_NAMES, BRANCH_NAMES, STEM_NAMES, buildNarrativeText } from './localization';
import { getElementBalanceContext, ELEMENT_GENERATES, ELEMENT_CONTROLS } from './modifiers';
import { analyzeNodeChain, enrichClashWithChainAnalysis, STORAGE_BRANCHES } from './chain-engine';

// ---------------------------------------------------------------------------
// Node to Pillar Mapping
// ---------------------------------------------------------------------------

export const NODE_TO_PILLAR: Record<string, string> = {
  hs_y: "year", eb_y: "year",
  hs_m: "month", eb_m: "month",
  hs_d: "day", eb_d: "day",
  hs_h: "hour", eb_h: "hour",
  hs_10yl: "10yl", eb_10yl: "10yl",
  hs_yl: "annual", eb_yl: "annual",
  hs_ml: "monthly", eb_ml: "monthly",
  hs_dl: "daily", eb_dl: "daily",
  hs_hl: "hourly", eb_hl: "hourly",
};

// ---------------------------------------------------------------------------
// Pillar Life Areas
// ---------------------------------------------------------------------------

export const PILLAR_LIFE_AREAS: Record<string, string[]> = {
  year: ["ancestry", "early_childhood", "external_environment"],
  month: ["parents", "career", "social_position"],
  day: ["self", "marriage", "inner_nature"],
  hour: ["children", "later_life", "legacy"],
};

// ---------------------------------------------------------------------------
// Type Chinese and Polarity
// ---------------------------------------------------------------------------

const TYPE_CHINESE: Record<string, string> = {
  three_meetings: "三會",
  three_combinations: "三合",
  six_harmonies: "六合",
  half_meetings: "半會",
  half_combinations: "半合",
  arched_combinations: "拱合",
  stem_combination: "天干合",
  clash: "沖",
  punishment: "刑",
  harm: "害",
  destruction: "破",
  stem_conflict: "天干剋",
};

const TYPE_POLARITY: Record<string, 'positive' | 'negative'> = {
  three_meetings: "positive",
  three_combinations: "positive",
  six_harmonies: "positive",
  half_meetings: "positive",
  half_combinations: "positive",
  arched_combinations: "positive",
  stem_combination: "positive",
  clash: "negative",
  punishment: "negative",
  harm: "negative",
  destruction: "negative",
  stem_conflict: "negative",
};

// ---------------------------------------------------------------------------
// Element Chinese
// ---------------------------------------------------------------------------

function elementToChinese(element: string): string {
  const map: Record<string, string> = {
    Wood: "木", Fire: "火", Earth: "土", Metal: "金", Water: "水",
  };
  return map[element] ?? element;
}

// ---------------------------------------------------------------------------
// Generate Narrative (Main Entry Point)
// ---------------------------------------------------------------------------

export interface NarrativeInput {
  interactions: Record<string, any>;
  element_scores: Record<string, number>;
  daymaster_stem: StemName;
  daymaster_element: Element;
  dm_strength_score: number;
  dm_strength_verdict: string;
  seasonal_states?: Record<string, string>;
  wealth_storage?: Record<string, any>;
  shen_sha?: Array<Record<string, any>>;
  ten_gods?: Array<Record<string, any>>;
  nodes?: Record<string, any>;
}

export interface NarrativeOutput {
  narratives: NarrativeEntry[];
  chronological: Array<Record<string, any>>;
  summary: { en: string; zh: string };
  category_groups: Record<string, NarrativeEntry[]>;
}

export function generateNarrative(input: NarrativeInput): NarrativeOutput {
  const narratives: NarrativeEntry[] = [];

  // 1. Day Master narrative
  const dmNarrative = generateDaymasterNarrative(
    input.daymaster_stem,
    input.daymaster_element,
    input.dm_strength_score,
    input.dm_strength_verdict
  );
  narratives.push(dmNarrative);

  // 2. Element balance narratives
  const balanceNarratives = generateElementBalanceNarratives(
    input.element_scores,
    input.daymaster_element
  );
  narratives.push(...balanceNarratives);

  // 3. Interaction narratives
  for (const [intId, intData] of Object.entries(input.interactions)) {
    if (typeof intData === 'string') continue;

    const narrative = processInteraction(intId, intData, input);
    if (narrative) {
      narratives.push(narrative);
    }
  }

  // 4. Wealth storage narratives
  if (input.wealth_storage) {
    const wealthNarratives = generateWealthStorageNarratives(input.wealth_storage);
    narratives.push(...wealthNarratives);
  }

  // 5. Ten Gods narratives
  if (input.ten_gods) {
    const tenGodNarratives = generateTenGodsNarratives(input.ten_gods);
    narratives.push(...tenGodNarratives);
  }

  // 6. Build chronological list
  const chronological = buildAllChronological(narratives);

  // 7. Prioritize
  const sorted = prioritizeNarratives(narratives);

  // 8. Group by category
  const groups: Record<string, NarrativeEntry[]> = {};
  for (const n of sorted) {
    const cat = n.category || 'other';
    if (!groups[cat]) groups[cat] = [];
    groups[cat].push(n);
  }

  // 9. Summary
  const summary = generateSummary(input, sorted);

  return {
    narratives: sorted,
    chronological,
    summary,
    category_groups: groups,
  };
}

// ---------------------------------------------------------------------------
// Day Master Narrative
// ---------------------------------------------------------------------------

function generateDaymasterNarrative(
  stem: StemName,
  element: Element,
  score: number,
  verdict: string
): NarrativeEntry {
  let templateKey: string;
  if (score >= 24) {
    templateKey = 'daymaster_strong';
  } else if (score <= 16) {
    templateKey = 'daymaster_weak';
  } else {
    templateKey = 'daymaster_balanced';
  }

  const template = NARRATIVE_TEMPLATES[templateKey];
  const stemZh = STEM_NAMES[stem]?.zh ?? stem;
  const elementZh = elementToChinese(element);

  const textEn = template.en
    .replaceAll('{stem}', stem)
    .replaceAll('{element}', element)
    .replaceAll('{score}', String(Math.round(score)));

  const textZh = template.zh
    .replaceAll('{stem_zh}', stemZh)
    .replaceAll('{element_zh}', elementZh)
    .replaceAll('{score}', String(Math.round(score)));

  return {
    type: templateKey,
    category: 'daymaster',
    priority: template.priority,
    text_en: textEn,
    text_zh: textZh,
    sentiment: template.sentiment,
  };
}

// ---------------------------------------------------------------------------
// Element Balance Narratives
// ---------------------------------------------------------------------------

function generateElementBalanceNarratives(
  elementScores: Record<string, number>,
  daymasterElement: Element
): NarrativeEntry[] {
  const results: NarrativeEntry[] = [];
  const contexts = getElementBalanceContext(elementScores, daymasterElement);

  for (const ctx of contexts) {
    if (ctx.status === 'balanced') continue;

    const templateKey = ctx.status === 'excess' ? 'element_excess' : 'element_deficient';
    const template = NARRATIVE_TEMPLATES[templateKey];
    if (!template) continue;

    const manifestation = ELEMENT_MANIFESTATIONS[ctx.element];
    const manifestText = ctx.status === 'excess'
      ? manifestation?.excess
      : manifestation?.deficient;

    const textEn = template.en
      .replaceAll('{element}', ctx.element)
      .replaceAll('{score}', String(ctx.percentage))
      .replaceAll('{excess_text}', manifestText?.en ?? '')
      .replaceAll('{deficient_text}', manifestText?.en ?? '');

    const textZh = template.zh
      .replaceAll('{element_zh}', elementToChinese(ctx.element))
      .replaceAll('{score}', String(ctx.percentage))
      .replaceAll('{excess_text_zh}', manifestText?.zh ?? '')
      .replaceAll('{deficient_text_zh}', manifestText?.zh ?? '');

    results.push({
      type: templateKey,
      category: 'balance',
      priority: template.priority,
      text_en: textEn,
      text_zh: textZh,
      sentiment: template.sentiment,
    });
  }

  return results;
}

// ---------------------------------------------------------------------------
// Process Interaction
// ---------------------------------------------------------------------------

function processInteraction(
  intId: string,
  intData: Record<string, any>,
  input: NarrativeInput
): NarrativeEntry | null {
  const parts = intId.split('~');
  if (parts.length < 2) return null;

  const intType = parts[0];
  const participants = parts[1]?.split('-') ?? [];

  // Determine category key
  const categoryMap: Record<string, string> = {
    THREE_MEETINGS: 'three_meetings',
    THREE_COMBINATIONS: 'three_combinations',
    SIX_HARMONIES: 'six_harmonies',
    HALF_MEETINGS: 'half_meetings',
    HALF_COMBINATIONS: 'half_combinations',
    ARCHED_COMBINATIONS: 'arched_combinations',
    HS_COMBINATIONS: 'stem_combination',
    STEM_COMBINATION: 'stem_combination',
    CLASH: 'clash',
    CLASHES: 'clash',
    PUNISHMENT: 'punishment',
    PUNISHMENTS: 'punishment',
    HARM: 'harm',
    HARMS: 'harm',
    DESTRUCTION: 'destruction',
    STEM_CONFLICT: 'stem_conflict',
    STEM_CONFLICTS: 'stem_conflict',
  };

  const category = categoryMap[intType];
  if (!category) return null;

  const template = NARRATIVE_TEMPLATES[category];
  if (!template) return null;

  // Extract variables
  const element = intData.element ?? '';
  const distance = intData.distance ?? 1;
  const isTransformed = intData.transformed ?? false;
  const positions = intData.positions ?? [];
  const pillar = positions.length > 0
    ? positionToName(Math.min(...positions))
    : 'natal';

  // Build text
  const branchesStr = participants.join('-');
  const branchesZh = participants
    .map((b: string) => BRANCH_NAMES[b as BranchName]?.zh ?? b)
    .join('');

  const textEn = template.en
    .replaceAll('{branches}', branchesStr)
    .replaceAll('{stems}', branchesStr)
    .replaceAll('{element}', element)
    .replaceAll('{pillars}', pillar)
    .replaceAll('{domains}', category)
    .replaceAll('{severity_text}', '')
    .replaceAll('{punishment_type}', intData.punishment_type ?? '');

  const textZh = template.zh
    .replaceAll('{branches_zh}', branchesZh)
    .replaceAll('{stems_zh}', branchesZh)
    .replaceAll('{element_zh}', elementToChinese(element))
    .replaceAll('{pillars_zh}', pillar)
    .replaceAll('{domains_zh}', TYPE_CHINESE[category] ?? category)
    .replaceAll('{severity_text_zh}', '')
    .replaceAll('{punishment_type_zh}', intData.punishment_type ?? '');

  return {
    type: category,
    category: template.category,
    priority: template.priority,
    text_en: textEn,
    text_zh: textZh,
    sentiment: template.sentiment,
    distance,
    is_transformed: isTransformed,
    pillar,
    interaction_id: intId,
    participants,
    element,
  };
}

// ---------------------------------------------------------------------------
// Wealth Storage Narratives
// ---------------------------------------------------------------------------

function generateWealthStorageNarratives(
  wealthStorage: Record<string, any>
): NarrativeEntry[] {
  const results: NarrativeEntry[] = [];

  if (wealthStorage.has_storage) {
    const template = NARRATIVE_TEMPLATES.wealth_storage_present;
    if (template) {
      results.push({
        type: 'wealth_storage_present',
        category: 'wealth',
        priority: template.priority,
        text_en: template.en
          .replaceAll('{branch}', wealthStorage.storage_branch ?? '')
          .replaceAll('{pillar}', wealthStorage.pillar ?? '')
          .replaceAll('{element}', wealthStorage.element ?? '')
          .replaceAll('{state}', wealthStorage.state ?? ''),
        text_zh: template.zh
          .replaceAll('{branch_zh}', wealthStorage.branch_zh ?? '')
          .replaceAll('{pillar_zh}', wealthStorage.pillar_zh ?? '')
          .replaceAll('{element_zh}', wealthStorage.element_zh ?? '')
          .replaceAll('{state_zh}', wealthStorage.state_zh ?? ''),
        sentiment: template.sentiment,
      });
    }

    if (wealthStorage.is_clashed) {
      const clashTemplate = NARRATIVE_TEMPLATES.wealth_storage_clashed;
      if (clashTemplate) {
        results.push({
          type: 'wealth_storage_clashed',
          category: 'wealth',
          priority: clashTemplate.priority,
          text_en: clashTemplate.en
            .replaceAll('{branch}', wealthStorage.storage_branch ?? '')
            .replaceAll('{pillar}', wealthStorage.pillar ?? ''),
          text_zh: clashTemplate.zh
            .replaceAll('{branch_zh}', wealthStorage.branch_zh ?? '')
            .replaceAll('{pillar_zh}', wealthStorage.pillar_zh ?? ''),
          sentiment: clashTemplate.sentiment,
        });
      }
    }
  }

  return results;
}

// ---------------------------------------------------------------------------
// Ten Gods Narratives
// ---------------------------------------------------------------------------

function generateTenGodsNarratives(
  tenGods: Array<Record<string, any>>
): NarrativeEntry[] {
  const results: NarrativeEntry[] = [];
  const template = NARRATIVE_TEMPLATES.ten_god_pillar;
  if (!template) return results;

  for (const tg of tenGods) {
    results.push({
      type: 'ten_god_pillar',
      category: 'ten_gods',
      priority: template.priority,
      text_en: template.en
        .replaceAll('{ten_god}', tg.english ?? '')
        .replaceAll('{ten_god_chinese}', tg.chinese ?? '')
        .replaceAll('{position}', tg.position ?? '')
        .replaceAll('{meaning}', tg.meaning ?? ''),
      text_zh: template.zh
        .replaceAll('{ten_god}', tg.english ?? '')
        .replaceAll('{ten_god_chinese}', tg.chinese ?? '')
        .replaceAll('{position_zh}', tg.position_zh ?? tg.position ?? '')
        .replaceAll('{meaning_zh}', tg.meaning_zh ?? tg.meaning ?? ''),
      sentiment: template.sentiment,
    });
  }

  return results;
}

// ---------------------------------------------------------------------------
// Chronological List
// ---------------------------------------------------------------------------

function buildAllChronological(
  narratives: NarrativeEntry[]
): Array<Record<string, any>> {
  return narratives
    .filter((n) => n.interaction_id)
    .map((n) => buildChronologicalEntry(n));
}

function buildChronologicalEntry(
  narrative: NarrativeEntry
): Record<string, any> {
  return {
    type: narrative.type,
    type_zh: TYPE_CHINESE[narrative.type] ?? narrative.type,
    polarity: TYPE_POLARITY[narrative.type] ?? 'neutral',
    participants: narrative.participants ?? [],
    element: narrative.element ?? '',
    pillar: narrative.pillar ?? '',
    distance: narrative.distance ?? 0,
    is_transformed: narrative.is_transformed ?? false,
    text_en: narrative.text_en,
    text_zh: narrative.text_zh,
  };
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

function generateSummary(
  input: NarrativeInput,
  narratives: NarrativeEntry[]
): { en: string; zh: string } {
  const positiveCount = narratives.filter((n) => n.sentiment === 'positive').length;
  const negativeCount = narratives.filter((n) => n.sentiment === 'negative').length;
  const totalCount = narratives.length;

  const balance = positiveCount > negativeCount
    ? 'favorable'
    : negativeCount > positiveCount
      ? 'challenging'
      : 'balanced';

  const en = `Chart has ${totalCount} narrative elements: ${positiveCount} positive, ${negativeCount} negative. Overall outlook: ${balance}. Day Master ${input.daymaster_stem} (${input.daymaster_element}) at ${Math.round(input.dm_strength_score)}% strength.`;
  const zh = `命盤有${totalCount}個敘事元素：${positiveCount}個正面，${negativeCount}個負面。整體展望：${balance === 'favorable' ? '有利' : balance === 'challenging' ? '具挑戰性' : '平衡'}。日主${STEM_NAMES[input.daymaster_stem]?.zh ?? input.daymaster_stem}（${elementToChinese(input.daymaster_element)}）強度${Math.round(input.dm_strength_score)}%。`;

  return { en, zh };
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function positionToName(position: number): string {
  const map: Record<number, string> = {
    0: "hour", 1: "day", 2: "month", 3: "year",
    4: "10yl", 5: "annual", 6: "monthly", 7: "daily", 8: "hourly",
  };
  return map[position] ?? "unknown";
}

function addPillarContext(
  narrative: NarrativeEntry,
  pillar: string
): NarrativeEntry {
  const context = PILLAR_CONTEXT[pillar];
  if (!context) return narrative;

  return {
    ...narrative,
    text_en: `${narrative.text_en} ${context.en}`,
    text_zh: `${narrative.text_zh} ${context.zh}`,
  };
}
