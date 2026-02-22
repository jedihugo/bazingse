import { describe, it, expect } from 'vitest';
import {
  HS_POINTS,
  EB_HIDDEN_STEMS,
  EB_POLARITY,
  PILLAR_GAP,
  gapMultiplier,
  COMBO_RATES,
  TRANSFORMATION_MULTIPLIER,
  ATTENTION_WEIGHTS,
  SEASONAL_MULTIPLIERS,
  SEASONAL_MATRIX,
  MONTH_BRANCH_SEASON,
  CONTROL_LOOKUP,
  THREE_MEETINGS_TABLE,
  THREE_COMBOS_TABLE,
  SIX_HARMONIES_TABLE,
  HALF_MEETINGS_TABLE,
  ARCHED_COMBOS_TABLE,
  STEM_COMBOS_TABLE,
  SIX_CLASHES_TABLE,
  PUNISHMENTS_TABLE,
  SIX_HARMS_TABLE,
  DESTRUCTIONS_TABLE,
  STEM_CLASHES_TABLE,
  NEGATIVE_RATES,
  getStep7Gap,
} from '../tables';

// =============================================================================
// 1. HS_POINTS
// =============================================================================

describe('HS_POINTS', () => {
  it('should have exactly 10 entries', () => {
    expect(Object.keys(HS_POINTS)).toHaveLength(10);
  });

  it('should assign 10 points to every stem', () => {
    for (const stem of Object.values(HS_POINTS)) {
      expect(stem.points).toBe(10);
    }
  });

  it('should have correct elements', () => {
    expect(HS_POINTS.Jia.element).toBe('Wood');
    expect(HS_POINTS.Bing.element).toBe('Fire');
    expect(HS_POINTS.Wu.element).toBe('Earth');
    expect(HS_POINTS.Geng.element).toBe('Metal');
    expect(HS_POINTS.Ren.element).toBe('Water');
  });

  it('should have correct polarities', () => {
    expect(HS_POINTS.Jia.polarity).toBe('Yang');
    expect(HS_POINTS.Yi.polarity).toBe('Yin');
    expect(HS_POINTS.Bing.polarity).toBe('Yang');
    expect(HS_POINTS.Ding.polarity).toBe('Yin');
  });

  it('should have 2 stems per element', () => {
    const counts: Record<string, number> = {};
    for (const stem of Object.values(HS_POINTS)) {
      counts[stem.element] = (counts[stem.element] || 0) + 1;
    }
    expect(counts).toEqual({ Wood: 2, Fire: 2, Earth: 2, Metal: 2, Water: 2 });
  });
});

// =============================================================================
// 2. EB_HIDDEN_STEMS
// =============================================================================

describe('EB_HIDDEN_STEMS', () => {
  it('should have exactly 12 entries', () => {
    expect(Object.keys(EB_HIDDEN_STEMS)).toHaveLength(12);
  });

  it('pure qi branches (1 hidden stem) should total 10 points', () => {
    const pureBranches = ['Zi', 'Mao', 'You'] as const;
    for (const branch of pureBranches) {
      const stems = EB_HIDDEN_STEMS[branch];
      expect(stems).toHaveLength(1);
      expect(stems[0].points).toBe(10);
    }
  });

  it('2-qi branches should have 8 + 3 = 11 total points', () => {
    const twoBranches = ['Wu', 'Hai'] as const;
    for (const branch of twoBranches) {
      const stems = EB_HIDDEN_STEMS[branch];
      expect(stems).toHaveLength(2);
      expect(stems[0].points).toBe(8);
      expect(stems[1].points).toBe(3);
      const total = stems.reduce((s, e) => s + e.points, 0);
      expect(total).toBe(11);
    }
  });

  it('3-qi branches should have 8 + 3 + 1 = 12 total points', () => {
    const threeBranches = ['Chou', 'Yin', 'Chen', 'Si', 'Wei', 'Shen', 'Xu'] as const;
    for (const branch of threeBranches) {
      const stems = EB_HIDDEN_STEMS[branch];
      expect(stems).toHaveLength(3);
      expect(stems[0].points).toBe(8);
      expect(stems[1].points).toBe(3);
      expect(stems[2].points).toBe(1);
      const total = stems.reduce((s, e) => s + e.points, 0);
      expect(total).toBe(12);
    }
  });

  it('Zi should contain only Gui/Water', () => {
    expect(EB_HIDDEN_STEMS.Zi).toEqual([{ stem: 'Gui', element: 'Water', points: 10 }]);
  });

  it('Yin should contain Jia/Wood, Bing/Fire, Wu/Earth', () => {
    expect(EB_HIDDEN_STEMS.Yin[0]).toEqual({ stem: 'Jia', element: 'Wood', points: 8 });
    expect(EB_HIDDEN_STEMS.Yin[1]).toEqual({ stem: 'Bing', element: 'Fire', points: 3 });
    expect(EB_HIDDEN_STEMS.Yin[2]).toEqual({ stem: 'Wu', element: 'Earth', points: 1 });
  });

  it('Wu branch should contain Ding/Fire and Ji/Earth', () => {
    expect(EB_HIDDEN_STEMS.Wu[0]).toEqual({ stem: 'Ding', element: 'Fire', points: 8 });
    expect(EB_HIDDEN_STEMS.Wu[1]).toEqual({ stem: 'Ji', element: 'Earth', points: 3 });
  });
});

