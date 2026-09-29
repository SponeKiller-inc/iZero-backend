from typing import Protocol

from app.domain.auth.entities.refresh_token import RefreshToken


class RefreshTokenRepository(Protocol):
    def get_by_session_id(self, session_id: int) -> RefreshToken | None:
        """
        Get refresh token by session id

        Args:
            session_id: Session id

        Returns:
            RefreshToken entity if found, else None
        """
        ...

    def save(self, refresh_token: RefreshToken) -> RefreshToken:
        """
        Save refresh token

        Args:
            refresh_token: RefreshToken entity to save

        Returns:
            Saved RefreshToken entity
        """
        ...
