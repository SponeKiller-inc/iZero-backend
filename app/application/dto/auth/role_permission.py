from dataclasses import dataclass

from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.constants.role_type import RoleType
from app.application.constants.use_case import UseCase

@dataclass(frozen=True)
class AssignRolePermissionIn:
    """DTO for assigning a permission to a role."""
    role: RoleType
    entity: EntityType
    method: UseCase

