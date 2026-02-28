# CLAUDE.md

Guidance for AI agents working on **BaZingSe** - a full-stack Chinese BaZi (Four Pillars/八字) astrology application.

**Status**: SvelteKit + Svelte 5 frontend, TypeScript BaZi engine, tRPC API, Drizzle ORM, deployed on Cloudflare Pages + D1.

---

## Project Overview

- **Frontend**: SvelteKit + Svelte 5 (runes mode) at repo root
- **Backend**: tRPC routers + TypeScript BaZi engine (same repo, server-side)
- **Database**: Cloudflare D1 (SQLite) via Drizzle ORM
- **Deployment**: Cloudflare Pages (frontend + API)
- **i18n**: Deferred (hardcoded English strings for now)
- **UI Paradigm**: TUI-style Anti-WIMP (keyboard-first, no modals)

---

## Project Structure

```
bazingse/
├── svelte.config.js           # SvelteKit config (Cloudflare adapter)
├── vite.config.ts             # Vite config
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
├── capacitor.config.ts        # Capacitor iOS/Android config
├── src/
│   ├── app.css                # Global styles (TUI theme)
│   ├── app.html               # HTML shell
│   ├── routes/                # SvelteKit routes (3 pages + API)
│   │   ├── +layout.svelte     # Root layout (PasswordGate, Header, ThemeToggle)
│   │   ├── +page.svelte       # Home page (profiles list)
│   │   ├── profile/[id]/
│   │   │   └── +page.svelte   # Profile detail page
│   │   ├── calendar/
│   │   │   └── +page.svelte   # Dong Gong calendar page
│   │   └── api/               # REST + tRPC API routes
│   │       ├── trpc/[...path]/+server.ts  # tRPC handler
│   │       ├── health/+server.ts
│   │       ├── profiles/+server.ts
│   │       ├── profiles/[id]/+server.ts
│   │       ├── profiles/[id]/life_events/+server.ts
│   │       ├── profiles/[id]/life_events/[eid]/+server.ts
│   │       ├── analyze_bazi/+server.ts
│   │       └── dong_gong_calendar/+server.ts
│   ├── components/            # Svelte 5 components
│   │   ├── chat-form/         # TUI-style input components
│   │   ├── BaZiChart.svelte   # Pillar cards renderer
│   │   ├── PillarCard.svelte  # Individual pillar display
│   │   ├── PillarTag.svelte   # Compact pillar label
│   │   ├── ElementAnalysis.svelte
│   │   ├── NarrativeCard.svelte
│   │   ├── NarrativeDisplay.svelte
│   │   ├── DmLensDisplay.svelte
│   │   ├── WealthStorageDisplay.svelte
│   │   ├── ClientSummaryDisplay.svelte
│   │   ├── ProfilePage.svelte
│   │   ├── ProfileInfoBlock.svelte
│   │   ├── LifeEventBlock.svelte
│   │   ├── InlineProfileForm.svelte
│   │   ├── InlineLifeEventForm.svelte
│   │   ├── SearchableProfileList.svelte
│   │   ├── DongGongCalendar.svelte
│   │   ├── PasswordGate.svelte
│   │   ├── Header.svelte
│   │   └── ThemeToggle.svelte
│   └── lib/                   # Shared libraries
│       ├── api.ts             # Client API (tRPC-backed)
│       ├── api.types.ts       # Shared TypeScript types
│       ├── api.utils.ts       # LocalStorage, validation utils
│       ├── trpc.ts            # tRPC client setup
│       ├── bazi/              # BaZi calculation engine (TypeScript)
│       │   ├── core.ts        # STEMS + BRANCHES (source of truth)
│       │   ├── chart.ts       # Chart construction
│       │   ├── index.ts       # Engine entry point
│       │   ├── comprehensive/ # Comprehensive analysis engine
│       │   ├── narrative/     # Narrative generation
│       │   ├── life-aspects/  # Health, wealth, learning
│       │   ├── pattern-engine/# Universal pattern detection
│       │   ├── wuxing/        # Wu Xing scoring
│       │   └── *.ts           # Other modules
│       └── server/            # Server-side only
│           ├── db/
│           │   ├── index.ts   # D1 database connection
│           │   └── schema.ts  # Drizzle schema
│           ├── services/      # Business logic
│           │   ├── bazi.ts
│           │   └── dong-gong.ts
│           └── trpc/          # tRPC setup
│               ├── init.ts    # tRPC initialization
│               ├── router.ts  # Root router (AppRouter)
│               ├── context.ts # Request context (D1 db)
│               ├── errors.ts  # Error mapping
│               ├── schemas.ts # Zod schemas
│               └── routers/   # Sub-routers
│                   ├── profile.ts
│                   ├── lifeEvent.ts
│                   ├── bazi.ts
│                   ├── dongGong.ts
│                   └── health.ts
├── api/                       # Legacy Python backend (to be removed)
├── mcp-server/                # Legacy MCP server (to be removed)
├── ios/                       # Capacitor iOS app
└── tests/                     # Playwright tests
```

