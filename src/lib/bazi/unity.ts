import 'server-only';

// =============================================================================
// WU XING COMBAT ENGINE (五行戰鬥引擎)
// =============================================================================
// Core combat system for ALL Wu Xing element interactions.
// This is the foundation for:
// - Pillar Unity: HS<->EB within same pillar (distance=1.0, amplifier=1.0)
// - Cross-pillar interactions (with distance modifier)
// - Combinations/Transformations (生 generation cycle)
// - Clashes/Harms (克 control cycle, amplifier=1.618)
// - Punishments (amplifier varies by severity)

export const WUXING_COMBAT = {
  // Base interaction formula
  ENGAGEMENT_RATE: 0.382,    // phi^2 - interaction_point = min(qi) * 0.382
  SOURCE_RATIO: 0.618,       // Golden ratio phi - source loses 0.618 of interaction
  TARGET_RATIO: 1.0,         // Target loses/gains 1.0 of interaction

  // Amplifiers for special interactions
  AMPLIFIER_CLASH: 1.618,    // Golden ratio phi for clashes (沖)
  AMPLIFIER_HARM: 1.618,     // Golden ratio phi for harms (害)
  AMPLIFIER_NORMAL: 1.0,     // Normal interactions

  // Distance multipliers for qi interactions (Primary Qi + Hidden Stems)
  DISTANCE_MULTIPLIERS: {
    1: 1.0,      // Distance 1: HS <-> Primary Qi (base pillar unity)
    2: 0.618,    // Distance 2: HS <-> Hidden Stem (golden ratio phi)
    3: 0.5,      // Distance 3
    4: 0.382,    // Distance 4 (phi^2)
    5: 0.236,    // Distance 5 (phi^3)
    // Distance > 5: No interaction (returns 0.0)
  } as Record<number, number>,
} as const;

/**
 * Get the distance multiplier for Wu Xing interactions.
 */
export function getDistanceMultiplier(distance: number): number {
  if (distance in WUXING_COMBAT.DISTANCE_MULTIPLIERS) {
    return WUXING_COMBAT.DISTANCE_MULTIPLIERS[distance as keyof typeof WUXING_COMBAT.DISTANCE_MULTIPLIERS];
  }
  // For distances beyond 5, no interaction
  return 0.0;
}

/**
 * Determine if a qi value is Primary Qi or Hidden Stem based on index.
 */
export function getQiType(stemIndex: number): "PRIMARY_QI" | "HIDDEN_STEM" {
  return stemIndex === 0 ? "PRIMARY_QI" : "HIDDEN_STEM";
}

// Backward compatibility alias
export const getHiddenStemPriority = getQiType;

/**
 * Calculate the penalty for qi interactions based on visibility.
 */
export function calculateHiddenPenalty(
  sourceIsHs: boolean,
  sourcePriority: "PRIMARY" | "SECONDARY",
  targetIsHs: boolean,
  targetPriority: "PRIMARY" | "SECONDARY",
): number {
  // HS (Heavenly Stem) interacting with EB qi
  if (sourceIsHs) {
    if (targetPriority === "PRIMARY") return 0;
    return 1;
  }

  if (targetIsHs) {
    if (sourcePriority === "PRIMARY") return 0;
    return 1;
  }

  // Both are EB qi values
  if (sourcePriority === "PRIMARY" && targetPriority === "PRIMARY") return 0;
  if (sourcePriority === "SECONDARY" && targetPriority === "SECONDARY") return 2;
  return 1;
}

/**
 * Generate a 1-liner math formula for UI display.
 */
export function formatInteractionMath(
  sourceQi: number,
  targetQi: number,
  distanceMultiplier: number,
  sourceLoss: number,
  targetChange: number,
  isControl = true,
): string {
  const minQi = Math.min(sourceQi, targetQi);
  const interactionBase = minQi * 0.5;

  let formula: string;
  let result: number;
  if (distanceMultiplier === 1.0) {
    formula = `min(${sourceQi.toFixed(0)},${targetQi.toFixed(0)})\u00d70.5`;
    result = interactionBase;
  } else {
    formula = `min(${sourceQi.toFixed(0)},${targetQi.toFixed(0)})\u00d70.5\u00d7${distanceMultiplier}`;
    result = interactionBase * distanceMultiplier;
  }

  const targetSign = isControl ? "-" : "+";
  return `${formula} = ${result.toFixed(1)} \u2192 -${sourceLoss.toFixed(1)}, ${targetSign}${Math.abs(targetChange).toFixed(1)}`;
}

