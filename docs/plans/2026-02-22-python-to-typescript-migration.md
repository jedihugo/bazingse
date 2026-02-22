# Python-to-TypeScript Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Eliminate the entire Python/FastAPI backend, migrating all BaZi logic to TypeScript so the app runs as a single Next.js application on Vercel.

**Architecture:** All BaZi engine code moves to `src/lib/bazi/` (server-only). Profile data moves from Railway SQLite to Vercel KV. Next.js API routes at `src/app/api/` replace FastAPI endpoints. Frontend components stay unchanged — API response shape is identical.

**Tech Stack:** Next.js 14, TypeScript, lunar-typescript (replaces sxtwl), Vercel KV (@vercel/kv), server-only npm package.

**Key files to reference during migration:**
- Python core data: `api/library/core.py` (STEMS + BRANCHES)
- Python derived: `api/library/derived.py` (computed lookups)
- Python chart calc: `api/chart_constructor.py` (sxtwl → pillar generation)
- Python routes: `api/routes.py` (all API endpoints + response shapes)
- Python CRUD: `api/crud.py` (profile/life event operations)
- Python schemas: `api/schemas.py` (request/response validation)
- Python comprehensive engine: `api/library/comprehensive/` (the active engine)
- Frontend API client: `src/lib/api.ts` (TypeScript interfaces + fetch calls)
- Existing TS test: `tests/pillar_test_lunar_ts.ts` (proven lunar-typescript usage)

---

## Phase 0: Golden File Test Suite

Capture current Python API output as ground truth. Every subsequent phase validates against these.

### Task 0.1: Generate golden files from Python API

**Files:**
- Create: `tests/golden/generate_golden.py`
- Create: `tests/golden/*.json` (output files)

**Steps:**

1. Write a Python script that calls the running Python API (localhost:8008) with a comprehensive set of test inputs:
   - 10+ profiles with different birth dates/times/genders
   - Each profile analyzed at multiple years (natal only, with luck pillar, with monthly, with daily)
   - 2+ months of Dong Gong calendar data
   - Edge cases: unknown birth time, Li Chun boundary dates, 23:00 births
2. Save each API response as a JSON golden file
3. Run it: `source api/.venv/bin/activate && python3 api/run_bazingse.py &` then `python3 tests/golden/generate_golden.py`
4. Verify golden files are generated and non-empty
5. Commit: `git add tests/golden/ && git commit -m "test: add golden files from Python API for migration verification"`

**Test inputs must include at minimum:**
```
Natal only:     1990-01-15 10:30 male
With luck:      1990-01-15 10:30 male, analysis_year=2026
Monthly:        1990-01-15 10:30 male, analysis_year=2026, analysis_month=6
Daily:          1990-01-15 10:30 male, analysis_year=2026, analysis_month=6, analysis_day=15
Unknown time:   1985-12-25 unknown female
Li Chun edge:   2024-02-04 03:00 male (before Li Chun)
Li Chun edge:   2024-02-04 17:00 female (after Li Chun)
23:00 birth:    1995-08-10 23:30 male
Physics school: 1990-01-15 10:30 male, school=physics
Dong Gong:      year=2026, month=2
Dong Gong:      year=2026, month=6
```

---

## Phase 1: Foundation — Core Data + Chart Calculator

Port the fundamental BaZi data and pillar calculation. This is the foundation everything else depends on.

### Task 1.1: Install dependencies

**Steps:**
1. `npm install server-only @vercel/kv`
2. `lunar-typescript` is already installed (verified in package.json)
3. Commit: `git add package.json package-lock.json && git commit -m "deps: add server-only and @vercel/kv"`

### Task 1.2: Port core.ts (STEMS + BRANCHES)

**Files:**
- Create: `src/lib/bazi/core.ts`
- Reference: `api/library/core.py` (385 lines)

**Steps:**
1. Create `src/lib/bazi/core.ts` with `import 'server-only'` at top
2. Convert Python STEMS dict → TypeScript `STEMS` const with full type interface
3. Convert Python BRANCHES dict → TypeScript `BRANCHES` const with full type interface
4. Key type differences:
   - Python tuples `("F", "Friend", "比肩")` → TS tuples `["F", "Friend", "比肩"] as const`
   - Python `None` → TS `null`
   - Python `True/False` → TS `true/false`
   - Ten gods map stays the same shape: `Record<string, readonly [string, string, string]>`
