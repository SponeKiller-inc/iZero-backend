from datetime import datetime, timedelta, timezone
from typing import Optional

from app.domain.services.interfaces.clock import IClock

class Clock(IClock):
    """Utility service for UTC time."""
    
    @staticmethod
    def now() -> datetime:
        """
        Returns the current UTC time
        
        Returns:
            datetime: current UTC time
        """
        return datetime.now(timezone.utc)

    @classmethod
    def get_expiration(cls, minutes: Optional[int] = None) -> datetime:
        """
        Calculates expiration using the class's own 'now' method

        Args:
            minutes (int): minutes to expiration (if 0, 
             expiration = now + 100ms)
    
        Returns:
            datetime: time of expiration (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
        """
        now = cls.now()
        if minutes is None: return now
        delta = timedelta(minutes=minutes) if minutes > 0 else timedelta(milliseconds=100)
        return now + delta