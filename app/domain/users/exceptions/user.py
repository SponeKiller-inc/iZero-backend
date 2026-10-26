from app.domain.shared.exceptions.errors import DomainError


class UserValidationError(DomainError):
    """Reserved for user validation errors"""

class PasswordPolicyError(UserValidationError):
    """Password does not satisfy the password rules."""

class PasswordTooShortError(PasswordPolicyError):
    """Password is shorter than the minimal length."""

class PasswordTooLongError(PasswordPolicyError):
    """Password is longer than the maximal length."""

class UserHasNoPasswordError(UserValidationError):
    """User account has no password (e.g. registered via oauth provider)."""
