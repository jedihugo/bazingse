# CLAUDE.md

Guidance for AI agents working on **BaZingSe** - a full-stack Chinese BaZi (Four Pillars/八字) astrology application.

**Status**: Production-ready API with 8-26 node extensible architecture, Next.js 14 frontend with i18n, TUI-style Anti-WIMP input system, deployed on Vercel.

---

## Project Overview

- **Frontend**: Next.js 14 + React 18 at repo root (NOT in `app/` subfolder)
- **Backend**: Python FastAPI + sxtwl calendar library
- **Deployment**: Vercel (frontend) + separate API hosting
- **i18n**: next-intl with locales: `en`, `id` (default), `zh`
- **Testing**: Playwright E2E test suite
- **UI Paradigm**: TUI-style Anti-WIMP (keyboard-first, no modals)

---

## CRITICAL: Project Structure (Updated 2026-02)

**The Next.js app is at the REPO ROOT, not in a subfolder.**

```
bazingse/
├── middleware.ts              # MUST be at root for Next.js Edge runtime
├── next.config.js             # Next.js config with next-intl plugin
├── package.json               # Frontend dependencies
├── tsconfig.json              # TypeScript config
├── src/                       # Next.js source code
│   ├── app/                   # App Router
│   │   ├── layout.tsx         # Root layout with PasswordGate
│   │   ├── page.tsx           # Root redirect to /id
│   │   ├── globals.css        # Global styles (~53KB)
│   │   └── [locale]/          # i18n routes
│   │       ├── layout.tsx     # Locale provider
│   │       ├── page.tsx       # Home page (profiles list)
│   │       └── profile/[id]/  # Profile pages
│   ├── components/            # React components
│   │   ├── chat-form/         # TUI-style input components (NEW)
│   │   ├── PasswordGate.tsx   # App access protection
│   │   └── ...                # Other components
│   ├── i18n/                  # Internationalization config
│   │   ├── config.ts          # Locales: en, id, zh
│   │   ├── routing.ts         # next-intl routing
│   │   └── request.ts         # Server-side i18n
│   ├── lib/                   # Utilities
│   └── locales/               # Translation files
│       ├── en/
│       ├── id/
│       └── zh/
├── public/                    # Static assets
├── api/                       # Backend - Python FastAPI
│   ├── bazingse.py            # Core interaction engine
│   ├── routes.py              # API endpoints
│   └── ...
├── ios/                       # Capacitor iOS app
└── tests/                     # Playwright tests
```

### CRITICAL: Middleware Location

**Middleware MUST be at project root (`middleware.ts`), NOT in `src/`.**

Next.js requires middleware at the root level when the app is at root. If middleware is in `src/middleware.ts`, it will NOT be recognized and all routes will 404.

```typescript
// middleware.ts (at repo root)
import createMiddleware from 'next-intl/middleware';
import { defineRouting } from 'next-intl/routing';

// Inline routing config to avoid import issues on Vercel Edge
const routing = defineRouting({
  locales: ['en', 'id', 'zh'],
  defaultLocale: 'id',
  localePrefix: 'always',
});

export default createMiddleware(routing);
```

---

## Anti-WIMP Input System (TUI-Style)

**Design Philosophy**: Replace traditional WIMP (Windows, Icons, Menus, Pointer) UI with terminal/chat-style keyboard-first interactions.

### Key Principles

1. **No Modals** - Use inline forms/panels instead
2. **Keyboard-First** - Tab, Enter, Escape for navigation
3. **Auto-Advance** - Type 4-digit year → auto-move to month
4. **Visual Cursor** - `>` indicator for active field
5. **Inline Forms** - Forms appear in context, not overlays

### Chat-Form Components (`src/components/chat-form/`)

| Component | Purpose |
|-----------|---------|
| `ChatFormContext.tsx` | React context for focus management |
| `ChatForm.tsx` | Container with title bar, keyboard shortcuts |
| `ChatFormField.tsx` | Field wrapper with blinking cursor `>` |
| `GuidedDateInput.tsx` | YYYY/MM/DD with auto-advance |
| `GuidedTimeInput.tsx` | HH:MM with unknown toggle |
| `InlineSelector.tsx` | Radio-style keyboard selection `(●)/(○)` |
| `TypeaheadSelect.tsx` | Keyboard-navigable dropdown replacement |

### Auto-Advance Logic

```typescript
// Year: 4 digits → move to month
if (yearValue.length === 4 && isValidYear(yearValue)) {
  monthRef.current?.focus();
}

// Month: 2 digits OR single digit > 1 → move to day
if (monthValue.length === 2 || parseInt(monthValue) > 1) {
  dayRef.current?.focus();
}
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Move to next field |
| Shift+Tab | Move to previous field |
| Enter | Submit form |
| Escape | Cancel/close form |
| `m` / `f` | Jump to Male/Female in gender selector |
| Arrow keys | Navigate options in selectors |

### CSS Cursor Animation

```css
.chat-field-cursor-active {
  color: var(--tui-water);
  animation: cursor-blink 1s step-end infinite;
}