// =============================================================================
// 3. EB_POLARITY
// =============================================================================

describe('EB_POLARITY', () => {
  it('should have exactly 12 entries', () => {
    expect(Object.keys(EB_POLARITY)).toHaveLength(12);
  });

  it('should have 6 Yang and 6 Yin', () => {
    const values = Object.values(EB_POLARITY);
    expect(values.filter(v => v === 'Yang')).toHaveLength(6);
    expect(values.filter(v => v === 'Yin')).toHaveLength(6);
  });

  it('Yang branches are Zi, Yin, Chen, Wu, Shen, Xu', () => {
    expect(EB_POLARITY.Zi).toBe('Yang');
    expect(EB_POLARITY.Yin).toBe('Yang');
    expect(EB_POLARITY.Chen).toBe('Yang');
    expect(EB_POLARITY.Wu).toBe('Yang');
    expect(EB_POLARITY.Shen).toBe('Yang');
    expect(EB_POLARITY.Xu).toBe('Yang');
  });

  it('Yin branches are Chou, Mao, Si, Wei, You, Hai', () => {
    expect(EB_POLARITY.Chou).toBe('Yin');
    expect(EB_POLARITY.Mao).toBe('Yin');
    expect(EB_POLARITY.Si).toBe('Yin');
    expect(EB_POLARITY.Wei).toBe('Yin');
    expect(EB_POLARITY.You).toBe('Yin');
    expect(EB_POLARITY.Hai).toBe('Yin');
  });
});

// =============================================================================
// 4. PILLAR_GAP + gapMultiplier
// =============================================================================

describe('PILLAR_GAP', () => {
  it('adjacent pillar pairs have gap 0', () => {
    expect(PILLAR_GAP['YP']['MP']).toBe(0);
    expect(PILLAR_GAP['MP']['DP']).toBe(0);
    expect(PILLAR_GAP['DP']['HP']).toBe(0);
  });

  it('1-step apart pairs have gap 1', () => {
    expect(PILLAR_GAP['YP']['DP']).toBe(1);
    expect(PILLAR_GAP['MP']['HP']).toBe(1);
  });

  it('2-step apart pair has gap 2', () => {
    expect(PILLAR_GAP['YP']['HP']).toBe(2);
  });

  it('is symmetric', () => {
    const pillars = ['YP', 'MP', 'DP', 'HP'] as const;
    for (const a of pillars) {
      for (const b of pillars) {
        expect(PILLAR_GAP[a][b]).toBe(PILLAR_GAP[b][a]);
      }
    }
  });

  it('self-gap is always 0', () => {
    expect(PILLAR_GAP['YP']['YP']).toBe(0);
    expect(PILLAR_GAP['MP']['MP']).toBe(0);
    expect(PILLAR_GAP['DP']['DP']).toBe(0);
    expect(PILLAR_GAP['HP']['HP']).toBe(0);
  });
});

describe('gapMultiplier', () => {
  it('gap 0 -> 1.0', () => expect(gapMultiplier(0)).toBe(1.0));
  it('gap 1 -> 0.75', () => expect(gapMultiplier(1)).toBe(0.75));
  it('gap 2 -> 0.5', () => expect(gapMultiplier(2)).toBe(0.5));
  it('gap 3 -> 0.25', () => expect(gapMultiplier(3)).toBe(0.25));
  it('gap 4+ -> 0.25', () => expect(gapMultiplier(5)).toBe(0.25));
  it('negative gap -> 1.0', () => expect(gapMultiplier(-1)).toBe(1.0));
});

