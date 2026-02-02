import { redirect } from 'next/navigation';
import { defaultLocale } from '@/i18n/config';

// Root page redirects to default locale
// This is a fallback in case middleware doesn't handle it
export default function RootPage() {
  redirect(`/${defaultLocale}`);
}
