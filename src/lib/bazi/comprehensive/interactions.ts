import 'server-only';

// =============================================================================
// BRANCH INTERACTIONS ENGINE
// =============================================================================
// Detects ALL branch interactions between natal pillars and with luck pillar:
//   - Six Clashes (六冲)
//   - Six Harmonies (六合)
//   - Three Harmony Frames (三合局)
//   - Directional Combinations (三会局)
//   - Three Punishments (三刑)
//   - Six Harms (六害)
//   - Destructions (破)
//   - Heavenly Stem Combinations (天干合)
// =============================================================================

import { STEMS, BRANCHES, type StemName, type BranchName } from '../core';
import type { BranchInteraction, ChartData } from './models';

// Palace names for human-readable output
const PALACE_NAMES: Record<string, string> = {
  year: "Year (Parents/Ancestry)",
  month: "Month (Career/Social)",
  day: "Day (Self/Spouse)",
  hour: "Hour (Children/Legacy)",
  luck_pillar: "Current Luck Pillar",
  annual: "Annual Luck",
  monthly: "Monthly Luck",
  daily: "Daily Luck",
  hourly: "Hourly Luck",
};

// Helper to make a sorted pair key for frozenset-like lookups
function pairKey(a: string, b: string): string {
  return a < b ? `${a}|${b}` : `${b}|${a}`;
}

// Helper to make a sorted triple key
function tripleKey(a: string, b: string, c: string): string {
  return [a, b, c].sort().join("|");
}

function getAllBranches(chart: ChartData, includeLp = true): Array<[string, string]> {
  const pairs: Array<[string, string]> = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    pairs.push([pos, chart.pillars[pos].branch]);
  }
  if (includeLp && chart.luck_pillar) {
    pairs.push(["luck_pillar", chart.luck_pillar.branch]);
  }
  for (const [pos, pillar] of Object.entries(chart.time_period_pillars)) {
    pairs.push([pos, pillar.branch]);
  }
  return pairs;
}

// =============================================================================
// SIX CLASHES (六冲)
// =============================================================================

const CLASH_PAIRS_SET = new Set([
  pairKey("Zi", "Wu"), pairKey("Chou", "Wei"),
  pairKey("Yin", "Shen"), pairKey("Mao", "You"),
  pairKey("Chen", "Xu"), pairKey("Si", "Hai"),
]);

function detectClashes(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);

  for (let i = 0; i < pairs.length; i++) {
    for (let j = i + 1; j < pairs.length; j++) {
      const [pos1, br1] = pairs[i];
      const [pos2, br2] = pairs[j];
      if (CLASH_PAIRS_SET.has(pairKey(br1, br2))) {
        const activated = pos1 === "luck_pillar" || pos2 === "luck_pillar";
        const elem1 = BRANCHES[br1 as BranchName].element;
        const elem2 = BRANCHES[br2 as BranchName].element;

        results.push({
          interaction_type: "clash",
          chinese_name: "六冲",
          branches: [br1, br2],
          palaces: [PALACE_NAMES[pos1] ?? pos1, PALACE_NAMES[pos2] ?? pos2],
          description: `${BRANCHES[br1 as BranchName].chinese}${BRANCHES[br2 as BranchName].chinese}冲 (${elem1} vs ${elem2})`,
          activated_by_lp: activated,
          severity: "severe",
        });
      }
    }
  }
  return results;
}

// =============================================================================
// SIX HARMONIES (六合)
// =============================================================================

export const HARMONY_PAIRS: Record<string, string> = {
  [pairKey("Zi", "Chou")]: "Earth",
  [pairKey("Yin", "Hai")]: "Wood",
  [pairKey("Mao", "Xu")]: "Fire",
  [pairKey("Chen", "You")]: "Metal",
  [pairKey("Si", "Shen")]: "Water",
  [pairKey("Wu", "Wei")]: "Fire",
};

