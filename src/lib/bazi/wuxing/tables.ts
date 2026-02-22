// =============================================================================
// WU XING CALCULATOR - STATIC LOOKUP TABLES
// =============================================================================
// Pure data, no side effects. All tables used by the point-based Wu Xing
// (Five Element) calculator. Do NOT add 'server-only' here.
// =============================================================================

import type { Element, StemName, BranchName } from '../core';

// ---------------------------------------------------------------------------
// 1. HS_POINTS - Heavenly Stem point table
// ---------------------------------------------------------------------------
// Each of the 10 stems contributes exactly 10 points.

export const HS_POINTS: Record<StemName, { points: number; element: Element; polarity: 'Yang' | 'Yin' }> = {
  Jia:  { points: 10, element: 'Wood',  polarity: 'Yang' },
  Yi:   { points: 10, element: 'Wood',  polarity: 'Yin'  },
  Bing: { points: 10, element: 'Fire',  polarity: 'Yang' },
  Ding: { points: 10, element: 'Fire',  polarity: 'Yin'  },
  Wu:   { points: 10, element: 'Earth', polarity: 'Yang' },
  Ji:   { points: 10, element: 'Earth', polarity: 'Yin'  },
  Geng: { points: 10, element: 'Metal', polarity: 'Yang' },
  Xin:  { points: 10, element: 'Metal', polarity: 'Yin'  },
  Ren:  { points: 10, element: 'Water', polarity: 'Yang' },
  Gui:  { points: 10, element: 'Water', polarity: 'Yin'  },
};

// ---------------------------------------------------------------------------
// 2. EB_HIDDEN_STEMS - Earthly Branch hidden stem point distribution
// ---------------------------------------------------------------------------
// Point values per the skill spec (NOT core.ts qi percentages):
//   Pure qi (1 hidden stem):  10 pts
//   2 hidden stems:           8 + 3 = 11 pts
//   3 hidden stems:           8 + 3 + 1 = 12 pts

export const EB_HIDDEN_STEMS: Record<BranchName, Array<{ stem: StemName; element: Element; points: number }>> = {
  Zi:   [{ stem: 'Gui',  element: 'Water', points: 10 }],
  Chou: [{ stem: 'Ji',   element: 'Earth', points: 8 }, { stem: 'Gui',  element: 'Water', points: 3 }, { stem: 'Xin',  element: 'Metal', points: 1 }],
  Yin:  [{ stem: 'Jia',  element: 'Wood',  points: 8 }, { stem: 'Bing', element: 'Fire',  points: 3 }, { stem: 'Wu',   element: 'Earth', points: 1 }],
  Mao:  [{ stem: 'Yi',   element: 'Wood',  points: 10 }],
  Chen: [{ stem: 'Wu',   element: 'Earth', points: 8 }, { stem: 'Yi',   element: 'Wood',  points: 3 }, { stem: 'Gui',  element: 'Water', points: 1 }],
  Si:   [{ stem: 'Bing', element: 'Fire',  points: 8 }, { stem: 'Wu',   element: 'Earth', points: 3 }, { stem: 'Geng', element: 'Metal', points: 1 }],
  Wu:   [{ stem: 'Ding', element: 'Fire',  points: 8 }, { stem: 'Ji',   element: 'Earth', points: 3 }],
  Wei:  [{ stem: 'Ji',   element: 'Earth', points: 8 }, { stem: 'Ding', element: 'Fire',  points: 3 }, { stem: 'Yi',   element: 'Wood',  points: 1 }],
  Shen: [{ stem: 'Geng', element: 'Metal', points: 8 }, { stem: 'Ren',  element: 'Water', points: 3 }, { stem: 'Wu',   element: 'Earth', points: 1 }],
  You:  [{ stem: 'Xin',  element: 'Metal', points: 10 }],
  Xu:   [{ stem: 'Wu',   element: 'Earth', points: 8 }, { stem: 'Xin',  element: 'Metal', points: 3 }, { stem: 'Ding', element: 'Fire',  points: 1 }],
  Hai:  [{ stem: 'Ren',  element: 'Water', points: 8 }, { stem: 'Jia',  element: 'Wood',  points: 3 }],
};

