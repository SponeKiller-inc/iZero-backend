from dataclasses import dataclass, field
from typing import ClassVar

from app.domain.users.exceptions.user import (
    PasswordTooLongError,
    PasswordTooShortError,
)


@dataclass(frozen=True)
class Password:
    """
    Value Object representing a plain text password that satisfies the password rules.
    """
    value: str = field(repr=False)
    min_length: ClassVar[int] = 8
    max_length: ClassVar[int] = 128

    def __post_init__(self):
        if len(self.value) < self.min_length:
            raise PasswordTooShortError(
                f"Password is too short (min {self.min_length})"
            )

        if len(self.value) > self.max_length:
            raise PasswordTooLongError(
                f"Password is too long (max {self.max_length})"
            )