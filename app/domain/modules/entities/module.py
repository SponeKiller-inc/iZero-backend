from datetime import datetime
from app.domain.shared.value_objects.period import ValidityPeriod
from dataclasses import dataclass

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

    def is_active(self, current_time: datetime) -> bool:
        """
        Check if module is valid at current time

        Args:
            current_time: Current time
        
        Returns:
            True if module is valid, False otherwise
        """
        return self.validity.is_active(current_time)
