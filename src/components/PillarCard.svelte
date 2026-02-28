<script lang="ts">
  interface QiPhaseAnalysis {
    phase_id: string;
    phase_chinese: string;
    phase_english: string;
    strength: string;
    interpretation: string;
    tandem_effects: Array<{ shen_sha: string; effect: string }>;
  }

  interface Pillar {
    label: string;
    stem: { chinese: string; element: string; color: string };
    stemName: string;
    branch: { chinese: string; animal: string; element: string; color: string };
    branchName: string;
    hiddenStems: Record<string, string>;
    hiddenQi: Record<string, number>;
    tenGod: string | null;
    isDayMaster?: boolean;
    isUnknown?: boolean;
    qiPhase?: string | null;
    qiPhaseAnalysis?: QiPhaseAnalysis;
    stemTransformations: any[];
    branchTransformations: any[];
    stemCombinations: any[];
    branchCombinations: any[];
    stemNegatives: any[];
    branchNegatives: any[];
    branchWealthStorage: any[];
    isLuckPillar?: boolean;
    isAnnualLuck?: boolean;
    timing?: { start_year: number; end_year: number; start_age: number; end_age: number };
    year?: number;
  }

  interface PillarCardProps {
    pillar: Pillar;
    type: 'stem' | 'branch';
    index: number;
    mappings: any;
    isLuck?: boolean;
    isTalisman?: boolean;
    isLocation?: boolean;
    isOverseas?: boolean;
    isBirthplace?: boolean;
    isEmpty?: boolean;
    hoveredInteractionId?: string | null;
    onHoverInteraction?: (id: string | null) => void;
  }

  let {
    pillar,
    type,
    index,
    mappings,
    isLuck = false,
    isTalisman = false,
    isLocation = false,
    isOverseas = false,
    isBirthplace = false,
    isEmpty = false,
    hoveredInteractionId = null,
    onHoverInteraction,
  }: PillarCardProps = $props();

  // Element to TUI color class mapping
  const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
    'Wood': 'tui-text-wood',
    'Fire': 'tui-text-fire',
    'Earth': 'tui-text-earth',
    'Metal': 'tui-text-metal',
    'Water': 'tui-text-water',
  };

  // Stem to element mapping (reliable local lookup)
  const STEM_TO_ELEMENT: Record<string, string> = {
    'Jia': 'Wood', 'Yi': 'Wood',
    'Bing': 'Fire', 'Ding': 'Fire',
    'Wu': 'Earth', 'Ji': 'Earth',
    'Geng': 'Metal', 'Xin': 'Metal',
    'Ren': 'Water', 'Gui': 'Water',
  };

  // Qi phase strength to TUI color style
  const STRENGTH_STYLE: Record<string, string> = {
    'peak': 'var(--tui-fire)',
    'strong': 'var(--tui-wood)',
    'growing': 'var(--tui-wood-yin)',
    'moderate': 'var(--tui-earth)',
    'declining': 'var(--tui-metal)',
    'weak': 'var(--tui-water)',
    'dead': 'var(--tui-fg-muted)',
  };

  // Get element from stem/branch element string (removes Yang/Yin prefix)
  function getBaseElement(elementStr: string): string {
    return elementStr.replace('Yang ', '').replace('Yin ', '');
  }

  let qiPhaseExpanded = $state(false);

  // Border style
  let borderStyle = $derived.by(() => {
    const base = 'border-width: 1px; border-style: solid; border-color: var(--tui-border);';
    if (isEmpty) {
      return base.replace('border-style: solid', 'border-style: dashed') + ' background: transparent;';
    }
    return base;
  });

  // Stem element and color class
  let stemElement = $derived(getBaseElement(pillar.stem?.element || 'Unknown'));
  let stemColorClass = $derived(ELEMENT_TO_TUI_CLASS[stemElement] || 'tui-text');

  // Branch element and color class
  let branchElement = $derived(getBaseElement(pillar.branch?.element || 'Unknown'));
  let branchColorClass = $derived(ELEMENT_TO_TUI_CLASS[branchElement] || 'tui-text');

  // Hidden qi entries
  let hiddenQiEntries = $derived(Object.entries(pillar.hiddenQi || {}));
  let numStems = $derived(hiddenQiEntries.length);

  // Qi Phase Analysis
  let qpa = $derived(pillar.qiPhaseAnalysis);
</script>

