from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.users import Users
from app.exceptions.domain import UserExistsError, RegistrationError

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
        
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
        self.db.add(new_user)
        try:
            self.db.commit()
            return new_user
        except IntegrityError as e:
            raise UserExistsError from e
        except OperationalError as e:
            raise RegistrationError from e