import 'server-only';

// =============================================================================
// CHAIN ENGINE
// =============================================================================
// Contextual chain analysis for BaZi narrative enrichment.
// Provides deep analysis of node interactions with Shen Sha and Qi Phase context.
// Ported from api/library/narrative/chain_engine.py
// =============================================================================

import type { Element, StemName, BranchName } from '../core';
import { STEMS } from '../core';

// ---------------------------------------------------------------------------
// Shen Sha Contextual Meanings
// ---------------------------------------------------------------------------

export interface ShenShaMeaning {
  name_en: string;
  name_zh: string;
  positive: { en: string; zh: string };
  negative: { en: string; zh: string };
  with_clash: { en: string; zh: string };
  with_combination: { en: string; zh: string };
}

export const SHEN_SHA_MEANINGS: Record<string, ShenShaMeaning> = {
  GU_CHEN: {
    name_en: "Lonely Star",
    name_zh: "孤辰",
    positive: {
      en: "Independence and self-reliance, spiritual depth",
      zh: "獨立自主，精神深度",
    },
    negative: {
      en: "Isolation, difficulty in relationships, loneliness",
      zh: "孤立，人際關係困難，孤獨",
    },
    with_clash: {
      en: "Loneliness amplified by clash - forced separation from loved ones",
      zh: "孤獨因沖而加劇 - 被迫與親人分離",
    },
    with_combination: {
      en: "Loneliness tempered by combination - companionship mitigates isolation",
      zh: "孤獨因合而緩和 - 陪伴減輕孤立",
    },
  },
  GUA_SU: {
    name_en: "Widow Star",
    name_zh: "寡宿",
    positive: {
      en: "Self-sufficiency, spiritual practice, contemplative nature",
      zh: "自給自足，修行，沉思的性格",
    },
    negative: {
      en: "Loss of partner, widowhood risk, solitary life",
      zh: "失去伴侶，守寡風險，獨居生活",
    },
    with_clash: {
      en: "Widow star intensified by clash - potential loss in relationships",
      zh: "寡宿因沖而加強 - 感情可能有損失",
    },
    with_combination: {
      en: "Widow star softened by combination - new companionship possible",
      zh: "寡宿因合而減緩 - 可能有新的陪伴",
    },
  },
  HUA_GAI: {
    name_en: "Canopy Star",
    name_zh: "華蓋",
    positive: {
      en: "Artistic talent, spiritual insight, scholarly achievement",
      zh: "藝術才華，靈性洞察，學術成就",
    },
    negative: {
      en: "Social isolation, excessive idealism, difficulty connecting",
      zh: "社交孤立，過度理想主義，難以建立聯繫",
    },
    with_clash: {
      en: "Creative disruption - artistic breakthroughs through crisis",
      zh: "創意中斷 - 通過危機實現藝術突破",
    },
    with_combination: {
      en: "Creative harmony - artistic collaboration and recognition",
      zh: "創意和諧 - 藝術合作和認可",
    },
  },
  TIAN_YI: {
    name_en: "Heavenly Noble",
    name_zh: "天乙",
    positive: {
      en: "Noble help arrives, mentors appear, opportunities emerge",
      zh: "貴人相助，良師出現，機會浮現",
    },
    negative: {
      en: "Over-reliance on others, passive approach to problems",
      zh: "過度依賴他人，被動處理問題",
    },
    with_clash: {
      en: "Noble help during crisis - savior appears in darkest moment",
      zh: "危機中的貴人相助 - 最黑暗時刻出現救星",
    },
    with_combination: {
      en: "Noble synergy - helpful connections multiply benefits",
      zh: "貴人協同 - 有益的人脈倍增利益",
    },
  },
  TAO_HUA: {
    name_en: "Peach Blossom",
    name_zh: "桃花",
    positive: {
      en: "Romantic charm, artistic beauty, social popularity",
      zh: "浪漫魅力，藝術之美，社交人氣",
    },
    negative: {
      en: "Romantic entanglements, scandal risk, superficial attractions",
      zh: "感情糾葛，醜聞風險，膚淺的吸引",
    },
    with_clash: {
      en: "Romantic crisis - affairs exposed, relationship turbulence",
      zh: "感情危機 - 外遇曝光，關係動盪",
    },
    with_combination: {
      en: "Romantic harmony - beautiful partnership, creative collaboration",
      zh: "感情和諧 - 美好的伴侶關係，創意合作",
    },
  },
  YANG_REN: {
    name_en: "Yang Blade",
    name_zh: "羊刃",
    positive: {
      en: "Decisive action, competitive edge, strong willpower",
      zh: "果斷行動，競爭優勢，堅強意志",
    },
    negative: {
      en: "Aggression, injury risk, conflict with authority",
      zh: "攻擊性，受傷風險，與權威衝突",
    },
    with_clash: {
      en: "Blade meets clash - high injury/accident risk, surgical intervention",
      zh: "羊刃遇沖 - 高受傷/事故風險，手術干預",
    },
    with_combination: {
      en: "Blade tempered by combination - controlled power, martial arts skill",
      zh: "羊刃因合而收斂 - 控制力量，武術技能",
    },
  },
};

