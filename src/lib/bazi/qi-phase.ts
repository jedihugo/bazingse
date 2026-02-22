import 'server-only';

// =============================================================================
// QI PHASE (十二長生 / Twelve Life Stages)
// =============================================================================
// Classical BaZi concept describing the life cycle of each element
// through 12 phases as it moves through the Earthly Branches.
//
// Principle: 陽順陰逆 (Yang Forward, Yin Reverse)
// - Yang stems progress forward through branches from their birth point
// - Yin stems progress backward through branches from their birth point

import type { StemName, BranchName } from './core';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type QiPhaseStrength =
  | "strong"
  | "weak"
  | "growing"
  | "peak"
  | "declining"
  | "dead"
  | "stored"
  | "nascent";

export interface QiPhase {
  readonly id: string;
  readonly chinese: string;
  readonly english: string;
  readonly description: string;
  readonly strength: QiPhaseStrength;
  readonly order: number;
}

export interface QiPhaseForPillar extends QiPhase {
  stem: StemName;
  branch: BranchName;
}

// ---------------------------------------------------------------------------
// The 12 Qi Phases in lifecycle order
// ---------------------------------------------------------------------------

export const QI_PHASES: readonly QiPhase[] = [
  {
    id: "changsheng",
    chinese: "長生",
    english: "Birth",
    description: "Element is born, full of potential",
    strength: "strong",
    order: 0,
  },
  {
    id: "muyu",
    chinese: "沐浴",
    english: "Bathing",
    description: "Vulnerable stage, like bathing a newborn",
    strength: "weak",
    order: 1,
  },
  {
    id: "guandai",
    chinese: "冠帶",
    english: "Capping",
    description: "Coming of age, putting on the cap",
    strength: "growing",
    order: 2,
  },
  {
    id: "linguan",
    chinese: "臨官",
    english: "Official",
    description: "Taking office, career begins",
    strength: "strong",
    order: 3,
  },
  {
    id: "diwang",
    chinese: "帝旺",
    english: "Peak",
    description: "Emperor stage, maximum power",
    strength: "peak",
    order: 4,
  },
  {
    id: "shuai",
    chinese: "衰",
    english: "Decline",
    description: "Beginning to weaken",
    strength: "declining",
    order: 5,
  },
  {
    id: "bing",
    chinese: "病",
    english: "Sickness",
    description: "Getting ill, energy depleted",
    strength: "weak",
    order: 6,
  },
  {
    id: "si",
    chinese: "死",
    english: "Death",
    description: "Dying, end of active cycle",
    strength: "dead",
    order: 7,
  },
  {
    id: "mu",
    chinese: "墓",
    english: "Tomb",
    description: "Buried, stored away (also: Storage/庫)",
    strength: "stored",
    order: 8,
  },
  {
    id: "jue",
    chinese: "絕",
    english: "Extinction",
    description: "Complete ending, void",
    strength: "dead",
    order: 9,
  },
  {
    id: "tai",
    chinese: "胎",
    english: "Embryo",
    description: "New conception begins",
    strength: "nascent",
    order: 10,
  },
  {
    id: "yang",
    chinese: "養",
    english: "Nurturing",
    description: "Being nurtured in womb",
    strength: "nascent",
    order: 11,
  },
];

// Create lookup by id
export const QI_PHASE_BY_ID: Readonly<Record<string, QiPhase>> = Object.fromEntries(
  QI_PHASES.map((phase) => [phase.id, phase])
);

// Branch order for index calculations
const BRANCH_ORDER: readonly BranchName[] = [
  "Zi", "Chou", "Yin", "Mao", "Chen", "Si",
  "Wu", "Wei", "Shen", "You", "Xu", "Hai",
];
const BRANCH_INDEX: Record<string, number> = Object.fromEntries(
  BRANCH_ORDER.map((branch, i) => [branch, i])
);

