<script lang="ts">
  interface DmLensDisplayProps {
    chartData: any;
  }

  let { chartData }: DmLensDisplayProps = $props();

  // Element to TUI color class
  const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
    'Wood': 'tui-text-wood',
    'Fire': 'tui-text-fire',
    'Earth': 'tui-text-earth',
    'Metal': 'tui-text-metal',
    'Water': 'tui-text-water',
  };

  // Element Chinese characters
  const ELEMENT_CHINESE: Record<string, string> = {
    'Wood': '木',
    'Fire': '火',
    'Earth': '土',
    'Metal': '金',
    'Water': '水',
  };

  // ASCII bar helper
  function generateBar(pct: number, width: number = 12): { filled: string; empty: string } {
    const filled = Math.round((pct / 100) * width);
    return {
      filled: '█'.repeat(Math.min(filled, width)),
      empty: '░'.repeat(Math.max(0, width - filled)),
    };
  }

  let lens = $derived(chartData?.dm_lens);
  let dmColorClass = $derived(ELEMENT_TO_TUI_CLASS[lens?.dmElement] || 'tui-text');
</script>

{#if lens}
  <div class="tui-frame mt-2">
    <!-- Header -->
    <div class="tui-frame-title flex items-center justify-between">
      <span>DM Lens</span>
      <span class="tui-text-muted text-xs">
        <span class={dmColorClass}>{lens.dmStem}</span>
        {' '}{ELEMENT_CHINESE[lens.dmElement]}
        {' '}{lens.dmPercent}%
        {' '}{lens.dmStrengthZh}
        {#if lens.seasonalState}
          {' '}· 令{lens.seasonalState}
        {/if}
      </span>
    </div>

    <!-- Rows -->
    <div class="p-2 space-y-0 font-mono text-xs">
      {#each lens.rows as row, i (row.role)}
        {@const colorClass = ELEMENT_TO_TUI_CLASS[row.element] || 'tui-text'}
        {@const bar = generateBar(row.percent)}

        <!-- Separator before drain section -->
        {#if i === 2}
          <div class="flex items-center gap-2 py-0.5 tui-text-muted">
            <span class="flex-1 border-t tui-border-color"></span>
            <span class="text-[10px]">
              Support {lens.supportPercent}%
            </span>
            <span class="flex-1 border-t tui-border-color"></span>
          </div>
        {/if}

        <div class="flex items-start gap-1 py-0.5">
          <!-- Role label -->
          <span class="w-[72px] shrink-0 tui-text-dim truncate">
            {row.tenGodZh} {row.roleZh.split(' ')[1]}
          </span>

          <!-- Element + bar -->
          <span class="w-5 shrink-0 {colorClass}">
            {ELEMENT_CHINESE[row.element]}
          </span>
          <span class="tui-bar shrink-0">
            <span class={colorClass}>{bar.filled}</span>
            <span class="tui-text-muted">{bar.empty}</span>
          </span>

          <!-- Percentage -->
          <span class="w-8 shrink-0 text-right tui-text-dim">
            {Math.round(row.percent)}%
          </span>
        </div>

        <!-- Narrative -->
        <div class="pl-[76px] pb-1 tui-text-muted text-[10px] leading-tight">
          {row.narrative}
        </div>
      {/each}

      <!-- Drain footer -->
      <div class="flex items-center gap-2 py-0.5 tui-text-muted">
        <span class="flex-1 border-t tui-border-color"></span>
        <span class="text-[10px]">
          Drain {lens.drainPercent}%
        </span>
        <span class="flex-1 border-t tui-border-color"></span>
      </div>

      <!-- Ratio -->
      <div class="text-center py-1 tui-text-dim text-[10px]">
        Support {lens.supportPercent}% : Drain {lens.drainPercent}% → {lens.ratio}
      </div>

      <!-- Cross-patterns -->
      {#if lens.crossPatterns && lens.crossPatterns.length > 0}
        <div class="pt-1 border-t tui-border-color space-y-0.5">
          {#each lens.crossPatterns as p (p.id)}
            <div class="flex gap-2 text-[10px]">
              <span class="tui-text-dim shrink-0">{p.nameZh}</span>
              <span class="tui-text-muted">{p.narrative}</span>
            </div>
          {/each}
        </div>
      {/if}

      <!-- Synthesis -->
      {#if lens.synthesis}
        <div class="pt-1 border-t tui-border-color text-[10px] tui-text leading-tight">
          {lens.synthesis}
        </div>
      {/if}
    </div>
  </div>
{/if}
