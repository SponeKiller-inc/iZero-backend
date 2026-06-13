from app.domain.shared.constants.role_type import RoleType
from typing import Optional
from typing import Protocol
from app.domain.users.entities.user_role import UserRole

class UserRoleRepository(Protocol):
    def get_user_role(self, user_id: int, role: RoleType) -> Optional[UserRole]:
        ...
    
    def save(self, user_role: UserRole) -> UserRole:
        ...
