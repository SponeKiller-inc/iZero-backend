from dataclasses import dataclass
from datetime import datetime

@dataclass
class TokenPayload:
    """DTO carrying access token payload"""
    user_id: int
    expired_at: datetime