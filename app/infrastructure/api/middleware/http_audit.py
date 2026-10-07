import json
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.infrastructure.config import settings
from app.infrastructure.database.session import db_session
from app.infrastructure.observability.redaction import (
    redact_body,
    redact_headers,
    stringify_body,
)
from app.infrastructure.repositories.observability.internal_request_log import (
    AlchemyInternalRequestLogRepository,
)
from app.infrastructure.repositories.observability.internal_response_log import (
    AlchemyInternalResponseLogRepository,
)

# Headers/body fields that must never land in the DB, regardless of which
# endpoint is called. Shared with the outbound HTTP audit - configurable via
# HTTP_AUDIT_SENSITIVE_HEADERS / HTTP_AUDIT_SENSITIVE_BODY_FIELDS /
# HTTP_AUDIT_MAX_BODY_LENGTH in .env.
_SENSITIVE_HEADERS = {h.lower() for h in settings.http_audit_sensitive_headers}
_SENSITIVE_BODY_FIELDS = {f.lower() for f in settings.http_audit_sensitive_body_fields}
_MAX_BODY_LENGTH = settings.http_audit_max_body_length


class HttpAuditMiddleware(BaseHTTPMiddleware):
    """
    Audits every incoming API call (the request our API receives and the
    response it sends back), mirroring the outbound audit performed by
    app/infrastructure/providers/http_audit.py for external HTTP calls.

    Must be the outermost middleware (added last in main.py) so it captures
    the request/response exactly as the client sent/received them, before or
    after any other middleware touches them.
    """

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        request_id = _log_request(request, body)

        started = time.monotonic()
        status_code = None
        error = None
        response = None
        response_body = b""
        try:
            response = await call_next(request)
            status_code = response.status_code

            # call_next() returns a streaming response whose body_iterator can
            # only be consumed once - read it here to audit it, then hand the
            # client a fresh iterator over the same bytes.
            response_body = b"".join([chunk async for chunk in response.body_iterator])
            response.body_iterator = _iter_bytes(response_body)
            return response
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
            raise
        finally:
            duration_ms = (time.monotonic() - started) * 1000
            _log_response(request_id, status_code, response, response_body, duration_ms, error)


async def _iter_bytes(data: bytes):
    yield data


def _log_request(request: Request, body: bytes) -> int | None:
    try:
        redacted_body = redact_body(body or None, request.headers.get("content-type"), _SENSITIVE_BODY_FIELDS)
        with db_session() as db:
            return AlchemyInternalRequestLogRepository(db).save(
                method=request.method,
                url=str(request.url),
                headers=json.dumps(redact_headers(request.headers, _SENSITIVE_HEADERS)),
                body=stringify_body(redacted_body, _MAX_BODY_LENGTH),
            )
    except Exception:  # noqa: BLE001 - auditing must never break the real call
        return None


def _log_response(
    request_id: int | None,
    status_code: int | None,
    response: Response | None,
    response_body: bytes,
    duration_ms: float,
    error: str | None,
) -> None:
    if request_id is None:
        return

    try:
        redacted_body = (
            redact_body(response_body or None, response.headers.get("content-type"), _SENSITIVE_BODY_FIELDS)
            if response is not None
            else None
        )
        with db_session() as db:
            AlchemyInternalResponseLogRepository(db).save(
                request_id=request_id,
                status_code=status_code,
                headers=json.dumps(redact_headers(response.headers, _SENSITIVE_HEADERS)) if response is not None else None,
                body=stringify_body(redacted_body, _MAX_BODY_LENGTH) if response is not None else None,
                duration_ms=duration_ms,
                error=error,
            )
    except Exception:  # noqa: BLE001, S110 - auditing must never break the real call
        pass
