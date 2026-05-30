from app.domain.shared.exceptions.errors import DomainError

class UserNotFoundError(DomainError):
    pass

class LocalUserNotFoundError(DomainError):
    """Reserved for login locally, which not exists"""
    def __init__(self, email: str):
        super().__init__(f"Local user with email '{email}' not found")

class GoogleUserNotFoundError(DomainError):
    """Reserved for login via google, which not exists"""
    def __init__(self, email: str, provider_user_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"provider_user_id '{provider_user_id}' not found"
        )

class LocalUserExistsError(DomainError):
    """Reserved for registration locally, which exists in system"""
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")

class GoogleUserExistsError(DomainError):
    """Reserved for registration via Google api, which exists in system"""
    def __init__(self, email: str, provider_user_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"provider_user_id '{provider_user_id}' already exists"
        )
