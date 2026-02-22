import { NextResponse } from 'next/server';
import { getProfiles, createProfile } from '@/lib/db';

const TEST_PRESETS = [
  { date: '1969-07-04', time: '18:20', gender: 'female' as const, name: 'Test 1969-07-04' },
  { date: '1992-07-06', time: '09:30', gender: 'female' as const, name: 'Test 1992-07-06' },
  { date: '1995-04-19', time: '17:30', gender: 'male' as const, name: 'Test 1995-04-19' },
  { date: '1985-06-23', time: '13:30', gender: 'male' as const, name: 'Test 1985-06-23' },
  { date: '1988-02-02', time: '13:30', gender: 'male' as const, name: 'Test 1988-02-02' },
  { date: '1986-11-29', time: '13:30', gender: 'male' as const, name: 'Test 1986-11-29' },
  { date: '1995-08-14', time: '11:30', gender: 'female' as const, name: 'Test 1995-08-14' },
  { date: '1995-07-18', time: '16:30', gender: 'female' as const, name: 'Test 1995-07-18' },
  { date: '1992-09-18', time: '09:30', gender: 'female' as const, name: 'Test 1992-09-18' },
  { date: '2002-04-17', time: '08:20', gender: 'female' as const, name: 'Test 2002-04-17' },
  { date: '2019-09-18', time: '05:00', gender: 'female' as const, name: 'Test 2019-09-18' },
  { date: '2021-08-09', time: '21:00', gender: 'female' as const, name: 'Test 2021-08-09' },
  { date: '1985-03-20', time: '23:00', gender: 'female' as const, name: 'Test 1985-03-20' },
  { date: '1995-02-10', time: '10:10', gender: 'female' as const, name: 'Test 1995-02-10' },
  { date: '1946-08-12', time: '07:00', gender: 'male' as const, name: 'Suharsa' },
  { date: '1962-11-03', time: '11:45', gender: 'male' as const, name: 'Malaysian - Mata Ikan' },
  { date: '1954-02-09', time: '09:30', gender: 'female' as const, name: 'Test 1954-02-09' },
  { date: '1949-12-19', time: '08:00', gender: 'male' as const, name: 'Test 1949-12-19' },
  { date: '1955-10-18', time: '20:00', gender: 'female' as const, name: 'Test 1955-10-18' },
  { date: '1992-12-25', time: undefined, gender: 'female' as const, name: 'Test 1992-12-25 (Unknown Hour)' },
  { date: '1945-03-26', time: '18:00', gender: 'male' as const, name: 'Batubara (hutan, tanah, pulau)' },
  { date: '1969-04-07', time: '18:30', gender: 'female' as const, name: 'Wu Chen Wealth Storage' },
];

// POST /api/seed — seed KV with test profiles (only if empty)
export async function POST() {
  const existing = await getProfiles(0, 1);

  if (existing.length > 0) {
    return NextResponse.json(
      { message: `Database already has profiles. Skipping seed.` },
      { status: 200 },
    );
  }

  for (const preset of TEST_PRESETS) {
    await createProfile({
      name: preset.name,
      birth_date: preset.date,
      birth_time: preset.time,
      gender: preset.gender,
    });
  }

  return NextResponse.json(
    { message: `Successfully seeded ${TEST_PRESETS.length} profiles.` },
    { status: 201 },
  );
}
