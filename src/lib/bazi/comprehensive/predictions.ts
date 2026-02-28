
// =============================================================================
// EVENT PREDICTION ENGINE
// =============================================================================
// Year-by-year scoring for major life events:
//   - Marriage timing
//   - Divorce risk
//   - Children arrival
//   - Career peaks/changes
// Uses natal chart, luck pillars, and annual pillar interactions.
// =============================================================================

import { BRANCHES, type BranchName, type StemName } from '../core';
import { getTenGod, getAllBranchQi, STEM_ORDER, BRANCH_ORDER } from '../derived';
import type { EventPrediction, ChartData } from './models';
import { HONG_LUAN_LOOKUP, TIAN_XI_LOOKUP, TAO_HUA_LOOKUP } from './shen-sha';

// =============================================================================
// ANNUAL PILLAR CALCULATOR
// =============================================================================

export function getAnnualPillar(year: number): [StemName, BranchName] {
  /** Calculate the Heavenly Stem and Earthly Branch for a given year. */
  const stemIdx = ((year - 4) % 10 + 10) % 10;
  const branchIdx = ((year - 4) % 12 + 12) % 12;
  return [STEM_ORDER[stemIdx], BRANCH_ORDER[branchIdx]];
}

// =============================================================================
// CLASH DETECTION HELPERS
// =============================================================================

const CLASH_MAP: Record<string, string> = {};
const HARMONY_MAP: Record<string, string> = {};
for (const b of Object.keys(BRANCHES) as BranchName[]) {
  CLASH_MAP[b] = BRANCHES[b].clashes;
  HARMONY_MAP[b] = BRANCHES[b].harmonizes;
}

function _branchesClash(b1: string, b2: string): boolean {
  return CLASH_MAP[b1] === b2;
}

function _branchesHarmonize(b1: string, b2: string): boolean {
  return HARMONY_MAP[b1] === b2;
}

// =============================================================================
// MARRIAGE TIMING PREDICTOR
// =============================================================================