// ---------------------------------------------------------------------------
// 3. EB_POLARITY - Branch polarity lookup
// ---------------------------------------------------------------------------

export const EB_POLARITY: Record<BranchName, 'Yang' | 'Yin'> = {
  Zi:   'Yang',
  Chou: 'Yin',
  Yin:  'Yang',
  Mao:  'Yin',
  Chen: 'Yang',
  Si:   'Yin',
  Wu:   'Yang',
  Wei:  'Yin',
  Shen: 'Yang',
  You:  'Yin',
  Xu:   'Yang',
  Hai:  'Yin',
};

// ---------------------------------------------------------------------------
// 4. PILLAR_GAP - Gap matrix + multiplier helper
// ---------------------------------------------------------------------------
// Pillar positions: YP (Year), MP (Month), DP (Day), HP (Hour)
// Adjacent pillars have gap 0; each step apart adds 1.

export type PillarPosition = 'YP' | 'MP' | 'DP' | 'HP';

export const PILLAR_GAP: Record<PillarPosition, Record<PillarPosition, number>> = {
  YP: { YP: 0, MP: 0, DP: 1, HP: 2 },
  MP: { YP: 0, MP: 0, DP: 0, HP: 1 },
  DP: { YP: 1, MP: 0, DP: 0, HP: 0 },
  HP: { YP: 2, MP: 1, DP: 0, HP: 0 },
};

/**
 * Convert a pillar gap distance to its score multiplier.
 * 0 -> 1.0, 1 -> 0.75, 2 -> 0.5, 3+ -> 0.25
 */
export function gapMultiplier(gap: number): number {
  if (gap <= 0) return 1.0;
  if (gap === 1) return 0.75;
  if (gap === 2) return 0.5;
  return 0.25;
}

// ---------------------------------------------------------------------------
// 5. COMBO_RATES - Rate per combination type
// ---------------------------------------------------------------------------

export const COMBO_RATES = {
  THREE_MEETINGS: 0.30,
  THREE_COMBOS:   0.25,
  SIX_HARMONIES:  0.20,
  HALF_MEETINGS:  0.20,
  ARCHED_COMBOS:  0.15,
  STEM_COMBOS:    0.30,
} as const;

// ---------------------------------------------------------------------------
// 6. TRANSFORMATION_MULTIPLIER
// ---------------------------------------------------------------------------

export const TRANSFORMATION_MULTIPLIER = 2.5;

// ---------------------------------------------------------------------------
// 7. ATTENTION_WEIGHTS - Per interaction type
// ---------------------------------------------------------------------------

export const ATTENTION_WEIGHTS = {
  THREE_MEETINGS:  63,
  THREE_COMBOS:    42,
  SIX_CLASH:       42,
  PUNISHMENT_FULL: 42,
  SIX_HARMONIES:   28,
  DESTRUCTION:     28,
  SIX_HARM:        28,
  HALF_MEETINGS:   12,
  ARCHED_COMBO:     7,
} as const;

// ---------------------------------------------------------------------------
// 8. SEASONAL_MULTIPLIERS - Five states (旺相休囚死)
// ---------------------------------------------------------------------------

export type SeasonalState = 'Prosperous' | 'Prime' | 'Rest' | 'Imprisoned' | 'Dead';

export const SEASONAL_MULTIPLIERS: Record<SeasonalState, number> = {
  Prosperous: 1.25,  // 旺 - same as seasonal element
  Prime:      1.15,  // 相 - produced by seasonal element
  Rest:       1.0,   // 休 - produces the seasonal element
  Imprisoned: 0.85,  // 囚 - controls the seasonal element
  Dead:       0.75,  // 死 - controlled by seasonal element
};

