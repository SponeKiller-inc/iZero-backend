from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class SessionConstants:
    SESSION_EXPIRATION_MINUTES: Final[int] = 600
    
    