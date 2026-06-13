from app.application.exceptions.base import ApplicationError


class RegisterLocalError(ApplicationError):
    pass

class RegisterOAuthError(ApplicationError):
    pass

class UserNotFoundError(ApplicationError):
    pass