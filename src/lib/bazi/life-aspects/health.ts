import 'server-only';

// =============================================================================
// HEALTH ANALYSIS
// =============================================================================
// TCM-based health analysis from BaZi element interactions.
// Ported from api/library/life_aspects/health.py
// =============================================================================

import type { Element } from '../core';
import { ELEMENT_CONTROLS, ORGAN_SYSTEMS, BODY_PARTS } from './base';

// ---------------------------------------------------------------------------
// Element-Organ Mapping (TCM)
// ---------------------------------------------------------------------------

export interface OrganMapping {
  zang: string;
  fu: string;
  body_parts: string[];
  emotion: string;
  season: string;
}

export const ELEMENT_ORGANS: Record<Element, OrganMapping> = {
  Wood: { zang: "Liver", fu: "Gallbladder", body_parts: ["eyes", "tendons", "nails"], emotion: "anger", season: "Spring" },
  Fire: { zang: "Heart", fu: "Small Intestine", body_parts: ["tongue", "blood vessels", "complexion"], emotion: "joy/anxiety", season: "Summer" },
  Earth: { zang: "Spleen", fu: "Stomach", body_parts: ["muscles", "mouth", "lips"], emotion: "worry", season: "Late Summer" },
  Metal: { zang: "Lungs", fu: "Large Intestine", body_parts: ["skin", "nose", "body hair"], emotion: "grief", season: "Autumn" },
  Water: { zang: "Kidneys", fu: "Bladder", body_parts: ["bones", "ears", "head hair", "brain"], emotion: "fear", season: "Winter" },
};

// ---------------------------------------------------------------------------
// Conflict Health Weights
// ---------------------------------------------------------------------------

export const CONFLICT_HEALTH_WEIGHTS: Record<string, number> = {
  clash: 1.0,
  punishment: 0.9,
  harm: 0.7,
  destruction: 0.5,
  stem_conflict: 0.6,
};

// ---------------------------------------------------------------------------
// Seasonal Health Modifier
// ---------------------------------------------------------------------------

export const SEASONAL_HEALTH_MODIFIER: Record<string, number> = {
  Prosperous: 0.5,
  Strengthening: 0.7,
  Resting: 1.0,
  Trapped: 1.5,
  Dead: 2.0,
};

// ---------------------------------------------------------------------------
// Health Analysis Result
// ---------------------------------------------------------------------------

export interface HealthAnalysisResult {
  overall_risk: string;
  risk_score: number;
  vulnerable_elements: Array<{
    element: Element;
    organ: OrganMapping;
    seasonal_state: string;
    vulnerability_score: number;
    description_en: string;
    description_zh: string;
  }>;
  conflict_impacts: Array<{
    type: string;
    elements: Element[];
    weight: number;
    description: string;
  }>;
  recommendations_en: string[];
  recommendations_zh: string[];
}

// ---------------------------------------------------------------------------
// Main Analysis Function
// ---------------------------------------------------------------------------

export function generateHealthAnalysis(
  elementScores: Record<string, number>,
  seasonalStates: Record<string, string>,
  interactions: Record<string, any>,
  daymasterElement: Element
): HealthAnalysisResult {
  const vulnerableElements = detectVulnerableElements(elementScores, seasonalStates);
  const conflictImpacts = aggregateConflictsByElement(interactions);
  const riskScore = calculateRiskScore(vulnerableElements, conflictImpacts);

  const overallRisk = riskScore >= 7 ? 'high'
    : riskScore >= 4 ? 'moderate'
    : 'low';

  const recommendations = generateAnalysisText(
    vulnerableElements,
    conflictImpacts,
    daymasterElement,
    overallRisk
  );

  return {
    overall_risk: overallRisk,
    risk_score: Math.round(riskScore * 10) / 10,
    vulnerable_elements: vulnerableElements,
    conflict_impacts: conflictImpacts,
    recommendations_en: recommendations.en,
    recommendations_zh: recommendations.zh,
  };
}

// ---------------------------------------------------------------------------
// Element Seasonal State Detection
// ---------------------------------------------------------------------------

function getElementSeasonalStates(
  seasonalStates: Record<string, string>
): Record<Element, string> {
  const result: Record<string, string> = {};
  for (const [elem, state] of Object.entries(seasonalStates)) {
    result[elem] = state;
  }
  return result as Record<Element, string>;
}

// ---------------------------------------------------------------------------
// Vulnerability Detection
// ---------------------------------------------------------------------------

