import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';
import { mapTRPCErrorToStatus } from '$lib/server/trpc/errors';

export const GET: RequestHandler = async (event) => {
	try {
		const url = event.url;

		const birth_date = url.searchParams.get('birth_date');
		if (!birth_date) {
			return json({ error: 'birth_date is required' }, { status: 400 });
		}

		const gender = url.searchParams.get('gender');
		if (!gender || (gender !== 'male' && gender !== 'female')) {
			return json({ error: 'gender must be "male" or "female"' }, { status: 400 });
		}

		const analysisYear = url.searchParams.get('analysis_year');
		const analysisMonth = url.searchParams.get('analysis_month');
		const analysisDay = url.searchParams.get('analysis_day');

		const input = {
			birth_date,
			birth_time: url.searchParams.get('birth_time') ?? undefined,
			gender: gender as 'male' | 'female',
			analysis_year: analysisYear ? Number(analysisYear) : undefined,
			include_annual_luck: url.searchParams.get('include_annual_luck') !== 'false',
			analysis_month: analysisMonth ? Number(analysisMonth) : undefined,
			analysis_day: analysisDay ? Number(analysisDay) : undefined,
			analysis_time: url.searchParams.get('analysis_time') ?? undefined,
			school: (url.searchParams.get('school') as 'classic' | 'physics') ?? undefined,
			location:
				(url.searchParams.get('location') as 'overseas' | 'birthplace') ?? undefined,
			talisman_year_hs: url.searchParams.get('talisman_year_hs') ?? undefined,
			talisman_year_eb: url.searchParams.get('talisman_year_eb') ?? undefined,
			talisman_month_hs: url.searchParams.get('talisman_month_hs') ?? undefined,
			talisman_month_eb: url.searchParams.get('talisman_month_eb') ?? undefined,
			talisman_day_hs: url.searchParams.get('talisman_day_hs') ?? undefined,
			talisman_day_eb: url.searchParams.get('talisman_day_eb') ?? undefined,
			talisman_hour_hs: url.searchParams.get('talisman_hour_hs') ?? undefined,
			talisman_hour_eb: url.searchParams.get('talisman_hour_eb') ?? undefined,
		};

		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.bazi.analyze(input);
		return json(result);
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};
