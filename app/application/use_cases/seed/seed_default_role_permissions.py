from app.application.constants.use_case import UseCase
from app.application.ports.time_provider import TimeProvider
from app.domain.auth.entities.role_permission import RolePermission
from app.domain.auth.repositories.role_permission import RolePermissionRepository
from app.domain.auth.value_object.permission_code import PermissionCode
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.constants.role_type import ADMIN_ROLE_ID, REGULAR_ROLE_ID
from app.domain.shared.value_objects.entity import Entity

# Permissions the default "user" role needs to use the app out of the box
DEFAULT_USER_PERMISSIONS: tuple[tuple[EntityType, UseCase], ...] = (
    (EntityType.USERS, UseCase.USERS_ASSIGN_MODULE),
    (EntityType.USERS, UseCase.USERS_RETRIEVE_MODULE),
)

# Permissions reserved for the admin role on top of the regular ones
DEFAULT_ADMIN_PERMISSIONS: tuple[tuple[EntityType, UseCase], ...] = (
    (EntityType.USERS, UseCase.USERS_DELETE),
)

DEFAULT_ROLE_PERMISSIONS: dict[int, tuple[tuple[EntityType, UseCase], ...]] = {
    REGULAR_ROLE_ID: DEFAULT_USER_PERMISSIONS,
    ADMIN_ROLE_ID: DEFAULT_ADMIN_PERMISSIONS,
}


class SeedDefaultRolePermissions:
    """Grants the default (regular/user) and admin roles their baseline permissions."""

    def __init__(
        self,
        role_permission_repository: RolePermissionRepository,
        time_provider: TimeProvider,
    ) -> None:
        self.role_permission_repository = role_permission_repository
        self.time_provider = time_provider

    def execute(self) -> None:
        now = self.time_provider.now()

        for role_id, permissions in DEFAULT_ROLE_PERMISSIONS.items():
            existing_codes = {
                (role_permission.permission_code.entity.type, role_permission.permission_code.method)
                for role_permission in self.role_permission_repository.get(role_id, now)
            }

            for entity_type, use_case in permissions:
                if (entity_type, use_case.value) in existing_codes:
                    continue

                permission = RolePermission.create_permission(
                    role_id=role_id,
                    permission_code=PermissionCode(entity=Entity(entity_type), method=use_case.value),
                    current_time=now,
                )
                self.role_permission_repository.save(permission)
