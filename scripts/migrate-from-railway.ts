/**
 * Migration script: Fetch all profiles from Railway API and write to local SQLite.
 *
 * Usage:
 *   DATABASE_PATH=./bazingse.db npx tsx scripts/migrate-from-railway.ts
 *
 * Environment variables:
 *   RAILWAY_API_URL — Railway backend URL (default: https://bazingse-production.up.railway.app)
 *   DATABASE_PATH   — SQLite file path (default: ./bazingse.db)
 */

import Database from 'better-sqlite3';

interface LifeEvent {
  id: string;
  year: number;
  month?: number | null;
  day?: number | null;
  location?: string | null;
  notes?: string | null;
  is_abroad?: boolean;
  created_at: string;
  updated_at: string;
}

interface Profile {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string | null;
  gender: 'male' | 'female';
  place_of_birth: string | null;
  phone: string | null;
  life_events: LifeEvent[] | null;
  created_at: string | null;
  updated_at: string | null;
}

const RAILWAY_API_URL =
  process.env.RAILWAY_API_URL ?? 'https://bazingse-production.up.railway.app';
const DB_PATH = process.env.DATABASE_PATH ?? './bazingse.db';

async function main() {
  console.log(`Fetching profiles from Railway: ${RAILWAY_API_URL}/api/profiles?limit=10000`);

  const res = await fetch(`${RAILWAY_API_URL}/api/profiles?limit=10000`);
  if (!res.ok) {
    throw new Error(`Railway API error: ${res.status} ${await res.text()}`);
  }

  const profiles: Profile[] = await res.json();
  console.log(`Fetched ${profiles.length} profiles from Railway.`);

  const db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS profiles (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      birth_date TEXT NOT NULL,
      birth_time TEXT,
      gender TEXT NOT NULL,
      place_of_birth TEXT,
      phone TEXT,
      life_events TEXT DEFAULT '[]',
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    )
  `);

  const insert = db.prepare(`
    INSERT OR REPLACE INTO profiles (id, name, birth_date, birth_time, gender, place_of_birth, phone, life_events, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const insertMany = db.transaction((items: Profile[]) => {
    for (const p of items) {
      insert.run(
        p.id, p.name, p.birth_date, p.birth_time, p.gender,
        p.place_of_birth, p.phone,
        JSON.stringify(p.life_events ?? []),
        p.created_at, p.updated_at,
      );
    }
  });

  insertMany(profiles);

  console.log(`Written ${profiles.length} profiles to ${DB_PATH}`);
  console.log('Migration complete!');

  db.close();
}

main().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
