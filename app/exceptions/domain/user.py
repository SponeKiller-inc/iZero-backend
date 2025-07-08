from .errors import DomainError

# Base user Error
class RegistrationError(DomainError):
    """Reserved for failed registration"""
    def __init__(self):
        super().__init__("Unable to register user at this time")

class UserNotFoundError(DomainError):
    """Base error: user not found in system"""
    pass

class UserExistsError(DomainError):
    """Base error: user exists in system"""
    pass

class UserNotVerifiedError(DomainError):
    """Base error: user exists in system"""
    pass
class UserVerificationError(DomainError):
    """Base error: we were not able to verify user on our side err"""
    pass

# Specific user Error

class LocalUserNotFoundError(UserNotFoundError):
    """Reserved for login locally, which not exists"""
    def __init__(self, email: str):
        super().__init__(f"Local user with email '{email}' not found")

class GoogleUserNotFoundError(UserNotFoundError):
    """Reserved for login via google, which not exists"""
    def __init__(self, email: str, provider_user_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"provider_user_id '{provider_user_id}' not found"
        )

class LocalUserExistsError(UserExistsError):
    """Reserved for registration locally, which exists in system"""
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")

class GoogleUserExistsError(UserExistsError):
    """Reserved for registration via Google api, which exists in system"""
    def __init__(self, email: str, provider_user_id: str):
        super().__init__(
            f"Google user with email '{email}' and "
            f"provider_user_id '{provider_user_id}' already exists"
        )

class LocalUserNotVerifiedError(UserNotVerifiedError):
    """Reserved for login locally"""
    def __init__(self):
        super().__init__("E-mail or password is wrong")
        
class GoogleUserNotVerifiedError(UserNotVerifiedError):
    """Reserved for login via Google api"""
    def __init__(self):
        super().__init__("User does not exist")

class LocalUserVerificationError(UserVerificationError):
    """Reserved for login locally for err on our side"""
    def __init__(self):
        super().__init__("Unable to verify user, please, try again later")

class GoogleUserVerificationError(UserVerificationError):
    """Reserved for login via google for err on our side"""
    def __init__(self):
        super().__init__("Unable to verify token, please, try again later")