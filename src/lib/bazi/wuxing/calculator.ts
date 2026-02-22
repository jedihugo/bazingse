// =============================================================================
// WU XING CALCULATOR - MAIN ENGINE
// =============================================================================
// Deterministic point-based Wu Xing (Five Element) calculator.
// Chains steps 0-9 to produce a WuxingResult from pillar inputs.
// All steps (0-9) produce real data.
// =============================================================================

import type { Element, StemName, BranchName } from '../core';
import {
  HS_POINTS,
  EB_HIDDEN_STEMS,
  EB_POLARITY,
  MONTH_BRANCH_SEASON,
  CONTROL_LOOKUP,
  PILLAR_GAP,
  gapMultiplier,
  COMBO_RATES,
  TRANSFORMATION_MULTIPLIER,
  ATTENTION_WEIGHTS,
  THREE_MEETINGS_TABLE,
  THREE_COMBOS_TABLE,
  SIX_HARMONIES_TABLE,
  HALF_MEETINGS_TABLE,
  ARCHED_COMBOS_TABLE,
  SIX_CLASHES_TABLE,
  DESTRUCTIONS_TABLE,
  SIX_HARMS_TABLE,
  PUNISHMENTS_TABLE,
  STEM_COMBOS_TABLE,
  STEM_CLASHES_TABLE,
  NEGATIVE_RATES,
  SEASONAL_MATRIX,
  SEASONAL_MULTIPLIERS,
  getStep7Gap,
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
// Step 1: HS↔EB Pillar Pair Interactions
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

// ---------------------------------------------------------------------------
// Step 2: EB Positive Interactions — 三会/三合/六合/半会/拱合
// ---------------------------------------------------------------------------

/** Pillar position to numeric index for gap calculations */
const PILLAR_INDEX: Record<PillarPosition, number> = {
  YP: 0, MP: 1, DP: 2, HP: 3,
};

/** Helper: sort an array of branch names alphabetically and join with '-' */
function branchKey(...branches: BranchName[]): string {
  return [...branches].sort().join('-');
}

/** Combo type strength ordering (strongest first) */
const COMBO_STRENGTH_ORDER = [
  'THREE_MEETINGS',
  'THREE_COMBOS',
  'SIX_HARMONIES',
  'HALF_MEETINGS',
  'ARCHED_COMBOS',
] as const;

/** A detected interaction (both positive and negative) for pre-scan */
interface DetectedInteraction {
  type: string;
  branches: BranchName[];
  pillars: PillarPosition[];
  element: Element;          // produced element (positive) or involved element (negative)
  attentionWeight: number;
  nullified: boolean;        // set true if a larger combo absorbs this
  logOnly?: boolean;         // for same-element clashes/destructions
  rate?: number;             // combo rate for positive interactions
  isPositive: boolean;
}

/**
 * Step 2: EB positive interactions — 三会/三合/六合/半会/拱合
 *
 * Phase 1: Pre-scan all branch combinations (positive + negative for attention)
 * Phase 2: Build attention map
 * Phase 3: Process combos in pillar priority order, create BonusNodes
 */
export function step2EbPositive(state: WuxingState): WuxingState {
  // Collect branch -> pillar mapping
  const branchToPillars = new Map<BranchName, PillarPosition[]>();
  for (const pos of ['YP', 'MP', 'DP', 'HP'] as PillarPosition[]) {
    const pillar = _resolvedPillar(state, pos);
    const branch = pillar.branch;
    const existing = branchToPillars.get(branch) ?? [];
    existing.push(pos);
    branchToPillars.set(branch, existing);
  }

  // Set of all unique branches in the chart
  const chartBranches = new Set(branchToPillars.keys());

  // -----------------------------------------------------------------------
  // Phase 1: Detect all interactions
  // -----------------------------------------------------------------------
  const detected: DetectedInteraction[] = [];

  // --- Positive interactions ---

  // 三会 THREE_MEETINGS (3 seasonal branches)
  for (const [key, data] of Object.entries(THREE_MEETINGS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      // Find all pillar combos (one pillar per branch)
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        detected.push({
          type: 'THREE_MEETINGS',
          branches,
          pillars,
          element: data.element,
          attentionWeight: ATTENTION_WEIGHTS.THREE_MEETINGS,
          nullified: false,
          rate: COMBO_RATES.THREE_MEETINGS,
          isPositive: true,
        });
      }
    }
  }

  // 三合 THREE_COMBOS (triangular harmony)
  for (const [key, data] of Object.entries(THREE_COMBOS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        detected.push({
          type: 'THREE_COMBOS',
          branches,
          pillars,
          element: data.element,
          attentionWeight: ATTENTION_WEIGHTS.THREE_COMBOS,
          nullified: false,
          rate: COMBO_RATES.THREE_COMBOS,
          isPositive: true,
        });
      }
    }
  }

  // 六合 SIX_HARMONIES (pair harmonies)
  for (const [key, data] of Object.entries(SIX_HARMONIES_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        detected.push({
          type: 'SIX_HARMONIES',
          branches,
          pillars,
          element: data.element,
          attentionWeight: ATTENTION_WEIGHTS.SIX_HARMONIES,
          nullified: false,
          rate: COMBO_RATES.SIX_HARMONIES,
          isPositive: true,
        });
      }
    }
  }

  // 半三会 HALF_MEETINGS (2 of 3 seasonal)
  for (const [key, data] of Object.entries(HALF_MEETINGS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        detected.push({
          type: 'HALF_MEETINGS',
          branches,
          pillars,
          element: data.element,
          attentionWeight: ATTENTION_WEIGHTS.HALF_MEETINGS,
          nullified: false,
          rate: COMBO_RATES.HALF_MEETINGS,
          isPositive: true,
        });
      }
    }
  }

  // 拱合 ARCHED_COMBOS (Growth + Tomb, Peak missing)
  for (const [key, data] of Object.entries(ARCHED_COMBOS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        detected.push({
          type: 'ARCHED_COMBOS',
          branches,
          pillars,
          element: data.element,
          attentionWeight: ATTENTION_WEIGHTS.ARCHED_COMBO,
          nullified: false,
          rate: COMBO_RATES.ARCHED_COMBOS,
          isPositive: true,
        });
      }
    }
  }

  // --- Negative interactions (for attention pre-scan only) ---

  // 六冲 SIX_CLASH
  for (const [key, data] of Object.entries(SIX_CLASHES_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        // Same-pillar clashes don't happen (same branch can't clash with itself)
        if (pillars[0] === pillars[1]) continue;
        detected.push({
          type: 'SIX_CLASH',
          branches,
          pillars,
          element: 'Earth', // placeholder for attention tracking
          attentionWeight: ATTENTION_WEIGHTS.SIX_CLASH,
          nullified: false,
          logOnly: data.type === 'same',
          isPositive: false,
        });
      }
    }
  }

  // 破 DESTRUCTION
  for (const [key, data] of Object.entries(DESTRUCTIONS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        if (pillars[0] === pillars[1]) continue;
        detected.push({
          type: 'DESTRUCTION',
          branches,
          pillars,
          element: 'Earth', // placeholder
          attentionWeight: ATTENTION_WEIGHTS.DESTRUCTION,
          nullified: false,
          logOnly: data.type === 'same',
          isPositive: false,
        });
      }
    }
  }

  // 六害 SIX_HARM — only at gap 0 (adjacent pillars)
  for (const [key, _data] of Object.entries(SIX_HARMS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (branches.every(b => chartBranches.has(b))) {
      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        if (pillars[0] === pillars[1]) continue;
        const gap = PILLAR_GAP[pillars[0]][pillars[1]];
        if (gap !== 0) continue; // Only adjacent
        detected.push({
          type: 'SIX_HARM',
          branches,
          pillars,
          element: 'Earth', // placeholder
          attentionWeight: ATTENTION_WEIGHTS.SIX_HARM,
          nullified: false,
          isPositive: false,
        });
      }
    }
  }

  // 三刑 PUNISHMENT
  for (const [key, data] of Object.entries(PUNISHMENTS_TABLE)) {
    if (data.type === 'self') continue; // Self-punishments not relevant for attention
    if (data.branches) {
      // Group punishment (3-way or requiresAll)
      const branches = data.branches;
      if (data.requiresAll) {
        // All 3 must be present
        if (branches.every(b => chartBranches.has(b))) {
          const pillarCombos = _allPillarCombinations(branches, branchToPillars);
          for (const pillars of pillarCombos) {
            detected.push({
              type: 'PUNISHMENT_FULL',
              branches: [...branches],
              pillars,
              element: 'Earth',
              attentionWeight: ATTENTION_WEIGHTS.PUNISHMENT_FULL,
              nullified: false,
              logOnly: data.logOnly,
              isPositive: false,
            });
          }
        }
      } else {
        // Pair punishments from the group (shi type — any 2 of 3)
        if (data.pairs) {
          for (const pairDef of data.pairs) {
            const pairBranches = pairDef.pair;
            if (pairBranches.every(b => chartBranches.has(b))) {
              const pillarCombos = _allPillarCombinations(pairBranches, branchToPillars);
              for (const pillars of pillarCombos) {
                if (pillars[0] === pillars[1]) continue;
                detected.push({
                  type: 'PUNISHMENT_FULL',
                  branches: [...pairBranches],
                  pillars,
                  element: 'Earth',
                  attentionWeight: ATTENTION_WEIGHTS.PUNISHMENT_FULL,
                  nullified: false,
                  isPositive: false,
                });
              }
            }
          }
        }
      }
    } else if (data.attacker && data.victim) {
      // Pair punishment (en type)
      const branches = [data.attacker, data.victim] as BranchName[];
      if (branches.every(b => chartBranches.has(b))) {
        const pillarCombos = _allPillarCombinations(branches, branchToPillars);
        for (const pillars of pillarCombos) {
          if (pillars[0] === pillars[1]) continue;
          detected.push({
            type: 'PUNISHMENT_FULL',
            branches,
            pillars,
            element: 'Earth',
            attentionWeight: ATTENTION_WEIGHTS.PUNISHMENT_FULL,
            nullified: false,
            isPositive: false,
          });
        }
      }
    }
  }

  // -----------------------------------------------------------------------
  // Three-Branch Priority: nullify subsets
  // -----------------------------------------------------------------------
  const fullTrios = detected.filter(
    d => (d.type === 'THREE_MEETINGS' || d.type === 'THREE_COMBOS') && d.isPositive
  );

  for (const trio of fullTrios) {
    const trioBranchSet = new Set(trio.branches);

    for (const d of detected) {
      if (d === trio || d.nullified || !d.isPositive) continue;
      if (d.branches.length >= 3) continue; // Don't nullify other trios

      // Check if BOTH branches of the 2-branch combo are in this trio
      if (d.branches.every(b => trioBranchSet.has(b))) {
        // 三会 nullifies: 半三会 subsets + any 六合 between trio branches
        if (trio.type === 'THREE_MEETINGS' &&
            (d.type === 'HALF_MEETINGS' || d.type === 'SIX_HARMONIES')) {
          d.nullified = true;
        }
        // 三合 nullifies: 拱合 subset
        if (trio.type === 'THREE_COMBOS' && d.type === 'ARCHED_COMBOS') {
          d.nullified = true;
        }
      }
    }
  }

  // -----------------------------------------------------------------------
  // Phase 2: Build attention map
  // -----------------------------------------------------------------------
  // For each EB node, collect all (non-nullified) interactions it participates in
  const attentionMap = new Map<string, Array<{ type: string; weight: number }>>();

  for (const d of detected) {
    if (d.nullified) continue;
    for (const pillar of d.pillars) {
      const nodeId = `${pillar}.EB`;
      const existing = attentionMap.get(nodeId) ?? [];
      existing.push({ type: d.type, weight: d.attentionWeight });
      attentionMap.set(nodeId, existing);
    }
  }

  state.attentionMap = attentionMap;

  // -----------------------------------------------------------------------
  // Phase 3: Process combinations in pillar priority order
  // -----------------------------------------------------------------------
  // Collect visible HS elements for transformation check
  const visibleHsElements = new Set<Element>();
  for (const pos of ['YP', 'MP', 'DP', 'HP'] as PillarPosition[]) {
    const hsNode = state.nodes.find(n => n.id === `${pos}.HS`)!;
    visibleHsElements.add(hsNode.element);
  }

  // Track processed combos to avoid duplicates (by a unique identity key)
  const processedCombos = new Set<string>();

  // Get only active (non-nullified) positive combos
  const activePositive = detected.filter(d => d.isPositive && !d.nullified);

  for (const pillar of state.pillarPriority) {
    // Find combos involving this pillar's EB
    const combosForPillar = activePositive.filter(d => d.pillars.includes(pillar));

    // Sort by combo strength (strongest first)
    combosForPillar.sort((a, b) => {
      const aIdx = COMBO_STRENGTH_ORDER.indexOf(a.type as typeof COMBO_STRENGTH_ORDER[number]);
      const bIdx = COMBO_STRENGTH_ORDER.indexOf(b.type as typeof COMBO_STRENGTH_ORDER[number]);
      return aIdx - bIdx;
    });

    for (const combo of combosForPillar) {
      // Build a unique key for this specific combo instance
      const comboKey = `${combo.type}:${combo.pillars.sort().join(',')}:${combo.branches.sort().join(',')}`;
      if (processedCombos.has(comboKey)) continue;
      processedCombos.add(comboKey);

      // a. basis = min(main qi pts of all combining EBs) — use CURRENT values
      const ebNodes = combo.pillars.map(p => state.nodes.find(n => n.id === `${p}.EB`)!);
      const basis = Math.min(...ebNodes.map(n => n.points));

      // b. Gap multiplier
      let gapMult: number;
      if (combo.pillars.length === 3) {
        // For 3-branch: gaps = span - count
        const indices = combo.pillars.map(p => PILLAR_INDEX[p]);
        const span = Math.max(...indices) - Math.min(...indices) + 1;
        const gaps = span - combo.pillars.length;
        gapMult = gapMultiplier(gaps);
      } else {
        // For 2-branch: use PILLAR_GAP directly
        gapMult = gapMultiplier(PILLAR_GAP[combo.pillars[0]][combo.pillars[1]]);
      }

      // c. combo_pts_per_node = basis * rate * gap_multiplier
      let comboPtsPerNode = basis * combo.rate! * gapMult;

      // d. Transformation check: any visible HS has same element as combo result?
      const transformed = visibleHsElements.has(combo.element);
      if (transformed) {
        comboPtsPerNode *= TRANSFORMATION_MULTIPLIER;
      }

      // e. Apply attention share per node and create BonusNodes
      for (let i = 0; i < combo.pillars.length; i++) {
        const p = combo.pillars[i];
        const nodeId = `${p}.EB`;
        const branch = combo.branches[i];

        // Attention share calculation
        const nodeAttention = attentionMap.get(nodeId) ?? [];
        const totalWeight = nodeAttention.reduce((sum, a) => sum + a.weight, 0);
        const thisWeight = combo.attentionWeight;
        const share = totalWeight > 0 ? thisWeight / totalWeight : 1;

        const effectivePts = comboPtsPerNode * share;

        // Polarity: EB produces the combo element in its own polarity
        const polarity = EB_POLARITY[branch];

        state.bonusNodes.push({
          id: `${p}.EB+${combo.element}_${combo.type}`,
          sourceNode: nodeId,
          pillar: p,
          element: combo.element,
          polarity,
          points: effectivePts,
          source: combo.type,
        });
      }

      // Log the interaction
      state.interactions.push({
        step: 2,
        type: combo.type,
        nodes: combo.pillars.map(p => `${p}.EB`),
        branches: [...combo.branches],
        resultElement: combo.element,
        transformed,
        gapMultiplier: gapMult,
        basis,
        details: `${combo.type}: ${combo.branches.join('+')} → ${combo.element}${transformed ? ' (transformed ×2.5)' : ''}, basis=${basis.toFixed(1)}, gap×${gapMult}`,
      });
    }
  }

  return state;
}

