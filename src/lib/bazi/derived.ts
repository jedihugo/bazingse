
// =============================================================================
// BAZI DERIVED - All data derived from STEMS and BRANCHES
// =============================================================================
// This file contains ALL derived data, lookups, and utility functions.
// Everything here is computed from the core.ts STEMS and BRANCHES.
// =============================================================================

import {
  STEMS,
  BRANCHES,
  type Element,
  type Polarity,
  type StemName,
  type BranchName,
  type StemData,
  type BranchData,
  type TenGodCode,
  type QiEntry,
  type HarmRole,
  type ElementState,
} from './core';

// =============================================================================
// DERIVED: Element Cycles (computed from STEMS)
// =============================================================================
// Build the generating and controlling cycles from stem element relationships

// Get unique elements from stems (preserving insertion order)
const _seenElements = new Set<Element>();
for (const s of Object.keys(STEMS) as StemName[]) {
  _seenElements.add(STEMS[s].element);
}
export const ELEMENTS: readonly Element[] = Array.from(_seenElements);

// Build from the known Wu Xing sequence
const _wuxing_order: readonly Element[] = ["Wood", "Fire", "Earth", "Metal", "Water"];

type ElementCycleMap = Record<Element, Element>;

const _generating: Record<string, Element> = {};
const _controlling: Record<string, Element> = {};

for (let i = 0; i < _wuxing_order.length; i++) {
  const elem = _wuxing_order[i];
  const nextElem = _wuxing_order[(i + 1) % 5];
  _generating[elem] = nextElem;
}

for (let i = 0; i < _wuxing_order.length; i++) {
  const elem = _wuxing_order[i];
  const controlled = _wuxing_order[(i + 2) % 5];
  _controlling[elem] = controlled;
}

// Reverse lookups
const _generated_by: Record<string, Element> = {};
const _controlled_by: Record<string, Element> = {};
for (const [k, v] of Object.entries(_generating)) {
  _generated_by[v] = k as Element;
}
for (const [k, v] of Object.entries(_controlling)) {
  _controlled_by[v] = k as Element;
}

export const ELEMENT_CYCLES = {
  generating: _generating as ElementCycleMap,
  controlling: _controlling as ElementCycleMap,
  generated_by: _generated_by as ElementCycleMap,
  controlled_by: _controlled_by as ElementCycleMap,
} as const;

// Element Chinese characters
export const ELEMENT_CHINESE: Readonly<Record<Element, string>> = {
  Wood: "木",
  Fire: "火",
  Earth: "土",
  Metal: "金",
  Water: "水",
};

// =============================================================================
// DERIVED: Day Officers (computed for Dong Gong)
// =============================================================================

export interface DayOfficer {
  readonly id: string;
  readonly chinese: string;
  readonly english: string;
}

export const DAY_OFFICERS: Readonly<Record<number, DayOfficer>> = {
  0: { id: "Jian", chinese: "建", english: "Establish" },
  1: { id: "Chu", chinese: "除", english: "Remove" },
  2: { id: "Man", chinese: "滿", english: "Full" },
  3: { id: "Ping", chinese: "平", english: "Balance" },
  4: { id: "Ding", chinese: "定", english: "Stable" },
  5: { id: "Zhi", chinese: "執", english: "Initiate" },
  6: { id: "Po", chinese: "破", english: "Destruction" },
  7: { id: "Wei", chinese: "危", english: "Danger" },
  8: { id: "Cheng", chinese: "成", english: "Success" },
  9: { id: "Shou", chinese: "收", english: "Receive" },
  10: { id: "Kai", chinese: "開", english: "Open" },
  11: { id: "Bi", chinese: "閉", english: "Close" },
};

export const DAY_OFFICER_ORDER: readonly string[] = Array.from(
  { length: 12 },
  (_, i) => DAY_OFFICERS[i].id
);

// =============================================================================
// DERIVED: Ordered Lists (for index lookups)
// =============================================================================

export const STEM_ORDER: readonly StemName[] = (
  Object.keys(STEMS) as StemName[]
).slice().sort((a, b) => STEMS[a].index - STEMS[b].index);

export const STEM_CHINESE: readonly string[] = STEM_ORDER.map(
  (s) => STEMS[s].chinese
);

