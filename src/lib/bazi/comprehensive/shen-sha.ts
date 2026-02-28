
// =============================================================================
// COMPLETE SHEN SHA (神煞) ENGINE — All 37+ Stars
// =============================================================================
// Every star has:
//   1. A lookup table for derivation
//   2. A check function that returns ShenShaResult
//   3. Full derivation logic shown in the result
//
// CORRECTED: Kong Wang uses full Day Pillar (stem+branch), not just stem.
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName } from '../core';
import { STEM_ORDER, BRANCH_ORDER } from '../derived';
import type { ShenShaResult, ChartData } from './models';

// =============================================================================
// UTILITY: 60 Jiazi cycle
// =============================================================================

function _jiaziNumber(stem: string, branch: string): number {
  /** Calculate the 60 Jiazi pillar number (0-59) from stem and branch. */
  const si = STEMS[stem as StemName].index;
  const bi = BRANCHES[branch as BranchName].index;
  for (let n = 0; n < 60; n++) {
    if (n % 10 === si && n % 12 === bi) {
      return n;
    }
  }
  return -1;
}

export function _xunVoidBranches(stem: string, branch: string): [string, string] {
  /**
   * Calculate the two Void (空亡) branches for a given pillar.
   * Uses the full stem+branch to determine the 旬 (decade).
   */
  const n = _jiaziNumber(stem, branch);
  if (n < 0) return ["", ""];
  const xunStart = Math.floor(n / 10) * 10;
  const usedBranches = new Set<number>();
  for (let i = 0; i < 10; i++) {
    usedBranches.add((xunStart + i) % 12);
  }
  const voidIndices: number[] = [];
  for (let i = 0; i < 12; i++) {
    if (!usedBranches.has(i)) voidIndices.push(i);
  }
  voidIndices.sort((a, b) => a - b);
  return [BRANCH_ORDER[voidIndices[0]], BRANCH_ORDER[voidIndices[1]]];
}

// =============================================================================
// HELPER: Check if a branch is in the chart
// =============================================================================

function _findBranch(
  chart: ChartData,
  targetBranch: string,
  includeLp = true,
): Array<{ palace: string; activated_by: string | null }> {
  const results: Array<{ palace: string; activated_by: string | null }> = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    if (chart.pillars[pos].branch === targetBranch) {
      results.push({ palace: pos, activated_by: null });
    }
  }
  if (includeLp && chart.luck_pillar && chart.luck_pillar.branch === targetBranch) {
    results.push({ palace: "luck_pillar", activated_by: "luck_pillar" });
  }
  for (const [pos, pillar] of Object.entries(chart.time_period_pillars)) {
    if (pillar.branch === targetBranch) {
      results.push({ palace: pos, activated_by: pos });
    }
  }
  return results;
}

// Helper to make a default ShenShaResult with absent defaults
function _absent(
  nameEnglish: string,
  nameChinese: string,
  derivation: string,
  overrides: Partial<ShenShaResult> = {},
): ShenShaResult {
  return {
    name_english: nameEnglish,
    name_chinese: nameChinese,
    present: false,
    location: null,
    palace: null,
    activated_by: null,
    derivation,
    nature: "neutral",
    impact: "",
    life_areas: [],
    severity: "mild",
    is_void: false,
    ...overrides,
  };
}

function _present(
  nameEnglish: string,
  nameChinese: string,
  derivation: string,
  overrides: Partial<ShenShaResult> = {},
): ShenShaResult {
  return {
    name_english: nameEnglish,
    name_chinese: nameChinese,
    present: true,
    location: null,
    palace: null,
    activated_by: null,
    derivation,
    nature: "auspicious",
    impact: "",
    life_areas: [],
    severity: "mild",
    is_void: false,
    ...overrides,
  };
}

// =============================================================================
// 1. 天乙贵人 (Tian Yi Gui Ren / Heavenly Noble)
// =============================================================================

const TIAN_YI_LOOKUP: Record<string, [string, string]> = {
  Jia: ["Chou", "Wei"], Yi: ["Zi", "Shen"], Bing: ["Hai", "You"],
  Ding: ["Hai", "You"], Wu: ["Chou", "Wei"], Ji: ["Zi", "Shen"],
  Geng: ["Chou", "Wei"], Xin: ["Yin", "Wu"], Ren: ["Mao", "Si"],
  Gui: ["Mao", "Si"],
};

function checkTianYi(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const targets = TIAN_YI_LOOKUP[dm] ?? [];
  const results: ShenShaResult[] = [];
  for (const t of targets) {
    const locs = _findBranch(chart, t);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Heavenly Noble", "天乙贵人",
          `For ${dm} DM: Tian Yi at ${BRANCHES[t as BranchName].chinese} (${t}). Found in ${loc.palace.replace(/_/g, " ")} palace.`,
          { location: t, palace: loc.palace, activated_by: loc.activated_by,
            life_areas: ["career", "relationship", "wealth"] }));
      }
    } else {
      results.push(_absent("Heavenly Noble", "天乙贵人",
        `For ${dm} DM: Tian Yi at ${BRANCHES[t as BranchName].chinese} (${t}). Not in chart.`,
        { location: t }));
    }
  }
  return results;
}

// =============================================================================
// 2. 太极贵人 (Tai Ji Gui Ren / Tai Ji Noble)
// =============================================================================

const TAI_JI_LOOKUP: Record<string, [string, string]> = {
  Jia: ["Zi", "Wu"], Yi: ["Zi", "Wu"], Bing: ["Mao", "You"], Ding: ["Mao", "You"],
  Wu: ["Mao", "You"], Ji: ["Mao", "You"], Geng: ["Chou", "Wei"], Xin: ["Chou", "Wei"],
  Ren: ["Zi", "Wu"], Gui: ["Zi", "Wu"],
};

function checkTaiJi(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const targets = TAI_JI_LOOKUP[dm] ?? [];
  const results: ShenShaResult[] = [];
  for (const t of targets) {
    const locs = _findBranch(chart, t);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Tai Ji Noble", "太极贵人",
          `For ${dm} DM: Tai Ji at ${BRANCHES[t as BranchName].chinese}. In ${loc.palace}.`,
          { location: t, palace: loc.palace, activated_by: loc.activated_by,
            life_areas: ["career", "education"] }));
      }
    }
  }
  if (!results.some(r => r.present)) {
    results.push(_absent("Tai Ji Noble", "太极贵人",
      `For ${dm} DM: Tai Ji at ${targets.map(t => BRANCHES[t as BranchName].chinese).join(", ")}. Not in chart.`));
  }
  return results;
}

