import { Solar } from 'lunar-typescript';
import { generateBaziChart, generateLuckPillars, generateXiaoYunPillars } from '$lib/bazi/chart';
import { buildChart, analyzeForApi } from '$lib/bazi/comprehensive/engine';
import { adaptToFrontend } from '$lib/bazi/comprehensive/adapter';
import { BRANCHES, type BranchName } from '$lib/bazi/core';
import {
  getDongGongOfficer, getDongGongRating, getDongGongDayInfo, checkConsultPromotion,
  DONG_GONG_RATINGS, DONG_GONG_DAY_OFFICERS, DONG_GONG_MONTHS, DONG_GONG_BRANCH_TO_MONTH,
} from '$lib/bazi/dong-gong';

// =============================================================================
// FOUR EXTINCTION / FOUR SEPARATION CHECK
// =============================================================================

const JIEQI_NAMES: Record<number, [string, string, string]> = {
  3:  ["li_chun",  "\u7acb\u6625", "Li Chun"],
  9:  ["li_xia",   "\u7acb\u590f", "Li Xia"],
  15: ["li_qiu",   "\u7acb\u79cb", "Li Qiu"],
  21: ["li_dong",  "\u7acb\u51ac", "Li Dong"],
  0:  ["dong_zhi", "\u51ac\u81f3", "Dong Zhi"],
  6:  ["chun_fen", "\u6625\u5206", "Chun Fen"],
  12: ["xia_zhi",  "\u590f\u81f3", "Xia Zhi"],
  18: ["qiu_fen",  "\u79cb\u5206", "Qiu Fen"],
};

const FOUR_EXTINCTION_TERM_NAMES = new Set([
  "\u7acb\u6625", "\u7acb\u590f", "\u7acb\u79cb", "\u7acb\u51ac",
]);

const FOUR_SEPARATION_TERM_NAMES = new Set([
  "\u51ac\u81f3", "\u6625\u5206", "\u590f\u81f3", "\u79cb\u5206",
]);

const TERM_CHINESE_TO_IDX: Record<string, number> = {};
for (const [idx, [, chinese]] of Object.entries(JIEQI_NAMES)) {
  TERM_CHINESE_TO_IDX[chinese] = Number(idx);
}

export function checkFourExtinctionSeparation(
  year: number, month: number, day: number, hour?: number,
): {
  type: string;
  chinese: string;
  english: string;
  solar_term_id: string;
  solar_term_chinese: string;
  solar_term_english: string;
  forbidden_start_hour: number;
  forbidden_end_hour: number;
} | null {
  for (let dayOffset = 0; dayOffset < 2; dayOffset++) {
    const checkDate = new Date(year, month - 1, day + dayOffset);
    const checkY = checkDate.getFullYear();
    const checkM = checkDate.getMonth() + 1;
    const checkD = checkDate.getDate();

    const solar = Solar.fromYmd(checkY, checkM, checkD);
    const lunar = solar.getLunar();

    const jieqiName = lunar.getJieQi();
    if (!jieqiName) continue;

    const isExtinction = FOUR_EXTINCTION_TERM_NAMES.has(jieqiName);
    const isSeparation = FOUR_SEPARATION_TERM_NAMES.has(jieqiName);
    if (!isExtinction && !isSeparation) continue;

    const jqIdx = TERM_CHINESE_TO_IDX[jieqiName];
    if (jqIdx === undefined) continue;

    const jieqiTable = lunar.getJieQiTable();
    const termSolar = jieqiTable[jieqiName];
    if (!termSolar) continue;

    const transitionHour = termSolar.getHour() + termSolar.getMinute() / 60;
    const termTotal = dayOffset * 24 + transitionHour;
    const forbiddenStartTotal = termTotal - 24;
    const forbiddenEndTotal = termTotal;

    const overlapStart = Math.max(forbiddenStartTotal, 0);
    const overlapEnd = Math.min(forbiddenEndTotal, 24);

    if (overlapStart >= overlapEnd) continue;
    if (hour !== undefined && !(overlapStart <= hour && hour < overlapEnd)) continue;

    const [jqId, jqChinese, jqEnglish] = JIEQI_NAMES[jqIdx];

    return {
      type: isExtinction ? "four_extinction" : "four_separation",
      chinese: isExtinction ? "\u56db\u7d55" : "\u56db\u96e2",
      english: isExtinction ? "Four Extinction" : "Four Separation",
      solar_term_id: jqId,
      solar_term_chinese: jqChinese,
      solar_term_english: jqEnglish,
      forbidden_start_hour: Math.round(overlapStart * 100) / 100,
      forbidden_end_hour: Math.round(overlapEnd * 100) / 100,
    };
  }

  return null;
}