export const BRANCH_ORDER: readonly BranchName[] = (
  Object.keys(BRANCHES) as BranchName[]
).slice().sort((a, b) => BRANCHES[a].index - BRANCHES[b].index);

export const BRANCH_CHINESE: readonly string[] = BRANCH_ORDER.map(
  (b) => BRANCHES[b].chinese
);

// =============================================================================
// DERIVED: Lookup Tables
// =============================================================================

// Chinese -> Pinyin mappings
export const STEM_CHINESE_TO_PINYIN: Readonly<Record<string, StemName>> =
  Object.fromEntries(
    (Object.keys(STEMS) as StemName[]).map((s) => [STEMS[s].chinese, s])
  ) as Record<string, StemName>;

export const BRANCH_CHINESE_TO_PINYIN: Readonly<Record<string, BranchName>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((b) => [BRANCHES[b].chinese, b])
  ) as Record<string, BranchName>;

// Element + Polarity -> Stem
export const ELEMENT_POLARITY_TO_STEM: Readonly<Record<string, StemName>> =
  Object.fromEntries(
    (Object.keys(STEMS) as StemName[]).map((s) => [
      `${STEMS[s].element}|${STEMS[s].polarity}`,
      s,
    ])
  ) as Record<string, StemName>;

// Storage branches
export interface StorageBranchData {
  readonly stored_element: Element;
  readonly stored_stem: StemName;
  readonly opener: BranchName;
}

export const STORAGE_BRANCHES: Readonly<Record<string, StorageBranchData>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[])
      .filter((b) => (BRANCHES[b] as BranchData).is_storage)
      .map((b) => {
        const br = BRANCHES[b] as BranchData;
        return [
          b,
          {
            stored_element: br.stored_element!,
            stored_stem: br.stored_stem!,
            opener: br.opener!,
          },
        ];
      })
  ) as Record<string, StorageBranchData>;

// Branch -> Month and reverse
export const BRANCH_TO_MONTH: Readonly<Record<BranchName, number>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((b) => [b, BRANCHES[b].month])
  ) as Record<BranchName, number>;

export const MONTH_TO_BRANCH: Readonly<Record<number, BranchName>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((b) => [BRANCHES[b].month, b])
  ) as Record<number, BranchName>;

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Get stem by pinyin, chinese, or index.
 */
export function getStem(identifier: string | number): StemData | null {
  if (typeof identifier === "number" && identifier >= 0 && identifier < 10) {
    return STEMS[STEM_ORDER[identifier]];
  }
  if (typeof identifier === "string") {
    if (identifier in STEMS) {
      return STEMS[identifier as StemName];
    }
    if (identifier in STEM_CHINESE_TO_PINYIN) {
      return STEMS[STEM_CHINESE_TO_PINYIN[identifier]];
    }
  }
  return null;
}

/**
 * Get branch by pinyin, chinese, or index.
 */
export function getBranch(identifier: string | number): BranchData | null {
  if (typeof identifier === "number" && identifier >= 0 && identifier < 12) {
    return BRANCHES[BRANCH_ORDER[identifier]];
  }
  if (typeof identifier === "string") {
    if (identifier in BRANCHES) {
      return BRANCHES[identifier as BranchName];
    }
    if (identifier in BRANCH_CHINESE_TO_PINYIN) {
      return BRANCHES[BRANCH_CHINESE_TO_PINYIN[identifier]];
    }
  }
  return null;
}

/**
 * Get Primary Qi (本氣) for a branch - the main energy at index 0.
 *
 * PRIMARY QI is the dominant energy of the Earthly Branch.
 * This is NOT a hidden stem - it's the visible, main energy.
 *
 * @param branchId - Branch ID like "Yin", "Si", etc.
 * @returns [stemName, score] or [null, 0] if branch not found
 */
export function getPrimaryQi(
  branchId: string
): readonly [StemName, number] | readonly [null, 0] {
  if (branchId in BRANCHES) {
    const branch = BRANCHES[branchId as BranchName];
    if (branch.qi && branch.qi.length > 0) {
      return branch.qi[0];
    }
  }
  return [null, 0] as const;
}

