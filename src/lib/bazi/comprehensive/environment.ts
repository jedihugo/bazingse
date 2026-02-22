import 'server-only';

// =============================================================================
// ENVIRONMENTAL QI & RELOCATION ASSESSMENT (过江龙)
// =============================================================================

import type { BranchName } from '../core';
import { ELEMENT_CHINESE } from '../derived';
import type { EnvironmentAssessment, ChartData, StrengthAssessment } from './models';
import { calculateWuxing, wuxingToElementCounts, type WuxingResult } from '../wuxing/calculator';
import { chartToWuxingInput } from './wuxing-bridge';
import { YI_MA_LOOKUP, getVoidBranches } from './shen-sha';

// =============================================================================
// DIRECTIONAL ELEMENTS
// =============================================================================

const DIRECTION_ELEMENTS: Record<string, string> = {
  East: "Wood", South: "Fire", West: "Metal", North: "Water",
  Center: "Earth", Southeast: "Wood", Southwest: "Earth",
  Northeast: "Earth", Northwest: "Metal",
};

const ELEMENT_DIRECTIONS: Record<string, string[]> = {
  Wood: ["East", "Southeast"],
  Fire: ["South"],
  Earth: ["Center", "Southwest", "Northeast"],
  Metal: ["West", "Northwest"],
  Water: ["North"],
};

const ELEMENT_CLIMATES: Record<string, string> = {
  Wood: "warm and humid, with abundant vegetation",
  Fire: "hot, tropical, sunny climate",
  Earth: "moderate, stable climate with good agriculture",
  Metal: "cool, dry, crisp air climate",
  Water: "cold, coastal, or near bodies of water",
};

const ELEMENT_GEOGRAPHY: Record<string, string> = {
  Wood: "forested areas, near parks and greenery",
  Fire: "tropical regions, elevated or volcanic areas",
  Earth: "flat plains, agricultural regions, central locations",
  Metal: "mountainous regions, mineral-rich areas, western areas",
  Water: "coastal cities, river valleys, island nations, lakeside",
};

// =============================================================================
// CROSSING WATER (过江龙) ASSESSMENT
// =============================================================================

function assessCrossingWater(
  chart: ChartData,
  strength: StrengthAssessment,
  elemCounts: Record<string, number>,
): { score: number; verdict: string; benefit: boolean; reason: string; factors: string[] } {
  let score = 0;
  const factors: string[] = [];
  const dmElement = chart.dm_element;

  // 1. DM needs Water
  if (strength.favorable_elements.includes("Water")) {
    score += 1;
    factors.push("Water is a favorable element for this chart");
  }

  if (dmElement === "Water" && (strength.verdict === "weak" || strength.verdict === "extremely_weak")) {
    score += 1;
    factors.push("Weak Water DM directly benefits from Water environment");
  }

  // 2. Water depleted in natal chart
  const waterCount = elemCounts["Water"] ?? 0;
  const fireCount = elemCounts["Fire"] ?? 0;
  const earthCount = elemCounts["Earth"] ?? 0;

  if (waterCount < 1.0) {
    score += 1;
    factors.push(`Water element severely depleted (count: ${waterCount.toFixed(1)})`);
  } else if (waterCount < 2.0) {
    factors.push(`Water element below average (count: ${waterCount.toFixed(1)})`);
  }

  // 3. Fire/Earth dominance
  if (fireCount + earthCount > 5.0) {
    score += 1;
    factors.push(`Fire+Earth dominance (${fireCount.toFixed(1)}+${earthCount.toFixed(1)}) needs Water to balance`);
  }

  // 4. Yi Ma presence (travel star)
  let hasYiMa = false;
  for (const basePos of ["year", "day"]) {
    const baseBr = chart.pillars[basePos].branch;
    const target = YI_MA_LOOKUP[baseBr];
    if (target) {
      const natalBranches = new Set(
        ["year", "month", "day", "hour"].map(p => chart.pillars[p].branch));
      if (natalBranches.has(target as BranchName)) {
        hasYiMa = true;
        break;
      }
    }
  }
  if (hasYiMa) {
    score += 1;
    factors.push("Traveling Horse (驿马) present = natural traveler");
  }

  let verdict: string;
  let benefit: boolean;
  let reason: string;

  if (score >= 4) {
    verdict = "strong";
    benefit = true;
    reason = "This chart strongly benefits from crossing water. Relocation abroad or near major bodies of water is a PRIMARY life remedy.";
  } else if (score >= 2) {
    verdict = "moderate";
    benefit = true;
    reason = "This chart moderately benefits from crossing water. Living near water or abroad will significantly help.";
  } else {
    verdict = "not_applicable";
    benefit = false;
    reason = "Crossing water is neutral for this chart. Relocation is not a significant remedy.";
  }

  return { score, verdict, benefit, reason, factors };
}

