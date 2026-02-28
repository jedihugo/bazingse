import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';
import { mapTRPCErrorToStatus } from '$lib/server/trpc/errors';

export const POST: RequestHandler = async (event) => {
	try {
		const body = await event.request.json();
		const caller = appRouter.createCaller(createContext(event));
		const result = await caller.lifeEvent.create({
			profileId: event.params.id,
			data: body,
		});
		return json(result, { status: 201 });
	} catch (e: unknown) {
		const { status, message } = mapTRPCErrorToStatus(e);
		return json({ error: message }, { status });
	}
};
