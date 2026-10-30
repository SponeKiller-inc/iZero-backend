from typing import Self

from app.domain.bank.entities.bank import Bank
from app.domain.bank.exceptions.bank_account import BankAccountValidationError
from app.domain.bank.value_objects.bank_identification import (
    AccountNumber,
    AccountPrefix,
    Iban,
)


class BankAccount:
    """
    Represents a bank account held at a bank from the catalogue.

    Attributes:
        id: The bank account ID.
        bank_id: The ID of the bank the account is held at.
        owner_name: The name of the account owner.
        account_prefix: The domestic account prefix (zeros if the account has none).
        account_number: The domestic account number.
        iban: The account's IBAN.
    """

    def __init__(
        self,
        id: int | None,
        bank_id: int,
        owner_name: str,
        account_prefix: AccountPrefix,
        account_number: AccountNumber,
        iban: Iban,
    ):
        self.id = id
        self.bank_id = bank_id
        self.owner_name = owner_name
        self.account_prefix = account_prefix
        self.account_number = account_number
        self.iban = iban

    @classmethod
    def create(
        cls,
        bank: Bank,
        owner_name: str,
        account_prefix: AccountPrefix,
        account_number: AccountNumber,
        iban: Iban,
    ) -> Self:
        """
        Creates a new bank account.

        Args:
            bank: The bank the account is held at.
            owner_name: The name of the account owner.
            account_prefix: The domestic account prefix (zeros if the account has none).
            account_number: The domestic account number.
            iban: The account's IBAN.

        Returns:
            The newly created bank account.

        Raises:
            BankAccountValidationError: If owner_name is empty/blank or the
                IBAN is not a Czech one.
        """
        cls._validate(owner_name, iban)

        return cls(
            id=None,
            bank_id=bank.id,
            owner_name=owner_name,
            account_prefix=account_prefix,
            account_number=account_number,
            iban=iban,
        )

    def update(
        self,
        bank: Bank,
        owner_name: str,
        account_prefix: AccountPrefix,
        account_number: AccountNumber,
        iban: Iban,
    ) -> None:
        """
        Updates the bank account's details.

        Args:
            bank: The bank the account is held at.
            owner_name: The name of the account owner.
            account_prefix: The domestic account prefix (zeros if the account has none).
            account_number: The domestic account number.
            iban: The account's IBAN.

        Raises:
            BankAccountValidationError: If owner_name is empty/blank or the
                IBAN is not a Czech one.
        """
        self._validate(owner_name, iban)

        self.bank_id = bank.id
        self.owner_name = owner_name
        self.account_prefix = account_prefix
        self.account_number = account_number
        self.iban = iban

    @staticmethod
    def _validate(owner_name: str, iban: Iban) -> None:
        """
        Validates the fields shared by `create` and `update`; the IBAN format
        itself is validated by the Iban value object.

        Raises:
            BankAccountValidationError: If owner_name is empty/blank or the
                IBAN is not a Czech one, as the bank catalogue holds Czech
                banks only.
        """
        if not owner_name or not owner_name.strip():
            raise BankAccountValidationError("Bank account's owner name must be a non-empty string.")

        if iban.value[:2] != "CZ":
            raise BankAccountValidationError("IBAN does not match the bank's country.")
