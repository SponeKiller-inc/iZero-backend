from app.application.exceptions.base import ApplicationError

class IdentityProviderError(ApplicationError):
    """Specific error indicating that the identity provider has failed."""
    pass

class AccessTokenProviderError(ApplicationError):
    """Specific error indicating that the access token provider has failed."""
    pass