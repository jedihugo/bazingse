'use client';

import NarrativeCard from './NarrativeCard';

interface NarrativeDisplayProps {
  chartData: any;
}

export default function NarrativeDisplay({ chartData }: NarrativeDisplayProps) {
  const narrativeAnalysis = chartData?.narrative_analysis;
  const chronological = narrativeAnalysis?.all_chronological;

  if (!narrativeAnalysis || !chronological || chronological.length === 0) {
    return null;
  }

  return (
    <div className="narrative-panel">
      <div className="narrative-panel-inner">
        <div className="space-y-1.5">
          {chronological.map((entry: any) => (
            <NarrativeCard
              key={`chrono-${entry.seq}`}
              narrative={entry}
              mappings={chartData?.mappings}
            />
          ))}
        </div>
        <div className="mt-2 text-[9px] tui-text-dim font-mono text-right">
          {chronological.length} interactions (chronological)
        </div>
      </div>
    </div>
  );
}
