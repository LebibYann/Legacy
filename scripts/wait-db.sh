#!/usr/bin/env bash
set -e

# Check for pg_isready
if ! command -v pg_isready > /dev/null 2>&1; then
  echo "❌ pg_isready command not found. Please install PostgreSQL client tools."
  exit 1
fi

# Usage: ./wait-db.sh [timeout_seconds]
TIMEOUT="${1:-60}"
ELAPSED=0

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

echo "⏳  Waiting for Postgres at ${DATABASE_URL##*@} (timeout: $TIMEOUT seconds)..."
while [ $ELAPSED -lt $TIMEOUT ]; do
  if nc -zv $DB_HOST $DB_PORT; then
    echo "Postgres is ready!"
    exit 0
  fi
  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

echo "❌ Timeout: Postgres did not become ready after $TIMEOUT seconds."
exit 1