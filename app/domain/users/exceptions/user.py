from app.domain.shared.exceptions.errors import DomainError


class UserValidationError(DomainError):
    """Reserved for user validation errors"""

class UserInactiveError(UserValidationError):
    """User has already been soft deleted"""

class UserProtectedError(UserValidationError):
    """User must not be deactivated (bootstrap admin or the acting user)"""

