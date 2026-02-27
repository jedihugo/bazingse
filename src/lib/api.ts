// API helpers for BaZi chart generation — powered by tRPC for end-to-end type safety

import { trpc } from './trpc';

// ---------------------------------------------------------------------------
// Re-export types from Zod schemas (inferred from tRPC router)
// ---------------------------------------------------------------------------

export type { Profile, ProfileCreate, ProfileUpdate,
  LifeEvent, LifeEventCreate, LifeEventUpdate,
  DongGongDay, DongGongCalendarResponse, DongGongOfficer,
  DongGongRating, DongGongConsult, DongGongForbidden,
  AnalyzeBaziParams, StoredFormData,
} from './api.types';

// Re-export utility functions (unchanged — they don't call APIs)
export { loadFromStorage, saveToStorage, isValidDate, isValidJiaziPair } from './api.utils';

// ---------------------------------------------------------------------------
// Profile CRUD — now via tRPC
// ---------------------------------------------------------------------------

import type { Profile, ProfileCreate, ProfileUpdate } from './api.types';

export async function getProfiles(limit: number = 10000): Promise<Profile[]> {
  return trpc.profile.list.query({ limit });
}

export async function getProfile(id: string): Promise<Profile> {
  return trpc.profile.get.query({ id });
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  return trpc.profile.create.mutate(data);
}

export async function updateProfile(id: string, data: ProfileUpdate): Promise<Profile> {
  return trpc.profile.update.mutate({ id, data });
}

export async function deleteProfile(id: string): Promise<void> {
  await trpc.profile.delete.mutate({ id });
}

// ---------------------------------------------------------------------------
// Life Event CRUD — now via tRPC
// ---------------------------------------------------------------------------

import type { LifeEvent, LifeEventCreate, LifeEventUpdate } from './api.types';

export async function createLifeEvent(profileId: string, data: LifeEventCreate): Promise<LifeEvent> {
  return trpc.lifeEvent.create.mutate({ profileId, data });
}

export async function updateLifeEvent(
  profileId: string,
  eventId: string,
  data: LifeEventUpdate,
): Promise<LifeEvent> {
  return trpc.lifeEvent.update.mutate({ profileId, eventId, data });
}

export async function deleteLifeEvent(profileId: string, eventId: string): Promise<void> {
  await trpc.lifeEvent.delete.mutate({ profileId, eventId });
}

// ---------------------------------------------------------------------------
// Dong Gong Calendar — now via tRPC
// ---------------------------------------------------------------------------

import type { DongGongCalendarResponse } from './api.types';

export async function getDongGongCalendar(year: number, month: number): Promise<DongGongCalendarResponse> {
  return trpc.dongGong.calendar.query({ year, month });
}

// ---------------------------------------------------------------------------
// BaZi Analysis — now via tRPC
// ---------------------------------------------------------------------------

import type { AnalyzeBaziParams } from './api.types';

export async function analyzeBazi(params: AnalyzeBaziParams) {
  const timeParam = params.unknownHour ? 'unknown' : params.birthTime;

  return trpc.bazi.analyze.query({
    birth_date: params.birthDate,
    birth_time: timeParam || null,
    gender: params.gender,
    analysis_year: params.analysisYear ?? null,
    include_annual_luck: params.includeAnnualLuck ?? true,
    analysis_month: (params.analysisMonth && params.includeMonthlyLuck) ? params.analysisMonth : null,
    analysis_day: (params.analysisDay && params.includeDailyLuck) ? params.analysisDay : null,
    analysis_time: (params.analysisTime && params.includeHourlyLuck) ? params.analysisTime : null,
    school: params.school ?? 'classic',
    talisman_year_hs: params.showTalismans ? (params.talismanYearHS ?? null) : null,
    talisman_year_eb: params.showTalismans ? (params.talismanYearEB ?? null) : null,
    talisman_month_hs: params.showTalismans ? (params.talismanMonthHS ?? null) : null,
    talisman_month_eb: params.showTalismans ? (params.talismanMonthEB ?? null) : null,
    talisman_day_hs: params.showTalismans ? (params.talismanDayHS ?? null) : null,
    talisman_day_eb: params.showTalismans ? (params.talismanDayEB ?? null) : null,
    talisman_hour_hs: params.showTalismans ? (params.talismanHourHS ?? null) : null,
    talisman_hour_eb: params.showTalismans ? (params.talismanHourEB ?? null) : null,
    location: (params.showLocation && params.locationType) ? params.locationType : null,
  });
}
