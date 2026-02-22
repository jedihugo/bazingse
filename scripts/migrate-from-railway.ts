/**
 * Migration script: Fetch all profiles from Railway API and write to Vercel Blob.
 *
 * Usage:
 *   BLOB_READ_WRITE_TOKEN=... npx tsx scripts/migrate-from-railway.ts
 *
 * Environment variables:
 *   RAILWAY_API_URL       — Railway backend URL (default: https://bazingse-production.up.railway.app)
 *   BLOB_READ_WRITE_TOKEN — Vercel Blob read/write token (required)
 */

import { put } from '@vercel/blob';

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

interface ProfileIndexEntry {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string | null;
  gender: 'male' | 'female';
  place_of_birth: string | null;
  phone: string | null;
  created_at: string | null;
  updated_at: string | null;
}

const RAILWAY_API_URL =
  process.env.RAILWAY_API_URL ?? 'https://bazingse-production.up.railway.app';
const BLOB_TOKEN = process.env.BLOB_READ_WRITE_TOKEN;

if (!BLOB_TOKEN) {
  console.error('Missing required env: BLOB_READ_WRITE_TOKEN');
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Blob helper
// ---------------------------------------------------------------------------

async function writeBlob(pathname: string, data: unknown): Promise<void> {
  await put(pathname, JSON.stringify(data), {
    access: 'public',
    addRandomSuffix: false,
    contentType: 'application/json',
    token: BLOB_TOKEN,
  });
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`Fetching profiles from Railway: ${RAILWAY_API_URL}/api/profiles?limit=10000`);

  const res = await fetch(`${RAILWAY_API_URL}/api/profiles?limit=10000`);
  if (!res.ok) {
    throw new Error(`Railway API error: ${res.status} ${await res.text()}`);
  }

  const profiles: Profile[] = await res.json();
  console.log(`Fetched ${profiles.length} profiles from Railway.`);

  const index: ProfileIndexEntry[] = [];

  for (const profile of profiles) {
    if (!profile.life_events) {
      profile.life_events = [];
    }

    const path = `profiles/${profile.id}.json`;
    await writeBlob(path, profile);
    console.log(`  Written: ${path} (${profile.name})`);

    index.push({
      id: profile.id,
      name: profile.name,
      birth_date: profile.birth_date,
      birth_time: profile.birth_time,
      gender: profile.gender as 'male' | 'female',
      place_of_birth: profile.place_of_birth,
      phone: profile.phone,
      created_at: profile.created_at,
      updated_at: profile.updated_at,
    });
  }

  await writeBlob('profiles/_index.json', index);
  console.log(`\nWritten profiles/_index.json with ${index.length} entries.`);
  console.log('Migration complete!');
}

main().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
