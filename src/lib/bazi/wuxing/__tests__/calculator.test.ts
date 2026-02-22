import { describe, it, expect } from 'vitest';
import {
  calculateWuxing,
  calculateWuxingUpToStep,
  initializeState,
  calculatePillarPriority,
  step1PillarPairs,
  step2EbPositive,
  step3HsPositive,
  step4EbNegative,
  step5HsNegative,
  step6Seasonal,
  step7NaturalFlow,
  step8Report,
  step9BalanceSim,
  type WuxingInput,
  type WuxingResult,
  type WuxingState,
} from '../calculator';

// =============================================================================
// Test chart: 丙寅·己亥·丁丑·丁未 (age 40, male, hometown)
// =============================================================================

const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

// =============================================================================
// 1. calculateWuxing — full pipeline returns valid WuxingResult
// =============================================================================

describe('calculateWuxing', () => {
  let result: WuxingResult;

  beforeAll(() => {
    result = calculateWuxing(INPUT);
  });

  it('returns all required top-level fields', () => {
    expect(result).toHaveProperty('nodes');
    expect(result).toHaveProperty('bonusNodes');
    expect(result).toHaveProperty('elements');
    expect(result).toHaveProperty('dayMaster');
    expect(result).toHaveProperty('gods');
    expect(result).toHaveProperty('interactions');
  });

  it('day master is Ding Fire', () => {
    expect(result.dayMaster.stem).toBe('Ding');
    expect(result.dayMaster.element).toBe('Fire');
  });

  it('element percentages sum to ~100%', () => {
    const totalPct = Object.values(result.elements)
      .reduce((sum, e) => sum + e.percent, 0);
    expect(totalPct).toBeCloseTo(100, 0);
  });

  it('five gods use all 5 distinct elements', () => {
    const godElements = new Set([
      result.gods.useful,
      result.gods.favorable,
      result.gods.unfavorable,
      result.gods.enemy,
      result.gods.idle,
    ]);
    expect(godElements.size).toBe(5);
  });

  it('elements are ranked 1-5 with no duplicates', () => {
    const ranks = Object.values(result.elements).map(e => e.rank).sort();
    expect(ranks).toEqual([1, 2, 3, 4, 5]);
  });

  it('bonusNodes is an array (populated by Step 2)', () => {
    expect(Array.isArray(result.bonusNodes)).toBe(true);
    // Step 2 detects combos for this chart (Yin+Hai 六合, Chou+Hai 半三会, Hai+Wei 拱合)
    expect(result.bonusNodes.length).toBeGreaterThan(0);
  });

  it('interactions is an array with Step 1 entries', () => {
    expect(Array.isArray(result.interactions)).toBe(true);
    // Step 1 produces 4 pillar pair interactions for this chart
    expect(result.interactions.length).toBeGreaterThanOrEqual(4);
  });

  it('node initial points are preserved in output', () => {
    // HS nodes always start at 10
    expect(result.nodes['YP.HS'].initial).toBe(10);
    expect(result.nodes['MP.HS'].initial).toBe(10);
    expect(result.nodes['DP.HS'].initial).toBe(10);
    expect(result.nodes['HP.HS'].initial).toBe(10);

    // After Step 1, HS/EB nodes have deltas; hidden stems remain unchanged
    for (const node of Object.values(result.nodes)) {
      expect(node.delta).toBe(node.final - node.initial);
    }
  });
});

// =============================================================================
// 2. initializeState — correct node creation
// =============================================================================

