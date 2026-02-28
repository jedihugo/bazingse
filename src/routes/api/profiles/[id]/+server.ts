import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';
import { mapTRPCErrorToStatus } from '$lib/server/trpc/errors';

export const GET: RequestHandler = async (event) => {
	try {
		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.profile.get({ id: event.params.id });
		return json(result);
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};

export const PUT: RequestHandler = async (event) => {
	try {
		const body = await event.request.json();
		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.profile.update({ id: event.params.id, data: body });
		return json(result);
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};

export const DELETE: RequestHandler = async (event) => {
	try {
		const caller = appRouter.createCaller(createContext(event));
		await caller.profile.delete({ id: event.params.id });
		return json({ success: true });
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};
