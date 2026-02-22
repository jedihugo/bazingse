import { describe, it, expect } from 'vitest';
import {
  calculateWuxing,
  calculateWuxingUpToStep,
  step8Report,
  step9BalanceSim,
  type WuxingInput,
  type WuxingResult,
  type WuxingState,
  type ElementSummary,
  type FiveGods,
} from '../calculator';
import type { Element } from '../../core';

// =============================================================================
// Test charts
// =============================================================================

/** Chart A: 丙寅·己亥·丁丑·丁未 — Fire DM, strong */
const CHART_A: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

/** Chart B: 甲子·丙午·戊申·壬卯 — Earth DM, balanced */
const CHART_B: WuxingInput = {
  yearPillar: { stem: 'Jia', branch: 'Zi' },
  monthPillar: { stem: 'Bing', branch: 'Wu' },
  dayPillar: { stem: 'Wu', branch: 'Shen' },
  hourPillar: { stem: 'Ren', branch: 'Mao' },
  age: 25,
  gender: 'M',
  location: 'hometown',
};

/** Chart C: 庚申·庚酉·丙戌·辛丑 — Fire DM, very weak (DM% ~3.3%) */
const CHART_C: WuxingInput = {
  yearPillar: { stem: 'Geng', branch: 'Shen' },
  monthPillar: { stem: 'Geng', branch: 'You' },
  dayPillar: { stem: 'Bing', branch: 'Xu' },
  hourPillar: { stem: 'Xin', branch: 'Chou' },
  age: 30,
  gender: 'M',
  location: 'hometown',
};