// =============================================================================
// 3. 天德贵人 (Tian De Gui Ren / Heavenly Virtue)
// =============================================================================

const TIAN_DE_LOOKUP: Record<string, string> = {
  Yin: "Ding", Mao: "Shen", Chen: "Ren", Si: "Xin",
  Wu: "Hai", Wei: "Jia", Shen: "Gui", You: "Yin",
  Xu: "Bing", Hai: "Yi", Zi: "Si", Chou: "Geng",
};

function checkTianDe(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const target = TIAN_DE_LOOKUP[monthBranch];
  if (!target) {
    return [_absent("Heavenly Virtue", "天德贵人", "Could not determine month branch.")];
  }

  let found = false;
  let palace: string | null = null;
  let activatedBy: string | null = null;

  if (target in STEMS) {
    for (const pos of ["year", "month", "day", "hour"]) {
      if (chart.pillars[pos].stem === target) {
        found = true;
        palace = pos;
        break;
      }
    }
  }

  if (target in BRANCHES) {
    const locs = _findBranch(chart, target);
    if (locs.length > 0) {
      found = true;
      palace = locs[0].palace;
      activatedBy = locs[0].activated_by;
    }
  }

  return [found
    ? _present("Heavenly Virtue", "天德贵人",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Tian De = ${target}. PRESENT.`,
        { location: target, palace, activated_by: activatedBy, life_areas: ["general", "health"] })
    : _absent("Heavenly Virtue", "天德贵人",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Tian De = ${target}. ABSENT.`,
        { location: target, life_areas: ["general", "health"] })
  ];
}

// =============================================================================
// 4. 月德贵人 (Yue De Gui Ren / Monthly Virtue)
// =============================================================================

const YUE_DE_LOOKUP: Record<string, string> = {
  Yin: "Bing", Wu: "Bing", Xu: "Bing",
  Shen: "Ren", Zi: "Ren", Chen: "Ren",
  Si: "Geng", You: "Geng", Chou: "Geng",
  Hai: "Jia", Mao: "Jia", Wei: "Jia",
};

function checkYueDe(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const targetStem = YUE_DE_LOOKUP[monthBranch];
  if (!targetStem) {
    return [_absent("Monthly Virtue", "月德贵人", "Could not determine.")];
  }

  let found = false;
  let palace: string | null = null;
  for (const pos of ["year", "month", "day", "hour"]) {
    if (chart.pillars[pos].stem === targetStem) {
      found = true; palace = pos; break;
    }
  }
  if (!found) {
    for (const pos of ["year", "month", "day", "hour"]) {
      for (const [hs] of chart.pillars[pos].hidden_stems) {
        if (hs === targetStem) { found = true; palace = pos; break; }
      }
      if (found) break;
    }
  }

  return [found
    ? _present("Monthly Virtue", "月德贵人",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Yue De = ${STEMS[targetStem as StemName].chinese}. PRESENT.`,
        { location: targetStem, palace, life_areas: ["general", "health"] })
    : _absent("Monthly Virtue", "月德贵人",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Yue De = ${STEMS[targetStem as StemName].chinese}. ABSENT.`,
        { location: targetStem })
  ];
}

// =============================================================================
// 5. 文昌贵人 (Wen Chang / Academic Star)
// =============================================================================

const WEN_CHANG_LOOKUP: Record<string, string> = {
  Jia: "Si", Yi: "Wu", Bing: "Shen", Ding: "You",
  Wu: "Shen", Ji: "You", Geng: "Hai", Xin: "Zi",
  Ren: "Yin", Gui: "Mao",
};

function checkWenChang(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = WEN_CHANG_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  if (locs.length > 0) {
    return [_present("Academic Star", "文昌贵人",
      `For ${dm} DM: Wen Chang at ${BRANCHES[target as BranchName].chinese}. In ${locs[0].palace}.`,
      { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
        life_areas: ["education", "career"] })];
  }
  return [_absent("Academic Star", "文昌贵人",
    `For ${dm} DM: Wen Chang at ${BRANCHES[target as BranchName].chinese}. Not in chart.`,
    { location: target })];
}

// =============================================================================
// 6. 金舆 (Jin Yu / Golden Carriage)
// =============================================================================

const JIN_YU_LOOKUP: Record<string, string> = {
  Jia: "Chen", Yi: "Si", Bing: "Wei", Ding: "Shen",
  Wu: "Wei", Ji: "Shen", Geng: "Xu", Xin: "Hai",
  Ren: "Zi", Gui: "Chou",
};

function checkJinYu(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = JIN_YU_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Golden Carriage", "金舆",
        `For ${dm} DM: Jin Yu at ${BRANCHES[target as BranchName].chinese}. PRESENT in ${locs[0].palace}.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          life_areas: ["wealth", "status"] })
    : _absent("Golden Carriage", "金舆",
        `For ${dm} DM: Jin Yu at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["wealth", "status"] })
  ];
}

// =============================================================================
// 7. 天厨贵人 (Tian Chu / Heavenly Kitchen)
// =============================================================================

const TIAN_CHU_LOOKUP: Record<string, string> = {
  Jia: "Si", Yi: "Wu", Bing: "Si", Ding: "Wu",
  Wu: "Si", Ji: "Wu", Geng: "Shen", Xin: "You",
  Ren: "Shen", Gui: "You",
};

function checkTianChu(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = TIAN_CHU_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Heavenly Kitchen", "天厨贵人",
        `For ${dm} DM: Tian Chu at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, life_areas: ["wealth", "food"] })
    : _absent("Heavenly Kitchen", "天厨贵人",
        `For ${dm} DM: Tian Chu at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["wealth", "food"] })
  ];
}

// =============================================================================
// 8. 禄神 (Lu Shen / Prosperity Star)
// =============================================================================

