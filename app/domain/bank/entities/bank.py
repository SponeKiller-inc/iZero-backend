from typing import Self

from app.domain.bank.exceptions.bank import BankValidationError
from app.domain.bank.value_objects.bank_identification import BankCode, Swift
from app.domain.shared.value_objects.identification import RegistrationNumber


class Bank:
    """
    Represents a bank from the bank catalogue.

    Attributes:
        id: The bank ID.
        name: The bank name.
        address_id: The ID of the bank's seat address.
        code: The national bank code.
        swift: The bank's SWIFT/BIC.
        registration_number: The bank's company registration number.
        tax_number: The bank's tax number (VAT group tax number if the bank
            is a member of a VAT group).
    """

    def __init__(
        self,
        id: int | None,
        name: str,
        address_id: int,
        code: BankCode,
        swift: Swift,
        registration_number: RegistrationNumber,
        tax_number: str,
    ):
        self.id = id
        self.name = name
        self.address_id = address_id
        self.code = code
        self.swift = swift
        self.registration_number = registration_number
        self.tax_number = tax_number

    @classmethod
    def create(
        cls,
        name: str,
        address_id: int,
        code: BankCode,
        swift: Swift,
        registration_number: RegistrationNumber,
        tax_number: str,
    ) -> Self:
        """
        Creates a new bank.

        Args:
            name: The bank name.
            address_id: The ID of the bank's seat address.
            code: The national bank code.
            swift: The bank's SWIFT/BIC.
            registration_number: The bank's company registration number.
            tax_number: The bank's tax number.

        Returns:
            The newly created bank.

        Raises:
            BankValidationError: If name or tax_number is empty/blank.
        """
        cls._validate(name, tax_number)

        return cls(
            id=None,
            name=name,
            address_id=address_id,
            code=code,
            swift=swift,
            registration_number=registration_number,
            tax_number=tax_number,
        )

    def update(
        self,
        name: str,
        address_id: int,
        swift: Swift,
        registration_number: RegistrationNumber,
        tax_number: str,
    ) -> None:
        """
        Updates the bank's mutable fields; the national bank code identifies
        the bank and cannot change.

        Args:
            name: The bank name.
            address_id: The ID of the bank's seat address.
            swift: The bank's SWIFT/BIC.
            registration_number: The bank's company registration number.
            tax_number: The bank's tax number.

        Raises:
            BankValidationError: If name or tax_number is empty/blank.
        """
        self._validate(name, tax_number)

        self.name = name
        self.address_id = address_id
        self.swift = swift
        self.registration_number = registration_number
        self.tax_number = tax_number

    @staticmethod
    def _validate(name: str, tax_number: str) -> None:
        """
        Validates the fields shared by `create` and `update`.

        Raises:
            BankValidationError: If name or tax_number is empty/blank.
        """
        if not name or not name.strip():
            raise BankValidationError("Bank's name must be a non-empty string.")
        if not tax_number or not tax_number.strip():
            raise BankValidationError("Bank's tax number must be a non-empty string.")
