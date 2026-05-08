from typing import Optional
from app.domain.users.exceptions.user import (
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError
)
from app.application.ports.password_hasher import PasswordHasher

class Auth:
    def __init__(
        self,
        password_hash: Optional[str] = None,
    ):
        self.password_hash = password_hash

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
