import 'server-only';

// =============================================================================
// BAZI CORE - THE 10 HEAVENLY STEMS & 12 EARTHLY BRANCHES
// =============================================================================
// This file contains ONLY the two fundamental constants: STEMS and BRANCHES.
// All other data, patterns, and functions are derived from these.
// =============================================================================

// ---------------------------------------------------------------------------
// Type definitions
// ---------------------------------------------------------------------------

export type Element = "Wood" | "Fire" | "Earth" | "Metal" | "Water";
export type Polarity = "Yang" | "Yin";
export type Season = "Spring" | "Summer" | "Autumn" | "Winter";
export type ElementState = "Prosperous" | "Strengthening" | "Resting" | "Trapped" | "Dead";

export type TenGodCode = "F" | "RW" | "EG" | "HO" | "IW" | "DW" | "7K" | "DO" | "IR" | "DR";

export type TenGodTuple = readonly [TenGodCode, string, string];

export type StemName = "Jia" | "Yi" | "Bing" | "Ding" | "Wu" | "Ji" | "Geng" | "Xin" | "Ren" | "Gui";
export type BranchName = "Zi" | "Chou" | "Yin" | "Mao" | "Chen" | "Si" | "Wu" | "Wei" | "Shen" | "You" | "Xu" | "Hai";

export type HarmRole = "victim" | "controller";
export type PunishmentType = "wu_li" | "shi" | "en";

export type QiEntry = readonly [StemName, number];

export interface StemData {
  readonly index: number;
  readonly chinese: string;
  readonly element: Element;
  readonly polarity: Polarity;
  readonly color: string;
  readonly combines_with: StemName;
  readonly combination_element: Element;
  readonly controls: StemName;
  readonly controlled_by: StemName;
  readonly ten_gods: Readonly<Record<StemName, TenGodTuple>>;
}

export interface BranchData {
  readonly index: number;
  readonly chinese: string;
  readonly element: Element;
  readonly polarity: Polarity;
  readonly animal: string;
  readonly color: string;
  readonly month: number;
  readonly season: Season;
  readonly dong_gong_index: number;
  readonly qi: readonly QiEntry[];
  readonly clashes: BranchName;
  readonly harmonizes: BranchName;
  readonly harmony_element: Element;
  readonly harms: BranchName;
  readonly harm_role: HarmRole;
  readonly destroys: BranchName | null;
  readonly three_combo: readonly [BranchName, BranchName, BranchName, Element];
  readonly season_combo: readonly [BranchName, BranchName, BranchName, Element];
  readonly punishment_group?: readonly [BranchName, BranchName, BranchName, PunishmentType];
  readonly punishment_pair?: readonly [BranchName, PunishmentType, HarmRole];
  readonly self_punishment: boolean;
  readonly self_punishment_nature?: string;
  readonly is_storage?: boolean;
  readonly stored_element?: Element;
  readonly stored_stem?: StemName;
  readonly opener?: BranchName;
  readonly element_states: Readonly<Record<Element, ElementState>>;
}

