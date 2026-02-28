
// =============================================================================
// NARRATIVE TEMPLATES
// =============================================================================
// Template text for generating BaZi narrative descriptions.
// Ported from api/library/narrative/templates.py
// =============================================================================

import type { Element } from '../core';

// ---------------------------------------------------------------------------
// Template Entry
// ---------------------------------------------------------------------------

export interface NarrativeTemplate {
  en: string;
  zh: string;
  category: string;
  sentiment: 'positive' | 'negative' | 'neutral' | 'conditional';
  priority: number;
}

// ---------------------------------------------------------------------------
// NARRATIVE TEMPLATES
// ---------------------------------------------------------------------------

export const NARRATIVE_TEMPLATES: Record<string, NarrativeTemplate> = {
  // ---- Branch Combinations (positive) ----
  three_meetings: {
    en: "Three Meetings ({branches}) form {element} energy in {pillars}. This powerful seasonal combination brings concentrated {element} influence, affecting {domains}.",
    zh: "三會{element_zh}局（{branches_zh}）在{pillars_zh}形成。這個強大的方局帶來集中的{element_zh}力量，影響{domains_zh}。",
    category: "combination",
    sentiment: "positive",
    priority: 100,
  },
  three_combinations: {
    en: "Three Combinations ({branches}) unite into {element} in {pillars}. This triangular harmony creates balanced {element} energy, benefiting {domains}.",
    zh: "三合{element_zh}局（{branches_zh}）在{pillars_zh}。三角和諧產生平衡的{element_zh}能量，有益於{domains_zh}。",
    category: "combination",
    sentiment: "positive",
    priority: 110,
  },
  six_harmonies: {
    en: "Six Harmonies between {branches} create {element} in {pillars}. This intimate pairing brings harmony and cooperation in {domains}.",
    zh: "六合（{branches_zh}）在{pillars_zh}合{element_zh}。這個親密的配對帶來和諧與合作，影響{domains_zh}。",
    category: "combination",
    sentiment: "positive",
    priority: 120,
  },
  half_meetings: {
    en: "Half Meeting ({branches}) suggests partial {element} energy in {pillars}. Incomplete but still influential for {domains}.",
    zh: "半會（{branches_zh}）在{pillars_zh}暗示部分{element_zh}能量。雖不完整但仍影響{domains_zh}。",
    category: "combination",
    sentiment: "positive",
    priority: 130,
  },
  half_combinations: {
    en: "Half Combination ({branches}) hints at {element} potential in {pillars}. A partial triangle with latent energy for {domains}.",
    zh: "半合（{branches_zh}）在{pillars_zh}暗示{element_zh}潛力。部分三角帶有潛在能量，影響{domains_zh}。",
    category: "combination",
    sentiment: "positive",
    priority: 140,
  },
  arched_combinations: {
    en: "Arched Combination ({branches}) weakly connects to {element} in {pillars}. The weakest combination form, with subtle {domains} influence.",
    zh: "拱合（{branches_zh}）在{pillars_zh}弱連接{element_zh}。最弱的合局形式，對{domains_zh}有微妙影響。",
    category: "combination",
    sentiment: "positive",
    priority: 150,
  },
  stem_combination: {
    en: "Stem Combination ({stems}) transforms to {element} in {pillars}. Heavenly stems unite, bringing {domains} benefits.",
    zh: "天干合（{stems_zh}）在{pillars_zh}化{element_zh}。天干合化帶來{domains_zh}的好處。",
    category: "combination",
    sentiment: "positive",
    priority: 50,
  },

  // ---- Branch Conflicts (negative) ----
  clash: {
    en: "Clash between {branches} in {pillars}. Direct opposition creates turbulence in {domains}. {severity_text}",
    zh: "地支沖（{branches_zh}）在{pillars_zh}。直接對沖造成{domains_zh}的動盪。{severity_text_zh}",
    category: "conflict",
    sentiment: "negative",
    priority: 200,
  },
  punishment: {
    en: "Punishment ({branches}) in {pillars}. {punishment_type} punishment brings {domains} challenges. {severity_text}",
    zh: "地支刑（{branches_zh}）在{pillars_zh}。{punishment_type_zh}刑帶來{domains_zh}的挑戰。{severity_text_zh}",
    category: "conflict",
    sentiment: "negative",
    priority: 210,
  },
  harm: {
    en: "Harm between {branches} in {pillars}. Subtle undermining affects {domains}. {severity_text}",
    zh: "地支害（{branches_zh}）在{pillars_zh}。暗中破壞影響{domains_zh}。{severity_text_zh}",
    category: "conflict",
    sentiment: "negative",
    priority: 240,
  },
  destruction: {
    en: "Destruction between {branches} in {pillars}. Breaking force impacts {domains}. {severity_text}",
    zh: "地支破（{branches_zh}）在{pillars_zh}。破壞力量影響{domains_zh}。{severity_text_zh}",
    category: "conflict",
    sentiment: "negative",
    priority: 250,
  },
  stem_conflict: {
    en: "Stem Conflict ({stems}) in {pillars}. Heavenly stem clash disrupts {domains}. {severity_text}",
    zh: "天干剋（{stems_zh}）在{pillars_zh}。天干衝突擾亂{domains_zh}。{severity_text_zh}",
    category: "conflict",
    sentiment: "negative",
    priority: 60,
  },

  // ---- Element Balance ----
  element_excess: {
    en: "{element} is excessive ({score}%). {excess_text} Consider activities that channel this abundance constructively.",
    zh: "{element_zh}過旺（{score}%）。{excess_text_zh} 建議從事能建設性地引導這種過剩的活動。",
    category: "balance",
    sentiment: "conditional",
    priority: 300,
  },
  element_deficient: {
    en: "{element} is deficient ({score}%). {deficient_text} Consider strengthening this element through lifestyle adjustments.",
    zh: "{element_zh}不足（{score}%）。{deficient_text_zh} 建議通過生活方式調整來加強這個元素。",
    category: "balance",
    sentiment: "conditional",
    priority: 310,
  },

  // ---- Day Master ----
  daymaster_strong: {
    en: "Day Master {stem} ({element}) is strong at {score}%. Self-reliant nature with abundant personal energy. May benefit from channeling energy outward.",
    zh: "日主{stem_zh}（{element_zh}）旺相，{score}%。自立自強，個人能量充沛。可能受益於將能量向外引導。",
    category: "daymaster",
    sentiment: "neutral",
    priority: 10,
  },
  daymaster_weak: {
    en: "Day Master {stem} ({element}) is weak at {score}%. Receptive nature that benefits from support. Seek allies and resources aligned with {element}.",
    zh: "日主{stem_zh}（{element_zh}）偏弱，{score}%。善於接受，需要支持。尋求與{element_zh}一致的盟友和資源。",
    category: "daymaster",
    sentiment: "neutral",
    priority: 10,
  },
  daymaster_balanced: {
    en: "Day Master {stem} ({element}) is balanced at {score}%. Harmonious self-expression with neither excess nor deficiency.",
    zh: "日主{stem_zh}（{element_zh}）平衡，{score}%。和諧的自我表達，既不過多也不缺乏。",
    category: "daymaster",
    sentiment: "positive",
    priority: 10,
  },

  // ---- Wealth Storage ----
  wealth_storage_present: {
    en: "Wealth Storage ({branch}) present in {pillar}. Natural ability to accumulate and preserve wealth. The {element} storage is {state}.",
    zh: "財庫（{branch_zh}）在{pillar_zh}。天生善於積累和保存財富。{element_zh}庫{state_zh}。",
    category: "wealth",
    sentiment: "positive",
    priority: 400,
  },
  wealth_storage_clashed: {
    en: "Wealth Storage ({branch}) is clashed in {pillar}. The vault is opened - wealth flows out. Can indicate large transactions or unexpected expenses.",
    zh: "財庫（{branch_zh}）在{pillar_zh}被沖。庫門打開 - 財富外流。可能表示大額交易或意外支出。",
    category: "wealth",
    sentiment: "conditional",
    priority: 410,
  },

  // ---- Shen Sha ----
  shen_sha: {
    en: "{star_name} ({star_chinese}) present in {pillar}. {description}",
    zh: "{star_chinese}（{star_name}）在{pillar_zh}。{description_zh}",
    category: "shen_sha",
    sentiment: "conditional",
    priority: 500,
  },

  // ---- Ten Gods ----
  ten_god_pillar: {
    en: "{ten_god} ({ten_god_chinese}) at {position} pillar: {meaning}",
    zh: "{ten_god_chinese}（{ten_god}）在{position_zh}柱：{meaning_zh}",
    category: "ten_gods",
    sentiment: "neutral",
    priority: 600,
  },

  // ---- Summary ----
  chart_summary: {
    en: "Chart Overview: {summary_text}",
    zh: "命盤概覽：{summary_text_zh}",
    category: "summary",
    sentiment: "neutral",
    priority: 1,
  },
};

