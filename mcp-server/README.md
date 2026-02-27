# BaZingSe MCP Server

MCP (Model Context Protocol) server for the BaZingSe BaZi astrology API. Connects to the running Next.js app via tRPC.

## Setup

```bash
cd mcp-server
npm install
npm run build
```

## Usage

Add to your Claude Code config (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "bazingse": {
      "command": "node",
      "args": ["/path/to/bazingse/mcp-server/dist/index.js"],
      "env": {
        "BAZINGSE_URL": "http://localhost:4321"
      }
    }
  }
}
```

For production (connecting to Vercel deployment):

```json
{
  "mcpServers": {
    "bazingse": {
      "command": "node",
      "args": ["/path/to/bazingse/mcp-server/dist/index.js"],
      "env": {
        "BAZINGSE_URL": "https://bazingse.vercel.app"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `health_check` | Check if the API is running |
| `list_profiles` | List all BaZi profiles |
| `get_profile` | Get a profile by ID |
| `create_profile` | Create a new profile |
| `update_profile` | Update a profile |
| `delete_profile` | Delete a profile |
| `analyze_bazi` | Run BaZi Four Pillars analysis |
| `dong_gong_calendar` | Get Dong Gong date selection calendar |
| `create_life_event` | Add a life event to a profile |
| `update_life_event` | Update a life event |
| `delete_life_event` | Delete a life event |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BAZINGSE_URL` | `http://localhost:4321` | URL of the running BaZingSe Next.js app |
