from .errors import ServiceError

class ModuleServiceError(ServiceError):
    """Reserved for service server side issue"""
    def __init__(self, err: str):
        super().__init__(err)