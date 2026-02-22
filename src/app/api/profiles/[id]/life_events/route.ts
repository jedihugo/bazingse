import { NextRequest, NextResponse } from 'next/server';
import { addLifeEvent } from '@/lib/db';

interface RouteParams {
  params: Promise<{ id: string }>;
}

// POST /api/profiles/:id/life_events — add a life event
export async function POST(request: NextRequest, { params }: RouteParams) {
  const { id } = await params;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ detail: 'Invalid JSON body' }, { status: 422 });
  }

  const data = body as Record<string, unknown>;

  // Validate required fields
  if (data.year === undefined || typeof data.year !== 'number') {
    return NextResponse.json({ detail: 'year is required and must be a number' }, { status: 422 });
  }
  if (data.year < 1900 || data.year > 2100) {
    return NextResponse.json({ detail: 'year must be between 1900 and 2100' }, { status: 422 });
  }

  // Validate optional fields
  if (data.month !== undefined && data.month !== null) {
    if (typeof data.month !== 'number' || data.month < 1 || data.month > 12) {
      return NextResponse.json({ detail: 'month must be between 1 and 12' }, { status: 422 });
    }
  }
  if (data.day !== undefined && data.day !== null) {
    if (typeof data.day !== 'number' || data.day < 1 || data.day > 31) {
      return NextResponse.json({ detail: 'day must be between 1 and 31' }, { status: 422 });
    }
  }

  const event = await addLifeEvent(id, {
    year: data.year as number,
    month: (data.month as number | null | undefined) ?? undefined,
    day: (data.day as number | null | undefined) ?? undefined,
    location: (data.location as string | null | undefined) ?? undefined,
    notes: (data.notes as string | null | undefined) ?? undefined,
    is_abroad: (data.is_abroad as boolean | undefined) ?? undefined,
  });

  if (!event) {
    return NextResponse.json({ detail: 'Profile not found' }, { status: 404 });
  }

  return NextResponse.json(event, { status: 201 });
}
