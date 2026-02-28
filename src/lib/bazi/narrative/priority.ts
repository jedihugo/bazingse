
// =============================================================================
// NARRATIVE PRIORITY SYSTEM
// =============================================================================
// Scores and ranks narrative entries for display ordering.
// Ported from api/library/narrative/priority.py
// =============================================================================

// ---------------------------------------------------------------------------
// Narrative Entry (input type)
// ---------------------------------------------------------------------------

export interface NarrativeEntry {
  type: string;
  category: string;
  priority: number;
  text_en: string;
  text_zh: string;
  sentiment: string;
  distance?: number;
  is_transformed?: boolean;
  pillar?: string;
  [key: string]: any;
}

// ---------------------------------------------------------------------------
// Priority Constants
// ---------------------------------------------------------------------------

export const TYPE_PRIORITY: Record<string, number> = {
  chart_summary: 1,
  daymaster: 10,
  stem_combination: 50,
  stem_conflict: 60,
  three_meetings: 100,
  three_combinations: 110,
  six_harmonies: 120,
  half_meetings: 130,
  half_combinations: 140,
  arched_combinations: 150,
  clash: 200,
  punishment: 210,
  harm: 240,
  destruction: 250,
  element_excess: 300,
  element_deficient: 310,
  wealth_storage_present: 400,
  wealth_storage_clashed: 410,
  shen_sha: 500,
  ten_god_pillar: 600,
};

export const TRANSFORMATION_MULTIPLIER = 1.3;
export const PILLAR_MULTIPLIER: Record<string, number> = {
  day: 1.5,
  month: 1.2,
  year: 1.0,
  hour: 1.0,
};
export const DISTANCE_MULTIPLIER: Record<number, number> = {
  0: 1.0,
  1: 0.85,
  2: 0.7,
  3: 0.55,
  4: 0.45,
};

// ---------------------------------------------------------------------------
// Priority Calculation
// ---------------------------------------------------------------------------

export function calculatePriorityScore(entry: NarrativeEntry): number {
  // Base priority from type
  const basePriority = TYPE_PRIORITY[entry.type] ?? entry.priority ?? 500;

  // Invert: lower number = higher priority, so we compute sort weight
  let score = 1000 - basePriority;

  // Transformation bonus
  if (entry.is_transformed) {
    score *= TRANSFORMATION_MULTIPLIER;
  }

  // Pillar modifier
  if (entry.pillar && PILLAR_MULTIPLIER[entry.pillar]) {
    score *= PILLAR_MULTIPLIER[entry.pillar];
  }

  // Distance modifier (closer = more impactful)
  if (entry.distance !== undefined && DISTANCE_MULTIPLIER[entry.distance] !== undefined) {
    score *= DISTANCE_MULTIPLIER[entry.distance];
  }

  return Math.round(score * 100) / 100;
}

// ---------------------------------------------------------------------------
// Prioritize Narratives
// ---------------------------------------------------------------------------

export function prioritizeNarratives(narratives: NarrativeEntry[]): NarrativeEntry[] {
  return [...narratives].sort((a, b) => {
    const scoreA = calculatePriorityScore(a);
    const scoreB = calculatePriorityScore(b);
    return scoreB - scoreA; // Higher score first
  });
}

// ---------------------------------------------------------------------------
// Group by Category
// ---------------------------------------------------------------------------

export function groupNarrativesByCategory(
  narratives: NarrativeEntry[]
): Record<string, NarrativeEntry[]> {
  const groups: Record<string, NarrativeEntry[]> = {};

  for (const narrative of narratives) {
    const cat = narrative.category || 'other';
    if (!groups[cat]) {
      groups[cat] = [];
    }
    groups[cat].push(narrative);
  }

  // Sort within each group
  for (const cat of Object.keys(groups)) {
    groups[cat] = prioritizeNarratives(groups[cat]);
  }

  return groups;
}
