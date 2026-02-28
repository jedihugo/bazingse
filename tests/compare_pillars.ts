/**
 * Compare pillar results from sxtwl (Python) and lunar-typescript.
 * Reads both JSON files and shows matches/mismatches.
 */
import * as fs from 'fs';

interface PillarResult {
  date: string;
  time: string | null;
  desc: string;
  pillars?: {
    year: string;
    month: string;
    day: string;
    hour?: string;
  };
  error?: string;
}

const sxtwlData: PillarResult[] = JSON.parse(fs.readFileSync('/tmp/sxtwl_results.json', 'utf-8'));
const lunarTsData: PillarResult[] = JSON.parse(fs.readFileSync('/tmp/lunar_ts_results.json', 'utf-8'));

let matches = 0;
let mismatches = 0;
let errors = 0;

console.log('='.repeat(90));
console.log('PILLAR COMPARISON: sxtwl (Python) vs lunar-typescript');
console.log('='.repeat(90));
console.log('');

for (let i = 0; i < sxtwlData.length; i++) {
  const sx = sxtwlData[i];
  const lt = lunarTsData[i];

  if (lt.error) {
    errors++;
    console.log(`❌ ERROR  ${sx.date} ${sx.time ?? 'no-time'} | ${sx.desc}`);
    console.log(`   lunar-typescript error: ${lt.error}`);
    console.log('');
    continue;
  }

  if (!sx.pillars || !lt.pillars) continue;

  const pillarKeys = ['year', 'month', 'day', 'hour'] as const;
  const diffs: string[] = [];

  for (const key of pillarKeys) {
    const sxVal = sx.pillars[key];
    const ltVal = lt.pillars[key];
    if (sxVal === undefined && ltVal === undefined) continue;
    if (sxVal !== ltVal) {
      diffs.push(`${key}: sxtwl="${sxVal}" vs lunar-ts="${ltVal}"`);
    }
  }

  if (diffs.length === 0) {
    matches++;
    console.log(`✅ MATCH  ${sx.date} ${sx.time ?? 'no-time'} | ${sx.desc}`);
    console.log(`   Y: ${sx.pillars.year}  M: ${sx.pillars.month}  D: ${sx.pillars.day}${sx.pillars.hour ? '  H: ' + sx.pillars.hour : ''}`);
  } else {
    mismatches++;
    console.log(`⚠️  DIFF   ${sx.date} ${sx.time ?? 'no-time'} | ${sx.desc}`);
    for (const d of diffs) {
      console.log(`   ${d}`);
    }
  }
  console.log('');
}

console.log('='.repeat(90));
console.log(`SUMMARY: ${matches} matches, ${mismatches} mismatches, ${errors} errors out of ${sxtwlData.length} test cases`);
console.log('='.repeat(90));

if (mismatches === 0 && errors === 0) {
  console.log('\n🎉 PERFECT MATCH — lunar-typescript produces identical results to sxtwl!');
} else if (mismatches <= 2) {
  console.log('\n⚠️  CLOSE — only minor differences, likely edge case handling. Review diffs above.');
} else {
  console.log('\n❌ SIGNIFICANT DIFFERENCES — would need investigation before migration.');
}
