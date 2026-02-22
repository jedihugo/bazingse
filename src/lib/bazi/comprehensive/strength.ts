import 'server-only';

// =============================================================================
// DAY MASTER STRENGTH ASSESSMENT ENGINE
// =============================================================================
// DM strength = DM's element percentage of total chart elements.
// ~20% = balanced (100% / 5 elements).
// Branch interactions adjust element weights before computing percentages.
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName, type Element } from '../core';
import { ELEMENT_CYCLES, getAllBranchQi } from '../derived';
import { SEASONAL_ADJUSTMENT } from '../seasonal';
import type { StrengthAssessment, BranchInteraction, ChartData } from './models';
import { HARMONY_PAIRS, THREE_HARMONY_FRAMES, DIRECTIONAL_COMBOS } from './interactions';

// Local helpers matching the pairKey/tripleKey from interactions.ts
function pairKey(a: string, b: string): string {
  return a < b ? `${a}|${b}` : `${b}|${a}`;
}

function tripleKey(a: string, b: string, c: string): string {
  return [a, b, c].sort().join("|");
}

// =============================================================================
// ELEMENT ROLE CLASSIFICATION
// =============================================================================

function _elementRole(dmElement: string, targetElement: string): string {
  /**
   * Classify an element's role relative to the Day Master's element.
   * Returns: "support", "drain", or "neutral" (same=support via companion)
   */
  if (targetElement === dmElement) {
    return "support"; // Same element = companions
  }
  if (ELEMENT_CYCLES.generated_by[dmElement as Element] === targetElement) {
    return "support"; // Resource (generates me)
  }
  // Everything else drains: output, wealth, officer
  return "drain";
}

// =============================================================================
// SEASONAL QI STATE
// =============================================================================

export function getSeasonalState(chart: ChartData): string {
  /** Get the Day Master's seasonal state based on month branch. */
  const monthBranch = chart.pillars["month"].branch;
  const dmElement = chart.dm_element;
  const states = BRANCHES[monthBranch as BranchName].element_states;
  return (states as Record<string, string>)[dmElement] ?? "Resting";
}

export function getSeasonalMultiplier(state: string): number {
  /** Convert seasonal state to multiplier. */
  const key = state.toLowerCase() as keyof typeof SEASONAL_ADJUSTMENT;
  return SEASONAL_ADJUSTMENT[key] ?? 1.0;
}

export function applySeasonalScaling(
  elementCounts: Record<string, number>,
  monthBranch: string,
): Record<string, number> {
  /**
   * Scale element weights by seasonal multipliers based on month branch.
   * The month branch sets the seasonal context for the entire chart.
   */
  const states = BRANCHES[monthBranch as BranchName].element_states;
  const scaled: Record<string, number> = {};
  for (const [elem, count] of Object.entries(elementCounts)) {
    const state = (states as Record<string, string>)[elem] ?? "Resting";
    const key = state.toLowerCase() as keyof typeof SEASONAL_ADJUSTMENT;
    const multiplier = SEASONAL_ADJUSTMENT[key] ?? 1.0;
    scaled[elem] = count * multiplier;
  }
  return scaled;
}

// =============================================================================
// ROOTING ANALYSIS
// =============================================================================

export function checkRooting(chart: ChartData): {
  roots: Array<{
    position: string;
    branch: string;
    stem: string;
    qi_score: number;
    is_exact: boolean;
  }>;
  root_count: number;
  total_root_score: number;
  has_root: boolean;
  has_strong_root: boolean;
} {
  /**
   * Check if the Day Master has roots in the earthly branches.
   * A root = the DM's element appearing in a branch's qi.
   */
  const dm = chart.day_master;
  const dmElement = chart.dm_element;
  const roots: Array<{
    position: string;
    branch: string;
    stem: string;
    qi_score: number;
    is_exact: boolean;
  }> = [];

  for (const pos of ["year", "month", "day", "hour"]) {
    const branch = chart.pillars[pos].branch;
    const branchQi = getAllBranchQi(branch);
    for (const [stem, score] of branchQi) {
      if (STEMS[stem as StemName].element === dmElement) {
        roots.push({
          position: pos,
          branch,
          stem,
          qi_score: score,
          is_exact: stem === dm,
        });
      }
    }
  }

  const totalRootScore = roots.reduce((sum, r) => sum + r.qi_score, 0);
  const hasRoot = roots.length > 0;
  const hasStrongRoot = roots.some(r => r.qi_score >= 50);

  return {
    roots,
    root_count: roots.length,
    total_root_score: totalRootScore,
    has_root: hasRoot,
    has_strong_root: hasStrongRoot,
  };
}

