from errors import DataAccessError

class QueryExecutionError(DataAccessError):
    """Reserved for query eror on db side (timeout, connection ...)"""
    pass
class CreateExecutionError(DataAccessError):
    """Reserved for create error on db side (timeout, connection ...)"""
    pass
class UpdateExecutionError(DataAccessError):
    """Reserved for update error on db side (timeout, connection ...)"""
    pass
class DeleteExecutionError(DataAccessError):
    """Reserved for delete error on db side (timeout, connection ...)"""
    pass