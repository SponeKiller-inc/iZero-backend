from typing import Protocol
from app.domain.users.entities.user import User

class UserRepository(Protocol):
    def get(self, user_id: int) -> User | None:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User entity if found, else None
        """
        ...

    def get_local(self, email: str) -> User | None:
        """
        Get local user by email
        
        Args:
            email: User email
            
        Returns:
            User entity if found, else None
        """
        ...

    def get_oauth_user(self, provider_user_id: str) -> User | None:
        """
        Get OAuth user by provider user ID
        
        Args:
            provider_user_id: Provider user ID
            
        Returns:
            User entity if found, else None
        """
        ...

    def exists_local(self, email: str) -> bool:
        """
        Check if local user exists by email
        
        Args:
            email: User email
            
        Returns:
            True if exists, else False
        """
        ...

    def exists_oauth_user(self, provider_user_id: str) -> bool:
        """
        Check if OAuth user exists by provider user ID
        
        Args:
            provider_user_id: Provider user ID
            
        Returns:
            True if exists, else False
        """
        ...

    def save(self, user: User) -> User:
        """
        Save user
        
        Args:
            user: User entity to save
            
        Returns:
            Saved User entity
        """
        ...