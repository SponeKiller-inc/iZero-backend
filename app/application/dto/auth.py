from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RegistrationInfo:
    """DTO carrying user data from any identity provider."""
    user_id: str
    email: str

@dataclass
class TokenPayload:
    """DTO carrying access token payload"""
    user_id: int
    expired_at: datetime