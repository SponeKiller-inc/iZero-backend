from app.application.ports.identity_provider import IdentityProvider
from app.application.ports.time_provider import TimeProvider
from app.application.dto.user.registration import RegistrationOauthIn
from app.application.exceptions.user import RegisterOauthError
from app.domain.users.repositories.user import UserRepository
from app.domain.users.repositories.user_role import UserRoleRepository
from app.domain.users.entities.user import User
from app.domain.users.entities.user_role import UserRole

class RegisterOauth:

    def __init__(
        self,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
    ) -> None:
        """
        Register user via OAuth

        Args:
            user_repository: User repository
            user_role_repository: User role repository
            identity_provider: Identity provider
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.user_role_repository = user_role_repository
        self.identity_provider = identity_provider
        self.time_provider = time_provider

    def execute(self, dto: RegistrationOauthIn) -> None:
        """
        
        Args:
            dto: DTO carrying user data from any identity provider.
        
        Raises:
            RegisterOauthError: If user already exists
            IdentityProviderError: If identity provider has failed
        """

        user_data = self.identity_provider.get_user_info(dto.token)
        
        if self.user_repository.exists_oauth_user(user_data.id):
            raise RegisterOauthError("User already exists")

      
        user = User.create_oauth(
            email=user_data.email,
            provider_user_id=user_data.id,
        )

        user = self.user_repository.save(user)

        user_role = UserRole.create_regular_role(
            user_id=user.id,
            current_time=self.time_provider.now()
        )
        
        self.user_role_repository.save(user_role)
        