function detectHarmonies(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);

  for (let i = 0; i < pairs.length; i++) {
    for (let j = i + 1; j < pairs.length; j++) {
      const [pos1, br1] = pairs[i];
      const [pos2, br2] = pairs[j];
      const key = pairKey(br1, br2);
      if (key in HARMONY_PAIRS) {
        const element = HARMONY_PAIRS[key];
        const activated = pos1 === "luck_pillar" || pos2 === "luck_pillar";

        results.push({
          interaction_type: "harmony",
          chinese_name: "六合",
          branches: [br1, br2],
          palaces: [PALACE_NAMES[pos1] ?? pos1, PALACE_NAMES[pos2] ?? pos2],
          description: `${BRANCHES[br1 as BranchName].chinese}${BRANCHES[br2 as BranchName].chinese}合 → ${element}`,
          activated_by_lp: activated,
          severity: "mild",
        });
      }
    }
  }
  return results;
}

// =============================================================================
// THREE HARMONY FRAMES (三合局)
// =============================================================================

export const THREE_HARMONY_FRAMES: Record<string, string> = {
  [tripleKey("Shen", "Zi", "Chen")]: "Water",
  [tripleKey("Hai", "Mao", "Wei")]: "Wood",
  [tripleKey("Yin", "Wu", "Xu")]: "Fire",
  [tripleKey("Si", "You", "Chou")]: "Metal",
};

// Pre-compute frame sets for iteration
const THREE_HARMONY_FRAME_SETS: Array<{ branches: Set<string>; element: string; key: string }> = [
  { branches: new Set(["Shen", "Zi", "Chen"]), element: "Water", key: tripleKey("Shen", "Zi", "Chen") },
  { branches: new Set(["Hai", "Mao", "Wei"]), element: "Wood", key: tripleKey("Hai", "Mao", "Wei") },
  { branches: new Set(["Yin", "Wu", "Xu"]), element: "Fire", key: tripleKey("Yin", "Wu", "Xu") },
  { branches: new Set(["Si", "You", "Chou"]), element: "Metal", key: tripleKey("Si", "You", "Chou") },
];

function detectThreeHarmony(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);
  const allBranches = new Set(pairs.map(([, br]) => br));

  for (const frame of THREE_HARMONY_FRAME_SETS) {
    const present = new Set([...frame.branches].filter(b => allBranches.has(b)));

    if (present.size === 3) {
      // Full frame present
      const positions: string[] = [];
      let activated = false;
      for (const [pos, br] of pairs) {
        if (frame.branches.has(br)) {
          positions.push(PALACE_NAMES[pos] ?? pos);
          if (pos === "luck_pillar") activated = true;
        }
      }

      const sorted = [...frame.branches].sort((a, b) => BRANCHES[a as BranchName].index - BRANCHES[b as BranchName].index);
      const branchesChinese = sorted.map(b => BRANCHES[b as BranchName].chinese).join("");
      results.push({
        interaction_type: "three_harmony",
        chinese_name: "三合局",
        branches: sorted,
        palaces: positions,
        description: `${branchesChinese}三合${frame.element}局`,
        activated_by_lp: activated,
        severity: "mild",
      });
    } else if (present.size === 2) {
      // Partial frame (half combination)
      const branchesList = [...present].sort((a, b) => BRANCHES[a as BranchName].index - BRANCHES[b as BranchName].index);
      const positions: string[] = [];
      let activated = false;
      for (const [pos, br] of pairs) {
        if (present.has(br)) {
          positions.push(PALACE_NAMES[pos] ?? pos);
          if (pos === "luck_pillar") activated = true;
        }
      }

      const missing = [...frame.branches].find(b => !present.has(b))!;
      const branchesChinese = branchesList.map(b => BRANCHES[b as BranchName].chinese).join("");
      results.push({
        interaction_type: "half_three_harmony",
        chinese_name: "半三合",
        branches: branchesList,
        palaces: positions,
        description: `${branchesChinese}半合${frame.element}局 (missing ${BRANCHES[missing as BranchName].chinese})`,
        activated_by_lp: activated,
        severity: "mild",
      });
    }
  }

  return results;
}

// =============================================================================
// DIRECTIONAL COMBINATIONS (三会局)
// =============================================================================

export const DIRECTIONAL_COMBOS: Record<string, [string, string]> = {
  [tripleKey("Yin", "Mao", "Chen")]: ["Wood", "East"],
  [tripleKey("Si", "Wu", "Wei")]: ["Fire", "South"],
  [tripleKey("Shen", "You", "Xu")]: ["Metal", "West"],
  [tripleKey("Hai", "Zi", "Chou")]: ["Water", "North"],
};

