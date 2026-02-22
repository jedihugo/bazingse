import 'server-only';

// =============================================================================
// Qi Phase Contextual Analysis (十二长生深度分析)
// All 12 phases x 4 pillars + tandem effects with Shen Sha.
// =============================================================================

import { getQiPhaseForPillar } from '../qi-phase';
import type { ChartData, ShenShaResult } from './models';

// =============================================================================
// PILLAR-CONTEXTUAL MEANINGS (12 phases x 4 positions)
// =============================================================================

const PHASE_PILLAR_MEANINGS: Record<string, Record<string, string>> = {
  changsheng: {
    year: "Born into a growing family, pioneering lineage, ancestors who started fresh",
    month: "Career with fresh beginnings, good for entrepreneurship, building from scratch",
    day: "Vitality in self and marriage, spouse brings new energy, relationship grows over time",
    hour: "Children with great potential, legacy of new beginnings, vibrant old age",
  },
  muyu: {
    year: "Family scandals or instability in ancestry, parents with romantic complications",
    month: "Career instability, romantic entanglements at work, changing jobs frequently",
    day: "Romantic but turbulent marriage, strong sexual energy, spouse with wild streak",
    hour: "Children with rebellious nature, unstable later years, romance in old age",
  },
  guandai: {
    year: "Family gaining recognition, ancestors who rose in social status",
    month: "Career advancement phase, gaining professional credentials, respected at work",
    day: "Maturing self/marriage, taking responsibility in partnership, growing together",
    hour: "Children who achieve recognition, legacy of achievement, dignified old age",
  },
  linguan: {
    year: "Powerful family, ancestors in government or authority positions",
    month: "Strong career authority, leadership roles, professional peak",
    day: "Authoritative personality, spouse with power/status, commanding presence",
    hour: "Children in authority positions, legacy of power, respected elder",
  },
  diwang: {
    year: "Extremely powerful family, peak of ancestral fortune — but at turning point",
    month: "Career at absolute peak — maximum achievement but also maximum vulnerability to decline",
    day: "Maximum personal power, dominant in marriage — risk of overbearing. Life's turning point",
    hour: "Children at peak potential but risk of excess, legacy that peaks then transforms",
  },
  shuai: {
    year: "Family past its prime, declining ancestral fortune, inherited debts or burdens",
    month: "Career losing momentum, need to conserve resources, past professional peak",
    day: "Personal energy declining, marriage entering comfortable but less passionate phase",
    hour: "Children face declining circumstances, legacy needs protection, health-conscious old age",
  },
  bing: {
    year: "Sickly ancestors, inherited health vulnerabilities, childhood health issues",
    month: "Career struggles, professional setbacks, work-related stress or health issues",
    day: "Personal health vulnerabilities, marriage under stress, spouse may have health issues",
    hour: "Children with health concerns, old age requiring medical attention, fragile legacy",
  },
  si: {
    year: "Ancestral endings, family line transformation, loss of heritage",
    month: "Career ending or major transformation, old profession dies to birth new one",
    day: "Transformation of self, marriage through death-and-rebirth cycle, complete personal change",
    hour: "Children bring endings that create new beginnings, twilight as transformation",
  },
  mu: {
    year: "Hidden family wealth or secrets, ancestors left buried treasures — literal or figurative",
    month: "Career potential locked away, stored professional capabilities awaiting release via clash",
    day: "Spouse carries hidden assets or hidden emotional depth, relationship has buried potential",
    hour: "Children hold things inside, legacy stored for future generations, retirement savings",
  },
  jue: {
    year: "Complete break from ancestry, orphan energy, family line cut",
    month: "Career void, complete professional restart needed, old path extinct",
    day: "Self at void point — seed of complete rebirth. Marriage may start from absolute zero",
    hour: "Children face starting from nothing, legacy of spiritual emptiness becoming freedom",
  },
  tai: {
    year: "Family in transition, new generation forming, pregnancy energy in family history",
    month: "Career plans forming but not yet manifest, professional ideas gestating",
    day: "Relationship developing, potential not yet realized, self in planning stage",
    hour: "Children planned or forming, legacy being conceived, old age as new beginning",
  },
  yang: {
    year: "Protected childhood, well-nurtured ancestry, family that builds slowly",
    month: "Career being nurtured by mentors, slow professional development, building foundation",
    day: "Nurturing relationship, patient partnership, self being cultivated over time",
    hour: "Children well-cared for, legacy being tended carefully, comfortable retirement",
  },
};