const LU_SHEN_LOOKUP: Record<string, string> = {
  Jia: "Yin", Yi: "Mao", Bing: "Si", Ding: "Wu",
  Wu: "Si", Ji: "Wu", Geng: "Shen", Xin: "You",
  Ren: "Hai", Gui: "Zi",
};

function checkLuShen(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = LU_SHEN_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Prosperity Star", "禄神",
        `For ${dm} DM: Lu Shen at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          life_areas: ["wealth", "career"] })
    : _absent("Prosperity Star", "禄神",
        `For ${dm} DM: Lu Shen at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["wealth", "career"] })
  ];
}

// =============================================================================
// 9. 将星 (Jiang Xing / General Star)
// =============================================================================

const JIANG_XING_LOOKUP: Record<string, string> = {
  Yin: "Wu", Wu: "Wu", Xu: "Wu",
  Shen: "Zi", Zi: "Zi", Chen: "Zi",
  Si: "You", You: "You", Chou: "You",
  Hai: "Mao", Mao: "Mao", Wei: "Mao",
};

function checkJiangXing(chart: ChartData): ShenShaResult[] {
  const results: ShenShaResult[] = [];
  for (const basePos of ["year", "day"]) {
    const baseBranch = chart.pillars[basePos].branch;
    const target = JIANG_XING_LOOKUP[baseBranch];
    if (!target) continue;
    const locs = _findBranch(chart, target, true);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("General Star", "将星",
          `For ${basePos} branch ${BRANCHES[baseBranch as BranchName].chinese}: Jiang Xing at ${BRANCHES[target as BranchName].chinese}. In ${loc.palace}.`,
          { location: target, palace: loc.palace, activated_by: loc.activated_by,
            life_areas: ["career", "authority"] }));
      }
    }
  }
  if (results.length === 0) {
    const yearBranch = chart.pillars["year"].branch;
    const target = JIANG_XING_LOOKUP[yearBranch] ?? "?";
    const chinese = target !== "?" && target in BRANCHES
      ? BRANCHES[target as BranchName].chinese : "?";
    results.push(_absent("General Star", "将星",
      `Jiang Xing at ${chinese}. ABSENT.`,
      { location: target !== "?" ? target : null }));
  }
  return results;
}

// =============================================================================
// 10. 天医 (Tian Yi / Heavenly Doctor)
// =============================================================================

const TIAN_YI_DOCTOR_LOOKUP: Record<string, string> = {
  Yin: "Chou", Mao: "Yin", Chen: "Mao", Si: "Chen",
  Wu: "Si", Wei: "Wu", Shen: "Wei", You: "Shen",
  Xu: "You", Hai: "Xu", Zi: "Hai", Chou: "Zi",
};

