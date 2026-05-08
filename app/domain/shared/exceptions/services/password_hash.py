from app.domain.exceptions.errors import DomainError

class InvalidHashFormatError(DomainError):
    """Exception for invalid hash format"""
    def __init__(self, message: str = "Invalid hash format"):
        self.message = message
        super().__init__(self.message)