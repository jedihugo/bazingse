import 'server-only';

import { put, list, del } from '@vercel/blob';
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
// Blob path helpers
// ---------------------------------------------------------------------------

const INDEX_PATH = 'profiles/_index.json';
const profilePath = (id: string) => `profiles/${id}.json`;

// ---------------------------------------------------------------------------
// Index entry — lightweight shape stored in the index blob
// ---------------------------------------------------------------------------

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

function toIndexEntry(p: Profile): ProfileIndexEntry {
  return {
    id: p.id,
    name: p.name,
    birth_date: p.birth_date,
    birth_time: p.birth_time,
    gender: p.gender as 'male' | 'female',
    place_of_birth: p.place_of_birth,
    phone: p.phone,
    created_at: p.created_at,
    updated_at: p.updated_at,
  };
}

// ---------------------------------------------------------------------------
// Blob I/O helpers
// ---------------------------------------------------------------------------

/** Find a blob's public URL by exact pathname. */
async function getBlobUrl(pathname: string): Promise<string | null> {
  const { blobs } = await list({ prefix: pathname, limit: 1 });
  if (blobs.length === 0 || blobs[0].pathname !== pathname) return null;
  return blobs[0].url;
}

/** Read and parse a JSON blob by pathname. */
async function readBlob<T>(pathname: string): Promise<T | null> {
  const url = await getBlobUrl(pathname);
  if (!url) return null;
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json() as Promise<T>;
}

/** Write a JSON blob (creates or overwrites). */
async function writeBlob(pathname: string, data: unknown): Promise<void> {
  await put(pathname, JSON.stringify(data), {
    access: 'public',
    addRandomSuffix: false,
    contentType: 'application/json',
  });
}

/** Delete a blob by pathname. */
async function deleteBlobByPath(pathname: string): Promise<void> {
  const url = await getBlobUrl(pathname);
  if (url) await del(url);
}

// ---------------------------------------------------------------------------
// Profile CRUD
// ---------------------------------------------------------------------------

/** List profiles (from lightweight index). */
export async function getProfiles(
  skip = 0,
  limit = 100,
): Promise<Profile[]> {
  const index = await readBlob<ProfileIndexEntry[]>(INDEX_PATH);
  if (!index) return [];

  const page = index.slice(skip, skip + limit);

  const profiles = await Promise.all(
    page.map(async (entry) => {
      const full = await readBlob<Profile>(profilePath(entry.id));
      return full ?? { ...entry, life_events: [] };
    }),
  );

  return profiles;
}

/** Get a single profile by ID (full, with life_events). */
export async function getProfile(id: string): Promise<Profile | null> {
  return readBlob<Profile>(profilePath(id));
}

/** Create a new profile. Returns the created profile. */
export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const now = new Date().toISOString();
  const profile: Profile = {
    id: randomUUID(),
    name: data.name,
    birth_date: data.birth_date,
    birth_time: data.birth_time ?? null,
    gender: data.gender,
    place_of_birth: data.place_of_birth ?? null,
    phone: data.phone ?? null,
    life_events: [],
    created_at: now,
    updated_at: now,
  };

  await writeBlob(profilePath(profile.id), profile);

  const index = (await readBlob<ProfileIndexEntry[]>(INDEX_PATH)) ?? [];
  index.push(toIndexEntry(profile));
  await writeBlob(INDEX_PATH, index);

  return profile;
}

/** Update an existing profile (partial update). Returns null if not found. */
export async function updateProfile(
  id: string,
  data: ProfileUpdate,
): Promise<Profile | null> {
  const profile = await readBlob<Profile>(profilePath(id));
  if (!profile) return null;

  const now = new Date().toISOString();

  if (data.name !== undefined) profile.name = data.name;
  if (data.birth_date !== undefined) profile.birth_date = data.birth_date;
  if (data.birth_time !== undefined) profile.birth_time = data.birth_time ?? null;
  if (data.gender !== undefined) profile.gender = data.gender;
  if (data.place_of_birth !== undefined) profile.place_of_birth = data.place_of_birth ?? null;
  if (data.phone !== undefined) profile.phone = data.phone ?? null;
  profile.updated_at = now;

  await writeBlob(profilePath(id), profile);

  const index = (await readBlob<ProfileIndexEntry[]>(INDEX_PATH)) ?? [];
  const idx = index.findIndex((e) => e.id === id);
  if (idx !== -1) {
    index[idx] = toIndexEntry(profile);
    await writeBlob(INDEX_PATH, index);
  }

  return profile;
}

/** Delete a profile. Returns true if deleted, false if not found. */
export async function deleteProfile(id: string): Promise<boolean> {
  const profile = await readBlob<Profile>(profilePath(id));
  if (!profile) return false;

  await deleteBlobByPath(profilePath(id));

  const index = (await readBlob<ProfileIndexEntry[]>(INDEX_PATH)) ?? [];
  const filtered = index.filter((e) => e.id !== id);
  await writeBlob(INDEX_PATH, filtered);

  return true;
}

// ---------------------------------------------------------------------------
// Life Event CRUD
// ---------------------------------------------------------------------------

/** Add a life event to a profile. */
export async function addLifeEvent(
  profileId: string,
  data: LifeEventCreate,
): Promise<LifeEvent | null> {
  const profile = await readBlob<Profile>(profilePath(profileId));
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

  if (!profile.life_events) profile.life_events = [];
  profile.life_events.push(event);
  profile.updated_at = now;

  await writeBlob(profilePath(profileId), profile);

  return event;
}

/** Update a life event. */
export async function updateLifeEvent(
  profileId: string,
  eventId: string,
  data: LifeEventUpdate,
): Promise<LifeEvent | null> {
  const profile = await readBlob<Profile>(profilePath(profileId));
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
  profile.updated_at = now;

  await writeBlob(profilePath(profileId), profile);

  return event;
}

/** Delete a life event. */
export async function deleteLifeEvent(
  profileId: string,
  eventId: string,
): Promise<boolean> {
  const profile = await readBlob<Profile>(profilePath(profileId));
  if (!profile || !profile.life_events) return false;

  const before = profile.life_events.length;
  profile.life_events = profile.life_events.filter((e) => e.id !== eventId);

  if (profile.life_events.length === before) return false;

  profile.updated_at = new Date().toISOString();
  await writeBlob(profilePath(profileId), profile);

  return true;
}

/** Get a single life event. */
export async function getLifeEvent(
  profileId: string,
  eventId: string,
): Promise<LifeEvent | null> {
  const profile = await readBlob<Profile>(profilePath(profileId));
  if (!profile || !profile.life_events) return null;

  return profile.life_events.find((e) => e.id === eventId) ?? null;
}
