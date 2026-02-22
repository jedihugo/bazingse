import 'server-only';

// =============================================================================
// LIFE ASPECTS BASE
// =============================================================================
// Foundation types and utilities for life aspect analysis modules.
// Ported from api/library/life_aspects/base.py
// =============================================================================

import type { Element, StemName } from '../core';
import { STEMS } from '../core';

// ---------------------------------------------------------------------------
// Node Relationship Context
// ---------------------------------------------------------------------------

export interface NodeRelationship {
  pillar: string;
  represents: string;
  life_domain: string;
}

export const NODE_RELATIONSHIPS: Record<string, NodeRelationship> = {
  hs_y: { pillar: "year", represents: "grandfather/father", life_domain: "ancestry" },
  eb_y: { pillar: "year", represents: "grandmother/mother", life_domain: "ancestry" },
  hs_m: { pillar: "month", represents: "father/boss", life_domain: "career" },
  eb_m: { pillar: "month", represents: "mother/society", life_domain: "career" },
  hs_d: { pillar: "day", represents: "self", life_domain: "self" },
  eb_d: { pillar: "day", represents: "spouse", life_domain: "marriage" },
  hs_h: { pillar: "hour", represents: "first child", life_domain: "children" },
  eb_h: { pillar: "hour", represents: "second child", life_domain: "children" },
  hs_10yl: { pillar: "10yl", represents: "luck_stem", life_domain: "luck" },
  eb_10yl: { pillar: "10yl", represents: "luck_branch", life_domain: "luck" },
  hs_yl: { pillar: "annual", represents: "year_stem", life_domain: "annual" },
  eb_yl: { pillar: "annual", represents: "year_branch", life_domain: "annual" },
  hs_ml: { pillar: "monthly", represents: "month_stem", life_domain: "monthly" },
  eb_ml: { pillar: "monthly", represents: "month_branch", life_domain: "monthly" },
  hs_dl: { pillar: "daily", represents: "day_stem", life_domain: "daily" },
  eb_dl: { pillar: "daily", represents: "day_branch", life_domain: "daily" },
  hs_hl: { pillar: "hourly", represents: "hour_stem", life_domain: "hourly" },
  eb_hl: { pillar: "hourly", represents: "hour_branch", life_domain: "hourly" },
};

// ---------------------------------------------------------------------------
// Pillar Life Periods
// ---------------------------------------------------------------------------

export const PILLAR_LIFE_PERIODS: Record<string, { age_range: string; en: string; zh: string }> = {
  year: { age_range: "0-15", en: "Early childhood, ancestry", zh: "幼年，祖先" },
  month: { age_range: "16-30", en: "Youth, career formation", zh: "青年，事業形成" },
  day: { age_range: "31-45", en: "Adulthood, marriage", zh: "壯年，婚姻" },
  hour: { age_range: "46+", en: "Later life, children, legacy", zh: "晚年，子女，遺產" },
};

// ---------------------------------------------------------------------------
// Ten God Aspect Mapping
// ---------------------------------------------------------------------------

export const TEN_GOD_ASPECT_MAPPING: Record<string, {
  en: string;
  zh: string;
  aspect: string;
  domains: string[];
}> = {
  F: { en: "Friend/Companion", zh: "比肩", aspect: "self", domains: ["self", "siblings"] },
  RW: { en: "Rob Wealth", zh: "劫財", aspect: "self", domains: ["competition", "loss"] },
  EG: { en: "Eating God", zh: "食神", aspect: "output", domains: ["creativity", "food", "children"] },
  HO: { en: "Hurting Officer", zh: "傷官", aspect: "output", domains: ["rebellion", "talent", "injury"] },
  DW: { en: "Direct Wealth", zh: "正財", aspect: "wealth", domains: ["salary", "property", "wife"] },
  IW: { en: "Indirect Wealth", zh: "偏財", aspect: "wealth", domains: ["windfall", "speculation", "father"] },
  DO: { en: "Direct Officer", zh: "正官", aspect: "authority", domains: ["career", "law", "husband"] },
  "7K": { en: "Seven Killings", zh: "七殺", aspect: "authority", domains: ["power", "danger", "reform"] },
  DR: { en: "Direct Resource", zh: "正印", aspect: "resource", domains: ["education", "mother", "protection"] },
  IR: { en: "Indirect Resource", zh: "偏印", aspect: "resource", domains: ["unconventional_learning", "loneliness"] },
};

// ---------------------------------------------------------------------------
// Element Cycles
// ---------------------------------------------------------------------------

export const ELEMENT_CONTROLS: Record<Element, Element> = {
  Wood: "Earth",
  Fire: "Metal",
  Earth: "Water",
  Metal: "Wood",
  Water: "Fire",
};

export const ELEMENT_GENERATES: Record<Element, Element> = {
  Wood: "Fire",
  Fire: "Earth",
  Earth: "Metal",
  Metal: "Water",
  Water: "Wood",
};

// ---------------------------------------------------------------------------
// Stem to Element
// ---------------------------------------------------------------------------

