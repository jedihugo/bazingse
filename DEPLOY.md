# Deploying BaZingSe to Cloudflare Pages + D1

## Prerequisites

- Cloudflare account
- `wrangler` CLI (included in devDependencies)
- Node.js 20+

## 1. Create D1 Database

```bash
npx wrangler d1 create bazingse-db
```

Copy the `database_id` from the output and paste it into `wrangler.jsonc`:

```jsonc
"database_id": "<paste-your-id-here>"
```

## 2. Apply Database Migrations

Local (for development):

```bash
npm run db:migrate:local
```

Production:

```bash
npm run db:migrate:prod
```

## 3. Connect GitHub Repo to Cloudflare Pages

1. Go to **Cloudflare Dashboard > Workers & Pages > Create > Pages > Connect to Git**
2. Select the `bazingse` repository
3. Configure build settings:
   - **Build command:** `npm run build`
   - **Build output directory:** `.svelte-kit/cloudflare`
4. The D1 binding is already configured in `wrangler.jsonc` — no manual binding needed

Cloudflare will auto-deploy on every push to the connected branch.

## 4. Local Development

```bash
npm run db:migrate:local   # Create local D1 tables
npm run dev                # Start dev server with D1 proxy
```

The `platformProxy: { persist: true }` option in `svelte.config.js` ensures local D1 data persists between dev server restarts (stored in `.wrangler/`).

## Migrating Data from Railway

If you have an existing SQLite database from Railway, use the migration script:

```bash
bash scripts/migrate-railway-to-d1.sh path/to/bazingse.db
```

See the script for details.
