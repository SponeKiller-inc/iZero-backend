from dataclasses import dataclass

from app.application.dto.bank.bank_account import BankAccountIn


@dataclass(frozen=True)
class UserBankAccountIn:
    """
    Input DTO for AddUserBankAccount and ChangeUserBankAccount use-cases.
    """
    user_id: int
    bank_account: BankAccountIn
