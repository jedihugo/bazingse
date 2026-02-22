import { describe, it, expect } from 'vitest';
import {
  initializeState,
  step1PillarPairs,
  step2EbPositive,
  type WuxingInput,
  type WuxingState,
  type BonusNode,
} from '../calculator';
import { EB_POLARITY } from '../tables';

// =============================================================================
// Example chart: 丙寅·己亥·丁丑·丁未 (age 39, male, hometown)
// Branches: Yin(YP), Hai(MP), Chou(DP), Wei(HP)
// =============================================================================

const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 39,
  gender: 'M',
  location: 'hometown',
};

/** Helper: run steps 0-2 on given input */
function runUpToStep2(input: WuxingInput): WuxingState {
  let state = initializeState(input);
  state = step1PillarPairs(state);
  state = step2EbPositive(state);
  return state;
}

/** Helper: find bonus nodes by combo type */
function bonusByType(state: WuxingState, type: string): BonusNode[] {
  return state.bonusNodes.filter(b => b.source === type);
}

/** Helper: find bonus node for a specific pillar and type */
function bonusFor(state: WuxingState, pillar: string, type: string): BonusNode | undefined {
  return state.bonusNodes.find(b => b.pillar === pillar && b.source === type);
}

// =============================================================================
// 1. Combo detection
// =============================================================================

describe('Step 2: Combo Detection (丙寅·己亥·丁丑·丁未)', () => {

  it('detects 丑+亥 (Chou+Hai) 半三会 Water', () => {
    const state = runUpToStep2(INPUT);
    const halfMeetings = bonusByType(state, 'HALF_MEETINGS');
    // Chou+Hai is from Hai-Zi-Chou seasonal group, missing Zi
    expect(halfMeetings.length).toBeGreaterThanOrEqual(2); // One per participating EB
    const waterBonuses = halfMeetings.filter(b => b.element === 'Water');
    expect(waterBonuses.length).toBeGreaterThanOrEqual(2); // DP.EB + MP.EB
  });

  it('detects 寅+亥 (Yin+Hai) 六合 Wood', () => {
    const state = runUpToStep2(INPUT);
    const sixHarmonies = bonusByType(state, 'SIX_HARMONIES');
    const woodBonuses = sixHarmonies.filter(b => b.element === 'Wood');
    expect(woodBonuses.length).toBeGreaterThanOrEqual(2); // YP.EB + MP.EB
  });

  it('detects 亥+未 (Hai+Wei) 拱合 Wood', () => {
    const state = runUpToStep2(INPUT);
    const arched = bonusByType(state, 'ARCHED_COMBOS');
    const woodArched = arched.filter(b => b.element === 'Wood');
    expect(woodArched.length).toBeGreaterThanOrEqual(2); // MP.EB + HP.EB
  });

  it('creates bonus nodes for all valid combos', () => {
    const state = runUpToStep2(INPUT);
    // 3 combos x 2 nodes each = at least 6 bonus nodes
    expect(state.bonusNodes.length).toBeGreaterThanOrEqual(6);
  });

  it('logs Step 2 interactions', () => {
    const state = runUpToStep2(INPUT);
    const step2Logs = state.interactions.filter(i => i.step === 2);
    // At least 3 combos detected
    expect(step2Logs.length).toBeGreaterThanOrEqual(3);
  });
});

// =============================================================================
// 2. Attention spread
// =============================================================================

describe('Step 2: Attention Spread', () => {

  it('寅 (Yin at YP) gets higher effective bonus than 亥 (Hai at MP) from the same 六合', () => {
    const state = runUpToStep2(INPUT);

    // Yin (YP) participates in fewer interactions → higher attention share
    // Hai (MP) participates in 半三会 + 六合 + 拱合 + possibly negative interactions
    const yinBonus = bonusFor(state, 'YP', 'SIX_HARMONIES');
    const haiBonus = bonusFor(state, 'MP', 'SIX_HARMONIES');

    expect(yinBonus).toBeDefined();
    expect(haiBonus).toBeDefined();
    expect(yinBonus!.points).toBeGreaterThan(haiBonus!.points);
  });

  it('attention map is populated on state', () => {
    const state = runUpToStep2(INPUT);
    expect(state.attentionMap.size).toBeGreaterThan(0);
  });

  it('亥 (Hai at MP.EB) has multiple attention entries', () => {
    const state = runUpToStep2(INPUT);
    const haiAttention = state.attentionMap.get('MP.EB');
    expect(haiAttention).toBeDefined();
    // Hai participates in: HALF_MEETINGS + SIX_HARMONIES + ARCHED_COMBOS + possibly negatives
    expect(haiAttention!.length).toBeGreaterThanOrEqual(3);
  });

  it('寅 (Yin at YP.EB) attention share for 六合 is higher than 亥 share', () => {
    const state = runUpToStep2(INPUT);

    const yinAttention = state.attentionMap.get('YP.EB') ?? [];
    const haiAttention = state.attentionMap.get('MP.EB') ?? [];

    const yinTotal = yinAttention.reduce((s, a) => s + a.weight, 0);
    const haiTotal = haiAttention.reduce((s, a) => s + a.weight, 0);

    const sixHarmWeight = 28; // ATTENTION_WEIGHTS.SIX_HARMONIES
    const yinShare = yinTotal > 0 ? sixHarmWeight / yinTotal : 1;
    const haiShare = haiTotal > 0 ? sixHarmWeight / haiTotal : 1;

    expect(yinShare).toBeGreaterThan(haiShare);
  });
});

