#!/usr/bin/env node

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

// ---------------------------------------------------------------------------
// tRPC HTTP client — calls the Next.js tRPC endpoint directly
// ---------------------------------------------------------------------------

const BASE_URL = process.env.BAZINGSE_URL ?? 'http://localhost:4321';

async function trpcQuery(path: string, input?: unknown): Promise<unknown> {
  const url = new URL(`/api/trpc/${path}`, BASE_URL);
  url.searchParams.set('input', JSON.stringify({ json: input ?? null }));

  const res = await fetch(url.toString());
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`tRPC error (${res.status}): ${text}`);
  }
  const data = await res.json();
  return data.result?.data?.json ?? data.result?.data;
}

async function trpcMutate(path: string, input?: unknown): Promise<unknown> {
  const res = await fetch(`${BASE_URL}/api/trpc/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ json: input ?? null }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`tRPC error (${res.status}): ${text}`);
  }
  const data = await res.json();
  return data.result?.data?.json ?? data.result?.data;
}

function formatResult(data: unknown): { content: Array<{ type: 'text'; text: string }> } {
  return { content: [{ type: 'text' as const, text: JSON.stringify(data, null, 2) }] };
}

function formatError(error: unknown): { content: Array<{ type: 'text'; text: string }>; isError: true } {
  return {
    content: [{ type: 'text' as const, text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
    isError: true,
  };
}

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new McpServer({
  name: 'bazingse',
  version: '1.0.0',
});

// --- Health Check ---
server.tool(
  'health_check',
  'Check if the BaZingSe API is running',
  {},
  async () => {
    try {
      return formatResult(await trpcQuery('health.check'));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- List Profiles ---
server.tool(
  'list_profiles',
  'List all BaZi profiles',
  {
    limit: z.number().int().min(1).max(10000).default(100).describe('Maximum number of profiles to return'),
  },
  async ({ limit }) => {
    try {
      return formatResult(await trpcQuery('profile.list', { limit }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Get Profile ---
server.tool(
  'get_profile',
  'Get a BaZi profile by ID, including life events',
  {
    id: z.string().describe('Profile ID'),
  },
  async ({ id }) => {
    try {
      return formatResult(await trpcQuery('profile.get', { id }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Create Profile ---
server.tool(
  'create_profile',
  'Create a new BaZi profile',
  {
    name: z.string().min(1).describe('Person name'),
    birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).describe('Birth date in YYYY-MM-DD format'),
    gender: z.enum(['male', 'female']).describe('Gender'),
    birth_time: z.string().regex(/^\d{2}:\d{2}$/).optional().describe('Birth time in HH:MM format (optional)'),
    place_of_birth: z.string().optional().describe('Place of birth (optional)'),
    phone: z.string().optional().describe('Phone number (optional)'),
  },
  async (input) => {
    try {
      return formatResult(await trpcMutate('profile.create', input));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Update Profile ---
server.tool(
  'update_profile',
  'Update an existing BaZi profile',
  {
    id: z.string().describe('Profile ID'),
    name: z.string().min(1).optional().describe('New name'),
    birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional().describe('New birth date'),
    gender: z.enum(['male', 'female']).optional().describe('New gender'),
    birth_time: z.string().regex(/^\d{2}:\d{2}$/).optional().describe('New birth time'),
    place_of_birth: z.string().optional().describe('New place of birth'),
    phone: z.string().optional().describe('New phone number'),
  },
  async ({ id, ...data }) => {
    try {
      return formatResult(await trpcMutate('profile.update', { id, data }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Delete Profile ---
server.tool(
  'delete_profile',
  'Delete a BaZi profile',
  {
    id: z.string().describe('Profile ID to delete'),
  },
  async ({ id }) => {
    try {
      await trpcMutate('profile.delete', { id });
      return formatResult({ success: true, message: `Profile ${id} deleted` });
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Analyze BaZi ---
server.tool(
  'analyze_bazi',
  'Run BaZi (Four Pillars) analysis for a birth date. Returns pillar data, element analysis, ten gods, interactions, narratives, and more.',
  {
    birth_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).describe('Birth date in YYYY-MM-DD format'),
    gender: z.enum(['male', 'female']).describe('Gender'),
    birth_time: z.string().nullable().optional().describe('Birth time in HH:MM format, "unknown", or null'),
    analysis_year: z.number().int().nullable().optional().describe('Year to analyze (for luck pillars)'),
    analysis_month: z.number().int().min(1).max(12).nullable().optional().describe('Month to analyze'),
    analysis_day: z.number().int().min(1).max(31).nullable().optional().describe('Day to analyze'),
    analysis_time: z.string().nullable().optional().describe('Time to analyze in HH:MM format'),
    school: z.enum(['classic', 'physics']).optional().default('classic').describe('BaZi school of analysis'),
  },
  async (input) => {
    try {
      return formatResult(await trpcQuery('bazi.analyze', input));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Dong Gong Calendar ---
server.tool(
  'dong_gong_calendar',
  'Get Dong Gong date selection calendar for a month. Shows auspicious/inauspicious days, officers, ratings, moon phases.',
  {
    year: z.number().int().describe('Year'),
    month: z.number().int().min(1).max(12).describe('Month (1-12)'),
  },
  async ({ year, month }) => {
    try {
      return formatResult(await trpcQuery('dongGong.calendar', { year, month }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Create Life Event ---
server.tool(
  'create_life_event',
  'Add a life event to a profile (e.g., marriage, job change, travel)',
  {
    profile_id: z.string().describe('Profile ID'),
    year: z.number().int().min(1900).max(2100).describe('Year of the event'),
    month: z.number().int().min(1).max(12).nullable().optional().describe('Month (optional)'),
    day: z.number().int().min(1).max(31).nullable().optional().describe('Day (optional)'),
    location: z.string().nullable().optional().describe('Location of the event'),
    notes: z.string().nullable().optional().describe('Notes about the event'),
    is_abroad: z.boolean().optional().describe('Whether the person was abroad'),
  },
  async ({ profile_id, ...data }) => {
    try {
      return formatResult(await trpcMutate('lifeEvent.create', { profileId: profile_id, data }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Update Life Event ---
server.tool(
  'update_life_event',
  'Update an existing life event',
  {
    profile_id: z.string().describe('Profile ID'),
    event_id: z.string().describe('Life event ID'),
    year: z.number().int().min(1900).max(2100).optional().describe('New year'),
    month: z.number().int().min(1).max(12).nullable().optional().describe('New month'),
    day: z.number().int().min(1).max(31).nullable().optional().describe('New day'),
    location: z.string().nullable().optional().describe('New location'),
    notes: z.string().nullable().optional().describe('New notes'),
    is_abroad: z.boolean().optional().describe('Whether abroad'),
  },
  async ({ profile_id, event_id, ...data }) => {
    try {
      return formatResult(await trpcMutate('lifeEvent.update', {
        profileId: profile_id,
        eventId: event_id,
        data,
      }));
    } catch (error) {
      return formatError(error);
    }
  },
);

// --- Delete Life Event ---
server.tool(
  'delete_life_event',
  'Delete a life event from a profile',
  {
    profile_id: z.string().describe('Profile ID'),
    event_id: z.string().describe('Life event ID'),
  },
  async ({ profile_id, event_id }) => {
    try {
      await trpcMutate('lifeEvent.delete', { profileId: profile_id, eventId: event_id });
      return formatResult({ success: true, message: `Life event ${event_id} deleted` });
    } catch (error) {
      return formatError(error);
    }
  },
);

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('BaZingSe MCP server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
