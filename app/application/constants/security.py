from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class SecurityConstants:
    AUTH_SECRET: Final[str] = 'e4b7c2a9d8f1e0b3c5a6d7f8e9a0b1c2'
    
    