// Birth points (長生 location) for each Heavenly Stem
// Yang stems: forward progression | Yin stems: reverse progression
const STEM_BIRTH_POINTS: Readonly<Record<string, { birth_branch: BranchName; direction: "forward" | "reverse" }>> = {
  // Yang stems (forward from birth point)
  Jia:  { birth_branch: "Hai",  direction: "forward" },  // Yang Wood born at Hai (Water produces Wood)
  Bing: { birth_branch: "Yin",  direction: "forward" },  // Yang Fire born at Yin (Wood produces Fire)
  Wu:   { birth_branch: "Yin",  direction: "forward" },  // Yang Earth born at Yin (same as Fire)
  Geng: { birth_branch: "Si",   direction: "forward" },  // Yang Metal born at Si
  Ren:  { birth_branch: "Shen", direction: "forward" },  // Yang Water born at Shen (Metal produces Water)

  // Yin stems (reverse from birth point) - 陽順陰逆
  Yi:   { birth_branch: "Wu",   direction: "reverse" },  // Yin Wood born at Wu
  Ding: { birth_branch: "You",  direction: "reverse" },  // Yin Fire born at You
  Ji:   { birth_branch: "You",  direction: "reverse" },  // Yin Earth born at You (same as Ding)
  Xin:  { birth_branch: "Zi",   direction: "reverse" },  // Yin Metal born at Zi
  Gui:  { birth_branch: "Mao",  direction: "reverse" },  // Yin Water born at Mao
};

/**
 * Get the Qi Phase for a Heavenly Stem in a given Earthly Branch.
 */
export function getQiPhase(stemId: string, branchId: string): QiPhase | null {
  if (!(stemId in STEM_BIRTH_POINTS)) return null;
  if (!(branchId in BRANCH_INDEX)) return null;

  const birthInfo = STEM_BIRTH_POINTS[stemId];
  const birthIdx = BRANCH_INDEX[birthInfo.birth_branch];
  const currentIdx = BRANCH_INDEX[branchId];

  let phaseIdx: number;
  if (birthInfo.direction === "forward") {
    // Yang stems: count forward from birth point
    phaseIdx = ((currentIdx - birthIdx) % 12 + 12) % 12;
  } else {
    // Yin stems: count backward from birth point
    phaseIdx = ((birthIdx - currentIdx) % 12 + 12) % 12;
  }

  return { ...QI_PHASES[phaseIdx] };
}

/**
 * Get Qi Phase for a pillar (HS in context of its EB).
 * Returns the phase of the Heavenly Stem relative to the Earthly Branch.
 */
export function getQiPhaseForPillar(
  hsId: StemName,
  ebId: BranchName,
): QiPhaseForPillar | null {
  const phase = getQiPhase(hsId, ebId);
  if (phase) {
    return { ...phase, stem: hsId, branch: ebId };
  }
  return null;
}

// Pre-computed full lookup table for performance
// Format: QI_PHASE_TABLE[stem_id][branch_id] = phase_id
const _qiPhaseTable: Record<string, Record<string, string | null>> = {};
for (const stemId of Object.keys(STEM_BIRTH_POINTS)) {
  _qiPhaseTable[stemId] = {};
  for (const branchId of BRANCH_ORDER) {
    const phase = getQiPhase(stemId, branchId);
    _qiPhaseTable[stemId][branchId] = phase ? phase.id : null;
  }
}

export const QI_PHASE_TABLE: Readonly<Record<string, Readonly<Record<string, string | null>>>> = _qiPhaseTable;

/**
 * Fast lookup returning just the phase ID.
 */
export function getQiPhaseId(stemId: string, branchId: string): string | null {
  return QI_PHASE_TABLE[stemId]?.[branchId] ?? null;
}

// Strength categories for UI styling
export const QI_PHASE_STRENGTH_COLORS: Readonly<Record<QiPhaseStrength, string>> = {
  peak: "#22c55e",      // Green - maximum power
  strong: "#84cc16",    // Lime - strong
  growing: "#a3e635",   // Light lime - developing
  declining: "#fbbf24", // Amber - weakening
  weak: "#f97316",      // Orange - weak
  dead: "#ef4444",      // Red - no power
  stored: "#8b5cf6",    // Purple - stored/hidden
  nascent: "#06b6d4",   // Cyan - potential/forming
};
