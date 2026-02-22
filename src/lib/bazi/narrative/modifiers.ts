import 'server-only';

// =============================================================================
// NARRATIVE MODIFIERS
// =============================================================================
// Element balance analysis and modifiers for narrative generation.
// Ported from api/library/narrative/modifiers.py
// =============================================================================

import type { Element, StemName } from '../core';
import { STEMS } from '../core';

// ---------------------------------------------------------------------------
// Balance Thresholds
// ---------------------------------------------------------------------------

export const BALANCE_THRESHOLDS = {
  excess: 30,      // Element is excessive above this %
  deficient: 10,   // Element is deficient below this %
  balanced_low: 15,
  balanced_high: 25,
} as const;

// ---------------------------------------------------------------------------
// Ten Gods for Element Mapping
// ---------------------------------------------------------------------------

export const TEN_GODS_FOR_ELEMENT: Record<string, Record<Element, string>> = {
  self: {
    Wood: "Wood", Fire: "Fire", Earth: "Earth", Metal: "Metal", Water: "Water",
  },
  resource: {
    Wood: "Water", Fire: "Wood", Earth: "Fire", Metal: "Earth", Water: "Metal",
  },
  output: {
    Wood: "Fire", Fire: "Earth", Earth: "Metal", Metal: "Water", Water: "Wood",
  },
  wealth: {
    Wood: "Earth", Fire: "Metal", Earth: "Water", Metal: "Wood", Water: "Fire",
  },
  authority: {
    Wood: "Metal", Fire: "Water", Earth: "Wood", Metal: "Fire", Water: "Earth",
  },
};

// ---------------------------------------------------------------------------
// Ten Gods Excess Meaning
// ---------------------------------------------------------------------------

export const TEN_GODS_EXCESS_MEANING: Record<string, { en: string; zh: string }> = {
  self: {
    en: "Strong self but risk of stubbornness",
    zh: "自我強大但有固執的風險",
  },
  resource: {
    en: "Abundant resources but possible over-reliance",
    zh: "資源豐富但可能過度依賴",
  },
  output: {
    en: "Creative energy but risk of exhaustion",
    zh: "創造力充沛但有耗竭的風險",
  },
  wealth: {
    en: "Wealth potential but possible greed",
    zh: "財富潛力但可能貪婪",
  },
  authority: {
    en: "Strong discipline but risk of oppression",
    zh: "紀律嚴明但有壓迫的風險",
  },
};

// ---------------------------------------------------------------------------
// Element Cycles
// ---------------------------------------------------------------------------

export const ELEMENT_GENERATES: Record<Element, Element> = {
  Wood: "Fire",
  Fire: "Earth",
  Earth: "Metal",
  Metal: "Water",
  Water: "Wood",
};

export const ELEMENT_CONTROLS: Record<Element, Element> = {
  Wood: "Earth",
  Fire: "Metal",
  Earth: "Water",
  Metal: "Wood",
  Water: "Fire",
};

// ---------------------------------------------------------------------------
// Element Balance Context
// ---------------------------------------------------------------------------

export interface ElementBalanceContext {
  element: Element;
  percentage: number;
  status: 'excess' | 'deficient' | 'balanced';
  ten_god_role: string;
  meaning_en: string;
  meaning_zh: string;
}

export function getElementBalanceContext(
  elementScores: Record<string, number>,
  daymasterElement: Element
): ElementBalanceContext[] {
  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);
  if (total === 0) return [];

  const results: ElementBalanceContext[] = [];

  for (const [element, score] of Object.entries(elementScores)) {
    const elem = element as Element;
    const percentage = (score / total) * 100;

    let status: 'excess' | 'deficient' | 'balanced';
    if (percentage > BALANCE_THRESHOLDS.excess) {
      status = 'excess';
    } else if (percentage < BALANCE_THRESHOLDS.deficient) {
      status = 'deficient';
    } else {
      status = 'balanced';
    }

    // Determine ten god role
    const tenGodRole = determineTenGodRole(elem, daymasterElement);

    // Get meaning
    const meaning = status === 'balanced'
      ? { en: `${element} is balanced`, zh: `${element}平衡` }
      : status === 'excess'
        ? TEN_GODS_EXCESS_MEANING[tenGodRole] ?? { en: "Excess energy", zh: "能量過剩" }
        : { en: `${element} needs strengthening`, zh: `${element}需要加強` };

    results.push({
      element: elem,
      percentage: Math.round(percentage * 10) / 10,
      status,
      ten_god_role: tenGodRole,
      meaning_en: meaning.en,
      meaning_zh: meaning.zh,
    });
  }

  return results;
}

function determineTenGodRole(element: Element, daymasterElement: Element): string {
  if (element === daymasterElement) return 'self';

  for (const [role, mapping] of Object.entries(TEN_GODS_FOR_ELEMENT)) {
    if (mapping[daymasterElement] === element) return role;
  }

  return 'self';
}

// ---------------------------------------------------------------------------
// Modifiers
// ---------------------------------------------------------------------------

export function applyElementModifiers(
  narrativeText: string,
  elementScores: Record<string, number>,
  daymasterElement: Element
): string {
  const context = getElementBalanceContext(elementScores, daymasterElement);
  const modifiers: string[] = [];

  for (const ctx of context) {
    if (ctx.status === 'excess') {
      modifiers.push(`[${ctx.element} excess: ${ctx.meaning_en}]`);
    } else if (ctx.status === 'deficient') {
      modifiers.push(`[${ctx.element} deficient: ${ctx.meaning_en}]`);
    }
  }

  if (modifiers.length > 0) {
    return `${narrativeText}\n\nElement Balance Notes: ${modifiers.join("; ")}`;
  }

  return narrativeText;
}

export function applyShenShaModifiers(
  narrativeText: string,
  shenShaList: Array<{ name: string; description: string }>
): string {
  if (shenShaList.length === 0) return narrativeText;

  const notes = shenShaList
    .map((s) => `[${s.name}: ${s.description}]`)
    .join("; ");

  return `${narrativeText}\n\nShen Sha Notes: ${notes}`;
}

// ---------------------------------------------------------------------------
// Helper: Stems to Elements
// ---------------------------------------------------------------------------

export function stemsToElements(stems: StemName[]): Record<Element, number> {
  const totals: Record<string, number> = {
    Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0,
  };

  for (const stem of stems) {
    const data = STEMS[stem];
    if (data) {
      totals[data.element] = (totals[data.element] ?? 0) + 1;
    }
  }

  return totals as Record<Element, number>;
}

// ---------------------------------------------------------------------------
// Determine Favorable Elements
// ---------------------------------------------------------------------------

export function determineFavorableElements(
  daymasterElement: Element,
  dmStrength: 'strong' | 'weak' | 'balanced'
): Element[] {
  if (dmStrength === 'weak') {
    // Weak DM needs: resource (produces DM) and self (same element)
    const resource = Object.entries(ELEMENT_GENERATES).find(
      ([, target]) => target === daymasterElement
    );
    const resourceElem = resource ? resource[0] as Element : daymasterElement;
    return [daymasterElement, resourceElem];
  } else if (dmStrength === 'strong') {
    // Strong DM needs: output (DM produces), wealth (DM controls), authority (controls DM)
    const output = ELEMENT_GENERATES[daymasterElement];
    const wealth = ELEMENT_CONTROLS[daymasterElement];
    return [output, wealth];
  }

  // Balanced: moderate approach
  return [daymasterElement];
}
