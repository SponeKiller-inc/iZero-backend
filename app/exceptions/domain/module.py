from .errors import DomainError

class ModuleNotFoundError(DomainError):
    """Reserved for not found any module available for user"""
    def __init__(self):
        super().__init__("User has no active modules")