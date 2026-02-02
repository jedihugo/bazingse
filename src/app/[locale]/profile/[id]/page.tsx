'use client';

import { useParams } from 'next/navigation';
import Header from '@/components/Header';
import ProfilePage from '@/components/ProfilePage';

export default function ProfileRoute() {
  const params = useParams();
  const profileId = params?.id as string;

  if (!profileId) {
    return (
      <div className="min-h-screen tui-bg">
        <Header />
        <main className="mx-auto main-content p-4">
          <p className="text-center tui-text-muted">Loading...</p>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen tui-bg">
      <Header />
      <main className="mx-auto main-content">
        <div className="mx-auto" style={{ maxWidth: '900px' }}>
          <ProfilePage profileId={profileId} />
        </div>
      </main>
    </div>
  );
}
