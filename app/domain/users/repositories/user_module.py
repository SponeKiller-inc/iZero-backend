from datetime import datetime
from typing import Protocol
from app.domain.users.entities.user_module import UserModule

class UserModuleRepository(Protocol):
    def get(self, user_id: int, ref_date: datetime) -> list[UserModule]:
        """
        Get all user modules by user ID
        
        Args:
            user_id: User ID
            ref_date: Reference date
        
        Returns:
            List of user modules
        """
        ...
    
    def get_module(
        self, 
        user_id: int, 
        module_id: int,
        ref_date: datetime,
    ) -> UserModule | None:
        """
        Get user module
        
        Args:
            user_id: User ID
            module_id: Module ID
            ref_date: Reference date
        
        Returns:
            User module entity
        """
        ...
    
    def save(self, user_module: UserModule) -> UserModule:
        """
        Save user module
        
        Args:
            user_module: User module entity
        
        Returns:
            User module entity
        """
        ...
