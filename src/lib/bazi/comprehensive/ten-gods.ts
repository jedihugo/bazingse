
// =============================================================================
// TEN GODS (十神) COMPREHENSIVE MAPPING ENGINE
// =============================================================================
// Maps all Ten Gods across every visible stem and hidden stem in all pillars.
// Classifies each Ten God's strength in the chart.
// =============================================================================

import { getTenGod, getAllBranchQi } from '../derived';
import type { TenGodEntry, ChartData } from './models';

// Ten God display info
export const TEN_GOD_INFO: Readonly<Record<string, {
  english: string;
  chinese: string;
  category: string;
  element_role: string;
}>> = {
  F:  { english: "Friend",           chinese: "比肩", category: "companion", element_role: "same" },
  RW: { english: "Rob Wealth",       chinese: "劫財", category: "companion", element_role: "same" },
  EG: { english: "Eating God",       chinese: "食神", category: "output",    element_role: "output" },
  HO: { english: "Hurting Officer",  chinese: "傷官", category: "output",    element_role: "output" },
  IW: { english: "Indirect Wealth",  chinese: "偏財", category: "wealth",    element_role: "wealth" },
  DW: { english: "Direct Wealth",    chinese: "正財", category: "wealth",    element_role: "wealth" },
  "7K": { english: "Seven Killings", chinese: "七殺", category: "officer",   element_role: "officer" },
  DO: { english: "Direct Officer",   chinese: "正官", category: "officer",   element_role: "officer" },
  IR: { english: "Indirect Resource",chinese: "偏印", category: "resource",  element_role: "resource" },
  DR: { english: "Direct Resource",  chinese: "正印", category: "resource",  element_role: "resource" },
};

// Male and female specific meanings for Ten Gods
export const TEN_GOD_LIFE_MEANING: Readonly<Record<string, Record<string, string>>> = {
  male: {
    DW: "wife star",
    IW: "mistress/father star",
    DO: "children (daughters) star",
    "7K": "children (sons) / authority star",
    DR: "mother star",
    IR: "stepmother / unusual knowledge star",
    F:  "siblings (same gender) / competitors",
    RW: "siblings (opposite gender) / rivals",
    EG: "subordinates / talent star",
    HO: "creativity / rebellion star",
  },
  female: {
    DO: "husband star",
    "7K": "boyfriend / lover / authority star",
    EG: "children (daughters) star",
    HO: "children (sons) / creativity star",
    DW: "father star",
    IW: "father figure star",
    DR: "mother star",
    IR: "stepmother / unusual knowledge star",
    F:  "siblings (same gender) / competitors",
    RW: "siblings (opposite gender) / rivals",
  },
};

export function mapAllTenGods(chart: ChartData): TenGodEntry[] {
  /** Map Ten Gods for every stem in the chart (visible + hidden). */
  const dm = chart.day_master;
  const entries: TenGodEntry[] = [];

  for (const pos of ["year", "month", "day", "hour"]) {
    const pillar = chart.pillars[pos];

    // Visible stem (skip Day Master itself for the mapping)
    const stem = pillar.stem;
    const tg = getTenGod(dm, stem);
    if (tg) {
      entries.push({
        stem,
        abbreviation: tg[0],
        english: tg[1],
        chinese: tg[2],
        location: `${pos}_stem`,
        position: pos,
        visible: true,
      });
    }

    // Hidden stems in branch
    const branchQi = getAllBranchQi(pillar.branch);
    for (let idx = 0; idx < branchQi.length; idx++) {
      const [hs] = branchQi[idx];
      const tgH = getTenGod(dm, hs);
      if (tgH) {
        const label = idx === 0 ? "primary_qi" : `hidden_${idx}`;
        entries.push({
          stem: hs,
          abbreviation: tgH[0],
          english: tgH[1],
          chinese: tgH[2],
          location: `${pos}_branch_${label}`,
          position: pos,
          visible: false,
        });
      }
    }
  }

  // Luck pillar if present
  if (chart.luck_pillar) {
    const lp = chart.luck_pillar;
    const tg = getTenGod(dm, lp.stem);
    if (tg) {
      entries.push({
        stem: lp.stem,
        abbreviation: tg[0],
        english: tg[1],
        chinese: tg[2],
        location: "luck_pillar_stem",
        position: "luck_pillar",
        visible: true,
      });
    }
    const branchQi = getAllBranchQi(lp.branch);
    for (let idx = 0; idx < branchQi.length; idx++) {
      const [hs] = branchQi[idx];
      const tgH = getTenGod(dm, hs);
      if (tgH) {
        const label = idx === 0 ? "primary_qi" : `hidden_${idx}`;
        entries.push({
          stem: hs,
          abbreviation: tgH[0],
          english: tgH[1],
          chinese: tgH[2],
          location: `luck_pillar_branch_${label}`,
          position: "luck_pillar",
          visible: false,
        });
      }
    }
  }

  // Time-period pillars
  for (const [tpPos, tpPillar] of Object.entries(chart.time_period_pillars)) {
    const tg = getTenGod(dm, tpPillar.stem);
    if (tg) {
      entries.push({
        stem: tpPillar.stem,
        abbreviation: tg[0],
        english: tg[1],
        chinese: tg[2],
        location: `${tpPos}_stem`,
        position: tpPos,
        visible: true,
      });
    }
    const branchQi = getAllBranchQi(tpPillar.branch);
    for (let idx = 0; idx < branchQi.length; idx++) {
      const [hs] = branchQi[idx];
      const tgH = getTenGod(dm, hs);
      if (tgH) {
        const label = idx === 0 ? "primary_qi" : `hidden_${idx}`;
        entries.push({
          stem: hs,
          abbreviation: tgH[0],
          english: tgH[1],
          chinese: tgH[2],
          location: `${tpPos}_branch_${label}`,
          position: tpPos,
          visible: false,
        });
      }
    }
  }

  return entries;
}

