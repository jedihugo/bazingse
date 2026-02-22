import { NextRequest, NextResponse } from 'next/server';
import { getProfiles, createProfile } from '@/lib/db';

// GET /api/profiles — list all profiles
export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  const skip = parseInt(searchParams.get('skip') ?? '0', 10);
  const limit = parseInt(searchParams.get('limit') ?? '100', 10);

  const profiles = await getProfiles(skip, limit);
  return NextResponse.json(profiles);
}

// POST /api/profiles — create a new profile
export async function POST(request: NextRequest) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ detail: 'Invalid JSON body' }, { status: 422 });
  }

  const data = body as Record<string, unknown>;

  // Validate required fields
  if (!data.name || typeof data.name !== 'string' || data.name.length === 0) {
    return NextResponse.json({ detail: 'name is required' }, { status: 422 });
  }
  if (!data.birth_date || typeof data.birth_date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(data.birth_date)) {
    return NextResponse.json({ detail: 'birth_date is required (YYYY-MM-DD)' }, { status: 422 });
  }
  if (!data.gender || (data.gender !== 'male' && data.gender !== 'female')) {
    return NextResponse.json({ detail: 'gender must be "male" or "female"' }, { status: 422 });
  }

  // Validate optional birth_time format
  if (data.birth_time !== undefined && data.birth_time !== null) {
    if (typeof data.birth_time !== 'string' || !/^\d{2}:\d{2}$/.test(data.birth_time)) {
      return NextResponse.json({ detail: 'birth_time must be HH:MM format' }, { status: 422 });
    }
  }

  const profile = await createProfile({
    name: data.name as string,
    birth_date: data.birth_date as string,
    birth_time: (data.birth_time as string) ?? undefined,
    gender: data.gender as 'male' | 'female',
    place_of_birth: (data.place_of_birth as string) ?? undefined,
    phone: (data.phone as string) ?? undefined,
  });

  return NextResponse.json(profile, { status: 201 });
}
