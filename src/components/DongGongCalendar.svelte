<script lang="ts">
  import { onMount } from 'svelte';
  import { getDongGongCalendar } from '$lib/api';
  import type { DongGongDay, DongGongCalendarResponse, DongGongForbidden } from '$lib/api.types';

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  /** Format a decimal hour (e.g. 14.5) as "14:30" */
  function formatHour(h: number): string {
    const hrs = Math.floor(h);
    const mins = Math.round((h - hrs) * 60);
    return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}`;
  }

  /** Human-readable forbidden range, e.g. "14:23 - 24:00" */
  function forbiddenRange(f: DongGongForbidden): string {
    return `${formatHour(f.forbidden_start_hour)} \u2013 ${formatHour(f.forbidden_end_hour)}`;
  }

  function ratingColor(value: number): string {
    if (value >= 4) return 'var(--tui-wood)';
    if (value === 3) return 'var(--tui-earth)';
    if (value === 2.5) return 'var(--tui-water)';
    if (value <= 1) return '#000000';
    return 'var(--tui-fire)';
  }

  function ratingBg(value: number): string {
    if (value >= 4) return 'color-mix(in srgb, var(--tui-wood) 15%, var(--tui-bg))';
    if (value === 3) return 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))';
    if (value === 2.5) return 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))';
    if (value <= 1) return 'color-mix(in srgb, #000000 15%, var(--tui-bg))';
    return 'color-mix(in srgb, var(--tui-fire) 15%, var(--tui-bg))';
  }

  /** Map stem pinyin to CSS variable for its element color */
  const STEM_COLOR: Record<string, string> = {
    Jia: 'var(--tui-wood)', Yi: 'var(--tui-wood-yin)',
    Bing: 'var(--tui-fire)', Ding: 'var(--tui-fire-yin)',
    Wu: 'var(--tui-earth)', Ji: 'var(--tui-earth-yin)',
    Geng: 'var(--tui-metal)', Xin: 'var(--tui-metal-yin)',
    Ren: 'var(--tui-water)', Gui: 'var(--tui-water-yin)',
  };

  /** Map branch pinyin to CSS variable for its main element color */
  const BRANCH_COLOR: Record<string, string> = {
    Zi: 'var(--tui-water)', Chou: 'var(--tui-earth-yin)',
    Yin: 'var(--tui-wood)', Mao: 'var(--tui-wood-yin)',
    Chen: 'var(--tui-earth)', Si: 'var(--tui-fire-yin)',
    Wu: 'var(--tui-fire)', Wei: 'var(--tui-earth-yin)',
    Shen: 'var(--tui-metal)', You: 'var(--tui-metal-yin)',
    Xu: 'var(--tui-earth)', Hai: 'var(--tui-water-yin)',
  };

  const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const MONTH_NAMES = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
  ];

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  const today = new Date();

  let year = $state(today.getFullYear());
  let month = $state(today.getMonth() + 1);
  let data = $state<DongGongCalendarResponse | null>(null);
  let selectedDay = $state<number | null>(null);
  let focusedDay = $state<number | null>(null);
  let isLoading = $state(true);
  let error = $state<string | null>(null);

  // ---------------------------------------------------------------------------
  // Derived
  // ---------------------------------------------------------------------------

  let selectedDayData = $derived(data?.days.find(d => d.day === selectedDay) ?? null);
  let emptyCells = $derived(data ? data.first_day_weekday : 0);

  function isToday(day: number): boolean {
    return year === today.getFullYear() && month === today.getMonth() + 1 && day === today.getDate();
  }

  /** Year pillar display list: if a day is selected/today, show its specific year; otherwise show all spanned */
  let yearsList = $derived.by(() => {
    if (!data) return [];
    const activeDayData = selectedDayData || data.days.find(d => isToday(d.day));
    if (activeDayData) {
      return [{
        stem: activeDayData.year_stem,
        stem_chinese: activeDayData.year_stem_chinese,
        branch: activeDayData.year_branch,
        branch_chinese: activeDayData.year_branch_chinese,
      }];
    }
    return data.chinese_years_spanned;
  });

  /** Month pillar display list: reactive to selected day */
  let monthsList = $derived.by(() => {
    if (!data) return [];
    const activeDayData = selectedDayData || data.days.find(d => isToday(d.day));
    if (activeDayData) {
      return data.chinese_months_spanned.filter(cm => cm.month === activeDayData.chinese_month);
    }
    return data.chinese_months_spanned;
  });

  // ---------------------------------------------------------------------------
  // Data loading
  // ---------------------------------------------------------------------------

  async function loadCalendar() {
    try {
      isLoading = true;
      error = null;
      const result = await getDongGongCalendar(year, month);
      data = result;
    } catch (err) {
      error = err instanceof Error ? err.message : 'Failed to load calendar';
    } finally {
      isLoading = false;
    }
  }

  // Load on mount and whenever year/month changes
  onMount(() => {
    loadCalendar();
  });

  // Track year/month changes after mount
  let prevYear = $state(year);
  let prevMonth = $state(month);

  $effect(() => {
    if (year !== prevYear || month !== prevMonth) {
      prevYear = year;
      prevMonth = month;
      selectedDay = null;
      focusedDay = null;
      loadCalendar();
    }
  });

  // ---------------------------------------------------------------------------
  // Navigation
  // ---------------------------------------------------------------------------

  function goToPrevMonth() {
    if (month === 1) { year = year - 1; month = 12; }
    else { month = month - 1; }
  }

  function goToNextMonth() {
    if (month === 12) { year = year + 1; month = 1; }
    else { month = month + 1; }
  }

  function goToToday() {
    year = today.getFullYear();
    month = today.getMonth() + 1;
    selectedDay = today.getDate();
    focusedDay = today.getDate();
  }

  function toggleDay(day: number) {
    selectedDay = selectedDay === day ? null : day;
  }

  // ---------------------------------------------------------------------------
  // Keyboard navigation
  // ---------------------------------------------------------------------------

  function handleKeydown(e: KeyboardEvent) {
    // Ignore if typing in an input
    if ((e.target as HTMLElement)?.tagName === 'INPUT') return;

    if (e.key === '[' || e.key === 'h') { goToPrevMonth(); return; }
    if (e.key === ']' || e.key === 'l') { goToNextMonth(); return; }
    if (e.key === 't') { goToToday(); return; }

    if (!data) return;
    const maxDay = data.days_in_month;

    if (e.key === 'Escape') { selectedDay = null; return; }

    if (e.key === 'Enter' && focusedDay) {
      selectedDay = selectedDay === focusedDay ? null : focusedDay;
      return;
    }

    // Arrow key navigation
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) {
      e.preventDefault();
      const current = focusedDay || 1;
      let next = current;
      if (e.key === 'ArrowLeft') next = current - 1;
      if (e.key === 'ArrowRight') next = current + 1;
      if (e.key === 'ArrowUp') next = current - 7;
      if (e.key === 'ArrowDown') next = current + 7;
      if (next < 1) next = 1;
      if (next > maxDay) next = maxDay;
      focusedDay = next;
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="tui-frame calendar-frame">
  <!-- Title bar -->
  <div class="calendar-title-bar">
    Dong Gong Date Selection
  </div>

  <!-- Month navigation -->
  <div class="calendar-nav">
    <button onclick={goToPrevMonth} class="tui-btn nav-btn" title="Previous month">
      &lt;
    </button>
    <div class="nav-center">
      <span class="font-bold tui-text">{MONTH_NAMES[month - 1]} {year}</span>
      {#if data}
        <div class="pillar-info">
          <!-- Year pillar(s) -->
          <div>
            {#each yearsList as yr, i}
              {#if i > 0}<span class="tui-text-muted"> &rarr; </span>{/if}
              <span style="color: {STEM_COLOR[yr.stem]}">{yr.stem_chinese}</span><span style="color: {BRANCH_COLOR[yr.branch]}">{yr.branch_chinese}</span>
              <span class="tui-text-muted"> &middot; </span>
              <span style="color: {STEM_COLOR[yr.stem]}">{yr.stem}</span>
              {' '}
              <span style="color: {BRANCH_COLOR[yr.branch]}">{yr.branch}</span>
            {/each}
            <span class="tui-text-muted"> \u5E74</span>
          </div>
          <!-- Month pillar(s) -->
          <div>
            {#each monthsList as cm, i}
              {#if i > 0}<span class="tui-text-muted"> / </span>{/if}
              <span class="tui-text-muted">{cm.chinese} </span>
              <span style="color: {STEM_COLOR[cm.stem]}">{cm.stem_chinese}</span><span style="color: {BRANCH_COLOR[cm.branch_id]}">{cm.branch_chinese}</span>
              <span class="tui-text-muted"> &middot; </span>
              <span style="color: {STEM_COLOR[cm.stem]}">{cm.stem}</span>
              {' '}
              <span style="color: {BRANCH_COLOR[cm.branch_id]}">{cm.branch_id}</span>
            {/each}
          </div>
        </div>
      {/if}
    </div>
    <button onclick={goToNextMonth} class="tui-btn nav-btn" title="Next month">
      &gt;
    </button>
  </div>

  <!-- Today button -->
  <div class="today-bar">
    <button onclick={goToToday} class="tui-btn today-btn">
      Today
    </button>
  </div>

  <!-- Loading / Error -->
  {#if isLoading}
    <div class="status-msg tui-text-muted">Loading...</div>
  {/if}
  {#if error}
    <div class="status-msg error-msg">{error}</div>
  {/if}

  <!-- Calendar grid -->
  {#if data && !isLoading}
    <div>
      <!-- Weekday headers -->
      <div class="weekday-header">
        {#each WEEKDAYS as wd}
          <div class="tui-text-muted">{wd}</div>
        {/each}
      </div>

      <!-- Day cells -->
      <div class="day-grid">
        <!-- Empty cells for offset -->
        {#each Array(emptyCells) as _, i}
          <div class="empty-cell" style="grid-column: {i + 1};"></div>
        {/each}

        <!-- Day cells -->
        {#each data.days as dayData (dayData.day)}
          {@const isTodayCell = isToday(dayData.day)}
          {@const isSelected = selectedDay === dayData.day}
          {@const isFocused = focusedDay === dayData.day}
          <button
            onclick={() => toggleDay(dayData.day)}
            onfocus={() => focusedDay = dayData.day}
            class="day-cell"
            style="
              background: {isSelected ? (dayData.rating ? ratingBg(dayData.rating.value) : 'var(--tui-bg-alt)') : 'transparent'};
              outline: {isFocused ? '2px solid var(--tui-water)' : isTodayCell ? '2px solid var(--tui-water)' : 'none'};
              outline-offset: -2px;
              border-right: {(emptyCells + dayData.day) % 7 !== 0 ? '1px solid var(--tui-border-dim, var(--tui-border))' : 'none'};
            "
          >
            <!-- Day number -->
            <div class="day-number" style="color: {dayData.weekday === 0 ? 'var(--tui-fire)' : 'var(--tui-fg)'}">
              {dayData.day}
            </div>

            <!-- Rating symbol -->
            {#if dayData.rating}
              <div class="day-rating">
                <span style="color: {ratingColor(dayData.rating.value)}">
                  {dayData.rating.symbol}
                </span>
                {#if dayData.forbidden}
                  <span style="color: #000000">/\u2717</span>
                {/if}
              </div>
            {/if}

            <!-- Day stem-branch with element colors -->
            <div class="day-pillar">
              <div class="day-pillar-chinese">
                <span style="color: {STEM_COLOR[dayData.day_stem]}">{dayData.day_stem_chinese}</span><span style="color: {BRANCH_COLOR[dayData.day_branch]}">{dayData.day_branch_chinese}</span>
              </div>
              <div class="day-pillar-pinyin">
                <span style="color: {STEM_COLOR[dayData.day_stem]}">{dayData.day_stem}</span>
                {' '}
                <span style="color: {BRANCH_COLOR[dayData.day_branch]}">{dayData.day_branch}</span>
              </div>
            </div>

            <!-- Moon phase -->
            {#if dayData.moon_phase}
              <div class="day-moon">
                {dayData.moon_phase.emoji}
              </div>
            {/if}
          </button>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Selected day detail panel -->
  {#if selectedDayData}
    <div class="detail-panel">
      <!-- Header: date + pillar -->
      <div class="detail-header">
        <div class="detail-title">
          <span class="tui-text">{selectedDayData.day} &middot; </span>
          <span style="color: {STEM_COLOR[selectedDayData.day_stem]}">{selectedDayData.day_stem_chinese}</span><span style="color: {BRANCH_COLOR[selectedDayData.day_branch]}">{selectedDayData.day_branch_chinese}</span>
          <span class="tui-text"> </span>
          <span style="color: {STEM_COLOR[selectedDayData.day_stem]}">{selectedDayData.day_stem}</span>
          {' '}
          <span style="color: {BRANCH_COLOR[selectedDayData.day_branch]}">{selectedDayData.day_branch}</span>
        </div>
        <button onclick={() => selectedDay = null} class="tui-btn close-btn">
          &times;
        </button>
      </div>

      <!-- Officer + Rating -->
      <div class="detail-badges">
        {#if selectedDayData.officer}
          <span class="tui-text-muted">
            {selectedDayData.officer.chinese} {selectedDayData.officer.english}
          </span>
        {/if}
        {#if selectedDayData.rating}
          <span
            class="rating-badge"
            style="color: {ratingColor(selectedDayData.rating.value)}; background: {ratingBg(selectedDayData.rating.value)};"
          >
            {selectedDayData.rating.symbol} {selectedDayData.rating.chinese}
          </span>
        {/if}
        {#if selectedDayData.moon_phase}
          <span class="tui-text-muted detail-moon">
            {selectedDayData.moon_phase.emoji} {selectedDayData.moon_phase.chinese} {selectedDayData.moon_phase.english}
          </span>
        {/if}
      </div>

      <!-- Forbidden day info -->
      {#if selectedDayData.forbidden}
        <div class="forbidden-block">
          <div class="forbidden-title">
            \u2717 {selectedDayData.forbidden.chinese} ({selectedDayData.forbidden.english})
          </div>
          <div class="tui-text-muted forbidden-detail">
            Before {selectedDayData.forbidden.solar_term_chinese} {selectedDayData.forbidden.solar_term_english}
          </div>
          <div class="tui-text-muted">
            Forbidden hours: {forbiddenRange(selectedDayData.forbidden)}
          </div>
        </div>
      {/if}

      <!-- Consult promotion info -->
      {#if selectedDayData.consult?.promoted}
        <div class="consult-block">
          <span class="tui-text-muted">
            Originally: {selectedDayData.consult.original_rating?.symbol} {selectedDayData.consult.original_rating?.chinese}
          </span>
          <span class="consult-separator">&mdash;</span>
          <span style="color: var(--tui-water)">{selectedDayData.consult.reason}</span>
        </div>
      {/if}

      <!-- Chinese month -->
      {#if selectedDayData.chinese_month_name}
        <div class="chinese-month tui-text-muted">
          {selectedDayData.chinese_month_name}
        </div>
      {/if}

      <!-- Good for -->
      {#if selectedDayData.good_for.length > 0}
        <div class="activity-block">
          <span class="activity-label good-label">Good for: </span>
          <span class="tui-text activity-list">
            {selectedDayData.good_for.map(a => a.replace(/_/g, ' ')).join(', ')}
          </span>
        </div>
      {/if}

      <!-- Bad for -->
      {#if selectedDayData.bad_for.length > 0}
        <div class="activity-block">
          <span class="activity-label bad-label">Avoid: </span>
          <span class="tui-text activity-list">
            {selectedDayData.bad_for.map(a => a.replace(/_/g, ' ')).join(', ')}
          </span>
        </div>
      {/if}

      <!-- Description -->
      {#if selectedDayData.description_chinese}
        <div class="description-block tui-text-muted">
          {selectedDayData.description_chinese}
        </div>
      {/if}
      {#if selectedDayData.description_english}
        <div class="description-eng tui-text-muted">
          {selectedDayData.description_english}
        </div>
      {/if}
    </div>
  {/if}

  <!-- Keyboard hints -->
  <div class="keyboard-hints tui-text-muted">
    [h/&#91;] Prev &nbsp; [l/&#93;] Next &nbsp; [t] Today &nbsp; [Enter] Select &nbsp; [Esc] Close
  </div>
</div>

<style>
  .calendar-frame {
    border: 1px solid var(--tui-border);
  }

  .calendar-title-bar {
    padding: 0.5rem 0.75rem;
    text-align: center;
    font-weight: bold;
    font-size: 0.875rem;
    border-bottom: 1px solid var(--tui-border);
    background: var(--tui-bg-alt);
  }

  .calendar-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--tui-border);
  }

  .nav-btn {
    padding: 0.125rem 0.5rem;
    font-size: 0.875rem;
  }

  .nav-center {
    text-align: center;
  }

  .pillar-info {
    font-size: 0.75rem;
    margin-top: 0.125rem;
    line-height: 1.625;
  }

  .today-bar {
    display: flex;
    justify-content: center;
    padding: 0.375rem 0;
    border-bottom: 1px solid var(--tui-border);
  }

  .today-btn {
    font-size: 0.75rem;
    padding: 0.125rem 0.75rem;
  }

  .status-msg {
    padding: 2rem 0;
    text-align: center;
    font-size: 0.875rem;
  }

  .error-msg {
    padding: 1rem 0;
    color: var(--tui-fire);
  }

  .weekday-header {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    text-align: center;
    font-size: 0.75rem;
    font-weight: bold;
    padding: 0.25rem 0;
    border-bottom: 1px solid var(--tui-border);
    background: var(--tui-bg-alt);
  }

  .day-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
  }

  .empty-cell {
    border-bottom: 1px solid var(--tui-border-dim, var(--tui-border));
  }

  .day-cell {
    position: relative;
    text-align: center;
    padding: 0.375rem 0.125rem;
    border-bottom: 1px solid var(--tui-border-dim, var(--tui-border));
    cursor: pointer;
    min-height: 52px;
    border: none;
    border-bottom: 1px solid var(--tui-border-dim, var(--tui-border));
    font-family: inherit;
  }

  .day-number {
    font-size: 0.875rem;
    font-weight: bold;
  }

  .day-rating {
    font-size: 0.75rem;
    font-weight: bold;
    margin-top: 0.125rem;
  }

  .day-pillar {
    margin-top: 0.125rem;
    line-height: 1;
  }

  .day-pillar-chinese {
    font-size: 9px;
  }

  .day-pillar-pinyin {
    font-size: 7px;
  }

  .day-moon {
    font-size: 8px;
    line-height: 1;
    opacity: 0.6;
    margin-top: 0.125rem;
  }

  /* Detail panel */
  .detail-panel {
    padding: 0.75rem;
    border-top: 2px solid var(--tui-border-bright, var(--tui-border));
  }

  .detail-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .detail-title {
    font-weight: bold;
    font-size: 0.875rem;
  }

  .close-btn {
    font-size: 0.75rem;
    padding: 0.125rem 0.375rem;
  }

  .detail-badges {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
  }

  .rating-badge {
    font-weight: bold;
    padding: 0.125rem 0.375rem;
    font-size: 0.75rem;
  }

  .detail-moon {
    font-size: 0.75rem;
  }

  .forbidden-block {
    margin-bottom: 0.5rem;
    font-size: 0.75rem;
    border-left: 3px solid #000000;
    padding-left: 0.5rem;
  }

  .forbidden-title {
    font-weight: bold;
    color: #000000;
  }

  .forbidden-detail {
    margin-top: 0.125rem;
  }

  .consult-block {
    margin-bottom: 0.5rem;
    font-size: 0.75rem;
  }

  .consult-separator {
    margin: 0 0.25rem;
  }

  .chinese-month {
    font-size: 0.75rem;
    margin-bottom: 0.5rem;
  }

  .activity-block {
    margin-bottom: 0.375rem;
  }

  .activity-label {
    font-size: 0.75rem;
    font-weight: bold;
  }

  .good-label {
    color: var(--tui-wood);
  }

  .bad-label {
    color: var(--tui-fire);
  }

  .activity-list {
    font-size: 0.75rem;
  }

  .description-block {
    font-size: 0.75rem;
    margin-top: 0.5rem;
    line-height: 1.625;
    border-top: 1px solid var(--tui-border);
    padding-top: 0.5rem;
  }

  .description-eng {
    font-size: 0.75rem;
    margin-top: 0.25rem;
    line-height: 1.625;
  }

  .keyboard-hints {
    text-align: center;
    font-size: 10px;
    padding: 0.375rem 0.5rem;
    border-top: 1px solid var(--tui-border);
  }
</style>
