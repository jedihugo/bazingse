import { locales } from '@/i18n/config';
import LocaleProvider from './LocaleProvider';

// Generate static pages for each locale
export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

export default function LocaleLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <LocaleProvider>{children}</LocaleProvider>;
}
