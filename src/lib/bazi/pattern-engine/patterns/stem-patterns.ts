
// =============================================================================
// HEAVENLY STEM PATTERNS (Declarative Format)
// =============================================================================
// All Heavenly Stem interactions expressed as PatternSpecs.
// Includes: STEM_COMBINATIONS (天干合), STEM_CONFLICTS (天干沖/剋)
// Ported from api/library/pattern_engine/patterns/stem_patterns.py
// =============================================================================

import {
  type PatternSpec,
  PatternCategory,
  NodeType,
  LifeDomain,
  BadgeType,
} from '../pattern-spec';

// =============================================================================
// STEM COMBINATIONS (天干五合) - The Five Stem Pairs
// =============================================================================
// Yang stem combines with Yin stem 5 positions apart.
// Transformation requires supporting element in Earthly Branches.

export const STEM_COMBINATIONS_PATTERNS: PatternSpec[] = [
  // Jia-Ji -> Earth (甲己合土)
  {
    id: "STEM_COMBINATION~Jia-Ji~Earth",
    category: PatternCategory.STEM_COMBINATION,
    priority: 50,
    chinese_name: "甲己合土",
    english_name: "Jia-Ji Combine to Earth",
    node_filters: [
      { stems: new Set(["Jia", "Ji"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    transformation: {
      resulting_element: "Earth",
      requires_element_support: true,
      supporting_elements: new Set(["Earth"]),
      use_branch_polarity: false,
    },
    base_score_combined: 15.0,
    base_score_transformed: 22.0,
    distance_multipliers: [1.0, 0.85, 0.7],
    qi_effects: [
      { target: "all", qi_change: 10.0, is_percentage: false },
    ],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.CAREER, LifeDomain.WEALTH, LifeDomain.FAMILY]),
    pillar_meanings: {
      year: "Grounded family foundation, stable ancestry",
      month: "Career stability through partnerships",
      day: "Stable marriage, grounded self",
      hour: "Children's security and stability",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.CAREER, LifeDomain.FAMILY]),
      positive_events: [
        ["career", "job_new"],
        ["career", "promotion"],
        ["relationship", "marriage"],
        ["wealth", "property_purchase"],
      ],
      domain_sentiment: [
        ["career", "positive"],
        ["family", "positive"],
        ["wealth", "positive"],
      ],
    },
    description: "Wood (Jia) + Earth (Ji) combine to pure Earth - grounding partnership",
    classical_source: "三命通會",
    notes: "Transformation requires Earth in EB (Chou, Chen, Wei, Xu, or Earth-element branches)",
  },

  // Yi-Geng -> Metal (乙庚合金)
  {
    id: "STEM_COMBINATION~Yi-Geng~Metal",
    category: PatternCategory.STEM_COMBINATION,
    priority: 50,
    chinese_name: "乙庚合金",
    english_name: "Yi-Geng Combine to Metal",
    node_filters: [
      { stems: new Set(["Yi", "Geng"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    transformation: {
      resulting_element: "Metal",
      requires_element_support: true,
      supporting_elements: new Set(["Metal"]),
      use_branch_polarity: false,
    },
    base_score_combined: 15.0,
    base_score_transformed: 22.0,
    distance_multipliers: [1.0, 0.85, 0.7],
    qi_effects: [
      { target: "all", qi_change: 10.0, is_percentage: false },
    ],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]),
    pillar_meanings: {
      year: "Wealthy heritage, disciplined upbringing",
      month: "Career through precision and structure",
      day: "Relationship with strong boundaries",
      hour: "Children's financial acumen",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]),
      positive_events: [
        ["wealth", "income_increase"],
        ["wealth", "investment_gain"],
        ["career", "promotion"],
        ["legal", "contract_signed"],
      ],
      domain_sentiment: [
        ["wealth", "positive"],
        ["career", "positive"],
      ],
    },
    description: "Wood (Yi) + Metal (Geng) combine to pure Metal - refinement partnership",
    classical_source: "三命通會",
    notes: "Interesting: Controller (Metal) combines with controlled (Wood)",
  },

  // Bing-Xin -> Water (丙辛合水)
  {
    id: "STEM_COMBINATION~Bing-Xin~Water",
    category: PatternCategory.STEM_COMBINATION,
    priority: 50,
    chinese_name: "丙辛合水",
    english_name: "Bing-Xin Combine to Water",
    node_filters: [
      { stems: new Set(["Bing", "Xin"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    transformation: {
      resulting_element: "Water",
      requires_element_support: true,
      supporting_elements: new Set(["Water"]),
      use_branch_polarity: false,
    },
    base_score_combined: 15.0,
    base_score_transformed: 22.0,
    distance_multipliers: [1.0, 0.85, 0.7],
    qi_effects: [
      { target: "all", qi_change: 10.0, is_percentage: false },
    ],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.CAREER, LifeDomain.TRAVEL]),
    pillar_meanings: {
      year: "Intelligent ancestry, adaptive upbringing",
      month: "Career through wisdom and adaptability",
      day: "Emotionally intelligent partnership",
      hour: "Children's academic success",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.EDUCATION, LifeDomain.CAREER]),
      positive_events: [
        ["education", "graduation"],
        ["education", "certification"],
        ["career", "promotion"],
        ["travel", "relocation_major"],
      ],
      domain_sentiment: [
        ["education", "positive"],
        ["career", "positive"],
      ],
    },
    description: "Fire (Bing) + Metal (Xin) combine to pure Water - wisdom partnership",
    classical_source: "三命通會",
    notes: "Fire melts Metal into flowing Water - transformative combination",
  },

  // Ding-Ren -> Wood (丁壬合木)
  {
    id: "STEM_COMBINATION~Ding-Ren~Wood",
    category: PatternCategory.STEM_COMBINATION,
    priority: 50,
    chinese_name: "丁壬合木",
    english_name: "Ding-Ren Combine to Wood",
    node_filters: [
      { stems: new Set(["Ding", "Ren"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    transformation: {
      resulting_element: "Wood",
      requires_element_support: true,
      supporting_elements: new Set(["Wood"]),
      use_branch_polarity: false,
    },
    base_score_combined: 15.0,
    base_score_transformed: 22.0,
    distance_multipliers: [1.0, 0.85, 0.7],
    qi_effects: [
      { target: "all", qi_change: 10.0, is_percentage: false },
    ],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION, LifeDomain.CAREER]),
    pillar_meanings: {
      year: "Growth-oriented ancestry, nurturing upbringing",
      month: "Career through growth and development",
      day: "Nurturing partnership, growth together",
      hour: "Children's development and education",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.HEALTH, LifeDomain.EDUCATION]),
      positive_events: [
        ["health", "recovery"],
        ["education", "enrollment"],
        ["career", "job_new"],
        ["family", "birth_child"],
      ],
      domain_sentiment: [
        ["health", "positive"],
        ["education", "positive"],
      ],
    },
    description: "Fire (Ding) + Water (Ren) combine to pure Wood - growth partnership",
    classical_source: "三命通會",
    notes: "Water normally controls Fire, but here they unite to produce Wood",
  },

  // Wu-Gui -> Fire (戊癸合火)
  {
    id: "STEM_COMBINATION~Wu-Gui~Fire",
    category: PatternCategory.STEM_COMBINATION,
    priority: 50,
    chinese_name: "戊癸合火",
    english_name: "Wu-Gui Combine to Fire",
    node_filters: [
      { stems: new Set(["Wu", "Gui"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    transformation: {
      resulting_element: "Fire",
      requires_element_support: true,
      supporting_elements: new Set(["Fire"]),
      use_branch_polarity: false,
    },
    base_score_combined: 15.0,
    base_score_transformed: 22.0,
    distance_multipliers: [1.0, 0.85, 0.7],
    qi_effects: [
      { target: "all", qi_change: 10.0, is_percentage: false },
    ],
    badge_type: BadgeType.TRANSFORMATION,
    life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.WEALTH]),
    pillar_meanings: {
      year: "Passionate ancestry, warm family",
      month: "Career recognition, public visibility",
      day: "Passionate marriage, warm relationship",
      hour: "Children's fame and recognition",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
      positive_events: [
        ["career", "recognition"],
        ["career", "promotion"],
        ["relationship", "marriage"],
        ["relationship", "engagement"],
      ],
      domain_sentiment: [
        ["career", "positive"],
        ["relationship", "positive"],
      ],
    },
    description: "Earth (Wu) + Water (Gui) combine to pure Fire - passion partnership",
    classical_source: "三命通會",
    notes: "Earth controls Water, but together they create Fire (wu wei = no obstruction)",
  },
];


// =============================================================================
// STEM CONFLICTS (天干相剋) - Control/Clash Relationships
// =============================================================================
// Same polarity stems in controlling relationship clash.
// Yang controls Yang, Yin controls Yin (same polarity = conflict).

export const STEM_CONFLICTS_PATTERNS: PatternSpec[] = [
  // Jia-Geng Conflict (Wood vs Metal, Yang vs Yang)
  {
    id: "STEM_CONFLICT~Jia-Geng~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "甲庚剋",
    english_name: "Jia-Geng Clash",
    node_filters: [
      { stems: new Set(["Jia", "Geng"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]),
    pillar_meanings: {
      year: "Authority conflicts in childhood",
      month: "Career power struggles",
      day: "Personal will vs external pressure",
      hour: "Children face authority issues",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER]),
      negative_events: [
        ["health", "illness_minor"],
        ["health", "surgery"],
        ["career", "job_loss"],
        ["legal", "lawsuit_filed"],
      ],
      domain_sentiment: [
        ["health", "negative"],
        ["career", "negative"],
      ],
    },
    description: "Yang Metal (Geng) chops Yang Wood (Jia) - direct confrontation",
    classical_source: "三命通會",
    notes: "Both Yang - direct clash. Geng is the controller (victor)",
  },

  // Yi-Xin Conflict (Wood vs Metal, Yin vs Yin)
  {
    id: "STEM_CONFLICT~Yi-Xin~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "乙辛剋",
    english_name: "Yi-Xin Clash",
    node_filters: [
      { stems: new Set(["Yi", "Xin"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
    pillar_meanings: {
      year: "Subtle family cutting remarks",
      month: "Career undermining",
      day: "Relationship criticism",
      hour: "Children's self-criticism",
    },
    description: "Yin Metal (Xin) cuts Yin Wood (Yi) - subtle undermining",
    notes: "Both Yin - indirect, cutting conflict. Less direct than Yang-Yang",
  },

  // Bing-Ren Conflict (Fire vs Water, Yang vs Yang)
  {
    id: "STEM_CONFLICT~Bing-Ren~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "丙壬剋",
    english_name: "Bing-Ren Clash",
    node_filters: [
      { stems: new Set(["Bing", "Ren"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
    pillar_meanings: {
      year: "Emotional chaos in childhood",
      month: "Career passion vs practicality",
      day: "Relationship fire and water",
      hour: "Children's emotional turbulence",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
      negative_events: [
        ["health", "mental_health"],
        ["health", "illness_major"],
        ["relationship", "conflict_partner"],
        ["relationship", "divorce"],
      ],
      domain_sentiment: [
        ["health", "negative"],
        ["relationship", "negative"],
      ],
    },
    description: "Yang Water (Ren) extinguishes Yang Fire (Bing) - emotional clash",
    notes: "Both Yang - dramatic confrontation. Ren controls Bing",
  },

  // Ding-Gui Conflict (Fire vs Water, Yin vs Yin)
  {
    id: "STEM_CONFLICT~Ding-Gui~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "丁癸剋",
    english_name: "Ding-Gui Clash",
    node_filters: [
      { stems: new Set(["Ding", "Gui"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.RELATIONSHIP]),
    pillar_meanings: {
      year: "Subtle emotional dampening",
      month: "Career passion suppressed",
      day: "Relationship warmth cooled",
      hour: "Children's joy dampened",
    },
    description: "Yin Water (Gui) dampens Yin Fire (Ding) - subtle emotional suppression",
    notes: "Both Yin - gentle but persistent dampening",
  },

  // Wu-Jia Conflict (Earth vs Wood, Yang vs Yang)
  {
    id: "STEM_CONFLICT~Jia-Wu~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "甲戊剋",
    english_name: "Jia-Wu Clash",
    node_filters: [
      { stems: new Set(["Jia", "Wu"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.WEALTH, LifeDomain.FAMILY]),
    pillar_meanings: {
      year: "Ancestral property disputes",
      month: "Career territory conflicts",
      day: "Personal boundaries broken",
      hour: "Children's stability threatened",
    },
    description: "Yang Wood (Jia) breaks through Yang Earth (Wu) - boundary conflict",
    notes: "Jia controls Wu. Wood penetrates Earth",
  },

  // Ji-Yi Conflict (Earth vs Wood, Yin vs Yin)
  {
    id: "STEM_CONFLICT~Yi-Ji~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "乙己剋",
    english_name: "Yi-Ji Clash",
    node_filters: [
      { stems: new Set(["Yi", "Ji"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER]),
    pillar_meanings: {
      year: "Subtle family land issues",
      month: "Career niche encroachment",
      day: "Personal space erosion",
      hour: "Children's territory issues",
    },
    description: "Yin Wood (Yi) slowly erodes Yin Earth (Ji) - gradual boundary erosion",
    notes: "Yi controls Ji. Grass slowly covers garden soil",
  },

  // Geng-Bing Conflict (Metal vs Fire, Yang vs Yang)
  {
    id: "STEM_CONFLICT~Bing-Geng~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "丙庚剋",
    english_name: "Bing-Geng Clash",
    node_filters: [
      { stems: new Set(["Bing", "Geng"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER, LifeDomain.HEALTH]),
    pillar_meanings: {
      year: "Family wealth melted",
      month: "Career structure destroyed",
      day: "Personal discipline burned",
      hour: "Children's resources consumed",
    },
    event_mapping: {
      primary_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]),
      negative_events: [
        ["wealth", "investment_loss"],
        ["wealth", "income_decrease"],
        ["career", "job_loss"],
      ],
    },
    description: "Yang Fire (Bing) melts Yang Metal (Geng) - structure destroyed",
    notes: "Bing controls Geng. Sun melts ore",
  },

  // Xin-Ding Conflict (Metal vs Fire, Yin vs Yin)
  {
    id: "STEM_CONFLICT~Ding-Xin~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "丁辛剋",
    english_name: "Ding-Xin Clash",
    node_filters: [
      { stems: new Set(["Ding", "Xin"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.WEALTH, LifeDomain.RELATIONSHIP]),
    pillar_meanings: {
      year: "Jewelry/valuables lost in youth",
      month: "Career refinement issues",
      day: "Relationship valuables",
      hour: "Children's precious things",
    },
    description: "Yin Fire (Ding) reshapes Yin Metal (Xin) - precious things transformed",
    notes: "Ding controls Xin. Candle flame reshapes jewelry",
  },

  // Ren-Wu Conflict (Water vs Earth, Yang vs Yang)
  {
    id: "STEM_CONFLICT~Wu-Ren~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "戊壬剋",
    english_name: "Wu-Ren Clash",
    node_filters: [
      { stems: new Set(["Wu", "Ren"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.TRAVEL, LifeDomain.CAREER]),
    pillar_meanings: {
      year: "Learning blocked in youth",
      month: "Career flow obstructed",
      day: "Personal adaptability hampered",
      hour: "Children's education blocked",
    },
    description: "Yang Earth (Wu) dams Yang Water (Ren) - flow obstructed",
    notes: "Wu controls Ren. Dam blocks river",
  },

  // Gui-Ji Conflict (Water vs Earth, Yin vs Yin)
  {
    id: "STEM_CONFLICT~Ji-Gui~",
    category: PatternCategory.STEM_CONFLICT,
    priority: 60,
    chinese_name: "己癸剋",
    english_name: "Ji-Gui Clash",
    node_filters: [
      { stems: new Set(["Ji", "Gui"]), node_types: new Set([NodeType.HEAVENLY_STEM]) },
    ],
    min_nodes: 2,
    max_nodes: 2,
    base_score_combined: 12.0,
    distance_multipliers: [1.0, 0.8, 0.6],
    qi_effects: [
      { target: "source", qi_change: -5.0, is_percentage: false },
      { target: "target", qi_change: -10.0, is_percentage: false },
    ],
    badge_type: BadgeType.STEM_CONFLICT,
    life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.HEALTH]),
    pillar_meanings: {
      year: "Subtle learning absorption",
      month: "Career knowledge absorbed",
      day: "Personal wisdom muddied",
      hour: "Children's learning absorbed",
    },
    description: "Yin Earth (Ji) absorbs Yin Water (Gui) - knowledge absorbed",
    notes: "Ji controls Gui. Garden soil absorbs dew",
  },
];


// =============================================================================
// COMBINED EXPORT
// =============================================================================

export const ALL_STEM_PATTERNS: PatternSpec[] = [
  ...STEM_COMBINATIONS_PATTERNS,
  ...STEM_CONFLICTS_PATTERNS,
];

export function getAllStemPatterns(): PatternSpec[] {
  return [...ALL_STEM_PATTERNS];
}
