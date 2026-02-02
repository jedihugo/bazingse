'use client';

interface PillarTagProps {
  text: string;
  nodeType?: string;
  position?: string;
}

// Color scheme based on pillar type
const POSITION_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  // Natal pillars
  h: { bg: '#fef3c7', text: '#92400e', border: '#f59e0b' },      // Hour - amber
  d: { bg: '#f3e8ff', text: '#7e22ce', border: '#a855f7' },      // Day - purple
  m: { bg: '#dbeafe', text: '#1e40af', border: '#3b82f6' },      // Month - blue
  y: { bg: '#dcfce7', text: '#166534', border: '#22c55e' },      // Year - green

  // Luck pillars
  '10yl': { bg: '#fce7f3', text: '#9d174d', border: '#ec4899' }, // 10Y Luck - pink
  yl: { bg: '#e0e7ff', text: '#3730a3', border: '#6366f1' },     // Annual - indigo
  ml: { bg: '#cffafe', text: '#0e7490', border: '#06b6d4' },     // Monthly - cyan
  dl: { bg: '#fef9c3', text: '#854d0e', border: '#eab308' },     // Daily - yellow
  hl: { bg: '#fed7aa', text: '#9a3412', border: '#f97316' },     // Hourly - orange

  // Talisman pillars
  ty: { bg: '#f1f5f9', text: '#475569', border: '#94a3b8' },     // Talisman Year - slate
  tm: { bg: '#f1f5f9', text: '#475569', border: '#94a3b8' },     // Talisman Month
  td: { bg: '#f1f5f9', text: '#475569', border: '#94a3b8' },     // Talisman Day
  th: { bg: '#f1f5f9', text: '#475569', border: '#94a3b8' },     // Talisman Hour

  // Default
  unknown: { bg: '#f3f4f6', text: '#374151', border: '#9ca3af' },
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
