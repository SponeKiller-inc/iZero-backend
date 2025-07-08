
from app.repositories.user import UserRepository
from app.repositories.token import TokenRepository
from app.services.token import TokenService
from app.services.google import GoogleAPI
from app.models.users import Users

from app.exceptions.domain.user import (
    UserVerificationError,
    UserNotVerifiedError,
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError,
    LocalUserVerificationError,
    GoogleUserVerificationError,
)
from app.exceptions.domain.token import AccessTokenServiceError
from app.exceptions.domain.google import GoogleAuthError
from app.exceptions.infrastucture.repository import QueryExecutionError

from app.utils import utils

class AuthService:
    def __init__(
        self, 
        user_repo: UserRepository,
        token_repo: TokenRepository,
        token_service: TokenService,
        google_api: GoogleAPI,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.token_service = token_service
        self.google_api = google_api
        
    def authenticate_user_local(self, email: str, password: str) -> int:
        """
        Verifies user locally registered

        Args:
            email (str): user email
            password (str): user password 
            
        Returns:
            int: user id
        
        Raises:
            LocalUserVerificationError: Error while verifying on our side
            LocalUserNotVerifiedError: Invalid credential / not found
        """
        try:
            if (self.user_repo.exists_local(email)):
                # User exists, verify password
                user: Users = self.user_repo.get_user_local(email)
                verified = utils.verify_hash(password, user.password)
            else:
                # User doesnt exist
                verified = False
        except QueryExecutionError as e:
            raise LocalUserVerificationError from e

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
            GoogleUserVerificationError: Error while verifying on our side
            GoogleUserNotVerifiedError: Invalid token / not found
        """
        # Validate token + verify existance of user 
        try:
            data = self.google_api.get_registration_info(jwt_token)
            user = self.user_repo.get_user_google(data["user_id"])
        except (GoogleAuthError, QueryExecutionError) as e:
            raise GoogleUserVerificationError from e
        
        if user is None:
            raise GoogleUserNotVerifiedError
        
        return user.id
    
    def authenticate_user_token(self, jwt_token: str) -> int:
        """
        Verifies user auth token

        Args:
            jwt_token (str) - access token
        
        Returns:
            int: user id
            
        Raises:
            UserVerificationError: Error while verifying on our side
            UserNotVerifiedError: Invalid token / not found
        """
        try:
            user_id = self.token_service.verify_access_token(jwt_token)
            user = self.user_repo.get_user(user_id)
            
            if user is None:
                raise UserNotVerifiedError("User does not exist")
            
            return user.id
        except AccessTokenServiceError as e:
            raise UserNotVerifiedError("Unable to validate token") from e
        except QueryExecutionError as e:
            raise UserVerificationError("Unable to verify user, server side error") from e