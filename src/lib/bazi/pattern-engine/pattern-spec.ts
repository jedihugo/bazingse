
// =============================================================================
// PATTERN SPECIFICATION TYPES
// =============================================================================
// Core types for the declarative pattern engine.
// Python frozen dataclasses -> TypeScript interfaces.
// Ported from api/library/pattern_engine/pattern_spec.py
// =============================================================================

// ---------------------------------------------------------------------------
// Enums
// ---------------------------------------------------------------------------

export enum PatternCategory {
  THREE_MEETINGS = "three_meetings",
  THREE_COMBINATIONS = "three_combinations",
  SIX_HARMONIES = "six_harmonies",
  HALF_MEETINGS = "half_meetings",
  HALF_COMBINATIONS = "half_combinations",
  ARCHED_COMBINATIONS = "arched_combinations",
  STEM_COMBINATION = "stem_combination",
  CLASH = "clash",
  PUNISHMENT = "punishment",
  HARM = "harm",
  DESTRUCTION = "destruction",
  STEM_CONFLICT = "stem_conflict",
  KONG_WANG = "kong_wang",
  GUI_REN = "gui_ren",
  TAO_HUA = "tao_hua",
  YI_MA = "yi_ma",
  YANG_REN = "yang_ren",
  LU_SHEN = "lu_shen",
  HUA_GAI = "hua_gai",
  GU_CHEN = "gu_chen",
  GUA_SU = "gua_su",
}

export enum PunishmentType {
  SHI_XING = "shi_xing",
  WU_LI_XING = "wu_li_xing",
  EN_XING = "en_xing",
  ZI_XING = "zi_xing",
}

export enum SeasonalState {
  PROSPEROUS = "Prosperous",
  STRENGTHENING = "Strengthening",
  RESTING = "Resting",
  TRAPPED = "Trapped",
  DEAD = "Dead",
}

export enum LifeDomain {
  HEALTH = "health",
  WEALTH = "wealth",
  CAREER = "career",
  RELATIONSHIP = "relationship",
  EDUCATION = "education",
  FAMILY = "family",
  LEGAL = "legal",
  TRAVEL = "travel",
}

export enum NodeType {
  HEAVENLY_STEM = "heavenly_stem",
  EARTHLY_BRANCH = "earthly_branch",
}

export enum PillarType {
  YEAR = "year",
  MONTH = "month",
  DAY = "day",
  HOUR = "hour",
}

export enum BadgeType {
  TRANSFORMATION = "transformation",
  COMBINATION = "combination",
  CLASH = "clash",
  PUNISHMENT = "punishment",
  HARM = "harm",
  DESTRUCTION = "destruction",
  STEM_CONFLICT = "stem_conflict",
}

// ---------------------------------------------------------------------------
// Interfaces (frozen dataclasses -> readonly interfaces)
// ---------------------------------------------------------------------------

export interface NodeFilter {
  readonly branches?: ReadonlySet<string>;
  readonly stems?: ReadonlySet<string>;
  readonly elements?: ReadonlySet<string>;
  readonly node_types: ReadonlySet<NodeType>;
}

export interface SpatialRule {
  readonly max_distance?: number;
  readonly require_adjacent?: boolean;
  readonly require_same_pillar?: boolean;
}

export interface TemporalRule {
  readonly seasonal_states?: ReadonlySet<SeasonalState>;
  readonly excluded_seasons?: ReadonlySet<SeasonalState>;
}

export interface TransformSpec {
  readonly resulting_element: string;
  readonly requires_element_support: boolean;
  readonly supporting_elements: ReadonlySet<string>;
  readonly use_branch_polarity: boolean;
  readonly base_score_multiplier?: number;
}

export interface QiEffect {
  readonly target: string; // "source", "target", "all"
  readonly qi_change: number;
  readonly is_percentage: boolean;
}

export interface PillarMeaning {
  readonly year: string;
  readonly month: string;
  readonly day: string;
  readonly hour: string;
}

export interface EventMapping {
  readonly primary_domains?: ReadonlySet<LifeDomain>;
  readonly positive_events?: ReadonlyArray<[string, string]>;
  readonly negative_events?: ReadonlyArray<[string, string]>;
  readonly domain_sentiment?: ReadonlyArray<[string, string]>;
  readonly pillar_severity_modifiers?: ReadonlyArray<[string, number]>;
}

export interface PatternSpec {
  readonly id: string;
  readonly category: PatternCategory;
  readonly priority: number;
  readonly chinese_name: string;
  readonly english_name: string;
  readonly node_filters: readonly NodeFilter[];
  readonly min_nodes: number;
  readonly max_nodes?: number;
  readonly spatial_rule?: SpatialRule;
  readonly temporal_rule?: TemporalRule;
  readonly transformation?: TransformSpec;
  readonly base_score_combined: number;
  readonly base_score_transformed?: number;
  readonly distance_multipliers: readonly number[];
  readonly qi_effects?: readonly QiEffect[];
  readonly badge_type: BadgeType;
  readonly life_domains: ReadonlySet<LifeDomain>;
  readonly pillar_meanings?: PillarMeaning;
  readonly event_mapping?: EventMapping;
  readonly description: string;
  readonly classical_source?: string;
  readonly severity_formula?: string;
  readonly notes?: string;
}

export interface PatternMatch {
  readonly pattern: PatternSpec;
  readonly matched_nodes: readonly string[];
  readonly score: number;
  readonly is_transformed: boolean;
  readonly distance: number;
}

// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------

export function createBranchFilter(branches: string[]): NodeFilter {
  return {
    branches: new Set(branches),
    node_types: new Set([NodeType.EARTHLY_BRANCH]),
  };
}

export function createStemFilter(stems: string[]): NodeFilter {
  return {
    stems: new Set(stems),
    node_types: new Set([NodeType.HEAVENLY_STEM]),
  };
}

export function createElementFilter(elements: string[]): NodeFilter {
  return {
    elements: new Set(elements),
    node_types: new Set([NodeType.EARTHLY_BRANCH, NodeType.HEAVENLY_STEM]),
  };
}
