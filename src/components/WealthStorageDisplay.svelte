<script lang="ts">
  interface WealthStorageDisplayProps {
    chartData: any;
  }

  let { chartData }: WealthStorageDisplayProps = $props();

  const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
    'Wood': 'tui-text-wood',
    'Fire': 'tui-text-fire',
    'Earth': 'tui-text-earth',
    'Metal': 'tui-text-metal',
    'Water': 'tui-text-water',
  };

  const ACTIVATION_STYLE: Record<string, { label: string; color: string }> = {
    'maximum': { label: 'MAX', color: 'var(--tui-wood)' },
    'activated': { label: 'ACT', color: 'var(--tui-water)' },
    'latent': { label: 'LAT', color: 'var(--tui-fg-muted)' },
  };

  let ws = $derived(chartData?.wealth_storage_analysis);
  let storages = $derived((ws?.storages || []) as any[]);
  let wealthColor = $derived(ELEMENT_TO_TUI_CLASS[ws?.wealth_element] || 'tui-text');
  let dmColor = $derived(ELEMENT_TO_TUI_CLASS[ws?.daymaster_element] || 'tui-text');
</script>

{#if ws && ws.wealth_storage_branch}
  <div class="tui-frame mt-2">
    <div class="tui-frame-title flex items-center justify-between">
      <span>Wealth Storage 財庫</span>
      <span>
        <span class={dmColor}>{ws.daymaster_stem}</span>
        {' → '}
        <span class={wealthColor}>{ws.wealth_element}</span>
        {' → '}
        <span class="tui-text-dim">{ws.wealth_storage_branch}</span>
      </span>
    </div>

    <div class="p-2 font-mono space-y-1">
      {#if storages.length === 0}
        <div class="tui-text-muted text-center py-1">
          No {ws.wealth_storage_branch} branch in chart — no storage
        </div>
      {:else}
        {#each storages as s, i (i)}
          {@const act = ACTIVATION_STYLE[s.activation_level] || ACTIVATION_STYLE['latent']}
          <div class="flex items-center gap-2 flex-wrap">
            <!-- Position -->
            <span class="w-12 tui-text-dim text-right">{s.position}</span>

            <!-- Pillar -->
            <span class={wealthColor}>{s.pillar_chinese || s.pillar}</span>

            <!-- Large badge -->
            {#if s.is_large}
              <span
                class="text-xs px-1"
                style="background: var(--tui-earth); color: var(--tui-bg);"
              >LARGE</span>
            {/if}

            <!-- Activation level -->
            <span
              class="text-xs px-1"
              style="color: {act.color}; border: 1px solid {act.color};"
            >{act.label}</span>

            <!-- Filler indicator -->
            <span class={s.is_filled ? 'tui-text-wood' : 'tui-text-muted'}>
              {s.is_filled ? '填' : '—'}
            </span>

            <!-- Opener indicator -->
            <span class={s.is_opened ? 'tui-text-fire' : 'tui-text-muted'}>
              {s.is_opened ? '冲' : '—'}
            </span>

            <!-- Detail on where filler/opener came from -->
            {#if (s.filler_positions?.length > 0 || s.opener_positions?.length > 0)}
              <span class="tui-text-muted text-xs">
                {#if s.filler_positions?.length > 0}fill:{s.filler_positions.join(',')}{/if}
                {#if s.filler_positions?.length > 0 && s.opener_positions?.length > 0}{' '}{/if}
                {#if s.opener_positions?.length > 0}open:{s.opener_positions.join(',')}{/if}
              </span>
            {/if}
          </div>
        {/each}
      {/if}
    </div>

    <!-- Summary footer -->
    <div class="border-t tui-border-color px-2 py-1 tui-text-muted text-xs">
      {ws.summary}
    </div>
  </div>
{/if}
