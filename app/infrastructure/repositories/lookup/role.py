from typing import Optional
from app.infrastructure.repositories.base import BaseAlchemyRepository
from app.domain.shared.repositories.role import RoleRepository
from app.domain.shared.entities.role import Role
from app.infrastructure.models.lookup.role import RoleModel

class AlchemyRoleRepository(BaseAlchemyRepository, RoleRepository):
    def get(self, role_id: int) -> Optional[Role]:
        """
        Get a role by its ID

        Args:
            role_id (int): role id

        Returns:
            Role or None: role entity or None if no role found
        """
        
        model = self.db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if not model:
            return None
        return Role(id=model.id, name=model.name, disabled=model.disabled)
