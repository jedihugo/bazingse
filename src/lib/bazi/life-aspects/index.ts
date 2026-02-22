import 'server-only';

// =============================================================================
// LIFE ASPECTS MODULE - Barrel Export
// =============================================================================

// Base
export {
  NODE_RELATIONSHIPS,
  PILLAR_LIFE_PERIODS,
  TEN_GOD_ASPECT_MAPPING,
  ELEMENT_CONTROLS,
  ELEMENT_GENERATES,
  STEM_TO_ELEMENT,
  ELEMENT_NAMES_L,
  SEASONAL_STATES_L,
  SEVERITY_LABELS,
  OUTLOOK_LABELS,
  ORGAN_SYSTEMS,
  BODY_PARTS,
  stemsToElementTotals,
  getNodeRelationshipContext,
  detectControlImbalances,
  calculateAspectSeverity,
} from './base';
export type { NodeRelationship } from './base';

// Health
export {
  generateHealthAnalysis,
  ELEMENT_ORGANS,
  CONFLICT_HEALTH_WEIGHTS,
  SEASONAL_HEALTH_MODIFIER,
} from './health';
export type { HealthAnalysisResult, OrganMapping } from './health';

// Wealth
export {
  generateWealthAnalysis,
  OPPORTUNITY_WEIGHTS,
  RISK_WEIGHTS,
  PROPERTY_STORAGE_BRANCHES,
  PROPERTY_INDICATORS,
  WEALTH_TEN_GODS,
  WEALTH_INDICATORS,
  DM_WEALTH_ELEMENT,
} from './wealth';
export type { WealthAnalysisResult } from './wealth';

// Learning
export {
  generateLearningAnalysis,
  LEARNING_TEN_GODS,
  LEARNING_INDICATORS,
  DM_RESOURCE_ELEMENT,
  DM_OUTPUT_ELEMENT,
} from './learning';
export type { LearningAnalysisResult } from './learning';

// Ten Gods Detail
export {
  getTenGodForStem,
  analyzeInteractionImpact,
  generateTenGodsDetail,
  TEN_GOD_PILLAR_MEANINGS,
  MEANING_TRANSLATIONS_ID,
} from './ten-gods-detail';
export type { TenGodsDetailResult, PillarMeaningEntry } from './ten-gods-detail';
