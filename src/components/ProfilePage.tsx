'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  getProfile,
  analyzeBazi,
  deleteLifeEvent,
  type Profile,
  type LifeEvent,
} from '@/lib/api';
import ProfileInfoBlock from './ProfileInfoBlock';
import LifeEventBlock from './LifeEventBlock';
import InlineLifeEventForm from './InlineLifeEventForm';
import InlineSelector from './chat-form/InlineSelector';
import { useT } from './LanguageProvider';
import { PROFILE_PAGE, CHART, EVENT_FORM } from '@/lib/t';

interface LifeEventWithChart {
  event: LifeEvent;
  chartData: any;
  isLoading: boolean;
  error: string | null;
}

interface ProfilePageProps {
  profileId: string;
}

// Sort events by date (ascending)
function sortEventsByDate(a: LifeEvent, b: LifeEvent): number {
  if (a.year !== b.year) return a.year - b.year;
  if ((a.month || 0) !== (b.month || 0)) return (a.month || 0) - (b.month || 0);
  return (a.day || 0) - (b.day || 0);
}

const SCHOOL_OPTIONS = [
  { value: 'classic', label: 'Classic' },
  { value: 'physics', label: 'Physics' },
];

export default function ProfilePage({ profileId }: ProfilePageProps) {
  const { t } = useT();
  const router = useRouter();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [natalChartData, setNatalChartData] = useState<any>(null);
  const [lifeEvents, setLifeEvents] = useState<LifeEventWithChart[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [school, setSchool] = useState<'classic' | 'physics'>('classic');

  // Fetch chart data for a life event
  const fetchChartForEvent = useCallback(async (
    profileData: Profile,
    event: LifeEvent
  ): Promise<any> => {
    return analyzeBazi({
      birthDate: profileData.birth_date,
      birthTime: profileData.birth_time || '',
      gender: profileData.gender as 'male' | 'female',
      unknownHour: !profileData.birth_time,
      analysisYear: event.year,
      includeAnnualLuck: true,
      analysisMonth: event.month || null,
      includeMonthlyLuck: !!event.month,
      analysisDay: event.day || null,
      includeDailyLuck: !!event.day,
      showLocation: !!event.is_abroad,
      locationType: event.is_abroad ? 'overseas' : null,
      school,
    });
  }, [school]);

  // Load profile and all chart data
  const loadProfile = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const profileData = await getProfile(profileId);
      setProfile(profileData);

      // Load natal chart
      const natalChart = await analyzeBazi({
        birthDate: profileData.birth_date,
        birthTime: profileData.birth_time || '',
        gender: profileData.gender as 'male' | 'female',
        unknownHour: !profileData.birth_time,
        school,
      });
      setNatalChartData(natalChart);

      // Load charts for existing life events
      const events = profileData.life_events || [];
      const sortedEvents = [...events].sort(sortEventsByDate);

      // Initialize events with loading state
      const eventsWithCharts: LifeEventWithChart[] = sortedEvents.map(event => ({
        event,
        chartData: null,
        isLoading: true,
        error: null,
      }));
      setLifeEvents(eventsWithCharts);

      // Fetch chart data for each event
      for (let i = 0; i < sortedEvents.length; i++) {
        try {
          const chartData = await fetchChartForEvent(profileData, sortedEvents[i]);
          setLifeEvents(prev =>
            prev.map((item, idx) =>
              idx === i ? { ...item, chartData, isLoading: false } : item
            )
          );
        } catch (err) {
          setLifeEvents(prev =>
            prev.map((item, idx) =>
              idx === i
                ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
                : item
            )
          );
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile');
    } finally {
      setIsLoading(false);
    }
  }, [profileId, fetchChartForEvent, school]);

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  // Handle profile update from ProfileInfoBlock
  const handleProfileUpdate = useCallback((updatedProfile: Profile) => {
    setProfile(updatedProfile);
  }, []);

  // Handle new life event
  const handleAddEvent = useCallback(async (newEvent: LifeEvent) => {
    setShowAddForm(false);

    if (!profile) return;

    // Add to state with loading
    const newEventWithChart: LifeEventWithChart = {
      event: newEvent,
      chartData: null,
      isLoading: true,
      error: null,
    };

    setLifeEvents(prev => {
      const updated = [...prev, newEventWithChart];
      return updated.sort((a, b) => sortEventsByDate(a.event, b.event));
    });

    // Update profile's life_events
    setProfile(prev => prev ? {
      ...prev,
      life_events: [...(prev.life_events || []), newEvent],
    } : null);

    // Fetch chart data
    try {
      const chartData = await fetchChartForEvent(profile, newEvent);
      setLifeEvents(prev =>
        prev.map(item =>
          item.event.id === newEvent.id
            ? { ...item, chartData, isLoading: false }
            : item
        )
      );
    } catch (err) {
      setLifeEvents(prev =>
        prev.map(item =>
          item.event.id === newEvent.id
            ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
            : item
        )
      );
    }
  }, [profile, fetchChartForEvent]);

  // Handle event update (e.g., notes changed, abroad toggled)
  const handleEventUpdate = useCallback(async (updatedEvent: LifeEvent) => {
    // Check if is_abroad changed — need to re-fetch chart
    const previousEvent = lifeEvents.find(item => item.event.id === updatedEvent.id);
    const abroadChanged = previousEvent && (!!previousEvent.event.is_abroad !== !!updatedEvent.is_abroad);

    setLifeEvents(prev =>
      prev.map(item =>
        item.event.id === updatedEvent.id
          ? { ...item, event: updatedEvent, ...(abroadChanged ? { isLoading: true, error: null } : {}) }
          : item
      )
    );

    // Update profile's life_events
    setProfile(prev => prev ? {
      ...prev,
      life_events: (prev.life_events || []).map(e =>
        e.id === updatedEvent.id ? updatedEvent : e
      ),
    } : null);

    // Re-fetch chart if abroad flag changed
    if (abroadChanged && profile) {
      try {
        const chartData = await fetchChartForEvent(profile, updatedEvent);
        setLifeEvents(prev =>
          prev.map(item =>
            item.event.id === updatedEvent.id
              ? { ...item, chartData, isLoading: false }
              : item
          )
        );
      } catch (err) {
        setLifeEvents(prev =>
          prev.map(item =>
            item.event.id === updatedEvent.id
              ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
              : item
          )
        );
      }
    }
  }, [lifeEvents, profile, fetchChartForEvent]);

  // Handle event deletion
  const handleDeleteEvent = useCallback(async (eventId: string) => {
    try {
      await deleteLifeEvent(profileId, eventId);

      // Remove from state
      setLifeEvents(prev => prev.filter(item => item.event.id !== eventId));

      // Update profile's life_events
      setProfile(prev => prev ? {
        ...prev,
        life_events: (prev.life_events || []).filter(e => e.id !== eventId),
      } : null);
    } catch (err) {
      console.error('Failed to delete event:', err);
    }
  }, [profileId]);

  // Create a synthetic "natal" event for consistent rendering
  const natalEvent: LifeEvent = {
    id: 'natal',
    year: profile ? parseInt(profile.birth_date.split('-')[0]) : 0,
    month: profile ? parseInt(profile.birth_date.split('-')[1]) : null,
    day: profile ? parseInt(profile.birth_date.split('-')[2]) : null,
    notes: null,
    created_at: '',
    updated_at: '',
  };

  // Loading state
  if (isLoading && !profile) {
    return (
      <div className="py-12 text-center tui-text-muted">
        <div className="inline-block animate-spin h-6 w-6 border-2 tui-border mr-2" style={{ borderTopColor: 'var(--tui-water)' }}></div>
        {t(PROFILE_PAGE.loading)}
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="py-12 text-center">
        <div className="mb-4" style={{ color: 'var(--tui-error)' }}>{error}</div>
        <button
          onClick={() => router.push('/')}
          className="tui-btn"
        >
          {t(PROFILE_PAGE.back)}
        </button>
      </div>
    );
  }

  // Not found state
  if (!profile) {
    return (
      <div className="py-12 text-center tui-text-muted">
        {t(PROFILE_PAGE.not_found)}
      </div>
    );
  }

  const existingDates = lifeEvents.map(item => ({
    year: item.event.year,
    month: item.event.month,
    day: item.event.day,
  }));

  return (
    <div className="min-h-screen tui-bg">
      {/* Profile Info Block (fixed header) */}
      <ProfileInfoBlock
        profile={profile}
        onProfileUpdate={handleProfileUpdate}
        onBack={() => router.push('/')}
        onBirthDataChange={loadProfile}
      />

      {/* School Toggle */}
      <div className="px-4 pt-2 flex items-center gap-2">
        <span className="tui-text-muted text-sm">{t(CHART.school)}:</span>
        <InlineSelector
          options={SCHOOL_OPTIONS}
          value={school}
          onChange={(v) => setSchool(v as 'classic' | 'physics')}
        />
      </div>

      {/* Main content */}
      <div className="px-4 pb-8 space-y-4">
        {/* Natal Chart Block */}
        {natalChartData && (
          <LifeEventBlock
            profileId={profileId}
            event={natalEvent}
            chartData={natalChartData}
            isNatal={true}
          />
        )}

        {/* Life Event Blocks */}
        {lifeEvents.map(item => (
          <LifeEventBlock
            key={item.event.id}
            profileId={profileId}
            event={item.event}
            chartData={item.chartData}
            isLoading={item.isLoading}
            error={item.error}
            onDelete={() => handleDeleteEvent(item.event.id)}
            onEventUpdate={handleEventUpdate}
          />
        ))}

        {/* Add Life Event - Inline Form or Button */}
        {showAddForm ? (
          <div className="py-2">
            <InlineLifeEventForm
              profileId={profileId}
              onSuccess={handleAddEvent}
              onCancel={() => setShowAddForm(false)}
              existingDates={existingDates}
            />
          </div>
        ) : (
          <button
            onClick={() => setShowAddForm(true)}
            className="w-full py-3 border-2 border-dashed tui-border-color tui-text-muted transition-colors flex items-center justify-center gap-2"
            style={{ '--hover-border': 'var(--tui-water)' } as React.CSSProperties}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
            {t(EVENT_FORM.add_button)}
          </button>
        )}
      </div>
    </div>
  );
}
