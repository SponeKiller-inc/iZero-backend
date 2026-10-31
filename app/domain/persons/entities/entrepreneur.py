from typing import Self

from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions.person import PersonValidationError
from app.domain.shared.entities.email import Email
from app.domain.shared.entities.phone import Phone
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)


class Entrepreneur:
    """
    Represents the details of an entrepreneur (self-employed person, sole trader).

    Attributes:
        id: The entrepreneur ID.
        person_id: The ID of the person these details belong to.
        name: The trade name.
        registration_number: The company registration number.
        vat_number: The VAT ID, if assigned.
        is_vat_payer: Whether the entrepreneur is registered for VAT.
        phone_id: The ID of the phone, if known.
        email_id: The ID of the e-mail, if known.
    """

    def __init__(
        self,
        id: int | None,
        person_id: int,
        name: str,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        phone_id: int | None,
        email_id: int | None,
    ):
        self.id = id
        self.person_id = person_id
        self.name = name
        self.registration_number = registration_number
        self.vat_number = vat_number
        self.is_vat_payer = is_vat_payer
        self.phone_id = phone_id
        self.email_id = email_id

    @classmethod
    def create(
        cls,
        person: Person,
        name: str,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        phone: Phone | None,
        email: Email | None,
    ) -> Self:
        """
        Creates the details of an entrepreneur.

        Args:
            person: The person these details belong to.
            name: The trade name.
            registration_number: The company registration number.
            vat_number: The VAT ID , if assigned.
            is_vat_payer: Whether the entrepreneur is registered for VAT.
            phone: The phone number, if known.
            email: The e-mail address, if known.

        Returns:
            The newly created entrepreneur.

        Raises:
            PersonValidationError: If the person is not an entrepreneur, name is
                empty/blank or a VAT payer has no VAT ID.
        """
        cls._validate(person, name, vat_number, is_vat_payer)

        return cls(
            id=None,
            person_id=person.id,
            name=name,
            registration_number=registration_number,
            vat_number=vat_number,
            is_vat_payer=is_vat_payer,
            phone_id=phone.id if phone else None,
            email_id=email.id if email else None,
        )

    def update(
        self,
        person: Person,
        name: str,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        phone: Phone | None,
        email: Email | None,
    ) -> None:
        """
        Updates the details of the entrepreneur.

        Args:
            person: The person these details belong to.
            name: The trade name.
            registration_number: The company registration number.
            vat_number: The VAT ID, if assigned.
            is_vat_payer: Whether the entrepreneur is registered for VAT.
            phone: The phone number, if known.
            email: The e-mail address, if known.

        Raises:
            PersonValidationError: If the person is not an entrepreneur, name is
                empty/blank or a VAT payer has no VAT ID.
        """
        self._validate(person, name, vat_number, is_vat_payer)

        self.name = name
        self.registration_number = registration_number
        self.vat_number = vat_number
        self.is_vat_payer = is_vat_payer
        self.phone_id = phone.id if phone else None
        self.email_id = email.id if email else None

    @staticmethod
    def _validate(person: Person, name: str, vat_number: VatNumber | None, is_vat_payer: bool) -> None:
        """
        Validates the fields shared by `create` and `update`; the formats of the
        registration number and VAT ID are validated by their value objects.

        Raises:
            PersonValidationError: If the person is not an entrepreneur (BR-2), name is
                empty/blank or a VAT payer has no VAT ID.
        """
        if person.person_type != PersonType.ENTREPRENEUR:
            raise PersonValidationError("Person is not an entrepreneur.")
        if not name or not name.strip():
            raise PersonValidationError("Entrepreneur's name must be a non-empty string.")
        if is_vat_payer and vat_number is None:
            raise PersonValidationError("VAT payer must have a VAT ID.")
