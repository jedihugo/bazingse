# Svelte 5 Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Next.js/React with SvelteKit/Svelte 5 + Cloudflare Pages + D1 + Drizzle ORM, in-place.

**Architecture:** SvelteKit at repo root. tRPC server in `src/lib/server/trpc/`, Drizzle ORM talks to Cloudflare D1. All BaZi logic in `src/lib/bazi/` stays untouched. Svelte 5 runes for reactivity. Scoped CSS per component. Capacitor kept for iOS.

**Tech Stack:** SvelteKit 2, Svelte 5, tRPC 11, Drizzle ORM, Cloudflare Pages + D1, Zod, Capacitor 8

**Design Doc:** `docs/plans/2026-02-28-svelte5-migration-design.md`

---

## Phase 0: Scaffold SvelteKit (nuke React)

### Task 1: Create migration branch and backup

**Files:**
- None (git operations only)

**Step 1: Create branch**

```bash
git checkout -b svelte5-migration
```

**Step 2: Commit current state as checkpoint**

```bash
git add -A && git commit -m "checkpoint: pre-migration state"
```

---

### Task 2: Remove React/Next.js files and dependencies

**Files:**
- Delete: `next.config.js`, `middleware.ts`, `next-env.d.ts`, `.next/`
- Delete: `src/app/` (entire directory — pages, API routes, globals.css)
- Delete: `src/components/` (entire directory — will recreate as .svelte)
- Delete: `src/i18n/`, `src/locales/` (i18n deferred)
- Delete: `src/lib/t.ts` (translation key constants)
- Delete: `src/lib/__mocks__/`
- Keep: `src/lib/bazi/`, `src/lib/api.types.ts`, `src/lib/api.utils.ts`
- Keep: `src/server/` (routers, schemas, services)

**Step 1: Delete Next.js config files**

```bash
rm -f next.config.js middleware.ts next-env.d.ts
rm -rf .next out
```

**Step 2: Delete React component directories**

```bash
rm -rf src/app src/components src/i18n src/locales
rm -f src/lib/t.ts
rm -rf src/lib/__mocks__
```

**Step 3: Strip React/Next deps from package.json**

Remove these dependencies from `package.json`:
- `next`, `react`, `react-dom`, `server-only`
- `@vercel/analytics`
- `@types/react`, `@types/react-dom`
- `@capacitor/android` (keep ios)

Keep: `@trpc/client`, `@trpc/server`, `superjson`, `zod`, `@capacitor/core`, `@capacitor/cli`, `@capacitor/ios`, `@playwright/test`, `typescript`, `lunar-typescript`, `vitest`

**Step 4: Clean node_modules**

```bash
rm -rf node_modules package-lock.json
```

**Step 5: Commit the teardown**

```bash
git add -A && git commit -m "chore: remove Next.js/React files and dependencies"
```

---

### Task 3: Initialize SvelteKit project

**Files:**
- Create: `svelte.config.js`
- Create: `vite.config.ts`
- Modify: `package.json` (new deps + scripts)
- Modify: `tsconfig.json` (SvelteKit paths)
- Create: `src/app.html`
- Create: `src/app.css`

**Step 1: Install SvelteKit and dependencies**

```bash
npm create svelte@latest . -- --template skeleton --types typescript --no-add-ons
```

If prompted about existing files, overwrite `package.json` and `tsconfig.json` only. Then add the remaining deps:

```bash
npm install @sveltejs/adapter-cloudflare @trpc/client@^11 @trpc/server@^11 superjson zod drizzle-orm @capacitor/core @capacitor/cli @capacitor/ios
npm install -D drizzle-kit @cloudflare/workers-types wrangler lunar-typescript vitest @playwright/test
```

**Step 2: Configure svelte.config.js**

```javascript
import adapter from '@sveltejs/adapter-cloudflare';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    alias: {
      '$lib': './src/lib',
      '$lib/*': './src/lib/*',
    },
  },
};

export default config;
```

