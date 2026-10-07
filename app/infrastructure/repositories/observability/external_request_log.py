from app.infrastructure.models.observability.external_request_log import (
    ExternalRequestLogModel,
)
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyExternalRequestLogRepository(BaseAlchemyRepository):
    """Persists an outbound HTTP request."""

    def save(
        self,
        method: str,
        url: str,
        headers: str | None,
        body: str | None,
    ) -> int:
        """
        Persist an outbound HTTP request.

        Args:
            method: HTTP method.
            url: Target URL.
            headers: Request headers, if any.
            body: Request body, if any.

        Returns:
            int: id of the stored request log row.
        """
        return self._insert(method, url, headers, body)

    def _insert(
        self,
        method: str,
        url: str,
        headers: str | None,
        body: str | None,
    ) -> int:
        request_log = ExternalRequestLogModel(
            method=method,
            url=url,
            headers=headers,
            body=body,
        )
        self.db.add(request_log)
        self.db.flush()
        self.db.refresh(request_log)

        return request_log.id
