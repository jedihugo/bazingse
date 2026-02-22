import 'server-only';

// =============================================================================
// NEGATIVE CONFLICT PATTERNS (DERIVED FROM CORE)
// =============================================================================
// All negative/destructive branch and stem interactions
// Patterns are DERIVED from core.ts STEMS and BRANCHES.

import { STEMS, BRANCHES, type StemName, type BranchName, type BranchData, type Element } from './core';
import { ELEMENT_CYCLES } from './derived';
import {
  BASE_SCORES,
  generateSingleScoring,
  generateAsymmetricScoring,
} from './scoring';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface PunishmentEntry {
  readonly branches: readonly string[];
  readonly type: "3-node" | "2-node" | "self";
  readonly category: string;
  readonly chinese_name: string;
  readonly english_name: string;
  readonly severity: "severe" | "moderate" | "light" | "self";
  readonly element_conflict?: boolean;
  readonly controller?: string;
  readonly controlled?: string;
  readonly element_relationship?: string;
  readonly element?: Element;
  readonly nature?: string;
  readonly scoring: Record<string, number> | { victim: Record<string, number>; controller: Record<string, number> };
  readonly description: string;
}

export interface HarmEntry {
  readonly branches: readonly string[];
  readonly controller: string;
  readonly controlled: string;
  readonly scoring: { victim: Record<string, number>; controller: Record<string, number> };
}

export interface ClashEntry {
  readonly branches: readonly string[];
  readonly type: "same" | "opposite";
  readonly controller?: string;
  readonly controlled?: string;
  readonly scoring: Record<string, number> | { victim: Record<string, number>; controller: Record<string, number> };
}

export interface DestructionEntry {
  readonly branches: readonly string[];
  readonly type: "same" | "opposite";
  readonly controller?: string;
  readonly controlled?: string;
  readonly scoring: Record<string, number> | { victim: Record<string, number>; controller: Record<string, number> };
}

export interface StemConflictEntry {
  readonly controller: string;
  readonly controlled: string;
  readonly scoring: { victim: Record<string, number>; controller: Record<string, number> };
}

// ---------------------------------------------------------------------------
// SCORING CONFIGURATIONS
// ---------------------------------------------------------------------------

const _CLASHES_OPPOSITE_SCORING = generateAsymmetricScoring(
  BASE_SCORES.CLASHES_OPPOSITE.damage, "two_branch", 0.618,
);
const _CLASHES_SAME_SCORING = generateSingleScoring(
  BASE_SCORES.CLASHES_SAME.damage, "two_branch",
);
const _STEM_CONFLICTS_SCORING = generateAsymmetricScoring(
  BASE_SCORES.STEM_CONFLICTS.damage, "two_branch", 0.618,
);
const _PUNISHMENTS_3NODE_SCORING = generateSingleScoring(
  BASE_SCORES.PUNISHMENTS_3NODE.damage, "two_branch",
);
const _PUNISHMENTS_2NODE_SCORING = generateAsymmetricScoring(
  BASE_SCORES.PUNISHMENTS_2NODE.damage, "two_branch", 0.618,
);
const _PUNISHMENTS_SELF_SCORING = generateSingleScoring(
  BASE_SCORES.PUNISHMENTS_2NODE.damage, "two_branch",
);
const _HARMS_SCORING = generateAsymmetricScoring(
  BASE_SCORES.HARMS.damage, "two_branch", 0.618,
);
const _DESTRUCTION_OPPOSITE_SCORING = generateAsymmetricScoring(
  BASE_SCORES.DESTRUCTION_OPPOSITE.damage, "two_branch", 0.618,
);
const _DESTRUCTION_SAME_SCORING = generateSingleScoring(
  BASE_SCORES.DESTRUCTION_SAME.damage, "two_branch",
);

// ---------------------------------------------------------------------------
// PUNISHMENTS (刑)
// ---------------------------------------------------------------------------

interface PunishmentGroupRaw {
  branches: string[];
  type: string;
  controller?: string;
  controlled?: string;
}

const _punishmentGroups: Record<string, PunishmentGroupRaw> = {};
const _selfPunishments: BranchName[] = [];

