<script lang="ts">
  import PillarCard from './PillarCard.svelte';

  interface BaZiChartProps {
    chartData: any;
    showNatal?: boolean;
    show10YrLuck?: boolean;
    showLuck?: boolean;
    showTalisman?: boolean;
    showLocation?: boolean;
  }

  let {
    chartData,
    showNatal = true,
    show10YrLuck = false,
    showLuck = true,
    showTalisman = true,
    showLocation = true,
  }: BaZiChartProps = $props();

  // Branch to element mapping
  const BRANCH_TO_ELEMENT: Record<string, string> = {
    'Zi': 'Water', 'Chou': 'Earth', 'Yin': 'Wood', 'Mao': 'Wood',
    'Chen': 'Earth', 'Si': 'Fire', 'Wu': 'Fire', 'Wei': 'Earth',
    'Shen': 'Metal', 'You': 'Metal', 'Xu': 'Earth', 'Hai': 'Water',
  };

  // Stem to element mapping (with yin/yang polarity)
  const STEM_TO_ELEMENT: Record<string, { element: string; polarity: 'yang' | 'yin' }> = {
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

  // Element to Chinese character
  const ELEMENT_CHAR: Record<string, string> = {
    'Wood': '\u6728', 'Fire': '\u706B', 'Earth': '\u571F', 'Metal': '\u91D1', 'Water': '\u6C34',
  };

  let mappings = $derived(chartData?.mappings || {});
  let dayMasterStem = $derived(chartData?.hs_d?.id || 'Yi');
  let hoveredInteractionId = $state<string | null>(null);

  // Build pillar data from node
  function buildPillar(hsKey: string, ebKey: string, label: string, isDayMaster = false) {
    const hsNode = chartData?.[hsKey];
    const ebNode = chartData?.[ebKey];

    if (!hsNode && !ebNode) return null;

    const stemId = hsNode?.id;
    const branchId = ebNode?.id;

    // Get stem data from API mappings
    const stemMapping = mappings.heavenly_stems?.[stemId] || {};
    const stemInfo = STEM_TO_ELEMENT[stemId];
    const stemElement = stemInfo?.element || 'Unknown';

    const stem = {
      chinese: stemMapping.chinese || stemId || '?',
      element: stemElement,
      color: stemMapping.hex_color,
    };

    // Check if branch is pure element transformation
    const isPureElement = ['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(branchId);

    let branch;
    if (isPureElement) {
      branch = {
        chinese: ELEMENT_CHAR[branchId] || branchId,
        animal: branchId,
        element: branchId,
        color: mappings.elements?.[branchId]?.hex_color,
      };
    } else {
      const branchMapping = mappings.earthly_branches?.[branchId] || {};
      const branchElement = BRANCH_TO_ELEMENT[branchId] || 'Unknown';
      branch = {
        chinese: branchMapping.chinese || branchId || '?',
        animal: branchMapping.animal || '?',
        element: branchElement,
        color: branchMapping.hex_color,
      };
    }

    // Get hidden stems (qi) data - use base_qi only
    const baseQi = ebNode?.base_qi && Object.keys(ebNode.base_qi).length > 0
      ? ebNode.base_qi : null;
    const hiddenQi = baseQi || {};

    // Map hidden stems to Ten Gods
    const hiddenStems: Record<string, string> = {};
    if (hiddenQi && mappings.ten_gods) {
      for (const stemName of Object.keys(hiddenQi)) {
        const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemName];
        hiddenStems[stemName] = tenGodData?.abbreviation || tenGodData?.id || '';
      }
    }

    // Get Ten God for stem
    let tenGod = null;
    if (isDayMaster) {
      tenGod = 'DM';
    } else if (stemId && mappings.ten_gods) {
      const tenGodData = mappings.ten_gods?.[dayMasterStem]?.[stemId];
      tenGod = tenGodData?.abbreviation || tenGodData?.id || null;
    }

    // Get badges
    const stemBadges = hsNode?.badges || [];
    const branchBadges = ebNode?.badges || [];

    return {
      label,
      stem,
      stemName: stemId,
      branch,
      branchName: branchId,
      stemKey: hsKey,
      branchKey: ebKey,
      hiddenStems,
      hiddenQi,
      tenGod,
      isDayMaster,
      isUnknown: !hsNode && !ebNode,
      qiPhase: hsNode?.qi_phase || ebNode?.qi_phase || null,
      qiPhaseAnalysis: undefined as any,
      stemTransformations: stemBadges.filter((b: any) => b.type === 'transformation'),
      branchTransformations: branchBadges.filter((b: any) => b.type === 'transformation'),
      stemCombinations: stemBadges.filter((b: any) => b.type === 'combination'),
      branchCombinations: branchBadges.filter((b: any) => b.type === 'combination'),
      stemNegatives: stemBadges.filter((b: any) =>
        ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)),
      branchNegatives: branchBadges.filter((b: any) =>
        ['clash', 'harm', 'punishment', 'destruction', 'stem_conflict'].includes(b.type)),
      branchWealthStorage: branchBadges.filter((b: any) => b.type === 'wealth_storage'),
    };
  }

  // Empty placeholder pillar for alignment
  function createEmptyPillar(label: string) {
    return {
      label,
      stem: { chinese: '', element: 'Unknown', color: '' },
      stemName: '',
      branch: { chinese: '', animal: '', element: 'Unknown', color: '' },
      branchName: '',
      hiddenStems: {},
      hiddenQi: {},
      tenGod: null,
      isDayMaster: false,
      isUnknown: true,
      isEmpty: true,
      stemTransformations: [],
      branchTransformations: [],
      stemCombinations: [],
      branchCombinations: [],
      stemNegatives: [],
      branchNegatives: [],
      branchWealthStorage: [],
    };
  }

  // Build natal pillars
  let natalPillars = $derived.by(() => {
    const hour = buildPillar('hs_h', 'eb_h', 'Hour \u6642') || {
      label: 'Hour \u6642',
      stem: { chinese: '?', element: 'Unknown', color: '' },
      stemName: '?',
      branch: { chinese: '?', animal: '?', element: 'Unknown', color: '' },
      branchName: '?',
      hiddenStems: {},
      hiddenQi: {},
      tenGod: null,
      isDayMaster: false,
      isUnknown: true,
      qiPhaseAnalysis: undefined as any,
      stemTransformations: [],
      branchTransformations: [],
      stemCombinations: [],
      branchCombinations: [],
      stemNegatives: [],
      branchNegatives: [],
      branchWealthStorage: [],
    };
    const day = buildPillar('hs_d', 'eb_d', 'Day \u65E5', true);
    const month = buildPillar('hs_m', 'eb_m', 'Month \u6708');
    const year = buildPillar('hs_y', 'eb_y', 'Year \u5E74');

    // Attach qi phase analysis to natal pillars
    const qiPhaseData = chartData?.qi_phase_analysis?.pillars;
    const pillarPositionMap: Record<number, string> = { 0: 'hour', 1: 'day', 2: 'month', 3: 'year' };
    const result = [hour, day, month, year];
    if (qiPhaseData) {
      result.forEach((pillar, idx) => {
        if (pillar) {
          const posKey = pillarPositionMap[idx];
          (pillar as any).qiPhaseAnalysis = qiPhaseData[posKey] || undefined;
        }
      });
    }

    return result.filter(Boolean) as any[];
  });

  // Build aligned comparison row: Hourly | Daily | Monthly | Annual | 10-Yr Luck
  let alignedLuckPillars = $derived.by(() => {
    // Hourly luck (aligns with Hour)
    let hourlyPillar: any = createEmptyPillar('Hourly \u6642\u904B');
    if (chartData?.analysis_info?.has_hourly && chartData?.hs_hl && chartData?.eb_hl) {
      const pillar = buildPillar('hs_hl', 'eb_hl', 'Hourly \u6642\u904B') as any;
      if (pillar) {
        pillar.isHourlyLuck = true;
        hourlyPillar = pillar;
      }
    }

    // Daily luck (aligns with Day)
    let dailyPillar: any = createEmptyPillar('Daily \u65E5\u904B');
    if (chartData?.analysis_info?.has_daily && chartData?.hs_dl && chartData?.eb_dl) {
      const pillar = buildPillar('hs_dl', 'eb_dl', 'Daily \u65E5\u904B') as any;
      if (pillar) {
        pillar.isDailyLuck = true;
        dailyPillar = pillar;
      }
    }

    // Monthly luck (aligns with Month)
    let monthlyPillar: any = createEmptyPillar('Monthly \u6708\u904B');
    if (chartData?.analysis_info?.has_monthly && chartData?.hs_ml && chartData?.eb_ml) {
      const pillar = buildPillar('hs_ml', 'eb_ml', 'Monthly \u6708\u904B') as any;
      if (pillar) {
        pillar.isMonthlyLuck = true;
        monthlyPillar = pillar;
      }
    }

    // Annual luck (aligns with Year)
    let annualPillar: any = createEmptyPillar('Annual \u5E74\u904B');
    if (chartData?.analysis_info?.year && chartData?.hs_yl && chartData?.eb_yl) {
      const pillar = buildPillar('hs_yl', 'eb_yl', 'Annual \u5E74\u904B') as any;
      if (pillar) {
        pillar.isAnnualLuck = true;
        pillar.year = chartData.analysis_info.year;
        annualPillar = pillar;
      }
    }

    // 10-Yr luck (rightmost column)
    let tenYrPillar: any = createEmptyPillar('10-Yr \u5927\u904B');
    if (chartData?.analysis_info?.has_luck_pillar && chartData?.hs_10yl && chartData?.eb_10yl) {
      const pillar = buildPillar('hs_10yl', 'eb_10yl', '10-Yr \u5927\u904B') as any;
      if (pillar) {
        pillar.isLuckPillar = true;
        pillar.is10YrLuck = true;
        const misc = chartData.hs_10yl?.misc || chartData.eb_10yl?.misc;
        if (misc) {
          pillar.timing = {
            start_year: parseInt(misc.start_date?.split('-')[0] || '0'),
            end_year: parseInt(misc.end_date?.split('-')[0] || '0'),
            start_age: misc.start_age || 0,
            end_age: misc.end_age || 10,
          };
        }
        tenYrPillar = pillar;
      }
    }

    return [hourlyPillar, dailyPillar, monthlyPillar, annualPillar, tenYrPillar];
  });

  // Build talisman pillars
  let talismanPillars = $derived.by(() => {
    const pillars: any[] = [];

    if (chartData?.hs_ty || chartData?.eb_ty) {
      const pillar = buildPillar('hs_ty', 'eb_ty', 'T Year') as any;
      if (pillar) { pillar.isTalisman = true; pillar.isTalismanYear = true; pillars.push(pillar); }
    }
    if (chartData?.hs_tm || chartData?.eb_tm) {
      const pillar = buildPillar('hs_tm', 'eb_tm', 'T Month') as any;
      if (pillar) { pillar.isTalisman = true; pillar.isTalismanMonth = true; pillars.push(pillar); }
    }
    if (chartData?.hs_td || chartData?.eb_td) {
      const pillar = buildPillar('hs_td', 'eb_td', 'T Day') as any;
      if (pillar) { pillar.isTalisman = true; pillar.isTalismanDay = true; pillars.push(pillar); }
    }
    if (chartData?.hs_th || chartData?.eb_th) {
      const pillar = buildPillar('hs_th', 'eb_th', 'T Hour') as any;
      if (pillar) { pillar.isTalisman = true; pillar.isTalismanHour = true; pillars.push(pillar); }
    }

    return pillars;
  });

  // Build location pillars (overseas or birthplace)
  let locationPillars = $derived.by(() => {
    const pillars: any[] = [];

    // Overseas pillars (o1, o2)
    if (chartData?.hs_o1 || chartData?.eb_o1) {
      const pillar = buildPillar('hs_o1', 'eb_o1', 'Overseas 1') as any;
      if (pillar) { pillar.isLocation = true; pillar.isOverseas = true; pillars.push(pillar); }
    }
    if (chartData?.hs_o2 || chartData?.eb_o2) {
      const pillar = buildPillar('hs_o2', 'eb_o2', 'Overseas 2') as any;
      if (pillar) { pillar.isLocation = true; pillar.isOverseas = true; pillars.push(pillar); }
    }

    // Birthplace pillars (b1-b4)
    if (chartData?.hs_b1 || chartData?.eb_b1) {
      const pillar = buildPillar('hs_b1', 'eb_b1', 'Birthplace 1') as any;
      if (pillar) { pillar.isLocation = true; pillar.isBirthplace = true; pillars.push(pillar); }
    }
    if (chartData?.hs_b2 || chartData?.eb_b2) {
      const pillar = buildPillar('hs_b2', 'eb_b2', 'Birthplace 2') as any;
      if (pillar) { pillar.isLocation = true; pillar.isBirthplace = true; pillars.push(pillar); }
    }
    if (chartData?.hs_b3 || chartData?.eb_b3) {
      const pillar = buildPillar('hs_b3', 'eb_b3', 'Birthplace 3') as any;
      if (pillar) { pillar.isLocation = true; pillar.isBirthplace = true; pillars.push(pillar); }
    }
    if (chartData?.hs_b4 || chartData?.eb_b4) {
      const pillar = buildPillar('hs_b4', 'eb_b4', 'Birthplace 4') as any;
      if (pillar) { pillar.isLocation = true; pillar.isBirthplace = true; pillars.push(pillar); }
    }

    return pillars;
  });

  // Filter pillars based on props
  let displayNatalPillars = $derived(showNatal ? natalPillars : []);
  let displayAlignedLuckPillars = $derived((showLuck || show10YrLuck) ? alignedLuckPillars : []);
  let displayTalismanPillars = $derived(showTalisman ? talismanPillars : []);
  let displayLocationPillars = $derived(showLocation ? locationPillars : []);

  // Calculate cumulative indices for proper ordering
  let luckOffset = $derived(displayNatalPillars.length);
  let talismanOffset = $derived(luckOffset + displayAlignedLuckPillars.length);
  let locationOffset = $derived(talismanOffset + displayTalismanPillars.length);

  // Check if any pillars to display
  let hasPillars = $derived(
    displayNatalPillars.length > 0 || displayAlignedLuckPillars.length > 0 ||
    displayTalismanPillars.length > 0 || displayLocationPillars.length > 0
  );

  // Dong Gong helpers
  let dongGong = $derived(chartData?.dong_gong);
  let dongGongRating = $derived(dongGong?.rating);
  let dongGongColor = $derived.by(() => {
    if (!dongGongRating) return 'var(--tui-fg)';
    const v = dongGongRating.value;
    if (v >= 4) return 'var(--tui-wood)';
    if (v === 3) return 'var(--tui-earth)';
    if (v === 2.5) return 'var(--tui-water)';
    if (v <= 1) return '#000000';
    return 'var(--tui-fire)';
  });
  let dongGongTitle = $derived.by(() => {
    if (!dongGong) return '';
    if (dongGong.forbidden) {
      return `\u8463\u516C: ${dongGong.forbidden.chinese} (${dongGong.forbidden.solar_term_chinese}) \u2014 ${dongGong.forbidden.english}`;
    }
    if (dongGong.consult?.promoted) {
      return `\u8463\u516C: ${dongGong.officer?.chinese || ''} \u8B70 (originally \u51F6) \u2014 ${dongGong.consult.reason}`;
    }
    return `\u8463\u516C: ${dongGong.officer?.chinese || ''} ${dongGongRating?.chinese || ''}`;
  });
