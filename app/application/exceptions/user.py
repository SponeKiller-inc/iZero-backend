from app.application.exceptions.base import ApplicationError


class RegisterLocalError(ApplicationError):
    pass

class RegisterOauthError(ApplicationError):
    pass

class UserNotFoundError(ApplicationError):
    pass