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
3. Runs `python -m app.infrastructure.seed.run` (seeds default configuration data, see below)
4. Hands over to `CMD` (uvicorn)

> Migrations therefore run automatically on container startup. With multiple replicas you must ensure only one instance performs the migration. TODO: decide on a strategy.

## Default data seed

[app/infrastructure/seed/run.py](../app/infrastructure/seed/run.py) seeds fixed reference data required for the app to work out of the box. It runs on every container start right after migrations and is idempotent (checks by fixed ID before inserting, so it's safe to re-run).

| Use case | What it seeds | Fixed ID(s) |
|----------|----------------|-------------|
| `SeedDefaultRoles` ([seed_default_roles.py](../app/application/use_cases/seed/seed_default_roles.py)) | `roles` row `"user"` — the role assigned to every newly registered user (`REGULAR_ROLE_ID`) | `1` |
| `SeedDefaultTitles` ([seed_default_titles.py](../app/application/use_cases/seed/seed_default_titles.py)) | `titles` rows `"prefix"` / `"suffix"`, referenced by `prefix_titles`/`suffix_titles` | `1`, `2` |
| `SeedDefaultRolePermissions` ([seed_default_role_permissions.py](../app/application/use_cases/seed/seed_default_role_permissions.py)) | `role_permission` rows granting the `"user"` role `USERS_ASSIGN_MODULE` and `USERS_RETRIEVE_MODULE` — without this, `@authorize`-protected use-cases reject every regular user | — |

Order matters: roles are seeded before role permissions (FK dependency).

Not seeded yet (deliberately, no canonical values exist in code — needs a product decision before implementing):
- `entity_types` (customer type — individual/business/proprietor/...)
- `module_groups` / `modules` — created dynamically via `MODULES_CREATE_GROUP` / `MODULES_CREATE` use-cases, not fixed reference data

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