// =============================================================================
// ELEMENT COUNTING
// =============================================================================

export function countElements(chart: ChartData): Record<string, number> {
  /**
   * Count all element weights in the natal chart.
   * Visible stems count full weight (1.0).
   * Hidden stems count proportionally based on qi score (score/100).
   */
  const elementCounts: Record<string, number> = {
    Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0,
  };

  for (const pos of ["year", "month", "day", "hour"]) {
    const pillar = chart.pillars[pos];

    // Heavenly stem = full weight
    const stemElement = STEMS[pillar.stem].element;
    elementCounts[stemElement] += 1.0;

    // Branch qi = weighted by score
    const branchQi = getAllBranchQi(pillar.branch);
    for (const [stem, score] of branchQi) {
      const elem = STEMS[stem as StemName].element;
      elementCounts[elem] += score / 100.0;
    }
  }

  return elementCounts;
}

export function countAllElements(chart: ChartData): Record<string, number> {
  /** Count element weights across ALL pillars (natal + luck + time-period). */
  const elementCounts = countElements(chart); // Start with natal

  // Add luck pillar
  if (chart.luck_pillar) {
    const stemElement = STEMS[chart.luck_pillar.stem].element;
    elementCounts[stemElement] += 1.0;
    for (const [stem, score] of getAllBranchQi(chart.luck_pillar.branch)) {
      elementCounts[STEMS[stem as StemName].element] += score / 100.0;
    }
  }

  // Add time-period pillars
  for (const [, pillar] of Object.entries(chart.time_period_pillars)) {
    const stemElement = STEMS[pillar.stem].element;
    elementCounts[stemElement] += 1.0;
    for (const [stem, score] of getAllBranchQi(pillar.branch)) {
      elementCounts[STEMS[stem as StemName].element] += score / 100.0;
    }
  }

  return elementCounts;
}

export function countSupportVsDrain(chart: ChartData): [number, number] {
  /**
   * Count supporting vs draining element weights.
   * Support = same element + resource element
   * Drain = output + wealth + officer elements
   */
  const dmElement = chart.dm_element;
  const resourceElement = ELEMENT_CYCLES.generated_by[dmElement];

  let support = 0;
  let drain = 0;

  for (const pos of ["year", "month", "day", "hour"]) {
    const pillar = chart.pillars[pos];

    // Heavenly stem
    const stemElem = STEMS[pillar.stem].element;
    if (stemElem === dmElement || stemElem === resourceElement) {
      support += 1.0;
    } else {
      drain += 1.0;
    }

    // Branch qi
    const branchQi = getAllBranchQi(pillar.branch);
    for (const [stem, score] of branchQi) {
      const elem = STEMS[stem as StemName].element;
      const weight = score / 100.0;
      if (elem === dmElement || elem === resourceElement) {
        support += weight;
      } else {
        drain += weight;
      }
    }
  }

  return [support, drain];
}

// =============================================================================
// INTERACTION-ADJUSTED ELEMENT COUNTING
// =============================================================================

// Bonuses for combinations that generate elements.
// Transformed = resulting element present as visible Heavenly Stem.
const INTERACTION_BONUSES: Record<string, { transformed: number; combined: number }> = {
  directional_combo:  { transformed: 2.0, combined: 0.8 },
  three_harmony:      { transformed: 1.5, combined: 0.6 },
  half_three_harmony: { transformed: 0.3, combined: 0.2 },
  harmony:            { transformed: 0.5, combined: 0.2 },
  stem_combination:   { transformed: 1.0, combined: 0.4 },
};

const CLASH_PENALTY = 0.3;

