import 'server-only';

// =============================================================================
// COMPREHENSIVE MODULE - Barrel Export
// =============================================================================

// Models
export {
  getPalaceName,
  getPalaceChinese,
} from './models';
export type {
  Pillar,
  TenGodEntry,
  ShenShaResult,
  BranchInteraction,
  StrengthAssessment,
  RedFlag,
  EventPrediction,
  LuckPillarInfo,
  EnvironmentAssessment,
  ChartData,
} from './models';

// Strength (element counting & utilities — scoring moved to wuxing/calculator.ts)
export {
  getSeasonalState,
  getSeasonalMultiplier,
  applySeasonalScaling,
  checkRooting,
  countElements,
  countAllElements,
  countSupportVsDrain,
  adjustElementsForInteractions,
  detectFollowingChart,
  VERDICT_THRESHOLDS,
} from './strength';

// Ten Gods
export {
  TEN_GOD_INFO,
  TEN_GOD_LIFE_MEANING,
  mapAllTenGods,
  classifyTenGodStrength,
  getDominantTenGods,
  getAbsentTenGods,
  checkSpouseStar,
  checkChildrenStar,
  getTenGodElementCounts,
  analyzeTenGodPatterns,
} from './ten-gods';

// Qi Phase Analysis
export {
  TANDEM_EFFECTS,
  analyzeQiPhases,
} from './qi-phase-analysis';

// Spiritual Sensitivity
export {
  assessSpiritualSensitivity,
} from './spiritual-sensitivity';

// Templates
export {
  _pick,
  DM_NATURE,
  STRENGTH_VERDICTS,
  TEN_GOD_INTERPRETATIONS,
  SHEN_SHA_IMPACTS,
  INTERACTION_IMPACTS,
  SEVERITY_LANGUAGE,
  HEALTH_ELEMENT_MAP,
  ELEMENT_REMEDIES,
  LIFE_LESSON_TEMPLATES,
  STRENGTH_EXPLANATION,
  HEALTH_BEHAVIORAL_REMEDIES,
  CONTROL_CYCLE_EXPLANATIONS,
} from './templates';

// Shen Sha
export {
  _xunVoidBranches,
  HONG_LUAN_LOOKUP,
  TIAN_XI_LOOKUP,
  getVoidBranches,
  TAO_HUA_LOOKUP,
  YI_MA_LOOKUP,
  runAllShenSha,
  getPresentShenSha,
  getAbsentCriticalShenSha,
} from './shen-sha';

// Engine
export {
  buildChart,
  analyzeForApi,
  analyze,
} from './engine';

// Wuxing Bridge (ChartData <-> WuxingInput)
export { chartToWuxingInput } from './wuxing-bridge';

// Interactions
export {
  HARMONY_PAIRS,
  THREE_HARMONY_FRAMES,
  DIRECTIONAL_COMBOS,
  detectAllInteractions,
  getNegativeInteractions,
  getPositiveInteractions,
} from './interactions';

// Adapter
export {
  adaptToFrontend,
} from './adapter';

// Predictions
export {
  getAnnualPillar,
  predictMarriageYears,
  predictDivorceYears,
  predictChildrenYears,
  predictCareerYears,
  runAllPredictions,
} from './predictions';

// Report
export {
  generateComprehensiveReport,
} from './report';

// Environment
export {
  assessEnvironment,
} from './environment';
