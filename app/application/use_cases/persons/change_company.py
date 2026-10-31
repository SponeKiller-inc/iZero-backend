from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyIn
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import (
    PersonNotFoundError,
    PersonTypeChangeNotAllowedError,
    PersonValidationError,
)
from app.application.security.authorize import authorize
from app.application.use_cases.contacts.retrieve_email import RetrieveEmail
from app.application.use_cases.contacts.retrieve_phone import RetrievePhone
from app.application.use_cases.persons.change_natural_person import ChangeNaturalPerson
from app.application.use_cases.persons.retrieve_person import RetrievePerson
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.exceptions import person as person_errors
from app.domain.persons.repositories.company import CompanyRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.legal_form import LegalFormRepository
from app.domain.shared.value_objects.identification import (
    RegistrationNumber,
    VatNumber,
)


class ChangeCompany:

    def __init__(
        self,
        person_repository: PersonRepository,
        company_repository: CompanyRepository,
        legal_form_repository: LegalFormRepository,
        retrieve_phone: RetrievePhone,
        retrieve_email: RetrieveEmail,
        change_natural_person: ChangeNaturalPerson,
        retrieve_person: RetrievePerson,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            company_repository: Company repository
            legal_form_repository: Legal form repository
            retrieve_phone: Retrieve phone use-case
            retrieve_email: Retrieve e-mail use-case
            change_natural_person: Change natural person use-case (changes the representative)
            retrieve_person: Retrieve person use-case
        """
        self.person_repository = person_repository
        self.company_repository = company_repository
        self.legal_form_repository = legal_form_repository
        self.retrieve_phone = retrieve_phone
        self.retrieve_email = retrieve_email
        self.change_natural_person = change_natural_person
        self.retrieve_person = retrieve_person

    @authorize(EntityType.PERSONS, UseCase.PERSONS_CHANGE)
    def execute(self, person_id: int, dto: CompanyIn) -> PersonOut:
        """
        Change details of a company together with the details of its representative

        Args:
            person_id: Person ID
            dto: DTO carrying changed company data and the representative's data

        Returns:
            The changed person with its company details

        Raises:
            PersonNotFoundError: If the person or its company details do not exist
            PersonTypeChangeNotAllowedError: If the person is not a company
            PhoneValidationError: If the phone of the company or the representative is
                incomplete, its calling code does not exist or the number has invalid format
            EmailValidationError: If the e-mail address of the company or the representative
                has invalid format
            PersonValidationError: If legal form does not exist, registration number or VAT ID
                has invalid format, name is empty, a VAT payer has no VAT ID or the
                representative's details are invalid (see ChangeNaturalPerson)
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

        phone = (
            self.retrieve_phone.execute(dto.phone_prefix_id, dto.phone_number)
            if dto.phone_prefix_id is not None or dto.phone_number
            else None
        )
        email = self.retrieve_email.execute(dto.email) if dto.email else None

        legal_form = self.legal_form_repository.get(dto.legal_form_id)

        if legal_form is None:
            raise PersonValidationError("Legal form does not exist")

        self.change_natural_person.execute(company.representative_person_id, dto.representative)
        representative = self.person_repository.get(company.representative_person_id)

        try:
            company.update(
                person=person,
                name=dto.name,
                legal_form=legal_form,
                registration_number=registration_number,
                vat_number=vat_number,
                is_vat_payer=dto.is_vat_payer,
                representative=representative,
                phone_id=phone.id if phone else None,
                email_id=email.id if email else None,
            )
        except person_errors.PersonValidationError as e:
            raise PersonValidationError(str(e)) from e

        self.company_repository.save(company)

        return self.retrieve_person.execute(person_id)
