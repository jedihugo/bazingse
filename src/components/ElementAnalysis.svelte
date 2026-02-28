<script lang="ts">
  interface ElementAnalysisProps {
    chartData: any;
  }

  let { chartData }: ElementAnalysisProps = $props();

  // Five elements in traditional order
  const FIVE_ELEMENTS = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'];

  // Element to TUI color class (yang - brighter)
  const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
    'Wood': 'tui-text-wood',
    'Fire': 'tui-text-fire',
    'Earth': 'tui-text-earth',
    'Metal': 'tui-text-metal',
    'Water': 'tui-text-water',
  };

  // Element to TUI color class for yin (slightly dimmer/different shade)
  const ELEMENT_TO_TUI_CLASS_YIN: Record<string, string> = {
    'Wood': 'tui-text-wood-yin',
    'Fire': 'tui-text-fire-yin',
    'Earth': 'tui-text-earth-yin',
    'Metal': 'tui-text-metal-yin',
    'Water': 'tui-text-water-yin',
  };

  // Stem to element and polarity mapping
  const STEM_INFO: Record<string, { element: string; polarity: 'yang' | 'yin' }> = {
    'Jia': { element: 'Wood', polarity: 'yang' },
    'Yi': { element: 'Wood', polarity: 'yin' },
    'Bing': { element: 'Fire', polarity: 'yang' },
    'Ding': { element: 'Fire', polarity: 'yin' },
    'Wu': { element: 'Earth', polarity: 'yang' },
    'Ji': { element: 'Earth', polarity: 'yin' },
    'Geng': { element: 'Metal', polarity: 'yang' },
    'Xin': { element: 'Metal', polarity: 'yin' },
    'Ren': { element: 'Water', polarity: 'yang' },
    'Gui': { element: 'Water', polarity: 'yin' },
  };

  // Element Chinese characters
  const ELEMENT_CHINESE: Record<string, string> = {
    'Wood': '\u6728',
    'Fire': '\u706B',
    'Earth': '\u571F',
    'Metal': '\u91D1',
    'Water': '\u6C34',
  };

  // Daymaster relationship to element
  const ELEMENT_RELATIONSHIPS: Record<string, Record<string, string>> = {
    'Wood': { 'Wood': 'Self', 'Fire': 'Output', 'Earth': 'Wealth', 'Metal': 'Officer', 'Water': 'Resource' },
    'Fire': { 'Wood': 'Resource', 'Fire': 'Self', 'Earth': 'Output', 'Metal': 'Wealth', 'Water': 'Officer' },
    'Earth': { 'Wood': 'Officer', 'Fire': 'Resource', 'Earth': 'Self', 'Metal': 'Output', 'Water': 'Wealth' },
    'Metal': { 'Wood': 'Wealth', 'Fire': 'Officer', 'Earth': 'Resource', 'Metal': 'Self', 'Water': 'Output' },
    'Water': { 'Wood': 'Output', 'Fire': 'Wealth', 'Earth': 'Officer', 'Metal': 'Resource', 'Water': 'Self' },
  };

  // Convert stem-based scores to element-based scores with yang/yin breakdown
  function aggregateByElement(stemScores: Record<string, number>): Record<string, { total: number; yang: number; yin: number }> {
    const elementScores: Record<string, { total: number; yang: number; yin: number }> = {
      Wood: { total: 0, yang: 0, yin: 0 },
      Fire: { total: 0, yang: 0, yin: 0 },
      Earth: { total: 0, yang: 0, yin: 0 },
      Metal: { total: 0, yang: 0, yin: 0 },
      Water: { total: 0, yang: 0, yin: 0 },
    };

    for (const [stem, score] of Object.entries(stemScores)) {
      const info = STEM_INFO[stem];
      if (info) {
        elementScores[info.element].total += score;
        elementScores[info.element][info.polarity] += score;
      }
    }

    return elementScores;
  }

  // Generate ASCII progress bar with yang/yin breakdown
  function generateAsciiBarParts(percentage: number, yangRatio: number, width: number = 16): { yang: string; yin: string; empty: string } {
    const totalFilled = Math.round((percentage / 100) * width);
    const yangFilled = Math.round(totalFilled * yangRatio);
    const yinFilled = totalFilled - yangFilled;
    const empty = width - totalFilled;

    return {
      yang: '\u2588'.repeat(yangFilled),
      yin: '\u2588'.repeat(yinFilled),
      empty: '\u2591'.repeat(empty),
    };
  }

  // Get daymaster element
  let daymasterAnalysis = $derived(chartData?.daymaster_analysis);
  let daymaster = $derived(daymasterAnalysis?.daymaster || '');
  let daymasterElement = $derived.by(() => {
    const dm = daymaster;
    if (dm.includes('Wood')) return 'Wood';
    if (dm.includes('Fire')) return 'Fire';
    if (dm.includes('Earth')) return 'Earth';
    if (dm.includes('Metal')) return 'Metal';
    if (dm.includes('Water')) return 'Water';
    return '';
  });

  // Get element scores for Natal and Post comparison
  let elementData = $derived.by(() => {
    const rawNatalScores = chartData?.natal_element_score || chartData?.base_element_score || {};
    const rawPostScores = chartData?.post_element_score || chartData?.advanced_post_elements || rawNatalScores;

    const natalScores = aggregateByElement(rawNatalScores);
    const postScores = aggregateByElement(rawPostScores);

    const natalTotal = FIVE_ELEMENTS.reduce((sum, el) => sum + (natalScores[el]?.total || 0), 0);
    const postTotal = FIVE_ELEMENTS.reduce((sum, el) => sum + (postScores[el]?.total || 0), 0);

    const elements = FIVE_ELEMENTS.map(element => {
      const natalData = natalScores[element] || { total: 0, yang: 0, yin: 0 };
      const postData = postScores[element] || { total: 0, yang: 0, yin: 0 };

      const natalPct = natalTotal > 0 ? (natalData.total / natalTotal) * 100 : 0;
      const postPct = postTotal > 0 ? (postData.total / postTotal) * 100 : 0;
      const change = postPct - natalPct;
      const relationship = daymasterElement ? ELEMENT_RELATIONSHIPS[daymasterElement]?.[element] || '' : '';

      const useData = postTotal !== natalTotal ? postData : natalData;
      const yangRatio = useData.total > 0 ? useData.yang / useData.total : 0.5;
      const yinRatio = useData.total > 0 ? useData.yin / useData.total : 0.5;

      return {
        name: element,
        natalPct,
        postPct,
        change,
        relationship,
        yangRatio,
        yinRatio,
      };
    });

    return { elements, natalTotal, postTotal, hasPost: postTotal !== natalTotal };
  });

  let daymasterColorClass = $derived(ELEMENT_TO_TUI_CLASS[daymasterElement] || 'tui-text');
