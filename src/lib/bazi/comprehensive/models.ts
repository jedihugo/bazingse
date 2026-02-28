
// =============================================================================
// DATA MODELS for Comprehensive BaZi Analysis
// =============================================================================
// All structured data types used across the analysis engine.
// Python dataclasses -> TypeScript interfaces.
// =============================================================================

import type { StemName, BranchName, Element, Polarity } from '../core';

// ---------------------------------------------------------------------------
// Pillar
// ---------------------------------------------------------------------------

export interface Pillar {
  position: string;             // "year", "month", "day", "hour"
  stem: StemName;
  branch: BranchName;
  stem_chinese: string;
  branch_chinese: string;
  stem_element: Element | string;
  stem_polarity: Polarity | string;
  branch_element: Element | string;
  branch_polarity: Polarity | string;
  hidden_stems: Array<[StemName, number]>;
}

export function getPalaceName(position: string): string {
  const map: Record<string, string> = {
    year: "Parents/Ancestry",
    month: "Career/Social",
    day: "Self/Spouse",
    hour: "Children/Legacy",
    luck_pillar: "Current Luck Pillar",
    annual: "Annual Luck",
    monthly: "Monthly Luck",
    daily: "Daily Luck",
    hourly: "Hourly Luck",
  };
  return map[position] ?? position;
}

export function getPalaceChinese(position: string): string {
  const map: Record<string, string> = {
    year: "年柱 (父母宫)",
    month: "月柱 (事业宫)",
    day: "日柱 (夫妻宫)",
    hour: "时柱 (子女宫)",
    luck_pillar: "大运",
    annual: "流年",
    monthly: "流月",
    daily: "流日",
    hourly: "流时",
  };
  return map[position] ?? position;
}

// ---------------------------------------------------------------------------
// TenGodEntry
// ---------------------------------------------------------------------------

export interface TenGodEntry {
  stem: StemName;
  abbreviation: string;         // "F", "RW", "EG", etc.
  english: string;
  chinese: string;
  location: string;             // "year_stem", "month_stem", "day_branch_hidden_1", etc.
  position: string;             // "year", "month", "day", "hour"
  visible: boolean;
}

// ---------------------------------------------------------------------------
// ShenShaResult
// ---------------------------------------------------------------------------

export interface ShenShaResult {
  name_english: string;
  name_chinese: string;
  present: boolean;
  location: string | null;
  palace: string | null;
  activated_by: string | null;
  derivation: string;
  nature: string;               // "auspicious", "inauspicious", "mixed", "neutral"
  impact: string;
  life_areas: string[];
  severity: string;             // "mild", "moderate", "severe", "critical"
  is_void: boolean;
}

// ---------------------------------------------------------------------------
// BranchInteraction
// ---------------------------------------------------------------------------

export interface BranchInteraction {
  interaction_type: string;     // "clash", "harmony", "punishment", etc.
  chinese_name: string;
  branches: string[];           // Branch (or stem for stem_combination) IDs involved
  palaces: string[];
  description: string;
  activated_by_lp: boolean;
  severity: string;
}

// ---------------------------------------------------------------------------
// StrengthAssessment
// ---------------------------------------------------------------------------

export interface StrengthAssessment {
  score: number;
  verdict: string;              // "extremely_strong", "strong", "neutral", "weak", "extremely_weak"
  support_count: number;
  drain_count: number;
  seasonal_state: string;
  is_following_chart: boolean;
  following_type: string | null;
  useful_god: string;
  favorable_elements: string[];
  unfavorable_elements: string[];
  element_percentages: Record<string, number>;
  best_element_pairs: Array<Record<string, unknown>>;
}

// ---------------------------------------------------------------------------
// RedFlag
// ---------------------------------------------------------------------------

export interface RedFlag {
  life_area: string;
  indicator_type: string;       // "ten_god", "branch_interaction", "shen_sha"
  indicator_name: string;
  description: string;
  severity: string;
}

// ---------------------------------------------------------------------------
// EventPrediction
// ---------------------------------------------------------------------------

export interface EventPrediction {
  event_type: string;
  year: number;
  age: number;
  score: number;
  factors: string[];
}

// ---------------------------------------------------------------------------
// LuckPillarInfo
// ---------------------------------------------------------------------------

export interface LuckPillarInfo {
  stem: StemName;
  branch: BranchName;
  stem_chinese: string;
  branch_chinese: string;
  start_age: number;
  end_age: number;
  start_year: number;
  end_year: number;
  stem_ten_god: string;
  stem_ten_god_chinese: string;
  is_current: boolean;
  hidden_stems: Array<[StemName, number]>;
}

// ---------------------------------------------------------------------------
// EnvironmentAssessment
// ---------------------------------------------------------------------------

export interface EnvironmentAssessment {
  crosses_water_benefit: boolean;
  crosses_water_reason: string;
  favorable_directions: string[];
  unfavorable_directions: string[];
  ideal_climate: string;
  ideal_geography: string;
  guo_jiang_long_score: number;
  guo_jiang_long_verdict: string;
  guo_jiang_long_factors: string[];
  void_disruption_palaces: string[];
  location_recommendations: string;
}

// ---------------------------------------------------------------------------
// ChartData
// ---------------------------------------------------------------------------

export interface ChartData {
  gender: string;               // "male" or "female"
  birth_year: number;
  age: number;
  pillars: Record<string, Pillar>; // "year", "month", "day", "hour"
  day_master: StemName;
  dm_element: Element;
  dm_polarity: Polarity;
  dm_chinese: string;
  luck_pillar: Pillar | null;
  luck_pillars: LuckPillarInfo[];
  time_period_pillars: Record<string, Pillar>;
  current_year_stem: StemName | string;
  current_year_branch: BranchName | string;
}
