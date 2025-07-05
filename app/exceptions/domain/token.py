from .errors import DomainError

class TokenServiceError(DomainError):
    """Unable to generate token"""
    
class AccessTokenServiceError(DomainError):
    """Reserved for access token error"""
    def __init__(self):
        super().__init__(f"Unable to generate access token")
    
class RefreshTokenServiceError(DomainError):
    """Reserved for refresh token error"""
    def __init__(self):
        super().__init__(f"Unable to generate refresh token")

class CSRFTokenCreationError(DomainError):
    """Reserved for CSRF token error"""
    def __init__(self):
        super().__init__(f"Unable to generate CSRF token")