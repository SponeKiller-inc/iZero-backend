from .errors import RepositoryError

class UserRoleNotAddedError(RepositoryError):
    """Reserved for not added user role"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to add user role, invalid data "
            "(user or role not existing)" + err
        )
        
class UserRoleNotUpdatedError(RepositoryError):
    """Reserved for not updated user role"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to update user role, invalid data "
            "(user or role not existing)" + err
        )