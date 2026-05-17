from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RefreshToken:
    session_id: int
    token: str
    expired_at: datetime