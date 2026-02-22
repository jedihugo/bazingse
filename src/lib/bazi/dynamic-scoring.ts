import 'server-only';

// =============================================================================
// DYNAMIC SCORING SYSTEM (動態計分系統)
// =============================================================================
// Core dynamic calculation system for BaZi combinations and conflicts.
// Points are NO LONGER static - calculated based on current qi of interacting nodes.

import { BRANCHES, STEMS, type StemName, type BranchName } from './core';
import { WUXING_COMBAT, getDistanceMultiplier } from './unity';

// =============================================================================
// COMBINATION MULTIPLIERS
// =============================================================================

export const COMBINATION_MULTIPLIERS: Readonly<Record<string, number>> = {
  THREE_MEETINGS: 0.382,
  THREE_COMBINATIONS: 0.238,
  STEM_COMBINATIONS: 0.238,
  HALF_MEETINGS: 0.382,
  SIX_HARMONIES: 0.238,
  ARCHED_COMBINATIONS: 0.146,
};

// Transformation Bonus (successful transformation multiplier)
export const TRANSFORMATION_BONUS = 2.0;

// =============================================================================
// Combination type Chinese names
// =============================================================================

export const COMBINATION_TYPE_CHINESE: Readonly<Record<string, string>> = {
  THREE_MEETINGS: "三會",
  THREE_COMBINATIONS: "三合",
  SIX_HARMONIES: "六合",
  HALF_MEETINGS: "半會",
  ARCHED_COMBINATIONS: "拱合",
  STEM_COMBINATIONS: "天干五合",
};

// =============================================================================
// Types for runtime node objects
// =============================================================================

/** Minimal interface for an element node used in dynamic scoring calculations. */
export interface ElementNodeLike {
  readonly node_id: string;
  readonly node_type: "stem" | "branch";
  readonly value: string;
  readonly elements: Readonly<Record<string, { score: number }>>;
  getTotalScore(): number;
}

// =============================================================================
// PRIMARY QI HELPERS
// =============================================================================

/**
 * Get the PRIMARY QI (本氣) info for a branch.
 * PRIMARY QI is the main energy of the Earthly Branch at index 0.
 */
export function getPrimaryQiInfo(
  branchValue: string,
): [StemName | null, number] {
  if (!(branchValue in BRANCHES)) return [null, 0];

  const qiList = BRANCHES[branchValue as BranchName].qi;
  if (!qiList || (qiList.length as number) === 0) return [null, 0];

  // Primary Qi is index 0
  const primaryStem = qiList[0][0];
  const baseQi = qiList[0][1];

  return [primaryStem, baseQi];
}

// Backward compatibility alias
export const getPrimaryHiddenStemInfo = getPrimaryQiInfo;

/**
 * Get the current qi value for a specific stem from a node.
 */
export function getCurrentQiForStem(
  node: ElementNodeLike,
  stemId: string,
): number {
  if (!(stemId in STEMS)) return 0;

  const stem = STEMS[stemId as StemName];
  const elementKey = `${stem.polarity} ${stem.element}`;

  return node.elements[elementKey]?.score ?? 0;
}

// =============================================================================
// DYNAMIC COMBINATION SCORING
// =============================================================================

export interface QiDetail {
  readonly stemId: string | null;
  readonly qi: number;
  readonly nodeId: string;
}

export interface NodeQiInfo {
  readonly node_id: string;
  readonly branch?: string;
  readonly stem?: string;
  readonly primary_qi_stem?: string;
  readonly primary_qi_stem_chinese?: string;
  readonly primary_qi_element?: string;
  readonly stem_chinese?: string;
  readonly element?: string;
  readonly base_qi?: number;
  readonly current_qi: number;
}

export interface CalculationStep {
  readonly step: number;
  readonly operation: string;
  readonly description?: string;
  readonly formula?: string;
  readonly values?: readonly NodeQiInfo[];
  readonly result: number | readonly number[];
  readonly multiplier?: number;
  readonly multiplier_type?: string;
  readonly explanation?: string;
}

