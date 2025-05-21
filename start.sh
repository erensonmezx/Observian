#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL to be ready..."
while ! nc -z $DB_HOST $DB_PORT; do
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