function checkTianYiDoctor(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const target = TIAN_YI_DOCTOR_LOOKUP[monthBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Heavenly Doctor", "天医",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Tian Yi Doctor at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, life_areas: ["health"] })
    : _absent("Heavenly Doctor", "天医",
        `For ${BRANCHES[monthBranch as BranchName].chinese} month: Tian Yi Doctor at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health"] })
  ];
}

// =============================================================================
// 11. 天赦 (Tian She / Heavenly Pardon)
// =============================================================================

const TIAN_SHE_LOOKUP: Record<string, string> = {
  Spring: "Wu-Yin", Summer: "Jia-Wu", Autumn: "Wu-Shen", Winter: "Jia-Zi",
};

function checkTianShe(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const season = BRANCHES[monthBranch as BranchName].season;
  const required = TIAN_SHE_LOOKUP[season];
  if (!required) return [];
  const dayKey = `${chart.pillars["day"].stem}-${chart.pillars["day"].branch}`;
  const present = dayKey === required;
  return [present
    ? _present("Heavenly Pardon", "天赦",
        `Born in ${season} (${BRANCHES[monthBranch as BranchName].chinese} month): Tian She requires ${required} day. Day is ${dayKey}. PRESENT.`,
        { life_areas: ["legal", "general"] })
    : _absent("Heavenly Pardon", "天赦",
        `Born in ${season} (${BRANCHES[monthBranch as BranchName].chinese} month): Tian She requires ${required} day. Day is ${dayKey}. ABSENT.`,
        { life_areas: ["legal", "general"] })
  ];
}

// =============================================================================
// 12. 红鸾 (Hong Luan / Red Phoenix)
// =============================================================================

export const HONG_LUAN_LOOKUP: Record<string, string> = {
  Zi: "Mao", Chou: "Yin", Yin: "Chou", Mao: "Zi",
  Chen: "Hai", Si: "Xu", Wu: "You", Wei: "Shen",
  Shen: "Wei", You: "Wu", Xu: "Si", Hai: "Chen",
};

function checkHongLuan(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = HONG_LUAN_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Red Phoenix", "红鸾",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Hong Luan at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          life_areas: ["marriage", "relationship"] })
    : _absent("Red Phoenix", "红鸾",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Hong Luan at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["marriage", "relationship"] })
  ];
}

// =============================================================================
// 13. 天喜 (Tian Xi / Heavenly Happiness)
// =============================================================================

export const TIAN_XI_LOOKUP: Record<string, string> = {
  Zi: "You", Chou: "Shen", Yin: "Wei", Mao: "Wu",
  Chen: "Si", Si: "Chen", Wu: "Mao", Wei: "Yin",
  Shen: "Chou", You: "Zi", Xu: "Hai", Hai: "Xu",
};

function checkTianXi(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = TIAN_XI_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Heavenly Happiness", "天喜",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Tian Xi at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          life_areas: ["marriage", "celebration"] })
    : _absent("Heavenly Happiness", "天喜",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Tian Xi at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["marriage", "celebration"] })
  ];
}

// =============================================================================
// 14. 福星贵人 (Fu Xing / Fortune Star)
// =============================================================================

const FU_XING_LOOKUP: Record<string, string> = {
  Jia: "Yin", Yi: "Mao", Bing: "Si", Ding: "Wu",
  Wu: "Si", Ji: "Wu", Geng: "Shen", Xin: "You",
  Ren: "Hai", Gui: "Zi",
};

function checkFuXing(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = FU_XING_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Fortune Star", "福星贵人",
        `For ${dm} DM: Fu Xing at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, life_areas: ["wealth", "luck"] })
    : _absent("Fortune Star", "福星贵人",
        `For ${dm} DM: Fu Xing at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["wealth", "luck"] })
  ];
}

// =============================================================================
// 15. 三奇贵人 (San Qi / Three Wonders Noble)
// =============================================================================

function checkSanQi(chart: ChartData): ShenShaResult[] {
  const stems = ["year", "month", "day", "hour"].map(p => chart.pillars[p].stem);

  const heaven = ["Jia", "Wu", "Geng"];
  const earth = ["Yi", "Bing", "Ding"];
  const human = ["Ren", "Gui", "Xin"];

  function checkSequence(seq: string[]): boolean {
    for (let i = 0; i <= stems.length - 3; i++) {
      if (stems[i] === seq[0] && stems[i + 1] === seq[1] && stems[i + 2] === seq[2]) {
        return true;
      }
    }
    return false;
  }

  const results: ShenShaResult[] = [];
  const checks: Array<[string[], string, string]> = [
    [heaven, "Heavenly", "天上三奇"],
    [earth, "Earthly", "地上三奇"],
    [human, "Human", "人中三奇"],
  ];

  for (const [seq, label, cn] of checks) {
    if (checkSequence(seq)) {
      results.push(_present(`Three Wonders (${label})`, cn,
        `Stems sequence ${seq.map(s => STEMS[s as StemName].chinese).join(" → ")} found in pillars.`,
        { life_areas: ["intelligence", "career"] }));
    }
  }

  if (results.length === 0) {
    results.push(_absent("Three Wonders Noble", "三奇贵人",
      "No Three Wonders sequence (甲戊庚, 乙丙丁, 壬癸辛) found in stem order."));
  }
  return results;
}

// =============================================================================
// 16. 羊刃 (Yang Ren / Sheep Blade)
// =============================================================================

const YANG_REN_LOOKUP: Record<string, string> = {
  Jia: "Mao", Bing: "Wu", Wu: "Wu", Geng: "You", Ren: "Zi",
  Yi: "Chen", Ding: "Wei", Ji: "Wei", Xin: "Xu", Gui: "Chou",
};

function checkYangRen(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = YANG_REN_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  const isYang = STEMS[dm].polarity === "Yang";
  return [present
    ? _present("Sheep Blade", "羊刃",
        `For ${dm} DM (${isYang ? "Yang" : "Yin, extended"}): Yang Ren at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          nature: "inauspicious", life_areas: ["health", "career", "legal"], severity: "moderate" })
    : _absent("Sheep Blade", "羊刃",
        `For ${dm} DM (${isYang ? "Yang" : "Yin, extended"}): Yang Ren at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "career", "legal"] })
  ];
}

// =============================================================================
// 17. 空亡 (Kong Wang / Void)
// =============================================================================

function _getXunName(stem: string, branch: string): string {
  const n = _jiaziNumber(stem, branch);
  const xunStart = Math.floor(n / 10) * 10;
  const sIdx = xunStart % 10;
  const bIdx = xunStart % 12;
  return `${STEMS[STEM_ORDER[sIdx]].chinese}${BRANCHES[BRANCH_ORDER[bIdx]].chinese}旬`;
}

function checkKongWang(chart: ChartData): ShenShaResult[] {
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  const [voidB1, voidB2] = _xunVoidBranches(dayStem, dayBranch);

  const results: ShenShaResult[] = [];
  for (const vb of [voidB1, voidB2]) {
    if (!vb) continue;
    const locs = _findBranch(chart, vb, false);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Void Star", "空亡",
          `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese} is in ${_getXunName(dayStem, dayBranch)}. Void at ${BRANCHES[vb as BranchName].chinese}. Found in ${loc.palace}.`,
          { location: vb, palace: loc.palace, nature: "inauspicious",
            life_areas: ["career", "relationship", "children"], severity: "moderate" }));
      }
    } else {
      results.push(_absent("Void Star", "空亡",
        `Void at ${BRANCHES[vb as BranchName].chinese}. Not in natal branches.`,
        { location: vb }));
    }
  }
  return results;
}

export function getVoidBranches(chart: ChartData): Set<string> {
  /** Get the set of Void branch IDs for this chart. */
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  const [vb1, vb2] = _xunVoidBranches(dayStem, dayBranch);
  const result = new Set<string>();
  if (vb1) result.add(vb1);
  if (vb2) result.add(vb2);
  return result;
}

// =============================================================================
// 18. 桃花 (Tao Hua / Peach Blossom)
// =============================================================================

export const TAO_HUA_LOOKUP: Record<string, string> = {
  Yin: "Mao", Wu: "Mao", Xu: "Mao",
  Shen: "You", Zi: "You", Chen: "You",
  Si: "Wu", You: "Wu", Chou: "Wu",
  Hai: "Zi", Mao: "Zi", Wei: "Zi",
};

function checkTaoHua(chart: ChartData): ShenShaResult[] {
  const results: ShenShaResult[] = [];
  const seen = new Set<string>();
  for (const basePos of ["year", "day"]) {
    const baseBranch = chart.pillars[basePos].branch;
    const target = TAO_HUA_LOOKUP[baseBranch];
    if (!target || seen.has(target)) continue;
    seen.add(target);
    const locs = _findBranch(chart, target);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Peach Blossom", "桃花",
          `For ${basePos} branch ${BRANCHES[baseBranch as BranchName].chinese}: Peach Blossom at ${BRANCHES[target as BranchName].chinese}. In ${loc.palace}.`,
          { location: target, palace: loc.palace, activated_by: loc.activated_by,
            nature: "mixed", life_areas: ["relationship", "career"] }));
      }
    }
  }
  if (!results.some(r => r.present)) {
    const yearBranch = chart.pillars["year"].branch;
    const target = TAO_HUA_LOOKUP[yearBranch] ?? "?";
    const chinese = target !== "?" && target in BRANCHES ? BRANCHES[target as BranchName].chinese : "?";
    results.push(_absent("Peach Blossom", "桃花",
      `Peach Blossom at ${chinese}. ABSENT.`,
      { location: target !== "?" ? target : null }));
  }
  return results;
}

// =============================================================================
// 19. 华盖 (Hua Gai / Canopy Star)
// =============================================================================

const HUA_GAI_LOOKUP: Record<string, string> = {
  Yin: "Xu", Wu: "Xu", Xu: "Xu",
  Shen: "Chen", Zi: "Chen", Chen: "Chen",
  Si: "Chou", You: "Chou", Chou: "Chou",
  Hai: "Wei", Mao: "Wei", Wei: "Wei",
};

function checkHuaGai(chart: ChartData): ShenShaResult[] {
  const results: ShenShaResult[] = [];
  const seen = new Set<string>();
  for (const basePos of ["year", "day"]) {
    const baseBranch = chart.pillars[basePos].branch;
    const target = HUA_GAI_LOOKUP[baseBranch];
    if (!target || seen.has(target)) continue;
    seen.add(target);
    const locs = _findBranch(chart, target);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Canopy Star", "华盖",
          `For ${basePos} branch ${BRANCHES[baseBranch as BranchName].chinese}: Hua Gai at ${BRANCHES[target as BranchName].chinese}. In ${loc.palace}.`,
          { nature: "mixed", location: target, palace: loc.palace,
            life_areas: ["spirituality", "education"] }));
      }
    }
  }
  if (!results.some(r => r.present)) {
    const yearBranch = chart.pillars["year"].branch;
    const target = HUA_GAI_LOOKUP[yearBranch] ?? "?";
    const chinese = target !== "?" && target in BRANCHES ? BRANCHES[target as BranchName].chinese : "?";
    results.push(_absent("Canopy Star", "华盖",
      `Hua Gai at ${chinese}. ABSENT.`));
  }
  return results;
}

// =============================================================================
// 20. 驿马 (Yi Ma / Traveling Horse)
// =============================================================================

export const YI_MA_LOOKUP: Record<string, string> = {
  Yin: "Shen", Wu: "Shen", Xu: "Shen",
  Shen: "Yin", Zi: "Yin", Chen: "Yin",
  Si: "Hai", You: "Hai", Chou: "Hai",
  Hai: "Si", Mao: "Si", Wei: "Si",
};

function checkYiMa(chart: ChartData): ShenShaResult[] {
  const results: ShenShaResult[] = [];
  const seen = new Set<string>();
  for (const basePos of ["year", "day"]) {
    const baseBranch = chart.pillars[basePos].branch;
    const target = YI_MA_LOOKUP[baseBranch];
    if (!target || seen.has(target)) continue;
    seen.add(target);
    const locs = _findBranch(chart, target);
    if (locs.length > 0) {
      for (const loc of locs) {
        results.push(_present("Traveling Horse", "驿马",
          `For ${basePos} branch ${BRANCHES[baseBranch as BranchName].chinese}: Yi Ma at ${BRANCHES[target as BranchName].chinese}. In ${loc.palace}.`,
          { location: target, palace: loc.palace, activated_by: loc.activated_by,
            nature: "mixed", life_areas: ["travel", "career"] }));
      }
    }
  }
  if (results.length === 0) {
    const yearBranch = chart.pillars["year"].branch;
    const target = YI_MA_LOOKUP[yearBranch] ?? "?";
    const chinese = target !== "?" && target in BRANCHES ? BRANCHES[target as BranchName].chinese : "?";
    results.push(_absent("Traveling Horse", "驿马",
      `Yi Ma at ${chinese}. ABSENT.`,
      { location: target !== "?" ? target : null }));
  }
  return results;
}

// =============================================================================
// 21. 劫煞 (Jie Sha / Robbery Star)
// =============================================================================

const JIE_SHA_LOOKUP: Record<string, string> = {
  Yin: "Hai", Wu: "Hai", Xu: "Hai",
  Shen: "Si", Zi: "Si", Chen: "Si",
  Si: "Yin", You: "Yin", Chou: "Yin",
  Hai: "Shen", Mao: "Shen", Wei: "Shen",
};

function checkJieSha(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = JIE_SHA_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Robbery Star", "劫煞",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Jie Sha at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          nature: "inauspicious", life_areas: ["wealth", "safety"], severity: "moderate" })
    : _absent("Robbery Star", "劫煞",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Jie Sha at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["wealth", "safety"] })
  ];
}

// =============================================================================
// 22. 亡神 (Wang Shen / Lost Spirit)
// =============================================================================

const WANG_SHEN_LOOKUP: Record<string, string> = {
  Yin: "Si", Wu: "Si", Xu: "Si",
  Shen: "Hai", Zi: "Hai", Chen: "Hai",
  Si: "Shen", You: "Shen", Chou: "Shen",
  Hai: "Yin", Mao: "Yin", Wei: "Yin",
};

function checkWangShen(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = WANG_SHEN_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Lost Spirit", "亡神",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Wang Shen at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health", "spirit"], severity: "moderate" })
    : _absent("Lost Spirit", "亡神",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Wang Shen at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "spirit"] })
  ];
}

// =============================================================================
// 23. 灾煞 (Zai Sha / Disaster Star) — CORRECTED
// =============================================================================

const ZAI_SHA_LOOKUP: Record<string, string> = {
  Yin: "Zi", Wu: "Zi", Xu: "Zi",
  Si: "Wu", You: "Wu", Chou: "Wu",
  Shen: "Mao", Zi: "Mao", Chen: "Mao",
  Hai: "You", Mao: "You", Wei: "You",
};

function checkZaiSha(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = ZAI_SHA_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Disaster Star", "灾煞",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Zai Sha at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health", "safety"], severity: "severe" })
    : _absent("Disaster Star", "灾煞",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Zai Sha at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "safety"] })
  ];
}

// =============================================================================
// 24. 天罗地网 (Tian Luo Di Wang / Heaven's Net and Earth's Snare)
// =============================================================================

function checkTianLuoDiWang(chart: ChartData): ShenShaResult[] {
  const results: ShenShaResult[] = [];
  const tianLuo = new Set(["Xu", "Hai"]);
  const diWang = new Set(["Chen", "Si"]);

  for (const pos of ["year", "month", "day", "hour"]) {
    const br = chart.pillars[pos].branch;
    if (tianLuo.has(br)) {
      results.push(_present("Heaven's Net", "天罗",
        `${BRANCHES[br as BranchName].chinese} in ${pos} palace = Heaven's Net (天罗).`,
        { location: br, palace: pos, nature: "inauspicious",
          life_areas: ["legal", "relationship"], severity: "moderate" }));
    }
    if (diWang.has(br)) {
      results.push(_present("Earth's Snare", "地网",
        `${BRANCHES[br as BranchName].chinese} in ${pos} palace = Earth's Snare (地网).`,
        { location: br, palace: pos, nature: "inauspicious",
          life_areas: ["legal", "relationship"], severity: "moderate" }));
    }
  }

  if (results.length === 0) {
    results.push(_absent("Heaven's Net / Earth's Snare", "天罗地网",
      "No 辰巳 (Earth's Snare) or 戌亥 (Heaven's Net) in natal branches."));
  }
  return results;
}

