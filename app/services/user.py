from app.repositories.user import UserRepository
from app.models.users import Users
from app.services.google import GoogleAPI
from app.exceptions.domain.user import (
    LocalUserExistsError, 
    GoogleUserExistsError, 
    UserExistsError, 
    RegistrationError,
    UserNotFoundError,
)
from app.exceptions.domain.google import GoogleAuthError
from app.exceptions.infrastucture.repository import QueryExecutionError 
from app.exceptions.infrastucture.domain import UserServiceError

from app.utils import utils
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
    
    def retrieve_user(self, user_id: int) -> Users:
        """
        Retrieve user data 

        Args:
            user_id (int) - user id
        
        Returns:
            Users: user data 
        
        Raises:
            UserNotFoundError: user id not found in db
            UserServiceError: Server side err, while processing
        """

        try:
            user = self.repo.get_user(user_id)
            
            if user is None:
                raise UserNotFoundError
            
            return user
        except QueryExecutionError as e:
            raise UserServiceError("Unable to retrieve user data")
            