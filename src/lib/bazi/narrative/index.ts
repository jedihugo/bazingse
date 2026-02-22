import 'server-only';

// =============================================================================
// NARRATIVE MODULE - Barrel Export
// =============================================================================

// Main entry point
export { generateNarrative } from './interpreter';
export type { NarrativeInput, NarrativeOutput } from './interpreter';
export { NODE_TO_PILLAR, PILLAR_LIFE_AREAS } from './interpreter';

// Templates
export { NARRATIVE_TEMPLATES, ELEMENT_MANIFESTATIONS, PILLAR_CONTEXT } from './templates';
export type { NarrativeTemplate, ElementManifestation } from './templates';

// Priority
export { calculatePriorityScore, prioritizeNarratives, groupNarrativesByCategory } from './priority';
export type { NarrativeEntry } from './priority';

// Modifiers
export {
  applyElementModifiers,
  applyShenShaModifiers,
  getElementBalanceContext,
  stemsToElements,
  determineFavorableElements,
  BALANCE_THRESHOLDS,
  TEN_GODS_FOR_ELEMENT,
  TEN_GODS_EXCESS_MEANING,
  ELEMENT_GENERATES,
  ELEMENT_CONTROLS,
} from './modifiers';
export type { ElementBalanceContext } from './modifiers';

// Remedies
export {
  generateRemedies,
  getQuickRemedies,
  REMEDY_TEMPLATES,
  ELEMENT_REMEDIES,
} from './remedies';
export type { ElementRemedy, RemedyTemplate } from './remedies';

// Localization
export {
  buildNarrativeText,
  getLocalizedTemplate,
  formatPillarReference,
  formatBranchesDisplay,
  formatStemsDisplay,
  SUPPORTED_LOCALES,
  ELEMENT_NAMES,
  STEM_NAMES,
  BRANCH_NAMES,
  SEASONAL_STATES,
  PUNISHMENT_TYPES,
} from './localization';
export type { SupportedLocale } from './localization';

// Chain Engine
export {
  analyzeNodeChain,
  enrichClashWithChainAnalysis,
  buildCombinedNarrative,
  SHEN_SHA_MEANINGS,
  QI_PHASE_MEANINGS,
  STORAGE_BRANCHES,
  DM_TO_WEALTH_STORAGE,
  TEN_GOD_NAMES,
  TEN_GOD_EXCESS_TRAITS,
} from './chain-engine';
export type { ShenShaMeaning, ChainAnalysisResult } from './chain-engine';

// Qi Phase
export {
  getQiPhase,
  getQiPhaseForStem,
  getStorageInfo,
  getAllPhasesForBranch,
  findPhasesInBranch,
  getQiPhaseNarrativeContext,
  QI_PHASE_INFO,
  QI_PHASE_ORDER,
} from './qi-phase';
export type { QiPhaseInfo, QiPhaseName } from './qi-phase';