function _getResultingElement(interaction: BranchInteraction): string | null {
  /** Look up the resulting element for a combination interaction. */
  const itype = interaction.interaction_type;
  const branches = interaction.branches;

  if (itype === "directional_combo") {
    if (branches.length === 3) {
      const key = tripleKey(branches[0], branches[1], branches[2]);
      const info = DIRECTIONAL_COMBOS[key];
      return info ? info[0] : null;
    }
    return null;
  } else if (itype === "three_harmony") {
    if (branches.length === 3) {
      const key = tripleKey(branches[0], branches[1], branches[2]);
      return THREE_HARMONY_FRAMES[key] ?? null;
    }
    return null;
  } else if (itype === "half_three_harmony") {
    // Check if these 2 branches are a subset of any frame
    const branchSet = new Set(branches);
    for (const [frameKey, elem] of Object.entries(THREE_HARMONY_FRAMES)) {
      const frameBranches = frameKey.split("|");
      if (frameBranches.every(b => branchSet.has(b)) ||
          [...branchSet].every(b => frameBranches.includes(b))) {
        return elem;
      }
    }
    return null;
  } else if (itype === "harmony") {
    if (branches.length === 2) {
      const key = pairKey(branches[0], branches[1]);
      return HARMONY_PAIRS[key] ?? null;
    }
    return null;
  } else if (itype === "stem_combination") {
    // Stems are stored in branches field; look up combination_element
    const stem1 = branches[0];
    if (stem1 in STEMS) {
      return STEMS[stem1 as StemName].combination_element;
    }
    return null;
  }
  return null;
}

export function adjustElementsForInteractions(
  elementCounts: Record<string, number>,
  interactions: BranchInteraction[],
  chart: ChartData,
): Record<string, number> {
  /**
   * Adjust element counts based on branch interactions.
   * Positive combinations add weight to the resulting element.
   * Transformed (resulting element present as HS) = larger bonus.
   * Clashes reduce both elements slightly.
   */
  const adjusted = { ...elementCounts };

  // Collect visible Heavenly Stem elements
  const hsElements = new Set<string>();
  for (const pos of ["year", "month", "day", "hour"]) {
    hsElements.add(chart.pillars[pos].stem_element as string);
  }

  for (const interaction of interactions) {
    const itype = interaction.interaction_type;

    if (itype in INTERACTION_BONUSES) {
      const resultingElement = _getResultingElement(interaction);
      if (resultingElement) {
        const transformed = hsElements.has(resultingElement);
        const key = transformed ? "transformed" : "combined";
        const bonus = INTERACTION_BONUSES[itype][key];
        adjusted[resultingElement] = (adjusted[resultingElement] ?? 0) + bonus;
      }
    } else if (itype === "clash") {
      for (const br of interaction.branches) {
        if (br in BRANCHES) {
          const elem = BRANCHES[br as BranchName].element;
          adjusted[elem] = Math.max(0, (adjusted[elem] ?? 0) - CLASH_PENALTY);
        }
      }
    }
  }

  return adjusted;
}

// =============================================================================
// FOLLOWING CHART (从格) DETECTION
// =============================================================================

export function detectFollowingChart(
  chart: ChartData,
  support: number,
  drain: number,
  seasonalState: string,
  rootInfo: { has_strong_root: boolean },
): [boolean, string | null] {
  /**
   * Detect if this is a Following Chart (从格).
   * Conditions:
   * - DM is extremely weak (very low support, no strong root)
   * - No resource or companion stems in visible positions
   * - Seasonal state is Trapped or Dead
   */
  const dmElement = chart.dm_element;
  const resourceElement = ELEMENT_CYCLES.generated_by[dmElement];

  // Check if DM has any visible support
  let visibleSupport = 0;
  for (const pos of ["year", "month", "hour"]) { // Skip day stem (that's the DM itself)
    const stemElem = STEMS[chart.pillars[pos].stem].element;
    if (stemElem === dmElement || stemElem === resourceElement) {
      visibleSupport += 1;
    }
  }

  // Following chart conditions
  if (
    visibleSupport === 0 &&
    !rootInfo.has_strong_root &&
    (seasonalState === "Trapped" || seasonalState === "Dead") &&
    drain > support * 3
  ) {
    // Determine following type based on dominant drain
    const elementCounts = countElements(chart);
    // Remove DM's own element count to see what dominates
    const drainElements: Record<string, number> = {};
    for (const [elem, count] of Object.entries(elementCounts)) {
      if (elem !== dmElement && elem !== resourceElement) {
        drainElements[elem] = count;
      }
    }

    const drainKeys = Object.keys(drainElements);
    if (drainKeys.length > 0) {
      const dominant = drainKeys.reduce((a, b) =>
        drainElements[a] > drainElements[b] ? a : b
      );
      const outputElement = ELEMENT_CYCLES.generating[dmElement];
      const wealthElement = ELEMENT_CYCLES.controlling[dmElement];
      const officerElement = ELEMENT_CYCLES.controlled_by[dmElement];

      if (dominant === outputElement) {
        return [true, "output"];
      } else if (dominant === wealthElement) {
        return [true, "wealth"];
      } else if (dominant === officerElement) {
        return [true, "officer"];
      }
      return [true, "mixed"];
    }
  }

  return [false, null];
}

