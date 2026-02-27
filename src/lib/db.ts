import 'server-only';

import type {
  Profile,
  LifeEvent,
  ProfileCreate,
  ProfileUpdate,
  LifeEventCreate,
  LifeEventUpdate,
} from './api.types';

// ---------------------------------------------------------------------------
// Railway API base URL
// ---------------------------------------------------------------------------

const RAILWAY_URL = process.env.RAILWAY_API_URL
  ?? 'https://bazingse-production.up.railway.app';

async function railwayFetch(path: string, init?: RequestInit): Promise<Response> {
  return fetch(`${RAILWAY_URL}${path}`, {
    ...init,
    cache: 'no-store',
  });
}

// ---------------------------------------------------------------------------
// Profile CRUD
// ---------------------------------------------------------------------------

export async function getProfiles(
  skip = 0,
  limit = 100,
): Promise<Profile[]> {
  const res = await railwayFetch(`/api/profiles?skip=${skip}&limit=${limit}`);
  if (!res.ok) return [];
  return res.json();
}

export async function getProfile(id: string): Promise<Profile | null> {
  const res = await railwayFetch(`/api/profiles/${id}`);
  if (!res.ok) return null;
  return res.json();
}

export async function createProfile(data: ProfileCreate): Promise<Profile> {
  const res = await railwayFetch('/api/profiles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function updateProfile(
  id: string,
  data: ProfileUpdate,
): Promise<Profile | null> {
  const res = await railwayFetch(`/api/profiles/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function deleteProfile(id: string): Promise<boolean> {
  const res = await railwayFetch(`/api/profiles/${id}`, { method: 'DELETE' });
  return res.ok;
}

// ---------------------------------------------------------------------------
// Life Event CRUD
// ---------------------------------------------------------------------------

export async function addLifeEvent(
  profileId: string,
  data: LifeEventCreate,
): Promise<LifeEvent | null> {
  const res = await railwayFetch(`/api/profiles/${profileId}/life_events`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function updateLifeEvent(
  profileId: string,
  eventId: string,
  data: LifeEventUpdate,
): Promise<LifeEvent | null> {
  const res = await railwayFetch(`/api/profiles/${profileId}/life_events/${eventId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function deleteLifeEvent(
  profileId: string,
  eventId: string,
): Promise<boolean> {
  const res = await railwayFetch(`/api/profiles/${profileId}/life_events/${eventId}`, {
    method: 'DELETE',
  });
  return res.ok;
}

export async function getLifeEvent(
  profileId: string,
  eventId: string,
): Promise<LifeEvent | null> {
  const res = await railwayFetch(`/api/profiles/${profileId}/life_events/${eventId}`);
  if (!res.ok) return null;
  return res.json();
}
