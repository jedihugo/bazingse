// =============================================================================
// BAZI CHART CALCULATOR — TypeScript port using lunar-typescript
// =============================================================================
// Generates the Four Pillars (year, month, day, hour) and luck pillars.
// This module is self-contained: no dependency on core.ts / derived.ts
// (which carry 'server-only') so it can be used in tests and edge runtime.
// =============================================================================

import { Solar } from 'lunar-typescript';

// ---------------------------------------------------------------------------
// Chinese character -> Pinyin lookup (same order as core.ts)
// ---------------------------------------------------------------------------

const STEM_CN_TO_PINYIN: Record<string, string> = {
  '甲': 'Jia', '乙': 'Yi', '丙': 'Bing', '丁': 'Ding', '戊': 'Wu',
  '己': 'Ji', '庚': 'Geng', '辛': 'Xin', '壬': 'Ren', '癸': 'Gui',
};

const BRANCH_CN_TO_PINYIN: Record<string, string> = {
  '子': 'Zi', '丑': 'Chou', '寅': 'Yin', '卯': 'Mao', '辰': 'Chen', '巳': 'Si',
  '午': 'Wu', '未': 'Wei', '申': 'Shen', '酉': 'You', '戌': 'Xu', '亥': 'Hai',
};

// ---------------------------------------------------------------------------
// 60-pillar (Jia Zi) cycle
// ---------------------------------------------------------------------------

const HEAVENLY_STEMS = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'] as const;
const EARTHLY_BRANCHES = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai'] as const;

const SIXTY_PILLARS: string[] = [];
for (let i = 0; i < 60; i++) {
  SIXTY_PILLARS.push(`${HEAVENLY_STEMS[i % 10]} ${EARTHLY_BRANCHES[i % 12]}`);
}

// ---------------------------------------------------------------------------
// Helper: parse a 2-char Chinese ganzhi string to "Stem Branch" pinyin
// ---------------------------------------------------------------------------

function parsePillar(ganzhi: string): string {
  const stem = STEM_CN_TO_PINYIN[ganzhi[0]];
  const branch = BRANCH_CN_TO_PINYIN[ganzhi[1]];
  if (!stem || !branch) {
    throw new Error(`Cannot parse ganzhi: "${ganzhi}"`);
  }
  return `${stem} ${branch}`;
}

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface BaziChart {
  year_pillar: string;   // e.g. "Jia Zi"
  month_pillar: string;
  day_pillar: string;
  hour_pillar?: string;  // undefined when birth hour unknown
}

export interface LuckPillar {
  pillar: string;
  start_age: number;
  end_age: number;
}

export interface XiaoYunPillar {
  pillar: string;
  chinese_age: number;
  start_age: number;
  end_age: number;
  is_xiao_yun: true;
}

// ---------------------------------------------------------------------------
// generateBaziChart
// ---------------------------------------------------------------------------
// lunar-typescript's EightChar handles solar term boundaries for year/month
// pillars automatically when given exact time via Solar.fromYmdHms().
// Day pillar at 23:00+: lunar-typescript does NOT auto-advance the day,
// so we manually create a next-day Solar to get the correct day pillar.
// ---------------------------------------------------------------------------

export function generateBaziChart(
  year: number,
  month: number,
  day: number,
  hour?: number | null,
  minute?: number | null,
): BaziChart {
  const hasTime = hour != null;
  const h = hour ?? 0;
  const m = minute ?? 0;

  // Create Solar object — with or without time
  const solar = hasTime
    ? Solar.fromYmdHms(year, month, day, h, m, 0)
    : Solar.fromYmd(year, month, day);

  const lunar = solar.getLunar();
  const eightChar = lunar.getEightChar();

  // Year pillar — lunar-typescript respects Li Chun boundary with exact time
  const yearPillar = parsePillar(eightChar.getYear());

  // Month pillar — lunar-typescript respects Jie (节) boundaries with exact time
  const monthPillar = parsePillar(eightChar.getMonth());

  // Day pillar — BaZi day starts at 23:00 (Zi hour of next day)
  let dayPillar: string;
  if (hasTime && h >= 23) {
    // Advance to next calendar day for the day pillar
    const nextSolar = Solar.fromYmdHms(year, month, day + 1, 0, 0, 0);
    const nextLunar = nextSolar.getLunar();
    const nextEightChar = nextLunar.getEightChar();
    dayPillar = parsePillar(nextEightChar.getDay());
  } else {
    dayPillar = parsePillar(eightChar.getDay());
  }

  const result: BaziChart = {
    year_pillar: yearPillar,
    month_pillar: monthPillar,
    day_pillar: dayPillar,
  };

  // Hour pillar — only when birth hour is known
  if (hasTime) {
    result.hour_pillar = parsePillar(eightChar.getTime());
  }

  return result;
}

