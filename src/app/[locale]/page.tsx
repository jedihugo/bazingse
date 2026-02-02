'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import InlineProfileForm from '@/components/InlineProfileForm';
import { getProfiles, deleteProfile, type Profile } from '@/lib/api';

// Detect if running inside Capacitor native app (hide debug link on mobile)
const isCapacitor = typeof window !== 'undefined' &&
  // @ts-expect-error - Capacitor is injected at runtime
  (window.Capacitor?.isNativePlatform?.() || window.Capacitor?.platform !== 'web');

export default function Home() {
  const router = useRouter();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [showDebugLink, setShowDebugLink] = useState(false);

  // Only show debug link on web (not in native mobile app)
  useEffect(() => {
    setShowDebugLink(!isCapacitor);
  }, []);

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
      <main className="mx-auto main-content px-4 py-6">
        <div className="mx-auto" style={{ maxWidth: '800px' }}>
          <div className="flex justify-between items-center mb-6">
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
            <div className="mb-6">
              <InlineProfileForm
                onSuccess={handleProfileCreated}
                onCancel={() => setShowCreateForm(false)}
              />
            </div>
          )}

          {isLoading ? (
            <div className="text-center py-12 tui-text-muted">Loading profiles...</div>
          ) : profiles.length === 0 && !showCreateForm ? (
            <div className="text-center py-12">
              <p className="tui-text-muted mb-4">No profiles yet</p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="tui-btn"
              >
                Create your first profile
              </button>
            </div>
          ) : (
            <div className="grid gap-4">
              {profiles.map(profile => (
                <div
                  key={profile.id}
                  onClick={() => router.push(`/profile/${profile.id}`)}
                  className="tui-frame p-4 cursor-pointer"
                  style={{ transition: 'border-color 0.15s' }}
                  onMouseEnter={(e) => e.currentTarget.style.borderColor = 'var(--tui-water)'}
                  onMouseLeave={(e) => e.currentTarget.style.borderColor = ''}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-lg tui-text">{profile.name}</h3>
                      <p className="text-sm tui-text-dim">
                        {profile.birth_date}
                        {profile.birth_time && ` ${profile.birth_time}`}
                        {' - '}
                        <span style={{ color: profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)' }}>
                          {profile.gender === 'female' ? '\u2640' : '\u2642'}
                        </span>
                      </p>
                    </div>
                    <button
                      onClick={(e) => handleDeleteProfile(profile.id, e)}
                      className="tui-text-muted p-1"
                      style={{ transition: 'color 0.15s' }}
                      onMouseEnter={(e) => e.currentTarget.style.color = 'var(--tui-fire)'}
                      onMouseLeave={(e) => e.currentTarget.style.color = ''}
                      title="Delete profile"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Quick link to debug page - hidden on mobile app */}
          {showDebugLink && (
            <div className="mt-8 pt-4 border-t tui-border-color">
              <a
                href="/debug"
                className="text-sm tui-text-muted"
              >
                Debug Mode
              </a>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
