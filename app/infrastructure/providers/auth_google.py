from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

from app.application.dto.auth.identity_provider import IdentityProviderOut
from app.application.exceptions.auth import IdentityProviderError

class GoogleIdentityProvider:   
    def __init__(self, client_id: str):
        self.client_id = client_id

    def get_user_info(self, token: str) -> IdentityProviderOut:
        """
        Get user registration info from Google

        Args:
            token (str): JWT token from Google

        Returns:
            IdentityProviderOut: User registration info

        Raises:
            IdentityProviderError: If invalid token or something else goes wrong
        """


        try:
            response = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.client_id
            )
            
            return IdentityProviderOut(
                id=response["sub"],
                email=response["email"]
            )
        except ValueError as e:
            raise IdentityProviderError("Google token is invalid") from e
        except GoogleAuthError as e:
            raise IdentityProviderError("Google authentication failed") from e