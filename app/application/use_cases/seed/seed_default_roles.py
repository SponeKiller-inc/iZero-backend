from app.domain.shared.constants.role_type import REGULAR_ROLE_ID, REGULAR_ROLE_NAME
from app.domain.shared.entities.role import Role
from app.domain.shared.repositories.role import RoleRepository


class SeedDefaultRoles:
    """Ensures the default (regular/user) role exists, so newly registered users can be assigned to it."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self.role_repository = role_repository

    def execute(self) -> None:
        """Create the default role under the fixed REGULAR_ROLE_ID if it doesn't exist yet."""
        if self.role_repository.get(REGULAR_ROLE_ID) is not None:
            return

        role = Role(id=REGULAR_ROLE_ID, name=REGULAR_ROLE_NAME)
        self.role_repository.save(role)

