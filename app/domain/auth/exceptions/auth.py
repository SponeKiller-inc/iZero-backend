from app.domain.exceptions.errors import DomainError

class InvalidCredentialsError(DomainError):
    """
    Error raised when invalid credentials are provided.
    """
    pass

class IdentityNotVerifiedError(DomainError):
    """
    Error raised when identity is not verified.
    """
    pass