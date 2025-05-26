class GoogleAPIError(Exception):
    """General exception for google apis"""

class GoogleAuthError(GoogleAPIError):
    """Raised when the JWT token has not been validated."""
