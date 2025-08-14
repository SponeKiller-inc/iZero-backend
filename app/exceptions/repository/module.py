from .errors import RepositoryError

class UserModuleNotAddedError(RepositoryError):
    """Reserved from not added module to user"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to add module to user, invalid "
            "data or module not exists" + err
        )
        
class ModuleGroupNotAddedError(RepositoryError):
    """Reserved from not added module group"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to add module group, invalid data" + err
        )

class ModuleNotAddedError(RepositoryError):
    """Reserved from not added module"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to add module, invalid data or "
            "module group not exists" + err
        )
        