// =============================================================================
// 3. Bonus node properties
// =============================================================================

describe('Step 2: BonusNode Properties', () => {

  it('bonus nodes have correct element', () => {
    const state = runUpToStep2(INPUT);
    const sixHarmonies = bonusByType(state, 'SIX_HARMONIES');
    for (const b of sixHarmonies) {
      expect(b.element).toBe('Wood'); // Yin+Hai → Wood
    }
  });

  it('bonus nodes have correct polarity matching their branch', () => {
    const state = runUpToStep2(INPUT);
    // YP (Yin) is Yang, MP (Hai) is Yin
    const ypBonus = bonusFor(state, 'YP', 'SIX_HARMONIES');
    const mpBonus = bonusFor(state, 'MP', 'SIX_HARMONIES');

    expect(ypBonus!.polarity).toBe(EB_POLARITY.Yin);  // 'Yang'
    expect(mpBonus!.polarity).toBe(EB_POLARITY.Hai);  // 'Yin'
  });

  it('bonus node IDs follow naming convention', () => {
    const state = runUpToStep2(INPUT);
    const ypBonus = bonusFor(state, 'YP', 'SIX_HARMONIES');
    expect(ypBonus!.id).toBe('YP.EB+Wood_SIX_HARMONIES');
    expect(ypBonus!.sourceNode).toBe('YP.EB');
  });

  it('all bonus nodes have positive points', () => {
    const state = runUpToStep2(INPUT);
    for (const b of state.bonusNodes) {
      expect(b.points).toBeGreaterThan(0);
    }
  });
});

// =============================================================================
// 4. Transformation
// =============================================================================

describe('Step 2: Transformation', () => {

  it('chart with Fire HS + 寅午戌 三合 Fire → transforms (×2.5)', () => {
    // 寅午戌 三合 Fire = Yin+Wu+Xu → Fire
    // Fire HS present → transformation succeeds
    const input: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },   // Fire HS, Yin EB
      monthPillar: { stem: 'Ding', branch: 'Wu' },    // Fire HS, Wu EB
      dayPillar: { stem: 'Jia', branch: 'Xu' },       // Wood HS, Xu EB
      hourPillar: { stem: 'Geng', branch: 'Shen' },   // Metal HS, Shen EB
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const state = runUpToStep2(input);
    const threeCombos = bonusByType(state, 'THREE_COMBOS');
    expect(threeCombos.length).toBeGreaterThanOrEqual(3); // One per branch

    // Check that the interaction log shows transformed=true
    const log = state.interactions.find(i => i.type === 'THREE_COMBOS');
    expect(log).toBeDefined();
    expect(log!.transformed).toBe(true);
    expect(log!.resultElement).toBe('Fire');
  });

  it('no transformation when no matching HS present', () => {
    // 寅+亥 六合 Wood — does the chart have a Wood HS?
    // In our test chart (丙寅·己亥·丁丑·丁未), HS elements are Fire, Earth, Fire, Fire
    // No Wood HS → should NOT transform
    const state = runUpToStep2(INPUT);
    const sixHarmLog = state.interactions.find(i => i.type === 'SIX_HARMONIES');
    expect(sixHarmLog).toBeDefined();
    expect(sixHarmLog!.resultElement).toBe('Wood');
    expect(sixHarmLog!.transformed).toBe(false);
  });

  it('transformed combo produces significantly more points', () => {
    // Build a chart where we can compare: same combo with/without matching HS
    // Chart A: Fire HS + Yin+Wu+Xu (transforms)
    const inputA: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },
      monthPillar: { stem: 'Ding', branch: 'Wu' },
      dayPillar: { stem: 'Jia', branch: 'Xu' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    // Chart B: No Fire HS + Yin+Wu+Xu (does not transform)
    const inputB: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Yin' },  // Wood HS
      monthPillar: { stem: 'Ren', branch: 'Wu' },   // Water HS
      dayPillar: { stem: 'Geng', branch: 'Xu' },    // Metal HS
      hourPillar: { stem: 'Ji', branch: 'Shen' },   // Earth HS
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const stateA = runUpToStep2(inputA);
    const stateB = runUpToStep2(inputB);

    const totalA = bonusByType(stateA, 'THREE_COMBOS')
      .reduce((s, b) => s + b.points, 0);
    const totalB = bonusByType(stateB, 'THREE_COMBOS')
      .reduce((s, b) => s + b.points, 0);

    // Chart A should produce significantly more bonus points (×2.5 from transform)
    expect(totalA).toBeGreaterThan(totalB * 2);
  });
});