export const STEM_TO_ELEMENT: Record<StemName, Element> = {
  Jia: "Wood", Yi: "Wood",
  Bing: "Fire", Ding: "Fire",
  Wu: "Earth", Ji: "Earth",
  Geng: "Metal", Xin: "Metal",
  Ren: "Water", Gui: "Water",
};

// ---------------------------------------------------------------------------
// Translation Constants
// ---------------------------------------------------------------------------

export const ELEMENT_NAMES_L: Record<Element, { en: string; zh: string; id: string }> = {
  Wood: { en: "Wood", zh: "木", id: "Kayu" },
  Fire: { en: "Fire", zh: "火", id: "Api" },
  Earth: { en: "Earth", zh: "土", id: "Tanah" },
  Metal: { en: "Metal", zh: "金", id: "Logam" },
  Water: { en: "Water", zh: "水", id: "Air" },
};

export const SEASONAL_STATES_L: Record<string, { en: string; zh: string; id: string }> = {
  Prosperous: { en: "Prosperous", zh: "旺", id: "Makmur" },
  Strengthening: { en: "Strengthening", zh: "相", id: "Menguat" },
  Resting: { en: "Resting", zh: "休", id: "Istirahat" },
  Trapped: { en: "Trapped", zh: "囚", id: "Terjebak" },
  Dead: { en: "Dead", zh: "死", id: "Mati" },
};

export const SEVERITY_LABELS: Record<string, { en: string; zh: string; id: string }> = {
  low: { en: "Low", zh: "低", id: "Rendah" },
  moderate: { en: "Moderate", zh: "中", id: "Sedang" },
  high: { en: "High", zh: "高", id: "Tinggi" },
  critical: { en: "Critical", zh: "嚴重", id: "Kritis" },
};

export const OUTLOOK_LABELS: Record<string, { en: string; zh: string; id: string }> = {
  positive: { en: "Positive", zh: "正面", id: "Positif" },
  negative: { en: "Negative", zh: "負面", id: "Negatif" },
  neutral: { en: "Neutral", zh: "中性", id: "Netral" },
  mixed: { en: "Mixed", zh: "混合", id: "Campuran" },
};

export const ORGAN_SYSTEMS: Record<Element, { zang: string; fu: string; zh_zang: string; zh_fu: string }> = {
  Wood: { zang: "Liver", fu: "Gallbladder", zh_zang: "肝", zh_fu: "膽" },
  Fire: { zang: "Heart", fu: "Small Intestine", zh_zang: "心", zh_fu: "小腸" },
  Earth: { zang: "Spleen", fu: "Stomach", zh_zang: "脾", zh_fu: "胃" },
  Metal: { zang: "Lungs", fu: "Large Intestine", zh_zang: "肺", zh_fu: "大腸" },
  Water: { zang: "Kidneys", fu: "Bladder", zh_zang: "腎", zh_fu: "膀胱" },
};

export const BODY_PARTS: Record<Element, string[]> = {
  Wood: ["eyes", "tendons", "nails", "sinews"],
  Fire: ["tongue", "blood vessels", "complexion", "sweat"],
  Earth: ["muscles", "mouth", "lips", "flesh"],
  Metal: ["skin", "nose", "body hair", "pores"],
  Water: ["bones", "ears", "head hair", "marrow", "brain"],
};

// ---------------------------------------------------------------------------
// Utility Functions
// ---------------------------------------------------------------------------

export function stemsToElementTotals(stems: StemName[]): Record<Element, number> {
  const totals: Record<string, number> = {
    Wood: 0, Fire: 0, Earth: 0, Metal: 0, Water: 0,
  };

  for (const stem of stems) {
    const element = STEM_TO_ELEMENT[stem];
    if (element) {
      totals[element]++;
    }
  }

  return totals as Record<Element, number>;
}

export function getNodeRelationshipContext(nodeId: string): NodeRelationship | null {
  return NODE_RELATIONSHIPS[nodeId] ?? null;
}

export function detectControlImbalances(
  elementScores: Record<string, number>,
  daymasterElement: Element
): Array<{ controller: Element; controlled: Element; severity: string }> {
  const results: Array<{ controller: Element; controlled: Element; severity: string }> = [];
  const total = Object.values(elementScores).reduce((sum, v) => sum + v, 0);
  if (total === 0) return results;

  for (const [controller, controlled] of Object.entries(ELEMENT_CONTROLS)) {
    const ctrlPct = ((elementScores[controller] ?? 0) / total) * 100;
    const ctldPct = ((elementScores[controlled] ?? 0) / total) * 100;

    if (ctrlPct > 25 && ctldPct < 15) {
      const severity = ctrlPct > 35 ? 'high' : 'moderate';
      results.push({
        controller: controller as Element,
        controlled: controlled as Element,
        severity,
      });
    }
  }

  return results;
}

export function calculateAspectSeverity(
  score: number,
  maxScore: number
): string {
  const ratio = score / maxScore;
  if (ratio >= 0.7) return 'high';
  if (ratio >= 0.4) return 'moderate';
  return 'low';
}
