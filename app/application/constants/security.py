from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class SecurityConstants:
    AUTH_SECRET: Final[str] = 'e4b7c2a9d8f1e0b3c5a6d7f8e9a0b1c2'
    ACCESS_TOKEN_SECRET_KEY: Final[str] = 'a1f3c9e2b6d4f8017c5a9e3b2d6f4c81'
    BEARER_TOKEN_TYPE: Final[str] = 'bearer'
    ACCESS_TOKEN_ALGORITHM: Final[str] = 'HS256'
    
    