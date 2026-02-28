
// =============================================================================
// PATTERN ENGINE INTEGRATION
// =============================================================================
// Bridges the existing BaZi analysis with the new Pattern Engine.
// Provides enhanced pattern detection, severity calculation, and predictions.
// Ported from api/library/pattern_engine/integration.py
// =============================================================================

import type { PatternSpec } from './pattern-spec';
import { PatternCategory, LifeDomain } from './pattern-spec';
import { PatternRegistry, getGlobalRegistry } from './pattern-registry';
import {
  getSpecialStarsForDayMaster,
  getSpecialStarsForYearBranch,
} from './patterns/special-stars';

import {
  type SeverityResult,
  calculatePatternSeverity,
  calculateCompoundSeverity,
  calculateHealthSeverity,
  SEASONAL_STATE_MULTIPLIERS,
} from './life-events/severity';

import {
  LifeDomain as TaxonomyLifeDomain,
  Severity as TaxonomySeverity,
  TCM_ORGANS,
  ALL_EVENT_TYPES,
} from './life-events/taxonomy';

// Forward imports for pattern loading
import { ALL_BRANCH_COMBINATION_PATTERNS } from './patterns/branch-combinations';
import { ALL_BRANCH_CONFLICT_PATTERNS } from './patterns/branch-conflicts';
import { ALL_STEM_PATTERNS } from './patterns/stem-patterns';
import { ALL_SPECIAL_STAR_PATTERNS } from './patterns/special-stars';


// =============================================================================
// PATTERN MATCH RESULT
// =============================================================================

export interface EnhancedPatternMatch {
  readonly pattern_id: string;
  readonly category: string;
  readonly chinese_name: string;
  readonly english_name: string;
  readonly participants: string[];
  readonly distance: number;
  readonly is_transformed: boolean;
  readonly severity: SeverityResult;
  readonly affected_domains: string[];
  readonly pillar_meaning: string;
  readonly event_predictions: Record<string, any>[];
}


// =============================================================================
// INTERACTION TO PATTERN MAPPING
// =============================================================================

const INTERACTION_TYPE_TO_CATEGORY: Record<string, string> = {
  THREE_MEETINGS: "three_meetings",
  THREE_COMBINATIONS: "three_combinations",
  SIX_HARMONIES: "six_harmonies",
  HALF_MEETINGS: "half_meetings",
  HALF_COMBINATIONS: "half_combinations",
  ARCHED_COMBINATIONS: "arched_combinations",
  HS_COMBINATIONS: "stem_combination",
  STEM_COMBINATION: "stem_combination",
  CLASH: "clash",
  CLASHES: "clash",
  PUNISHMENT: "punishment",
  PUNISHMENTS: "punishment",
  HARM: "harm",
  HARMS: "harm",
  DESTRUCTION: "destruction",
  STEM_CONFLICT: "stem_conflict",
  STEM_CONFLICTS: "stem_conflict",
};


export function parseInteractionId(interactionId: string): [string, string[], string] {
  const parts = interactionId.split("~");

  if (parts.length >= 3) {
    return [parts[0], parts[1].split("-"), parts[2]];
  } else if (parts.length === 2) {
    return [parts[0], parts[1].split("-"), ""];
  }
  return [parts[0], [], ""];
}

function constructRegistryPatternId(
  intType: string,
  participants: string[],
  element?: string | null,
  subtype?: string | null,
  trailingTilde: boolean = false,
): string {
  const participantsStr = participants.join("-");

  if (element) {
    return `${intType}~${participantsStr}~${element}`;
  } else if (subtype) {
    return `${intType}~${participantsStr}~${subtype}`;
  } else if (trailingTilde) {
    return `${intType}~${participantsStr}~`;
  }
  return `${intType}~${participantsStr}`;
}

function permutations<T>(arr: T[]): T[][] {
  if (arr.length <= 1) return [arr];
  const result: T[][] = [];
  for (let i = 0; i < arr.length; i++) {
    const rest = [...arr.slice(0, i), ...arr.slice(i + 1)];
    for (const perm of permutations(rest)) {
      result.push([arr[i], ...perm]);
    }
  }
  return result;
}

