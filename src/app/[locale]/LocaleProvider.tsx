'use client';

import { NextIntlClientProvider } from 'next-intl';
import { useParams } from 'next/navigation';
import { locales, type Locale } from '@/i18n/config';

// Static imports for messages
import enMessages from '@/locales/en';
import idMessages from '@/locales/id';
import zhMessages from '@/locales/zh';

const messagesMap: Record<Locale, typeof enMessages> = {
  en: enMessages,
  id: idMessages,
  zh: zhMessages,
};

export default function LocaleProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const params = useParams();
  const locale = (params.locale as Locale) || 'id';

  // Default to 'id' if locale not valid
  const validLocale = locales.includes(locale) ? locale : 'id';
  const messages = messagesMap[validLocale];

  return (
    <NextIntlClientProvider locale={validLocale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
