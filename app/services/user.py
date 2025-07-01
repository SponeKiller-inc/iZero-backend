from app.repositories.user import UserRepository
from app.models.users import Users
from app.exceptions.domain.user import (
    LocalUserExistsError, 
    GoogleUserExistsError, 
    UserExistsError, 
    RegistrationError,
    LocalUserNotVerifiedError,
    GoogleUserNotVerifiedError,
    LocalUserVerificationError,
    GoogleUserVerificationError,
)
from app.exceptions.domain.google import GoogleAuthError
from app.exceptions.infrastucture.repository import QueryExecutionError
from app.utils import utils
from app.services.google import GoogleAPI
class UserService:
    def __init__(
        self, 
        repo: UserRepository, 
        google_api: GoogleAPI
    ):
        self.repo = repo
        self.google_api = google_api
        
    def register_user_local(
        self, 
        email: str,  
        password: str
    ) -> Users:
        
        """
        Registration user locally (without 3rd party api)

        Args:
            email (str): user e-mail
            password (str): user password
        
        Returns:
            Users: Object newly created user
        
        Raises:
            LocalUserExistsError: User with e-mail exists
            RegistrationError: If something went wrong while
                creating user in db
        """

        new_user = Users(
            email=email,
            password=utils.hash_password(password),
        )
    
        try:
            return self.repo.create_user(new_user)
        except UserExistsError as e:
            raise LocalUserExistsError(email) from e
        except RegistrationError:
            raise
        
    def register_user_google(
        self, 
        jwt_token
    ) -> Users:
    
        """
        Registration user via Google API

        Args:
            jwt_token (str) - token which user got
            from google to get user data
        
        Returns:
            Users: Object newly created user
        
        Raises:
            GoogleUserExistsError: user with e-mail or provider_user_id
                already exists
            RegistrationError: If something went wrong while
                creating user in db
        """
        try:
            data = self.google_api.get_registration_info(jwt_token)
        except GoogleAuthError as e:
            raise RegistrationError from e
        

        new_user = Users(
            email=data["email"],
            provider_user_id=data["user_id"],
            provider='google'
        )

        try:
            return self.repo.create_user(new_user)
        except UserExistsError as e:
            raise GoogleUserExistsError(
                data["email"], 
                data["user_id"]
            ) from e
        except RegistrationError:
            raise
    
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
            if (self.repo.exists_local(email)):
                # User exists, verify password
                user: Users = self.repo.get_user_local(email)
                verified = utils.verify_hash(password, user.password)
            else:
                # User doesnt exist
                verified = False
        except QueryExecutionError as e:
            raise LocalUserVerificationError from e

        if not verified:
            raise LocalUserNotVerifiedError
        
        return user.id
    
    def authentiace_user_google(self, jwt_token: str) -> int:
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
            user = self.repo.get_user_google(data["user_id"])
        except (GoogleAuthError, QueryExecutionError) as e:
            raise GoogleUserVerificationError from e
        
        if user is None:
            raise GoogleUserNotVerifiedError
        
        return user.id