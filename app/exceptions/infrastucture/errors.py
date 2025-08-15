class DataAccessError(Exception):
    """Technical error, data access (DB, site, filesystem...)."""
    def __init__(self, err: str = ""):
        super().__init__("Repository, server-side error: " + err)
class ServiceError(Exception):
    """Technical error due to wich business logic has not been processed"""
    def __init__(self, err: str = ""):
        super().__init__("Service, server-side error: " + err)