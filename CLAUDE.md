# CLAUDE.md

Guidance for AI agents working on **BaZingSe** - a full-stack Chinese BaZi (Four Pillars/八字) astrology application.

**Status**: Production-ready API with comprehensive analysis engine, Next.js 14 frontend with i18n, TUI-style Anti-WIMP input system, deployed on Vercel + Railway.

---

## Project Overview

- **Frontend**: Next.js 14 + React 18 at repo root (NOT in `app/` subfolder)
- **Backend**: Python FastAPI + sxtwl calendar library
- **Deployment**: Vercel (frontend) + Railway (backend + SQLite DB)
- **i18n**: next-intl with locales: `en`, `id` (default), `zh`
- **Testing**: Playwright E2E test suite
- **UI Paradigm**: TUI-style Anti-WIMP (keyboard-first, no modals)

---

## CRITICAL: Project Structure (Updated 2026-02-17)

**The Next.js app is at the REPO ROOT, not in a subfolder.**

```
bazingse/
├── middleware.ts              # MUST be at root for Next.js Edge runtime
├── next.config.js             # Next.js config with next-intl plugin
├── package.json               # Frontend dependencies
├── tsconfig.json              # TypeScript config
├── src/                       # Next.js source code
│   ├── app/                   # App Router (3 pages)
│   │   ├── layout.tsx         # Root layout with PasswordGate + Analytics
│   │   ├── page.tsx           # Home page (profiles list)
│   │   ├── globals.css        # Global styles (~53KB)
│   │   ├── profile/[id]/      # Profile detail page
│   │   │   └── page.tsx
│   │   └── calendar/          # Dong Gong calendar page
│   │       └── page.tsx
│   ├── components/            # React components
│   │   ├── chat-form/         # TUI-style input components
│   │   └── *.tsx              # Page-level and display components
│   ├── i18n/                  # Internationalization config
│   ├── lib/                   # Utilities (api.ts)
│   └── locales/               # Translation files (en/, id/, zh/)
├── public/                    # Static assets
├── api/                       # Backend - Python FastAPI
│   ├── bazingse.py            # Core interaction engine (~5300 lines)
│   ├── routes.py              # API endpoints
│   ├── chart_constructor.py   # Chart generation
│   ├── library/               # All BaZi logic modules
│   │   ├── core.py            # STEMS + BRANCHES (single source of truth)
│   │   ├── comprehensive/     # New comprehensive analysis engine
│   │   ├── narrative/         # Narrative generation
│   │   ├── life_aspects/      # Health, wealth, learning analysis
│   │   ├── pattern_engine/    # Universal pattern detection
│   │   └── *.py               # Scoring, physics, qi_phase, etc.
│   ├── crud.py / models.py / schemas.py / database.py  # DB layer
│   └── run_bazingse.py        # Local dev server
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

## Frontend Pages & Component Tree

### 3 Pages (App Router)

| Route | Page File | Key Components |
|-------|-----------|----------------|
| `/` | `src/app/page.tsx` | Header, InlineProfileForm, SearchableProfileList |
| `/profile/[id]` | `src/app/profile/[id]/page.tsx` | Header, ProfilePage |
| `/calendar` | `src/app/calendar/page.tsx` | Header, DongGongCalendar |

### Core Components (`src/components/`)

| Component | Purpose |
|-----------|---------|
| `PasswordGate.tsx` | App access protection |
| `Header.tsx` | Logo + title + ThemeToggle |
| `ProfilePage.tsx` | Profile view orchestrator (info, life events, chart) |
| `ProfileInfoBlock.tsx` | Editable profile info display |
| `LifeEventBlock.tsx` | Life event display with BaZi chart + analysis |
| `BaZiChart.tsx` | Pillar cards renderer |
| `PillarCard.tsx` | Individual pillar display |
| `PillarTag.tsx` | Compact pillar label |
| `ElementAnalysis.tsx` | Element score breakdown |
| `NarrativeDisplay.tsx` | Narrative cards container |
| `NarrativeCard.tsx` | Individual narrative card |
| `ClientSummaryDisplay.tsx` | Client-facing summary with diffs |
| `DongGongCalendar.tsx` | Dong Gong date selection calendar |
| `InlineProfileForm.tsx` | Create profile (inline, no modal) |
| `InlineLifeEventForm.tsx` | Add life event (inline, no modal) |
| `SearchableProfileList.tsx` | Filterable profile list on home page |
| `ThemeToggle.tsx` | Dark/light mode toggle |
| `LocaleProvider.tsx` | i18n context wrapper |

### Input Components (`src/components/chat-form/`)

| Component | Purpose |
|-----------|---------|
| `ChatFormContext.tsx` | React context for focus management |
| `ChatForm.tsx` | Container with title bar, keyboard shortcuts |
| `ChatFormField.tsx` | Field wrapper with blinking cursor `>` |
| `GuidedDateInput.tsx` | YYYY/MM/DD with auto-advance |
| `GuidedTimeInput.tsx` | HH:MM with unknown toggle |
| `InlineSelector.tsx` | Radio-style keyboard selection `(●)/(○)` |
| `TypeaheadSelect.tsx` | Keyboard-navigable dropdown replacement |

---

## Backend Architecture

### Core Engine

- `api/bazingse.py` (~5300 lines) — Monolithic with inner functions (closures over `nodes` dict)
- All BaZi logic lives in `api/library/` modules; `bazingse.py` uses `from library import *`

### Library Modules (`api/library/`)

| Module | Purpose |
|--------|---------|
| `core.py` | STEMS + BRANCHES — single source of truth |
| `derived.py` | All computed data from core |
| `combinations.py` | Positive: Three Meetings, Six Harmonies, etc. |
| `conflicts.py` | Negative: Punishments, Harms, Clashes, etc. |
| `scoring.py` / `dynamic_scoring.py` | Element scoring systems |
| `seasonal.py` | Seasonal strength configs |
| `qi_phase.py` | Twelve Life Stages (十二长生) |
| `physics.py` | Physics school (Yin/Yang polarity modifier) |
| `wealth_storage.py` | Wealth storage (財庫) analysis |
| `dong_gong.py` | Dong Gong date selection system |
| `distance.py` | Node distance calculations |
| `unity.py` | Wu Xing combat engine |
| `unit_tracker.py` | Unit story tracker |
| `comprehensive/` | New comprehensive analysis engine (zero-LLM) |
| `narrative/` | Narrative generation (templates, chains, localization) |
| `life_aspects/` | Health, wealth, learning, ten gods detail |
| `pattern_engine/` | Universal pattern detection + life events |

### API Endpoints (`api/routes.py`)

```
GET  /health                              # Health check
GET  /api/analyze_bazi?...                # BaZi chart analysis (main)
GET  /api/comprehensive_analysis?...      # Comprehensive report (zero-LLM, markdown)
GET  /api/dong_gong_calendar?...          # Dong Gong date selection
POST /api/seed                            # Seed database (if empty)
GET  /api/profiles                        # List all profiles
POST /api/profiles                        # Create profile
GET  /api/profiles/{id}                   # Get profile
PUT  /api/profiles/{id}                   # Update profile
DELETE /api/profiles/{id}                 # Delete profile
POST /api/profiles/{id}/life_events       # Add life event
GET  /api/profiles/{id}/life_events/{eid} # Get life event
PUT  /api/profiles/{id}/life_events/{eid} # Update life event
DELETE /api/profiles/{id}/life_events/{eid} # Delete life event
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