5. Verify: `npx tsc --noEmit` passes
6. Commit

### Task 1.3: Port derived.ts (computed lookups)

**Files:**
- Create: `src/lib/bazi/derived.ts`
- Reference: `api/library/derived.py` (367 lines)

**Steps:**
1. Port all computed data: ELEMENTS, ELEMENT_CYCLES, STEM_ORDER, BRANCH_ORDER
2. Port lookup arrays: STEM_CHINESE, BRANCH_CHINESE, STEM_CHINESE_TO_PINYIN, BRANCH_CHINESE_TO_PINYIN
3. Port utility functions: `getStem()`, `getBranch()`, `getPrimaryQi()`, `getHiddenStems()`, `getAllBranchQi()`, `getTenGod()`
4. Port backward-compat aliases: `Gan`, `Zhi`, `GAN_MAP`, `ZHI_MAP`
5. Port DAY_OFFICERS, QI_PHASE_TABLE (十二長生), NAYIN table
6. Verify: `npx tsc --noEmit`
7. Commit

### Task 1.4: Port chart.ts (pillar calculator using lunar-typescript)

**Files:**
- Create: `src/lib/bazi/chart.ts`
- Reference: `api/chart_constructor.py` (306 lines)
- Reference: `tests/pillar_test_lunar_ts.ts` (proven lunar-typescript usage)

**Steps:**
1. Port `generateBaziChart()` — use `Solar.fromYmdHms()` + `EightChar` from lunar-typescript
   - lunar-typescript handles year/month pillar solar term transitions automatically (verified)
   - Still need manual 23:00 day boundary handling for day pillar
   - Parse Chinese characters from `EightChar.getYear/Month/Day/Time()` → pinyin using STEM_MAP/BRANCH_MAP
2. Port `generateLuckPillars()` — use lunar-typescript's `Lunar.getNextJie()` for finding next major Jieqi
   - `getNextJie().getSolar()` gives exact date (no day-walking loop needed!)
   - Calculate days difference, divide by 3, ceiling = start age
3. Port `generateXiaoYunPillars()` — pure arithmetic on 60-pillar cycle (no sxtwl/lunar-ts needed)
4. Port SIXTY_PILLARS constant (used by luck pillar generation)
5. Write comparison test: run both Python and TS chart generation for golden file inputs, assert identical pillar strings
6. Commit

### Task 1.5: Validate Phase 1 against golden files

**Files:**
- Create: `tests/validate_chart.ts`

**Steps:**
1. Write test that loads golden files, extracts the birth_info/pillar data, runs TS `generateBaziChart()` with same inputs
2. Assert year/month/day/hour pillars match exactly
3. Run: `npx tsx tests/validate_chart.ts`
4. Fix any discrepancies
5. Commit

---

## Phase 2: Data Layer — Vercel KV + Profile API Routes

### Task 2.1: Create Vercel KV wrapper (db.ts)

**Files:**
- Create: `src/lib/db.ts`
- Reference: `api/crud.py` (165 lines)

**Steps:**
1. Create `src/lib/db.ts` with Vercel KV operations:
   - `getProfiles(skip, limit)` — read `profiles:index` key, slice for pagination
   - `getProfile(id)` — read `profile:{id}` key
   - `createProfile(data)` — generate UUID, write `profile:{id}`, update `profiles:index`
   - `updateProfile(id, data)` — read-modify-write `profile:{id}`, update index
   - `deleteProfile(id)` — delete `profile:{id}`, update index
   - Life event CRUD: read-modify-write on the profile's `life_events` array
2. For local development: use `@vercel/kv` with `KV_REST_API_URL` and `KV_REST_API_TOKEN` env vars (Vercel provides these automatically in production)
3. Verify: `npx tsc --noEmit`
4. Commit

### Task 2.2: Create Profile API routes

**Files:**
- Create: `src/app/api/profiles/route.ts` (GET list + POST create)
- Create: `src/app/api/profiles/[id]/route.ts` (GET + PUT + DELETE)
- Create: `src/app/api/profiles/[id]/life-events/route.ts` (POST)
- Create: `src/app/api/profiles/[id]/life-events/[eid]/route.ts` (GET + PUT + DELETE)
- Reference: `api/routes.py:725-993` (profile endpoints)
- Reference: `api/schemas.py` (validation schemas)

