'use client';

import PillarTag from './PillarTag';

interface NarrativeCardProps {
  narrative: any;
  isExpanded: boolean;
  onToggle: () => void;
  mappings?: any;
}

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

// Theme-aware color helper
const themeColor = (cssVar: string) => ({
  text: cssVar,
  bg: `color-mix(in srgb, ${cssVar} 15%, var(--tui-bg))`,
  border: `color-mix(in srgb, ${cssVar} 40%, var(--tui-bg))`,
});

// Polarity to color mapping
const POLARITY_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  positive: themeColor('var(--tui-success)'),
  negative: themeColor('var(--tui-error)'),
  neutral: { bg: 'var(--tui-bg-alt)', border: 'var(--tui-border)', text: 'var(--tui-fg)' },
};

export default function NarrativeCard({ narrative, isExpanded, onToggle, mappings }: NarrativeCardProps) {
  const polarity = narrative.polarity || 'neutral';
  const colors = POLARITY_COLORS[polarity] || POLARITY_COLORS.neutral;
  const icon = ICON_MAP[narrative.icon] || narrative.type?.slice(0, 2).toUpperCase() || '??';

  // Get element color if available
  const elementColor = narrative.element
    ? mappings?.elements?.[narrative.element]?.hex_color
    : null;

  return (
    <div
      className="narrative-card"
      style={{
        backgroundColor: colors.bg,
        borderColor: colors.border,
        borderWidth: '1px',
        borderStyle: 'solid',
      }}
    >
      {/* Card Header - Always Visible */}
      <button
        onClick={onToggle}
        className="w-full flex items-start gap-2 text-left p-2"
      >
        {/* Icon Badge */}
        <div
          className="shrink-0 w-7 h-7 flex items-center justify-center rounded text-[10px] font-bold"
          style={{
            backgroundColor: elementColor || colors.border,
            color: 'var(--tui-bg)',
          }}
        >
          {icon}
        </div>

        {/* Title and Points */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-semibold" style={{ color: colors.text }}>
              {narrative.title}
            </span>

            {/* Element indicator */}
            {narrative.element && (
              <span
                className="px-1 py-0.5 text-[9px] rounded"
                style={{
                  backgroundColor: elementColor ? `color-mix(in srgb, ${elementColor} 20%, var(--tui-bg))` : 'var(--tui-bg-alt)',
                  color: elementColor || 'var(--tui-fg-dim)',
                }}
              >
                {narrative.element}
              </span>
            )}

            {/* Points indicator */}
            {narrative.points && (
              <span className="text-[9px] tui-text-muted font-mono">
                {narrative.points}
              </span>
            )}
          </div>

          {/* Pillar Tags */}
          {narrative.pillar_refs && narrative.pillar_refs.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-1">
              {narrative.pillar_refs.map((ref: any, idx: number) => (
                <PillarTag
                  key={idx}
                  text={ref.abbrev}
                  nodeType={ref.node_type}
                  position={ref.position}
                />
              ))}
            </div>
          )}
        </div>

        {/* Expand/Collapse Arrow */}
        <div className="shrink-0 tui-text-muted text-xs">
          {isExpanded ? '▲' : '▼'}
        </div>
      </button>

      {/* Expanded Content - Points focused */}
      {isExpanded && (
        <div className="px-2 pb-2 pt-0 border-t tui-border-color mt-1">
          {/* Status Detail (Transformed/Partial) */}
          {narrative.status_detail && (
            <div className="mt-1.5 text-[10px] tui-text-muted italic">
              {narrative.status_detail}
            </div>
          )}

          {/* Distance/Priority */}
          <div className="mt-1.5 flex items-center gap-3 text-[9px] tui-text-muted font-mono">
            {narrative.distance && (
              <span>Distance: {narrative.distance}</span>
            )}
            {narrative.priority_score && (
              <span>Priority: {narrative.priority_score}</span>
            )}
          </div>

          {/* Branches Display */}
          {narrative.branches_display && (
            <div className="mt-1.5 text-[10px] tui-text-muted">
              <span className="font-medium">Branches: </span>
              <span className="font-mono">{narrative.branches_display}</span>
            </div>
          )}

          {/* Percentage for balance items */}
          {narrative.percentage !== undefined && (
            <div className="mt-1.5 text-[10px] tui-text-muted font-mono">
              {narrative.element}: {narrative.percentage?.toFixed(1)}%
            </div>
          )}
        </div>
      )}
    </div>
  );
}