// =============================================================================
// 5. COMBO_RATES
// =============================================================================

describe('COMBO_RATES', () => {
  it('THREE_MEETINGS = 0.30', () => expect(COMBO_RATES.THREE_MEETINGS).toBe(0.30));
  it('THREE_COMBOS = 0.25', () => expect(COMBO_RATES.THREE_COMBOS).toBe(0.25));
  it('SIX_HARMONIES = 0.20', () => expect(COMBO_RATES.SIX_HARMONIES).toBe(0.20));
  it('HALF_MEETINGS = 0.20', () => expect(COMBO_RATES.HALF_MEETINGS).toBe(0.20));
  it('ARCHED_COMBOS = 0.15', () => expect(COMBO_RATES.ARCHED_COMBOS).toBe(0.15));
  it('STEM_COMBOS = 0.30', () => expect(COMBO_RATES.STEM_COMBOS).toBe(0.30));
});

// =============================================================================
// 6. TRANSFORMATION_MULTIPLIER
// =============================================================================

describe('TRANSFORMATION_MULTIPLIER', () => {
  it('should be 2.5', () => expect(TRANSFORMATION_MULTIPLIER).toBe(2.5));
});

// =============================================================================
// 7. ATTENTION_WEIGHTS
// =============================================================================

describe('ATTENTION_WEIGHTS', () => {
  it('THREE_MEETINGS = 63', () => expect(ATTENTION_WEIGHTS.THREE_MEETINGS).toBe(63));
  it('THREE_COMBOS = 42', () => expect(ATTENTION_WEIGHTS.THREE_COMBOS).toBe(42));
  it('SIX_CLASH = 42', () => expect(ATTENTION_WEIGHTS.SIX_CLASH).toBe(42));
  it('PUNISHMENT_FULL = 42', () => expect(ATTENTION_WEIGHTS.PUNISHMENT_FULL).toBe(42));
  it('SIX_HARMONIES = 28', () => expect(ATTENTION_WEIGHTS.SIX_HARMONIES).toBe(28));
  it('DESTRUCTION = 28', () => expect(ATTENTION_WEIGHTS.DESTRUCTION).toBe(28));
  it('SIX_HARM = 28', () => expect(ATTENTION_WEIGHTS.SIX_HARM).toBe(28));
  it('HALF_MEETINGS = 12', () => expect(ATTENTION_WEIGHTS.HALF_MEETINGS).toBe(12));
  it('ARCHED_COMBO = 7', () => expect(ATTENTION_WEIGHTS.ARCHED_COMBO).toBe(7));
});

// =============================================================================
// 8. SEASONAL_MULTIPLIERS
// =============================================================================

describe('SEASONAL_MULTIPLIERS', () => {
  it('Prosperous = 1.25', () => expect(SEASONAL_MULTIPLIERS.Prosperous).toBe(1.25));
  it('Prime = 1.15', () => expect(SEASONAL_MULTIPLIERS.Prime).toBe(1.15));
  it('Rest = 1.0', () => expect(SEASONAL_MULTIPLIERS.Rest).toBe(1.0));
  it('Imprisoned = 0.85', () => expect(SEASONAL_MULTIPLIERS.Imprisoned).toBe(0.85));
  it('Dead = 0.75', () => expect(SEASONAL_MULTIPLIERS.Dead).toBe(0.75));
});

// =============================================================================
// 9. SEASONAL_MATRIX
// =============================================================================

