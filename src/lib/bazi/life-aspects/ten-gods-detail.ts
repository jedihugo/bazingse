import 'server-only';

// =============================================================================
// TEN GODS DETAIL ANALYSIS
// =============================================================================
// Detailed Ten Gods analysis with pillar-specific meanings.
// Ported from api/library/life_aspects/ten_gods_detail.py
// =============================================================================

import type { Element, StemName } from '../core';
import { STEMS } from '../core';
import { STEM_TO_ELEMENT, TEN_GOD_ASPECT_MAPPING } from './base';

// ---------------------------------------------------------------------------
// Get Ten God for Stem
// ---------------------------------------------------------------------------

export function getTenGodForStem(
  daymasterStem: StemName,
  targetStem: StemName
): string | null {
  const dmData = STEMS[daymasterStem];
  const targetData = STEMS[targetStem];
  if (!dmData || !targetData) return null;

  const dmElement = dmData.element as Element;
  const targetElement = targetData.element as Element;
  const dmPolarity = dmData.polarity;
  const targetPolarity = targetData.polarity;
  const samePolarity = dmPolarity === targetPolarity;

  // Same element
  if (dmElement === targetElement) {
    return samePolarity ? 'F' : 'RW';
  }

  // DM generates target (output)
  const generates: Record<Element, Element> = {
    Wood: "Fire", Fire: "Earth", Earth: "Metal", Metal: "Water", Water: "Wood",
  };
  if (generates[dmElement] === targetElement) {
    return samePolarity ? 'EG' : 'HO';
  }

  // DM controls target (wealth)
  const controls: Record<Element, Element> = {
    Wood: "Earth", Fire: "Metal", Earth: "Water", Metal: "Wood", Water: "Fire",
  };
  if (controls[dmElement] === targetElement) {
    return samePolarity ? 'DW' : 'IW';
  }

  // Target controls DM (authority)
  if (controls[targetElement] === dmElement) {
    return samePolarity ? '7K' : 'DO';
  }

  // Target generates DM (resource)
  if (generates[targetElement] === dmElement) {
    return samePolarity ? 'IR' : 'DR';
  }

  return null;
}

// ---------------------------------------------------------------------------
// Ten God Pillar Meanings
// ---------------------------------------------------------------------------

export interface PillarMeaningEntry {
  meaning: string;
  positive: string;
  negative: string;
}

export const TEN_GOD_PILLAR_MEANINGS: Record<string, Record<string, PillarMeaningEntry>> = {
  F: {
    year: { meaning: "Siblings help in childhood", positive: "Strong family support", negative: "Competition with siblings" },
    month: { meaning: "Peers and colleagues", positive: "Good teamwork", negative: "Workplace rivalry" },
    day: { meaning: "Self-identity", positive: "Strong sense of self", negative: "Stubbornness" },
    hour: { meaning: "Friends in later life", positive: "Loyal companions", negative: "Competition with children" },
  },
  RW: {
    year: { meaning: "Competitive siblings", positive: "Drives ambition", negative: "Family wealth disputes" },
    month: { meaning: "Business competition", positive: "Entrepreneurial spirit", negative: "Loss through competition" },
    day: { meaning: "Aggressive self-expression", positive: "Bold personality", negative: "Relationship conflicts" },
    hour: { meaning: "Active later years", positive: "Energetic retirement", negative: "Financial loss in old age" },
  },
  EG: {
    year: { meaning: "Creative childhood", positive: "Artistic upbringing", negative: "Scattered early education" },
    month: { meaning: "Creative career", positive: "Artistic profession", negative: "Unreliable income" },
    day: { meaning: "Personal creativity", positive: "Rich inner life", negative: "Difficulty focusing" },
    hour: { meaning: "Creative children", positive: "Talented offspring", negative: "Permissive parenting" },
  },
  HO: {
    year: { meaning: "Rebellious childhood", positive: "Independent thinking", negative: "Conflicts with authority" },
    month: { meaning: "Unconventional career", positive: "Innovative work", negative: "Career instability" },
    day: { meaning: "Sharp personality", positive: "Incisive mind", negative: "Relationship friction" },
    hour: { meaning: "Innovative children", positive: "Progressive offspring", negative: "Children challenge traditions" },
  },
  DW: {
    year: { meaning: "Family wealth", positive: "Comfortable upbringing", negative: "Materialistic family" },
    month: { meaning: "Steady income", positive: "Reliable career earnings", negative: "Limited growth" },
    day: { meaning: "Spouse/partnership", positive: "Supportive partner", negative: "Possessive relationship" },
    hour: { meaning: "Financial security", positive: "Comfortable retirement", negative: "Worry about money" },
  },
  IW: {
    year: { meaning: "Father's influence", positive: "Entrepreneurial family", negative: "Unstable finances" },
    month: { meaning: "Variable income", positive: "Windfall potential", negative: "Financial volatility" },
    day: { meaning: "Speculative nature", positive: "Intuitive investor", negative: "Gambling tendency" },
    hour: { meaning: "Unexpected gains", positive: "Lucky in later life", negative: "Financial instability" },
  },
  DO: {
    year: { meaning: "Disciplined upbringing", positive: "Strong moral foundation", negative: "Strict parents" },
    month: { meaning: "Authority position", positive: "Leadership career", negative: "Heavy responsibility" },
    day: { meaning: "Husband (for female)", positive: "Stable marriage", negative: "Controlling partner" },
    hour: { meaning: "Respected elder", positive: "Authority in old age", negative: "Rigid in later life" },
  },
  "7K": {
    year: { meaning: "Challenging childhood", positive: "Builds resilience", negative: "Trauma from authority" },
    month: { meaning: "Power and danger", positive: "Powerful career position", negative: "Dangerous work environment" },
    day: { meaning: "Intense relationships", positive: "Passionate partnerships", negative: "Domineering partner" },
    hour: { meaning: "Challenging children", positive: "Strong offspring", negative: "Conflict with children" },
  },
  DR: {
    year: { meaning: "Mother's influence", positive: "Nurturing upbringing", negative: "Over-protected childhood" },
    month: { meaning: "Academic career", positive: "Teaching or scholarly work", negative: "Overly theoretical" },
    day: { meaning: "Supportive partner", positive: "Nurturing relationship", negative: "Dependency on others" },
    hour: { meaning: "Wisdom in age", positive: "Knowledgeable elder", negative: "Overly cautious" },
  },
  IR: {
    year: { meaning: "Unconventional upbringing", positive: "Unique perspective", negative: "Lonely childhood" },
    month: { meaning: "Alternative career", positive: "Unique profession", negative: "Career uncertainty" },
    day: { meaning: "Independent thinker", positive: "Original ideas", negative: "Social isolation" },
    hour: { meaning: "Spiritual later life", positive: "Contemplative old age", negative: "Isolation in retirement" },
  },
};

