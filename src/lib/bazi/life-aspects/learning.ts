
// =============================================================================
// LEARNING ANALYSIS
// =============================================================================
// Education and learning potential analysis from BaZi elements.
// Ported from api/library/life_aspects/learning.py
// =============================================================================

import type { Element } from '../core';

// ---------------------------------------------------------------------------
// Learning Ten Gods
// ---------------------------------------------------------------------------

export const LEARNING_TEN_GODS = ['DR', 'IR', 'EG'] as const;

export const LEARNING_INDICATORS: Record<string, { en: string; zh: string; weight: number }> = {
  DR: { en: "Direct Resource (formal education)", zh: "正印（正規教育）", weight: 1.5 },
  IR: { en: "Indirect Resource (unconventional learning)", zh: "偏印（非傳統學習）", weight: 1.2 },
  EG: { en: "Eating God (creative expression)", zh: "食神（創意表達）", weight: 1.0 },
};

// ---------------------------------------------------------------------------
// DM Resource Element
// ---------------------------------------------------------------------------

export const DM_RESOURCE_ELEMENT: Record<Element, Element> = {
  Wood: "Water",
  Fire: "Wood",
  Earth: "Fire",
  Metal: "Earth",
  Water: "Metal",
};

export const DM_OUTPUT_ELEMENT: Record<Element, Element> = {
  Wood: "Fire",
  Fire: "Earth",
  Earth: "Metal",
  Metal: "Water",
  Water: "Wood",
};

// ---------------------------------------------------------------------------
// Learning Analysis Result
// ---------------------------------------------------------------------------

export interface LearningAnalysisResult {
  resource_element: Element;
  output_element: Element;
  resource_score: number;
  output_score: number;
  learning_style: string;
  learning_ten_gods_count: number;
  strengths_en: string[];
  strengths_zh: string[];
  description_en: string;
  description_zh: string;
}

// ---------------------------------------------------------------------------
// Main Analysis Function
// ---------------------------------------------------------------------------

export function generateLearningAnalysis(
  elementScores: Record<string, number>,
  seasonalStates: Record<string, string>,
  daymasterElement: Element,
  tenGods?: Array<Record<string, any>>
): LearningAnalysisResult {
  const resourceElement = DM_RESOURCE_ELEMENT[daymasterElement];
  const outputElement = DM_OUTPUT_ELEMENT[daymasterElement];

  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);
  const resourcePct = total > 0 ? ((elementScores[resourceElement] ?? 0) / total) * 100 : 0;
  const outputPct = total > 0 ? ((elementScores[outputElement] ?? 0) / total) * 100 : 0;

  // Count learning ten gods
  let learningTenGodsCount = 0;
  if (tenGods) {
    for (const tg of tenGods) {
      if (LEARNING_TEN_GODS.includes(tg.abbreviation as any)) {
        learningTenGodsCount++;
      }
    }
  }

  // Determine learning style
  let learningStyle: string;
  if (resourcePct > outputPct + 5) {
    learningStyle = 'absorptive'; // Strong resource = good at absorbing knowledge
  } else if (outputPct > resourcePct + 5) {
    learningStyle = 'expressive'; // Strong output = good at expressing/applying
  } else {
    learningStyle = 'balanced';
  }

  const strengthsEn: string[] = [];
  const strengthsZh: string[] = [];

  if (resourcePct > 20) {
    strengthsEn.push("Strong learning ability - absorbs knowledge easily");
    strengthsZh.push("學習能力強 - 容易吸收知識");
  }
  if (outputPct > 20) {
    strengthsEn.push("Strong creative expression - applies knowledge well");
    strengthsZh.push("創意表達強 - 善於應用知識");
  }
  if (learningTenGodsCount >= 2) {
    strengthsEn.push("Multiple learning stars present - academic potential");
    strengthsZh.push("多個學習星出現 - 有學術潛力");
  }

  if (strengthsEn.length === 0) {
    strengthsEn.push("Practical learning style - learns through experience");
    strengthsZh.push("實踐型學習風格 - 通過經驗學習");
  }

  const descEn = `Resource element: ${resourceElement} (${resourcePct.toFixed(1)}%). Output element: ${outputElement} (${outputPct.toFixed(1)}%). Learning style: ${learningStyle}. ${learningTenGodsCount} learning Ten Gods present.`;
  const descZh = `印星元素：${resourceElement}（${resourcePct.toFixed(1)}%）。食傷元素：${outputElement}（${outputPct.toFixed(1)}%）。學習風格：${learningStyle}。${learningTenGodsCount}個學習十神。`;

  return {
    resource_element: resourceElement,
    output_element: outputElement,
    resource_score: Math.round(resourcePct * 10) / 10,
    output_score: Math.round(outputPct * 10) / 10,
    learning_style: learningStyle,
    learning_ten_gods_count: learningTenGodsCount,
    strengths_en: strengthsEn,
    strengths_zh: strengthsZh,
    description_en: descEn,
    description_zh: descZh,
  };
}
