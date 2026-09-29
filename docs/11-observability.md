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