const DIRECTIONAL_COMBO_SETS: Array<{ branches: Set<string>; element: string; direction: string }> = [
  { branches: new Set(["Yin", "Mao", "Chen"]), element: "Wood", direction: "East" },
  { branches: new Set(["Si", "Wu", "Wei"]), element: "Fire", direction: "South" },
  { branches: new Set(["Shen", "You", "Xu"]), element: "Metal", direction: "West" },
  { branches: new Set(["Hai", "Zi", "Chou"]), element: "Water", direction: "North" },
];

function detectDirectionalCombos(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);
  const allBranches = new Set(pairs.map(([, br]) => br));

  for (const combo of DIRECTIONAL_COMBO_SETS) {
    const present = new Set([...combo.branches].filter(b => allBranches.has(b)));
    if (present.size >= 3) {
      const positions: string[] = [];
      let activated = false;
      for (const [pos, br] of pairs) {
        if (combo.branches.has(br)) {
          positions.push(PALACE_NAMES[pos] ?? pos);
          if (pos === "luck_pillar") activated = true;
        }
      }

      const sorted = [...combo.branches].sort((a, b) => BRANCHES[a as BranchName].index - BRANCHES[b as BranchName].index);
      const branchesChinese = sorted.map(b => BRANCHES[b as BranchName].chinese).join("");
      results.push({
        interaction_type: "directional_combo",
        chinese_name: "三会局",
        branches: sorted,
        palaces: positions,
        description: `${branchesChinese}三会${combo.element}局 (${combo.direction})`,
        activated_by_lp: activated,
        severity: "mild",
      });
    }
  }

  return results;
}

// =============================================================================
// THREE PUNISHMENTS (三刑)
// =============================================================================

const PUNISHMENT_GROUPS: Record<string, { branches: Set<string>; chinese: string; english: string }> = {
  ungrateful: {
    branches: new Set(["Yin", "Si", "Shen"]),
    chinese: "寅巳申 恃势之刑",
    english: "Ungrateful/Power Punishment",
  },
  bullying: {
    branches: new Set(["Chou", "Wei", "Xu"]),
    chinese: "丑未戌 无礼之刑",
    english: "Bullying/Rudeness Punishment",
  },
};

const PUNISHMENT_PAIR: Array<{ branches: Set<string>; chinese: string; english: string }> = [
  {
    branches: new Set(["Zi", "Mao"]),
    chinese: "子卯 无恩之刑",
    english: "Rude/Graceless Punishment",
  },
];

const SELF_PUNISHMENT_BRANCHES = new Set(["Chen", "Wu", "You", "Hai"]);