// =============================================================================
// 25. 阴差阳错 (Yin Cha Yang Cuo / Yin-Yang Disharmony Day)
// =============================================================================

const YIN_CHA_YANG_CUO_DAYS = new Set([
  "Bing|Zi", "Bing|Wu", "Ding|Chou", "Ding|Wei",
  "Wu|Yin", "Wu|Shen", "Xin|Mao", "Xin|You",
  "Ren|Chen", "Ren|Xu", "Gui|Si", "Gui|Hai",
]);

function checkYinChaYangCuo(chart: ChartData): ShenShaResult[] {
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  const present = YIN_CHA_YANG_CUO_DAYS.has(`${dayStem}|${dayBranch}`);
  return [present
    ? _present("Yin-Yang Disharmony Day", "阴差阳错",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: IS a Yin-Yang Disharmony day.`,
        { nature: "inauspicious", life_areas: ["marriage", "relationship"], severity: "critical" })
    : _absent("Yin-Yang Disharmony Day", "阴差阳错",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: is NOT a Yin-Yang Disharmony day.`,
        { life_areas: ["marriage", "relationship"] })
  ];
}

// =============================================================================
// 26. 孤辰 (Gu Chen / Lonely Star)
// =============================================================================

const GU_CHEN_LOOKUP: Record<string, string> = {
  Zi: "Yin", Chou: "Yin", Hai: "Yin",
  Yin: "Si", Mao: "Si", Chen: "Si",
  Si: "Shen", Wu: "Shen", Wei: "Shen",
  Shen: "Hai", You: "Hai", Xu: "Hai",
};