// =============================================================================
// HELPERS
// =============================================================================

function extractHourMinute(birthTime: string | null): [number | null, number | null] {
  if (!birthTime || birthTime === "unknown") return [null, null];

  if (!birthTime.includes(" - ") && birthTime.includes(":")) {
    const parts = birthTime.split(":");
    return [parseInt(parts[0], 10), parseInt(parts[1], 10)];
  }

  const hourRangeStart = birthTime.split(" - ")[0];
  const parts = hourRangeStart.split(":");
  return [parseInt(parts[0], 10), parseInt(parts[1], 10)];
}

function addYears(
  baseYear: number, baseMonth: number, baseDay: number, yearsToAdd: number,
): string {
  const ms = new Date(baseYear, baseMonth - 1, baseDay).getTime()
    + yearsToAdd * 365.25 * 24 * 60 * 60 * 1000;
  return new Date(ms).toISOString().split("T")[0];
}

// =============================================================================
// ANALYZE BAZI — extracted service function
// =============================================================================

export interface AnalyzeBaziInput {
  birth_date: string;
  birth_time?: string | null;
  gender: 'male' | 'female';
  analysis_year?: number | null;
  include_annual_luck?: boolean;
  analysis_month?: number | null;
  analysis_day?: number | null;
  analysis_time?: string | null;
  school?: string;
  location?: string | null;
  talisman_year_hs?: string | null;
  talisman_year_eb?: string | null;
  talisman_month_hs?: string | null;
  talisman_month_eb?: string | null;
  talisman_day_hs?: string | null;
  talisman_day_eb?: string | null;
  talisman_hour_hs?: string | null;
  talisman_hour_eb?: string | null;
}

