from dataclasses import dataclass

from app.domain.shared.value_objects.entity import Entity
from app.domain.auth.exceptions.permission_code import PermissionCodeError

@dataclass(frozen=True)
class PermissionCode:
    """
    Value Object representing permission code.
    """
    entity: Entity
    method: str

    def __post_init__(self) -> None:
        if not self.method.strip():
            raise PermissionCodeError("method must be non-empty string.")

        object.__setattr__(self, "method", self.method.strip().lower())