describe('SEASONAL_MATRIX', () => {
  it('has 5 season entries', () => {
    expect(Object.keys(SEASONAL_MATRIX)).toHaveLength(5);
  });

  it('each season maps to 5 target elements', () => {
    for (const season of Object.values(SEASONAL_MATRIX)) {
      expect(Object.keys(season)).toHaveLength(5);
    }
  });

  it('same element is always Prosperous', () => {
    const elements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'] as const;
    for (const el of elements) {
      expect(SEASONAL_MATRIX[el][el]).toBe('Prosperous');
    }
  });

  it('Winter (Water season) is correct', () => {
    expect(SEASONAL_MATRIX.Water.Water).toBe('Prosperous');  // 旺
    expect(SEASONAL_MATRIX.Water.Wood).toBe('Prime');         // 相 (Water produces Wood)
    expect(SEASONAL_MATRIX.Water.Metal).toBe('Rest');         // 休 (Metal produces Water)
    expect(SEASONAL_MATRIX.Water.Earth).toBe('Imprisoned');   // 囚 (Earth controls Water)
    expect(SEASONAL_MATRIX.Water.Fire).toBe('Dead');          // 死 (Water controls Fire)
  });

  it('Spring (Wood season) is correct', () => {
    expect(SEASONAL_MATRIX.Wood.Wood).toBe('Prosperous');
    expect(SEASONAL_MATRIX.Wood.Fire).toBe('Prime');
    expect(SEASONAL_MATRIX.Wood.Water).toBe('Rest');
    expect(SEASONAL_MATRIX.Wood.Metal).toBe('Imprisoned');
    expect(SEASONAL_MATRIX.Wood.Earth).toBe('Dead');
  });

  it('Summer (Fire season) is correct', () => {
    expect(SEASONAL_MATRIX.Fire.Fire).toBe('Prosperous');
    expect(SEASONAL_MATRIX.Fire.Earth).toBe('Prime');
    expect(SEASONAL_MATRIX.Fire.Wood).toBe('Rest');
    expect(SEASONAL_MATRIX.Fire.Water).toBe('Imprisoned');
    expect(SEASONAL_MATRIX.Fire.Metal).toBe('Dead');
  });

  it('each season has exactly one of each state', () => {
    for (const season of Object.values(SEASONAL_MATRIX)) {
      const states = Object.values(season);
      expect(states.filter(s => s === 'Prosperous')).toHaveLength(1);
      expect(states.filter(s => s === 'Prime')).toHaveLength(1);
      expect(states.filter(s => s === 'Rest')).toHaveLength(1);
      expect(states.filter(s => s === 'Imprisoned')).toHaveLength(1);
      expect(states.filter(s => s === 'Dead')).toHaveLength(1);
    }
  });
});

// =============================================================================
// 10. MONTH_BRANCH_SEASON
// =============================================================================

describe('MONTH_BRANCH_SEASON', () => {
  it('has exactly 12 entries', () => {
    expect(Object.keys(MONTH_BRANCH_SEASON)).toHaveLength(12);
  });

  it('Spring branches map to Wood', () => {
    expect(MONTH_BRANCH_SEASON.Yin).toBe('Wood');
    expect(MONTH_BRANCH_SEASON.Mao).toBe('Wood');
  });

  it('Summer branches map to Fire', () => {
    expect(MONTH_BRANCH_SEASON.Si).toBe('Fire');
    expect(MONTH_BRANCH_SEASON.Wu).toBe('Fire');
  });

  it('Autumn branches map to Metal', () => {
    expect(MONTH_BRANCH_SEASON.Shen).toBe('Metal');
    expect(MONTH_BRANCH_SEASON.You).toBe('Metal');
  });

  it('Winter branches map to Water', () => {
    expect(MONTH_BRANCH_SEASON.Hai).toBe('Water');
    expect(MONTH_BRANCH_SEASON.Zi).toBe('Water');
  });

  it('Transition branches map to Earth', () => {
    expect(MONTH_BRANCH_SEASON.Chen).toBe('Earth');
    expect(MONTH_BRANCH_SEASON.Wei).toBe('Earth');
    expect(MONTH_BRANCH_SEASON.Xu).toBe('Earth');
    expect(MONTH_BRANCH_SEASON.Chou).toBe('Earth');
  });
});

// =============================================================================
// 11. CONTROL_LOOKUP
// =============================================================================

