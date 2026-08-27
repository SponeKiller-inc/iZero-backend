from app.domain.shared.value_objects.period import ValidityPeriod
from datetime import datetime
from app.domain.auth.entities.role_permission import RolePermission
from app.infrastructure.repositories.base import BaseAlchemyRepository
from app.infrastructure.models.auth.role_permission import RolePermissionModel

class AlchemyRolePermissionRepository(BaseAlchemyRepository):
    def get(self, role_id: int, ref_date: datetime) -> list[RolePermission]:

        role_permission_models = (
            self.db
                .query(RolePermissionModel)
                .filter(
                    RolePermissionModel.role_id == role_id,
                    RolePermissionModel.valid_at(ref_date),
                )
                .all()
        )

        if not role_permission_models:
            return []

        return [
            RolePermission(
                id=role_permission.id,
                role_id=role_permission.role_id,
                permission_code=role_permission.permission_code,
                validity=ValidityPeriod(
                    role_permission.valid_from,
                    role_permission.valid_to,
                )
            )
            for role_permission in role_permission_models
        ]

    def save(self, role_permission: RolePermission) -> RolePermission:
        """
        Create or update RolePermission

        Args:
            role_permission (RolePermission): data to create or update
        
        Returns:
            RolePermission: newly created or updated role permission
        """
        if role_permission.id is None:
            return self._insert(role_permission)
        else:
            return self._update(role_permission)

    def _insert(self, role_permission: RolePermission) -> RolePermission:
        """
        Create RolePermission

        Args:
            role_permission (RolePermission): data to create role permission
        
        Returns:
            RolePermission: newly created role permission
        """
        role_permission_model = RolePermissionModel(
            role_id=role_permission.role_id,
            entity_type=role_permission.permission_code.entity.type,
            method=role_permission.permission_code.method,
            valid_from=role_permission.validity.valid_from,
            valid_to=role_permission.validity.valid_to,
        )
        self.db.add(role_permission_model)
        self.db.commit()
        self.db.refresh(role_permission_model)

        return RolePermission(
            id=role_permission_model.id,
            role_id=role_permission.role_id,
            permission_code=role_permission.permission_code,
            validity=role_permission.validity,
        )

    def _update(self, role_permission: RolePermission) -> RolePermission:
        """
        Update RolePermission

        Args:
            role_permission (RolePermission): data to update role permission
        
        Returns:
            RolePermission: updated role permission
        """
        updated_model = (
            self.db
                .query(RolePermissionModel)
                .filter(RolePermissionModel.id == role_permission.id)
                .first()      
        )

        updated_model.role_id = role_permission.role_id
        updated_model.entity_type = role_permission.permission_code.entity.type
        updated_model.method = role_permission.permission_code.method
        updated_model.valid_from = role_permission.validity.valid_from
        updated_model.valid_to = role_permission.validity.valid_to

        self.db.commit()
        self.db.refresh(updated_model)

        return RolePermission(
            id=updated_model.id,
            role_id=role_permission.role_id,
            permission_code=role_permission.permission_code,
            validity=role_permission.validity,
        )