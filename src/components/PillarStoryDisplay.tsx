'use client';

import { useState } from 'react';

interface PillarStoryDisplayProps {
  chartData: any;
}

// Element colors
const ELEMENT_COLORS: Record<string, string> = {
  Wood: '#22c55e',
  Fire: '#ef4444',
  Earth: '#eab308',
  Metal: '#94a3b8',
  Water: '#3b82f6',
};

// Ten God abbreviations
const TEN_GOD_ABBREV: Record<string, string> = {
  resource: 'R',
  companion: 'C',
  output: 'O',
  wealth: 'W',
  officer: 'P',
};

export default function PillarStoryDisplay({ chartData }: PillarStoryDisplayProps) {
  const [activeNodeId, setActiveNodeId] = useState<string | null>(null);
  const [expandedStory, setExpandedStory] = useState<string | null>(null);

  const pillarStories = chartData?.pillar_stories;
  if (!pillarStories) return null;

  const { minimap, pillar_stories: stories } = pillarStories;

  const handleStoryHover = (nodeId: string | null) => {
    setActiveNodeId(nodeId);
  };

  const handleStoryClick = (nodeId: string) => {
    setExpandedStory(expandedStory === nodeId ? null : nodeId);
  };

  return (
    <div className="pillar-story-panel">
      <h3 className="text-sm font-semibold tui-text mb-3">Chart Story (Node by Node)</h3>

      {/* Minimap */}
      <div className="minimap mb-4">
        <div className="flex justify-center gap-1">
          {minimap?.pillars?.map((pillar: any) => (
            <div
              key={pillar.pillar}
              className="minimap-pillar"
            >
              {/* Pillar Label */}
              <div className="text-[9px] tui-text-muted text-center mb-0.5 uppercase">
                {pillar.pillar.slice(0, 2)}
              </div>

              {/* HS Cell */}
              <div
                className={`minimap-cell ${activeNodeId === pillar.hs.node_id ? 'ring-2' : ''}`}
                style={{
                  backgroundColor: ELEMENT_COLORS[pillar.hs.element] || '#e5e7eb',
                  '--tw-ring-color': 'var(--tui-accent-purple)',
                } as React.CSSProperties}
                title={`${pillar.hs.value} (${pillar.hs.element})`}
              >
                <span className="text-[8px] font-bold text-white drop-shadow">
                  {pillar.hs.value?.slice(0, 2)}
                </span>
              </div>

              {/* EB Cell */}
              <div
                className={`minimap-cell mt-0.5 ${activeNodeId === pillar.eb.node_id ? 'ring-2' : ''}`}
                style={{
                  backgroundColor: ELEMENT_COLORS[pillar.eb.element] || '#e5e7eb',
                  '--tw-ring-color': 'var(--tui-accent-purple)',
                } as React.CSSProperties}
                title={`${pillar.eb.value} (${pillar.eb.element})`}
              >
                <span className="text-[8px] font-bold text-white drop-shadow">
                  {pillar.eb.value?.slice(0, 2)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Story Cards */}
      <div className="space-y-1.5">
        {stories?.map((story: any) => {
          const isActive = activeNodeId === story.node_id;
          const isExpanded = expandedStory === story.node_id;
          const elementColor = ELEMENT_COLORS[story.element] || '#9ca3af';

          return (
            <div
              key={story.node_id}
              className={`story-card ${isActive ? 'ring-2' : ''}`}
              style={{ '--tw-ring-color': 'var(--tui-accent-purple)' } as React.CSSProperties}
              onMouseEnter={() => handleStoryHover(story.node_id)}
              onMouseLeave={() => handleStoryHover(null)}
              onClick={() => handleStoryClick(story.node_id)}
            >
              {/* Header Row */}
              <div className="flex items-center gap-2">
                {/* Element Badge */}
                <div
                  className="w-8 h-8 rounded flex items-center justify-center shrink-0"
                  style={{ backgroundColor: elementColor }}
                >
                  <span className="text-[10px] font-bold text-white">
                    {story.is_daymaster ? 'DM' : TEN_GOD_ABBREV[story.ten_god_role] || '?'}
                  </span>
                </div>

                {/* Node Info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold tui-text">
                      {story.node_name}
                    </span>
                    <span
                      className="text-[9px] px-1 py-0.5 rounded"
                      style={{
                        backgroundColor: elementColor + '30',
                        color: elementColor,
                      }}
                    >
                      {story.element} {story.element_percentage?.toFixed(1)}%
                    </span>
                    {!story.is_favorable && (
                      <span className="text-[9px]" style={{ color: 'var(--tui-accent-orange)' }}>⚠</span>
                    )}
                    {story.is_excessive && (
                      <span className="text-[9px]" style={{ color: 'var(--tui-fire)' }}>🔥</span>
                    )}
                  </div>

                  <div className="text-[10px] tui-text-dim">
                    {story.ten_god_name}
                    {story.node_role && ` • ${story.node_role}`}
                  </div>
                </div>

                {/* Expand Arrow */}
                <div className="tui-text-muted text-xs shrink-0">
                  {isExpanded ? '▲' : '▼'}
                </div>
              </div>

              {/* Quick Info Row (always visible) */}
              <div className="mt-1.5 flex flex-wrap gap-1">
                {/* Qi Phase Badge */}
                {story.qi_phase && (
                  <span
                    className="text-[9px] px-1.5 py-0.5 rounded"
                    style={{ background: 'var(--tui-accent-teal)', color: 'var(--tui-bg)' }}
                  >
                    {story.qi_phase.chinese} {story.qi_phase.english}
                  </span>
                )}

                {/* Storage Badge */}
                {story.storage && (
                  <span
                    className="text-[9px] px-1.5 py-0.5 rounded font-semibold"
                    style={story.storage.is_wealth_storage
                      ? { background: 'var(--tui-earth)', color: 'var(--tui-bg)' }
                      : { background: 'var(--tui-bg-alt)', color: 'var(--tui-fg-dim)' }
                    }
                  >
                    {story.storage.is_wealth_storage ? '💰' : '📦'} {story.storage.stores}库
                  </span>
                )}

                {/* Shen Sha Badges */}
                {story.shen_sha?.map((ss: any, idx: number) => (
                  <span
                    key={idx}
                    className="text-[9px] px-1.5 py-0.5 rounded"
                    style={{ background: 'var(--tui-accent-purple)', color: 'var(--tui-bg)' }}
                  >
                    ⭐ {ss.chinese}
                  </span>
                ))}
              </div>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="mt-2 pt-2 border-t tui-border-color text-[10px] space-y-1.5">
                  {/* Role Description */}
                  <div className="tui-text-dim">
                    <span className="font-medium">Represents: </span>
                    {story.node_represents}
                  </div>

                  {/* Ten God Meaning */}
                  <div className="tui-text-dim">
                    <span className="font-medium">{story.ten_god_name}: </span>
                    {story.ten_god_meaning}
                  </div>

                  {/* Excess Meaning */}
                  {story.excess_meaning && (
                    <div
                      className="p-1.5 rounded"
                      style={{ background: 'var(--tui-fire)', color: 'var(--tui-bg)' }}
                    >
                      <span className="font-medium">Excess Effect: </span>
                      {story.excess_meaning}
                    </div>
                  )}

                  {/* Qi Phase Detail */}
                  {story.qi_phase && (
                    <div className="tui-text-dim">
                      <span className="font-medium">Qi Phase ({story.qi_phase.chinese}): </span>
                      {story.qi_phase.meaning}
                    </div>
                  )}

                  {/* Storage Detail */}
                  {story.storage && (
                    <div
                      className="p-1.5 rounded"
                      style={story.storage.is_wealth_storage
                        ? { background: 'var(--tui-earth)', color: 'var(--tui-bg)' }
                        : { background: 'var(--tui-bg-alt)', color: 'var(--tui-fg-dim)' }
                      }
                    >
                      <div className="font-medium">
                        {story.storage.is_wealth_storage ? '💰 Wealth Storage!' : '📦 Storage Branch'}
                      </div>
                      <div>
                        Stores {story.storage.stores} • Opened by {story.storage.opener} clash
                      </div>
                    </div>
                  )}

                  {/* Shen Sha Detail */}
                  {story.shen_sha?.map((ss: any, idx: number) => (
                    <div
                      key={idx}
                      className="p-1.5 rounded"
                      style={{ background: 'var(--tui-accent-purple)', color: 'var(--tui-bg)' }}
                    >
                      <div className="font-medium">⭐ {ss.chinese} ({ss.english})</div>
                      <div>{ss.base_meaning}</div>
                    </div>
                  ))}

                  {/* Interactions */}
                  {story.interactions?.length > 0 && (
                    <div className="tui-text-muted">
                      <span className="font-medium">Interactions: </span>
                      {story.interactions.map((i: any) => i.type).join(', ')}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
