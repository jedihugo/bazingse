
// =============================================================================
// ELEMENT REMEDIES
// =============================================================================
// Remedy recommendations based on element balance.
// Ported from api/library/narrative/remedies.py
// =============================================================================

import type { Element } from '../core';

// ---------------------------------------------------------------------------
// Element Remedy Details
// ---------------------------------------------------------------------------

export interface ElementRemedy {
  colors: string[];
  directions: string[];
  activities: string[];
  foods: string[];
  materials: string[];
  numbers: number[];
  seasons: string[];
}

export const ELEMENT_REMEDIES: Record<Element, ElementRemedy> = {
  Wood: {
    colors: ["green", "teal", "lime"],
    directions: ["East"],
    activities: ["hiking", "gardening", "yoga", "reading", "planning"],
    foods: ["leafy greens", "sour foods", "sprouts", "green tea"],
    materials: ["wood", "bamboo", "paper", "cotton"],
    numbers: [3, 8],
    seasons: ["Spring"],
  },
  Fire: {
    colors: ["red", "orange", "pink", "purple"],
    directions: ["South"],
    activities: ["exercise", "socializing", "public speaking", "cooking", "dancing"],
    foods: ["red foods", "bitter foods", "peppers", "tomatoes"],
    materials: ["candles", "incense", "electronics", "lights"],
    numbers: [2, 7],
    seasons: ["Summer"],
  },
  Earth: {
    colors: ["yellow", "brown", "beige", "ochre"],
    directions: ["Center", "Southwest", "Northeast"],
    activities: ["meditation", "pottery", "cooking", "farming", "organizing"],
    foods: ["root vegetables", "sweet foods", "grains", "squash"],
    materials: ["clay", "stone", "ceramics", "crystals"],
    numbers: [5, 10],
    seasons: ["Late Summer"],
  },
  Metal: {
    colors: ["white", "silver", "gold", "grey"],
    directions: ["West"],
    activities: ["martial arts", "singing", "organizing", "precision crafts", "breathing exercises"],
    foods: ["spicy foods", "white foods", "radish", "ginger"],
    materials: ["metal", "gold", "silver", "copper", "stainless steel"],
    numbers: [4, 9],
    seasons: ["Autumn"],
  },
  Water: {
    colors: ["black", "dark blue", "navy"],
    directions: ["North"],
    activities: ["swimming", "meditation", "writing", "studying", "sleeping well"],
    foods: ["salty foods", "seaweed", "dark foods", "beans", "fish"],
    materials: ["glass", "water features", "mirrors"],
    numbers: [1, 6],
    seasons: ["Winter"],
  },
};

// ---------------------------------------------------------------------------
// Remedy Templates
// ---------------------------------------------------------------------------

export interface RemedyTemplate {
  en: string;
  zh: string;
}

export const REMEDY_TEMPLATES: Record<string, RemedyTemplate> = {
  strengthen: {
    en: "To strengthen {element}: Wear {colors} colors, face {direction}, engage in {activities}. Eat more {foods}. Use {materials} in your environment.",
    zh: "增強{element_zh}：穿戴{colors_zh}色系，朝向{direction_zh}，從事{activities_zh}。多吃{foods_zh}。在環境中使用{materials_zh}。",
  },
  reduce: {
    en: "To balance excess {element}: Reduce exposure to {colors} colors and {direction} direction. Moderate {activities}. Eat less {foods}.",
    zh: "平衡過多的{element_zh}：減少{colors_zh}色系和{direction_zh}方向的接觸。適度{activities_zh}。少吃{foods_zh}。",
  },
  general: {
    en: "General recommendation: Focus on {element} element activities and environment to maintain balance.",
    zh: "一般建議：注重{element_zh}元素的活動和環境以保持平衡。",
  },
};

// ---------------------------------------------------------------------------
// Remedy Generation
// ---------------------------------------------------------------------------

export function generateRemedies(
  elementScores: Record<string, number>,
  daymasterElement: Element
): Array<{ element: Element; type: string; text_en: string; text_zh: string }> {
  const remedies: Array<{ element: Element; type: string; text_en: string; text_zh: string }> = [];
  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);

  if (total === 0) return remedies;

  for (const [element, score] of Object.entries(elementScores)) {
    const percentage = (score / total) * 100;
    const elem = element as Element;
    const remedy = ELEMENT_REMEDIES[elem];
    if (!remedy) continue;

    if (percentage < 15) {
      // Deficient - strengthen
      const built = buildRemedy(elem, 'strengthen', remedy);
      remedies.push(built);
    } else if (percentage > 30) {
      // Excessive - reduce
      const built = buildRemedy(elem, 'reduce', remedy);
      remedies.push(built);
    }
  }

  return remedies;
}

function buildRemedy(
  element: Element,
  type: string,
  remedy: ElementRemedy
): { element: Element; type: string; text_en: string; text_zh: string } {
  const template = REMEDY_TEMPLATES[type] ?? REMEDY_TEMPLATES.general;

  const ELEMENT_CHINESE: Record<Element, string> = {
    Wood: "木", Fire: "火", Earth: "土", Metal: "金", Water: "水",
  };

  let textEn = template.en;
  let textZh = template.zh;

  const replacements: Record<string, string> = {
    element: element,
    element_zh: ELEMENT_CHINESE[element],
    colors: remedy.colors.slice(0, 2).join(", "),
    colors_zh: remedy.colors.slice(0, 2).join("、"),
    direction: remedy.directions[0],
    direction_zh: remedy.directions[0],
    activities: remedy.activities.slice(0, 3).join(", "),
    activities_zh: remedy.activities.slice(0, 3).join("、"),
    foods: remedy.foods.slice(0, 2).join(", "),
    foods_zh: remedy.foods.slice(0, 2).join("、"),
    materials: remedy.materials.slice(0, 2).join(", "),
    materials_zh: remedy.materials.slice(0, 2).join("、"),
  };

  for (const [key, value] of Object.entries(replacements)) {
    textEn = textEn.replaceAll(`{${key}}`, value);
    textZh = textZh.replaceAll(`{${key}}`, value);
  }

  return { element, type, text_en: textEn, text_zh: textZh };
}

export function getQuickRemedies(
  weakElements: Element[]
): Record<Element, { colors: string[]; activities: string[] }> {
  const result: Record<string, { colors: string[]; activities: string[] }> = {};

  for (const elem of weakElements) {
    const remedy = ELEMENT_REMEDIES[elem];
    if (remedy) {
      result[elem] = {
        colors: remedy.colors.slice(0, 3),
        activities: remedy.activities.slice(0, 3),
      };
    }
  }

  return result as Record<Element, { colors: string[]; activities: string[] }>;
}
