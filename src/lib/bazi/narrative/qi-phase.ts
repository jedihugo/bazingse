import 'server-only';

// =============================================================================
// QI PHASE (十二长生)
// =============================================================================
// Twelve Life Stages for stem-branch relationships.
// Ported from api/library/narrative/qi_phase.py
// =============================================================================

import type { Element, StemName, BranchName } from '../core';
import { STEMS } from '../core';

// ---------------------------------------------------------------------------
// Qi Phase Order (12 life stages)
// ---------------------------------------------------------------------------

export const QI_PHASE_ORDER = [
  "長生", // Birth / Growing
  "沐浴", // Bathing
  "冠帶", // Capping
  "臨官", // Arriving at Office
  "帝旺", // Emperor's Peak
  "衰",   // Declining
  "病",   // Sickness
  "死",   // Death
  "墓",   // Tomb / Storage
  "絕",   // Extinction
  "胎",   // Embryo
  "養",   // Nurturing
] as const;

export type QiPhaseName = typeof QI_PHASE_ORDER[number];

// ---------------------------------------------------------------------------
// Branch Order for computation
// ---------------------------------------------------------------------------

const BRANCH_ORDER: BranchName[] = [
  "Zi", "Chou", "Yin", "Mao", "Chen", "Si",
  "Wu", "Wei", "Shen", "You", "Xu", "Hai",
];

// ---------------------------------------------------------------------------
// Element Birth Branch (长生 starting point)
// ---------------------------------------------------------------------------

const ELEMENT_BIRTH_BRANCH: Record<string, BranchName> = {
  "Wood|Yang": "Hai",    // Jia: 甲長生在亥
  "Wood|Yin": "Wu",      // Yi: 乙長生在午
  "Fire|Yang": "Yin",    // Bing: 丙長生在寅
  "Fire|Yin": "You",     // Ding: 丁長生在酉
  "Earth|Yang": "Yin",   // Wu: 戊長生在寅 (same as Bing)
  "Earth|Yin": "You",    // Ji: 己長生在酉 (same as Ding)
  "Metal|Yang": "Si",    // Geng: 庚長生在巳
  "Metal|Yin": "Zi",     // Xin: 辛長生在子
  "Water|Yang": "Shen",  // Ren: 壬長生在申
  "Water|Yin": "Mao",    // Gui: 癸長生在卯
};

// ---------------------------------------------------------------------------
// QI PHASE INFO
// ---------------------------------------------------------------------------

export interface QiPhaseInfo {
  chinese: string;
  english: string;
  pinyin: string;
  description_en: string;
  description_zh: string;
  strength: number; // 0-10 scale
  is_storage: boolean;
}

export const QI_PHASE_INFO: Record<string, QiPhaseInfo> = {
  "長生": {
    chinese: "長生",
    english: "Birth",
    pinyin: "Cháng Shēng",
    description_en: "Beginning of life energy. Fresh start, new potential emerging.",
    description_zh: "生命能量的開始。新的開始，新的潛力正在顯現。",
    strength: 7,
    is_storage: false,
  },
  "沐浴": {
    chinese: "沐浴",
    english: "Bathing",
    pinyin: "Mù Yù",
    description_en: "Cleansing phase. Vulnerability, exposure, romantic energy.",
    description_zh: "沐浴階段。脆弱、暴露、浪漫能量。",
    strength: 5,
    is_storage: false,
  },
  "冠帶": {
    chinese: "冠帶",
    english: "Capping",
    pinyin: "Guàn Dài",
    description_en: "Coming of age. Gaining recognition, building identity.",
    description_zh: "成年階段。獲得認可，建立身份。",
    strength: 6,
    is_storage: false,
  },
  "臨官": {
    chinese: "臨官",
    english: "Arriving at Office",
    pinyin: "Lín Guān",
    description_en: "Taking position. Authority, responsibility, career advancement.",
    description_zh: "就任階段。權威、責任、事業提升。",
    strength: 8,
    is_storage: false,
  },
  "帝旺": {
    chinese: "帝旺",
    english: "Emperor's Peak",
    pinyin: "Dì Wàng",
    description_en: "Peak of power. Maximum strength, but watch for overextension.",
    description_zh: "權力巔峰。最大力量，但要注意過度擴張。",
    strength: 10,
    is_storage: false,
  },
  "衰": {
    chinese: "衰",
    english: "Declining",
    pinyin: "Shuāi",
    description_en: "Beginning of decline. Energy waning, time to consolidate.",
    description_zh: "開始衰退。能量減弱，是鞏固的時候。",
    strength: 4,
    is_storage: false,
  },
  "病": {
    chinese: "病",
    english: "Sickness",
    pinyin: "Bìng",
    description_en: "Weakness phase. Vulnerability to illness, need for rest.",
    description_zh: "虛弱階段。容易生病，需要休息。",
    strength: 3,
    is_storage: false,
  },
  "死": {
    chinese: "死",
    english: "Death",
    pinyin: "Sǐ",
    description_en: "Cessation of active energy. Rest, withdrawal, reflection.",
    description_zh: "活力停止。休息、退隱、反思。",
    strength: 1,
    is_storage: false,
  },
  "墓": {
    chinese: "墓",
    english: "Tomb/Storage",
    pinyin: "Mù",
    description_en: "Storage phase. Energy preserved, hidden resources, wealth storage.",
    description_zh: "庫存階段。能量保存，隱藏資源，財庫。",
    strength: 2,
    is_storage: true,
  },
  "絕": {
    chinese: "絕",
    english: "Extinction",
    pinyin: "Jué",
    description_en: "Complete cessation. Letting go, emptiness before rebirth.",
    description_zh: "完全停止。放下，重生前的空虛。",
    strength: 0,
    is_storage: false,
  },
  "胎": {
    chinese: "胎",
    english: "Embryo",
    pinyin: "Tāi",
    description_en: "Conception phase. Seeds of new life, hidden potential.",
    description_zh: "受孕階段。新生命的種子，隱藏的潛力。",
    strength: 3,
    is_storage: false,
  },
  "養": {
    chinese: "養",
    english: "Nurturing",
    pinyin: "Yǎng",
    description_en: "Nurturing phase. Protected growth, gathering strength.",
    description_zh: "養育階段。受保護的成長，聚集力量。",
    strength: 5,
    is_storage: false,
  },
};