function checkGuChen(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = GU_CHEN_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Lonely Star", "孤辰",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Gu Chen at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          nature: "inauspicious", life_areas: ["relationship", "family"], severity: "moderate" })
    : _absent("Lonely Star", "孤辰",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Gu Chen at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["relationship", "family"] })
  ];
}

// =============================================================================
// 27. 寡宿 (Gua Su / Widow Star)
// =============================================================================

const GUA_SU_LOOKUP: Record<string, string> = {
  Zi: "Xu", Chou: "Xu", Hai: "Xu",
  Yin: "Chou", Mao: "Chou", Chen: "Chou",
  Si: "Chen", Wu: "Chen", Wei: "Chen",
  Shen: "Wei", You: "Wei", Xu: "Wei",
};

function checkGuaSu(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = GUA_SU_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Widow Star", "寡宿",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Gua Su at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["relationship"], severity: "moderate" })
    : _absent("Widow Star", "寡宿",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Gua Su at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["relationship"] })
  ];
}

// =============================================================================
// 28. 四废 (Si Fei / Four Wastes)
// =============================================================================

const SI_FEI_DAYS: Record<string, Set<string>> = {
  Spring: new Set(["Geng|Shen", "Xin|You"]),
  Summer: new Set(["Ren|Zi", "Gui|Hai"]),
  Autumn: new Set(["Jia|Yin", "Yi|Mao"]),
  Winter: new Set(["Bing|Wu", "Ding|Si"]),
};

function checkSiFei(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const season = BRANCHES[monthBranch as BranchName].season;
  const dayPair = `${chart.pillars["day"].stem}|${chart.pillars["day"].branch}`;
  const wasteDays = SI_FEI_DAYS[season] ?? new Set();
  const present = wasteDays.has(dayPair);
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  return [present
    ? _present("Four Wastes", "四废",
        `Born in ${season} (${BRANCHES[monthBranch as BranchName].chinese} month). Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: IS a Four Wastes day.`,
        { nature: "inauspicious", life_areas: ["health", "general"], severity: "severe" })
    : _absent("Four Wastes", "四废",
        `Born in ${season} (${BRANCHES[monthBranch as BranchName].chinese} month). Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: is NOT a Four Wastes day.`,
        { life_areas: ["health", "general"] })
  ];
}

// =============================================================================
// 29. 十恶大败 (Shi E Da Bai / Ten Evils Great Defeat)
// =============================================================================

const SHI_E_DA_BAI_DAYS = new Set([
  "Jia|Chen", "Yi|Si", "Bing|Shen", "Ding|Hai",
  "Wu|Xu", "Ji|Chou", "Geng|Chen", "Xin|Si",
  "Ren|Shen", "Gui|Hai",
]);

function checkShiEDaBai(chart: ChartData): ShenShaResult[] {
  const dayPair = `${chart.pillars["day"].stem}|${chart.pillars["day"].branch}`;
  const present = SHI_E_DA_BAI_DAYS.has(dayPair);
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  return [present
    ? _present("Ten Evils Great Defeat", "十恶大败",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: IS a Ten Evils day.`,
        { nature: "inauspicious", life_areas: ["wealth", "general"], severity: "severe" })
    : _absent("Ten Evils Great Defeat", "十恶大败",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: is NOT a Ten Evils day.`,
        { life_areas: ["wealth", "general"] })
  ];
}

// =============================================================================
// 30. 魁罡 (Kui Gang)
// =============================================================================

const KUI_GANG_DAYS = new Set([
  "Ren|Chen", "Geng|Chen", "Geng|Xu", "Wu|Xu",
]);

