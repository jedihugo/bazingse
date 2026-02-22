import 'server-only';

// =============================================================================
// SPECIAL STARS PATTERNS (神煞 Shen Sha)
// =============================================================================
// Classical BaZi special stars expressed as PatternSpecs.
// These are context-dependent patterns based on Day Master or Year Branch.
// Includes: KONG_WANG, GUI_REN, TAO_HUA, YI_MA, YANG_REN, LU_SHEN, HUA_GAI
// Ported from api/library/pattern_engine/patterns/special_stars.py
// =============================================================================

import {
  type PatternSpec,
  PatternCategory,
  NodeType,
  LifeDomain,
  BadgeType,
} from '../pattern-spec';

// =============================================================================
// KONG WANG (空亡) - Void/Empty Stars
// =============================================================================
// Each Jia-Zi decade has two "empty" branches where energy is void.
// Determined by Day Master's Jia-Zi pillar position.

export const KONG_WANG_LOOKUP: Record<string, ReadonlySet<string>> = {
  "Jia": new Set(["Xu", "Hai"]),
  "Yi": new Set(["Xu", "Hai"]),
  "Bing": new Set(["Shen", "You"]),
  "Ding": new Set(["Shen", "You"]),
  "Wu": new Set(["Wu", "Wei"]),
  "Ji": new Set(["Wu", "Wei"]),
  "Geng": new Set(["Chen", "Si"]),
  "Xin": new Set(["Chen", "Si"]),
  "Ren": new Set(["Yin", "Mao"]),
  "Gui": new Set(["Yin", "Mao"]),
};

function generateKongWangPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [dayStem, emptyBranches] of Object.entries(KONG_WANG_LOOKUP)) {
    for (const branch of emptyBranches) {
      patterns.push({
        id: `KONG_WANG~${dayStem}~${branch}`,
        category: PatternCategory.KONG_WANG,
        priority: 300,
        chinese_name: "空亡",
        english_name: `Void Star (${branch})`,
        node_filters: [
          { branches: new Set([branch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
        ],
        min_nodes: 1,
        base_score_combined: 8.0,
        distance_multipliers: [1.0, 0.8, 0.6],
        badge_type: BadgeType.COMBINATION,
        life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
        pillar_meanings: {
          year: "Ancestral void - detachment from family legacy",
          month: "Career void - unconventional career path",
          day: "Spouse void - late marriage or unique partnership",
          hour: "Children void - fewer children or spiritual focus",
        },
        description: `Day Master ${dayStem} has void in ${branch} - emptiness in that domain`,
        classical_source: "三命通會",
        notes: `Context-dependent: Only applies when Day Stem is ${dayStem}`,
      });
    }
  }

  return patterns;
}

export const KONG_WANG_PATTERNS: PatternSpec[] = generateKongWangPatterns();


// =============================================================================
// GUI REN (貴人) - Noble Person Stars
// =============================================================================
// Based on Day Master, certain branches indicate noble helpers.

export const GUI_REN_LOOKUP: Record<string, ReadonlySet<string>> = {
  "Jia": new Set(["Chou", "Wei"]),
  "Yi": new Set(["Zi", "Shen"]),
  "Bing": new Set(["Hai", "You"]),
  "Ding": new Set(["Hai", "You"]),
  "Wu": new Set(["Chou", "Wei"]),
  "Ji": new Set(["Zi", "Shen"]),
  "Geng": new Set(["Chou", "Wei"]),
  "Xin": new Set(["Yin", "Wu"]),
  "Ren": new Set(["Mao", "Si"]),
  "Gui": new Set(["Mao", "Si"]),
};

function generateGuiRenPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [dayStem, nobleBranches] of Object.entries(GUI_REN_LOOKUP)) {
    for (const branch of nobleBranches) {
      patterns.push({
        id: `GUI_REN~${dayStem}~${branch}`,
        category: PatternCategory.GUI_REN,
        priority: 310,
        chinese_name: "貴人",
        english_name: `Noble Person (${branch})`,
        node_filters: [
          { branches: new Set([branch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
        ],
        min_nodes: 1,
        base_score_combined: 12.0,
        distance_multipliers: [1.0, 0.85, 0.7],
        badge_type: BadgeType.COMBINATION,
        life_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP, LifeDomain.WEALTH]),
        pillar_meanings: {
          year: "Noble ancestry - helpful family connections",
          month: "Noble career - mentors and sponsors at work",
          day: "Noble partner - spouse brings good fortune",
          hour: "Noble children - children bring honor",
        },
        event_mapping: {
          primary_domains: new Set([LifeDomain.CAREER, LifeDomain.RELATIONSHIP]),
          positive_events: [
            ["career", "promotion"],
            ["career", "recognition"],
            ["relationship", "new_relationship"],
            ["wealth", "windfall"],
          ],
          domain_sentiment: [
            ["career", "positive"],
            ["relationship", "positive"],
            ["wealth", "positive"],
          ],
        },
        description: `Day Master ${dayStem} has noble person in ${branch} - benefactors and helpers`,
        classical_source: "三命通會",
        notes: `Context-dependent: Only applies when Day Stem is ${dayStem}`,
      });
    }
  }

  return patterns;
}

export const GUI_REN_PATTERNS: PatternSpec[] = generateGuiRenPatterns();


// =============================================================================
// TAO HUA (桃花) - Peach Blossom Stars
// =============================================================================
// Romance/attraction stars based on Year/Day Branch.

export const TAO_HUA_LOOKUP: Record<string, string> = {
  "Yin": "Mao",
  "Wu": "Mao",
  "Xu": "Mao",
  "Shen": "You",
  "Zi": "You",
  "Chen": "You",
  "Si": "Wu",
  "You": "Wu",
  "Chou": "Wu",
  "Hai": "Zi",
  "Mao": "Zi",
  "Wei": "Zi",
};

function generateTaoHuaPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [baseBranch, peachBranch] of Object.entries(TAO_HUA_LOOKUP)) {
    patterns.push({
      id: `TAO_HUA~${baseBranch}~${peachBranch}`,
      category: PatternCategory.TAO_HUA,
      priority: 320,
      chinese_name: "桃花",
      english_name: `Peach Blossom (${peachBranch})`,
      node_filters: [
        { branches: new Set([peachBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 10.0,
      distance_multipliers: [1.0, 0.8, 0.6],
      badge_type: BadgeType.COMBINATION,
      life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.CAREER]),
      pillar_meanings: {
        year: "Family romance karma - attractive lineage",
        month: "Career charisma - popular at work",
        day: "Personal charm - romantic nature",
        hour: "Late life romance - continued attraction",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.RELATIONSHIP]),
        positive_events: [
          ["relationship", "new_relationship"],
          ["relationship", "marriage"],
          ["career", "recognition"],
        ],
        negative_events: [
          ["relationship", "breakup"],
          ["relationship", "conflict_partner"],
        ],
        domain_sentiment: [
          ["relationship", "conditional"],
        ],
      },
      description: `Year/Day Branch ${baseBranch} has Peach Blossom in ${peachBranch} - romance and attraction`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Year or Day Branch is ${baseBranch}`,
    });
  }

  return patterns;
}

export const TAO_HUA_PATTERNS: PatternSpec[] = generateTaoHuaPatterns();


// =============================================================================
// YI MA (驛馬) - Traveling Horse Stars
// =============================================================================
// Travel and movement stars based on Year/Day Branch.

export const YI_MA_LOOKUP: Record<string, string> = {
  "Yin": "Shen",
  "Wu": "Shen",
  "Xu": "Shen",
  "Shen": "Yin",
  "Zi": "Yin",
  "Chen": "Yin",
  "Si": "Hai",
  "You": "Hai",
  "Chou": "Hai",
  "Hai": "Si",
  "Mao": "Si",
  "Wei": "Si",
};

function generateYiMaPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [baseBranch, travelBranch] of Object.entries(YI_MA_LOOKUP)) {
    patterns.push({
      id: `YI_MA~${baseBranch}~${travelBranch}`,
      category: PatternCategory.YI_MA,
      priority: 330,
      chinese_name: "驛馬",
      english_name: `Traveling Horse (${travelBranch})`,
      node_filters: [
        { branches: new Set([travelBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 10.0,
      distance_multipliers: [1.0, 0.8, 0.6],
      badge_type: BadgeType.COMBINATION,
      life_domains: new Set([LifeDomain.TRAVEL, LifeDomain.CAREER]),
      pillar_meanings: {
        year: "Ancestral travel - family immigration history",
        month: "Career travel - work-related moves",
        day: "Personal movement - restless nature",
        hour: "Late life travel - retirement relocations",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.TRAVEL]),
        positive_events: [
          ["travel", "relocation_major"],
          ["travel", "immigration"],
          ["career", "job_new"],
        ],
        domain_sentiment: [
          ["travel", "conditional"],
          ["career", "conditional"],
        ],
      },
      description: `Year/Day Branch ${baseBranch} has Travel Horse in ${travelBranch} - movement and change`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Year or Day Branch is ${baseBranch}`,
    });
  }

  return patterns;
}