describe('CONTROL_LOOKUP', () => {
  it('same element is always SAME', () => {
    const elements = ['Wood', 'Fire', 'Earth', 'Metal', 'Water'] as const;
    for (const el of elements) {
      expect(CONTROL_LOOKUP[el][el]).toBe('SAME');
    }
  });

  it('Wood produces Fire', () => {
    expect(CONTROL_LOOKUP.Wood.Fire).toBe('HS_PRODUCES_EB');
  });

  it('Wood controls Earth', () => {
    expect(CONTROL_LOOKUP.Wood.Earth).toBe('HS_CONTROLS_EB');
  });

  it('Water produces Wood (EB produces HS)', () => {
    expect(CONTROL_LOOKUP.Wood.Water).toBe('EB_PRODUCES_HS');
  });

  it('Metal controls Wood (EB controls HS)', () => {
    expect(CONTROL_LOOKUP.Wood.Metal).toBe('EB_CONTROLS_HS');
  });

  it('Fire + Earth: Fire produces Earth (common mistake check)', () => {
    expect(CONTROL_LOOKUP.Fire.Earth).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Earth.Fire).toBe('EB_PRODUCES_HS');
  });

  it('is fully populated: 5x5 = 25 entries', () => {
    let count = 0;
    for (const row of Object.values(CONTROL_LOOKUP)) {
      count += Object.keys(row).length;
    }
    expect(count).toBe(25);
  });

  it('production cycle direction is consistent', () => {
    // Wood->Fire->Earth->Metal->Water->Wood
    expect(CONTROL_LOOKUP.Wood.Fire).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Fire.Earth).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Earth.Metal).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Metal.Water).toBe('HS_PRODUCES_EB');
    expect(CONTROL_LOOKUP.Water.Wood).toBe('HS_PRODUCES_EB');
  });

  it('control cycle direction is consistent', () => {
    // Wood->Earth->Water->Fire->Metal->Wood
    expect(CONTROL_LOOKUP.Wood.Earth).toBe('HS_CONTROLS_EB');
    expect(CONTROL_LOOKUP.Earth.Water).toBe('HS_CONTROLS_EB');
    expect(CONTROL_LOOKUP.Water.Fire).toBe('HS_CONTROLS_EB');
    expect(CONTROL_LOOKUP.Fire.Metal).toBe('HS_CONTROLS_EB');
    expect(CONTROL_LOOKUP.Metal.Wood).toBe('HS_CONTROLS_EB');
  });
});

// =============================================================================
// 12. Combo tables (positive interactions)
// =============================================================================

describe('THREE_MEETINGS_TABLE', () => {
  it('has 4 entries', () => {
    expect(Object.keys(THREE_MEETINGS_TABLE)).toHaveLength(4);
  });

  it('Yin-Mao-Chen = Wood', () => {
    expect(THREE_MEETINGS_TABLE['Yin-Mao-Chen'].element).toBe('Wood');
  });

  it('Si-Wu-Wei = Fire', () => {
    expect(THREE_MEETINGS_TABLE['Si-Wu-Wei'].element).toBe('Fire');
  });

  it('Shen-You-Xu = Metal', () => {
    expect(THREE_MEETINGS_TABLE['Shen-You-Xu'].element).toBe('Metal');
  });

  it('Hai-Zi-Chou = Water', () => {
    expect(THREE_MEETINGS_TABLE['Hai-Zi-Chou'].element).toBe('Water');
  });
});

describe('THREE_COMBOS_TABLE', () => {
  it('has 4 entries', () => {
    expect(Object.keys(THREE_COMBOS_TABLE)).toHaveLength(4);
  });

  it('Hai-Mao-Wei = Wood', () => {
    expect(THREE_COMBOS_TABLE['Hai-Mao-Wei'].element).toBe('Wood');
  });

  it('Yin-Wu-Xu = Fire', () => {
    expect(THREE_COMBOS_TABLE['Yin-Wu-Xu'].element).toBe('Fire');
  });

  it('Si-You-Chou = Metal', () => {
    expect(THREE_COMBOS_TABLE['Si-You-Chou'].element).toBe('Metal');
  });

  it('Shen-Zi-Chen = Water', () => {
    expect(THREE_COMBOS_TABLE['Shen-Zi-Chen'].element).toBe('Water');
  });
});

describe('SIX_HARMONIES_TABLE', () => {
  it('has 6 entries', () => {
    expect(Object.keys(SIX_HARMONIES_TABLE)).toHaveLength(6);
  });

  it('Chou-Zi = Earth', () => expect(SIX_HARMONIES_TABLE['Chou-Zi'].element).toBe('Earth'));
  it('Hai-Yin = Wood', () => expect(SIX_HARMONIES_TABLE['Hai-Yin'].element).toBe('Wood'));
  it('Mao-Xu = Fire', () => expect(SIX_HARMONIES_TABLE['Mao-Xu'].element).toBe('Fire'));
  it('Chen-You = Metal', () => expect(SIX_HARMONIES_TABLE['Chen-You'].element).toBe('Metal'));
  it('Shen-Si = Water', () => expect(SIX_HARMONIES_TABLE['Shen-Si'].element).toBe('Water'));
  it('Wei-Wu = Fire', () => expect(SIX_HARMONIES_TABLE['Wei-Wu'].element).toBe('Fire'));
});