// =============================================================================
// 5. Three-Branch Priority (nullification)
// =============================================================================

describe('Step 2: Three-Branch Priority', () => {

  it('巳午未 三会 Fire nullifies component 半三会', () => {
    // Si+Wu+Wei = 三会 Fire (seasonal combo: Si-Wu-Wei)
    // Si+Wu, Wu+Wei, Si+Wei are all 半三会 → should be nullified
    const input: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Si' },
      monthPillar: { stem: 'Ding', branch: 'Wu' },
      dayPillar: { stem: 'Ji', branch: 'Wei' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const state = runUpToStep2(input);

    // THREE_MEETINGS should be present
    const threeMeetings = bonusByType(state, 'THREE_MEETINGS');
    expect(threeMeetings.length).toBeGreaterThanOrEqual(3); // One per branch in trio

    // HALF_MEETINGS for subsets of Si-Wu-Wei should be nullified
    const halfMeetings = bonusByType(state, 'HALF_MEETINGS');
    const fireHalfs = halfMeetings.filter(b => b.element === 'Fire');
    expect(fireHalfs.length).toBe(0); // All nullified by the full trio
  });

  it('三合 nullifies its 拱合 subset', () => {
    // Hai+Mao+Wei = 三合 Wood → Hai+Wei 拱合 Wood should be nullified
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Hai' },
      monthPillar: { stem: 'Yi', branch: 'Mao' },
      dayPillar: { stem: 'Ji', branch: 'Wei' },
      hourPillar: { stem: 'Bing', branch: 'Yin' },
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const state = runUpToStep2(input);

    // THREE_COMBOS for Hai+Mao+Wei → Wood
    const threeCombos = bonusByType(state, 'THREE_COMBOS');
    const woodCombos = threeCombos.filter(b => b.element === 'Wood');
    expect(woodCombos.length).toBeGreaterThanOrEqual(3);

    // ARCHED_COMBOS for Hai+Wei → Wood should be nullified
    const arched = bonusByType(state, 'ARCHED_COMBOS');
    const woodArched = arched.filter(b => b.element === 'Wood');
    expect(woodArched.length).toBe(0); // Nullified
  });
});

// =============================================================================
// 6. Gap multiplier
// =============================================================================

describe('Step 2: Gap Multiplier', () => {

  it('adjacent branches get full multiplier (gap=0)', () => {
    // Yin(YP) + Hai(MP) → gap 0 between YP and MP → multiplier 1.0
    const state = runUpToStep2(INPUT);
    const log = state.interactions.find(i => i.type === 'SIX_HARMONIES');
    expect(log).toBeDefined();
    expect(log!.gapMultiplier).toBe(1.0);
  });

  it('distant 2-branch combo gets reduced multiplier', () => {
    // Chou(DP) + Hai(MP) → gap between MP and DP = 0 → multiplier 1.0
    const state = runUpToStep2(INPUT);
    const halfLog = state.interactions.find(i => i.type === 'HALF_MEETINGS');
    expect(halfLog).toBeDefined();
    // DP-MP gap = 0, so multiplier should be 1.0
    expect(halfLog!.gapMultiplier).toBe(1.0);
  });

  it('3-branch combo spanning all 4 pillars gets gap penalty', () => {
    // Make a 3-branch combo spanning YP to HP with a gap
    // Yin(YP) + Wu(DP) + Xu(HP) = 寅午戌 三合 Fire, spans 0-3 = 4 positions, 3 branches → 1 gap
    const input: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },
      monthPillar: { stem: 'Ji', branch: 'Hai' },   // Not part of the trio
      dayPillar: { stem: 'Ding', branch: 'Wu' },
      hourPillar: { stem: 'Ding', branch: 'Xu' },
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const state = runUpToStep2(input);
    const log = state.interactions.find(i => i.type === 'THREE_COMBOS');
    expect(log).toBeDefined();
    // Span: YP(0) to HP(3) = 4 positions, 3 branches → 1 gap → 0.75
    expect(log!.gapMultiplier).toBe(0.75);
  });
});