describe('initializeState', () => {
  let state: WuxingState;

  beforeAll(() => {
    state = initializeState(INPUT);
  });

  it('creates correct total number of nodes', () => {
    // YP: Yin has 3 hidden stems -> 1 HS + 3 EB = 4
    // MP: Hai has 2 hidden stems -> 1 HS + 2 EB = 3
    // DP: Chou has 3 hidden stems -> 1 HS + 3 EB = 4
    // HP: Wei has 3 hidden stems -> 1 HS + 3 EB = 4
    // Total: 4 + 3 + 4 + 4 = 15
    expect(state.nodes).toHaveLength(15);
  });

  it('creates 4 HS nodes (one per pillar)', () => {
    const hsNodes = state.nodes.filter(n => n.slot === 'HS');
    expect(hsNodes).toHaveLength(4);
  });

  it('all HS nodes have 10 points', () => {
    const hsNodes = state.nodes.filter(n => n.slot === 'HS');
    for (const node of hsNodes) {
      expect(node.points).toBe(10);
      expect(node.initialPoints).toBe(10);
    }
  });

  it('YP.HS is Bing Fire Yang', () => {
    const node = state.nodes.find(n => n.id === 'YP.HS')!;
    expect(node.stem).toBe('Bing');
    expect(node.element).toBe('Fire');
    expect(node.polarity).toBe('Yang');
  });

  it('DP.HS is Ding Fire Yin', () => {
    const node = state.nodes.find(n => n.id === 'DP.HS')!;
    expect(node.stem).toBe('Ding');
    expect(node.element).toBe('Fire');
    expect(node.polarity).toBe('Yin');
  });

  it('YP.EB (Yin main qi) is Jia Wood 8pts', () => {
    const node = state.nodes.find(n => n.id === 'YP.EB')!;
    expect(node.stem).toBe('Jia');
    expect(node.element).toBe('Wood');
    expect(node.points).toBe(8);
  });

  it('YP.EB.h1 (Yin hidden 1) is Bing Fire 3pts', () => {
    const node = state.nodes.find(n => n.id === 'YP.EB.h1')!;
    expect(node.stem).toBe('Bing');
    expect(node.element).toBe('Fire');
    expect(node.points).toBe(3);
  });

  it('YP.EB.h2 (Yin hidden 2) is Wu Earth 1pt', () => {
    const node = state.nodes.find(n => n.id === 'YP.EB.h2')!;
    expect(node.stem).toBe('Wu');
    expect(node.element).toBe('Earth');
    expect(node.points).toBe(1);
  });

  it('MP.EB (Hai main qi) is Ren Water 8pts', () => {
    const node = state.nodes.find(n => n.id === 'MP.EB')!;
    expect(node.stem).toBe('Ren');
    expect(node.element).toBe('Water');
    expect(node.points).toBe(8);
  });

  it('MP.EB.h1 (Hai hidden 1) is Jia Wood 3pts', () => {
    const node = state.nodes.find(n => n.id === 'MP.EB.h1')!;
    expect(node.stem).toBe('Jia');
    expect(node.element).toBe('Wood');
    expect(node.points).toBe(3);
  });

  it('MP branch (Hai) has no h2 hidden stem', () => {
    const node = state.nodes.find(n => n.id === 'MP.EB.h2');
    expect(node).toBeUndefined();
  });

  it('season is Water (month branch Hai)', () => {
    expect(state.season).toBe('Water');
  });

  it('pillarPriority starts with DP for age 40', () => {
    expect(state.pillarPriority[0]).toBe('DP');
  });

  it('bonusNodes starts empty', () => {
    expect(state.bonusNodes).toHaveLength(0);
  });

  it('interactions starts empty', () => {
    expect(state.interactions).toHaveLength(0);
  });

  it('attentionMap starts empty', () => {
    expect(state.attentionMap.size).toBe(0);
  });
});

// =============================================================================
// 3. initializeState — HP fallback when hourPillar is missing
// =============================================================================

describe('initializeState — no hourPillar', () => {
  it('uses DP stem+branch as HP fallback', () => {
    const noHourInput: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },
      monthPillar: { stem: 'Ji', branch: 'Hai' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      age: 40,
      gender: 'M',
      location: 'hometown',
    };

    const state = initializeState(noHourInput);
    const hpHs = state.nodes.find(n => n.id === 'HP.HS')!;
    const dpHs = state.nodes.find(n => n.id === 'DP.HS')!;

    // HP should mirror DP
    expect(hpHs.stem).toBe(dpHs.stem);
    expect(hpHs.element).toBe(dpHs.element);

    // HP.EB should also mirror DP.EB
    const hpEb = state.nodes.find(n => n.id === 'HP.EB')!;
    const dpEb = state.nodes.find(n => n.id === 'DP.EB')!;
    expect(hpEb.stem).toBe(dpEb.stem);
    expect(hpEb.element).toBe(dpEb.element);
  });
});

// =============================================================================
// 4. calculatePillarPriority
// =============================================================================

describe('calculatePillarPriority', () => {
  it('age 10 -> YP first', () => {
    const prio = calculatePillarPriority(10);
    expect(prio[0]).toBe('YP');
    expect(prio[1]).toBe('DP'); // DP always 2nd
    expect(prio).toHaveLength(4);
  });

  it('age 25 -> MP first, DP second', () => {
    const prio = calculatePillarPriority(25);
    expect(prio[0]).toBe('MP');
    expect(prio[1]).toBe('DP');
  });

  it('age 40 -> DP first', () => {
    const prio = calculatePillarPriority(40);
    expect(prio[0]).toBe('DP');
    // DP is already first, so 2nd should be next closest
  });

  it('age 40 -> priority is DP, MP, HP, YP', () => {
    const prio = calculatePillarPriority(40);
    expect(prio).toEqual(['DP', 'MP', 'HP', 'YP']);
  });

  it('age 55 -> HP first, DP second', () => {
    const prio = calculatePillarPriority(55);
    expect(prio[0]).toBe('HP');
    expect(prio[1]).toBe('DP');
  });

  it('boundary: age 16 -> YP (last year of YP bracket)', () => {
    expect(calculatePillarPriority(16)[0]).toBe('YP');
  });

  it('boundary: age 17 -> MP (first year of MP bracket)', () => {
    expect(calculatePillarPriority(17)[0]).toBe('MP');
  });

  it('boundary: age 33 -> DP', () => {
    expect(calculatePillarPriority(33)[0]).toBe('DP');
  });

  it('boundary: age 49 -> HP', () => {
    expect(calculatePillarPriority(49)[0]).toBe('HP');
  });

  it('always contains all 4 pillars', () => {
    for (const age of [0, 10, 16, 17, 32, 33, 48, 49, 64]) {
      const prio = calculatePillarPriority(age);
      expect(prio).toHaveLength(4);
      expect(new Set(prio).size).toBe(4);
    }
  });
});

