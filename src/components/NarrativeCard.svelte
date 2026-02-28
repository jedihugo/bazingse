<script lang="ts">
  import PillarTag from './PillarTag.svelte';

  interface NarrativeCardProps {
    narrative: any;
    mappings?: any;
  }

  let { narrative, mappings }: NarrativeCardProps = $props();

  // Icon mappings for different narrative types
  const ICON_MAP: Record<string, string> = {
    // Combinations
    meeting: '3M',
    triangle: '3H',
    harmony: '6H',
    half_meeting: 'HM',
    half_combo: 'HC',
    arch: 'AH',
    stem_combo: 'SC',

    // Conflicts
    clash: 'CL',
    punishment: 'XG',
    harm: 'HI',
    destruction: 'PO',
    stem_conflict: 'KE',
    cross_pillar: 'WX',

    // Balance
    excess: 'EX',
    deficiency: 'DF',

    // Wealth
    wealth_open: 'WO',
    wealth_closed: 'WC',

    // Other
    season: 'SN',
    flow: 'FL',
  };

  let polarity = $derived(narrative.polarity || 'neutral');
  let icon = $derived(ICON_MAP[narrative.icon] || narrative.type?.slice(0, 2).toUpperCase() || '??');
  let seq = $derived(narrative.seq);

  // Get element color if available
  let elementColor = $derived(
    narrative.element
      ? mappings?.elements?.[narrative.element]?.hex_color
      : null
  );

  // Polarity class for left border
  let polarityClass = $derived(
    polarity === 'positive'
      ? 'narrative-card-positive'
      : polarity === 'negative'
        ? 'narrative-card-negative'
        : 'narrative-card-neutral'
  );

  // Formula color based on polarity
  let formulaColor = $derived(
    polarity === 'positive'
      ? 'var(--tui-success)'
      : polarity === 'negative'
        ? 'var(--tui-error)'
        : 'var(--tui-text-muted)'
  );
</script>

<div class="narrative-card {polarityClass}">
  <div class="p-2">
    <!-- Row 1: Seq + Icon + Title + Element + Points -->
    <div class="flex items-center gap-2">
      <!-- Sequence number -->
      <span class="shrink-0 text-[9px] font-mono tui-text-dim w-4 text-right">
        {seq}
      </span>

      <!-- Icon Badge -->
      <div
        class="shrink-0 w-6 h-6 flex items-center justify-center rounded text-[9px] font-bold"
        style={elementColor ? `background-color: ${elementColor}; color: #fff;` : ''}
      >
        {icon}
      </div>

      <!-- Title + Element + Points -->
      <div class="flex-1 min-w-0 flex items-center gap-1.5 flex-wrap">
        <span class="text-xs font-semibold tui-text">
          {narrative.title}
        </span>

        {#if narrative.element}
          <span
            class="px-1 py-0.5 text-[9px] rounded font-medium"
            style={elementColor ? `color: ${elementColor};` : ''}
          >
            {narrative.element}
          </span>
        {/if}

        {#if narrative.points}
          <span class="text-[9px] tui-text-muted font-mono">
            {narrative.points}
          </span>
        {/if}
      </div>
    </div>

    <!-- Row 2: Formula (always visible, colored by polarity) -->
    {#if narrative.formula}
      <div class="mt-1 ml-12 text-[10px] font-mono" style="color: {formulaColor};">
        {narrative.formula}
      </div>
    {/if}

    <!-- Row 3: Match (always visible) -->
    {#if narrative.match}
      <div class="mt-0.5 ml-12 text-[10px] tui-text-muted font-mono">
        {narrative.match}
      </div>
    {/if}

    <!-- Row 4: Qi before->after changes -->
    {#if narrative.qi_changes && narrative.qi_changes.length > 0}
      <div class="mt-1 ml-12 flex flex-wrap gap-x-3 gap-y-0.5">
        {#each narrative.qi_changes as qc, idx (idx)}
          <span class="text-[10px] font-mono tui-text-muted">
            {qc.stem}: {qc.before}
            {#if qc.before !== qc.after}
              <span style="color: {qc.after > qc.before ? 'var(--tui-success)' : 'var(--tui-error)'};">
                &rarr;{qc.after}
              </span>
            {:else if qc.note}
              <span class="tui-text-dim"> ({qc.note})</span>
            {/if}
          </span>
        {/each}
      </div>
    {/if}

    <!-- Row 5: Pillar Tags -->
    {#if narrative.pillar_refs && narrative.pillar_refs.length > 0}
      <div class="flex flex-wrap gap-1 mt-1 ml-12">
        {#each narrative.pillar_refs as ref, idx (idx)}
          <PillarTag
            text={ref.abbrev}
            nodeType={ref.node_type}
            position={ref.position}
          />
        {/each}
      </div>
    {/if}

    <!-- Row 6: Math formula (scoring breakdown) -->
    {#if narrative.math_formula}
      <div class="mt-0.5 ml-12 text-[9px] tui-text-dim font-mono">
        {narrative.math_formula}
      </div>
    {/if}
  </div>
</div>
