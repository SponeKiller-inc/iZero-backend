from app.domain.repository.user import IUserRepository
from app.models.users import Users
from app.models.user_roles import UserRoles
from app.domain.entity.google import GoogleAPI
from .constants import SERVICE_CONST
from app.exceptions.domain.user import (
    LocalUserExistsError, 
    GoogleUserExistsError, 
    UserExistsError, 
    RegistrationError,
    UserNotFoundError,
    UserRoleNotFoundError,
)
from app.exceptions.repository.user import (
    UserRoleNotAddedError,
)
from app.exceptions.domain.google import GoogleAuthError
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
)
from app.exceptions.infrastucture.domain import UserServiceError

from app.application.ports.password_hasher import PasswordHasher

class UserService:
    def __init__(
        self, 
        repo: IUserRepository, 
        google_api: GoogleAPI,
        password_hasher: PasswordHasher
    ):
        self.repo = repo
        self.google_api = google_api
        self.password_hasher = password_hasher
        
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
    
        try:
            # Create user
            new_user = Users(
            email=email,
            password=self.password_hasher.hash(password),
            )
            new_user = self.repo.create_user(new_user)
            
            # Create user role
            new_user_role = UserRoles(
                user_id=new_user.id,
                role_type_id=SERVICE_CONST.DEFAULT_USER_ROLE
            )
            self.repo.add_user_role(new_user_role)
            
            return new_user
        except UserExistsError as e:
            raise LocalUserExistsError(email) from e
        except (
            RegistrationError, 
            UserRoleNotAddedError, 
            CreateExecutionError,
        )  as e:
            raise RegistrationError from e
        
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
            # Validate google user token
            data = self.google_api.get_registration_info(jwt_token)

            # Create new user
            new_user = Users(
                email=data["email"],
                provider_user_id=data["user_id"],
                provider='google'
            )
            
            new_user = self.repo.create_user(new_user)
            
            # Create user role
            new_user_role = UserRoles(
                user_id=new_user.id,
                role_type_id=SERVICE_CONST.DEFAULT_USER_ROLE
            )
            self.repo.add_user_role(new_user_role)
            
            return new_user
        except UserExistsError as e:
            raise GoogleUserExistsError(
                data["email"], 
                data["user_id"]
            ) from e
        except (
            RegistrationError, 
            UserRoleNotAddedError, 
            CreateExecutionError,
            GoogleAuthError,
        )  as e:
            raise RegistrationError from e
    
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
            raise UserServiceError("Unable to retrieve user data") from e
    
    def retrieve_user_role(self, user_id: int) -> str:
        """
        Retrieve user role 

        Args:
            user_id (int) - user id
        
        Returns:
            str - user role
        
        Raises:
            UserRoleNotFoundError: user role not found
            UserServiceError: Server side err, while processing
        """
        
        try:
            user_role = self.repo.get_user_role(user_id)
            
            if user_role is None:
                raise UserRoleNotFoundError
            
            return user_role
        except QueryExecutionError as e:
            raise UserServiceError("Unable to retrieve user role") from e
    
    def exists_user(self, user_id: int) -> bool:
        """
        Check if user exists in db

        Args:
            user_id (int): user id

        Returns:
            bool: returns True if user exists
        
        Raises:
            UserServiceError: Server side err, while processing
        """
        try:
            return self.repo.exists_user(user_id)
        except QueryExecutionError as e:
            raise UserServiceError("Unable to verify user existance") from e