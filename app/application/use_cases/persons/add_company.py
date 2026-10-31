from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyIn
from app.application.dto.person.retrieve_person import RetrievePersonOut
from app.application.exceptions.person import (
    PersonAlreadyExistsError,
    PersonValidationError,
)
from app.application.security.authorize import authorize
from app.application.use_cases.persons.email import get_or_create_email
from app.application.use_cases.persons.phone import get_or_create_phone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.entities.company import Company
from app.domain.persons.entities.person import Person
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.company import CompanyRepository
from app.domain.persons.repositories.entrepreneur import EntrepreneurRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.legal_form import LegalFormRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)


class AddCompany:

    def __init__(
        self,
        person_repository: PersonRepository,
        entrepreneur_repository: EntrepreneurRepository,
        company_repository: CompanyRepository,
        legal_form_repository: LegalFormRepository,
        phone_prefix_repository: PhonePrefixRepository,
        phone_repository: PhoneRepository,
        email_repository: EmailRepository,
        retrieve_person: RetrievePerson,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            entrepreneur_repository: Entrepreneur repository
            company_repository: Company repository
            legal_form_repository: Legal form repository
            phone_prefix_repository: Phone prefix repository
            phone_repository: Phone repository
            email_repository: E-mail repository
            retrieve_person: Retrieve person use-case
        """
        self.person_repository = person_repository
        self.entrepreneur_repository = entrepreneur_repository
        self.company_repository = company_repository
        self.legal_form_repository = legal_form_repository
        self.phone_prefix_repository = phone_prefix_repository
        self.phone_repository = phone_repository
        self.email_repository = email_repository
        self.retrieve_person = retrieve_person

    @authorize(EntityType.PERSONS, UseCase.PERSONS_ADD)
    def execute(self, dto: CompanyIn) -> RetrievePersonOut:
        """
        Add a new company

        Args:
            dto: DTO carrying company data

        Returns:
            The added person with its company details

        Raises:
            PersonValidationError: If the phone is incomplete or its calling code does not
                exist, if legal form does not exist, registration number, VAT ID,
                phone number or e-mail has invalid format, name is empty, a VAT payer has no
                VAT ID or the representative does not exist or is not a natural person
            PersonAlreadyExistsError: If the registration number already identifies
                an entrepreneur or a company
        """
        try:
            registration_number = RegistrationNumber(dto.registration_number)
            vat_number = VatNumber(dto.vat_number) if dto.vat_number else None
        except ValueError as e:
            raise PersonValidationError(str(e)) from e

        phone = get_or_create_phone(
            self.phone_prefix_repository,
            self.phone_repository,
            dto.phone_prefix_id,
            dto.phone_number,
        )
        email = get_or_create_email(self.email_repository, dto.email)

        if (
            self.entrepreneur_repository.get_by_registration_number(registration_number.value) is not None
            or self.company_repository.get_by_registration_number(registration_number.value) is not None
        ):
            raise PersonAlreadyExistsError("Registration number already belongs to another person")

        legal_form = self.legal_form_repository.get(dto.legal_form_id)

        if legal_form is None:
            raise PersonValidationError("Legal form does not exist")

        representative = self.person_repository.get(dto.representative_person_id)

        if representative is None:
            raise PersonValidationError("Company's representative does not exist")

        person = self.person_repository.save(Person.create(PersonType.COMPANY))

        try:
            company = Company.create(
                person=person,
                name=dto.name,
                legal_form=legal_form,
                registration_number=registration_number,
                vat_number=vat_number,
                is_vat_payer=dto.is_vat_payer,
                representative=representative,
                phone=phone,
                email=email,
            )
        except person_errors.PersonValidationError as e:
            raise PersonValidationError(str(e)) from e

        self.company_repository.save(company)

        return self.retrieve_person.execute(person.id)
