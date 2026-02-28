/**
 * Generate pillar data using lunar-typescript for comparison with sxtwl.
 * Outputs JSON to stdout.
 */
import { Solar, Lunar, EightChar } from 'lunar-typescript';

// Stem index → pinyin (matching sxtwl's ordering)
const STEM_PINYIN = ['Jia', 'Yi', 'Bing', 'Ding', 'Wu', 'Ji', 'Geng', 'Xin', 'Ren', 'Gui'];
const BRANCH_PINYIN = ['Zi', 'Chou', 'Yin', 'Mao', 'Chen', 'Si', 'Wu', 'Wei', 'Shen', 'You', 'Xu', 'Hai'];

// Chinese character → pinyin lookup
const STEM_MAP: Record<string, string> = {
  '甲': 'Jia', '乙': 'Yi', '丙': 'Bing', '丁': 'Ding', '戊': 'Wu',
  '己': 'Ji', '庚': 'Geng', '辛': 'Xin', '壬': 'Ren', '癸': 'Gui',
};
const BRANCH_MAP: Record<string, string> = {
  '子': 'Zi', '丑': 'Chou', '寅': 'Yin', '卯': 'Mao', '辰': 'Chen', '巳': 'Si',
  '午': 'Wu', '未': 'Wei', '申': 'Shen', '酉': 'You', '戌': 'Xu', '亥': 'Hai',
};

interface TestCase {
  year: number;
  month: number;
  day: number;
  hour: number | null;
  minute: number | null;
  desc: string;
}

// Same test cases as the Python script
const TEST_CASES: TestCase[] = [
  { year: 1990, month: 1, day: 15, hour: 10, minute: 30, desc: "Normal date 1990" },
  { year: 2000, month: 6, day: 15, hour: 14, minute: 0, desc: "Normal date 2000" },
  { year: 2024, month: 3, day: 20, hour: 8, minute: 45, desc: "Normal date 2024" },
  { year: 1985, month: 12, day: 25, hour: 6, minute: 0, desc: "Christmas 1985" },
  { year: 1976, month: 7, day: 4, hour: 12, minute: 0, desc: "Midday 1976" },

  { year: 2024, month: 2, day: 4, hour: 3, minute: 0, desc: "Before Li Chun 2024 (Feb 4 ~16:27)" },
  { year: 2024, month: 2, day: 4, hour: 17, minute: 0, desc: "After Li Chun 2024" },
  { year: 2025, month: 2, day: 3, hour: 10, minute: 0, desc: "Before Li Chun 2025 (Feb 3 ~22:10)" },
  { year: 2025, month: 2, day: 3, hour: 23, minute: 0, desc: "After Li Chun 2025 + day crossover" },
  { year: 2026, month: 2, day: 4, hour: 3, minute: 0, desc: "Before Li Chun 2026 (Feb 4 ~04:02)" },
  { year: 2026, month: 2, day: 4, hour: 5, minute: 0, desc: "After Li Chun 2026" },

  { year: 1995, month: 8, day: 10, hour: 23, minute: 30, desc: "Late night - day changes at 23:00" },
  { year: 2000, month: 1, day: 1, hour: 23, minute: 0, desc: "New Year midnight boundary" },
  { year: 2010, month: 6, day: 15, hour: 22, minute: 59, desc: "Just before day change" },
  { year: 2010, month: 6, day: 15, hour: 23, minute: 0, desc: "Exactly at day change" },

  { year: 2024, month: 3, day: 5, hour: 10, minute: 0, desc: "Near Jingzhe 2024 (Awakening of Insects)" },
  { year: 2024, month: 4, day: 4, hour: 15, minute: 0, desc: "Near Qingming 2024 (Clear and Bright)" },
  { year: 2024, month: 5, day: 5, hour: 8, minute: 0, desc: "Near Lixia 2024 (Start of Summer)" },
  { year: 2024, month: 6, day: 21, hour: 4, minute: 0, desc: "Near Xiazhi 2024 (Summer Solstice)" },
  { year: 2024, month: 12, day: 21, hour: 18, minute: 0, desc: "Near Dongzhi 2024 (Winter Solstice)" },

  { year: 1950, month: 3, day: 15, hour: 9, minute: 0, desc: "1950 date" },
  { year: 1960, month: 11, day: 8, hour: 16, minute: 30, desc: "1960 date" },
  { year: 2030, month: 7, day: 20, hour: 11, minute: 0, desc: "Future date 2030" },

  { year: 1988, month: 9, day: 22, hour: null, minute: null, desc: "No birth time" },
  { year: 2024, month: 1, day: 1, hour: null, minute: null, desc: "New Year 2024 no time" },

  { year: 2024, month: 1, day: 6, hour: 5, minute: 0, desc: "Near Xiaohan 2024 (Minor Cold)" },
  { year: 2024, month: 8, day: 7, hour: 8, minute: 0, desc: "Near Liqiu 2024 (Start of Autumn)" },
  { year: 2024, month: 11, day: 7, hour: 6, minute: 0, desc: "Near Lidong 2024 (Start of Winter)" },
];

