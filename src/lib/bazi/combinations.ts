import 'server-only';

// =============================================================================
// POSITIVE COMBINATION PATTERNS (DERIVED FROM CORE)
// =============================================================================
// All positive/supportive branch and stem interactions
// Patterns are DERIVED from the core.ts STEMS and BRANCHES.

import { STEMS, BRANCHES, type StemName, type BranchName, type Element } from './core';
import { ELEMENT_POLARITY_TO_STEM } from './derived';
import { BASE_SCORES, DISTANCE_MULTIPLIERS, generateScoring } from './scoring';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface BranchCombination {
  readonly branches: readonly string[];
  readonly element: Element;
  readonly scoring: Record<string, Record<string, number>>;
}

export interface HalfMeetingEntry {
  readonly branches: readonly string[];
  readonly element: Element;
  readonly missing: string;
  readonly blocked_by: readonly string[];
  readonly scoring: Record<string, Record<string, number>>;
}

export interface ArchedCombinationEntry {
  readonly branches: readonly string[];
  readonly element: Element;
  readonly missing: string;
  readonly scoring: { detected: Record<string, number> };
}

export interface StemCombinationEntry {
  readonly interaction_type: "HS_COMBINATIONS";
  readonly transform_to: StemName | undefined;
  readonly transform_element: Element;
  readonly transformation_requirement: {
    readonly element: Element;
    readonly location: "eb";
  };
  readonly scoring: Record<string, Record<string, number>>;
  readonly meaning: Record<string, never>;
}

// ---------------------------------------------------------------------------
// THREE MEETINGS (三會 - Seasonal Directional Combos)
// ---------------------------------------------------------------------------

const _THREE_MEETINGS_SCORING = generateScoring(
  BASE_SCORES.THREE_MEETINGS.combined,
  BASE_SCORES.THREE_MEETINGS.transformed,
  "three_branch",
);

const _seasonCombosSeen = new Set<string>();
const _threeMeetings: Record<string, BranchCombination> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const seasonCombo = branch.season_combo;
  if (seasonCombo) {
    const key = `${seasonCombo[0]}-${seasonCombo[1]}-${seasonCombo[2]}`;
    if (!_seasonCombosSeen.has(key)) {
      _seasonCombosSeen.add(key);
      _threeMeetings[key] = {
        branches: [seasonCombo[0], seasonCombo[1], seasonCombo[2]],
        element: seasonCombo[3],
        scoring: _THREE_MEETINGS_SCORING,
      };
    }
  }
}
export const THREE_MEETINGS: Readonly<Record<string, BranchCombination>> = _threeMeetings;

// ---------------------------------------------------------------------------
// THREE COMBINATIONS (三合 - Triangular Combos)
// ---------------------------------------------------------------------------

const _THREE_COMBINATIONS_SCORING = generateScoring(
  BASE_SCORES.THREE_COMBINATIONS.combined,
  BASE_SCORES.THREE_COMBINATIONS.transformed,
  "three_branch",
);

const _threeCombosSeen = new Set<string>();
const _threeCombinations: Record<string, BranchCombination> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const threeCombo = branch.three_combo;
  if (threeCombo) {
    const key = `${threeCombo[0]}-${threeCombo[1]}-${threeCombo[2]}`;
    if (!_threeCombosSeen.has(key)) {
      _threeCombosSeen.add(key);
      _threeCombinations[key] = {
        branches: [threeCombo[0], threeCombo[1], threeCombo[2]],
        element: threeCombo[3],
        scoring: _THREE_COMBINATIONS_SCORING,
      };
    }
  }
}
export const THREE_COMBINATIONS: Readonly<Record<string, BranchCombination>> = _threeCombinations;

// ---------------------------------------------------------------------------
// HALF MEETINGS (半會) - Requires Earth (storage) branch to be present
// ---------------------------------------------------------------------------

const _HALF_MEETINGS_SCORING = generateScoring(
  BASE_SCORES.HALF_MEETINGS.combined,
  BASE_SCORES.HALF_MEETINGS.transformed,
  "two_branch",
);

