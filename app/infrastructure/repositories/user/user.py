from sqlalchemy.orm import Session

from app.domain.users.entities.user import User
from app.infrastructure.models.user.users import UserModel
from app.infrastructure.repositories.base import BaseAlchemyRepository

class AlchemyUserRepository(BaseAlchemyRepository):
    def get(self, user_id: str) -> User | None:
        """
        Retrieve user data by id

        Args:
            user_id (int): user id

        Returns:
            User or None:  user data or None if no user found
        """

        user_model = (
            self.db
                .query(UserModel)
                .filter(UserModel.id == user_id)
                .first()
        )

        if user_model is None:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            provider=user_model.provider,
            password=user_model.password,
            provider_user_id=user_model.provider_user_id,
        )
    
    def get_local(self, email: str) -> User | None:
        """
        Retrieve user data registered locally

        Args:
            email (str): user e-mai

        Returns:
            User or None: local user data 
        """

        user_model = (
            self.db
                .query(UserModel)
                .filter(UserModel.email == email)
                .first()
        )

        if user_model is None:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            provider=user_model.provider,
            password=user_model.password,
            provider_user_id=user_model.provider_user_id,
        )
    
    def get_oauth_user(self, provider_user_id: str) -> User | None:
        """
        Retrieve user data registered via oauth provider

        Args:
            provider_user_id (str): oauth provider user id

        Returns:
            User or None: user data or None if user not found 
        """

        user_model = (
            self.db
                .query(UserModel)
                .filter(UserModel.provider_user_id == provider_user_id)
                .first()
        )

        if user_model is None:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            provider=user_model.provider,
            password=user_model.password,
            provider_user_id=user_model.provider_user_id,
        )
            
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
                .query(UserModel)
                .filter(UserModel.email == email)
                .first() is not None
        )
        
    def exists_oauth_user(self, provider_user_id: str) -> bool:
        """
        Check if user created via oauth provider exists in db

        Args:
            provider_user_id (str): User provider_user_id registered 
                at oauth provider

        Returns:
            bool: returns True if user exists
        """
    
        return (
            self.db
                .query(UserModel)
                .filter(UserModel.provider_user_id == provider_user_id)
                .first() is not None
        )
    
    def save(self, user: User) -> User:
        """
        Create or update User

        Args:
            user (User): data to create or update user
        
        Returns:
            User: data newly created or updated user
        """
         
        if user.id is None:
            return self._insert(user)
        else:
            return self._update(user)
        

    def _insert(self, user: User) -> User:
        """
        Create user

        Args:
            user (User) - data tu create user
        
        Returns:
            User: data newly created user
        """
               
        user_model = UserModel(
            email=user.email,
            provider=user.provider,
            password=user.password,
            provider_user_id=user.provider_user_id,
        )
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return User(
            id=user_model.id,
            email=user_model.email,
            provider=user_model.provider,
            password=user_model.password,
            provider_user_id=user_model.provider_user_id, 
        )

    def _update(self, user: User) -> User:
        """
        Update user

        Args:
            user (User) - data to update user
        
        Returns:
            User: data updated user
        """

        updated_user = (
            self.db
                .query(UserModel)
                .filter(UserModel.id == user.id)
                .first()      
        )

        updated_user.email = user.email
        updated_user.provider = user.provider
        updated_user.password = user.password
        updated_user.provider_user_id = user.provider_user_id

        self.db.commit()
        self.db.refresh(updated_user)

        return User(
            id=updated_user.id,
            email=updated_user.email,
            provider=updated_user.provider,
            password=updated_user.password,
            provider_user_id=updated_user.provider_user_id, 
        )