function parsePillar(ganzhiStr: string): string {
  // ganzhiStr is like "甲子" — 2 characters: stem + branch
  const stem = STEM_MAP[ganzhiStr[0]];
  const branch = BRANCH_MAP[ganzhiStr[1]];
  if (!stem || !branch) {
    throw new Error(`Cannot parse ganzhi: "${ganzhiStr}" (stem=${ganzhiStr[0]}, branch=${ganzhiStr[1]})`);
  }
  return `${stem} ${branch}`;
}

function getPillars(year: number, month: number, day: number, hour: number | null, minute: number | null) {
  // lunar-typescript's EightChar handles solar term boundaries for year/month pillars internally
  // It uses Solar → Lunar → EightChar pipeline

  let solar: Solar;
  if (hour !== null && minute !== null) {
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0);
  } else {
    solar = Solar.fromYmd(year, month, day);
  }

  const lunar = solar.getLunar();
  const eightChar = lunar.getEightChar();

  // Get year, month, day pillars
  const yearPillar = parsePillar(eightChar.getYear());
  const monthPillar = parsePillar(eightChar.getMonth());

  // Day pillar — lunar-typescript may or may not handle 23:00 boundary
  // We need to check and possibly adjust
  let dayPillar: string;
  if (hour !== null && hour >= 23) {
    // In BaZi, 23:00+ belongs to next day
    const nextSolar = Solar.fromYmdHms(year, month, day + 1, 0, 0, 0);
    const nextLunar = nextSolar.getLunar();
    const nextEightChar = nextLunar.getEightChar();
    dayPillar = parsePillar(nextEightChar.getDay());
  } else {
    dayPillar = parsePillar(eightChar.getDay());
  }

  const result: Record<string, string> = {
    year: yearPillar,
    month: monthPillar,
    day: dayPillar,
  };

  // Hour pillar
  if (hour !== null) {
    const timePillar = parsePillar(eightChar.getTime());
    result.hour = timePillar;
  }

  return result;
}

const results = TEST_CASES.map(tc => {
  try {
    const pillars = getPillars(tc.year, tc.month, tc.day, tc.hour, tc.minute);
    return {
      date: `${tc.year}-${String(tc.month).padStart(2, '0')}-${String(tc.day).padStart(2, '0')}`,
      time: tc.hour !== null && tc.minute !== null
        ? `${String(tc.hour).padStart(2, '0')}:${String(tc.minute).padStart(2, '0')}`
        : null,
      desc: tc.desc,
      pillars,
    };
  } catch (e: any) {
    return {
      date: `${tc.year}-${String(tc.month).padStart(2, '0')}-${String(tc.day).padStart(2, '0')}`,
      time: tc.hour !== null && tc.minute !== null
        ? `${String(tc.hour).padStart(2, '0')}:${String(tc.minute).padStart(2, '0')}`
        : null,
      desc: tc.desc,
      error: e.message,
    };
  }
});

console.log(JSON.stringify(results, null, 2));
