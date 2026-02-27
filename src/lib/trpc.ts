import { createTRPCClient, httpBatchLink } from '@trpc/client';
import superjson from 'superjson';
import type { AppRouter } from '@/server/routers/_app';

function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  // SSR — use localhost
  return `http://localhost:${process.env.PORT ?? 4321}`;
}

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: `${getBaseUrl()}/api/trpc`,
      transformer: superjson,
    }),
  ],
});
