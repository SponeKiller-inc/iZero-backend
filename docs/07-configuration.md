# 07 – Configuration

Configuration is loaded through pydantic-settings from the `.env` file in the project root or from environment variables ([config.py](../app/infrastructure/config.py)). Names are not case-sensitive and unknown keys are ignored.

All variables are **required** — the application will not start without them.

## Database

| Variable | Type | Description |
|----------|------|-------------|
| `DATABASE_HOSTNAME` | str | PostgreSQL host |
| `DATABASE_PORT` | int | PostgreSQL port |
| `DATABASE_NAME` | str | Database name |
| `DATABASE_USERNAME` | str | User |
| `DATABASE_PASSWORD` | str | Password (secret) |

## Tokens and authentication

| Variable | Type | Description |
|----------|------|-------------|
| `PWD_CONTEXT_SCHEME` | str | Password hashing scheme for passlib |
| `GOOGLE_OAUTH_CLIENT_ID` | str | Client ID used to verify the Google id_token |

## Application

| Variable | Type | Description |
|----------|------|-------------|
| `USER_MODULE_EXPIRE_MINUTES` | int | Default validity of a granted module |
| `CORS_ALLOW_ORIGINS` | str | Comma-separated list of origins |
| `CORS_ALLOW_METHODS` | str | Comma-separated list of methods |
| `CORS_ALLOW_HEADERS` | str | Comma-separated list of headers |
| `SENTRY_DSN` | str | Sentry DSN (secret) |

## HTTP audit

Shared by both the outbound audit (external calls made via `requests`, see [http_audit.py](../app/infrastructure/providers/http_audit.py)) and the inbound audit (incoming API calls, see [http_audit.py](../app/infrastructure/api/middleware/http_audit.py)).

| Variable | Type | Description |
|----------|------|-------------|
| `HTTP_AUDIT_SENSITIVE_HEADERS` | list[str] (JSON array) | Header names redacted before being stored by the HTTP audit logs, e.g. `["authorization","cookie"]` (default: `authorization,cookie,set-cookie,x-api-key,proxy-authorization`) |
| `HTTP_AUDIT_MAX_BODY_LENGTH` | int | Max number of characters of request/response body stored by the HTTP audit logs before truncation (default: `10000`) |

## `.env` template

TODO: keep a `.env.example` file in the repository with the same list of keys and empty values.

## Secret management

TODO: describe where secrets are stored for each environment (dev / staging / prod) and how they are rotated.