// ---------------------------------------------------------------------------
// Qi Phase Meanings (for chain context)
// ---------------------------------------------------------------------------

export const QI_PHASE_MEANINGS: Record<string, { en: string; zh: string }> = {
  "長生": { en: "energy is being born - new beginnings", zh: "能量正在誕生 - 新的開始" },
  "沐浴": { en: "energy is vulnerable and exposed", zh: "能量脆弱且暴露" },
  "冠帶": { en: "energy is growing and gaining form", zh: "能量在成長並獲得形態" },
  "臨官": { en: "energy reaches official position", zh: "能量達到官位" },
  "帝旺": { en: "energy is at its peak", zh: "能量達到巔峰" },
  "衰": { en: "energy begins to decline", zh: "能量開始衰退" },
  "病": { en: "energy is weakened and sick", zh: "能量虛弱生病" },
  "死": { en: "energy ceases active expression", zh: "能量停止活躍表達" },
  "墓": { en: "energy is stored/hidden in tomb", zh: "能量存儲/隱藏在墓中" },
  "絕": { en: "energy reaches extinction", zh: "能量達到絕滅" },
  "胎": { en: "new energy conceived", zh: "新能量受孕" },
  "養": { en: "energy is being nurtured", zh: "能量正在被養育" },
};

// ---------------------------------------------------------------------------
// Storage Branches Mapping
// ---------------------------------------------------------------------------

export const STORAGE_BRANCHES: Record<string, Element> = {
  Chen: "Water",
  Xu: "Fire",
  Chou: "Metal",
  Wei: "Wood",
};

// ---------------------------------------------------------------------------
// DM to Wealth Storage mapping
// ---------------------------------------------------------------------------

export const DM_TO_WEALTH_STORAGE: Record<Element, BranchName> = {
  Wood: "Xu",    // Wood controls Earth, Earth storage = Xu (Fire storage, but Earth wealth is Fire墓)
  Fire: "Chou",  // Fire controls Metal, Metal storage = Chou
  Earth: "Chen", // Earth controls Water, Water storage = Chen
  Metal: "Wei",  // Metal controls Wood, Wood storage = Wei
  Water: "Xu",   // Water controls Fire, Fire storage = Xu
};

// ---------------------------------------------------------------------------
// Ten God Names
// ---------------------------------------------------------------------------

