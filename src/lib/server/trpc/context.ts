import type { RequestEvent } from '@sveltejs/kit';
import { getDb, type Database } from '$lib/server/db';

export interface TRPCContext {
	db: Database;
}

export function createContext(event: RequestEvent): TRPCContext {
	const d1 = event.platform?.env?.DB;
	if (!d1) throw new Error('D1 database not available');
	return { db: getDb(d1) };
}
