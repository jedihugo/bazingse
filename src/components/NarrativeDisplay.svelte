<script lang="ts">
  import NarrativeCard from './NarrativeCard.svelte';

  interface NarrativeDisplayProps {
    chartData: any;
  }

  let { chartData }: NarrativeDisplayProps = $props();

  let narrativeAnalysis = $derived(chartData?.narrative_analysis);
  let chronological = $derived(narrativeAnalysis?.all_chronological);
  let hasData = $derived(narrativeAnalysis && chronological && chronological.length > 0);
</script>

{#if hasData}
  <div class="narrative-panel">
    <div class="narrative-panel-inner">
      <div class="space-y-1.5">
        {#each chronological as entry (entry.seq)}
          <NarrativeCard
            narrative={entry}
            mappings={chartData?.mappings}
          />
        {/each}
      </div>
      <div class="mt-2 text-[9px] tui-text-dim font-mono text-right">
        {chronological.length} interactions
      </div>
    </div>
  </div>
{/if}
