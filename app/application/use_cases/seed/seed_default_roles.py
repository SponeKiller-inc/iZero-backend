from app.domain.shared.constants.role_type import (
    ADMIN_ROLE_ID,
    ADMIN_ROLE_NAME,
    REGULAR_ROLE_ID,
    REGULAR_ROLE_NAME,
)
from app.domain.shared.entities.role import Role
from app.domain.shared.repositories.role import RoleRepository


class SeedDefaultRoles:
    """Ensures the default (regular/user) and admin roles exist under their fixed IDs."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self.role_repository = role_repository

    def execute(self) -> None:
        """Create the default and admin roles under their fixed IDs if they don't exist yet."""
        for role_id, role_name in ((REGULAR_ROLE_ID, REGULAR_ROLE_NAME), (ADMIN_ROLE_ID, ADMIN_ROLE_NAME)):
            if self.role_repository.get(role_id) is not None:
                continue

            self.role_repository.save(Role(id=role_id, name=role_name))

