import 'server-only';

import Database from 'better-sqlite3';
import { randomUUID } from 'crypto';
import type {
  Profile,
  LifeEvent,
  ProfileCreate,
  ProfileUpdate,
  LifeEventCreate,
  LifeEventUpdate,
} from './api';

// ---------------------------------------------------------------------------
// Database connection (singleton)
// ---------------------------------------------------------------------------

const DB_PATH = process.env.DATABASE_PATH ?? '/data/bazingse.db';

let _db: Database.Database | null = null;

function getDb(): Database.Database {
  if (!_db) {
    _db = new Database(DB_PATH);
    _db.pragma('journal_mode = WAL');
    _db.pragma('foreign_keys = ON');
    ensureSchema(_db);
  }
  return _db;
}

function ensureSchema(db: Database.Database): void {
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
}

// ---------------------------------------------------------------------------
// Row → Profile helper
// ---------------------------------------------------------------------------

interface ProfileRow {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string | null;
  gender: string;
  place_of_birth: string | null;
  phone: string | null;
  life_events: string | null;
  created_at: string | null;
  updated_at: string | null;
}

function rowToProfile(row: ProfileRow): Profile {
  let events: LifeEvent[] = [];
  if (row.life_events) {
    try { events = JSON.parse(row.life_events); } catch { /* empty */ }
  }
  return {
    id: row.id,
    name: row.name,
    birth_date: row.birth_date,
    birth_time: row.birth_time,
    gender: row.gender as 'male' | 'female',
    place_of_birth: row.place_of_birth,
    phone: row.phone,
    life_events: events,
    created_at: row.created_at,
    updated_at: row.updated_at,
  };
}

// ---------------------------------------------------------------------------
// Profile CRUD
// ---------------------------------------------------------------------------

export async function getProfiles(
  skip = 0,
  limit = 100,
): Promise<Profile[]> {
  const db = getDb();
  const rows = db.prepare(
    'SELECT * FROM profiles ORDER BY name ASC LIMIT ? OFFSET ?'
  ).all(limit, skip) as ProfileRow[];
  return rows.map(rowToProfile);
}

export async function getProfile(id: string): Promise<Profile | null> {
  const db = getDb();
  const row = db.prepare('SELECT * FROM profiles WHERE id = ?').get(id) as ProfileRow | undefined;
  return row ? rowToProfile(row) : null;
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const db = getDb();
  const now = new Date().toISOString();
  const id = randomUUID();

  db.prepare(`
    INSERT INTO profiles (id, name, birth_date, birth_time, gender, place_of_birth, phone, life_events, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, '[]', ?, ?)
  `).run(
    id, data.name, data.birth_date, data.birth_time ?? null,
    data.gender, data.place_of_birth ?? null, data.phone ?? null,
    now, now,
  );

  return (await getProfile(id))!;
}

export async function updateProfile(
  id: string,
  data: ProfileUpdate,
): Promise<Profile | null> {
  const db = getDb();
  const existing = db.prepare('SELECT * FROM profiles WHERE id = ?').get(id) as ProfileRow | undefined;
  if (!existing) return null;

  const now = new Date().toISOString();

  db.prepare(`
    UPDATE profiles SET
      name = ?, birth_date = ?, birth_time = ?, gender = ?,
      place_of_birth = ?, phone = ?, updated_at = ?
    WHERE id = ?
  `).run(
    data.name !== undefined ? data.name : existing.name,
    data.birth_date !== undefined ? data.birth_date : existing.birth_date,
    data.birth_time !== undefined ? (data.birth_time ?? null) : existing.birth_time,
    data.gender !== undefined ? data.gender : existing.gender,
    data.place_of_birth !== undefined ? (data.place_of_birth ?? null) : existing.place_of_birth,
    data.phone !== undefined ? (data.phone ?? null) : existing.phone,
    now, id,
  );

  return getProfile(id);
}

export async function deleteProfile(id: string): Promise<boolean> {
  const db = getDb();
  const result = db.prepare('DELETE FROM profiles WHERE id = ?').run(id);
  return result.changes > 0;
}

// ---------------------------------------------------------------------------
// Life Event CRUD (stored as JSON array in profiles.life_events)
// ---------------------------------------------------------------------------

export async function addLifeEvent(
  profileId: string,
  data: LifeEventCreate,
): Promise<LifeEvent | null> {
  const db = getDb();
  const profile = await getProfile(profileId);
  if (!profile) return null;

  const now = new Date().toISOString();
  const event: LifeEvent = {
    id: randomUUID(),
    year: data.year,
    month: data.month ?? null,
    day: data.day ?? null,
    location: data.location ?? null,
    notes: data.notes ?? null,
    is_abroad: data.is_abroad ?? false,
    created_at: now,
    updated_at: now,
  };

  const events = profile.life_events ?? [];
  events.push(event);

  db.prepare('UPDATE profiles SET life_events = ?, updated_at = ? WHERE id = ?')
    .run(JSON.stringify(events), now, profileId);

  return event;
}

export async function updateLifeEvent(
  profileId: string,
  eventId: string,
  data: LifeEventUpdate,
): Promise<LifeEvent | null> {
  const db = getDb();
  const profile = await getProfile(profileId);
  if (!profile || !profile.life_events) return null;

  const idx = profile.life_events.findIndex((e) => e.id === eventId);
  if (idx === -1) return null;

  const event = profile.life_events[idx];
  const now = new Date().toISOString();

  if (data.year !== undefined) event.year = data.year;
  if (data.month !== undefined) event.month = data.month ?? null;
  if (data.day !== undefined) event.day = data.day ?? null;
  if (data.location !== undefined) event.location = data.location ?? null;
  if (data.notes !== undefined) event.notes = data.notes ?? null;
  if (data.is_abroad !== undefined) event.is_abroad = data.is_abroad ?? false;
  event.updated_at = now;

  profile.life_events[idx] = event;

  db.prepare('UPDATE profiles SET life_events = ?, updated_at = ? WHERE id = ?')
    .run(JSON.stringify(profile.life_events), now, profileId);

  return event;
}

export async function deleteLifeEvent(
  profileId: string,
  eventId: string,
): Promise<boolean> {
  const db = getDb();
  const profile = await getProfile(profileId);
  if (!profile || !profile.life_events) return false;

  const before = profile.life_events.length;
  const filtered = profile.life_events.filter((e) => e.id !== eventId);
  if (filtered.length === before) return false;

  const now = new Date().toISOString();
  db.prepare('UPDATE profiles SET life_events = ?, updated_at = ? WHERE id = ?')
    .run(JSON.stringify(filtered), now, profileId);

  return true;
}

export async function getLifeEvent(
  profileId: string,
  eventId: string,
): Promise<LifeEvent | null> {
  const profile = await getProfile(profileId);
  if (!profile || !profile.life_events) return null;
  return profile.life_events.find((e) => e.id === eventId) ?? null;
}