for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId] as BranchData;

  const punishmentGroup = branch.punishment_group;
  if (punishmentGroup) {
    const groupKey = `${punishmentGroup[0]}-${punishmentGroup[1]}-${punishmentGroup[2]}`;
    if (!(groupKey in _punishmentGroups)) {
      _punishmentGroups[groupKey] = {
        branches: [punishmentGroup[0], punishmentGroup[1], punishmentGroup[2]],
        type: punishmentGroup[3],
      };
    }
  }

  const punishmentPair = branch.punishment_pair;
  if (punishmentPair) {
    const [partner, punType, role] = punishmentPair;
    const pairKey = role === "controller"
      ? `${branchId}-${partner}`
      : `${partner}-${branchId}`;
    if (!(pairKey in _punishmentGroups)) {
      _punishmentGroups[pairKey] = {
        branches: role === "controller"
          ? [branchId, partner]
          : [partner, branchId],
        type: punType,
        controller: role === "controller" ? branchId : partner,
        controlled: role === "controller" ? partner : branchId,
      };
    }
  }

  if (branch.self_punishment) {
    _selfPunishments.push(branchId);
  }
}

const _punishments: Record<string, PunishmentEntry> = {};

for (const [groupKey, group] of Object.entries(_punishmentGroups)) {
  const branches = group.branches;
  const punType = group.type;

  if (branches.length === 3) {
    if (punType === "shi") {
      _punishments[groupKey] = {
        branches,
        type: "3-node",
        category: "shi_xing",
        chinese_name: "勢刑",
        english_name: "Bullying Punishment",
        severity: "severe",
        element_conflict: true,
        scoring: _PUNISHMENTS_3NODE_SCORING,
        description: "Three powerful branches in mutual conflict (恃勢之刑)",
      };
    } else if (punType === "wu_li") {
      _punishments[groupKey] = {
        branches,
        type: "3-node",
        category: "wu_li_xing",
        chinese_name: "無禮刑",
        english_name: "Rudeness Punishment",
        severity: "moderate",
        element_conflict: false,
        scoring: _PUNISHMENTS_3NODE_SCORING,
        description: "Earth branches showing disrespect to each other (無禮之刑)",
      };
    }
  } else if (branches.length === 2 && punType === "en") {
    const controller = group.controller!;
    const controlled = group.controlled!;
    _punishments[groupKey] = {
      branches,
      type: "2-node",
      category: "en_xing",
      chinese_name: "恩刑",
      english_name: "Ungrateful Punishment",
      severity: "light",
      controller,
      controlled,
      element_relationship: "productive",
      scoring: _PUNISHMENTS_2NODE_SCORING,
      description: "Beneficiary punishes benefactor - betrayal (持恩之刑)",
    };
  }
}

// Self-punishment data now embedded in BRANCHES as self_punishment_nature
for (const branchId of _selfPunishments) {
  const branch = BRANCHES[branchId] as BranchData;
  const nature = branch.self_punishment_nature ?? "Self-conflict";
  const key = `${branchId}-${branchId}`;
  _punishments[key] = {
    branches: [branchId, branchId],
    type: "self",
    category: "zi_xing",
    chinese_name: "自刑",
    english_name: `Self-Punishment (${branch.animal})`,
    severity: "self",
    element: branch.element,
    nature,
    scoring: _PUNISHMENTS_SELF_SCORING,
    description: `${branch.animal}'s nature punishes itself (${branchId}自刑)`,
  };
}

export const PUNISHMENTS: Readonly<Record<string, PunishmentEntry>> = _punishments;

export const PUNISHMENT_SEVERITY: Readonly<Record<string, number>> = {
  severe: 1.0,
  moderate: 0.85,
  light: 0.70,
  self: 0.60,
};

// ---------------------------------------------------------------------------
// HARMS (害)
// ---------------------------------------------------------------------------

const _harmsSeen = new Set<string>();
const _harms: Record<string, HarmEntry> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const partner = branch.harms;
  const role = branch.harm_role;
  if (partner && role) {
    const pair = [branchId, partner].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_harmsSeen.has(pairKey)) {
      _harmsSeen.add(pairKey);
      let controller: string;
      let controlled: string;
      if (role === "controller") {
        controller = branchId;
        controlled = partner;
      } else {
        controller = partner;
        controlled = branchId;
      }
      const key = `${pair[0]}-${pair[1]}`;
      _harms[key] = {
        branches: pair,
        controller,
        controlled,
        scoring: _HARMS_SCORING,
      };
    }
  }
}
export const HARMS: Readonly<Record<string, HarmEntry>> = _harms;

