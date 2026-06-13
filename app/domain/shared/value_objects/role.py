from dataclasses import dataclass

from app.domain.shared.constants.role_type import RoleType

@dataclass(frozen=True)
class Role:
    """
    Represents the role of a user.

    Attributes:
        type: The type of the role.
    """
    type: RoleType