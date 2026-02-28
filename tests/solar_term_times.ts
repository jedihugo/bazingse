/**
 * Check if lunar-typescript can compute exact solar term transition times.
 * Verify against known Li Chun times.
 */
import { Solar, Lunar } from 'lunar-typescript';

// Known Li Chun times (Beijing time, CST UTC+8) from authoritative sources:
// 2024: Feb 4, 16:27
// 2025: Feb 3, 22:10
// 2026: Feb 4, 04:02
// 2027: Feb 4, 09:46

console.log('=== Solar Term Exact Times — lunar-typescript vs Known ===\n');

const testDates = [
  { year: 2024, month: 2, day: 4, knownTime: "16:27" },
  { year: 2025, month: 2, day: 3, knownTime: "22:10" },
  { year: 2026, month: 2, day: 4, knownTime: "04:02" },
  { year: 2027, month: 2, day: 4, knownTime: "09:46" },
];

for (const td of testDates) {
  const solar = Solar.fromYmd(td.year, td.month, td.day);
  const lunar = solar.getLunar();
  const nextJie = lunar.getNextJie();
  if (nextJie) {
    const s = nextJie.getSolar();
    const computed = `${String(s.getHour()).padStart(2,'0')}:${String(s.getMinute()).padStart(2,'0')}`;
    const match = computed === td.knownTime ? '✅' : '⚠️';
    console.log(`${match} Li Chun ${td.year}: lunar-ts=${s.toYmdHms()}  known=${td.knownTime}  ${computed === td.knownTime ? 'EXACT MATCH' : 'OFF BY ~' + computed}`);
  }
}

console.log('\n=== Year Pillar Transition — Li Chun 2026 (known: Feb 4, 04:02 CST) ===\n');

const times = [
  { h: 3, m: 0, label: "03:00 — before Li Chun" },
  { h: 4, m: 0, label: "04:00 — 2 min before" },
  { h: 4, m: 1, label: "04:01 — 1 min before" },
  { h: 4, m: 2, label: "04:02 — exact Li Chun" },
  { h: 4, m: 3, label: "04:03 — 1 min after" },
  { h: 5, m: 0, label: "05:00 — well after" },
];

for (const t of times) {
  const solar = Solar.fromYmdHms(2026, 2, 4, t.h, t.m, 0);
  const lunar = solar.getLunar();
  const ec = lunar.getEightChar();
  console.log(`  ${t.label}  →  Year: ${ec.getYear()}  Month: ${ec.getMonth()}`);
}

console.log('\n=== Month Pillar Transition — Jingzhe 2024 (Awakening of Insects, ~Mar 5) ===\n');

// Check month pillar changes at exact Jie time
const mar5 = Solar.fromYmd(2024, 3, 5);
const mar5Jie = mar5.getLunar().getNextJie();
if (mar5Jie) {
  console.log(`Jingzhe 2024: ${mar5Jie.getSolar().toYmdHms()}`);
}
const monthTimes = [
  { y: 2024, mo: 3, d: 5, h: 8, mi: 0, label: "Mar 5 08:00" },
  { y: 2024, mo: 3, d: 5, h: 11, mi: 0, label: "Mar 5 11:00" },
  { y: 2024, mo: 3, d: 5, h: 12, mi: 0, label: "Mar 5 12:00" },
  { y: 2024, mo: 3, d: 6, h: 8, mi: 0, label: "Mar 6 08:00" },
];
for (const t of monthTimes) {
  const solar = Solar.fromYmdHms(t.y, t.mo, t.d, t.h, t.mi, 0);
  const ec = solar.getLunar().getEightChar();
  console.log(`  ${t.label}  →  Month: ${ec.getMonth()}  Year: ${ec.getYear()}`);
}
