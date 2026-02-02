'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

// Root page redirects to default locale (client-side for static export)
export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/id/');
  }, [router]);

  return (
    <div className="min-h-screen tui-bg flex items-center justify-center">
      <div className="tui-text-muted">Loading...</div>
    </div>
  );
}
