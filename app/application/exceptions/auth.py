from app.application.exceptions.base import ApplicationError

class IdentityProviderError(ApplicationError):
    """Specific error indicating that the identity provider has failed."""
    pass

class AccessTokenProviderError(ApplicationError):
    """Specific error indicating that the access token provider has failed."""
    pass

class InvalidHashFormatError(ApplicationError):
    """Specific error indicating that the hash has an invalid format."""
    pass

class AuthHashVerificationError(ApplicationError):
    """Specific error indicating that the auth hash verification has failed."""
    pass

class UnauthenticatedUserError(ApplicationError):
    """Specific error indicating that user is not authenticated."""
    pass

class AssignRolePermissionError(ApplicationError):
    """Specific error indicating that the role permission assignment has failed."""
    pass