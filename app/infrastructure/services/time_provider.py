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
    def get_expiration(
        cls,
        minutes: Optional[int] = None,
        days: Optional[int] = None,
    ) -> datetime:
        """
        Calculates expiration using the class's own 'now' method
        (if no minutes and no days, returns now + 100ms)

        Args:
            minutes (int): minutes to expiration
            days (int): days to expiration
        Returns:
            datetime: time of expiration (YYYY-MM-DD HH:MM:SS.ffffff±HH:MM)
        """
        base = cls.now()
        if not minutes and not days:
            return base + timedelta(milliseconds=100)
        return base + timedelta(minutes=minutes or 0, days=days or 0)
    
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