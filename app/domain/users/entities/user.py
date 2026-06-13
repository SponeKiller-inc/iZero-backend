from __future__ import annotations
from typing import Self, Optional

class User:
    """
    Represents a user.
    
    Attributes:
        id: The user ID.
        email: The user email.
        password: The user password.
        provider_user_id: The provider user ID.
        provider: The provider.
    """
    
    def __init__(
        self,   
        id: int, 
        email: str,
        provider: str,
        password: Optional[str] = None, 
        provider_user_id: Optional[str] = None,        
    ):
        self.id = id
        self.email = email
        self.password = password
        self.provider_user_id = provider_user_id
        self.provider = provider

    @classmethod
    def create(
        cls,
        email: str,
        provider: str,
        password: Optional[str] = None,
        provider_user_id: Optional[str] = None,
    ) -> Self:
        """
        Creates a new user instance with validation rules.
        """
        if provider == "local" and not password:
            raise ValueError("password must be not empty")

        if provider != "local":
            if not provider_user_id:
                raise ValueError("provider_user_id must be not empty")
            if password:
                raise ValueError("password must be empty")

        return cls(
            id=0,
            email=email,
            provider=provider,
            password=password,
            provider_user_id=provider_user_id,
        )