export interface CalculationDetails {
  readonly combination_type: string;
  readonly combination_type_chinese: string;
  readonly is_transformed: boolean;
  readonly transformation_reason: string;
  readonly base_multiplier: number;
  readonly distance_multiplier: number;
  readonly transformation_bonus: number | null;
  readonly participating_nodes: readonly NodeQiInfo[];
  readonly average_qi: number;
  readonly final_score: number;
  readonly steps: readonly CalculationStep[];
  readonly formula_summary: string;
}

/**
 * Calculate dynamic score for a combination based on current node qi.
 */
export function calculateDynamicCombinationScore(
  nodes: readonly ElementNodeLike[],
  combinationType: string,
  isTransformed = false,
  distanceMultiplier = 1.0,
): [number, string, readonly QiDetail[], CalculationDetails] {
  const qiValues: number[] = [];
  const qiDetails: QiDetail[] = [];
  const qiStrings: string[] = [];
  const nodeQiInfo: NodeQiInfo[] = [];

  for (const node of nodes) {
    if (node.node_type === "branch") {
      const [stemId, baseQi] = getPrimaryQiInfo(node.value);
      if (stemId) {
        const qi = getCurrentQiForStem(node, stemId);
        qiValues.push(qi);
        qiDetails.push({ stemId, qi, nodeId: node.node_id });
        qiStrings.push(qi.toFixed(1));
        const stemData = STEMS[stemId as StemName];
        nodeQiInfo.push({
          node_id: node.node_id,
          branch: node.value,
          primary_qi_stem: stemId,
          primary_qi_stem_chinese: stemData?.chinese ?? "?",
          primary_qi_element: stemData?.element ?? "?",
          base_qi: baseQi,
          current_qi: Math.round(qi * 100) / 100,
        });
      }
    } else if (node.node_type === "stem") {
      const qi = node.getTotalScore();
      qiValues.push(qi);
      qiDetails.push({ stemId: node.value, qi, nodeId: node.node_id });
      qiStrings.push(qi.toFixed(1));
      const stemData = STEMS[node.value as StemName];
      nodeQiInfo.push({
        node_id: node.node_id,
        stem: node.value,
        stem_chinese: stemData?.chinese ?? "?",
        element: stemData?.element ?? "?",
        current_qi: Math.round(qi * 100) / 100,
      });
    }
  }

  if (qiValues.length === 0) {
    const emptyDetails: CalculationDetails = {
      combination_type: combinationType,
      combination_type_chinese: COMBINATION_TYPE_CHINESE[combinationType] ?? combinationType,
      is_transformed: isTransformed,
      transformation_reason: "",
      base_multiplier: 0,
      distance_multiplier: distanceMultiplier,
      transformation_bonus: null,
      participating_nodes: [],
      average_qi: 0,
      final_score: 0,
      steps: [],
      formula_summary: "No qi values",
    };
    return [0, "No qi values", [], emptyDetails];
  }

  // Calculate average qi
  const avgQi = qiValues.reduce((a, b) => a + b, 0) / qiValues.length;

  // Get combination multiplier
  const comboMult = COMBINATION_MULTIPLIERS[combinationType] ?? 0.5;

  // Calculate intermediate score
  const afterComboMult = avgQi * comboMult;
  const afterDistance = afterComboMult * distanceMultiplier;

  // Build calculation steps
  const calculationSteps: CalculationStep[] = [];

  calculationSteps.push({
    step: 1,
    operation: "Get Primary Qi from each node",
    description: "Extract the primary qi (本氣) from each participating Earthly Branch",
    values: nodeQiInfo,
    result: qiValues.map((q) => Math.round(q * 100) / 100),
  });

  calculationSteps.push({
    step: 2,
    operation: "Calculate Average",
    formula: `(${qiStrings.join(" + ")}) \u00f7 ${qiValues.length}`,
    description: "Average of all primary qi values",
    result: Math.round(avgQi * 100) / 100,
  });

  calculationSteps.push({
    step: 3,
    operation: "Apply Combination Multiplier",
    formula: `${avgQi.toFixed(2)} \u00d7 ${comboMult}`,
    multiplier: comboMult,
    multiplier_type: combinationType,
    result: Math.round(afterComboMult * 100) / 100,
  });

  if (distanceMultiplier !== 1.0) {
    calculationSteps.push({
      step: 4,
      operation: "Apply Distance Decay",
      formula: `${afterComboMult.toFixed(2)} \u00d7 ${distanceMultiplier}`,
      multiplier: distanceMultiplier,
      explanation: `Distance decay: farther nodes = weaker effect. Multiplier: ${distanceMultiplier}`,
      result: Math.round(afterDistance * 100) / 100,
    });
  }

  // Build formula string and final score
  const qiStr = qiStrings.join(", ");
  let finalScore: number;
  let formula: string;

  if (isTransformed) {
    finalScore = afterDistance * TRANSFORMATION_BONUS;

    calculationSteps.push({
      step: calculationSteps.length + 1,
      operation: "Apply Transformation Bonus",
      formula: `${afterDistance.toFixed(2)} \u00d7 ${TRANSFORMATION_BONUS.toFixed(3)}`,
      multiplier: TRANSFORMATION_BONUS,
      explanation: `Transformation bonus (\u03c6 = Golden Ratio 1.618) - Heavenly Stem supports the transformed element`,
      result: Math.round(finalScore * 100) / 100,
    });

    if (distanceMultiplier !== 1.0) {
      formula = `avg(${qiStr}) \u00d7 ${comboMult} \u00d7 ${distanceMultiplier} \u00d7 ${TRANSFORMATION_BONUS.toFixed(3)} = ${finalScore.toFixed(1)}`;
    } else {
      formula = `avg(${qiStr}) \u00d7 ${comboMult} \u00d7 ${TRANSFORMATION_BONUS.toFixed(3)} = ${finalScore.toFixed(1)}`;
    }
    formula += ` \u2192 +${finalScore.toFixed(1)} (transformed!)`;
  } else {
    finalScore = afterDistance;

    if (distanceMultiplier !== 1.0) {
      formula = `avg(${qiStr}) \u00d7 ${comboMult} \u00d7 ${distanceMultiplier} = ${finalScore.toFixed(1)}`;
    } else {
      formula = `avg(${qiStr}) \u00d7 ${comboMult} = ${finalScore.toFixed(1)}`;
    }
    formula += ` \u2192 +${finalScore.toFixed(1)} (combined)`;
  }

  const calculationDetails: CalculationDetails = {
    combination_type: combinationType,
    combination_type_chinese: COMBINATION_TYPE_CHINESE[combinationType] ?? combinationType,
    is_transformed: isTransformed,
    transformation_reason: isTransformed
      ? "Heavenly Stem element matches transformed element"
      : "No matching Heavenly Stem element for full transformation",
    base_multiplier: comboMult,
    distance_multiplier: distanceMultiplier,
    transformation_bonus: isTransformed ? TRANSFORMATION_BONUS : null,
    participating_nodes: nodeQiInfo,
    average_qi: Math.round(avgQi * 100) / 100,
    final_score: Math.round(finalScore * 100) / 100,
    steps: calculationSteps,
    formula_summary: formula,
  };

  return [Math.round(finalScore * 100) / 100, formula, qiDetails, calculationDetails];
}

