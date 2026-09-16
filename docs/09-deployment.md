# 09 – Deployment

## Container

[Dockerfile](../Dockerfile):

- Based on `python:3.11-slim`
- Installs `build-essential`, `libpq-dev`, `postgresql-client` (needed for psycopg2 and `pg_isready`)
- Installs dependencies from `requirements.txt`
- Exposes port `8000`
- `ENTRYPOINT` is [entrypoint.sh](../entrypoint.sh)

On startup [entrypoint.sh](../entrypoint.sh):

1. Waits for PostgreSQL to become available (`pg_isready`)
2. Runs `alembic upgrade head`
3. Hands over to `CMD` (uvicorn)

> Migrations therefore run automatically on container startup. With multiple replicas you must ensure only one instance performs the migration. TODO: decide on a strategy.

## Build and run

```powershell
docker build -t izero-backend .
docker run --env-file .env -p 8000:8000 izero-backend
```

## Environments

| Environment | URL | Database | Note |
|-------------|-----|----------|------|
| Local | http://localhost:8000 | local | TODO |
| Staging | TODO | TODO | TODO |
| Production | TODO | TODO | TODO |

## Release procedure

TODO: document
1. Merge into the main branch
2. Build and tag the image
3. Deploy
4. Verification (health check, smoke test)

## Rollback

TODO: describe how to revert to the previous image and, if needed, run `alembic downgrade`.

## Backups

TODO: database backup frequency, retention, and a verified restore procedure.

## Health check

TODO: the application has no health endpoint yet — add `GET /health`.
