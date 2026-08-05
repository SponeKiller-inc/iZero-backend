from datetime import datetime
from app.domain.auth.entities.role_permission import RolePermission
from app.domain.shared.value_objects.role import Role
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyRolePermission(BaseAlchemyRepository):
    def get(self, role: Role, ref_date: datetime) -> list[RolePermission]:

        role_permission_models = (
            self.db
                .query(RolePermissionModel)
                .filter(
                    RolePermissionModel.role == role,
                    RolePermissionModel.start_date <= ref_date,
                    RolePermissionModel.end_date >= ref_date,
                )
                .all()
        )

        if not role_permission_models:
            return []

        return [
            RolePermission(
                id=role_permission.id,
                role=role_permission.role,
                permission_code=role_permission.permission_code,
                start_date=role_permission.start_date,
                end_date=role_permission.end_date,
            )
            for role_permission in role_permission_models
        ]