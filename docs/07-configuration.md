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
| `SECRET_KEY` | str | JWT signing key (secret) |
| `ALGORITHM` | str | JWT signing algorithm, e.g. `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_MINUTES` | int | Refresh token lifetime |
| `REFRESH_TOKEN_LENGTH` | int | Length of the generated refresh token |
| `CSRF_TOKEN_LENGTH` | int | Length of the generated CSRF token |
| `SESSION_EXPIRE_MINUTES` | int | Session lifetime |
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

## `.env` template

TODO: keep a `.env.example` file in the repository with the same list of keys and empty values.

## Secret management

TODO: describe where secrets are stored for each environment (dev / staging / prod) and how they are rotated.
