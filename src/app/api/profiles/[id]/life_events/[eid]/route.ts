import { NextRequest, NextResponse } from 'next/server';
import {
  getLifeEvent,
  updateLifeEvent,
  deleteLifeEvent,
} from '@/lib/db';

interface RouteParams {
  params: Promise<{ id: string; eid: string }>;
}

// GET /api/profiles/:id/life_events/:eid — get a single life event
export async function GET(_request: NextRequest, { params }: RouteParams) {
  const { id, eid } = await params;
  const event = await getLifeEvent(id, eid);

  if (!event) {
    return NextResponse.json({ detail: 'Life event not found' }, { status: 404 });
  }

  return NextResponse.json(event);
}

// PUT /api/profiles/:id/life_events/:eid — update a life event
export async function PUT(request: NextRequest, { params }: RouteParams) {
  const { id, eid } = await params;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ detail: 'Invalid JSON body' }, { status: 422 });
  }

  const data = body as Record<string, unknown>;

  // Validate optional fields
  if (data.year !== undefined && data.year !== null) {
    if (typeof data.year !== 'number' || data.year < 1900 || data.year > 2100) {
      return NextResponse.json({ detail: 'year must be between 1900 and 2100' }, { status: 422 });
    }
  }
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

  const event = await updateLifeEvent(id, eid, {
    year: data.year as number | undefined,
    month: data.month as number | null | undefined,
    day: data.day as number | null | undefined,
    location: data.location as string | null | undefined,
    notes: data.notes as string | null | undefined,
    is_abroad: data.is_abroad as boolean | undefined,
  });

  if (!event) {
    return NextResponse.json({ detail: 'Life event not found' }, { status: 404 });
  }

  return NextResponse.json(event);
}

// DELETE /api/profiles/:id/life_events/:eid — delete a life event
export async function DELETE(_request: NextRequest, { params }: RouteParams) {
  const { id, eid } = await params;
  const success = await deleteLifeEvent(id, eid);

  if (!success) {
    return NextResponse.json({ detail: 'Life event not found' }, { status: 404 });
  }

  return new NextResponse(null, { status: 204 });
}
