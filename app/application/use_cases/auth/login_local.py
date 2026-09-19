from app.application.ports.time_provider import TimeProvider
from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.access_token_generator import AccessTokenGenerator
from app.application.ports.token_generator import TokenGenerator
from app.application.constants.security import SecurityConstants
from app.application.constants.token import TokenConstants
from app.application.dto.auth.login_local import LoginLocalIn, LoginLocalOut
from app.application.exceptions.auth import InvalidCredentialsError
from app.domain.auth.entities.refresh_token import RefreshToken
from app.domain.auth.repositories.refresh_token import RefreshTokenRepository
from app.domain.users.repositories.user import UserRepository

class LoginLocal:

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        password_hasher: PasswordHasher,
        access_token_generator: AccessTokenGenerator,
        refresh_token_generator: TokenGenerator,
        csrf_token_generator: TokenGenerator,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            user_repository: User repository
            refresh_token_repository: Refresh token repository
            password_hasher: Password hasher
            access_token_generator: Access token generator
            refresh_token_generator: Token generator implementation used for refresh tokens
            csrf_token_generator: Token generator implementation used for CSRF tokens
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.password_hasher = password_hasher
        self.access_token_generator = access_token_generator
        self.refresh_token_generator = refresh_token_generator
        self.csrf_token_generator = csrf_token_generator
        self.time_provider = time_provider

    def execute(self, dto: LoginLocalIn) -> LoginLocalOut:
        """
        Authenticates a local user and issues access, refresh and CSRF tokens
        for the session already initialized by SIDMiddleware.

        Args:
            dto: DTO carrying login credentials and the current session id.

        Returns:
            LoginLocalOut: Access, refresh and CSRF tokens.

        Raises:
            InvalidCredentialsError: If email/password combination is invalid.
        """
        user = self.user_repository.get_local(dto.email)

        if (
            user is None
            or user.password is None
            or not self.password_hasher.verify(dto.password, user.password)
        ):
            raise InvalidCredentialsError("Invalid credentials")

        access_token = self.access_token_generator.encode(
            user.id,
            self.time_provider.get_expiration(
                minutes=TokenConstants.ACCESS_TOKEN_EXPIRATION_MINUTES,
            ),
        )

        refresh_token_expires_at = self.time_provider.get_expiration(
            minutes=TokenConstants.REFRESH_TOKEN_EXPIRATION_MINUTES,
        )
        refresh_token = self.refresh_token_generator.generate(TokenConstants.REFRESH_TOKEN_LENGTH)

        self.refresh_token_repository.save(
            RefreshToken.create_new(
                session_id=dto.session_id,
                token=refresh_token,
                expire_at=refresh_token_expires_at,
                current_time=self.time_provider.now(),
            )
        )

        csrf_token = self.csrf_token_generator.generate(TokenConstants.CSRF_TOKEN_LENGTH)

        return LoginLocalOut(
            access_token=access_token,
            access_token_type=SecurityConstants.BEARER_TOKEN_TYPE,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_token_expires_at,
            csrf_token=csrf_token,
        )
