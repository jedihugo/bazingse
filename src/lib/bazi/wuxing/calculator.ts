// =============================================================================
// WU XING CALCULATOR - MAIN ENGINE
// =============================================================================
// Deterministic point-based Wu Xing (Five Element) calculator.
// Chains steps 0-9 to produce a WuxingResult from pillar inputs.
// Steps 1-7 are stubs — they pass state through unchanged for now.
// =============================================================================

import type { Element, StemName, BranchName } from '../core';
import {
  HS_POINTS,
  EB_HIDDEN_STEMS,
  EB_POLARITY,
  MONTH_BRANCH_SEASON,
  CONTROL_LOOKUP,
} from './tables';
import type { PillarPosition, ControlRelation } from './tables';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Node slots within a pillar */
export type NodeSlot = 'HS' | 'EB' | 'EB.h1' | 'EB.h2';

/** Full node identifier: e.g. 'DP.HS', 'YP.EB.h1' */
export type NodeId = `${PillarPosition}.${NodeSlot}`;

/** Input pillar (stem + branch pair) */
export interface PillarInput {
  stem: StemName;
  branch: BranchName;
}

/** Calculator input */
export interface WuxingInput {
  yearPillar: PillarInput;
  monthPillar: PillarInput;
  dayPillar: PillarInput;
  hourPillar?: PillarInput;
  tenYearLuck?: PillarInput; // future
  age: number;
  gender: 'M' | 'F';
  location: 'hometown' | 'out_of_town' | 'overseas';
}

/** A node in the chart */
export interface WuxingNode {
  id: NodeId;
  pillar: PillarPosition;
  slot: NodeSlot;
  stem: StemName;
  element: Element;
  polarity: 'Yang' | 'Yin';
  points: number;          // mutable — updated each step
  initialPoints: number;   // frozen at Step 0
  seasonalMultiplier?: number; // set in Step 6
}

/** Bonus node from combo/transform */
export interface BonusNode {
  id: string;              // e.g. "YP.EB+Wood_SIX_HARMONIES"
  sourceNode: string;      // which node created this
  pillar: PillarPosition;
  element: Element;
  polarity: 'Yang' | 'Yin';
  points: number;
  source: string;          // interaction type that created it
}

/** Interaction log entry */
export interface InteractionLog {
  step: number;
  type: string;            // 'PILLAR_PAIR', 'THREE_MEETINGS', 'SIX_CLASH', etc.
  nodes?: string[];        // node IDs involved
  branches?: string[];     // branch names involved
  nodeA?: string;
  nodeB?: string;
  relationship?: string;
  basis?: number;
  resultElement?: Element;
  transformed?: boolean;
  gapMultiplier?: number;
  attacker?: string;
  victim?: string;
  logOnly?: boolean;
  details?: string;
}

/** Internal state passed through steps */
export interface WuxingState {
  input: WuxingInput;
  nodes: WuxingNode[];
  bonusNodes: BonusNode[];
  interactions: InteractionLog[];
  season: Element;
  pillarPriority: PillarPosition[];
  attentionMap: Map<string, Array<{ type: string; weight: number }>>;
}

/** Element summary for output */
export interface ElementSummary {
  total: number;
  percent: number;
  rank: number;
}

/** Day Master summary */
export interface DayMasterSummary {
  stem: StemName;
  element: Element;
  percent: number;
  strength: 'dominant' | 'strong' | 'balanced' | 'weak' | 'very_weak';
}

/** Five Gods (用神/喜神/忌神/仇神/闲神) */
export interface FiveGods {
  useful: Element;      // 用神
  favorable: Element;   // 喜神
  unfavorable: Element; // 忌神
  enemy: Element;       // 仇神
  idle: Element;        // 闲神
}

/** Per-node output */
export interface NodeOutput {
  stem: StemName;
  element: Element;
  polarity: 'Yang' | 'Yin';
  initial: number;
  final: number;
  delta: number;
}

