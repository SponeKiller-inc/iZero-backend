"""
Shared helpers for HTTP audit logging.

Used both by the outbound audit hook (app/infrastructure/providers/http_audit.py,
which logs calls our code makes to external services) and by the inbound audit
middleware (app/infrastructure/api/middleware/http_audit.py, which logs calls
made to our own API), so redaction and truncation rules stay consistent in
both directions.
"""


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
