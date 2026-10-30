from app.application.exceptions.base import ApplicationError


class BankNotFoundError(ApplicationError):
    pass

class BankAccountNotFoundError(ApplicationError):
    pass

class BankAccountAlreadyExistsError(ApplicationError):
    """User already has a bank account (BR-6)."""

class BankAccountValidationError(ApplicationError):
    """Bank account details violate the bank account rules (format of account prefix,
    account number or IBAN, empty owner name, IBAN of another country)."""