export const YI_MA_PATTERNS: PatternSpec[] = generateYiMaPatterns();


// =============================================================================
// YANG REN (羊刃) - Yang Blade Stars
// =============================================================================
// Aggressive/cutting energy based on Day Master.

export const YANG_REN_LOOKUP: Record<string, string> = {
  "Jia": "Mao",
  "Bing": "Wu",
  "Wu": "Wu",
  "Geng": "You",
  "Ren": "Zi",
};

function generateYangRenPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [dayStem, bladeBranch] of Object.entries(YANG_REN_LOOKUP)) {
    patterns.push({
      id: `YANG_REN~${dayStem}~${bladeBranch}`,
      category: PatternCategory.YANG_REN,
      priority: 340,
      chinese_name: "羊刃",
      english_name: `Yang Blade (${bladeBranch})`,
      node_filters: [
        { branches: new Set([bladeBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 12.0,
      distance_multipliers: [1.0, 0.85, 0.7],
      badge_type: BadgeType.CLASH,
      life_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER, LifeDomain.LEGAL]),
      pillar_meanings: {
        year: "Ancestral blade - aggressive family nature",
        month: "Career blade - competitive work environment",
        day: "Personal blade - aggressive personality",
        hour: "Late blade - sharp tongue in old age",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.HEALTH, LifeDomain.CAREER]),
        positive_events: [
          ["career", "promotion"],
          ["career", "business_start"],
        ],
        negative_events: [
          ["health", "injury_accident"],
          ["health", "surgery"],
          ["legal", "lawsuit_filed"],
        ],
        domain_sentiment: [
          ["health", "negative"],
          ["career", "conditional"],
          ["legal", "negative"],
        ],
      },
      description: `Day Master ${dayStem} has Yang Blade in ${bladeBranch} - aggressive/cutting energy`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Day Stem is ${dayStem} (Yang stems only)`,
    });
  }

  return patterns;
}

export const YANG_REN_PATTERNS: PatternSpec[] = generateYangRenPatterns();


// =============================================================================
// LU SHEN (祿神) - Prosperity God Stars
// =============================================================================
// Self-prosperity based on Day Master.

export const LU_SHEN_LOOKUP: Record<string, string> = {
  "Jia": "Yin",
  "Yi": "Mao",
  "Bing": "Si",
  "Ding": "Wu",
  "Wu": "Si",
  "Ji": "Wu",
  "Geng": "Shen",
  "Xin": "You",
  "Ren": "Hai",
  "Gui": "Zi",
};

function generateLuShenPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [dayStem, prosperityBranch] of Object.entries(LU_SHEN_LOOKUP)) {
    patterns.push({
      id: `LU_SHEN~${dayStem}~${prosperityBranch}`,
      category: PatternCategory.LU_SHEN,
      priority: 350,
      chinese_name: "祿神",
      english_name: `Prosperity God (${prosperityBranch})`,
      node_filters: [
        { branches: new Set([prosperityBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 12.0,
      distance_multipliers: [1.0, 0.85, 0.7],
      badge_type: BadgeType.COMBINATION,
      life_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]),
      pillar_meanings: {
        year: "Ancestral prosperity - inherited wealth",
        month: "Career prosperity - good salary",
        day: "Personal prosperity - self-made wealth",
        hour: "Late prosperity - comfortable retirement",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.WEALTH, LifeDomain.CAREER]),
        positive_events: [
          ["wealth", "income_increase"],
          ["wealth", "investment_gain"],
          ["career", "promotion"],
        ],
        domain_sentiment: [
          ["wealth", "positive"],
          ["career", "positive"],
        ],
      },
      description: `Day Master ${dayStem} has Prosperity God in ${prosperityBranch} - self-made wealth`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Day Stem is ${dayStem}`,
    });
  }

  return patterns;
}

