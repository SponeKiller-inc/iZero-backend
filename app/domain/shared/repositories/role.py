from typing import Protocol, Optional
from app.domain.shared.entities.role import Role

class RoleRepository(Protocol):
    """Repository interface for Role entity."""
    
    def get(self, role_id: int) -> Optional[Role]:
        """
        Get a role by its ID.
        
        Args:
            role_id: The ID of the role.
            
        Returns:
            The Role entity if found, None otherwise.
        """
        ...
