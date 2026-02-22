import 'server-only';

// =============================================================================
// SCORING SYSTEM - FORMULA-BASED
// =============================================================================
// Define multipliers for distance-based scoring

export const DISTANCE_MULTIPLIERS = {
  three_branch: {  // For THREE_MEETINGS and THREE_COMBINATIONS
    "2": 1.0,      // Three consecutive nodes (best)
    "3": 0.786,
    "4": 0.618,
    "5": 0.500,
    "6": 0.382,
    "7": 0.236,
  },
  two_branch: {  // For all other branch interactions
    "1": 1.0,      // Gap = 1 (adjacent pillars, luck-natal)
    "2": 0.618,    // Gap = 2
    "3": 0.382,    // Gap = 3
    "4": 0.236,    // Gap = 4 (cross-layer at gap=3)
  },
} as const;

export type PatternType = keyof typeof DISTANCE_MULTIPLIERS;

// Base scores for each interaction type
// POSITIVE: p = combined (detected), q = transformed (fully activated)
// NEGATIVE: p = impact (initial conflict), q = severity (intensified conflict)
export const BASE_SCORES = {
  // Positive Interactions (supportive, generative)
  THREE_MEETINGS: { combined: 35, transformed: 61.8 },
  THREE_COMBINATIONS: { combined: 25, transformed: 45 },
  HALF_MEETINGS: { combined: 20, transformed: 40 },
  STEM_COMBINATIONS: { combined: 19, transformed: 38 },
  SIX_HARMONIES: { combined: 18, transformed: 35 },
  ARCHED_COMBINATIONS: { combined: 12, transformed: 25 },

  // Negative Interactions (conflicting, destructive)
  CLASHES_OPPOSITE: { damage: 38 },  // Opposite elements: asymmetric (victim 1.0, controller 0.618)
  CLASHES_SAME: { damage: 38 },      // Same element: equal mutual damage
  PUNISHMENTS_3NODE: { damage: 38 },  // 3-node: equal 1:1:1, ELEVATED severity
  STEM_CONFLICTS: { damage: 35 },    // HS asymmetric (victim 1.0, controller 0.618)
  HARMS: { damage: 20 },             // EB asymmetric (victim 1.0, controller 0.618)
  DESTRUCTION_OPPOSITE: { damage: 20 }, // Opposite elements: asymmetric, distance 0 only
  DESTRUCTION_SAME: { damage: 20 },     // Same element: equal mutual, distance 0 only
  PUNISHMENTS_2NODE: { damage: 16 },    // 2-node: asymmetric 0.618:1 (less than HARMS)
} as const;

/**
 * Generate scoring dictionary with distance multipliers applied.
 *
 * Formula: score = base_score * multiplier
 */
export function generateScoring(
  base1: number,
  base2: number,
  patternType: PatternType,
  state1 = "combined",
  state2 = "transformed",
): Record<string, Record<string, number>> {
  const multipliers = DISTANCE_MULTIPLIERS[patternType];

  const scoring: Record<string, Record<string, number>> = {
    [state1]: {},
    [state2]: {},
  };

  for (const [distanceKey, multiplier] of Object.entries(multipliers)) {
    scoring[state1][distanceKey] = Math.round(base1 * multiplier);
    scoring[state2][distanceKey] = Math.round(base2 * multiplier);
  }

  return scoring;
}

/**
 * Generate simple scoring with only distance decay (no states).
 * Used for mutual/equal damage patterns like CLASHES.
 */
export function generateSingleScoring(
  base: number,
  patternType: PatternType,
): Record<string, number> {
  const multipliers = DISTANCE_MULTIPLIERS[patternType];
  const scoring: Record<string, number> = {};

  for (const [distanceKey, multiplier] of Object.entries(multipliers)) {
    scoring[distanceKey] = Math.round(base * multiplier);
  }

  return scoring;
}

/**
 * Generate asymmetric scoring for controller-victim relationships.
 * Used for STEM_CONFLICTS where controller expends less energy than victim suffers.
 */
export function generateAsymmetricScoring(
  base: number,
  patternType: PatternType,
  ratio = 0.618,
): { victim: Record<string, number>; controller: Record<string, number> } {
  const multipliers = DISTANCE_MULTIPLIERS[patternType];

  const scoring = {
    victim: {} as Record<string, number>,
    controller: {} as Record<string, number>,
  };

  for (const [distanceKey, multiplier] of Object.entries(multipliers)) {
    scoring.victim[distanceKey] = Math.round(base * multiplier);
    scoring.controller[distanceKey] = Math.round(base * ratio * multiplier);
  }

  return scoring;
}
