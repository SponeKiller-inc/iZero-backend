from errors import RepositoryError

class RefreshTokenNotFoundError(RepositoryError):
    """Reserved for refresh token not found (not existing ID...)"""
    pass

class RefreshTokenCreationError(RepositoryError):
    """
    Reserved for refresh token creation 
    (not existing session id, invalid data...)
    """
    pass

class RefreshTokenUpdateError(RepositoryError):
    """
    Reserved for refresh token update 
    (not existing session id, invalid data...)
    """
    pass

