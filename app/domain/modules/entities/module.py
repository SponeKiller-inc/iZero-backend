from __future__ import annotations
from typing import Self
from datetime import datetime
from dataclasses import dataclass

from app.domain.shared.value_objects.period import ValidityPeriod

@dataclass
class Module:
    """
    Module entity.

    Attributes:
        id (int): Module ID.
        name (str): Module name.
        module_group_id (int): Module group ID.
        validity (ValidityPeriod): Validity period of the module.
    """
    id: int
    name: str
    module_group_id: int
    validity: ValidityPeriod

    @classmethod
    def create(
        self, 
        name: str, 
        module_group_id: int,
        valid_from: datetime,
    ) -> Self:
        """
        Create new module

        Args:
            name: Module name
            module_group_id: Module group ID
            valid_from: Validity period start
        
        Returns:
            New module
        """
        return Module(0, name, module_group_id, ValidityPeriod(valid_from))

    def is_active(self, current_time: datetime) -> bool:
        """
        Check if module is valid at current time

        Args:
            current_time: Current time
        
        Returns:
            True if module is valid, False otherwise
        """
        return self.validity.is_active(current_time)
