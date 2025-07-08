from .errors import RepositoryError

class SessionCreationError(RepositoryError):
    """Reserved for session creation (not existing user id, invalid data...)"""
    def __init__(self):
        super().__init__(
            "Unable create session invalid data or user not exist"
        )

class SessionUpdateError(RepositoryError):
    """Reserved for session update (not existing user id, invalid data...)"""
    def __init__(self):
        super().__init__("Session id does not exist")

class SessionLogCreationError(RepositoryError):
    """Reserved for session creation (not existing user id, invalid data...)"""
    def __init__(self):
        super().__init__(
            "Unable create session log invalid data or session not exist"
        )