// =============================================================================
// USEFUL GOD (用神) DETERMINATION — BALANCE SIMULATION
// =============================================================================

function _calcImbalance(pcts: Record<string, number>): number {
  /** Sum of squared deviations from 20% — lower = more balanced. */
  let sum = 0;
  for (const p of Object.values(pcts)) {
    sum += (p - 20.0) ** 2;
  }
  return sum;
}

function _simulateDose(
  elementCounts: Record<string, number>,
  total: number,
  additions: Record<string, number>,
): [number, Record<string, number>] {
  /** Apply element additions and return [new_imbalance, new_percentages]. */
  const adjusted = { ...elementCounts };
  let doseTotal = 0;
  for (const [elem, dose] of Object.entries(additions)) {
    adjusted[elem] += dose;
    doseTotal += dose;
  }
  const newTotal = total + doseTotal;
  const newPcts: Record<string, number> = {};
  for (const [e, c] of Object.entries(adjusted)) {
    newPcts[e] = (c / newTotal) * 100;
  }
  return [_calcImbalance(newPcts), newPcts];
}

export function simulateElementBalance(elementCounts: Record<string, number>): {
  useful_god: string | null;
  favorable: string[];
  unfavorable: string[];
} {
  /**
   * Simulate adding each element to find which best balances the chart.
   * Imbalance = sum of squared deviations from 20% (ideal equal distribution).
   * The element whose addition produces the lowest imbalance = useful god.
   */
  const total = Object.values(elementCounts).reduce((a, b) => a + b, 0);
  if (total === 0) {
    return { useful_god: null, favorable: [], unfavorable: [] };
  }

  const currentPcts: Record<string, number> = {};
  for (const [e, c] of Object.entries(elementCounts)) {
    currentPcts[e] = (c / total) * 100;
  }
  const currentImbalance = _calcImbalance(currentPcts);

  // Standard dose = 1.0 (one Heavenly Stem equivalent, like a luck pillar)
  const dose = 1.0;
  const improvements: Record<string, number> = {};

  for (const testElem of Object.keys(elementCounts)) {
    const [newImb] = _simulateDose(elementCounts, total, { [testElem]: dose });
    improvements[testElem] = Math.round((currentImbalance - newImb) * 100) / 100;
  }

  // Rank by improvement (highest = most balancing)
  const ranked = Object.keys(improvements).sort(
    (a, b) => improvements[b] - improvements[a]
  );
  const favorable = ranked.filter(e => improvements[e] > 0);
  const unfavorable = ranked.filter(e => improvements[e] <= 0);

  return {
    useful_god: ranked[0] ?? null,
    favorable,
    unfavorable,
  };
}

