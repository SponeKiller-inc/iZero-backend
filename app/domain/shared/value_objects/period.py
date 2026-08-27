from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Self

@dataclass(frozen=True)
class ValidityPeriod:
    """
    Represents the validity period of a session.

    Attributes:
        valid_from: The start of the validity period.
        valid_to: The end of the validity period.
         Defaults to 1.1.3000 if not provided

    Raises:
        ValueError: If valid_from is after valid_to.
    """
    valid_from: datetime
    valid_to: datetime = field(
        default_factory=lambda: datetime(3000, 1, 1, tzinfo=timezone.utc)
    )

    def __post_init__(self):
        if self.valid_from > self.valid_to:
            raise ValueError("valid_from must be before or equal to valid_to")

    def is_active(self, ref_time: datetime) -> bool:
        return self.valid_from <= ref_time <= self.valid_to
    
    def overlaps_with(self, other: Self) -> bool:
        """
        Checks if this validity period overlaps with another validity period.
        """
        return self.valid_from <= other.valid_to and self.valid_to >= other.valid_from