// ---------------------------------------------------------------------------
// ELEMENT MANIFESTATIONS
// ---------------------------------------------------------------------------

export interface ElementManifestation {
  excess: { en: string; zh: string };
  deficient: { en: string; zh: string };
}

export const ELEMENT_MANIFESTATIONS: Record<Element, ElementManifestation> = {
  Wood: {
    excess: {
      en: "Excessive Wood can manifest as stubbornness, anger, overplanning, and liver/gallbladder stress.",
      zh: "木過旺可能表現為固執、易怒、過度計劃，以及肝膽壓力。",
    },
    deficient: {
      en: "Wood deficiency may show as indecisiveness, lack of growth, difficulty planning, and weakened liver function.",
      zh: "木不足可能表現為優柔寡斷、缺乏成長、難以規劃，以及肝功能減弱。",
    },
  },
  Fire: {
    excess: {
      en: "Excessive Fire can manifest as anxiety, restlessness, impulsivity, and heart/circulatory issues.",
      zh: "火過旺可能表現為焦慮、不安、衝動，以及心血管問題。",
    },
    deficient: {
      en: "Fire deficiency may show as lack of passion, cold personality, depression, and poor circulation.",
      zh: "火不足可能表現為缺乏熱情、性格冷淡、抑鬱，以及循環不良。",
    },
  },
  Earth: {
    excess: {
      en: "Excessive Earth can manifest as overthinking, worry, stubbornness, and digestive problems.",
      zh: "土過旺可能表現為多慮、擔憂、固執，以及消化問題。",
    },
    deficient: {
      en: "Earth deficiency may show as instability, poor boundaries, scattered thinking, and weak digestion.",
      zh: "土不足可能表現為不穩定、缺乏邊界、思維散亂，以及消化功能弱。",
    },
  },
  Metal: {
    excess: {
      en: "Excessive Metal can manifest as rigidity, perfectionism, grief, and respiratory issues.",
      zh: "金過旺可能表現為僵硬、完美主義、悲傷，以及呼吸系統問題。",
    },
    deficient: {
      en: "Metal deficiency may show as lack of discipline, poor boundaries, vulnerability, and weak lungs.",
      zh: "金不足可能表現為缺乏紀律、邊界不清、脆弱，以及肺功能弱。",
    },
  },
  Water: {
    excess: {
      en: "Excessive Water can manifest as fear, indecision, excess emotion, and kidney/bladder issues.",
      zh: "水過旺可能表現為恐懼、猶豫不決、情緒過多，以及腎膀胱問題。",
    },
    deficient: {
      en: "Water deficiency may show as lack of wisdom, rigidity, dryness, and weakened kidneys.",
      zh: "水不足可能表現為缺乏智慧、僵硬、乾燥，以及腎功能減弱。",
    },
  },
};

// ---------------------------------------------------------------------------
// PILLAR CONTEXT
// ---------------------------------------------------------------------------

export const PILLAR_CONTEXT: Record<string, { en: string; zh: string }> = {
  year: {
    en: "Year pillar represents ancestry, early childhood (0-15), and external environment.",
    zh: "年柱代表祖先、幼年（0-15歲）和外部環境。",
  },
  month: {
    en: "Month pillar represents parents, career (16-30), and social position.",
    zh: "月柱代表父母、事業（16-30歲）和社會地位。",
  },
  day: {
    en: "Day pillar represents self, marriage (31-45), and inner nature.",
    zh: "日柱代表自己、婚姻（31-45歲）和內在本質。",
  },
  hour: {
    en: "Hour pillar represents children, later life (46+), and legacy.",
    zh: "時柱代表子女、晚年（46歲以上）和遺產。",
  },
};
