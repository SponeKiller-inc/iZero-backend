from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.users import Users
from app.models.user_roles import UserRoles
from app.models.role_types import RoleTypes
from app.exceptions.domain.user import (
    UserExistsError, 
    RegistrationError,
)
from app.exceptions.repository.user import (
    UserRoleNotAddedError,
)
from app.exceptions.infrastucture.repository import (
    QueryExecutionError,
    CreateExecutionError,
    UpdateExecutionError,
)


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_user(self, user_id: str) -> Users | None:
        """
        Retrieve user data by id

        Args:
            user_id (int): user id

        Returns:
            Users or None:  user data or None if no user found
            
        Raises:
            QueryExecutionError - server side error while execution
        """
        try: 
            return (
                self.db
                    .query(Users)
                    .filter(Users.id == user_id)
                    .first()
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to retrieve user data") from e
        
    
    def get_user_local(self, email: str) -> Users | None:
        """
        Retrieve user data registered locally

        Args:
            email (str): user e-mai

        Returns:
            Users or None: local user data 
            
        Raises:
            QueryExecutionError - server side error while execution
        """
        try: 
            return (
                self.db
                    .query(Users)
                    .filter(Users.email == email)
                    .first()
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to retrieve user data") from e
    
    def get_user_google(self, provider_user_id: str) -> Users | None:
        """
        Retrieve user data registered via google

        Args:
            provider_user_id (str): google user id

        Returns:
            Users or None: user data or None if user not found 
        
        Raises:
            QueryExecutionError - server side error while execution
        """
        try:
            return (
                self.db
                    .query(Users)
                    .filter(
                        Users.provider_user_id == provider_user_id,
                        Users.provider == "google"
                    )
                    .first()
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to retrieve user data") from e
    def get_user_role(self, user_id: int) -> str | None:
        """
        Get user role

        Args:
            user_id (int): user id

        Returns:
            str or None: user role or None if user not found 
        
        Raises:
            QueryExecutionError - server side error while execution
        """
        
        try:
            return (
                self.db
                    .query(RoleTypes.name)
                    .join(UserRoles, RoleTypes.id == UserRoles.role_type_id)
                    .filter(UserRoles.user_id == user_id)
                    .scalar()
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError("Failed to get user role") from e
        
    def add_user_role(self, new_user_role: UserRoles) -> UserRoles:
        """
        Add user role

        Args:
            new_user_role (UserRoles): user role data

        Returns:
            UserRoles: newly created user role 
        
        Raises:
            UserRoleNotAddedError - invalid data (user or role not existing) 
            CreateExecutionError - server side error while execution
        """
        
        try:
            self.db.add(new_user_role)
            self.db.commit()
            return new_user_role
        except IntegrityError as e:
            raise UserRoleNotAddedError from e
        except SQLAlchemyError as e:
            raise CreateExecutionError("Failed to add user role") from e
    
    def update_user_role(self, user_id: int, role_type_id: int) -> UserRoles:
        """
        Update user role

        Args:
            user_id (int): user id
            role_type_id (int): new user role id

        Returns:
            UserRoles: newly created user role 
        
        Raises:
            UserRoleNotUpdatedError - invalid data (user or role not exists)
            UpdateExecutionError - server side error while execution
        """
        
        try:
            user_role = self.db.query(UserRoles).filter(UserRoles.user_id == user_id).first()
            
            if user_role is None:
                raise UserRoleNotAddedError
            
            user_role.role_type_id = role_type_id
            self.db.commit()
            return user_role
        except IntegrityError as e:
            raise UserRoleNotAddedError from e
        except SQLAlchemyError as e:
            raise UpdateExecutionError("Failed to update user role") from e
            
    def exists_local(self, email: str) -> bool:
        """
        Check if user created locally exists in db 

        Args:
            email (str): user e-mai

        Returns:
            bool: returns True if user exists
        
        Raises:
            QueryExecutionError - server side error while execution
        """
        try:
            return (
                self.db
                    .query(Users)
                    .filter(Users.email == email)
                    .first() is not None
            )
        except SQLAlchemyError as e:
            raise QueryExecutionError(
                "Failed to verify local user existance"
            ) from e
        
    def exists_google(self, provider_user_id: str, email: str) -> bool:
        """
        Check if user created via google exists in db

        Args:
            provider_user_id (str): User provider_user_id registered at google
            email (str): user e-mail

        Returns:
            bool: returns True if user exists
        
        Raises:
            QueryExecutionError - server side error while execution
        """
        
        # Use exists if found via e-mail or provider_user_id
        try: 
            is_provider_user_id = (
                self.db
                    .query(Users)
                    .filter(
                        Users.provider_user_id == provider_user_id,
                        Users.provider == "google"
                    )
                    .first() is not None
            )
            
            is_email = (
                self.db
                    .query(Users)
                    .filter(Users.email == email)
                    .first() is not None
            )
        
            return is_provider_user_id or is_email
        except SQLAlchemyError as e:
            raise QueryExecutionError(
                "Failed to verify google user existance"
            ) from e
    
    def create_user(self, new_user: Users) -> Users:
        """
        Create new user 

        Args:
            new_user (Users): new user data 

        Returns:
            Users: users model
        
        Raises:
            UserExistsError: User exists in db
            RegistrationError: something went wrong with
                registration
        """
        
        try:
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except IntegrityError as e:
            raise UserExistsError from e
        except SQLAlchemyError as e:
            raise RegistrationError from e
        
        
    