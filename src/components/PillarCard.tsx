'use client';

import { useState } from 'react';

interface QiPhaseAnalysis {
  phase_id: string;
  phase_chinese: string;
  phase_english: string;
  strength: string;
  interpretation: string;
  tandem_effects: Array<{ shen_sha: string; effect: string }>;
}

interface Pillar {
  label: string;
  stem: { chinese: string; element: string; color: string };
  stemName: string;
  branch: { chinese: string; animal: string; element: string; color: string };
  branchName: string;
  hiddenStems: Record<string, string>;
  hiddenQi: Record<string, number>;
  tenGod: string | null;
  isDayMaster?: boolean;
  isUnknown?: boolean;
  qiPhase?: string | null;
  qiPhaseAnalysis?: QiPhaseAnalysis;
  stemTransformations: any[];
  branchTransformations: any[];
  stemCombinations: any[];
  branchCombinations: any[];
  stemNegatives: any[];
  branchNegatives: any[];
  branchWealthStorage: any[];
  isLuckPillar?: boolean;
  isAnnualLuck?: boolean;
  timing?: { start_year: number; end_year: number; start_age: number; end_age: number };
  year?: number;
}

interface PillarCardProps {
  pillar: Pillar;
  type: 'stem' | 'branch';
  index: number;
  mappings: any;
  isLuck?: boolean;
  isTalisman?: boolean;
  isLocation?: boolean;
  isOverseas?: boolean;
  isBirthplace?: boolean;
  isEmpty?: boolean;
  hoveredInteractionId?: string | null;
  onHoverInteraction?: (id: string | null) => void;
}

// Element to TUI color class mapping
const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
  'Wood': 'tui-text-wood',
  'Fire': 'tui-text-fire',
  'Earth': 'tui-text-earth',
  'Metal': 'tui-text-metal',
  'Water': 'tui-text-water',
};

// Stem to element mapping (reliable local lookup)
const STEM_TO_ELEMENT: Record<string, string> = {
  'Jia': 'Wood', 'Yi': 'Wood',
  'Bing': 'Fire', 'Ding': 'Fire',
  'Wu': 'Earth', 'Ji': 'Earth',
  'Geng': 'Metal', 'Xin': 'Metal',
  'Ren': 'Water', 'Gui': 'Water',
};

// Qi phase strength to TUI color style
const STRENGTH_STYLE: Record<string, string> = {
  'peak': 'var(--tui-fire)',
  'strong': 'var(--tui-wood)',
  'growing': 'var(--tui-wood-yin)',
  'moderate': 'var(--tui-earth)',
  'declining': 'var(--tui-metal)',
  'weak': 'var(--tui-water)',
  'dead': 'var(--tui-fg-muted)',
};

// Get element from stem/branch element string (removes Yang/Yin prefix)
function getBaseElement(elementStr: string): string {
  return elementStr.replace('Yang ', '').replace('Yin ', '');
}

