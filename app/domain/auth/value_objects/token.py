from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RefreshToken:
    session_id: int
    token: str
    expired_at: datetime

    def __post_init__(self):
        if self.expired_at <= datetime.now(self.expired_at.tzinfo):
            raise ValueError("Token vypršel nebo expirace není v budoucnosti.")