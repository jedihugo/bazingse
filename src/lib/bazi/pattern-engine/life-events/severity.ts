
// =============================================================================
// SEVERITY CALCULATION ENGINE
// =============================================================================
// Calculates life event severity from pattern matches, seasonal states,
// pillar positions, and Day Master relevance.
// Ported from api/library/pattern_engine/life_events/severity.py
// =============================================================================

import {
  LifeDomain,
  Severity as SeverityLevel,
  TCM_ORGANS,
} from './taxonomy';

// =============================================================================
// SEVERITY MULTIPLIERS
// =============================================================================

export const DISTANCE_MULTIPLIERS: Record<number, number> = {
  0: 1.0,
  1: 0.85,
  2: 0.70,
  3: 0.55,
  4: 0.45,
};

export const SEASONAL_STATE_MULTIPLIERS: Record<string, number> = {
  "Prosperous": 0.6,
  "Strengthening": 0.8,
  "Resting": 1.0,
  "Trapped": 1.4,
  "Dead": 1.8,
};

export const PILLAR_POSITION_MULTIPLIERS: Record<string, number> = {
  year: 1.0,
  month: 1.2,
  day: 1.5,
  hour: 1.0,
};

const POSITION_TO_PILLAR: Record<number, string> = {
  0: "hour",
  1: "day",
  2: "month",
  3: "year",
  4: "10yl",
  5: "annual",
  6: "monthly",
  7: "daily",
  8: "hourly",
};

export const PATTERN_CATEGORY_WEIGHTS: Record<string, number> = {
  punishment: 1.0,
  clash: 0.9,
  harm: 0.7,
  destruction: 0.5,
  stem_conflict: 0.6,
  three_meetings: 1.0,
  three_combinations: 0.9,
  six_harmonies: 0.7,
  half_meetings: 0.5,
  half_combinations: 0.4,
  arched_combinations: 0.3,
  stem_combination: 0.8,
};


// =============================================================================
// SEVERITY CALCULATION
// =============================================================================

export interface SeverityResult {
  readonly raw_score: number;
  readonly normalized_score: number;
  readonly severity_level: SeverityLevel;
  readonly contributing_factors: Record<string, any>;
  readonly explanation: string;
}

export function calculatePatternSeverity(
  patternId: string,
  patternCategory: string,
  distance: number,
  seasonalState: string,
  pillarPosition: number,
  daymasterElement: string,
  patternElement: string | null = null,
  isTransformed: boolean = false,
): SeverityResult {
  const factors: Record<string, number> = {};

  // Base weight from pattern category
  const categoryKey = patternCategory.toLowerCase();
  const baseWeight = PATTERN_CATEGORY_WEIGHTS[categoryKey] ?? 0.5;
  factors["base_weight"] = baseWeight;

  // Distance multiplier
  const distanceMult = DISTANCE_MULTIPLIERS[distance] ?? 0.4;
  factors["distance_mult"] = distanceMult;

  // Seasonal state multiplier
  const seasonalMult = SEASONAL_STATE_MULTIPLIERS[seasonalState] ?? 1.0;
  factors["seasonal_mult"] = seasonalMult;

  // Pillar position multiplier
  const pillarName = POSITION_TO_PILLAR[pillarPosition] ?? "year";
  const pillarMult = PILLAR_POSITION_MULTIPLIERS[pillarName] ?? 1.0;
  factors["pillar_mult"] = pillarMult;

  // Day Master relevance
  let dmMult = 1.0;
  if (patternElement) {
    if (patternElement === daymasterElement) {
      dmMult = 1.5;
    } else if (elementsRelated(patternElement, daymasterElement)) {
      dmMult = 1.2;
    }
  }
  factors["dm_relevance"] = dmMult;

  // Transformation bonus
  const transformBonus = isTransformed ? 1.3 : 1.0;
  factors["transform_bonus"] = transformBonus;

  // Calculate raw score
  const rawScore =
    baseWeight *
    distanceMult *
    seasonalMult *
    pillarMult *
    dmMult *
    transformBonus *
    10;

  // Normalize to 0-100
  const normalized = Math.min(100, (rawScore / 30) * 100);

  // Determine severity level
  let level: SeverityLevel;
  if (normalized >= 70) {
    level = SeverityLevel.CRITICAL;
  } else if (normalized >= 50) {
    level = SeverityLevel.MAJOR;
  } else if (normalized >= 30) {
    level = SeverityLevel.MODERATE;
  } else {
    level = SeverityLevel.MINOR;
  }

  // Generate explanation
  const explanation = generateSeverityExplanation(
    patternId, level, factors, seasonalState, pillarName
  );

  return {
    raw_score: Math.round(rawScore * 100) / 100,
    normalized_score: Math.round(normalized * 10) / 10,
    severity_level: level,
    contributing_factors: factors,
    explanation,
  };
}