/** Final output */
export interface WuxingResult {
  nodes: Record<string, NodeOutput>;
  bonusNodes: BonusNode[];
  elements: Record<Element, ElementSummary>;
  dayMaster: DayMasterSummary;
  gods: FiveGods;
  interactions: InteractionLog[];
}

// Re-export PillarPosition from tables so consumers don't need two imports
export type { PillarPosition } from './tables';

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const ELEMENTS: Element[] = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'];

/** Production cycle: each element produces the next */
const PRODUCES: Record<Element, Element> = {
  Wood: 'Fire',
  Fire: 'Earth',
  Earth: 'Metal',
  Metal: 'Water',
  Water: 'Wood',
};

// ---------------------------------------------------------------------------
// Pillar Priority
// ---------------------------------------------------------------------------

/**
 * Determine pillar priority order based on age.
 *
 * Active pillar by age bracket:
 *   0-16  -> YP
 *   17-32 -> MP
 *   33-48 -> DP
 *   49-64 -> HP
 *
 * Rules:
 *   1. Active pillar first
 *   2. DP always 2nd (unless already 1st)
 *   3. Remaining ordered by proximity to age boundaries
 */
export function calculatePillarPriority(age: number): PillarPosition[] {
  // Determine which pillar is active
  let active: PillarPosition;
  if (age <= 16) active = 'YP';
  else if (age <= 32) active = 'MP';
  else if (age <= 48) active = 'DP';
  else active = 'HP';

  // Age boundaries for proximity calculation
  const boundaries: Record<PillarPosition, { start: number; end: number }> = {
    YP: { start: 0, end: 16 },
    MP: { start: 17, end: 32 },
    DP: { start: 33, end: 48 },
    HP: { start: 49, end: 64 },
  };

  // Distance from age to a bracket's nearest boundary
  function distanceTo(p: PillarPosition): number {
    const b = boundaries[p];
    if (age >= b.start && age <= b.end) return 0;
    return Math.min(Math.abs(age - b.start), Math.abs(age - b.end));
  }

  const result: PillarPosition[] = [active];

  // DP is always 2nd unless it's already 1st
  if (active !== 'DP') {
    result.push('DP');
  }

  // Remaining pillars sorted by proximity
  const remaining = (['YP', 'MP', 'DP', 'HP'] as PillarPosition[])
    .filter(p => !result.includes(p));

  remaining.sort((a, b) => distanceTo(a) - distanceTo(b));
  result.push(...remaining);

  return result;
}

// ---------------------------------------------------------------------------
// Step 0: Initialize State
// ---------------------------------------------------------------------------

/**
 * Create all chart nodes from pillar inputs (Step 0).
 *
 * For each pillar:
 *   - HS node: 10 points
 *   - EB hidden stem nodes: points from EB_HIDDEN_STEMS table
 *
 * If hourPillar is not provided, HP nodes use DP's stem and branch as fallback.
 */
export function initializeState(input: WuxingInput): WuxingState {
  const nodes: WuxingNode[] = [];

  // Resolve HP: use hourPillar if provided, otherwise fallback to DP
  const resolvedPillars: Record<PillarPosition, PillarInput> = {
    YP: input.yearPillar,
    MP: input.monthPillar,
    DP: input.dayPillar,
    HP: input.hourPillar ?? input.dayPillar,
  };

  for (const pos of ['YP', 'MP', 'DP', 'HP'] as PillarPosition[]) {
    const pillar = resolvedPillars[pos];

    // HS node
    const hsData = HS_POINTS[pillar.stem];
    nodes.push({
      id: `${pos}.HS` as NodeId,
      pillar: pos,
      slot: 'HS',
      stem: pillar.stem,
      element: hsData.element,
      polarity: hsData.polarity,
      points: hsData.points,
      initialPoints: hsData.points,
    });

    // EB hidden stem nodes
    const ebStems = EB_HIDDEN_STEMS[pillar.branch];
    const slotNames: NodeSlot[] = ['EB', 'EB.h1', 'EB.h2'];

    for (let i = 0; i < ebStems.length; i++) {
      const entry = ebStems[i];
      nodes.push({
        id: `${pos}.${slotNames[i]}` as NodeId,
        pillar: pos,
        slot: slotNames[i],
        stem: entry.stem,
        element: entry.element,
        polarity: EB_POLARITY[pillar.branch],
        points: entry.points,
        initialPoints: entry.points,
      });
    }
  }

  const season = MONTH_BRANCH_SEASON[input.monthPillar.branch];
  const pillarPriority = calculatePillarPriority(input.age);

  return {
    input,
    nodes,
    bonusNodes: [],
    interactions: [],
    season,
    pillarPriority,
    attentionMap: new Map(),
  };
}

