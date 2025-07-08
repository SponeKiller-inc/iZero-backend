from .errors import DomainError

class SessionServiceError(DomainError):
    """Unable to generate session"""
    
class UserSessionServiceError(DomainError):
    """Reserved for generation user session"""
    def __init__(self):
        super().__init__(f"Unable to generate user session")
    
class LogSessionServiceError(DomainError):
    """Reserved for generation session log"""
    def __init__(self):
        super().__init__(f"Unable to generate session log")
               
class InicializeSessionServiceError(DomainError):
    """Reserved for session inicialization"""
    def __init__(self):
        super().__init__(f"Unable to inicialize session")

class GetSessionServiceError(DomainError):
    """Reserved for retrieving session data"""
    def __init__(self):
        super().__init__(f"Unable to retriev session data")