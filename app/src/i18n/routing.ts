import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';
import { locales, defaultLocale } from './config';

export const routing = defineRouting({
  locales,
  defaultLocale,
  localePrefix: 'always', // Always show locale in URL: /en, /id, /zh
});

// Lightweight wrappers around Next.js navigation APIs
// that handle locale routing
export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
