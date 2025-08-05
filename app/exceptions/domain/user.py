from .errors import DomainError

# Base user Error
class RegistrationError(DomainError):
    """Reserved for failed registration"""
    def __init__(self):
        super().__init__("Unable to register user at this time")

class UserNotFoundError(DomainError):
    """Reserved for user not found in system"""
    def __init__(self):
        super().__init__("User has not been found")

class UserRoleNotFoundError(DomainError):
    """Reserved for user role not found in system"""
    def __init__(self):
        super().__init__("User role has not been found")

class UserExistsError(DomainError):
    """Reserved for user exists in db"""
    pass

class UserNotVerifiedError(DomainError):
    """Rserved fo"""
    pass
class UserVerificationError(DomainError):
    """we were not able to verify user on our side err"""
    pass

# Specific user Error

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

class LocalUserNotVerifiedError(DomainError):
    """Reserved for login locally"""
    def __init__(self):
        super().__init__("E-mail or password is wrong")
        
class GoogleUserNotVerifiedError(DomainError):
    """Reserved for login via Google api"""
    def __init__(self):
        super().__init__("User does not exist")

class LocalUserVerificationError(DomainError):
    """Reserved for login locally for err on our side"""
    def __init__(self):
        super().__init__("Unable to verify user, please, try again later")

class GoogleUserVerificationError(DomainError):
    """Reserved for login via google for err on our side"""
    def __init__(self):
        super().__init__("Unable to verify token, please, try again later")