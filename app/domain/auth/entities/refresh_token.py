from __future__ import annotations
from typing import Optional, Self
from datetime import datetime

from app.domain.shared.value_objects.period import ValidityPeriod


class RefreshToken:
    """
    Represents a refresh token bound to a session.

    Attributes:
        id: The refresh token ID.
        session_id: The session ID the token belongs to.
        token: The token value.
        validity: The validity period of the token.
    """

    def __init__(
        self,
        id: Optional[int],
        session_id: int,
        token: str,
        validity: ValidityPeriod,
    ) -> None:
        self.id = id
        self.session_id = session_id
        self.token = token
        self.validity = validity

    @classmethod
    def create_new(
        cls,
        session_id: int,
        token: str,
        expire_at: datetime,
        current_time: datetime,
    ) -> Self:
        """
        Creates a new refresh token.

        Args:
            session_id: The session ID the token belongs to.
            token: The token value.
            expire_at: The expiration time of the token.
            current_time: The current time.

        Returns:
            RefreshToken: New refresh token.
        """
        return cls(
            id=None,
            session_id=session_id,
            token=token,
            validity=ValidityPeriod(valid_from=current_time, valid_to=expire_at),
        )

    def is_expired(self, ref_time: datetime) -> bool:
        """
        Check if refresh token is expired

        Args:
            ref_time (datetime): The reference time.

        Returns:
            bool: True if refresh token is expired, False otherwise
        """
        return not self.validity.is_active(ref_time)
