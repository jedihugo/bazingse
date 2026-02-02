'use client';

import { useLocale } from 'next-intl';
import { useRouter, usePathname } from 'next/navigation';
import { useTransition } from 'react';
import { locales, localeNames, localeFlags, type Locale } from '@/i18n/config';

export default function LocaleSwitcher() {
  const locale = useLocale() as Locale;
  const router = useRouter();
  const pathname = usePathname();
  const [isPending, startTransition] = useTransition();

  const handleChange = (newLocale: Locale) => {
    if (newLocale === locale) return;

    startTransition(() => {
      // Replace the locale segment in the pathname
      const segments = pathname.split('/');
      // segments[0] is empty string from leading /
      // segments[1] is the locale
      if (locales.includes(segments[1] as Locale)) {
        segments[1] = newLocale;
      } else {
        // If no locale in path, insert it
        segments.splice(1, 0, newLocale);
      }
      router.push(segments.join('/'));
    });
  };

  return (
    <div className="flex gap-1">
      {locales.map((loc) => (
        <button
          key={loc}
          onClick={() => handleChange(loc)}
          disabled={isPending}
          className={`tui-btn px-2 py-1 text-xs transition-all ${
            locale === loc
              ? ''
              : 'opacity-60'
          } ${isPending ? 'opacity-50 cursor-wait' : ''}`}
          style={locale === loc ? { background: 'var(--tui-water)', color: 'var(--tui-bg)' } : undefined}
          title={localeNames[loc]}
        >
          {localeFlags[loc]}
        </button>
      ))}
    </div>
  );
}