**Steps:**
1. Create route handlers matching existing FastAPI endpoints exactly
2. Use Next.js `NextRequest` / `NextResponse`
3. Request validation: check required fields, return 422 with `detail` message on validation errors (matching FastAPI format)
4. Response format must be IDENTICAL to current Python API (same field names, same JSON structure)
5. Key: `life_events` path uses underscore (matching current API contract: `/api/profiles/{id}/life_events`)
6. Verify: `npx tsc --noEmit`
7. Commit

### Task 2.3: Create seed endpoint + data migration script

**Files:**
- Create: `src/app/api/seed/route.ts`
- Create: `scripts/migrate-from-railway.ts`

**Steps:**
1. Create seed route that populates KV with test profiles (matching existing seed data)
2. Create migration script that reads all profiles from Railway API and writes them to Vercel KV
3. Script: `for each profile from GET /api/profiles?limit=10000 → kv.set(profile:{id}, profile) + build index`
4. Commit

---

## Phase 3: BaZi Engine Modules

Convert all `api/library/` modules to TypeScript. These are mostly data tables and pure functions — mechanical conversion. Port in dependency order.

### Task 3.1: Port data table modules (low logic, high data)

**Files to create (one commit per file):**
- `src/lib/bazi/combinations.ts` ← `api/library/combinations.py` (241 lines)
- `src/lib/bazi/conflicts.ts` ← `api/library/conflicts.py` (309 lines)
- `src/lib/bazi/scoring.ts` ← `api/library/scoring.py` (143 lines)
- `src/lib/bazi/seasonal.ts` ← `api/library/seasonal.py` (29 lines)
- `src/lib/bazi/qi-phase.ts` ← `api/library/qi_phase.py` (210 lines)
- `src/lib/bazi/physics.ts` ← `api/library/physics.py` (19 lines)
- `src/lib/bazi/distance.ts` ← `api/library/distance.py` (136 lines)
- `src/lib/bazi/wealth-storage.ts` ← `api/library/wealth_storage.py` (136 lines)

**Conversion rules:**
- Python dict → TypeScript `Record<string, ...>` or typed const
- Python list → TypeScript `readonly` array
- Python tuple → TypeScript `readonly` tuple with `as const`
- Every file starts with `import 'server-only'`
- Verify each: `npx tsc --noEmit`

### Task 3.2: Port logic modules

**Files to create:**
- `src/lib/bazi/dynamic-scoring.ts` ← `api/library/dynamic_scoring.py` (549 lines)
- `src/lib/bazi/unity.ts` ← `api/library/unity.py` (295 lines)
- `src/lib/bazi/dong-gong.ts` ← `api/library/dong_gong.py` (2,359 lines)

**Notes:**
- `dong-gong.ts` is the largest — mostly the DONG_GONG 12×12 matrix data table. Mechanical conversion.
- `unity.ts` has Wu Xing combat logic — ensure element interaction arithmetic is identical.
- `dynamic-scoring.ts` has narrative text strings — keep them identical.

### Task 3.3: Port comprehensive engine

**Files to create (in dependency order):**
1. `src/lib/bazi/comprehensive/models.ts` ← `models.py` (182 lines) — dataclasses → TS interfaces
2. `src/lib/bazi/comprehensive/strength.ts` ← `strength.py` (590 lines) — DM strength
3. `src/lib/bazi/comprehensive/interactions.ts` ← `interactions.py` (516 lines) — branch detection
4. `src/lib/bazi/comprehensive/ten-gods.ts` ← `ten_gods.py` (390 lines) — ten god mapping
5. `src/lib/bazi/comprehensive/shen-sha.ts` ← `shen_sha.py` (1,513 lines) — 30+ star checks
6. `src/lib/bazi/comprehensive/predictions.ts` ← `predictions.py` (435 lines) — life predictions
7. `src/lib/bazi/comprehensive/environment.ts` ← `environment.py` (261 lines) — qi assessment
8. `src/lib/bazi/comprehensive/qi-phase-analysis.ts` ← `qi_phase_analysis.py` (193 lines)
9. `src/lib/bazi/comprehensive/spiritual-sensitivity.ts` ← `spiritual_sensitivity.py` (333 lines)
10. `src/lib/bazi/comprehensive/templates.ts` ← `templates.py` (660 lines) — text templates
11. `src/lib/bazi/comprehensive/report.ts` ← `report.py` (765 lines) — markdown report
12. `src/lib/bazi/comprehensive/engine.ts` ← `engine.py` (223 lines) — main entry point
13. `src/lib/bazi/comprehensive/adapter.ts` ← `adapter.py` (2,412 lines) — JSON shaping for frontend