export function simulateElementPairs(elementCounts: Record<string, number>): Array<Record<string, unknown>> {
  /**
   * Simulate adding pairs of elements (like a luck pillar's stem + branch).
   * Tests all 15 unique pairs at equal dose (0.5 + 0.5 = 1.0 total).
   * Returns top 5 pairs ranked by balancing improvement.
   */
  const total = Object.values(elementCounts).reduce((a, b) => a + b, 0);
  if (total === 0) {
    return [];
  }

  const currentPcts: Record<string, number> = {};
  for (const [e, c] of Object.entries(elementCounts)) {
    currentPcts[e] = (c / total) * 100;
  }
  const currentImbalance = _calcImbalance(currentPcts);

  const elements = Object.keys(elementCounts).sort();
  const results: Array<Record<string, unknown>> = [];

  for (let i = 0; i < elements.length; i++) {
    const e1 = elements[i];
    for (let j = i; j < elements.length; j++) {
      const e2 = elements[j];
      const additions: Record<string, number> = {};
      if (e1 === e2) {
        additions[e1] = 1.0; // Same element: full dose
      } else {
        additions[e1] = 0.5;
        additions[e2] = 0.5;
      }

      const [newImb, newPcts] = _simulateDose(elementCounts, total, additions);
      const improvement = Math.round((currentImbalance - newImb) * 100) / 100;

      const resultPcts: Record<string, number> = {};
      for (const [k, v] of Object.entries(newPcts)) {
        resultPcts[k] = Math.round(v * 10) / 10;
      }

      results.push({
        elements: e1 !== e2 ? [e1, e2] : [e1],
        improvement,
        result_pcts: resultPcts,
      });
    }
  }

  results.sort((a, b) => (b.improvement as number) - (a.improvement as number));
  return results.slice(0, 5); // Top 5 pairs
}

export function determineUsefulGod(
  chart: ChartData,
  verdict: string,
  isFollowing: boolean,
  followingType: string | null,
  elementCounts?: Record<string, number>,
): { useful_god: string | null; favorable: string[]; unfavorable: string[] } {
  /**
   * Determine the Useful God (用神) and favorable/unfavorable elements.
   * Uses balance simulation: which element, when added, brings the chart
   * closest to 20% equilibrium across all five elements.
   * Following charts use categorical rules (go with the dominant force).
   */
  const dmElement = chart.dm_element;
  const resourceElement = ELEMENT_CYCLES.generated_by[dmElement];
  const outputElement = ELEMENT_CYCLES.generating[dmElement];
  const wealthElement = ELEMENT_CYCLES.controlling[dmElement];
  const officerElement = ELEMENT_CYCLES.controlled_by[dmElement];

  if (isFollowing) {
    // Following chart: go WITH the dominant force (no rebalancing)
    if (followingType === "wealth") {
      return {
        useful_god: wealthElement,
        favorable: [wealthElement, outputElement, officerElement],
        unfavorable: [dmElement, resourceElement],
      };
    } else if (followingType === "officer") {
      return {
        useful_god: officerElement,
        favorable: [officerElement, wealthElement, outputElement],
        unfavorable: [dmElement, resourceElement],
      };
    } else if (followingType === "output") {
      return {
        useful_god: outputElement,
        favorable: [outputElement, wealthElement],
        unfavorable: [dmElement, resourceElement, officerElement],
      };
    } else {
      return {
        useful_god: wealthElement,
        favorable: [wealthElement, outputElement],
        unfavorable: [dmElement, resourceElement],
      };
    }
  }

  // Balance simulation: which element brings the chart closest to equilibrium?
  if (elementCounts) {
    return simulateElementBalance(elementCounts);
  }

  // Fallback (shouldn't reach here — element_counts always passed from assess)
  return {
    useful_god: outputElement,
    favorable: [outputElement, wealthElement],
    unfavorable: [],
  };
}

// =============================================================================
// MAIN STRENGTH ASSESSMENT
// =============================================================================

// Verdict thresholds (20% = balanced center)
export const VERDICT_THRESHOLDS = {
  extremely_strong: 30.0,
  strong: 24.0,
  neutral_upper: 24.0,
  neutral_lower: 16.0,
  weak: 10.0,
} as const;

