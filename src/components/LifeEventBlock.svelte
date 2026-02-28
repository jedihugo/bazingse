<script lang="ts">
  import { tick } from 'svelte';
  import BaZiChart from './BaZiChart.svelte';
  import ElementAnalysis from './ElementAnalysis.svelte';
  import DmLensDisplay from './DmLensDisplay.svelte';
  import WealthStorageDisplay from './WealthStorageDisplay.svelte';
  import NarrativeDisplay from './NarrativeDisplay.svelte';
  import NarrativeCard from './NarrativeCard.svelte';
  import ClientSummaryDisplay from './ClientSummaryDisplay.svelte';
  import { updateLifeEvent, type LifeEvent } from '$lib/api';

  interface LifeEventBlockProps {
    profileId: string;
    event: LifeEvent;
    chartData: any;
    isLoading?: boolean;
    error?: string | null;
    isNatal?: boolean;
    onDelete?: () => void;
    onEventUpdate?: (event: LifeEvent) => void;
  }

  let {
    profileId,
    event,
    chartData,
    isLoading = false,
    error = null,
    isNatal = false,
    onDelete,
    onEventUpdate,
  }: LifeEventBlockProps = $props();

  let isEditingNotes = $state(false);
  let notes = $state(event.notes || '');
  let isSaving = $state(false);
  let isTogglingAbroad = $state(false);
  let showDeleteConfirm = $state(false);
  let textareaEl: HTMLTextAreaElement;

  // Sync notes state with prop
  $effect(() => {
    notes = event.notes || '';
  });

  // Auto-resize textarea
  $effect(() => {
    if (isEditingNotes && textareaEl) {
      textareaEl.focus();
      textareaEl.style.height = 'auto';
      textareaEl.style.height = textareaEl.scrollHeight + 'px';
    }
  });

  function formatDateLabel(ev: LifeEvent): string {
    const parts = [ev.year.toString()];
    if (ev.month) {
      const monthName = new Date(2000, ev.month - 1, 1).toLocaleString('default', { month: 'short' });
      parts.push(monthName);
    }
    if (ev.day) {
      parts.push(ev.day.toString());
    }
    return parts.join(' - ');
  }

  async function handleSaveNotes() {
    if (isSaving) return;
    const trimmedNotes = notes.trim();

    if (trimmedNotes === (event.notes || '')) {
      isEditingNotes = false;
      return;
    }

    try {
      isSaving = true;
      const updated = await updateLifeEvent(profileId, event.id, {
        notes: trimmedNotes || null,
      });
      onEventUpdate?.(updated);
    } catch (err) {
      console.error('Failed to save notes:', err);
      notes = event.notes || '';
    } finally {
      isSaving = false;
      isEditingNotes = false;
    }
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Escape') {
      notes = event.notes || '';
      isEditingNotes = false;
    }
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      handleSaveNotes();
    }
  }

  function handleDelete() {
    showDeleteConfirm = false;
    onDelete?.();
  }

  async function handleToggleAbroad() {
    if (isTogglingAbroad) return;
    try {
      isTogglingAbroad = true;
      const newValue = !event.is_abroad;
      const updated = await updateLifeEvent(profileId, event.id, {
        is_abroad: newValue,
      });
      onEventUpdate?.(updated);
    } catch (err) {
      console.error('Failed to toggle abroad:', err);
    } finally {
      isTogglingAbroad = false;
    }
  }

  // Spiritual sensitivity helpers
  let ss = $derived(chartData?.spiritual_sensitivity);
  let ssScore = $derived(ss?.score ?? 0);
  let ssFilled = $derived(Math.round(ssScore / 10));
  let ssEmpty = $derived(10 - ssFilled);
  let ssBar = $derived('\u2588'.repeat(ssFilled) + '\u2591'.repeat(ssEmpty));
  let ssColor = $derived.by(() => {
    if (ssScore <= 20) return 'var(--tui-wood)';
    if (ssScore <= 40) return 'var(--tui-warning)';
    if (ssScore <= 60) return 'var(--tui-accent-orange)';
    if (ssScore <= 80) return 'var(--tui-fire)';
    return 'var(--tui-accent-purple)';
  });
  let ssIndicators = $derived<Array<{ name: string; name_zh: string; weight: number; reason: string }>>(ss?.indicators || []);
</script>

