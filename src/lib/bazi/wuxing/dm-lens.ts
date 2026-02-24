// =============================================================================
// DM LENS — Day Master Support-Pressure Analysis (Step 8b)
// =============================================================================
// Categorizes element totals from the DM's perspective into 5 Ten God groups.
// Pure re-categorization of WuxingResult data — no new calculations.
// =============================================================================

import type { Element } from '../core';
import type { WuxingResult, DayMasterSummary } from './calculator';
import { SEASONAL_MATRIX } from './tables';
import type { SeasonalState } from './tables';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type TenGodGroup = 'companion' | 'resource' | 'output' | 'wealth' | 'power';
export type DmStrength = DayMasterSummary['strength'];

export interface DmLensRow {
  role: TenGodGroup;
  roleZh: string;        // e.g. '同我 Companion'
  tenGodZh: string;      // e.g. '比劫'
  element: Element;
  points: number;
  percent: number;
  narrative: string;
}

export interface CrossPattern {
  id: string;             // e.g. 'sha_yin_xiang_sheng'
  nameZh: string;         // e.g. '杀印相生'
  narrative: string;
}

export interface DmLensResult {
  dmStem: string;
  dmElement: Element;
  dmPercent: number;
  dmStrength: DmStrength;
  dmStrengthZh: string;
  seasonalState: string;     // '旺' | '相' | '休' | '囚' | '死' | ''
  rows: DmLensRow[];
  supportTotal: number;
  supportPercent: number;
  drainTotal: number;
  drainPercent: number;
  ratio: string;             // e.g. '0.3:1'
  crossPatterns: CrossPattern[];
  synthesis: string;         // 1-2 line overall narrative
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const PRODUCES: Record<Element, Element> = {
  Wood: 'Fire', Fire: 'Earth', Earth: 'Metal', Metal: 'Water', Water: 'Wood',
};

const CONTROLS: Record<Element, Element> = {
  Wood: 'Earth', Fire: 'Metal', Earth: 'Water', Metal: 'Wood', Water: 'Fire',
};

/** What produces this element */
const PRODUCED_BY: Record<Element, Element> = {
  Wood: 'Water', Fire: 'Wood', Earth: 'Fire', Metal: 'Earth', Water: 'Metal',
};

/** What controls this element */
const CONTROLLED_BY: Record<Element, Element> = {
  Wood: 'Metal', Fire: 'Water', Earth: 'Wood', Metal: 'Fire', Water: 'Earth',
};

const STRENGTH_ZH: Record<DmStrength, string> = {
  dominant: '极强',
  strong: '偏强',
  balanced: '中和',
  weak: '偏弱',
  very_weak: '极弱',
};

const ROLE_META: Record<TenGodGroup, { roleZh: string; tenGodZh: string }> = {
  companion: { roleZh: '同我 Companion',  tenGodZh: '比劫' },
  resource:  { roleZh: '生我 Resource',   tenGodZh: '印星' },
  output:    { roleZh: '我生 Output',     tenGodZh: '食伤' },
  wealth:    { roleZh: '我克 Wealth',     tenGodZh: '财星' },
  power:     { roleZh: '克我 Power',      tenGodZh: '官杀' },
};

// Thresholds for "high" and "low" relative to balanced 20%
const HIGH_THRESHOLD = 24; // notably above balanced share
const LOW_THRESHOLD = 14;  // notably below balanced share

// ---------------------------------------------------------------------------
// Core: Determine DM relationship for each element
// ---------------------------------------------------------------------------

function getDmRelationship(dmElement: Element, targetElement: Element): TenGodGroup {
  if (targetElement === dmElement) return 'companion';
  if (PRODUCED_BY[dmElement] === targetElement) return 'resource';
  if (PRODUCES[dmElement] === targetElement) return 'output';
  if (CONTROLS[dmElement] === targetElement) return 'wealth';
  if (CONTROLLED_BY[dmElement] === targetElement) return 'power';
  // Should never reach here with 5 elements
  return 'companion';
}

// ---------------------------------------------------------------------------
// Narrative generation
// ---------------------------------------------------------------------------

type StrengthBucket = 'weak' | 'balanced' | 'strong';

function strengthBucket(s: DmStrength): StrengthBucket {
  if (s === 'weak' || s === 'very_weak') return 'weak';
  if (s === 'strong' || s === 'dominant') return 'strong';
  return 'balanced';
}

type LevelBucket = 'high' | 'moderate' | 'low';

function levelBucket(pct: number): LevelBucket {
  if (pct >= HIGH_THRESHOLD) return 'high';
  if (pct <= LOW_THRESHOLD) return 'low';
  return 'moderate';
}

// Narrative lookup: [strengthBucket][role][levelBucket]
const NARRATIVES: Record<StrengthBucket, Record<TenGodGroup, Record<LevelBucket, string>>> = {
  weak: {
    companion: {
      high: 'Carried by allies — not alone in struggle, peers share the burden',
      moderate: 'Some peer support available, but not enough to fully rely on',
      low: 'Isolated — few peers, must stand alone through challenges',
    },
    resource: {
      high: 'Well-nurtured despite weakness — protected by elders, knowledge, or mentors',
      moderate: 'Some nurturing available — partial shelter from pressures',
      low: 'Self-taught, limited mentorship — independence forced early',
    },
    output: {
      high: 'Pressured to produce beyond capacity — obligations drain an already tired DM',
      moderate: 'Moderate output demands — manageable but tiring for weak DM',
      low: 'Conserves energy — limited output but sustainable pace',
    },
    wealth: {
      high: 'Wealth beyond grasp — ambitious but overextended, chasing what can\'t be held',
      moderate: 'Some wealth opportunity — but weak DM struggles to hold it',
      low: 'Few material demands — simpler path, less pressure to acquire',
    },
    power: {
      high: 'Crushed by authority — heavy external pressure on an already weak DM',
      moderate: 'Noticeable authority pressure — discipline from above demands resilience',
      low: 'Few constraints — freedom to find own way, though with less structure',
    },
  },
  balanced: {
    companion: {
      high: 'Strong peer presence — allies abundant but competition also grows',
      moderate: 'Healthy peer balance — support without excessive rivalry',
      low: 'Independent path — few competitors but also fewer allies',
    },
    resource: {
      high: 'Abundant nurture — well-supported by knowledge and mentors, may become comfortable',
      moderate: 'Adequate mentorship — learns and grows at natural pace',
      low: 'Light on support — self-reliant learner, builds own foundation',
    },
    output: {
      high: 'Active producer — strong creative drive, busy with expression and work',
      moderate: 'Steady output — productive without overextension',
      low: 'Restrained output — potential held in reserve',
    },
    wealth: {
      high: 'Wealth-oriented — strong material drive, capable of acquisition',
      moderate: 'Balanced material engagement — neither chasing nor avoiding wealth',
      low: 'Material simplicity — wealth is not the primary life theme',
    },
    power: {
      high: 'Authority-heavy — significant external demands, must rise to meet them',
      moderate: 'Healthy discipline — structure provides direction without crushing',
      low: 'Light governance — free to chart own course',
    },
  },
  strong: {
    companion: {
      high: 'Too many competitors for same resources — rivalry over territory',
      moderate: 'Peers present but strong DM dominates the group',
      low: 'Stands out — few rivals, clear field, unchallenged position',
    },
    resource: {
      high: 'Over-protected — may lack drive, comfortable but risks stagnation',
      moderate: 'Supported strength — nurture reinforces an already capable DM',
      low: 'Self-made strength — didn\'t need much nurturing to become powerful',
    },
    output: {
      high: 'Natural creator — loves expression, productive and energized by output',
      moderate: 'Capable output — strong DM channels energy into results',
      low: 'Strong but unexpressive — power held inward, potential untapped',
    },
    wealth: {
      high: 'Capable wealth-holder — ambitious and rewarded, strong enough to command resources',
      moderate: 'Comfortable material position — wealth comes without overreach',
      low: 'Strong but limited stage — talent without opportunity',
    },
    power: {
      high: 'Disciplined strength — authority channeled into achievement and structure',
      moderate: 'Governance accepted — strong DM respects structure',
      low: 'Unchecked strength — may lack direction or accountability',
    },
  },
};

function getRowNarrative(dmStrength: DmStrength, role: TenGodGroup, pct: number): string {
  const sb = strengthBucket(dmStrength);
  const lb = levelBucket(pct);
  return NARRATIVES[sb][role][lb];
}

// ---------------------------------------------------------------------------
// Cross-row pattern detection
// ---------------------------------------------------------------------------

interface PatternDef {
  id: string;
  nameZh: string;
  test: (levels: Record<TenGodGroup, LevelBucket>, sb: StrengthBucket) => boolean;
  narrative: string;
}

const CROSS_PATTERNS: PatternDef[] = [
  {
    id: 'sha_yin_xiang_sheng',
    nameZh: '杀印相生',
    test: (l) => l.power === 'high' && l.resource === 'high',
    narrative: 'Pressure channeled through mentorship — growth through adversity',
  },
  {
    id: 'sha_wu_yin_hua',
    nameZh: '杀无印化',
    test: (l) => l.power === 'high' && l.resource === 'low',
    narrative: 'Raw oppression without shelter — harsh, unprotected life challenges',
  },
  {
    id: 'shi_shang_sheng_cai',
    nameZh: '食伤生财',
    test: (l) => l.output === 'high' && l.wealth === 'high',
    narrative: 'Output converts to reward — hard work pays off materially',
  },
  {
    id: 'shi_shang_wu_cai',
    nameZh: '食伤无财',
    test: (l) => l.output === 'high' && l.wealth === 'low',
    narrative: 'Produces much but gains little — creative yet unrewarded',
  },
  {
    id: 'bi_jie_duo_cai',
    nameZh: '比劫夺财',
    test: (l) => l.companion === 'high' && l.wealth === 'low',
    narrative: 'Many competitors, little to share — rivalry over scraps',
  },
  {
    id: 'yin_zhong_shi_qing',
    nameZh: '印重食轻',
    test: (l) => l.resource === 'high' && l.output === 'low',
    narrative: 'Over-thinking, under-doing — sheltered but unproductive',
  },
  {
    id: 'cai_duo_shen_ruo',
    nameZh: '财多身弱',
    test: (l, sb) => l.wealth === 'high' && sb === 'weak',
    narrative: 'Wealth crushes weak master — bites off more than can chew',
  },
  {
    id: 'guan_sha_hun_za',
    nameZh: '官杀混杂',
    test: (l) => l.power === 'high' && l.companion === 'high',
    narrative: 'Authority vs rebellion — inner conflict, power struggles',
  },
];

// ---------------------------------------------------------------------------
// Synthesis generation
// ---------------------------------------------------------------------------

function generateSynthesis(
  dmStrength: DmStrength,
  supportPct: number,
  drainPct: number,
  rows: DmLensRow[],
  crossPatterns: CrossPattern[],
): string {
  const sb = strengthBucket(dmStrength);

  // Find the dominant drain category
  const drainRows = rows.filter(r => r.role === 'output' || r.role === 'wealth' || r.role === 'power');
  const topDrain = drainRows.length > 0
    ? drainRows.reduce((a, b) => a.percent > b.percent ? a : b)
    : null;

  const supportRows = rows.filter(r => r.role === 'companion' || r.role === 'resource');
  const topSupport = supportRows.length > 0
    ? supportRows.reduce((a, b) => a.percent > b.percent ? a : b)
    : null;

  const ratio = drainPct > 0 ? supportPct / drainPct : 99;

  const parts: string[] = [];

  // Main DM condition
  if (sb === 'weak') {
    if (ratio < 0.5) {
      parts.push('Weak DM under heavy pressure');
    } else {
      parts.push('Weak DM with some support');
    }
  } else if (sb === 'strong') {
    if (ratio > 1.5) {
      parts.push('Strong DM with abundant backing');
    } else {
      parts.push('Strong DM channeling energy outward');
    }
  } else {
    parts.push('Balanced DM with moderate pressure and support');
  }

  // Dominant theme
  if (topDrain && topDrain.percent >= HIGH_THRESHOLD) {
    const label = ROLE_META[topDrain.role].tenGodZh;
    parts.push(`dominant ${label} theme shapes life direction`);
  }

  if (topSupport && topSupport.percent >= HIGH_THRESHOLD) {
    const label = ROLE_META[topSupport.role].tenGodZh;
    parts.push(`${label} provides key backing`);
  }

  // Cross-pattern summary (take first, most significant)
  if (crossPatterns.length > 0) {
    parts.push(crossPatterns[0].narrative.toLowerCase());
  }

  return parts.join(' — ');
}

// ---------------------------------------------------------------------------
// Main entry point
// ---------------------------------------------------------------------------

export function calculateDmLens(wuxingResult: WuxingResult): DmLensResult {
  const { dayMaster, elements, nodes } = wuxingResult;
  const dmElement = dayMaster.element;
  const dmStrength = dayMaster.strength;

  // Get DM node points (DP.HS) to exclude from totals
  const dmNode = nodes['DP.HS'];
  const dmNodePoints = dmNode ? dmNode.final : 0;

  // Grand total excluding DM's own node
  const grandTotal = Object.values(elements).reduce((s, e) => s + e.total, 0);
  const adjustedTotal = grandTotal - dmNodePoints;

  // Build rows
  const ELEMENTS: Element[] = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'];
  const roleOrder: TenGodGroup[] = ['companion', 'resource', 'output', 'wealth', 'power'];

  const rowMap = new Map<TenGodGroup, { element: Element; points: number }>();

  for (const elem of ELEMENTS) {
    const role = getDmRelationship(dmElement, elem);
    let pts = elements[elem].total;

    // Subtract DM's own node from companion
    if (role === 'companion') {
      pts = Math.max(0, pts - dmNodePoints);
    }

    rowMap.set(role, { element: elem, points: pts });
  }

  const rows: DmLensRow[] = roleOrder.map(role => {
    const data = rowMap.get(role)!;
    const pct = adjustedTotal > 0 ? (data.points / adjustedTotal) * 100 : 0;
    const meta = ROLE_META[role];

    return {
      role,
      roleZh: meta.roleZh,
      tenGodZh: meta.tenGodZh,
      element: data.element,
      points: Math.round(data.points * 100) / 100,
      percent: Math.round(pct * 10) / 10,
      narrative: getRowNarrative(dmStrength, role, pct),
    };
  });

  // Support vs Drain
  const supportTotal = rows
    .filter(r => r.role === 'companion' || r.role === 'resource')
    .reduce((s, r) => s + r.points, 0);
  const drainTotal = rows
    .filter(r => r.role === 'output' || r.role === 'wealth' || r.role === 'power')
    .reduce((s, r) => s + r.points, 0);

  const supportPercent = adjustedTotal > 0 ? (supportTotal / adjustedTotal) * 100 : 0;
  const drainPercent = adjustedTotal > 0 ? (drainTotal / adjustedTotal) * 100 : 0;

  const ratioVal = drainPercent > 0 ? supportPercent / drainPercent : 99;
  const ratio = ratioVal >= 10 ? `${Math.round(ratioVal)}:1` : `${ratioVal.toFixed(1)}:1`;

  // Cross-row pattern detection
  const levels: Record<TenGodGroup, LevelBucket> = {} as any;
  for (const row of rows) {
    levels[row.role] = levelBucket(row.percent);
  }
  const sb = strengthBucket(dmStrength);

  const crossPatterns: CrossPattern[] = CROSS_PATTERNS
    .filter(p => p.test(levels, sb))
    .map(p => ({ id: p.id, nameZh: p.nameZh, narrative: p.narrative }));

  // Seasonal state — derive from season element + DM element
  const SEASONAL_STATE_ZH: Record<SeasonalState, string> = {
    Prosperous: '旺', Prime: '相', Rest: '休', Imprisoned: '囚', Dead: '死',
  };
  const dmSeasonalState: SeasonalState = SEASONAL_MATRIX[wuxingResult.season][dmElement];
  const seasonalState = SEASONAL_STATE_ZH[dmSeasonalState];

  const synthesis = generateSynthesis(dmStrength, supportPercent, drainPercent, rows, crossPatterns);

  return {
    dmStem: dayMaster.stem,
    dmElement,
    dmPercent: Math.round(dayMaster.percent * 10) / 10,
    dmStrength,
    dmStrengthZh: STRENGTH_ZH[dmStrength],
    seasonalState,
    rows,
    supportTotal: Math.round(supportTotal * 100) / 100,
    supportPercent: Math.round(supportPercent * 10) / 10,
    drainTotal: Math.round(drainTotal * 100) / 100,
    drainPercent: Math.round(drainPercent * 10) / 10,
    ratio,
    crossPatterns,
    synthesis,
  };
}