// =============================================================================
// THE 10 HEAVENLY STEMS (天干)
// =============================================================================
// Each stem contains ALL its properties including element relationships.
// Element cycles (generating/controlling) can be derived from the element field.
export const STEMS = {
  Jia: {
    index: 0, chinese: "甲", element: "Wood", polarity: "Yang",
    color: "#c2d4be",
    combines_with: "Ji", combination_element: "Earth",
    controls: "Wu", controlled_by: "Geng",
    ten_gods: {
      Jia: ["F", "Friend", "比肩"] as const,
      Yi: ["RW", "Rob Wealth", "劫財"] as const,
      Bing: ["EG", "Eating God", "食神"] as const,
      Ding: ["HO", "Hurting Officer", "傷官"] as const,
      Wu: ["IW", "Indirect Wealth", "偏財"] as const,
      Ji: ["DW", "Direct Wealth", "正財"] as const,
      Geng: ["7K", "Seven Killings", "七殺"] as const,
      Xin: ["DO", "Direct Officer", "正官"] as const,
      Ren: ["IR", "Indirect Resource", "偏印"] as const,
      Gui: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Yi: {
    index: 1, chinese: "乙", element: "Wood", polarity: "Yin",
    color: "#d6e2bb",
    combines_with: "Geng", combination_element: "Metal",
    controls: "Ji", controlled_by: "Xin",
    ten_gods: {
      Yi: ["F", "Friend", "比肩"] as const,
      Jia: ["RW", "Rob Wealth", "劫財"] as const,
      Ding: ["EG", "Eating God", "食神"] as const,
      Bing: ["HO", "Hurting Officer", "傷官"] as const,
      Ji: ["IW", "Indirect Wealth", "偏財"] as const,
      Wu: ["DW", "Direct Wealth", "正財"] as const,
      Xin: ["7K", "Seven Killings", "七殺"] as const,
      Geng: ["DO", "Direct Officer", "正官"] as const,
      Gui: ["IR", "Indirect Resource", "偏印"] as const,
      Ren: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Bing: {
    index: 2, chinese: "丙", element: "Fire", polarity: "Yang",
    color: "#fca5a5",
    combines_with: "Xin", combination_element: "Water",
    controls: "Geng", controlled_by: "Ren",
    ten_gods: {
      Bing: ["F", "Friend", "比肩"] as const,
      Ding: ["RW", "Rob Wealth", "劫財"] as const,
      Wu: ["EG", "Eating God", "食神"] as const,
      Ji: ["HO", "Hurting Officer", "傷官"] as const,
      Geng: ["IW", "Indirect Wealth", "偏財"] as const,
      Xin: ["DW", "Direct Wealth", "正財"] as const,
      Ren: ["7K", "Seven Killings", "七殺"] as const,
      Gui: ["DO", "Direct Officer", "正官"] as const,
      Jia: ["IR", "Indirect Resource", "偏印"] as const,
      Yi: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Ding: {
    index: 3, chinese: "丁", element: "Fire", polarity: "Yin",
    color: "#f9d3ad",
    combines_with: "Ren", combination_element: "Wood",
    controls: "Xin", controlled_by: "Gui",
    ten_gods: {
      Ding: ["F", "Friend", "比肩"] as const,
      Bing: ["RW", "Rob Wealth", "劫財"] as const,
      Ji: ["EG", "Eating God", "食神"] as const,
      Wu: ["HO", "Hurting Officer", "傷官"] as const,
      Xin: ["IW", "Indirect Wealth", "偏財"] as const,
      Geng: ["DW", "Direct Wealth", "正財"] as const,
      Gui: ["7K", "Seven Killings", "七殺"] as const,
      Ren: ["DO", "Direct Officer", "正官"] as const,
      Yi: ["IR", "Indirect Resource", "偏印"] as const,
      Jia: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Wu: {
    index: 4, chinese: "戊", element: "Earth", polarity: "Yang",
    color: "#e6ceb7",
    combines_with: "Gui", combination_element: "Fire",
    controls: "Ren", controlled_by: "Jia",
    ten_gods: {
      Wu: ["F", "Friend", "比肩"] as const,
      Ji: ["RW", "Rob Wealth", "劫財"] as const,
      Geng: ["EG", "Eating God", "食神"] as const,
      Xin: ["HO", "Hurting Officer", "傷官"] as const,
      Ren: ["IW", "Indirect Wealth", "偏財"] as const,
      Gui: ["DW", "Direct Wealth", "正財"] as const,
      Jia: ["7K", "Seven Killings", "七殺"] as const,
      Yi: ["DO", "Direct Officer", "正官"] as const,
      Bing: ["IR", "Indirect Resource", "偏印"] as const,
      Ding: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Ji: {
    index: 5, chinese: "己", element: "Earth", polarity: "Yin",
    color: "#efe3cc",
    combines_with: "Jia", combination_element: "Earth",
    controls: "Gui", controlled_by: "Yi",
    ten_gods: {
      Ji: ["F", "Friend", "比肩"] as const,
      Wu: ["RW", "Rob Wealth", "劫財"] as const,
      Xin: ["EG", "Eating God", "食神"] as const,
      Geng: ["HO", "Hurting Officer", "傷官"] as const,
      Gui: ["IW", "Indirect Wealth", "偏財"] as const,
      Ren: ["DW", "Direct Wealth", "正財"] as const,
      Yi: ["7K", "Seven Killings", "七殺"] as const,
      Jia: ["DO", "Direct Officer", "正官"] as const,
      Ding: ["IR", "Indirect Resource", "偏印"] as const,
      Bing: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Geng: {
    index: 6, chinese: "庚", element: "Metal", polarity: "Yang",
    color: "#ccd8e6",
    combines_with: "Yi", combination_element: "Metal",
    controls: "Jia", controlled_by: "Bing",
    ten_gods: {
      Geng: ["F", "Friend", "比肩"] as const,
      Xin: ["RW", "Rob Wealth", "劫財"] as const,
      Ren: ["EG", "Eating God", "食神"] as const,
      Gui: ["HO", "Hurting Officer", "傷官"] as const,
      Jia: ["IW", "Indirect Wealth", "偏財"] as const,
      Yi: ["DW", "Direct Wealth", "正財"] as const,
      Bing: ["7K", "Seven Killings", "七殺"] as const,
      Ding: ["DO", "Direct Officer", "正官"] as const,
      Wu: ["IR", "Indirect Resource", "偏印"] as const,
      Ji: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Xin: {
    index: 7, chinese: "辛", element: "Metal", polarity: "Yin",
    color: "#e6e8f7",
    combines_with: "Bing", combination_element: "Water",
    controls: "Yi", controlled_by: "Ding",
    ten_gods: {
      Xin: ["F", "Friend", "比肩"] as const,
      Geng: ["RW", "Rob Wealth", "劫財"] as const,
      Gui: ["EG", "Eating God", "食神"] as const,
      Ren: ["HO", "Hurting Officer", "傷官"] as const,
      Yi: ["IW", "Indirect Wealth", "偏財"] as const,
      Jia: ["DW", "Direct Wealth", "正財"] as const,
      Ding: ["7K", "Seven Killings", "七殺"] as const,
      Bing: ["DO", "Direct Officer", "正官"] as const,
      Ji: ["IR", "Indirect Resource", "偏印"] as const,
      Wu: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Ren: {
    index: 8, chinese: "壬", element: "Water", polarity: "Yang",
    color: "#b9cbff",
    combines_with: "Ding", combination_element: "Wood",
    controls: "Bing", controlled_by: "Wu",
    ten_gods: {
      Ren: ["F", "Friend", "比肩"] as const,
      Gui: ["RW", "Rob Wealth", "劫財"] as const,
      Jia: ["EG", "Eating God", "食神"] as const,
      Yi: ["HO", "Hurting Officer", "傷官"] as const,
      Bing: ["IW", "Indirect Wealth", "偏財"] as const,
      Ding: ["DW", "Direct Wealth", "正財"] as const,
      Wu: ["7K", "Seven Killings", "七殺"] as const,
      Ji: ["DO", "Direct Officer", "正官"] as const,
      Geng: ["IR", "Indirect Resource", "偏印"] as const,
      Xin: ["DR", "Direct Resource", "正印"] as const,
    },
  },
  Gui: {
    index: 9, chinese: "癸", element: "Water", polarity: "Yin",
    color: "#e0e9ff",
    combines_with: "Wu", combination_element: "Fire",
    controls: "Ding", controlled_by: "Ji",
    ten_gods: {
      Gui: ["F", "Friend", "比肩"] as const,
      Ren: ["RW", "Rob Wealth", "劫財"] as const,
      Yi: ["EG", "Eating God", "食神"] as const,
      Jia: ["HO", "Hurting Officer", "傷官"] as const,
      Ding: ["IW", "Indirect Wealth", "偏財"] as const,
      Bing: ["DW", "Direct Wealth", "正財"] as const,
      Ji: ["7K", "Seven Killings", "七殺"] as const,
      Wu: ["DO", "Direct Officer", "正官"] as const,
      Xin: ["IR", "Indirect Resource", "偏印"] as const,
      Geng: ["DR", "Direct Resource", "正印"] as const,
    },
  },
} as const satisfies Record<StemName, StemData>;

// =============================================================================
// THE 12 EARTHLY BRANCHES (地支)
// =============================================================================
// Each branch contains ALL its properties, relationships, and metadata.
// Day Officers (十二建除) are embedded via dong_gong_index.
export const BRANCHES = {
  Zi: {
    index: 0, chinese: "子", element: "Water", polarity: "Yang",
    animal: "Rat", color: "#b9cbff", month: 11, season: "Winter",
    dong_gong_index: 10,
    qi: [["Gui", 100] as const],
    clashes: "Wu", harmonizes: "Chou", harmony_element: "Earth",
    harms: "Wei", harm_role: "victim",
    destroys: "You",
    three_combo: ["Shen", "Zi", "Chen", "Water"] as const,
    season_combo: ["Hai", "Zi", "Chou", "Water"] as const,
    self_punishment: false,
    // Winter (Water rules): Water=旺, Wood=相(Xiang), Metal=休, Earth=囚, Fire=死
    element_states: { Wood: "Strengthening", Fire: "Dead", Earth: "Trapped", Metal: "Resting", Water: "Prosperous" },
  },
  Chou: {
    index: 1, chinese: "丑", element: "Earth", polarity: "Yin",
    animal: "Ox", color: "#efe3cc", month: 12, season: "Winter",
    dong_gong_index: 11,
    qi: [["Ji", 75] as const, ["Gui", 25] as const, ["Xin", 10] as const],
    clashes: "Wei", harmonizes: "Zi", harmony_element: "Earth",
    harms: "Wu", harm_role: "victim",
    destroys: "Chen",
    three_combo: ["Si", "You", "Chou", "Metal"] as const,
    season_combo: ["Hai", "Zi", "Chou", "Water"] as const,
    punishment_group: ["Chou", "Wei", "Xu", "wu_li"] as const,
    self_punishment: false,
    is_storage: true, stored_element: "Metal", stored_stem: "Xin", opener: "Wei",
    // Earth* season (Earth rules): Earth=旺(Wang), Metal=相(Xiang), Fire=休(Xiu), Wood=囚(Qiu), Water=死(Si)
    element_states: { Wood: "Trapped", Fire: "Resting", Earth: "Prosperous", Metal: "Strengthening", Water: "Dead" },
  },
  Yin: {
    index: 2, chinese: "寅", element: "Wood", polarity: "Yang",
    animal: "Tiger", color: "#c2d4be", month: 1, season: "Spring",
    dong_gong_index: 0,
    qi: [["Jia", 75] as const, ["Bing", 25] as const, ["Wu", 10] as const],
    clashes: "Shen", harmonizes: "Hai", harmony_element: "Wood",
    harms: "Si", harm_role: "victim",
    destroys: null,
    three_combo: ["Yin", "Wu", "Xu", "Fire"] as const,
    season_combo: ["Yin", "Mao", "Chen", "Wood"] as const,
    punishment_group: ["Yin", "Si", "Shen", "shi"] as const,
    self_punishment: false,
    // Spring (Wood rules): Wood=旺, Fire=相, Water=休, Metal=囚, Earth=死
    element_states: { Wood: "Prosperous", Fire: "Strengthening", Earth: "Dead", Metal: "Trapped", Water: "Resting" },
  },
  Mao: {
    index: 3, chinese: "卯", element: "Wood", polarity: "Yin",
    animal: "Rabbit", color: "#d6e2bb", month: 2, season: "Spring",
    dong_gong_index: 1,
    qi: [["Yi", 100] as const],
    clashes: "You", harmonizes: "Xu", harmony_element: "Fire",
    harms: "Chen", harm_role: "victim",
    destroys: "Wu",
    three_combo: ["Hai", "Mao", "Wei", "Wood"] as const,
    season_combo: ["Yin", "Mao", "Chen", "Wood"] as const,
    punishment_pair: ["Zi", "en", "controller"] as const,
    self_punishment: false,
    // Spring (Wood rules): Wood=旺, Fire=相, Water=休, Metal=囚, Earth=死
    element_states: { Wood: "Prosperous", Fire: "Strengthening", Earth: "Dead", Metal: "Trapped", Water: "Resting" },
  },
  Chen: {
    index: 4, chinese: "辰", element: "Earth", polarity: "Yang",
    animal: "Dragon", color: "#e6ceb7", month: 3, season: "Spring",
    dong_gong_index: 2,
    qi: [["Wu", 75] as const, ["Yi", 25] as const, ["Gui", 10] as const],
    clashes: "Xu", harmonizes: "You", harmony_element: "Metal",
    harms: "Mao", harm_role: "controller",
    destroys: "Chou",
    three_combo: ["Shen", "Zi", "Chen", "Water"] as const,
    season_combo: ["Yin", "Mao", "Chen", "Wood"] as const,
    self_punishment: true,
    self_punishment_nature: "Earth Dragon - stubborn pride leads to isolation",
    is_storage: true, stored_element: "Water", stored_stem: "Gui", opener: "Xu",
    // Earth* season (Earth rules): Earth=旺(Wang), Metal=相(Xiang), Fire=休(Xiu), Wood=囚(Qiu), Water=死(Si)
    element_states: { Wood: "Trapped", Fire: "Resting", Earth: "Prosperous", Metal: "Strengthening", Water: "Dead" },
  },
  Si: {
    index: 5, chinese: "巳", element: "Fire", polarity: "Yin",
    animal: "Snake", color: "#f9d3ad", month: 4, season: "Summer",
    dong_gong_index: 3,
    qi: [["Bing", 75] as const, ["Geng", 25] as const, ["Wu", 10] as const],
    clashes: "Hai", harmonizes: "Shen", harmony_element: "Water",
    harms: "Yin", harm_role: "controller",
    destroys: null,
    three_combo: ["Si", "You", "Chou", "Metal"] as const,
    season_combo: ["Si", "Wu", "Wei", "Fire"] as const,
    punishment_group: ["Yin", "Si", "Shen", "shi"] as const,
    self_punishment: false,
    // Summer (Fire rules): Fire=旺, Earth=相, Wood=休, Water=囚, Metal=死
    element_states: { Wood: "Resting", Fire: "Prosperous", Earth: "Strengthening", Metal: "Dead", Water: "Trapped" },
  },
  Wu: {
    index: 6, chinese: "午", element: "Fire", polarity: "Yang",
    animal: "Horse", color: "#f3adae", month: 5, season: "Summer",
    dong_gong_index: 4,
    qi: [["Ding", 80] as const, ["Ji", 20] as const],
    clashes: "Zi", harmonizes: "Wei", harmony_element: "Fire",
    harms: "Chou", harm_role: "controller",
    destroys: "Mao",
    three_combo: ["Yin", "Wu", "Xu", "Fire"] as const,
    season_combo: ["Si", "Wu", "Wei", "Fire"] as const,
    self_punishment: true,
    self_punishment_nature: "Fire Horse - restless energy burns itself out",
    // Summer (Fire rules): Fire=旺, Earth=相, Wood=休, Water=囚, Metal=死
    element_states: { Wood: "Resting", Fire: "Prosperous", Earth: "Strengthening", Metal: "Dead", Water: "Trapped" },
  },
  Wei: {
    index: 7, chinese: "未", element: "Earth", polarity: "Yin",
    animal: "Goat", color: "#efe3cc", month: 6, season: "Summer",
    dong_gong_index: 5,
    qi: [["Ji", 75] as const, ["Ding", 25] as const, ["Yi", 10] as const],
    clashes: "Chou", harmonizes: "Wu", harmony_element: "Fire",
    harms: "Zi", harm_role: "controller",
    destroys: "Xu",
    three_combo: ["Hai", "Mao", "Wei", "Wood"] as const,
    season_combo: ["Si", "Wu", "Wei", "Fire"] as const,
    punishment_group: ["Chou", "Wei", "Xu", "wu_li"] as const,
    self_punishment: false,
    is_storage: true, stored_element: "Wood", stored_stem: "Yi", opener: "Chou",
    // Earth* season (Earth rules): Earth=旺(Wang), Metal=相(Xiang), Fire=休(Xiu), Wood=囚(Qiu), Water=死(Si)
    element_states: { Wood: "Trapped", Fire: "Resting", Earth: "Prosperous", Metal: "Strengthening", Water: "Dead" },
  },
  Shen: {
    index: 8, chinese: "申", element: "Metal", polarity: "Yang",
    animal: "Monkey", color: "#ccd8e6", month: 7, season: "Autumn",
    dong_gong_index: 6,
    qi: [["Geng", 75] as const, ["Ren", 25] as const, ["Wu", 10] as const],
    clashes: "Yin", harmonizes: "Si", harmony_element: "Water",
    harms: "Hai", harm_role: "victim",
    destroys: null,
    three_combo: ["Shen", "Zi", "Chen", "Water"] as const,
    season_combo: ["Shen", "You", "Xu", "Metal"] as const,
    punishment_group: ["Yin", "Si", "Shen", "shi"] as const,
    self_punishment: false,
    // Autumn (Metal rules): Metal=旺, Water=相, Earth=休, Fire=囚, Wood=死
    element_states: { Wood: "Dead", Fire: "Trapped", Earth: "Resting", Metal: "Prosperous", Water: "Strengthening" },
  },
  You: {
    index: 9, chinese: "酉", element: "Metal", polarity: "Yin",
    animal: "Rooster", color: "#e6e8f7", month: 8, season: "Autumn",
    dong_gong_index: 7,
    qi: [["Xin", 100] as const],
    clashes: "Mao", harmonizes: "Chen", harmony_element: "Metal",
    harms: "Xu", harm_role: "victim",
    destroys: "Zi",
    three_combo: ["Si", "You", "Chou", "Metal"] as const,
    season_combo: ["Shen", "You", "Xu", "Metal"] as const,
    self_punishment: true,
    self_punishment_nature: "Metal Rooster - perfectionism leads to self-criticism",
    // Autumn (Metal rules): Metal=旺, Water=相, Earth=休, Fire=囚, Wood=死
    element_states: { Wood: "Dead", Fire: "Trapped", Earth: "Resting", Metal: "Prosperous", Water: "Strengthening" },
  },
  Xu: {
    index: 10, chinese: "戌", element: "Earth", polarity: "Yang",
    animal: "Dog", color: "#e6ceb7", month: 9, season: "Autumn",
    dong_gong_index: 8,
    qi: [["Wu", 75] as const, ["Xin", 25] as const, ["Ding", 10] as const],
    clashes: "Chen", harmonizes: "Mao", harmony_element: "Fire",
    harms: "You", harm_role: "controller",
    destroys: "Wei",
    three_combo: ["Yin", "Wu", "Xu", "Fire"] as const,
    season_combo: ["Shen", "You", "Xu", "Metal"] as const,
    punishment_group: ["Chou", "Wei", "Xu", "wu_li"] as const,
    self_punishment: false,
    is_storage: true, stored_element: "Fire", stored_stem: "Ding", opener: "Chen",
    // Earth* season (Earth rules): Earth=旺(Wang), Metal=相(Xiang), Fire=休(Xiu), Wood=囚(Qiu), Water=死(Si)
    element_states: { Wood: "Trapped", Fire: "Resting", Earth: "Prosperous", Metal: "Strengthening", Water: "Dead" },
  },
  Hai: {
    index: 11, chinese: "亥", element: "Water", polarity: "Yin",
    animal: "Pig", color: "#e0e9ff", month: 10, season: "Winter",
    dong_gong_index: 9,
    qi: [["Ren", 80] as const, ["Jia", 20] as const],
    clashes: "Si", harmonizes: "Yin", harmony_element: "Wood",
    harms: "Shen", harm_role: "controller",
    destroys: null,
    three_combo: ["Hai", "Mao", "Wei", "Wood"] as const,
    season_combo: ["Hai", "Zi", "Chou", "Water"] as const,
    self_punishment: true,
    self_punishment_nature: "Water Pig - indulgence leads to self-harm",
    // Winter (Water rules): Water=旺, Wood=相(Xiang), Metal=休, Earth=囚, Fire=死
    element_states: { Wood: "Strengthening", Fire: "Dead", Earth: "Trapped", Metal: "Resting", Water: "Prosperous" },
  },
} as const satisfies Record<BranchName, BranchData>;