/**
 * Resolve the PillarInput for a given position, handling HP fallback.
 */
function _resolvedPillar(state: WuxingState, pos: PillarPosition): PillarInput {
  const input = state.input;
  if (pos === 'HP') return input.hourPillar ?? input.dayPillar;
  if (pos === 'MP') return input.monthPillar;
  if (pos === 'YP') return input.yearPillar;
  return input.dayPillar;
}

/**
 * Generate all valid pillar combinations for a set of branches.
 * Each branch must come from a different pillar position.
 *
 * E.g., if branches = ['Hai', 'Chou'] and Hai is at MP, Chou is at DP:
 *   → [['MP', 'DP']]
 *
 * If a branch appears in multiple pillars, we get multiple combos.
 */
function _allPillarCombinations(
  branches: BranchName[],
  branchToPillars: Map<BranchName, PillarPosition[]>,
): PillarPosition[][] {
  // For each branch, get its possible pillar positions
  const pillarOptions: PillarPosition[][] = branches.map(b => branchToPillars.get(b) ?? []);

  // Generate cartesian product, filtering out combos where any two branches share a pillar
  const results: PillarPosition[][] = [];
  _cartesian(pillarOptions, 0, [], results);
  return results;
}

/** Recursive cartesian product with distinct-pillar constraint */
function _cartesian(
  options: PillarPosition[][],
  idx: number,
  current: PillarPosition[],
  results: PillarPosition[][],
): void {
  if (idx === options.length) {
    results.push([...current]);
    return;
  }
  for (const pillar of options[idx]) {
    if (current.includes(pillar)) continue; // Each branch must be from a different pillar
    current.push(pillar);
    _cartesian(options, idx + 1, current, results);
    current.pop();
  }
}

