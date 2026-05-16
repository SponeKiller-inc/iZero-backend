from datetime import datetime, timedelta, timezone
from typing import Optional

from app.application.ports.time_provider import TimeProvider

class SystemTimeProvider(TimeProvider):
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
    
    @staticmethod
    def from_timestamp(ts: float) -> datetime:
        """
        Converts timestamp to UTC datetime.

        Args:
            ts (float): Unix timestamp

        Returns:
            datetime: UTC datetime
        """
        return datetime.fromtimestamp(ts, tz=timezone.utc)