// =============================================================================
// DYNAMIC CONFLICT SCORING
// =============================================================================

/**
 * Calculate dynamic score for conflicts using Wu Xing Combat Engine.
 */
export function calculateDynamicConflictScore(
  controllerNode: ElementNodeLike,
  victimNode: ElementNodeLike,
  conflictType = "CONFLICT",
  distance = 1,
  severityMultiplier = 1.0,
  amplifier = 1.0,
): [number, number, string, readonly QiDetail[]] {
  // Get qi values
  let controllerQi: number;
  let controllerStem: string | null;
  if (controllerNode.node_type === "branch") {
    const [stemId] = getPrimaryQiInfo(controllerNode.value);
    controllerQi = stemId ? getCurrentQiForStem(controllerNode, stemId) : 0;
    controllerStem = stemId;
  } else {
    controllerQi = controllerNode.getTotalScore();
    controllerStem = controllerNode.value;
  }

  let victimQi: number;
  let victimStem: string | null;
  if (victimNode.node_type === "branch") {
    const [stemId] = getPrimaryQiInfo(victimNode.value);
    victimQi = stemId ? getCurrentQiForStem(victimNode, stemId) : 0;
    victimStem = stemId;
  } else {
    victimQi = victimNode.getTotalScore();
    victimStem = victimNode.value;
  }

  const qiDetails: QiDetail[] = [
    { stemId: controllerStem, qi: controllerQi, nodeId: controllerNode.node_id },
    { stemId: victimStem, qi: victimQi, nodeId: victimNode.node_id },
  ];

  // Calculate using Wu Xing Combat Engine formula
  const minQi = Math.min(controllerQi, victimQi);
  const distanceMult = distance > 0 ? getDistanceMultiplier(distance) : 1.0;

  // Base interaction
  const interactionPoint = minQi * WUXING_COMBAT.ENGAGEMENT_RATE;
  const effective = interactionPoint * distanceMult * severityMultiplier * amplifier;

  // Asymmetric damage
  const controllerDamage = effective * WUXING_COMBAT.SOURCE_RATIO;
  const victimDamage = effective * WUXING_COMBAT.TARGET_RATIO;

  // Build formula
  let formulaStr = `min(${controllerQi.toFixed(1)}, ${victimQi.toFixed(1)}) x 0.5`;
  if (distanceMult !== 1.0) formulaStr += ` x ${distanceMult}`;
  if (severityMultiplier !== 1.0) formulaStr += ` x ${severityMultiplier.toFixed(2)}`;
  if (amplifier !== 1.0) formulaStr += ` x ${amplifier.toFixed(3)}`;
  formulaStr += ` = ${effective.toFixed(1)} -> -${controllerDamage.toFixed(1)}, -${victimDamage.toFixed(1)}`;

  return [
    Math.round(controllerDamage * 100) / 100,
    Math.round(victimDamage * 100) / 100,
    formulaStr,
    qiDetails,
  ];
}

