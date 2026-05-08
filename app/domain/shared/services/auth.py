from app.domain.repository.user import IUserRepository
from app.domain.repository.token import ITokenRepository
from app.domain.entity.token import TokenService
from app.domain.entity.google import GoogleAPI
from app.infrastructure.database.models.user.users import Users

from app.domain.users.exceptions.user import (
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError
)
from app.application.ports.password_hasher import PasswordHasher

class AuthService:
    def __init__(   
        self, 
        user_repo: IUserRepository,
        token_repo: ITokenRepository,
        token_service: TokenService,
        google_api: GoogleAPI,
        password_hasher: PasswordHasher,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service
        self.google_api = google_api
        self.password_hasher = password_hasher
        
    def authenticate_user_local(self, email: str, password: str) -> int:
        """
        Verifies user locally registered

        Args:
            email (str): user email
            password (str): user password 
            
        Returns:
            int: user id
        
        Raises:
            LocalUserNotVerifiedError: Invalid credential / not found
        """

        if (self.user_repo.exists_local(email)):
            # User exists, verify password
            user: Users = self.user_repo.get_user_local(email)
            verified = self.password_hasher.verify(password, user.password)
        else:
            # User doesnt exist
            verified = False

        if not verified:
            raise LocalUserNotVerifiedError
        
        return user.id
    
    def authenticate_user_google(self, jwt_token: str) -> int:
        """
        Verifies user registered via google api

        Args:
            jwt_token (str) - token which user got
            from google to get user data
        
        Returns:
            int: user id
            
        Raises:
            GoogleUserNotVerifiedError: Invalid token / not found
        """
        # Validate token + verify existance of user 
        data = self.google_api.get_registration_info(jwt_token)
        user = self.user_repo.get_user_google(data["user_id"])
        
        if user is None:
            raise GoogleUserNotVerifiedError
        
        return user.id