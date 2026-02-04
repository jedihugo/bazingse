'use client';

import { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import { type Profile } from '@/lib/api';

interface SearchableProfileListProps {
  profiles: Profile[];
  onDeleteProfile: (id: string, e: React.MouseEvent) => void;
  isLoading?: boolean;
}

const ITEMS_PER_PAGE = 50;

export default function SearchableProfileList({
  profiles,
  onDeleteProfile,
  isLoading = false,
}: SearchableProfileListProps) {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [visibleCount, setVisibleCount] = useState(ITEMS_PER_PAGE);
  const listRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const itemRefs = useRef<(HTMLDivElement | null)[]>([]);

  // Filter profiles based on search query
  const filteredProfiles = useMemo(() => {
    if (!searchQuery.trim()) return profiles;

    const query = searchQuery.toLowerCase();
    return profiles.filter(profile => {
      const name = profile.name?.toLowerCase() || '';
      const date = profile.birth_date || '';
      const place = profile.place_of_birth?.toLowerCase() || '';
      return name.includes(query) || date.includes(query) || place.includes(query);
    });
  }, [profiles, searchQuery]);

  // Visible profiles (lazy loaded)
  const visibleProfiles = useMemo(() => {
    return filteredProfiles.slice(0, visibleCount);
  }, [filteredProfiles, visibleCount]);

  // Reset selection when search changes
  useEffect(() => {
    setSelectedIndex(0);
    setVisibleCount(ITEMS_PER_PAGE);
  }, [searchQuery]);

  // Scroll selected item into view
  useEffect(() => {
    const selectedItem = itemRefs.current[selectedIndex];
    if (selectedItem) {
      selectedItem.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }, [selectedIndex]);

  // Handle infinite scroll
  const handleScroll = useCallback(() => {
    if (!listRef.current) return;

    const { scrollTop, scrollHeight, clientHeight } = listRef.current;
    const nearBottom = scrollTop + clientHeight >= scrollHeight - 200;

    if (nearBottom && visibleCount < filteredProfiles.length) {
      setVisibleCount(prev => Math.min(prev + ITEMS_PER_PAGE, filteredProfiles.length));
    }
  }, [visibleCount, filteredProfiles.length]);

  // Keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    const maxIndex = visibleProfiles.length - 1;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => {
          const next = Math.min(prev + 1, maxIndex);
          // Load more if near end
          if (next >= visibleCount - 5 && visibleCount < filteredProfiles.length) {
            setVisibleCount(prev => Math.min(prev + ITEMS_PER_PAGE, filteredProfiles.length));
          }
          return next;
        });
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (visibleProfiles[selectedIndex]) {
          router.push(`/profile/${visibleProfiles[selectedIndex].id}`);
        }
        break;
      case 'Escape':
        e.preventDefault();
        if (searchQuery) {
          setSearchQuery('');
        } else {
          searchRef.current?.blur();
        }
        break;
    }
  }, [visibleProfiles, selectedIndex, visibleCount, filteredProfiles.length, searchQuery, router]);

  // Focus search on mount
  useEffect(() => {
    searchRef.current?.focus();
  }, []);

  const handleProfileClick = (profile: Profile) => {
    router.push(`/profile/${profile.id}`);
  };

  if (isLoading) {
    return (
      <div className="text-center py-12 tui-text-muted">Loading profiles...</div>
    );
  }

  return (
    <div className="flex flex-col" style={{ height: 'calc(100vh - 200px)' }}>
      {/* Search Input */}
      <div className="tui-frame p-3 mb-4">
        <div className="flex items-center gap-2">
          <span className="tui-text" style={{ color: 'var(--tui-water)' }}>&gt;</span>
          <input
            ref={searchRef}
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type to search..."
            className="flex-1 bg-transparent border-none outline-none tui-text"
            style={{ caretColor: 'var(--tui-water)' }}
            autoComplete="off"
            spellCheck={false}
          />
          <span className="text-xs tui-text-muted">
            {filteredProfiles.length.toLocaleString()} profiles
          </span>
        </div>
        <div className="mt-2 text-xs tui-text-dim flex gap-4">
          <span>[&uarr;&darr;] Navigate</span>
          <span>[Enter] Open</span>
          <span>[Esc] Clear</span>
        </div>
      </div>

      {/* Profile List */}
      <div
        ref={listRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto"
        style={{ scrollbarWidth: 'thin' }}
      >
        {visibleProfiles.length === 0 ? (
          <div className="text-center py-8 tui-text-muted">
            {searchQuery ? `No profiles matching "${searchQuery}"` : 'No profiles yet'}
          </div>
        ) : (
          <div className="space-y-1">
            {visibleProfiles.map((profile, index) => (
              <div
                key={profile.id}
                ref={(el) => { itemRefs.current[index] = el; }}
                onClick={() => handleProfileClick(profile)}
                onMouseEnter={() => setSelectedIndex(index)}
                className={`p-3 cursor-pointer transition-colors ${
                  index === selectedIndex ? 'tui-frame' : ''
                }`}
                style={{
                  borderColor: index === selectedIndex ? 'var(--tui-water)' : 'transparent',
                  backgroundColor: index === selectedIndex ? 'var(--tui-bg-alt)' : 'transparent',
                }}
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-start gap-2">
                    <span
                      className="font-mono"
                      style={{
                        color: index === selectedIndex ? 'var(--tui-water)' : 'transparent',
                        width: '1rem'
                      }}
                    >
                      &gt;
                    </span>
                    <div>
                      <div className="font-semibold tui-text">{profile.name}</div>
                      <div className="text-sm tui-text-dim">
                        {profile.birth_date}
                        {profile.birth_time && ` ${profile.birth_time}`}
                        {' - '}
                        <span style={{ color: profile.gender === 'female' ? 'var(--tui-accent-pink)' : 'var(--tui-water)' }}>
                          {profile.gender === 'female' ? '\u2640' : '\u2642'}
                        </span>
                        {profile.place_of_birth && (
                          <span className="ml-2 tui-text-muted">
                            {profile.place_of_birth.length > 30
                              ? profile.place_of_birth.substring(0, 30) + '...'
                              : profile.place_of_birth}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteProfile(profile.id, e);
                    }}
                    className="tui-text-muted p-1 opacity-0 hover:opacity-100 transition-opacity"
                    style={{ color: index === selectedIndex ? 'var(--tui-text-muted)' : '' }}
                    onMouseEnter={(e) => e.currentTarget.style.color = 'var(--tui-fire)'}
                    onMouseLeave={(e) => e.currentTarget.style.color = ''}
                    title="Delete profile"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}

            {/* Load more indicator */}
            {visibleCount < filteredProfiles.length && (
              <div className="text-center py-4 tui-text-muted text-sm">
                Showing {visibleCount.toLocaleString()} of {filteredProfiles.length.toLocaleString()}
                <span className="ml-2">(scroll for more)</span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
