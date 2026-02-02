'use client';

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

// Get element from stem/branch element string (removes Yang/Yin prefix)
function getBaseElement(elementStr: string): string {
  return elementStr.replace('Yang ', '').replace('Yin ', '');
}

export default function PillarCard({ pillar, type, index, mappings, isLuck, isEmpty }: PillarCardProps) {
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
                    flex: idx === 0 ? '2' : idx === 1 ? '1.5' : '1',
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
    </div>
  );
}
