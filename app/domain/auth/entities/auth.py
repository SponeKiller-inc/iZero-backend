from typing import Optional
from app.domain.auth.exceptions.auth import (
    InvalidCredentialsError,
    IdentityNotVerifiedError
)
from app.application.ports.password_hasher import PasswordHasher

class Auth:
    def __init__(
        self,
        user_id: int,
        password_hash: Optional[str] = None,
    ):
        self.user_id = user_id
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
        if not self.password_hash:
            raise IdentityNotVerifiedError("Password is not set.")
            
        if not hasher.verify(password, self.password_hash):
            # Tady v budoucnu zavoláš: self._register_failed_attempt()
            raise InvalidCredentialsError("Invalid password.")