/**
 * Calculate symmetric damage for conflicts where both sides take equal damage.
 */
export function calculateSymmetricConflictScore(
  node1: ElementNodeLike,
  node2: ElementNodeLike,
  _conflictType = "CONFLICT",
  distance = 1,
  severityMultiplier = 1.0,
): [number, string, readonly QiDetail[]] {
  // Get qi values
  let node1Qi: number;
  let node1Stem: string | null;
  if (node1.node_type === "branch") {
    const [stemId] = getPrimaryQiInfo(node1.value);
    node1Qi = stemId ? getCurrentQiForStem(node1, stemId) : 0;
    node1Stem = stemId;
  } else {
    node1Qi = node1.getTotalScore();
    node1Stem = node1.value;
  }

  let node2Qi: number;
  let node2Stem: string | null;
  if (node2.node_type === "branch") {
    const [stemId] = getPrimaryQiInfo(node2.value);
    node2Qi = stemId ? getCurrentQiForStem(node2, stemId) : 0;
    node2Stem = stemId;
  } else {
    node2Qi = node2.getTotalScore();
    node2Stem = node2.value;
  }

  const qiDetails: QiDetail[] = [
    { stemId: node1Stem, qi: node1Qi, nodeId: node1.node_id },
    { stemId: node2Stem, qi: node2Qi, nodeId: node2.node_id },
  ];

  // Calculate
  const minQi = Math.min(node1Qi, node2Qi);
  const distanceMult = distance > 0 ? getDistanceMultiplier(distance) : 1.0;

  // Symmetric damage
  const interactionPoint = minQi * WUXING_COMBAT.ENGAGEMENT_RATE;
  const damage = interactionPoint * distanceMult * severityMultiplier;

  // Build formula
  let formulaStr = `min(${node1Qi.toFixed(1)}, ${node2Qi.toFixed(1)}) x 0.5`;
  if (distanceMult !== 1.0) formulaStr += ` x ${distanceMult}`;
  if (severityMultiplier !== 1.0) formulaStr += ` x ${severityMultiplier.toFixed(2)}`;
  formulaStr += ` = ${damage.toFixed(1)} -> -${damage.toFixed(1)} (each)`;

  return [Math.round(damage * 100) / 100, formulaStr, qiDetails];
}

