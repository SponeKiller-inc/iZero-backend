from __future__ import annotations
from typing import Self
from datetime import datetime

from app.domain.shared.value_objects.period import ValidityPeriod
from app.domain.shared.constants.role_type import REGULAR_ROLE_ID

class UserRole:
    """
    Represents a role assigned to a user.

    Attributes:
        id (int): The ID of the user role.
        user_id (int): The ID of the user.
        role (Role): The role assigned to the user.
        validity (ValidityPeriod): The validity period of the user role.
    """
    def __init__(
        self,
        id: int | None,
        user_id: int,
        role_id: int,
        validity: ValidityPeriod
    ):
        self.id = id
        self.user_id = user_id
        self.role_id = role_id
        self.validity = validity

    @classmethod
    def create_regular_role(
        cls, 
        user_id: int, 
        current_time: datetime
    ) -> Self:
        """
        Factory method for quick creation of a regular role.

        Args:
            id (int): The ID of the user role.
            user_id (int): The ID of the user.
            validity (ValidityPeriod): The validity period of the user role.
        
        Returns:
            UserRole: The newly created user role.
        """
        return cls(
            id=None,
            user_id=user_id,
            role_id=REGULAR_ROLE_ID,
            validity=ValidityPeriod(current_time)
        )
    
    def is_active(self, current_time: datetime) -> bool:
        """Check if user_role is active at the given time.
        Args:
            current_time (datetime): The time to check.
        Returns:
            bool: True if the user_role is active, False otherwise.
        """
        return self.validity.is_active(current_time)