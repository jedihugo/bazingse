'use client';

import { useState, useMemo } from 'react';
import NarrativeCard from './NarrativeCard';

interface NarrativeDisplayProps {
  chartData: any;
}

// Category display order and colors - theme-aware via CSS variables
const CATEGORY_CONFIG: Record<string, { label: string; labelZh: string; color: string; bgColor: string }> = {
  combination: { label: 'Combinations', labelZh: '组合', color: 'var(--tui-accent-purple)', bgColor: 'color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))' },
  conflict: { label: 'Conflicts', labelZh: '冲突', color: 'var(--tui-error)', bgColor: 'color-mix(in srgb, var(--tui-error) 15%, var(--tui-bg))' },
  balance: { label: 'Element Balance', labelZh: '五行平衡', color: 'var(--tui-earth)', bgColor: 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))' },
  wealth: { label: 'Wealth', labelZh: '财运', color: 'var(--tui-success)', bgColor: 'color-mix(in srgb, var(--tui-success) 15%, var(--tui-bg))' },
  seasonal: { label: 'Seasonal', labelZh: '季节', color: 'var(--tui-accent-teal)', bgColor: 'color-mix(in srgb, var(--tui-accent-teal) 15%, var(--tui-bg))' },
  energy: { label: 'Energy Flow', labelZh: '能量', color: 'var(--tui-info)', bgColor: 'color-mix(in srgb, var(--tui-info) 15%, var(--tui-bg))' },
};

// Category display order (no daymaster)
const CATEGORY_ORDER = ['combination', 'conflict', 'balance', 'wealth', 'seasonal', 'energy'];

export default function NarrativeDisplay({ chartData }: NarrativeDisplayProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [showAllCategories, setShowAllCategories] = useState(false);

  const narrativeAnalysis = chartData?.narrative_analysis;

  const groupedNarratives = useMemo(() => {
    if (!narrativeAnalysis?.narratives_by_category) {
      return {};
    }
    return narrativeAnalysis.narratives_by_category;
  }, [narrativeAnalysis]);

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
      </div>
    </div>
  );
}
