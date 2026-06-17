from typing import Optional
from typing import Protocol
from app.domain.users.entities.user_module import UserModule

class UserModuleRepository(Protocol):
    def get_user_module(
        self, 
        user_id: int, 
        module_id: int
    ) -> Optional[UserModule]:
        """
        Get user module
        
        Args:
            user_id: User ID
            module_id: Module ID
        
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