export function analyzeBazi(input: AnalyzeBaziInput): Record<string, unknown> {
  const {
    birth_date: birthDateStr,
    birth_time: birthTime = null,
    gender,
    analysis_year: analysisYear = null,
    include_annual_luck: includeAnnualLuck = true,
    analysis_month: analysisMonth = null,
    analysis_day: analysisDay = null,
    analysis_time: analysisTime = null,
    school = 'classic',
  } = input;

  const [bdYear, bdMonth, bdDay] = birthDateStr.split("-").map(Number);

  const [hour, minute] = extractHourMinute(birthTime ?? null);

  // 1. Generate natal chart
  const natalChart = generateBaziChart(bdYear, bdMonth, bdDay, hour, minute);

  // 2. Start with natal chart dict
  const chartDict: Record<string, string> = {
    year_pillar: natalChart.year_pillar,
    month_pillar: natalChart.month_pillar,
    day_pillar: natalChart.day_pillar,
  };
  if (natalChart.hour_pillar) {
    chartDict.hour_pillar = natalChart.hour_pillar;
  }

  // 3. If analysis_year: generate luck + time period pillars
  interface LuckInfo {
    start_date: string;
    end_date: string;
    is_xiao_yun: boolean;
    chinese_age?: number;
    start_time?: string;
    end_time?: string;
  }
  let luck10yInfo: LuckInfo | null = null;
  let luckPillarsRaw: Array<{ pillar: string; start_age: number; end_age: number }> | null = null;
  let daYunStartAge: number | null = null;
  let annualPillarForDisplay: string | null = null;

  if (analysisYear) {
    luckPillarsRaw = generateLuckPillars(
      natalChart.year_pillar,
      natalChart.month_pillar,
      gender,
      { year: bdYear, month: bdMonth, day: bdDay },
    );

    daYunStartAge = luckPillarsRaw.length > 0 ? luckPillarsRaw[0].start_age : 0;
    const ageAtAnalysis = analysisYear - bdYear;

    if (ageAtAnalysis < daYunStartAge && natalChart.hour_pillar) {
      const xiaoYunPillars = generateXiaoYunPillars(
        natalChart.hour_pillar,
        natalChart.year_pillar,
        gender,
        daYunStartAge,
      );

      let found = false;
      for (const xp of xiaoYunPillars) {
        if (xp.start_age === ageAtAnalysis) {
          chartDict.luck_10_year = xp.pillar;
          const startDate = new Date(bdYear + ageAtAnalysis, bdMonth - 1, bdDay);
          const endDate = new Date(bdYear + ageAtAnalysis + 1, bdMonth - 1, bdDay);
          luck10yInfo = {
            start_date: startDate.toISOString().split("T")[0],
            end_date: endDate.toISOString().split("T")[0],
            is_xiao_yun: true,
            chinese_age: xp.chinese_age,
          };
          if (birthTime) {
            luck10yInfo.start_time = birthTime;
            luck10yInfo.end_time = birthTime;
          }
          found = true;
          break;
        }
      }

      if (!found && xiaoYunPillars.length > 0) {
        const firstXp = xiaoYunPillars[0];
        chartDict.luck_10_year = firstXp.pillar;
        const startDate = new Date(bdYear, bdMonth - 1, bdDay);
        const endDate = new Date(bdYear + 1, bdMonth - 1, bdDay);
        luck10yInfo = {
          start_date: startDate.toISOString().split("T")[0],
          end_date: endDate.toISOString().split("T")[0],
          is_xiao_yun: true,
          chinese_age: firstXp.chinese_age,
        };
        if (birthTime) {
          luck10yInfo.start_time = birthTime;
          luck10yInfo.end_time = birthTime;
        }
      }
    } else {
      for (const lp of luckPillarsRaw) {
        const startAge = lp.start_age;
        const endAge = startAge + 10;
        if (startAge <= ageAtAnalysis && ageAtAnalysis < endAge) {
          chartDict.luck_10_year = lp.pillar;
          const startDate = addYears(bdYear, bdMonth, bdDay, startAge);
          const endDate = addYears(bdYear, bdMonth, bdDay, endAge);
          luck10yInfo = {
            start_date: startDate,
            end_date: endDate,
            is_xiao_yun: false,
          };
          if (birthTime) {
            luck10yInfo.start_time = birthTime;
            luck10yInfo.end_time = birthTime;
          }
          break;
        }
      }

      if (!chartDict.luck_10_year && luckPillarsRaw.length > 0) {
        const firstLp = luckPillarsRaw[0];
        chartDict.luck_10_year = firstLp.pillar;
        const startAge = firstLp.start_age;
        const endAge = startAge + 10;
        const startDate = addYears(bdYear, bdMonth, bdDay, startAge);
        const endDate = addYears(bdYear, bdMonth, bdDay, endAge);
        luck10yInfo = {
          start_date: startDate,
          end_date: endDate,
          is_xiao_yun: false,
        };
        if (birthTime) {
          luck10yInfo.start_time = birthTime;
          luck10yInfo.end_time = birthTime;
        }
      }
    }

    const analysisMonthVal = analysisMonth || 2;
    const analysisDayVal = analysisDay || 15;

    let analysisHourVal: number | null = null;
    let analysisMinuteVal: number | null = null;
    if (analysisTime) {
      [analysisHourVal, analysisMinuteVal] = extractHourMinute(analysisTime);
    }

    const timePillars = generateBaziChart(
      analysisYear,
      analysisMonthVal,
      analysisDayVal,
      analysisHourVal,
      analysisMinuteVal,
    );

    annualPillarForDisplay = timePillars.year_pillar;

    if (includeAnnualLuck) {
      chartDict.yearly_luck = timePillars.year_pillar;
    }
    if (analysisMonth) {
      chartDict.monthly_luck = timePillars.month_pillar;
    }
    if (analysisDay) {
      chartDict.daily_luck = timePillars.day_pillar;
    }
    if (analysisTime && timePillars.hour_pillar) {
      chartDict.hourly_luck = timePillars.hour_pillar;
    }
  }

  // 4. Extract stems and branches
  const [yearStem, yearBranch] = natalChart.year_pillar.split(" ");
  const [monthStem, monthBranch] = natalChart.month_pillar.split(" ");
  const [dayStem, dayBranch] = natalChart.day_pillar.split(" ");

  let hourStem: string;
  let hourBranch: string;
  if (natalChart.hour_pillar) {
    [hourStem, hourBranch] = natalChart.hour_pillar.split(" ");
  } else {
    hourStem = dayStem;
    hourBranch = dayBranch;
  }

  let lpStem = "";
  let lpBranch = "";
  if (chartDict.luck_10_year) {
    [lpStem, lpBranch] = chartDict.luck_10_year.split(" ");
  }

  const luckPillarsList: Array<Record<string, unknown>> = [];
  if (luckPillarsRaw) {
    for (const lpData of luckPillarsRaw) {
      const [lps, lpb] = lpData.pillar.split(" ");
      luckPillarsList.push({
        stem: lps,
        branch: lpb,
        start_age: lpData.start_age,
        end_age: lpData.start_age + 10,
        start_year: bdYear + lpData.start_age,
        end_year: bdYear + lpData.start_age + 10,
      });
    }
  }

  // 5. Extract time-period stems/branches
  let tpAnnualStem = "", tpAnnualBranch = "";
  let tpMonthlyStem = "", tpMonthlyBranch = "";
  let tpDailyStem = "", tpDailyBranch = "";
  let tpHourlyStem = "", tpHourlyBranch = "";

  if (chartDict.yearly_luck) {
    [tpAnnualStem, tpAnnualBranch] = chartDict.yearly_luck.split(" ");
  }
  if (chartDict.monthly_luck) {
    [tpMonthlyStem, tpMonthlyBranch] = chartDict.monthly_luck.split(" ");
  }
  if (chartDict.daily_luck) {
    [tpDailyStem, tpDailyBranch] = chartDict.daily_luck.split(" ");
  }
  if (chartDict.hourly_luck) {
    [tpHourlyStem, tpHourlyBranch] = chartDict.hourly_luck.split(" ");
  }

  // Build comprehensive chart and run analysis
  const comprehensiveChart = buildChart({
    gender,
    birth_year: bdYear,
    year_stem: yearStem, year_branch: yearBranch,
    month_stem: monthStem, month_branch: monthBranch,
    day_stem: dayStem, day_branch: dayBranch,
    hour_stem: hourStem, hour_branch: hourBranch,
    luck_pillar_stem: lpStem,
    luck_pillar_branch: lpBranch,
    luck_pillars: luckPillarsList,
    current_year: analysisYear || new Date().getFullYear(),
    annual_stem: tpAnnualStem, annual_branch: tpAnnualBranch,
    monthly_stem: tpMonthlyStem, monthly_branch: tpMonthlyBranch,
    daily_stem: tpDailyStem, daily_branch: tpDailyBranch,
    hourly_stem: tpHourlyStem, hourly_branch: tpHourlyBranch,
  });

  const results = analyzeForApi(comprehensiveChart);

  // 6. Build response with adapter
  const response: Record<string, unknown> = {
    birth_info: {
      date: birthDateStr,
      time: birthTime || "Unknown",
      gender,
    },
    analysis_info: {
      year: analysisYear,
      month: analysisMonth,
      day: analysisDay,
      time: analysisTime,
      has_luck_pillar: !!chartDict.luck_10_year,
      has_annual: !!chartDict.yearly_luck,
      has_monthly: !!chartDict.monthly_luck,
      has_daily: !!chartDict.daily_luck,
      has_hourly: !!chartDict.hourly_luck,
      annual_disabled: analysisYear != null && !includeAnnualLuck,
      is_xiao_yun: luck10yInfo?.is_xiao_yun ?? false,
      da_yun_start_age: daYunStartAge,
    },
  };

  const adapted = adaptToFrontend(comprehensiveChart, results);
  Object.assign(response, adapted);

  // If annual luck was disabled but year was provided, add display-only nodes
  if (analysisYear && !includeAnnualLuck && annualPillarForDisplay) {
    const [annualHs, annualEb] = annualPillarForDisplay.split(" ");
    response.hs_yl = {
      id: annualHs,
      base: { id: annualHs, qi: { [annualHs]: 100.0 } },
      interaction_ids: [],
      post: { id: annualHs, qi: { [annualHs]: 100.0 } },
      badges: [],
      disabled: true,
    };
    const ebData = BRANCHES[annualEb as BranchName];
    const ebQi: Record<string, number> = {};
    if (ebData) {
      for (const [stemId, score] of ebData.qi) {
        ebQi[stemId] = score;
      }
    }
    response.eb_yl = {
      id: annualEb,
      base: { id: annualEb, qi: ebQi },
      interaction_ids: [],
      post: { id: annualEb, qi: { ...ebQi } },
      badges: [],
      disabled: true,
    };
  }

  // Add misc field to 10-year luck nodes if they exist
  if (luck10yInfo && response.hs_10yl && response.eb_10yl) {
    (response.hs_10yl as Record<string, unknown>).misc = luck10yInfo;
    (response.eb_10yl as Record<string, unknown>).misc = luck10yInfo;
  }

  // Add Dong Gong Date Selection info when daily luck is present
  if (analysisYear && analysisMonth && analysisDay &&
      chartDict.daily_luck && chartDict.monthly_luck) {
    const [dgDailyStem, dgDailyBranch] = chartDict.daily_luck.split(" ");
    const [, dgMonthlyBranch] = chartDict.monthly_luck.split(" ");

    const chineseMonth = DONG_GONG_BRANCH_TO_MONTH[dgMonthlyBranch as BranchName];

    if (chineseMonth && dgMonthlyBranch) {
      const dayOfficer = getDongGongOfficer(dgMonthlyBranch, dgDailyBranch);
      const officerInfo = dayOfficer ? DONG_GONG_DAY_OFFICERS[dayOfficer] : null;

      const rating = getDongGongRating(chineseMonth, dgDailyBranch, dgDailyStem);
      const ratingInfo = rating ? DONG_GONG_RATINGS[rating] : null;

      const dayInfo = getDongGongDayInfo(chineseMonth, dgDailyBranch);

      const dongGongData: Record<string, unknown> = {
        month: chineseMonth,
        month_branch: dgMonthlyBranch,
        month_chinese: DONG_GONG_MONTHS[chineseMonth]?.chinese ?? "",
        day_stem: dgDailyStem,
        day_branch: dgDailyBranch,
        pillar: chartDict.daily_luck,
        officer: dayOfficer ? {
          id: dayOfficer,
          chinese: officerInfo?.chinese ?? "",
          english: officerInfo?.english ?? "",
        } : null,
        rating: ratingInfo ? {
          id: rating,
          value: ratingInfo.value,
          symbol: ratingInfo.symbol,
          chinese: ratingInfo.chinese,
        } : null,
        good_for: dayInfo?.good_for ?? [],
        bad_for: dayInfo?.bad_for ?? [],
        description_chinese: dayInfo?.description_chinese ?? "",
        description_english: dayInfo?.description_english ?? "",
      };

      let analysisHourFloat: number | undefined;
      if (analysisTime) {
        const [ah, am] = extractHourMinute(analysisTime);
        if (ah != null) {
          analysisHourFloat = ah + (am ?? 0) / 60;
        }
      }

      const forbidden = checkFourExtinctionSeparation(
        analysisYear, analysisMonth, analysisDay, analysisHourFloat,
      );

      if (forbidden) {
        dongGongData.forbidden = forbidden;
        dongGongData.consult = null;
        dongGongData.rating = {
          id: "dire",
          value: 1,
          symbol: "\u2717",
          chinese: forbidden.chinese,
        };
      } else {
        dongGongData.forbidden = null;
        const consult = checkConsultPromotion(rating ?? "", dayInfo);
        if (consult) {
          dongGongData.consult = {
            promoted: true,
            original_rating: dongGongData.rating,
            reason: consult.reason,
          };
          dongGongData.rating = { id: "consult", value: 2.5, symbol: "?", chinese: "\u8b70" };
        } else {
          dongGongData.consult = null;
        }
      }

      response.dong_gong = dongGongData;
    }
  }

  response.school = school;

  return response;
}
