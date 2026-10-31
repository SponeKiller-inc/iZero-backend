from app.application.exceptions.base import ApplicationError


class PhoneValidationError(ApplicationError):
    """Phone violates the phone rules (incomplete phone, unknown calling code, number that is
    not a Czech 9-digit number)."""

class EmailValidationError(ApplicationError):
    """E-mail address has invalid format."""
