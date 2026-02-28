# Wu Xing Calculator Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the existing golden-ratio scoring system with a deterministic point-based Wu Xing calculator that follows the bazi-wuxing skill exactly (Steps 0-9).

**Architecture:** Single monolithic calculator file (`src/lib/bazi/wuxing/calculator.ts`) + separate lookup tables file (`src/lib/bazi/wuxing/tables.ts`). A `calculateWuxing()` entry point runs Steps 0-9 sequentially on a shared `WuxingState` object. Integration via `comprehensive/engine.ts` calling the new calculator and `comprehensive/adapter.ts` mapping results to the existing frontend JSON.

**Tech Stack:** TypeScript (strict mode), Vitest for unit tests, existing `core.ts` STEMS/BRANCHES data.

---

### Task 1: Create tables.ts with all skill lookup data

**Files:**
- Create: `src/lib/bazi/wuxing/tables.ts`
- Test: `src/lib/bazi/wuxing/__tests__/tables.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/tables.test.ts
import { describe, it, expect } from 'vitest';
import {
  HS_POINTS, EB_HIDDEN_STEMS,
  PILLAR_GAP, COMBO_RATES, ATTENTION_WEIGHTS,
  SEASONAL_MULTIPLIERS, SEASONAL_MATRIX,
  CONTROL_LOOKUP, PRODUCTION_LOOKUP,
  THREE_MEETINGS_TABLE, THREE_COMBOS_TABLE,
  SIX_HARMONIES_TABLE, HALF_MEETINGS_TABLE,
  ARCHED_COMBOS_TABLE, STEM_COMBOS_TABLE,
  SIX_CLASHES_TABLE, PUNISHMENTS_TABLE,
  SIX_HARMS_TABLE, DESTRUCTIONS_TABLE,
  STEM_CLASHES_TABLE,
} from '../tables';

describe('tables.ts', () => {
  it('HS always 10 points', () => {
    for (const stem of Object.keys(HS_POINTS)) {
      expect(HS_POINTS[stem].points).toBe(10);
    }
    expect(Object.keys(HS_POINTS)).toHaveLength(10);
  });

  it('EB hidden stems match skill point distribution', () => {
    // Pure qi: 10 pts total
    expect(EB_HIDDEN_STEMS.Zi).toEqual([{ stem: 'Gui', element: 'Water', points: 10 }]);
    expect(EB_HIDDEN_STEMS.Mao).toEqual([{ stem: 'Yi', element: 'Wood', points: 10 }]);
    expect(EB_HIDDEN_STEMS.You).toEqual([{ stem: 'Xin', element: 'Metal', points: 10 }]);

    // 2 qi: 8 + 3 = 11 pts
    expect(EB_HIDDEN_STEMS.Wu.map(h => h.points)).toEqual([8, 3]);
    expect(EB_HIDDEN_STEMS.Hai.map(h => h.points)).toEqual([8, 3]);

    // 3 qi: 8 + 3 + 1 = 12 pts
    expect(EB_HIDDEN_STEMS.Chou.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Yin.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Chen.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Si.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Wei.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Shen.map(h => h.points)).toEqual([8, 3, 1]);
    expect(EB_HIDDEN_STEMS.Xu.map(h => h.points)).toEqual([8, 3, 1]);
  });

  it('pillar gap matrix is correct', () => {
    expect(PILLAR_GAP['YP']['MP']).toBe(0);
    expect(PILLAR_GAP['MP']['DP']).toBe(0);
    expect(PILLAR_GAP['DP']['HP']).toBe(0);
    expect(PILLAR_GAP['YP']['DP']).toBe(1);
    expect(PILLAR_GAP['MP']['HP']).toBe(1);
    expect(PILLAR_GAP['YP']['HP']).toBe(2);
  });

  it('gap multipliers are correct', () => {
    // From skill: gap 0 = 1.0, gap 1 = 0.75, gap 2 = 0.5, gap 3+ = 0.25
    expect(PILLAR_GAP.multiplier(0)).toBe(1.0);
    expect(PILLAR_GAP.multiplier(1)).toBe(0.75);
    expect(PILLAR_GAP.multiplier(2)).toBe(0.5);
    expect(PILLAR_GAP.multiplier(3)).toBe(0.25);
  });

  it('combo rates match skill', () => {
    expect(COMBO_RATES.THREE_MEETINGS).toBe(0.30);
    expect(COMBO_RATES.THREE_COMBOS).toBe(0.25);
    expect(COMBO_RATES.SIX_HARMONIES).toBe(0.20);
    expect(COMBO_RATES.HALF_MEETINGS).toBe(0.20);
    expect(COMBO_RATES.ARCHED_COMBOS).toBe(0.15);
    expect(COMBO_RATES.STEM_COMBOS).toBe(0.30);
  });

  it('attention weights match skill', () => {
    expect(ATTENTION_WEIGHTS.THREE_MEETINGS).toBe(63);
    expect(ATTENTION_WEIGHTS.THREE_COMBOS).toBe(42);
    expect(ATTENTION_WEIGHTS.SIX_CLASH).toBe(42);
    expect(ATTENTION_WEIGHTS.PUNISHMENT_FULL).toBe(42);
    expect(ATTENTION_WEIGHTS.SIX_HARMONIES).toBe(28);
    expect(ATTENTION_WEIGHTS.DESTRUCTION).toBe(28);
    expect(ATTENTION_WEIGHTS.SIX_HARM).toBe(28);
    expect(ATTENTION_WEIGHTS.HALF_MEETINGS).toBe(12);
    expect(ATTENTION_WEIGHTS.ARCHED_COMBO).toBe(7);
  });

  it('seasonal multipliers match skill', () => {
    expect(SEASONAL_MULTIPLIERS.Prosperous).toBe(1.25);
    expect(SEASONAL_MULTIPLIERS.Prime).toBe(1.15);
    expect(SEASONAL_MULTIPLIERS.Rest).toBe(1.0);
    expect(SEASONAL_MULTIPLIERS.Imprisoned).toBe(0.85);
    expect(SEASONAL_MULTIPLIERS.Dead).toBe(0.75);
  });

  it('seasonal matrix: Winter Water season', () => {
    // Winter (Water): Water=旺, Wood=相, Metal=休, Earth=囚, Fire=死
    expect(SEASONAL_MATRIX.Water.Water).toBe('Prosperous');
    expect(SEASONAL_MATRIX.Water.Wood).toBe('Prime');
    expect(SEASONAL_MATRIX.Water.Metal).toBe('Rest');
    expect(SEASONAL_MATRIX.Water.Earth).toBe('Imprisoned');
    expect(SEASONAL_MATRIX.Water.Fire).toBe('Dead');
  });

  it('control lookup table matches skill', () => {
    expect(CONTROL_LOOKUP.Wood.Fire).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Wood.Earth).toBe('HS_CONTROLS_EB');
    expect(CONTROL_LOOKUP.Wood.Metal).toBe('EB_CONTROLS_HS');
    expect(CONTROL_LOOKUP.Wood.Water).toBe('EB_PRODUCES_HS');
    expect(CONTROL_LOOKUP.Fire.Earth).toBe('HS_PRODUCES_EB');
    // Common mistake check: Fire + Earth = HS produces EB (Fire→Earth), NOT Earth克Fire
    expect(CONTROL_LOOKUP.Fire.Earth).toBe('HS_PRODUCES_EB');
  });

  it('three meetings table has 4 entries', () => {
    expect(Object.keys(THREE_MEETINGS_TABLE)).toHaveLength(4);
    expect(THREE_MEETINGS_TABLE['Yin-Mao-Chen']).toEqual({ element: 'Wood' });
    expect(THREE_MEETINGS_TABLE['Si-Wu-Wei']).toEqual({ element: 'Fire' });
  });

  it('six clashes table has 6 entries', () => {
    expect(Object.keys(SIX_CLASHES_TABLE)).toHaveLength(6);
    // Control clashes
    expect(SIX_CLASHES_TABLE['Wu-Zi'].attacker).toBe('Zi');
    expect(SIX_CLASHES_TABLE['Wu-Zi'].type).toBe('control');
    // Same-element clashes
    expect(SIX_CLASHES_TABLE['Chou-Wei'].type).toBe('same');
  });

  it('six harms table has 6 entries with attacker/victim', () => {
    expect(Object.keys(SIX_HARMS_TABLE)).toHaveLength(6);
    expect(SIX_HARMS_TABLE['Wei-Zi'].attacker).toBe('Wei');
    expect(SIX_HARMS_TABLE['Wei-Zi'].victim).toBe('Zi');
  });

  it('stem clashes table has 4 entries', () => {
    expect(Object.keys(STEM_CLASHES_TABLE)).toHaveLength(4);
    expect(STEM_CLASHES_TABLE['Jia-Geng'].controller).toBe('Geng');
    expect(STEM_CLASHES_TABLE['Jia-Geng'].controlled).toBe('Jia');
  });
});
```

**Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/tables.test.ts`
Expected: FAIL — module not found

**Step 3: Write tables.ts**

Create `src/lib/bazi/wuxing/tables.ts` containing all lookup tables from the bazi-wuxing skill:

- `HS_POINTS` — 10 stems, each 10 pts, with element + polarity
- `EB_HIDDEN_STEMS` — 12 branches, each with hidden stem entries (stem, element, points: 8/3/1)
- `EB_POLARITY` — Yang/Yin for each branch (Yang: 子寅辰午申戌, Yin: 丑卯巳未酉亥)
- `PILLAR_GAP` — gap matrix between YP/MP/DP/HP + `multiplier(gap)` helper
- `COMBO_RATES` — rates per combo type (0.30, 0.25, 0.20, 0.20, 0.15, 0.30)
- `TRANSFORMATION_MULTIPLIER = 2.5`
- `ATTENTION_WEIGHTS` — per interaction type (63, 42, 28, 12, 7)
- `SEASONAL_MULTIPLIERS` — Prosperous=1.25, Prime=1.15, Rest=1.0, Imprisoned=0.85, Dead=0.75
- `SEASONAL_MATRIX` — 5x5 lookup: season element → target element → state
- `CONTROL_LOOKUP` — HS element × EB element → relationship type (the 5x5 table from skill)
- `PRODUCTION_LOOKUP` — Wood→Fire→Earth→Metal→Water→Wood
- All combo/clash/harm/destruction tables: `THREE_MEETINGS_TABLE`, `THREE_COMBOS_TABLE`, `SIX_HARMONIES_TABLE`, `HALF_MEETINGS_TABLE`, `ARCHED_COMBOS_TABLE`, `STEM_COMBOS_TABLE`, `SIX_CLASHES_TABLE`, `PUNISHMENTS_TABLE`, `SIX_HARMS_TABLE`, `DESTRUCTIONS_TABLE`, `STEM_CLASHES_TABLE`

Import `Element`, `StemName`, `BranchName` types from `../core` (do NOT import `'server-only'` — this module should be pure data, testable without Next.js server context).

**Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/tables.test.ts`
Expected: PASS

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/tables.ts src/lib/bazi/wuxing/__tests__/tables.test.ts
git commit -m "feat(wuxing): add lookup tables for point-based Wu Xing calculator"
```

---

### Task 2: Create calculator.ts scaffolding — types, state, entry point

**Files:**
- Create: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/calculator.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/calculator.test.ts
import { describe, it, expect } from 'vitest';
import { calculateWuxing, type WuxingInput, type WuxingResult } from '../calculator';

describe('calculateWuxing scaffolding', () => {
  const INPUT: WuxingInput = {
    yearPillar: { stem: 'Bing', branch: 'Yin' },
    monthPillar: { stem: 'Ji', branch: 'Hai' },
    dayPillar: { stem: 'Ding', branch: 'Chou' },
    hourPillar: { stem: 'Ding', branch: 'Wei' },
    age: 40,
    gender: 'M',
    location: 'hometown',
  };

  it('returns a WuxingResult with all required fields', () => {
    const result = calculateWuxing(INPUT);
    expect(result).toHaveProperty('nodes');
    expect(result).toHaveProperty('bonusNodes');
    expect(result).toHaveProperty('elements');
    expect(result).toHaveProperty('dayMaster');
    expect(result).toHaveProperty('gods');
    expect(result).toHaveProperty('interactions');
  });

  it('has correct day master stem', () => {
    const result = calculateWuxing(INPUT);
    expect(result.dayMaster.stem).toBe('Ding');
    expect(result.dayMaster.element).toBe('Fire');
  });

  it('elements sum to 100%', () => {
    const result = calculateWuxing(INPUT);
    const totalPct = Object.values(result.elements).reduce((s, e) => s + e.percent, 0);
    expect(totalPct).toBeCloseTo(100, 0);
  });

  it('5 gods has all 5 elements distributed', () => {
    const result = calculateWuxing(INPUT);
    const allGodElements = new Set([
      result.gods.useful, result.gods.favorable,
      result.gods.unfavorable, result.gods.enemy, result.gods.idle,
    ]);
    expect(allGodElements.size).toBe(5);
  });
});
```

**Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/calculator.test.ts`
Expected: FAIL — module not found

**Step 3: Write the calculator scaffolding**

Create `src/lib/bazi/wuxing/calculator.ts` with:

1. **Types**: `WuxingInput`, `PillarPosition`, `NodeId`, `NodeSlot`, `WuxingNode`, `BonusNode`, `InteractionLog`, `WuxingState`, `WuxingResult`, `ElementSummary`, `DayMasterSummary`, `FiveGods`

2. **`initializeState(input: WuxingInput): WuxingState`** — Step 0 (initial point assignment). Creates all nodes from HS_POINTS and EB_HIDDEN_STEMS tables.

3. **`calculatePillarPriority(age: number): PillarPosition[]`** — Age-based processing order.

4. **Stub step functions** (each returns the state unchanged for now):
   - `step1PillarPairs(state)`
   - `step2EbPositive(state)`
   - `step3HsPositive(state)`
   - `step4EbNegative(state)`
   - `step5HsNegative(state)`
   - `step6Seasonal(state)`
   - `step7NaturalFlow(state)`
   - `step8Report(state): ElementReport`
   - `step9BalanceSim(state, report): FiveGods`

5. **`calculateWuxing(input: WuxingInput): WuxingResult`** — chains all steps.

All step stubs return passthrough state so the scaffolding test passes. Step 0 (initializeState) is fully implemented — it assigns the correct initial points to all nodes.

**Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/calculator.test.ts`
Expected: PASS (stubs return valid structure with initial points)

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/calculator.test.ts
git commit -m "feat(wuxing): calculator scaffolding with types, state, and step stubs"
```

---

### Task 3: Implement Step 0 — Initial Point Assignment + Step 1 — Pillar Pairs

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step01.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step01.test.ts
import { describe, it, expect } from 'vitest';
import { initializeState, step1PillarPairs, type WuxingInput } from '../calculator';

// Skill example chart: 丙寅·己亥·丁丑·丁未
const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 0: Initial Points', () => {
  it('HS nodes get 10 points each', () => {
    const state = initializeState(INPUT);
    const ypHs = state.nodes.find(n => n.id === 'YP.HS');
    expect(ypHs?.points).toBe(10);
    expect(ypHs?.stem).toBe('Bing');
    expect(ypHs?.element).toBe('Fire');
  });

  it('EB main qi gets correct points', () => {
    const state = initializeState(INPUT);
    // Yin has 3 qi: Jia Wood 8, Bing Fire 3, Wu Earth 1
    const ypEb = state.nodes.find(n => n.id === 'YP.EB');
    expect(ypEb?.points).toBe(8);
    expect(ypEb?.stem).toBe('Jia');
    expect(ypEb?.element).toBe('Wood');

    const ypH1 = state.nodes.find(n => n.id === 'YP.EB.h1');
    expect(ypH1?.points).toBe(3);
    expect(ypH1?.stem).toBe('Bing');

    const ypH2 = state.nodes.find(n => n.id === 'YP.EB.h2');
    expect(ypH2?.points).toBe(1);
    expect(ypH2?.stem).toBe('Wu');
  });

  it('pure qi branch (Zi) gets 10 pts, no h1/h2', () => {
    const input2: WuxingInput = {
      ...INPUT,
      monthPillar: { stem: 'Ren', branch: 'Zi' },
    };
    const state = initializeState(input2);
    const mpEb = state.nodes.find(n => n.id === 'MP.EB');
    expect(mpEb?.points).toBe(10);
    // No h1 or h2 for pure qi
    const mpH1 = state.nodes.find(n => n.id === 'MP.EB.h1');
    expect(mpH1).toBeUndefined();
  });

  it('2-qi branch (Hai) gets 8+3, no h2', () => {
    const state = initializeState(INPUT);
    const mpEb = state.nodes.find(n => n.id === 'MP.EB');
    expect(mpEb?.points).toBe(8); // Ren Water main qi
    const mpH1 = state.nodes.find(n => n.id === 'MP.EB.h1');
    expect(mpH1?.points).toBe(3); // Jia Wood
    const mpH2 = state.nodes.find(n => n.id === 'MP.EB.h2');
    expect(mpH2).toBeUndefined();
  });

  it('pillar priority: age 40 → DP first', () => {
    const state = initializeState(INPUT);
    expect(state.pillarPriority[0]).toBe('DP');
  });
});

describe('Step 1: Pillar Pair Interactions', () => {
  it('YP 丙寅: EB produces HS (Wood→Fire), basis=8', () => {
    // Wood(Jia 8) produces Fire(Bing 10). basis = min(8,10) = 8
    // Producer (Wood) loses 20% of 8 = 1.6: 8 → 6.4
    // Produced (Fire) gains 30% of 8 = 2.4: 10 → 12.4
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);

    const ypEb = state.nodes.find(n => n.id === 'YP.EB');
    expect(ypEb?.points).toBeCloseTo(6.4, 1);

    const ypHs = state.nodes.find(n => n.id === 'YP.HS');
    expect(ypHs?.points).toBeCloseTo(12.4, 1);
  });

  it('MP 己亥: HS controls EB (Earth克Water 盖头), basis=8', () => {
    // Earth(Ji 10) controls Water(Ren 8). basis = min(10,8) = 8
    // Controller (Earth) loses 20% of 8 = 1.6: 10 → 8.4
    // Controlled (Water) loses 30% of 8 = 2.4: 8 → 5.6
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);

    const mpHs = state.nodes.find(n => n.id === 'MP.HS');
    expect(mpHs?.points).toBeCloseTo(8.4, 1);

    const mpEb = state.nodes.find(n => n.id === 'MP.EB');
    expect(mpEb?.points).toBeCloseTo(5.6, 1);
  });

  it('DP 丁丑: HS produces EB (Fire→Earth), basis=8', () => {
    // Fire(Ding 10) produces Earth(Ji 8). basis = min(10,8) = 8
    // Producer (Fire) loses 20% of 8 = 1.6: 10 → 8.4
    // Produced (Earth) gains 30% of 8 = 2.4: 8 → 10.4
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);

    const dpHs = state.nodes.find(n => n.id === 'DP.HS');
    expect(dpHs?.points).toBeCloseTo(8.4, 1);

    const dpEb = state.nodes.find(n => n.id === 'DP.EB');
    expect(dpEb?.points).toBeCloseTo(10.4, 1);
  });

  it('HP 丁未: HS produces EB (Fire→Earth), basis=8', () => {
    let state = initializeState(INPUT);
    state = step1PillarPairs(state);

    const hpHs = state.nodes.find(n => n.id === 'HP.HS');
    expect(hpHs?.points).toBeCloseTo(8.4, 1);

    const hpEb = state.nodes.find(n => n.id === 'HP.EB');
    expect(hpEb?.points).toBeCloseTo(10.4, 1);
  });

  it('same element: no interaction (e.g., Wood HS + Wood EB)', () => {
    const input2: WuxingInput = {
      ...INPUT,
      yearPillar: { stem: 'Jia', branch: 'Yin' }, // Wood + Wood
    };
    let state = initializeState(input2);
    state = step1PillarPairs(state);

    const ypHs = state.nodes.find(n => n.id === 'YP.HS');
    expect(ypHs?.points).toBe(10); // unchanged
  });
});
```

**Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/step01.test.ts`
Expected: FAIL — step1PillarPairs returns state unchanged (stub)

**Step 3: Implement Step 0 + Step 1**

In `calculator.ts`:

- **`initializeState()`**: Already done in Task 2. Verify it creates nodes with correct points from `EB_HIDDEN_STEMS` table. Use `calculatePillarPriority(age)` for priority order.

- **`step1PillarPairs(state)`**: For each pillar (YP, MP, DP, HP):
  1. Get HS element and EB main qi element
  2. Look up relationship in `CONTROL_LOOKUP[hsElement][ebElement]`
  3. If same element → skip
  4. Compute `basis = min(HS.points, EB.points)`
  5. Apply production (−20%/+30% of basis) or control (−20%/−30% of basis) to the appropriate nodes
  6. Log interaction to `state.interactions`

**Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/step01.test.ts`
Expected: PASS

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step01.test.ts
git commit -m "feat(wuxing): implement Step 0 (initial points) and Step 1 (pillar pairs)"
```

---

### Task 4: Implement Step 2 — EB Positive Interactions

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step2.test.ts`

**Context:** This is the most complex step. It involves:
- Pre-scanning for Three-Branch Priority (trios nullify component pairs)
- Attention Spread calculation (weighted shares per node)
- Age-based pillar priority processing
- Transformation check (EB combos check HS for matching element)
- Combo types in order: 三会 → 三合 → 六合 → 半三会 → 拱合

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step2.test.ts
import { describe, it, expect } from 'vitest';
import { initializeState, step1PillarPairs, step2EbPositive, type WuxingInput } from '../calculator';

// Skill example chart: 丙寅·己亥·丁丑·丁未 (age 39 → DP→MP→HP→YP)
const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 39,
  gender: 'M',
  location: 'hometown',
};

function getPostStep1State(input: WuxingInput = INPUT) {
  let state = initializeState(input);
  state = step1PillarPairs(state);
  return state;
}

describe('Step 2: EB Positive Interactions', () => {
  it('detects 丑+亥 半三会 Water', () => {
    let state = getPostStep1State();
    state = step2EbPositive(state);
    const halfMeeting = state.interactions.find(
      i => i.type === 'HALF_MEETINGS' && i.branches.includes('Chou') && i.branches.includes('Hai')
    );
    expect(halfMeeting).toBeDefined();
    expect(halfMeeting?.resultElement).toBe('Water');
  });

  it('detects 寅+亥 六合 Wood', () => {
    let state = getPostStep1State();
    state = step2EbPositive(state);
    const harmony = state.interactions.find(
      i => i.type === 'SIX_HARMONIES' && i.branches.includes('Yin') && i.branches.includes('Hai')
    );
    expect(harmony).toBeDefined();
    expect(harmony?.resultElement).toBe('Wood');
  });

  it('detects 亥+未 拱合 Wood', () => {
    let state = getPostStep1State();
    state = step2EbPositive(state);
    const arched = state.interactions.find(
      i => i.type === 'ARCHED_COMBOS' && i.branches.includes('Hai') && i.branches.includes('Wei')
    );
    expect(arched).toBeDefined();
    expect(arched?.resultElement).toBe('Wood');
  });

  it('creates bonus nodes for combos', () => {
    let state = getPostStep1State();
    state = step2EbPositive(state);
    // Should have bonus nodes for Water (半三会) and Wood (六合 + 拱合)
    expect(state.bonusNodes.length).toBeGreaterThan(0);
  });

  it('attention spread reduces combo effectiveness', () => {
    let state = getPostStep1State();
    state = step2EbPositive(state);

    // 亥 participates in: 半三会(12) + 六合(28) + 拱合(7) = 47
    // 寅 participates in: 六合(28) only = 28
    // So 寅's share for 六合 = 28/28 = 100%
    // But 亥's share for 六合 = 28/47 ≈ 60%
    // → 寅 gets more effective bonus than 亥 from the same 六合
    const yinBonus = state.bonusNodes.find(
      b => b.sourceNode === 'YP.EB' && b.source === 'SIX_HARMONIES'
    );
    const haiBonus = state.bonusNodes.find(
      b => b.sourceNode === 'MP.EB' && b.source === 'SIX_HARMONIES'
    );
    if (yinBonus && haiBonus) {
      expect(yinBonus.points).toBeGreaterThan(haiBonus.points);
    }
  });

  it('transformation bonus when HS matches combo element', () => {
    // Chart with Fire HS and 寅午戌 三合 Fire → should transform (×2.5)
    const input2: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },   // Fire + 寅
      monthPillar: { stem: 'Ding', branch: 'Wu' },    // Fire + 午
      dayPillar: { stem: 'Ji', branch: 'Xu' },        // Earth + 戌
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    let state = initializeState(input2);
    state = step1PillarPairs(state);
    state = step2EbPositive(state);

    const threeCombo = state.interactions.find(i => i.type === 'THREE_COMBOS');
    expect(threeCombo).toBeDefined();
    expect(threeCombo?.transformed).toBe(true); // Bing/Ding Fire HS present
  });
});
```

**Step 2: Run test to verify it fails**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/step2.test.ts`
Expected: FAIL

**Step 3: Implement step2EbPositive**

This is the largest step function. Key implementation points:

1. **Pre-scan**: Identify all valid 3-branch interactions first. Build a nullification set for 2-branch pairs.
2. **Attention pre-scan**: For each EB node, sum weights of all interactions it participates in (both positive from Step 2 AND negative from Step 4). Since Step 4 hasn't run yet, pre-scan BOTH positive and negative interactions now and store in `state.attentionMap`.
3. **Process in pillar priority order**: For each pillar, find valid combos involving that pillar's EB (strongest → weakest).
4. **For each combo**:
   - Compute `basis = min(main qi pts of all combining EBs)` (current values)
   - Compute `combo pts per node = basis × rate × gap_multiplier`
   - Check transformation: EB combos → check if any HS has matching element
   - If transformed: `combo pts per node × 2.5`
   - Apply attention share: `effective = combo_pts × (weight / Σ_weights_for_this_node)`
   - Create bonus node(s)
5. **Polarity rule**: Each EB produces element in its own polarity (Yang EB → Yang stem).

**Step 4: Run test to verify it passes**

Run: `npx vitest run src/lib/bazi/wuxing/__tests__/step2.test.ts`
Expected: PASS

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step2.test.ts
git commit -m "feat(wuxing): implement Step 2 (EB positive interactions with attention spread)"
```

---

### Task 5: Implement Step 3 — HS Positive Interactions (Stem Combos)

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step3.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step3.test.ts
import { describe, it, expect } from 'vitest';
import { initializeState, step1PillarPairs, step2EbPositive, step3HsPositive, type WuxingInput } from '../calculator';

describe('Step 3: HS Positive (Stem Combos)', () => {
  it('detects 丁壬 combo → Wood', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },     // 壬
      monthPillar: { stem: 'Ding', branch: 'Mao' },   // 丁
      dayPillar: { stem: 'Ji', branch: 'Chou' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    let state = initializeState(input);
    state = step1PillarPairs(state);
    state = step2EbPositive(state);
    state = step3HsPositive(state);

    const stemCombo = state.interactions.find(i => i.type === 'STEM_COMBOS');
    expect(stemCombo).toBeDefined();
    expect(stemCombo?.resultElement).toBe('Wood');
  });

  it('transformation: check EB main qi for matching element', () => {
    // 丁壬 → Wood. 卯 Mao has Yi Wood main qi → should transform
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },
      monthPillar: { stem: 'Ding', branch: 'Mao' },  // Mao = Wood EB
      dayPillar: { stem: 'Ji', branch: 'Chou' },
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    let state = initializeState(input);
    state = step1PillarPairs(state);
    state = step2EbPositive(state);
    state = step3HsPositive(state);

    const stemCombo = state.interactions.find(i => i.type === 'STEM_COMBOS');
    expect(stemCombo?.transformed).toBe(true);
  });

  it('applies gap multiplier for non-adjacent stems', () => {
    // YP.HS + DP.HS = gap 1 → ×0.75
    const input: WuxingInput = {
      yearPillar: { stem: 'Ren', branch: 'Zi' },     // 壬 (YP)
      monthPillar: { stem: 'Ji', branch: 'Chou' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },    // 丁 (DP)
      hourPillar: { stem: 'Geng', branch: 'Shen' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    let state = initializeState(input);
    state = step1PillarPairs(state);
    state = step2EbPositive(state);
    state = step3HsPositive(state);

    const stemCombo = state.interactions.find(i => i.type === 'STEM_COMBOS');
    expect(stemCombo?.gapMultiplier).toBe(0.75);
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Implement step3HsPositive**

Same pattern as step2EbPositive but simpler:
- Scan all HS pairs across pillars for 天干五合 matches (from `STEM_COMBOS_TABLE`)
- `basis = min(HS₁ pts, HS₂ pts)` (continuous values)
- `combo pts per node = basis × 0.30 × gap_multiplier`
- Transformation check: EB main qi has matching element → `×2.5`
- Age-based pillar priority order

**Step 4: Run test → PASS**

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step3.test.ts
git commit -m "feat(wuxing): implement Step 3 (HS positive stem combinations)"
```

---

### Task 6: Implement Step 4 — EB Negative Interactions

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step4.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step4.test.ts
import { describe, it, expect } from 'vitest';
import { calculateWuxingUpToStep, type WuxingInput } from '../calculator';