function detectPunishments(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);
  const allBranchesList = pairs.map(([, br]) => br);
  const allBranchesSet = new Set(allBranchesList);

  // 3-branch group punishments
  for (const [, info] of Object.entries(PUNISHMENT_GROUPS)) {
    const present = new Set([...info.branches].filter(b => allBranchesSet.has(b)));
    if (present.size >= 2) {
      const positions: string[] = [];
      let activated = false;
      for (const [pos, br] of pairs) {
        if (present.has(br)) {
          positions.push(PALACE_NAMES[pos] ?? pos);
          if (pos === "luck_pillar") activated = true;
        }
      }

      const full = present.size === 3;
      const sorted = [...present].sort((a, b) => BRANCHES[a as BranchName].index - BRANCHES[b as BranchName].index);
      results.push({
        interaction_type: "punishment",
        chinese_name: full ? "三刑" : "半刑",
        branches: sorted,
        palaces: positions,
        description: `${info.chinese} (${full ? "FULL" : "PARTIAL"}) - ${info.english}`,
        activated_by_lp: activated,
        severity: full ? "severe" : "moderate",
      });
    }
  }

  // 2-branch pair punishments
  for (const info of PUNISHMENT_PAIR) {
    const present = new Set([...info.branches].filter(b => allBranchesSet.has(b)));
    if (present.size === 2) {
      const positions: string[] = [];
      let activated = false;
      for (const [pos, br] of pairs) {
        if (info.branches.has(br)) {
          positions.push(PALACE_NAMES[pos] ?? pos);
          if (pos === "luck_pillar") activated = true;
        }
      }

      const sorted = [...info.branches].sort((a, b) => BRANCHES[a as BranchName].index - BRANCHES[b as BranchName].index);
      results.push({
        interaction_type: "punishment",
        chinese_name: "二刑",
        branches: sorted,
        palaces: positions,
        description: `${info.chinese} - ${info.english}`,
        activated_by_lp: activated,
        severity: "moderate",
      });
    }
  }

  // Self-punishments (same branch appearing twice)
  const branchCounts: Record<string, number> = {};
  for (const br of allBranchesList) {
    branchCounts[br] = (branchCounts[br] ?? 0) + 1;
  }
  for (const [br, count] of Object.entries(branchCounts)) {
    if (SELF_PUNISHMENT_BRANCHES.has(br) && count >= 2) {
      const positions = pairs.filter(([, b]) => b === br).map(([pos]) => PALACE_NAMES[pos] ?? pos);
      const activated = pairs.some(([pos, b]) => b === br && pos === "luck_pillar");

      const brData = BRANCHES[br as BranchName];
      results.push({
        interaction_type: "self_punishment",
        chinese_name: "自刑",
        branches: [br, br],
        palaces: positions,
        description: `${brData.chinese}${brData.chinese}自刑 - ${brData.self_punishment_nature ?? "Self-conflict"}`,
        activated_by_lp: activated,
        severity: "moderate",
      });
    }
  }

  return results;
}

// =============================================================================
// SIX HARMS (六害)
// =============================================================================

const HARM_PAIRS_SET = new Set([
  pairKey("Zi", "Wei"), pairKey("Chou", "Wu"),
  pairKey("Yin", "Si"), pairKey("Mao", "Chen"),
  pairKey("Shen", "Hai"), pairKey("You", "Xu"),
]);

function detectHarms(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);

  for (let i = 0; i < pairs.length; i++) {
    for (let j = i + 1; j < pairs.length; j++) {
      const [pos1, br1] = pairs[i];
      const [pos2, br2] = pairs[j];
      if (HARM_PAIRS_SET.has(pairKey(br1, br2))) {
        const activated = pos1 === "luck_pillar" || pos2 === "luck_pillar";
        results.push({
          interaction_type: "harm",
          chinese_name: "六害",
          branches: [br1, br2],
          palaces: [PALACE_NAMES[pos1] ?? pos1, PALACE_NAMES[pos2] ?? pos2],
          description: `${BRANCHES[br1 as BranchName].chinese}${BRANCHES[br2 as BranchName].chinese}害`,
          activated_by_lp: activated,
          severity: "moderate",
        });
      }
    }
  }
  return results;
}

// =============================================================================
// DESTRUCTIONS (破)
// =============================================================================

const DESTRUCTION_PAIRS_SET = new Set([
  pairKey("Zi", "You"), pairKey("Chou", "Chen"),
  pairKey("Yin", "Hai"), pairKey("Mao", "Wu"),
  pairKey("Si", "Shen"), pairKey("Wei", "Xu"),
]);

function detectDestructions(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  const pairs = getAllBranches(chart);

  for (let i = 0; i < pairs.length; i++) {
    for (let j = i + 1; j < pairs.length; j++) {
      const [pos1, br1] = pairs[i];
      const [pos2, br2] = pairs[j];
      if (DESTRUCTION_PAIRS_SET.has(pairKey(br1, br2))) {
        const activated = pos1 === "luck_pillar" || pos2 === "luck_pillar";
        results.push({
          interaction_type: "destruction",
          chinese_name: "破",
          branches: [br1, br2],
          palaces: [PALACE_NAMES[pos1] ?? pos1, PALACE_NAMES[pos2] ?? pos2],
          description: `${BRANCHES[br1 as BranchName].chinese}${BRANCHES[br2 as BranchName].chinese}破`,
          activated_by_lp: activated,
          severity: "mild",
        });
      }
    }
  }
  return results;
}

// =============================================================================
// HEAVENLY STEM COMBINATIONS (天干合)
// =============================================================================

