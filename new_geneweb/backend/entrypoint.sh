#!/usr/bin/env bash

./wait-db.sh &

APP_MODULE="app.main:app"
# Liste des variables que tu veux mettre à jour
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
)

for v in "${vars[@]}"; do
  val="${!v}"
  if [ -n "$val" ]; then
    # Si le fichier contient déjà la variable
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