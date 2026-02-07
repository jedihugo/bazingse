'use client';

import BaZiChart from './BaZiChart';
import ElementAnalysis from './ElementAnalysis';

interface TimelineEntryProps {
  date: { year: number; month?: number; day?: number };
  chartData: any;
  isNatal?: boolean;
  onDelete?: () => void;
  isLoading?: boolean;
  error?: string | null;
}

function formatDateLabel(date: { year: number; month?: number; day?: number }): string {
  const parts = [date.year.toString()];
  if (date.month) {
    const monthName = new Date(2000, date.month - 1, 1).toLocaleString('default', { month: 'short' });
    parts.push(monthName);
  }
  if (date.day) {
    parts.push(date.day.toString());
  }
  return parts.join(' - ');
}

export default function TimelineEntry({
  date,
  chartData,
  isNatal = false,
  onDelete,
  isLoading = false,
  error = null,
}: TimelineEntryProps) {
  return (
    <div className={`tui-bg-panel tui-frame overflow-hidden ${isNatal ? '' : ''}`} style={isNatal ? { borderColor: 'var(--tui-accent-purple)' } : undefined}>
      {/* Header */}
      <div className={`flex items-center justify-between px-4 py-2 ${isNatal ? '' : 'tui-bg-alt'}`} style={isNatal ? { background: 'var(--tui-accent-purple)', opacity: 0.15 } : undefined}>
        <div className="flex items-center gap-2">
          <span className={`font-semibold ${isNatal ? '' : 'tui-text-dim'}`} style={isNatal ? { color: 'var(--tui-accent-purple)' } : undefined}>
            {isNatal ? 'Natal Chart' : formatDateLabel(date)}
          </span>
          {isNatal && (
            <span className="text-xs px-2 py-0.5 rounded" style={{ background: 'var(--tui-accent-purple)', color: 'var(--tui-bg)' }}>Birth</span>
          )}
          {chartData?.hs_10yl?.misc && (
            <span className="text-xs tui-text-muted">
              10Y Luck: {chartData.hs_10yl.misc.start_date?.split('-')[0]} - {chartData.hs_10yl.misc.end_date?.split('-')[0]}
            </span>
          )}
          {chartData?.dong_gong?.rating && (
            <span
              className="text-xs px-1.5 py-0.5 font-medium"
              style={{
                background: chartData.dong_gong.rating.value >= 4 ? 'color-mix(in srgb, var(--tui-wood) 20%, var(--tui-bg))'
                  : chartData.dong_gong.rating.value === 3 ? 'color-mix(in srgb, var(--tui-earth) 20%, var(--tui-bg))'
                  : 'color-mix(in srgb, var(--tui-fire) 20%, var(--tui-bg))',
                color: chartData.dong_gong.rating.value >= 4 ? 'var(--tui-wood)'
                  : chartData.dong_gong.rating.value === 3 ? 'var(--tui-earth)'
                  : 'var(--tui-fire)',
              }}
              title={`董公: ${chartData.dong_gong.officer?.chinese || ''} ${chartData.dong_gong.rating.chinese}`}
            >
              {chartData.dong_gong.rating.symbol} {chartData.dong_gong.rating.chinese}
            </span>
          )}
        </div>
        {!isNatal && onDelete && (
          <button
            onClick={onDelete}
            className="tui-text-muted p-1"
            style={{ '--hover-color': 'var(--tui-error)' } as React.CSSProperties}
            title="Remove entry"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>

      {/* Content */}
      <div className="p-2">
        {isLoading ? (
          <div className="py-8 text-center tui-text-muted">Loading...</div>
        ) : error ? (
          <div className="py-4 px-3 tui-frame text-sm rounded" style={{ borderColor: 'var(--tui-error)', color: 'var(--tui-error)' }}>{error}</div>
        ) : chartData ? (
          <>
            {/* Row 1: Natal only (Hour | Day | Month | Year) */}
            <BaZiChart
              chartData={chartData}
              showNatal={true}
              showLuck={false}
              showTalisman={false}
              showLocation={false}
            />

            {/* Row 2: Aligned comparison (Hourly|Daily|Monthly|Annual|10Y) */}
            {!isNatal && chartData?.analysis_info?.year && (
              <div className="mt-1">
                <BaZiChart
                  chartData={chartData}
                  showNatal={false}
                  showLuck={true}
                  showTalisman={false}
                  showLocation={false}
                />
              </div>
            )}

            {/* Element Analysis */}
            <ElementAnalysis chartData={chartData} />
          </>
        ) : (
          <div className="py-8 text-center tui-text-muted">No data</div>
        )}
      </div>
    </div>
  );
}
