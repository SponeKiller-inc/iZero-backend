from typing import Protocol

class PasswordHasher(Protocol):
    """
    Interface for working with passwords.
    """

    def hash(self, password: str) -> str:
        """
        Creates a secure hash from a text password.
        
        Args:
            password (str): password
        
        Returns:
            str: hash
        """
        ...

    def verify(self, password: str, hashed_password: str) -> bool:
        """
        Verifies that the password matches the stored hash.
        
        Args:
            password (str): password
            hashed_password (str): hashed password
        
        Returns:
            bool: true = hash and password are identical
        
        Raises:
            InvalidHashFormatError: If the hash has an invalid format.
        """
        ...