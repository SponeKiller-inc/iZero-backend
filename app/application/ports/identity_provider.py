from typing import Protocol
from app.application.dto.auth import RegistrationInfo

class IdentityProvider(Protocol):
    def get_registration_info(self, token: str) -> RegistrationInfo:
        """
        Returns basic registration information from the token.
        
        Args:
            token (str): token to verify
        
        Returns:
            RegistrationInfo: basic registration information
        
        Raises:
            IdentityProviderError: If the identity provider has failed.
        """
        ...