export const TEN_GOD_NAMES: Record<string, { en: string; zh: string }> = {
  F: { en: "Friend", zh: "比肩" },
  RW: { en: "Rob Wealth", zh: "劫財" },
  EG: { en: "Eating God", zh: "食神" },
  HO: { en: "Hurting Officer", zh: "傷官" },
  DW: { en: "Direct Wealth", zh: "正財" },
  IW: { en: "Indirect Wealth", zh: "偏財" },
  DO: { en: "Direct Officer", zh: "正官" },
  "7K": { en: "Seven Killings", zh: "七殺" },
  DR: { en: "Direct Resource", zh: "正印" },
  IR: { en: "Indirect Resource", zh: "偏印" },
};

export const TEN_GOD_EXCESS_TRAITS: Record<string, { en: string; zh: string }> = {
  F: { en: "competitive, self-centered", zh: "好勝，自我中心" },
  RW: { en: "aggressive, impulsive", zh: "攻擊性，衝動" },
  EG: { en: "indulgent, scattered", zh: "放縱，分散" },
  HO: { en: "rebellious, sharp-tongued", zh: "叛逆，尖銳" },
  DW: { en: "materialistic, possessive", zh: "物質主義，占有欲" },
  IW: { en: "speculative, unfocused", zh: "投機，不專注" },
  DO: { en: "rigid, constrained", zh: "僵化，受約束" },
  "7K": { en: "domineering, ruthless", zh: "霸道，無情" },
  DR: { en: "dependent, passive", zh: "依賴，被動" },
  IR: { en: "isolated, unconventional", zh: "孤立，非常規" },
};

// ---------------------------------------------------------------------------
// Chain Analysis
// ---------------------------------------------------------------------------

export interface ChainAnalysisResult {
  node_id: string;
  element: string;
  qi_phase: string | null;
  qi_phase_meaning: { en: string; zh: string } | null;
  shen_sha: Array<{ type: string; meaning: ShenShaMeaning }>;
  ten_god: string | null;
  ten_god_info: { en: string; zh: string } | null;
  is_storage: boolean;
  storage_element: string | null;
  narrative_en: string;
  narrative_zh: string;
}

export function analyzeNodeChain(
  nodeId: string,
  stem: StemName | null,
  branch: BranchName | null,
  daymasterStem: StemName,
  shenShaByNode: Record<string, string[]>,
  qiPhaseByNode: Record<string, string>,
  tenGodByNode: Record<string, string>
): ChainAnalysisResult {
  const parts: string[] = [];
  const partsZh: string[] = [];

  // Qi Phase
  const qiPhase = qiPhaseByNode[nodeId] ?? null;
  let qiPhaseMeaning: { en: string; zh: string } | null = null;
  if (qiPhase && QI_PHASE_MEANINGS[qiPhase]) {
    qiPhaseMeaning = QI_PHASE_MEANINGS[qiPhase];
    parts.push(`Qi phase: ${qiPhase} - ${qiPhaseMeaning.en}`);
    partsZh.push(`氣相：${qiPhase} - ${qiPhaseMeaning.zh}`);
  }

  // Shen Sha
  const nodeShenSha = shenShaByNode[nodeId] ?? [];
  const shenShaResults: Array<{ type: string; meaning: ShenShaMeaning }> = [];
  for (const ssType of nodeShenSha) {
    const meaning = SHEN_SHA_MEANINGS[ssType];
    if (meaning) {
      shenShaResults.push({ type: ssType, meaning });
      parts.push(`${meaning.name_en} (${meaning.name_zh}): ${meaning.positive.en}`);
      partsZh.push(`${meaning.name_zh}（${meaning.name_en}）：${meaning.positive.zh}`);
    }
  }

  // Ten God
  const tenGod = tenGodByNode[nodeId] ?? null;
  let tenGodInfo: { en: string; zh: string } | null = null;
  if (tenGod && TEN_GOD_NAMES[tenGod]) {
    tenGodInfo = TEN_GOD_NAMES[tenGod];
    parts.push(`Ten God: ${tenGodInfo.en} (${tenGodInfo.zh})`);
    partsZh.push(`十神：${tenGodInfo.zh}（${tenGodInfo.en}）`);
  }

  // Storage check
  let isStorage = false;
  let storageElement: string | null = null;
  if (branch && STORAGE_BRANCHES[branch]) {
    isStorage = true;
    storageElement = STORAGE_BRANCHES[branch];
    parts.push(`Storage branch for ${storageElement}`);
    partsZh.push(`${storageElement}的庫位`);
  }

  // Element
  let element = '';
  if (stem) {
    const stemData = STEMS[stem];
    element = stemData?.element ?? '';
  }

  return {
    node_id: nodeId,
    element,
    qi_phase: qiPhase,
    qi_phase_meaning: qiPhaseMeaning,
    shen_sha: shenShaResults,
    ten_god: tenGod,
    ten_god_info: tenGodInfo,
    is_storage: isStorage,
    storage_element: storageElement,
    narrative_en: parts.join(". ") || "No additional context.",
    narrative_zh: partsZh.join("。") || "無額外背景。",
  };
}

