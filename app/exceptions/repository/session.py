from .errors import RepositoryError

class SessionCreationError(RepositoryError):
    """Reserved for session creation (not existing user id, invalid data...)"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable create session invalid data or user not exist" + err
        )

class SessionUpdateError(RepositoryError):
    """Reserved for session update (not existing user id, invalid data...)"""
    def __init__(self, err: str = ""):
        super().__init__("Session id does not exist" + err)

class SessionLogCreationError(RepositoryError):
    """Reserved for session creation (not existing user id, invalid data...)"""
    def __init__(self, err: str = ""):
        super().__init__(
            "Unable create session log invalid data or session not exist" + err
        )


