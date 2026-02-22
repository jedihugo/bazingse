import 'server-only';

// =============================================================================
// WEALTH ANALYSIS
// =============================================================================
// Wealth potential analysis from BaZi element interactions.
// Ported from api/library/life_aspects/wealth.py
// =============================================================================

import type { Element } from '../core';
import { ELEMENT_CONTROLS } from './base';

// ---------------------------------------------------------------------------
// Wealth Constants
// ---------------------------------------------------------------------------

export const OPPORTUNITY_WEIGHTS: Record<string, number> = {
  three_meetings: 3.0,
  three_combinations: 2.5,
  six_harmonies: 2.0,
  half_meetings: 1.5,
  half_combinations: 1.2,
  arched_combinations: 0.8,
  stem_combination: 2.0,
};

export const RISK_WEIGHTS: Record<string, number> = {
  clash: 2.5,
  punishment: 2.0,
  harm: 1.5,
  destruction: 1.0,
  stem_conflict: 1.5,
};

// ---------------------------------------------------------------------------
// Property Storage
// ---------------------------------------------------------------------------

export const PROPERTY_STORAGE_BRANCHES: Record<string, string> = {
  Chen: "Water",
  Xu: "Fire",
  Chou: "Metal",
  Wei: "Wood",
};

export const PROPERTY_INDICATORS: Record<string, number> = {
  storage_present: 2.0,
  storage_clashed: -1.5,
  storage_combined: 1.0,
};

// ---------------------------------------------------------------------------
// Wealth Ten Gods
// ---------------------------------------------------------------------------

export const WEALTH_TEN_GODS = ['DW', 'IW'] as const;

export const WEALTH_INDICATORS: Record<string, { en: string; zh: string; weight: number }> = {
  DW: { en: "Direct Wealth (steady income)", zh: "正財（穩定收入）", weight: 1.0 },
  IW: { en: "Indirect Wealth (windfall/speculation)", zh: "偏財（橫財/投機）", weight: 1.2 },
};

// ---------------------------------------------------------------------------
// DM Wealth Element
// ---------------------------------------------------------------------------

export const DM_WEALTH_ELEMENT: Record<Element, Element> = {
  Wood: "Earth",   // Wood controls Earth -> Earth is Wood's wealth
  Fire: "Metal",   // Fire controls Metal -> Metal is Fire's wealth
  Earth: "Water",  // Earth controls Water -> Water is Earth's wealth
  Metal: "Wood",   // Metal controls Wood -> Wood is Metal's wealth
  Water: "Fire",   // Water controls Fire -> Fire is Water's wealth
};

// ---------------------------------------------------------------------------
// Wealth Analysis Result
// ---------------------------------------------------------------------------

export interface WealthAnalysisResult {
  wealth_element: Element;
  wealth_score: number;
  opportunity_score: number;
  risk_score: number;
  net_score: number;
  outlook: string;
  has_storage: boolean;
  storage_clashed: boolean;
  wealth_ten_gods_count: number;
  description_en: string;
  description_zh: string;
  recommendations_en: string[];
  recommendations_zh: string[];
}

// ---------------------------------------------------------------------------
// Main Analysis Function
// ---------------------------------------------------------------------------

export function generateWealthAnalysis(
  elementScores: Record<string, number>,
  seasonalStates: Record<string, string>,
  interactions: Record<string, any>,
  daymasterElement: Element,
  tenGods?: Array<Record<string, any>>,
  wealthStorage?: Record<string, any>
): WealthAnalysisResult {
  const wealthElement = DM_WEALTH_ELEMENT[daymasterElement];

  // Count wealth ten gods
  let wealthTenGodsCount = 0;
  if (tenGods) {
    for (const tg of tenGods) {
      if (WEALTH_TEN_GODS.includes(tg.abbreviation as any)) {
        wealthTenGodsCount++;
      }
    }
  }

  // Calculate opportunity score from positive interactions
  let opportunityScore = 0;
  let riskScore = 0;

  for (const [intId, intData] of Object.entries(interactions)) {
    if (typeof intData === 'string') continue;
    const parts = intId.split('~');
    const intType = parts[0]?.toLowerCase() ?? '';

    // Check if this interaction involves wealth element
    const element = intData.element;
    const isWealthRelated = element === wealthElement;

    if (OPPORTUNITY_WEIGHTS[intType] !== undefined) {
      const weight = OPPORTUNITY_WEIGHTS[intType];
      opportunityScore += weight * (isWealthRelated ? 1.5 : 0.5);
    }

    if (RISK_WEIGHTS[intType] !== undefined) {
      const weight = RISK_WEIGHTS[intType];
      riskScore += weight * (isWealthRelated ? 1.5 : 0.5);
    }
  }

  // Wealth element strength
  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);
  const wealthPct = total > 0 ? ((elementScores[wealthElement] ?? 0) / total) * 100 : 0;
  const wealthScore = wealthPct;

  // Storage
  const hasStorage = wealthStorage?.has_storage ?? false;
  const storageClashed = wealthStorage?.is_clashed ?? false;

  if (hasStorage) {
    opportunityScore += PROPERTY_INDICATORS.storage_present;
    if (storageClashed) {
      riskScore += Math.abs(PROPERTY_INDICATORS.storage_clashed);
    }
  }

  // Ten gods bonus
  opportunityScore += wealthTenGodsCount * 1.5;

  // Net score
  const netScore = opportunityScore - riskScore;

  // Outlook
  const outlook = netScore > 3 ? 'positive'
    : netScore < -2 ? 'negative'
    : 'neutral';

  // Generate text
  const descEn = `Wealth element: ${wealthElement} (${wealthPct.toFixed(1)}%). Opportunity score: ${opportunityScore.toFixed(1)}, Risk score: ${riskScore.toFixed(1)}. ${wealthTenGodsCount} wealth Ten Gods present.${hasStorage ? ' Wealth storage present.' : ''}${storageClashed ? ' Storage clashed (vault opened).' : ''}`;
  const descZh = `財星元素：${wealthElement}（${wealthPct.toFixed(1)}%）。機會分數：${opportunityScore.toFixed(1)}，風險分數：${riskScore.toFixed(1)}。${wealthTenGodsCount}個財星十神。${hasStorage ? '有財庫。' : ''}${storageClashed ? '財庫被沖（庫門打開）。' : ''}`;

  const recsEn: string[] = [];
  const recsZh: string[] = [];

  if (outlook === 'positive') {
    recsEn.push("Favorable wealth outlook. Good period for investments and business expansion.");
    recsZh.push("財運有利。適合投資和業務擴展。");
  } else if (outlook === 'negative') {
    recsEn.push("Financial caution advised. Avoid major investments and reduce risk exposure.");
    recsZh.push("建議財務謹慎。避免大額投資，降低風險敞口。");
  } else {
    recsEn.push("Neutral wealth outlook. Maintain steady financial practices.");
    recsZh.push("財運中性。保持穩健的財務實踐。");
  }

  return {
    wealth_element: wealthElement,
    wealth_score: Math.round(wealthScore * 10) / 10,
    opportunity_score: Math.round(opportunityScore * 10) / 10,
    risk_score: Math.round(riskScore * 10) / 10,
    net_score: Math.round(netScore * 10) / 10,
    outlook,
    has_storage: hasStorage,
    storage_clashed: storageClashed,
    wealth_ten_gods_count: wealthTenGodsCount,
    description_en: descEn,
    description_zh: descZh,
    recommendations_en: recsEn,
    recommendations_zh: recsZh,
  };
}
