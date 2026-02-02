import createMiddleware from 'next-intl/middleware';
import { defineRouting } from 'next-intl/routing';

// Inline routing config to avoid import issues on Vercel Edge
const routing = defineRouting({
  locales: ['en', 'id', 'zh'],
  defaultLocale: 'id',
  localePrefix: 'always',
});

export default createMiddleware(routing);

export const config = {
  // Match all pathnames except for:
  // - API routes (/api)
  // - Static files (_next, images, favicon, etc.)
  matcher: [
    // Match root
    '/',
    // Match locale paths
    '/(en|id|zh)/:path*',
    // Match paths without locale (to redirect to default)
    '/((?!api|_next|.*\\..*).*)',
  ],
};
