# Python-to-TypeScript Migration Design

**Date:** 2026-02-22
**Status:** Approved
**Goal:** Eliminate Python/FastAPI backend entirely. Single Next.js app on Vercel.

## Architecture

```
bazingse/
├── src/
│   ├── app/api/                  Next.js API routes (replaces FastAPI)
│   │   ├── analyze-bazi/route.ts
│   │   ├── dong-gong/route.ts
│   │   ├── profiles/route.ts
│   │   └── profiles/[id]/
│   │       ├── route.ts
│   │       └── life-events/route.ts
│   ├── lib/
│   │   ├── bazi/                  BaZi engine (replaces api/library/)
│   │   │   ├── core.ts           STEMS + BRANCHES
│   │   │   ├── derived.ts        computed lookups
│   │   │   ├── chart.ts          pillar calc (lunar-typescript)
│   │   │   ├── combinations.ts
│   │   │   ├── conflicts.ts
│   │   │   ├── scoring.ts
│   │   │   ├── dynamic-scoring.ts
│   │   │   ├── seasonal.ts
│   │   │   ├── qi-phase.ts
│   │   │   ├── unity.ts
│   │   │   ├── physics.ts
│   │   │   ├── distance.ts
│   │   │   ├── wealth-storage.ts
│   │   │   ├── dong-gong.ts
│   │   │   ├── comprehensive/    engine, adapter, strength, interactions,
│   │   │   │                     ten-gods, shen-sha, predictions,
│   │   │   │                     environment, qi-phase-analysis,
│   │   │   │                     spiritual-sensitivity, report, templates
│   │   │   ├── narrative/        interpreter, templates, modifiers,
│   │   │   │                     chain-engine, localization, priority,
│   │   │   │                     remedies, qi-phase
│   │   │   ├── life-aspects/     base, health, wealth, learning,
│   │   │   │                     ten-gods-detail
│   │   │   └── pattern-engine/   pattern-spec, registry, integration,
│   │   │                         patterns/*, life-events/*
│   │   ├── db.ts                 Vercel KV wrapper
│   │   └── api.ts                updated: relative URLs
│   └── components/               unchanged
```

## Key Decisions

1. **lunar-typescript** replaces sxtwl — verified accurate to the minute for solar terms
2. **Vercel KV** replaces Railway SQLite — sub-ms reads, built into Vercel, free tier
3. **Next.js API routes** replace FastAPI — same endpoints, same JSON response shape
4. **`server-only`** guard on all bazi/ modules — prevents client bundle bloat
5. **Golden file tests** — capture Python API output before porting, verify TS matches
6. **Drop bazingse.py** — 4,857 lines of legacy code, replaced by comprehensive engine
7. **Frontend unchanged** — same components, same API contract

## Storage: Vercel KV

- Key pattern: `profile:{uuid}` → full profile JSON with life events
- Key pattern: `profiles:index` → lightweight list for home page pagination
- ~2000 profiles, ~2KB each = ~4MB total (well within 256MB free tier)
- Read-heavy (100:1 ratio), sub-millisecond reads

## What Gets Deleted (~5,600 lines)

- `api/bazingse.py` (legacy engine, replaced by comprehensive/)
- `api/models.py`, `api/database.py` (SQLAlchemy ORM)
- `api/index.py`, `api/run_bazingse.py` (Python server entry points)
- `api/test_analyze_bazi.py` (Python tests)

## Migration Verification

Before port: capture golden files from Python API for all seed profiles.
After port: verify TypeScript API produces identical JSON responses.
Key edge cases: Li Chun boundary, 23:00 day crossover, solar term month transitions.
