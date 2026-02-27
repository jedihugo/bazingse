import { NextRequest, NextResponse } from 'next/server';
import { analyzeBazi } from '@/server/services/bazi';

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;

  const birthDateStr = params.get("birth_date");
  const gender = params.get("gender") as "male" | "female" | null;

  if (!birthDateStr || !gender) {
    return NextResponse.json(
      { error: "birth_date and gender are required" },
      { status: 400 },
    );
  }

  try {
    const result = analyzeBazi({
      birth_date: birthDateStr,
      birth_time: params.get("birth_time") || null,
      gender,
      analysis_year: params.get("analysis_year") ? parseInt(params.get("analysis_year")!, 10) : null,
      include_annual_luck: params.get("include_annual_luck") !== "false",
      analysis_month: params.get("analysis_month") ? parseInt(params.get("analysis_month")!, 10) : null,
      analysis_day: params.get("analysis_day") ? parseInt(params.get("analysis_day")!, 10) : null,
      analysis_time: params.get("analysis_time") || null,
      school: params.get("school") || "classic",
      location: params.get("location") || null,
      talisman_year_hs: params.get("talisman_year_hs") || null,
      talisman_year_eb: params.get("talisman_year_eb") || null,
      talisman_month_hs: params.get("talisman_month_hs") || null,
      talisman_month_eb: params.get("talisman_month_eb") || null,
      talisman_day_hs: params.get("talisman_day_hs") || null,
      talisman_day_eb: params.get("talisman_day_eb") || null,
      talisman_hour_hs: params.get("talisman_hour_hs") || null,
      talisman_hour_eb: params.get("talisman_hour_eb") || null,
    });

    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "BaZi analysis failed" },
      { status: 500 },
    );
  }
}
