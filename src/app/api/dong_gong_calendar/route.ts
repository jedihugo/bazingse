import { NextRequest, NextResponse } from 'next/server';
import { getDongGongCalendar } from '@/server/services/dong-gong';

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;

  const yearStr = params.get("year");
  const monthStr = params.get("month");

  if (!yearStr || !monthStr) {
    return NextResponse.json(
      { error: "year and month are required" },
      { status: 400 },
    );
  }

  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);

  if (month < 1 || month > 12) {
    return NextResponse.json(
      { error: "month must be between 1 and 12" },
      { status: 400 },
    );
  }

  try {
    const result = getDongGongCalendar({ year, month });
    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Calendar generation failed" },
      { status: 500 },
    );
  }
}
