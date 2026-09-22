from app.application.constants.security import SecurityConstants
from app.application.constants.token import TokenConstants
from app.application.dto.auth.login_google import LoginGoogleIn, LoginGoogleOut
from app.application.exceptions.user import UserNotFoundError
from app.application.ports.access_token_generator import AccessTokenGenerator
from app.application.ports.identity_provider import IdentityProvider
from app.application.ports.time_provider import TimeProvider
from app.application.ports.token_generator import TokenGenerator
from app.domain.auth.entities.refresh_token import RefreshToken
from app.domain.auth.repositories.refresh_token import RefreshTokenRepository
from app.domain.users.repositories.user import UserRepository


class LoginGoogle:

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: RefreshTokenRepository,
        identity_provider: IdentityProvider,
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
            identity_provider: Identity provider
            access_token_generator: Access token generator
            refresh_token_generator: Token generator implementation used for refresh tokens
            csrf_token_generator: Token generator implementation used for CSRF tokens
            time_provider: Time provider
        """
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.identity_provider = identity_provider
        self.access_token_generator = access_token_generator
        self.refresh_token_generator = refresh_token_generator
        self.csrf_token_generator = csrf_token_generator
        self.time_provider = time_provider

    def execute(self, dto: LoginGoogleIn) -> LoginGoogleOut:
        """
        Authenticates a Google user and issues access, refresh and CSRF tokens
        for the session already initialized by SIDMiddleware.

        Args:
            dto: DTO carrying the Google identity token and the current session id.

        Returns:
            LoginGoogleOut: Access, refresh and CSRF tokens.

        Raises:
            IdentityProviderError: If the Google token is invalid.
            UserNotFoundError: If no user is registered for the Google account.
        """
        user_data = self.identity_provider.get_user_info(dto.token)

        user = self.user_repository.get_oauth_user(user_data.id)
        if user is None:
            raise UserNotFoundError("User not found")

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

        return LoginGoogleOut(
            access_token=access_token,
            access_token_type=SecurityConstants.BEARER_TOKEN_TYPE,
            refresh_token=refresh_token,
            refresh_token_expires_at=refresh_token_expires_at,
            csrf_token=csrf_token,
        )
