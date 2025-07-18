from .errors import DataAccessError

class QueryExecutionError(DataAccessError):
    """Reserved for query eror on db side (timeout, connection ...)"""
    def __init__(self, err: str):
        super().__init__(err)
class CreateExecutionError(DataAccessError):
    """Reserved for create error on db side (timeout, connection ...)"""
    def __init__(self, err: str):
        super().__init__(err)
class UpdateExecutionError(DataAccessError):
    """Reserved for update error on db side (timeout, connection ...)"""
    def __init__(self, err: str):
        super().__init__(err)
class DeleteExecutionError(DataAccessError):
    """Reserved for delete error on db side (timeout, connection ...)"""
    def __init__(self, err: str):
        super().__init__(err)