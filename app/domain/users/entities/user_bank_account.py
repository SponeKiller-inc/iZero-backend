from typing import Self


class UserBankAccount:
    """
    Represents a bank account assigned to a user.

    Attributes:
        id: The assignment ID.
        user_id: The ID of the user owning the account.
        bank_account_id: The ID of the assigned bank account.
    """

    def __init__(
        self,
        id: int | None,
        user_id: int,
        bank_account_id: int,
    ):
        self.id = id
        self.user_id = user_id
        self.bank_account_id = bank_account_id

    @classmethod
    def assign(cls, user_id: int, bank_account_id: int) -> Self:
        """
        Assign bank account to user

        Args:
            user_id: The ID of the user owning the account.
            bank_account_id: The ID of the assigned bank account.

        Returns:
            The newly created assignment.
        """
        return cls(
            id=None,
            user_id=user_id,
            bank_account_id=bank_account_id,
        )