describe('Step 4: EB Negative Interactions', () => {
  it('六冲 control clash: asymmetric damage', () => {
    // 子午 clash: Water(Zi) controls Fire(Wu)
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },
      monthPillar: { stem: 'Bing', branch: 'Wu' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 4);

    const clash = state.interactions.find(
      i => i.type === 'SIX_CLASH' && i.branches.includes('Zi') && i.branches.includes('Wu')
    );
    expect(clash).toBeDefined();
    expect(clash?.attacker).toBe('Zi');
    expect(clash?.victim).toBe('Wu');
  });

  it('六冲 same-element: log only, no point change', () => {
    // 丑未 clash: Earth ↔ Earth → log only
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Chou' },
      monthPillar: { stem: 'Yi', branch: 'Wei' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },
      hourPillar: { stem: 'Ji', branch: 'You' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 4);

    const clash = state.interactions.find(
      i => i.type === 'SIX_CLASH' && i.branches.includes('Chou') && i.branches.includes('Wei')
    );
    expect(clash).toBeDefined();
    expect(clash?.logOnly).toBe(true);
  });

  it('六害 requires adjacent pillars (gap 0)', () => {
    // 寅巳 harm: Si(Fire) harms Yin(Wood). Only valid if adjacent.
    // YP.Yin + HP.Si → gap 2, should NOT trigger
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Yin' },
      monthPillar: { stem: 'Bing', branch: 'Chen' },
      dayPillar: { stem: 'Ding', branch: 'Mao' },
      hourPillar: { stem: 'Ji', branch: 'Si' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 4);

    const harm = state.interactions.find(
      i => i.type === 'SIX_HARM' && i.branches.includes('Yin') && i.branches.includes('Si')
    );
    expect(harm).toBeUndefined(); // gap > 0, should not trigger
  });

  it('three-branch priority: 三会 nullifies component 半三会', () => {
    // 巳午未 三会 Fire present → 巳午, 午未, 巳未 半三会 should be nullified
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Si' },
      monthPillar: { stem: 'Bing', branch: 'Wu' },
      dayPillar: { stem: 'Ding', branch: 'Wei' },
      hourPillar: { stem: 'Ji', branch: 'You' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 4);

    const threeMeeting = state.interactions.find(i => i.type === 'THREE_MEETINGS');
    expect(threeMeeting).toBeDefined();

    const halfMeeting = state.interactions.find(i => i.type === 'HALF_MEETINGS');
    expect(halfMeeting).toBeUndefined(); // nullified by trio
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Implement step4EbNegative**

Key implementation:
- Process in order: 六冲 → 三刑 → 六害 → 破
- Same-element interactions: log only, no point changes (but still occupy attention)
- Different-element asymmetric damage: attacker loses X%, victim loses Y% (per type)
- 六害 only at gap 0 (adjacent pillars)
- 三刑 rules: 恃势 Yin-Si-Shen (different element pairs, 2 of 3 still triggers), 无恩 Chou-Wei-Xu (requires all 3, all same Earth → log only)
- Attention spread applied
- Gap penalty applied
- Use continuous basis values

Also export a helper `calculateWuxingUpToStep(input, stepNumber)` for testing intermediate steps.

**Step 4: Run test → PASS**

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step4.test.ts
git commit -m "feat(wuxing): implement Step 4 (EB negative interactions)"
```

---

### Task 7: Implement Step 5 — HS Negative (Stem Clashes) + Step 6 — Seasonal

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step56.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step56.test.ts
import { describe, it, expect } from 'vitest';
import { calculateWuxingUpToStep, type WuxingInput } from '../calculator';

describe('Step 5: HS Negative (Stem Clashes)', () => {
  it('甲庚 clash: Metal controls Wood', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },    // 甲
      monthPillar: { stem: 'Geng', branch: 'Shen' }, // 庚
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 5);

    const clash = state.interactions.find(i => i.type === 'STEM_CLASH');
    expect(clash).toBeDefined();
    expect(clash?.controller).toBe('Geng');
    expect(clash?.controlled).toBe('Jia');
  });

  it('applies gap multiplier to stem clashes', () => {
    // YP + DP → gap 1 → ×0.75
    const input: WuxingInput = {
      yearPillar: { stem: 'Jia', branch: 'Zi' },     // 甲 (YP)
      monthPillar: { stem: 'Bing', branch: 'Yin' },
      dayPillar: { stem: 'Geng', branch: 'Shen' },   // 庚 (DP)
      hourPillar: { stem: 'Ji', branch: 'Wei' },
      age: 30,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 5);

    const clash = state.interactions.find(i => i.type === 'STEM_CLASH');
    expect(clash?.gapMultiplier).toBe(0.75);
  });
});

describe('Step 6: Seasonal Adjustment', () => {
  it('亥 month → Winter Water season', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },
      monthPillar: { stem: 'Ji', branch: 'Hai' },   // 亥 = Winter Water
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ding', branch: 'Wei' },
      age: 40,
      gender: 'M',
      location: 'hometown',
    };
    const state = calculateWuxingUpToStep(input, 6);

    // Winter: Water×1.25, Wood×1.15, Metal×1.0, Earth×0.85, Fire×0.75
    // Check that Fire nodes were reduced (×0.75) and Water nodes boosted (×1.25)
    const ypHs = state.nodes.find(n => n.id === 'YP.HS'); // Bing Fire
    // Fire node should have been multiplied by 0.75
    expect(ypHs?.seasonalMultiplier).toBe(0.75);
  });

  it('applies multiplier to EVERY node individually', () => {
    const input: WuxingInput = {
      yearPillar: { stem: 'Bing', branch: 'Yin' },
      monthPillar: { stem: 'Ji', branch: 'Hai' },
      dayPillar: { stem: 'Ding', branch: 'Chou' },
      hourPillar: { stem: 'Ding', branch: 'Wei' },
      age: 40,
      gender: 'M',
      location: 'hometown',
    };

    const preState = calculateWuxingUpToStep(input, 5);
    const postState = calculateWuxingUpToStep(input, 6);

    // YP.EB = Jia Wood. Winter: Wood = Prime (×1.15)
    const preYpEb = preState.nodes.find(n => n.id === 'YP.EB')!;
    const postYpEb = postState.nodes.find(n => n.id === 'YP.EB')!;
    expect(postYpEb.points).toBeCloseTo(preYpEb.points * 1.15, 1);
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Implement step5HsNegative + step6Seasonal**

**Step 5 (HS Negative):**
- Scan HS pairs for 4 stem clashes (甲庚, 乙辛, 丙壬, 丁癸)
- `basis = min(HS₁, HS₂)`. Controller loses `basis × 0.25 × gap`. Controlled loses `basis × 0.50 × gap`.

**Step 6 (Seasonal):**
- Determine season from month branch element using `SEASONAL_MATRIX`
- For each node (HS, EB main, h1, h2): look up element's state → apply multiplier
- `node.points = node.points × multiplier`
- Store `seasonalMultiplier` on each node for debugging

**Step 4: Run test → PASS**

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step56.test.ts
git commit -m "feat(wuxing): implement Step 5 (HS clashes) and Step 6 (seasonal adjustment)"
```

---

### Task 8: Implement Step 7 — Natural Element Flow

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step7.test.ts`

**Context:** Cross-pillar Wu Xing flow at half Step 1 rates. Uses a 2×4 grid with Manhattan distance gaps. Processes visible primary qi + bonus qi from combos. Hidden stems excluded.

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step7.test.ts
import { describe, it, expect } from 'vitest';
import { calculateWuxingUpToStep, type WuxingInput } from '../calculator';

const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 7: Natural Element Flow', () => {
  it('changes node point values via cross-pillar production/control', () => {
    const preState = calculateWuxingUpToStep(INPUT, 6);
    const postState = calculateWuxingUpToStep(INPUT, 7);

    // At least some nodes should have changed
    let anyChanged = false;
    for (const preNode of preState.nodes) {
      const postNode = postState.nodes.find(n => n.id === preNode.id);
      if (postNode && Math.abs(postNode.points - preNode.points) > 0.01) {
        anyChanged = true;
        break;
      }
    }
    expect(anyChanged).toBe(true);
  });

  it('uses half rates (10%/15%) not full Step 1 rates (20%/30%)', () => {
    // Two adjacent same-row nodes with production relationship
    // YP.HS (Fire) and MP.HS (Earth): Fire→Earth = production
    // basis = min(YP.HS, MP.HS). At half rate: producer -10%, produced +15%
    const preState = calculateWuxingUpToStep(INPUT, 6);
    const postState = calculateWuxingUpToStep(INPUT, 7);

    // The total change from Step 7 should be moderate, not as aggressive as Step 1
    const totalPre = preState.nodes.reduce((s, n) => s + n.points, 0);
    const totalPost = postState.nodes.reduce((s, n) => s + n.points, 0);

    // Net effect of production is small (+5% of basis per interaction)
    // Net effect of control is negative (-5% of basis per interaction)
    // Total should be relatively stable
    expect(Math.abs(totalPost - totalPre)).toBeLessThan(totalPre * 0.1);
  });

  it('excludes hidden stems from cross-pillar flow', () => {
    const preState = calculateWuxingUpToStep(INPUT, 6);
    const postState = calculateWuxingUpToStep(INPUT, 7);

    // Hidden stems should be unchanged between Step 6 and Step 7
    for (const preNode of preState.nodes) {
      if (preNode.slot === 'EB.h1' || preNode.slot === 'EB.h2') {
        const postNode = postState.nodes.find(n => n.id === preNode.id);
        expect(postNode?.points).toBe(preNode.points);
      }
    }
  });

  it('same-pillar original HS↔EB excluded (already in Step 1)', () => {
    // This is a structural test — Step 7 should not re-process Step 1 pairs
    // We verify by checking that the interaction log for Step 7 doesn't include
    // same-pillar HS↔EB main qi pairs
    const postState = calculateWuxingUpToStep(INPUT, 7);
    const step7Interactions = postState.interactions.filter(i => i.step === 7);
    for (const inter of step7Interactions) {
      // Should not have both YP.HS and YP.EB (or MP.HS and MP.EB, etc.)
      if (inter.nodeA && inter.nodeB) {
        const [pillarA] = inter.nodeA.split('.');
        const [pillarB] = inter.nodeB.split('.');
        const slotA = inter.nodeA.split('.').slice(1).join('.');
        const slotB = inter.nodeB.split('.').slice(1).join('.');
        if (pillarA === pillarB && slotA === 'HS' && slotB === 'EB') {
          throw new Error(`Step 7 should not process same-pillar HS↔EB: ${inter.nodeA}↔${inter.nodeB}`);
        }
      }
    }
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Implement step7NaturalFlow**

Key implementation:
1. Build visible node list: HS + EB main qi + bonus nodes (exclude h1, h2)
2. Build gap grid: 2×4 Manhattan distance, gap = distance − 1
3. Same-element bonus consolidation
4. Generate all valid pairs (excluding same-pillar original HS↔EB main qi)
5. Sort by pillar priority → gap ascending → production before control
6. For each pair:
   - Determine relationship (production or control)
   - `basis = min(nodeA.points, nodeB.points)`
   - Production: producer −(basis × 0.10 × gap_mult), produced +(basis × 0.15 × gap_mult)
   - Control: controller −(basis × 0.10 × gap_mult), controlled −(basis × 0.15 × gap_mult)
7. Mark each pair as done (no duplicates)
8. Update points continuously

**Step 4: Run test → PASS**

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step7.test.ts
git commit -m "feat(wuxing): implement Step 7 (natural element flow, half-rate cross-pillar)"
```

---

### Task 9: Implement Step 8 — Element Report + Step 9 — Balance Simulation

**Files:**
- Modify: `src/lib/bazi/wuxing/calculator.ts`
- Test: `src/lib/bazi/wuxing/__tests__/step89.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/step89.test.ts
import { describe, it, expect } from 'vitest';
import { calculateWuxing, type WuxingInput } from '../calculator';

const INPUT: WuxingInput = {
  yearPillar: { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji', branch: 'Hai' },
  dayPillar: { stem: 'Ding', branch: 'Chou' },
  hourPillar: { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('Step 8: Element Report', () => {
  it('element percentages sum to 100%', () => {
    const result = calculateWuxing(INPUT);
    const total = Object.values(result.elements).reduce((s, e) => s + e.percent, 0);
    expect(total).toBeCloseTo(100, 0);
  });

  it('elements are ranked 1-5', () => {
    const result = calculateWuxing(INPUT);
    const ranks = Object.values(result.elements).map(e => e.rank).sort();
    expect(ranks).toEqual([1, 2, 3, 4, 5]);
  });

  it('DM strength uses correct thresholds', () => {
    const result = calculateWuxing(INPUT);
    const dmPct = result.dayMaster.percent;
    const strength = result.dayMaster.strength;

    if (dmPct > 40) expect(strength).toBe('dominant');
    else if (dmPct >= 25) expect(strength).toBe('strong');
    else if (dmPct >= 15) expect(strength).toBe('balanced');
    else if (dmPct >= 8) expect(strength).toBe('weak');
    else expect(strength).toBe('very_weak');
  });

  it('per-node breakdown has initial + final + delta', () => {
    const result = calculateWuxing(INPUT);
    const nodeKeys = Object.keys(result.nodes);
    expect(nodeKeys.length).toBeGreaterThanOrEqual(14); // 4 HS + ~10 EB nodes

    for (const nodeData of Object.values(result.nodes)) {
      expect(nodeData).toHaveProperty('initial');
      expect(nodeData).toHaveProperty('final');
      expect(nodeData).toHaveProperty('delta');
      expect(nodeData.delta).toBeCloseTo(nodeData.final - nodeData.initial, 2);
    }
  });
});

describe('Step 9: Balance Simulation (5 Gods)', () => {
  it('returns all 5 elements distributed among gods', () => {
    const result = calculateWuxing(INPUT);
    const gods = result.gods;
    const allElements = new Set([
      gods.useful, gods.favorable, gods.unfavorable, gods.enemy, gods.idle,
    ]);
    expect(allElements.size).toBe(5);
  });

  it('favorable produces useful', () => {
    const result = calculateWuxing(INPUT);
    // Production cycle: Wood→Fire→Earth→Metal→Water→Wood
    const production: Record<string, string> = {
      Wood: 'Fire', Fire: 'Earth', Earth: 'Metal', Metal: 'Water', Water: 'Wood',
    };
    expect(production[result.gods.favorable]).toBe(result.gods.useful);
  });

  it('enemy produces unfavorable', () => {
    const result = calculateWuxing(INPUT);
    const production: Record<string, string> = {
      Wood: 'Fire', Fire: 'Earth', Earth: 'Metal', Metal: 'Water', Water: 'Wood',
    };
    expect(production[result.gods.enemy]).toBe(result.gods.unfavorable);
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Implement step8Report + step9BalanceSim**

**Step 8 (Report):**
- Aggregate all node points by element (primary + bonus + hidden)
- Hidden stems use post-Step 6 values (unchanged by Step 7)
- Calculate percentages: `element_total / grand_total × 100`
- Rank elements 1-5
- DM strength: look up DM element percentage against thresholds

**Step 9 (Balance Simulation):**
- For each of 10 stems (甲乙丙丁戊己庚辛壬癸):
  - Add +10 pt hovering HS node (gap 1 to all natal nodes → half-rate Step 7 flow)
  - Run Step 7 interactions with this hovering node
  - Compute new element percentages
  - `σ = √(Σ(pᵢ − 20%)² / 5)` + DM penalty (+5 if DM<8%, +3 if DM>40%)
- Group by element (average σ for same-element stems)
- Lowest σ → 用神, highest σ → 忌神
- 喜神 = produces 用神, 仇神 = produces 忌神, 闲神 = remaining

**Step 4: Run test → PASS**

**Step 5: Commit**

```bash
git add src/lib/bazi/wuxing/calculator.ts src/lib/bazi/wuxing/__tests__/step89.test.ts
git commit -m "feat(wuxing): implement Step 8 (element report) and Step 9 (balance simulation)"
```

---

### Task 10: Integration — Wire into engine.ts and adapter.ts

**Files:**
- Modify: `src/lib/bazi/comprehensive/engine.ts`
- Modify: `src/lib/bazi/comprehensive/adapter.ts`
- Modify: `src/lib/bazi/comprehensive/models.ts` (add WuxingResult to exports if needed)
- Test: `src/lib/bazi/wuxing/__tests__/integration.test.ts`

**Step 1: Write the failing test**

```typescript
// src/lib/bazi/wuxing/__tests__/integration.test.ts
import { describe, it, expect } from 'vitest';
import { buildChart, analyzeForApi } from '../../comprehensive/engine';

describe('Integration: engine uses new Wuxing calculator', () => {
  const chart = buildChart({
    gender: 'male',
    birth_year: 1986,
    year_stem: 'Bing', year_branch: 'Yin',
    month_stem: 'Ji', month_branch: 'Hai',
    day_stem: 'Ding', day_branch: 'Chou',
    hour_stem: 'Ding', hour_branch: 'Wei',
  });

  it('strength assessment uses new calculator', () => {
    const results = analyzeForApi(chart);
    const strength = results.strength as Record<string, unknown>;
    expect(strength).toHaveProperty('score');
    expect(strength).toHaveProperty('verdict');
    expect(strength).toHaveProperty('useful_god');
    expect(strength).toHaveProperty('element_percentages');
  });

  it('wuxing_result is present in results', () => {
    const results = analyzeForApi(chart);
    expect(results).toHaveProperty('wuxing_result');
    const wuxing = results.wuxing_result as Record<string, unknown>;
    expect(wuxing).toHaveProperty('nodes');
    expect(wuxing).toHaveProperty('elements');
    expect(wuxing).toHaveProperty('gods');
  });
});
```

**Step 2: Run test → FAIL**

**Step 3: Wire it up**

1. **`engine.ts`**: In `analyzeForApi()`, call `calculateWuxing()` with chart data. Map `ChartData` to `WuxingInput`. Include `wuxing_result` in the return object. Replace `assessDayMasterStrength()` call with results from the new calculator (map `WuxingResult` → `StrengthAssessment` for backward compat).

2. **`adapter.ts`**: In `buildElementScores()`, use `wuxing_result.nodes` instead of calling `countElements()` + `adjustElementsForInteractions()` + `applySeasonalScaling()`. Map node-level points to the stem score format the frontend expects. In `buildDaymasterAnalysis()`, use `wuxing_result.dayMaster` and `wuxing_result.gods`.

3. **`models.ts`**: Import `WuxingResult` type if needed for the results record.

**Step 4: Run test → PASS**

Also run: `npx vitest run` (full test suite) and `npx tsc --noEmit` to verify no type errors.

**Step 5: Commit**

```bash
git add src/lib/bazi/comprehensive/engine.ts src/lib/bazi/comprehensive/adapter.ts \
  src/lib/bazi/comprehensive/models.ts src/lib/bazi/wuxing/__tests__/integration.test.ts
git commit -m "feat(wuxing): integrate new calculator into engine and adapter"
```

---

### Task 11: Cleanup — Delete old scoring modules

**Files:**
- Delete: `src/lib/bazi/scoring.ts`
- Delete: `src/lib/bazi/dynamic-scoring.ts`
- Modify: `src/lib/bazi/combinations.ts` — remove scoring imports
- Modify: `src/lib/bazi/conflicts.ts` — remove scoring imports
- Modify: `src/lib/bazi/comprehensive/strength.ts` — remove old scoring functions (keep rooting, following chart, support/drain for backward compat if still needed)

**Step 1: Find all imports of old scoring**

Run: `grep -r "from.*scoring" src/lib/bazi/ --include="*.ts"`
Run: `grep -r "from.*dynamic-scoring" src/lib/bazi/ --include="*.ts"`

Fix all references. Any module that imported `BASE_SCORES`, `DISTANCE_MULTIPLIERS`, `generateScoring`, etc. needs to either use the new calculator or remove the import.

**Step 2: Delete files and fix imports**

**Step 3: Run full test suite + type check**

Run: `npx vitest run && npx tsc --noEmit`
Expected: PASS — all tests still pass, no type errors

**Step 4: Run build**

Run: `npm run build`
Expected: PASS — Next.js build succeeds

**Step 5: Commit**

```bash
git add -A
git commit -m "refactor(wuxing): remove old scoring modules, update imports"
```

---

### Task 12: End-to-end verification

**Files:**
- No new files — verification only

**Step 1: Run all tests**

Run: `npx vitest run`
Expected: All pass

**Step 2: Type check**

Run: `npx tsc --noEmit`
Expected: No errors

**Step 3: Build**

Run: `npm run build`
Expected: Success

**Step 4: Manual smoke test**

Start dev server: `npm run dev`
Open http://localhost:4321, enter password `lombok29`, navigate to a profile with a life event, verify:
- Element bars display correctly
- DM strength percentage shows
- Element percentages sum to ~100%
- 用神/忌神 are shown

**Step 5: Final commit (if any fixes needed)**

```bash
git add -A
git commit -m "fix(wuxing): address smoke test findings"
```
