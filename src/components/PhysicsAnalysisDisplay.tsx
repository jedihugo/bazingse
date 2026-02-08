'use client';

import type { PhysicsAnalysis } from '@/types/bazi';

interface PhysicsAnalysisDisplayProps {
  physicsAnalysis: PhysicsAnalysis;
  mappings?: any;
}

// Element to TUI color class
const ELEMENT_COLOR: Record<string, string> = {
  Wood: 'tui-text-wood',
  Fire: 'tui-text-fire',
  Earth: 'tui-text-earth',
  Metal: 'tui-text-metal',
  Water: 'tui-text-water',
};

// Outcome to display style
const OUTCOME_STYLE: Record<string, { label: string; color: string }> = {
  harmonious: { label: 'Harmonious', color: 'tui-text-wood' },
  overwhelming: { label: 'Overwhelming', color: 'tui-text-fire' },
  insufficient: { label: 'Insufficient', color: 'tui-text-muted' },
  destructive: { label: 'Destructive', color: 'tui-text-fire' },
  reversed: { label: 'Reversed', color: 'tui-text-water' },
  transformative: { label: 'Transformative', color: 'tui-text-earth' },
  stalemate: { label: 'Stalemate', color: 'tui-text-metal' },
};

export default function PhysicsAnalysisDisplay({ physicsAnalysis, mappings }: PhysicsAnalysisDisplayProps) {
  const { element_states, chain_reactions, stem_interactions } = physicsAnalysis;

  const hasContent = element_states.length > 0 || chain_reactions.length > 0 || stem_interactions.length > 0;

  if (!hasContent) {
    return (
      <div className="tui-frame mt-2">
        <div className="tui-frame-title">PHYSICS 物理派</div>
        <div className="p-2 tui-text-muted text-xs font-mono">
          No physics effects detected in this chart.
        </div>
      </div>
    );
  }

  return (
    <div className="tui-frame mt-2">
      <div className="tui-frame-title flex items-center justify-between">
        <span>PHYSICS 物理派</span>
        <span className="tui-text-muted text-xs">
          {stem_interactions.length} effects
          {element_states.length > 0 && ` | ${element_states.length} states`}
          {chain_reactions.length > 0 && ` | ${chain_reactions.length} chains`}
        </span>
      </div>

      {/* Element States */}
      {element_states.length > 0 && (
        <div className="border-b tui-border-color p-2">
          <div className="text-[10px] tui-text-dim mb-1 font-mono">ELEMENT STATES</div>
          <div className="space-y-1">
            {element_states.map((state) => (
              <div key={state.state_id} className="font-mono text-xs">
                <div className="flex items-center gap-2">
                  <span className={`font-bold ${ELEMENT_COLOR[state.base_element] || ''}`}>
                    {state.name_zh} {state.name_en}
                  </span>
                  <span className="tui-text-muted">
                    {state.trigger_element}/{state.base_element} = {state.ratio}x
                  </span>
                  <span className="tui-text-fire text-[10px]">
                    ({(state.production_factor * 100).toFixed(0)}% output)
                  </span>
                </div>
                <div className="text-[10px] tui-text-muted pl-2">
                  {state.description_en}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Chain Reactions */}
      {chain_reactions.length > 0 && (
        <div className="border-b tui-border-color p-2">
          <div className="text-[10px] tui-text-dim mb-1 font-mono">CHAIN REACTIONS</div>
          <div className="space-y-1">
            {chain_reactions.map((chain, idx) => (
              <div key={idx} className="font-mono text-xs">
                <span className="tui-text-fire">{chain.trigger_name_zh}</span>
                {chain.steps.map((step) => (
                  <div key={step.step} className="pl-2 text-[10px] tui-text-muted">
                    {step.step}. {step.effect}
                    <span className={step.effect_type === 'weaken' ? 'tui-text-fire' : 'tui-text-wood'}>
                      {' '}({(step.factor * 100).toFixed(0)}%)
                    </span>
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stem Interactions */}
      {stem_interactions.length > 0 && (
        <div className="p-2">
          <div className="text-[10px] tui-text-dim mb-1 font-mono">STEM IMAGERY</div>
          <div className="space-y-1.5">
            {stem_interactions.map((interaction, idx) => {
              const outcomeStyle = OUTCOME_STYLE[interaction.outcome] || { label: interaction.outcome, color: 'tui-text-muted' };
              return (
                <div key={idx} className="font-mono text-xs border-l-2 pl-2" style={{
                  borderColor: interaction.outcome === 'harmonious' ? 'var(--tui-wood)' :
                               interaction.outcome === 'overwhelming' || interaction.outcome === 'destructive' ? 'var(--tui-fire)' :
                               interaction.outcome === 'reversed' ? 'var(--tui-water)' :
                               'var(--tui-border)'
                }}>
                  <div className="flex items-center gap-2">
                    <span className={outcomeStyle.color}>{outcomeStyle.label}</span>
                    <span className="tui-text-muted">{interaction.source} → {interaction.target}</span>
                    {interaction.state_blocked && (
                      <span className="tui-text-fire text-[10px]">[BLOCKED: {interaction.state_name}]</span>
                    )}
                  </div>
                  <div className="text-[10px] tui-text-muted">
                    {interaction.zh}
                  </div>
                  <div className="text-[10px] tui-text-dim">
                    {interaction.en}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