export function calculateCompoundSeverity(
  patternResults: SeverityResult[],
  domain: LifeDomain,
): SeverityResult {
  if (patternResults.length === 0) {
    return {
      raw_score: 0,
      normalized_score: 0,
      severity_level: SeverityLevel.MINOR,
      contributing_factors: {},
      explanation: "No patterns detected",
    };
  }

  // Sum individual scores
  const totalRaw = patternResults.reduce((sum, r) => sum + r.raw_score, 0);

  // Apply compound bonus (+25% per additional pattern)
  const patternCount = patternResults.length;
  const compoundMult = 1.0 + (patternCount - 1) * 0.25;

  const compoundedRaw = totalRaw * compoundMult;

  // Normalize
  const normalized = Math.min(100, (compoundedRaw / 50) * 100);

  // Determine level
  let level: SeverityLevel;
  if (normalized >= 70) {
    level = SeverityLevel.CRITICAL;
  } else if (normalized >= 50) {
    level = SeverityLevel.MAJOR;
  } else if (normalized >= 30) {
    level = SeverityLevel.MODERATE;
  } else {
    level = SeverityLevel.MINOR;
  }

  const factors: Record<string, any> = {
    pattern_count: patternCount,
    compound_multiplier: compoundMult,
    individual_scores: patternResults.map((r) => r.raw_score),
  };

  const explanation =
    `${patternCount} patterns converge affecting ${domain} domain. ` +
    `Combined severity: ${level}.`;

  return {
    raw_score: Math.round(compoundedRaw * 100) / 100,
    normalized_score: Math.round(normalized * 10) / 10,
    severity_level: level,
    contributing_factors: factors,
    explanation,
  };
}


// =============================================================================
// DOMAIN-SPECIFIC SEVERITY
// =============================================================================

export function calculateHealthSeverity(
  patternResults: SeverityResult[],
  affectedElements: Set<string>,
  seasonalStates: Record<string, string>,
  daymasterElement: string,
): Record<string, any> {
  const baseResult = calculateCompoundSeverity(patternResults, LifeDomain.HEALTH);

  // Find affected organs
  const affectedOrgans: Record<string, any>[] = [];
  for (const element of affectedElements) {
    const organ = TCM_ORGANS[element];
    if (organ) {
      const organSeverity = seasonalStates[element] ?? "Resting";
      affectedOrgans.push({
        element,
        zang: organ.zang_organ,
        fu: organ.fu_organ,
        chinese_zang: organ.chinese_zang,
        chinese_fu: organ.chinese_fu,
        body_parts: [...organ.body_parts],
        emotion: organ.emotion,
        seasonal_state: organSeverity,
        vulnerability: SEASONAL_STATE_MULTIPLIERS[organSeverity] ?? 1.0,
      });
    }
  }

  // Sort by vulnerability (higher = more at risk)
  affectedOrgans.sort((a, b) => b.vulnerability - a.vulnerability);

  return {
    severity_result: baseResult,
    affected_organs: affectedOrgans,
    most_vulnerable: affectedOrgans.length > 0 ? affectedOrgans[0] : null,
    recommendation: generateHealthRecommendation(
      affectedOrgans, baseResult.severity_level
    ),
  };
}