function detectVulnerableElements(
  elementScores: Record<string, number>,
  seasonalStates: Record<string, string>
): Array<{
  element: Element;
  organ: OrganMapping;
  seasonal_state: string;
  vulnerability_score: number;
  description_en: string;
  description_zh: string;
}> {
  const results: Array<{
    element: Element;
    organ: OrganMapping;
    seasonal_state: string;
    vulnerability_score: number;
    description_en: string;
    description_zh: string;
  }> = [];

  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);
  if (total === 0) return results;

  for (const [element, score] of Object.entries(elementScores)) {
    const elem = element as Element;
    const percentage = (score / total) * 100;
    const state = seasonalStates[element] ?? 'Resting';
    const modifier = SEASONAL_HEALTH_MODIFIER[state] ?? 1.0;
    const organ = ELEMENT_ORGANS[elem];
    if (!organ) continue;

    // Vulnerability: low score + weak seasonal state
    let vulnScore = 0;
    if (percentage < 15) {
      vulnScore = (15 - percentage) * modifier * 0.5;
    } else if (percentage > 30) {
      vulnScore = (percentage - 30) * 0.3; // Excess also causes issues
    }

    if (vulnScore > 1) {
      results.push({
        element: elem,
        organ,
        seasonal_state: state,
        vulnerability_score: Math.round(vulnScore * 10) / 10,
        description_en: `${organ.zang} (${element}) is ${percentage < 15 ? 'deficient' : 'excessive'} at ${percentage.toFixed(1)}%, ${state} state. Associated body parts: ${organ.body_parts.join(', ')}. Emotional tendency: ${organ.emotion}.`,
        description_zh: `${ORGAN_SYSTEMS[elem].zh_zang}（${element}）${percentage < 15 ? '不足' : '過旺'}（${percentage.toFixed(1)}%），${state}狀態。相關身體部位：${organ.body_parts.join('、')}。情緒傾向：${organ.emotion}。`,
      });
    }
  }

  results.sort((a, b) => b.vulnerability_score - a.vulnerability_score);
  return results;
}

// ---------------------------------------------------------------------------
// Conflict Aggregation
// ---------------------------------------------------------------------------

function aggregateConflictsByElement(
  interactions: Record<string, any>
): Array<{
  type: string;
  elements: Element[];
  weight: number;
  description: string;
}> {
  const results: Array<{
    type: string;
    elements: Element[];
    weight: number;
    description: string;
  }> = [];

  for (const [intId, intData] of Object.entries(interactions)) {
    if (typeof intData === 'string') continue;

    const parts = intId.split('~');
    const intType = parts[0]?.toLowerCase() ?? '';

    const weight = CONFLICT_HEALTH_WEIGHTS[intType];
    if (weight === undefined) continue;

    const element = intData.element;
    const elements = element ? [element as Element] : [];

    results.push({
      type: intType,
      elements,
      weight,
      description: `${intType} interaction affecting ${elements.join(', ') || 'multiple elements'}`,
    });
  }

  return results;
}

// ---------------------------------------------------------------------------
// Risk Score Calculation
// ---------------------------------------------------------------------------

function calculateRiskScore(
  vulnerableElements: Array<{ vulnerability_score: number }>,
  conflictImpacts: Array<{ weight: number }>
): number {
  const vulnTotal = vulnerableElements.reduce((sum, v) => sum + v.vulnerability_score, 0);
  const conflictTotal = conflictImpacts.reduce((sum, c) => sum + c.weight, 0);
  return vulnTotal + conflictTotal;
}

// ---------------------------------------------------------------------------
// Analysis Text
// ---------------------------------------------------------------------------

function generateAnalysisText(
  vulnerableElements: Array<{
    element: Element;
    organ: OrganMapping;
    seasonal_state: string;
  }>,
  conflictImpacts: Array<{ type: string; elements: Element[] }>,
  daymasterElement: Element,
  overallRisk: string
): { en: string[]; zh: string[] } {
  const en: string[] = [];
  const zh: string[] = [];

  if (vulnerableElements.length > 0) {
    const primary = vulnerableElements[0];
    en.push(`Primary vulnerability: ${primary.organ.zang} (${primary.element}). Support through ${primary.organ.season}-associated activities. Manage ${primary.organ.emotion} for better balance.`);
    zh.push(`主要弱點：${ORGAN_SYSTEMS[primary.element].zh_zang}（${primary.element}）。通過與${primary.organ.season}相關的活動來支持。管理${primary.organ.emotion}以獲得更好的平衡。`);
  }

  if (overallRisk === 'high') {
    en.push("Overall health risk is elevated. Consider regular check-ups and preventive care.");
    zh.push("整體健康風險偏高。建議定期檢查和預防保健。");
  }

  if (en.length === 0) {
    en.push("No significant health vulnerabilities detected in the chart.");
    zh.push("命盤中未檢測到明顯的健康弱點。");
  }

  return { en, zh };
}