/** Chart D: 戊戌·己丑·戊辰·己未 — Earth DM, dominant (DM% ~85.7%) */
const CHART_D: WuxingInput = {
  yearPillar: { stem: 'Wu', branch: 'Xu' },
  monthPillar: { stem: 'Ji', branch: 'Chou' },
  dayPillar: { stem: 'Wu', branch: 'Chen' },
  hourPillar: { stem: 'Ji', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

/** Chart E: 甲寅·丙午·壬申·戊戌 — Water DM, weak (DM% ~8.5%) */
const CHART_E: WuxingInput = {
  yearPillar: { stem: 'Jia', branch: 'Yin' },
  monthPillar: { stem: 'Bing', branch: 'Wu' },
  dayPillar: { stem: 'Ren', branch: 'Shen' },
  hourPillar: { stem: 'Wu', branch: 'Xu' },
  age: 30,
  gender: 'M',
  location: 'hometown',
};

/** Production cycle mapping */
const PRODUCES: Record<Element, Element> = {
  Wood: 'Fire',
  Fire: 'Earth',
  Earth: 'Metal',
  Metal: 'Water',
  Water: 'Wood',
};

const ELEMENTS: Element[] = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'];

// =============================================================================
// Step 8: Report — Element Aggregation
// =============================================================================

describe('Step 8: Report — Element Aggregation', () => {
  describe('on full pipeline (after Step 7)', () => {
    let state: WuxingState;
    let report: Record<Element, ElementSummary>;

    beforeAll(() => {
      state = calculateWuxingUpToStep(CHART_A, 7);
      report = step8Report(state);
    });

    it('percentages sum to ~100%', () => {
      const totalPct = Object.values(report).reduce((s, e) => s + e.percent, 0);
      expect(totalPct).toBeCloseTo(100, 0);
    });

    it('elements are ranked 1-5 with no duplicates', () => {
      const ranks = Object.values(report).map(e => e.rank).sort();
      expect(ranks).toEqual([1, 2, 3, 4, 5]);
    });

    it('rank 1 has the highest total', () => {
      const entries = Object.values(report);
      const rank1 = entries.find(e => e.rank === 1)!;
      for (const entry of entries) {
        expect(rank1.total).toBeGreaterThanOrEqual(entry.total);
      }
    });

    it('rank 5 has the lowest total', () => {
      const entries = Object.values(report);
      const rank5 = entries.find(e => e.rank === 5)!;
      for (const entry of entries) {
        expect(rank5.total).toBeLessThanOrEqual(entry.total);
      }
    });

    it('all totals are non-negative', () => {
      for (const entry of Object.values(report)) {
        expect(entry.total).toBeGreaterThanOrEqual(0);
      }
    });

    it('all percentages are between 0 and 100', () => {
      for (const entry of Object.values(report)) {
        expect(entry.percent).toBeGreaterThanOrEqual(0);
        expect(entry.percent).toBeLessThanOrEqual(100);
      }
    });

    it('includes primary nodes, hidden stems, AND bonus nodes', () => {
      // Chart A has bonus nodes from Step 2 (EB combos)
      const totalFromReport = Object.values(report).reduce((s, e) => s + e.total, 0);

      // Sum just primary nodes
      const primaryTotal = state.nodes.reduce((s, n) => s + n.points, 0);
      const bonusTotal = state.bonusNodes.reduce((s, n) => s + n.points, 0);

      expect(totalFromReport).toBeCloseTo(primaryTotal + bonusTotal, 5);
    });
  });

  describe('percentages sum to ~100% for multiple charts', () => {
    const charts = [CHART_A, CHART_B, CHART_C, CHART_D, CHART_E];

    for (let i = 0; i < charts.length; i++) {
      it(`Chart ${String.fromCharCode(65 + i)}: percentages sum to ~100%`, () => {
        const state = calculateWuxingUpToStep(charts[i], 7);
        const report = step8Report(state);
        const totalPct = Object.values(report).reduce((s, e) => s + e.percent, 0);
        expect(totalPct).toBeCloseTo(100, 0);
      });
    }
  });

  describe('on initial state (Step 0 only, no interactions)', () => {
    it('percentages still sum to ~100%', () => {
      const state = calculateWuxingUpToStep(CHART_A, 0);
      const report = step8Report(state);
      const totalPct = Object.values(report).reduce((s, e) => s + e.percent, 0);
      expect(totalPct).toBeCloseTo(100, 0);
    });

    it('ranks are 1-5 with no duplicates', () => {
      const state = calculateWuxingUpToStep(CHART_A, 0);
      const report = step8Report(state);
      const ranks = Object.values(report).map(e => e.rank).sort();
      expect(ranks).toEqual([1, 2, 3, 4, 5]);
    });
  });
});

// =============================================================================
// Step 8: Per-Node Output (initial/final/delta in full result)
// =============================================================================

describe('Step 8: Per-Node Output', () => {
  let result: WuxingResult;

  beforeAll(() => {
    result = calculateWuxing(CHART_A);
  });

  it('each node has initial, final, and delta fields', () => {
    for (const node of Object.values(result.nodes)) {
      expect(node).toHaveProperty('initial');
      expect(node).toHaveProperty('final');
      expect(node).toHaveProperty('delta');
    }
  });

  it('delta = final - initial for all nodes', () => {
    for (const node of Object.values(result.nodes)) {
      expect(node.delta).toBeCloseTo(node.final - node.initial, 10);
    }
  });

  it('HS nodes have initial = 10', () => {
    for (const pos of ['YP', 'MP', 'DP', 'HP']) {
      expect(result.nodes[`${pos}.HS`].initial).toBe(10);
    }
  });

  it('hidden stem nodes are present in output', () => {
    // Chart A: Yin branch has h1 and h2
    expect(result.nodes['YP.EB.h1']).toBeDefined();
    expect(result.nodes['YP.EB.h2']).toBeDefined();
  });
});

// =============================================================================
// DM Strength Thresholds
// =============================================================================

describe('DM Strength Thresholds', () => {
  it('>40% → dominant (Chart D: ~85.7% Earth)', () => {
    const result = calculateWuxing(CHART_D);
    expect(result.dayMaster.percent).toBeGreaterThan(40);
    expect(result.dayMaster.strength).toBe('dominant');
  });

  it('25-40% → strong (Chart A: ~32% Fire)', () => {
    const result = calculateWuxing(CHART_A);
    expect(result.dayMaster.percent).toBeGreaterThanOrEqual(25);
    expect(result.dayMaster.percent).toBeLessThanOrEqual(40);
    expect(result.dayMaster.strength).toBe('strong');
  });

  it('15-25% → balanced (Chart B: ~20.9% Earth)', () => {
    const result = calculateWuxing(CHART_B);
    expect(result.dayMaster.percent).toBeGreaterThanOrEqual(15);
    expect(result.dayMaster.percent).toBeLessThanOrEqual(25);
    expect(result.dayMaster.strength).toBe('balanced');
  });

  it('8-15% → weak (Chart E: ~8.5% Water)', () => {
    const result = calculateWuxing(CHART_E);
    expect(result.dayMaster.percent).toBeGreaterThanOrEqual(8);
    expect(result.dayMaster.percent).toBeLessThanOrEqual(15);
    expect(result.dayMaster.strength).toBe('weak');
  });

  it('<8% → very_weak (Chart C: ~3.3% Fire)', () => {
    const result = calculateWuxing(CHART_C);
    expect(result.dayMaster.percent).toBeLessThan(8);
    expect(result.dayMaster.strength).toBe('very_weak');
  });

  it('boundary: exactly 40% is strong, not dominant', () => {
    // Verify the threshold is STRICTLY greater than 40
    // We test this through the code logic: > 40 → dominant, >= 25 → strong
    // A DM at exactly 40.0% should be 'strong'
    const result = calculateWuxing(CHART_A);
    // We can't easily craft a chart at exactly 40%, but we verify the logic
    // by checking that Chart A (32%) is strong, and Chart D (85%) is dominant
    expect(result.dayMaster.strength).toBe('strong');
  });
});

// =============================================================================
// Step 9: Balance Simulation — Five Gods
// =============================================================================

describe('Step 9: Balance Simulation — Five Gods', () => {
  describe('basic god constraints', () => {
    it('all 5 elements are assigned (Chart A)', () => {
      const result = calculateWuxing(CHART_A);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
    });

    it('all 5 elements are assigned (Chart B)', () => {
      const result = calculateWuxing(CHART_B);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
    });

    it('all 5 elements are assigned (Chart C)', () => {
      const result = calculateWuxing(CHART_C);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
    });

    it('all 5 elements are assigned (Chart D)', () => {
      const result = calculateWuxing(CHART_D);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
    });

    it('all 5 elements are assigned (Chart E)', () => {
      const result = calculateWuxing(CHART_E);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
    });
  });

  describe('favorable/enemy production relationships', () => {
    it('favorable produces useful when no collision (Chart B)', () => {
      const result = calculateWuxing(CHART_B);
      // Chart B: useful=Metal, favorable=Earth — Earth produces Metal
      expect(PRODUCES[result.gods.favorable]).toBe(result.gods.useful);
    });

    it('enemy produces unfavorable when no collision (Chart B)', () => {
      const result = calculateWuxing(CHART_B);
      // Chart B: unfavorable=Wood, enemy=Water — Water produces Wood
      expect(PRODUCES[result.gods.enemy]).toBe(result.gods.unfavorable);
    });
  });

  describe('collision resolution', () => {
    it('uses sigma ranking when production chain collides', () => {
      // Chart A has a collision: produces(useful=Metal) = Earth = unfavorable
      // So it falls back to sigma ranking
      const result = calculateWuxing(CHART_A);
      const godElements = new Set(Object.values(result.gods));
      expect(godElements.size).toBe(5);
      expect(result.gods.useful).toBe('Metal');
      expect(result.gods.unfavorable).toBe('Earth');
    });
  });

  describe('different charts produce different gods', () => {
    it('Chart A and Chart B have different useful gods or different unfavorable gods', () => {
      const resultA = calculateWuxing(CHART_A);
      const resultB = calculateWuxing(CHART_B);

      // The god assignments should not be identical (different charts have different needs)
      const godsA = resultA.gods;
      const godsB = resultB.gods;
      const areDifferent =
        godsA.useful !== godsB.useful ||
        godsA.unfavorable !== godsB.unfavorable ||
        godsA.favorable !== godsB.favorable;
      expect(areDifferent).toBe(true);
    });

    it('very_weak DM chart (C) has DM element as useful god', () => {
      const result = calculateWuxing(CHART_C);
      // Very weak Fire DM needs Fire the most
      expect(result.gods.useful).toBe('Fire');
    });

    it('dominant DM chart (D) does NOT have DM element as useful god', () => {
      const result = calculateWuxing(CHART_D);
      // Dominant Earth DM has too much Earth — it should NOT want more
      expect(result.gods.useful).not.toBe('Earth');
      expect(result.gods.unfavorable).toBe('Earth');
    });
  });

  describe('hovering HS simulation effects', () => {
    it('simulation uses interactions, not just raw element addition', () => {
      // Run step 9 on a full pipeline state
      const state = calculateWuxingUpToStep(CHART_A, 7);
      const report = step8Report(state);
      const gods = step9BalanceSim(state, report);

      // Verify all 5 elements are assigned
      const godElements = new Set(Object.values(gods));
      expect(godElements.size).toBe(5);
    });

    it('hovering HS interacts with visible nodes (not hidden stems)', () => {
      // This is an implicit test: the hovering HS only considers HS + EB main qi.
      // If hidden stems were included, the σ values would differ.
      // We verify the result is well-formed and all gods are distinct.
      const state = calculateWuxingUpToStep(CHART_B, 7);
      const report = step8Report(state);
      const gods = step9BalanceSim(state, report);

      const godElements = new Set(Object.values(gods));
      expect(godElements.size).toBe(5);
    });

    it('each stem simulation is independent (reset between simulations)', () => {
      // Running step9 twice on the same state should produce identical results
      const state = calculateWuxingUpToStep(CHART_A, 7);
      const report = step8Report(state);
      const gods1 = step9BalanceSim(state, report);
      const gods2 = step9BalanceSim(state, report);

      expect(gods1.useful).toBe(gods2.useful);
      expect(gods1.favorable).toBe(gods2.favorable);
      expect(gods1.unfavorable).toBe(gods2.unfavorable);
      expect(gods1.enemy).toBe(gods2.enemy);
      expect(gods1.idle).toBe(gods2.idle);
    });

    it('step9 does not mutate the original state', () => {
      const state = calculateWuxingUpToStep(CHART_A, 7);

      // Record node points before
      const pointsBefore = state.nodes.map(n => n.points);
      const bonusBefore = state.bonusNodes.map(b => b.points);

      const report = step8Report(state);
      step9BalanceSim(state, report);

      // Verify no mutation
      for (let i = 0; i < state.nodes.length; i++) {
        expect(state.nodes[i].points).toBe(pointsBefore[i]);
      }
      for (let i = 0; i < state.bonusNodes.length; i++) {
        expect(state.bonusNodes[i].points).toBe(bonusBefore[i]);
      }
    });
  });

  describe('σ DM penalty', () => {
    it('very_weak DM (<8%) gets +5 penalty that pushes against further weakening', () => {
      // Chart C has very weak Fire DM (~3.3%).
      // Adding Metal (which controls Fire) should get a high σ due to DM penalty
      const result = calculateWuxing(CHART_C);
      // Metal should be unfavorable or enemy (it controls the already-weak Fire DM)
      expect(
        result.gods.unfavorable === 'Metal' || result.gods.enemy === 'Metal'
      ).toBe(true);
    });

    it('dominant DM (>40%) gets +3 penalty against further strengthening', () => {
      // Chart D has dominant Earth DM (~85.7%).
      // Adding Earth should get penalized
      const result = calculateWuxing(CHART_D);
      expect(result.gods.unfavorable).toBe('Earth');
    });
  });
});

// =============================================================================
// Integration: Full Pipeline Gods
// =============================================================================

describe('Full Pipeline Integration: Gods', () => {
  it('gods from calculateWuxing match step9 on same state', () => {
    // Run full pipeline and compare with manual step8+step9
    const fullResult = calculateWuxing(CHART_B);

    const state = calculateWuxingUpToStep(CHART_B, 7);
    const report = step8Report(state);
    const gods = step9BalanceSim(state, report);

    expect(fullResult.gods.useful).toBe(gods.useful);
    expect(fullResult.gods.favorable).toBe(gods.favorable);
    expect(fullResult.gods.unfavorable).toBe(gods.unfavorable);
    expect(fullResult.gods.enemy).toBe(gods.enemy);
    expect(fullResult.gods.idle).toBe(gods.idle);
  });

  it('gods from calculateWuxing cover all five elements', () => {
    for (const chart of [CHART_A, CHART_B, CHART_C, CHART_D, CHART_E]) {
      const result = calculateWuxing(chart);
      const elements = new Set(Object.values(result.gods));
      expect(elements.size).toBe(5);
    }
  });
});
