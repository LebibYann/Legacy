#!/usr/bin/env bash

./wait-db.sh &

APP_MODULE="app.main:app"

if [ "$MODE" = "dev" ]; then
  echo "Starting development server..."
  exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --reload
else
  echo "Starting production server..."
  exec gunicorn "$APP_MODULE" \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind "$HOST:$PORT"
fi