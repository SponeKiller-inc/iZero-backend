"""Generic retry-with-exponential-backoff helper for outbound HTTP calls made
via `requests`. Shared by any infrastructure provider that talks to an
external service, so each one doesn't have to reimplement its own retry loop.
"""
import time
from collections.abc import Callable
from typing import TypeVar

import requests

T = TypeVar("T")

# HTTP status codes treated as transient (worth retrying) rather than a
# permanent request/server error.
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def _default_is_retryable(result: object) -> bool:
    """
    Default retry predicate: treats a `requests.Response` with a transient
    (429/5xx) status code as retryable; any other result (or a non-HTTP
    result a caller might return) is treated as final.
    """
    return (
        isinstance(result, requests.Response)
        and result.status_code in _RETRYABLE_STATUS_CODES
    )


def call_with_retries(
    func: Callable[[], T],
    *,
    max_retries: int,
    base_delay_seconds: float,
    is_retryable: Callable[[T], bool] = _default_is_retryable,
) -> T:
    """
    Calls `func`, retrying with exponential backoff on failure.

    A failure is either a `requests.RequestException` (connection error,
    timeout, ...) or a successful call whose result `is_retryable` flags as
    transient (by default, a `requests.Response` with a 429/5xx status). The
    delay starts at `base_delay_seconds` and doubles after every retry.

    Args:
        func: The call to attempt, e.g. `lambda: requests.get(url, ...)`.
        max_retries: Number of additional attempts after the first failure.
        base_delay_seconds: Delay before the first retry; doubled after each
            subsequent attempt.
        is_retryable: Predicate deciding whether a *successful* result should
            still be retried. Not called when `func` raises - exceptions are
            always retried. Defaults to checking for a 429/5xx HTTP response.

    Returns:
        The first result of `func` that doesn't raise and that `is_retryable`
        accepts, or the last result once `max_retries` is exhausted.

    Raises:
        requests.RequestException: Propagated from `func` once `max_retries`
            failed attempts have been exhausted.
    """
    delay = base_delay_seconds

    for attempt in range(max_retries + 1):
        try:
            result = func()
        except requests.RequestException:
            if attempt >= max_retries:
                raise
        else:
            if attempt >= max_retries or not is_retryable(result):
                return result

        time.sleep(delay)
        delay *= 2
