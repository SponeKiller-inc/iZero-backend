from typing import Protocol, Any

class IdentityProvider(Protocol):
    def get_registration_info(self, token: str) -> dict[str, Any]:
        """
        Returns basic registration information from the token.
        
        Args:
            token (str): token to verify
        
        Returns:
            dict[str, Any]: basic registration information
        
        Raises:
            IdentityProviderError: If the identity provider has failed.
        """
        ...