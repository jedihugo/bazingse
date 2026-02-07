'use client';

import { type Profile } from '@/lib/api';

interface ProfileHeaderProps {
  profile: Profile;
  onBack?: () => void;
}

export default function ProfileHeader({ profile, onBack }: ProfileHeaderProps) {
  return (
    <div className="tui-bg-panel tui-frame p-4 mb-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {onBack && (
            <button
              onClick={onBack}
              className="tui-back-btn"
              title="Back to profiles"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          )}
          <div>
            <h1 className="text-2xl font-bold tui-text">{profile.name}</h1>
            <div className="flex items-center gap-3 text-sm tui-text-dim mt-1">
              <span>{profile.birth_date}</span>
              {profile.birth_time && (
                <>
                  <span className="tui-text-muted">|</span>
                  <span>{profile.birth_time}</span>
                </>
              )}
              <span className="tui-text-muted">|</span>
              <span style={{ color: profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)' }}>
                {profile.gender === 'female' ? '\u2640 Female' : '\u2642 Male'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