@keyframes cursor-blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```

---

## Password Gate

The app is protected by a simple password gate.

**Password**: `lombok29`

**Implementation** (`src/components/PasswordGate.tsx`):
- Checks `sessionStorage` for auth status
- Shows password input if not authenticated
- Auth persists for browser session (until tab closed)
- Wraps entire app in `src/app/layout.tsx`

---

## Vercel Deployment

### Configuration

No `vercel.json` needed - Next.js at repo root is auto-detected.

### Common Issues & Solutions

**404 on all routes:**
- Middleware not at project root → Move `src/middleware.ts` to `middleware.ts`
- Residual `app/` directory at root → Delete it

**500 MIDDLEWARE_INVOCATION_FAILED:**
- Import issues in middleware → Inline routing config instead of importing

**Build fails "No Next.js version detected":**
- Next.js not at repo root → Move all Next.js files from subfolder to root

### Lessons Learned (2026-02 Deployment)

1. **Never put Next.js in a subfolder for Vercel** - Always at repo root
2. **Middleware must be at root** - Not in `src/` when app is at root
3. **Inline middleware config** - Avoid imports in middleware for Edge compatibility
4. **Clean up residual directories** - Old `app/` folders cause conflicts

---

## Internationalization (i18n)

Using `next-intl` for multi-language support.

### Supported Locales

| Code | Language | Default |
|------|----------|---------|
| `id` | Bahasa Indonesia | ✓ |
| `en` | English | |
| `zh` | 中文 | |

### URL Structure

```
/           → Redirects to /id/
/id/        → Indonesian home
/en/        → English home
/zh/        → Chinese home
/id/profile/123  → Profile page in Indonesian
```

### Adding Translations

1. Add JSON file in `src/locales/{locale}/`
2. Export from `src/locales/{locale}/index.ts`
3. Use in components: `const t = useTranslations('namespace');`

---

## Development Commands

### Frontend (Next.js 14 - Port 4321)
```bash
cd /Users/macbookair/GitHub/bazingse
npm install
npm run dev     # Development server: http://localhost:4321
npm run build   # Production build
npm run start   # Preview production build
```

### Backend (FastAPI - Port 8008)
```bash
cd /Users/macbookair/GitHub/bazingse/api
source .venv/bin/activate
pip install -r requirements.txt
python run_bazingse.py  # http://localhost:8008
```

### Kill Port Conflicts
```bash
lsof -ti:4321 | xargs kill -9  # Kill frontend port
lsof -ti:8008 | xargs kill -9  # Kill backend port
```

---

## CRITICAL: Pattern-Based Thinking

**When given an example, NEVER hardcode for just that one case. Always identify the pattern and apply it universally.**

### Key Questions to Ask:
1. **"Is this a single instance or a pattern?"** (Usually a pattern!)
2. **"Where else does this pattern occur?"** (Search with grep/Glob)
3. **"What's the root cause?"** (Fix the source, not symptoms)
4. **"Are there similar cases?"** (Apply fix universally)

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

## CRITICAL: API is the Single Source of Truth

**ALL BaZi calculations and display metadata MUST live in the Python API backend.**

**Frontend responsibilities (ONLY):**
- Collect user inputs
- Call backend APIs
- Display returned data using API-provided styling
- Handle UI interactions

**Frontend must NEVER:**
- Calculate elements, stems, branches, or Ten Gods
- Hardcode hex colors or styling
- Create mock/fallback data

---

## Design Principles

1. **Backend is Source of Truth** - Never calculate BaZi logic in frontend
2. **KISS** - Keep solutions simple (middle-schooler friendly)
3. **Anti-WIMP** - Keyboard-first, no modals, inline forms
4. **TUI-Style** - Terminal aesthetic, content-first, minimal chrome
5. **Mobile-First** - 99% users on mobile, desktop = mobile + padding
6. **NO HORIZONTAL SCROLLING** - Page must never scroll left/right
7. **i18n Ready** - All user-facing strings in locale files
8. **TypeScript Strict Mode** - All frontend code typed

---

## Component Architecture

### Core Components (`src/components/`)

| Component | Purpose |
|-----------|---------|
| `PasswordGate.tsx` | App access protection |
| `Header.tsx` | Logo + title + locale switcher |
| `BaZiApp.tsx` | Main debug page orchestrator |
| `BaZiChart.tsx` | Pillar cards renderer |
| `PillarCard.tsx` | Individual pillar display |
| `ProfilePage.tsx` | Profile view with life events |
| `InlineProfileForm.tsx` | Create profile (inline, no modal) |
| `InlineLifeEventForm.tsx` | Add life event (inline, no modal) |

### Input Components (`src/components/chat-form/`)

| Component | Purpose |
|-----------|---------|
| `GuidedDateInput.tsx` | YYYY/MM/DD with auto-advance |
| `GuidedTimeInput.tsx` | HH:MM with unknown toggle |
| `InlineSelector.tsx` | Radio-style `(●)/(○)` selection |
| `TypeaheadSelect.tsx` | Searchable keyboard dropdown |

---

## TL;DR for AI Agents

1. **Next.js is at REPO ROOT** - Not in `app/` subfolder
2. **Middleware at root** - `middleware.ts`, NOT `src/middleware.ts`
3. **Password**: `lombok29` (stored in sessionStorage)
4. **Anti-WIMP** - No modals, inline forms, keyboard-first
5. **i18n locales**: `en`, `id` (default), `zh`
6. **Port 4321** for frontend, **Port 8008** for backend
7. **Vercel auto-deploys** - No config needed if Next.js at root
8. **Backend is Source of Truth** - No BaZi logic in frontend
9. **Pattern-based thinking** - Apply fixes universally, not just to examples
10. **Non-technical user** - Explain in plain language, no jargon

---

**Last Updated:** 2026-02-03 (Anti-WIMP input system, Vercel deployment, project restructure)
