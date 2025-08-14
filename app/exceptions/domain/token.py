from .errors import DomainError

class TokenServiceError(DomainError):
    """Unable to generate token"""
    
class AccessTokenServiceError(DomainError):
    """Reserved for access token error"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to generate access token" + err)
    
class RefreshTokenServiceError(DomainError):
    """Reserved for refresh token error"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to generate refresh token" + err)

class CSRFTokenCreationError(DomainError):
    """Reserved for CSRF token error"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to generate CSRF token" + err)