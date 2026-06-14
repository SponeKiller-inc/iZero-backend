from typing import Protocol
from app.application.dto.auth.identity_provider import IdentityProviderOut

class IdentityProvider(Protocol):
    def get_user_info(self, token: str) -> IdentityProviderOut:
        """
        Returns basic user information from the token.
        
        Args:
            token (str): token to verify
        
        Returns:
            IdentityProviderOut: basic user information
        
        Raises:
            IdentityProviderError: If the identity provider has failed.
        """
        ...