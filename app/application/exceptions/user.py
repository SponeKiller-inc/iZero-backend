from app.application.exceptions.base import ApplicationError


class RegisterLocalError(ApplicationError):
    pass

class RegisterOauthError(ApplicationError):
    pass

class UserNotFoundError(ApplicationError):
    pass

class UserCannotBeDeletedError(ApplicationError):
    pass

class UserDeleteForbiddenError(ApplicationError):
    pass

class UserModuleNotAssignedError(ApplicationError):
    pass