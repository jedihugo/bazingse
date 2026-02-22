import 'server-only';

// =============================================================================
// PATTERN ENGINE MODULE - Barrel Export
// =============================================================================

// Pattern Spec (types + enums)
export {
  PatternCategory,
  PunishmentType,
  SeasonalState,
  LifeDomain,
  NodeType,
  PillarType,
  BadgeType,
  createBranchFilter,
  createStemFilter,
  createElementFilter,
} from './pattern-spec';
export type {
  NodeFilter,
  SpatialRule,
  TemporalRule,
  TransformSpec,
  QiEffect,
  PillarMeaning,
  EventMapping,
  PatternSpec,
  PatternMatch,
} from './pattern-spec';

// Pattern Registry
export {
  PatternRegistryError,
  DuplicatePatternError,
  CircularDependencyError,
  MissingDependencyError,
  ContradictionError,
  DependencyGraph,
  PatternRegistry,
  getGlobalRegistry,
  resetGlobalRegistry,
} from './pattern-registry';

// Branch Combinations
export {
  THREE_MEETINGS_PATTERNS,
  THREE_COMBINATIONS_PATTERNS,
  SIX_HARMONIES_PATTERNS,
  HALF_MEETINGS_PATTERNS,
  HALF_COMBINATIONS_PATTERNS,
  ARCHED_COMBINATIONS_PATTERNS,
  ALL_BRANCH_COMBINATION_PATTERNS,
  getAllBranchCombinationPatterns,
} from './patterns/branch-combinations';

// Branch Conflicts
export {
  CLASHES_PATTERNS,
  PUNISHMENTS_PATTERNS,
  HARMS_PATTERNS,
  DESTRUCTION_PATTERNS,
  ALL_BRANCH_CONFLICT_PATTERNS,
  getAllBranchConflictPatterns,
} from './patterns/branch-conflicts';

// Stem Patterns
export {
  STEM_COMBINATIONS_PATTERNS,
  STEM_CONFLICTS_PATTERNS,
  ALL_STEM_PATTERNS,
  getAllStemPatterns,
} from './patterns/stem-patterns';

// Special Stars
export {
  KONG_WANG_LOOKUP,
  GUI_REN_LOOKUP,
  TAO_HUA_LOOKUP,
  YI_MA_LOOKUP,
  YANG_REN_LOOKUP,
  LU_SHEN_LOOKUP,
  HUA_GAI_LOOKUP,
  GU_CHEN_GUA_SU_LOOKUP,
  KONG_WANG_PATTERNS,
  GUI_REN_PATTERNS,
  TAO_HUA_PATTERNS,
  YI_MA_PATTERNS,
  YANG_REN_PATTERNS,
  LU_SHEN_PATTERNS,
  HUA_GAI_PATTERNS,
  GU_CHEN_PATTERNS,
  GUA_SU_PATTERNS,
  ALL_SPECIAL_STAR_PATTERNS,
  getAllSpecialStarPatterns,
  getSpecialStarsForDayMaster,
  getSpecialStarsForYearBranch,
} from './patterns/special-stars';

// Life Events - Taxonomy
export {
  LifeDomain as EventLifeDomain,
  Sentiment,
  Severity,
  TCM_ORGANS as EVENT_TCM_ORGANS,
  HEALTH_EVENTS,
  WEALTH_EVENTS,
  CAREER_EVENTS,
  RELATIONSHIP_EVENTS,
  EDUCATION_EVENTS,
  FAMILY_EVENTS,
  LEGAL_EVENTS,
  TRAVEL_EVENTS,
  ALL_EVENT_TYPES,
  getEventsByDomain,
  getEventsByElement,
  getEventStatistics,
} from './life-events/taxonomy';
export type {
  TCMOrganSystem,
  EventType,
} from './life-events/taxonomy';

// Life Events - Severity
export {
  DISTANCE_MULTIPLIERS,
  SEASONAL_STATE_MULTIPLIERS,
  PILLAR_POSITION_MULTIPLIERS,
  PATTERN_CATEGORY_WEIGHTS,
  calculatePatternSeverity,
  calculateCompoundSeverity,
  calculateHealthSeverity,
  calculateWealthSeverity,
} from './life-events/severity';
export type { SeverityResult } from './life-events/severity';

// Integration
export {
  PatternEngineAnalyzer,
  getPatternAnalyzer,
  analyzeWithPatternEngine,
  parseInteractionId,
} from './integration';
export type { EnhancedPatternMatch } from './integration';
