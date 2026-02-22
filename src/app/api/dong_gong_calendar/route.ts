import { NextRequest, NextResponse } from 'next/server';
import { Solar } from 'lunar-typescript';
import {
  getDongGongOfficer, getDongGongRating, getDongGongDayInfo, checkConsultPromotion,
  DONG_GONG_RATINGS, DONG_GONG_DAY_OFFICERS, DONG_GONG_MONTHS, DONG_GONG_BRANCH_TO_MONTH,
} from '@/lib/bazi/dong-gong';
import type { BranchName } from '@/lib/bazi/core';


// =============================================================================
// CHINESE -> PINYIN MAPS
// =============================================================================

const STEM_MAP: Record<string, string> = {
  '\u7532': 'Jia', '\u4e59': 'Yi', '\u4e19': 'Bing', '\u4e01': 'Ding', '\u620a': 'Wu',
  '\u5df1': 'Ji', '\u5e9a': 'Geng', '\u8f9b': 'Xin', '\u58ec': 'Ren', '\u7678': 'Gui',
};

const BRANCH_MAP: Record<string, string> = {
  '\u5b50': 'Zi', '\u4e11': 'Chou', '\u5bc5': 'Yin', '\u536f': 'Mao',
  '\u8fb0': 'Chen', '\u5df3': 'Si', '\u5348': 'Wu', '\u672a': 'Wei',
  '\u7533': 'Shen', '\u9149': 'You', '\u620c': 'Xu', '\u4ea5': 'Hai',
};


// =============================================================================
// MOON PHASES
// =============================================================================

const MOON_PHASES: Array<[number, number, string, string, string]> = [
  [1,  1,  "\ud83c\udf11", "New Moon",        "\u65b0\u6708"],
  [2,  6,  "\ud83c\udf12", "Waxing Crescent", "\u86fe\u7709\u6708"],
  [7,  8,  "\ud83c\udf13", "First Quarter",   "\u4e0a\u5f26\u6708"],
  [9,  14, "\ud83c\udf14", "Waxing Gibbous",  "\u76c8\u51f8\u6708"],
  [15, 15, "\ud83c\udf15", "Full Moon",        "\u6ee1\u6708"],
  [16, 21, "\ud83c\udf16", "Waning Gibbous",  "\u4e8f\u51f8\u6708"],
  [22, 23, "\ud83c\udf17", "Last Quarter",     "\u4e0b\u5f26\u6708"],
  [24, 30, "\ud83c\udf18", "Waning Crescent", "\u6b8b\u6708"],
];

function getMoonPhase(lunarDayNum: number): Record<string, unknown> {
  for (const [start, end, emoji, english, chinese] of MOON_PHASES) {
    if (start <= lunarDayNum && lunarDayNum <= end) {
      return { emoji, english, chinese, lunar_day: lunarDayNum };
    }
  }
  return { emoji: "\ud83c\udf11", english: "New Moon", chinese: "\u65b0\u6708", lunar_day: lunarDayNum };
}


// =============================================================================
// FOUR EXTINCTION / FOUR SEPARATION (shared logic)
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

