from typing import Protocol

from app.domain.bank.entities.bank_account import BankAccount


class BankAccountRepository(Protocol):
    def get(self, bank_account_id: int) -> BankAccount | None:
        """
        Get bank account by ID

        Args:
            bank_account_id: Bank account ID

        Returns:
            BankAccount entity if found, else None
        """
        ...

    def save(self, bank_account: BankAccount) -> BankAccount:
        """
        Save new or existing bank account

        Args:
            bank_account: BankAccount entity to save

        Returns:
            Saved bank account entity
        """
        ...