// ---------------------------------------------------------------------------
// Step 3: HS Positive Interactions — 天干五合 (Stem Combinations)
// ---------------------------------------------------------------------------

/**
 * Step 3: Scan all visible HS pairs across different pillars for the five
 * stem combinations from STEM_COMBOS_TABLE.
 *
 * Formula:
 *   basis = min(HS₁.points, HS₂.points)
 *   combo_pts_per_node = basis × 0.30 × gap_multiplier
 *   transform_pts = combo_pts_per_node × 2.5 (if transformation condition met)
 *
 * Transformation condition: An EB's main qi anywhere in the chart has the
 * same element as the combo's produced element.
 *
 * Processing order: pillar priority. For each pillar's HS, find valid combos
 * with other pillars' HSs not yet processed.
 */
export function step3HsPositive(state: WuxingState): WuxingState {
  const PILLARS: PillarPosition[] = ['YP', 'MP', 'DP', 'HP'];

  // Collect EB main qi elements for transformation check
  const ebMainQiElements = new Set<Element>();
  for (const pos of PILLARS) {
    const ebNode = state.nodes.find(n => n.id === `${pos}.EB`)!;
    ebMainQiElements.add(ebNode.element);
  }

  // Build stem key helper (alphabetically sorted)
  function stemKey(a: StemName, b: StemName): string {
    return [a, b].sort().join('-');
  }

  // Track which HS nodes have already been processed (consumed by a combo)
  const processedHs = new Set<string>();

  // Process in pillar priority order
  for (const pillarA of state.pillarPriority) {
    const hsA = state.nodes.find(n => n.id === `${pillarA}.HS`)!;
    if (processedHs.has(hsA.id)) continue;

    // Find combo partner from remaining pillars (in priority order)
    for (const pillarB of state.pillarPriority) {
      if (pillarB === pillarA) continue;
      const hsB = state.nodes.find(n => n.id === `${pillarB}.HS`)!;
      if (processedHs.has(hsB.id)) continue;

      const key = stemKey(hsA.stem, hsB.stem);
      const comboData = STEM_COMBOS_TABLE[key];
      if (!comboData) continue;

      // Found a combo
      const basis = Math.min(hsA.points, hsB.points);
      const gap = PILLAR_GAP[pillarA][pillarB];
      const gapMult = gapMultiplier(gap);

      let comboPtsPerNode = basis * COMBO_RATES.STEM_COMBOS * gapMult;

      // Transformation: check if any EB main qi matches combo element
      const transformed = ebMainQiElements.has(comboData.element);
      if (transformed) {
        comboPtsPerNode *= TRANSFORMATION_MULTIPLIER;
      }

      // Create bonus nodes for each participating HS
      state.bonusNodes.push({
        id: `${pillarA}.HS+${comboData.element}_STEM_COMBOS`,
        sourceNode: hsA.id,
        pillar: pillarA,
        element: comboData.element,
        polarity: hsA.polarity,
        points: comboPtsPerNode,
        source: 'STEM_COMBOS',
      });

      state.bonusNodes.push({
        id: `${pillarB}.HS+${comboData.element}_STEM_COMBOS`,
        sourceNode: hsB.id,
        pillar: pillarB,
        element: comboData.element,
        polarity: hsB.polarity,
        points: comboPtsPerNode,
        source: 'STEM_COMBOS',
      });

      // Log
      state.interactions.push({
        step: 3,
        type: 'STEM_COMBOS',
        nodeA: hsA.id,
        nodeB: hsB.id,
        nodes: [hsA.id, hsB.id],
        resultElement: comboData.element,
        transformed,
        gapMultiplier: gapMult,
        basis,
        details: `STEM_COMBOS: ${hsA.stem}+${hsB.stem} → ${comboData.element}${transformed ? ' (transformed ×2.5)' : ''}, basis=${basis.toFixed(1)}, gap×${gapMult}`,
      });

      // Mark both HS as processed
      processedHs.add(hsA.id);
      processedHs.add(hsB.id);
      break; // This HS is consumed, move to next pillar
    }
  }

  return state;
}

// ---------------------------------------------------------------------------
// Step 4: EB Negative Interactions — 六冲/三刑/六害/破
// ---------------------------------------------------------------------------

/**
 * Step 4: Process negative EB interactions in strength order:
 * 六冲 (Six Clashes) → 三刑 (Punishments) → 六害 (Six Harms) → 破 (Destructions)
 *
 * Uses the attention map built in Step 2's pre-scan.
 * EBs are NOT consumed — they can participate in multiple negative interactions.
 * Three-Branch Priority nullifications from Step 2 are respected.
 */
