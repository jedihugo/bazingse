'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import InlineProfileForm from '@/components/InlineProfileForm';
import SearchableProfileList from '@/components/SearchableProfileList';
import { getProfiles, deleteProfile, type Profile } from '@/lib/api';

export default function Home() {
  const router = useRouter();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  const loadProfiles = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await getProfiles();
      setProfiles(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profiles');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadProfiles();
  }, [loadProfiles]);

  const handleProfileCreated = (profile: { id: string; name: string }) => {
    setShowCreateForm(false);
    router.push(`/profile/${profile.id}`);
  };

  const handleDeleteProfile = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this profile?')) return;

    try {
      await deleteProfile(id);
      setProfiles(profiles.filter(p => p.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete profile');
    }
  };

  return (
    <div className="min-h-screen tui-bg">
      <Header />
      <main className="mx-auto main-content px-4 py-4">
        <div className="mx-auto" style={{ maxWidth: '800px' }}>
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-2xl font-bold tui-text">Profiles</h1>
            {!showCreateForm && (
              <button
                onClick={() => setShowCreateForm(true)}
                className="tui-btn"
              >
                + New Profile
              </button>
            )}
          </div>

          {error && (
            <div className="mb-4 p-3 tui-frame" style={{ borderColor: 'var(--tui-error)', color: 'var(--tui-error)' }}>
              {error}
            </div>
          )}

          {/* Inline Create Form */}
          {showCreateForm && (
            <div className="mb-4">
              <InlineProfileForm
                onSuccess={handleProfileCreated}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          )}

          {/* Searchable Profile List */}
          {!showCreateForm && (
            <SearchableProfileList
              profiles={profiles}
              onDeleteProfile={handleDeleteProfile}
              isLoading={isLoading}
            />
          )}
        </div>
      </main>
    </div>
  );
}