/**
 * Get Hidden Stems (藏干) for a branch - secondary/tertiary energies at index 1+.
 *
 * IMPORTANT: The PRIMARY QI at index 0 is NOT a hidden stem.
 * Only index 1+ are actual hidden stems (藏干).
 *
 * @param branchId - Branch ID like "Yin", "Si", etc.
 * @returns List of [stemName, score] tuples for hidden stems only.
 *          Empty array if branch has only Primary Qi (e.g., Zi, Mao, You).
 */
export function getHiddenStems(branchId: string): readonly QiEntry[] {
  if (branchId in BRANCHES) {
    const branch = BRANCHES[branchId as BranchName];
    if (branch.qi && branch.qi.length > 1) {
      return branch.qi.slice(1);
    }
  }
  return [];
}

/**
 * Get all qi values for a branch (Primary Qi + Hidden Stems combined).
 *
 * This returns the complete qi list. Use getPrimaryQi() for just the
 * main energy, or getHiddenStems() for just the secondary/tertiary energies.
 *
 * @param branchId - Branch ID like "Yin", "Si", etc.
 * @returns List of [stemName, score] tuples for all qi values
 */
export function getAllBranchQi(branchId: string): readonly QiEntry[] {
  if (branchId in BRANCHES) {
    return BRANCHES[branchId as BranchName].qi;
  }
  return [];
}

/**
 * Get stem ID for element + polarity combination.
 */
export function getStemByElementPolarity(
  element: Element,
  polarity: Polarity
): StemName | undefined {
  return ELEMENT_POLARITY_TO_STEM[`${element}|${polarity}`];
}

/**
 * Calculate the Day Officer (十二建除) for a given month and day branch.
 * Formula: officer_index = (day_dong_gong_index - month_dong_gong_index + 12) % 12
 */
export function getDayOfficer(
  monthBranch: string,
  dayBranch: string
): DayOfficer | null {
  if (!(monthBranch in BRANCHES) || !(dayBranch in BRANCHES)) {
    return null;
  }
  const monthIdx = BRANCHES[monthBranch as BranchName].dong_gong_index;
  const dayIdx = BRANCHES[dayBranch as BranchName].dong_gong_index;
  const officerIdx = (dayIdx - monthIdx + 12) % 12;
  return DAY_OFFICERS[officerIdx];
}

/**
 * Compute the Ten God relationship between daymaster and target stem.
 * @returns [id, english, chinese] or null
 */
export function getTenGod(
  daymaster: string,
  targetStem: string
): readonly [TenGodCode, string, string] | null {
  if (!(daymaster in STEMS) || !(targetStem in STEMS)) {
    return null;
  }

  const dm = STEMS[daymaster as StemName];
  const tg = STEMS[targetStem as StemName];
  const dmElem = dm.element;
  const dmPol = dm.polarity;
  const tgElem = tg.element;
  const tgPol = tg.polarity;
  const samePolarity = dmPol === tgPol;

  // Same element
  if (dmElem === tgElem) {
    if (samePolarity) return ["F", "Friend", "比肩"] as const;
    return ["RW", "Rob Wealth", "劫財"] as const;
  }

  // I generate (output)
  if (ELEMENT_CYCLES.generating[dmElem] === tgElem) {
    if (samePolarity) return ["EG", "Eating God", "食神"] as const;
    return ["HO", "Hurting Officer", "傷官"] as const;
  }

  // I control (wealth)
  if (ELEMENT_CYCLES.controlling[dmElem] === tgElem) {
    if (samePolarity) return ["IW", "Indirect Wealth", "偏財"] as const;
    return ["DW", "Direct Wealth", "正財"] as const;
  }

  // Controls me (influence/officer)
  if (ELEMENT_CYCLES.controlled_by[dmElem] === tgElem) {
    if (samePolarity) return ["7K", "Seven Killings", "七殺"] as const;
    return ["DO", "Direct Officer", "正官"] as const;
  }

  // Generates me (resource)
  if (ELEMENT_CYCLES.generated_by[dmElem] === tgElem) {
    if (samePolarity) return ["IR", "Indirect Resource", "偏印"] as const;
    return ["DR", "Direct Resource", "正印"] as const;
  }

  return null;
}

