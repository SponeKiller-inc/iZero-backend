from __future__ import annotations
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True, slots=True)
class UserRole:
    """
    Value Object representing user role.
    """
    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Role ID must be positive integer.")
        
    @classmethod
    def default(cls) -> Self:
        return cls(value=1)

    def is_admin(self) -> bool:
        return self.value == 0