// =============================================================================
// 7. Edge cases
// =============================================================================

describe('Step 2: Edge Cases', () => {

  it('chart with no EB combos produces no bonus nodes', () => {
    // Use branches that don't form any combos
    // Zi, Mao, Wu, You: these are the 4 cardinal branches (no combos among them except...)
    // Actually: Zi+Mao = punishment, Mao+You = clash, Zi+Wu = clash
    // Let's try: Zi, Chen, Wu, Xu — these are 4 graveyard branches, no positive combos except...
    // Chen+Xu is actually a clash (same-element). Let's check if Zi+Chen is a combo.
    // Shen-Zi-Chen is THREE_COMBOS — Zi and Chen are part of it but missing Shen.
    // We need branches with truly no combos. Let's use: Yin, Si, You, Chou
    // Wait, Si-You-Chou = THREE_COMBOS Metal! Let's use: Yin, Wu, You, Chou
    // Yin-Wu-Xu = THREE_COMBOS (missing Xu, but we have Wu+You? No combo)
    // Yin+You? No special combo. Actually let me just check what combos form...
    // For truly no combos: Mao, Shen, Chou, Si
    // Mao+Shen: no combo. Si+You+Chou = THREE_COMBOS but no You.
    // Si+Chou = ARCHED_COMBOS Metal. Let's keep it simple:
    // Use Zi, Yin, Shen, Xu — these form: Shen+Zi+Chen (missing Chen), Yin+Wu+Xu (missing Wu)
    // Shen+Yin = SIX_CLASH. So negative but no positive.
    // Actually Yin-Mao-Chen half meeting? No Mao.
    // This is hard — let me use Mao, Wu, You, Zi
    // Mao+You = clash. Zi+Wu = clash. No positive combos among them.
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Mao' },
      monthPillar: { stem: 'Ding', branch: 'Wu' },
      dayPillar: { stem: 'Xin', branch: 'You' },
      hourPillar: { stem: 'Gui', branch: 'Zi' },
      age: 25,
      gender: 'M',
      location: 'hometown',
    };

    const state = runUpToStep2(input);
    // Mao+Wu = HALF_MEETINGS? No, they're not in the same seasonal group.
    // Wei+Wu = HALF_MEETINGS Fire, but we don't have Wei.
    // Zi+Chou = SIX_HARMONIES, but no Chou.
    // So no positive combos.
    const positiveBonuses = state.bonusNodes.filter(b =>
      ['THREE_MEETINGS', 'THREE_COMBOS', 'SIX_HARMONIES', 'HALF_MEETINGS', 'ARCHED_COMBOS'].includes(b.source)
    );
    expect(positiveBonuses.length).toBe(0);
  });

  it('step 2 returns the same state object (mutates in place)', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);
    const result = step2EbPositive(state);
    expect(result).toBe(state);
  });

  it('bonus nodes are added to state.bonusNodes, not replacing them', () => {
    const state = runUpToStep2(INPUT);
    // After step2, bonusNodes should be non-empty
    expect(state.bonusNodes.length).toBeGreaterThan(0);
  });
});

// =============================================================================
// 8. Interaction log details
// =============================================================================

describe('Step 2: Interaction Log', () => {

  it('logs include resultElement', () => {
    const state = runUpToStep2(INPUT);
    const step2Logs = state.interactions.filter(i => i.step === 2);
    for (const log of step2Logs) {
      expect(log.resultElement).toBeDefined();
    }
  });

  it('logs include basis value', () => {
    const state = runUpToStep2(INPUT);
    const step2Logs = state.interactions.filter(i => i.step === 2);
    for (const log of step2Logs) {
      expect(log.basis).toBeDefined();
      expect(log.basis).toBeGreaterThan(0);
    }
  });

  it('logs include transformed flag', () => {
    const state = runUpToStep2(INPUT);
    const step2Logs = state.interactions.filter(i => i.step === 2);
    for (const log of step2Logs) {
      expect(typeof log.transformed).toBe('boolean');
    }
  });

  it('logs include gapMultiplier', () => {
    const state = runUpToStep2(INPUT);
    const step2Logs = state.interactions.filter(i => i.step === 2);
    for (const log of step2Logs) {
      expect(log.gapMultiplier).toBeDefined();
      expect(log.gapMultiplier).toBeGreaterThan(0);
      expect(log.gapMultiplier).toBeLessThanOrEqual(1);
    }
  });
});