<div class="tui-frame overflow-hidden" style={isNatal ? 'border-color: var(--tui-accent-purple)' : ''}>
  <!-- Header -->
  <div
    class="px-4 py-2"
    style={isNatal
      ? 'background: color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))'
      : 'background: var(--tui-bg-alt)'}
  >
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2 flex-wrap">
        <span
          class="font-semibold"
          style={isNatal ? 'color: var(--tui-accent-purple)' : 'color: var(--tui-fg-dim)'}
        >
          {isNatal ? 'Birth Chart' : formatDateLabel(event)}
        </span>
        {#if isNatal}
          <span
            class="text-xs px-2 py-0.5"
            style="background: var(--tui-accent-purple); color: var(--tui-bg)"
          >Birth</span>
        {/if}
        {#if chartData?.school && chartData.school !== 'classic'}
          <span
            class="text-xs px-2 py-0.5"
            style="background: var(--tui-water); color: var(--tui-bg)"
          >{chartData.school}</span>
        {/if}
        {#if chartData?.hs_10yl?.misc}
          <span class="text-xs tui-text-muted">
            10Y: {chartData.hs_10yl.misc.start_date?.split('-')[0]} - {chartData.hs_10yl.misc.end_date?.split('-')[0]}
          </span>
        {/if}
      </div>

      <!-- Delete button -->
      {#if !isNatal && onDelete}
        <div class="relative">
          {#if showDeleteConfirm}
            <div class="flex items-center gap-2">
              <span class="text-xs tui-text-muted">Delete?</span>
              <button
                onclick={handleDelete}
                class="text-xs px-2 py-1"
                style="background: var(--tui-error); color: var(--tui-bg)"
              >Yes</button>
              <button
                onclick={() => showDeleteConfirm = false}
                class="tui-btn text-xs px-2 py-1"
              >No</button>
            </div>
          {:else}
            <button
              onclick={() => showDeleteConfirm = true}
              class="tui-text-muted p-1"
              title="Delete"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          {/if}
        </div>
      {/if}
    </div>

    <!-- Location line with abroad toggle -->
    {#if !isNatal && event.location}
      <div class="text-xs mt-1 flex items-center gap-2 flex-wrap">
        <span class="tui-text-dim">{event.location}</span>
        <button
          onclick={handleToggleAbroad}
          disabled={isTogglingAbroad}
          class="inline-flex items-center gap-1 px-1.5 py-0.5 transition-colors"
          style="color: {event.is_abroad ? 'var(--tui-water)' : 'var(--tui-fg-muted)'}; background: {event.is_abroad ? 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' : 'transparent'}; border: 1px solid {event.is_abroad ? 'var(--tui-water)' : 'var(--tui-border)'}; opacity: {isTogglingAbroad ? 0.5 : 1}"
          title="Toggle abroad status for location-based analysis"
        >
          <span style="font-family: monospace">{event.is_abroad ? '[x]' : '[_]'}</span>
          <span>Abroad</span>
        </button>
      </div>
    {/if}
  </div>

  <!-- Content -->
  <div class="p-2">
    {#if isLoading}
      <div class="py-8 text-center tui-text-muted">
        <div class="inline-block animate-spin h-5 w-5 border-2 tui-border mr-2" style="border-top-color: var(--tui-water)"></div>
        Loading chart...
      </div>
    {:else if error}
      <div class="py-4 px-3 text-sm" style="background: color-mix(in srgb, var(--tui-error) 10%, var(--tui-bg)); color: var(--tui-error)">{error}</div>
    {:else if chartData}
      <!-- Row 1: Natal only -->
      <BaZiChart
        {chartData}
        showNatal={true}
        showLuck={false}
        showTalisman={false}
        showLocation={false}
      />

      <!-- Row 2: Aligned comparison -->
      {#if !isNatal && chartData?.analysis_info?.year}
        <div class="mt-1">
          <BaZiChart
            {chartData}
            showNatal={false}
            showLuck={true}
            showTalisman={false}
            showLocation={false}
          />
        </div>
      {/if}

      <!-- Element Analysis -->
      <ElementAnalysis {chartData} />

      <!-- DM Lens -->
      <DmLensDisplay {chartData} />

      <!-- Wealth Storage Analysis -->
      <WealthStorageDisplay {chartData} />

      <!-- Spiritual Sensitivity (natal only) -->
      {#if isNatal && ss}
        <div class="tui-frame mt-2">
          <div class="tui-frame-title flex items-center justify-between">
            <span>Spiritual Sensitivity</span>
            <span
              class="text-xs px-1.5 py-0.5"
              style="background: {ssColor}; color: var(--tui-bg)"
            >
              {ss.label_zh || ss.level}
            </span>
          </div>

          <div class="p-2 font-mono space-y-2">
            <!-- Score bar -->
            <div class="flex items-center gap-2 text-sm">
              <span class="tui-text-muted w-10 text-right">{ssScore}</span>
              <span style="color: {ssColor}; letter-spacing: 1px">{ssBar}</span>
              <span class="tui-text-muted">100</span>
            </div>

            <!-- Level label -->
            <div class="text-xs tui-text-dim">
              {ss.label_zh && ss.label_en
                ? `${ss.label_zh} / ${ss.label_en}`
                : ss.label_en || ss.label_zh || ss.level}
            </div>

            <!-- Description -->
            {#if ss.description_en || ss.description_zh}
              <div class="text-xs tui-text-dim" style="line-height: 1.5">
                {ss.description_zh || ss.description_en}
              </div>
            {/if}

            <!-- Indicators -->
            {#if ssIndicators.length > 0}
              <details class="mt-1">
                <summary class="text-xs tui-text-muted cursor-pointer py-1">
                  Indicators ({ssIndicators.length})
                </summary>
                <div class="space-y-1 mt-1">
                  {#each ssIndicators as ind, i (i)}
                    <div class="text-xs flex gap-2 flex-wrap">
                      <span
                        class="px-1"
                        style="color: {ssColor}; border: 1px solid {ssColor}"
                      >
                        +{ind.weight}
                      </span>
                      <span class="tui-text-dim">
                        {ind.name_zh} {ind.name}
                      </span>
                      {#if ind.reason}
                        <span class="tui-text-muted">{ind.reason}</span>
                      {/if}
                    </div>
                  {/each}
                </div>
              </details>
            {/if}

            <!-- Guidance -->
            {#if ss.guidance_en || ss.guidance_zh}
              <details class="mt-1">
                <summary class="text-xs tui-text-muted cursor-pointer py-1">
                  Guidance
                </summary>
                <div class="text-xs tui-text-dim mt-1" style="line-height: 1.5">
                  {ss.guidance_zh || ss.guidance_en}
                </div>
              </details>
            {/if}
          </div>
        </div>
      {/if}

      <!-- Interaction-Based Narratives -->
      {#if isNatal && chartData?.narrative_analysis}
        <details class="mt-3">
          <summary class="text-xs font-semibold tui-text-dim cursor-pointer p-2 tui-bg-alt tui-border">
            Interaction Analysis
          </summary>
          <NarrativeDisplay {chartData} />
        </details>
      {/if}

      <!-- Shen Sha Stars -->
      {#if isNatal && chartData?.narrative_analysis?.shen_sha_cards?.length > 0}
        <details class="mt-3">
          <summary class="text-xs font-semibold tui-text-dim cursor-pointer p-2 tui-bg-alt tui-border">
            Shen Sha Stars
          </summary>
          <div class="narrative-panel">
            <div class="narrative-panel-inner">
              <div class="space-y-1.5">
                {#each chartData.narrative_analysis.shen_sha_cards as entry (entry.seq)}
                  <NarrativeCard
                    narrative={entry}
                    mappings={chartData?.mappings}
                  />
                {/each}
              </div>
              <div class="mt-2 text-[9px] tui-text-dim font-mono text-right">
                {chartData.narrative_analysis.shen_sha_cards.length} stars
              </div>
            </div>
          </div>
        </details>
      {/if}

      <!-- Client Summary -->
      {#if chartData?.client_summary}
        <ClientSummaryDisplay {chartData} />
      {/if}
    {:else}
      <div class="py-8 text-center tui-text-muted">No data</div>
    {/if}
  </div>

  <!-- Notes section (non-natal only) -->
  {#if !isNatal && !isLoading && !error}
    <div class="border-t tui-border-color px-4 py-3">
      {#if isEditingNotes}
        <div class="relative">
          <textarea
            bind:this={textareaEl}
            bind:value={notes}
            onblur={handleSaveNotes}
            onkeydown={handleKeyDown}
            placeholder="Add notes..."
            class="tui-input w-full text-sm px-3 py-2 resize-none min-h-[60px]"
            maxlength={10000}
          ></textarea>
          <div class="flex justify-between items-center mt-1 text-xs tui-text-muted">
            <span>Esc to cancel</span>
            {#if isSaving}
              <span>Saving...</span>
            {/if}
          </div>
        </div>
      {:else}
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div
          onclick={() => isEditingNotes = true}
          class="text-sm cursor-pointer px-2 py-1 -mx-2 {notes ? 'tui-text-dim' : 'tui-text-muted italic'}"
          title="Click to add notes"
        >
          {notes || 'Click to add notes'}
        </div>
      {/if}
    </div>
  {/if}
</div>
