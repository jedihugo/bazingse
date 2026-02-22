import 'server-only';

// =============================================================================
// COMPREHENSIVE BAZI ENGINE — Main Entry Point
// =============================================================================
// Provides the primary interface for constructing ChartData from pillar inputs
// and generating complete reports.
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName } from '../core';
import { getAllBranchQi, getTenGod, STEM_ORDER, BRANCH_ORDER } from '../derived';
import type { ChartData, Pillar, LuckPillarInfo, StrengthAssessment } from './models';
import { generateComprehensiveReport } from './report';
import { mapAllTenGods, classifyTenGodStrength } from './ten-gods';
import { assessDayMasterStrength } from './strength';
import { detectAllInteractions } from './interactions';
import { runAllShenSha } from './shen-sha';
import { runAllPredictions } from './predictions';
import { assessEnvironment } from './environment';
import { calculateWuxing, type WuxingInput, type WuxingResult } from '../wuxing/calculator';


export function buildChart(args: {
  gender: string;
  birth_year: number;
  year_stem: string; year_branch: string;
  month_stem: string; month_branch: string;
  day_stem: string; day_branch: string;
  hour_stem: string; hour_branch: string;
  luck_pillar_stem?: string;
  luck_pillar_branch?: string;
  luck_pillars?: Array<Record<string, unknown>>;
  current_year?: number;
  annual_stem?: string; annual_branch?: string;
  monthly_stem?: string; monthly_branch?: string;
  daily_stem?: string; daily_branch?: string;
  hourly_stem?: string; hourly_branch?: string;
}): ChartData {
  /**
   * Build a ChartData object from raw pillar inputs.
   */
  const {
    gender, birth_year,
    year_stem, year_branch,
    month_stem, month_branch,
    day_stem, day_branch,
    hour_stem, hour_branch,
    luck_pillar_stem = "",
    luck_pillar_branch = "",
    luck_pillars,
    annual_stem = "", annual_branch = "",
    monthly_stem = "", monthly_branch = "",
    daily_stem = "", daily_branch = "",
    hourly_stem = "", hourly_branch = "",
  } = args;

  let currentYear = args.current_year ?? 0;
  if (currentYear === 0) {
    currentYear = new Date().getFullYear();
  }

  const age = currentYear - birth_year;

  // Build pillar objects
  const pillars: Record<string, Pillar> = {};
  const pillarDefs: Array<[string, string, string]> = [
    ["year", year_stem, year_branch],
    ["month", month_stem, month_branch],
    ["day", day_stem, day_branch],
    ["hour", hour_stem, hour_branch],
  ];

  for (const [pos, stem, branch] of pillarDefs) {
    const qi = getAllBranchQi(branch);
    pillars[pos] = {
      position: pos,
      stem: stem as StemName,
      branch: branch as BranchName,
      stem_chinese: STEMS[stem as StemName].chinese,
      branch_chinese: BRANCHES[branch as BranchName].chinese,
      stem_element: STEMS[stem as StemName].element,
      stem_polarity: STEMS[stem as StemName].polarity,
      branch_element: BRANCHES[branch as BranchName].element,
      branch_polarity: BRANCHES[branch as BranchName].polarity,
      hidden_stems: [...qi] as Array<[StemName, number]>,
    };
  }

  // Build luck pillar
  let lp: Pillar | null = null;
  if (luck_pillar_stem && luck_pillar_branch) {
    const lpQi = getAllBranchQi(luck_pillar_branch);
    lp = {
      position: "luck_pillar",
      stem: luck_pillar_stem as StemName,
      branch: luck_pillar_branch as BranchName,
      stem_chinese: STEMS[luck_pillar_stem as StemName].chinese,
      branch_chinese: BRANCHES[luck_pillar_branch as BranchName].chinese,
      stem_element: STEMS[luck_pillar_stem as StemName].element,
      stem_polarity: STEMS[luck_pillar_stem as StemName].polarity,
      branch_element: BRANCHES[luck_pillar_branch as BranchName].element,
      branch_polarity: BRANCHES[luck_pillar_branch as BranchName].polarity,
      hidden_stems: [...lpQi] as Array<[StemName, number]>,
    };
  }

  // Build luck pillars list
  const lpList: LuckPillarInfo[] = [];
  if (luck_pillars) {
    for (const lpData of luck_pillars) {
      const stem = lpData.stem as string;
      const branch = lpData.branch as string;
      const tg = getTenGod(day_stem as StemName, stem as StemName);
      lpList.push({
        stem: stem as StemName,
        branch: branch as BranchName,
        stem_chinese: STEMS[stem as StemName].chinese,
        branch_chinese: BRANCHES[branch as BranchName].chinese,
        start_age: (lpData.start_age as number) ?? 0,
        end_age: (lpData.end_age as number) ?? 0,
        start_year: (lpData.start_year as number) ?? 0,
        end_year: (lpData.end_year as number) ?? 0,
        stem_ten_god: tg ? tg[0] : "",
        stem_ten_god_chinese: tg ? tg[2] : "",
        is_current: luck_pillar_stem === stem && luck_pillar_branch === branch,
        hidden_stems: [...getAllBranchQi(branch)] as Array<[StemName, number]>,
      });
    }
  }

  // Build time-period pillars
  const tpPillars: Record<string, Pillar> = {};
  const tpDefs: Array<[string, string, string]> = [
    ["annual", annual_stem, annual_branch],
    ["monthly", monthly_stem, monthly_branch],
    ["daily", daily_stem, daily_branch],
    ["hourly", hourly_stem, hourly_branch],
  ];
  for (const [tpPos, tpStem, tpBranch] of tpDefs) {
    if (tpStem && tpBranch) {
      const tpQi = getAllBranchQi(tpBranch);
      tpPillars[tpPos] = {
        position: tpPos,
        stem: tpStem as StemName,
        branch: tpBranch as BranchName,
        stem_chinese: STEMS[tpStem as StemName].chinese,
        branch_chinese: BRANCHES[tpBranch as BranchName].chinese,
        stem_element: STEMS[tpStem as StemName].element,
        stem_polarity: STEMS[tpStem as StemName].polarity,
        branch_element: BRANCHES[tpBranch as BranchName].element,
        branch_polarity: BRANCHES[tpBranch as BranchName].polarity,
        hidden_stems: [...tpQi] as Array<[StemName, number]>,
      };
    }
  }

  // Day Master info
  const dm = day_stem as StemName;
  const dmInfo = STEMS[dm];

  // Current year stems
  const cyStemIdx = ((currentYear - 4) % 10 + 10) % 10;
  const cyBranchIdx = ((currentYear - 4) % 12 + 12) % 12;

  const chart: ChartData = {
    gender: gender.toLowerCase(),
    birth_year,
    age,
    pillars,
    day_master: dm,
    dm_element: dmInfo.element,
    dm_polarity: dmInfo.polarity,
    dm_chinese: dmInfo.chinese,
    luck_pillar: lp,
    luck_pillars: lpList,
    time_period_pillars: tpPillars,
    current_year_stem: STEM_ORDER[cyStemIdx],
    current_year_branch: BRANCH_ORDER[cyBranchIdx],
  };

  return chart;
}


