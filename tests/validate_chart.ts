/**
 * Validate chart.ts against golden files from the Python API.
 *
 * Compares four natal pillars from generateBaziChart() against the
 * golden JSON files that were captured from the production sxtwl-based
 * Python backend.
 *
 * Run: npx tsx tests/validate_chart.ts
 */

import * as fs from 'fs';
import * as path from 'path';
import { generateBaziChart, generateLuckPillars } from '../src/lib/bazi/chart';

// ---------------------------------------------------------------------------
// Golden file definitions
// ---------------------------------------------------------------------------

interface GoldenCase {
  file: string;
  description: string;
  /** Known discrepancy that we accept (e.g. sxtwl year bug on Li Chun day) */
  knownDiffs?: Record<string, string>;
}

const GOLDEN_CASES: GoldenCase[] = [
  {
    file: 'natal_basic.json',
    description: '1990-01-15 10:30 male — normal date',
  },
  {
    file: 'natal_lichun_before.json',
    description: '2024-02-04 03:00 male — before Li Chun (sxtwl has year bug)',
    knownDiffs: {
      // sxtwl returns Jia Chen (new year) for the entire day of Li Chun,
      // even though 03:00 is before the transition at ~16:27.
      // lunar-typescript correctly returns Gui Mao (old year).
      year: 'sxtwl=Jia Chen, lunar-ts=Gui Mao (lunar-ts is correct)',
    },
  },
  {
    file: 'natal_lichun_after.json',
    description: '2024-02-04 17:00 female — after Li Chun',
  },
  {
    file: 'natal_23h.json',
    description: '1995-08-10 23:30 male — day changes at 23:00',
  },
  {
    file: 'natal_unknown_time.json',
    description: '1985-12-25 unknown female — no birth time',
  },
];

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function loadGolden(filename: string): Record<string, any> {
  const filePath = path.join(__dirname, 'golden', filename);
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

function extractExpectedPillars(data: Record<string, any>): Record<string, string | undefined> {
  const result: Record<string, string | undefined> = {
    year: `${data.hs_y.id} ${data.eb_y.id}`,
    month: `${data.hs_m.id} ${data.eb_m.id}`,
    day: `${data.hs_d.id} ${data.eb_d.id}`,
  };
  // Hour pillar may not be meaningful when time is unknown
  if (data.hs_h && data.eb_h) {
    result.hour = `${data.hs_h.id} ${data.eb_h.id}`;
  }
  return result;
}

function parseBirthInfo(data: Record<string, any>): {
  year: number;
  month: number;
  day: number;
  hour: number | null;
  minute: number | null;
  gender: 'male' | 'female';
} {
  const bi = data.birth_info;
  const [y, m, d] = bi.date.split('-').map(Number);

  let hour: number | null = null;
  let minute: number | null = null;
  if (bi.time && bi.time !== 'unknown') {
    const [h, min] = bi.time.split(':').map(Number);
    hour = h;
    minute = min;
  }

  return { year: y, month: m, day: d, hour, minute, gender: bi.gender };
}

// ---------------------------------------------------------------------------
// Main validation
// ---------------------------------------------------------------------------

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;
let knownDiffTests = 0;

console.log('=== Chart.ts Validation Against Golden Files ===\n');

for (const gc of GOLDEN_CASES) {
  const data = loadGolden(gc.file);
  const expected = extractExpectedPillars(data);
  const bi = parseBirthInfo(data);

  const chart = generateBaziChart(bi.year, bi.month, bi.day, bi.hour, bi.minute);

  const actual: Record<string, string | undefined> = {
    year: chart.year_pillar,
    month: chart.month_pillar,
    day: chart.day_pillar,
    hour: chart.hour_pillar,
  };

  console.log(`--- ${gc.file} ---`);
  console.log(`    ${gc.description}`);

  const pillarNames = ['year', 'month', 'day', 'hour'] as const;
  let casePass = true;

  for (const p of pillarNames) {
    totalTests++;
    const exp = expected[p];
    const act = actual[p];

    // Skip hour comparison when time is unknown
    // (golden file may have dummy hour data from the API)
    if (p === 'hour' && bi.hour === null) {
      if (act === undefined) {
        console.log(`    ${p}: SKIP (no birth time — correctly omitted)`);
        passedTests++;
      } else {
        console.log(`    ${p}: SKIP (no birth time — returned "${act}", ignoring)`);
        passedTests++;
      }
      continue;
    }

    if (act === exp) {
      console.log(`    ${p}: MATCH "${act}"`);
      passedTests++;
    } else if (gc.knownDiffs && gc.knownDiffs[p]) {
      console.log(`    ${p}: KNOWN DIFF — expected="${exp}", got="${act}"`);
      console.log(`           ${gc.knownDiffs[p]}`);
      knownDiffTests++;
      passedTests++; // Count as pass since lunar-ts is actually correct
    } else {
      console.log(`    ${p}: MISMATCH — expected="${exp}", got="${act}"`);
      casePass = false;
      failedTests++;
    }
  }

  if (!casePass) {
    console.log(`    RESULT: FAIL`);
  }
  console.log('');
}

// ---------------------------------------------------------------------------
// Luck pillar validation (natal_basic has da_yun_start_age = 4 in with_luck)
// ---------------------------------------------------------------------------

console.log('--- Luck Pillar Validation ---');
console.log('    natal_basic: 1990-01-15, Ji Si year, Ding Chou month, male');

const luckPillars = generateLuckPillars(
  'Ji Si',    // year pillar
  'Ding Chou', // month pillar
  'male',
  { year: 1990, month: 1, day: 15 },
);

// Expected from Python: start_age=4, backward direction
// Pillars: Bing Zi, Yi Hai, Jia Xu, Gui You, Ren Shen, Xin Wei, Geng Wu, Ji Si
const expectedLuck = [
  { pillar: 'Bing Zi', start_age: 4 },
  { pillar: 'Yi Hai', start_age: 14 },
  { pillar: 'Jia Xu', start_age: 24 },
  { pillar: 'Gui You', start_age: 34 },
  { pillar: 'Ren Shen', start_age: 44 },
  { pillar: 'Xin Wei', start_age: 54 },
  { pillar: 'Geng Wu', start_age: 64 },
  { pillar: 'Ji Si', start_age: 74 },
];

for (let i = 0; i < expectedLuck.length; i++) {
  totalTests++;
  const exp = expectedLuck[i];
  const act = luckPillars[i];
  if (act.pillar === exp.pillar && act.start_age === exp.start_age) {
    console.log(`    LP${i + 1}: MATCH "${act.pillar}" age=${act.start_age}`);
    passedTests++;
  } else {
    console.log(`    LP${i + 1}: MISMATCH — expected="${exp.pillar}" age=${exp.start_age}, got="${act.pillar}" age=${act.start_age}`);
    failedTests++;
  }
}

console.log('');

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log('=== Summary ===');
console.log(`Total: ${totalTests}  Passed: ${passedTests}  Failed: ${failedTests}  Known diffs: ${knownDiffTests}`);

if (failedTests > 0) {
  console.log('\nFAILED — see mismatches above');
  process.exit(1);
} else {
  console.log('\nALL PASSED');
  process.exit(0);
}