// ---------------------------------------------------------------------------
// 9. SEASONAL_MATRIX - Season element -> target element -> state
// ---------------------------------------------------------------------------
// Production cycle: Wood->Fire->Earth->Metal->Water->Wood
// Control cycle:    Wood->Earth->Water->Fire->Metal->Wood

export const SEASONAL_MATRIX: Record<Element, Record<Element, SeasonalState>> = {
  Wood: {
    Wood:  'Prosperous',  // 旺 same
    Fire:  'Prime',       // 相 Wood produces Fire
    Water: 'Rest',        // 休 Water produces Wood
    Metal: 'Imprisoned',  // 囚 Metal controls Wood
    Earth: 'Dead',        // 死 Wood controls Earth
  },
  Fire: {
    Fire:  'Prosperous',
    Earth: 'Prime',       // Fire produces Earth
    Wood:  'Rest',        // Wood produces Fire
    Water: 'Imprisoned',  // Water controls Fire
    Metal: 'Dead',        // Fire controls Metal
  },
  Earth: {
    Earth: 'Prosperous',
    Metal: 'Prime',       // Earth produces Metal
    Fire:  'Rest',        // Fire produces Earth
    Wood:  'Imprisoned',  // Wood controls Earth
    Water: 'Dead',        // Earth controls Water
  },
  Metal: {
    Metal: 'Prosperous',
    Water: 'Prime',       // Metal produces Water
    Earth: 'Rest',        // Earth produces Metal
    Fire:  'Imprisoned',  // Fire controls Metal
    Wood:  'Dead',        // Metal controls Wood
  },
  Water: {
    Water: 'Prosperous',
    Wood:  'Prime',       // Water produces Wood
    Metal: 'Rest',        // Metal produces Water
    Earth: 'Imprisoned',  // Earth controls Water
    Fire:  'Dead',        // Water controls Fire
  },
};

// ---------------------------------------------------------------------------
// 10. MONTH_BRANCH_SEASON - Month branch -> seasonal element
// ---------------------------------------------------------------------------

export const MONTH_BRANCH_SEASON: Record<BranchName, Element> = {
  Yin:  'Wood',   // Spring
  Mao:  'Wood',   // Spring
  Chen: 'Earth',  // transition
  Si:   'Fire',   // Summer
  Wu:   'Fire',   // Summer
  Wei:  'Earth',  // transition
  Shen: 'Metal',  // Autumn
  You:  'Metal',  // Autumn
  Xu:   'Earth',  // transition
  Hai:  'Water',  // Winter
  Zi:   'Water',  // Winter
  Chou: 'Earth',  // transition
};

// ---------------------------------------------------------------------------
// 11. CONTROL_LOOKUP - HS element x EB element -> relationship
// ---------------------------------------------------------------------------

export type ControlRelation = 'SAME' | 'HS_PRODUCES_EB' | 'EB_PRODUCES_HS' | 'HS_CONTROLS_EB' | 'EB_CONTROLS_HS';

export const CONTROL_LOOKUP: Record<Element, Record<Element, ControlRelation>> = {
  Wood: {
    Wood:  'SAME',
    Fire:  'HS_PRODUCES_EB',
    Earth: 'HS_CONTROLS_EB',
    Metal: 'EB_CONTROLS_HS',
    Water: 'EB_PRODUCES_HS',
  },
  Fire: {
    Wood:  'EB_PRODUCES_HS',
    Fire:  'SAME',
    Earth: 'HS_PRODUCES_EB',
    Metal: 'HS_CONTROLS_EB',
    Water: 'EB_CONTROLS_HS',
  },
  Earth: {
    Wood:  'EB_CONTROLS_HS',
    Fire:  'EB_PRODUCES_HS',
    Earth: 'SAME',
    Metal: 'HS_PRODUCES_EB',
    Water: 'HS_CONTROLS_EB',
  },
  Metal: {
    Wood:  'HS_CONTROLS_EB',
    Fire:  'EB_CONTROLS_HS',
    Earth: 'EB_PRODUCES_HS',
    Metal: 'SAME',
    Water: 'HS_PRODUCES_EB',
  },
  Water: {
    Wood:  'HS_PRODUCES_EB',
    Fire:  'HS_CONTROLS_EB',
    Earth: 'EB_CONTROLS_HS',
    Metal: 'EB_PRODUCES_HS',
    Water: 'SAME',
  },
};

