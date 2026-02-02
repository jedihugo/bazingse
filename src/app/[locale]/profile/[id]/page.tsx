import ProfilePageClient from './ProfilePageClient';
import { locales } from '@/i18n/config';

// For static export - generate placeholder, actual data loaded client-side
export function generateStaticParams() {
  // Generate a placeholder for each locale
  return locales.map((locale) => ({
    locale,
    id: '_', // Placeholder - real IDs handled client-side
  }));
}

// Allow any dynamic ID (client-side routing)
export const dynamicParams = true;

export default function ProfileRoute() {
  return <ProfilePageClient />;
}
