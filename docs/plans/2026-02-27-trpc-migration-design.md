# tRPC Migration + MCP Server Design

**Date:** 2026-02-27
**Status:** Implementing

## Goal

Add end-to-end type safety between Next.js frontend and API layer using tRPC. Create an MCP server that reuses the tRPC router types.

## Architecture

### Current Flow
```
Component → api.ts (fetch) → Next.js API Routes → db.ts → Railway Python
```

### New Flow
```
Component → tRPC Client → /api/trpc/[...trpc] → tRPC Routers → db.ts → Railway Python
                                                              → local BaZi engine
```

### MCP Server
```
Claude Code → MCP Server → tRPC Client → /api/trpc/[...trpc] → same routers
```

## Key Decisions

1. **Vanilla tRPC client** (not React Query) — keeps migration minimal, preserves existing useState/useEffect patterns
2. **Extract service layer** — move logic from route handlers into shared service functions
3. **Keep old API routes** — for backward compatibility during migration; can remove later
4. **Zod schemas** — for runtime validation + type inference
5. **superjson transformer** — handle Date serialization
6. **MCP server as separate package** — in `mcp-server/` directory, imports AppRouter type

## File Structure

```
src/
├── server/
│   ├── trpc.ts                    # tRPC init (context, router factory)
│   └── routers/
│       ├── _app.ts                # Root app router (merges sub-routers)
│       ├── profile.ts             # Profile CRUD
│       ├── lifeEvent.ts           # Life event CRUD
│       ├── bazi.ts                # BaZi analysis (calls extracted service)
│       ├── dongGong.ts            # Dong Gong calendar
│       └── health.ts              # Health check
├── lib/
│   ├── trpc.ts                    # tRPC vanilla client config
│   └── api.ts                     # REPLACED: thin wrappers over tRPC client
├── app/
│   └── api/
│       └── trpc/
│           └── [...trpc]/
│               └── route.ts       # tRPC catch-all handler
mcp-server/
├── src/
│   └── index.ts                   # MCP server
├── package.json
└── tsconfig.json
```

## Router Procedures

### profile router
- `profile.list` — query, returns Profile[]
- `profile.get` — query, returns Profile
- `profile.create` — mutation, returns Profile
- `profile.update` — mutation, returns Profile
- `profile.delete` — mutation, returns void

### lifeEvent router
- `lifeEvent.create` — mutation, returns LifeEvent
- `lifeEvent.get` — query, returns LifeEvent
- `lifeEvent.update` — mutation, returns LifeEvent
- `lifeEvent.delete` — mutation, returns void

### bazi router
- `bazi.analyze` — query, returns full BaZi analysis

### dongGong router
- `dongGong.calendar` — query, returns DongGongCalendarResponse

### health router
- `health.check` — query, returns { status: "ok" }

## MCP Server Tools

Maps 1:1 to tRPC procedures:
- `list_profiles` — List all profiles
- `get_profile` — Get a profile by ID
- `create_profile` — Create a new profile
- `update_profile` — Update a profile
- `delete_profile` — Delete a profile
- `analyze_bazi` — Run BaZi analysis
- `dong_gong_calendar` — Get Dong Gong calendar
- `create_life_event` — Add life event to profile
- `update_life_event` — Update a life event
- `delete_life_event` — Delete a life event