// ---------------------------------------------------------------------------
// CLASHES (沖)
// ---------------------------------------------------------------------------

const _clashesSeen = new Set<string>();
const _clashes: Record<string, ClashEntry> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const partner = branch.clashes;
  if (partner) {
    const pair = [branchId, partner].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_clashesSeen.has(pairKey)) {
      _clashesSeen.add(pairKey);
      const b1Elem = branch.element;
      const b2Elem = BRANCHES[partner].element;
      const key = `${pair[0]}-${pair[1]}`;

      if (b1Elem === b2Elem) {
        _clashes[key] = {
          branches: pair,
          type: "same",
          scoring: _CLASHES_SAME_SCORING,
        };
      } else {
        let controller: string;
        let controlled: string;
        if (ELEMENT_CYCLES.controlling[b1Elem] === b2Elem) {
          controller = branchId;
          controlled = partner;
        } else {
          controller = partner;
          controlled = branchId;
        }
        _clashes[key] = {
          branches: pair,
          type: "opposite",
          controller,
          controlled,
          scoring: _CLASHES_OPPOSITE_SCORING,
        };
      }
    }
  }
}
export const CLASHES: Readonly<Record<string, ClashEntry>> = _clashes;

// ---------------------------------------------------------------------------
// DESTRUCTION (破)
// ---------------------------------------------------------------------------

const _destructionSeen = new Set<string>();
const _destruction: Record<string, DestructionEntry> = {};
for (const branchId of Object.keys(BRANCHES) as BranchName[]) {
  const branch = BRANCHES[branchId];
  const partner = branch.destroys;
  if (partner) {
    const pair = [branchId, partner].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_destructionSeen.has(pairKey)) {
      _destructionSeen.add(pairKey);
      const b1Elem = branch.element;
      const b2Elem = BRANCHES[partner].element;
      const key = `${pair[0]}-${pair[1]}`;

      if (b1Elem === b2Elem) {
        _destruction[key] = {
          branches: pair,
          type: "same",
          scoring: _DESTRUCTION_SAME_SCORING,
        };
      } else {
        let controller: string;
        let controlled: string;
        if (ELEMENT_CYCLES.generating[b1Elem] === b2Elem) {
          controller = branchId;
          controlled = partner;
        } else {
          controller = partner;
          controlled = branchId;
        }
        _destruction[key] = {
          branches: pair,
          type: "opposite",
          controller,
          controlled,
          scoring: _DESTRUCTION_OPPOSITE_SCORING,
        };
      }
    }
  }
}
export const DESTRUCTION: Readonly<Record<string, DestructionEntry>> = _destruction;

// ---------------------------------------------------------------------------
// STEM CONFLICTS (天干相剋)
// ---------------------------------------------------------------------------

const _stemConflictsSeen = new Set<string>();
const _stemConflicts: Record<string, StemConflictEntry> = {};
for (const stemId of Object.keys(STEMS) as StemName[]) {
  const stem = STEMS[stemId];
  const controlled = stem.controls;
  if (controlled) {
    const pair = [stemId, controlled].sort() as [string, string];
    const pairKey = pair.join(",");
    if (!_stemConflictsSeen.has(pairKey)) {
      _stemConflictsSeen.add(pairKey);
      const key = `${pair[0]}-${pair[1]}`;
      _stemConflicts[key] = {
        controller: stemId,
        controlled,
        scoring: _STEM_CONFLICTS_SCORING,
      };
    }
  }
}
export const STEM_CONFLICTS: Readonly<Record<string, StemConflictEntry>> = _stemConflicts;

// ---------------------------------------------------------------------------
// WUXING ENERGY FLOW (五行流動)
// ---------------------------------------------------------------------------

export const WUXING_ENERGY_FLOW = {
  generation: ELEMENT_CYCLES.generating,
  control: ELEMENT_CYCLES.controlling,
  scoring: {
    generating: {
      generator_loss: 7,
      receiver_gain: 10,
      count_increment: 0.25,
    },
    controlling: {
      controller_loss: 5,
      controlled_loss: 10,
      count_decrement: 0.25,
    },
  },
} as const;
