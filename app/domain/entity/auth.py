from typing import Optional
from app.domain.exceptions.entity.user import (
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError
)
from app.application.ports.password_hasher import PasswordHasher

class Auth:
    def __init__(
        self,
        id: int,
        password_hash: Optional[str] = None,
        google_user_id: Optional[str] = None
    ):
        self.id = id
        self.password_hash = password_hash
        self.google_user_id = google_user_id

    def verify_password(
        self,
        password: str,
        hasher: PasswordHasher
    ) -> None:
        """
        Verify password

        Args:
            password (str): password to verify
            hasher (PasswordHasher): password hasher

        Raises:
            LocalUserNotVerifiedError: if password is not verified
        """
        if not self.password_hash or not hasher.verify(password, self.password_hash):
            raise LocalUserNotVerifiedError

    def verify_google_identity(self, provided_google_id: str) -> None:
        """
        Verify google identity

        Args:
            provided_google_id (str): google user id

        Raises:
            GoogleUserNotVerifiedError: if google identity is not verified
        """
        if not self.google_user_id or self.google_user_id != provided_google_id:
            raise GoogleUserNotVerifiedError