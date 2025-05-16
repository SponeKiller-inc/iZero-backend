#!/bin/sh
set -e

# wait on postgres 
until pg_isready -h "$DATABASE_HOSTNAME" -p "$DATABASE_PORT"; do
  echo "Waiting for Postgres at $DATABASE_HOSTNAME:$DATABASE_PORT..."
  sleep 1
done

# Migration db tables
alembic upgrade head

# start Uvicorn
exec "$@"