function findPatternInRegistry(
  registry: PatternRegistry,
  intType: string,
  participants: string[],
  element?: string | null,
  subtype?: string | null,
): PatternSpec | undefined {
  const candidates: string[] = [];

  // 1. Original order (without and with trailing tilde)
  const origId = constructRegistryPatternId(intType, participants, element, subtype);
  candidates.push(origId);
  const origIdTilde = constructRegistryPatternId(intType, participants, element, subtype, true);
  if (!candidates.includes(origIdTilde)) candidates.push(origIdTilde);

  // 2. Reversed for 2-participant patterns
  if (participants.length === 2) {
    const rev = [...participants].reverse();
    const revId = constructRegistryPatternId(intType, rev, element, subtype);
    if (!candidates.includes(revId)) candidates.push(revId);
    const revIdTilde = constructRegistryPatternId(intType, rev, element, subtype, true);
    if (!candidates.includes(revIdTilde)) candidates.push(revIdTilde);
  }

  // 3. All permutations for 3-participant patterns
  if (participants.length === 3) {
    for (const perm of permutations(participants)) {
      const permId = constructRegistryPatternId(intType, perm, element, subtype);
      if (!candidates.includes(permId)) candidates.push(permId);
      const permIdTilde = constructRegistryPatternId(intType, perm, element, subtype, true);
      if (!candidates.includes(permIdTilde)) candidates.push(permIdTilde);
    }
  }

  // Try each candidate
  for (const candidateId of candidates) {
    const pattern = registry.get(candidateId);
    if (pattern) return pattern;
  }

  return undefined;
}

