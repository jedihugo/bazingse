#!/usr/bin/env bash
set -euo pipefail

# Migrate a Railway SQLite database to Cloudflare D1
#
# Usage:
#   bash scripts/migrate-railway-to-d1.sh path/to/bazingse.db
#
# Prerequisites:
#   - wrangler CLI authenticated (npx wrangler login)
#   - D1 database created and database_id set in wrangler.jsonc
#   - Drizzle migrations already applied to D1 (npm run db:migrate:prod)

DB_FILE="${1:?Usage: $0 <path-to-sqlite-db>}"
DUMP_FILE="railway-dump.sql"
D1_NAME="bazingse-db"

if [ ! -f "$DB_FILE" ]; then
  echo "Error: Database file not found: $DB_FILE"
  exit 1
fi

echo "==> Exporting data from Railway SQLite..."
sqlite3 "$DB_FILE" <<'SQL' > "$DUMP_FILE"
.mode insert
SELECT * FROM profiles;
SQL

sqlite3 "$DB_FILE" <<'SQL' >> "$DUMP_FILE"
.mode insert
SELECT * FROM life_events;
SQL

if [ ! -s "$DUMP_FILE" ]; then
  echo "Warning: No data found in $DB_FILE (empty dump)"
  rm -f "$DUMP_FILE"
  exit 0
fi

echo "==> Importing data into D1..."
npx wrangler d1 execute "$D1_NAME" --remote --file="$DUMP_FILE"

echo "==> Verifying import..."
npx wrangler d1 execute "$D1_NAME" --remote --command="SELECT 'profiles:', count(*) FROM profiles; SELECT 'life_events:', count(*) FROM life_events;"

echo "==> Cleaning up..."
rm -f "$DUMP_FILE"

echo "Done! Data migrated to D1."
