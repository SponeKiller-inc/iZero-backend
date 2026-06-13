from app.application.ports.time_provider import TimeProvider
from app.application.ports.password_hasher import PasswordHasher
from app.application.dto.user.registration import RegistrationLocalIn
from app.application.exceptions.user import RegisterLocalError
from app.domain.users.repositories.user import UserRepository
from app.domain.users.entities.user import User
from app.domain.users.entities.user_role import UserRole
from app.domain.users.exceptions.user import UserValidationError
from app.domain.users.repositories.user_role import UserRoleRepository

class RegisterLocal:

    def __init__(
        self,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        password_hasher: PasswordHasher,
        time_provider: TimeProvider,
    ) -> None:
        """
        Register user locally

        Args:
            user_repository: User repository
            user_role_repository: User role repository
            password_hasher: PasswordHasher
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.user_role_repository = user_role_repository
        self.password_hasher = password_hasher
        self.time_provider = time_provider
        
    def execute(self, dto: RegistrationLocalIn) -> None:
        """
        
        Args:
            dto: DTO carrying user data from any identity provider.
        
        Raises:
            RegisterLocalError: If user already exists or not valid data
        """
        
        if self.user_repository.exists_local(dto.email):
            raise RegisterLocalError("User already exists")

        try:
            user = User.create(
                email=dto.email,
                provider="local",
                password=self.password_hasher.hash(dto.password)
            )
        except UserValidationError as e:
            raise RegisterLocalError("User data is not valid") from e

        user = self.user_repository.save(user)

        user_role = UserRole.create_regular_role(
            user_id=user.id,
            current_time=self.time_provider.now()
        )
        
        self.user_role_repository.save(user_role)

