# 11 – Operations & Monitoring

## Sentry

Initialized in [main.py](../app/infrastructure/api/main.py):

- DSN from `SENTRY_DSN`
- `traces_sample_rate=1.0` — 100 % of transactions are recorded. TODO: lower this in production.
- `send_default_pii=True` — personal data (IP, user) is sent. TODO: assess GDPR compliance.

A global handler catches every unhandled exception, reports it to Sentry and returns 500 with `SYSTEM_INTERNAL_FAIL` to the client.

## Logging

TODO: document
- Library and format in use (structured JSON logs recommended)
- Log levels per environment
- Request correlation ID (the `sid` cookie or a dedicated `X-Request-ID` are natural candidates)
- Prohibition on logging passwords, tokens and personal data

## Audit

The `session_log` table records session events (`event_type`).

TODO: define the list of event types and the retention period.

### HTTP call audit

Every HTTP call is persisted for troubleshooting/traceability purposes, with sensitive headers redacted and bodies truncated per `HTTP_AUDIT_SENSITIVE_HEADERS` / `HTTP_AUDIT_MAX_BODY_LENGTH` (see [07-configuration.md](07-configuration.md)):

- **Outbound** (calls our code makes to external services): installed once as a hook around `requests.adapters.HTTPAdapter.send` in [http_audit.py](../app/infrastructure/providers/http_audit.py). Stored in `external_request_log` / `external_response_log`.
- **Inbound** (calls made to our own API): captured by `HttpAuditMiddleware` in [http_audit.py](../app/infrastructure/api/middleware/http_audit.py), registered as the outermost middleware in [main.py](../app/infrastructure/api/main.py) so it sees the request/response exactly as the client sent/received them. Stored in `internal_request_log` / `internal_response_log`.

Both directions share redaction/truncation logic from [redaction.py](../app/infrastructure/observability/redaction.py). Logging failures never break the real request/response - they're swallowed and ignored.

Header redaction alone does not protect credentials carried in the body itself (e.g. `password` on `/user` registration and on `/token/local` - an `OAuth2PasswordRequestForm` - or `jwt_token` on `/token/google`, and the `access_token` returned in the login response). Request/response bodies are therefore also redacted by content type before being persisted, via `redact_body` in [redaction.py](../app/infrastructure/observability/redaction.py):

- `application/json` (and `+json`) bodies are parsed and any key (recursively, case-insensitive) matching `HTTP_AUDIT_SENSITIVE_BODY_FIELDS` has its value replaced with `***`.
- `application/x-www-form-urlencoded` bodies (e.g. `OAuth2PasswordRequestForm`) are parsed the same way field-by-field.
- `multipart/form-data` bodies are not parsed (they may carry file contents) and are stored as a fixed placeholder instead.
- Fails closed for everything else: a body claiming to be JSON/form but failing to parse, or any content type not in the list above, is never stored raw - it's replaced with an `<unprocessable content-type '...'>` placeholder, since we can't guarantee it carries no credential.

## Metrics

TODO: define tracked metrics (latency, error rate, login count, active sessions) and the tooling.

## Alerting

TODO: define rules and escalation.

## Runbook

TODO: procedures for common incidents:
- Database unavailable
- DB connection pool exhausted
- High 5xx error rate
- Migration stuck during startup
