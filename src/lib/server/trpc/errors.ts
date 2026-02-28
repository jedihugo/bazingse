import { TRPCError } from '@trpc/server';

/**
 * Maps tRPC error codes to HTTP status codes.
 * Used by REST backward-compatibility routes to return proper HTTP responses.
 */
const TRPC_ERROR_CODE_HTTP_STATUS: Record<string, number> = {
	PARSE_ERROR: 400,
	BAD_REQUEST: 400,
	UNAUTHORIZED: 401,
	FORBIDDEN: 403,
	NOT_FOUND: 404,
	METHOD_NOT_SUPPORTED: 405,
	TIMEOUT: 408,
	CONFLICT: 409,
	PRECONDITION_FAILED: 412,
	PAYLOAD_TOO_LARGE: 413,
	UNPROCESSABLE_CONTENT: 422,
	TOO_MANY_REQUESTS: 429,
	CLIENT_CLOSED_REQUEST: 499,
	INTERNAL_SERVER_ERROR: 500,
	NOT_IMPLEMENTED: 501,
};

export function mapTRPCErrorToStatus(e: unknown): { status: number; message: string } {
	if (e instanceof TRPCError) {
		const status = TRPC_ERROR_CODE_HTTP_STATUS[e.code] ?? 500;
		return { status, message: e.message };
	}
	const message = e instanceof Error ? e.message : 'Internal server error';
	return { status: 500, message };
}