// =============================================================================
// TANDEM EFFECTS: Qi Phase + Shen Sha combinations
// =============================================================================
// [qi_phase_id, shen_sha_chinese, effect_description, spiritual_bonus]

export const TANDEM_EFFECTS: ReadonlyArray<readonly [string, string, string, number]> = [
  ["muyu", "桃花", "EXTREMELY strong romantic/affair energy — sexual magnetism at maximum", 0],
  ["muyu", "偏印", "Vulnerability + unconventional thinking = spiritual opening, psychic sensitivity", 5],
  ["diwang", "羊刃", "Dangerously aggressive, accident-prone — but extremely powerful if channeled", 0],
  ["diwang", "将星", "Born commander — natural authority at peak, military/leadership destiny", 0],
  ["mu", "华盖", "Deep spiritual storage — can perceive hidden/mystical things, meditation talent", 10],
  ["mu", "空亡", "Buried emptiness — hidden losses, but also gateway to spiritual realm", 5],
  ["changsheng", "天乙贵人", "Blessed beginning — protected by helpers, smooth start in that domain", 0],
  ["changsheng", "禄神", "Born into wealth flow, self-renewing prosperity", 0],
  ["jue", "空亡", "Complete emptiness — extremely thin veil between worlds, high spiritual sensitivity", 10],
  ["jue", "童子", "Past-life soul — strong indicator of being a spirit sent from heaven", 10],
  ["linguan", "文昌贵人", "Scholar-official destiny — authority through education and knowledge", 0],
  ["bing", "天医", "Healer archetype — illness in chart drives toward medical/healing career", 0],
  ["shuai", "劫煞", "Declining energy + robbery = vulnerable to loss, timing of financial setback", 0],
  ["tai", "红鸾", "New romance forming — pregnancy of love, relationship about to be born", 0],
  ["si", "华盖", "Death + solitude = deep mystical transformation, near-death spiritual awakening", 8],
  ["yang", "天乙贵人", "Nurturing protected by noble people — slow but blessed development", 0],
];

export function analyzeQiPhases(
  chart: ChartData,
  shenShaResults: ShenShaResult[],
): { pillars: Record<string, Record<string, unknown>>; spiritual_bonus: number } {
  const dmStem = chart.day_master;
  const presentShenSha = new Set(
    shenShaResults.filter(r => r.present).map(r => r.name_chinese));

  // Build a map of shen_sha per palace for tandem detection
  const shenShaByPalace: Record<string, Set<string>> = {
    year: new Set(), month: new Set(), day: new Set(), hour: new Set(),
  };
  for (const r of shenShaResults) {
    if (r.present && r.palace && r.palace in shenShaByPalace) {
      shenShaByPalace[r.palace].add(r.name_chinese);
    }
  }

  const resultPillars: Record<string, Record<string, unknown>> = {};
  let totalSpiritualBonus = 0;

  for (const pos of ["year", "month", "day", "hour"]) {
    const pillar = chart.pillars[pos];
    const phase = getQiPhaseForPillar(dmStem, pillar.branch);

    if (!phase) {
      resultPillars[pos] = {
        phase_id: null,
        phase_chinese: "未知",
        phase_english: "Unknown",
        strength: "unknown",
        interpretation: "Cannot determine qi phase",
        tandem_effects: [],
      };
      continue;
    }

    // Note: TS getQiPhaseForPillar returns object with .id property (not dict)
    const phaseId = phase.id;
    const meanings = PHASE_PILLAR_MEANINGS[phaseId] ?? {};
    const interpretation = meanings[pos] ?? "No specific interpretation available";

    // Check tandem effects for this pillar
    const tandemHits: Array<Record<string, unknown>> = [];
    for (const [tPhase, tShensha, tEffect, tSpiritual] of TANDEM_EFFECTS) {
      if (phaseId === tPhase) {
        if (shenShaByPalace[pos].has(tShensha) || presentShenSha.has(tShensha)) {
          tandemHits.push({
            shen_sha: tShensha,
            effect: tEffect,
            spiritual_bonus: tSpiritual,
          });
          totalSpiritualBonus += tSpiritual;
        }
      }
    }

    resultPillars[pos] = {
      phase_id: phaseId,
      phase_chinese: phase.chinese,
      phase_english: phase.english,
      strength: phase.strength ?? "unknown",
      interpretation,
      tandem_effects: tandemHits,
    };
  }

  return {
    pillars: resultPillars,
    spiritual_bonus: totalSpiritualBonus,
  };
}
