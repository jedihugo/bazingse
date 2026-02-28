# BaZingSe: Svelte 5 Migration Design

**Date:** 2026-02-28
**Status:** Approved
**Goal:** Replace Next.js/React with SvelteKit/Svelte 5 + Cloudflare Pages + D1 + Drizzle ORM

---

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Framework | SvelteKit + Svelte 5 | Runes, scoped CSS, simpler mental model |
| Hosting | Cloudflare Pages | Edge-first, D1 integration, auto-config (Wrangler 4.68+) |
| Database | Cloudflare D1 (SQLite) | Serverless SQLite, no separate DB server |
| ORM | Drizzle ORM | Lightweight, type-safe, first-class D1 support |
| Type safety | tRPC (kept) | Already in place, framework-agnostic |
| Styling | Scoped CSS in Svelte components | Built-in, no extra deps, TUI aesthetic preserved |
| i18n | Deferred | Hardcode strings now, add Paraglide.js later |
| Mobile | Capacitor kept | iOS wrapper stays |
| Python backend | Killed | All BaZi logic already ported to TypeScript |
| MCP server | Rebuilt later | Separate effort after migration |

---

## Project Structure

```
bazingse/
├── svelte.config.js
├── vite.config.ts
├── package.json
├── tsconfig.json
├── drizzle.config.ts
├── src/
│   ├── app.html                  # SvelteKit shell
│   ├── app.css                   # Global TUI theme variables
│   ├── hooks.server.ts           # Server hooks (tRPC context)
│   ├── lib/
│   │   ├── bazi/                 # KEPT AS-IS — pure TypeScript
│   │   ├── server/
│   │   │   ├── db/
│   │   │   │   ├── schema.ts     # Drizzle schema
│   │   │   │   └── index.ts      # D1 connection
│   │   │   ├── trpc/
│   │   │   │   ├── init.ts       # tRPC initialization
│   │   │   │   ├── router.ts     # Root router (AppRouter)
│   │   │   │   └── routers/      # Sub-routers
│   │   │   └── services/         # KEPT — bazi.ts, dong-gong.ts
│   │   ├── trpc.ts               # tRPC client
│   │   ├── api.types.ts          # KEPT
│   │   └── api.utils.ts          # KEPT
│   ├── routes/
│   │   ├── +layout.svelte        # Root layout (PasswordGate, theme)
│   │   ├── +page.svelte          # Home (profiles list)
│   │   ├── profile/[id]/
│   │   │   └── +page.svelte      # Profile detail
│   │   ├── calendar/
│   │   │   └── +page.svelte      # Dong Gong calendar
│   │   └── api/trpc/[...path]/
│   │       └── +server.ts        # tRPC HTTP handler
│   └── components/               # Svelte 5 components (runes)
├── ios/                          # Capacitor (kept)
└── drizzle/                      # Generated migrations
```

---

## Data Layer: Drizzle + D1

Two tables matching existing Python models:

```typescript
// profiles
id:             text PK
name:           text NOT NULL
birth_date:     text NOT NULL     // "YYYY-MM-DD"
birth_time:     text              // "HH:MM" or null
gender:         text NOT NULL     // "male" | "female"
place_of_birth: text
phone:          text
created_at:     text
updated_at:     text

// life_events
id:             text PK
profile_id:     text FK → profiles.id
year:           integer NOT NULL
month:          integer
day:            integer
location:       text
notes:          text
is_abroad:      integer (boolean)
created_at:     text
updated_at:     text
```

D1 binding comes through SvelteKit `platform.env.DB`. Drizzle wraps it:

```typescript
import { drizzle } from 'drizzle-orm/d1';
export function getDb(d1: D1Database) {
  return drizzle(d1, { schema });
}
```

Migration from Railway: one-time SQLite export → `wrangler d1 execute` import.

---

## tRPC Wiring

Existing tRPC code (routers, schemas, services) is framework-agnostic. Changes:

1. **Handler**: SvelteKit catch-all route at `api/trpc/[...path]/+server.ts` using `fetchRequestHandler`
2. **Context**: passes `db` from `platform.env.DB` into tRPC context
3. **Client**: same `createTRPCClient` with `httpBatchLink` pointing to `/api/trpc`
4. **Routers**: receive `ctx.db` instead of importing db module directly
5. **Services**: zero changes — pure computation functions

---

## Component Migration: React → Svelte 5

22 React components → Svelte 5 with runes. Translation patterns:

| React | Svelte 5 |
|-------|----------|
| `useState(x)` | `let x = $state(x)` |
| `useMemo` | `let x = $derived(...)` |
| `useEffect` | `$effect(() => ...)` |
| `useRef` | `bind:this` |
| `useContext` | `setContext`/`getContext` |
| `{cond && <X/>}` | `{#if cond}<X/>{/if}` |
| `arr.map()` | `{#each arr as x}<X/>{/each}` |
| Props interface | `let { ... }: Props = $props()` |
| `className` | `class` |
| `onClick` | `onclick` |

Priority order (dependencies first):
1. PasswordGate, Header, ThemeToggle — layout shell
2. PillarCard, PillarTag — leaf components
3. BaZiChart, ElementAnalysis — compose pillars
4. NarrativeCard, NarrativeDisplay — standalone
5. Chat-form components — TUI input system
6. InlineProfileForm, SearchableProfileList — home page
7. ProfilePage, ProfileInfoBlock, LifeEventBlock — profile detail
8. InlineLifeEventForm — life event form
9. DongGongCalendar — calendar page
10. DmLensDisplay, WealthStorageDisplay, ClientSummaryDisplay — remaining

---

## What Gets Killed

- `next.config.js`, `middleware.ts`, `next-env.d.ts`
- `src/app/` directory (Next.js App Router)
- All `.tsx` files
- `react`, `react-dom`, `next`, `next-intl`, `@vercel/analytics` deps
- `src/i18n/`, `src/locales/` (deferred)
- `api/` Python backend
- `mcp-server/` (rebuilt later)

## What Survives Unchanged

- `src/lib/bazi/` — entire BaZi engine (pure TS)
- `src/server/services/bazi.ts`, `dong-gong.ts` — pure TS
- `src/server/schemas.ts` — Zod schemas
- `src/lib/api.types.ts` — types
- `src/lib/api.utils.ts` — utilities
- `ios/` — Capacitor
- CSS theme variables (extracted + slimmed into `app.css`)
