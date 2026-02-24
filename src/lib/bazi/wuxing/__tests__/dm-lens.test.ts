import { calculateDmLens, type DmLensResult } from '../dm-lens';
import { calculateWuxing, type WuxingInput } from '../calculator';

// Chart: 丙寅·己亥·丁丑·丁未 — Ding Fire DM, age 40
const INPUT: WuxingInput = {
  yearPillar:  { stem: 'Bing', branch: 'Yin' },
  monthPillar: { stem: 'Ji',   branch: 'Hai' },
  dayPillar:   { stem: 'Ding', branch: 'Chou' },
  hourPillar:  { stem: 'Ding', branch: 'Wei' },
  age: 40,
  gender: 'M',
  location: 'hometown',
};

describe('calculateDmLens', () => {
  const wuxingResult = calculateWuxing(INPUT);
  const lens = calculateDmLens(wuxingResult);

  it('returns correct DM element and stem', () => {
    expect(lens.dmElement).toBe('Fire');
    expect(lens.dmStem).toBe('Ding');
  });

  it('has 5 rows in the correct order', () => {
    expect(lens.rows).toHaveLength(5);
    expect(lens.rows[0].role).toBe('companion');
    expect(lens.rows[1].role).toBe('resource');
    expect(lens.rows[2].role).toBe('output');
    expect(lens.rows[3].role).toBe('wealth');
    expect(lens.rows[4].role).toBe('power');
  });

  it('maps elements correctly for Fire DM', () => {
    expect(lens.rows[0].element).toBe('Fire');   // companion = same
    expect(lens.rows[1].element).toBe('Wood');   // resource = Wood→Fire
    expect(lens.rows[2].element).toBe('Earth');  // output = Fire→Earth
    expect(lens.rows[3].element).toBe('Metal');  // wealth = Fire→Metal
    expect(lens.rows[4].element).toBe('Water');  // power = Water→Fire
  });

  it('row percentages sum to approximately 100', () => {
    const total = lens.rows.reduce((s, r) => s + r.percent, 0);
    expect(total).toBeCloseTo(100, 0);
  });

  it('support + drain percentages sum to approximately 100', () => {
    expect(lens.supportPercent + lens.drainPercent).toBeCloseTo(100, 0);
  });

  it('each row has a non-empty narrative', () => {
    for (const row of lens.rows) {
      expect(row.narrative.length).toBeGreaterThan(10);
    }
  });

  it('has a non-empty synthesis', () => {
    expect(lens.synthesis.length).toBeGreaterThan(10);
  });

  it('has a valid ratio string', () => {
    expect(lens.ratio).toMatch(/^\d+\.?\d*:\d$/);
  });

  it('has seasonal state for DM element', () => {
    // Month branch is Hai (Winter/Water) — Fire should be 死
    expect(lens.seasonalState).toBe('死');
  });

  it('dmStrengthZh matches strength', () => {
    const strengthMap: Record<string, string> = {
      dominant: '极强', strong: '偏强', balanced: '中和', weak: '偏弱', very_weak: '极弱',
    };
    expect(lens.dmStrengthZh).toBe(strengthMap[lens.dmStrength]);
  });
});

// Test with different DM element (Metal)
describe('calculateDmLens — Metal DM', () => {
  const metalInput: WuxingInput = {
    yearPillar:  { stem: 'Yi',   branch: 'Mao' },
    monthPillar: { stem: 'Gui',  branch: 'Wei' },
    dayPillar:   { stem: 'Geng', branch: 'Xu' },
    hourPillar:  { stem: 'Jia',  branch: 'Shen' },
    age: 35,
    gender: 'F',
    location: 'hometown',
  };

  const wuxingResult = calculateWuxing(metalInput);
  const lens = calculateDmLens(wuxingResult);

  it('maps elements correctly for Metal DM', () => {
    expect(lens.dmElement).toBe('Metal');
    expect(lens.rows[0].element).toBe('Metal');  // companion
    expect(lens.rows[1].element).toBe('Earth');  // resource = Earth→Metal
    expect(lens.rows[2].element).toBe('Water');  // output = Metal→Water
    expect(lens.rows[3].element).toBe('Wood');   // wealth = Metal→Wood
    expect(lens.rows[4].element).toBe('Fire');   // power = Fire→Metal
  });

  it('row percentages sum to approximately 100', () => {
    const total = lens.rows.reduce((s, r) => s + r.percent, 0);
    expect(total).toBeCloseTo(100, 0);
  });
});
