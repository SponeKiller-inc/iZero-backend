from passlib.context import CryptContext

from app.infrastructure.config import settings
from app.application.ports.password_hasher import PasswordHasher
from app.domain.exceptions.auth.password import InvalidHashFormatError

class PasswordHasher(PasswordHasher):
    """
    Password Hasher using passlib
    """
    
    _pwd_context = CryptContext(
    schemes=[settings.pwd_context_scheme],
    deprecated="auto"
    )

    def hash(self, password: str) -> str:
        """
        Hashes the given password.
        
        Args:
            password (str): The password to hash.
        
        Returns:
            str: The hashed password.
        """
        return self._pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifies the password against the hash.
        
        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password.
        
        Returns:
            bool: True if the password matches the hash, False otherwise.

        Raises:
            InvalidHashFormatError: If the hash has an invalid format.
        """
        try:
            return self._pwd_context.verify(password, hashed_password)
        except Exception as e:
            raise InvalidHashFormatError from e