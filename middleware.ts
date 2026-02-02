import createMiddleware from 'next-intl/middleware';

// Minimal config for Edge runtime - no external imports
export default createMiddleware({
  locales: ['en', 'id', 'zh'],
  defaultLocale: 'id',
  localePrefix: 'always'
});

export const config = {
  matcher: '/((?!api|_next|_vercel|.*\\..*).*)'
};
