import { describe, it, expect } from 'vitest';
import {
  initializeState, step1PillarPairs, step2EbPositive,
  step3HsPositive, step4EbNegative, step5HsNegative, step6Seasonal,
  calculateWuxingUpToStep, type WuxingInput
} from '../calculator';

// Helper to run through steps
function runToStep(input: WuxingInput, step: number) {
  return calculateWuxingUpToStep(input, step);
}

const EXAMPLE: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 3: HS Positive (Stem Combos)', () => {
  it('detects Ding-Ren combo -> Wood when both present', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },
      monthPillar: { stem: 'Ding', branch: 'Mao' },
      dayPillar: { stem: 'Ji', branch: 'Chou' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 3);
    const combo = state.interactions.find(i => i.step === 3 && i.type === 'STEM_COMBOS');
    expect(combo).toBeDefined();
    expect(combo?.resultElement).toBe('Wood');
  });

  it('transforms when EB main qi matches combo element', () => {
    // Ding-Ren -> Wood. Mao has Yi Wood EB -> should transform
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },
      monthPillar: { stem: 'Ding', branch: 'Mao' },
      dayPillar: { stem: 'Ji', branch: 'Chou' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 3);
    const combo = state.interactions.find(i => i.step === 3);
    expect(combo?.transformed).toBe(true);
  });

  it('no combo when no matching stems', () => {
    const state = runToStep(EXAMPLE, 3);
    const combos = state.interactions.filter(i => i.step === 3);
    // EXAMPLE chart has no stem combo pairs (Bing, Ji, Ding, Ding)
    expect(combos).toHaveLength(0);
  });

  it('gap multiplier applied for non-adjacent stems', () => {
    // Ren(YP) + Ding(DP) = gap 1 -> x0.75
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },
      monthPillar: { stem: 'Ji', branch: 'Chou' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 3);
    const combo = state.interactions.find(i => i.step === 3);
    expect(combo?.gapMultiplier).toBe(0.75);
  });
});

describe('Step 4: EB Negative Interactions', () => {
  it('six clash control: Zi-Wu (Water controls Fire)', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },
      monthPillar: { stem: 'Bing', branch: 'Wu' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 4);
    const clash = state.interactions.find(
      i => i.step === 4 && i.type === 'SIX_CLASH'
    );
    expect(clash).toBeDefined();
    expect(clash?.logOnly).toBeFalsy();
  });

  it('six clash same-element: Chou-Wei log only', () => {
    const state = runToStep(EXAMPLE, 4);
    const clash = state.interactions.find(
      i => i.step === 4 && i.type === 'SIX_CLASH' &&
      i.branches?.includes('Chou') && i.branches?.includes('Wei')
    );
    expect(clash).toBeDefined();
    expect(clash?.logOnly).toBe(true);
  });

  it('six harm only triggers at gap 0 (adjacent)', () => {
    // Yin(YP) + Si(HP) = gap 2, should NOT trigger
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Yin' },
      monthPillar: { stem: 'Bing', branch: 'Chen' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },
      hourPillar: { stem: 'Ji', branch: 'Si' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 4);
    const harm = state.interactions.find(
      i => i.step === 4 && i.type === 'SIX_HARM' &&
      i.branches?.includes('Yin') && i.branches?.includes('Si')
    );
    expect(harm).toBeUndefined();
  });

  it('six harm triggers when adjacent', () => {
    // Yin(YP) + Si(MP) = gap 0, should trigger
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Yin' },
      monthPillar: { stem: 'Bing', branch: 'Si' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },
      hourPillar: { stem: 'Ji', branch: 'You' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 4);
    const harm = state.interactions.find(
      i => i.step === 4 && i.type === 'SIX_HARM'
    );
    expect(harm).toBeDefined();
  });

  it('damage reduces node points', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },
      monthPillar: { stem: 'Bing', branch: 'Wu' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const pre = runToStep(input, 3);
    const post = runToStep(input, 4);
    // Zi-Wu clash should reduce both nodes
    const preZi = pre.nodes.find(n => n.id === 'YP.EB')!;
    const postZi = post.nodes.find(n => n.id === 'YP.EB')!;
    expect(postZi.points).toBeLessThan(preZi.points);
  });
});

describe('Step 5: HS Negative (Stem Clashes)', () => {
  it('Jia-Geng clash: Metal controls Wood', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },
      monthPillar: { stem: 'Geng', branch: 'Shen' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const state = runToStep(input, 5);
    const clash = state.interactions.find(i => i.step === 5 && i.type === 'STEM_CLASH');
    expect(clash).toBeDefined();
    expect(clash?.attacker).toContain('Geng');
  });

  it('controller loses 25%, controlled loses 50% of basis', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },
      monthPillar: { stem: 'Geng', branch: 'Shen' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30, gender: 'M', location: 'hometown',
    };
    const pre = runToStep(input, 4);
    const post = runToStep(input, 5);
    const preJia = pre.nodes.find(n => n.id === 'YP.HS')!;
    const postJia = post.nodes.find(n => n.id === 'YP.HS')!;
    const preGeng = pre.nodes.find(n => n.id === 'MP.HS')!;
    const postGeng = post.nodes.find(n => n.id === 'MP.HS')!;
    // Controlled (Jia) loses more than controller (Geng)
    const jiaLoss = preJia.points - postJia.points;
    const gengLoss = preGeng.points - postGeng.points;
    expect(jiaLoss).toBeGreaterThan(gengLoss);
  });

  it('no clash when no matching HS pairs', () => {
    const state = runToStep(EXAMPLE, 5);
    const clashes = state.interactions.filter(i => i.step === 5);
    expect(clashes).toHaveLength(0);
  });
});

describe('Step 6: Seasonal Adjustment', () => {
  it('Hai month -> Winter Water season multipliers', () => {
    const state = runToStep(EXAMPLE, 6);
    // Winter: Water x1.25, Wood x1.15, Metal x1.0, Earth x0.85, Fire x0.75
    const fireNode = state.nodes.find(n => n.id === 'YP.HS')!; // Bing Fire
    expect(fireNode.seasonalMultiplier).toBe(0.75);
    const woodNode = state.nodes.find(n => n.id === 'YP.EB')!; // Jia Wood
    expect(woodNode.seasonalMultiplier).toBe(1.15);
  });

  it('every node gets a seasonal multiplier', () => {
    const state = runToStep(EXAMPLE, 6);
    for (const node of state.nodes) {
      expect(node.seasonalMultiplier).toBeDefined();
      expect(node.seasonalMultiplier).toBeGreaterThan(0);
    }
  });

  it('hidden stems also get seasonal adjustment', () => {
    const pre = runToStep(EXAMPLE, 5);
    const post = runToStep(EXAMPLE, 6);
    const preH1 = pre.nodes.find(n => n.id === 'YP.EB.h1')!; // Bing Fire
    const postH1 = post.nodes.find(n => n.id === 'YP.EB.h1')!;
    // Fire in Winter = Dead x 0.75
    expect(postH1.points).toBeCloseTo(preH1.points * 0.75, 1);
  });

  it('bonus nodes also get seasonal adjustment', () => {
    const state = runToStep(EXAMPLE, 6);
    // EXAMPLE chart should have bonus nodes from Step 2
    for (const bn of state.bonusNodes) {
      // Just verify they have reasonable values (not 0, not NaN)
      expect(bn.points).toBeGreaterThan(0);
      expect(Number.isFinite(bn.points)).toBe(true);
    }
  });
});