describe('HALF_MEETINGS_TABLE', () => {
  it('has 12 entries', () => {
    expect(Object.keys(HALF_MEETINGS_TABLE)).toHaveLength(12);
  });

  it('has 3 Wood entries', () => {
    const woodEntries = Object.values(HALF_MEETINGS_TABLE).filter(v => v.season === 'Wood');
    expect(woodEntries).toHaveLength(3);
  });

  it('has 3 Fire entries', () => {
    const fireEntries = Object.values(HALF_MEETINGS_TABLE).filter(v => v.season === 'Fire');
    expect(fireEntries).toHaveLength(3);
  });

  it('has 3 Metal entries', () => {
    const metalEntries = Object.values(HALF_MEETINGS_TABLE).filter(v => v.season === 'Metal');
    expect(metalEntries).toHaveLength(3);
  });

  it('has 3 Water entries', () => {
    const waterEntries = Object.values(HALF_MEETINGS_TABLE).filter(v => v.season === 'Water');
    expect(waterEntries).toHaveLength(3);
  });

  it('Mao-Yin = Wood', () => {
    expect(HALF_MEETINGS_TABLE['Mao-Yin'].element).toBe('Wood');
    expect(HALF_MEETINGS_TABLE['Mao-Yin'].season).toBe('Wood');
  });

  it('Si-Wu = Fire', () => {
    expect(HALF_MEETINGS_TABLE['Si-Wu'].element).toBe('Fire');
  });
});

describe('ARCHED_COMBOS_TABLE', () => {
  it('has 4 entries', () => {
    expect(Object.keys(ARCHED_COMBOS_TABLE)).toHaveLength(4);
  });

  it('Hai-Wei = Wood, missing Mao', () => {
    expect(ARCHED_COMBOS_TABLE['Hai-Wei'].element).toBe('Wood');
    expect(ARCHED_COMBOS_TABLE['Hai-Wei'].missing).toBe('Mao');
  });

  it('Yin-Xu = Fire, missing Wu', () => {
    expect(ARCHED_COMBOS_TABLE['Yin-Xu'].element).toBe('Fire');
    expect(ARCHED_COMBOS_TABLE['Yin-Xu'].missing).toBe('Wu');
  });

  it('Chou-Si = Metal, missing You', () => {
    expect(ARCHED_COMBOS_TABLE['Chou-Si'].element).toBe('Metal');
    expect(ARCHED_COMBOS_TABLE['Chou-Si'].missing).toBe('You');
  });

  it('Chen-Shen = Water, missing Zi', () => {
    expect(ARCHED_COMBOS_TABLE['Chen-Shen'].element).toBe('Water');
    expect(ARCHED_COMBOS_TABLE['Chen-Shen'].missing).toBe('Zi');
  });
});

describe('STEM_COMBOS_TABLE', () => {
  it('has 5 entries', () => {
    expect(Object.keys(STEM_COMBOS_TABLE)).toHaveLength(5);
  });

  it('Jia-Ji = Earth', () => expect(STEM_COMBOS_TABLE['Jia-Ji'].element).toBe('Earth'));
  it('Geng-Yi = Metal', () => expect(STEM_COMBOS_TABLE['Geng-Yi'].element).toBe('Metal'));
  it('Bing-Xin = Water', () => expect(STEM_COMBOS_TABLE['Bing-Xin'].element).toBe('Water'));
  it('Ding-Ren = Wood', () => expect(STEM_COMBOS_TABLE['Ding-Ren'].element).toBe('Wood'));
  it('Gui-Wu = Fire', () => expect(STEM_COMBOS_TABLE['Gui-Wu'].element).toBe('Fire'));
});

// =============================================================================
// 13. Negative interaction tables
// =============================================================================

