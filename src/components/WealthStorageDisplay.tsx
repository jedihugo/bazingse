'use client';

import { tri, WEALTH } from '@/lib/t';

interface WealthStorageDisplayProps {
  chartData: any;
}

const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
  'Wood': 'tui-text-wood',
  'Fire': 'tui-text-fire',
  'Earth': 'tui-text-earth',
  'Metal': 'tui-text-metal',
  'Water': 'tui-text-water',
};

const ACTIVATION_STYLE: Record<string, { label: string; color: string }> = {
  'maximum': { label: 'MAX', color: 'var(--tui-wood)' },
  'activated': { label: 'ACT', color: 'var(--tui-water)' },
  'latent': { label: 'LAT', color: 'var(--tui-fg-muted)' },
};

export default function WealthStorageDisplay({ chartData }: WealthStorageDisplayProps) {
  const ws = chartData?.wealth_storage_analysis;
  if (!ws || !ws.wealth_storage_branch) return null;

  const storages: any[] = ws.storages || [];
  const wealthColor = ELEMENT_TO_TUI_CLASS[ws.wealth_element] || 'tui-text';
  const dmColor = ELEMENT_TO_TUI_CLASS[ws.daymaster_element] || 'tui-text';

  return (
    <div className="tui-frame mt-2">
      <div className="tui-frame-title flex items-center justify-between">
        <span>{tri(WEALTH.title)}</span>
        <span>
          <span className={dmColor}>{ws.daymaster_stem}</span>
          {' → '}
          <span className={wealthColor}>{ws.wealth_element}</span>
          {' → '}
          <span className="tui-text-dim">{ws.wealth_storage_branch}</span>
        </span>
      </div>

      <div className="p-2 font-mono space-y-1">
        {storages.length === 0 ? (
          <div className="tui-text-muted text-center py-1">
            No {ws.wealth_storage_branch} branch in chart — no storage
          </div>
        ) : (
          storages.map((s: any, i: number) => {
            const act = ACTIVATION_STYLE[s.activation_level] || ACTIVATION_STYLE['latent'];
            return (
              <div key={i} className="flex items-center gap-2 flex-wrap">
                {/* Position */}
                <span className="w-12 tui-text-dim text-right">{s.position}</span>

                {/* Pillar */}
                <span className={wealthColor}>{s.pillar_chinese || s.pillar}</span>

                {/* Large badge */}
                {s.is_large && (
                  <span
                    className="text-xs px-1"
                    style={{ background: 'var(--tui-earth)', color: 'var(--tui-bg)' }}
                  >LARGE</span>
                )}

                {/* Activation level */}
                <span
                  className="text-xs px-1"
                  style={{ color: act.color, border: `1px solid ${act.color}` }}
                >{act.label}</span>

                {/* Filler indicator */}
                <span className={s.is_filled ? 'tui-text-wood' : 'tui-text-muted'}>
                  {s.is_filled ? '填' : '—'}
                </span>

                {/* Opener indicator */}
                <span className={s.is_opened ? 'tui-text-fire' : 'tui-text-muted'}>
                  {s.is_opened ? '冲' : '—'}
                </span>

                {/* Detail on where filler/opener came from */}
                {(s.filler_positions?.length > 0 || s.opener_positions?.length > 0) && (
                  <span className="tui-text-muted text-xs">
                    {s.filler_positions?.length > 0 && `fill:${s.filler_positions.join(',')}`}
                    {s.filler_positions?.length > 0 && s.opener_positions?.length > 0 && ' '}
                    {s.opener_positions?.length > 0 && `open:${s.opener_positions.join(',')}`}
                  </span>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Summary footer */}
      <div className="border-t tui-border-color px-2 py-1 tui-text-muted text-xs">
        {ws.summary}
      </div>
    </div>
  );
}
