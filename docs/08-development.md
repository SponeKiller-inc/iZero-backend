# 08 – Development

## Prerequisites

- Python 3.11
- PostgreSQL (locally or in a container)
- Git

## Running locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# create .env as described in docs/07-configuration.md
alembic upgrade head
uvicorn app.infrastructure.api.main:app --reload
```

The API runs at `http://127.0.0.1:8000`, Swagger at `/docs`.

> Note: the `Dockerfile` starts `app.main:app`, while the local entry point is `app.infrastructure.api.main:app`. TODO: unify.

## Working with the code

Adding a new feature typically means:

1. Domain entity / value object in `app/domain/<context>/`
2. Repository interface in `app/domain/<context>/repositories/`
3. DTO in `app/application/dto/<area>/`
4. Use case in `app/application/use_cases/<area>/`
5. ORM model in `app/infrastructure/models/<area>/` + Alembic migration
6. Repository implementation in `app/infrastructure/repositories/<area>/`
7. Pydantic schema + endpoint in `app/infrastructure/api/`
8. DI container in `app/infrastructure/api/dependencies/`
9. Tests + documentation update

## Conventions

- Google-style docstrings (`Args:`, `Returns:`, `Raises:`), written in English.
- Type hints are mandatory on public methods.
- Always work with time through `SystemTimeProvider` (UTC), never `datetime.now()` without a timezone.
- Domain exceptions are not surfaced as HTTP details — translation to a `message_id` happens in the API layer.

TODO: document the configured linter/formatter (ruff, black) and its settings.

## Git workflow

TODO: document
- Branch naming
- Commit message format
- PR and review rules
- Protected branches

## CI

TODO: describe the pipeline (lint, tests, image build).