export function predictMarriageYears(
  chart: ChartData,
  startYear = 0,
  endYear = 0,
): EventPrediction[] {
  if (startYear === 0) startYear = chart.birth_year + 18;
  if (endYear === 0) endYear = chart.birth_year + 55;

  const dm = chart.day_master;
  const dayBranch = chart.pillars["day"].branch;
  const yearBranch = chart.pillars["year"].branch;

  const spouseStarAbbr = chart.gender === "male" ? "DW" : "DO";

  const hlTarget = HONG_LUAN_LOOKUP[yearBranch] ?? null;
  const txTarget = TIAN_XI_LOOKUP[yearBranch] ?? null;

  const pbTargets = new Set<string>();
  for (const base of ["year", "day"]) {
    const baseBr = chart.pillars[base].branch;
    const pb = TAO_HUA_LOOKUP[baseBr];
    if (pb) pbTargets.add(pb);
  }

  const results: EventPrediction[] = [];

  for (let year = startYear; year <= endYear; year++) {
    const age = year - chart.birth_year;
    let score = 0;
    const factors: string[] = [];

    const [annualStem, annualBranch] = getAnnualPillar(year);

    // 1. Hong Luan activated
    if (annualBranch === hlTarget) {
      score += 25;
      factors.push("Hong Luan (红鸾) activated");
    }

    // 2. Tian Xi activated
    if (annualBranch === txTarget) {
      score += 20;
      factors.push("Tian Xi (天喜) activated");
    }

    // 3. Peach Blossom activated
    if (pbTargets.has(annualBranch)) {
      score += 15;
      factors.push("Peach Blossom (桃花) activated");
    }

    // 4. Spouse palace harmonized
    if (_branchesHarmonize(dayBranch, annualBranch)) {
      score += 20;
      factors.push("Spouse palace harmonized by annual branch");
    }

    // 5. Spouse palace clashed
    if (_branchesClash(dayBranch, annualBranch)) {
      score += 10;
      factors.push("Spouse palace clashed (can trigger marriage event)");
    }

    // 6. Spouse star in annual stem
    const tg = getTenGod(dm, annualStem);
    if (tg && tg[0] === spouseStarAbbr) {
      score += 20;
      factors.push(`Spouse star (${spouseStarAbbr}) in annual stem`);
    }

    // 7. Spouse star in annual branch hidden stems
    for (const [hs] of getAllBranchQi(annualBranch)) {
      const tgH = getTenGod(dm, hs);
      if (tgH && tgH[0] === spouseStarAbbr) {
        score += 10;
        factors.push("Spouse star in annual branch hidden stem");
        break;
      }
    }

    // 8. Cultural age window
    if (chart.gender === "male") {
      if (age >= 26 && age <= 33) {
        score += 10;
        factors.push("Prime marriage age window (male 26-33)");
      } else if (age >= 22 && age <= 25) {
        score += 5;
      }
    } else {
      if (age >= 23 && age <= 29) {
        score += 10;
        factors.push("Prime marriage age window (female 23-29)");
      } else if (age >= 20 && age <= 22) {
        score += 5;
      }
    }

    // 9. Luck pillar alignment
    for (const lp of chart.luck_pillars) {
      if (lp.start_year <= year && year <= lp.end_year) {
        const lpTg = getTenGod(dm, lp.stem);
        if (lpTg && lpTg[0] === spouseStarAbbr) {
          score += 10;
          factors.push("Luck pillar stem = spouse star");
        }
        if (_branchesHarmonize(dayBranch, lp.branch)) {
          score += 5;
          factors.push("Luck pillar harmonizes spouse palace");
        }
        break;
      }
    }

    if (score >= 20) {
      results.push({
        event_type: "marriage",
        year,
        age,
        score: Math.round(score * 10) / 10,
        factors,
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

// =============================================================================
// DIVORCE RISK PREDICTOR
// =============================================================================

export function predictDivorceYears(
  chart: ChartData,
  startYear = 0,
  endYear = 0,
): EventPrediction[] {
  if (startYear === 0) startYear = chart.birth_year + 20;
  if (endYear === 0) endYear = chart.birth_year + 60;

  const dm = chart.day_master;
  const dayBranch = chart.pillars["day"].branch;
  const results: EventPrediction[] = [];

  for (let year = startYear; year <= endYear; year++) {
    const age = year - chart.birth_year;
    let score = 0;
    const factors: string[] = [];

    const [annualStem, annualBranch] = getAnnualPillar(year);

    // 1. Spouse palace clashed
    if (_branchesClash(dayBranch, annualBranch)) {
      score += 25;
      factors.push("Spouse palace directly clashed");
    }

    // 2. Rob Wealth in annual stem
    const tg = getTenGod(dm, annualStem);
    if (tg && tg[0] === "RW") {
      score += 20;
      factors.push("Rob Wealth appears (competitor for spouse)");
    }

    // 3. Hurting Officer
    if (tg && tg[0] === "HO") {
      const bonus = chart.gender === "female" ? 20 : 10;
      score += bonus;
      factors.push("Hurting Officer appears (damages marriage structure)");
    }

    // 4. Seven Killings for females
    if (chart.gender === "female" && tg && tg[0] === "7K") {
      score += 10;
      factors.push("Seven Killings appears (rival/affair indicator)");
    }

    // 5. Punishment patterns
    const natalBranches = ["year", "month", "day", "hour"].map(p => chart.pillars[p].branch);
    const punishmentCheck = new Set([...natalBranches, annualBranch]);

    const ungrateful = new Set(["Yin", "Si", "Shen"]);
    const ungratefulIntersect = [...ungrateful].filter(x => punishmentCheck.has(x as BranchName));
    if (ungratefulIntersect.length >= 3 && ungrateful.has(annualBranch)) {
      score += 15;
      factors.push("Ungrateful punishment activated");
    }

    const bullying = new Set(["Chou", "Wei", "Xu"]);
    const bullyingIntersect = [...bullying].filter(x => punishmentCheck.has(x as BranchName));
    if (bullyingIntersect.length >= 3 && bullying.has(annualBranch)) {
      score += 15;
      factors.push("Bullying punishment activated");
    }

    // 6. Luck pillar clash
    for (const lp of chart.luck_pillars) {
      if (lp.start_year <= year && year <= lp.end_year) {
        if (_branchesClash(dayBranch, lp.branch)) {
          score += 15;
          factors.push("Luck pillar also clashes spouse palace");
        }
        break;
      }
    }

    if (score >= 20) {
      results.push({
        event_type: "divorce",
        year,
        age,
        score: Math.round(score * 10) / 10,
        factors,
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

// =============================================================================
// CHILDREN ARRIVAL PREDICTOR
// =============================================================================

export function predictChildrenYears(
  chart: ChartData,
  startYear = 0,
  endYear = 0,
): EventPrediction[] {
  if (startYear === 0) startYear = chart.birth_year + 20;
  if (endYear === 0) endYear = chart.birth_year + 50;

  const dm = chart.day_master;
  const hourBranch = chart.pillars["hour"].branch;

  const childStars = new Set(
    chart.gender === "male" ? ["7K", "DO"] : ["HO", "EG"]);

  const results: EventPrediction[] = [];

  for (let year = startYear; year <= endYear; year++) {
    const age = year - chart.birth_year;
    let score = 0;
    const factors: string[] = [];

    const [annualStem, annualBranch] = getAnnualPillar(year);

    // 1. Children star in annual stem
    const tg = getTenGod(dm, annualStem);
    if (tg && childStars.has(tg[0])) {
      score += 25;
      factors.push(`Children star (${tg[0]}) in annual stem`);
    }

    // 2. Children star in annual branch hidden stems
    for (const [hs] of getAllBranchQi(annualBranch)) {
      const tgH = getTenGod(dm, hs);
      if (tgH && childStars.has(tgH[0])) {
        score += 10;
        factors.push("Children star in annual branch");
        break;
      }
    }

    // 3. Hour palace harmonized
    if (_branchesHarmonize(hourBranch, annualBranch)) {
      score += 15;
      factors.push("Children palace harmonized");
    }

    // 4. Cultural age window
    if (chart.gender === "male") {
      if (age >= 27 && age <= 36) score += 8;
    } else {
      if (age >= 24 && age <= 33) score += 8;
    }

    // 5. Luck pillar alignment
    for (const lp of chart.luck_pillars) {
      if (lp.start_year <= year && year <= lp.end_year) {
        const lpTg = getTenGod(dm, lp.stem);
        if (lpTg && childStars.has(lpTg[0])) {
          score += 10;
          factors.push("Luck pillar stem = children star");
        }
        break;
      }
    }

    if (score >= 20) {
      results.push({
        event_type: "child_birth",
        year,
        age,
        score: Math.round(score * 10) / 10,
        factors,
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

// =============================================================================
// CAREER PEAK PREDICTOR
// =============================================================================

export function predictCareerYears(
  chart: ChartData,
  startYear = 0,
  endYear = 0,
): EventPrediction[] {
  if (startYear === 0) startYear = chart.birth_year + 20;
  if (endYear === 0) endYear = chart.birth_year + 65;

  const dm = chart.day_master;
  const results: EventPrediction[] = [];

  for (let year = startYear; year <= endYear; year++) {
    const age = year - chart.birth_year;
    let score = 0;
    const factors: string[] = [];

    const [annualStem, annualBranch] = getAnnualPillar(year);
    const tg = getTenGod(dm, annualStem);

    // 1. Direct Officer
    if (tg && tg[0] === "DO") {
      score += 20;
      factors.push("Direct Officer year (recognition, promotion)");
    }

    // 2. Seven Killings
    if (tg && tg[0] === "7K") {
      score += 15;
      factors.push("Seven Killings year (power grab, risk)");
    }

    // 3. Indirect Wealth
    if (tg && tg[0] === "IW") {
      score += 15;
      factors.push("Indirect Wealth year (windfall, opportunity)");
    }

    // 4. Month pillar (career palace) harmonized
    const monthBranch = chart.pillars["month"].branch;
    if (_branchesHarmonize(monthBranch, annualBranch)) {
      score += 15;
      factors.push("Career palace harmonized");
    }

    // 5. Career palace clashed
    if (_branchesClash(monthBranch, annualBranch)) {
      score += 10;
      factors.push("Career palace clashed (career change event)");
    }

    // 6. Luck pillar alignment
    for (const lp of chart.luck_pillars) {
      if (lp.start_year <= year && year <= lp.end_year) {
        const lpTg = getTenGod(dm, lp.stem);
        if (lpTg && (lpTg[0] === "DO" || lpTg[0] === "7K" || lpTg[0] === "IW")) {
          score += 10;
          factors.push(`Luck pillar = ${lpTg[0]} (career energy)`);
        }
        break;
      }
    }

    if (score >= 20) {
      results.push({
        event_type: "career_peak",
        year,
        age,
        score: Math.round(score * 10) / 10,
        factors,
      });
    }
  }

  results.sort((a, b) => b.score - a.score);
  return results;
}

// =============================================================================
// MASTER PREDICTION FUNCTION
// =============================================================================

export function runAllPredictions(chart: ChartData): Record<string, EventPrediction[]> {
  /** Run all prediction algorithms and return top results for each category. */
  return {
    marriage: predictMarriageYears(chart).slice(0, 5),
    divorce: predictDivorceYears(chart).slice(0, 5),
    children: predictChildrenYears(chart).slice(0, 5),
    career: predictCareerYears(chart).slice(0, 5),
  };
}
