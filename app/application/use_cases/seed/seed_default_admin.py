from app.application.constants.security import SecurityConstants
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.time_provider import TimeProvider
from app.domain.users.constants.admin import ADMIN_EMAIL
from app.domain.users.entities.user import User
from app.domain.users.entities.user_role import UserRole
from app.domain.users.repositories.user import UserRepository
from app.domain.users.repositories.user_role import UserRoleRepository


class SeedDefaultAdmin:
    """Ensures the bootstrap admin account exists. The only caller allowed to invoke User.create_admin."""

    def __init__(
        self,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        password_hasher: PasswordHasher,
        time_provider: TimeProvider,
    ) -> None:
        self.user_repository = user_repository
        self.user_role_repository = user_role_repository
        self.password_hasher = password_hasher
        self.time_provider = time_provider

    def execute(self) -> None:
        """Creates the admin user under the fixed ADMIN_EMAIL if it doesn't exist yet."""
        if self.user_repository.exists_local(ADMIN_EMAIL):
            return

        password = SecurityConstants.ADMIN_PASSWORD
        admin = User.create_admin(password=self.password_hasher.hash(password))
        admin = self.user_repository.save(admin)

        admin_role = UserRole.create_admin_role(
            user_id=admin.id,
            current_time=self.time_provider.now()
        )
        self.user_role_repository.save(admin_role)

        regular_role = UserRole.create_regular_role(
            user_id=admin.id,
            current_time=self.time_provider.now()
        )
        self.user_role_repository.save(regular_role)


