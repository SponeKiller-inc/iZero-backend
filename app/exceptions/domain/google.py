from .errors import DomainError

class GoogleAPIError(DomainError):
    """General exception for google apis"""

class GoogleAuthError(GoogleAPIError):
    """Raised when the JWT token has not been validated."""