</script>

{#if daymasterAnalysis}
  <div class="tui-frame mt-2">
    <!-- Header -->
    <div class="tui-frame-title flex items-center justify-between">
      <span>Wu Xing \u4E94\u884C</span>
      <span></span>
    </div>

    <!-- Element Bars -->
    <div class="p-2 space-y-1 font-mono">
      {#each elementData.elements as element (element.name)}
        {@const colorClass = ELEMENT_TO_TUI_CLASS[element.name] || 'tui-text'}
        {@const hasChange = Math.abs(element.change) > 0.5}
        {@const displayPct = elementData.hasPost ? element.postPct : element.natalPct}
        {@const isDM = element.name === daymasterElement}
        {@const parts = generateAsciiBarParts(displayPct, element.yangRatio, 16)}
        {@const yinClass = ELEMENT_TO_TUI_CLASS_YIN[element.name] || colorClass}
        <div class="flex items-center gap-2 {isDM ? 'font-bold' : ''}">
          <!-- Element Chinese + Name -->
          <span class="w-12 {colorClass}">
            {ELEMENT_CHINESE[element.name]} {isDM ? 'DM' : element.name.substring(0, 2)}
          </span>

          <!-- ASCII Bar with Yang/Yin colors -->
          <span class="tui-bar">
            <span class={colorClass}>{parts.yang}</span>
            <span class={yinClass}>{parts.yin}</span>
            <span class="tui-text-muted">{parts.empty}</span>
          </span>

          <!-- Percentage -->
          <span class="w-8 text-right tui-text-dim">
            {Math.round(displayPct)}%
          </span>

          <!-- Change indicator (if post data exists) -->
          {#if elementData.hasPost && hasChange}
            <span class={element.change > 0 ? 'tui-text-wood' : 'tui-text-fire'}>
              {element.change > 0 ? '\u25B2' : '\u25BC'}{Math.abs(Math.round(element.change))}
            </span>
          {/if}

          <!-- Relationship -->
          <span class="w-16 text-right tui-text-muted">
            {element.relationship}
          </span>
        </div>
      {/each}
    </div>

    <!-- Footer note -->
    <div class="border-t tui-border-color px-2 py-1 tui-text-muted text-center">
      {elementData.hasPost ? 'Post-interaction' : 'Natal'}
    </div>
  </div>
{/if}
