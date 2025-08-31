#!/bin/bash
set -e

# Ensure the database host resolves before attempting connection checks
if ! getent hosts "$DB_HOST" >/dev/null; then
  echo "❌ Unable to resolve host: $DB_HOST"
  exit 1
fi

echo "🔄 Waiting for PostgreSQL to be ready..."
START_TIME=$(date +%s)
TIMEOUT=${DB_TIMEOUT:-60}
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  elapsed=$(( $(date +%s) - START_TIME ))
  if [ "$elapsed" -ge "$TIMEOUT" ]; then
    echo "⏰ Timeout: unable to connect to $DB_HOST:$DB_PORT after ${TIMEOUT}s"
    exit 1
  fi
  sleep 1
done

echo "✅ PostgreSQL is up. Running DB migrations..."
python -m app.db.init_db

if [ "$SEED_DATA" = "true" ]; then
  echo "🌱 Seeding initial data..."
  python -m app.db.seed_data
fi

echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