{#if isEmpty}
  <!-- Empty placeholder cell -->
  <div class="w-28 flex-shrink-0">
    <div
      class="tui-cell flex items-center justify-center"
      style="{borderStyle} height: {type === 'stem' ? '4rem' : '5rem'};"
    >
      <span class="tui-text-muted">{pillar.label || '---'}</span>
    </div>
  </div>
{:else if type === 'stem'}
  <!-- Stem card -->
  <div class="w-28 flex-shrink-0">
    <div class="tui-cell p-1" style="{borderStyle} height: 4rem;">
      <div class="flex flex-col items-center justify-center h-full">
        <span class="text-lg {pillar.isUnknown ? 'tui-text-muted' : stemColorClass}">
          {pillar.stem?.chinese || '?'}
        </span>
        <span class="tui-text-dim">
          {pillar.isUnknown ? '?' : (index === 1 && !isLuck ? 'DM' : (pillar.tenGod || ''))}
        </span>
      </div>
    </div>
  </div>
{:else}
  <!-- Branch card -->
  <div class="w-28 flex-shrink-0">
    <div class="tui-cell relative" style="{borderStyle} height: 5rem;">
      <!-- Main content -->
      <div class="flex flex-col items-center justify-center pt-2 pb-5">
        <span class="text-lg {pillar.isUnknown ? 'tui-text-muted' : branchColorClass}">
          {pillar.branch?.chinese || '?'}
        </span>
        {#if !pillar.isUnknown && pillar.branch?.animal && !['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(pillar.branch.animal)}
          <span class="tui-text-dim">{pillar.branch.animal}</span>
        {/if}
      </div>

      <!-- Hidden Stems - bottom row -->
      {#if hiddenQiEntries.length > 0}
        <div
          class="absolute bottom-0 left-0 right-0 flex overflow-hidden"
          style="height: 1.25rem; border-top: 1px solid var(--tui-border);"
        >
          {#each hiddenQiEntries as [stemName, qi], idx (stemName)}
            {@const stemMapping = mappings?.heavenly_stems?.[stemName] || {}}
            {@const tenGod = pillar.hiddenStems?.[stemName] || ''}
            {@const stemEl = STEM_TO_ELEMENT[stemName] || getBaseElement(stemMapping.element || 'Unknown')}
            {@const stemClrClass = ELEMENT_TO_TUI_CLASS[stemEl] || 'tui-text'}
            <div
              class="flex items-center justify-center overflow-hidden"
              style="flex: 1; {idx < numStems - 1 ? 'border-right: 1px solid var(--tui-border);' : ''} min-width: 0;"
              title="{stemMapping.chinese || stemName} {tenGod}"
            >
              <span class="text-xs {stemClrClass}">
                {stemMapping.chinese || stemName.charAt(0)}
              </span>
              <span class="text-xs tui-text-muted">{tenGod}</span>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Qi Phase Analysis - compact collapsible below branch -->
    {#if qpa}
      <div
        class="cursor-pointer select-none"
        style="border-left: 1px solid var(--tui-border); border-right: 1px solid var(--tui-border); border-bottom: 1px solid var(--tui-border); font-size: 0.65rem; line-height: 1.1; background: var(--tui-bg-alt);"
        onclick={() => qiPhaseExpanded = !qiPhaseExpanded}
        role="button"
        tabindex="0"
        onkeydown={(e) => { if (e.key === 'Enter' || e.key === ' ') qiPhaseExpanded = !qiPhaseExpanded; }}
      >
        <!-- Header: phase name + strength -->
        <div class="flex items-center justify-center gap-1 px-1 py-0.5">
          <span style="color: {STRENGTH_STYLE[qpa.strength] || 'var(--tui-fg-dim)'};">
            {qpa.phase_chinese}
          </span>
          <span class="tui-text-muted">
            {qpa.phase_english}
          </span>
        </div>

        <!-- Expanded: interpretation + tandem effects -->
        {#if qiPhaseExpanded}
          <div
            class="px-1 pb-1"
            style="border-top: 1px dashed var(--tui-border-dim, var(--tui-border));"
          >
            <div class="tui-text-dim py-0.5" style="white-space: normal;">
              {qpa.interpretation}
            </div>
            {#if qpa.tandem_effects && qpa.tandem_effects.length > 0}
              <div class="mt-0.5" style="border-top: 1px dotted var(--tui-border-dim, var(--tui-border));">
                {#each qpa.tandem_effects as te, idx (idx)}
                  <div class="py-0.5" style="white-space: normal;">
                    <span style="color: var(--tui-accent-purple);">{te.shen_sha}</span>
                    <span class="tui-text-dim"> {te.effect}</span>
                  </div>
                {/each}
              </div>
            {/if}
          </div>
        {/if}
      </div>
    {/if}
  </div>
{/if}
