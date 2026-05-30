from app.domain.shared.exceptions.errors import DomainError

class UserRoleNotFoundError(DomainError):
    """Reserved for user role not found in system"""
    def __init__(self, err: str = ""):
        super().__init__("User role has not been found" + err)