**Critical: adapter.ts must produce the EXACT same JSON shape as the Python adapter.**
Cross-reference `src/lib/api.ts` TypeScript interfaces — these define the frontend contract.

### Task 3.4: Port narrative system

**Files to create:**
- `src/lib/bazi/narrative/templates.ts` ← (873 lines) — template strings
- `src/lib/bazi/narrative/interpreter.ts` ← (1,487 lines) — narrative generation
- `src/lib/bazi/narrative/modifiers.ts` ← (610 lines) — element/shen sha modifiers
- `src/lib/bazi/narrative/chain-engine.ts` ← (736 lines) — multi-step stories
- `src/lib/bazi/narrative/localization.ts` ← (321 lines) — locale strings
- `src/lib/bazi/narrative/priority.ts` ← (258 lines) — priority scoring
- `src/lib/bazi/narrative/remedies.ts` ← (492 lines) — remedy generation
- `src/lib/bazi/narrative/qi-phase.ts` ← (371 lines) — qi phase narratives

### Task 3.5: Port life aspects

**Files to create:**
- `src/lib/bazi/life-aspects/base.ts` ← (627 lines) — shared utilities
- `src/lib/bazi/life-aspects/health.ts` ← (512 lines) — TCM health analysis
- `src/lib/bazi/life-aspects/wealth.ts` ← (433 lines) — wealth analysis
- `src/lib/bazi/life-aspects/learning.ts` ← (364 lines) — education analysis
- `src/lib/bazi/life-aspects/ten-gods-detail.ts` ← (711 lines) — detailed interpretations

### Task 3.6: Port pattern engine

**Files to create:**
- `src/lib/bazi/pattern-engine/pattern-spec.ts` ← (550 lines)
- `src/lib/bazi/pattern-engine/pattern-registry.ts` ← (580 lines)
- `src/lib/bazi/pattern-engine/integration.ts` ← (769 lines)
- `src/lib/bazi/pattern-engine/patterns/branch-combinations.ts` ← (921 lines)
- `src/lib/bazi/pattern-engine/patterns/branch-conflicts.ts` ← (924 lines)
- `src/lib/bazi/pattern-engine/patterns/stem-patterns.ts` ← (696 lines)
- `src/lib/bazi/pattern-engine/patterns/special-stars.ts` ← (840 lines)
- `src/lib/bazi/pattern-engine/life-events/taxonomy.ts` ← (903 lines)
- `src/lib/bazi/pattern-engine/life-events/severity.ts` ← (437 lines)

### Task 3.7: Create barrel exports

**Files:**
- Create: `src/lib/bazi/index.ts` — re-exports everything (like Python `library/__init__.py`)
- Create: `src/lib/bazi/comprehensive/index.ts`
- Create: `src/lib/bazi/narrative/index.ts`
- Create: `src/lib/bazi/life-aspects/index.ts`
- Create: `src/lib/bazi/pattern-engine/index.ts`

**Steps:**
1. Create index files that re-export public API from each module
2. Verify full project compiles: `npx tsc --noEmit`
3. Commit

---

## Phase 4: API Routes — BaZi Analysis + Calendar

### Task 4.1: Create analyze-bazi route

**Files:**
- Create: `src/app/api/analyze-bazi/route.ts`
- Reference: `api/routes.py:168-700` (the analyze_bazi endpoint)

**Steps:**
1. Port the entire analyze_bazi endpoint logic:
   - Parse query params (birth_date, birth_time, gender, analysis_year, etc.)
   - Generate natal chart via `generateBaziChart()`
   - Generate luck pillars via `generateLuckPillars()` + `generateXiaoYunPillars()`
   - Build chart_dict with natal + luck + time period pillars
   - Run comprehensive engine: `buildChart()` → `analyzeForApi()`
   - Adapt to frontend format: `adaptToFrontend()`
   - Check Four Extinction/Separation (port `check_four_extinction_separation()`)
2. URL mapping: `/api/analyze_bazi` → `/api/analyze-bazi` (update frontend api.ts)
   - OR keep `/api/analyze_bazi` for backward compatibility using route file at `src/app/api/analyze_bazi/route.ts`
3. Response must match golden files exactly
4. Commit

### Task 4.2: Create dong-gong calendar route

