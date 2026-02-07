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

  // Daymaster
  strong: 'ST',
  weak: 'WK',

  // Wealth
  wealth_open: 'WO',
  wealth_closed: 'WC',

  // Other
  season: 'SN',
  flow: 'FL',
};

// Theme-aware color helper: derives bg/border from a CSS variable using color-mix
const themeColor = (cssVar: string) => ({
  text: cssVar,
  bg: `color-mix(in srgb, ${cssVar} 15%, var(--tui-bg))`,
  border: `color-mix(in srgb, ${cssVar} 40%, var(--tui-bg))`,
});

// Polarity to color mapping - theme-aware
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

        {/* Title and Summary */}
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

          {/* Summary */}
          <p className="text-[11px] tui-text-dim mt-0.5 line-clamp-2">
            {narrative.summary}
          </p>

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

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-2 pb-2 pt-0 border-t tui-border-color mt-1">
          {/* Detail */}
          {narrative.detail && (
            <p className="text-[11px] tui-text-dim mt-1.5 leading-relaxed">
              {narrative.detail}
            </p>
          )}

          {/* Meaning */}
          {narrative.meaning && (
            <div className="mt-2 p-1.5 tui-bg-alt rounded text-[10px]">
              <span className="font-semibold tui-text-dim">Meaning: </span>
              <span className="tui-text-dim">{narrative.meaning}</span>
            </div>
          )}

          {/* Advice */}
          {narrative.advice && (
            <div
              className="mt-1.5 p-1.5 rounded text-[10px]"
              style={{ background: 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' }}
            >
              <span className="font-semibold" style={{ color: 'var(--tui-water)' }}>Advice: </span>
              <span style={{ color: 'var(--tui-water)' }}>{narrative.advice}</span>
            </div>
          )}

          {/* Status Detail (Transformed/Partial) */}
          {narrative.status_detail && (
            <div className="mt-1.5 text-[10px] tui-text-muted italic">
              {narrative.status_detail}
            </div>
          )}

          {/* Element Note (from modifiers) */}
          {narrative.element_note && (
            <div
              className="mt-1.5 text-[10px] p-1 rounded"
              style={{
                background: 'color-mix(in srgb, var(--tui-accent-orange) 15%, var(--tui-bg))',
                color: 'var(--tui-accent-orange)'
              }}
            >
              {narrative.element_note}
            </div>
          )}

          {/* Shen Sha Stars */}
          {narrative.shen_sha && narrative.shen_sha.length > 0 && (
            <div className="mt-2 text-[10px]">
              <span className="font-semibold" style={{ color: 'var(--tui-accent-purple)' }}>Special Stars: </span>
              <span style={{ color: 'var(--tui-accent-purple)' }}>
                {narrative.shen_sha.map((star: any) =>
                  `${star.chinese_name || star.name}`
                ).join(', ')}
              </span>
              {narrative.shen_sha_note && (
                <span className="tui-text-muted ml-1">
                  - {narrative.shen_sha_note}
                </span>
              )}
            </div>
          )}

          {/* DM-Spouse Relationship Chain (for Day EB conflicts) */}
          {narrative.dm_spouse_relationship && (
            <div
              className="mt-2 p-2 rounded"
              style={{
                background: 'color-mix(in srgb, var(--tui-accent-pink) 15%, var(--tui-bg))',
                border: '1px solid color-mix(in srgb, var(--tui-accent-pink) 40%, var(--tui-bg))'
              }}
            >
              <div className="text-[10px] font-semibold mb-1.5" style={{ color: 'var(--tui-accent-pink)' }}>
                ❤️ Spouse Palace Chain Analysis
              </div>

              {/* DM-Spouse Relationship */}
              <div className="text-[10px] leading-relaxed" style={{ color: 'var(--tui-accent-pink)' }}>
                {narrative.dm_spouse_relationship.dm_spouse_meaning}
              </div>

              {/* Spouse Star Strength */}
              {narrative.dm_spouse_relationship.spouse_star_meaning && (
                <div className="mt-1.5 text-[10px]" style={{ color: 'var(--tui-accent-pink)' }}>
                  {narrative.dm_spouse_relationship.spouse_star_meaning}
                </div>
              )}

              {/* Chain Interpretation */}
              {narrative.dm_spouse_relationship.chain_interpretation && (
                <div className="mt-2 p-1.5 tui-bg-alt rounded text-[10px] font-medium" style={{ color: 'var(--tui-accent-pink)' }}>
                  {narrative.dm_spouse_relationship.chain_interpretation}
                </div>
              )}
            </div>
          )}

          {/* Branch Chain Analyses (Full chain for conflicts) */}
          {narrative.branch_chain_analyses && narrative.branch_chain_analyses.length > 0 && (
            <details className="mt-2">
              <summary className="text-[10px] font-semibold cursor-pointer" style={{ color: 'var(--tui-accent-purple)' }}>
                🔗 Detailed Chain Analysis ({narrative.branch_chain_analyses.length} branches)
              </summary>
              <div className="mt-2 space-y-2">
                {narrative.branch_chain_analyses.map((ba: any, idx: number) => (
                  <div
                    key={idx}
                    className="p-2 tui-bg-alt tui-frame rounded"
                  >
                    <div className="text-[10px] font-semibold mb-1" style={{ color: 'var(--tui-accent-purple)' }}>
                      [{ba.branch}] {ba.pillar_type?.toUpperCase()} Pillar
                    </div>

                    {/* Chain Items */}
                    {ba.analysis?.chains?.map((chain: any, chainIdx: number) => (
                      <div key={chainIdx} className="mt-1 text-[9px]">
                        {chain.type === 'element' && (
                          <div className="flex items-center gap-1 tui-text-dim">
                            <span className="font-medium" style={{ color: 'var(--tui-wood)' }}>Element:</span>
                            <span>{chain.element} ({chain.percentage?.toFixed(1)}%)</span>
                            <span style={{ color: chain.favorable ? 'var(--tui-wood)' : 'var(--tui-earth)' }}>
                              {chain.favorable ? '✓ favorable' : '⚠ unfavorable'}
                            </span>
                          </div>
                        )}

                        {chain.type === 'ten_god' && (
                          <div className="tui-text-dim">
                            <span className="font-medium" style={{ color: 'var(--tui-water)' }}>Ten God:</span>
                            <span className="ml-1">{chain.name_en}</span>
                            {chain.is_excess && (
                              <span className="ml-1" style={{ color: 'var(--tui-earth)' }}>
                                (excess: {chain.excess_traits?.join(', ')})
                              </span>
                            )}
                          </div>
                        )}

                        {chain.type === 'shen_sha' && (
                          <div
                            className="p-1 rounded mt-1"
                            style={{
                              background: 'color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))',
                              color: 'var(--tui-accent-purple)'
                            }}
                          >
                            <div className="font-medium">
                              ⭐ {chain.chinese} / {chain.english}
                            </div>
                            <div className="mt-0.5">
                              {chain.base_meaning}
                            </div>
                            {chain.contextual_meanings?.length > 0 && (
                              <div className="mt-0.5 font-medium">
                                → {chain.contextual_meanings.join(' → ')}
                              </div>
                            )}
                          </div>
                        )}

                        {chain.type === 'qi_phase' && (
                          <div className="tui-text-dim">
                            <span className="font-medium" style={{ color: 'var(--tui-accent-teal)' }}>Qi Phase:</span>
                            <span className="ml-1">{chain.chinese} ({chain.english})</span>
                            <span className="ml-1 tui-text-muted">- {chain.base_meaning}</span>
                            {chain.is_storage && (
                              <div className="mt-0.5 p-1 rounded" style={{ background: 'var(--tui-earth)', color: 'var(--tui-bg)' }}>
                                📦 {chain.storage_meaning}
                              </div>
                            )}
                          </div>
                        )}

                        {chain.type === 'storage' && (
                          <div
                            className="p-1 rounded mt-1"
                            style={{
                              background: 'color-mix(in srgb, var(--tui-accent-orange) 15%, var(--tui-bg))',
                              color: 'var(--tui-accent-orange)'
                            }}
                          >
                            <div className="font-medium">
                              🏛️ Storage: {chain.stores} element
                            </div>
                            {chain.is_wealth_storage && (
                              <div className="mt-0.5">
                                💰 Wealth Storage | Wealth: {chain.wealth_percentage?.toFixed(1)}% ({chain.wealth_strength})
                              </div>
                            )}
                            <div className="mt-0.5">
                              {chain.opener_meaning}
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </details>
          )}

          {/* Master Chain Narrative */}
          {narrative.master_chain_narrative && (
            <div className="mt-2 p-2 tui-bg-alt tui-frame rounded">
              <div className="text-[9px] font-semibold tui-text-dim mb-1">
                📜 Chain Summary
              </div>
              <div className="text-[9px] tui-text leading-relaxed">
                {narrative.master_chain_narrative}
              </div>
            </div>
          )}

          {/* Life Area Impact */}
          {narrative.life_area_impact && (
            <div className="mt-1.5 text-[10px] tui-text-dim tui-bg-alt p-1.5 rounded">
              {narrative.life_area_impact}
            </div>
          )}

          {/* Branches Display */}
          {narrative.branches_display && (
            <div className="mt-1.5 text-[10px] tui-text-muted">
              <span className="font-medium">Branches: </span>
              <span className="font-mono">{narrative.branches_display}</span>
            </div>
          )}

          {/* Distance/Priority */}
          <div className="mt-2 flex items-center gap-3 text-[9px] tui-text-muted">
            {narrative.distance && (
              <span>Distance: {narrative.distance}</span>
            )}
            {narrative.priority_score && (
              <span>Priority: {narrative.priority_score}</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
