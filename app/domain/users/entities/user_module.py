from datetime import datetime

from app.domain.shared.value_objects.period import ValidityPeriod

class UserModule:
    """
    Represents a module assigned to a user.
    """
    def __init__(self, user_module_id: int, module_id: int, validity: ValidityPeriod):
        self.id = user_module_id
        self.module_id = module_id
        self.validity = validity

    def is_active(self, current_time: datetime) -> bool:
        """Check if module is active at the given time.
        Args:
            current_time: The time to check.
        Returns:
            True if the module is active, False otherwise.
        """
        return self.validity.is_active(current_time)