// ---------------------------------------------------------------------------
// Steps 1-7: Stubs (pass through unchanged)
// ---------------------------------------------------------------------------

/**
 * Step 1: HS↔EB pillar pair interactions.
 *
 * For each pillar, the HS element interacts with the EB main qi element
 * (the first hidden stem, slot 'EB'). Hidden stems h1/h2 are NOT affected.
 *
 * Relationship is looked up via CONTROL_LOOKUP[hsElement][ebMainQiElement]:
 *   SAME            → skip (no interaction)
 *   HS_PRODUCES_EB  → HS loses 20% of basis, EB gains 30% of basis
 *   EB_PRODUCES_HS  → EB loses 20% of basis, HS gains 30% of basis
 *   HS_CONTROLS_EB  → HS loses 20% of basis (盖头), EB loses 30% of basis
 *   EB_CONTROLS_HS  → EB loses 20% of basis (截脚), HS loses 30% of basis
 *
 * basis = min(HS.points, EB.points)
 */
export function step1PillarPairs(state: WuxingState): WuxingState {
  const PILLAR_ORDER: PillarPosition[] = ['YP', 'MP', 'DP', 'HP'];

  for (const pos of PILLAR_ORDER) {
    const hsNode = state.nodes.find(n => n.id === `${pos}.HS`)!;
    const ebNode = state.nodes.find(n => n.id === `${pos}.EB`)!;

    const relation: ControlRelation = CONTROL_LOOKUP[hsNode.element][ebNode.element];

    if (relation === 'SAME') continue;

    const basis = Math.min(hsNode.points, ebNode.points);
    const loss20 = basis * 0.20;
    const effect30 = basis * 0.30;

    switch (relation) {
      case 'HS_PRODUCES_EB':
        // Producer (HS) loses 20%, produced (EB) gains 30%
        hsNode.points -= loss20;
        ebNode.points += effect30;
        break;

      case 'EB_PRODUCES_HS':
        // Producer (EB) loses 20%, produced (HS) gains 30%
        ebNode.points -= loss20;
        hsNode.points += effect30;
        break;

      case 'HS_CONTROLS_EB':
        // Controller (HS) loses 20%, controlled (EB) loses 30% — 盖头
        hsNode.points -= loss20;
        ebNode.points -= effect30;
        break;

      case 'EB_CONTROLS_HS':
        // Controller (EB) loses 20%, controlled (HS) loses 30% — 截脚
        ebNode.points -= loss20;
        hsNode.points -= effect30;
        break;
    }

    state.interactions.push({
      step: 1,
      type: 'PILLAR_PAIR',
      nodeA: hsNode.id,
      nodeB: ebNode.id,
      relationship: relation,
      basis,
      details: `${pos}: ${hsNode.stem}(${hsNode.element}) ${relation} ${ebNode.stem}(${ebNode.element}), basis=${basis}`,
    });
  }

  return state;
}

/** Step 2: EB positive interactions — 三会/三合/六合/半会/拱合 (stub) */
export function step2EbPositive(state: WuxingState): WuxingState {
  return state;
}

