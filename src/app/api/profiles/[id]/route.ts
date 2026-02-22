import { NextRequest, NextResponse } from 'next/server';
import {
  getProfile,
  updateProfile,
  deleteProfile,
} from '@/lib/db';

interface RouteParams {
  params: Promise<{ id: string }>;
}

// GET /api/profiles/:id — get a single profile
export async function GET(_request: NextRequest, { params }: RouteParams) {
  const { id } = await params;
  const profile = await getProfile(id);

  if (!profile) {
    return NextResponse.json({ detail: 'Profile not found' }, { status: 404 });
  }

  return NextResponse.json(profile);
}

// PUT /api/profiles/:id — update a profile
export async function PUT(request: NextRequest, { params }: RouteParams) {
  const { id } = await params;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ detail: 'Invalid JSON body' }, { status: 422 });
  }

  const data = body as Record<string, unknown>;

  // Validate optional fields if provided
  if (data.name !== undefined && (typeof data.name !== 'string' || data.name.length === 0)) {
    return NextResponse.json({ detail: 'name must be a non-empty string' }, { status: 422 });
  }
  if (data.birth_date !== undefined && (typeof data.birth_date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(data.birth_date))) {
    return NextResponse.json({ detail: 'birth_date must be YYYY-MM-DD format' }, { status: 422 });
  }
  if (data.gender !== undefined && data.gender !== 'male' && data.gender !== 'female') {
    return NextResponse.json({ detail: 'gender must be "male" or "female"' }, { status: 422 });
  }
  if (data.birth_time !== undefined && data.birth_time !== null) {
    if (typeof data.birth_time !== 'string' || !/^\d{2}:\d{2}$/.test(data.birth_time)) {
      return NextResponse.json({ detail: 'birth_time must be HH:MM format' }, { status: 422 });
    }
  }

  const profile = await updateProfile(id, {
    name: data.name as string | undefined,
    birth_date: data.birth_date as string | undefined,
    birth_time: data.birth_time as string | undefined,
    gender: data.gender as 'male' | 'female' | undefined,
    place_of_birth: data.place_of_birth as string | undefined,
    phone: data.phone as string | undefined,
  });

  if (!profile) {
    return NextResponse.json({ detail: 'Profile not found' }, { status: 404 });
  }

  return NextResponse.json(profile);
}

// DELETE /api/profiles/:id — delete a profile
export async function DELETE(_request: NextRequest, { params }: RouteParams) {
  const { id } = await params;
  const success = await deleteProfile(id);

  if (!success) {
    return NextResponse.json({ detail: 'Profile not found' }, { status: 404 });
  }

  return new NextResponse(null, { status: 204 });
}