**Files:**
- Create: `src/app/api/dong-gong/route.ts`
- Reference: `api/routes.py:750-950` (dong_gong_calendar endpoint)

**Steps:**
1. Port dong_gong_calendar endpoint:
   - For each day in month: get pillar via lunar-typescript, look up Dong Gong officer + rating
   - Moon phase from `Lunar.getLunarDay()`
   - Four Extinction/Separation checks
   - Chinese month/year spans
2. URL mapping: `/api/dong_gong_calendar` → keep same path
3. Response must match golden files exactly
4. Commit

### Task 4.3: Create health check route

**Files:**
- Create: `src/app/api/health/route.ts`

**Steps:**
1. Simple GET that returns `{ "status": "ok" }`
2. Commit

---

## Phase 5: Frontend Updates

### Task 5.1: Update api.ts for local API routes

**Files:**
- Modify: `src/lib/api.ts`

**Steps:**
1. Change `API_BASE_URL` logic:
   - In production: empty string (same-origin, API routes are on same Vercel deployment)
   - In development: empty string (Next.js dev server serves both pages and API routes)
   - Remove Railway URL entirely
   - Keep Capacitor detection for native app (point to Vercel URL)
2. Update endpoint paths if any changed (e.g., `analyze_bazi` → `analyze-bazi`)
3. Verify: `npm run build` succeeds
4. Commit

### Task 5.2: Add Vercel KV environment variables

**Files:**
- Modify: `.env.local` (for local dev)

**Steps:**
1. Create Vercel KV store from Vercel dashboard
2. Copy `KV_REST_API_URL` and `KV_REST_API_TOKEN` to `.env.local`
3. Add to `.gitignore` if not already there
4. Commit (only .gitignore changes, NOT .env.local)

---

## Phase 6: Verification + Cleanup

### Task 6.1: Full golden file validation

**Files:**
- Create: `tests/validate_full.ts`

**Steps:**
1. Start Next.js dev server: `npm run dev`
2. Run every golden file test case against the NEW TypeScript API routes
3. Compare JSON responses field-by-field against golden files
4. Track and fix any discrepancies
5. Commit test

### Task 6.2: Build verification

**Steps:**
1. Run: `npx tsc --noEmit` — must pass with zero errors
2. Run: `npm run build` — must pass (no build errors)
3. Manually test in browser: create profile, view chart, check calendar
4. Verify password gate still works

### Task 6.3: Migrate data from Railway to Vercel KV

**Steps:**
1. Ensure Railway API is still running
2. Run migration script: `npx tsx scripts/migrate-from-railway.ts`
3. Verify profile count matches
4. Spot-check 5 profiles in the new system

### Task 6.4: Deploy to Vercel

**Steps:**
1. Push to main branch
2. Verify Vercel deployment succeeds
3. Test production URL: profiles load, chart analysis works, calendar works
4. Verify no CORS issues (all same-origin now)

### Task 6.5: Delete Python backend

**Files to delete:**
- `api/` directory (entire thing)
- `requirements.txt` if at root
- Any Python-related config

**Steps:**
1. Remove entire `api/` directory
2. Clean up any Python references in config files
3. Update CLAUDE.md — remove all Python/FastAPI/Railway references
4. Commit: `git commit -m "chore: remove Python backend — fully migrated to TypeScript"`

### Task 6.6: Shut down Railway

**Steps:**
1. Verify production is stable on Vercel-only for 24+ hours
2. Shut down Railway service
3. Cancel Railway billing

---

## Migration Statistics

| Metric | Value |
|--------|-------|
| Python files to port | ~45 |
| Python lines to port | ~30,000 |
| Python lines to delete (legacy) | ~5,600 |
| New TypeScript files | ~50 |
| Frontend files changed | 1 (api.ts) |
| Dependencies added | 2 (server-only, @vercel/kv) |
| Dependencies removed | 0 (lunar-typescript already installed) |
| Services eliminated | Railway (backend + database) |
| Services remaining | Vercel (everything) |

---

## Risk Mitigation

1. **Golden files are the safety net.** Every phase validates against them.
2. **Keep Railway running** until Phase 6.4 is verified in production.
3. **`server-only` import** prevents BaZi engine from leaking into client bundle.
4. **Same API response shape** means frontend components need zero changes.
5. **lunar-typescript accuracy** already verified to the minute (tests in `tests/solar_term_times.ts`).