The app is protected by a simple password gate.

**Password**: `lombok29`

**Implementation** (`src/components/PasswordGate.tsx`):
- Checks `sessionStorage` for auth status
- Shows password input if not authenticated
- Auth persists for browser session (until tab closed)
- Wraps entire app in `src/app/layout.tsx`

---

## Production Infrastructure

### Frontend: Vercel
- **URL**: https://bazingse.vercel.app
- Auto-deploys from `main` branch
- Vercel Web Analytics enabled
- No `vercel.json` needed - Next.js at repo root is auto-detected

### Backend: Railway
- **URL**: https://bazingse-production.up.railway.app
- Python FastAPI with sxtwl calendar library
- Auto-deploys from `main` branch (watches `api/` directory)

### Database: Railway SQLite (SOURCE OF TRUTH)
- **Location**: `/data/bazingse.db` on Railway persistent volume
- **NO local database** - Railway is the single source of truth
- Seed endpoint: `POST /api/seed` (only works if DB is empty)

---

## Internationalization (i18n)

Using `next-intl` for multi-language support.

| Code | Language | Default |
|------|----------|---------|
| `id` | Bahasa Indonesia | yes |
| `en` | English | |
| `zh` | 中文 | |

### URL Structure

```
/               → Home (profiles list)
/profile/123    → Profile page
/calendar       → Dong Gong calendar
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

## TL;DR for AI Agents

1. **Next.js is at REPO ROOT** - Not in `app/` subfolder
2. **Middleware at root** - `middleware.ts`, NOT `src/middleware.ts`
3. **Password**: `lombok29` (stored in sessionStorage)
4. **Anti-WIMP** - No modals, inline forms, keyboard-first
5. **i18n locales**: `en`, `id` (default), `zh`
6. **Port 4321** for frontend, **Port 8008** for backend
7. **Vercel** for frontend, **Railway** for backend + database
8. **Railway SQLite is SOURCE OF TRUTH** - No local database, always refer to Railway
9. **Backend is Source of Truth** - No BaZi logic in frontend
10. **Pattern-based thinking** - Apply fixes universally, not just to examples
11. **Non-technical user** - Explain in plain language, no jargon
12. **3 pages**: Home (profiles), Profile detail, Calendar

---

**Last Updated:** 2026-02-17 (Comprehensive engine, calendar, wealth storage, client summary, cleanup)
