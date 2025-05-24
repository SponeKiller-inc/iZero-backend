class GoogleAPIError(Exception):
    """General exception for google apis"""

class GoogleAuthError(GoogleAPIError):
    """Exception jwt_token havent been validated"""
