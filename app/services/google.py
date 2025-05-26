from typing import Any

from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError as AuthError

from app.exceptions.google import GoogleAuthError
from app.utils.config import settings

class GoogleAPI:
    def __init__(self):
        self.client_id = settings.google_oauth_client_id
    
    def _verify_token(self, token: str) -> dict[str, Any]:
        """
        Verify JWT token 
        
        Args:
            token (str) - JWT token
        
        Returns
            dict: (str, Any)
        
        """
        return id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            self.client_id
        )
   
    
    def get_registration_info(self, token: str) -> dict[str, Any]:
        """
        Returns user data needed for registration

        Args:
            token (str): JWT 
        
        Returns:
            dict: Dictionary with following keys
                - user_id (str): unique user identifier at google
                - email (str): user e-mail adress
        """
        
        try:
            response = self._verify_token(token)
            
            return {
                "user_id": response["sub"],
                "email": response["email"]
            }
        except ValueError as e:
            raise GoogleAuthError("Invalid Token") from e
        except AuthError as e:
            raise GoogleAuthError("Authentication failed") from e
            