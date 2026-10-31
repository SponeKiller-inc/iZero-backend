from dataclasses import dataclass
from typing import ClassVar

from app.domain.shared.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class RegistrationNumber(BaseValueObject):
    """
    Czech company registration number – 8 digits, the last one is a mod 11 check digit.

    Raises:
        ValueError: If the value is not exactly 8 digits (validated by BaseValueObject)
            or its check digit does not match.
    """
    length: ClassVar[int] = 8
    pattern: ClassVar[str] = r"^\d{8}$"

    def __post_init__(self):
        # Raises ValueError on invalid format, so the check digit is computed only for 8 digits
        super().__post_init__()

        # (11 - remainder) % 10 maps remainder 0 to 1 and remainder 1 to 0, as algorithm requires
        weighted_sum = sum(int(digit) * (8 - i) for i, digit in enumerate(self.value[:7]))
        check_digit = (11 - weighted_sum % 11) % 10

        if check_digit != int(self.value[7]):
            raise ValueError(f"Invalid check digit for {self.__class__.__name__}: {self.value}")

@dataclass(frozen=True)
class VatNumber(BaseValueObject):
    """Czech VAT ID – country code "CZ" followed by 8–10 digits."""
    length: ClassVar[int] = 12
    pattern: ClassVar[str] = r"^CZ\d{8,10}$"