// =============================================================================
// FAVORABLE DIRECTIONS
// =============================================================================

function getFavorableDirections(strength: StrengthAssessment): {
  favorable: string[];
  unfavorable: string[];
} {
  const favorable: string[] = [];
  const unfavorable: string[] = [];

  for (const elem of strength.favorable_elements) {
    const dirs = ELEMENT_DIRECTIONS[elem] ?? [];
    favorable.push(...dirs);
  }

  for (const elem of strength.unfavorable_elements) {
    const dirs = ELEMENT_DIRECTIONS[elem] ?? [];
    unfavorable.push(...dirs);
  }

  // Deduplicate preserving order
  return {
    favorable: [...new Map(favorable.map(d => [d, d])).values()],
    unfavorable: [...new Map(unfavorable.map(d => [d, d])).values()],
  };
}

// =============================================================================
// IDEAL ENVIRONMENT
// =============================================================================

function getIdealEnvironment(strength: StrengthAssessment): {
  ideal_climate: string;
  ideal_geography: string;
  useful_element: string;
  useful_element_chinese: string;
} {
  const useful = strength.useful_god;
  return {
    ideal_climate: ELEMENT_CLIMATES[useful] ?? "moderate climate",
    ideal_geography: ELEMENT_GEOGRAPHY[useful] ?? "balanced environment",
    useful_element: useful,
    useful_element_chinese: ELEMENT_CHINESE[useful as keyof typeof ELEMENT_CHINESE] ?? "",
  };
}

// =============================================================================
// VOID DISRUPTION ASSESSMENT
// =============================================================================

function assessVoidDisruption(chart: ChartData): string[] {
  const voidBrs = getVoidBranches(chart);
  const disrupted: string[] = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    if (voidBrs.has(chart.pillars[pos].branch)) {
      disrupted.push(pos);
    }
  }
  return disrupted;
}

// =============================================================================
// MASTER ENVIRONMENT ASSESSMENT
// =============================================================================

export function assessEnvironment(
  chart: ChartData,
  strength: StrengthAssessment,
  wuxingResult?: WuxingResult,
): EnvironmentAssessment {
  // Compute wuxing result if not provided
  if (!wuxingResult) {
    wuxingResult = calculateWuxing(chartToWuxingInput(chart));
  }
  const elemCounts = wuxingToElementCounts(wuxingResult);
  const cw = assessCrossingWater(chart, strength, elemCounts);
  const dirs = getFavorableDirections(strength);
  const env = getIdealEnvironment(strength);
  const voidPalaces = assessVoidDisruption(chart);

  let locationRecs: string;
  if (cw.benefit) {
    locationRecs = `Relocating abroad or near water is strongly recommended. Best directions: ${dirs.favorable.join(", ")}. Ideal environment: ${env.ideal_climate}. Best geography: ${env.ideal_geography}.`;
  } else {
    locationRecs = `Relocation is neutral. If moving, favor these directions: ${dirs.favorable.join(", ")}. Ideal climate: ${env.ideal_climate}.`;
  }

  return {
    crosses_water_benefit: cw.benefit,
    crosses_water_reason: cw.reason,
    favorable_directions: dirs.favorable,
    unfavorable_directions: dirs.unfavorable,
    ideal_climate: env.ideal_climate,
    ideal_geography: env.ideal_geography,
    guo_jiang_long_score: cw.score,
    guo_jiang_long_verdict: cw.verdict,
    guo_jiang_long_factors: cw.factors,
    void_disruption_palaces: voidPalaces,
    location_recommendations: locationRecs,
  };
}
