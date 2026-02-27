// Shared type definitions for the BaZi API
// These types are used by both the tRPC client (api.ts) and components.

// ---------------------------------------------------------------------------
// Life Event types
// ---------------------------------------------------------------------------

export interface LifeEvent {
  id: string;
  year: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
  is_abroad?: boolean;
  created_at: string;
  updated_at: string;
}

export interface LifeEventCreate {
  year: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
  is_abroad?: boolean;
}

export interface LifeEventUpdate {
  year?: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
  is_abroad?: boolean;
}

// ---------------------------------------------------------------------------
// Profile types
// ---------------------------------------------------------------------------

export interface Profile {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string | null;
  gender: 'male' | 'female';
  place_of_birth: string | null;
  phone: string | null;
  life_events: LifeEvent[] | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface ProfileCreate {
  name: string;
  birth_date: string;
  birth_time?: string;
  gender: 'male' | 'female';
  place_of_birth?: string;
  phone?: string;
}

export interface ProfileUpdate {
  name?: string;
  birth_date?: string;
  birth_time?: string;
  gender?: 'male' | 'female';
  place_of_birth?: string;
  phone?: string;
}

// ---------------------------------------------------------------------------
// Dong Gong Calendar types
// ---------------------------------------------------------------------------

export interface DongGongOfficer {
  id: string;
  chinese: string;
  english: string;
}

export interface DongGongRating {
  id: string;
  value: number;
  symbol: string;
  chinese: string;
}

export interface DongGongConsult {
  promoted: boolean;
  original_rating: DongGongRating | null;
  reason: string;
}

export interface DongGongForbidden {
  type: string;
  chinese: string;
  english: string;
  solar_term_id: string;
  solar_term_chinese: string;
  solar_term_english: string;
  forbidden_start_hour: number;
  forbidden_end_hour: number;
}

export interface DongGongDay {
  day: number;
  weekday: number;
  day_stem: string;
  day_branch: string;
  day_stem_chinese: string;
  day_branch_chinese: string;
  pillar: string;
  year_stem: string;
  year_branch: string;
  year_stem_chinese: string;
  year_branch_chinese: string;
  chinese_month: number | null;
  chinese_month_name: string;
  officer: DongGongOfficer | null;
  rating: DongGongRating | null;
  good_for: string[];
  bad_for: string[];
  description_chinese: string;
  description_english: string;
  consult?: DongGongConsult | null;
  forbidden?: DongGongForbidden | null;
  moon_phase: { emoji: string; english: string; chinese: string; lunar_day: number };
}

export interface DongGongCalendarResponse {
  year: number;
  month: number;
  first_day_weekday: number;
  days_in_month: number;
  days: DongGongDay[];
  chinese_months_spanned: {
    month: number;
    chinese: string;
    branch: string;
    stem: string;
    stem_chinese: string;
    branch_id: string;
    branch_chinese: string;
  }[];
  chinese_years_spanned: {
    stem: string;
    stem_chinese: string;
    branch: string;
    branch_chinese: string;
  }[];
}

// ---------------------------------------------------------------------------
// BaZi Analysis types
// ---------------------------------------------------------------------------

export interface AnalyzeBaziParams {
  birthDate: string;
  birthTime: string;
  gender: 'male' | 'female';
  unknownHour?: boolean;
  // Time travel / analysis period
  analysisYear?: number | null;
  includeAnnualLuck?: boolean;
  analysisMonth?: number | null;
  includeMonthlyLuck?: boolean;
  analysisDay?: number | null;
  includeDailyLuck?: boolean;
  analysisTime?: string;
  includeHourlyLuck?: boolean;
  // Talisman parameters
  showTalismans?: boolean;
  talismanYearHS?: string | null;
  talismanYearEB?: string | null;
  talismanMonthHS?: string | null;
  talismanMonthEB?: string | null;
  talismanDayHS?: string | null;
  talismanDayEB?: string | null;
  talismanHourHS?: string | null;
  talismanHourEB?: string | null;
  // Location
  showLocation?: boolean;
  locationType?: 'overseas' | 'birthplace' | null;
  // School
  school?: 'classic' | 'physics';
}

// ---------------------------------------------------------------------------
// LocalStorage types
// ---------------------------------------------------------------------------

export interface StoredFormData {
  birthDate: string;
  birthTime: string;
  gender: 'male' | 'female';
  unknownHour: boolean;
  yearInput: number;
  monthInput: number;
  dayInput: number;
  analysisYear: number | null;
  analysisMonth: number | null;
  analysisDay: number | null;
  analysisTime: string;
  showAnalysisPeriod: boolean;
  includeAnnualLuck: boolean;
  includeMonthlyLuck: boolean;
  includeDailyLuck: boolean;
  includeHourlyLuck: boolean;
  showTalismans: boolean;
  talismanYearHS: string | null;
  talismanYearEB: string | null;
  talismanMonthHS: string | null;
  talismanMonthEB: string | null;
  talismanDayHS: string | null;
  talismanDayEB: string | null;
  talismanHourHS: string | null;
  talismanHourEB: string | null;
  showLocation: boolean;
  locationType: 'overseas' | 'birthplace' | null;
}
