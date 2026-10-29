from typing import Protocol

from app.domain.users.entities.user_bank_account import UserBankAccount


class UserBankAccountRepository(Protocol):
    def get(self, user_id: int) -> UserBankAccount | None:
        """
        Get bank account assignment of the user

        Args:
            user_id: User ID

        Returns:
            UserBankAccount entity if found, else None
        """
        ...

    def save(self, user_bank_account: UserBankAccount) -> UserBankAccount:
        """
        Save new or existing bank account assignment

        Args:
            user_bank_account: UserBankAccount entity to save

        Returns:
            Saved user bank account entity
        """
        ...
