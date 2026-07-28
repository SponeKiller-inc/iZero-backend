from app.application.exceptions.auth import AssignRolePermissionError
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.constants.role_type import RoleType
from app.domain.shared.value_objects.role import Role
from app.domain.shared.value_objects.entity import Entity
from app.application.security import authorize
from app.domain.auth.repositories.role_permission import RolePermissionRepository
from app.application.ports.time_provider import TimeProvider
from app.application.dto.auth.role_permission import AssignRolePermissionIn
from app.application.constants.use_case import UseCase


class AssignRolePermission:

    def __init__(
        self,
        role_permission_repository: RolePermissionRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            role_permission_repository: Role permission repository
            time_provider: Time provider
        """
        self.role_permission_repository = role_permission_repository
        self.time_provider = time_provider

    @authorize
    def execute(self, dto: AssignRolePermissionIn) -> None:
        """
        Assign permission to role.

        Args:
            dto: DTO carrying role and permission data.
        """

        # 1. vytvoříme instanci role
        # 1 vytvoříme instanci entity
        # 2. zvalidujeme zda metoda existuje
        # 3. vytvoříme entitu PermissionRole
        # 4. uložíme permission role 

        if not UseCase.has_member(dto.entity.upper + '_' + dto.method.upper):
            raise AssignRolePermissionError('Method dos not exists for given entity')

        role = Role(RoleType[dto.role])
        entity = Entity(EntityType[dto.entity])

