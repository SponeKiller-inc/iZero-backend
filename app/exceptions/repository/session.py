from errors import RepositoryError

class SessionNotFoundError(RepositoryError):
    """Reserved for  session not found (not existing ID...)"""
    pass

class SessionCreationError(RepositoryError):
    """Reserved for session creation (not existing user id, invalid data...)"""
    pass

class SessionUpdateError(RepositoryError):
    """Reserved for session update (not existing user id, invalid data...)"""
    pass

