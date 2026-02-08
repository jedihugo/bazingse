'use client';

import PillarTag from './PillarTag';

interface NarrativeCardProps {
  narrative: any;
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

export default function NarrativeCard({ narrative, mappings }: NarrativeCardProps) {
  const polarity = narrative.polarity || 'neutral';
  const icon = ICON_MAP[narrative.icon] || narrative.type?.slice(0, 2).toUpperCase() || '??';
  const seq = narrative.seq;

  // Get element color if available
  const elementColor = narrative.element
    ? mappings?.elements?.[narrative.element]?.hex_color
    : null;

  // Polarity class for left border
  const polarityClass = polarity === 'positive'
    ? 'narrative-card-positive'
    : polarity === 'negative'
      ? 'narrative-card-negative'
      : 'narrative-card-neutral';

  // Formula color based on polarity
  const formulaColor = polarity === 'positive'
    ? 'var(--tui-success)'
    : polarity === 'negative'
      ? 'var(--tui-error)'
      : 'var(--tui-text-muted)';

  return (
    <div className={`narrative-card ${polarityClass}`}>
      <div className="p-2">
        {/* Row 1: Seq + Icon + Title + Element + Points */}
        <div className="flex items-center gap-2">
          {/* Sequence number */}
          <span className="shrink-0 text-[9px] font-mono tui-text-dim w-4 text-right">
            {seq}
          </span>

          {/* Icon Badge */}
          <div
            className="shrink-0 w-6 h-6 flex items-center justify-center rounded text-[9px] font-bold"
            style={elementColor ? { backgroundColor: elementColor, color: '#fff' } : undefined}
          >
            {icon}
          </div>

          {/* Title + Element + Points */}
          <div className="flex-1 min-w-0 flex items-center gap-1.5 flex-wrap">
            <span className="text-xs font-semibold tui-text">
              {narrative.title}
            </span>

            {narrative.element && (
              <span
                className="px-1 py-0.5 text-[9px] rounded font-medium"
                style={elementColor ? { color: elementColor } : undefined}
              >
                {narrative.element}
              </span>
            )}

            {narrative.points && (
              <span className="text-[9px] tui-text-muted font-mono">
                {narrative.points}
              </span>
            )}
          </div>
        </div>

        {/* Row 2: Formula (always visible, colored by polarity) */}
        {narrative.formula && (
          <div className="mt-1 ml-12 text-[10px] font-mono" style={{ color: formulaColor }}>
            {narrative.formula}
          </div>
        )}

        {/* Row 3: Match (always visible) */}
        {narrative.match && (
          <div className="mt-0.5 ml-12 text-[10px] tui-text-muted font-mono">
            {narrative.match}
          </div>
        )}

        {/* Row 4: Qi before→after changes */}
        {narrative.qi_changes && narrative.qi_changes.length > 0 && (
          <div className="mt-1 ml-12 flex flex-wrap gap-x-3 gap-y-0.5">
            {narrative.qi_changes.map((qc: any, idx: number) => (
              <span key={idx} className="text-[10px] font-mono tui-text-muted">
                {qc.stem}: {qc.before}
                {qc.before !== qc.after ? (
                  <span style={{ color: qc.after > qc.before ? 'var(--tui-success)' : 'var(--tui-error)' }}>
                    →{qc.after}
                  </span>
                ) : (
                  qc.note && <span className="tui-text-dim"> ({qc.note})</span>
                )}
              </span>
            ))}
          </div>
        )}

        {/* Row 5: Pillar Tags */}
        {narrative.pillar_refs && narrative.pillar_refs.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1 ml-12">
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

        {/* Row 6: Math formula (scoring breakdown) */}
        {narrative.math_formula && (
          <div className="mt-0.5 ml-12 text-[9px] tui-text-dim font-mono">
            {narrative.math_formula}
          </div>
        )}
      </div>
    </div>
  );
}
