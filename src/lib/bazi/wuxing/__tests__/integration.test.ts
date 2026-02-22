import { describe, it, expect } from 'vitest';
import { buildChart, analyzeForApi } from '../../comprehensive/engine';
import { adaptToFrontend } from '../../comprehensive/adapter';
import type { WuxingResult } from '../calculator';

// =============================================================================
// Test chart: 丙寅·己亥·丁丑·丁未 (same as calculator.test.ts)
// Male, born 1986, current year 2026
// =============================================================================

const CHART_ARGS = {
  gender: 'male',
  birth_year: 1986,
  year_stem: 'Bing', year_branch: 'Yin',
  month_stem: 'Ji', month_branch: 'Hai',
  day_stem: 'Ding', day_branch: 'Chou',
  hour_stem: 'Ding', hour_branch: 'Wei',
  current_year: 2026,
};

// =============================================================================
// 1. analyzeForApi returns wuxing_result
// =============================================================================

describe('analyzeForApi — wuxing integration', () => {
  const chart = buildChart(CHART_ARGS);
  const results = analyzeForApi(chart);

  it('returns wuxing_result in results', () => {
    expect(results).toHaveProperty('wuxing_result');
  });

  it('wuxing_result has nodes', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(wr.nodes).toBeDefined();
    expect(Object.keys(wr.nodes).length).toBeGreaterThan(0);
  });

  it('wuxing_result has elements', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(wr.elements).toBeDefined();
    expect(wr.elements.Wood).toBeDefined();
    expect(wr.elements.Fire).toBeDefined();
    expect(wr.elements.Earth).toBeDefined();
    expect(wr.elements.Metal).toBeDefined();
    expect(wr.elements.Water).toBeDefined();
  });

  it('wuxing_result has gods with 5 distinct elements', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(wr.gods).toBeDefined();
    const godElements = new Set([
      wr.gods.useful,
      wr.gods.favorable,
      wr.gods.unfavorable,
      wr.gods.enemy,
      wr.gods.idle,
    ]);
    expect(godElements.size).toBe(5);
  });

  it('wuxing_result element percentages sum to ~100', () => {
    const wr = results.wuxing_result as WuxingResult;
    const totalPct = Object.values(wr.elements)
      .reduce((sum, e) => sum + e.percent, 0);
    expect(totalPct).toBeCloseTo(100, 0);
  });

  it('wuxing_result dayMaster matches chart day stem', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(wr.dayMaster.stem).toBe('Ding');
    expect(wr.dayMaster.element).toBe('Fire');
  });
});

// =============================================================================
// 2. strength assessment uses wuxing calculator values
// =============================================================================

describe('strength assessment — wuxing override', () => {
  const chart = buildChart(CHART_ARGS);
  const results = analyzeForApi(chart);
  const strength = results.strength as {
    score: number;
    verdict: string;
    useful_god: string;
    element_percentages: Record<string, number>;
    favorable_elements: string[];
    unfavorable_elements: string[];
    support_count: number;
    drain_count: number;
    seasonal_state: string;
    is_following_chart: boolean;
    best_element_pairs: unknown[];
  };

  it('strength.score comes from wuxing DM percent', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(strength.score).toBe(wr.dayMaster.percent);
  });

  it('strength.useful_god is a valid element', () => {
    const validElements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'];
    expect(validElements).toContain(strength.useful_god);
  });

  it('strength.useful_god comes from wuxing gods', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(strength.useful_god).toBe(wr.gods.useful);
  });

  it('strength.element_percentages sum to ~100', () => {
    const total = Object.values(strength.element_percentages)
      .reduce((sum, v) => sum + v, 0);
    expect(total).toBeCloseTo(100, 0);
  });

  it('strength.element_percentages come from wuxing elements', () => {
    const wr = results.wuxing_result as WuxingResult;
    for (const elem of ['Wood', 'Fire', 'Earth', 'Metal', 'Water']) {
      expect(strength.element_percentages[elem]).toBe(wr.elements[elem as keyof typeof wr.elements].percent);
    }
  });

  it('strength.verdict is valid', () => {
    const validVerdicts = ['extremely_strong', 'strong', 'neutral', 'weak', 'extremely_weak'];
    expect(validVerdicts).toContain(strength.verdict);
  });

  it('strength.favorable_elements comes from wuxing gods', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(strength.favorable_elements).toContain(wr.gods.useful);
    expect(strength.favorable_elements).toContain(wr.gods.favorable);
  });

  it('strength.unfavorable_elements comes from wuxing gods', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(strength.unfavorable_elements).toContain(wr.gods.unfavorable);
    expect(strength.unfavorable_elements).toContain(wr.gods.enemy);
  });

  it('keeps backward-compatible fields', () => {
    expect(typeof strength.support_count).toBe('number');
    expect(typeof strength.drain_count).toBe('number');
    expect(typeof strength.seasonal_state).toBe('string');
    expect(typeof strength.is_following_chart).toBe('boolean');
    expect(Array.isArray(strength.best_element_pairs)).toBe(true);
  });
});