// ---------------------------------------------------------------------------
// Meaning Translations (Indonesian)
// ---------------------------------------------------------------------------

export const MEANING_TRANSLATIONS_ID: Record<string, string> = {
  "Siblings help in childhood": "Saudara membantu di masa kecil",
  "Peers and colleagues": "Rekan dan kolega",
  "Self-identity": "Identitas diri",
  "Creative childhood": "Masa kecil kreatif",
  "Creative career": "Karir kreatif",
  "Family wealth": "Kekayaan keluarga",
  "Steady income": "Pendapatan tetap",
  "Authority position": "Posisi otoritas",
  "Mother's influence": "Pengaruh ibu",
  "Academic career": "Karir akademis",
};

// ---------------------------------------------------------------------------
// Interaction Impact Analysis
// ---------------------------------------------------------------------------

export function analyzeInteractionImpact(
  tenGodCode: string,
  interactionType: string,
  pillar: string
): { impact_en: string; impact_zh: string; severity: string } {
  const meaning = TEN_GOD_PILLAR_MEANINGS[tenGodCode]?.[pillar];
  if (!meaning) {
    return {
      impact_en: `${tenGodCode} in ${pillar} pillar affected by ${interactionType}`,
      impact_zh: `${tenGodCode}在${pillar}柱受到${interactionType}影響`,
      severity: 'low',
    };
  }

  const isNegativeInteraction = ['clash', 'punishment', 'harm', 'destruction', 'stem_conflict'].includes(interactionType);

  if (isNegativeInteraction) {
    return {
      impact_en: `${meaning.meaning} disrupted by ${interactionType}: ${meaning.negative}`,
      impact_zh: `${meaning.meaning}被${interactionType}擾亂：${meaning.negative}`,
      severity: pillar === 'day' ? 'high' : 'moderate',
    };
  }

  return {
    impact_en: `${meaning.meaning} enhanced by ${interactionType}: ${meaning.positive}`,
    impact_zh: `${meaning.meaning}被${interactionType}增強：${meaning.positive}`,
    severity: 'low',
  };
}

// ---------------------------------------------------------------------------
// Main Analysis Function
// ---------------------------------------------------------------------------

export interface TenGodsDetailResult {
  pillar_analysis: Array<{
    position: string;
    ten_god: string;
    ten_god_info: { en: string; zh: string };
    meaning: PillarMeaningEntry | null;
    aspect: string;
    domains: string[];
  }>;
  dominant_aspects: string[];
  summary_en: string;
  summary_zh: string;
}

export function generateTenGodsDetail(
  daymasterStem: StemName,
  pillarStems: Record<string, StemName>,
  interactions?: Record<string, any>
): TenGodsDetailResult {
  const pillarAnalysis: Array<{
    position: string;
    ten_god: string;
    ten_god_info: { en: string; zh: string };
    meaning: PillarMeaningEntry | null;
    aspect: string;
    domains: string[];
  }> = [];

  const aspectCounts: Record<string, number> = {};

  for (const [position, stem] of Object.entries(pillarStems)) {
    if (position === 'day') continue; // Skip Day Master itself

    const tenGodCode = getTenGodForStem(daymasterStem, stem);
    if (!tenGodCode) continue;

    const mapping = TEN_GOD_ASPECT_MAPPING[tenGodCode];
    const meaning = TEN_GOD_PILLAR_MEANINGS[tenGodCode]?.[position] ?? null;

    const info = mapping
      ? { en: mapping.en, zh: mapping.zh }
      : { en: tenGodCode, zh: tenGodCode };

    const aspect = mapping?.aspect ?? 'unknown';
    const domains = mapping?.domains ?? [];

    aspectCounts[aspect] = (aspectCounts[aspect] ?? 0) + 1;

    pillarAnalysis.push({
      position,
      ten_god: tenGodCode,
      ten_god_info: info,
      meaning,
      aspect,
      domains,
    });
  }

  // Find dominant aspects
  const dominantAspects = Object.entries(aspectCounts)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 2)
    .map(([aspect]) => aspect);

  const summaryEn = `Ten Gods analysis: ${pillarAnalysis.length} positions analyzed. Dominant aspects: ${dominantAspects.join(', ') || 'balanced'}.`;
  const summaryZh = `十神分析：分析了${pillarAnalysis.length}個位置。主要方面：${dominantAspects.join('、') || '平衡'}。`;

  return {
    pillar_analysis: pillarAnalysis,
    dominant_aspects: dominantAspects,
    summary_en: summaryEn,
    summary_zh: summaryZh,
  };
}
