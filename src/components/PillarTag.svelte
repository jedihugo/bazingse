<script lang="ts">
  interface PillarTagProps {
    text: string;
    nodeType?: string;
    position?: string;
  }

  let { text, nodeType, position }: PillarTagProps = $props();

  // Theme-aware color helper
  function themeColor(cssVar: string) {
    return {
      bg: `color-mix(in srgb, ${cssVar} 15%, var(--tui-bg))`,
      text: cssVar,
      border: `color-mix(in srgb, ${cssVar} 40%, var(--tui-bg))`,
    };
  }

  // Color scheme based on pillar type - theme-aware via CSS variables
  const POSITION_COLORS: Record<string, { bg: string; text: string; border: string }> = {
    // Natal pillars
    h: themeColor('var(--tui-earth)'),
    d: themeColor('var(--tui-accent-purple)'),
    m: themeColor('var(--tui-water)'),
    y: themeColor('var(--tui-wood)'),

    // Luck pillars
    '10yl': themeColor('var(--tui-accent-pink)'),
    yl: themeColor('var(--tui-accent-purple)'),
    ml: themeColor('var(--tui-accent-teal)'),
    dl: themeColor('var(--tui-earth)'),
    hl: themeColor('var(--tui-accent-orange)'),

    // Talisman pillars
    ty: themeColor('var(--tui-metal)'),
    tm: themeColor('var(--tui-metal)'),
    td: themeColor('var(--tui-metal)'),
    th: themeColor('var(--tui-metal)'),

    // Default
    unknown: themeColor('var(--tui-fg-muted)'),
  };

  // Node type indicators
  const NODE_TYPE_ICON: Record<string, string> = {
    hs: '\u5E72', // 干 Heavenly Stem
    eb: '\u652F', // 支 Earthly Branch
  };

  let posKey = $derived(position || 'unknown');
  let colors = $derived(POSITION_COLORS[posKey] || POSITION_COLORS.unknown);
  let typeIcon = $derived(nodeType ? NODE_TYPE_ICON[nodeType] || '' : '');
</script>

<span
  class="inline-flex items-center gap-0.5 px-1 py-0.5 rounded text-[9px] font-medium"
  style="background-color: {colors.bg}; color: {colors.text}; border: 1px solid {colors.border};"
>
  {#if typeIcon}
    <span class="opacity-60">{typeIcon}</span>
  {/if}
  <span>{text}</span>
</span>
