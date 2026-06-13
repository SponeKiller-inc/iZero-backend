from app.domain.users.entities.user_role import UserRole
from app.domain.shared.constants.role_type import RoleType
from app.infrastructure.models.user.user_roles import UserRoleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyUserRoleRepository(BaseAlchemyRepository):
    def get_user_role(self, user_id: int, role: RoleType) -> UserRole | None:
        return self.db.query(UserRoleModel).filter(UserRoleModel.user_id == user_id, UserRoleModel.role == role).first()
    
    def save(self, user_role: UserRole) -> UserRole:
        return self._save(user_role)