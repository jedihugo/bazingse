import createMiddleware from 'next-intl/middleware';
import { routing } from './src/i18n/routing';

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