**Step 3: Configure vite.config.ts**

```typescript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    port: 4321,
  },
});
```

**Step 4: Update tsconfig.json**

Replace contents with SvelteKit-compatible config:

```json
{
  "extends": "./.svelte-kit/tsconfig.json",
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "sourceMap": true,
    "strict": true,
    "moduleResolution": "bundler"
  }
}
```

**Step 5: Update package.json scripts**

```json
{
  "scripts": {
    "dev": "vite dev --port 4321",
    "build": "vite build",
    "preview": "vite preview --port 4321",
    "check": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json",
    "check:watch": "svelte-kit sync && svelte-check --tsconfig ./tsconfig.json --watch"
  }
}
```

**Step 6: Create src/app.html**

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover" />
    <meta name="mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="default" />
    <meta name="format-detection" content="telephone=no" />
    <meta name="color-scheme" content="dark light" />
    <meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff" />
    <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#1e1e2e" />
    <link rel="icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" href="/bazingse-logo.png" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet" />
    %sveltekit.head%
  </head>
  <body>
    <div id="svelte">%sveltekit.body%</div>
  </body>
</html>
```

**Step 7: Create src/app.css**

Extract ONLY the CSS custom properties (theme variables) and base resets from the old `globals.css`. This is the global foundation — component-specific styles move into `.svelte` files later.

Read the old `globals.css` (it was deleted but exists in git history):

```bash
git show HEAD~1:src/app/globals.css > /tmp/globals-backup.css
```

Copy the `:root` variables, `*` reset, `html`/`body` base, light/dark theme variables, and core utility classes (`.tui-bg`, `.tui-text`, `.tui-btn`, `.tui-frame`, `.tui-input`, `.main-content`). Leave component-specific classes for scoped CSS.

**Step 8: Commit SvelteKit scaffold**

```bash
git add -A && git commit -m "feat: initialize SvelteKit scaffold with Cloudflare adapter"
```

**Step 9: Verify dev server starts**

```bash
npm run dev
```

Expected: Vite dev server on port 4321, blank page loads.

---

## Phase 1: Data Layer (Drizzle + D1)

### Task 4: Create Drizzle schema and DB connection

**Files:**
- Create: `src/lib/server/db/schema.ts`
- Create: `src/lib/server/db/index.ts`
- Create: `drizzle.config.ts`
- Create: `src/app.d.ts` (SvelteKit platform types)

**Step 1: Create src/app.d.ts for Cloudflare D1 types**

```typescript
/// <reference types="@sveltejs/adapter-cloudflare" />

declare global {
  namespace App {
    interface Platform {
      env: {
        DB: D1Database;
      };
    }
  }
}

export {};
```

**Step 2: Create Drizzle schema**

Create `src/lib/server/db/schema.ts`:

```typescript
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const profiles = sqliteTable('profiles', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  birth_date: text('birth_date').notNull(),
  birth_time: text('birth_time'),
  gender: text('gender', { enum: ['male', 'female'] }).notNull(),
  place_of_birth: text('place_of_birth'),
  phone: text('phone'),
  created_at: text('created_at'),
  updated_at: text('updated_at'),
});

export const lifeEvents = sqliteTable('life_events', {
  id: text('id').primaryKey(),
  profile_id: text('profile_id').notNull().references(() => profiles.id, { onDelete: 'cascade' }),
  year: integer('year').notNull(),
  month: integer('month'),
  day: integer('day'),
  location: text('location'),
  notes: text('notes'),
  is_abroad: integer('is_abroad', { mode: 'boolean' }).default(false),
  created_at: text('created_at'),
  updated_at: text('updated_at'),
});
```

**Step 3: Create DB connection helper**

Create `src/lib/server/db/index.ts`:

```typescript
import { drizzle } from 'drizzle-orm/d1';
import * as schema from './schema';

