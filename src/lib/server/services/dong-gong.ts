import { Solar } from 'lunar-typescript';
import {
  getDongGongOfficer, getDongGongRating, getDongGongDayInfo, checkConsultPromotion,
  DONG_GONG_RATINGS, DONG_GONG_DAY_OFFICERS, DONG_GONG_MONTHS, DONG_GONG_BRANCH_TO_MONTH,
} from '$lib/bazi/dong-gong';
import type { BranchName } from '$lib/bazi/core';
import { checkFourExtinctionSeparation } from './bazi';

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

function getMoonPhase(lunarDayNum: number): { emoji: string; english: string; chinese: string; lunar_day: number } {
  for (const [start, end, emoji, english, chinese] of MOON_PHASES) {
    if (start <= lunarDayNum && lunarDayNum <= end) {
      return { emoji, english, chinese, lunar_day: lunarDayNum };
    }
  }
  return { emoji: "\ud83c\udf11", english: "New Moon", chinese: "\u65b0\u6708", lunar_day: lunarDayNum };
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
// DONG GONG CALENDAR — extracted service function
// =============================================================================

export interface DongGongCalendarInput {
  year: number;
  month: number;
}

export interface DongGongDayResult {
  day: number;
  weekday: number;
  day_stem: string;
  day_branch: string;
  day_stem_chinese: string;
  day_branch_chinese: string;
  pillar: string;
  year_stem: string;
  year_branch: string;
  year_stem_chinese: string;
  year_branch_chinese: string;
  chinese_month: number | null;
  chinese_month_name: string;
  officer: { id: string; chinese: string; english: string } | null;
  rating: { id: string; value: number; symbol: string; chinese: string } | null;
  good_for: string[];
  bad_for: string[];
  description_chinese: string;
  description_english: string;
  consult: { promoted: boolean; original_rating: { id: string; value: number; symbol: string; chinese: string } | null; reason: string } | null;
  forbidden: {
    type: string;
    chinese: string;
    english: string;
    solar_term_id: string;
    solar_term_chinese: string;
    solar_term_english: string;
    forbidden_start_hour: number;
    forbidden_end_hour: number;
  } | null;
  moon_phase: { emoji: string; english: string; chinese: string; lunar_day: number };
}

export interface DongGongCalendarResult {
  year: number;
  month: number;
  first_day_weekday: number;
  days_in_month: number;
  days: DongGongDayResult[];
  chinese_months_spanned: Array<{
    month: number;
    chinese: string;
    branch: string;
    stem: string;
    stem_chinese: string;
    branch_id: string;
    branch_chinese: string;
  }>;
  chinese_years_spanned: Array<{
    stem: string;
    stem_chinese: string;
    branch: string;
    branch_chinese: string;
  }>;
}

export function getDongGongCalendar(input: DongGongCalendarInput): DongGongCalendarResult {
  const { year, month } = input;

  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDayWeekday = new Date(year, month - 1, 1).getDay();

  const days: DongGongDayResult[] = [];
  const chineseMonthsSeen: Record<number, DongGongCalendarResult['chinese_months_spanned'][0]> = {};
  const chineseYearsSeen: Record<string, DongGongCalendarResult['chinese_years_spanned'][0]> = {};

  for (let day = 1; day <= daysInMonth; day++) {
    const solar = Solar.fromYmd(year, month, day);
    const lunar = solar.getLunar();
    const ec = lunar.getEightChar();

    const yearGanzhi = parseGanzhi(ec.getYear());

    const yrKey = `${yearGanzhi.stem}${yearGanzhi.branch}`;
    if (!(yrKey in chineseYearsSeen)) {
      chineseYearsSeen[yrKey] = {
        stem: yearGanzhi.stem,
        stem_chinese: yearGanzhi.stemChinese,
        branch: yearGanzhi.branch,
        branch_chinese: yearGanzhi.branchChinese,
      };
    }

    const monthGanzhi = parseGanzhi(ec.getMonth());
    const dayGanzhi = parseGanzhi(ec.getDay());

    const chineseMonth = DONG_GONG_BRANCH_TO_MONTH[monthGanzhi.branch as BranchName] ?? null;

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

    const lunarDay = lunar.getDay();

    const dayObj: DongGongDayResult = {
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
      officer: null,
      rating: null,
      good_for: [],
      bad_for: [],
      description_chinese: "",
      description_english: "",
      consult: null,
      forbidden: null,
      moon_phase: getMoonPhase(lunarDay),
    };

    if (chineseMonth != null && monthGanzhi.branch) {
      const dayOfficer = getDongGongOfficer(monthGanzhi.branch, dayGanzhi.branch);
      const officerInfo = dayOfficer ? DONG_GONG_DAY_OFFICERS[dayOfficer] : null;
      dayObj.officer = dayOfficer ? {
        id: dayOfficer,
        chinese: officerInfo?.chinese ?? "",
        english: officerInfo?.english ?? "",
      } : null;

      const rating = getDongGongRating(chineseMonth, dayGanzhi.branch, dayGanzhi.stem);
      if (rating) {
        const ratingInfo = DONG_GONG_RATINGS[rating];
        dayObj.rating = {
          id: rating,
          value: ratingInfo.value,
          symbol: ratingInfo.symbol,
          chinese: ratingInfo.chinese,
        };
      }

      const dayInfo = getDongGongDayInfo(chineseMonth, dayGanzhi.branch);
      dayObj.good_for = [...(dayInfo?.good_for ?? [])];
      dayObj.bad_for = [...(dayInfo?.bad_for ?? [])];
      dayObj.description_chinese = dayInfo?.description_chinese ?? "";
      dayObj.description_english = dayInfo?.description_english ?? "";

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
        }
      }
    }

    days.push(dayObj);
  }

  return {
    year,
    month,
    first_day_weekday: firstDayWeekday,
    days_in_month: daysInMonth,
    days,
    chinese_months_spanned: Object.values(chineseMonthsSeen),
    chinese_years_spanned: Object.values(chineseYearsSeen),
  };
}