// ---------------------------------------------------------------------------
// 12. Combo tables (positive interactions)
// ---------------------------------------------------------------------------

// THREE_MEETINGS_TABLE - 三会 (seasonal directional combos)
export const THREE_MEETINGS_TABLE: Record<string, { element: Element }> = {
  'Yin-Mao-Chen':  { element: 'Wood'  },
  'Si-Wu-Wei':     { element: 'Fire'  },
  'Shen-You-Xu':   { element: 'Metal' },
  'Hai-Zi-Chou':   { element: 'Water' },
};

// THREE_COMBOS_TABLE - 三合 (triangular harmony combos)
export const THREE_COMBOS_TABLE: Record<string, { element: Element }> = {
  'Hai-Mao-Wei':   { element: 'Wood'  },
  'Yin-Wu-Xu':     { element: 'Fire'  },
  'Si-You-Chou':   { element: 'Metal' },
  'Shen-Zi-Chen':  { element: 'Water' },
};

// SIX_HARMONIES_TABLE - 六合 (branch pair harmonies)
// Keys: alphabetically sorted branch names joined with '-'
export const SIX_HARMONIES_TABLE: Record<string, { element: Element }> = {
  'Chou-Zi':   { element: 'Earth' },
  'Hai-Yin':   { element: 'Wood'  },
  'Mao-Xu':    { element: 'Fire'  },
  'Chen-You':  { element: 'Metal' },
  'Shen-Si':   { element: 'Water' },
  'Wei-Wu':    { element: 'Fire'  },
};

// HALF_MEETINGS_TABLE - pairs from each seasonal group
// Keys: alphabetically sorted branch names joined with '-'
export const HALF_MEETINGS_TABLE: Record<string, { element: Element; season: Element }> = {
  // Wood (Yin-Mao-Chen)
  'Mao-Yin':   { element: 'Wood',  season: 'Wood'  },
  'Chen-Mao':  { element: 'Wood',  season: 'Wood'  },
  'Chen-Yin':  { element: 'Wood',  season: 'Wood'  },
  // Fire (Si-Wu-Wei)
  'Si-Wu':     { element: 'Fire',  season: 'Fire'  },
  'Wei-Wu':    { element: 'Fire',  season: 'Fire'  },
  'Si-Wei':    { element: 'Fire',  season: 'Fire'  },
  // Metal (Shen-You-Xu)
  'Shen-You':  { element: 'Metal', season: 'Metal' },
  'Xu-You':    { element: 'Metal', season: 'Metal' },
  'Shen-Xu':   { element: 'Metal', season: 'Metal' },
  // Water (Hai-Zi-Chou)
  'Hai-Zi':    { element: 'Water', season: 'Water' },
  'Chou-Zi':   { element: 'Water', season: 'Water' },
  'Chou-Hai':  { element: 'Water', season: 'Water' },
};

// ARCHED_COMBOS_TABLE - 拱合 (Growth + Tomb, Peak missing)
// Keys: alphabetically sorted branch names joined with '-'
export const ARCHED_COMBOS_TABLE: Record<string, { element: Element; missing: BranchName }> = {
  'Hai-Wei':    { element: 'Wood',  missing: 'Mao' },
  'Yin-Xu':     { element: 'Fire',  missing: 'Wu'  },
  'Chou-Si':    { element: 'Metal', missing: 'You' },
  'Chen-Shen':  { element: 'Water', missing: 'Zi'  },
};

