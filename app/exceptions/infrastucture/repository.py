from errors import DataAccessError

class QueryExecutionError(DataAccessError):
    """Failed Select execution (syntax, deadlock, timeout...)."""
    pass