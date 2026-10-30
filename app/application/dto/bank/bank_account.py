from dataclasses import dataclass


@dataclass(frozen=True)
class BankAccountIn:
    """
    Input DTO for AddBankAccount and ChangeBankAccount use-cases.
    """
    bank_id: int
    owner_name: str
    account_prefix: str
    account_number: str
    iban: str
