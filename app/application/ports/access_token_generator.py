from typing import Protocol
from datetime import datetime

from app.application.dto.auth.token import TokenPayload

class AccessTokenGenerator(Protocol):
    """Interface for access token provider"""
    
    def encode(self, user_id: int, expires_at: datetime) -> str: 
        """
        Encodes user id and expiration time into JWT token.
        
        Args:
            user_id (int): id of user
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