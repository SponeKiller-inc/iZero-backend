# 04 – Data Model

Database: PostgreSQL. ORM: SQLAlchemy 2.x, declarative models in `app/infrastructure/models/`.

## Common conventions

Every table inherits from `Base` (`app/infrastructure/database/base.py`), which adds:

| Column | Type | Note |
|--------|------|------|
| `created_at` | `timestamptz` | defaults to the current time (UTC) at insert; not passed in by callers |
| `updated_at` | `timestamptz` | defaults to the current time (UTC) at insert; reset to the current time (UTC) on every update |

Tables with time validity additionally use `ValidityMixin`:

| Column | Type | Note |
|--------|------|------|
| `valid_from` | `timestamptz` | required |
| `valid_to` | `timestamptz` | required, constraint `ck_<table>_valid_dates` |

Further conventions:
- Primary key `id`, `Integer`, autoincrement.
- Foreign keys to the owning entity use `ondelete="CASCADE"`.
- All timestamps are UTC.

## Table overview

| Area | Tables |
|------|--------|
| Users | `users`, `user_roles`, `user_modules`, `user_addresses` |
| Authorization | `roles`, `role_permission` |
| Sessions | `sessions`, `refresh_token`, `session_log` |
| Modules | `module_groups`, `modules` |
| Customers | `customers`, `entity_types` |
| Addresses | `addresses`, `address_types`, `countries` |
| Banks | `banks`, `bank_accounts`, `bank_addresses` |
| Contacts | `emails`, `phones` |
| Titles | `titles`, `prefix_titles`, `suffix_titles` |
| Observability | `external_request_log`, `external_response_log`, `internal_request_log`, `internal_response_log` |

See [ER Diagram](er-diagram.md) for how these tables relate to each other.

## Repositories

Each domain context declares a repository interface as a `Protocol` in `app/domain/<context>/repositories/` (e.g. `UserRepository`, `ModuleRepository`) — a structural contract with no SQLAlchemy dependency.

Concrete implementations live in `app/infrastructure/repositories/<area>/`, named `Alchemy<Entity>Repository`, and inherit `BaseAlchemyRepository` (holds the `Session` only).

Common pattern inside an implementation:
- A private mapper (typically `_to_entity()`) converts an ORM model to the corresponding domain entity.
- `save()` inspects whether the entity has an `id` and dispatches to a private `_insert()` or `_update()`.
- Each method calls `self.db.flush()` only — commit/rollback is centralized in `app/infrastructure/database/session.py` (`_session_scope`/`db_session`), which wraps the whole request (or `with db_session():` block) as the unit-of-work boundary.

### Bulk writes (`upsert_many`)

`save()` costs two round-trips per row (`flush` = `INSERT ... RETURNING id`, `refresh` = `SELECT` of the same row), which is fine for a single entity but not for bulk imports. Measured locally on `addresses`: ~1.26 ms/row via `save()` (≈ 63 min for the 3M-row RÚIAN catalogue) vs ~0.06–0.09 ms/row via a bulk upsert (≈ 3–5 min).

Whenever a use case persists many entities at once (imports, synchronization with an external source), the repository exposes `upsert_many(entities: list[Entity]) -> None` instead of looping over `save()`:

- Matches existing rows by the entity's **natural key** backed by a unique constraint (e.g. `uq_addresses_external_id_country_id`), never by `id` — external data has no internal ID.
- Implemented as a single PostgreSQL `INSERT ... ON CONFLICT ON CONSTRAINT <uq> DO UPDATE SET col = EXCLUDED.col` (`sqlalchemy.dialects.postgresql.insert`), executed with the batch passed as parameters (`self.db.execute(stmt, rows)`, executemany/insertmanyvalues) rather than `.values(rows)`, which is ~3× slower.
- New rows are inserted; existing rows are overwritten but keep their `id`, so foreign keys pointing at them (e.g. `user_addresses`) stay intact. That also makes the write idempotent: re-running an interrupted import or re-importing to fix data is safe.
- The `SET` list names the updatable columns explicitly and leaves out `id`, the natural key and `created_at`. It must include `updated_at`, because the ORM `onupdate` hook doesn't fire for `ON CONFLICT DO UPDATE`.
- Duplicates of the natural key within one batch are collapsed in Python first (last one wins) — PostgreSQL rejects a statement that updates the same row twice.
- Entities are still built through the domain (`Entity.create(...)`) so validation runs; the repository only maps them to rows. It returns nothing and doesn't load ORM objects into the session.
- Callers pass reasonably sized batches (one provider page, e.g. 2000 rows), not the whole data set.

Implementation reference: `AlchemyAddressRepository.upsert_many` ([address.py](../app/infrastructure/repositories/address/address.py)).

## Migrations

- Tool: Alembic, configuration in [alembic.ini](../alembic.ini), environment in [app/infrastructure/alembic/env.py](../app/infrastructure/alembic/env.py).
- `target_metadata` is `Base.metadata`; models are registered by importing the `app.infrastructure.models` package.
- The connection string is built from `Settings` at runtime, not from `alembic.ini`.

Common commands:

```powershell
alembic revision --autogenerate -m "describe change"
alembic upgrade head
alembic downgrade -1
alembic history --verbose
```

Rules:
- Always review an autogenerated migration manually (autogenerate cannot detect renames or data transformations).
- Every migration must have a working `downgrade()`.
- Migrations that delete data must be described in a comment and approved in the PR.