export function classifyTenGodStrength(entries: TenGodEntry[]): Record<string, Record<string, unknown>> {
  /**
   * Classify each Ten God's strength in the chart.
   * Returns dict keyed by abbreviation with strength, counts, locations.
   */
  const natalPositions = new Set(["year", "month", "day", "hour"]);
  const tgCounts: Record<string, Record<string, unknown>> = {};

  for (const [abbr, info] of Object.entries(TEN_GOD_INFO)) {
    tgCounts[abbr] = {
      abbreviation: abbr,
      english: info.english,
      chinese: info.chinese,
      category: info.category,
      visible_count: 0,
      hidden_count: 0,
      total_count: 0,
      locations: [] as string[],
      strength: "ABSENT",
    };
  }

  for (const entry of entries) {
    if (!natalPositions.has(entry.position)) continue;
    const info = tgCounts[entry.abbreviation];
    if (!info) continue;
    if (entry.visible) {
      info.visible_count = (info.visible_count as number) + 1;
    } else {
      info.hidden_count = (info.hidden_count as number) + 1;
    }
    info.total_count = (info.total_count as number) + 1;
    (info.locations as string[]).push(entry.location);
  }

  for (const info of Object.values(tgCounts)) {
    const vc = info.visible_count as number;
    const hc = info.hidden_count as number;
    const total = info.total_count as number;

    if (total === 0) {
      info.strength = "ABSENT";
    } else if (vc >= 2) {
      info.strength = "PROMINENT";
    } else if (vc === 1 && hc >= 1) {
      info.strength = "PROMINENT";
    } else if (vc === 1) {
      info.strength = "PRESENT";
    } else if (hc >= 2) {
      info.strength = "PRESENT";
    } else if (hc === 1) {
      info.strength = "HIDDEN_ONLY";
    } else {
      info.strength = "WEAK";
    }
  }

  return tgCounts;
}

export function getDominantTenGods(classification: Record<string, Record<string, unknown>>): string[] {
  /** Return Ten God abbreviations that are PROMINENT. */
  return Object.entries(classification)
    .filter(([, info]) => info.strength === "PROMINENT")
    .map(([abbr]) => abbr);
}

export function getAbsentTenGods(classification: Record<string, Record<string, unknown>>): string[] {
  /** Return Ten God abbreviations that are ABSENT. */
  return Object.entries(classification)
    .filter(([, info]) => info.strength === "ABSENT")
    .map(([abbr]) => abbr);
}

export function checkSpouseStar(
  chart: ChartData,
  classification: Record<string, Record<string, unknown>>,
): Record<string, unknown> {
  /**
   * Check the spouse star status for this chart.
   * Male: DW (Direct Wealth) = wife star
   * Female: DO (Direct Officer) = husband star
   */
  let star: string;
  let label: string;
  if (chart.gender === "male") {
    star = "DW";
    label = "wife star (正財)";
  } else {
    star = "DO";
    label = "husband star (正官)";
  }

  const info = classification[star] ?? {};
  const strength = (info.strength as string) ?? "ABSENT";

  return {
    star,
    label,
    strength,
    present: strength !== "ABSENT",
    locations: (info.locations as string[]) ?? [],
    is_critical_absent: strength === "ABSENT",
  };
}

export function checkChildrenStar(
  chart: ChartData,
  classification: Record<string, Record<string, unknown>>,
): Record<string, unknown> {
  /**
   * Check children star status.
   * Male: 7K (sons), DO (daughters)
   * Female: EG (daughters), HO (sons)
   */
  let primary: string;
  let secondary: string;
  if (chart.gender === "male") {
    primary = "7K";
    secondary = "DO";
  } else {
    primary = "HO";
    secondary = "EG";
  }

  const pInfo = classification[primary] ?? {};
  const sInfo = classification[secondary] ?? {};

  return {
    primary_star: primary,
    secondary_star: secondary,
    primary_strength: (pInfo.strength as string) ?? "ABSENT",
    secondary_strength: (sInfo.strength as string) ?? "ABSENT",
    any_present: ((pInfo.strength as string) ?? "ABSENT") !== "ABSENT" ||
                 ((sInfo.strength as string) ?? "ABSENT") !== "ABSENT",
  };
}

