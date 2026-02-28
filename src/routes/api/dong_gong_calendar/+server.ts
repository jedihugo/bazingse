import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';
import { mapTRPCErrorToStatus } from '$lib/server/trpc/errors';

export const GET: RequestHandler = async (event) => {
	try {
		const yearParam = event.url.searchParams.get('year');
		const monthParam = event.url.searchParams.get('month');

		if (!yearParam || !monthParam) {
			return json({ error: 'year and month query parameters are required' }, { status: 400 });
		}

		const year = Number(yearParam);
		const month = Number(monthParam);

		if (isNaN(year) || isNaN(month)) {
			return json({ error: 'year and month must be valid numbers' }, { status: 400 });
		}

		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.dongGong.calendar({ year, month });
		return json(result);
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};
