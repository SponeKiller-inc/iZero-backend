from app.application.constants.use_case import UseCase
from app.application.dto.person.company import CompanyOut
from app.application.dto.person.entrepreneur import EntrepreneurOut
from app.application.dto.person.natural_person import NaturalPersonOut
from app.application.dto.person.person import PersonOut
from app.application.exceptions.person import PersonNotFoundError
from app.application.ports.time_provider import TimeProvider
from app.application.security.authorize import authorize
from app.domain.persons.constants.person_type import PersonType
from app.domain.persons.repositories.company import CompanyRepository
from app.domain.persons.repositories.entrepreneur import EntrepreneurRepository
from app.domain.persons.repositories.natural_person import NaturalPersonRepository
from app.domain.persons.repositories.person import PersonRepository
from app.domain.persons.repositories.person_title import PersonTitleRepository
from app.domain.shared.constants.entity_type import EntityType
from app.domain.shared.constants.title_type import TITLE_PREFIX_NAME, TITLE_SUFFIX_NAME
from app.domain.shared.repositories.email import EmailRepository
from app.domain.shared.repositories.legal_form import LegalFormRepository
from app.domain.shared.repositories.phone import PhoneRepository
from app.domain.shared.repositories.phone_prefix import PhonePrefixRepository
from app.domain.shared.repositories.title import TitleRepository


class RetrievePerson:

    def __init__(
        self,
        person_repository: PersonRepository,
        natural_person_repository: NaturalPersonRepository,
        entrepreneur_repository: EntrepreneurRepository,
        company_repository: CompanyRepository,
        legal_form_repository: LegalFormRepository,
        title_repository: TitleRepository,
        person_title_repository: PersonTitleRepository,
        phone_repository: PhoneRepository,
        phone_prefix_repository: PhonePrefixRepository,
        email_repository: EmailRepository,
        time_provider: TimeProvider,
    ) -> None:
        """
        Initialize use-case

        Args:
            person_repository: Person repository
            natural_person_repository: Natural person repository
            entrepreneur_repository: Entrepreneur repository
            company_repository: Company repository
            legal_form_repository: Legal form repository
            title_repository: Title repository
            person_title_repository: Person title repository
            phone_repository: Phone repository
            phone_prefix_repository: Phone prefix repository
            email_repository: E-mail repository
            time_provider: Time provider
        """
        self.person_repository = person_repository
        self.natural_person_repository = natural_person_repository
        self.entrepreneur_repository = entrepreneur_repository
        self.company_repository = company_repository
        self.legal_form_repository = legal_form_repository
        self.title_repository = title_repository
        self.person_title_repository = person_title_repository
        self.phone_repository = phone_repository
        self.phone_prefix_repository = phone_prefix_repository
        self.email_repository = email_repository
        self.time_provider = time_provider

    @authorize(EntityType.PERSONS, UseCase.PERSONS_RETRIEVE)
    def execute(self, person_id: int) -> PersonOut:
        """
        Retrieve a person with the details of its type

        Args:
            person_id: Person ID

        Returns:
            The person with the details of its type

        Raises:
            PersonNotFoundError: If the person or its type-specific details do not exist
        """
        person = self.person_repository.get(person_id)

        if person is None:
            raise PersonNotFoundError("Person does not exist")

        match person.person_type:
            case PersonType.NATURAL_PERSON:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    natural_person=self._retrieve_natural_person(person.id),
                )
            case PersonType.ENTREPRENEUR:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    entrepreneur=self._retrieve_entrepreneur(person.id),
                )
            case PersonType.COMPANY:
                return PersonOut(
                    id=person.id,
                    person_type=person.person_type.value,
                    company=self._retrieve_company(person.id),
                )

    def _retrieve_natural_person(self, person_id: int) -> NaturalPersonOut:
        natural_person = self.natural_person_repository.get_by_person_id(person_id)

        if natural_person is None:
            raise PersonNotFoundError("Natural person details do not exist")

        person_titles = self.person_title_repository.get(person_id, self.time_provider.now())
        titles = self.title_repository.get_many([person_title.title_id for person_title in person_titles])

        phone_prefix_id, phone_prefix, phone_number = self._get_phone(natural_person.phone_id)

        return NaturalPersonOut(
            first_name=natural_person.first_name,
            last_name=natural_person.last_name,
            date_of_birth=natural_person.date_of_birth,
            prefix_titles=[title.name for title in titles if title.title_type == TITLE_PREFIX_NAME],
            suffix_titles=[title.name for title in titles if title.title_type == TITLE_SUFFIX_NAME],
            phone_prefix_id=phone_prefix_id,
            phone_prefix=phone_prefix,
            phone_number=phone_number,
            email=self._get_email(natural_person.email_id),
        )

    def _retrieve_entrepreneur(self, person_id: int) -> EntrepreneurOut:
        entrepreneur = self.entrepreneur_repository.get_by_person_id(person_id)

        if entrepreneur is None:
            raise PersonNotFoundError("Entrepreneur details do not exist")

        phone_prefix_id, phone_prefix, phone_number = self._get_phone(entrepreneur.phone_id)

        return EntrepreneurOut(
            name=entrepreneur.name,
            registration_number=entrepreneur.registration_number.value,
            vat_number=entrepreneur.vat_number.value if entrepreneur.vat_number else None,
            is_vat_payer=entrepreneur.is_vat_payer,
            phone_prefix_id=phone_prefix_id,
            phone_prefix=phone_prefix,
            phone_number=phone_number,
            email=self._get_email(entrepreneur.email_id),
        )

    def _retrieve_company(self, person_id: int) -> CompanyOut:
        company = self.company_repository.get_by_person_id(person_id)

        if company is None:
            raise PersonNotFoundError("Company details do not exist")

        legal_form = self.legal_form_repository.get(company.legal_form_id)

        phone_prefix_id, phone_prefix, phone_number = self._get_phone(company.phone_id)

        return CompanyOut(
            name=company.name,
            legal_form_id=company.legal_form_id,
            legal_form=legal_form.code,
            registration_number=company.registration_number.value,
            vat_number=company.vat_number.value if company.vat_number else None,
            is_vat_payer=company.is_vat_payer,
            representative_person_id=company.representative_person_id,
            phone_prefix_id=phone_prefix_id,
            phone_prefix=phone_prefix,
            phone_number=phone_number,
            email=self._get_email(company.email_id),
        )

    def _get_phone(self, phone_id: int | None) -> tuple[int | None, str | None, str | None]:
        """Returns the calling code ID, calling code and national number of the phone, all None without a phone."""
        if phone_id is None:
            return None, None, None

        phone = self.phone_repository.get(phone_id)
        phone_prefix = self.phone_prefix_repository.get(phone.phone_prefix_id)

        return phone_prefix.id, phone_prefix.prefix, phone.number.value

    def _get_email(self, email_id: int | None) -> str | None:
        """Returns the e-mail address, None without an e-mail."""
        if email_id is None:
            return None

        return self.email_repository.get(email_id).address.value