// =============================================================================
// 5. step8Report — element aggregation
// =============================================================================

describe('step8Report', () => {
  it('percentages sum to ~100%', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const totalPct = Object.values(report).reduce((s, e) => s + e.percent, 0);
    expect(totalPct).toBeCloseTo(100, 0);
  });

  it('ranks are 1-5 with no duplicates', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const ranks = Object.values(report).map(e => e.rank).sort();
    expect(ranks).toEqual([1, 2, 3, 4, 5]);
  });

  it('rank 1 has the highest total', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const entries = Object.values(report);
    const rank1 = entries.find(e => e.rank === 1)!;
    for (const entry of entries) {
      expect(rank1.total).toBeGreaterThanOrEqual(entry.total);
    }
  });

  it('totals are non-negative', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    for (const entry of Object.values(report)) {
      expect(entry.total).toBeGreaterThanOrEqual(0);
    }
  });
});

// =============================================================================
// 6. step9BalanceSim — five gods
// =============================================================================

describe('step9BalanceSim', () => {
  it('returns 5 distinct elements', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const gods = step9BalanceSim(state, report);
    const elements = new Set([gods.useful, gods.favorable, gods.unfavorable, gods.enemy, gods.idle]);
    expect(elements.size).toBe(5);
  });

  it('favorable produces useful', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const gods = step9BalanceSim(state, report);

    // Production cycle: Wood->Fire->Earth->Metal->Water->Wood
    const produces: Record<string, string> = {
      Wood: 'Fire', Fire: 'Earth', Earth: 'Metal', Metal: 'Water', Water: 'Wood',
    };
    expect(produces[gods.favorable]).toBe(gods.useful);
  });

  it('enemy produces unfavorable', () => {
    const state = initializeState(INPUT);
    const report = step8Report(state);
    const gods = step9BalanceSim(state, report);

    const produces: Record<string, string> = {
      Wood: 'Fire', Fire: 'Earth', Earth: 'Metal', Metal: 'Water', Water: 'Wood',
    };
    expect(produces[gods.enemy]).toBe(gods.unfavorable);
  });
});

// =============================================================================
// 7. calculateWuxingUpToStep
// =============================================================================

describe('calculateWuxingUpToStep', () => {
  it('step=0 returns initialized state', () => {
    const state = calculateWuxingUpToStep(INPUT, 0);
    expect(state.nodes.length).toBeGreaterThan(0);
    expect(state.season).toBe('Water');
  });

  it('step=1 modifies HS/EB points from step=0', () => {
    const s0 = calculateWuxingUpToStep(INPUT, 0);
    const s1 = calculateWuxingUpToStep(INPUT, 1);

    // Step 1 changes HS and EB main qi nodes
    const ypHs0 = s0.nodes.find(n => n.id === 'YP.HS')!;
    const ypHs1 = s1.nodes.find(n => n.id === 'YP.HS')!;
    expect(ypHs1.points).not.toBe(ypHs0.points);
  });

  it('step=6 applies seasonal multipliers (points differ from step=5)', () => {
    const s5 = calculateWuxingUpToStep(INPUT, 5);
    const s6 = calculateWuxingUpToStep(INPUT, 6);

    // Step 6 applies seasonal multipliers, so at least some nodes should differ
    let anyDifferent = false;
    for (let i = 0; i < s5.nodes.length; i++) {
      if (s5.nodes[i].points !== s6.nodes[i].points) {
        anyDifferent = true;
        break;
      }
    }
    expect(anyDifferent).toBe(true);
  });

  it('step=7 modifies node points from step=6 (natural element flow)', () => {
    const s6 = calculateWuxingUpToStep(INPUT, 6);
    const s7 = calculateWuxingUpToStep(INPUT, 7);

    // Step 7 applies cross-pillar interactions, so points should differ
    let anyDifferent = false;
    for (let i = 0; i < s6.nodes.length; i++) {
      if (s6.nodes[i].points !== s7.nodes[i].points) {
        anyDifferent = true;
        break;
      }
    }
    expect(anyDifferent).toBe(true);
  });
});

// =============================================================================
// 8. Stub functions are exported and pass through
// =============================================================================

describe('step return values', () => {
  it('step7NaturalFlow mutates and returns the same state object', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    state = step2EbPositive(state);
    state = step3HsPositive(state);
    state = step4EbNegative(state);
    state = step5HsNegative(state);
    state = step6Seasonal(state);
    const result = step7NaturalFlow(state);
    expect(result).toBe(state);
  });

  it('step2EbPositive mutates and returns the same state object', () => {
    const state = initializeState(INPUT);
    step1PillarPairs(state);
    const result = step2EbPositive(state);
    expect(result).toBe(state);
  });

  it('step1PillarPairs mutates and returns the same state object', () => {
    const state = initializeState(INPUT);
    const result = step1PillarPairs(state);
    expect(result).toBe(state);
  });
});
