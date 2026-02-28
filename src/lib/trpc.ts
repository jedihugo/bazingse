import { createTRPCClient, httpBatchLink } from '@trpc/client';
import superjson from 'superjson';
import type { AppRouter } from '$lib/server/trpc/router';

function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  // SSR on Cloudflare Workers — no localhost available, use relative URL
  return '';
}

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: `${getBaseUrl()}/api/trpc`,
      transformer: superjson,
    }),
  ],
});
