from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class SessionEvent:
    event_type: str
    occurred_at: datetime