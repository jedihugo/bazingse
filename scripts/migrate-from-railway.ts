/**
 * Migration script: Fetch all profiles from Railway API and write to Vercel KV.
 *
 * Usage:
 *   KV_REST_API_URL=... KV_REST_API_TOKEN=... npx tsx scripts/migrate-from-railway.ts
 *
 * Environment variables:
 *   RAILWAY_API_URL  — Railway backend URL (default: https://bazingse-production.up.railway.app)
 *   KV_REST_API_URL  — Vercel KV REST URL (required)
 *   KV_REST_API_TOKEN — Vercel KV REST token (required)
 */

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
const KV_REST_API_URL = process.env.KV_REST_API_URL;
const KV_REST_API_TOKEN = process.env.KV_REST_API_TOKEN;

if (!KV_REST_API_URL || !KV_REST_API_TOKEN) {
  console.error('Missing required env: KV_REST_API_URL and KV_REST_API_TOKEN');
  process.exit(1);
}

// ---------------------------------------------------------------------------
// KV helpers (direct REST calls — no @vercel/kv import outside Next.js)
// ---------------------------------------------------------------------------

async function kvSet(key: string, value: unknown): Promise<void> {
  const res = await fetch(`${KV_REST_API_URL}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${KV_REST_API_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(['SET', key, JSON.stringify(value)]),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`KV SET failed for ${key}: ${res.status} ${text}`);
  }
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

  // Build index
  const index: ProfileIndexEntry[] = [];

  for (const profile of profiles) {
    // Ensure life_events is an array
    if (!profile.life_events) {
      profile.life_events = [];
    }

    // Write full profile to KV
    const key = `profile:${profile.id}`;
    await kvSet(key, profile);
    console.log(`  Written: ${key} (${profile.name})`);

    // Add to index
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

  // Write index
  await kvSet('profiles:index', index);
  console.log(`\nWritten profiles:index with ${index.length} entries.`);
  console.log('Migration complete!');
}

main().catch((err) => {
  console.error('Migration failed:', err);
  process.exit(1);
});
