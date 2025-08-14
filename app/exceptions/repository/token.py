from .errors import RepositoryError

class RefreshTokenNotFoundError(RepositoryError):
    """Reserved for refresh token not found (not existing ID...)"""
    pass

class RefreshTokenCreationError(RepositoryError):
    """
    Reserved for refresh token creation 
    (not existing session id, invalid data...)
    """
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable to create refresh token"
            "session id not exists or invalid data" + err
        )


class RefreshTokenUpdateError(RepositoryError):
    """
    Reserved for refresh token update 
    (not existing session id, invalid data...)
    """
    pass

