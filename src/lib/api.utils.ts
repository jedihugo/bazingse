// Utility functions that don't call APIs — extracted from api.ts

import type { StoredFormData } from './api.types';

// LocalStorage helpers
const STORAGE_KEY = 'bazingse_form_data';

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
