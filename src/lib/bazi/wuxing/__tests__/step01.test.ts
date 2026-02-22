import { describe, it, expect } from 'vitest';
import { initializeState, step1PillarPairs, type WuxingInput } from '../calculator';

const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 1: Pillar Pair Interactions', () => {
  it('YP 丙寅: EB produces HS (Wood→Fire), basis=8', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const ypEb = state.nodes.find(n => n.id === 'YP.EB')!;
    const ypHs = state.nodes.find(n => n.id === 'YP.HS')!;
    expect(ypEb.points).toBeCloseTo(6.4, 1);
    expect(ypHs.points).toBeCloseTo(12.4, 1);
  });

  it('MP 己亥: HS controls EB (Earth克Water 盖头), basis=8', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const mpHs = state.nodes.find(n => n.id === 'MP.HS')!;
    const mpEb = state.nodes.find(n => n.id === 'MP.EB')!;
    expect(mpHs.points).toBeCloseTo(8.4, 1);
    expect(mpEb.points).toBeCloseTo(5.6, 1);
  });

  it('DP 丁丑: HS produces EB (Fire→Earth), basis=8', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const dpHs = state.nodes.find(n => n.id === 'DP.HS')!;
    const dpEb = state.nodes.find(n => n.id === 'DP.EB')!;
    expect(dpHs.points).toBeCloseTo(8.4, 1);
    expect(dpEb.points).toBeCloseTo(10.4, 1);
  });

  it('HP 丁未: HS produces EB (Fire→Earth), basis=8', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const hpHs = state.nodes.find(n => n.id === 'HP.HS')!;
    const hpEb = state.nodes.find(n => n.id === 'HP.EB')!;
    expect(hpHs.points).toBeCloseTo(8.4, 1);
    expect(hpEb.points).toBeCloseTo(10.4, 1);
  });

  it('same element: no interaction (e.g., Wood HS + Wood EB main qi)', () => {
    const input2: WuxingInput = {
      ...INPUT,
      yearPillar: { stem: 'Jia', branch: 'Yin' },
    };
    let state = initializeState(input2);
    state = step1PillarPairs(state);
    const ypHs = state.nodes.find(n => n.id === 'YP.HS')!;
    expect(ypHs.points).toBe(10); // unchanged
  });

  it('logs 4 interactions for this chart (no same-element pillars)', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const step1Ints = state.interactions.filter(i => i.step === 1);
    expect(step1Ints).toHaveLength(4);
  });

  it('EB控HS 截脚: both lose (EB main qi controls HS)', () => {
    // Yi(Wood HS) + Shen(Metal EB main qi = Geng Metal)
    // CONTROL_LOOKUP[Wood][Metal] = 'EB_CONTROLS_HS' (Metal controls Wood = 截脚)
    const input3: WuxingInput = {
      ...INPUT,
      yearPillar: { stem: 'Yi', branch: 'Shen' },
    };
    let state = initializeState(input3);
    state = step1PillarPairs(state);
    const ypHs = state.nodes.find(n => n.id === 'YP.HS')!;
    const ypEb = state.nodes.find(n => n.id === 'YP.EB')!;
    // basis = min(10, 8) = 8
    // EB controls HS: controller (EB Metal) loses 20% of 8 = 1.6 → 8-1.6 = 6.4
    // Controlled (HS Wood) loses 30% of 8 = 2.4 → 10-2.4 = 7.6
    expect(ypEb.points).toBeCloseTo(6.4, 1);
    expect(ypHs.points).toBeCloseTo(7.6, 1);
  });

  it('hidden stems are NOT affected by Step 1', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    // YP.EB.h1 should still be 3.0 (Bing Fire from Yin branch)
    const h1 = state.nodes.find(n => n.id === 'YP.EB.h1')!;
    expect(h1.points).toBe(3);
  });

  it('interaction log has correct details', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const ypInt = state.interactions.find(i => i.step === 1 && i.nodeA === 'YP.HS');
    expect(ypInt).toBeDefined();
    expect(ypInt!.type).toBe('PILLAR_PAIR');
    expect(ypInt!.relationship).toBe('EB_PRODUCES_HS');
    expect(ypInt!.basis).toBe(8);
  });
});
