#!/usr/bin/env bash
set -e

echo "⏳  Waiting for Postgres at ${DATABASE_URL##*@}..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-user}"; do
  sleep 1
done