// ---------------------------------------------------------------------------
// Core Functions
// ---------------------------------------------------------------------------

export function getQiPhase(element: Element, polarity: string, branch: BranchName): string | null {
  const key = `${element}|${polarity}`;
  const birthBranch = ELEMENT_BIRTH_BRANCH[key];
  if (!birthBranch) return null;

  const birthIndex = BRANCH_ORDER.indexOf(birthBranch);
  const branchIndex = BRANCH_ORDER.indexOf(branch);
  if (birthIndex === -1 || branchIndex === -1) return null;

  // Yang goes forward, Yin goes backward
  let offset: number;
  if (polarity === "Yang") {
    offset = (branchIndex - birthIndex + 12) % 12;
  } else {
    offset = (birthIndex - branchIndex + 12) % 12;
  }

  return QI_PHASE_ORDER[offset];
}

export function getQiPhaseForStem(stem: StemName, branch: BranchName): string | null {
  const stemData = STEMS[stem];
  if (!stemData) return null;

  return getQiPhase(
    stemData.element as Element,
    stemData.polarity,
    branch
  );
}

export function getStorageInfo(branch: BranchName): {
  element: Element;
  phase: string;
} | null {
  // Check which elements have their 墓 (tomb/storage) at this branch
  const elements: Array<{ element: Element; polarity: string }> = [
    { element: "Wood", polarity: "Yang" },
    { element: "Fire", polarity: "Yang" },
    { element: "Earth", polarity: "Yang" },
    { element: "Metal", polarity: "Yang" },
    { element: "Water", polarity: "Yang" },
  ];

  for (const { element, polarity } of elements) {
    const phase = getQiPhase(element, polarity, branch);
    if (phase === "墓") {
      return { element, phase };
    }
  }

  return null;
}

export function getAllPhasesForBranch(branch: BranchName): Array<{
  element: Element;
  polarity: string;
  phase: string;
}> {
  const results: Array<{ element: Element; polarity: string; phase: string }> = [];

  const combos: Array<{ element: Element; polarity: string }> = [
    { element: "Wood", polarity: "Yang" },
    { element: "Wood", polarity: "Yin" },
    { element: "Fire", polarity: "Yang" },
    { element: "Fire", polarity: "Yin" },
    { element: "Earth", polarity: "Yang" },
    { element: "Earth", polarity: "Yin" },
    { element: "Metal", polarity: "Yang" },
    { element: "Metal", polarity: "Yin" },
    { element: "Water", polarity: "Yang" },
    { element: "Water", polarity: "Yin" },
  ];

  for (const { element, polarity } of combos) {
    const phase = getQiPhase(element, polarity, branch);
    if (phase) {
      results.push({ element, polarity, phase });
    }
  }

  return results;
}

export function findPhasesInBranch(
  branch: BranchName,
  targetPhase: string
): Array<{ element: Element; polarity: string }> {
  return getAllPhasesForBranch(branch)
    .filter((r) => r.phase === targetPhase)
    .map(({ element, polarity }) => ({ element, polarity }));
}

export function getQiPhaseNarrativeContext(
  stem: StemName,
  branch: BranchName
): { phase: string; info: QiPhaseInfo; text_en: string; text_zh: string } | null {
  const phase = getQiPhaseForStem(stem, branch);
  if (!phase) return null;

  const info = QI_PHASE_INFO[phase];
  if (!info) return null;

  const stemData = STEMS[stem];
  const element = stemData?.element ?? stem;

  return {
    phase,
    info,
    text_en: `${stem} (${element}) is in ${info.english} (${info.chinese}) phase at ${branch}: ${info.description_en}`,
    text_zh: `${stem}（${element}）在${branch}處於${info.chinese}階段：${info.description_zh}`,
  };
}
