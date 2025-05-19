
class DomainError(Exception):
    pass

class LocalUserNotFoundError(DomainError):
    """Reserved for login locally, which not exists"""
    def __init__(self, email: str):
        super().__init__(f"Local user with email '{email}' not found")

class GoogleUserNotFoundError(DomainError):
    """Reserver for login via google, which not exists"""
    def __init__(self, email: str, client_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"client_id '{client_id}' not found"
        )
        
class LocalUserExistsError(DomainError):
    """Reserved for registration, which exists in system"""
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")

class GoogleUserExistsError(DomainError):
    """Reserves for registration via Google api, which exists in system"""
    def __init__(self, email: str, client_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"client_id '{client_id}' already exists"
        )
