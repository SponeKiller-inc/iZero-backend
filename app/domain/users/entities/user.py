from __future__ import annotations
from typing import Self, Optional

from app.domain.users.value_objects.registration_source import RegistrationSource
from app.domain.users.constants.registration_source_type import RegistrationSourceType

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
        provider: RegistrationSource,
        password: Optional[str] = None, 
        provider_user_id: Optional[str] = None,        
    ):
        self.id = id
        self.email = email
        self.password = password
        self.provider_user_id = provider_user_id
        self.provider = provider

    @classmethod
    def create_local(
        cls,
        email: str,
        password: str
    ) -> Self:
        """
        Creates a new user locally.
        """
        return cls(
            id=0,
            email=email,
            provider=RegistrationSource(RegistrationSourceType.LOCAL),
            password=password,
        )
    
    @classmethod
    def create_oauth(
        cls,
        email: str,
        provider_user_id: str
    ) -> Self:
        """
        Creates a new user via oauth provider.
        """
        return cls(
            id=0,
            email=email,
            provider=RegistrationSource(RegistrationSourceType.OAUTH),
            provider_user_id=provider_user_id,
        )