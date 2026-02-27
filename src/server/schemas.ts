import { z } from 'zod';

// ---------------------------------------------------------------------------
// Profile schemas
// ---------------------------------------------------------------------------

export const profileSchema = z.object({
  id: z.string(),
  name: z.string(),
  birth_date: z.string(),
  birth_time: z.string().nullable(),
  gender: z.enum(['male', 'female']),
  place_of_birth: z.string().nullable(),
  phone: z.string().nullable(),
  life_events: z.array(z.lazy(() => lifeEventSchema)).nullable(),
  created_at: z.string().nullable(),
  updated_at: z.string().nullable(),
});

export const profileCreateSchema = z.object({
  name: z.string().min(1),
  birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  birth_time: z.string().regex(/^\d{2}:\d{2}$/).optional(),
  gender: z.enum(['male', 'female']),
  place_of_birth: z.string().optional(),
  phone: z.string().optional(),
});

export const profileUpdateSchema = z.object({
  name: z.string().min(1).optional(),
  birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  birth_time: z.string().regex(/^\d{2}:\d{2}$/).optional(),
  gender: z.enum(['male', 'female']).optional(),
  place_of_birth: z.string().optional(),
  phone: z.string().optional(),
});

// ---------------------------------------------------------------------------
// Life Event schemas
// ---------------------------------------------------------------------------

export const lifeEventSchema = z.object({
  id: z.string(),
  year: z.number(),
  month: z.number().nullable().optional(),
  day: z.number().nullable().optional(),
  location: z.string().nullable().optional(),
  notes: z.string().nullable().optional(),
  is_abroad: z.boolean().optional(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const lifeEventCreateSchema = z.object({
  year: z.number().int().min(1900).max(2100),
  month: z.number().int().min(1).max(12).nullable().optional(),
  day: z.number().int().min(1).max(31).nullable().optional(),
  location: z.string().nullable().optional(),
  notes: z.string().nullable().optional(),
  is_abroad: z.boolean().optional(),
});

export const lifeEventUpdateSchema = z.object({
  year: z.number().int().min(1900).max(2100).optional(),
  month: z.number().int().min(1).max(12).nullable().optional(),
  day: z.number().int().min(1).max(31).nullable().optional(),
  location: z.string().nullable().optional(),
  notes: z.string().nullable().optional(),
  is_abroad: z.boolean().optional(),
});

// ---------------------------------------------------------------------------
// BaZi Analysis schemas
// ---------------------------------------------------------------------------

export const analyzeBaziInputSchema = z.object({
  birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  birth_time: z.string().nullable().optional(),
  gender: z.enum(['male', 'female']),
  analysis_year: z.number().int().nullable().optional(),
  include_annual_luck: z.boolean().optional().default(true),
  analysis_month: z.number().int().min(1).max(12).nullable().optional(),
  analysis_day: z.number().int().min(1).max(31).nullable().optional(),
  analysis_time: z.string().nullable().optional(),
  school: z.enum(['classic', 'physics']).optional().default('classic'),
  // Talisman parameters
  talisman_year_hs: z.string().nullable().optional(),
  talisman_year_eb: z.string().nullable().optional(),
  talisman_month_hs: z.string().nullable().optional(),
  talisman_month_eb: z.string().nullable().optional(),
  talisman_day_hs: z.string().nullable().optional(),
  talisman_day_eb: z.string().nullable().optional(),
  talisman_hour_hs: z.string().nullable().optional(),
  talisman_hour_eb: z.string().nullable().optional(),
  // Location
  location: z.enum(['overseas', 'birthplace']).nullable().optional(),
});

// The BaZi analysis response is complex and dynamic — we use passthrough
// to keep type safety on the input side while allowing the rich response through.
// The actual response shape is determined by the comprehensive engine.
export const analyzeBaziOutputSchema = z.record(z.string(), z.unknown());

// ---------------------------------------------------------------------------
// Dong Gong Calendar schemas
// ---------------------------------------------------------------------------

export const dongGongCalendarInputSchema = z.object({
  year: z.number().int(),
  month: z.number().int().min(1).max(12),
});

export const dongGongOfficerSchema = z.object({
  id: z.string(),
  chinese: z.string(),
  english: z.string(),
});

export const dongGongRatingSchema = z.object({
  id: z.string(),
  value: z.number(),
  symbol: z.string(),
  chinese: z.string(),
});

export const dongGongConsultSchema = z.object({
  promoted: z.boolean(),
  original_rating: dongGongRatingSchema.nullable(),
  reason: z.string(),
});

export const dongGongForbiddenSchema = z.object({
  type: z.string(),
  chinese: z.string(),
  english: z.string(),
  solar_term_id: z.string(),
  solar_term_chinese: z.string(),
  solar_term_english: z.string(),
  forbidden_start_hour: z.number(),
  forbidden_end_hour: z.number(),
});

export const moonPhaseSchema = z.object({
  emoji: z.string(),
  english: z.string(),
  chinese: z.string(),
  lunar_day: z.number(),
});

export const dongGongDaySchema = z.object({
  day: z.number(),
  weekday: z.number(),
  day_stem: z.string(),
  day_branch: z.string(),
  day_stem_chinese: z.string(),
  day_branch_chinese: z.string(),
  pillar: z.string(),
  year_stem: z.string(),
  year_branch: z.string(),
  year_stem_chinese: z.string(),
  year_branch_chinese: z.string(),
  chinese_month: z.number().nullable(),
  chinese_month_name: z.string(),
  officer: dongGongOfficerSchema.nullable(),
  rating: dongGongRatingSchema.nullable(),
  good_for: z.array(z.string()),
  bad_for: z.array(z.string()),
  description_chinese: z.string(),
  description_english: z.string(),
  consult: dongGongConsultSchema.nullable().optional(),
  forbidden: dongGongForbiddenSchema.nullable().optional(),
  moon_phase: moonPhaseSchema,
});

export const chineseMonthSpannedSchema = z.object({
  month: z.number(),
  chinese: z.string(),
  branch: z.string(),
  stem: z.string(),
  stem_chinese: z.string(),
  branch_id: z.string(),
  branch_chinese: z.string(),
});

export const chineseYearSpannedSchema = z.object({
  stem: z.string(),
  stem_chinese: z.string(),
  branch: z.string(),
  branch_chinese: z.string(),
});

export const dongGongCalendarOutputSchema = z.object({
  year: z.number(),
  month: z.number(),
  first_day_weekday: z.number(),
  days_in_month: z.number(),
  days: z.array(dongGongDaySchema),
  chinese_months_spanned: z.array(chineseMonthSpannedSchema),
  chinese_years_spanned: z.array(chineseYearSpannedSchema),
});
