from app.domain.shared.exceptions.errors import DomainError


class BankValidationError(DomainError):
    """Bank details violate the bank rules"""
