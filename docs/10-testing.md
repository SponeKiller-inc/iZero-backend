# 10 – Testing

## Strategy

| Level | What it covers | Tooling | Location |
|-------|----------------|---------|----------|
| Unit | Domain entities, value objects, use cases with fake ports | pytest | TODO `tests/unit/` |
| Integration | Repositories against a real database, migrations | pytest + test DB | TODO `tests/integration/` |
| API | Endpoints end-to-end via `TestClient` | pytest + httpx | TODO `tests/api/` |

Key benefit of the architecture: use cases depend on ports (`TimeProvider`, `PasswordHasher`, `TokenGenerator`, `IdentityProvider`), so they can be tested without a database and without network access.

## Running tests

```powershell
pytest
pytest --cov=app --cov-report=term-missing
```

TODO: add pytest and coverage to `requirements.txt` (or `requirements-dev.txt`).

## Test data

TODO: describe fixture setup, transaction isolation and lookup table seeding.

## Required coverage

- [ ] Password verification and hashing
- [ ] JWT encode/decode including expiry and malformed tokens
- [ ] Google id_token verification (mocked)
- [ ] Session initialization and restoration
- [ ] Authorization by role and time validity
- [ ] The `valid_at` filter over tables with validity
- [ ] Error responses and `message_id` values

## Definition of Done

TODO: define (e.g. every new use case has unit tests, every new endpoint has an API test, migrations verified for both upgrade and downgrade).