export function getDb(d1: D1Database) {
  return drizzle(d1, { schema });
}

export type Database = ReturnType<typeof getDb>;
```

**Step 4: Create drizzle.config.ts**

```typescript
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/lib/server/db/schema.ts',
  out: './drizzle',
  dialect: 'sqlite',
});
```

**Step 5: Generate initial migration**

```bash
npx drizzle-kit generate
```

**Step 6: Commit**

```bash
git add -A && git commit -m "feat: add Drizzle ORM schema and D1 connection"
```

---

## Phase 2: tRPC Server Wiring

### Task 5: Move tRPC server into SvelteKit structure

The existing tRPC code at `src/server/` needs to move to `src/lib/server/trpc/` (SvelteKit convention: `$lib/server/` for server-only code).

**Files:**
- Move: `src/server/trpc.ts` → `src/lib/server/trpc/init.ts`
- Move: `src/server/schemas.ts` → `src/lib/server/trpc/schemas.ts`
- Move: `src/server/routers/_app.ts` → `src/lib/server/trpc/router.ts`
- Move: `src/server/routers/*.ts` → `src/lib/server/trpc/routers/*.ts`
- Move: `src/server/services/*.ts` → `src/lib/server/services/*.ts`
- Delete: `src/server/` (old location)

**Step 1: Create directory structure**

```bash
mkdir -p src/lib/server/trpc/routers
mkdir -p src/lib/server/services
```

**Step 2: Move files**

```bash
cp src/server/trpc.ts src/lib/server/trpc/init.ts
cp src/server/schemas.ts src/lib/server/trpc/schemas.ts
cp src/server/routers/_app.ts src/lib/server/trpc/router.ts
cp src/server/routers/health.ts src/lib/server/trpc/routers/health.ts
cp src/server/routers/profile.ts src/lib/server/trpc/routers/profile.ts
cp src/server/routers/lifeEvent.ts src/lib/server/trpc/routers/lifeEvent.ts
cp src/server/routers/bazi.ts src/lib/server/trpc/routers/bazi.ts
cp src/server/routers/dongGong.ts src/lib/server/trpc/routers/dongGong.ts
cp src/server/services/bazi.ts src/lib/server/services/bazi.ts
cp src/server/services/dong-gong.ts src/lib/server/services/dong-gong.ts
rm -rf src/server
```

**Step 3: Update import paths**

All `@/server/` imports become `$lib/server/`. All `@/lib/` imports become `$lib/`. Update every moved file:

- `init.ts`: no path changes needed (self-contained)
- `router.ts`: update imports from `'../trpc'` → `'./init'`, `'./health'` → `'./routers/health'`, etc.
- Each router file: update `'../trpc'` → `'../init'`, `'../schemas'` → `'../schemas'` (stays same), service imports update
- Service files: update `'@/lib/bazi/'` → `'$lib/bazi/'`

**Step 4: Update routers to accept `ctx.db`**

The profile and lifeEvent routers currently import from `$lib/db.ts` (which calls Railway). Replace with Drizzle queries using `ctx.db`. The bazi and dongGong routers call pure service functions — no DB changes needed.

Update `profile.ts` router to use Drizzle:

```typescript
import { eq } from 'drizzle-orm';
import { profiles, lifeEvents } from '../db/schema';
// ... in each procedure, use ctx.db.select().from(profiles)...
```

Update `lifeEvent.ts` router similarly.

**Step 5: Delete old db.ts proxy**

```bash
rm src/lib/db.ts
```

**Step 6: Commit**

```bash
git add -A && git commit -m "feat: move tRPC server to SvelteKit lib structure with Drizzle"
```

---

### Task 6: Create tRPC endpoint and context

**Files:**
- Create: `src/routes/api/trpc/[...path]/+server.ts`
- Create: `src/lib/server/trpc/context.ts`
- Modify: `src/lib/server/trpc/init.ts` (add context type)

**Step 1: Create tRPC context**

Create `src/lib/server/trpc/context.ts`:

```typescript
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
```

**Step 2: Update tRPC init to use context**

Update `src/lib/server/trpc/init.ts`:

```typescript
import { initTRPC, TRPCError } from '@trpc/server';
import superjson from 'superjson';
import type { TRPCContext } from './context';

const t = initTRPC.context<TRPCContext>().create({
  transformer: superjson,
});

export const router = t.router;
export const publicProcedure = t.procedure;
export { TRPCError };
```

**Step 3: Create SvelteKit tRPC handler**

Create `src/routes/api/trpc/[...path]/+server.ts`:

```typescript
import type { RequestHandler } from './$types';
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '$lib/server/trpc/router';
import { createContext } from '$lib/server/trpc/context';

const handler: RequestHandler = async (event) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req: event.request,
    router: appRouter,
    createContext: () => createContext(event),
  });

export const GET = handler;
export const POST = handler;
```

**Step 4: Commit**

```bash
git add -A && git commit -m "feat: add tRPC SvelteKit endpoint with D1 context"
```

---

### Task 7: Update tRPC client

**Files:**
- Modify: `src/lib/trpc.ts`
- Modify: `src/lib/api.ts`

**Step 1: Update tRPC client**

Replace `src/lib/trpc.ts`:

```typescript
import { createTRPCClient, httpBatchLink } from '@trpc/client';
import superjson from 'superjson';
import type { AppRouter } from '$lib/server/trpc/router';

export const trpc = createTRPCClient<AppRouter>({
  links: [
    httpBatchLink({
      url: '/api/trpc',
      transformer: superjson,
    }),
  ],
});
```

**Step 2: Update api.ts imports**

Update `src/lib/api.ts` — change `@/` imports to `$lib/`:

```typescript
import { trpc } from '$lib/trpc';
import type { ... } from '$lib/api.types';
```

Remove `'use client'` if present.

**Step 3: Commit**

```bash
git add -A && git commit -m "feat: update tRPC client for SvelteKit"
```

---

## Phase 3: App Shell (Layout + Routing)

### Task 8: Create root layout with PasswordGate and ThemeToggle

**Files:**
- Create: `src/routes/+layout.svelte`
- Create: `src/components/PasswordGate.svelte`
- Create: `src/components/Header.svelte`
- Create: `src/components/ThemeToggle.svelte`

**Step 1: Create ThemeToggle.svelte**

```svelte
<script lang="ts">
  let dark = $state(false);

  $effect(() => {
    const saved = localStorage.getItem('theme');
    dark = saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  });

  function toggle() {
    dark = !dark;
    localStorage.setItem('theme', dark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  }
</script>

<button onclick={toggle} class="theme-toggle" aria-label="Toggle theme">
  {dark ? '☀' : '☽'}
</button>

<style>
  .theme-toggle {
    font-size: 1.2rem;
    padding: 0.25rem 0.5rem;
    border: 1px solid var(--tui-border);
    background: var(--tui-bg);
    color: var(--tui-fg);
    cursor: pointer;
  }
</style>
```

**Step 2: Create Header.svelte**

Port from React `Header.tsx`. Replace `Link` from next/link with `<a>` tags, `Image` from next/image with `<img>`.

```svelte
<script lang="ts">
  import ThemeToggle from './ThemeToggle.svelte';
</script>

<header class="header">
  <div class="header-inner">
    <a href="/" class="logo-link">
      <img src="/bazingse-logo.png" alt="BaZingSe" width="32" height="32" class="logo" />
      <span class="title">BaZingSe</span>
    </a>
    <div class="header-actions">
      <a href="/calendar" class="nav-link">Calendar</a>
      <ThemeToggle />
    </div>
  </div>
</header>

<style>
  /* Port header styles from globals.css */
  .header {
    border-bottom: 1px solid var(--tui-border);
    padding: 0.5rem 1rem;
    background: var(--tui-bg);
  }
  .header-inner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 900px;
    margin: 0 auto;
  }
  .logo-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    color: var(--tui-fg);
  }
  .logo { border-radius: 4px; }
  .title { font-weight: 700; font-size: 1.1rem; }
  .header-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  .nav-link {
    color: var(--tui-fg-dim);
    text-decoration: none;
    font-size: 0.9rem;
  }
  .nav-link:hover { color: var(--tui-fg); }
