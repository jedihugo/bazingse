import 'server-only';

// =============================================================================
// WEALTH STORAGE (財庫) SYSTEM
// =============================================================================
//
// Based on the Twelve Growth Stages (十二长生) cycle:
// Each element has a tomb/storage (墓/库) at a specific Earthly Branch.

import { STEMS, type Element, type StemName, type BranchName } from './core';
import { WUXING } from './derived';

// =============================================================================
// ELEMENT TO STORAGE BRANCH (十二长生 墓/库)
// =============================================================================

export const ELEMENT_STORAGE: Readonly<Record<Element, BranchName>> = {
  Wood:  "Wei",   // 木墓于未
  Fire:  "Xu",    // 火墓于戌
  Earth: "Xu",    // 土墓于戌 (Earth follows Fire's growth cycle)
  Metal: "Chou",  // 金墓于丑
  Water: "Chen",  // 水墓于辰
};

// =============================================================================
// DM TO WEALTH STORAGE BRANCH (財庫)
// =============================================================================
// DM controls wealth element -> wealth element's tomb branch

export const DM_WEALTH_STORAGE: Readonly<Record<Element, BranchName>> = {
  Wood:  "Xu",    // Wood -> controls Earth (wealth) -> Earth tomb at 戌
  Fire:  "Chou",  // Fire -> controls Metal (wealth) -> Metal tomb at 丑
  Earth: "Chen",  // Earth -> controls Water (wealth) -> Water tomb at 辰
  Metal: "Wei",   // Metal -> controls Wood (wealth) -> Wood tomb at 未
  Water: "Xu",    // Water -> controls Fire (wealth) -> Fire tomb at 戌
};

// =============================================================================
// STORAGE BRANCH OPENERS (冲開)
// =============================================================================
// The four 库 branches open through their clash (冲) partner.

export const STORAGE_OPENER: Readonly<Record<string, BranchName>> = {
  Chou: "Wei",   // 丑未冲
  Wei:  "Chou",  // 未丑冲
  Chen: "Xu",    // 辰戌冲
  Xu:   "Chen",  // 戌辰冲
};

// =============================================================================
// LARGE WEALTH STORAGE PILLARS (大財庫)
// =============================================================================
// When DM stem sits DIRECTLY on its own wealth storage branch
// in the same pillar. Most powerful wealth storage configuration.

export interface LargeWealthStorageEntry {
  readonly chinese: string;
  readonly dm_element: Element;
  readonly wealth_element: Element;
  readonly storage_branch: BranchName;
  readonly opener: BranchName;
}

export const LARGE_WEALTH_STORAGE: Readonly<Record<string, LargeWealthStorageEntry>> = {
  "Jia-Xu": {
    chinese: "甲戌",
    dm_element: "Wood",
    wealth_element: "Earth",
    storage_branch: "Xu",
    opener: "Chen",
  },
  "Ding-Chou": {
    chinese: "丁丑",
    dm_element: "Fire",
    wealth_element: "Metal",
    storage_branch: "Chou",
    opener: "Wei",
  },
  "Wu-Chen": {
    chinese: "戊辰",
    dm_element: "Earth",
    wealth_element: "Water",
    storage_branch: "Chen",
    opener: "Xu",
  },
  "Xin-Wei": {
    chinese: "辛未",
    dm_element: "Metal",
    wealth_element: "Wood",
    storage_branch: "Wei",
    opener: "Chou",
  },
  "Ren-Xu": {
    chinese: "壬戌",
    dm_element: "Water",
    wealth_element: "Fire",
    storage_branch: "Xu",
    opener: "Chen",
  },
};

// =============================================================================
// WEALTH ELEMENT BY DM (controlling cycle)
// =============================================================================

export const DM_WEALTH_ELEMENT: Readonly<Record<Element, Element>> =
  WUXING.controlling as Record<Element, Element>;

// =============================================================================
// WEALTH ELEMENT STEMS (for filler detection)
// =============================================================================
// Map element -> list of Heavenly Stems of that element

const _wealthElementStems: Record<string, StemName[]> = {};
for (const stemId of Object.keys(STEMS) as StemName[]) {
  const elem = STEMS[stemId].element;
  if (!_wealthElementStems[elem]) {
    _wealthElementStems[elem] = [];
  }
  _wealthElementStems[elem].push(stemId);
}

export const WEALTH_ELEMENT_STEMS: Readonly<Record<Element, readonly StemName[]>> =
  _wealthElementStems as Record<Element, StemName[]>;