const STEM_COMBO_CHINESE: Record<string, string> = {
  Jia: "甲己合土", Ji: "甲己合土",
  Yi: "乙庚合金", Geng: "乙庚合金",
  Bing: "丙辛合水", Xin: "丙辛合水",
  Ding: "丁壬合木", Ren: "丁壬合木",
  Wu: "戊癸合火", Gui: "戊癸合火",
};

function detectStemCombinations(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];

  // Collect all (position, stem) pairs
  const stemPairs: Array<[string, StemName]> = [];
  for (const pos of ["year", "month", "day", "hour"]) {
    stemPairs.push([pos, chart.pillars[pos].stem]);
  }
  if (chart.luck_pillar) {
    stemPairs.push(["luck_pillar", chart.luck_pillar.stem]);
  }
  for (const [pos, pillar] of Object.entries(chart.time_period_pillars)) {
    stemPairs.push([pos, pillar.stem]);
  }

  // Collect visible HS elements for transformation check
  const hsElements = new Set<string>();
  for (const pos of ["year", "month", "day", "hour"]) {
    hsElements.add(STEMS[chart.pillars[pos].stem].element);
  }

  // Check all pairs
  const seen = new Set<string>();
  for (let i = 0; i < stemPairs.length; i++) {
    const [pos1, stem1] = stemPairs[i];
    const combinesWith = STEMS[stem1].combines_with;
    if (!combinesWith) continue;

    for (let j = i + 1; j < stemPairs.length; j++) {
      const [pos2, stem2] = stemPairs[j];
      if (stem2 !== combinesWith) continue;

      const seenKey = pairKey(pos1, pos2);
      if (seen.has(seenKey)) continue;
      seen.add(seenKey);

      const resultElement = STEMS[stem1].combination_element;
      const transformed = hsElements.has(resultElement);
      const chinese = STEM_COMBO_CHINESE[stem1] ?? "天干合";

      // Adjacency check
      const pillarOrder = ["year", "month", "day", "hour"];
      let adjacent = false;
      const idx1 = pillarOrder.indexOf(pos1);
      const idx2 = pillarOrder.indexOf(pos2);
      if (idx1 >= 0 && idx2 >= 0) {
        adjacent = Math.abs(idx1 - idx2) === 1;
      }

      const descParts = [
        `${STEMS[stem1].chinese} (${pos1}) + ${STEMS[stem2].chinese} (${pos2})`,
        `→ ${resultElement}`,
        transformed ? "(transformed)" : "(combined — no visible HS catalyst)",
      ];
      if (!adjacent) {
        descParts.push("(distant — weaker bond)");
      }

      results.push({
        interaction_type: "stem_combination",
        chinese_name: chinese,
        branches: [stem1, stem2], // stems stored in branches field
        palaces: [PALACE_NAMES[pos1] ?? pos1, PALACE_NAMES[pos2] ?? pos2],
        description: descParts.join(" "),
        activated_by_lp: pos1 === "luck_pillar" || pos2 === "luck_pillar",
        severity: "mild",
      });
    }
  }

  return results;
}

// =============================================================================
// MASTER FUNCTION: Detect All Interactions
// =============================================================================

export function detectAllInteractions(chart: ChartData): BranchInteraction[] {
  const results: BranchInteraction[] = [];
  // Branch interactions
  results.push(...detectClashes(chart));
  results.push(...detectHarmonies(chart));
  results.push(...detectThreeHarmony(chart));
  results.push(...detectDirectionalCombos(chart));
  results.push(...detectPunishments(chart));
  results.push(...detectHarms(chart));
  results.push(...detectDestructions(chart));
  // Stem interactions
  results.push(...detectStemCombinations(chart));
  return results;
}

export function getNegativeInteractions(chart: ChartData): BranchInteraction[] {
  const negativeTypes = new Set(["clash", "punishment", "self_punishment", "harm", "destruction"]);
  return detectAllInteractions(chart).filter(i => negativeTypes.has(i.interaction_type));
}

export function getPositiveInteractions(chart: ChartData): BranchInteraction[] {
  const positiveTypes = new Set(["harmony", "three_harmony", "half_three_harmony", "directional_combo"]);
  return detectAllInteractions(chart).filter(i => positiveTypes.has(i.interaction_type));
}