describe('SIX_CLASHES_TABLE', () => {
  it('has 6 entries', () => {
    expect(Object.keys(SIX_CLASHES_TABLE)).toHaveLength(6);
  });

  it('has 4 control-type clashes', () => {
    const controls = Object.values(SIX_CLASHES_TABLE).filter(v => v.type === 'control');
    expect(controls).toHaveLength(4);
  });

  it('has 2 same-type clashes', () => {
    const sames = Object.values(SIX_CLASHES_TABLE).filter(v => v.type === 'same');
    expect(sames).toHaveLength(2);
  });

  it('Wu-Zi: Water controls Fire', () => {
    const clash = SIX_CLASHES_TABLE['Wu-Zi'];
    expect(clash.type).toBe('control');
    expect(clash.attacker).toBe('Zi');
    expect(clash.victim).toBe('Wu');
  });

  it('Shen-Yin: Metal controls Wood', () => {
    const clash = SIX_CLASHES_TABLE['Shen-Yin'];
    expect(clash.type).toBe('control');
    expect(clash.attacker).toBe('Shen');
    expect(clash.victim).toBe('Yin');
  });

  it('Chou-Wei: same element (Earth)', () => {
    expect(SIX_CLASHES_TABLE['Chou-Wei'].type).toBe('same');
  });

  it('Chen-Xu: same element (Earth)', () => {
    expect(SIX_CLASHES_TABLE['Chen-Xu'].type).toBe('same');
  });
});

describe('PUNISHMENTS_TABLE', () => {
  it('has the shi (bullying) punishment', () => {
    const p = PUNISHMENTS_TABLE['Shen-Si-Yin'];
    expect(p.type).toBe('shi');
    expect(p.branches).toEqual(['Yin', 'Si', 'Shen']);
    expect(p.requiresAll).toBe(false);
    expect(p.pairs).toHaveLength(3);
  });

  it('has the wu_li (ungrateful) punishment', () => {
    const p = PUNISHMENTS_TABLE['Chou-Wei-Xu'];
    expect(p.type).toBe('wu_li');
    expect(p.requiresAll).toBe(true);
    expect(p.logOnly).toBe(true);
  });

  it('has the en (rude) punishment', () => {
    const p = PUNISHMENTS_TABLE['Mao-Zi'];
    expect(p.type).toBe('en');
    expect(p.attacker).toBe('Mao');
    expect(p.victim).toBe('Zi');
  });

  it('has 4 self-punishment entries', () => {
    const selfKeys = ['Chen-Chen', 'Wu-Wu', 'You-You', 'Hai-Hai'];
    for (const key of selfKeys) {
      expect(PUNISHMENTS_TABLE[key].type).toBe('self');
      expect(PUNISHMENTS_TABLE[key].logOnly).toBe(true);
    }
  });
});

describe('SIX_HARMS_TABLE', () => {
  it('has 6 entries', () => {
    expect(Object.keys(SIX_HARMS_TABLE)).toHaveLength(6);
  });

  it('Wei-Zi: Earth controls Water', () => {
    expect(SIX_HARMS_TABLE['Wei-Zi'].attacker).toBe('Wei');
    expect(SIX_HARMS_TABLE['Wei-Zi'].victim).toBe('Zi');
  });

  it('Chen-Mao: Wood controls Earth', () => {
    expect(SIX_HARMS_TABLE['Chen-Mao'].attacker).toBe('Mao');
    expect(SIX_HARMS_TABLE['Chen-Mao'].victim).toBe('Chen');
  });
});

describe('DESTRUCTIONS_TABLE', () => {
  it('has 6 entries', () => {
    expect(Object.keys(DESTRUCTIONS_TABLE)).toHaveLength(6);
  });

  it('has 4 control-type destructions', () => {
    const controls = Object.values(DESTRUCTIONS_TABLE).filter(v => v.type === 'control');
    expect(controls).toHaveLength(4);
  });

  it('has 2 same-type destructions', () => {
    const sames = Object.values(DESTRUCTIONS_TABLE).filter(v => v.type === 'same');
    expect(sames).toHaveLength(2);
  });

  it('Shen-Si: Fire controls Metal', () => {
    const d = DESTRUCTIONS_TABLE['Shen-Si'];
    expect(d.type).toBe('control');
    expect(d.attacker).toBe('Si');
    expect(d.victim).toBe('Shen');
  });
});

describe('STEM_CLASHES_TABLE', () => {
  it('has 4 entries', () => {
    expect(Object.keys(STEM_CLASHES_TABLE)).toHaveLength(4);
  });

  it('Geng-Jia: Metal controls Wood', () => {
    expect(STEM_CLASHES_TABLE['Geng-Jia'].controller).toBe('Geng');
    expect(STEM_CLASHES_TABLE['Geng-Jia'].controlled).toBe('Jia');
  });

  it('Bing-Ren: Water controls Fire', () => {
    expect(STEM_CLASHES_TABLE['Bing-Ren'].controller).toBe('Ren');
    expect(STEM_CLASHES_TABLE['Bing-Ren'].controlled).toBe('Bing');
  });
});

