from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class TokenConstants:
    ACCESS_TOKEN_EXPIRATION_MINUTES: Final[int] = 15
    REFRESH_TOKEN_EXPIRATION_MINUTES: Final[int] = 43200
    REFRESH_TOKEN_LENGTH: Final[int] = 32
    CSRF_TOKEN_LENGTH: Final[int] = 32
