from typing import Self
from datetime import datetime

from app.domain.shared.entities.role import Role
from app.domain.auth.value_object.permission_code import PermissionCode
from app.domain.shared.value_objects.period import ValidityPeriod


class RolePermission:
    """
    Represents a role permission.
    
    Attributes:
        id: The role permission ID.
        role_id: The role id.
        permission_code: The permission code.
        validity: The validity period.
    """
    
    def __init__(
        self,   
        id: int, 
        role_id: int,
        permission_code: PermissionCode,
        validity: ValidityPeriod       
    ):
        self.id = id
        self.role_id = role_id
        self.permission_code = permission_code
        self.validity = validity

    @classmethod
    def create_permission(
        cls,
        role_id: int,
        permission_code: PermissionCode,
        current_time: datetime
    ) -> Self:
        """
        Creates a new role permission.

        Args:
            role_id: The role id.
            permission_code: The permission code.
            current_time: The current time.
        
        Returns:
            The new role permission.
        """
        return cls(
            id=0,
            role_id=role_id,
            permission_code=permission_code,
            validity=ValidityPeriod(valid_from=current_time)
        )
    
    def deactivate_permission(self, current_time: datetime) -> None:
        """
        Deactivates the role permission.

        Args:
            current_time: The current time.
        """
        self.validity.set_valid_to(current_time)