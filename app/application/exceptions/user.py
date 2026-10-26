from app.application.exceptions.base import ApplicationError


class RegisterLocalError(ApplicationError):
    pass

class RegisterOauthError(ApplicationError):
    pass

class UserNotFoundError(ApplicationError):
    pass

class UserModuleNotAssignedError(ApplicationError):
    pass

class PasswordChangeNotSupportedError(ApplicationError):
    """User account has no password (e.g. registered via oauth provider)."""

class InvalidCurrentPasswordError(ApplicationError):
    """Provided current password does not match the stored one."""

class PasswordTooShortError(ApplicationError):
    """New password is shorter than the minimal length."""

class PasswordTooLongError(ApplicationError):
    """New password is longer than the maximal length."""

class PasswordSameAsCurrentError(ApplicationError):
    """New password is the same as the current one."""

class PasswordConfirmationMismatchError(ApplicationError):
    """Password confirmation does not match the new password."""