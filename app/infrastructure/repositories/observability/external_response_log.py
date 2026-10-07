from app.infrastructure.models.observability.external_response_log import (
    ExternalResponseLogModel,
)
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyExternalResponseLogRepository(BaseAlchemyRepository):
    """Persists the outcome of an outbound HTTP request."""

    def save(
        self,
        request_id: int,
        status_code: int | None,
        headers: str | None,
        body: str | None,
        duration_ms: float,
        error: str | None,
    ) -> None:
        """
        Persist the outcome of a previously logged outbound HTTP request.

        Args:
            request_id: Request id
            status_code: HTTP status code
            headers: Response headers
            body: Response body
            duration_ms: Total time the call took, in milliseconds.
            error: Exception type/message, if the call failed.
        """
        self._insert(request_id, status_code, headers, body, duration_ms, error)

    def _insert(
        self,
        request_id: int,
        status_code: int | None,
        headers: str | None,
        body: str | None,
        duration_ms: float,
        error: str | None,
    ) -> None:
        self.db.add(
            ExternalResponseLogModel(
                request_id=request_id,
                status_code=status_code,
                headers=headers,
                body=body,
                duration_ms=duration_ms,
                error=error,
            )
        )
        self.db.flush()
