import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';
import { mapTRPCErrorToStatus } from '$lib/server/trpc/errors';

export const GET: RequestHandler = async (event) => {
	try {
		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.profile.list({ skip: 0, limit: 10000 });
		return json(result);
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};

export const POST: RequestHandler = async (event) => {
	try {
		const body = await event.request.json();
		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.profile.create(body);
		return json(result, { status: 201 });
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};