</script>

{#if hasPillars}
  <div class="relative">
    <div class="relative w-full">
      <!-- Heavenly Stems Row -->
      <div class="flex gap-0 items-center flex-wrap">
        <!-- Natal Pillar Stems -->
        {#each displayNatalPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="stem"
            index={index}
            {mappings}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Aligned Luck Pillar Stems -->
        {#each displayAlignedLuckPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="stem"
            index={luckOffset + index}
            {mappings}
            isLuck={true}
            isEmpty={pillar.isEmpty}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Divider before location pillars -->
        {#if displayAlignedLuckPillars.length > 0 && displayLocationPillars.length > 0}
          <div class="luck-divider self-stretch bg-gradient-to-b from-transparent to-transparent opacity-70 {displayLocationPillars[0]?.isOverseas ? 'via-blue-500' : 'via-amber-500'}"></div>
        {/if}

        <!-- Location Pillar Stems -->
        {#each displayLocationPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="stem"
            index={locationOffset + index}
            {mappings}
            isLocation={true}
            isOverseas={pillar.isOverseas}
            isBirthplace={pillar.isBirthplace}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Talisman Pillar Stems -->
        {#each displayTalismanPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="stem"
            index={talismanOffset + index}
            {mappings}
            isTalisman={true}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}
      </div>

      <!-- Dong Gong indicator row - between HS and EB on daily luck pillar -->
      {#if dongGongRating && displayAlignedLuckPillars.length > 0}
        <div class="flex gap-0 items-center">
          <!-- Empty spacers for natal pillars -->
          {#each displayNatalPillars as _, index (index)}
            <div class="w-28 flex-shrink-0"></div>
          {/each}
          <!-- Luck pillar columns - only daily (index 1) shows badge -->
          {#each displayAlignedLuckPillars as _, index (index)}
            <div class="w-28 flex-shrink-0 flex items-center justify-center">
              {#if index === 1}
                <span
                  class="text-xs font-medium px-1.5"
                  style="color: {dongGongColor};"
                  title={dongGongTitle}
                >
                  {dongGongRating.symbol} {dongGongRating.chinese}
                </span>
              {/if}
            </div>
          {/each}
        </div>
      {/if}

      <!-- Earthly Branches Row -->
      <div class="flex gap-0 overflow-visible items-stretch">
        <!-- Natal Pillar Branches -->
        {#each displayNatalPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="branch"
            index={index}
            {mappings}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Aligned Luck Pillar Branches -->
        {#each displayAlignedLuckPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="branch"
            index={luckOffset + index}
            {mappings}
            isLuck={true}
            isEmpty={pillar.isEmpty}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Divider before location pillars -->
        {#if displayAlignedLuckPillars.length > 0 && displayLocationPillars.length > 0}
          <div class="luck-divider self-stretch bg-gradient-to-b from-transparent to-transparent opacity-70 {displayLocationPillars[0]?.isOverseas ? 'via-blue-500' : 'via-amber-500'}"></div>
        {/if}

        <!-- Location Pillar Branches -->
        {#each displayLocationPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="branch"
            index={locationOffset + index}
            {mappings}
            isLocation={true}
            isOverseas={pillar.isOverseas}
            isBirthplace={pillar.isBirthplace}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}

        <!-- Talisman Pillar Branches -->
        {#each displayTalismanPillars as pillar, index (index)}
          <PillarCard
            {pillar}
            type="branch"
            index={talismanOffset + index}
            {mappings}
            isTalisman={true}
            {hoveredInteractionId}
            onHoverInteraction={(id) => hoveredInteractionId = id}
          />
        {/each}
      </div>
    </div>
  </div>
{/if}