// STEM_COMBOS_TABLE - 天干合 (Heavenly Stem combinations)
// Keys: alphabetically sorted stem names joined with '-'
export const STEM_COMBOS_TABLE: Record<string, { element: Element }> = {
  'Jia-Ji':    { element: 'Earth' },
  'Geng-Yi':   { element: 'Metal' },
  'Bing-Xin':  { element: 'Water' },
  'Ding-Ren':  { element: 'Wood'  },
  'Gui-Wu':    { element: 'Fire'  },
};

// ---------------------------------------------------------------------------
// 13. Negative interaction tables
// ---------------------------------------------------------------------------

// SIX_CLASHES_TABLE - 六冲
// Keys: alphabetically sorted branch names joined with '-'
export const SIX_CLASHES_TABLE: Record<string, { type: 'control' | 'same'; attacker?: BranchName; victim?: BranchName }> = {
  'Wu-Zi':     { type: 'control', attacker: 'Zi',   victim: 'Wu'  },   // Water controls Fire
  'Shen-Yin':  { type: 'control', attacker: 'Shen', victim: 'Yin' },   // Metal controls Wood
  'Mao-You':   { type: 'control', attacker: 'You',  victim: 'Mao' },   // Metal controls Wood
  'Hai-Si':    { type: 'control', attacker: 'Hai',  victim: 'Si'  },   // Water controls Fire
  'Chou-Wei':  { type: 'same' },                                        // Earth <-> Earth
  'Chen-Xu':   { type: 'same' },                                        // Earth <-> Earth
};

// PUNISHMENTS_TABLE - 刑
export const PUNISHMENTS_TABLE: Record<string, {
  type: 'shi' | 'wu_li' | 'en' | 'self';
  branches?: BranchName[];
  requiresAll?: boolean;
  logOnly?: boolean;
  pairs?: Array<{ pair: [BranchName, BranchName]; attacker: BranchName; victim: BranchName }>;
  attacker?: BranchName;
  victim?: BranchName;
}> = {
  // Bullying 恃势 (3-way, different elements)
  'Shen-Si-Yin': {
    type: 'shi',
    branches: ['Yin', 'Si', 'Shen'],
    requiresAll: false,
    pairs: [
      { pair: ['Yin', 'Si'],   attacker: 'Si',   victim: 'Yin'  },  // Fire drains Wood
      { pair: ['Si', 'Shen'],  attacker: 'Si',   victim: 'Shen' },  // Fire controls Metal
      { pair: ['Shen', 'Yin'], attacker: 'Shen', victim: 'Yin'  },  // Metal controls Wood
    ],
  },
  // Ungrateful 无恩 (3-way, all Earth -> log only)
  'Chou-Wei-Xu': {
    type: 'wu_li',
    branches: ['Chou', 'Wei', 'Xu'],
    requiresAll: true,
    logOnly: true,
  },
  // Rude 无礼 (pair)
  'Mao-Zi': {
    type: 'en',
    attacker: 'Mao',
    victim: 'Zi',   // Wood drains Water
  },
  // Self-punishments (log only)
  'Chen-Chen': { type: 'self', logOnly: true },
  'Wu-Wu':     { type: 'self', logOnly: true },
  'You-You':   { type: 'self', logOnly: true },
  'Hai-Hai':   { type: 'self', logOnly: true },
};

// SIX_HARMS_TABLE - 六害
// Keys: alphabetically sorted branch names joined with '-'
export const SIX_HARMS_TABLE: Record<string, { attacker: BranchName; victim: BranchName }> = {
  'Wei-Zi':    { attacker: 'Wei',  victim: 'Zi'   },  // Earth controls Water
  'Chou-Wu':   { attacker: 'Chou', victim: 'Wu'   },  // Fire->Earth drain
  'Si-Yin':    { attacker: 'Si',   victim: 'Yin'  },  // Wood->Fire drain
  'Chen-Mao':  { attacker: 'Mao',  victim: 'Chen' },  // Wood controls Earth
  'Hai-Shen':  { attacker: 'Hai',  victim: 'Shen' },  // Metal->Water drain
  'Xu-You':    { attacker: 'You',  victim: 'Xu'   },  // Earth->Metal drain
};

