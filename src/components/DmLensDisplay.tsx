'use client';

import { useMemo } from 'react';
import { useT } from './LanguageProvider';
import { WUXING } from '@/lib/t';

interface DmLensDisplayProps {
  chartData: any;
}

// Element to TUI color class
const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
  'Wood': 'tui-text-wood',
  'Fire': 'tui-text-fire',
  'Earth': 'tui-text-earth',
  'Metal': 'tui-text-metal',
  'Water': 'tui-text-water',
};

// Element Chinese characters
const ELEMENT_CHINESE: Record<string, string> = {
  'Wood': '木', 'Fire': '火', 'Earth': '土', 'Metal': '金', 'Water': '水',
};

// ASCII bar helper
function generateBar(pct: number, width: number = 12): { filled: string; empty: string } {
  const filled = Math.round((pct / 100) * width);
  return {
    filled: '█'.repeat(Math.min(filled, width)),
    empty: '░'.repeat(Math.max(0, width - filled)),
  };
}

export default function DmLensDisplay({ chartData }: DmLensDisplayProps) {
  const { t } = useT();

  const lens = chartData?.dm_lens;
  if (!lens) return null;

  const dmColorClass = ELEMENT_TO_TUI_CLASS[lens.dmElement] || 'tui-text';

  return (
    <div className="tui-frame mt-2">
      {/* Header */}
      <div className="tui-frame-title flex items-center justify-between">
        <span>{t(WUXING.dm_lens)}</span>
        <span className="tui-text-muted text-xs">
          <span className={dmColorClass}>{lens.dmStem}</span>
          {' '}{ELEMENT_CHINESE[lens.dmElement]}
          {' '}{lens.dmPercent}%
          {' '}{lens.dmStrengthZh}
          {lens.seasonalState && <> · 令{lens.seasonalState}</>}
        </span>
      </div>

      {/* Rows */}
      <div className="p-2 space-y-0 font-mono text-xs">
        {lens.rows.map((row: any, i: number) => {
          const colorClass = ELEMENT_TO_TUI_CLASS[row.element] || 'tui-text';
          const bar = generateBar(row.percent);
          const isSupport = row.role === 'companion' || row.role === 'resource';

          return (
            <div key={row.role}>
              {/* Separator before drain section */}
              {i === 2 && (
                <div className="flex items-center gap-2 py-0.5 tui-text-muted">
                  <span className="flex-1 border-t tui-border-color" />
                  <span className="text-[10px]">
                    {t(WUXING.support)} {lens.supportPercent}%
                  </span>
                  <span className="flex-1 border-t tui-border-color" />
                </div>
              )}

              <div className="flex items-start gap-1 py-0.5">
                {/* Role label */}
                <span className="w-[72px] shrink-0 tui-text-dim truncate">
                  {row.tenGodZh} {row.roleZh.split(' ')[1]}
                </span>

                {/* Element + bar */}
                <span className={`w-5 shrink-0 ${colorClass}`}>
                  {ELEMENT_CHINESE[row.element]}
                </span>
                <span className="tui-bar shrink-0">
                  <span className={colorClass}>{bar.filled}</span>
                  <span className="tui-text-muted">{bar.empty}</span>
                </span>

                {/* Percentage */}
                <span className="w-8 shrink-0 text-right tui-text-dim">
                  {Math.round(row.percent)}%
                </span>
              </div>

              {/* Narrative */}
              <div className="pl-[76px] pb-1 tui-text-muted text-[10px] leading-tight">
                {row.narrative}
              </div>
            </div>
          );
        })}

        {/* Drain footer */}
        <div className="flex items-center gap-2 py-0.5 tui-text-muted">
          <span className="flex-1 border-t tui-border-color" />
          <span className="text-[10px]">
            {t(WUXING.drain)} {lens.drainPercent}%
          </span>
          <span className="flex-1 border-t tui-border-color" />
        </div>

        {/* Ratio */}
        <div className="text-center py-1 tui-text-dim text-[10px]">
          {t(WUXING.support)} {lens.supportPercent}% : {t(WUXING.drain)} {lens.drainPercent}% → {lens.ratio}
        </div>

        {/* Cross-patterns */}
        {lens.crossPatterns && lens.crossPatterns.length > 0 && (
          <div className="pt-1 border-t tui-border-color space-y-0.5">
            {lens.crossPatterns.map((p: any) => (
              <div key={p.id} className="flex gap-2 text-[10px]">
                <span className="tui-text-dim shrink-0">{p.nameZh}</span>
                <span className="tui-text-muted">{p.narrative}</span>
              </div>
            ))}
          </div>
        )}

        {/* Synthesis */}
        {lens.synthesis && (
          <div className="pt-1 border-t tui-border-color text-[10px] tui-text leading-tight">
            {lens.synthesis}
          </div>
        )}
      </div>
    </div>
  );
}
