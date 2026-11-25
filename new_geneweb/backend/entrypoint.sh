#!/usr/bin/env bash

./wait-db.sh &

APP_MODULE="app.main:app"
# List of variables you want to update
vars=(
  FRONTEND_DNS
  BACKOFFICE_DNS
  OLD_BACKOFFICE_PORT
  OLD_FRONTEND_PORT
  NEW_BACKOFFICE_PORT
  NEW_FRONTEND_PORT
  MODE
  DB_HOST
  DB_PORT
  DB_USER
  DB_PASSWORD
  DB_NAME
  DATABASE_URL
  PORT
  HOST
  BACKOFFICE_USERNAME
  BACKOFFICE_PASSWORD
  APP_NAME
)

# Create .env if missing
if [ ! -f /app/.env ]; then
  echo "Creating missing .env file..."
  touch /app/.env
fi

for v in "${vars[@]}"; do
  val="${!v}"
  if [ -n "$val" ]; then
    # If the file already contains the variable
    if grep -q "^${v}=" .env; then
      sed -i "s|^${v}=.*|${v}=${val}|" .env
    else
      echo "${v}=${val}" >> .env
    fi
  fi
done

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