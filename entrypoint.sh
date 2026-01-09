#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."

# Wait for PostgreSQL to be ready
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-okurmen_user}"; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Run migrations
python manage.py migrate --noinput

# Collect static files (in case they weren't collected during build)
python manage.py collectstatic --noinput || true

# Execute command
exec "$@"

