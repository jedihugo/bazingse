<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import {
    getProfile,
    analyzeBazi,
    deleteLifeEvent,
    type Profile,
    type LifeEvent,
  } from '$lib/api';
  import ProfileInfoBlock from './ProfileInfoBlock.svelte';
  import LifeEventBlock from './LifeEventBlock.svelte';
  import InlineLifeEventForm from './InlineLifeEventForm.svelte';
  import InlineSelector from './chat-form/InlineSelector.svelte';

  interface LifeEventWithChart {
    event: LifeEvent;
    chartData: any;
    isLoading: boolean;
    error: string | null;
  }

  interface ProfilePageProps {
    profileId: string;
  }

  let { profileId }: ProfilePageProps = $props();

  let profile = $state<Profile | null>(null);
  let natalChartData = $state<any>(null);
  let lifeEvents = $state<LifeEventWithChart[]>([]);
  let isLoading = $state(true);
  let error = $state<string | null>(null);
  let showAddForm = $state(false);
  let school = $state<'classic' | 'physics'>('classic');

  const SCHOOL_OPTIONS = [
    { value: 'classic', label: 'Classic' },
    { value: 'physics', label: 'Physics' },
  ];

  function sortEventsByDate(a: LifeEvent, b: LifeEvent): number {
    if (a.year !== b.year) return a.year - b.year;
    if ((a.month || 0) !== (b.month || 0)) return (a.month || 0) - (b.month || 0);
    return (a.day || 0) - (b.day || 0);
  }

  async function fetchChartForEvent(profileData: Profile, event: LifeEvent): Promise<any> {
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
  }

  async function loadProfile() {
    try {
      isLoading = true;
      error = null;

      const profileData = await getProfile(profileId);
      profile = profileData;

      // Load natal chart
      const natalChart = await analyzeBazi({
        birthDate: profileData.birth_date,
        birthTime: profileData.birth_time || '',
        gender: profileData.gender as 'male' | 'female',
        unknownHour: !profileData.birth_time,
        school,
      });
      natalChartData = natalChart;

      // Load charts for existing life events
      const events = profileData.life_events || [];
      const sortedEvents = [...events].sort(sortEventsByDate);

      // Initialize events with loading state
      lifeEvents = sortedEvents.map(event => ({
        event,
        chartData: null,
        isLoading: true,
        error: null,
      }));

      // Fetch chart data for each event
      for (let i = 0; i < sortedEvents.length; i++) {
        try {
          const chartData = await fetchChartForEvent(profileData, sortedEvents[i]);
          lifeEvents = lifeEvents.map((item, idx) =>
            idx === i ? { ...item, chartData, isLoading: false } : item
          );
        } catch (err) {
          lifeEvents = lifeEvents.map((item, idx) =>
            idx === i
              ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
              : item
          );
        }
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to load profile';
    } finally {
      isLoading = false;
    }
  }

  // Reload when school changes
  $effect(() => {
    // Track school to trigger reload
    const _s = school;
    loadProfile();
  });

  function handleProfileUpdate(updatedProfile: Profile) {
    profile = updatedProfile;
  }

  async function handleAddEvent(newEvent: LifeEvent) {
    showAddForm = false;
    if (!profile) return;

    const newEventWithChart: LifeEventWithChart = {
      event: newEvent,
      chartData: null,
      isLoading: true,
      error: null,
    };

    lifeEvents = [...lifeEvents, newEventWithChart].sort((a, b) => sortEventsByDate(a.event, b.event));

    profile = {
      ...profile,
      life_events: [...(profile.life_events || []), newEvent],
    };

    try {
      const chartData = await fetchChartForEvent(profile, newEvent);
      lifeEvents = lifeEvents.map(item =>
        item.event.id === newEvent.id
          ? { ...item, chartData, isLoading: false }
          : item
      );
    } catch (err) {
      lifeEvents = lifeEvents.map(item =>
        item.event.id === newEvent.id
          ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
          : item
      );
    }
  }

  async function handleEventUpdate(updatedEvent: LifeEvent) {
    const previousEvent = lifeEvents.find(item => item.event.id === updatedEvent.id);
    const abroadChanged = previousEvent && (!!previousEvent.event.is_abroad !== !!updatedEvent.is_abroad);

    lifeEvents = lifeEvents.map(item =>
      item.event.id === updatedEvent.id
        ? { ...item, event: updatedEvent, ...(abroadChanged ? { isLoading: true, error: null } : {}) }
        : item
    );

    if (profile) {
      profile = {
        ...profile,
        life_events: (profile.life_events || []).map(e =>
          e.id === updatedEvent.id ? updatedEvent : e
        ),
      };
    }

    if (abroadChanged && profile) {
      try {
        const chartData = await fetchChartForEvent(profile, updatedEvent);
        lifeEvents = lifeEvents.map(item =>
          item.event.id === updatedEvent.id
            ? { ...item, chartData, isLoading: false }
            : item
        );
      } catch (err) {
        lifeEvents = lifeEvents.map(item =>
          item.event.id === updatedEvent.id
            ? { ...item, isLoading: false, error: err instanceof Error ? err.message : 'Failed to load' }
            : item
        );
      }
    }
  }

  async function handleDeleteEvent(eventId: string) {
    try {
      await deleteLifeEvent(profileId, eventId);
      lifeEvents = lifeEvents.filter(item => item.event.id !== eventId);
      if (profile) {
        profile = {
          ...profile,
          life_events: (profile.life_events || []).filter(e => e.id !== eventId),
        };
      }
    } catch (err) {
      console.error('Failed to delete event:', err);
    }
  }

  let natalEvent = $derived<LifeEvent>({
    id: 'natal',
    year: profile ? parseInt(profile.birth_date.split('-')[0]) : 0,
    month: profile ? parseInt(profile.birth_date.split('-')[1]) : null,
    day: profile ? parseInt(profile.birth_date.split('-')[2]) : null,
    notes: null,
    created_at: '',
    updated_at: '',
  });

  let existingDates = $derived(lifeEvents.map(item => ({
    year: item.event.year,
    month: item.event.month,
    day: item.event.day,
  })));
</script>

{#if isLoading && !profile}
  <div class="py-12 text-center tui-text-muted">
    <div class="inline-block animate-spin h-6 w-6 border-2 tui-border mr-2" style="border-top-color: var(--tui-water)"></div>
    Loading profile...
  </div>
{:else if error}
  <div class="py-12 text-center">
    <div class="mb-4" style="color: var(--tui-error)">{error}</div>
    <button
      onclick={() => goto('/')}
      class="tui-btn"
    >
      Back to profiles
    </button>
  </div>
{:else if !profile}
  <div class="py-12 text-center tui-text-muted">
    Profile not found
  </div>
{:else}
  <div class="min-h-screen tui-bg">
    <!-- Profile Info Block -->
    <ProfileInfoBlock
      {profile}
      onUpdate={handleProfileUpdate}
      onBack={() => goto('/')}
      onBirthDataChange={loadProfile}
    />

    <!-- School Toggle -->
    <div class="px-4 pt-2 flex items-center gap-2">
      <span class="tui-text-muted text-sm">School:</span>
      <InlineSelector
        options={SCHOOL_OPTIONS}
        value={school}
        onChange={(v) => school = v as 'classic' | 'physics'}
      />
    </div>

    <!-- Main content -->
    <div class="px-4 pb-8 space-y-4">
      <!-- Natal Chart Block -->
      {#if natalChartData}
        <LifeEventBlock
          {profileId}
          event={natalEvent}
          chartData={natalChartData}
          isNatal={true}
        />
      {/if}

      <!-- Life Event Blocks -->
      {#each lifeEvents as item (item.event.id)}
        <LifeEventBlock
          {profileId}
          event={item.event}
          chartData={item.chartData}
          isLoading={item.isLoading}
          error={item.error}
          onDelete={() => handleDeleteEvent(item.event.id)}
          onEventUpdate={handleEventUpdate}
        />
      {/each}

      <!-- Add Life Event -->
      {#if showAddForm}
        <div class="py-2">
          <InlineLifeEventForm
            {profileId}
            onSuccess={handleAddEvent}
            onCancel={() => showAddForm = false}
            {existingDates}
          />
        </div>
      {:else}
        <button
          onclick={() => showAddForm = true}
          class="w-full py-3 border-2 border-dashed tui-border-color tui-text-muted transition-colors flex items-center justify-center gap-2 add-event-btn"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add Life Event
        </button>
      {/if}
    </div>
  </div>
{/if}

<style>
  .add-event-btn:hover {
    border-color: var(--tui-water);
    color: var(--tui-water);
  }
</style>
