<script lang="ts">
  interface SectionItem {
    label: string;
    value: string;
    severity?: string;
  }

  interface Section {
    id: string;
    title: string;
    title_zh?: string;
    severity?: string;
    text?: string;
    items?: SectionItem[];
  }

  interface ClientSummary {
    tier: string;
    sections: Section[];
  }

  interface ClientSummaryDisplayProps {
    chartData: any;
  }

  let { chartData }: ClientSummaryDisplayProps = $props();

  // Severity badge style map
  const SEVERITY_BADGE_STYLES: Record<string, { bg: string; color: string }> = {
    strong: { bg: 'var(--tui-wood)', color: 'var(--tui-bg)' },
    weak: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    neutral: { bg: 'var(--tui-water)', color: 'var(--tui-bg)' },
    positive: { bg: 'var(--tui-wood)', color: 'var(--tui-bg)' },
    info: { bg: 'var(--tui-water)', color: 'var(--tui-bg)' },
    warning: { bg: 'var(--tui-accent-orange, var(--tui-earth))', color: 'var(--tui-bg)' },
    alert: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    severe: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    negative: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    moderate: { bg: 'var(--tui-earth)', color: 'var(--tui-bg)' },
    mild: { bg: 'var(--tui-metal)', color: 'var(--tui-bg)' },
  };

  // Severity left-border color map
  const SEVERITY_COLOR_MAP: Record<string, string> = {
    positive: 'var(--tui-wood)',
    info: 'var(--tui-water)',
    warning: 'var(--tui-accent-orange, var(--tui-earth))',
    alert: 'var(--tui-fire)',
    severe: 'var(--tui-fire)',
    negative: 'var(--tui-fire)',
    moderate: 'var(--tui-earth)',
    mild: 'var(--tui-metal)',
  };

  function severityColor(severity?: string): string {
    return severity ? (SEVERITY_COLOR_MAP[severity] || 'var(--tui-fg-dim)') : 'var(--tui-fg-dim)';
  }

  function getBadgeStyle(severity: string): { bg: string; color: string } {
    return SEVERITY_BADGE_STYLES[severity] || SEVERITY_BADGE_STYLES.info;
  }

  let summary = $derived(chartData?.client_summary as ClientSummary | undefined);

  let defaultOpenIds = $derived.by(() => {
    if (!summary) return new Set<string>();
    return new Set(
      summary.tier === 'full'
        ? ['luck_pillar', 'element_shift', 'ten_gods_diff', 'interactions_diff', 'shen_sha_diff']
        : ['red_flags', 'summary', 'chart_overview', 'strength']
    );
  });

  let headerText = $derived(
    summary?.tier === 'full' ? 'What Changed' : 'Natal Analysis'
  );
</script>

{#if summary?.sections?.length}
  <div class="mt-3 space-y-1">
    <div class="text-xs tui-text-muted px-2 py-1">
      {headerText}
    </div>

    {#each summary.sections as section (section.id)}
      {@const badgeStyle = section.severity ? getBadgeStyle(section.severity) : null}
      <details
        open={defaultOpenIds.has(section.id) || undefined}
        class="tui-frame"
      >
        <summary
          class="px-3 py-2 cursor-pointer text-sm font-medium flex items-center justify-between"
          style="background: var(--tui-bg-alt);"
        >
          <span>
            {section.title}
            {#if section.title_zh}
              <span class="tui-text-muted ml-1">{section.title_zh}</span>
            {/if}
          </span>
          {#if section.severity && badgeStyle}
            <span
              class="text-xs px-1.5 py-0.5 ml-2"
              style="background: {badgeStyle.bg}; color: {badgeStyle.color};"
            >
              {section.severity}
            </span>
          {/if}
        </summary>

        <div class="px-3 py-2 text-sm space-y-1">
          {#if section.text}
            <p class="tui-text-dim">{section.text}</p>
          {/if}

          {#if section.items}
            {#each section.items as item, i (i)}
              {@const itemColor = severityColor(item.severity)}
              <div
                class="flex gap-2 text-xs py-0.5"
                style={item.severity ? `border-left: 2px solid ${itemColor}; padding-left: 8px;` : ''}
              >
                <span class="font-medium shrink-0" style="color: {itemColor};">
                  {item.label}
                </span>
                <span class="tui-text-dim">{item.value}</span>
              </div>
            {/each}
          {/if}

          {#if !section.text && (!section.items || section.items.length === 0)}
            <p class="tui-text-muted text-xs">No data for this section</p>
          {/if}
        </div>
      </details>
    {/each}
  </div>
{/if}
