
from sqlalchemy import func, select

from app.domain.shared.entities.role import Role
from app.domain.shared.repositories.role import RoleRepository
from app.infrastructure.models.lookup.role import RoleModel
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AlchemyRoleRepository(BaseAlchemyRepository, RoleRepository):
    def get(self, role_id: int) -> Role | None:
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

    def save(self, role: Role) -> Role:
        """
        Create a role. If role.id is set, it is persisted as-is (used for seeding fixed IDs).

        Args:
            role (Role): data to create role

        Returns:
            Role: newly created role
        """

        model = RoleModel(id=role.id, name=role.name, disabled=role.disabled)
        self.db.add(model)
        self.db.flush()

        if role.id is not None:
            # explicit ID bypasses the identity sequence, so re-sync it to avoid future collisions
            self.db.execute(
                select(func.setval(func.pg_get_serial_sequence("roles", "id"), model.id))
            )

        self.db.refresh(model)

        return Role(id=model.id, name=model.name, disabled=model.disabled)
