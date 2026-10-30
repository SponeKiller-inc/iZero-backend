from app.domain.shared.exceptions.errors import DomainError


class BankAccountValidationError(DomainError):
    """Bank account details violate the bank account rules"""
