from app.application.exceptions.base import ApplicationError

class IdentityProviderError(ApplicationError):
    """Specific error indicating that the identity provider has failed."""
    pass