// =============================================================================
// NARRATIVE FORMATTERS
// =============================================================================

const PILLAR_MAP: Readonly<Record<string, string>> = {
  y: "Year", m: "Month", d: "Day", h: "Hour",
};

function getNodeName(nodeId: string): string {
  const suffix = nodeId.includes("_") ? nodeId.split("_")[1] : "";
  const pillar = PILLAR_MAP[suffix] ?? suffix.toUpperCase();
  const nodeType = nodeId.startsWith("hs_") ? "HS" : "EB";
  return `${pillar} ${nodeType}`;
}

/**
 * Generate detailed narrative for combination events.
 */
export function formatCombinationNarrative(
  nodeIds: readonly string[],
  combinationType: string,
  pattern: string,
  element: string,
  qiDetails: readonly QiDetail[],
  score: number,
  isTransformed: boolean,
): string {
  const nodeNames = nodeIds.map(getNodeName);

  const qiParts = qiDetails
    .filter((d) => d.stemId)
    .map((d) => {
      const chinese = d.stemId && d.stemId in STEMS
        ? STEMS[d.stemId as StemName].chinese
        : d.stemId;
      return `${d.stemId}(${chinese})=${d.qi.toFixed(1)}`;
    });

  const comboName = combinationType.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
  const multiplier = COMBINATION_MULTIPLIERS[combinationType] ?? 0.5;

  let narrative = `${nodeNames.join(" and ")} formed ${comboName} (${pattern}). `;
  narrative += `Primary qi: ${qiParts.join(", ")}. `;
  narrative += `Calculation: avg x ${multiplier}`;
  if (isTransformed) {
    narrative += ` x ${TRANSFORMATION_BONUS.toFixed(3)} (transformed)`;
  }
  narrative += ` = ${score.toFixed(1)}. `;
  narrative += `Result: +${score.toFixed(1)} ${element} qi added`;
  if (isTransformed) {
    narrative += " (fully transformed!)";
  } else {
    narrative += " (combined)";
  }
  narrative += ".";

  return narrative;
}

/**
 * Generate detailed narrative for conflict events.
 */
export function formatConflictNarrative(
  controllerNodeId: string,
  victimNodeId: string,
  conflictType: string,
  pattern: string,
  qiDetails: readonly QiDetail[],
  controllerDamage: number,
  victimDamage: number,
  severity = "",
): string {
  const controllerName = getNodeName(controllerNodeId);
  const victimName = getNodeName(victimNodeId);

  const qiParts = qiDetails
    .filter((d) => d.stemId)
    .map((d) => {
      const chinese = d.stemId && d.stemId in STEMS
        ? STEMS[d.stemId as StemName].chinese
        : d.stemId;
      const nodeName = getNodeName(d.nodeId);
      return `${d.stemId}(${chinese})@${nodeName}=${d.qi.toFixed(1)}`;
    });

  const conflictName = conflictType.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

  let narrative = `${controllerName} ${conflictName.toLowerCase()}s with ${victimName} (${pattern})`;
  if (severity) narrative += ` [${severity}]`;
  narrative += ". ";
  narrative += `Primary qi: ${qiParts.join(", ")}. `;
  narrative += `Result: Controller lost ${controllerDamage.toFixed(1)}, Victim lost ${victimDamage.toFixed(1)}.`;

  return narrative;
}
