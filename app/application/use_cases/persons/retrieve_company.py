from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.security.authorize import authorize
from app.domain.persons.repositories.company import CompanyRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.legal_form import LegalFormRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository


class RetrieveCompany:

    def __init__(
        self,
        company_repository: CompanyRepository,
        legal_form_repository: LegalFormRepository,
        phone_repository: PhoneRepository,
        phone_prefix_repository: PhonePrefixRepository,
        email_repository: EmailRepository,
    ) -> None:
        """
        Initialize use-case

        Args:
            company_repository: Company repository
            legal_form_repository: Legal form repository
            phone_repository: Phone repository
            phone_prefix_repository: Phone prefix repository
            email_repository: E-mail repository
        """
        self.company_repository = company_repository
        self.legal_form_repository = legal_form_repository
        self.phone_repository = phone_repository
        self.phone_prefix_repository = phone_prefix_repository
        self.email_repository = email_repository

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE)
    def execute(self, person_id: int) -> CompanyOut:
        """
        Retrieve the details of a company with its legal form and contacts

        Args:
            person_id: Person ID

        Returns:
            The company details

        Raises:
            PersonNotFoundError: If the company details do not exist
        """
        company = self.company_repository.get_by_person_id(person_id)

        if company is None:
            raise PersonNotFoundError("Company details do not exist")

        legal_form = self.legal_form_repository.get(company.legal_form_id)

        phone = self.phone_repository.get(company.phone_id) if company.phone_id is not None else None
        phone_prefix = self.phone_prefix_repository.get(phone.phone_prefix_id) if phone else None
        email = self.email_repository.get(company.email_id) if company.email_id is not None else None

        return CompanyOut(
            name=company.name,
            legal_form_id=company.legal_form_id,
            legal_form=legal_form.code,
            registration_number=company.registration_number.value,
            vat_number=company.vat_number.value if company.vat_number else None,
            is_vat_payer=company.is_vat_payer,
            representative_person_id=company.representative_person_id,
            phone_prefix_id=phone_prefix.id if phone_prefix else None,
            phone_prefix=phone_prefix.prefix if phone_prefix else None,
            phone_number=phone.number.value if phone else None,
            email=email.address.value if email else None,
        )
