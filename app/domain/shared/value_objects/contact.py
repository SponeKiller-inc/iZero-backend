from dataclasses import dataclass
from typing import ClassVar

from app.domain.shared.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class PhoneNumber(BaseValueObject):
    """National phone number without the calling code; only Czech numbers (9 digits) are supported."""
    length: ClassVar[int] = 9
    pattern: ClassVar[str] = r"^\d{9}$"

@dataclass(frozen=True)
class EmailAddress(BaseValueObject):
    """E-mail address in a basic local@domain.tld format."""
    length: ClassVar[int] = 254
    pattern: ClassVar[str] = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
