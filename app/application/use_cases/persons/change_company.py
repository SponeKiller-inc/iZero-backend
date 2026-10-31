from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import (
    PersonAlreadyExistsError,
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
from app.application.security.authorize import authorize
from app.application.use_cases.persons.email import get_or_create_email
from app.application.use_cases.persons.phone import get_or_create_phone
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
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


class ChangeCompany:

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

    @authorize(EntityType.PERSONS, UseCase.PERSONS_CHANGE)
    def execute(self, person_id: int, dto: CompanyIn) -> PersonOut:
        """
        Change details of a company

        Args:
            person_id: Person ID
            dto: DTO carrying changed company data

        Returns:
            The changed person with its company details

        Raises:
            PersonNotFoundError: If the person or its company details do not exist
            PersonTypeChangeNotAllowedError: If the person is not a company
            PersonValidationError: If the phone is incomplete or its calling code does not
                exist, if legal form does not exist, registration number, VAT ID,
                phone number or e-mail has invalid format, name is empty, a VAT payer has no
                VAT ID or the representative does not exist or is not a natural person
            PersonAlreadyExistsError: If the registration number already identifies
                an entrepreneur or another company
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        if person.person_type != PersonType.COMPANY:
            raise PersonTypeChangeNotAllowedError("Person is not a company")

        company = self.company_repository.get_by_person_id(person_id)

        if company is None:
            raise PersonNotFoundError("Company details do not exist")

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

        other_company = self.company_repository.get_by_registration_number(registration_number.value)

        if (
            (other_company is not None and other_company.person_id != person_id)
            or self.entrepreneur_repository.get_by_registration_number(registration_number.value) is not None
        ):
            raise PersonAlreadyExistsError("Registration number already belongs to another person")

        legal_form = self.legal_form_repository.get(dto.legal_form_id)

        if legal_form is None:
            raise PersonValidationError("Legal form does not exist")

        representative = self.person_repository.get(dto.representative_person_id)

        if representative is None:
            raise PersonValidationError("Company's representative does not exist")

        try:
            company.update(
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

        return self.retrieve_person.execute(person_id)
