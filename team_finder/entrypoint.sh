#!/bin/sh
set -e

echo "Waiting for postgres..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT" 2>/dev/null; do
  sleep 0.5
done
echo "PostgreSQL started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput --clear

# Load demo data only on the first run (when no users exist).
echo "Loading initial data if needed..."
python manage.py load_demo_data || true

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
