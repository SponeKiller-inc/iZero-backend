from datetime import datetime
from typing import Protocol
from app.domain.users.entities.user_role import UserRole

class UserRoleRepository(Protocol):
    def get(self, user_id: int, ref_date: datetime) -> list[UserRole]:
        """
        Get user roles by user ID and reference date

        Args:
            user_id: User ID
            ref_date: Reference date
        Returns:
            List of user roles
        """
        ...
    
    def save(self, user_role: UserRole) -> UserRole:
        """
        Save user role

        Args:
            user_role: User role
        Returns:
            Saved user role
        """
        ...
