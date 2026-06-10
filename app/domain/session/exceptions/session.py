from app.domain.shared.exceptions.errors import DomainError

class SessionExpiredError(DomainError):
    """Session has expired."""
    pass

class SessionSaveError(DomainError):
    """Session creation failed."""
    pass