export const LU_SHEN_PATTERNS: PatternSpec[] = generateLuShenPatterns();


// =============================================================================
// HUA GAI (華蓋) - Canopy Stars
// =============================================================================
// Artistic/spiritual inclination based on Year/Day Branch.

export const HUA_GAI_LOOKUP: Record<string, string> = {
  "Yin": "Xu",
  "Wu": "Xu",
  "Xu": "Xu",
  "Shen": "Chen",
  "Zi": "Chen",
  "Chen": "Chen",
  "Si": "Chou",
  "You": "Chou",
  "Chou": "Chou",
  "Hai": "Wei",
  "Mao": "Wei",
  "Wei": "Wei",
};

function generateHuaGaiPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [baseBranch, canopyBranch] of Object.entries(HUA_GAI_LOOKUP)) {
    patterns.push({
      id: `HUA_GAI~${baseBranch}~${canopyBranch}`,
      category: PatternCategory.HUA_GAI,
      priority: 360,
      chinese_name: "華蓋",
      english_name: `Canopy Star (${canopyBranch})`,
      node_filters: [
        { branches: new Set([canopyBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 8.0,
      distance_multipliers: [1.0, 0.8, 0.6],
      badge_type: BadgeType.COMBINATION,
      life_domains: new Set([LifeDomain.EDUCATION, LifeDomain.CAREER]),
      pillar_meanings: {
        year: "Ancestral canopy - artistic/spiritual lineage",
        month: "Career canopy - creative profession",
        day: "Personal canopy - artistic/spiritual nature",
        hour: "Late canopy - contemplative old age",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.EDUCATION]),
        positive_events: [
          ["education", "certification"],
          ["career", "recognition"],
        ],
        domain_sentiment: [
          ["education", "positive"],
          ["career", "positive"],
        ],
      },
      description: `Year/Day Branch ${baseBranch} has Canopy in ${canopyBranch} - artistic/spiritual inclination`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Year or Day Branch is ${baseBranch}`,
    });
  }

  return patterns;
}

export const HUA_GAI_PATTERNS: PatternSpec[] = generateHuaGaiPatterns();


// =============================================================================
// GU CHEN & GUA SU (孤辰寡宿) - Lonely and Widow Stars
// =============================================================================
// Critical for marriage analysis. Based on Year Branch.

export const GU_CHEN_GUA_SU_LOOKUP: Record<string, { gu_chen: string; gua_su: string }> = {
  "Zi": { gu_chen: "Yin", gua_su: "Xu" },
  "Chou": { gu_chen: "Yin", gua_su: "Xu" },
  "Yin": { gu_chen: "Si", gua_su: "Chou" },
  "Mao": { gu_chen: "Si", gua_su: "Chou" },
  "Chen": { gu_chen: "Si", gua_su: "Chou" },
  "Si": { gu_chen: "Shen", gua_su: "Chen" },
  "Wu": { gu_chen: "Shen", gua_su: "Chen" },
  "Wei": { gu_chen: "Shen", gua_su: "Chen" },
  "Shen": { gu_chen: "Hai", gua_su: "Wei" },
  "You": { gu_chen: "Hai", gua_su: "Wei" },
  "Xu": { gu_chen: "Hai", gua_su: "Wei" },
  "Hai": { gu_chen: "Yin", gua_su: "Xu" },
};

function generateGuChenPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [yearBranch, stars] of Object.entries(GU_CHEN_GUA_SU_LOOKUP)) {
    const lonelyBranch = stars.gu_chen;
    patterns.push({
      id: `GU_CHEN~${yearBranch}~${lonelyBranch}`,
      category: PatternCategory.GU_CHEN,
      priority: 370,
      chinese_name: "孤辰",
      english_name: `Lonely Star (${lonelyBranch})`,
      node_filters: [
        { branches: new Set([lonelyBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 10.0,
      distance_multipliers: [1.0, 0.85, 0.7],
      badge_type: BadgeType.CLASH,
      life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
      pillar_meanings: {
        year: "Ancestral loneliness - isolated family history",
        month: "Career loneliness - works alone, independent",
        day: "Personal loneliness - difficulty finding/keeping spouse",
        hour: "Late loneliness - solitary in old age",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.RELATIONSHIP]),
        negative_events: [
          ["relationship", "breakup"],
          ["relationship", "divorce"],
          ["family", "separation"],
        ],
        domain_sentiment: [
          ["relationship", "negative"],
          ["family", "negative"],
        ],
      },
      description: `Year Branch ${yearBranch} has Lonely Star in ${lonelyBranch} - isolation tendency`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Year Branch is ${yearBranch}. In Spouse Palace indicates marriage difficulty.`,
    });
  }

  return patterns;
}

function generateGuaSuPatterns(): PatternSpec[] {
  const patterns: PatternSpec[] = [];

  for (const [yearBranch, stars] of Object.entries(GU_CHEN_GUA_SU_LOOKUP)) {
    const widowBranch = stars.gua_su;
    patterns.push({
      id: `GUA_SU~${yearBranch}~${widowBranch}`,
      category: PatternCategory.GUA_SU,
      priority: 375,
      chinese_name: "寡宿",
      english_name: `Widow Star (${widowBranch})`,
      node_filters: [
        { branches: new Set([widowBranch]), node_types: new Set([NodeType.EARTHLY_BRANCH]) },
      ],
      min_nodes: 1,
      base_score_combined: 10.0,
      distance_multipliers: [1.0, 0.85, 0.7],
      badge_type: BadgeType.CLASH,
      life_domains: new Set([LifeDomain.RELATIONSHIP, LifeDomain.FAMILY]),
      pillar_meanings: {
        year: "Ancestral widow - widowhood in family history",
        month: "Career solitude - professional independence",
        day: "Personal widow - risk of losing partner or no marriage",
        hour: "Late solitude - alone in old age",
      },
      event_mapping: {
        primary_domains: new Set([LifeDomain.RELATIONSHIP]),
        negative_events: [
          ["relationship", "breakup"],
          ["relationship", "divorce"],
          ["family", "loss_death"],
        ],
        domain_sentiment: [
          ["relationship", "negative"],
          ["family", "negative"],
        ],
      },
      description: `Year Branch ${yearBranch} has Widow Star in ${widowBranch} - solitude tendency`,
      classical_source: "三命通會",
      notes: `Context-dependent: Only applies when Year Branch is ${yearBranch}. In Spouse Palace indicates widowhood risk.`,
    });
  }

  return patterns;
}

export const GU_CHEN_PATTERNS: PatternSpec[] = generateGuChenPatterns();
export const GUA_SU_PATTERNS: PatternSpec[] = generateGuaSuPatterns();


// =============================================================================
// COMBINED EXPORT
// =============================================================================

export const ALL_SPECIAL_STAR_PATTERNS: PatternSpec[] = [
  ...KONG_WANG_PATTERNS,
  ...GUI_REN_PATTERNS,
  ...TAO_HUA_PATTERNS,
  ...YI_MA_PATTERNS,
  ...YANG_REN_PATTERNS,
  ...LU_SHEN_PATTERNS,
  ...HUA_GAI_PATTERNS,
  ...GU_CHEN_PATTERNS,
  ...GUA_SU_PATTERNS,
];

export function getAllSpecialStarPatterns(): PatternSpec[] {
  return [...ALL_SPECIAL_STAR_PATTERNS];
}

export function getSpecialStarsForDayMaster(dayStem: string): PatternSpec[] {
  const applicable: PatternSpec[] = [];

  // Kong Wang
  const kongWangBranches = KONG_WANG_LOOKUP[dayStem];
  if (kongWangBranches) {
    for (const branch of kongWangBranches) {
      applicable.push(
        ...KONG_WANG_PATTERNS.filter((p) => p.id.includes(`~${dayStem}~${branch}`))
      );
    }
  }

  // Gui Ren
  const guiRenBranches = GUI_REN_LOOKUP[dayStem];
  if (guiRenBranches) {
    for (const branch of guiRenBranches) {
      applicable.push(
        ...GUI_REN_PATTERNS.filter((p) => p.id.includes(`~${dayStem}~${branch}`))
      );
    }
  }

  // Yang Ren (only Yang stems)
  const yangRenBranch = YANG_REN_LOOKUP[dayStem];
  if (yangRenBranch) {
    applicable.push(
      ...YANG_REN_PATTERNS.filter((p) => p.id.includes(`~${dayStem}~${yangRenBranch}`))
    );
  }

  // Lu Shen
  const luShenBranch = LU_SHEN_LOOKUP[dayStem];
  if (luShenBranch) {
    applicable.push(
      ...LU_SHEN_PATTERNS.filter((p) => p.id.includes(`~${dayStem}~${luShenBranch}`))
    );
  }

  return applicable;
}

export function getSpecialStarsForYearBranch(yearBranch: string): PatternSpec[] {
  const applicable: PatternSpec[] = [];

  // Gu Chen (Lonely Star)
  const gcgsStars = GU_CHEN_GUA_SU_LOOKUP[yearBranch];
  if (gcgsStars) {
    const lonelyBranch = gcgsStars.gu_chen;
    applicable.push(
      ...GU_CHEN_PATTERNS.filter((p) => p.id.includes(`~${yearBranch}~${lonelyBranch}`))
    );

    // Gua Su (Widow Star)
    const widowBranch = gcgsStars.gua_su;
    applicable.push(
      ...GUA_SU_PATTERNS.filter((p) => p.id.includes(`~${yearBranch}~${widowBranch}`))
    );
  }

  // Hua Gai (Imperial Canopy)
  const canopyBranch = HUA_GAI_LOOKUP[yearBranch];
  if (canopyBranch) {
    applicable.push(
      ...HUA_GAI_PATTERNS.filter((p) => p.id.includes(`~${yearBranch}~${canopyBranch}`))
    );
  }

  // Tao Hua (Peach Blossom)
  const peachBranch = TAO_HUA_LOOKUP[yearBranch];
  if (peachBranch) {
    applicable.push(
      ...TAO_HUA_PATTERNS.filter((p) => p.id.includes(`~${yearBranch}~${peachBranch}`))
    );
  }

  // Yi Ma (Travel Horse)
  const horseBranch = YI_MA_LOOKUP[yearBranch];
  if (horseBranch) {
    applicable.push(
      ...YI_MA_PATTERNS.filter((p) => p.id.includes(`~${yearBranch}~${horseBranch}`))
    );
  }

  return applicable;
}
