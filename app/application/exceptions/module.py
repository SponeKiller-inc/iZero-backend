from app.application.exceptions.base import ApplicationError


class ModuleNotFoundError(ApplicationError):
    pass

class ModuleGroupNotFoundError(ApplicationError):
    pass