// ---------------------------------------------------------------------------
// generateLuckPillars (Da Yun 大運)
// ---------------------------------------------------------------------------
// Uses lunar-typescript's getNextJie() / getPrevJie() to find the nearest
// major solar term (Jie 節), then calculates start age from day difference.
//
// Direction rules:
//   Yang year stem + male = forward (順排)
//   Yin year stem + female = forward
//   Otherwise = backward (逆排)
//
// Each 3 days of difference = 1 year of Da Yun start age (ceiling).
// ---------------------------------------------------------------------------

export function generateLuckPillars(
  yearPillar: string,
  monthPillar: string,
  gender: 'male' | 'female',
  dob: { year: number; month: number; day: number },
): LuckPillar[] {
  // Find month pillar index in the 60-pillar cycle
  const monthIndex = SIXTY_PILLARS.indexOf(monthPillar);
  if (monthIndex === -1) {
    throw new Error(`Month pillar "${monthPillar}" not found in sixty-pillar cycle`);
  }

  // Determine direction
  const yearStem = yearPillar.split(' ')[0];
  const isYangYear = ['Jia', 'Bing', 'Wu', 'Geng', 'Ren'].includes(yearStem);
  const forward = (gender === 'male') === isYangYear;

  // Use lunar-typescript to find next/prev Jie
  const solar = Solar.fromYmd(dob.year, dob.month, dob.day);
  const lunar = solar.getLunar();

  let daysDiff: number;
  if (forward) {
    const nextJie = lunar.getNextJie();
    const jieSolar = nextJie.getSolar();
    const jieDate = new Date(jieSolar.getYear(), jieSolar.getMonth() - 1, jieSolar.getDay());
    const birthDate = new Date(dob.year, dob.month - 1, dob.day);
    daysDiff = Math.round((jieDate.getTime() - birthDate.getTime()) / (1000 * 60 * 60 * 24));
  } else {
    const prevJie = lunar.getPrevJie();
    const jieSolar = prevJie.getSolar();
    const jieDate = new Date(jieSolar.getYear(), jieSolar.getMonth() - 1, jieSolar.getDay());
    const birthDate = new Date(dob.year, dob.month - 1, dob.day);
    daysDiff = Math.round((birthDate.getTime() - jieDate.getTime()) / (1000 * 60 * 60 * 24));
  }

  const startAge = Math.ceil(daysDiff / 3.0);

  // Generate 8 luck pillars
  const result: LuckPillar[] = [];
  for (let i = 0; i < 8; i++) {
    let luckIndex: number;
    if (forward) {
      luckIndex = ((monthIndex + i + 1) % 60 + 60) % 60;
    } else {
      luckIndex = ((monthIndex - i - 1) % 60 + 60) % 60;
    }

    result.push({
      pillar: SIXTY_PILLARS[luckIndex],
      start_age: startAge + (i * 10),
      end_age: startAge + ((i + 1) * 10) - 1,
    });
  }

  return result;
}

// ---------------------------------------------------------------------------
// generateXiaoYunPillars (小運 - Xiao Yun / Xing Nian 行年)
// ---------------------------------------------------------------------------
// Covers childhood years BEFORE Da Yun begins.
// Calculated from HOUR PILLAR (not month), each pillar = 1 year.
// Uses Chinese age (虛歲): age 1 = birth year.
// ---------------------------------------------------------------------------

export function generateXiaoYunPillars(
  hourPillar: string,
  yearPillar: string,
  gender: 'male' | 'female',
  daYunStartAge: number,
): XiaoYunPillar[] {
  // Find hour pillar index in the 60-pillar cycle
  const hourIndex = SIXTY_PILLARS.indexOf(hourPillar);
  if (hourIndex === -1) {
    throw new Error(`Hour pillar "${hourPillar}" not found in sixty-pillar cycle`);
  }

  // Determine direction — same rules as Da Yun
  const yearStem = yearPillar.split(' ')[0];
  const isYangYear = ['Jia', 'Bing', 'Wu', 'Geng', 'Ren'].includes(yearStem);
  const forward = (gender === 'male') === isYangYear;

  const result: XiaoYunPillar[] = [];
  for (let chineseAge = 1; chineseAge <= daYunStartAge; chineseAge++) {
    let xiaoYunIndex: number;
    if (forward) {
      xiaoYunIndex = ((hourIndex + chineseAge) % 60 + 60) % 60;
    } else {
      xiaoYunIndex = ((hourIndex - chineseAge) % 60 + 60) % 60;
    }

    const westernAge = chineseAge - 1;

    result.push({
      pillar: SIXTY_PILLARS[xiaoYunIndex],
      chinese_age: chineseAge,
      start_age: westernAge,
      end_age: westernAge,
      is_xiao_yun: true,
    });
  }

  return result;
}
