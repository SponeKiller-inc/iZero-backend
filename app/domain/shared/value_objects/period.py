from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ValidityPeriod:
    """
    Represents the validity period of a session.

    Attributes:
        valid_from: The start of the validity period.
        valid_to: The end of the validity period.

    Raises:
        ValueError: If valid_from is after valid_to.
    """
    valid_from: datetime
    valid_to: datetime

    def __post_init__(self):
        if self.valid_from > self.valid_to:
            raise ValueError("valid_from must be before or equal to valid_to")

    def is_active(self, ref_time: datetime) -> bool:
        return self.valid_from <= ref_time <= self.valid_to