export function analyzeForApi(chart: ChartData): Record<string, unknown> {
  /**
   * Run full analysis and return all intermediate results (not just markdown).
   * Used by the /api/analyze_bazi adapter.
   */
  const interactions = detectAllInteractions(chart);

  // Old strength assessment (kept for backward-compatible fields)
  const oldStrength = assessDayMasterStrength(chart, interactions);

  // New Wu Xing calculator
  const wuxingInput: WuxingInput = {
    yearPillar: { stem: chart.pillars.year.stem, branch: chart.pillars.year.branch },
    monthPillar: { stem: chart.pillars.month.stem, branch: chart.pillars.month.branch },
    dayPillar: { stem: chart.pillars.day.stem, branch: chart.pillars.day.branch },
    hourPillar: { stem: chart.pillars.hour.stem, branch: chart.pillars.hour.branch },
    age: chart.age,
    gender: chart.gender === 'male' ? 'M' : 'F',
    location: 'hometown',
  };
  const wuxingResult = calculateWuxing(wuxingInput);

  // Map wuxing strength label to legacy verdict
  const STRENGTH_TO_VERDICT: Record<string, string> = {
    dominant: 'extremely_strong',
    strong: 'strong',
    balanced: 'neutral',
    weak: 'weak',
    very_weak: 'extremely_weak',
  };

  // Build element_percentages from wuxing result
  const wuxingPercentages: Record<string, number> = {};
  for (const elem of ['Wood', 'Fire', 'Earth', 'Metal', 'Water'] as const) {
    wuxingPercentages[elem] = wuxingResult.elements[elem].percent;
  }

  // Build merged StrengthAssessment: wuxing values override, old fields kept for compat
  const strength: StrengthAssessment = {
    score: wuxingResult.dayMaster.percent,
    verdict: STRENGTH_TO_VERDICT[wuxingResult.dayMaster.strength] ?? 'neutral',
    useful_god: wuxingResult.gods.useful,
    element_percentages: wuxingPercentages,
    favorable_elements: [wuxingResult.gods.useful, wuxingResult.gods.favorable],
    unfavorable_elements: [wuxingResult.gods.unfavorable, wuxingResult.gods.enemy],
    // Backward-compatible fields from old assessment
    support_count: oldStrength.support_count,
    drain_count: oldStrength.drain_count,
    seasonal_state: oldStrength.seasonal_state,
    is_following_chart: oldStrength.is_following_chart,
    following_type: oldStrength.following_type,
    best_element_pairs: oldStrength.best_element_pairs,
  };

  const tgEntries = mapAllTenGods(chart);
  const tgClassification = classifyTenGodStrength(tgEntries);
  const shenSha = runAllShenSha(chart);
  const predictions = runAllPredictions(chart);
  const env = assessEnvironment(chart, strength);
  const comprehensiveReport = generateComprehensiveReport(chart);

  return {
    strength,
    wuxing_result: wuxingResult,
    ten_god_entries: tgEntries,
    ten_god_classification: tgClassification,
    interactions,
    shen_sha: shenSha,
    predictions,
    environment: env,
    comprehensive_report: comprehensiveReport,
  };
}


export function analyze(args: {
  gender: string;
  birth_year: number;
  year_stem: string; year_branch: string;
  month_stem: string; month_branch: string;
  day_stem: string; day_branch: string;
  hour_stem: string; hour_branch: string;
  luck_pillar_stem?: string;
  luck_pillar_branch?: string;
  luck_pillars?: Array<Record<string, unknown>>;
  current_year?: number;
}): string {
  /**
   * One-call comprehensive BaZi analysis.
   * Returns complete markdown report.
   */
  const chart = buildChart(args);
  return generateComprehensiveReport(chart);
}