// =============================================================================
// 14. NEGATIVE_RATES
// =============================================================================

describe('NEGATIVE_RATES', () => {
  it('SIX_CLASH: 0.25 / 0.50', () => {
    expect(NEGATIVE_RATES.SIX_CLASH.attackerLoss).toBe(0.25);
    expect(NEGATIVE_RATES.SIX_CLASH.victimLoss).toBe(0.50);
  });

  it('PUNISHMENT: 0.20 / 0.40', () => {
    expect(NEGATIVE_RATES.PUNISHMENT.attackerLoss).toBe(0.20);
    expect(NEGATIVE_RATES.PUNISHMENT.victimLoss).toBe(0.40);
  });

  it('SIX_HARM: 0.20 / 0.40', () => {
    expect(NEGATIVE_RATES.SIX_HARM.attackerLoss).toBe(0.20);
    expect(NEGATIVE_RATES.SIX_HARM.victimLoss).toBe(0.40);
  });

  it('DESTRUCTION: 0.20 / 0.40', () => {
    expect(NEGATIVE_RATES.DESTRUCTION.attackerLoss).toBe(0.20);
    expect(NEGATIVE_RATES.DESTRUCTION.victimLoss).toBe(0.40);
  });

  it('STEM_CLASH: 0.25 / 0.50', () => {
    expect(NEGATIVE_RATES.STEM_CLASH.attackerLoss).toBe(0.25);
    expect(NEGATIVE_RATES.STEM_CLASH.victimLoss).toBe(0.50);
  });

  it('victim always loses more than attacker', () => {
    for (const rate of Object.values(NEGATIVE_RATES)) {
      expect(rate.victimLoss).toBeGreaterThan(rate.attackerLoss);
    }
  });
});

// =============================================================================
// 15. getStep7Gap
// =============================================================================

describe('getStep7Gap', () => {
  it('same node has gap 0', () => {
    expect(getStep7Gap('YP.HS', 'YP.HS')).toBe(0);
    expect(getStep7Gap('DP.EB', 'DP.EB')).toBe(0);
  });

  it('adjacent nodes in same row: gap 0 (distance 1 - 1 = 0)', () => {
    expect(getStep7Gap('YP.HS', 'MP.HS')).toBe(0);
    expect(getStep7Gap('MP.EB', 'DP.EB')).toBe(0);
    expect(getStep7Gap('DP.HS', 'HP.HS')).toBe(0);
  });

  it('same column, different row: gap 0 (distance 1 - 1 = 0)', () => {
    expect(getStep7Gap('YP.HS', 'YP.EB')).toBe(0);
    expect(getStep7Gap('DP.HS', 'DP.EB')).toBe(0);
  });

  it('diagonal adjacent: gap 1 (distance 2 - 1 = 1)', () => {
    expect(getStep7Gap('YP.HS', 'MP.EB')).toBe(1);
    expect(getStep7Gap('MP.HS', 'YP.EB')).toBe(1);
  });

  it('2 apart in same row: gap 1 (distance 2 - 1 = 1)', () => {
    expect(getStep7Gap('YP.HS', 'DP.HS')).toBe(1);
    expect(getStep7Gap('MP.EB', 'HP.EB')).toBe(1);
  });

  it('3 apart in same row: gap 2 (distance 3 - 1 = 2)', () => {
    expect(getStep7Gap('YP.HS', 'HP.HS')).toBe(2);
    expect(getStep7Gap('YP.EB', 'HP.EB')).toBe(2);
  });

  it('far corner: gap 3 (distance 4 - 1 = 3)', () => {
    expect(getStep7Gap('YP.HS', 'HP.EB')).toBe(3);
    expect(getStep7Gap('YP.EB', 'HP.HS')).toBe(3);
  });

  it('is symmetric', () => {
    expect(getStep7Gap('YP.HS', 'HP.EB')).toBe(getStep7Gap('HP.EB', 'YP.HS'));
    expect(getStep7Gap('MP.HS', 'DP.EB')).toBe(getStep7Gap('DP.EB', 'MP.HS'));
  });

  it('throws for unknown nodes', () => {
    expect(() => getStep7Gap('XX.HS', 'YP.HS')).toThrow('Unknown node');
    expect(() => getStep7Gap('YP.HS', 'ZZ.EB')).toThrow('Unknown node');
  });
});
