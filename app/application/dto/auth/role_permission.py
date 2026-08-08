from dataclasses import dataclass

@dataclass(frozen=True)
class AssignRolePermissionIn:
    """DTO for assigning a permission to a role."""
    role_id: int
    entity: str
    method: str

