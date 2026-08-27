from __future__ import annotations
from typing import Self
from datetime import datetime

from app.domain.shared.value_objects.period import ValidityPeriod

class ModuleGroup:
    """
    Module group entity.

    Attributes:
        id: Module group ID.
        name: Module group name.
        validity: Validity period of the module group.
    """
    def __init__(
        self, 
        id: int | None, 
        name: str, 
        validity: ValidityPeriod,
    ):
        self.id = id
        self.name = name
        self.validity = validity

    @classmethod
    def create(cls, name: str, valid_from: datetime) -> Self:
        """
        Create new module group

        Args:
            name: Module group name
            valid_from: Validity period start

        Returns:
            New module group
        """
        return cls(
            id=None,
            name=name,
            validity=ValidityPeriod(valid_from)
        )

    def is_active(self, current_time: datetime) -> bool:
        """
        Check if module group is valid at current time

        Args:
            current_time: Current time

        Returns:
            True if module group is valid, False otherwise
        """
        return self.validity.is_active(current_time)