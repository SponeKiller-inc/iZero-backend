"""
Shared helpers for HTTP audit logging.

Used both by the outbound audit hook (app/infrastructure/providers/http_audit.py,
which logs calls our code makes to external services) and by the inbound audit
middleware (app/infrastructure/api/middleware/http_audit.py, which logs calls
made to our own API), so redaction and truncation rules stay consistent in
both directions.
"""

import json
from urllib.parse import parse_qsl, urlencode

_REDACTED = "***"
_MULTIPART_BODY = b"<multipart body omitted from audit log>"


def _unprocessable_body(content_type: str | None) -> bytes:
    """
    Placeholder stored instead of the raw body whenever it can't be safely
    redacted - either because its content type isn't one we know how to
    parse (fail closed: unknown types are never passed through raw), or
    because a body claiming to be JSON/form-urlencoded fails to parse as
    such. Keeps the content type in the placeholder to help diagnose issues
    without ever persisting the original, potentially sensitive, content.
    """
    label = content_type or "<none>"
    return f"<unprocessable content-type '{label}' - body omitted from audit log>".encode()


def redact_headers(headers, sensitive_headers: set[str]) -> dict[str, str]:
    """
    Replaces the value of any header whose name matches (case-insensitively)
    one of `sensitive_headers` with a placeholder, so secrets never land in
    the DB.
    """
    return {
        key: ("***" if key.lower() in sensitive_headers else value)
        for key, value in headers.items()
    }


def redact_body(
    body: bytes | str | None,
    content_type: str | None,
    sensitive_fields: set[str],
) -> bytes | str | None:
    """
    Redacts sensitive fields (e.g. passwords, tokens) from a request/response
    body before it is persisted, based on its content type.

    Credentials such as `RegistrationLocalSchemaIn.password`,
    `OAuth2PasswordRequestForm` fields or a returned `access_token` are not
    protected by header redaction alone, since they travel in the body - so
    JSON and form-urlencoded bodies are parsed and sensitive keys are
    replaced, recursively for JSON. Multipart bodies are not parsed (they may
    carry file contents) and are replaced wholesale with a placeholder.

    Fails closed: a content type we don't explicitly know how to parse (or a
    JSON/form body that fails to parse despite its declared content type) is
    never passed through raw - it's replaced with a placeholder, since we
    can't guarantee there's no credential hiding in it. Bodies that aren't
    `bytes`/`str` to begin with (streaming/file-like objects, which
    `stringify_body` can't serialize anyway) are returned unchanged.
    """
    if body is None or not sensitive_fields:
        return body

    if not isinstance(body, (bytes, str)):
        return body  # streaming/file-like - let stringify_body handle it

    raw = body if isinstance(body, bytes) else body.encode("utf-8")
    base_content_type = (content_type or "").split(";", 1)[0].strip().lower()

    if base_content_type == "application/json" or base_content_type.endswith("+json"):
        return _redact_json_body(raw, sensitive_fields, content_type)
    if base_content_type == "application/x-www-form-urlencoded":
        return _redact_form_body(raw, sensitive_fields, content_type)
    if base_content_type.startswith("multipart/"):
        return _MULTIPART_BODY

    return _unprocessable_body(content_type)


def _redact_json_body(raw: bytes, sensitive_fields: set[str], content_type: str | None) -> bytes:
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:  # noqa: BLE001 - malformed body must not break auditing
        return _unprocessable_body(content_type)
    return json.dumps(_redact_json_value(data, sensitive_fields)).encode("utf-8")


def _redact_json_value(value, sensitive_fields: set[str]):
    if isinstance(value, dict):
        return {
            key: (_REDACTED if key.lower() in sensitive_fields else _redact_json_value(val, sensitive_fields))
            for key, val in value.items()
        }
    if isinstance(value, list):
        return [_redact_json_value(item, sensitive_fields) for item in value]
    return value


def _redact_form_body(raw: bytes, sensitive_fields: set[str], content_type: str | None) -> bytes:
    try:
        pairs = parse_qsl(raw.decode("utf-8"), keep_blank_values=True, strict_parsing=False)
    except Exception:  # noqa: BLE001 - malformed body must not break auditing
        return _unprocessable_body(content_type)
    redacted_pairs = [
        (key, _REDACTED if key.lower() in sensitive_fields else value) for key, value in pairs
    ]
    return urlencode(redacted_pairs).encode("utf-8")


def stringify_body(body: bytes | str | None, max_length: int) -> str | None:
    """
    Converts a request/response body into a string safe to store in the DB,
    truncated to `max_length` characters.

    Returns None for missing bodies and for bodies that can't be safely
    serialized (e.g. streaming/file-like objects).
    """
    if body is None:
        return None

    if isinstance(body, bytes):
        try:
            text = body.decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001 - malformed body must not break auditing
            return None
    elif isinstance(body, str):
        text = body
    else:
        return None  # streaming/file-like body - not safely serializable

    if len(text) > max_length:
        return text[:max_length] + "...<truncated>"
    return text
