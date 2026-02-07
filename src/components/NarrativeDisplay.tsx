'use client';

import { useState, useMemo } from 'react';
import NarrativeCard from './NarrativeCard';
import PillarTag from './PillarTag';
import RemedyBadge from './RemedyBadge';

interface NarrativeDisplayProps {
  chartData: any;
}

// Category display order and colors - theme-aware via CSS variables
const CATEGORY_CONFIG: Record<string, { label: string; labelZh: string; color: string; bgColor: string }> = {
  combination: { label: 'Combinations', labelZh: '组合', color: 'var(--tui-accent-purple)', bgColor: 'color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))' },
  conflict: { label: 'Conflicts', labelZh: '冲突', color: 'var(--tui-error)', bgColor: 'color-mix(in srgb, var(--tui-error) 15%, var(--tui-bg))' },
  balance: { label: 'Element Balance', labelZh: '五行平衡', color: 'var(--tui-earth)', bgColor: 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))' },
  daymaster: { label: 'Daymaster', labelZh: '日主', color: 'var(--tui-water)', bgColor: 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' },
  wealth: { label: 'Wealth', labelZh: '财运', color: 'var(--tui-success)', bgColor: 'color-mix(in srgb, var(--tui-success) 15%, var(--tui-bg))' },
  seasonal: { label: 'Seasonal', labelZh: '季节', color: 'var(--tui-accent-teal)', bgColor: 'color-mix(in srgb, var(--tui-accent-teal) 15%, var(--tui-bg))' },
  energy: { label: 'Energy Flow', labelZh: '能量', color: 'var(--tui-info)', bgColor: 'color-mix(in srgb, var(--tui-info) 15%, var(--tui-bg))' },
};

// Category display order
const CATEGORY_ORDER = ['daymaster', 'combination', 'conflict', 'balance', 'wealth', 'seasonal', 'energy'];

