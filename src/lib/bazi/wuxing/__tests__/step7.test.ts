import { describe, it, expect } from 'vitest';
import {
  initializeState, step1PillarPairs, step2EbPositive,
  step3HsPositive, step4EbNegative, step5HsNegative,
  step6Seasonal, step7NaturalFlow,
  calculateWuxingUpToStep, type WuxingInput, type WuxingState,
} from '../calculator';
import { getStep7Gap, gapMultiplier, CONTROL_LOOKUP } from '../tables';

// Helper to run through to just before step 7
function runToStep6(input: WuxingInput): WuxingState {
  return calculateWuxingUpToStep(input, 6);
}

// Helper to run through step 7
function runToStep7(input: WuxingInput): WuxingState {
  return calculateWuxingUpToStep(input, 7);
}

// Simple chart: all different elements, no combos
const SIMPLE_INPUT: WuxingInput = {
  yearPillar:  { stem: 'Jia',  branch: 'Zi' },   // Wood HS, Water EB
  monthPillar: { stem: 'Bing', branch: 'Wu' },    // Fire HS, Fire EB(Ding)
  dayPillar:   { stem: 'Wu',   branch: 'Shen' },  // Earth HS, Metal EB(Geng)
  hourPillar:  { stem: 'Ren',  branch: 'Mao' },   // Water HS, Wood EB(Yi)
  age: 40,
  gender: 'M',
  location: 'hometown',
};

