import json
import time

import requests

from app.infrastructure.config import settings
from app.infrastructure.database.session import db_session
from app.infrastructure.observability.redaction import (
    redact_body,
    redact_headers,
    stringify_body,
)
from app.infrastructure.repositories.observability.external_request_log import (
    AlchemyExternalRequestLogRepository,
)
from app.infrastructure.repositories.observability.external_response_log import (
    AlchemyExternalResponseLogRepository,
)

# Headers/body fields that must never land in the DB, regardless of which
# service is called. Configurable via HTTP_AUDIT_SENSITIVE_HEADERS /
# HTTP_AUDIT_SENSITIVE_BODY_FIELDS / HTTP_AUDIT_MAX_BODY_LENGTH in .env.
_SENSITIVE_HEADERS = {h.lower() for h in settings.http_audit_sensitive_headers}
_SENSITIVE_BODY_FIELDS = {f.lower() for f in settings.http_audit_sensitive_body_fields}
_MAX_BODY_LENGTH = settings.http_audit_max_body_length

_original_send = requests.adapters.HTTPAdapter.send
_installed = False


def install_http_audit() -> None:
    """
    Installs a process-wide audit hook around requests.adapters.HTTPAdapter.send.

    Because every call made through the `requests` library - whether issued
    directly by our own code or internally by a third-party library - ends up
    calling this single method, patching it here captures all of them
    uniformly, without requiring every provider to instrument itself.

    Must run once, before the first real outbound call. It is invoked from
    app/infrastructure/providers/__init__.py, which runs as soon as any
    provider submodule is imported.
    """
    global _installed
    if _installed:
        return

    requests.adapters.HTTPAdapter.send = _audited_send
    _installed = True


def _audited_send(self, request, **kwargs):
    request_id = _log_request(request)

    # Reading the body of a streamed response would force it to be fully
    # downloaded here, defeating the caller's intent - skip body capture for those.
    capture_response_body = not kwargs.get("stream", False)

    started = time.monotonic()
    status_code = None
    error = None
    response = None
    try:
        response = _original_send(self, request, **kwargs)
        status_code = response.status_code
        return response
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        raise
    finally:
        duration_ms = (time.monotonic() - started) * 1000
        _log_response(request_id, status_code, response, duration_ms, error, capture_response_body)


def _log_request(request) -> int | None:
    try:
        redacted_body = redact_body(request.body, request.headers.get("Content-Type"), _SENSITIVE_BODY_FIELDS)
        with db_session() as db:
            return AlchemyExternalRequestLogRepository(db).save(
                method=request.method,
                url=request.url,
                headers=json.dumps(redact_headers(request.headers, _SENSITIVE_HEADERS)),
                body=stringify_body(redacted_body, _MAX_BODY_LENGTH),
            )
    except Exception:  # noqa: BLE001 - auditing must never break the real call
        return None


def _log_response(
    request_id: int | None,
    status_code: int | None,
    response,
    duration_ms: float,
    error: str | None,
    capture_body: bool,
) -> None:
    if request_id is None:
        return

    try:
        redacted_body = (
            redact_body(response.content, response.headers.get("Content-Type"), _SENSITIVE_BODY_FIELDS)
            if response is not None and capture_body
            else None
        )
        with db_session() as db:
            AlchemyExternalResponseLogRepository(db).save(
                request_id=request_id,
                status_code=status_code,
                headers=json.dumps(redact_headers(response.headers, _SENSITIVE_HEADERS)) if response is not None else None,
                body=stringify_body(redacted_body, _MAX_BODY_LENGTH) if response is not None and capture_body else None,
                duration_ms=duration_ms,
                error=error,
            )
    except Exception:  # noqa: BLE001, S110 - auditing must never break the real call
        pass