// =============================================================================
// 3. adaptToFrontend uses wuxing element scores
// =============================================================================

describe('adaptToFrontend — wuxing element scores', () => {
  const chart = buildChart(CHART_ARGS);
  const results = analyzeForApi(chart);
  const adapted = adaptToFrontend(chart, results);

  it('adapted output has base_element_score', () => {
    expect(adapted).toHaveProperty('base_element_score');
    const scores = adapted.base_element_score as Record<string, number>;
    expect(Object.keys(scores).length).toBeGreaterThan(0);
  });

  it('adapted output has natal_element_score', () => {
    expect(adapted).toHaveProperty('natal_element_score');
  });

  it('adapted output has post_element_score', () => {
    expect(adapted).toHaveProperty('post_element_score');
  });

  it('daymaster_analysis has correct useful_god', () => {
    const dma = adapted.daymaster_analysis as Record<string, unknown>;
    const wr = results.wuxing_result as WuxingResult;
    expect(dma.useful_god).toBe(wr.gods.useful);
  });

  it('daymaster_analysis has correct daymaster_percentage', () => {
    const dma = adapted.daymaster_analysis as Record<string, unknown>;
    const wr = results.wuxing_result as WuxingResult;
    expect(dma.daymaster_percentage).toBe(wr.dayMaster.percent);
  });

  it('all required response fields exist', () => {
    expect(adapted).toHaveProperty('interactions');
    expect(adapted).toHaveProperty('daymaster_analysis');
    expect(adapted).toHaveProperty('health_analysis');
    expect(adapted).toHaveProperty('wealth_analysis');
    expect(adapted).toHaveProperty('learning_analysis');
    expect(adapted).toHaveProperty('ten_gods_detail');
    expect(adapted).toHaveProperty('special_stars');
    expect(adapted).toHaveProperty('recommendations');
    expect(adapted).toHaveProperty('narrative_analysis');
    expect(adapted).toHaveProperty('mappings');
    expect(adapted).toHaveProperty('client_summary');
    expect(adapted).toHaveProperty('wealth_storage_analysis');
  });
});

// =============================================================================
// 4. Second chart — different pillar set to verify universality
// =============================================================================

describe('wuxing integration — second chart (甲子·丁卯·庚辰·壬午)', () => {
  const chart2Args = {
    gender: 'female',
    birth_year: 1984,
    year_stem: 'Jia', year_branch: 'Zi',
    month_stem: 'Ding', month_branch: 'Mao',
    day_stem: 'Geng', day_branch: 'Chen',
    hour_stem: 'Ren', hour_branch: 'Wu',
    current_year: 2026,
  };

  const chart = buildChart(chart2Args);
  const results = analyzeForApi(chart);

  it('wuxing_result exists', () => {
    expect(results.wuxing_result).toBeDefined();
  });

  it('dayMaster is Geng Metal', () => {
    const wr = results.wuxing_result as WuxingResult;
    expect(wr.dayMaster.stem).toBe('Geng');
    expect(wr.dayMaster.element).toBe('Metal');
  });

  it('strength uses wuxing values', () => {
    const wr = results.wuxing_result as WuxingResult;
    const strength = results.strength as { score: number; useful_god: string };
    expect(strength.score).toBe(wr.dayMaster.percent);
    expect(strength.useful_god).toBe(wr.gods.useful);
  });

  it('adapted output shape is intact', () => {
    const adapted = adaptToFrontend(chart, results);
    expect(adapted).toHaveProperty('base_element_score');
    expect(adapted).toHaveProperty('daymaster_analysis');
    expect(adapted).toHaveProperty('client_summary');
  });
});
