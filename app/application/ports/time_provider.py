from abc import ABC, abstractmethod
from datetime import datetime


class TimeProvider(ABC):
    """
    Defines contract for working with time,
    independently of the specific implementation.
    """
    @staticmethod
    @abstractmethod
    def now() -> datetime:
        """
        Returns the current UTC time
        
        Returns:
            datetime: current UTC time
        """
        ...

    @classmethod
    @abstractmethod
    def get_expiration(
        cls,
        minutes: int | None = None,
        days: int | None = None,
    ) -> datetime:
        """
        Calculates expiration using the class's own 'now' method

        Args:
            minutes (int): minutes to expiration (if 0, 
             expiration = now + 100ms)
    
        Returns:
            datetime: time of expiration (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
        """
        ...