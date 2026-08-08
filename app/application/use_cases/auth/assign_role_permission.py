from app.application.security import authorize
from app.application.ports.time_provider import TimeProvider
from app.application.dto.auth.role_permission import AssignRolePermissionIn
from app.application.constants.use_case import UseCase
from app.application.exceptions.auth import AssignRolePermissionError
from app.domain.auth.value_object.permission_code import PermissionCode
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.entities.role import Role
from app.domain.shared.value_objects.entity import Entity
from app.domain.auth.entities.role_permission import RolePermission
from app.domain.auth.repositories.role_permission import RolePermissionRepository
from app.domain.shared.repositories.role import RoleRepository

class AssignRolePermission:

    def __init__(
        self,
        role_permission_repository: RolePermissionRepository,
        role_repository: RoleRepository,
        time_provider: TimeProvider
    ) -> None:
        """
        Initialize use-case

        Args:
            role_permission_repository: Role permission repository
            role_repository: Role repository
            time_provider: Time provider
        """
        self.role_permission_repository = role_permission_repository
        self.role_repository = role_repository
        self.time_provider = time_provider

    @authorize
    def execute(self, dto: AssignRolePermissionIn) -> None:
        """
        Assign permission to role.

        Args:
            dto: DTO carrying role and permission data.
        """
        use_case_name = dto.entity.upper() + '_' + dto.method.upper()

        if not UseCase.has_member(use_case_name):
            raise AssignRolePermissionError(f'Method {use_case_name} dos not exists for given entity')
        
        if not EntityType.has_member(dto.entity.upper()):
            raise AssignRolePermissionError('Entity dos not exists')
        
        role = self.role_repository.get(dto.role_id)
        if not role:
            raise AssignRolePermissionError('Role does not exist')

        entity = Entity(EntityType[dto.entity])

        permission_role = RolePermission.create_permission(
            role_id=dto.role_id,
            permission_code=PermissionCode(
                entity=entity,
                method=UseCase.get_member(use_case_name)
            ),
            current_time=self.time_provider.now()
        )

        self.role_permission_repository.save(permission_role)

