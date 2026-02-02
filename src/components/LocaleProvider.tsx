'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { NextIntlClientProvider } from 'next-intl';

// Static imports for messages
import enMessages from '@/locales/en';
import idMessages from '@/locales/id';
import zhMessages from '@/locales/zh';

type Locale = 'en' | 'id' | 'zh';

const messagesMap: Record<Locale, typeof enMessages> = {
  en: enMessages,
  id: idMessages,
  zh: zhMessages,
};

const LocaleContext = createContext<{
  locale: Locale;
  setLocale: (locale: Locale) => void;
}>({
  locale: 'id',
  setLocale: () => {},
});

export function useLocale() {
  return useContext(LocaleContext);
}

export default function LocaleProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>('id');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Read from localStorage on mount
    const saved = localStorage.getItem('locale') as Locale;
    if (saved && messagesMap[saved]) {
      setLocaleState(saved);
    }
    setMounted(true);
  }, []);

  const setLocale = (newLocale: Locale) => {
    setLocaleState(newLocale);
    localStorage.setItem('locale', newLocale);
  };

  // Avoid hydration mismatch
  if (!mounted) {
    return null;
  }

  return (
    <LocaleContext.Provider value={{ locale, setLocale }}>
      <NextIntlClientProvider locale={locale} messages={messagesMap[locale]}>
        {children}
      </NextIntlClientProvider>
    </LocaleContext.Provider>
  );
}
