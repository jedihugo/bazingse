
// =============================================================================
// BRANCH COMBINATION PATTERNS (Declarative Format)
// =============================================================================
// All positive Earthly Branch combinations expressed as PatternSpecs.
// Ported from api/library/pattern_engine/patterns/branch_combinations.py
// =============================================================================

import {
  type PatternSpec,
  PatternCategory,
  NodeType,
  LifeDomain,
  BadgeType,
} from '../pattern-spec';

// ---------------------------------------------------------------------------
// Helper: create pattern with common defaults
// ---------------------------------------------------------------------------

function branchPattern(overrides: Partial<PatternSpec> & Pick<PatternSpec, 'id' | 'category' | 'priority' | 'chinese_name' | 'english_name' | 'base_score_combined' | 'description'>): PatternSpec {
  return {
    node_filters: [],
    min_nodes: 2,
    distance_multipliers: [1.0, 0.8, 0.6],
    badge_type: BadgeType.COMBINATION,
    life_domains: new Set([LifeDomain.CAREER]),
    ...overrides,
  } as PatternSpec;
}

// ---------------------------------------------------------------------------
// THREE MEETINGS (三會方局)
// ---------------------------------------------------------------------------

export const THREE_MEETINGS_PATTERNS: PatternSpec[] = [
  {
    id: "THREE_MEETINGS~Yin-Mao-Chen~Wood",
    category: PatternCategory.THREE_MEETINGS,
    priority: 100,
    chinese_name: "三會木局",
    english_name: "Spring Wood Meeting",
    node_filters: [{ branches: new Set(["Yin", "Mao", "Chen"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 3,
    transformation: { resulting_element: "Wood", requires_element_support: true, supporting_elements: new Set(["Wood"]), use_branch_polarity: true },
    base_score_combined: 20.0,
    base_score_transformed: 30.0,
    distance_multipliers: [1.0, 0.9, 0.7],
    qi_effects: [{ target: "all", qi_change: 15.0, is_percentage: false }],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.CAREER, LifeDomain.HEALTH, LifeDomain.EDUCATION]),
    pillar_meanings: { year: "Ancestral Wood qi blessing, early growth supported", month: "Career advancement through growth and expansion", day: "Personal transformation, new beginnings", hour: "Children's creativity and growth potential" },
    description: "Spring branches unite creating pure Wood energy - growth and expansion",
    classical_source: "三命通會",
  },
  {
    id: "THREE_MEETINGS~Si-Wu-Wei~Fire",
    category: PatternCategory.THREE_MEETINGS,
    priority: 100,
    chinese_name: "三會火局",
    english_name: "Summer Fire Meeting",
    node_filters: [{ branches: new Set(["Si", "Wu", "Wei"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 3,
    transformation: { resulting_element: "Fire", requires_element_support: true, supporting_elements: new Set(["Fire"]), use_branch_polarity: true },
    base_score_combined: 20.0,
    base_score_transformed: 30.0,
    distance_multipliers: [1.0, 0.9, 0.7],
    qi_effects: [{ target: "all", qi_change: 15.0, is_percentage: false }],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.CAREER, LifeDomain.WEALTH, LifeDomain.RELATIONSHIP]),
    pillar_meanings: { year: "Family reputation and fame, ancestral passion", month: "Public recognition, career breakthrough", day: "Personal charisma, passionate relationships", hour: "Legacy through creativity, children's achievements" },
    description: "Summer branches unite creating pure Fire energy - passion and recognition",
    classical_source: "三命通會",
  },
  {
    id: "THREE_MEETINGS~Shen-You-Xu~Metal",
    category: PatternCategory.THREE_MEETINGS,
    priority: 100,
    chinese_name: "三會金局",
    english_name: "Autumn Metal Meeting",
    node_filters: [{ branches: new Set(["Shen", "You", "Xu"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 3,
    transformation: { resulting_element: "Metal", requires_element_support: true, supporting_elements: new Set(["Metal"]), use_branch_polarity: true },
    base_score_combined: 20.0,
    base_score_transformed: 30.0,
    distance_multipliers: [1.0, 0.9, 0.7],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.WEALTH, LifeDomain.LEGAL, LifeDomain.CAREER]),
    description: "Autumn branches unite creating pure Metal energy - structure and wealth",
    classical_source: "三命通會",
  },
  {
    id: "THREE_MEETINGS~Hai-Zi-Chou~Water",
    category: PatternCategory.THREE_MEETINGS,
    priority: 100,
    chinese_name: "三會水局",
    english_name: "Winter Water Meeting",
    node_filters: [{ branches: new Set(["Hai", "Zi", "Chou"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 3,
    transformation: { resulting_element: "Water", requires_element_support: true, supporting_elements: new Set(["Water"]), use_branch_polarity: true },
    base_score_combined: 20.0,
    base_score_transformed: 30.0,
    distance_multipliers: [1.0, 0.9, 0.7],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.HEALTH, LifeDomain.TRAVEL]),
    description: "Winter branches unite creating pure Water energy - wisdom and flow",
    classical_source: "三命通會",
  },
];

// ---------------------------------------------------------------------------
// THREE COMBINATIONS (三合局)
// ---------------------------------------------------------------------------

export const THREE_COMBINATIONS_PATTERNS: PatternSpec[] = [
  { id: "THREE_COMBINATIONS~Shen-Zi-Chen~Water", category: PatternCategory.THREE_COMBINATIONS, priority: 110, chinese_name: "三合水局", english_name: "Water Triangle", node_filters: [{ branches: new Set(["Shen", "Zi", "Chen"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 3, transformation: { resulting_element: "Water", requires_element_support: true, supporting_elements: new Set(["Water"]), use_branch_polarity: true }, base_score_combined: 18.0, base_score_transformed: 25.0, distance_multipliers: [1.0, 0.85, 0.65], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.CAREER, LifeDomain.TRAVEL]), description: "Triangular Water combination - adaptability and intelligence", classical_source: "三命通會" },
  { id: "THREE_COMBINATIONS~Hai-Mao-Wei~Wood", category: PatternCategory.THREE_COMBINATIONS, priority: 110, chinese_name: "三合木局", english_name: "Wood Triangle", node_filters: [{ branches: new Set(["Hai", "Mao", "Wei"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 3, transformation: { resulting_element: "Wood", requires_element_support: true, supporting_elements: new Set(["Wood"]), use_branch_polarity: true }, base_score_combined: 18.0, base_score_transformed: 25.0, distance_multipliers: [1.0, 0.85, 0.65], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION, LifeDomain.FAMILY]), description: "Triangular Wood combination - growth and benevolence", classical_source: "三命通會" },
  { id: "THREE_COMBINATIONS~Yin-Wu-Xu~Fire", category: PatternCategory.THREE_COMBINATIONS, priority: 110, chinese_name: "三合火局", english_name: "Fire Triangle", node_filters: [{ branches: new Set(["Yin", "Wu", "Xu"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 3, transformation: { resulting_element: "Fire", requires_element_support: true, supporting_elements: new Set(["Fire"]), use_branch_polarity: true }, base_score_combined: 18.0, base_score_transformed: 25.0, distance_multipliers: [1.0, 0.85, 0.65], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.WEALTH]), description: "Triangular Fire combination - passion and fame", classical_source: "三命通會" },
  { id: "THREE_COMBINATIONS~Si-You-Chou~Metal", category: PatternCategory.THREE_COMBINATIONS, priority: 110, chinese_name: "三合金局", english_name: "Metal Triangle", node_filters: [{ branches: new Set(["Si", "You", "Chou"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 3, transformation: { resulting_element: "Metal", requires_element_support: true, supporting_elements: new Set(["Metal"]), use_branch_polarity: true }, base_score_combined: 18.0, base_score_transformed: 25.0, distance_multipliers: [1.0, 0.85, 0.65], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.WEALTH, LifeDomain.LEGAL, LifeDomain.CAREER]), description: "Triangular Metal combination - wealth and integrity", classical_source: "三命通會" },
];

// ---------------------------------------------------------------------------
// SIX HARMONIES (六合)
// ---------------------------------------------------------------------------

export const SIX_HARMONIES_PATTERNS: PatternSpec[] = [
  { id: "SIX_HARMONIES~Zi-Chou~Earth", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "子丑合土", english_name: "Rat-Ox Harmony (Earth)", node_filters: [{ branches: new Set(["Zi", "Chou"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Earth", requires_element_support: true, supporting_elements: new Set(["Earth"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY, LifeDomain.CAREER]), description: "Water meets Earth storage - grounding and stability", classical_source: "三命通會" },
  { id: "SIX_HARMONIES~Yin-Hai~Wood", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "寅亥合木", english_name: "Tiger-Pig Harmony (Wood)", node_filters: [{ branches: new Set(["Yin", "Hai"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Wood", requires_element_support: true, supporting_elements: new Set(["Wood"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION, LifeDomain.CAREER]), description: "Wood Tiger meets Water Pig - nurturing growth", classical_source: "三命通會" },
  { id: "SIX_HARMONIES~Mao-Xu~Fire", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "卯戌合火", english_name: "Rabbit-Dog Harmony (Fire)", node_filters: [{ branches: new Set(["Mao", "Xu"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Fire", requires_element_support: true, supporting_elements: new Set(["Fire"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.CAREER, LifeDomain.WEALTH]), description: "Wood Rabbit meets Earth Dog - creating Fire passion", classical_source: "三命通會" },
  { id: "SIX_HARMONIES~Chen-You~Metal", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "辰酉合金", english_name: "Dragon-Rooster Harmony (Metal)", node_filters: [{ branches: new Set(["Chen", "You"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Metal", requires_element_support: true, supporting_elements: new Set(["Metal"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]), description: "Earth Dragon meets Metal Rooster - refining wealth", classical_source: "三命通會" },
  { id: "SIX_HARMONIES~Si-Shen~Water", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "巳申合水", english_name: "Snake-Monkey Harmony (Water)", node_filters: [{ branches: new Set(["Si", "Shen"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Water", requires_element_support: true, supporting_elements: new Set(["Water"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.TRAVEL, LifeDomain.CAREER]), description: "Fire Snake meets Metal Monkey - generating Water wisdom", classical_source: "三命通會" },
  { id: "SIX_HARMONIES~Wu-Wei~Fire", category: PatternCategory.SIX_HARMONIES, priority: 120, chinese_name: "午未合火", english_name: "Horse-Goat Harmony (Fire)", node_filters: [{ branches: new Set(["Wu", "Wei"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Fire", requires_element_support: true, supporting_elements: new Set(["Fire"]), use_branch_polarity: true }, base_score_combined: 12.0, base_score_transformed: 18.0, distance_multipliers: [1.0, 0.8, 0.6], badge_type: BadgeType.TRANSFORMATION, life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.CAREER, LifeDomain.FAMILY]), description: "Fire Horse meets Earth Goat - sustained warmth", classical_source: "三命通會" },
];

// ---------------------------------------------------------------------------
// HALF MEETINGS (半會) - generated
// ---------------------------------------------------------------------------

export const HALF_MEETINGS_PATTERNS: PatternSpec[] = [
  { id: "HALF_MEETINGS~Hai-Chou~Water", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會水局", english_name: "Half Water Meeting", node_filters: [{ branches: new Set(["Hai", "Chou"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Water", requires_element_support: true, supporting_elements: new Set(["Water"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.TRAVEL]), description: "Partial Winter meeting - Water potential" },
  { id: "HALF_MEETINGS~Yin-Chen~Wood", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會木局", english_name: "Half Wood Meeting (Yin-Chen)", node_filters: [{ branches: new Set(["Yin", "Chen"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Wood", requires_element_support: true, supporting_elements: new Set(["Wood"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION]), description: "Partial Spring meeting - Wood potential" },
  { id: "HALF_MEETINGS~Mao-Chen~Wood", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會木局", english_name: "Half Wood Meeting (Mao-Chen)", node_filters: [{ branches: new Set(["Mao", "Chen"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Wood", requires_element_support: true, supporting_elements: new Set(["Wood"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION]), description: "Partial Spring meeting - Wood potential" },
  { id: "HALF_MEETINGS~Si-Wei~Fire", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會火局", english_name: "Half Fire Meeting", node_filters: [{ branches: new Set(["Si", "Wei"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Fire", requires_element_support: true, supporting_elements: new Set(["Fire"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]), description: "Partial Summer meeting - Fire potential" },
  { id: "HALF_MEETINGS~Shen-Xu~Metal", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會金局", english_name: "Half Metal Meeting (Shen-Xu)", node_filters: [{ branches: new Set(["Shen", "Xu"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Metal", requires_element_support: true, supporting_elements: new Set(["Metal"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]), description: "Partial Autumn meeting - Metal potential" },
  { id: "HALF_MEETINGS~You-Xu~Metal", category: PatternCategory.HALF_MEETINGS, priority: 130, chinese_name: "半會金局", english_name: "Half Metal Meeting (You-Xu)", node_filters: [{ branches: new Set(["You", "Xu"]), node_types: new Set([NodeType.EARTHLY_BRANCH]) }], min_nodes: 2, max_nodes: 2, transformation: { resulting_element: "Metal", requires_element_support: true, supporting_elements: new Set(["Metal"]), use_branch_polarity: true, base_score_multiplier: 0.7 }, base_score_combined: 10.0, base_score_transformed: 14.0, distance_multipliers: [1.0, 0.75, 0.5], badge_type: BadgeType.COMBINATION, life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]), description: "Partial Autumn meeting - Metal potential" },
];

// ---------------------------------------------------------------------------
// HALF COMBINATIONS (半合) - generated
// ---------------------------------------------------------------------------

function generateHalfCombinations(): PatternSpec[] {
  const halfCombos: Array<{ id: string; branches: string[]; element: string }> = [
    { id: "HALF_COMBINATIONS~Shen-Zi~Water", branches: ["Shen", "Zi"], element: "Water" },
    { id: "HALF_COMBINATIONS~Zi-Chen~Water", branches: ["Zi", "Chen"], element: "Water" },
    { id: "HALF_COMBINATIONS~Hai-Mao~Wood", branches: ["Hai", "Mao"], element: "Wood" },
    { id: "HALF_COMBINATIONS~Mao-Wei~Wood", branches: ["Mao", "Wei"], element: "Wood" },
    { id: "HALF_COMBINATIONS~Yin-Wu~Fire", branches: ["Yin", "Wu"], element: "Fire" },
    { id: "HALF_COMBINATIONS~Wu-Xu~Fire", branches: ["Wu", "Xu"], element: "Fire" },
    { id: "HALF_COMBINATIONS~Si-You~Metal", branches: ["Si", "You"], element: "Metal" },
    { id: "HALF_COMBINATIONS~You-Chou~Metal", branches: ["You", "Chou"], element: "Metal" },
  ];

  return halfCombos.map(({ id, branches, element }) => ({
    id,
    category: PatternCategory.HALF_COMBINATIONS,
    priority: 140,
    chinese_name: `半合${element}局`,
    english_name: `Half ${element} Combination`,
    node_filters: [{ branches: new Set(branches), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 2,
    max_nodes: 2,
    transformation: { resulting_element: element, requires_element_support: true, supporting_elements: new Set([element]), use_branch_polarity: true, base_score_multiplier: 0.6 },
    base_score_combined: 8.0,
    base_score_transformed: 12.0,
    distance_multipliers: [1.0, 0.7, 0.5],
    badge_type: BadgeType.COMBINATION,
    life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
    description: `Partial ${element} triangle - incomplete combination`,
  }));
}

export const HALF_COMBINATIONS_PATTERNS = generateHalfCombinations();

// ---------------------------------------------------------------------------
// ARCHED COMBINATIONS (拱合) - generated
// ---------------------------------------------------------------------------

function generateArchedCombinations(): PatternSpec[] {
  const arched: Array<{ id: string; branches: string[]; element: string }> = [
    { id: "ARCHED_COMBINATIONS~Shen-Chen~Water", branches: ["Shen", "Chen"], element: "Water" },
    { id: "ARCHED_COMBINATIONS~Hai-Wei~Wood", branches: ["Hai", "Wei"], element: "Wood" },
    { id: "ARCHED_COMBINATIONS~Yin-Xu~Fire", branches: ["Yin", "Xu"], element: "Fire" },
    { id: "ARCHED_COMBINATIONS~Si-Chou~Metal", branches: ["Si", "Chou"], element: "Metal" },
  ];

  return arched.map(({ id, branches, element }) => ({
    id,
    category: PatternCategory.ARCHED_COMBINATIONS,
    priority: 150,
    chinese_name: `拱合${element}局`,
    english_name: `Arched ${element} Combination`,
    node_filters: [{ branches: new Set(branches), node_types: new Set([NodeType.EARTHLY_BRANCH]) }],
    min_nodes: 2,
    max_nodes: 2,
    transformation: { resulting_element: element, requires_element_support: true, supporting_elements: new Set([element]), use_branch_polarity: true, base_score_multiplier: 0.5 },
    base_score_combined: 6.0,
    base_score_transformed: 9.0,
    distance_multipliers: [1.0, 0.65, 0.4],
    badge_type: BadgeType.COMBINATION,
    life_domains: new Set([LifeDomain.CAREER]),
    description: `Arched ${element} - weakest combination form, missing center`,
  }));
}

export const ARCHED_COMBINATIONS_PATTERNS = generateArchedCombinations();

// ---------------------------------------------------------------------------
// COMBINED EXPORT
// ---------------------------------------------------------------------------

export const ALL_BRANCH_COMBINATION_PATTERNS: PatternSpec[] = [
  ...THREE_MEETINGS_PATTERNS,
  ...THREE_COMBINATIONS_PATTERNS,
  ...SIX_HARMONIES_PATTERNS,
  ...HALF_MEETINGS_PATTERNS,
  ...HALF_COMBINATIONS_PATTERNS,
  ...ARCHED_COMBINATIONS_PATTERNS,
];

export function getAllBranchCombinationPatterns(): PatternSpec[] {
  return [...ALL_BRANCH_COMBINATION_PATTERNS];
}
