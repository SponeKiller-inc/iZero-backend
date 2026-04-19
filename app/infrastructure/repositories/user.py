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
    UserRoleNotUpdatedError,
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
        """

        return (
            self.db
                .query(Users)
                .filter(Users.id == user_id)
                .first()
        )
    
    def get_user_local(self, email: str) -> Users | None:
        """
        Retrieve user data registered locally

        Args:
            email (str): user e-mai

        Returns:
            Users or None: local user data 
        """

        return (
            self.db
                .query(Users)
                .filter(Users.email == email)
                .first()
        )
    
    def get_user_google(self, provider_user_id: str) -> Users | None:
        """
        Retrieve user data registered via google

        Args:
            provider_user_id (str): google user id

        Returns:
            Users or None: user data or None if user not found 
        """

        return (
            self.db
                .query(Users)
                .filter(
                    Users.provider_user_id == provider_user_id,
                    Users.provider == "google"
                )
                .first()
        )

    def get_user_role(self, user_id: int) -> str | None:
        """
        Get user role

        Args:
            user_id (int): user id

        Returns:
            str or None: user role or None if user not found 
        """

        return (
            self.db
                .query(RoleTypes.name)
                .join(UserRoles, RoleTypes.id == UserRoles.role_type_id)
                .filter(UserRoles.user_id == user_id)
                .scalar()
        )
        
    def add_user_role(self, new_user_role: UserRoles) -> UserRoles:
        """
        Add user role

        Args:
            new_user_role (UserRoles): user role data

        Returns:
            UserRoles: newly created user role 
        
        Raises:
            UserRoleNotAddedError - invalid data (user or role not existing) 
        """
        
        try:
            self.db.add(new_user_role)
            self.db.commit()
            return new_user_role
        except IntegrityError as e:
            raise UserRoleNotAddedError from e
    
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
        """
        
        try:
            user_role = self.db.query(UserRoles).filter(UserRoles.user_id == user_id).first()
            
            if user_role is None:
                raise UserRoleNotUpdatedError
            
            user_role.role_type_id = role_type_id
            self.db.commit()
            
            return user_role
        except IntegrityError as e:
            raise UserRoleNotUpdatedError from e
            
    def exists_local(self, email: str) -> bool:
        """
        Check if user created locally exists in db 

        Args:
            email (str): user e-mai

        Returns:
            bool: returns True if user exists
        """

        return (
            self.db
                .query(Users)
                .filter(Users.email == email)
                .first() is not None
        )
        
    def exists_google(self, provider_user_id: str, email: str) -> bool:
        """
        Check if user created via google exists in db

        Args:
            provider_user_id (str): User provider_user_id registered at google
            email (str): user e-mail

        Returns:
            bool: returns True if user exists
        """
        
        # Use exists if found via e-mail or provider_user_id
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
        
    def exists_user(self, user_id: int) -> bool:
        """
        Check if user exists in db

        Args:
            user_id (int): user id

        Returns:
            bool: returns True if user exists
        """

        return (
            self.db
                .query(Users)
                .filter(Users.id == user_id)
                .first() is not None
        )
    
    def create_user(self, new_user: Users) -> Users:
        """
        Create new user 

        Args:
            new_user (Users): new user data 

        Returns:
            Users: users model
        
        Raises:
            UserExistsError: User exists in db
        """
        
        try:
            self.db.add(new_user)
            self.db.commit()
            return new_user
        except IntegrityError as e:
            raise UserExistsError from e
        
    