export default function NarrativeDisplay({ chartData }: NarrativeDisplayProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showAllCategories, setShowAllCategories] = useState(false);

  // Extract narrative analysis from chart data
  const narrativeAnalysis = chartData?.narrative_analysis;

  // Group narratives by category
  const groupedNarratives = useMemo(() => {
    if (!narrativeAnalysis?.narratives_by_category) {
      return {};
    }
    return narrativeAnalysis.narratives_by_category;
  }, [narrativeAnalysis]);

  // Get summary info
  const summary = narrativeAnalysis?.summary;
  const quickRemedies = narrativeAnalysis?.quick_remedies;
  const remedies = narrativeAnalysis?.remedies || [];

  // Filter categories with content
  const categoriesWithContent = useMemo(() => {
    return CATEGORY_ORDER.filter(cat =>
      groupedNarratives[cat] && groupedNarratives[cat].length > 0
    );
  }, [groupedNarratives]);

  // Show only first 3 categories by default
  const visibleCategories = showAllCategories
    ? categoriesWithContent
    : categoriesWithContent.slice(0, 3);

  if (!narrativeAnalysis) {
    return null;
  }

  const handleToggle = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="narrative-panel">
      <div className="narrative-panel-inner">
        {/* Header with Summary */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-sm font-semibold tui-text mb-1">Chart Interpretation</h3>
            {summary && (
              <p className="text-xs tui-text-dim leading-relaxed">
                {summary.text}
              </p>
            )}
          </div>

          {/* Quick Remedies Badge */}
          {quickRemedies && quickRemedies.favorable_element && (
            <div className="ml-3 shrink-0">
              <RemedyBadge
                element={quickRemedies.favorable_element}
                colors={quickRemedies.lucky_colors}
                numbers={quickRemedies.lucky_numbers}
                direction={quickRemedies.favorable_direction}
              />
            </div>
          )}
        </div>

        {/* Outlook */}
        {summary?.outlook && (
          <div className="mb-3 p-2 tui-bg-alt tui-frame rounded text-xs tui-text-dim">
            {summary.outlook}
          </div>
        )}

        {/* Narrative Cards by Category */}
        <div className="space-y-3">
          {visibleCategories.map(category => {
            const config = CATEGORY_CONFIG[category];
            const narratives = groupedNarratives[category] || [];

            if (narratives.length === 0) return null;

            return (
              <div key={category} className="narrative-category">
                {/* Category Header */}
                <div
                  className="flex items-center gap-2 mb-1.5 pb-1 border-b"
                  style={{ borderColor: `color-mix(in srgb, ${config.color} 25%, var(--tui-bg))` }}
                >
                  <span
                    className="px-1.5 py-0.5 text-[10px] font-semibold rounded"
                    style={{
                      backgroundColor: config.bgColor,
                      color: config.color,
                    }}
                  >
                    {config.label}
                  </span>
                  <span className="text-[10px] tui-text-muted">
                    {narratives.length} {narratives.length === 1 ? 'item' : 'items'}
                  </span>
                </div>

                {/* Narrative Cards */}
                <div className="space-y-1.5">
                  {narratives.map((narrative: any) => (
                    <NarrativeCard
                      key={narrative.id}
                      narrative={narrative}
                      isExpanded={expandedId === narrative.id}
                      onToggle={() => handleToggle(narrative.id)}
                      mappings={chartData?.mappings}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Show More/Less */}
        {categoriesWithContent.length > 3 && (
          <button
            onClick={() => setShowAllCategories(!showAllCategories)}
            className="mt-3 w-full py-1.5 text-xs tui-text-dim tui-frame rounded hover:tui-bg-alt transition-colors"
          >
            {showAllCategories
              ? `Show Less`
              : `Show ${categoriesWithContent.length - 3} More Categories`
            }
          </button>
        )}

        {/* Detailed Remedies Section (Collapsed by default) */}
        {remedies.length > 0 && (
          <details className="mt-3">
            <summary className="text-xs font-semibold tui-text-dim cursor-pointer">
              Detailed Remedy Recommendations ({remedies.length})
            </summary>
            <div className="mt-2 space-y-2">
              {remedies.map((remedy: any, idx: number) => (
                <div
                  key={idx}
                  className="p-2 rounded text-xs"
                  style={{
                    background: 'color-mix(in srgb, var(--tui-wood) 15%, var(--tui-bg))',
                    border: '1px solid color-mix(in srgb, var(--tui-wood) 40%, var(--tui-bg))'
                  }}
                >
                  <div className="font-semibold mb-1" style={{ color: 'var(--tui-wood)' }}>
                    {remedy.title}
                  </div>
                  <p className="mb-2" style={{ color: 'var(--tui-wood)' }}>{remedy.intro}</p>

                  {remedy.recommendations && (
                    <div className="grid grid-cols-2 gap-2 text-[10px]">
                      {/* Colors */}
                      {remedy.recommendations.colors?.use?.length > 0 && (
                        <div>
                          <span className="font-medium tui-text-dim">Colors: </span>
                          <span className="tui-text">
                            {remedy.recommendations.colors.use.join(', ')}
                          </span>
                        </div>
                      )}

                      {/* Numbers */}
                      {remedy.recommendations.lucky_numbers?.length > 0 && (
                        <div>
                          <span className="font-medium tui-text-dim">Numbers: </span>
                          <span className="tui-text">
                            {remedy.recommendations.lucky_numbers.join(', ')}
                          </span>
                        </div>
                      )}

                      {/* Directions */}
                      {remedy.recommendations.directions?.favorable?.length > 0 && (
                        <div>
                          <span className="font-medium tui-text-dim">Directions: </span>
                          <span className="tui-text">
                            {remedy.recommendations.directions.favorable.join(', ')}
                          </span>
                        </div>
                      )}

                      {/* Season */}
                      {remedy.recommendations.favorable_season && (
                        <div>
                          <span className="font-medium tui-text-dim">Season: </span>
                          <span className="tui-text">
                            {remedy.recommendations.favorable_season}
                          </span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Activities */}
                  {remedy.recommendations?.activities?.length > 0 && (
                    <div className="mt-2 text-[10px]">
                      <span className="font-medium tui-text-dim">Suggested Activities:</span>
                      <ul className="mt-0.5 list-disc list-inside tui-text-dim">
                        {remedy.recommendations.activities.map((activity: string, i: number) => (
                          <li key={i}>{activity}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </details>
        )}
      </div>
    </div>
  );
}