---

## Frontend Pages & Component Tree

### 3 Pages (SvelteKit Routes)

| Route | Page File | Key Components |
|-------|-----------|----------------|
| `/` | `src/routes/+page.svelte` | Header, InlineProfileForm, SearchableProfileList |
| `/profile/[id]` | `src/routes/profile/[id]/+page.svelte` | Header, ProfilePage |
| `/calendar` | `src/routes/calendar/+page.svelte` | Header, DongGongCalendar |

### Core Components (`src/components/`)

| Component | Purpose |
|-----------|---------|
| `PasswordGate.svelte` | App access protection |
| `Header.svelte` | Logo + title + ThemeToggle |
| `ProfilePage.svelte` | Profile view orchestrator |
| `ProfileInfoBlock.svelte` | Editable profile info display |
| `LifeEventBlock.svelte` | Life event with BaZi chart + analysis |
| `BaZiChart.svelte` | Pillar cards renderer |
| `PillarCard.svelte` | Individual pillar display |
| `PillarTag.svelte` | Compact pillar label |
| `ElementAnalysis.svelte` | Element score breakdown |
| `NarrativeDisplay.svelte` | Narrative cards container |
| `NarrativeCard.svelte` | Individual narrative card |
| `DmLensDisplay.svelte` | Day Master lens analysis |
| `WealthStorageDisplay.svelte` | Wealth storage analysis |
| `ClientSummaryDisplay.svelte` | Client-facing summary |
| `DongGongCalendar.svelte` | Dong Gong calendar |
| `InlineProfileForm.svelte` | Create profile (inline) |
| `InlineLifeEventForm.svelte` | Add life event (inline) |
| `SearchableProfileList.svelte` | Filterable profile list |
| `ThemeToggle.svelte` | Dark/light mode toggle |

### Input Components (`src/components/chat-form/`)

| Component | Purpose |
|-----------|---------|
| `ChatFormContext.svelte` | Svelte context for focus management |
| `ChatForm.svelte` | Container with title bar, keyboard shortcuts |
| `ChatFormField.svelte` | Field wrapper with blinking cursor `>` |
| `GuidedDateInput.svelte` | YYYY/MM/DD with auto-advance |
| `GuidedTimeInput.svelte` | HH:MM with unknown toggle |
| `GuidedYearInput.svelte` | Year-only input |
| `InlineSelector.svelte` | Radio-style keyboard selection `(●)/(○)` |
| `GenderSelector.svelte` | Male/Female selector |
| `TypeaheadSelect.svelte` | Keyboard-navigable dropdown |

---

## Backend Architecture

### tRPC Router Structure

Root router (`src/lib/server/trpc/router.ts`) merges 5 sub-routers:
- `health` — Health check
- `profile` — CRUD for profiles
- `lifeEvent` — CRUD for life events
- `bazi` — BaZi chart analysis
- `dongGong` — Dong Gong calendar

### tRPC + REST API

The primary API is tRPC at `/api/trpc/[...path]`. REST routes at `/api/*` are thin backward-compatibility wrappers that create a server-side tRPC caller and delegate.

### BaZi Engine (`src/lib/bazi/`)

All BaZi calculations are in TypeScript:
- `core.ts` — STEMS + BRANCHES (single source of truth)
- `chart.ts` — Chart construction
- `comprehensive/` — Comprehensive analysis engine
- `narrative/` — Narrative generation
- `wuxing/` — Wu Xing scoring system
- `pattern-engine/` — Universal pattern detection

### Database

Cloudflare D1 (SQLite) accessed via Drizzle ORM:
- Schema: `src/lib/server/db/schema.ts`
- Connection: `src/lib/server/db/index.ts` (wraps D1 binding)

---

## Svelte 5 Conventions

