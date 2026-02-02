// API helpers for BaZi chart generation

// Detect if running inside Capacitor native app
const isCapacitor = typeof window !== 'undefined' &&
  // @ts-expect-error - Capacitor is injected at runtime
  (window.Capacitor?.isNativePlatform?.() || window.Capacitor?.platform !== 'web');

// In development, use the backend directly. In production (static export),
// the backend should be configured via NEXT_PUBLIC_API_URL or accessed directly.
// For Capacitor (mobile), localhost:8008 works in iOS Simulator (shares Mac's network)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || isCapacitor)
    ? 'http://localhost:8008'
    : '');

// Life Event types
export interface LifeEvent {
  id: string;
  year: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
}

export interface LifeEventCreate {
  year: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
}

export interface LifeEventUpdate {
  year?: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
}

// Profile types
export interface Profile {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string | null;
  gender: 'male' | 'female';
  place_of_birth: string | null;
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
}

export interface ProfileUpdate {
  name?: string;
  birth_date?: string;
  birth_time?: string;
  gender?: 'male' | 'female';
  place_of_birth?: string;
}

// Profile CRUD functions
export async function getProfiles(): Promise<Profile[]> {
  const response = await fetch(`${API_BASE_URL}/api/profiles`);
  if (!response.ok) {
    throw new Error('Failed to fetch profiles');
  }
  return response.json();
}

export async function getProfile(id: string): Promise<Profile> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${id}`);
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Profile not found');
    }
    throw new Error('Failed to fetch profile');
  }
  return response.json();
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const response = await fetch(`${API_BASE_URL}/api/profiles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to create profile');
  }
  return response.json();
}

export async function updateProfile(id: string, data: ProfileUpdate): Promise<Profile> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Profile not found');
    }
    throw new Error('Failed to update profile');
  }
  return response.json();
}

export async function deleteProfile(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Profile not found');
    }
    throw new Error('Failed to delete profile');
  }
}

// Life Event CRUD functions
export async function createLifeEvent(profileId: string, data: LifeEventCreate): Promise<LifeEvent> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${profileId}/life_events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Profile not found');
    }
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || 'Failed to create life event');
  }
  return response.json();
}

export async function updateLifeEvent(
  profileId: string,
  eventId: string,
  data: LifeEventUpdate
): Promise<LifeEvent> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${profileId}/life_events/${eventId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Life event not found');
    }
    throw new Error('Failed to update life event');
  }
  return response.json();
}

export async function deleteLifeEvent(profileId: string, eventId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/profiles/${profileId}/life_events/${eventId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Life event not found');
    }
    throw new Error('Failed to delete life event');
  }
}

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
}

export async function analyzeBazi(params: AnalyzeBaziParams) {
  const timeParam = params.unknownHour ? 'unknown' : params.birthTime;

  let apiUrl = `${API_BASE_URL}/api/analyze_bazi?birth_date=${params.birthDate}&birth_time=${encodeURIComponent(timeParam)}&gender=${params.gender}`;

  // Add analysis parameters if time travel mode is enabled
  if (params.analysisYear) {
    apiUrl += `&analysis_year=${params.analysisYear}`;
    apiUrl += `&include_annual_luck=${params.includeAnnualLuck ?? true}`;

    if (params.analysisMonth && params.includeMonthlyLuck) {
      apiUrl += `&analysis_month=${params.analysisMonth}`;
    }

    if (params.analysisDay && params.includeDailyLuck) {
      apiUrl += `&analysis_day=${params.analysisDay}`;
    }

    if (params.analysisTime && params.includeHourlyLuck) {
      apiUrl += `&analysis_time=${encodeURIComponent(params.analysisTime)}`;
    }
  }

  // Add talisman parameters
  if (params.showTalismans) {
    if (params.talismanYearHS) apiUrl += `&talisman_year_hs=${params.talismanYearHS}`;
    if (params.talismanYearEB) apiUrl += `&talisman_year_eb=${params.talismanYearEB}`;
    if (params.talismanMonthHS) apiUrl += `&talisman_month_hs=${params.talismanMonthHS}`;
    if (params.talismanMonthEB) apiUrl += `&talisman_month_eb=${params.talismanMonthEB}`;
    if (params.talismanDayHS) apiUrl += `&talisman_day_hs=${params.talismanDayHS}`;
    if (params.talismanDayEB) apiUrl += `&talisman_day_eb=${params.talismanDayEB}`;
    if (params.talismanHourHS) apiUrl += `&talisman_hour_hs=${params.talismanHourHS}`;
    if (params.talismanHourEB) apiUrl += `&talisman_hour_eb=${params.talismanHourEB}`;
  }

  // Add location parameter
  if (params.showLocation && params.locationType) {
    apiUrl += `&location=${params.locationType}`;
  }

  const response = await fetch(apiUrl);

  if (!response.ok) {
    let errorMessage = 'Chart API request failed';
    try {
      const errorData = await response.json();
      if (errorData.detail) {
        errorMessage = typeof errorData.detail === 'string'
          ? errorData.detail
          : JSON.stringify(errorData.detail);
      } else if (errorData.message) {
        errorMessage = errorData.message;
      }
    } catch {
      // Response wasn't JSON, use status text
      errorMessage = `API error: ${response.status} ${response.statusText}`;
    }
    throw new Error(errorMessage);
  }

  return response.json();
}