function checkFourExtinctionSeparation(
  year: number, month: number, day: number, hour?: number,
): Record<string, unknown> | null {
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
// HELPER: parse 2-char ganzhi to pinyin parts
// =============================================================================

function parseGanzhi(ganzhi: string): { stem: string; branch: string; stemChinese: string; branchChinese: string } {
  const stemChinese = ganzhi[0];
  const branchChinese = ganzhi[1];
  return {
    stem: STEM_MAP[stemChinese] ?? stemChinese,
    branch: BRANCH_MAP[branchChinese] ?? branchChinese,
    stemChinese,
    branchChinese,
  };
}


// =============================================================================
// GET /api/dong_gong_calendar
// =============================================================================

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;

  const yearStr = params.get("year");
  const monthStr = params.get("month");

  if (!yearStr || !monthStr) {
    return NextResponse.json(
      { error: "year and month are required" },
      { status: 400 },
    );
  }

  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);

  if (month < 1 || month > 12) {
    return NextResponse.json(
      { error: "month must be between 1 and 12" },
      { status: 400 },
    );
  }

  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDayWeekday = new Date(year, month - 1, 1).getDay(); // 0=Sun already

  const days: Array<Record<string, unknown>> = [];
  const chineseMonthsSeen: Record<number, Record<string, unknown>> = {};
  const chineseYearsSeen: Record<string, Record<string, unknown>> = {};

  for (let day = 1; day <= daysInMonth; day++) {
    const solar = Solar.fromYmd(year, month, day);
    const lunar = solar.getLunar();
    const ec = lunar.getEightChar();

    // Year pillar (changes at Li Chun, not Jan 1)
    const yearGanzhi = parseGanzhi(ec.getYear());

    // Track Chinese years
    const yrKey = `${yearGanzhi.stem}${yearGanzhi.branch}`;
    if (!(yrKey in chineseYearsSeen)) {
      chineseYearsSeen[yrKey] = {
        stem: yearGanzhi.stem,
        stem_chinese: yearGanzhi.stemChinese,
        branch: yearGanzhi.branch,
        branch_chinese: yearGanzhi.branchChinese,
      };
    }

    // Month pillar (handles jieqi boundaries automatically)
    const monthGanzhi = parseGanzhi(ec.getMonth());

    // Day pillar
    const dayGanzhi = parseGanzhi(ec.getDay());

    // Chinese month number from branch
    const chineseMonth = DONG_GONG_BRANCH_TO_MONTH[monthGanzhi.branch as BranchName] ?? null;

    // Track Chinese months
    if (chineseMonth != null && !(chineseMonth in chineseMonthsSeen)) {
      const monthInfo = DONG_GONG_MONTHS[chineseMonth];
      chineseMonthsSeen[chineseMonth] = {
        month: chineseMonth,
        chinese: monthInfo?.chinese ?? "",
        branch: monthInfo?.branch ?? "",
        stem: monthGanzhi.stem,
        stem_chinese: monthGanzhi.stemChinese,
        branch_id: monthGanzhi.branch,
        branch_chinese: monthGanzhi.branchChinese,
      };
    }

    // Lunar day for moon phase
    const lunarDay = lunar.getDay();

    // Build day object
    const dayObj: Record<string, unknown> = {
      day,
      weekday: (firstDayWeekday + day - 1) % 7,
      day_stem: dayGanzhi.stem,
      day_branch: dayGanzhi.branch,
      day_stem_chinese: dayGanzhi.stemChinese,
      day_branch_chinese: dayGanzhi.branchChinese,
      pillar: `${dayGanzhi.stem} ${dayGanzhi.branch}`,
      year_stem: yearGanzhi.stem,
      year_branch: yearGanzhi.branch,
      year_stem_chinese: yearGanzhi.stemChinese,
      year_branch_chinese: yearGanzhi.branchChinese,
      chinese_month: chineseMonth,
      chinese_month_name: chineseMonth != null
        ? (DONG_GONG_MONTHS[chineseMonth]?.chinese ?? "")
        : "",
      moon_phase: getMoonPhase(lunarDay),
    };

    if (chineseMonth != null && monthGanzhi.branch) {
      // Day officer
      const dayOfficer = getDongGongOfficer(monthGanzhi.branch, dayGanzhi.branch);
      const officerInfo = dayOfficer ? DONG_GONG_DAY_OFFICERS[dayOfficer] : null;
      dayObj.officer = dayOfficer ? {
        id: dayOfficer,
        chinese: officerInfo?.chinese ?? "",
        english: officerInfo?.english ?? "",
      } : null;

      // Rating
      const rating = getDongGongRating(chineseMonth, dayGanzhi.branch, dayGanzhi.stem);
      if (rating) {
        const ratingInfo = DONG_GONG_RATINGS[rating];
        dayObj.rating = {
          id: rating,
          value: ratingInfo.value,
          symbol: ratingInfo.symbol,
          chinese: ratingInfo.chinese,
        };
      } else {
        dayObj.rating = null;
      }

      // Day info (good_for, bad_for, descriptions)
      const dayInfo = getDongGongDayInfo(chineseMonth, dayGanzhi.branch);
      dayObj.good_for = dayInfo?.good_for ?? [];
      dayObj.bad_for = dayInfo?.bad_for ?? [];
      dayObj.description_chinese = dayInfo?.description_chinese ?? "";
      dayObj.description_english = dayInfo?.description_english ?? "";

      // Four Extinction / Four Separation (no hour for calendar)
      const forbidden = checkFourExtinctionSeparation(year, month, day);
      dayObj.forbidden = forbidden;

      if (forbidden) {
        dayObj.consult = null;
      } else {
        const consult = checkConsultPromotion(rating ?? "", dayInfo);
        if (consult) {
          dayObj.consult = {
            promoted: true,
            original_rating: dayObj.rating,
            reason: consult.reason,
          };
          dayObj.rating = { id: "consult", value: 2.5, symbol: "?", chinese: "\u8b70" };
        } else {
          dayObj.consult = null;
        }
      }
    } else {
      dayObj.officer = null;
      dayObj.rating = null;
      dayObj.good_for = [];
      dayObj.bad_for = [];
      dayObj.description_chinese = "";
      dayObj.description_english = "";
      dayObj.consult = null;
      dayObj.forbidden = null;
    }

    days.push(dayObj);
  }

  return NextResponse.json({
    year,
    month,
    first_day_weekday: firstDayWeekday,
    days_in_month: daysInMonth,
    days,
    chinese_months_spanned: Object.values(chineseMonthsSeen),
    chinese_years_spanned: Object.values(chineseYearsSeen),
  });
}