/**
 * Get the branch for a Chinese calendar month (1-12).
 */
export function getBranchByMonth(month: number): BranchName | undefined {
  return MONTH_TO_BRANCH[month];
}

// =============================================================================
// BACKWARD COMPATIBILITY ALIASES
// =============================================================================
export const HEAVENLY_STEMS = STEMS;
export const EARTHLY_BRANCHES = BRANCHES;
export const WUXING = ELEMENT_CYCLES;

// For sxtwl compatibility
export const Gan = STEM_CHINESE;
export const Zhi = BRANCH_CHINESE;
export const GAN_MAP = STEM_CHINESE_TO_PINYIN;
export const ZHI_MAP = BRANCH_CHINESE_TO_PINYIN;

// =============================================================================
// DERIVED: Stem Lookup Maps (from stems)
// =============================================================================

export interface StemCombinationInfo {
  readonly partner: StemName;
  readonly element: Element;
}

export const STEM_COMBINATIONS_MAP: Readonly<Record<StemName, StemCombinationInfo>> =
  Object.fromEntries(
    (Object.keys(STEMS) as StemName[]).map((stemId) => [
      stemId,
      {
        partner: STEMS[stemId].combines_with,
        element: STEMS[stemId].combination_element,
      },
    ])
  ) as Record<StemName, StemCombinationInfo>;

export interface StemConflictInfo {
  readonly controls: StemName;
  readonly controlled_by: StemName;
}

export const STEM_CONFLICTS_MAP: Readonly<Record<StemName, StemConflictInfo>> =
  Object.fromEntries(
    (Object.keys(STEMS) as StemName[]).map((stemId) => [
      stemId,
      {
        controls: STEMS[stemId].controls,
        controlled_by: STEMS[stemId].controlled_by,
      },
    ])
  ) as Record<StemName, StemConflictInfo>;

// =============================================================================
// DERIVED: Branch Lookup Maps (from branches)
// =============================================================================

export const BRANCH_TO_SEASON: Readonly<Record<BranchName, string>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((branchId) => [
      branchId,
      BRANCHES[branchId].season,
    ])
  ) as Record<BranchName, string>;

export interface SixHarmonyInfo {
  readonly partner: BranchName;
  readonly element: Element;
}

export const SIX_HARMONIES_MAP: Readonly<Record<BranchName, SixHarmonyInfo>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((branchId) => [
      branchId,
      {
        partner: BRANCHES[branchId].harmonizes,
        element: BRANCHES[branchId].harmony_element,
      },
    ])
  ) as Record<BranchName, SixHarmonyInfo>;

export interface ClashInfo {
  readonly partner: BranchName;
  readonly type: "opposite" | "same";
}

export const CLASHES_MAP: Readonly<Record<BranchName, ClashInfo>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((branchId) => {
      const branch = BRANCHES[branchId];
      const clashPartner = branch.clashes;
      const clashType =
        BRANCHES[clashPartner].element !== branch.element
          ? "opposite"
          : "same";
      return [branchId, { partner: clashPartner, type: clashType }];
    })
  ) as Record<BranchName, ClashInfo>;

export interface HarmInfo {
  readonly partner: BranchName;
  readonly role: HarmRole;
}

export const HARMS_MAP: Readonly<Record<BranchName, HarmInfo>> =
  Object.fromEntries(
    (Object.keys(BRANCHES) as BranchName[]).map((branchId) => [
      branchId,
      {
        partner: BRANCHES[branchId].harms,
        role: BRANCHES[branchId].harm_role,
      },
    ])
  ) as Record<BranchName, HarmInfo>;

export const SELF_PUNISHMENT_BRANCHES: readonly BranchName[] = (
  Object.keys(BRANCHES) as BranchName[]
).filter((branchId) => BRANCHES[branchId].self_punishment);

// =============================================================================
// DERIVED: Element Display Data (from elements)
// =============================================================================

export const ELEMENT_POLARITY_STEMS = ELEMENT_POLARITY_TO_STEM; // Alias

export interface ElementColorSet {
  readonly text: string;
  readonly bg: string;
  readonly border: string;
}

export const ELEMENT_COLORS: Readonly<
  Record<Element, Readonly<Record<"yang" | "yin", ElementColorSet>>>
