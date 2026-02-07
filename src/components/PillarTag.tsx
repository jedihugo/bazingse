'use client';

interface PillarTagProps {
  text: string;
  nodeType?: string;
  position?: string;
}

// Theme-aware color helper
const themeColor = (cssVar: string) => ({
  bg: `color-mix(in srgb, ${cssVar} 15%, var(--tui-bg))`,
  text: cssVar,
  border: `color-mix(in srgb, ${cssVar} 40%, var(--tui-bg))`,
});

// Color scheme based on pillar type - theme-aware via CSS variables
const POSITION_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  // Natal pillars
  h: themeColor('var(--tui-earth)'),           // Hour - gold
  d: themeColor('var(--tui-accent-purple)'),   // Day - purple
  m: themeColor('var(--tui-water)'),           // Month - blue
  y: themeColor('var(--tui-wood)'),            // Year - green

  // Luck pillars
  '10yl': themeColor('var(--tui-accent-pink)'),   // 10Y Luck - pink
  yl: themeColor('var(--tui-accent-purple)'),     // Annual - indigo
  ml: themeColor('var(--tui-accent-teal)'),       // Monthly - cyan
  dl: themeColor('var(--tui-earth)'),             // Daily - yellow
  hl: themeColor('var(--tui-accent-orange)'),     // Hourly - orange

  // Talisman pillars
  ty: themeColor('var(--tui-metal)'),     // Talisman Year
  tm: themeColor('var(--tui-metal)'),     // Talisman Month
  td: themeColor('var(--tui-metal)'),     // Talisman Day
  th: themeColor('var(--tui-metal)'),     // Talisman Hour

  // Default
  unknown: themeColor('var(--tui-fg-muted)'),
};

// Node type indicators
const NODE_TYPE_ICON: Record<string, string> = {
  hs: '干', // Heavenly Stem
  eb: '支', // Earthly Branch
};

export default function PillarTag({ text, nodeType, position }: PillarTagProps) {
  const posKey = position || 'unknown';
  const colors = POSITION_COLORS[posKey] || POSITION_COLORS.unknown;
  const typeIcon = nodeType ? NODE_TYPE_ICON[nodeType] : '';

  return (
    <span
      className="inline-flex items-center gap-0.5 px-1 py-0.5 rounded text-[9px] font-medium"
      style={{
        backgroundColor: colors.bg,
        color: colors.text,
        border: `1px solid ${colors.border}`,
      }}
    >
      {typeIcon && (
        <span className="opacity-60">{typeIcon}</span>
      )}
      <span>{text}</span>
    </span>
  );
}
