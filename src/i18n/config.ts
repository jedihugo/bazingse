// i18n Configuration
// Supported locales for BaZingSe app

export const locales = ['en', 'id', 'zh'] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = 'id';

export const localeNames: Record<Locale, string> = {
  en: 'English',
  id: 'Bahasa Indonesia',
  zh: '中文',
};

export const localeFlags: Record<Locale, string> = {
  en: '🇺🇸',
  id: '🇮🇩',
  zh: '🇨🇳',
};