export function step4EbNegative(state: WuxingState): WuxingState {
  const PILLARS: PillarPosition[] = ['YP', 'MP', 'DP', 'HP'];

  // Collect branch -> pillar mapping
  const branchToPillars = new Map<BranchName, PillarPosition[]>();
  for (const pos of PILLARS) {
    const pillar = _resolvedPillar(state, pos);
    const branch = pillar.branch;
    const existing = branchToPillars.get(branch) ?? [];
    existing.push(pos);
    branchToPillars.set(branch, existing);
  }

  const chartBranches = new Set(branchToPillars.keys());

  /**
   * Helper: compute attention share for a node in a specific interaction type.
   */
  function attentionShare(nodeId: string, interactionWeight: number): number {
    const entries = state.attentionMap.get(nodeId) ?? [];
    const totalWeight = entries.reduce((sum, a) => sum + a.weight, 0);
    if (totalWeight <= 0) return 1;
    return interactionWeight / totalWeight;
  }

  /**
   * Helper: apply asymmetric damage to attacker and victim EB nodes.
   */
  function applyDamage(
    attackerNodeId: string,
    victimNodeId: string,
    rates: { attackerLoss: number; victimLoss: number },
    gapMult: number,
    attackerAttShare: number,
    victimAttShare: number,
  ): { attackerLoss: number; victimLoss: number; basis: number } {
    const attackerNode = state.nodes.find(n => n.id === attackerNodeId)!;
    const victimNode = state.nodes.find(n => n.id === victimNodeId)!;
    const basis = Math.min(attackerNode.points, victimNode.points);

    const aLoss = basis * rates.attackerLoss * gapMult * attackerAttShare;
    const vLoss = basis * rates.victimLoss * gapMult * victimAttShare;

    attackerNode.points = Math.max(0, attackerNode.points - aLoss);
    victimNode.points = Math.max(0, victimNode.points - vLoss);

    return { attackerLoss: aLoss, victimLoss: vLoss, basis };
  }

  // -----------------------------------------------------------------------
  // 1. 六冲 Six Clashes (strongest negative)
  // -----------------------------------------------------------------------
  for (const [key, data] of Object.entries(SIX_CLASHES_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (!branches.every(b => chartBranches.has(b))) continue;

    const pillarCombos = _allPillarCombinations(branches, branchToPillars);
    // Sort by pillar priority
    pillarCombos.sort((a, b) => {
      const aIdx = Math.min(...a.map(p => state.pillarPriority.indexOf(p)));
      const bIdx = Math.min(...b.map(p => state.pillarPriority.indexOf(p)));
      return aIdx - bIdx;
    });

    for (const pillars of pillarCombos) {
      if (pillars[0] === pillars[1]) continue;

      if (data.type === 'same') {
        // Same-element clash: log only, no point change
        state.interactions.push({
          step: 4,
          type: 'SIX_CLASH',
          nodes: pillars.map(p => `${p}.EB`),
          branches: [...branches],
          logOnly: true,
          details: `SIX_CLASH (same-element): ${branches.join('-')} at ${pillars.join(',')} — log only`,
        });
      } else {
        // Control clash: asymmetric damage
        // Determine which pillar has the attacker branch and which has the victim
        const attackerBranch = data.attacker!;
        const victimBranch = data.victim!;
        const attackerPillar = pillars[branches.indexOf(attackerBranch)];
        const victimPillar = pillars[branches.indexOf(victimBranch)];

        const attackerNodeId = `${attackerPillar}.EB`;
        const victimNodeId = `${victimPillar}.EB`;
        const gap = PILLAR_GAP[attackerPillar][victimPillar];
        const gapMult = gapMultiplier(gap);

        const aShare = attentionShare(attackerNodeId, ATTENTION_WEIGHTS.SIX_CLASH);
        const vShare = attentionShare(victimNodeId, ATTENTION_WEIGHTS.SIX_CLASH);

        const result = applyDamage(
          attackerNodeId, victimNodeId,
          NEGATIVE_RATES.SIX_CLASH, gapMult,
          aShare, vShare,
        );

        state.interactions.push({
          step: 4,
          type: 'SIX_CLASH',
          nodes: [attackerNodeId, victimNodeId],
          branches: [...branches],
          attacker: `${attackerBranch}(${attackerPillar})`,
          victim: `${victimBranch}(${victimPillar})`,
          basis: result.basis,
          gapMultiplier: gapMult,
          details: `SIX_CLASH: ${attackerBranch}(${attackerPillar}) → ${victimBranch}(${victimPillar}), basis=${result.basis.toFixed(1)}, gap×${gapMult}`,
        });
      }
    }
  }

  // -----------------------------------------------------------------------
  // 2. 三刑 Punishments
  // -----------------------------------------------------------------------
  for (const [_key, data] of Object.entries(PUNISHMENTS_TABLE)) {
    if (data.type === 'self') {
      // Self-punishments: log only if the branch appears in chart
      const branch = _key.split('-')[0] as BranchName;
      if (!chartBranches.has(branch)) continue;
      const branchPillars = branchToPillars.get(branch) ?? [];
      // Need 2+ of the same branch for self-punishment
      if (branchPillars.length < 2) continue;
      state.interactions.push({
        step: 4,
        type: 'PUNISHMENT_SELF',
        branches: [branch, branch],
        logOnly: true,
        details: `PUNISHMENT_SELF: ${branch} at ${branchPillars.join(',')} — log only`,
      });
      continue;
    }

    if (data.type === 'wu_li' && data.requiresAll) {
      // Ungrateful (Chou-Wei-Xu): requires all 3, all Earth -> log only
      const branches = data.branches!;
      if (!branches.every(b => chartBranches.has(b))) continue;

      const pillarCombos = _allPillarCombinations(branches, branchToPillars);
      for (const pillars of pillarCombos) {
        state.interactions.push({
          step: 4,
          type: 'PUNISHMENT_WU_LI',
          nodes: pillars.map(p => `${p}.EB`),
          branches: [...branches],
          logOnly: true,
          details: `PUNISHMENT_WU_LI: ${branches.join('-')} at ${pillars.join(',')} — all Earth, log only`,
        });
      }
      continue;
    }

    if (data.type === 'shi' && data.pairs) {
      // Bullying (Yin-Si-Shen): each PAIR calculated separately. 2 of 3 triggers.
      for (const pairDef of data.pairs) {
        const pairBranches = pairDef.pair;
        if (!pairBranches.every(b => chartBranches.has(b))) continue;

        const pillarCombos = _allPillarCombinations(pairBranches, branchToPillars);
        // Sort by pillar priority
        pillarCombos.sort((a, b) => {
          const aIdx = Math.min(...a.map(p => state.pillarPriority.indexOf(p)));
          const bIdx = Math.min(...b.map(p => state.pillarPriority.indexOf(p)));
          return aIdx - bIdx;
        });

        for (const pillars of pillarCombos) {
          if (pillars[0] === pillars[1]) continue;

          const attackerBranch = pairDef.attacker;
          const victimBranch = pairDef.victim;
          const attackerPillar = pillars[pairBranches.indexOf(attackerBranch)];
          const victimPillar = pillars[pairBranches.indexOf(victimBranch)];

          const attackerNodeId = `${attackerPillar}.EB`;
          const victimNodeId = `${victimPillar}.EB`;
          const gap = PILLAR_GAP[attackerPillar][victimPillar];
          const gapMult = gapMultiplier(gap);

          const aShare = attentionShare(attackerNodeId, ATTENTION_WEIGHTS.PUNISHMENT_FULL);
          const vShare = attentionShare(victimNodeId, ATTENTION_WEIGHTS.PUNISHMENT_FULL);

          const result = applyDamage(
            attackerNodeId, victimNodeId,
            NEGATIVE_RATES.PUNISHMENT, gapMult,
            aShare, vShare,
          );

          state.interactions.push({
            step: 4,
            type: 'PUNISHMENT_SHI',
            nodes: [attackerNodeId, victimNodeId],
            branches: [...pairBranches],
            attacker: `${attackerBranch}(${attackerPillar})`,
            victim: `${victimBranch}(${victimPillar})`,
            basis: result.basis,
            gapMultiplier: gapMult,
            details: `PUNISHMENT_SHI: ${attackerBranch}(${attackerPillar}) → ${victimBranch}(${victimPillar}), basis=${result.basis.toFixed(1)}, gap×${gapMult}`,
          });
        }
      }
      continue;
    }

    if (data.type === 'en' && data.attacker && data.victim) {
      // Rude (Zi-Mao): pair punishment
      const attackerBranch = data.attacker;
      const victimBranch = data.victim;
      if (!chartBranches.has(attackerBranch) || !chartBranches.has(victimBranch)) continue;

      const pillarCombos = _allPillarCombinations(
        [attackerBranch, victimBranch],
        branchToPillars,
      );

      pillarCombos.sort((a, b) => {
        const aIdx = Math.min(...a.map(p => state.pillarPriority.indexOf(p)));
        const bIdx = Math.min(...b.map(p => state.pillarPriority.indexOf(p)));
        return aIdx - bIdx;
      });

      for (const pillars of pillarCombos) {
        if (pillars[0] === pillars[1]) continue;

        const attackerPillar = pillars[0]; // first is attacker branch
        const victimPillar = pillars[1]; // second is victim branch

        const attackerNodeId = `${attackerPillar}.EB`;
        const victimNodeId = `${victimPillar}.EB`;
        const gap = PILLAR_GAP[attackerPillar][victimPillar];
        const gapMult = gapMultiplier(gap);

        const aShare = attentionShare(attackerNodeId, ATTENTION_WEIGHTS.PUNISHMENT_FULL);
        const vShare = attentionShare(victimNodeId, ATTENTION_WEIGHTS.PUNISHMENT_FULL);

        const result = applyDamage(
          attackerNodeId, victimNodeId,
          NEGATIVE_RATES.PUNISHMENT, gapMult,
          aShare, vShare,
        );

        state.interactions.push({
          step: 4,
          type: 'PUNISHMENT_EN',
          nodes: [attackerNodeId, victimNodeId],
          branches: [attackerBranch, victimBranch],
          attacker: `${attackerBranch}(${attackerPillar})`,
          victim: `${victimBranch}(${victimPillar})`,
          basis: result.basis,
          gapMultiplier: gapMult,
          details: `PUNISHMENT_EN: ${attackerBranch}(${attackerPillar}) → ${victimBranch}(${victimPillar}), basis=${result.basis.toFixed(1)}, gap×${gapMult}`,
        });
      }
    }
  }

  // -----------------------------------------------------------------------
  // 3. 六害 Six Harms (ADJACENT ONLY — gap 0)
  // -----------------------------------------------------------------------
  for (const [key, data] of Object.entries(SIX_HARMS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (!branches.every(b => chartBranches.has(b))) continue;

    const pillarCombos = _allPillarCombinations(branches, branchToPillars);
    pillarCombos.sort((a, b) => {
      const aIdx = Math.min(...a.map(p => state.pillarPriority.indexOf(p)));
      const bIdx = Math.min(...b.map(p => state.pillarPriority.indexOf(p)));
      return aIdx - bIdx;
    });

    for (const pillars of pillarCombos) {
      if (pillars[0] === pillars[1]) continue;
      const gap = PILLAR_GAP[pillars[0]][pillars[1]];
      if (gap !== 0) continue; // Only adjacent

      const attackerBranch = data.attacker;
      const victimBranch = data.victim;
      const attackerPillar = pillars[branches.indexOf(attackerBranch)];
      const victimPillar = pillars[branches.indexOf(victimBranch)];

      const attackerNodeId = `${attackerPillar}.EB`;
      const victimNodeId = `${victimPillar}.EB`;
      const gapMult = gapMultiplier(0); // Always 1.0

      const aShare = attentionShare(attackerNodeId, ATTENTION_WEIGHTS.SIX_HARM);
      const vShare = attentionShare(victimNodeId, ATTENTION_WEIGHTS.SIX_HARM);

      const result = applyDamage(
        attackerNodeId, victimNodeId,
        NEGATIVE_RATES.SIX_HARM, gapMult,
        aShare, vShare,
      );

      state.interactions.push({
        step: 4,
        type: 'SIX_HARM',
        nodes: [attackerNodeId, victimNodeId],
        branches: [...branches],
        attacker: `${attackerBranch}(${attackerPillar})`,
        victim: `${victimBranch}(${victimPillar})`,
        basis: result.basis,
        gapMultiplier: gapMult,
        details: `SIX_HARM: ${attackerBranch}(${attackerPillar}) → ${victimBranch}(${victimPillar}), basis=${result.basis.toFixed(1)}, gap×${gapMult}`,
      });
    }
  }

  // -----------------------------------------------------------------------
  // 4. 破 Destructions (weakest negative)
  // -----------------------------------------------------------------------
  for (const [key, data] of Object.entries(DESTRUCTIONS_TABLE)) {
    const branches = key.split('-') as BranchName[];
    if (!branches.every(b => chartBranches.has(b))) continue;

    const pillarCombos = _allPillarCombinations(branches, branchToPillars);
    pillarCombos.sort((a, b) => {
      const aIdx = Math.min(...a.map(p => state.pillarPriority.indexOf(p)));
      const bIdx = Math.min(...b.map(p => state.pillarPriority.indexOf(p)));
      return aIdx - bIdx;
    });

    for (const pillars of pillarCombos) {
      if (pillars[0] === pillars[1]) continue;

      if (data.type === 'same') {
        // Same-element destruction: log only
        state.interactions.push({
          step: 4,
          type: 'DESTRUCTION',
          nodes: pillars.map(p => `${p}.EB`),
          branches: [...branches],
          logOnly: true,
          details: `DESTRUCTION (same-element): ${branches.join('-')} at ${pillars.join(',')} — log only`,
        });
      } else {
        // Different-element destruction
        const attackerBranch = data.attacker!;
        const victimBranch = data.victim!;
        const attackerPillar = pillars[branches.indexOf(attackerBranch)];
        const victimPillar = pillars[branches.indexOf(victimBranch)];

        const attackerNodeId = `${attackerPillar}.EB`;
        const victimNodeId = `${victimPillar}.EB`;
        const gap = PILLAR_GAP[attackerPillar][victimPillar];
        const gapMult = gapMultiplier(gap);

        const aShare = attentionShare(attackerNodeId, ATTENTION_WEIGHTS.DESTRUCTION);
        const vShare = attentionShare(victimNodeId, ATTENTION_WEIGHTS.DESTRUCTION);

        const result = applyDamage(
          attackerNodeId, victimNodeId,
          NEGATIVE_RATES.DESTRUCTION, gapMult,
          aShare, vShare,
        );

        state.interactions.push({
          step: 4,
          type: 'DESTRUCTION',
          nodes: [attackerNodeId, victimNodeId],
          branches: [...branches],
          attacker: `${attackerBranch}(${attackerPillar})`,
          victim: `${victimBranch}(${victimPillar})`,
          basis: result.basis,
          gapMultiplier: gapMult,
          details: `DESTRUCTION: ${attackerBranch}(${attackerPillar}) → ${victimBranch}(${victimPillar}), basis=${result.basis.toFixed(1)}, gap×${gapMult}`,
        });
      }
    }
  }

  return state;
}

// ---------------------------------------------------------------------------
// Step 5: HS Negative Interactions — 天干四冲 (Stem Clashes)
// ---------------------------------------------------------------------------

/**
 * Step 5: Scan visible HS pairs across different pillars for 4 stem clashes.
 *
 * Formula:
 *   basis = min(HS₁.points, HS₂.points)
 *   controller loses: basis × 0.25 × gap_multiplier
 *   controlled loses: basis × 0.50 × gap_multiplier
 *
 * No attention spread for HS clashes.
 */
export function step5HsNegative(state: WuxingState): WuxingState {
  const PILLARS: PillarPosition[] = ['YP', 'MP', 'DP', 'HP'];

  // Build stem key helper (alphabetically sorted)
  function stemKey(a: StemName, b: StemName): string {
    return [a, b].sort().join('-');
  }

  // Check all HS pairs (process in pillar priority order)
  const processedPairs = new Set<string>();

  for (const pillarA of state.pillarPriority) {
    const hsA = state.nodes.find(n => n.id === `${pillarA}.HS`)!;

    for (const pillarB of state.pillarPriority) {
      if (pillarB === pillarA) continue;

      // Avoid processing same pair twice
      const pairKey = [pillarA, pillarB].sort().join('-');
      if (processedPairs.has(pairKey)) continue;

      const hsB = state.nodes.find(n => n.id === `${pillarB}.HS`)!;
      const key = stemKey(hsA.stem, hsB.stem);
      const clashData = STEM_CLASHES_TABLE[key];
      if (!clashData) continue;

      processedPairs.add(pairKey);

      // Determine controller and controlled
      const controllerStem = clashData.controller;
      const controlledStem = clashData.controlled;
      const controllerNode = hsA.stem === controllerStem ? hsA : hsB;
      const controlledNode = hsA.stem === controlledStem ? hsA : hsB;
      const controllerPillar = controllerNode === hsA ? pillarA : pillarB;
      const controlledPillar = controlledNode === hsA ? pillarA : pillarB;

      const basis = Math.min(controllerNode.points, controlledNode.points);
      const gap = PILLAR_GAP[controllerPillar][controlledPillar];
      const gapMult = gapMultiplier(gap);

      const controllerLoss = basis * NEGATIVE_RATES.STEM_CLASH.attackerLoss * gapMult;
      const controlledLoss = basis * NEGATIVE_RATES.STEM_CLASH.victimLoss * gapMult;

      controllerNode.points = Math.max(0, controllerNode.points - controllerLoss);
      controlledNode.points = Math.max(0, controlledNode.points - controlledLoss);

      state.interactions.push({
        step: 5,
        type: 'STEM_CLASH',
        nodeA: controllerNode.id,
        nodeB: controlledNode.id,
        nodes: [controllerNode.id, controlledNode.id],
        attacker: `${controllerStem}(${controllerPillar})`,
        victim: `${controlledStem}(${controlledPillar})`,
        basis,
        gapMultiplier: gapMult,
        details: `STEM_CLASH: ${controllerStem}(${controllerPillar}) controls ${controlledStem}(${controlledPillar}), basis=${basis.toFixed(1)}, gap×${gapMult}`,
      });
    }
  }

  return state;
}

// ---------------------------------------------------------------------------
// Step 6: Seasonal Adjustment — 令调
// ---------------------------------------------------------------------------

/**
 * Step 6: Apply percentage multiplier to every node (HS, EB main qi, h1, h2)
 * and every bonus node based on the season determined by the month branch.
 *
 * For each node:
 *   1. Look up element's state: SEASONAL_MATRIX[season][node.element]
 *   2. Get multiplier: SEASONAL_MULTIPLIERS[state]
 *   3. node.points = node.points × multiplier
 *   4. Store node.seasonalMultiplier = multiplier
 */
export function step6Seasonal(state: WuxingState): WuxingState {
  const season = state.season;

  // Apply to all primary nodes
  for (const node of state.nodes) {
    const seasonalState = SEASONAL_MATRIX[season][node.element];
    const multiplier = SEASONAL_MULTIPLIERS[seasonalState];
    node.points = node.points * multiplier;
    node.seasonalMultiplier = multiplier;
  }

  // Apply to all bonus nodes
  for (const bonus of state.bonusNodes) {
    const seasonalState = SEASONAL_MATRIX[season][bonus.element];
    const multiplier = SEASONAL_MULTIPLIERS[seasonalState];
    bonus.points = bonus.points * multiplier;
  }

  return state;
}

// ---------------------------------------------------------------------------
// Step 7: Natural Element Flow 自然五行流转
// ---------------------------------------------------------------------------

/**
 * A "flow node" represents a visible node participating in cross-pillar
 * element interactions. Can be a native HS/EB or a bonus node, each
 * tagged with its grid position for gap calculation.
 */
interface FlowNode {
  id: string;            // node ID (e.g. 'YP.HS', 'MP.EB+Fire_SIX_HARMONIES')
  pillar: PillarPosition;
  row: 0 | 1;           // 0 = HS row, 1 = EB row
  element: Element;
  /** Live mutable reference to the actual points value */
  getPoints: () => number;
  setPoints: (v: number) => void;
  isBonus: boolean;
  /** Grid key for getStep7Gap, e.g. 'YP.HS' or 'MP.EB' */
  gridKey: string;
}

/**
 * Step 7: Natural Element Flow — cross-pillar Wu Xing production/control
 * interactions at half Step 1 rates.
 *
 * Scope:
 *   - Each pillar's HS (primary qi)
 *   - Each pillar's EB main qi (primary qi)
 *   - Bonus qi from Step 2/3 combos and transformations
 *   - Excluded: hidden stems (h1, h2)
 *   - Excluded: same-pillar native HS <-> native EB (already in Step 1)
 *
 * Rates (half of Step 1):
 *   Production: producer -10% of basis, produced +15% of basis
 *   Control:    controller -10% of basis, controlled -15% of basis
 *
 * Gap multipliers based on Manhattan distance - 1 on the 2x4 grid.
 * Processing order: pillar priority, then gap ascending, production before control.
 */
export function step7NaturalFlow(state: WuxingState): WuxingState {
  // -- 1. Build flow nodes ------------------------------------------------

  const flowNodes: FlowNode[] = [];

  // Map for same-element bonus consolidation: gridKey -> FlowNode
  // If a bonus node at a position has the same element as the native node
  // there, combine their points into one FlowNode for interaction purposes.
  const consolidatedMap = new Map<string, FlowNode>();

  // Add native HS and EB main qi nodes
  for (const pos of ['YP', 'MP', 'DP', 'HP'] as PillarPosition[]) {
    const hsNode = state.nodes.find(n => n.id === `${pos}.HS`)!;
    const ebNode = state.nodes.find(n => n.id === `${pos}.EB`)!;

    const hsFlow: FlowNode = {
      id: hsNode.id,
      pillar: pos,
      row: 0,
      element: hsNode.element,
      getPoints: () => hsNode.points,
      setPoints: (v) => { hsNode.points = v; },
      isBonus: false,
      gridKey: `${pos}.HS`,
    };
    flowNodes.push(hsFlow);
    consolidatedMap.set(`${pos}.HS:${hsNode.element}`, hsFlow);

    const ebFlow: FlowNode = {
      id: ebNode.id,
      pillar: pos,
      row: 1,
      element: ebNode.element,
      getPoints: () => ebNode.points,
      setPoints: (v) => { ebNode.points = v; },
      isBonus: false,
      gridKey: `${pos}.EB`,
    };
    flowNodes.push(ebFlow);
    consolidatedMap.set(`${pos}.EB:${ebNode.element}`, ebFlow);
  }

  // Add bonus nodes
  for (const bonus of state.bonusNodes) {
    // Determine grid position from sourceNode
    const sourceId = bonus.sourceNode; // e.g. 'YP.EB' or 'MP.HS'
    const parts = sourceId.split('.');
    const bonusPillar = parts[0] as PillarPosition;
    const sourceSlot = parts[1]; // 'HS' or 'EB'
    const bonusRow: 0 | 1 = sourceSlot === 'HS' ? 0 : 1;
    const gridKey = `${bonusPillar}.${sourceSlot}`;

    // Same-element bonus consolidation check
    const consolidationKey = `${gridKey}:${bonus.element}`;
    const existing = consolidatedMap.get(consolidationKey);

    if (existing) {
      // Same element at same position — consolidate.
      // Create a combined flow node that reads/writes the sum of both.
      // We wrap the existing node to include the bonus's points.
      const origGetPoints = existing.getPoints;
      const origSetPoints = existing.setPoints;
      const bonusRef = bonus;

      // Replace the flow node's getter/setter to include bonus points
      existing.getPoints = () => origGetPoints() + bonusRef.points;
      existing.setPoints = (v: number) => {
        // Distribute delta proportionally between original and bonus
        const origPts = origGetPoints();
        const bonusPts = bonusRef.points;
        const total = origPts + bonusPts;
        if (total > 0) {
          const origShare = origPts / total;
          origSetPoints(v * origShare);
          bonusRef.points = v * (1 - origShare);
        } else {
          origSetPoints(v);
        }
      };
      // Update the ID to show consolidation
      existing.id = `${existing.id}+consolidated`;
    } else {
      // Different element or no native at this position — add as separate flow node
      const bonusFlow: FlowNode = {
        id: bonus.id,
        pillar: bonusPillar,
        row: bonusRow,
        element: bonus.element,
        getPoints: () => bonus.points,
        setPoints: (v) => { bonus.points = v; },
        isBonus: true,
        gridKey,
      };
      flowNodes.push(bonusFlow);
      consolidatedMap.set(consolidationKey, bonusFlow);
    }
  }

  // -- 2. Generate all unique pairs, excluding same-pillar native HS<->EB --

  interface FlowPair {
    a: FlowNode;
    b: FlowNode;
    gap: number;
    gapMult: number;
    relation: 'produces' | 'controls' | 'produced_by' | 'controlled_by';
    anchorPillar: PillarPosition; // which pillar "anchors" this pair
  }

  const allPairs: FlowPair[] = [];

  for (let i = 0; i < flowNodes.length; i++) {
    for (let j = i + 1; j < flowNodes.length; j++) {
      const a = flowNodes[i];
      const b = flowNodes[j];

      // Skip same-element pairs
      if (a.element === b.element) continue;

      // Skip same-pillar native HS <-> native EB (already handled in Step 1)
      if (
        a.pillar === b.pillar &&
        !a.isBonus && !b.isBonus &&
        ((a.row === 0 && b.row === 1) || (a.row === 1 && b.row === 0))
      ) {
        continue;
      }

      // Compute gap using grid keys
      const gap = getStep7Gap(a.gridKey, b.gridKey);
      const gapMult = gapMultiplier(gap);

      // Determine relationship from A's perspective
      const rel = CONTROL_LOOKUP[a.element][b.element];
      let relation: FlowPair['relation'];
      switch (rel) {
        case 'HS_PRODUCES_EB': relation = 'produces'; break;
        case 'EB_PRODUCES_HS': relation = 'produced_by'; break;
        case 'HS_CONTROLS_EB': relation = 'controls'; break;
        case 'EB_CONTROLS_HS': relation = 'controlled_by'; break;
        default: continue; // SAME — skip
      }

      // Anchor pillar = the highest-priority pillar among the pair's pillars
      const aPriIdx = state.pillarPriority.indexOf(a.pillar);
      const bPriIdx = state.pillarPriority.indexOf(b.pillar);
      const anchorPillar = aPriIdx <= bPriIdx ? a.pillar : b.pillar;

      allPairs.push({ a, b, gap, gapMult, relation, anchorPillar });
    }
  }

  // -- 3. Sort by pillar priority -> gap ascending -> production before control

  /** Returns 0 for production/produced_by, 1 for controls/controlled_by */
  function relationSortKey(rel: FlowPair['relation']): number {
    return (rel === 'produces' || rel === 'produced_by') ? 0 : 1;
  }

  allPairs.sort((x, y) => {
    // Primary: anchor pillar priority
    const xPri = state.pillarPriority.indexOf(x.anchorPillar);
    const yPri = state.pillarPriority.indexOf(y.anchorPillar);
    if (xPri !== yPri) return xPri - yPri;

    // Secondary: gap ascending (closest first)
    if (x.gap !== y.gap) return x.gap - y.gap;

    // Tertiary: production before control
    return relationSortKey(x.relation) - relationSortKey(y.relation);
  });

  // -- 4. Process each pair with continuous basis ---------------------

  const PRODUCER_LOSS_RATE = 0.10;   // Half of Step 1's 20%
  const PRODUCED_GAIN_RATE = 0.15;   // Half of Step 1's 30%
  const CONTROLLER_LOSS_RATE = 0.10; // Half of Step 1's 20%
  const CONTROLLED_LOSS_RATE = 0.15; // Half of Step 1's 30%

  for (const pair of allPairs) {
    const { a, b, gapMult, relation } = pair;
    const aPts = a.getPoints();
    const bPts = b.getPoints();
    const basis = Math.min(aPts, bPts);

    if (basis <= 0) continue; // Skip if either node is depleted

    let logRelation: string;
    let logDetails: string;

    switch (relation) {
      case 'produces': {
        // A produces B: A loses, B gains
        const loss = basis * PRODUCER_LOSS_RATE * gapMult;
        const gain = basis * PRODUCED_GAIN_RATE * gapMult;
        a.setPoints(Math.max(0, aPts - loss));
        b.setPoints(bPts + gain);
        logRelation = 'produces';
        logDetails = `${a.id}(${a.element}) produces ${b.id}(${b.element}), basis=${basis.toFixed(2)}, gap×${gapMult}, loss=${loss.toFixed(2)}, gain=${gain.toFixed(2)}`;
        break;
      }
      case 'produced_by': {
        // B produces A: B loses, A gains
        const loss = basis * PRODUCER_LOSS_RATE * gapMult;
        const gain = basis * PRODUCED_GAIN_RATE * gapMult;
        b.setPoints(Math.max(0, bPts - loss));
        a.setPoints(aPts + gain);
        logRelation = 'produced_by';
        logDetails = `${b.id}(${b.element}) produces ${a.id}(${a.element}), basis=${basis.toFixed(2)}, gap×${gapMult}, loss=${loss.toFixed(2)}, gain=${gain.toFixed(2)}`;
        break;
      }
      case 'controls': {
        // A controls B: both lose
        const controllerLoss = basis * CONTROLLER_LOSS_RATE * gapMult;
        const controlledLoss = basis * CONTROLLED_LOSS_RATE * gapMult;
        a.setPoints(Math.max(0, aPts - controllerLoss));
        b.setPoints(Math.max(0, bPts - controlledLoss));
        logRelation = 'controls';
        logDetails = `${a.id}(${a.element}) controls ${b.id}(${b.element}), basis=${basis.toFixed(2)}, gap×${gapMult}, controllerLoss=${controllerLoss.toFixed(2)}, controlledLoss=${controlledLoss.toFixed(2)}`;
        break;
      }
      case 'controlled_by': {
        // B controls A: both lose
        const controllerLoss = basis * CONTROLLER_LOSS_RATE * gapMult;
        const controlledLoss = basis * CONTROLLED_LOSS_RATE * gapMult;
        b.setPoints(Math.max(0, bPts - controllerLoss));
        a.setPoints(Math.max(0, aPts - controlledLoss));
        logRelation = 'controlled_by';
        logDetails = `${b.id}(${b.element}) controls ${a.id}(${a.element}), basis=${basis.toFixed(2)}, gap×${gapMult}, controllerLoss=${controllerLoss.toFixed(2)}, controlledLoss=${controlledLoss.toFixed(2)}`;
        break;
      }
    }

    state.interactions.push({
      step: 7,
      type: 'NATURAL_FLOW',
      nodeA: a.id,
      nodeB: b.id,
      relationship: logRelation,
      basis,
      gapMultiplier: gapMult,
      details: logDetails,
    });
  }

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
 * All 10 Heavenly Stems in order, for iteration during balance simulation.
 */
const ALL_STEMS: StemName[] = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'];

/**
 * For each of the 10 stems, simulate adding a hovering +10pt HS node at gap 1
 * to all natal visible nodes. Run half-rate Step 7 interactions between the
 * hovering HS and each visible node (HS + EB main qi, excluding hidden stems).
 *
 * After interactions, compute element percentages and σ:
 *   σ = √(Σ(pᵢ − 20%)² / 5) + DM penalty (+5 if DM<8%, +3 if DM>40%)
 *
 * Group by element (average σ for same-element stems — e.g., 甲 and 乙 are both Wood).
 * Lowest σ → 用神 (useful), highest σ → 忌神 (unfavorable).
 * 喜神 = produces 用神, 仇神 = produces 忌神, 闲神 = remaining.
 */
export function step9BalanceSim(
  state: WuxingState,
  _elementSummary: Record<Element, ElementSummary>,
): FiveGods {
  const dmElement = HS_POINTS[state.input.dayPillar.stem].element;

  // Collect base element totals from ALL nodes (primary + bonus)
  const baseTotals: Record<Element, number> = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };
  for (const node of state.nodes) {
    baseTotals[node.element] += node.points;
  }
  for (const bonus of state.bonusNodes) {
    baseTotals[bonus.element] += bonus.points;
  }

  // Collect visible nodes: HS + EB main qi (not hidden stems h1/h2)
  // These are the nodes that the hovering HS interacts with.
  const visibleNodes: Array<{ element: Element; points: number }> = [];
  for (const node of state.nodes) {
    if (node.slot === 'HS' || node.slot === 'EB') {
      visibleNodes.push({ element: node.element, points: node.points });
    }
  }

  // Half-rate interaction constants (same as Step 7)
  const PRODUCER_LOSS_RATE = 0.10;
  const PRODUCED_GAIN_RATE = 0.15;
  const CONTROLLER_LOSS_RATE = 0.10;
  const CONTROLLED_LOSS_RATE = 0.15;

  // Gap multiplier for gap 1 = 0.75
  const GAP_MULT = gapMultiplier(1);

  // Per-stem sigma results
  const stemSigmas: Array<{ stem: StemName; element: Element; sigma: number }> = [];

  for (const stem of ALL_STEMS) {
    const hoveringElement = HS_POINTS[stem].element;
    let hoveringPts = 10; // Start with 10 points

    // Track element deltas from interactions
    const deltas: Record<Element, number> = { Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0 };

    // The hovering HS starts with +10 to its element
    deltas[hoveringElement] += 10;

    // Process interactions with each visible node (continuous basis — hovering pts update)
    for (const natal of visibleNodes) {
      if (hoveringPts <= 0) break;
      if (natal.points <= 0) continue;

      const rel = CONTROL_LOOKUP[hoveringElement][natal.element];
      if (rel === 'SAME') continue;

      const basis = Math.min(hoveringPts, natal.points);

      switch (rel) {
        case 'HS_PRODUCES_EB': {
          // Hovering produces natal: hovering loses, natal gains
          const loss = basis * PRODUCER_LOSS_RATE * GAP_MULT;
          const gain = basis * PRODUCED_GAIN_RATE * GAP_MULT;
          hoveringPts -= loss;
          deltas[hoveringElement] -= loss;
          deltas[natal.element] += gain;
          break;
        }
        case 'EB_PRODUCES_HS': {
          // Natal produces hovering: natal loses, hovering gains
          const loss = basis * PRODUCER_LOSS_RATE * GAP_MULT;
          const gain = basis * PRODUCED_GAIN_RATE * GAP_MULT;
          deltas[natal.element] -= loss;
          hoveringPts += gain;
          deltas[hoveringElement] += gain;
          break;
        }
        case 'HS_CONTROLS_EB': {
          // Hovering controls natal: both lose
          const controllerLoss = basis * CONTROLLER_LOSS_RATE * GAP_MULT;
          const controlledLoss = basis * CONTROLLED_LOSS_RATE * GAP_MULT;
          hoveringPts -= controllerLoss;
          deltas[hoveringElement] -= controllerLoss;
          deltas[natal.element] -= controlledLoss;
          break;
        }
        case 'EB_CONTROLS_HS': {
          // Natal controls hovering: both lose
          const controllerLoss = basis * CONTROLLER_LOSS_RATE * GAP_MULT;
          const controlledLoss = basis * CONTROLLED_LOSS_RATE * GAP_MULT;
          deltas[natal.element] -= controllerLoss;
          hoveringPts -= controlledLoss;
          deltas[hoveringElement] -= controlledLoss;
          break;
        }
      }
    }

    // Compute new element totals after simulation
    const newTotals: Record<Element, number> = { ...baseTotals };
    for (const el of ELEMENTS) {
      newTotals[el] = Math.max(0, newTotals[el] + deltas[el]);
    }

    const newGrand = ELEMENTS.reduce((s, el) => s + newTotals[el], 0);

    // Compute sigma
    let sumSqDev = 0;
    for (const el of ELEMENTS) {
      const pct = newGrand > 0 ? (newTotals[el] / newGrand) * 100 : 0;
      sumSqDev += (pct - 20) ** 2;
    }
    let sigma = Math.sqrt(sumSqDev / 5);

    // DM penalty
    const dmPct = newGrand > 0 ? (newTotals[dmElement] / newGrand) * 100 : 0;
    if (dmPct < 8) sigma += 5;
    if (dmPct > 40) sigma += 3;

    stemSigmas.push({ stem, element: hoveringElement, sigma });
  }

  // Group by element and average sigma for same-element stems
  const elementSigmaMap: Record<Element, number[]> = {
    Wood: [], Fire: [], Earth: [], Metal: [], Water: [],
  };
  for (const entry of stemSigmas) {
    elementSigmaMap[entry.element].push(entry.sigma);
  }

  const elementSigmas: Array<{ element: Element; avgSigma: number }> = ELEMENTS.map(el => ({
    element: el,
    avgSigma: elementSigmaMap[el].length > 0
      ? elementSigmaMap[el].reduce((s, v) => s + v, 0) / elementSigmaMap[el].length
      : Infinity,
  }));

  // Sort by avgSigma ascending (most beneficial first)
  elementSigmas.sort((a, b) => a.avgSigma - b.avgSigma);

  const useful = elementSigmas[0].element;
  const unfavorable = elementSigmas[4].element;

  // Preferred: favorable = produces useful, enemy = produces unfavorable
  const preferredFavorable = ELEMENTS.find(el => PRODUCES[el] === useful)!;
  const preferredEnemy = ELEMENTS.find(el => PRODUCES[el] === unfavorable)!;

  let favorable: Element;
  let enemy: Element;
  let idle: Element;

  // Check for collisions: all 5 gods must be distinct elements
  if (
    preferredFavorable !== useful &&
    preferredFavorable !== unfavorable &&
    preferredEnemy !== useful &&
    preferredEnemy !== unfavorable &&
    preferredFavorable !== preferredEnemy
  ) {
    // No collision — use preferred assignments
    favorable = preferredFavorable;
    enemy = preferredEnemy;
    const assigned = new Set([useful, favorable, unfavorable, enemy]);
    idle = ELEMENTS.find(el => !assigned.has(el))!;
  } else {
    // Collision — use σ ranking to assign roles
    // σ rank: [0]=useful, [1]=2nd best, [2]=3rd, [3]=4th, [4]=unfavorable
    // favorable = 2nd best σ (most beneficial after useful)
    // enemy = 4th best σ (least beneficial before unfavorable)
    // idle = remaining (3rd)
    favorable = elementSigmas[1].element;
    enemy = elementSigmas[3].element;
    idle = elementSigmas[2].element;
  }

  return { useful, favorable, unfavorable, enemy, idle };
}

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

/**
 * Run the full Wu Xing calculator pipeline.
 * Steps 0-9 all produce real data.
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
  if (dmPercent > 40) strength = 'dominant';
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
