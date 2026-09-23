from app.application.exceptions.base import ApplicationError


class IdentityProviderError(ApplicationError):
    """Specific error indicating that the identity provider has failed."""

class AccessTokenProviderError(ApplicationError):
    """Specific error indicating that the access token provider has failed."""

class InvalidHashFormatError(ApplicationError):
    """Specific error indicating that the hash has an invalid format."""

class AuthHashVerificationError(ApplicationError):
    """Specific error indicating that the auth hash verification has failed."""

class UnauthenticatedUserError(ApplicationError):
    """Specific error indicating that user is not authenticated."""

class InvalidCredentialsError(ApplicationError):
    """Specific error indicating that provided credentials are invalid."""

class AssignRolePermissionError(ApplicationError):
    """Specific error indicating that the role permission assignment has failed."""
