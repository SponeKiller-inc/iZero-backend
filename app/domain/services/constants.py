from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True, slots=True)
class UserServiceConstants:
    DEFAULT_USER_ROLE: int


SERVICE_CONST: Final = UserServiceConstants(
    DEFAULT_USER_ROLE=1
)