function checkKuiGang(chart: ChartData): ShenShaResult[] {
  const dayPair = `${chart.pillars["day"].stem}|${chart.pillars["day"].branch}`;
  const present = KUI_GANG_DAYS.has(dayPair);
  const dayStem = chart.pillars["day"].stem;
  const dayBranch = chart.pillars["day"].branch;
  return [present
    ? _present("Kui Gang", "魁罡",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: IS a Kui Gang day.`,
        { nature: "mixed", life_areas: ["career", "authority", "marriage"], severity: "moderate" })
    : _absent("Kui Gang", "魁罡",
        `Day Pillar ${STEMS[dayStem as StemName].chinese}${BRANCHES[dayBranch as BranchName].chinese}: is NOT a Kui Gang day.`,
        { life_areas: ["career", "authority", "marriage"] })
  ];
}

// =============================================================================
// 31. 血刃 (Xue Ren / Blood Blade)
// =============================================================================

const XUE_REN_LOOKUP: Record<string, string> = {
  Jia: "Mao", Yi: "Chen", Bing: "Wu", Ding: "Wei",
  Wu: "Wu", Ji: "Wei", Geng: "You", Xin: "Xu",
  Ren: "Zi", Gui: "Chou",
};

function checkXueRen(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = XUE_REN_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Blood Blade", "血刃",
        `For ${dm} DM: Blood Blade at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health"], severity: "moderate" })
    : _absent("Blood Blade", "血刃",
        `For ${dm} DM: Blood Blade at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health"] })
  ];
}

// =============================================================================
// 32. 勾绞 (Gou Jiao / Hook and Strangle)
// =============================================================================

function checkGouJiao(chart: ChartData): ShenShaResult[] {
  const yearIdx = BRANCHES[chart.pillars["year"].branch as BranchName].index;
  const gouIdx = (yearIdx + 1) % 12;
  const jiaoIdx = ((yearIdx - 1) % 12 + 12) % 12;
  const gouBranch = BRANCH_ORDER[gouIdx];
  const jiaoBranch = BRANCH_ORDER[jiaoIdx];

  const results: ShenShaResult[] = [];
  const checks: Array<[string, string, string]> = [
    [gouBranch, "Hook", "勾"],
    [jiaoBranch, "Strangle", "绞"],
  ];

  for (const [target, label, cn] of checks) {
    const locs = _findBranch(chart, target);
    if (locs.length > 0) {
      results.push(_present(`${label} Star`, cn,
        `Year ${chart.pillars["year"].branch_chinese}: ${label} at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, activated_by: locs[0].activated_by,
          nature: "inauspicious", life_areas: ["legal", "disputes"], severity: "moderate" }));
    }
  }

  if (results.length === 0) {
    results.push(_absent("Hook and Strangle", "勾绞",
      `Hook at ${BRANCHES[gouBranch].chinese}, Strangle at ${BRANCHES[jiaoBranch].chinese}. Both ABSENT.`));
  }
  return results;
}

// =============================================================================
// 33. 丧门 (Sang Men / Funeral Door)
// =============================================================================

function checkSangMen(chart: ChartData): ShenShaResult[] {
  const yearIdx = BRANCHES[chart.pillars["year"].branch as BranchName].index;
  const targetIdx = (yearIdx + 2) % 12;
  const target = BRANCH_ORDER[targetIdx];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Funeral Door", "丧门",
        `Year + 2 positions = ${BRANCHES[target].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health", "family"], severity: "moderate" })
    : _absent("Funeral Door", "丧门",
        `Year + 2 positions = ${BRANCHES[target].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "family"] })
  ];
}

// =============================================================================
// 34. 吊客 (Diao Ke / Hanging Guest)
// =============================================================================

function checkDiaoKe(chart: ChartData): ShenShaResult[] {
  const yearIdx = BRANCHES[chart.pillars["year"].branch as BranchName].index;
  const targetIdx = ((yearIdx - 2) % 12 + 12) % 12;
  const target = BRANCH_ORDER[targetIdx];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Hanging Guest", "吊客",
        `Year - 2 positions = ${BRANCHES[target].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health", "family"], severity: "moderate" })
    : _absent("Hanging Guest", "吊客",
        `Year - 2 positions = ${BRANCHES[target].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "family"] })
  ];
}

// =============================================================================
// 35. 咸池 (Xian Chi / Salty Pool)
// =============================================================================

const XIAN_CHI_LOOKUP: Record<string, string> = {
  Jia: "You", Yi: "You", Bing: "Zi", Ding: "Zi",
  Wu: "Zi", Ji: "Zi", Geng: "Mao", Xin: "Mao",
  Ren: "Wu", Gui: "Wu",
};

function checkXianChi(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const target = XIAN_CHI_LOOKUP[dm];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("Salty Pool", "咸池",
        `For ${dm} DM: Xian Chi at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["relationship"], severity: "moderate" })
    : _absent("Salty Pool", "咸池",
        `For ${dm} DM: Xian Chi at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["relationship"] })
  ];
}

// =============================================================================
// 36. 白虎 (Bai Hu / White Tiger)
// =============================================================================

const BAI_HU_LOOKUP: Record<string, string> = {
  Zi: "Wu", Chou: "Wei", Yin: "Shen", Mao: "You",
  Chen: "Xu", Si: "Hai", Wu: "Zi", Wei: "Chou",
  Shen: "Yin", You: "Mao", Xu: "Chen", Hai: "Si",
};