export function calculateWealthSeverity(
  patternResults: SeverityResult[],
  wealthElement: string,
  seasonalState: string,
): Record<string, any> {
  const baseResult = calculateCompoundSeverity(patternResults, LifeDomain.WEALTH);

  const wealthVulnerability = SEASONAL_STATE_MULTIPLIERS[seasonalState] ?? 1.0;
  const adjustedScore = baseResult.normalized_score * wealthVulnerability;

  return {
    severity_result: baseResult,
    wealth_element: wealthElement,
    wealth_seasonal_state: seasonalState,
    adjusted_score: Math.round(adjustedScore * 10) / 10,
    recommendation: generateWealthRecommendation(
      baseResult.severity_level, seasonalState
    ),
  };
}


// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function elementsRelated(elem1: string, elem2: string): boolean {
  const RELATIONS: Record<string, Set<string>> = {
    Wood: new Set(["Fire", "Earth"]),
    Fire: new Set(["Earth", "Metal"]),
    Earth: new Set(["Metal", "Water"]),
    Metal: new Set(["Water", "Wood"]),
    Water: new Set(["Wood", "Fire"]),
  };
  return RELATIONS[elem1]?.has(elem2) ?? false;
}

function generateSeverityExplanation(
  patternId: string,
  level: SeverityLevel,
  factors: Record<string, number>,
  seasonalState: string,
  pillarName: string,
): string {
  const parts: string[] = [];

  // Pattern identification
  const patternType = patternId.includes("~")
    ? patternId.split("~")[0]
    : patternId;
  parts.push(`${patternType} pattern detected`);

  // Severity level
  const levelText: Record<string, string> = {
    [SeverityLevel.MINOR]: "minor impact",
    [SeverityLevel.MODERATE]: "moderate impact",
    [SeverityLevel.MAJOR]: "significant impact",
    [SeverityLevel.CRITICAL]: "critical impact",
  };
  parts.push(levelText[level] ?? "some impact");

  // Key factors
  if ((factors["seasonal_mult"] ?? 1.0) > 1.2) {
    parts.push(`amplified by ${seasonalState} seasonal state`);
  }

  if ((factors["dm_relevance"] ?? 1.0) > 1.2) {
    parts.push("directly affecting Day Master");
  }

  if (pillarName === "day") {
    parts.push("in personal Day pillar");
  } else if (pillarName === "month") {
    parts.push("in career Month pillar");
  }

  return parts.join(". ") + ".";
}

function generateHealthRecommendation(
  affectedOrgans: Record<string, any>[],
  severity: SeverityLevel,
): string {
  if (affectedOrgans.length === 0) {
    return "No specific organ vulnerability detected.";
  }

  const primary = affectedOrgans[0];
  const organ = primary["zang"] as string;
  const element = primary["element"] as string;

  const recommendations: Record<string, string> = {
    Wood: `Support ${organ} through gentle exercise, avoid anger, eat green vegetables`,
    Fire: `Protect ${organ} through adequate rest, manage anxiety, avoid excessive heat`,
    Earth: `Strengthen ${organ} through regular meals, reduce worry, avoid dampness`,
    Metal: `Support ${organ} through breathing exercises, process grief, protect from cold`,
    Water: `Nourish ${organ} through adequate hydration, manage fear, get sufficient rest`,
  };

  const baseRec = recommendations[element] ?? `Support ${organ} function`;

  if (severity === SeverityLevel.MAJOR || severity === SeverityLevel.CRITICAL) {
    return `IMPORTANT: ${baseRec}. Consider consulting a healthcare provider.`;
  }

  return baseRec;
}

function generateWealthRecommendation(
  severity: SeverityLevel,
  _seasonalState: string,
): string {
  if (severity === SeverityLevel.CRITICAL) {
    return "High financial volatility expected. Avoid major investments. Preserve capital.";
  } else if (severity === SeverityLevel.MAJOR) {
    return "Financial caution advised. Review investments and reduce risk exposure.";
  } else if (severity === SeverityLevel.MODERATE) {
    return "Minor financial fluctuations possible. Maintain diversified portfolio.";
  }
  return "Financial outlook stable. Normal business operations can continue.";
}