function getPillarNameFromPosition(position: number): string {
  const POSITION_NAMES: Record<number, string> = {
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
  return POSITION_NAMES[position] ?? "unknown";
}


// =============================================================================
// LOAD ALL PATTERNS
// =============================================================================

function loadAllPatterns(registry?: PatternRegistry): PatternRegistry {
  const reg = registry ?? getGlobalRegistry();

  const allPatterns: PatternSpec[] = [
    ...ALL_BRANCH_COMBINATION_PATTERNS,
    ...ALL_BRANCH_CONFLICT_PATTERNS,
    ...ALL_STEM_PATTERNS,
    ...ALL_SPECIAL_STAR_PATTERNS,
  ];

  for (const pattern of allPatterns) {
    reg.register(pattern, true);
  }

  return reg;
}


// =============================================================================
// PATTERN ENGINE ANALYZER
// =============================================================================

export class PatternEngineAnalyzer {
  private registry: PatternRegistry;

  constructor() {
    this.registry = loadAllPatterns();
  }

  analyzeInteractions(
    interactions: Record<string, any>,
    seasonalStates: Record<string, string>,
    daymasterStem: string,
    daymasterElement: string,
    postElementScore: Record<string, number>,
    yearBranch: string = "",
  ): Record<string, any> {
    const enhancedPatterns: EnhancedPatternMatch[] = [];
    const domainRisks: Record<string, Record<string, any>[]> = {};
    for (const d of Object.values(TaxonomyLifeDomain)) {
      domainRisks[d] = [];
    }
    const affectedElements = new Set<string>();

    // Process each interaction
    for (const [intId, intData] of Object.entries(interactions)) {
      if (typeof intData === "string") continue;

      const [intType, participants] = parseInteractionId(intId);
      const category = INTERACTION_TYPE_TO_CATEGORY[intType];
      if (!category) continue;

      // Get element from interaction data
      let patternElement: string | null = (intData as any)?.element ?? null;

      // Look up pattern in registry
      let pattern = findPatternInRegistry(
        this.registry, intType, participants, patternElement
      );

      // Try alternate lookups
      if (!pattern && intType === "CLASH") {
        for (const sub of ["opposite", "same"]) {
          pattern = findPatternInRegistry(this.registry, intType, participants, null, sub);
          if (pattern) break;
        }
      }
      if (!pattern && intType === "STEM_CONFLICT") {
        pattern = findPatternInRegistry(this.registry, intType, participants);
      }
      if (!pattern && intType === "HARM") {
        pattern = findPatternInRegistry(this.registry, intType, participants);
      }

      // Get distance
      const distanceRaw = (intData as any)?.distance ?? 1;
      let distance: number;
      if (typeof distanceRaw === "string") {
        if (distanceRaw.startsWith("distance_")) {
          distance = parseInt(distanceRaw.split("_")[1], 10);
        } else {
          distance = parseInt(distanceRaw, 10) || 1;
        }
      } else {
        distance = Number(distanceRaw) || 1;
      }

      const isTransformed = (intData as any)?.transformed ?? false;

      if (patternElement) {
        affectedElements.add(patternElement);
      }

      const seasonalState = patternElement
        ? (seasonalStates[patternElement] ?? "Resting")
        : "Resting";

      const positions: number[] = (intData as any)?.positions ?? [];
      const primaryPosition = positions.length > 0 ? Math.min(...positions) : 1;

      // Calculate severity
      const severity = calculatePatternSeverity(
        intId,
        category,
        distance,
        seasonalState,
        primaryPosition,
        daymasterElement,
        patternElement,
        isTransformed,
      );

      // Get pattern metadata
      const chineseName = pattern?.chinese_name ?? intType;
      const englishName = pattern?.english_name ?? intType;
      const affectedDomains = pattern
        ? [...pattern.life_domains].map((d) => d as unknown as string)
        : [];
      let pillarMeaning = "";

      if (pattern?.pillar_meanings) {
        const pillarName = getPillarNameFromPosition(primaryPosition);
        pillarMeaning = (pattern.pillar_meanings as any)[pillarName] ?? "";
      }

      // Generate event predictions
      const eventPredictions = this.generateEventPredictions(
        pattern ?? null,
        category,
        severity,
        ["stem_combination", "three_meetings", "three_combinations", "six_harmonies"].includes(category),
      );

      const match: EnhancedPatternMatch = {
        pattern_id: intId,
        category,
        chinese_name: chineseName,
        english_name: englishName,
        participants,
        distance,
        is_transformed: isTransformed,
        severity,
        affected_domains: affectedDomains,
        pillar_meaning: pillarMeaning,
        event_predictions: eventPredictions,
      };

      enhancedPatterns.push(match);

      // Aggregate by domain
      for (const domain of affectedDomains) {
        if (domainRisks[domain]) {
          domainRisks[domain].push({
            pattern_id: intId,
            severity: severity.normalized_score,
            level: severity.severity_level,
          });
        }
      }
    }

    // Get special stars
    const specialStars = this.detectSpecialStars(daymasterStem, interactions, yearBranch);

    // Calculate compound severity by domain
    const domainAnalysis: Record<string, any> = {};
    for (const [domain, risks] of Object.entries(domainRisks)) {
      if (risks.length > 0) {
        const severityResults: SeverityResult[] = risks.map((r) => ({
          raw_score: r.severity * 0.3,
          normalized_score: r.severity,
          severity_level: r.level,
          contributing_factors: {},
          explanation: "",
        }));

        const compound = calculateCompoundSeverity(
          severityResults,
          domain as TaxonomyLifeDomain,
        );

        domainAnalysis[domain] = {
          pattern_count: risks.length,
          compound_severity: compound.normalized_score,
          severity_level: compound.severity_level,
          top_patterns: risks
            .sort((a, b) => b.severity - a.severity)
            .slice(0, 3),
        };
      }
    }

    // Generate health-specific analysis
    let healthEnhanced: Record<string, any> | null = null;
    if (domainAnalysis["health"] && affectedElements.size > 0) {
      const healthSeverities: SeverityResult[] = domainRisks["health"].map((r) => ({
        raw_score: r.severity * 0.3,
        normalized_score: r.severity,
        severity_level: r.level,
        contributing_factors: {},
        explanation: "",
      }));

      if (healthSeverities.length > 0) {
        healthEnhanced = calculateHealthSeverity(
          healthSeverities,
          affectedElements,
          seasonalStates,
          daymasterElement,
        );
      }
    }

    return {
      enhanced_patterns: enhancedPatterns.map((m) => this.matchToDict(m)),
      pattern_count: enhancedPatterns.length,
      domain_analysis: domainAnalysis,
      affected_elements: [...affectedElements],
      special_stars: specialStars,
      health_enhanced: healthEnhanced,
      recommendations: this.generateRecommendations(
        domainAnalysis, daymasterElement, seasonalStates
      ),
    };
  }

  private detectSpecialStars(
    daymasterStem: string,
    interactions: Record<string, any>,
    yearBranch: string = "",
  ): Record<string, any>[] {
    const stars: Record<string, any>[] = [];

    // Day Master-dependent patterns
    const applicablePatterns = getSpecialStarsForDayMaster(daymasterStem);

    // Year Branch-dependent patterns
    if (yearBranch) {
      const yearPatterns = getSpecialStarsForYearBranch(yearBranch);
      applicablePatterns.push(...yearPatterns);
    }

    // Get all branches present in the chart
    const presentBranches = new Set<string>();
    for (const intId of Object.keys(interactions)) {
      if (typeof intId === "string" && intId.includes("~")) {
        const [, participants] = parseInteractionId(intId);
        for (const p of participants) {
          if (p.length <= 4) presentBranches.add(p);
        }
      }
    }
    if (yearBranch) presentBranches.add(yearBranch);

    // Check each pattern for triggers
    for (const pattern of applicablePatterns) {
      for (const nf of pattern.node_filters) {
        if (nf.branches) {
          for (const targetBranch of nf.branches) {
            if (presentBranches.has(targetBranch)) {
              const triggers = this.findBranchTriggers(targetBranch, interactions);

              stars.push({
                pattern_id: pattern.id,
                chinese_name: pattern.chinese_name,
                english_name: pattern.english_name,
                category: pattern.category,
                target_branch: targetBranch,
                description: pattern.description,
                pillar_meanings: pattern.pillar_meanings
                  ? {
                      year: pattern.pillar_meanings.year,
                      month: pattern.pillar_meanings.month,
                      day: pattern.pillar_meanings.day,
                      hour: pattern.pillar_meanings.hour,
                    }
                  : {},
                triggers,
              });
            }
          }
        }
      }
    }

    return stars;
  }

  private findBranchTriggers(
    targetBranch: string,
    interactions: Record<string, any>,
  ): Record<string, string>[] {
    const triggers: Record<string, string>[] = [];

    for (const intId of Object.keys(interactions)) {
      if (typeof intId === "string" && intId.includes("~")) {
        const [, participants, nodesStr] = parseInteractionId(intId);

        if (participants.includes(targetBranch) && nodesStr) {
          const nodeIds = nodesStr.split("-");
          for (let i = 0; i < participants.length; i++) {
            if (participants[i] === targetBranch && i < nodeIds.length) {
              const nodeId = nodeIds[i];
              const pillarType = getPillarNameFromPosition(
                this.nodeIdToPosition(nodeId)
              );
              const trigger = { node_id: nodeId, pillar_type: pillarType };
              const exists = triggers.some(
                (t) => t.node_id === trigger.node_id && t.pillar_type === trigger.pillar_type
              );
              if (!exists) triggers.push(trigger);
            }
          }
        }
      }
    }

    return triggers;
  }

  private nodeIdToPosition(nodeId: string): number {
    const NODE_TO_POSITION: Record<string, number> = {
      hs_h: 0, eb_h: 0,
      hs_d: 1, eb_d: 1,
      hs_m: 2, eb_m: 2,
      hs_y: 3, eb_y: 3,
      hs_10yl: 4, eb_10yl: 4,
      hs_yl: 5, eb_yl: 5,
      hs_ml: 6, eb_ml: 6,
      hs_dl: 7, eb_dl: 7,
      hs_hl: 8, eb_hl: 8,
    };
    return NODE_TO_POSITION[nodeId] ?? 1;
  }

  private generateEventPredictions(
    pattern: PatternSpec | null,
    category: string,
    severity: SeverityResult,
    isPositive: boolean,
  ): Record<string, any>[] {
    const predictions: Record<string, any>[] = [];

    if (!pattern?.event_mapping) {
      if (isPositive) {
        predictions.push({
          domain: "career",
          event_type: "opportunity",
          sentiment: "positive",
          probability: Math.min(0.8, severity.normalized_score / 100),
        });
      } else {
        predictions.push({
          domain: "health",
          event_type: "attention_needed",
          sentiment: "negative",
          probability: Math.min(0.7, severity.normalized_score / 100),
        });
      }
      return predictions;
    }

    const mapping = pattern.event_mapping;

    // Positive event predictions
    if (mapping.positive_events) {
      for (const [domain, eventType] of mapping.positive_events) {
        predictions.push({
          domain,
          event_type: eventType,
          sentiment: "positive",
          probability: Math.min(0.9, 0.5 + severity.normalized_score / 200),
        });
      }
    }

    // Negative event predictions
    if (mapping.negative_events) {
      for (const [domain, eventType] of mapping.negative_events) {
        predictions.push({
          domain,
          event_type: eventType,
          sentiment: "negative",
          probability: Math.min(0.8, 0.4 + severity.normalized_score / 200),
        });
      }
    }

    return predictions.slice(0, 5);
  }

  private generateRecommendations(
    domainAnalysis: Record<string, any>,
    daymasterElement: string,
    seasonalStates: Record<string, string>,
  ): Record<string, string>[] {
    const recommendations: Record<string, string>[] = [];

    // Health recommendations
    if (domainAnalysis["health"]) {
      const health = domainAnalysis["health"];
      if ((health.compound_severity ?? 0) > 50) {
        let vulnerable: string | null = null;
        let maxVuln = 0;
        for (const [elem, state] of Object.entries(seasonalStates)) {
          const vuln = SEASONAL_STATE_MULTIPLIERS[state as string] ?? 1.0;
          if (vuln > maxVuln) {
            maxVuln = vuln;
            vulnerable = elem;
          }
        }

        if (vulnerable && TCM_ORGANS[vulnerable]) {
          const organ = TCM_ORGANS[vulnerable];
          recommendations.push({
            domain: "health",
            priority: health.compound_severity > 70 ? "high" : "medium",
            title: `Support ${organ.zang_organ} Function`,
            description:
              `Your ${organ.zang_organ} (${organ.chinese_zang}) may need attention. ` +
              `Associated body parts: ${[...organ.body_parts].join(", ")}. ` +
              `Manage ${organ.emotion} for better balance.`,
          });
        }
      }
    }

    // Wealth recommendations
    if (domainAnalysis["wealth"]) {
      const wealth = domainAnalysis["wealth"];
      if ((wealth.compound_severity ?? 0) > 40) {
        recommendations.push({
          domain: "wealth",
          priority: "medium",
          title: "Financial Caution Advised",
          description:
            "Multiple patterns indicate financial fluctuations. " +
            "Consider conservative investments and avoid major financial commitments.",
        });
      }
    }

    // Career recommendations
    if (domainAnalysis["career"]) {
      const career = domainAnalysis["career"];
      if ((career.compound_severity ?? 0) > 50) {
        recommendations.push({
          domain: "career",
          priority: "medium",
          title: "Career Dynamics Active",
          description:
            "Significant career energy detected. " +
            "Be prepared for changes and opportunities in your professional life.",
        });
      }
    }

    // Relationship recommendations
    if (domainAnalysis["relationship"]) {
      const rel = domainAnalysis["relationship"];
      if ((rel.compound_severity ?? 0) > 40) {
        recommendations.push({
          domain: "relationship",
          priority: "medium",
          title: "Relationship Attention Needed",
          description:
            "Relationship patterns are active. " +
            "Focus on communication and understanding in close relationships.",
        });
      }
    }

    return recommendations;
  }

  private matchToDict(match: EnhancedPatternMatch): Record<string, any> {
    return {
      pattern_id: match.pattern_id,
      category: match.category,
      chinese_name: match.chinese_name,
      english_name: match.english_name,
      participants: match.participants,
      distance: match.distance,
      is_transformed: match.is_transformed,
      severity: {
        raw_score: match.severity.raw_score,
        normalized_score: match.severity.normalized_score,
        level: match.severity.severity_level,
        explanation: match.severity.explanation,
      },
      affected_domains: match.affected_domains,
      pillar_meaning: match.pillar_meaning,
      event_predictions: match.event_predictions,
    };
  }
}


// =============================================================================
// GLOBAL ANALYZER INSTANCE
// =============================================================================

let globalAnalyzer: PatternEngineAnalyzer | null = null;

export function getPatternAnalyzer(): PatternEngineAnalyzer {
  if (!globalAnalyzer) {
    globalAnalyzer = new PatternEngineAnalyzer();
  }
  return globalAnalyzer;
}

export function analyzeWithPatternEngine(
  interactions: Record<string, any>,
  seasonalStates: Record<string, string>,
  daymasterStem: string,
  daymasterElement: string,
  postElementScore: Record<string, number>,
  yearBranch: string = "",
): Record<string, any> {
  const analyzer = getPatternAnalyzer();
  return analyzer.analyzeInteractions(
    interactions,
    seasonalStates,
    daymasterStem,
    daymasterElement,
    postElementScore,
    yearBranch,
  );
}
