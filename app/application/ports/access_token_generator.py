from datetime import datetime
from typing import Protocol

from app.application.dto.auth.token import TokenPayload
from app.domain.users.constants.registration_source_type import RegistrationSourceType


class AccessTokenGenerator(Protocol):
    """Interface for access token provider"""

    def encode(
        self,
        user_id: int,
        provider: RegistrationSourceType,
        expires_at: datetime,
    ) -> str:
        """
        Encodes user id, provider and expiration time into JWT token.

        Args:
            user_id (int): id of user
            provider (RegistrationSourceType): how the user account was created
            expires_at (datetime): time when token expires
            
        Returns:
            str: encoded token
        """
        ...
        
    def decode(self, token: str) -> TokenPayload: 
        """
        Decodes JWT token and returns user id.
        
        Args:
            token (str): token to decode
            
        Returns:
            TokenPayload: payload of token
            
        Raises:
            AccessTokenProviderError: If token is invalid
        """
        ...