### Runes (MUST use these patterns)

```svelte
<script lang="ts">
  // State
  let count = $state(0);
  let items = $state<string[]>([]);

  // Derived values
  let doubled = $derived(count * 2);
  let filtered = $derived.by(() => items.filter(i => i.length > 3));

  // Props
  interface Props { name: string; onClick?: () => void; }
  let { name, onClick }: Props = $props();

  // Effects
  $effect(() => { console.log(count); });
</script>
```

### Key Patterns

1. **Props:** `let { prop1, prop2 }: Props = $props()`
2. **Children:** `import type { Snippet } from 'svelte'; let { children }: { children: Snippet } = $props()` + `{@render children()}`
3. **Navigation:** `import { goto } from '$app/navigation'`
4. **Route params:** `import { page } from '$app/stores'; let id = $derived($page.params.id)`
5. **API calls:** Import from `$lib/api`
6. **Events:** `onclick` (lowercase), `onkeydown`, `oninput`
7. **Conditionals:** `{#if cond}...{:else}...{/if}`
8. **Loops:** `{#each arr as item (item.id)}...{/each}`
9. **Class binding:** `class:active={isActive}`
10. **Refs:** `bind:this={element}`
11. **Scoped CSS:** `<style>` block at end of file
12. **No `'use client'`** — not needed in Svelte

---

## Anti-WIMP Input System (TUI-Style)

**Design Philosophy**: Replace traditional WIMP (Windows, Icons, Menus, Pointer) UI with terminal/chat-style keyboard-first interactions.

### Key Principles

1. **No Modals** - Use inline forms/panels instead
2. **Keyboard-First** - Tab, Enter, Escape for navigation
3. **Auto-Advance** - Type 4-digit year → auto-move to month
4. **Visual Cursor** - `>` indicator for active field
5. **Inline Forms** - Forms appear in context, not overlays

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Move to next field |
| Shift+Tab | Move to previous field |
| Enter | Submit form |
| Escape | Cancel/close form |
| `m` / `f` | Jump to Male/Female in gender selector |
| Arrow keys | Navigate options in selectors |

---

## Password Gate

**Password**: `lombok29`

**Implementation** (`src/components/PasswordGate.svelte`):
- Checks `sessionStorage` for auth status
- Shows password input if not authenticated
- Wraps entire app in `src/routes/+layout.svelte`

---

## Development Commands

```bash
cd /Users/macbookair/GitHub/bazingse
npm install
npm run dev     # Development server (Vite)
npm run build   # Production build
npm run preview # Preview production build
```

---

## CRITICAL: Pattern-Based Thinking

**When given an example, NEVER hardcode for just that one case. Always identify the pattern and apply it universally.**

---

## Default Workflow: Background Agents + Learning Mode

**When given a prompt or task, follow this workflow by default:**

1. **Spin off a background agent** to work on the task asynchronously
2. **Periodically poll the agent** and summarize in **simple, non-technical language**
3. **Use the Explore agent** to explain how things work
4. **If errors occur**: Stop, explain in plain English, guide through fixes

### Why This Workflow?

The user is **non-technical**. This means:
- No jargon without explanation
- Use everyday analogies
- Focus on *what* and *why*, not *how* technically

---

## Design Principles

1. **KISS** - Keep solutions simple
2. **Anti-WIMP** - Keyboard-first, no modals, inline forms
3. **TUI-Style** - Terminal aesthetic, content-first, minimal chrome
4. **Mobile-First** - 99% users on mobile, desktop = mobile + padding
5. **NO HORIZONTAL SCROLLING** - Page must never scroll left/right
6. **TypeScript Strict Mode** - All code typed

---

## TL;DR for AI Agents

1. **SvelteKit + Svelte 5** with runes ($state, $derived, $props, $effect)
2. **tRPC** for type-safe API, REST routes for backward compat
3. **Cloudflare D1** database via Drizzle ORM
4. **Password**: `lombok29` (stored in sessionStorage)
5. **Anti-WIMP** - No modals, inline forms, keyboard-first
6. **BaZi engine** in TypeScript at `src/lib/bazi/`
7. **Pattern-based thinking** - Apply fixes universally
8. **Non-technical user** - Explain in plain language
9. **3 pages**: Home (profiles), Profile detail, Calendar

---

**Last Updated:** 2026-02-28 (SvelteKit + Svelte 5 migration complete)