// LocalStorage helpers
const STORAGE_KEY = 'bazingse_form_data';

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

export function loadFromStorage(): StoredFormData | null {
  if (typeof window === 'undefined') return null;
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved ? JSON.parse(saved) : null;
  } catch (e) {
    console.error('Error loading from localStorage:', e);
    return null;
  }
}

export function saveToStorage(data: Partial<StoredFormData>): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('Error saving to localStorage:', e);
  }
}

// Date validation helper
export function isValidDate(year: number, month: number, day: number): boolean {
  if (!year || !month || !day) return false;
  if (month < 1 || month > 12) return false;
  if (day < 1 || day > 31) return false;
  if (year < 1900 || year > 2100) return false;

  const date = new Date(year, month - 1, day);
  return date.getFullYear() === year &&
         date.getMonth() === month - 1 &&
         date.getDate() === day;
}

// 60 Jia-Zi validation
const JIAZI_60 = [
  { stem: 'Jia', branch: 'Zi' }, { stem: 'Yi', branch: 'Chou' }, { stem: 'Bing', branch: 'Yin' },
  { stem: 'Ding', branch: 'Mao' }, { stem: 'Wu', branch: 'Chen' }, { stem: 'Ji', branch: 'Si' },
  { stem: 'Geng', branch: 'Wu' }, { stem: 'Xin', branch: 'Wei' }, { stem: 'Ren', branch: 'Shen' },
  { stem: 'Gui', branch: 'You' }, { stem: 'Jia', branch: 'Xu' }, { stem: 'Yi', branch: 'Hai' },
  { stem: 'Bing', branch: 'Zi' }, { stem: 'Ding', branch: 'Chou' }, { stem: 'Wu', branch: 'Yin' },
  { stem: 'Ji', branch: 'Mao' }, { stem: 'Geng', branch: 'Chen' }, { stem: 'Xin', branch: 'Si' },
  { stem: 'Ren', branch: 'Wu' }, { stem: 'Gui', branch: 'Wei' }, { stem: 'Jia', branch: 'Shen' },
  { stem: 'Yi', branch: 'You' }, { stem: 'Bing', branch: 'Xu' }, { stem: 'Ding', branch: 'Hai' },
  { stem: 'Wu', branch: 'Zi' }, { stem: 'Ji', branch: 'Chou' }, { stem: 'Geng', branch: 'Yin' },
  { stem: 'Xin', branch: 'Mao' }, { stem: 'Ren', branch: 'Chen' }, { stem: 'Gui', branch: 'Si' },
  { stem: 'Jia', branch: 'Wu' }, { stem: 'Yi', branch: 'Wei' }, { stem: 'Bing', branch: 'Shen' },
  { stem: 'Ding', branch: 'You' }, { stem: 'Wu', branch: 'Xu' }, { stem: 'Ji', branch: 'Hai' },
  { stem: 'Geng', branch: 'Zi' }, { stem: 'Xin', branch: 'Chou' }, { stem: 'Ren', branch: 'Yin' },
  { stem: 'Gui', branch: 'Mao' }, { stem: 'Jia', branch: 'Chen' }, { stem: 'Yi', branch: 'Si' },
  { stem: 'Bing', branch: 'Wu' }, { stem: 'Ding', branch: 'Wei' }, { stem: 'Wu', branch: 'Shen' },
  { stem: 'Ji', branch: 'You' }, { stem: 'Geng', branch: 'Xu' }, { stem: 'Xin', branch: 'Hai' },
  { stem: 'Ren', branch: 'Zi' }, { stem: 'Gui', branch: 'Chou' }, { stem: 'Jia', branch: 'Yin' },
  { stem: 'Yi', branch: 'Mao' }, { stem: 'Bing', branch: 'Chen' }, { stem: 'Ding', branch: 'Si' },
  { stem: 'Wu', branch: 'Wu' }, { stem: 'Ji', branch: 'Wei' }, { stem: 'Geng', branch: 'Shen' },
  { stem: 'Xin', branch: 'You' }, { stem: 'Ren', branch: 'Xu' }, { stem: 'Gui', branch: 'Hai' }
];

export function isValidJiaziPair(hs: string | null, eb: string | null): boolean {
  if (!hs || !eb) return true; // Partial selection allowed
  return JIAZI_60.some(pair => pair.stem === hs && pair.branch === eb);
}