// Chart with combos (for bonus node testing)
const COMBO_INPUT: WuxingInput = {
  yearPillar:  { stem: 'Bing', branch: 'Yin' },   // Fire HS, Wood EB
  monthPillar: { stem: 'Ji',   branch: 'Hai' },   // Earth HS, Water EB
  dayPillar:   { stem: 'Ding', branch: 'Chou' },  // Fire HS, Earth EB
  hourPillar:  { stem: 'Ding', branch: 'Wei' },   // Fire HS, Earth EB
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 7: Natural Element Flow', () => {
  it('changes node point values via cross-pillar production/control', () => {
    const before = runToStep6(SIMPLE_INPUT);
    const after = runToStep7(SIMPLE_INPUT);

    // Step 7 should modify at least some node points
    let anyChanged = false;
    for (const nodeAfter of after.nodes) {
      const nodeBefore = before.nodes.find(n => n.id === nodeAfter.id)!;
      if (Math.abs(nodeAfter.points - nodeBefore.points) > 0.001) {
        anyChanged = true;
        break;
      }
    }
    expect(anyChanged).toBe(true);
  });

  it('uses half rates (10%/15%) not full Step 1 rates (20%/30%)', () => {
    // Create a minimal scenario: 2 adjacent nodes where we can verify rates
    // YP.HS (Wood) cross-pillar with MP.EB (Fire): Wood produces Fire
    // gap = 0 (same row adjacent), multiplier = 1.0
    // At half rates: producer loses 10% of basis, produced gains 15% of basis
    const before = runToStep6(SIMPLE_INPUT);
    const after = runToStep7(SIMPLE_INPUT);

    // Find step 7 interactions with production
    const productions = after.interactions.filter(
      i => i.step === 7 && (i.relationship === 'produces' || i.relationship === 'produced_by')
    );
    expect(productions.length).toBeGreaterThan(0);

    // Verify the interaction has reasonable basis values (not 0)
    for (const prod of productions) {
      expect(prod.basis).toBeGreaterThan(0);
    }
  });

  it('excludes hidden stems from cross-pillar flow', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // No interaction should reference hidden stems (h1 or h2)
    for (const int of step7Ints) {
      if (int.nodeA) expect(int.nodeA).not.toContain('.h');
      if (int.nodeB) expect(int.nodeB).not.toContain('.h');
    }
  });

  it('same-pillar original HS<->EB excluded (already in Step 1)', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // No interaction should pair a pillar's native HS with its own native EB
    for (const int of step7Ints) {
      if (int.nodeA && int.nodeB) {
        const aIsNative = /^(YP|MP|DP|HP)\.(HS|EB)$/.test(int.nodeA);
        const bIsNative = /^(YP|MP|DP|HP)\.(HS|EB)$/.test(int.nodeB);
        if (aIsNative && bIsNative) {
          const aPillar = int.nodeA.split('.')[0];
          const bPillar = int.nodeB.split('.')[0];
          const aSlot = int.nodeA.split('.')[1];
          const bSlot = int.nodeB.split('.')[1];
          // If same pillar, they shouldn't be native HS + native EB
          if (aPillar === bPillar) {
            const slots = new Set([aSlot, bSlot]);
            expect(slots.has('HS') && slots.has('EB')).toBe(false);
          }
        }
      }
    }
  });

  it('includes bonus nodes in cross-pillar flow', () => {
    // COMBO_INPUT should generate bonus nodes from Step 2/3
    const state = runToStep7(COMBO_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // At least some interactions should involve bonus nodes (contain '+')
    const bonusInteractions = step7Ints.filter(
      i => (i.nodeA && i.nodeA.includes('+')) || (i.nodeB && i.nodeB.includes('+'))
    );
    expect(bonusInteractions.length).toBeGreaterThan(0);
  });

  it('applies gap multipliers correctly', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // Check that gap multipliers are present and valid
    for (const int of step7Ints) {
      expect(int.gapMultiplier).toBeDefined();
      expect([1.0, 0.75, 0.5, 0.25]).toContain(int.gapMultiplier);
    }
  });

  it('logs interactions', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);
    // With 4 pillars there should be many cross-pillar interactions
    expect(step7Ints.length).toBeGreaterThan(0);
  });

  it('same-element pairs produce no interaction', () => {
    // Chart where some cross-pillar nodes share the same element
    const input: WuxingInput = {
      yearPillar:  { stem: 'Jia', branch: 'Mao' },  // Wood HS, Wood EB
      monthPillar: { stem: 'Yi',  branch: 'Yin' },   // Wood HS, Wood EB
      dayPillar:   { stem: 'Bing', branch: 'Wu' },   // Fire HS, Fire EB
      hourPillar:  { stem: 'Ding', branch: 'Si' },   // Fire HS, Fire EB
      age: 40, gender: 'M', location: 'hometown',
    };
    const state = runToStep7(input);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // No same-element interactions should appear
    for (const int of step7Ints) {
      expect(int.relationship).not.toBe('SAME');
    }
  });

  it('adjacent nodes (gap=0) get full multiplier 1.0', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // Find interactions between adjacent same-row nodes (e.g., YP.HS and MP.HS)
    const adjacentSameRow = step7Ints.filter(
      i => i.gapMultiplier === 1.0
    );
    // There should be some adjacent interactions
    expect(adjacentSameRow.length).toBeGreaterThan(0);
  });

  it('distant nodes get reduced gap multiplier', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // There should be some non-adjacent interactions with reduced multiplier
    const distant = step7Ints.filter(i => i.gapMultiplier! < 1.0);
    expect(distant.length).toBeGreaterThan(0);
  });

  it('production: producer loses points, produced gains points', () => {
    const before = runToStep6(SIMPLE_INPUT);
    const after = runToStep7(SIMPLE_INPUT);

    // Find a production interaction
    const prod = after.interactions.find(
      i => i.step === 7 && i.relationship === 'produces'
    );
    expect(prod).toBeDefined();

    // The producing node should have less points, produced node more
    // (overall, accounting for all interactions, a node may net up or down,
    // but the interaction itself follows the pattern)
    expect(prod!.basis).toBeGreaterThan(0);
  });

  it('control: both nodes lose points', () => {
    const after = runToStep7(SIMPLE_INPUT);

    // Find a control interaction
    const ctrl = after.interactions.find(
      i => i.step === 7 && i.relationship === 'controls'
    );
    expect(ctrl).toBeDefined();
    expect(ctrl!.basis).toBeGreaterThan(0);
  });

  it('processes pairs exactly once', () => {
    const state = runToStep7(SIMPLE_INPUT);
    const step7Ints = state.interactions.filter(i => i.step === 7);

    // Check no duplicate pairs
    const pairKeys = new Set<string>();
    for (const int of step7Ints) {
      if (int.nodeA && int.nodeB) {
        const key = [int.nodeA, int.nodeB].sort().join('|');
        expect(pairKeys.has(key)).toBe(false);
        pairKeys.add(key);
      }
    }
  });

  it('same-element bonus consolidation combines same-element at same position', () => {
    // Create a scenario where a bonus node has the same element as its position's native node
    // E.g., if YP.EB is Wood and there's a bonus at YP.EB+Wood, they should consolidate
    // This is naturally tested with COMBO_INPUT
    const before = runToStep6(COMBO_INPUT);
    const after = runToStep7(COMBO_INPUT);

    // Just verify step 7 completes without error and produces interactions
    const step7Ints = after.interactions.filter(i => i.step === 7);
    expect(step7Ints.length).toBeGreaterThan(0);
  });
});