> = {
  Wood: {
    yang: { text: "text-green-700", bg: "bg-green-100", border: "border-green-600" },
    yin: { text: "text-green-500", bg: "bg-green-50", border: "border-green-400" },
  },
  Fire: {
    yang: { text: "text-red-600", bg: "bg-red-100", border: "border-red-500" },
    yin: { text: "text-red-400", bg: "bg-red-50", border: "border-red-300" },
  },
  Earth: {
    yang: { text: "text-yellow-700", bg: "bg-yellow-100", border: "border-yellow-600" },
    yin: { text: "text-yellow-500", bg: "bg-yellow-50", border: "border-yellow-400" },
  },
  Metal: {
    yang: { text: "text-gray-600", bg: "bg-gray-100", border: "border-gray-500" },
    yin: { text: "text-gray-400", bg: "bg-gray-50", border: "border-gray-300" },
  },
  Water: {
    yang: { text: "text-blue-700", bg: "bg-blue-100", border: "border-blue-600" },
    yin: { text: "text-blue-500", bg: "bg-blue-50", border: "border-blue-400" },
  },
};

/**
 * Get the Tailwind color classes for an element + polarity.
 */
export function getElementColor(
  element: Element,
  polarity?: Polarity
): ElementColorSet {
  const polarityKey = polarity === "Yang" ? "yang" : "yin";
  return ELEMENT_COLORS[element]?.[polarityKey] ?? ELEMENT_COLORS.Wood.yang;
}

// Element characters including stem characters
export const ELEMENT_CHARACTERS: Readonly<Record<string, string>> = (() => {
  const chars: Record<string, string> = {
    Wood: "木",
    Fire: "火",
    Earth: "土",
    Metal: "金",
    Water: "水",
  };
  for (const stemId of Object.keys(STEMS) as StemName[]) {
    const stem = STEMS[stemId];
    chars[`${stem.polarity} ${stem.element}`] = stem.chinese;
  }
  return chars;
})();

// =============================================================================
// DERIVED: Ten Gods (十神) - built from STEMS.ten_gods static data
// =============================================================================

const _TEN_GOD_PINYIN: Readonly<Record<TenGodCode, string>> = {
  F: "bǐ jiān",
  RW: "jié cái",
  EG: "shí shén",
  HO: "shāng guān",
  IW: "piān cái",
  DW: "zhèng cái",
  "7K": "qī shā",
  DO: "zhèng guān",
  IR: "piān yìn",
  DR: "zhèng yìn",
};

// Ten God Notes - interpretive notes for each ten god
export const TEN_GOD_NOTES: Readonly<
  Record<TenGodCode, Readonly<Record<string, string>>>
> = {
  F: {},
  RW: {},
  EG: {},
  HO: {},
  IW: {},
  DW: {},
  "7K": {},
  DO: {},
  IR: {
    unfavorable: "Can indicate susceptibility to santet/black magic",
  },
  DR: {
    general: "Indicates physical health",
  },
};

export interface TenGodEntry {
  readonly id: TenGodCode;
  readonly abbreviation: TenGodCode;
  readonly english: string;
  readonly chinese: string;
  readonly pinyin: string;
  readonly meaning_male: readonly string[];
  readonly meaning_female: readonly string[];
}

export const TEN_GODS: Readonly<
  Record<StemName, Readonly<Record<StemName, TenGodEntry>>>
> = Object.fromEntries(
  (Object.keys(STEMS) as StemName[]).map((dmId) => {
    const stem = STEMS[dmId];
    const targetEntries = Object.fromEntries(
      (Object.keys(stem.ten_gods) as StemName[]).map((targetId) => {
        const tg = stem.ten_gods[targetId];
        return [
          targetId,
          {
            id: tg[0],
            abbreviation: tg[0],
            english: tg[1],
            chinese: tg[2],
            pinyin: _TEN_GOD_PINYIN[tg[0]] ?? "",
            meaning_male: [] as string[],
            meaning_female: [] as string[],
          },
        ];
      })
    );
    return [dmId, targetEntries];
  })
) as unknown as Record<StemName, Record<StemName, TenGodEntry>>;
