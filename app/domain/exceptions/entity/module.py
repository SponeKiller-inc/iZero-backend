from .errors import DomainError

class UserModuleNotFoundError(DomainError):
    """Reserved for not found any module available for user"""
    def __init__(self, err: str = ""):
        super().__init__("User module/s not found" + err)

class UserModuleNotAssignedError(DomainError):
    """Reserved for not able to assign module to user"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to assign module to user" + err)

class ModuleGroupNotCreatedError(DomainError):
    """Reserved for not able to create module group"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to create module group, Invalid data" + err)
        
class ModuleNotCreatedError(DomainError):
    """Reserved for not able to create module"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to create module, Invalid data or "
            "module group not exists" + err
        )