/**
 * Core Wu Xing combat engine. Calculates qi changes when elements interact.
 */
export function applyWuxingInteraction(
  sourceQi: number,
  targetQi: number,
  distanceModifier = 1.0,
  amplifier = 1.0,
): [number, number] {
  const interactionPoint = Math.min(sourceQi, targetQi) * WUXING_COMBAT.ENGAGEMENT_RATE;
  const effective = interactionPoint * distanceModifier * amplifier;
  const sourceLoss = effective * WUXING_COMBAT.SOURCE_RATIO;
  const targetChange = effective * WUXING_COMBAT.TARGET_RATIO;
  return [sourceLoss, targetChange];
}

export interface ControlResult {
  controller_loss: number;
  controlled_loss: number;
  interaction_point: number;
  effective: number;
  distance_modifier: number;
  amplifier: number;
}

/**
 * Calculate Wu Xing control interaction (克).
 * Both controller and controlled lose qi.
 */
export function calculateWuxingControl(
  controllerQi: number,
  controlledQi: number,
  distance = 0,
  isClash = false,
  isHarm = false,
): ControlResult {
  const distanceMod = getDistanceMultiplier(distance);
  let amplifier: number = WUXING_COMBAT.AMPLIFIER_NORMAL;
  if (isClash || isHarm) {
    amplifier = WUXING_COMBAT.AMPLIFIER_CLASH;
  }

  const [controllerLoss, controlledLoss] = applyWuxingInteraction(
    controllerQi, controlledQi, distanceMod, amplifier,
  );

  return {
    controller_loss: controllerLoss,
    controlled_loss: controlledLoss,
    interaction_point: Math.min(controllerQi, controlledQi) * WUXING_COMBAT.ENGAGEMENT_RATE,
    effective: Math.min(controllerQi, controlledQi) * WUXING_COMBAT.ENGAGEMENT_RATE * distanceMod * amplifier,
    distance_modifier: distanceMod,
    amplifier,
  };
}

export interface GenerationResult {
  producer_loss: number;
  receiver_gain: number;
  interaction_point: number;
  effective: number;
  distance_modifier: number;
  amplifier: number;
}

/**
 * Calculate Wu Xing generation interaction (生).
 * Producer loses qi, receiver gains qi.
 */
export function calculateWuxingGeneration(
  producerQi: number,
  receiverQi: number,
  distance = 0,
): GenerationResult {
  const distanceMod = getDistanceMultiplier(distance);
  const amplifier = WUXING_COMBAT.AMPLIFIER_NORMAL;

  const [producerLoss, receiverGain] = applyWuxingInteraction(
    producerQi, receiverQi, distanceMod, amplifier,
  );

  return {
    producer_loss: producerLoss,
    receiver_gain: receiverGain,
    interaction_point: Math.min(producerQi, receiverQi) * WUXING_COMBAT.ENGAGEMENT_RATE,
    effective: Math.min(producerQi, receiverQi) * WUXING_COMBAT.ENGAGEMENT_RATE * distanceMod * amplifier,
    distance_modifier: distanceMod,
    amplifier,
  };
}

// =============================================================================
// HIDDEN QI INTERACTIONS (藏干相剋)
// =============================================================================

export const HIDDEN_QI_INTERACTIONS = {
  PRIMARY_PRIMARY: 1.0,      // Full interaction between primary Qi
  PRIMARY_SECONDARY: 0.5,    // Half interaction with secondary Qi
  SECONDARY_SECONDARY: 0.25, // Quarter interaction between secondary Qi
  PRIMARY_TERTIARY: 0.30,    // Tertiary qi (余氣) interaction - weaker but present
  SECONDARY_TERTIARY: 0.15,  // Secondary-tertiary cross interaction
  TERTIARY_TERTIARY: 0.10,   // Rare - both nodes have tertiary qi conflict
  damage: {
    damage_factor: 0.15,           // For negative interactions on hidden qi
    tertiary_damage_factor: 0.05,  // Reduced damage for tertiary qi interactions
  },
} as const;
