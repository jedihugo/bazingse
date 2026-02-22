import 'server-only';

// =============================================================================
// NARRATIVE LOCALIZATION
// =============================================================================
// Bilingual text generation for narrative content.
// Ported from api/library/narrative/localization.py
// =============================================================================

import type { Element, StemName, BranchName } from '../core';

// ---------------------------------------------------------------------------
// Supported Locales
// ---------------------------------------------------------------------------

export const SUPPORTED_LOCALES = ['en', 'zh'] as const;
export type SupportedLocale = typeof SUPPORTED_LOCALES[number];

// ---------------------------------------------------------------------------
// Element Names
// ---------------------------------------------------------------------------

export const ELEMENT_NAMES: Record<Element, Record<SupportedLocale, string>> = {
  Wood: { en: "Wood", zh: "木" },
  Fire: { en: "Fire", zh: "火" },
  Earth: { en: "Earth", zh: "土" },
  Metal: { en: "Metal", zh: "金" },
  Water: { en: "Water", zh: "水" },
};

// ---------------------------------------------------------------------------
// Stem Names
// ---------------------------------------------------------------------------

export const STEM_NAMES: Record<StemName, Record<SupportedLocale, string>> = {
  Jia: { en: "Jia", zh: "甲" },
  Yi: { en: "Yi", zh: "乙" },
  Bing: { en: "Bing", zh: "丙" },
  Ding: { en: "Ding", zh: "丁" },
  Wu: { en: "Wu", zh: "戊" },
  Ji: { en: "Ji", zh: "己" },
  Geng: { en: "Geng", zh: "庚" },
  Xin: { en: "Xin", zh: "辛" },
  Ren: { en: "Ren", zh: "壬" },
  Gui: { en: "Gui", zh: "癸" },
};

// ---------------------------------------------------------------------------
// Branch Names
// ---------------------------------------------------------------------------

export const BRANCH_NAMES: Record<BranchName, Record<SupportedLocale, string>> = {
  Zi: { en: "Zi", zh: "子" },
  Chou: { en: "Chou", zh: "丑" },
  Yin: { en: "Yin", zh: "寅" },
  Mao: { en: "Mao", zh: "卯" },
  Chen: { en: "Chen", zh: "辰" },
  Si: { en: "Si", zh: "巳" },
  Wu: { en: "Wu", zh: "午" },
  Wei: { en: "Wei", zh: "未" },
  Shen: { en: "Shen", zh: "申" },
  You: { en: "You", zh: "酉" },
  Xu: { en: "Xu", zh: "戌" },
  Hai: { en: "Hai", zh: "亥" },
};

// ---------------------------------------------------------------------------
// Seasonal States
// ---------------------------------------------------------------------------

export const SEASONAL_STATES: Record<string, Record<SupportedLocale, string>> = {
  Prosperous: { en: "Prosperous", zh: "旺" },
  Strengthening: { en: "Strengthening", zh: "相" },
  Resting: { en: "Resting", zh: "休" },
  Trapped: { en: "Trapped", zh: "囚" },
  Dead: { en: "Dead", zh: "死" },
};

// ---------------------------------------------------------------------------
// Punishment Types
// ---------------------------------------------------------------------------

export const PUNISHMENT_TYPES: Record<string, Record<SupportedLocale, string>> = {
  shi_xing: { en: "Bullying", zh: "勢刑" },
  wu_li_xing: { en: "Rudeness", zh: "無禮刑" },
  en_xing: { en: "Ungrateful", zh: "恩刑" },
  zi_xing: { en: "Self", zh: "自刑" },
};

// ---------------------------------------------------------------------------
// Localization Functions
// ---------------------------------------------------------------------------

export function getLocalizedTemplate(
  template: { en: string; zh: string },
  locale: SupportedLocale
): string {
  return template[locale] ?? template.en;
}

export function buildNarrativeText(
  templateEn: string,
  templateZh: string,
  variables: Record<string, string>
): { en: string; zh: string } {
  let textEn = templateEn;
  let textZh = templateZh;

  for (const [key, value] of Object.entries(variables)) {
    textEn = textEn.replaceAll(`{${key}}`, value);
    textZh = textZh.replaceAll(`{${key}}`, value);
  }

  return { en: textEn, zh: textZh };
}

function localizeVariables(
  variables: Record<string, string>,
  locale: SupportedLocale
): Record<string, string> {
  const localized: Record<string, string> = { ...variables };

  // Localize element names
  if (variables.element && ELEMENT_NAMES[variables.element as Element]) {
    localized.element_zh = ELEMENT_NAMES[variables.element as Element].zh;
  }

  // Localize stem names
  if (variables.stem && STEM_NAMES[variables.stem as StemName]) {
    localized.stem_zh = STEM_NAMES[variables.stem as StemName].zh;
  }

  return localized;
}

// ---------------------------------------------------------------------------
// Display Formatting
// ---------------------------------------------------------------------------

export function formatPillarReference(pillar: string): { en: string; zh: string } {
  const pillarMap: Record<string, { en: string; zh: string }> = {
    year: { en: "Year", zh: "年" },
    month: { en: "Month", zh: "月" },
    day: { en: "Day", zh: "日" },
    hour: { en: "Hour", zh: "時" },
  };
  return pillarMap[pillar] ?? { en: pillar, zh: pillar };
}

export function formatBranchesDisplay(branches: string[]): { en: string; zh: string } {
  const en = branches.join("-");
  const zh = branches
    .map((b) => BRANCH_NAMES[b as BranchName]?.zh ?? b)
    .join("");
  return { en, zh };
}

export function formatStemsDisplay(stems: string[]): { en: string; zh: string } {
  const en = stems.join("-");
  const zh = stems
    .map((s) => STEM_NAMES[s as StemName]?.zh ?? s)
    .join("");
  return { en, zh };
}