function checkBaiHu(chart: ChartData): ShenShaResult[] {
  const yearBranch = chart.pillars["year"].branch;
  const target = BAI_HU_LOOKUP[yearBranch];
  if (!target) return [];
  const locs = _findBranch(chart, target);
  const present = locs.length > 0;
  return [present
    ? _present("White Tiger", "白虎",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Bai Hu at ${BRANCHES[target as BranchName].chinese}. PRESENT.`,
        { location: target, palace: locs[0].palace, nature: "inauspicious",
          life_areas: ["health", "safety"], severity: "severe" })
    : _absent("White Tiger", "白虎",
        `For ${BRANCHES[yearBranch as BranchName].chinese} year: Bai Hu at ${BRANCHES[target as BranchName].chinese}. ABSENT.`,
        { location: target, life_areas: ["health", "safety"] })
  ];
}

// =============================================================================
// 37. 童子 (Tong Zi / Child Star)
// =============================================================================

const TONG_ZI_SEASON_LOOKUP: Record<string, [string, string]> = {
  Spring: ["Yin", "Zi"], Summer: ["Mao", "Wei"],
  Autumn: ["Yin", "Zi"], Winter: ["Mao", "Wei"],
};

const TONG_ZI_ELEMENT_LOOKUP: Record<string, [string, string]> = {
  Metal: ["Wu", "Mao"], Wood: ["Wu", "Mao"],
  Water: ["You", "Xu"], Fire: ["You", "Xu"],
  Earth: ["Chen", "Si"],
};

function checkTongZi(chart: ChartData): ShenShaResult[] {
  const monthBranch = chart.pillars["month"].branch;
  const season = BRANCHES[monthBranch as BranchName].season;
  const dmElement = chart.dm_element;

  const natalBranches = new Set(
    ["year", "month", "day", "hour"].map(p => chart.pillars[p].branch));

  const seasonTargets = TONG_ZI_SEASON_LOOKUP[season] ?? [];
  const elementTargets = TONG_ZI_ELEMENT_LOOKUP[dmElement] ?? [];
  const allTargets = new Set([...seasonTargets, ...elementTargets]);
  const foundIn = [...allTargets].filter(t => natalBranches.has(t as BranchName));

  if (foundIn.length > 0) {
    const target = foundIn[0];
    const pos = ["year", "month", "day", "hour"].find(p => chart.pillars[p].branch === target)!;
    return [_present("Child Star", "童子",
      `Born in ${season}, DM element ${dmElement}. Check for ${[...allTargets].map(t => BRANCHES[t as BranchName].chinese).join(", ")}. ${BRANCHES[target as BranchName].chinese} found in ${pos}.`,
      { location: target, palace: pos, nature: "inauspicious",
        life_areas: ["marriage", "health", "children"], severity: "moderate" })];
  }
  return [_absent("Child Star", "童子",
    `Born in ${season}, DM element ${dmElement}. Check for ${[...allTargets].map(t => BRANCHES[t as BranchName].chinese).join(", ")}. None found.`)];
}

// =============================================================================
// 38. 財星 (Cai Xing / Wealth Star)
// =============================================================================

const WEALTH_STAR_TARGETS: Record<string, string[]> = {
  Jia: ["Chen", "Chou", "Wei", "Xu"], Yi: ["Chen", "Chou", "Wei", "Xu"],
  Bing: ["Shen", "You"], Ding: ["Shen", "You"],
  Wu: ["Zi", "Hai"], Ji: ["Zi", "Hai"],
  Geng: ["Yin", "Mao"], Xin: ["Yin", "Mao"],
  Ren: ["Si", "Wu"], Gui: ["Si", "Wu"],
};

const _DM_WEALTH: Record<string, string> = {
  Wood: "Earth", Fire: "Metal", Earth: "Water",
  Metal: "Wood", Water: "Fire",
};

function checkWealthStar(chart: ChartData): ShenShaResult[] {
  const dm = chart.day_master;
  const targets = WEALTH_STAR_TARGETS[dm] ?? [];
  const dmElem = STEMS[dm].element;
  const wealthElem = _DM_WEALTH[dmElem] ?? "";
  const results: ShenShaResult[] = [];
  let foundAny = false;

  for (const t of targets) {
    const locs = _findBranch(chart, t);
    if (locs.length > 0) {
      foundAny = true;
      for (const loc of locs) {
        results.push(_present("Wealth Star", "財星",
          `For ${dm} DM (${dmElem}): wealth=${wealthElem}. ${BRANCHES[t as BranchName].chinese} (${t}) carries ${wealthElem} qi. Found in ${loc.palace.replace(/_/g, " ")}.`,
          { location: t, palace: loc.palace, activated_by: loc.activated_by,
            life_areas: ["wealth"] }));
      }
    }
  }

  if (!foundAny) {
    const targetNames = targets.map(t => BRANCHES[t as BranchName].chinese).join(", ");
    results.push(_absent("Wealth Star", "財星",
      `For ${dm} DM (${dmElem}): wealth=${wealthElem}. Targets: ${targetNames}. None found.`));
  }

  return results;
}

// =============================================================================
// MASTER FUNCTION: Run All Shen Sha Checks
// =============================================================================

const ALL_CHECKS: Array<(chart: ChartData) => ShenShaResult[]> = [
  checkTianYi, checkTaiJi, checkTianDe, checkYueDe,
  checkWenChang, checkJinYu, checkTianChu, checkLuShen,
  checkJiangXing, checkTianYiDoctor, checkTianShe,
  checkHongLuan, checkTianXi, checkFuXing, checkSanQi,
  checkYangRen, checkKongWang, checkTaoHua, checkHuaGai,
  checkYiMa, checkJieSha, checkWangShen, checkZaiSha,
  checkTianLuoDiWang, checkYinChaYangCuo, checkGuChen,
  checkGuaSu, checkSiFei, checkShiEDaBai, checkKuiGang,
  checkXueRen, checkGouJiao, checkSangMen, checkDiaoKe,
  checkXianChi, checkBaiHu, checkTongZi, checkWealthStar,
];

export function runAllShenSha(chart: ChartData): ShenShaResult[] {
  /** Run all 37+ Shen Sha checks and return combined results. */
  const results: ShenShaResult[] = [];
  const voidBranches = getVoidBranches(chart);

  for (const checkFn of ALL_CHECKS) {
    const starResults = checkFn(chart);
    for (const r of starResults) {
      if (r.present && r.location && voidBranches.has(r.location)) {
        r.is_void = true;
      }
    }
    results.push(...starResults);
  }
  return results;
}

export function getPresentShenSha(chart: ChartData): ShenShaResult[] {
  /** Return only present/activated Shen Sha stars. */
  return runAllShenSha(chart).filter(r => r.present);
}

export function getAbsentCriticalShenSha(chart: ChartData): ShenShaResult[] {
  /** Return absent Shen Sha that would have been important for this chart. */
  const allResults = runAllShenSha(chart);
  const criticalNames = new Set(["禄神", "天医", "天德贵人", "天赦", "将星", "文昌贵人", "福星贵人"]);
  return allResults.filter(r => !r.present && criticalNames.has(r.name_chinese));
}
