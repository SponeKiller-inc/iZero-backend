from app.application.constants.use_case import UseCase
from app.application.dto.person.entrepreneur import EntrepreneurIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import PersonValidationError
from app.application.security.authorize import authorize
from app.application.use_cases.contacts.retrieve_email import RetrieveEmail
from app.application.use_cases.contacts.retrieve_phone import RetrievePhone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.entrepreneur import Entrepreneur
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.entrepreneur import EntrepreneurRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)


class AddEntrepreneur:

    def __init__(
        self,
        person_repository: PersonRepository,
        entrepreneur_repository: EntrepreneurRepository,
        retrieve_phone: RetrievePhone,
        retrieve_email: RetrieveEmail,
        retrieve_person: RetrievePerson,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            entrepreneur_repository: Entrepreneur repository
            retrieve_phone: Retrieve phone use-case
            retrieve_email: Retrieve e-mail use-case
            retrieve_person: Retrieve person use-case
        """
        self.person_repository = person_repository
        self.entrepreneur_repository = entrepreneur_repository
        self.retrieve_phone = retrieve_phone
        self.retrieve_email = retrieve_email
        self.retrieve_person = retrieve_person

    @authorize(EntityType.PERSONS, UseCase.PERSONS_ADD)
    def execute(self, dto: EntrepreneurIn) -> PersonOut:
        """
        Add a new entrepreneur

        Args:
            dto: DTO carrying entrepreneur data

        Returns:
            The added person with its entrepreneur details

        Raises:
            PhoneValidationError: If the phone is incomplete, its calling code does not exist
                or the number has invalid format
            EmailValidationError: If the e-mail address has invalid format
            PersonValidationError: If registration number or VAT ID has invalid format, name
                is empty or a VAT payer has no VAT ID
        """
        try:
            registration_number = RegistrationNumber(dto.registration_number)
            vat_number = VatNumber(dto.vat_number) if dto.vat_number else None
        except ValueError as e:
            raise PersonValidationError(str(e)) from e

        phone = (
            self.retrieve_phone.execute(dto.phone_prefix_id, dto.phone_number)
            if dto.phone_prefix_id is not None or dto.phone_number
            else None
        )
        email = self.retrieve_email.execute(dto.email) if dto.email else None

        person = self.person_repository.save(Person.create(PersonType.ENTREPRENEUR))

        try:
            entrepreneur = Entrepreneur.create(
                person=person,
                name=dto.name,
                registration_number=registration_number,
                vat_number=vat_number,
                is_vat_payer=dto.is_vat_payer,
                phone_id=phone.id if phone else None,
                email_id=email.id if email else None,
            )
        except person_errors.PersonValidationError as e:
            raise PersonValidationError(str(e)) from e

        self.entrepreneur_repository.save(entrepreneur)

        return self.retrieve_person.execute(person.id)
