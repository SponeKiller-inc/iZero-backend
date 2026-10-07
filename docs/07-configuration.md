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
| `HTTP_AUDIT_SENSITIVE_BODY_FIELDS` | list[str] (JSON array) | JSON/form field names (case-insensitive, matched recursively for JSON) redacted in request/response bodies before being stored, e.g. `["password","access_token"]` (default: `password,new_password,old_password,current_password,token,access_token,refresh_token,id_token,jwt_token,client_secret,secret,csrf_token,api_key,authorization`) |
| `HTTP_AUDIT_MAX_BODY_LENGTH` | int | Max number of characters of request/response body stored by the HTTP audit logs before truncation (default: `10000`) |

## RÚIAN address provider

| Variable | Type | Description |
|----------|------|-------------|
| `RUIAN_QUERY_URL` | str | URL of the RÚIAN `AdresniMisto` ArcGIS REST query endpoint |
| `RUIAN_PAGE_SIZE` | int | Number of address records requested per page |
| `RUIAN_REQUEST_TIMEOUT_SECONDS` | int | Timeout in seconds for each page request |
| `RUIAN_MAX_RETRIES` | int | Number of additional attempts for a page request after a transient failure (timeout, connection error, or a 5xx/429 response) before giving up (default: `3`) |
| `RUIAN_RETRY_BACKOFF_SECONDS` | float | Delay before the first retry; doubled after each subsequent attempt (default: `2.0`) |

Retries are handled by the generic [`call_with_retries`](../app/infrastructure/providers/http_retry.py) helper, shared by any infrastructure provider that needs to retry an outbound `requests` call.

## `.env` template

TODO: keep a `.env.example` file in the repository with the same list of keys and empty values.

## Secret management

TODO: describe where secrets are stored for each environment (dev / staging / prod) and how they are rotated.