</style>
```

**Step 3: Create PasswordGate.svelte**

Port from React `PasswordGate.tsx`. Password: `lombok29`.

```svelte
<script lang="ts">
  import { onMount } from 'svelte';

  let authenticated = $state(false);
  let password = $state('');
  let error = $state('');
  let mounted = $state(false);

  onMount(() => {
    authenticated = sessionStorage.getItem('bazingse_auth') === 'true';
    mounted = true;
  });

  function submit() {
    if (password === 'lombok29') {
      sessionStorage.setItem('bazingse_auth', 'true');
      authenticated = true;
      error = '';
    } else {
      error = 'Wrong password';
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') submit();
  }
</script>

{#if !mounted}
  <div class="gate-loading"></div>
{:else if authenticated}
  {@render children()}
{:else}
  <div class="gate">
    <div class="gate-box">
      <h2>BaZingSe</h2>
      <input
        type="password"
        bind:value={password}
        onkeydown={handleKeydown}
        placeholder="Password"
        class="tui-input"
      />
      {#if error}
        <p class="error">{error}</p>
      {/if}
      <button onclick={submit} class="tui-btn">Enter</button>
    </div>
  </div>
{/if}

{#snippet children()}
  <slot />
{/snippet}

<style>
  .gate {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: var(--tui-bg);
  }
  .gate-box {
    text-align: center;
    padding: 2rem;
    border: 1px solid var(--tui-border);
  }
  .gate-box h2 {
    margin-bottom: 1rem;
    color: var(--tui-fg);
  }
  .error {
    color: var(--tui-error);
    margin-top: 0.5rem;
    font-size: 0.85rem;
  }
  .gate-loading { min-height: 100vh; background: var(--tui-bg); }
</style>
```

**Step 4: Create root layout**

Create `src/routes/+layout.svelte`:

```svelte
<script lang="ts">
  import '../app.css';
  import PasswordGate from '$lib/../components/PasswordGate.svelte';
</script>

<svelte:head>
  <title>BaZingSe - Chinese BaZi Astrology</title>
  <meta name="description" content="Chinese BaZi Four Pillars astrology calculator" />
</svelte:head>

<PasswordGate>
  <slot />
</PasswordGate>
```

**Step 5: Create minimal home page placeholder**

Create `src/routes/+page.svelte`:

```svelte
<script lang="ts">
  import Header from '../components/Header.svelte';
</script>

<div class="min-h-screen tui-bg">
  <Header />
  <main class="mx-auto main-content px-4 py-4">
    <p class="tui-text">Home page — components coming next.</p>
  </main>
</div>
```

**Step 6: Verify the app runs**

```bash
npm run dev
```

Expected: Dev server starts, password gate shows, enter `lombok29`, see header + placeholder text.

**Step 7: Commit**

```bash
git add -A && git commit -m "feat: add SvelteKit root layout with PasswordGate, Header, ThemeToggle"
```

---

## Phase 4: Component Migration (React → Svelte 5)

Each task below converts one or more React components to Svelte 5 using runes. The general pattern:

- `useState(x)` → `let x = $state(x)`
- `useMemo(() => expr)` → `let x = $derived(expr)`
- `useEffect(() => { ... })` → `$effect(() => { ... })`
- `useCallback(fn)` → just `fn` (no wrapper needed)
- `useRef(null)` → `let el: HTMLElement` + `bind:this={el}`
- `useContext(Ctx)` → `getContext('key')`
- Props: `let { prop1, prop2 }: Props = $props()`
- `className` → `class`
- `onClick` → `onclick`
- `onChange` → `oninput` (for inputs)
- `{condition && <X/>}` → `{#if condition}<X/>{/if}`
- `arr.map(x => <X key={x.id}/>)` → `{#each arr as x (x.id)}<X/>{/each}`

### Task 9: PillarCard + PillarTag (leaf components)

**Files:**
- Create: `src/components/PillarCard.svelte` (from `PillarCard.tsx`, 243 lines)
- Create: `src/components/PillarTag.svelte` (from `PillarTag.tsx`, 67 lines)

Port these two leaf components. They have no children or complex state — just props and rendering. Copy the scoped styles from globals.css `.pillar-card` and `.pillar-tag` selectors into the component `<style>` blocks.

**Commit:** `feat: add PillarCard and PillarTag Svelte components`

---

### Task 10: BaZiChart (pillar grid)

**Files:**
- Create: `src/components/BaZiChart.svelte` (from `BaZiChart.tsx`, 635 lines)

This is the largest component. It renders a grid of PillarCards. Key conversion points:
- Multiple `useState` for expand/collapse states → `$state`
- `useMemo` for derived pillar data → `$derived`
- Event handlers → plain functions
- Import PillarCard.svelte and PillarTag.svelte

**Commit:** `feat: add BaZiChart Svelte component`

---

### Task 11: ElementAnalysis

**Files:**
- Create: `src/components/ElementAnalysis.svelte` (from `ElementAnalysis.tsx`, 223 lines)

Renders element score breakdowns. Mostly display logic with some derived calculations.

**Commit:** `feat: add ElementAnalysis Svelte component`

---

### Task 12: NarrativeCard + NarrativeDisplay

**Files:**
- Create: `src/components/NarrativeCard.svelte` (from `NarrativeCard.tsx`, 162 lines)
- Create: `src/components/NarrativeDisplay.svelte` (from `NarrativeDisplay.tsx`, 38 lines)

Simple display components. NarrativeDisplay wraps a list of NarrativeCards.

**Commit:** `feat: add NarrativeCard and NarrativeDisplay Svelte components`

---

### Task 13: Chat-form input system

**Files:**
- Create: `src/components/chat-form/context.ts` (Svelte context, replaces ChatFormContext.tsx)
- Create: `src/components/chat-form/ChatForm.svelte` (from ChatForm.tsx, 133 lines)
- Create: `src/components/chat-form/ChatFormField.svelte` (from ChatFormField.tsx, 86 lines)
- Create: `src/components/chat-form/GuidedDateInput.svelte` (from GuidedDateInput.tsx, 245 lines)
- Create: `src/components/chat-form/GuidedTimeInput.svelte` (from GuidedTimeInput.tsx, 183 lines)
- Create: `src/components/chat-form/InlineSelector.svelte` (from InlineSelector.tsx, 159 lines)
- Create: `src/components/chat-form/TypeaheadSelect.svelte` (from TypeaheadSelect.tsx, 254 lines)
- Create: `src/components/chat-form/index.ts`

This is the TUI input system — keyboard-first with focus management. Key conversions:
- `ChatFormContext` (React context) → Svelte `setContext`/`getContext` with a shared store
- `useRef` for focus management → `bind:this` + context
- `useCallback` for keyboard handlers → plain functions
- `useEffect` for event listeners → `$effect`

The context needs to track the active field index and provide `registerField`, `focusNext`, `focusPrev` functions.

**Commit:** `feat: add chat-form TUI input system (Svelte 5)`

---

### Task 14: InlineProfileForm

**Files:**
- Create: `src/components/InlineProfileForm.svelte` (from InlineProfileForm.tsx, 248 lines)

Uses chat-form components. Handles profile creation with guided date/time inputs.

**Commit:** `feat: add InlineProfileForm Svelte component`

---

### Task 15: SearchableProfileList

**Files:**
- Create: `src/components/SearchableProfileList.svelte` (from SearchableProfileList.tsx, 259 lines)

Filterable profile list with keyboard navigation. Key conversions:
- `useState` for search/filter → `$state`
- `useMemo` for filtered list → `$derived`
- `useRouter().push()` → `import { goto } from '$app/navigation'`

**Commit:** `feat: add SearchableProfileList Svelte component`

---

### Task 16: Home page (wire up)

**Files:**
- Modify: `src/routes/+page.svelte`

Wire up the actual home page with InlineProfileForm + SearchableProfileList. Port logic from the old `src/app/page.tsx`:
- Load profiles on mount via `$effect`
- Show/hide create form with `$state`
- Navigation with `goto()` from `$app/navigation`

**Commit:** `feat: wire up home page with profile list and create form`

---

### Task 17: Remaining display components

**Files:**
- Create: `src/components/DmLensDisplay.svelte` (140 lines)
- Create: `src/components/ClientSummaryDisplay.svelte` (127 lines)
- Create: `src/components/WealthStorageDisplay.svelte` (106 lines)

Three standalone display components. Mostly props → rendered HTML.

**Commit:** `feat: add DmLens, ClientSummary, WealthStorage display components`

---

### Task 18: ProfileInfoBlock

**Files:**
- Create: `src/components/ProfileInfoBlock.svelte` (from ProfileInfoBlock.tsx, 321 lines)

Editable profile info display. Uses chat-form components for inline editing.

**Commit:** `feat: add ProfileInfoBlock Svelte component`

---

### Task 19: InlineLifeEventForm

**Files:**
- Create: `src/components/InlineLifeEventForm.svelte` (from InlineLifeEventForm.tsx, 314 lines)

Life event creation form using chat-form components.

**Commit:** `feat: add InlineLifeEventForm Svelte component`

---

### Task 20: LifeEventBlock

**Files:**
- Create: `src/components/LifeEventBlock.svelte` (from LifeEventBlock.tsx, 438 lines)

Displays a life event with its BaZi chart and analysis. Uses BaZiChart, ElementAnalysis, NarrativeDisplay.

**Commit:** `feat: add LifeEventBlock Svelte component`

---

### Task 21: ProfilePage

**Files:**
- Create: `src/components/ProfilePage.svelte` (from ProfilePage.tsx, 373 lines)

Profile view orchestrator. Loads profile data, renders ProfileInfoBlock + LifeEventBlocks. Key conversions:
- `useRouter()` → `goto()`
- Multiple `useState` → `$state`
- `useEffect` for data loading → `$effect`
- `useCallback` → plain functions

**Commit:** `feat: add ProfilePage Svelte component`

---

### Task 22: Profile detail route

**Files:**
- Create: `src/routes/profile/[id]/+page.svelte`

```svelte
<script lang="ts">
  import { page } from '$app/stores';
  import Header from '../../../components/Header.svelte';
  import ProfilePage from '../../../components/ProfilePage.svelte';

  let profileId = $derived($page.params.id);
</script>

<div class="min-h-screen tui-bg">
  <Header />
  <main class="mx-auto main-content">
    <div class="mx-auto" style="max-width: 900px;">
      {#if profileId}
        <ProfilePage {profileId} />
      {:else}
        <p class="text-center tui-text-muted">Loading...</p>
      {/if}
    </div>
  </main>
</div>
```

**Commit:** `feat: add profile detail route`

---

### Task 23: DongGongCalendar

**Files:**
- Create: `src/components/DongGongCalendar.svelte` (from DongGongCalendar.tsx, 475 lines)

Calendar component with month navigation. Complex state for selected day, expanded details.

**Commit:** `feat: add DongGongCalendar Svelte component`

---

### Task 24: Calendar route

**Files:**
- Create: `src/routes/calendar/+page.svelte`

```svelte
<script lang="ts">
  import Header from '../../components/Header.svelte';
  import DongGongCalendar from '../../components/DongGongCalendar.svelte';
</script>

<div class="min-h-screen tui-bg">
  <Header />
  <main class="mx-auto main-content px-4 py-4">
    <div class="mx-auto" style="max-width: 800px;">
      <DongGongCalendar />
    </div>
  </main>
</div>
```

**Commit:** `feat: add calendar route`

---

## Phase 5: REST API Routes (backward compat)

### Task 25: Add REST API routes alongside tRPC

**Files:**
- Create: `src/routes/api/health/+server.ts`
- Create: `src/routes/api/profiles/+server.ts`
- Create: `src/routes/api/profiles/[id]/+server.ts`
- Create: `src/routes/api/profiles/[id]/life_events/+server.ts`
- Create: `src/routes/api/profiles/[id]/life_events/[eid]/+server.ts`
- Create: `src/routes/api/analyze_bazi/+server.ts`
- Create: `src/routes/api/dong_gong_calendar/+server.ts`

These are thin wrappers calling the same tRPC router procedures via `appRouter.createCaller()`. This provides REST + OpenAPI compatibility.

Each route handler:
1. Creates a tRPC caller with `createContext(event)`
2. Parses request params/body
3. Calls the appropriate procedure
4. Returns JSON response

**Commit:** `feat: add REST API routes (backward compat with tRPC caller)`

---

## Phase 6: Capacitor + Cleanup

### Task 26: Update Capacitor config

**Files:**
- Modify: `capacitor.config.ts`

Update `webDir` from `'out'` to `'build'` (SvelteKit's default output). Dev server URL stays `http://localhost:4321`.

```typescript
const config: CapacitorConfig = {
  appId: 'com.bazingse.app',
  appName: 'BaZingSe',
  webDir: 'build',
  server: USE_DEV_SERVER ? {
    url: 'http://localhost:4321',
    cleartext: true,
  } : {
    androidScheme: 'https'
  },
  // ... rest stays the same
};
```

**Commit:** `feat: update Capacitor config for SvelteKit build output`

---

### Task 27: Final cleanup and build verification

**Files:**
- Delete: any remaining React/Next.js artifacts
- Delete: `api/` Python backend directory
- Modify: `CLAUDE.md` (update project docs)

**Step 1: Delete Python backend**

```bash
rm -rf api/
```

**Step 2: Delete MCP server (will rebuild later)**

```bash
rm -rf mcp-server/
```

**Step 3: Run build**

```bash
npm run build
```

Expected: Clean build with no errors.

**Step 4: Run type checking**

```bash
npm run check
```

Expected: No type errors.

**Step 5: Commit**

```bash
git add -A && git commit -m "chore: remove Python backend, MCP server, update docs"
```

---

### Task 28: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

Update the project documentation to reflect the new architecture:
- SvelteKit 2 + Svelte 5 (not Next.js)
- Cloudflare Pages + D1 (not Vercel + Railway)
- Drizzle ORM (not Python SQLAlchemy)
- New file structure
- New dev commands
- Remove all Next.js-specific guidance

**Commit:** `feat: update CLAUDE.md for Svelte 5 architecture`

---

## Summary

| Phase | Tasks | What |
|-------|-------|------|
| 0 | 1-3 | Scaffold: branch, nuke React, init SvelteKit |
| 1 | 4 | Data layer: Drizzle schema + D1 |
| 2 | 5-7 | tRPC: move server, create endpoint, update client |
| 3 | 8 | App shell: layout, PasswordGate, Header |
| 4 | 9-24 | Components: 22 React → Svelte 5 conversions |
| 5 | 25 | REST API routes (backward compat) |
| 6 | 26-28 | Capacitor, cleanup, docs |

**Total: 28 tasks across 6 phases.**