// DESTRUCTIONS_TABLE - 破
// Keys: alphabetically sorted branch names joined with '-'
export const DESTRUCTIONS_TABLE: Record<string, { type: 'control' | 'same'; attacker?: BranchName; victim?: BranchName }> = {
  'You-Zi':    { type: 'control', attacker: 'Zi',  victim: 'You'  },  // Metal->Water drain
  'Hai-Yin':   { type: 'control', attacker: 'Yin', victim: 'Hai'  },  // Water->Wood drain
  'Mao-Wu':    { type: 'control', attacker: 'Wu',  victim: 'Mao'  },  // Wood->Fire drain
  'Shen-Si':   { type: 'control', attacker: 'Si',  victim: 'Shen' },  // Fire controls Metal
  'Chen-Chou': { type: 'same' },                                       // Earth <-> Earth
  'Wei-Xu':    { type: 'same' },                                       // Earth <-> Earth
};

// STEM_CLASHES_TABLE - 天干冲 (Heavenly Stem clashes)
// Keys: alphabetically sorted stem names joined with '-'
export const STEM_CLASHES_TABLE: Record<string, { controller: StemName; controlled: StemName }> = {
  'Geng-Jia':  { controller: 'Geng', controlled: 'Jia'  },  // Metal controls Wood, Yang
  'Xin-Yi':    { controller: 'Xin',  controlled: 'Yi'   },  // Metal controls Wood, Yin
  'Bing-Ren':  { controller: 'Ren',  controlled: 'Bing' },  // Water controls Fire, Yang
  'Ding-Gui':  { controller: 'Gui',  controlled: 'Ding' },  // Water controls Fire, Yin
};

// ---------------------------------------------------------------------------
// 14. NEGATIVE_RATES - Damage rates for negative interactions
// ---------------------------------------------------------------------------

export const NEGATIVE_RATES = {
  SIX_CLASH:   { attackerLoss: 0.25, victimLoss: 0.50 },
  PUNISHMENT:  { attackerLoss: 0.20, victimLoss: 0.40 },
  SIX_HARM:    { attackerLoss: 0.20, victimLoss: 0.40 },
  DESTRUCTION: { attackerLoss: 0.20, victimLoss: 0.40 },
  STEM_CLASH:  { attackerLoss: 0.25, victimLoss: 0.50 },
} as const;

// ---------------------------------------------------------------------------
// 15. Step 7 cross-pillar grid gaps (Manhattan distance - 1)
// ---------------------------------------------------------------------------
// Grid layout:
//   YP.HS -- MP.HS -- DP.HS -- HP.HS   (row 0)
//     |        |        |        |
//   YP.EB -- MP.EB -- DP.EB -- HP.EB   (row 1)
//
// Manhattan distance = |col_a - col_b| + |row_a - row_b|
// Gap = Manhattan distance - 1

type NodeId = `${'YP' | 'MP' | 'DP' | 'HP'}.${'HS' | 'EB'}`;

const NODE_COORDS: Record<NodeId, [col: number, row: number]> = {
  'YP.HS': [0, 0], 'MP.HS': [1, 0], 'DP.HS': [2, 0], 'HP.HS': [3, 0],
  'YP.EB': [0, 1], 'MP.EB': [1, 1], 'DP.EB': [2, 1], 'HP.EB': [3, 1],
};

/**
 * Returns the gap (Manhattan distance - 1) between two nodes on the
 * 4x2 cross-pillar grid. Nodes are identified as 'YP.HS', 'MP.EB', etc.
 */
export function getStep7Gap(nodeA: string, nodeB: string): number {
  const a = NODE_COORDS[nodeA as NodeId];
  const b = NODE_COORDS[nodeB as NodeId];
  if (!a || !b) throw new Error(`Unknown node: ${!a ? nodeA : nodeB}`);
  const manhattan = Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]);
  return Math.max(0, manhattan - 1);
}
