from .errors import ServiceError

class ModuleServiceError(ServiceError):
    """Reserved for server side issue in ModuleService module"""
    def __init__(self, err: str = ""):
        super().__init__(err)
        
class UserServiceError(ServiceError):
    """Reserved for server side issue in UserService module"""
    def __init__(self, err: str = ""):
        super().__init__(err)