// ---------------------------------------------------------------------------
// Enrich Clash with Chain Analysis
// ---------------------------------------------------------------------------

export function enrichClashWithChainAnalysis(
  clashNarrative: { en: string; zh: string },
  sourceChain: ChainAnalysisResult,
  targetChain: ChainAnalysisResult
): { en: string; zh: string } {
  const enrichEn: string[] = [clashNarrative.en];
  const enrichZh: string[] = [clashNarrative.zh];

  // Add Shen Sha context
  for (const chain of [sourceChain, targetChain]) {
    for (const ss of chain.shen_sha) {
      enrichEn.push(`${ss.meaning.name_en}: ${ss.meaning.with_clash.en}`);
      enrichZh.push(`${ss.meaning.name_zh}：${ss.meaning.with_clash.zh}`);
    }
  }

  // Add storage context
  if (sourceChain.is_storage || targetChain.is_storage) {
    const storageChain = sourceChain.is_storage ? sourceChain : targetChain;
    enrichEn.push(`Storage branch (${storageChain.storage_element}) is clashed - vault opened`);
    enrichZh.push(`庫位（${storageChain.storage_element}）被沖 - 庫門打開`);
  }

  // Add Qi Phase context
  for (const chain of [sourceChain, targetChain]) {
    if (chain.qi_phase_meaning) {
      enrichEn.push(`${chain.node_id}: ${chain.qi_phase_meaning.en}`);
      enrichZh.push(`${chain.node_id}：${chain.qi_phase_meaning.zh}`);
    }
  }

  return {
    en: enrichEn.join(". "),
    zh: enrichZh.join("。"),
  };
}

// ---------------------------------------------------------------------------
// Helper: Element Chinese
// ---------------------------------------------------------------------------

function elementZh(element: string): string {
  const map: Record<string, string> = {
    Wood: "木", Fire: "火", Earth: "土", Metal: "金", Water: "水",
  };
  return map[element] ?? element;
}

function traitsZh(traits: string): string {
  return traits; // Keep original for now
}

// ---------------------------------------------------------------------------
// Build Combined Narrative
// ---------------------------------------------------------------------------

export function buildCombinedNarrative(
  baseNarrative: { en: string; zh: string },
  chainResults: ChainAnalysisResult[]
): { en: string; zh: string } {
  const combinedEn = [baseNarrative.en];
  const combinedZh = [baseNarrative.zh];

  for (const chain of chainResults) {
    if (chain.narrative_en !== "No additional context.") {
      combinedEn.push(`[${chain.node_id}] ${chain.narrative_en}`);
    }
    if (chain.narrative_zh !== "無額外背景。") {
      combinedZh.push(`[${chain.node_id}] ${chain.narrative_zh}`);
    }
  }

  return {
    en: combinedEn.join("\n"),
    zh: combinedZh.join("\n"),
  };
}