export function assessDayMasterStrength(
  chart: ChartData,
  interactions?: BranchInteraction[],
): StrengthAssessment {
  /**
   * DM strength = DM's element percentage of total chart elements.
   * ~20% = balanced. Branch interactions and seasonal scaling adjust element weights.
   */
  // 1. Count raw elements
  let elementCounts = countElements(chart);

  // 2. Adjust for interactions (combinations add element weight, clashes reduce)
  if (interactions && interactions.length > 0) {
    elementCounts = adjustElementsForInteractions(
      elementCounts, interactions, chart);
  }

  // 3. Apply seasonal scaling (旺相休囚死) — most influential factor
  //    The month branch determines each element's seasonal state.
  //    e.g., Winter (Hai): Water Prosperous x1.382, Fire Dead x0.786
  const monthBranch = chart.pillars["month"].branch;
  elementCounts = applySeasonalScaling(elementCounts, monthBranch);

  // 4. Calculate percentages from seasonally-scaled weights
  const total = Object.values(elementCounts).reduce((a, b) => a + b, 0);
  let percentages: Record<string, number>;
  if (total > 0) {
    percentages = {};
    for (const [elem, count] of Object.entries(elementCounts)) {
      percentages[elem] = (count / total) * 100;
    }
  } else {
    percentages = {};
    for (const elem of Object.keys(elementCounts)) {
      percentages[elem] = 20.0;
    }
  }

  // 5. DM strength score = DM's element percentage (single source of truth)
  const dmElement = chart.dm_element;
  const score = Math.max(1.0, Math.min(50.0,
    Math.round(percentages[dmElement] * 10) / 10));

  // 6. Drain pressure: if drain elements individually exceed the DM,
  //    the DM is under pressure even at a "balanced" percentage.
  const outputElem = ELEMENT_CYCLES.generating[dmElement] ?? "";
  const wealthElem = ELEMENT_CYCLES.controlling[dmElement] ?? "";
  const officerElem = ELEMENT_CYCLES.controlled_by[dmElement] ?? "";

  let drainPressure = 0.0;
  for (const drainElem of [outputElem, wealthElem, officerElem]) {
    if (drainElem) {
      const excess = (percentages[drainElem] ?? 0) - score;
      if (excess > 0) {
        drainPressure += excess;
      }
    }
  }

  // 7. Seasonal state and root factors for verdict
  const seasonalState = getSeasonalState(chart);
  const rootInfo = checkRooting(chart);

  // Seasonal effect is now in the percentages via scaling (step 3).
  // Root adjustment is a small additional factor.
  let effectivePct = score;
  if (rootInfo.has_strong_root) {
    effectivePct += 1.0;
  } else if (!rootInfo.has_root) {
    effectivePct -= 1.5;
  }

  // 8. Apply drain pressure — each point of excess reduces effective strength
  effectivePct -= drainPressure * 0.4;

  // 9. Determine verdict using effective_pct (20% = balanced)
  let verdict: string;
  if (effectivePct >= 30.0) {
    verdict = "extremely_strong";
  } else if (effectivePct >= 24.0) {
    verdict = "strong";
  } else if (effectivePct >= 16.0) {
    verdict = "neutral";
  } else if (effectivePct >= 10.0) {
    verdict = "weak";
  } else {
    verdict = "extremely_weak";
  }

  // 10. Support/drain counts (kept for compatibility)
  const [support, drain] = countSupportVsDrain(chart);

  // 11. Check for following chart
  const [isFollowing, followingType] = detectFollowingChart(
    chart, support, drain, seasonalState, rootInfo);

  // 12. Determine useful god via balance simulation (uses seasonally-scaled counts)
  const godInfo = determineUsefulGod(chart, verdict, isFollowing, followingType,
    elementCounts);

  // 13. Simulate element pairs (best luck pillar combinations)
  const bestPairs = !isFollowing ? simulateElementPairs(elementCounts) : [];

  // Round percentages
  const roundedPercentages: Record<string, number> = {};
  for (const [k, v] of Object.entries(percentages)) {
    roundedPercentages[k] = Math.round(v * 10) / 10;
  }

  return {
    score,
    verdict,
    support_count: Math.round(support * 100) / 100,
    drain_count: Math.round(drain * 100) / 100,
    seasonal_state: seasonalState,
    is_following_chart: isFollowing,
    following_type: followingType,
    useful_god: godInfo.useful_god ?? "",
    favorable_elements: godInfo.favorable,
    unfavorable_elements: godInfo.unfavorable,
    element_percentages: roundedPercentages,
    best_element_pairs: bestPairs,
  };
}