export default function PillarCard({ pillar, type, index, mappings, isLuck, isEmpty }: PillarCardProps) {
  const [qiPhaseExpanded, setQiPhaseExpanded] = useState(false);

  // TUI style - simple uniform borders
  const getBorderStyle = (): React.CSSProperties => {
    const base: React.CSSProperties = {
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: 'var(--tui-border)',
    };

    if (isEmpty) {
      return { ...base, borderStyle: 'dashed', background: 'transparent' };
    }
    return base;
  };

  // Empty placeholder cell
  if (isEmpty) {
    return (
      <div className="w-28 flex-shrink-0">
        <div
          className="tui-cell flex items-center justify-center"
          style={{ ...getBorderStyle(), height: type === 'stem' ? '4rem' : '5rem' }}
        >
          <span className="tui-text-muted">{pillar.label || '---'}</span>
        </div>
      </div>
    );
  }

  if (type === 'stem') {
    const element = getBaseElement(pillar.stem?.element || 'Unknown');
    const colorClass = ELEMENT_TO_TUI_CLASS[element] || 'tui-text';

    return (
      <div className="w-28 flex-shrink-0">
        <div className="tui-cell p-1" style={{ ...getBorderStyle(), height: '4rem' }}>
          <div className="flex flex-col items-center justify-center h-full">
            <span className={`text-lg ${pillar.isUnknown ? 'tui-text-muted' : colorClass}`}>
              {pillar.stem?.chinese || '?'}
            </span>
            <span className="tui-text-dim">
              {pillar.isUnknown ? '?' : (index === 1 && !isLuck ? 'DM' : (pillar.tenGod || ''))}
            </span>
          </div>
        </div>
      </div>
    );
  }

  // Branch card
  const element = getBaseElement(pillar.branch?.element || 'Unknown');
  const colorClass = ELEMENT_TO_TUI_CLASS[element] || 'tui-text';
  const totalQi = Object.values(pillar.hiddenQi || {}).reduce((a: number, b: number) => a + b, 0);
  const qpa = pillar.qiPhaseAnalysis;

  return (
    <div className="w-28 flex-shrink-0">
      <div className="tui-cell relative" style={{ ...getBorderStyle(), height: '5rem' }}>
        {/* Main content */}
        <div className="flex flex-col items-center justify-center pt-2 pb-5">
          <span className={`text-lg ${pillar.isUnknown ? 'tui-text-muted' : colorClass}`}>
            {pillar.branch?.chinese || '?'}
          </span>
          {!pillar.isUnknown && pillar.branch?.animal && !['Fire', 'Water', 'Metal', 'Wood', 'Earth'].includes(pillar.branch.animal) && (
            <span className="tui-text-dim">{pillar.branch.animal}</span>
          )}
        </div>

        {/* Hidden Stems - bottom row */}
        {pillar.hiddenQi && Object.keys(pillar.hiddenQi).length > 0 && (
          <div
            className="absolute bottom-0 left-0 right-0 flex overflow-hidden"
            style={{ height: '1.25rem', borderTop: '1px solid var(--tui-border)' }}
          >
            {Object.entries(pillar.hiddenQi).map(([stemName, qi]: [string, number], idx: number) => {
              const stemMapping = mappings?.heavenly_stems?.[stemName] || {};
              const tenGod = pillar.hiddenStems?.[stemName] || '';
              const numStems = Object.keys(pillar.hiddenQi).length;
              const stemElement = STEM_TO_ELEMENT[stemName] || getBaseElement(stemMapping.element || 'Unknown');
              const stemColorClass = ELEMENT_TO_TUI_CLASS[stemElement] || 'tui-text';

              return (
                <div
                  key={stemName}
                  className="flex items-center justify-center overflow-hidden"
                  style={{
                    flex: '1',
                    borderRight: idx < numStems - 1 ? '1px solid var(--tui-border)' : 'none',
                    minWidth: 0,
                  }}
                  title={`${stemMapping.chinese || stemName} ${tenGod}`}
                >
                  <span className={`text-xs ${stemColorClass}`}>
                    {stemMapping.chinese || stemName.charAt(0)}
                  </span>
                  <span className="text-xs tui-text-muted">{tenGod}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Qi Phase Analysis — compact collapsible below branch */}
      {qpa && (
        <div
          className="cursor-pointer select-none"
          style={{
            borderLeft: '1px solid var(--tui-border)',
            borderRight: '1px solid var(--tui-border)',
            borderBottom: '1px solid var(--tui-border)',
            fontSize: '0.65rem',
            lineHeight: '1.1',
            background: 'var(--tui-bg-alt)',
          }}
          onClick={() => setQiPhaseExpanded(!qiPhaseExpanded)}
        >
          {/* Header: phase name + strength */}
          <div className="flex items-center justify-center gap-1 px-1 py-0.5">
            <span style={{ color: STRENGTH_STYLE[qpa.strength] || 'var(--tui-fg-dim)' }}>
              {qpa.phase_chinese}
            </span>
            <span className="tui-text-muted">
              {qpa.phase_english}
            </span>
          </div>

          {/* Expanded: interpretation + tandem effects */}
          {qiPhaseExpanded && (
            <div
              className="px-1 pb-1"
              style={{ borderTop: '1px dashed var(--tui-border-dim)' }}
            >
              <div className="tui-text-dim py-0.5" style={{ whiteSpace: 'normal' }}>
                {qpa.interpretation}
              </div>
              {qpa.tandem_effects && qpa.tandem_effects.length > 0 && (
                <div className="mt-0.5" style={{ borderTop: '1px dotted var(--tui-border-dim)' }}>
                  {qpa.tandem_effects.map((te, idx) => (
                    <div key={idx} className="py-0.5" style={{ whiteSpace: 'normal' }}>
                      <span style={{ color: 'var(--tui-accent-purple)' }}>{te.shen_sha}</span>
                      <span className="tui-text-dim"> {te.effect}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
