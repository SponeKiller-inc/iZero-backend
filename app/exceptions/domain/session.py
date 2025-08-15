from .errors import DomainError

class SessionServiceError(DomainError):
    """Unable to generate session"""
    
class UserSessionServiceError(DomainError):
    """Reserved for generation user session"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to generate user session" + err)
    
class LogSessionServiceError(DomainError):
    """Reserved for generation session log"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to generate session log" + err)
               
class InicializeSessionServiceError(DomainError):
    """Reserved for session inicialization"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to inicialize session" + err)

class GetSessionServiceError(DomainError):
    """Reserved for retrieving session data"""
    def __init__(self, err: str = ""):
        super().__init__("Unable to retriev session data" + err)