export function getTenGodElementCounts(entries: TenGodEntry[]): Record<string, number> {
  /**
   * Count element influence by Ten God category.
   * Visible stems count 1.0, hidden stems count proportionally less.
   * Only counts natal chart entries.
   */
  const HIDDEN_WEIGHT = 0.5;
  const natalPositions = new Set(["year", "month", "day", "hour"]);
  const counts: Record<string, number> = {
    companion: 0, output: 0, wealth: 0, officer: 0, resource: 0,
  };

  for (const entry of entries) {
    if (!natalPositions.has(entry.position)) continue;
    const info = TEN_GOD_INFO[entry.abbreviation];
    if (info) {
      const weight = entry.visible ? 1.0 : HIDDEN_WEIGHT;
      counts[info.category] += weight;
    }
  }

  return counts;
}

export function analyzeTenGodPatterns(
  chart: ChartData,
  classification: Record<string, Record<string, unknown>>,
): Array<Record<string, unknown>> {
  /**
   * Identify notable Ten God patterns in the chart.
   * Returns list of pattern descriptions.
   */
  const patterns: Array<Record<string, unknown>> = [];

  // Check for too many companions (Friend + Rob Wealth)
  const fTotal = (classification["F"].total_count as number) +
                 (classification["RW"].total_count as number);
  if (fTotal >= 3) {
    patterns.push({
      pattern: "companion_heavy",
      description: "Too many companions (Friend + Rob Wealth) = competition problems, " +
                   "wealth leakage, relationship interference",
      severity: "moderate",
      life_areas: ["wealth", "relationship"],
    });
  }

  // Check for output overload (Eating God + Hurting Officer)
  const egHo = (classification["EG"].total_count as number) +
               (classification["HO"].total_count as number);
  if (egHo >= 3) {
    patterns.push({
      pattern: "output_heavy",
      description: "Too much output energy (EG + HO) = energy drain, overwork, " +
                   "weakened authority, undermined structure",
      severity: "moderate",
      life_areas: ["health", "career"],
    });
  }

  // Hurting Officer prominent = trouble with authority
  if (classification["HO"].strength === "PROMINENT") {
    patterns.push({
      pattern: "ho_prominent",
      description: "Prominent Hurting Officer = rebellious, conflicts with authority, " +
                   "creative but destructive to structure and rules",
      severity: "moderate",
      life_areas: ["career", "relationship", "legal"],
    });
  }

  // Seven Killings prominent without control
  if (classification["7K"].strength === "PROMINENT") {
    const hasEg = (classification["EG"].total_count as number) > 0;
    patterns.push({
      pattern: "7k_prominent",
      description: "Seven Killings prominent" +
                   (hasEg
                     ? " but controlled by Eating God"
                     : " WITHOUT control = aggressive, ruthless, danger of conflicts"),
      severity: hasEg ? "mild" : "severe",
      life_areas: ["career", "health", "legal"],
    });
  }

  // Rob Wealth prominent = wealth problems
  if (classification["RW"].strength === "PROMINENT" ||
      classification["RW"].strength === "PRESENT") {
    patterns.push({
      pattern: "rw_present",
      description: "Rob Wealth present = money lost through others, " +
                   "partnerships can drain wealth, competitive spending",
      severity: "moderate",
      life_areas: ["wealth"],
    });
  }

  // No wealth at all
  if (classification["DW"].strength === "ABSENT" &&
      classification["IW"].strength === "ABSENT") {
    patterns.push({
      pattern: "no_wealth",
      description: "Both Direct and Indirect Wealth ABSENT = " +
                   "difficulty accumulating wealth, needs element remedies",
      severity: "severe",
      life_areas: ["wealth"],
    });
  }

  // No officer at all
  if (classification["DO"].strength === "ABSENT" &&
      classification["7K"].strength === "ABSENT") {
    patterns.push({
      pattern: "no_officer",
      description: "Both Direct Officer and Seven Killings ABSENT = " +
                   "lack of discipline, authority, and career structure",
      severity: "moderate",
      life_areas: ["career"],
    });
  }

  // No resource at all
  if (classification["DR"].strength === "ABSENT" &&
      classification["IR"].strength === "ABSENT") {
    patterns.push({
      pattern: "no_resource",
      description: "Both Direct and Indirect Resource ABSENT = " +
                   "lack of support, mentors, education backing, mother issues",
      severity: "moderate",
      life_areas: ["education", "health", "family"],
    });
  }

  return patterns;
}