export const HALF_MEETINGS: Readonly<Record<string, HalfMeetingEntry>> = {
  // Winter/Water - Hai-Zi-Chou, Earth=Chou
  "Hai-Chou": {
    branches: ["Hai", "Chou"],
    element: "Water",
    missing: "Zi",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
  // Spring/Wood - Yin-Mao-Chen, Earth=Chen
  "Yin-Chen": {
    branches: ["Yin", "Chen"],
    element: "Wood",
    missing: "Mao",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
  "Mao-Chen": {
    branches: ["Mao", "Chen"],
    element: "Wood",
    missing: "Yin",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
  // Summer/Fire - Si-Wu-Wei, Earth=Wei
  "Si-Wei": {
    branches: ["Si", "Wei"],
    element: "Fire",
    missing: "Wu",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
  // Autumn/Metal - Shen-You-Xu, Earth=Xu
  "Shen-Xu": {
    branches: ["Shen", "Xu"],
    element: "Metal",
    missing: "You",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
  "You-Xu": {
    branches: ["You", "Xu"],
    element: "Metal",
    missing: "Shen",
    blocked_by: [],
    scoring: _HALF_MEETINGS_SCORING,
  },
};

// ---------------------------------------------------------------------------
// SIX HARMONIES (六合 - Pair Combinations)
// ---------------------------------------------------------------------------

const _SIX_HARMONIES_SCORING = generateScoring(
  BASE_SCORES.SIX_HARMONIES.combined,
  BASE_SCORES.SIX_HARMONIES.transformed,
  "two_branch",
);

const _harmoniesSeen = new Set<string>();
const _sixHarmonies: Record<string, BranchCombination> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const partner = branch.harmonizes;
  const harmonyElement = branch.harmony_element;
  if (partner && harmonyElement) {
    const pair = [branchId, partner].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_harmoniesSeen.has(pairKey)) {
      _harmoniesSeen.add(pairKey);
      const key = `${pair[0]}-${pair[1]}`;
      _sixHarmonies[key] = {
        branches: pair,
        element: harmonyElement,
        scoring: _SIX_HARMONIES_SCORING,
      };
    }
  }
}
export const SIX_HARMONIES: Readonly<Record<string, BranchCombination>> = _sixHarmonies;

// ---------------------------------------------------------------------------
// ARCHED COMBINATIONS (拱合) - Any 2 of 3 branches from THREE_COMBINATIONS
// ---------------------------------------------------------------------------

const _ARCHED_COMBINATIONS_SCORING = {
  detected: {
    "1": BASE_SCORES.ARCHED_COMBINATIONS.combined,
    "2": Math.round(BASE_SCORES.ARCHED_COMBINATIONS.combined * DISTANCE_MULTIPLIERS.two_branch["2"]),
    "3": Math.round(BASE_SCORES.ARCHED_COMBINATIONS.combined * DISTANCE_MULTIPLIERS.two_branch["3"]),
    "4": Math.round(BASE_SCORES.ARCHED_COMBINATIONS.combined * DISTANCE_MULTIPLIERS.two_branch["4"]),
  },
};

const _archedCombinations: Record<string, ArchedCombinationEntry> = {};
for (const comboKey of Object.keys(_threeCombinations)) {
  const combo = _threeCombinations[comboKey];
  const branches = combo.branches;
  const element = combo.element;
  const [first, middle, third] = [branches[0], branches[1], branches[2]];
  // Generate all 3 possible pairs (any 2 of 3 branches)
  const pairs: [string[], string][] = [
    [[first, middle], third],   // first + middle, missing third
    [[middle, third], first],   // middle + third, missing first
    [[first, third], middle],   // first + third, missing middle
  ];
  for (const [pairBranches, missing] of pairs) {
    const archKey = `${pairBranches[0]}-${pairBranches[1]}`;
    if (!(archKey in _archedCombinations)) {
      _archedCombinations[archKey] = {
        branches: pairBranches,
        element,
        missing,
        scoring: _ARCHED_COMBINATIONS_SCORING,
      };
    }
  }
}
export const ARCHED_COMBINATIONS: Readonly<Record<string, ArchedCombinationEntry>> = _archedCombinations;

// ---------------------------------------------------------------------------
// STEM COMBINATIONS (天干五合)
// ---------------------------------------------------------------------------

const _STEM_COMBINATIONS_SCORING = generateScoring(
  BASE_SCORES.STEM_COMBINATIONS.combined,
  BASE_SCORES.STEM_COMBINATIONS.transformed,
  "two_branch",
);

const _stemCombosSeen = new Set<string>();
const _stemCombinations: Record<string, StemCombinationEntry> = {};
for (const stemId of Object.keys(STEMS) as StemName[]) {
  const stem = STEMS[stemId];
  const partner = stem.combines_with;
  const comboElement = stem.combination_element;
  if (partner && comboElement) {
    const pair = [stemId, partner].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_stemCombosSeen.has(pairKey)) {
      _stemCombosSeen.add(pairKey);
      const key = `${pair[0]}-${pair[1]}`;
      const transformTo = ELEMENT_POLARITY_TO_STEM[`${comboElement}|Yang`];
      _stemCombinations[key] = {
        interaction_type: "HS_COMBINATIONS",
        transform_to: transformTo,
        transform_element: comboElement,
        transformation_requirement: {
          element: comboElement,
          location: "eb",
        },
        scoring: _STEM_COMBINATIONS_SCORING,
        meaning: {} as Record<string, never>,
      };
    }
  }
}
export const STEM_COMBINATIONS: Readonly<Record<string, StemCombinationEntry>> = _stemCombinations;

// ---------------------------------------------------------------------------
// TRANSFORMATION STRENGTH TIERS
// ---------------------------------------------------------------------------

export const TRANSFORMATION_STRENGTH: Readonly<Record<string, string>> = {
  THREE_MEETINGS: "strong",
  THREE_COMBINATIONS: "normal",
  ARCHED_COMBINATIONS: "normal",
  SIX_HARMONIES: "weak",
};

export const STRENGTH_ORDER: Readonly<Record<string, number>> = {
  ultra_strong: 0,
  strong: 1,
  normal: 2,
  weak: 3,
};