/** Step 3: HS positive interactions — 天干合 (stub) */
export function step3HsPositive(state: WuxingState): WuxingState {
  return state;
}

/** Step 4: EB negative interactions — 六冲/刑/六害/破 (stub) */
export function step4EbNegative(state: WuxingState): WuxingState {
  return state;
}

/** Step 5: HS negative interactions — 天干冲 (stub) */
export function step5HsNegative(state: WuxingState): WuxingState {
  return state;
}

/** Step 6: Seasonal multipliers (stub) */
export function step6Seasonal(state: WuxingState): WuxingState {
  return state;
}

/** Step 7: Natural flow — cross-pillar element interactions (stub) */
export function step7NaturalFlow(state: WuxingState): WuxingState {
  return state;
}

// ---------------------------------------------------------------------------
// Step 8: Report — aggregate element totals
// ---------------------------------------------------------------------------

/**
 * Aggregate all node points by element.
 * Returns element totals, percentages, and rank (1 = highest).
 */
export function step8Report(state: WuxingState): Record<Element, ElementSummary> {
  // Sum points per element across primary + bonus nodes
  const totals: Record<Element, number> = {
    Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0,
  };

  for (const node of state.nodes) {
    totals[node.element] += node.points;
  }
  for (const bonus of state.bonusNodes) {
    totals[bonus.element] += bonus.points;
  }

  const grandTotal = ELEMENTS.reduce((sum, el) => sum + totals[el], 0);

  // Build unsorted entries with percentages
  const entries: Array<{ element: Element; total: number; percent: number }> = ELEMENTS.map(el => ({
    element: el,
    total: totals[el],
    percent: grandTotal > 0 ? (totals[el] / grandTotal) * 100 : 0,
  }));

  // Sort descending by total to assign ranks
  const sorted = [...entries].sort((a, b) => b.total - a.total);
  const rankMap = new Map<Element, number>();
  sorted.forEach((entry, idx) => rankMap.set(entry.element, idx + 1));

  // Build result
  const result = {} as Record<Element, ElementSummary>;
  for (const entry of entries) {
    result[entry.element] = {
      total: entry.total,
      percent: parseFloat(entry.percent.toFixed(2)),
      rank: rankMap.get(entry.element)!,
    };
  }

  return result;
}

// ---------------------------------------------------------------------------
// Step 9: Balance Simulation — determine Five Gods
// ---------------------------------------------------------------------------

/**
 * For each element, simulate adding 10 points and compute how balanced
 * the chart becomes. The element that creates the best balance is the
 * useful god (用神).
 *
 * sigma = sqrt( sum( (p_i - 20%)^2 ) / 5 )
 * DM penalty: +5 if DM% < 8%, +3 if DM% > 40%
 *
 * - Lowest sigma  -> useful (用神)
 * - Highest sigma -> unfavorable (忌神)
 * - Produces useful -> favorable (喜神)
 * - Produces unfavorable -> enemy (仇神)
 * - Remaining -> idle (闲神)
 */
