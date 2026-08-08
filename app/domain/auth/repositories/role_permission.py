from datetime import datetime
from typing import Protocol

from app.domain.auth.entities.role_permission import RolePermission

class RolePermissionRepository(Protocol):
    def get(self, role_id: int, ref_date: datetime) -> list[RolePermission]:
        """
        Get role permissions by role and reference date

        Args:
            role_id: role ide 
            ref_date: Reference date
        
        Returns:
            RolePermission if found
        """
        ...

    def save(self, role_permission: RolePermission) -> RolePermission:
        """
        Save new or existing role permission

        Args:
            role_permission: Role permission to save

        Returns:
            Updated or new role permission
        """
        ...