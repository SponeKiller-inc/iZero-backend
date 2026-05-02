from abc import ABC, abstractmethod

class PasswordHasher(ABC):
    """
    Domain Interface (Port).
    Defines contract for working with passwords,
    independently of the specific library.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """
        Creates a secure hash from a text password.
        
        Args:
            password (str): password
        
        Returns:
            str: hash
        """
        ...

    @abstractmethod
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