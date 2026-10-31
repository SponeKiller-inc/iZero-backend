from typing import Self

from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions.person import PersonValidationError
from app.domain.shared.entities.email import Email
from app.domain.shared.entities.legal_form import LegalForm
from app.domain.shared.entities.phone import Phone
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)


class Company:
    """
    Represents the details of a company (legal entity).

    Attributes:
        id: The company ID.
        person_id: The ID of the person these details belong to.
        name: The company name.
        legal_form_id: The ID of the legal form.
        registration_number: The company registration number.
        vat_number: The VAT ID, if assigned.
        is_vat_payer: Whether the company is registered for VAT.
        representative_person_id: The person ID of the natural person representing the company.
        phone_id: The ID of the phone, if known.
        email_id: The ID of the e-mail, if known.
    """

    def __init__(
        self,
        id: int | None,
        person_id: int,
        name: str,
        legal_form_id: int,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        representative_person_id: int,
        phone_id: int | None,
        email_id: int | None,
    ):
        self.id = id
        self.person_id = person_id
        self.name = name
        self.legal_form_id = legal_form_id
        self.registration_number = registration_number
        self.vat_number = vat_number
        self.is_vat_payer = is_vat_payer
        self.representative_person_id = representative_person_id
        self.phone_id = phone_id
        self.email_id = email_id

    @classmethod
    def create(
        cls,
        person: Person,
        name: str,
        legal_form: LegalForm,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        representative: Person,
        phone: Phone | None,
        email: Email | None,
    ) -> Self:
        """
        Creates the details of a company.

        Args:
            person: The person these details belong to.
            name: The company name.
            legal_form: The legal form.
            registration_number: The company registration number.
            vat_number: The VAT ID, if assigned.
            is_vat_payer: Whether the company is registered for VAT.
            representative: The natural person representing the company.
            phone: The phone number, if known.
            email: The e-mail address, if known.

        Returns:
            The newly created company.

        Raises:
            PersonValidationError: If the person is not a company, name is empty/blank,
                a VAT payer has no VAT ID or the representative is not a natural person.
        """
        cls._validate(person, name, vat_number, is_vat_payer, representative)

        return cls(
            id=None,
            person_id=person.id,
            name=name,
            legal_form_id=legal_form.id,
            registration_number=registration_number,
            vat_number=vat_number,
            is_vat_payer=is_vat_payer,
            representative_person_id=representative.id,
            phone_id=phone.id if phone else None,
            email_id=email.id if email else None,
        )

    def update(
        self,
        person: Person,
        name: str,
        legal_form: LegalForm,
        registration_number: RegistrationNumber,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        representative: Person,
        phone: Phone | None,
        email: Email | None,
    ) -> None:
        """
        Updates the details of the company.

        Args:
            person: The person these details belong to.
            name: The company name.
            legal_form: The legal form.
            registration_number: The company registration number.
            vat_number: The VAT ID, if assigned.
            is_vat_payer: Whether the company is registered for VAT.
            representative: The natural person representing the company.
            phone: The phone number, if known.
            email: The e-mail address, if known.

        Raises:
            PersonValidationError: If the person is not a company, name is empty/blank,
                a VAT payer has no VAT ID or the representative is not a natural person.
        """
        self._validate(person, name, vat_number, is_vat_payer, representative)

        self.name = name
        self.legal_form_id = legal_form.id
        self.registration_number = registration_number
        self.vat_number = vat_number
        self.is_vat_payer = is_vat_payer
        self.representative_person_id = representative.id
        self.phone_id = phone.id if phone else None
        self.email_id = email.id if email else None

    @staticmethod
    def _validate(
        person: Person,
        name: str,
        vat_number: VatNumber | None,
        is_vat_payer: bool,
        representative: Person,
    ) -> None:
        """
        Validates the fields shared by `create` and `update`; the formats of the
        registration number and VAT ID are validated by their value objects.

        Raises:
            PersonValidationError: If the person is not a company (BR-2), name is
                empty/blank, a VAT payer has no VAT ID or the representative is not
                a natural person (BR-10).
        """
        if person.person_type != PersonType.COMPANY:
            raise PersonValidationError("Person is not a company.")
        if not name or not name.strip():
            raise PersonValidationError("Company's name must be a non-empty string.")
        if is_vat_payer and vat_number is None:
            raise PersonValidationError("VAT payer must have a VAT ID.")
        if representative.person_type != PersonType.NATURAL_PERSON:
            raise PersonValidationError("Company's representative must be a natural person.")