export function step9BalanceSim(
  state: WuxingState,
  elementSummary: Record<Element, ElementSummary>,
): FiveGods {
  const dmElement = HS_POINTS[state.input.dayPillar.stem].element;

  // Current total points per element
  const baseTotals: Record<Element, number> = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };
  for (const node of state.nodes) {
    baseTotals[node.element] += node.points;
  }
  for (const bonus of state.bonusNodes) {
    baseTotals[bonus.element] += bonus.points;
  }

  const baseGrand = ELEMENTS.reduce((s, el) => s + baseTotals[el], 0);

  // Simulate adding 10 points to each element
  const sigmas: Array<{ element: Element; sigma: number }> = [];

  for (const testEl of ELEMENTS) {
    const newGrand = baseGrand + 10;
    let sumSqDev = 0;

    for (const el of ELEMENTS) {
      const newTotal = baseTotals[el] + (el === testEl ? 10 : 0);
      const pct = (newTotal / newGrand) * 100;
      sumSqDev += (pct - 20) ** 2;
    }

    let sigma = Math.sqrt(sumSqDev / 5);

    // DM penalty
    const dmNewTotal = baseTotals[dmElement] + (testEl === dmElement ? 10 : 0);
    const dmPct = (dmNewTotal / newGrand) * 100;
    if (dmPct < 8) sigma += 5;
    if (dmPct > 40) sigma += 3;

    sigmas.push({ element: testEl, sigma });
  }

  // Sort by sigma ascending
  sigmas.sort((a, b) => a.sigma - b.sigma);

  const useful = sigmas[0].element;
  const unfavorable = sigmas[sigmas.length - 1].element;

  // favorable = element that produces useful
  const favorable = ELEMENTS.find(el => PRODUCES[el] === useful)!;

  // enemy = element that produces unfavorable
  const enemy = ELEMENTS.find(el => PRODUCES[el] === unfavorable)!;

  // idle = the remaining element
  const assigned = new Set([useful, favorable, unfavorable, enemy]);
  const idle = ELEMENTS.find(el => !assigned.has(el))!;

  return { useful, favorable, unfavorable, enemy, idle };
}

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Run the full Wu Xing calculator pipeline.
 * Steps 1-7 are stubs — only Step 0 (init), Step 8 (report), and
 * Step 9 (balance sim) produce real data for now.
 */
export function calculateWuxing(input: WuxingInput): WuxingResult {
  let state = initializeState(input);
  state = step1PillarPairs(state);
  state = step2EbPositive(state);
  state = step3HsPositive(state);
  state = step4EbNegative(state);
  state = step5HsNegative(state);
  state = step6Seasonal(state);
  state = step7NaturalFlow(state);

  const elementSummary = step8Report(state);
  const gods = step9BalanceSim(state, elementSummary);

  // Build per-node output
  const nodeOutputs: Record<string, NodeOutput> = {};
  for (const node of state.nodes) {
    nodeOutputs[node.id] = {
      stem: node.stem,
      element: node.element,
      polarity: node.polarity,
      initial: node.initialPoints,
      final: node.points,
      delta: node.points - node.initialPoints,
    };
  }

  // Day Master
  const dmStem = input.dayPillar.stem;
  const dmElement = HS_POINTS[dmStem].element;
  const dmPercent = elementSummary[dmElement].percent;

  let strength: DayMasterSummary['strength'];
  if (dmPercent >= 35) strength = 'dominant';
  else if (dmPercent >= 25) strength = 'strong';
  else if (dmPercent >= 15) strength = 'balanced';
  else if (dmPercent >= 8) strength = 'weak';
  else strength = 'very_weak';

  return {
    nodes: nodeOutputs,
    bonusNodes: [...state.bonusNodes],
    elements: elementSummary,
    dayMaster: {
      stem: dmStem,
      element: dmElement,
      percent: dmPercent,
      strength,
    },
    gods,
    interactions: [...state.interactions],
  };
}

/**
 * Run the calculator up to a specific step (inclusive) and return
 * the intermediate state. Useful for testing individual steps.
 *
 * step=0 -> after initializeState
 * step=1 -> after step1PillarPairs
 * ...
 * step=7 -> after step7NaturalFlow
 */
export function calculateWuxingUpToStep(input: WuxingInput, step: number): WuxingState {
  const steps: Array<(s: WuxingState) => WuxingState> = [
    step1PillarPairs,
    step2EbPositive,
    step3HsPositive,
    step4EbNegative,
    step5HsNegative,
    step6Seasonal,
    step7NaturalFlow,
  ];

  let state = initializeState(input);

  // Steps 1-7 are indices 0-6 in the array
  const limit = Math.min(step, steps.length);
  for (let i = 0; i < limit; i++) {
    state = steps[i](state);
  }

  return state;
}
