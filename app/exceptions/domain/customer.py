from app.exceptions.domain.errors import DomainError

class CustomerNotFoundError(DomainError):
    """Reserved for not found customer"""
    def __init__(self, err: str = ""):
        super().__init__("Customer not found" + err)